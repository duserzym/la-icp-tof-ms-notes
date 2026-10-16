---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Sample introduction beyond laser ablation

**Goal:** choose the physical route from sample to plasma before selecting the mass-spectrometer settings. Complements notes 02–03.

## Cell design is part of the measurement

A cell must capture the laser plume, exchange gas reproducibly and transport material from different sample positions. A large nominal flow does not guarantee rapid, position-independent washout: dead volumes, recirculation, tubing junctions and particle deposition can preserve a long tail. A local collection region or two-volume cell can concentrate the flow near ablation while retaining a larger sample enclosure. Treat these as design ideas, not specifications of the course's installed laser.

For a perfectly mixed gas volume $V_c$ with volumetric flow $Q_g$, a first estimate is $\tau=V_c/Q_g$. **Synthetic example:** 1 cm³ and 1 L min$^{-1}$ give 60 ms. This is neither a universal cell washout time nor a particle-transport calculation. Real streamline capture can be faster, while tails and deposition can be slower. Measure a single-shot impulse response at multiple cell positions and for representative matrices. The observed boundary response also includes the crater footprint and plasma/acquisition response.

## Three other routes

| Route | Transformation before ICP | What can set the observed time resolution? |
|---|---|---|
| Solution nebulisation | Pumped liquid becomes droplets; a spray chamber removes much of the coarse aerosol | Tubing dispersion, mixing, spray-chamber response, memory and saved integration |
| Suspended particles through a nebuliser | Particles travel within a droplet aerosol | Particle-dependent transport, losses, aggregation and event overlap |
| Direct aerosol inlet | Airborne particles enter a controlled carrier stream | Inlet size selection, line deposition, residence-time spread and flow stability |
| Direct gas/vapour introduction | A suitable gas/vapour enters a controlled introduction system | Transfer volume, adsorption/desorption and species-specific delivery |

A conventional nebuliser uses liquid and gas flow to generate droplets; a spray chamber restricts the solvent/large-droplet load reaching the plasma and drains waste. Changing droplet production or chamber conditions changes delivery and plasma loading, not only sensitivity. Dry LA aerosol and wet solution aerosol need not give identical ionisation/transmission responses. “Direct” still has an inlet response function and is not a synonym for quantitative transport. Gas/vapour introduction only addresses species compatible with that method; it does not make all elements volatile.

A concrete published example is Stoll et al. (2026): their Nu Vitesse particle work used a concentric nebuliser and cooled cyclonic spray chamber, with uptake and transport calibration documented. It shows why solution introduction remains a separate part of a ToF method. These are their experimental conditions, not prescribed course settings. [Primary methods](https://tc.copernicus.org/articles/20/663/2026/tc-20-663-2026.html).

## Translate a concentration into delivered mass

For a homogeneous dissolved analyte, define mass concentration $C_e$, liquid uptake $Q_l$ and dissolved-analyte delivery efficiency $\eta_{e,l}$. An illustrative mass-balance model is

$$\dot m_{e,\mathrm{ICP}}=C_e Q_l\eta_{e,l}.$$

With $C_e=10$ ng mL$^{-1}$, $Q_l=0.20$ mL min$^{-1}$ and $\eta_{e,l}=0.05$, delivery is 0.10 ng min$^{-1}$, or 1.67 pg s$^{-1}$. Counts add isotope abundance, atom-number conversion, ionisation, transmission and detection. The liquid efficiency is not automatically the particle-number efficiency or solvent efficiency. [Bolea and Laborda's transport-efficiency analysis](https://doi.org/10.1016/j.sab.2024.106941) explicitly separates what each calibration method measures.

For an airborne aerosol of number concentration $C_{n,g}$, sample-gas flow $Q_g$ and particle delivery efficiency $\eta_{n,g}$, the ideal number arriving in time $T$ is $N=C_{n,g}Q_g\eta_{n,g}T$. Use matched volume units and reference temperature/pressure where needed. Do not substitute a liquid uptake rate into an air-volume calculation.

## Pilot tests and blanks

1. Measure a blank of the actual carrier/sample medium and a preparation/container blank. A gas blank does not test water preparation contamination.
2. Introduce a step or isolated impulse and measure delay, rise, tail and recovery; repeat at different loadings.
3. Check a rinse sequence after a high-concentration sample. A declining tail can look like continuing environmental events.
4. Compare a dissolved standard, a particle reference and an independent material as appropriate. Describe which efficiency is inferred from each.
5. Test dilution and recovery before interpreting a size distribution or rare chemical class.

**Choose by question:** use LA for spatially located solid domains, solution introduction for homogenised material where digestion/dissolution is part of the measurand, and validated aerosol/particle introduction for intact particle-event questions. Digestion removes spatial and particle identity; suspension sampling can select which particles survive preparation and transport.

**Course question:** which installed cell/inlet is demonstrated, how was its response measured, and which change in introduction mode requires retuning or recalibration?


[Home](index.md)
