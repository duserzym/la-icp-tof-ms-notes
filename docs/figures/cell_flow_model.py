"""Computed gas paths and residence times for a schematic two-volume laser ablation cell.

Run from this folder:  python3 cell_flow_model.py           (about 2-3 min on a laptop)
                       python3 cell_flow_model.py --sweep   (design sensitivity table, ~2 min on 7+ cores)
Needs  : numpy, scipy, pyamg, matplotlib  (pip install numpy scipy pyamg matplotlib)
Outputs: cell-flow-paths.json        streamlines, particle paths, residence-time curves, stats
         13-cell-residence-time.png  residence-time distributions at the cell exit
         Laser-3D.html               the same JSON is embedded between the CELLFLOW markers

What is modelled (all numbers are stated assumptions, not manufacturer CAD or a measured cell):
  * Steady, laminar, incompressible He at 25 C and 1 atm on a uniform staggered (MAC) grid.
    Momentum: third-order upwind advection + central diffusion, Heun steps in pseudo-time with a
    local time step; pressure projection solved with algebraic multigrid (pyamg). The local time
    step changes the path to steady state, not the steady solution itself.
  * Geometry is symmetric about z = 0, so each solve uses the half domain z >= 0 with a
    symmetry plane; particles reflect off that plane.
  * Two separate solves, as in a two-volume cell: (1) the inner cup with its He jet, exit tube and
    the surrounding gas (open, p = 0 boundaries) on a 0.2 mm grid; (2) the outer chamber flush on a
    2 mm grid with the cup and its window column as a solid obstacle. A third solve uses the same
    outer box as a conventional single-volume cell (carrier enters and leaves the big chamber).
  * Particles: released at rest relative to the gas, uniformly in a hemisphere of radius
    PLUME_R over the ablation site (the plume after it has stopped in the gas). Stokes drag with
    the Cunningham slip correction in He plus gravity; massless tracers follow the gas.
    Brownian motion is left out: for 0.1 um particles in He, D ~ 1.5e-9 m2/s, i.e. ~2 um in 1 ms.
  * Residence time = time from release to crossing a plane in the exit tube EXIT_PLANE mm from the
    cup wall (two-volume) or to leaving through the outlet (conventional). This is the cell alone:
    transfer tubing, the injector and the plasma add their own spread, so the published two-volume +
    DCI widths (1.5 / 3.2 / 4.9 ms at 50 / 10 / 1 %) are an upper bound to compare with, not a target.
"""
import json
import pathlib
import re
import time

import numpy as np
import pyamg
import scipy.sparse as sp
from scipy.ndimage import map_coordinates, maximum_filter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
RNG = np.random.default_rng(20261016)

# ------------------------------------------------------------------ gas and particles
T_K, P_PA = 298.15, 101325.0
MU_HE = 1.98e-5                                   # Pa s, He at 25 C
RHO_HE = P_PA * 4.0026e-3 / (8.314462 * T_K)      # kg/m3, ideal gas
NU_HE = MU_HE / RHO_HE                            # m2/s
M_HE = 4.0026e-3 / 6.02214076e23
MFP_HE = MU_HE / P_PA * np.sqrt(np.pi * 1.380649e-23 * T_K / (2 * M_HE))   # m, ~0.19 um
RHO_P = 3000.0                                    # kg/m3, silicate/oxide particle
G = 9.81

def relaxation_time(d):
    """Stokes relaxation time (s) of a sphere of diameter d (m) in He, with Cunningham slip."""
    if d == 0:
        return 0.0
    kn = 2 * MFP_HE / d
    cc = 1 + kn * (1.257 + 0.4 * np.exp(-1.1 / kn))
    return RHO_P * d * d * cc / (18 * MU_HE)

SIZES = [("massless", 0.0), ("0.1 um", 0.1e-6), ("1 um", 1.0e-6)]

# ------------------------------------------------------------------ geometry and flows (mm, L/min)
GEOM = dict(
    chamber=[100.0, 22.0, 70.0],      # outer chamber x, y (height), z
    cup_r=5.0, cup_wall=1.0, cup_h=1.5, cup_lid=1.0, gap=0.4,   # inner cup over the site
    jet_d=0.6, jet_w=3.0, jet_y=0.5, jet_aim_y=0.5,   # He jet nozzle: height (or ID if round), width,
                                                       # height at the cup wall, height it aims at over the site
    exit_d=1.0, exit_y=0.8, exit_angle=20.0,   # exit tube ID, entry height, upward angle (deg)
    tube_wall=0.3,
    port_d=4.0, port_y=11.0,          # outer chamber inlet/outlet ports (both end walls)
)
Q_JET = 0.8        # L/min He through the cup jet (= flow leaving through the exit tube)
Q_DRAW = 0.0       # L/min extra drawn out of the exit tube from the surrounding gas through the rim gap
Q_FLUSH = 0.5      # L/min He outer-chamber flush (two-volume case)
Q_CONV = 1.0       # L/min He carrier through a conventional single-volume cell
PLUME_R = 0.75     # mm, radius of the stopped plume hemisphere
EXIT_PLANE = 2.5   # mm along the exit tube axis from its entry at the cup wall
H_CUP, H_OUT = 0.2, 2.0   # grid spacing (mm) for the cup and outer-chamber solves
N_PART = 20000     # particles per size class in the cup
N_PART_CONV = 4000 # particles per size class in the conventional cell
T_MAX_CUP, T_MAX_CONV = 0.06, 60.0   # s, tracking horizon


# ================================================================== staggered-grid solver
def _ghost(a, ax, lo, hi):
    """Add two ghost layers along axis ax. Modes: edge | even | odd | oddface."""
    a = np.moveaxis(a, ax, 0)
    def g(mode, e0, e1, e2):
        return {"edge": (e0, e0), "even": (e0, e1), "odd": (-e0, -e1),
                "oddface": (2 * e0 - e1, 2 * e0 - e2)}[mode]
    l1, l2 = g(lo, a[0], a[1], a[2])
    h1, h2 = g(hi, a[-1], a[-2], a[-3])
    out = np.concatenate([l2[None], l1[None], a, h1[None], h2[None]])
    return np.moveaxis(out, 0, ax)


class Flow:
    """Steady incompressible Navier-Stokes on a masked MAC grid (units: m, s)."""

    def __init__(self, solid, h, origin, sides, nu=NU_HE):
        self.solid, self.h, self.o, self.nu = solid, h, np.asarray(origin, float), nu
        self.n = solid.shape
        self.sides = sides            # {(axis, 0|1): 'wall' | 'sym' | 'open'}
        fluid = ~solid
        self.active, self.open, self.fixed, self.val, self.vel = [], [], [], [], []
        for ax in range(3):
            fp = np.concatenate([np.zeros_like(np.take(fluid, [0], ax)), fluid,
                                 np.zeros_like(np.take(fluid, [0], ax))], axis=ax)
            lo = np.take(fp, range(0, self.n[ax] + 1), ax)
            hi = np.take(fp, range(1, self.n[ax] + 2), ax)
            act = lo & hi
            opn = np.zeros_like(act)
            for side, idx, cell in ((0, 0, hi), (1, self.n[ax], lo)):
                if sides[(ax, side)] == "open":
                    sl = [slice(None)] * 3
                    sl[ax] = idx
                    opn[tuple(sl)] = np.take(cell, idx, ax)
            self.active.append(act)
            self.open.append(opn)
            self.fixed.append(~act & ~opn)
            self.val.append(np.zeros(act.shape))
            self.vel.append(np.zeros(act.shape))
        self.fluid = fluid
        self.p = np.zeros(fluid.sum())

    def set_boundary(self, ax, side, mask2d, value, kind="fixed"):
        """Inflow/outflow on a domain side: 'fixed' normal velocity or 'open' (p = 0)."""
        sl = [slice(None)] * 3
        sl[ax] = 0 if side == 0 else self.n[ax]
        sl = tuple(sl)
        m = mask2d & np.take(self.fluid, 0 if side == 0 else self.n[ax] - 1, ax)
        self.fixed[ax][sl][m] = kind == "fixed"
        self.open[ax][sl][m] = kind == "open"
        self.val[ax][sl][m] = value[m] if np.ndim(value) else value

    # -------------------------------------------------------------- operators
    def _modes(self, comp, ax, side):
        t = self.sides[(ax, side)]
        if t == "open":
            return "edge"
        if comp == ax:
            return "oddface"
        return "odd" if t == "wall" else "even"

    def pad(self, comp, a):
        for ax in range(3):
            a = _ghost(a, ax, self._modes(comp, ax, 0), self._modes(comp, ax, 1))
        return a

    def rhs(self, vel):
        """-(u.grad)u + nu lap u on every face of every component."""
        h, n = self.h, self.n
        P = [self.pad(c, vel[c]) for c in range(3)]
        out = []
        for c in range(3):
            F = P[c]
            shp = vel[c].shape
            core = tuple(slice(2, 2 + s) for s in shp)
            adv = np.zeros(shp)
            lap = np.zeros(shp)
            for a in range(3):
                if a == c:
                    A = vel[c]
                else:   # component a averaged onto the faces of component c
                    acc = 0
                    for da in (0, 1):
                        for dc in (-1, 0):
                            sl = []
                            for k in range(3):
                                if k == a:
                                    sl.append(slice(2 + da, 2 + da + n[k]))
                                elif k == c:
                                    sl.append(slice(2 + dc, 2 + dc + n[k] + 1))
                                else:
                                    sl.append(slice(2, 2 + n[k]))
                            acc = acc + P[a][tuple(sl)]
                    A = 0.25 * acc
                def s(m):
                    sl = list(core)
                    sl[a] = slice(2 + m, 2 + m + shp[a])
                    return F[tuple(sl)]
                f0, fp1, fm1, fp2, fm2 = s(0), s(1), s(-1), s(2), s(-2)
                dp = (2 * fp1 + 3 * f0 - 6 * fm1 + fm2) / (6 * h)
                dm = (-fp2 + 6 * fp1 - 3 * f0 - 2 * fm1) / (6 * h)
                adv += np.where(A > 0, A * dp, A * dm)
                lap += (fp1 - 2 * f0 + fm1) / (h * h)
            out.append(-adv + self.nu * lap)
        return out

    def apply_bc(self, vel):
        for ax in range(3):
            v = vel[ax]
            v[self.fixed[ax]] = self.val[ax][self.fixed[ax]]
            if self.open[ax].any():
                n = self.n[ax]
                for idx, nb in ((0, 1), (n, n - 1)):
                    sl = [slice(None)] * 3
                    sl[ax] = idx
                    sn = list(sl)
                    sn[ax] = nb
                    m = self.open[ax][tuple(sl)]
                    v[tuple(sl)][m] = v[tuple(sn)][m]
        return vel

    def local_dt(self, vel, floor=1.0, cfl=0.35, dfac=0.15):
        """Pseudo-time step per face: local CFL and diffusion limits, speed floored at floor*|u|max."""
        speed = np.zeros(self.n)
        for ax in range(3):
            v = np.abs(vel[ax])
            speed = np.maximum(speed, np.maximum(np.take(v, range(self.n[ax]), ax),
                                                 np.take(v, range(1, self.n[ax] + 1), ax)))
        speed = maximum_filter(speed, size=7, mode="nearest")
        speed = np.maximum(speed, floor * speed.max())
        dtc = np.minimum(cfl * self.h / np.maximum(speed, 1e-9), dfac * self.h ** 2 / self.nu)
        dts = []   # face time step: min of the two neighbouring cells
        for ax in range(3):
            p = np.concatenate([np.take(dtc, [0], ax), dtc, np.take(dtc, [-1], ax)], axis=ax)
            dts.append(np.minimum(np.take(p, range(0, self.n[ax] + 1), ax),
                                  np.take(p, range(1, self.n[ax] + 2), ax)))
        return dts

    def build_poisson(self, dts):
        """Assemble div(dt grad p) on fluid cells; returns an AMG solver."""
        h, n = self.h, self.n
        idx = -np.ones(n, int)
        idx[self.fluid] = np.arange(self.fluid.sum())
        rows, cols, vals = [], [], []
        diag = np.zeros(self.fluid.sum())
        for ax in range(3):
            coef = dts[ax] / h ** 2
            # interior active faces
            a = self.active[ax]
            dummy = -np.ones_like(np.take(idx, [0], ax))
            ip = np.concatenate([dummy, idx, dummy], axis=ax)
            lo = np.take(ip, range(0, n[ax] + 1), ax)      # cell below face f is f-1
            hi = np.take(ip, range(1, n[ax] + 2), ax)      # cell above face f is f
            il, ih, cf = lo[a], hi[a], coef[a]
            rows += [il, ih]
            cols += [ih, il]
            vals += [cf, cf]
            np.add.at(diag, il, -cf)
            np.add.at(diag, ih, -cf)
            o = self.open[ax]
            if o.any():
                sl0 = [slice(None)] * 3
                sl0[ax] = 0
                sl1 = [slice(None)] * 3
                sl1[ax] = n[ax]
                for sl, ci in ((tuple(sl0), np.take(idx, 0, ax)), (tuple(sl1), np.take(idx, n[ax] - 1, ax))):
                    m = o[sl]
                    np.add.at(diag, ci[m], -coef[sl][m])
        rows.append(np.arange(diag.size))
        cols.append(np.arange(diag.size))
        vals.append(diag)
        A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(diag.size, diag.size))
        self.idx = idx
        np.random.seed(0)    # pyamg draws a random start vector during setup; fix it for repeatable output
        return pyamg.smoothed_aggregation_solver(-A, max_coarse=200)

    def divergence(self, vel):
        h = self.h
        d = sum(np.diff(vel[ax], axis=ax) for ax in range(3)) / h
        return d[self.fluid]

    def project(self, vel, dts, amg, tol=1e-7):
        rhs = self.divergence(vel)
        self.p = amg.solve(-rhs, x0=self.p, tol=tol, accel="cg", maxiter=300)   # (-A) p = -div u*
        pf = np.zeros(self.n)
        pf[self.fluid] = self.p
        h = self.h
        for ax in range(3):
            n = self.n[ax]
            pp = np.concatenate([np.zeros_like(np.take(pf, [0], ax)), pf,
                                 np.zeros_like(np.take(pf, [0], ax))], axis=ax)
            grad = np.diff(pp, axis=ax) / h      # (p_hi - p_lo)/h on every face, ghost p = 0
            m = self.active[ax] | self.open[ax]
            vel[ax][m] -= dts[ax][m] * grad[m]
        return vel

    def solve(self, steps=3000, warm=500, rebuild=25, floor=0.1, tol=2e-5, label=""):
        """Global time step for `warm` steps (lets the jet form), then local pseudo-time steps."""
        vel = [v.copy() for v in self.vel]
        self.apply_bc(vel)
        dts = self.local_dt([np.maximum(np.abs(self.val[a]).max(), 1e-3) * np.ones_like(vel[a])
                             for a in range(3)])
        amg = self.build_poisson(dts)
        vel = self.project(vel, dts, amg)
        t0 = time.time()
        for it in range(1, steps + 1):
            if it % rebuild == 0:
                dts = self.local_dt(vel, floor=1.0 if it < warm else floor)
                amg = self.build_poisson(dts)
            r0 = self.rhs(vel)
            v1 = self.apply_bc([vel[a] + np.where(self.active[a], dts[a] * r0[a], 0) for a in range(3)])
            r1 = self.rhs(v1)
            new = self.apply_bc([vel[a] + np.where(self.active[a], 0.5 * dts[a] * (r0[a] + r1[a]), 0)
                                 for a in range(3)])
            new = self.project(new, dts, amg, tol=1e-6)
            umax = max(np.abs(v).max() for v in new)
            change = max(np.abs(new[a] - vel[a]).max() for a in range(3)) / umax
            vel = new
            if it % 200 == 0:
                print(f"  {label} step {it:5d}  max rel. change {change:.2e}  |u|max {umax:.3g} m/s"
                      f"  ({time.time() - t0:.0f} s)")
            if not np.isfinite(umax):
                raise FloatingPointError(f"{label}: solution diverged at step {it}")
            if change < tol and it > warm:
                break
        self.vel = self.project(vel, dts, amg, tol=1e-10)
        print(f"  {label} stopped after {it} steps, max rel. change {change:.1e}, "
              f"max |div u|·h/|u|max = {np.abs(self.divergence(self.vel)).max() * self.h / umax:.1e}")
        self.padded = [self.pad(c, self.vel[c]) for c in range(3)]
        return self

    # -------------------------------------------------------------- interpolation
    def velocity(self, x):
        """Trilinear velocity (m/s) at points x (N,3, metres, half domain z >= 0)."""
        out = np.empty_like(x)
        for c in range(3):
            coords = []
            for k in range(3):
                q = (x[:, k] - self.o[k]) / self.h + 2.0
                if k != c:
                    q = q - 0.5
                coords.append(q)
            out[:, c] = map_coordinates(self.padded[c], coords, order=1, mode="nearest")
        return out

    def cell_of(self, x):
        ijk = np.floor((x - self.o) / self.h).astype(int)
        inside = np.all((ijk >= 0) & (ijk < np.array(self.n)), axis=1)
        return ijk, inside

    def is_solid(self, x):
        ijk, inside = self.cell_of(x)
        s = np.zeros(len(x), bool)
        s[inside] = self.solid[tuple(ijk[inside].T)]
        return s, inside


# ================================================================== geometry builders
def centers(n, h, o):
    return [o[k] + (np.arange(n[k]) + 0.5) * h for k in range(3)]


def tube_masks(X, Y, Z, p0, d, r, wall):
    """Distance to an axis through p0 along unit vector d, and axial coordinate s."""
    dx, dy, dz = X - p0[0], Y - p0[1], Z - p0[2]
    s = dx * d[0] + dy * d[1] + dz * d[2]
    dist = np.sqrt(np.maximum(dx * dx + dy * dy + dz * dz - s * s, 0))
    return s, dist


def jet_axes(g):
    """Nozzle exit point/direction (aimed at the ablation site) and exit-tube entry/direction, mm."""
    pn = np.array([-g["cup_r"], g["jet_y"], 0.0])
    dn = np.array([0.0, g["jet_aim_y"], 0.0]) - pn
    dn /= np.linalg.norm(dn)
    a = np.radians(g["exit_angle"])
    pe = np.array([g["cup_r"], g["exit_y"], 0.0])
    de = np.array([np.cos(a), np.sin(a), 0.0])
    return pn, dn, pe, de


def build_cup(h=H_CUP, g=GEOM, q_jet=Q_JET, q_draw=Q_DRAW):
    """Cup domain (mm): x in [-9, 9], y in [0, 5], z in [0, 7]; returns Flow plus metadata."""
    lo, hi = np.array([-9.0, 0.0, 0.0]), np.array([9.0, 5.0, 7.0])
    n = tuple(np.round((hi - lo) / h).astype(int))
    X, Y, Z = np.meshgrid(*centers(n, h, lo), indexing="ij")
    R = np.hypot(X, Z)
    rc, rw = g["cup_r"], g["cup_r"] + g["cup_wall"]
    solid = (R < rw) & (Y >= g["cup_h"])                          # lid/window and column above
    solid |= (R >= rc) & (R < rw) & (Y >= g["gap"])               # cup side wall, gap below the rim
    pn, dn, pe, de = jet_axes(g)
    sj, rj = tube_masks(X, Y, Z, pn, dn, 0, 0)
    se, re_ = tube_masks(X, Y, Z, pe, de, 0, 0)
    tw = g["tube_wall"]
    a, b = g["jet_d"] / 2, g.get("jet_w", g["jet_d"]) / 2
    if b > a:   # flat slot nozzle, horizontal: jet_d tall, jet_w wide
        dy, dz = np.abs(Y - g["jet_y"]), np.abs(Z)
        jet_in = (dy < a) & (dz < b) & (X <= -rc + 1.0)
        solid |= (dy < a + tw) & (dz < b + tw) & ~jet_in & (X <= -rc) & (R >= rc)
        jet_prof = (1 - (dy / a) ** 2) * (1 - (dz / b) ** 2)
    else:       # round nozzle along the aimed axis
        jet_in = (rj < a) & (sj <= 1.0)
        solid |= (rj >= a) & (rj < a + tw) & (sj <= 0) & (R >= rc)
        jet_prof = 1 - (rj / a) ** 2
    solid |= (re_ >= g["exit_d"] / 2) & (re_ < g["exit_d"] / 2 + tw) & (se >= 0) & (R >= rc)
    ex_in = (re_ < g["exit_d"] / 2) & (se >= -1.0)
    solid &= ~(jet_in | ex_in)
    sides = {(0, 0): "open", (0, 1): "open", (1, 0): "wall", (1, 1): "open",
             (2, 0): "sym", (2, 1): "open"}
    f = Flow(solid, h * 1e-3, lo * 1e-3, sides)
    ex_prof = 1 - (re_ / (g["exit_d"] / 2)) ** 2
    for side, inside, pr, Q in ((0, jet_in, jet_prof, q_jet), (1, ex_in, ex_prof, q_jet + q_draw)):
        idx = 0 if side == 0 else n[0] - 1      # parabolic inflow / fixed outflow profiles
        m = inside[idx]
        prof = np.where(m, np.maximum(pr[idx], 0.05), 0)
        q_half = Q / 60000 / 2
        val = prof / (prof.sum() * (h * 1e-3) ** 2) * q_half
        f.set_boundary(0, side, m, val, "fixed")
    meta = dict(lo=lo, hi=hi, pn=pn, dn=dn, pe=pe, de=de)
    return f, meta


def build_outer(with_cup, h=H_OUT, g=GEOM, Q=Q_FLUSH):
    L, Hc, W = g["chamber"]
    lo, hi = np.array([-L / 2, 0.0, 0.0]), np.array([L / 2, Hc, W / 2])
    n = tuple(np.round((hi - lo) / h).astype(int))
    X, Y, Z = np.meshgrid(*centers(n, h, lo), indexing="ij")
    solid = np.zeros(n, bool)
    if with_cup:
        solid |= np.hypot(X, Z) < g["cup_r"] + g["cup_wall"]   # cup + window column, floor to lid
    sides = {(a, s): "wall" for a in range(3) for s in (0, 1)}
    sides[(2, 0)] = "sym"
    f = Flow(solid, h * 1e-3, lo * 1e-3, sides)
    yc, zc = centers(n, h, lo)[1], centers(n, h, lo)[2]
    YY, ZZ = np.meshgrid(yc, zc, indexing="ij")
    port = np.hypot(YY - g["port_y"], ZZ) < (g["port_d"] + h) / 2   # staircase port, >= nominal size
    if port.sum() == 0:
        raise ValueError("port not resolved")
    val = np.where(port, Q / 60000 / 2 / (port.sum() * (h * 1e-3) ** 2), 0)
    f.set_boundary(0, 0, port, val, "fixed")
    f.set_boundary(0, 1, port, 0.0, "open")
    return f, dict(lo=lo, hi=hi)


# ================================================================== particles
def release(n, r=PLUME_R):
    """Uniform points in the upper hemisphere of radius r (mm) on the floor at the site, z >= 0."""
    u = RNG.random(n) ** (1 / 3) * r
    cth = RNG.random(n)
    phi = RNG.random(n) * np.pi
    sth = np.sqrt(1 - cth ** 2)
    pts = np.stack([u * sth * np.cos(phi), u * cth, u * sth * np.sin(phi)], 1)
    pts[:, 1] = np.maximum(pts[:, 1], 0.02)
    return pts * 1e-3


def track(flow, x0, tau, t_max, exit_test, open_exit=None, record=0, move=0.25, dt_max=None):
    """Integrate N particles; returns exit times (nan if not exited) and fates, plus recorded paths.

    exit_test(x) -> bool array, True when the particle has crossed the exit plane.
    Fates: 0 still in cell at t_max, 1 exited, 2 deposited on a wall (particles with mass stick),
           3 left through an open boundary into the surrounding chamber. Massless tracers that step
           into a staircase wall cell are put back into the gas; `touched` flags any wall contact.
    """
    N = len(x0)
    x = x0.copy()
    v = flow.velocity(x)
    t = np.zeros(N)
    fate = np.zeros(N, int)
    t_exit = np.full(N, np.nan)
    alive = np.ones(N, bool)
    touched = np.zeros(N, bool)
    hmin = flow.h
    dt_max = dt_max or t_max / 2000
    paths = [[(0.0, *x0[i])] for i in range(record)]
    tg = np.array([0, -G, 0]) * tau
    while alive.any():
        ia = np.flatnonzero(alive)
        xa, va = x[ia], v[ia]
        ua = flow.velocity(xa)
        sp_ = np.linalg.norm(np.maximum(np.abs(ua), np.abs(va)), axis=1)
        dt = np.minimum(move * hmin / np.maximum(sp_, 1e-9), dt_max)
        dt = np.minimum(dt, t_max - t[ia] + 1e-12)
        if tau == 0:
            xm = xa + 0.5 * dt[:, None] * ua
            xm[:, 2] = np.abs(xm[:, 2])
            um = flow.velocity(xm)
            xn = xa + dt[:, None] * um
            vn = um
        else:
            xm = xa + 0.5 * dt[:, None] * va
            xm[:, 2] = np.abs(xm[:, 2])
            um = flow.velocity(xm) + tg
            e = np.exp(-dt / tau)[:, None]
            vn = um + (va - um) * e
            xn = xa + um * dt[:, None] + (va - um) * tau * (1 - e)
        refl = xn[:, 2] < 0
        xn[refl, 2] *= -1
        vn[refl, 2] *= -1
        tn = t[ia] + dt
        done_exit = exit_test(xn)
        solid, inside = flow.is_solid(xn)
        out_open = open_exit(xn) & ~done_exit if open_exit is not None else np.zeros(len(xn), bool)
        hit = (solid | (~inside & ~done_exit)) & ~out_open & ~done_exit
        touched[ia[hit]] = True
        if tau > 0:     # particles with mass stick where they touch a wall
            fate[ia[hit]] = 2
        elif hit.any():  # tracers cannot leave the gas: step back towards the last fluid-cell centre
            ijk, _ = flow.cell_of(xa[hit])
            xn[hit] = xa[hit] + 0.3 * (flow.o + (ijk + 0.5) * flow.h - xa[hit])
            hit[:] = False
        fate[ia[done_exit]] = 1
        t_exit[ia[done_exit]] = tn[done_exit]
        fate[ia[out_open]] = 3
        stop = done_exit | out_open | hit
        timeout = tn >= t_max - 1e-12
        x[ia], v[ia], t[ia] = xn, vn, tn
        for k in range(record):
            if alive[k]:
                paths[k].append((t[k], *x[k]))
        alive[ia[stop | timeout]] = False
    return t_exit, fate, paths, touched


def resample_path(path, dt_s, t_end):
    a = np.array(path)
    ts = np.arange(0, min(a[-1, 0], t_end) + 1e-15, dt_s)
    return np.stack([np.interp(ts, a[:, 0], a[:, k]) for k in (1, 2, 3)], 1)


def streamline(flow, x0, t_max, steps=600, stop=None):
    x = np.array(x0, float)[None]
    pts = [x[0].copy()]
    for _ in range(steps):
        u = flow.velocity(x)
        s = np.linalg.norm(u)
        if s < 1e-7:
            break
        dt = 0.5 * flow.h / s
        xm = x + 0.5 * dt * u
        xm[:, 2] = np.abs(xm[:, 2])
        x = x + dt * flow.velocity(xm)
        x[:, 2] = np.abs(x[:, 2])
        solid, inside = flow.is_solid(x)
        if not inside[0] or solid[0] or (stop is not None and stop(x)[0]):
            pts.append(x[0].copy())
            break
        pts.append(x[0].copy())
    return np.array(pts)


def thin(pts, tol):
    """Keep points so that straight segments deviate less than tol (Douglas-Peucker)."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a
    L = np.linalg.norm(ab)
    if L == 0:
        d = np.linalg.norm(pts - a, axis=1)
    else:
        d = np.linalg.norm(np.cross(pts - a, ab / L), axis=1)
    i = int(np.argmax(d))
    if d[i] > tol:
        return np.vstack([thin(pts[:i + 1], tol)[:-1], thin(pts[i:], tol)])
    return np.vstack([a, b])


# ================================================================== residence-time statistics
def widths(t_exit, n_total, t_lo, t_hi, per_decade=50):
    """Full widths (s) at 50, 10 and 1 % of the peak signal, from log-spaced bins (less tail noise)."""
    te = t_exit[np.isfinite(t_exit)]
    edges = 10 ** np.arange(np.log10(t_lo), np.log10(t_hi) + 1 / per_decade, 1 / per_decade)
    c, _ = np.histogram(te, edges)
    k = np.exp(-0.5 * (np.arange(-3, 4) / 1.0) ** 2)
    s = np.convolve(c / np.diff(edges), k / k.sum(), mode="same")
    tc = np.sqrt(edges[1:] * edges[:-1])
    ip = int(np.argmax(s))
    out = {"peak": float(tc[ip])}
    for f in (0.5, 0.1, 0.01):
        lev = f * s[ip]
        i0 = ip
        while i0 > 0 and s[i0 - 1] >= lev:
            i0 -= 1
        i1 = int(np.flatnonzero(s >= lev).max())
        tl = tc[i0] if i0 == 0 else np.interp(lev, [s[i0 - 1], s[i0]], [tc[i0 - 1], tc[i0]])
        tr = tc[i1] if i1 == len(s) - 1 else np.interp(lev, [s[i1 + 1], s[i1]], [tc[i1 + 1], tc[i1]])
        out[f"w{int(f * 100)}"] = float(tr - tl)
        out[f"open{int(f * 100)}"] = bool(i1 >= len(s) - 3)     # still above the level at the horizon
    out["mean"] = float(te.mean()) if te.size else float("nan")
    out["exited"] = float(len(te) / n_total)
    return out


def log_curve(t_exit, grid, per_decade=24):
    """Signal per unit (linear) time on log-spaced bins, smoothed, peak-normalised, at grid points."""
    te = t_exit[np.isfinite(t_exit)]
    lg = np.log10(grid)
    edges = 10 ** np.arange(lg[0], lg[-1] + 1 / per_decade, 1 / per_decade)
    c, _ = np.histogram(te, edges)
    dens = c / np.diff(edges)
    k = np.exp(-0.5 * (np.arange(-3, 4) / 1.0) ** 2)
    dens = np.convolve(dens, k / k.sum(), mode="same")
    tc = np.sqrt(edges[1:] * edges[:-1])
    y = np.interp(lg, np.log10(tc), dens, left=0, right=0)
    return y / y.max() if y.max() > 0 else y


# ================================================================== cases
def cup_case(g=GEOM, q_jet=Q_JET, plume=PLUME_R, n_part=N_PART, sizes=SIZES, record=0, quiet=False):
    """Solve the cup flow and track particles; returns flow, metadata, stats, exit times, paths."""
    cup, cm = build_cup(g=g, q_jet=q_jet)
    if not quiet:
        print(f"  grid {cup.n}, {cup.fluid.sum()} fluid cells")
    cup.solve(steps=4000, label="cup" if not quiet else f"cup q={q_jet}")
    pe, de = cm["pe"] * 1e-3, cm["de"]
    rw = (g["cup_r"] + g["cup_wall"]) * 1e-3

    def cup_exit(x):
        s = (x - pe) @ de
        r = np.linalg.norm((x - pe) - s[:, None] * de, axis=1)
        return (s > EXIT_PLANE * 1e-3) & (r < 0.6 * g["exit_d"] * 1e-3)

    def cup_open(x):   # slipped under the rim into the outer chamber (or out through the top)
        r = np.hypot(x[:, 0], x[:, 2])
        tube = np.linalg.norm(np.cross(x - pe, de), axis=1) < 0.6 * g["exit_d"] * 1e-3
        return ~cup_exit(x) & ~tube & ((r > rw + 0.2e-3) | (x[:, 1] > cm["hi"][1] * 1e-3))

    stats, t_exit, paths = {}, {}, []
    for name, d in sizes:
        tau = relaxation_time(d)
        te, fate, pth, touched = track(cup, release(n_part, plume), tau, T_MAX_CUP, cup_exit, cup_open,
                                       record=record, dt_max=2e-5)
        st = widths(te, n_part, 1e-4, T_MAX_CUP)
        st.update(still_in=float(np.mean(fate == 0)), escaped=float(np.mean(fate == 3)),
                  deposited=float(np.mean(fate == 2)), touched_wall=float(touched.mean()), tau=tau)
        stats[name], t_exit[name] = st, te
        for i, p in enumerate(pth):
            r = resample_path(p, 0.05e-3, 0.012)
            paths.append({"s": name, "x": int(bool(np.isfinite(te[i]) and te[i] <= 0.012)),
                          "p": np.round(r.ravel() * 1e5).astype(int).tolist()})
        if not quiet:
            print(f"  {name:9s} FWHM {st['w50']*1e3:.2f} ms, 10% {st['w10']*1e3:.2f} ms, 1% {st['w1']*1e3:.2f} ms,"
                  f" peak {st['peak']*1e3:.2f} ms, exited {st['exited']:.3f}, escaped {st['escaped']:.3f},"
                  f" still in {st['still_in']:.3f}, deposited {st['deposited']:.3f}")
    return cup, cm, stats, t_exit, paths, cup_exit


SWEEP = [   # (label, geometry changes, jet flow L/min, plume radius mm), relative to the defaults
    ("default: flat jet 3 x 0.6 mm, 0.8 L/min, cup 1.5 mm tall", {}, Q_JET, PLUME_R),
    ("cup 2.0 mm tall", {"cup_h": 2.0}, Q_JET, PLUME_R),
    ("jet 0.5 L/min", {}, 0.5, PLUME_R),
    ("plume radius 0.4 mm", {}, Q_JET, 0.4),
    ("plume radius 1.2 mm", {}, Q_JET, 1.2),
    ("round 1 mm jet, sweeping low", {"jet_d": 1.0, "jet_w": 1.0, "jet_y": 0.8, "jet_aim_y": 0.8}, Q_JET, PLUME_R),
    ("round 1 mm jet, aimed down at the site", {"jet_d": 1.0, "jet_w": 1.0, "jet_y": 1.0, "jet_aim_y": 0.0,
                                                "exit_y": 1.0}, Q_JET, PLUME_R),
]


def _sweep_one(case):
    label, change, q, plume = case
    g = dict(GEOM, **change)
    _, _, stats, _, _, _ = cup_case(g, q, plume, n_part=10000, sizes=SIZES[:1], quiet=True)
    return label, stats["massless"]


def sweep():
    """Sensitivity of the cell-only response to the schematic design choices (massless particles)."""
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=len(SWEEP)) as ex:
        rows = list(ex.map(_sweep_one, SWEEP))
    print("\n| Case | FWHM (ms) | 10% (ms) | 1% (ms) | Exited by 60 ms | Under the rim |")
    print("|---|---|---|---|---|---|")
    for label, st in rows:
        w1 = f"{st['w1'] * 1e3:.1f}" + ("+" if st["open1"] else "")
        print(f"| {label} | {st['w50'] * 1e3:.2f} | {st['w10'] * 1e3:.1f} | {w1} | {st['exited'] * 100:.0f}% |"
              f" {st['escaped'] * 100:.0f}% |")


# ================================================================== main
def main():
    t_start = time.time()
    g = GEOM
    out = {"note": "Computed by cell_flow_model.py: schematic geometry, steady laminar He, not manufacturer CAD.",
           "geom": g, "flows_Lmin": {"jet": Q_JET, "flush": Q_FLUSH, "conventional": Q_CONV},
           "plume_r_mm": PLUME_R, "exit_plane_mm": EXIT_PLANE}

    print(f"He: nu = {NU_HE:.3e} m2/s, mean free path = {MFP_HE * 1e6:.3f} um")
    for name, d in SIZES:
        print(f"  {name:9s} tau = {relaxation_time(d):.2e} s")

    # ---------------- cup
    print("Cup solve and particle tracking")
    cup, cm, cup_stats, cup_t, cup_paths, cup_exit = cup_case(record=24)

    # cup streamlines: seeds across the nozzle, in the plume and in the cup body
    pn = cm["pn"]
    seeds = [np.array([pn[0] - 0.6, pn[1] + dy, z]) for dy in (-0.15, 0.15)
             for z in (0.1, 0.6, 1.1)]
    seeds += [np.array(s, float) for s in [(0, 0.3, 0.3), (0, 0.6, 0.6), (0.3, 0.2, 0.9), (-3, 1.0, 2.5),
                                             (0, 1.2, 3.5), (2, 0.6, 3.0), (-1, 0.9, 4.2), (2.5, 1.1, 1.5),
                                             (3.5, 0.2, 2.0), (-4, 1.2, 1.0)]]
    cup_lines = []
    for s0 in seeds:
        sl = streamline(cup, s0 * 1e-3, 0.05, steps=800, stop=cup_exit) * 1e3
        cup_lines.append(np.round(thin(sl, 0.02).ravel() * 100).astype(int).tolist())

    # ---------------- outer flush around the cup, and a conventional cell in the same box
    print("Outer flush solve (two-volume)")
    outer, _ = build_outer(True, Q=Q_FLUSH)
    outer.solve(steps=6000, label="outer", tol=1e-5)
    print("Conventional single-volume solve")
    conv, _ = build_outer(False, Q=Q_CONV)
    conv.solve(steps=6000, label="conv", tol=1e-5)

    def lines_outer(flow, tmax):
        res = []
        L = g["chamber"][0]
        for y_ in g["port_y"] + np.array([-1.2, 0, 1.2]):
            for z_ in (0.3, 1.2):
                sl = streamline(flow, np.array([-L / 2 + 0.5, y_, z_]) * 1e-3, tmax, steps=2500) * 1e3
                res.append(np.round(thin(sl, 0.3).ravel() * 10).astype(int).tolist())
        for x_, y_, z_ in [(-30, 3, 15), (-10, 18, 25), (10, 5, 28), (25, 15, 10), (-20, 10, 30),
                           (0, 2, 12), (30, 4, 25), (-40, 18, 8), (15, 19, 2), (-5, 6, 8)]:
            sl = streamline(flow, np.array([x_, y_, z_]) * 1e-3, tmax, steps=2500) * 1e3
            res.append(np.round(thin(sl, 0.3).ravel() * 10).astype(int).tolist())
        return res

    outer_lines = lines_outer(outer, 30)
    conv_lines = lines_outer(conv, 30)

    L = g["chamber"][0]

    def conv_exit(x):
        return x[:, 0] > (L / 2 - 0.5 * H_OUT) * 1e-3     # only the open outlet faces lead there

    conv_stats, conv_paths, conv_t = {}, [], {}
    for name, d in SIZES:
        tau = relaxation_time(d)
        te, fate, paths, touched = track(conv, release(N_PART_CONV), tau, T_MAX_CONV, conv_exit, None,
                                         record=24, move=0.3, dt_max=0.05)
        # most of the plume is still inside at the horizon, so report how fast it leaves, not peak widths
        st = {"exited": float(np.mean(fate == 1)), "still_in": float(np.mean(fate == 0)),
              "deposited": float(np.mean(fate == 2)), "tau": tau}
        ts = np.sort(te[np.isfinite(te)])
        for f in (0.01, 0.1, 0.5):
            k = int(np.ceil(f * N_PART_CONV)) - 1
            st[f"t{int(f * 100)}"] = float(ts[k]) if k < len(ts) else None
        conv_stats[name], conv_t[name] = st, te
        for i, p in enumerate(paths):
            r = resample_path(p, 0.25, 30.0)
            conv_paths.append({"s": name, "x": int(bool(np.isfinite(te[i]) and te[i] <= 30.0)),
                               "p": np.round(r.ravel() * 1e4).astype(int).tolist()})
        fmt = lambda v: "not reached" if v is None else f"{v:.1f} s"
        print(f"  conv {name:9s} 1% out after {fmt(st['t1'])}, 10% after {fmt(st['t10'])}, 50% after "
              f"{fmt(st['t50'])}; by {T_MAX_CONV:.0f} s: out {st['exited']:.3f}, deposited {st['deposited']:.3f},"
              f" still in {st['still_in']:.3f}")

    # ---------------- curves for the viewer and the figure
    grid = 10 ** np.linspace(-4, np.log10(T_MAX_CONV), 175)
    curves = {"t": [float(f"{v:.4g}") for v in grid]}
    for name, _ in SIZES:   # signal (peak = 1) and cumulative fraction of the plume that has left
        curves["twovol " + name] = np.round(log_curve(cup_t[name], grid), 3).tolist()
        curves["conv " + name] = np.round(log_curve(conv_t[name], grid), 3).tolist()
        for case, te, n in (("twovol", cup_t[name], N_PART), ("conv", conv_t[name], N_PART_CONV)):
            done = np.sort(te[np.isfinite(te)])
            curves[f"out {case} {name}"] = np.round(np.searchsorted(done, grid) / n, 3).tolist()

    def rnd(d):
        return {k: ((float(f"{v:.4g}") if np.isfinite(v) else None) if isinstance(v, float) else v)
                for k, v in d.items()}
    out.update(
        units={"cup_lines": "0.01 mm", "outer_lines": "0.1 mm", "cup_paths": "0.01 mm every 0.05 ms",
               "conv_paths": "0.1 mm every 0.25 s", "x": "1 if the particle left within the stored path",
               "coords": "x along chamber, y up from sample surface, z across; half domain z>=0, mirror for z<0"},
        cup_lines=cup_lines, outer_lines=outer_lines, conv_lines=conv_lines,
        cup_paths=cup_paths, conv_paths=conv_paths, curves=curves,
        stats={"twovol": {k: rnd(v) for k, v in cup_stats.items()},
               "conv": {k: rnd(v) for k, v in conv_stats.items()}},
        published_twovol_dci_ms={"w50": 1.5, "w10": 3.2, "w1": 4.9},
        axes={"pn": cm["pn"].round(3).tolist(), "dn": cm["dn"].round(4).tolist(),
              "pe": cm["pe"].round(3).tolist(), "de": cm["de"].round(4).tolist()},
        grid_mm={"cup": H_CUP, "outer": H_OUT},
    )
    js = json.dumps(out, separators=(",", ":"))
    (HERE / "cell-flow-paths.json").write_text(js)
    print(f"JSON {len(js) / 1024:.0f} kB")

    html = HERE / "Laser-3D.html"
    src = html.read_text()
    new, k = re.subn(r"/\*CELLFLOW\*/.*?/\*END CELLFLOW\*/",
                     lambda m: "/*CELLFLOW*/" + js + "/*END CELLFLOW*/", src, flags=re.S)
    if k == 1:
        html.write_text(new)
        print("embedded in Laser-3D.html")
    else:
        print("Laser-3D.html has no CELLFLOW marker; JSON not embedded")

    figure(grid, curves, cup_stats, conv_stats)
    print(f"done in {time.time() - t_start:.0f} s")


def emg_peak_aligned(t, t_peak, s=0.54e-3, tau=0.56e-3):
    """Published two-volume + DCI fit (1.5 / 3.2 / 4.9 ms widths), shifted so its peak sits at t_peak."""
    from math import erfc, exp, sqrt
    f = lambda x: exp(s * s / (2 * tau * tau) - x / tau) / (2 * tau) * erfc((s * s / tau - x) / (s * sqrt(2)))
    xs = np.linspace(-5 * s, 10 * tau, 4001)
    x0 = xs[np.argmax([f(x) for x in xs])]
    y = np.array([f(x - t_peak + x0) if x - t_peak + x0 > -6 * s else 0.0 for x in t])
    return y / y.max()


def figure(grid, curves, cup_stats, conv_stats):
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "axes.titlesize": 10})
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(7.2, 5.6), dpi=150, sharex=True)
    t = np.array(grid)
    cols = {"massless": "#1f6f8b", "0.1 um": "#3aa0a8", "1 um": "#e08a2c"}
    for name in cols:
        st = cup_stats[name]
        ax.plot(t, curves["twovol " + name], color=cols[name], lw=1.6,
                label=f"two-volume cup, {name}: {st['w50'] * 1e3:.2f} / {st['w10'] * 1e3:.1f} / {st['w1'] * 1e3:.1f} ms")
    ax.plot(t, emg_peak_aligned(t, cup_stats["massless"]["peak"]), color="0.45", lw=1.2, ls=":",
            label="published two-volume + DCI fit, whole system: 1.5 / 3.2 / 4.9 ms (peak aligned)")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("signal (peak = 1)")
    ax.set_title("Computed single-pulse response at the cell exit (schematic geometry, cell only)")
    ax.legend(fontsize=7, frameon=False, loc="upper right", title="widths at 50 / 10 / 1 % of peak",
              title_fontsize=7)
    for name, ls in (("massless", "-"), ("1 um", "--")):
        bx.plot(t, curves["out twovol " + name], color=cols[name], lw=1.6, ls=ls, label=f"two-volume cup, {name}")
        bx.plot(t, curves["out conv " + name], color="#8a4fb5", lw=1.6, ls=ls,
                label=f"conventional cell, {name}: {conv_stats[name]['exited'] * 100:.0f}% out by 60 s")
    bx.set_xscale("log")
    bx.set_xlim(1e-4, T_MAX_CONV)
    bx.set_ylim(0, 1.05)
    bx.set_ylabel("fraction of plume out")
    bx.set_xlabel("time after the pulse (s); tubing delay not included")
    bx.legend(fontsize=7, frameon=False, loc="center left")
    fig.tight_layout()
    fig.savefig(HERE / "13-cell-residence-time.png")


if __name__ == "__main__":
    import sys
    sweep() if "--sweep" in sys.argv else main()
