---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
  - instrument-visualization
---

# Instrument illustrations: originals and an interactive model

[Home](index.md) · [ToF derivation](05-time-of-flight-from-first-principles.md)

## Open the offline 3D illustration

[Open Instrument-3D.html in a browser](figures/Instrument-3D.html). On this site the link opens the viewer directly; see also [Interactive models](models.md). No server, Julia installation, plugins or network connection are needed. The viewer uses bundled **Three.js r160**; the browser must support WebGL. Here “three.jl” was interpreted as Three.js for browser illustrations.

- Drag to rotate, scroll to zoom, and use front view or ToF close-up.
- Select the component labels to read their physical roles; **Ion blanker** opens its detailed animation.
- Pause, scrub or restart the packet. Fe, Pb and U illustrate common extraction followed by different arrival times.
- Toggle the conceptual quadrupole bypass route.
- Change acceleration voltage and compare the calculated flight times for a hypothetical 1 m field-free path.
- Select **Reflectron focusing** to follow three ²⁰⁶Pb⁺ ions launched together with different kinetic energies. Watch the retarding electric field slow them, their different turning depths, and their return to the detector plane. Adjust the energy spread and field strength; **Tune first-order focus** restores the field that nearly aligns arrival times. Pause or scrub to inspect the turnaround.
- Compare the arrival-offset plot and the drift/mirror timing table: higher-energy ions save time in the drift but spend longer in the mirror. Different isotopes still arrive separately; the reflectron narrows the energy spread within each isotope's arrival peak.
- Select **Argon blanker** to inspect the interleaved wire sets between extraction and reflectron. Equal wire potentials transmit ions; opposite offsets produce sideways kicks in alternating directions. The gas and plasma remain on.
- Adjust the rejection **pulse width** and **center offset**, or disable blanking. A 30 ns pulse centered on the ideal mass-40 arrival rejects Ar-40 and Ca-40; widening it to 80 ns also rejects K-39. Moving it away from mass 40 permits argon leakage. The mass-80 argon dimer remains transmitted by this single-window example.
- Watch the synchronized gate-arrival timeline, wire-polarity readout, electric-field arrows, particle trajectories and selection table. Playback slows around argon's arrival so the short gate pulse remains visible. Pause and scrub to inspect the active field or interception.
- Expand the source panels for links to the original diagrams.
- Select **MagneTOF cutaway**, or click **Detector** in the instrument overview. Open the housing with the **Exploded housing** slider; inspect the impact plate, crossed fields, receiving dynodes, multiplier and anode. The replay follows three coincident impact positions through secondary-electron focusing and multiplication.
- In its separate two-ion waveform example, adjust pulse width, separation, sampling rate and sampling phase. Compare pulse overlap with additive ideal area and the area estimated from ADC samples. The dashed wider response is an invented comparison; this plot does not measure counting dead time.
- Select **Explore electron timing compensation** for the analytic crossed-field view. Three electron trajectories have different initial velocities and path lengths but return together after one gyroperiod. Adjust B and compare the path-length/arrival-time table. This same-origin example explains a timing property; broad-impact-area spatial focusing still requires the real detector's shaped fields.

The **component sequence and folded arrangement** follow Nu’s Vitesse brochure. Mesh shapes, electrode counts, scale, spacing, trajectories and animated speeds in instrument mode are educational constructions. This is not a Vitesse calibration or manufacturer CAD. Its numerical drift calculator uses $t=L\sqrt{m/(2qV)}$ with $L=1$ m and $q=e$, explicitly separate from the illustrative path. At 5 kV it gives 7.62 μs for mass 56, 14.61 μs for mass 206 and 15.71 μs for mass 238.

**Reflectron focusing mode**, added 10 October 2026, uses analytic one-dimensional motion in an ideal uniform retarding field, separate from the instrument reconstruction. Each ion travels 0.5 m to the mirror and 0.5 m back to the launch/detector plane; the three displayed lanes only separate the particles visually. Nominal energy is 5 keV, with adjustable spread. Potential increases into the mirror, while the electric field and force on positive ions point toward the entrance. Inside, $x=v\tau-\tfrac12(qE/m)\tau^2$ and the velocity reverses continuously. Total time is $t=L_d/v+2mv/(qE)$; at $E=20$ kV/m, nominal turning depth is 25 cm and $L_d=4d$. For ±10% energy spread, the three-ion arrival span falls from about 1470 ns in drift alone to 41 ns with the tuned mirror. First-order focusing leaves a small residual spread; these are teaching calculations, not measured peak widths or instrument settings. The arrival-offset plot uses a shared scale and subtracts each mode's nominal arrival time. See [the derivation and primary source](05-time-of-flight-from-first-principles.md#step-5-why-a-reflectron-works).

## Additions of 16 October 2026

**Collision cell / H₂ and He** (button **H₂/He cell**, or click **Segmented reaction cell** in the overview). A local cutaway of a segmented hexapole RF guide filled with H₂ (white pairs) and He (pink).

- **What happens to Ar⁺.** Ar⁺ (amber) becomes ArH⁺ (orange). That then becomes H₃⁺ (red) plus a neutral Ar atom (grey) that is no longer RF-guided and drifts to the wall.
- **Analytes.** Ca⁺, Fe⁺ and Pb⁺ pass through.
- **Controls.** H₂ pressure, ion residence time and He pressure. The exit fractions follow $e^{-k_1nt}$ and the sequential ArH⁺ chain, with $k_1=8.9\times10^{-10}$ and $k_2=6.3\times10^{-10}$ cm³ s⁻¹.
- **Plot.** The log-scale plot traces Ar⁺, ArH⁺ and the hydrogen products along the cell.
- **He cooling.** Raising He damps the drawn radial oscillation; this part is schematic, not computed.
- **Next stage.** **Next: blank the residual Ar⁺** jumps to the blanker.

The pressures and residence time are invented, the analytes are assumed unreactive, and scattering losses, back-reactions, RF stability and any KED barrier are omitted. The physics is in [note 06](06-detectors-noise-and-interferences.md#argon-why-the-plasma-gas-threatens-the-detector).

**Reflectron noisy ensemble.** In **Reflectron focusing**, choose **Ions → Noisy ensemble**. Up to 300 ²⁰⁶Pb⁺ ions get a Gaussian-random kinetic energy (σ adjustable) and a Gaussian-random start time (pusher jitter σ). They fly the same ideal field as the tracers, coloured slow → fast. Histograms compare drift-only and reflectron arrival offsets on one scale.

| Default draw (120 ions, σ_E = 3%, jitter σ = 2 ns) | Arrival σ |
|---|---|
| Drift only | 238 ns |
| Tuned mirror | 4.9 ns |
| Tuned mirror, no jitter (second-order residue) | 4.3 ns |
| Mirror detuned to 80% | 59 ns |

The mirror removes the energy part to first order. Start-time jitter passes through, because no static field can tell a late ion from a slow one. Initial position spread in the pusher and space charge are not simulated.

**Laser interaction and two-volume cell:** [Laser-3D.html](figures/Laser-3D.html), a separate offline viewer with the same bundled Three.js r160.

- **Three paired models.** Absorption, spontaneous emission and stimulated emission each show a two-level atom (left) beside the place where the process matters (right): the sample surface (with a band-gap slider), the hot plume, and the laser cavity (with an inversion slider).
- **Cell mode.** Shows the two-volume concept with a conventional-cell comparison, a laminar tubing-delay calculator and a single-pulse response plot.
- **Computed flow (added 16 October 2026).** The cell's gas streamlines and particle paths are computed, not drawn. [cell_flow_model.py](figures/cell_flow_model.py) solves steady laminar He flow for a schematic two-volume geometry and tracks massless, 0.1 μm and 1 μm particles from the ablation site. That geometry is a 100 × 70 × 22 mm chamber with its own flush, a 10 mm cup with a flat He jet, and a 1 mm exit tube; it is not ESL CAD. It also runs the same box as a conventional single-volume cell.
    - **Viewer.** **Cup close-up** and **Whole chamber** buttons switch the view. Pink lines are He in the cup, blue lines the separate outer flush and purple lines the conventional cell; the animated dots are computed particle paths.
    - **Plot.** The response plot shows the computed cell-only curves beside the published whole-system fit, with the fit's peak aligned so only widths compare. With the comparison on, dashed curves show the fraction of the plume that has left each cell.
    - **Data.** Streamlines, paths and curves are stored in [cell-flow-paths.json](figures/cell-flow-paths.json) and embedded in the HTML, so the file stays self-contained.
    - **Assumptions.** Grid sizes, boundary conditions, particle release and the design sweep are listed in [note 02](02-laser-ablation-and-particle-production.md#computed-flow-in-a-schematic-two-volume-cell).

All geometry is schematic and photon colours are false; see [note 02](02-laser-ablation-and-particle-production.md#three-ways-light-interacts-with-matter).

**Static figures:** [11-tof-arrival-Na-U.png](figures/11-tof-arrival-Na-U.png) and [12-tof-time-resolution-leakage.png](figures/12-tof-time-resolution-leakage.png), generated by [tof_arrival_leakage.py](figures/tof_arrival_leakage.py) from NIST abundances. [13-cell-residence-time.png](figures/13-cell-residence-time.png) is generated by [cell_flow_model.py](figures/cell_flow_model.py).

## Argon blanker animation and its assumptions

**Added 10 October 2026:** the instrument overview now includes a conceptual wire gate on the outgoing flight leg, between the pusher and reflectron. Its location is grounded in the [primary Vitesse gate study](https://doi.org/10.1039/D3JA00288H), rather than asserted from the brochure drawing. It is distinct from the upstream attenuator.

The detailed mode is a **local gate cutaway**: launch → mass-dependent drift → wire gate → transmitted beam toward the reflectron. Rejected particles are shown being intercepted outside downstream acceptance; the illustrated interception surfaces are not manufacturer CAD. It does not simulate the subsequent reflectron/detector flight, so its counters report **passed gate**, not measured detector counts.

Timing uses ideal field-free, singly charged 5 keV ions. The gate distance is chosen so nominal mass 40 arrives at 2 μs; other arrivals follow $t_g=2\sqrt{(m/z)/40}$ μs. The wire voltage is represented symbolically as $V_{\rm ref}\pm V_g$, without implying a measured pulser amplitude. Ar-40 and Ca-40 coincide in this **nominal-mass** calculation; the model does not claim their exact masses are identical. It shows species with equal visual prominence to make selection understandable, not their real abundance ratio.

The electric-field direction and opposite kicks in neighboring wire gaps follow the [Bradbury–Nielsen principle](https://web.stanford.edu/group/grattalab/Publications/BrunnerEtAl2012.pdf). Lateral particle paths and wire spacing are illustrative, not a numerical field solution. Packets are point arrivals with instantaneous gate switching. Real packet widths, rise/fall times, jitter and electronic settling artifacts are discussed in [the enriched detector notes](06-detectors-noise-and-interferences.md#how-the-argon-ion-blanker-works) but are not modelled. The animation is an isolated extraction replay. Its timing is not calibrated to the course's unconfirmed 200 kHz cycle or the Adamson et al. (2026) method, whose full settings remain unverified.

## MagneTOF exploded cutaway and its assumptions

**Added 10 October 2026:** this local detector view is grounded in [ETP's electron-focusing patent](https://patents.google.com/patent/US6982428B2/en) and [Simke et al.'s full paper](https://epub.ub.uni-greifswald.de/files/14308/1-s2.0-S1387380624001489-main.pdf). Pole pieces and a field-shaping electrode move outward for inspection; the functional surfaces and particle paths stay in place. This is a teaching exploded view, not an operable detector while disassembled.

The construction illustrates conversion → curved electron transport → progressively smaller receiving surfaces → secondary-emission amplification → anode collection. Shapes, materials/colors, stage count, field amplitudes and paths are illustrative. Arrows identify crossed field directions, with electric force on electrons opposite $\mathbf E$. The animation does not solve the Lorentz equation or establish actual transit-time compensation quantitatively. Multiplying dots symbolize an avalanche; they are not a calculation of gain or detection efficiency.

The **cutaway/cascade replay** has no calibrated time axis. The separate **timing insight** view uses analytic uniform crossed-field motion, with E = 80 kV/m, adjustable B = 10–40 mT, and initial velocities 0, 0.35 and 0.70 times E/B along the drift. Electrons start at the same physical position with zero initial transverse velocity; separate z lanes are visual offsets. At 20 mT all return after 1.786 ns, despite different path lengths. This example is not the shaped, partial-turn MagneTOF lens and does not establish spatial focusing from different starting positions. The display rescales with B; numerical lengths and times retain physical units.

The independent waveform panel uses two unit-area Gaussian pulses, with a selectable **0.50 ns illustrative** response or **1.00 ns** response corresponding approximately to Simke's single-ion pulse example. Neither is a measurement of the installed detector. Its dashed **2 ns** blur is entirely synthetic. Samples occur at the selected rate and phase; the sampled area uses a trapezoidal sum over the plotted 0–8 ns window. Noise, stochastic gain, analog bandwidth, quantization, saturation, ringing and event electronics are omitted. Pulse FWHM, counting dead time and overload recovery remain distinct. Read [the detector explanation](06-detectors-noise-and-interferences.md#inside-magnetof-why-the-electrical-pulse-can-be-so-short) alongside the illustration.

## Nu Vitesse: the manufacturer component drawing

Not reproduced here (© Nu Instruments / AMETEK). See the [Vitesse brochure, printed pages 4–5](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Brochure/Brochure_Vitesse.pdf) and the [official Vitesse page](https://www.nu-ins.com/Products/TOF-ICP-MS/Introduction-to-TOF/Vitesse).

Read the sequence left to right: ICP and focusing optics → quadrupole or bypass → segmented reaction cell → attenuator → ToF extraction and folded flight path. The laser/cell/transport line sits upstream of this drawing.

## Reflectron: original literature drawing

Not reproduced here: see **Figure 1** of the [primary paper](https://www.jetp.ras.ru/cgi-bin/dn/e_037_01_0045.pdf),, Mamyrin, Karataev, Shmikk and Zagulin (1973), “The mass-reflectron, a new nonmagnetic time-of-flight mass spectrometer with high resolution,” *Soviet Physics JETP* 37, 45–48, printed page **46**. The crop retains the figure labels and electronic blocks; neighboring text/figures are excluded. [Primary paper](https://www.jetp.ras.ru/cgi-bin/dn/e_037_01_0045.pdf).

I denotes the ion source, DP the deflecting plates, RS the reflecting system, and SEM the electron multiplier. This historical source is not an ICP. Follow the forward and returning trajectories. The diagram grounds the reflectron principle; the numerical focusing graph in [note 05](05-time-of-flight-from-first-principles.md) explains the idealized first-order compensation rather than reproducing this instrument’s complete optics.

## Nu Plasma: useful comparison, a different analyser

Multicollector photograph not reproduced (© Nu Instruments / AMETEK); see [Nu’s MC-ICP-MS introduction](https://www.nu-ins.com/Products/MC-ICP-MS/Introduction-to-MC-ICP-MS); [original image asset](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Thumbnails/thumbnail-collector.jpg). This shows a collector assembly, not an entire sector-field beam path. It illustrates the MC-ICP-MS family rather than documenting a particular Nu Plasma version’s detailed geometry.

Nu describes an electrostatic energy analyser followed by a magnetic sector and multiple collectors. A sector instrument separates the beam spatially; Vitesse ToF separates arrival times. Both can begin with ICP ion production. Do not use a Nu Plasma magnetic-sector schematic as a ToF flight-path schematic.

## A five-minute visual walkthrough

1. On the original Vitesse layout (brochure link above), point to where atoms become ions, then where ions are mass analysed. These are separate transformations.
2. In the 3D viewer, select sampler/skimmer, optics, and pusher. Explain why pumping, transmission and extraction all lose ions for different reasons.
3. Restart a packet and pause halfway. Name the clock you are observing: ToF extraction/flight, not a laser pulse or a saved pixel.
4. Double acceleration voltage. Verify that ideal drift time decreases by $1/\sqrt{2}$, not by one half.
5. Compare Mamyrin’s reflector with the focusing plot. Explain why a faster ion of the **same** m/z can spend more time in the mirror, even though a lighter ion at the same extraction voltage arrives sooner.

## Provenance and verification

Third-party figures are linked, not reproduced; the HTML 3D illustrations are separate reconstructions. Three.js is distributed under the MIT license; see [included license](figures/Threejs-LICENSE.txt) and [official r160 source](https://github.com/mrdoob/three.js/tree/r160). Each HTML file embeds the library. It makes no network requests during normal operation; source links open only when selected.

JavaScript syntax, the actual Three.js scene/math, component labels, pause/scrub/restart, bypass, view controls, voltage updates and numerical drift times were checked in Node with mocked DOM/WebGL rendering. Details of the earlier logic checks are in [logic verification](Reference/illustration-logic-verification.json).

The updated viewer was additionally checked in **Chromium with WebGL** on 10 October 2026. Desktop and mobile screenshots were inspected, with the blanker cutaway placed above its timeline to keep the wires and trajectories visible. Controls were checked for default Ar/Ca rejection, neighboring-gap kick directions, wider-window K loss, delayed-pulse argon leakage, disabled-gate transmission, pulse centering, field switching, pause/scrub/restart, and preservation of instrument/bypass and reflectron modes. No browser errors or horizontal overflow occurred at the tested 390 px mobile width. See [blanker verification](Reference/blanker-verification.json).

The **MagneTOF cutaway and timing view** were also rendered and visually inspected in Chromium at desktop and 390 px mobile sizes. Checks covered exploded construction, fields, ion conversion and cascade replay, pulse width/separation, sample phase/rate, and shared analytic return times. Doubling B halved the return period; an independent RK4 integration of the Lorentz equations agreed with the displayed analytic trajectories. The timing replay holds the completed return briefly so coincidence can be inspected. The two-ion example retained essentially unit-additive area at 25 GS/s; at 2 GS/s the estimated area depended on sampling phase, as expected for this synthetic narrow response. Existing reflectron and blanker modes still passed their selected checks. See [MagneTOF verification](Reference/magnetof-verification.json).

Earlier generic hardware sketches are retained in `figures/archive` for provenance and are no longer embedded in the study notes. The laser footprint, aerosol washout, energy-focusing, acquisition-clock and peak-width figures remain as explicitly conceptual or synthetic teaching plots.
