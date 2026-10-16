"""Teaching figures: ideal ToF arrival times for natural nuclides Na-U, and 1-amu leakage.

Run from this folder:  python3 tof_arrival_leakage.py
Inputs : ../Reference/nuclides-Na-U-NIST.csv (NIST Atomic Weights and Isotopic Compositions)
Outputs: 11-tof-arrival-Na-U.png, 12-tof-time-resolution-leakage.png

All instrument numbers are stated assumptions, not Vitesse calibration:
  U    = 1 kV   acceleration (course-reported pusher pulse; treated as the full ion energy per charge)
  L    = 1 m    effective field-free path (same teaching value as the 3D viewer)
  R    = 4000   FWHM resolving power, used only to set ideal Gaussian peak widths
  AS   = 6.5e-4 adjacent-mass abundance sensitivity (published icpTOF value, Hendriks et al. 2017)
"""
import csv
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
U_ACC, L_EFF, R_FWHM = 1000.0, 1.0, 4000.0
U_AMU, E_CH = 1.66053906660e-27, 1.602176634e-19

def flight_time(m):
    """Ideal field-free flight time in seconds for a singly charged ion of mass m (u)."""
    return L_EFF * math.sqrt(m * U_AMU / (2 * E_CH * U_ACC))

def load_nuclides():
    with open(HERE.parent / "Reference" / "nuclides-Na-U-NIST.csv") as f:
        return [dict(Z=int(r["Z"]), sym=r["symbol"], A=int(r["A"]), m=float(r["mass"]), ab=float(r["abundance"]))
                for r in csv.DictReader(f)]

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlesize": 10})

# ---------------------------------------------------------------- figure 11
nuc = load_nuclides()
t_min, t_max = flight_time(21) * 1e6, flight_time(242) * 1e6
time = np.linspace(t_min, t_max, 400_000)
signal = np.full_like(time, 1e-6)
for n in nuc:
    tc = flight_time(n["m"]) * 1e6
    sigma = tc / (2 * R_FWHM) / 2.354820045
    lo, hi = np.searchsorted(time, [tc - 8 * sigma, tc + 8 * sigma])
    signal[lo:hi] += n["ab"] * np.exp(-0.5 * ((time[lo:hi] - tc) / sigma) ** 2)

fig, (ax, axz) = plt.subplots(2, 1, figsize=(11, 6.4), gridspec_kw=dict(height_ratios=[2.1, 1], hspace=.55))
cmap = plt.get_cmap("viridis")
ax.plot(time, signal, lw=.5, color="#33475b")
for n in nuc:
    tc = flight_time(n["m"]) * 1e6
    ax.plot([tc, tc], [1e-6, n["ab"]], lw=.9, color=cmap((n["Z"] - 11) / 81))
ar = [flight_time(m) * 1e6 for m in (35.5, 40.5)]
ax.axvspan(*ar, color="#e58e26", alpha=.18, lw=0)
ax.text(ar[0] - .1, 2e-5, "Ar isotopes: in reality many orders\nlarger, removed by cell + blanker", ha="right", va="bottom", fontsize=7.5, color="#a35a00", bbox=dict(fc="white", ec="none", alpha=.9))
for sym in ["Na", "Si", "Ca", "Ti", "Fe", "Zn", "Sr", "Zr", "Sn", "Ba", "Nd", "Yb", "Hf", "Pb", "Th", "U"]:
    iso = max((n for n in nuc if n["sym"] == sym), key=lambda n: n["ab"])
    ax.text(flight_time(iso["m"]) * 1e6, iso["ab"] * 1.6, sym, ha="center", fontsize=7.5)
ax.set_yscale("log"); ax.set_ylim(5e-6, 8); ax.set_xlim(t_min, t_max)
ax.set_xlabel("Arrival time after extraction (μs)"); ax.set_ylabel("Relative signal\n(isotope abundance)")
ax.set_title(f"Ideal ToF arrival spectrum, all {len(nuc)} natural nuclides from Na to U (equal element concentrations)", loc="left")
top = ax.secondary_xaxis("top", functions=(lambda t: (t * 1e-6 / L_EFF) ** 2 * 2 * E_CH * U_ACC / U_AMU,
                                            lambda m: L_EFF * np.sqrt(np.maximum(m, 0) * U_AMU / (2 * E_CH * U_ACC)) * 1e6))
top.set_xticks([23, 40, 56, 88, 120, 140, 160, 180, 208, 238]); top.set_xlabel("m/z")

# Zoom: Hg-Tl-Pb-Bi region, where 1 amu is ~80 ns and peaks are ~3 ns wide.
zlo, zhi = flight_time(195.5) * 1e6, flight_time(209.6) * 1e6
mask = (time > zlo) & (time < zhi)
axz.plot(time[mask], signal[mask], lw=.8, color="#33475b")
axz.set_yscale("log"); axz.set_ylim(5e-6, 60); axz.set_xlim(zlo, zhi)
by_A = {}
for n in nuc:
    if zlo < flight_time(n["m"]) * 1e6 < zhi and n["ab"] > 1e-3:
        by_A.setdefault(n["A"], []).append(n)
for A, group in by_A.items():
    tc = flight_time(max(group, key=lambda n: n["ab"])["m"]) * 1e6
    top_ab = sum(n["ab"] for n in group)
    axz.text(tc, min(top_ab, 1) * 1.5, f"{A} " + "/".join(n["sym"] for n in group), ha="center", fontsize=6.5, rotation=90, va="bottom",
             color="#c0392b" if len(group) > 1 else "black")
axz.text(zlo + .01, 2e-4, "red = isobars: same nominal mass,\nunresolved at R = 4000", fontsize=7, color="#c0392b")
t206, t207 = flight_time(205.974) * 1e6, flight_time(206.976) * 1e6
axz.annotate("", xy=(t207, 2e-5), xytext=(t206, 2e-5), arrowprops=dict(arrowstyle="<->", lw=.8))
axz.text((t206 + t207) / 2, 3e-5, f"1 amu = {(t207 - t206) * 1e3:.0f} ns", ha="center", fontsize=7.5, bbox=dict(fc="white", ec="none", alpha=.9))
axz.set_xlabel("Arrival time (μs)"); axz.set_ylabel("Relative signal")
axz.set_title(f"Zoom m/z 196–209: peak FWHM ≈ t/2R = {flight_time(206) / (2 * R_FWHM) * 1e9:.1f} ns at m/z 206", loc="left")
fig.text(.01, .005, f"Assumptions: t = L√(m/2eU), U = {U_ACC / 1e3:.0f} kV, L = {L_EFF:.0f} m effective, R = {R_FWHM:.0f} (ideal Gaussian peaks), "
         "singly charged ions only, no polyatomics or doubly charged ions. Abundances: NIST. Teaching values, not Vitesse calibration.",
         fontsize=7, color="#555")
fig.savefig(HERE / "11-tof-arrival-Na-U.png", dpi=170, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- figure 12
masses = np.linspace(23, 238, 300)
t_s = np.array([flight_time(m) for m in masses])
dt_amu = t_s / (2 * masses) * 1e9           # ns between adjacent nominal masses
fwhm = t_s / (2 * R_FWHM) * 1e9              # ns ideal peak FWHM

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), gridspec_kw=dict(wspace=.38))
a = axes[0]
a.plot(masses, dt_amu, color="#1f6f8b", lw=2, label="Δt between adjacent masses = t/2m")
a.plot(masses, fwhm, color="#e58e26", lw=2, label=f"Peak FWHM = t/2R (R = {R_FWHM:.0f})")
for y, lab, c in [(0.5, "ADC interval at 2 GS/s (0.5 ns)", "#666"), (0.55, "", "#666")]:
    a.axhline(y, ls=":", color=c, lw=.9)
a.text(30, .56, "single-ion pulse ≈ 0.55 ns · ADC 0.5 ns", fontsize=7, color="#555", va="bottom")
a.axhspan(2, 20, color="#9b59b6", alpha=.12, lw=0)
a.text(30, 6, "illustrative event dead time /\nrecovery range (2–20 ns)", fontsize=7, color="#6c3483")
a.set_yscale("log"); a.set_ylim(.3, 600); a.set_xlabel("m/z"); a.set_ylabel("time (ns)")
a.set_title("A · Time resolution needed for 1 amu", loc="left"); a.legend(fontsize=7, frameon=False, loc="upper right")
for m in (23, 88, 238):
    a.annotate(f"{flight_time(m) / (2 * m) * 1e9:.0f} ns", (m, flight_time(m) / (2 * m) * 1e9), textcoords="offset points",
               xytext=(0, 6), ha="center", fontsize=7, color="#1f6f8b")

# B: peak model at m/z 88 -> 89. Gaussian + small exponential tail with tau fitted to reproduce AS.
AS_TARGET, F_TAIL, M0 = 6.5e-4, 0.05, 88
t0, t1 = flight_time(M0) * 1e9, flight_time(M0 + 1) * 1e9
sig = (t0 / (2 * R_FWHM)) / 2.354820045
w = 2 * sig * 2.354820045                    # integration window: +-1 FWHM around each peak

def tail_leak(tau):
    lo, hi = (t1 - t0) - w / 2, (t1 - t0) + w / 2
    return F_TAIL * (math.exp(-lo / tau) - math.exp(-hi / tau))

lo_tau, hi_tau = 1.0, t1 - t0                # bisection on the rising branch (tau < 1-amu spacing)
for _ in range(200):
    mid = math.sqrt(lo_tau * hi_tau)
    lo_tau, hi_tau = (mid, hi_tau) if tail_leak(mid) < AS_TARGET else (lo_tau, mid)
tau = math.sqrt(lo_tau * hi_tau)
tt = np.linspace(t0 - 15, t1 + 25, 8000) - t0
gauss = np.exp(-0.5 * (tt / sig) ** 2) / (sig * math.sqrt(2 * math.pi))
# Analytic exponentially modified Gaussian (unit area): Gaussian convolved with exp(-t/tau)/tau.
erfc = np.vectorize(math.erfc)
conv = np.exp(sig ** 2 / (2 * tau ** 2) - tt / tau) / (2 * tau) * erfc((sig ** 2 / tau - tt) / (sig * math.sqrt(2)))
major = (1 - F_TAIL) * gauss + F_TAIL * conv
trace_ratio = 1e-2                           # trace at 89 is 1% of the major peak
tr_peak = trace_ratio * np.exp(-0.5 * ((tt - (t1 - t0)) / sig) ** 2) / (sig * math.sqrt(2 * math.pi))
b = axes[1]
b.plot(tt, major, color="#1f6f8b", lw=1.6, label=f"m/z {M0} major (Gaussian + {F_TAIL:.0%} tail, τ = {tau:.0f} ns)")
b.plot(tt, tr_peak, color="#c0392b", lw=1.4, label=f"m/z {M0 + 1} trace at {trace_ratio:.0%} of major")
b.plot(tt, F_TAIL * conv, color="#1f6f8b", lw=.8, ls="--", label="tail component alone")
b.axvspan((t1 - t0) - w / 2, (t1 - t0) + w / 2, color="#c0392b", alpha=.12, lw=0)
b.set_yscale("log"); b.set_ylim(1e-7, 1); b.set_xlabel(f"time from m/z {M0} peak (ns)"); b.set_ylabel("signal per ns (major peak area = 1)")
b.set_title(f"B · Tail reproducing AS = {AS_TARGET:.1e} at {t1 - t0:.0f} ns", loc="left"); b.legend(fontsize=6.5, frameon=False, loc="upper right")
b.text((t1 - t0), 3e-7, "m/z 89\nwindow", ha="center", fontsize=7, color="#c0392b")

# C: bias on the trace vs major/trace intensity ratio.
c = axes[2]
ratio = np.logspace(0, 6, 200)
for AS, lab, col in [(2e-3, "2×10⁻³ (icpTOF-S2, 2023)", "#c0392b"), (6.5e-4, "6.5×10⁻⁴ (icpTOF, 2017)", "#1f6f8b"),
                     (1e-5, "1×10⁻⁵ (after tail fitting, illustrative)", "#7f8c8d"), (1e-7, "1×10⁻⁷ (good quadrupole)", "#27ae60")]:
    c.plot(ratio, 100 * AS * ratio, lw=1.8, color=col, label=f"AS {lab}")
c.axhline(1, color="#555", ls=":", lw=.9); c.text(1.3, 1.15, "1% bias", fontsize=7, color="#555")
c.axhline(100, color="#555", ls=":", lw=.9); c.text(1.3, 115, "leak = trace", fontsize=7, color="#555")
c.set_xscale("log"); c.set_yscale("log"); c.set_ylim(1e-4, 1e4)
c.set_xlabel("major (m) / trace (m+1) true intensity"); c.set_ylabel("apparent trace excess (%)")
c.set_title("C · How strong a neighbour must be", loc="left"); c.legend(fontsize=6.5, frameon=False, loc="upper left")
fig.text(.01, -.03, f"Assumptions as figure 11 (U = 1 kV, L = 1 m, R = {R_FWHM:.0f}). Panel B tail fraction ({F_TAIL:.0%}) is invented; τ is solved so the "
         "m+1 window (±1 FWHM) receives the published icpTOF AS. The tail stands for every slow component (detector recovery, ringing, ion-optical "
         "scattering); its real shape must be measured.", fontsize=7, color="#555", wrap=True)
fig.savefig(HERE / "12-tof-time-resolution-leakage.png", dpi=170, bbox_inches="tight")
plt.close(fig)

print(f"tau for AS {AS_TARGET:g} with {F_TAIL:.0%} tail at m/z {M0}: {tau:.1f} ns")
for m in (23, 40, 88, 206, 238):
    print(f"m/z {m}: t = {flight_time(m) * 1e6:.2f} us, 1 amu = {flight_time(m) / (2 * m) * 1e9:.1f} ns, FWHM = {flight_time(m) / (2 * R_FWHM) * 1e9:.2f} ns")
print("full-range period at U-238 arrival:", f"{flight_time(238) * 1e6:.1f} us -> max {1 / flight_time(238) / 1e3:.1f} kHz")
