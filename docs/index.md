---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# LA–ICP–ToF–MS fundamentals

An independent study guide prepared alongside the 2026 GSA Connects short course on ToF (October 2026). Course-derived instrument details are marked as such in the text. Written for geoscientists who know U–Pb geochronology and want the physical fundamentals of laser sampling, plasma ionisation, and ToF analysis. Julia/Python modeling exercises connect that intuition to quantitative experiments. It is not the course slide set or an instrument operating procedure.

**The central idea:** ToF measures many mass-to-charge channels from the same rapidly sampled ion population. That is extremely useful when the sample changes quickly. It does not make sampling stoichiometric, guarantee interference-free signals, or turn low counts into precise dates.

## Reading routes

Study times include working through equations and questions, rather than reading speed alone.

- **20-minute arrival catch-up:** [01 The Measurement Chain](01-the-measurement-chain.md), the first half of [05 Time of Flight from First Principles](05-time-of-flight-from-first-principles.md), and the four clocks in [07 Simultaneity Duty Cycle and Mapping](07-simultaneity-duty-cycle-and-mapping.md).
- **60-minute fundamentals route:** notes 01 → 02 → 03 → 04 → 05 → 07. Do exercises 1–4 in [11 Worked Exercises](11-worked-exercises.md).
- **Quantitative interpretation route, another 45–60 minutes:** notes 06 → 08 → 09 → 10, then exercises 5–9.
- **At the instrument:** keep [12 Glossary and Equation Sheet](12-glossary-and-equation-sheet.md) open and annotate the instrument-specific settings actually used.

## What you should be able to explain

1. Why accelerating ions through a common potential gives $t\propto\sqrt{m/z}$.
2. Why an ion mirror improves resolution rather than merely folding the instrument.
3. Why a microsecond spectrum does not automatically produce a microsecond sample response.
4. Why full-spectrum coverage, extraction duty cycle, and data-recording duty cycle are different.
5. Which biases cancel in a ratio and which survive.
6. Why a convincing date map needs independent reference-material checks and a geological interpretation of each domain.

## Note map

- [01 The Measurement Chain](01-the-measurement-chain.md): a forward model linking rock to counts
- [02 Laser Ablation and Particle Production](02-laser-ablation-and-particle-production.md): fluence, pulse length, sampling volume, fractionation
- [03 Aerosol Transport and Temporal Resolution](03-aerosol-transport-and-temporal-resolution.md): washout, convolution, cross-talk
- [04 Plasma Interface and Ion Optics](04-plasma-interface-and-ion-optics.md): atomization, ionization, sampling, transmission
- [05 Time of Flight from First Principles](05-time-of-flight-from-first-principles.md): derivation, focusing, resolution, mass calibration
- [06 Detectors Noise and Interferences](06-detectors-noise-and-interferences.md): counts, dynamic range, peak overlap
- [07 Simultaneity Duty Cycle and Mapping](07-simultaneity-duty-cycle-and-mapping.md): what “all elements at once” actually buys
- [08 Calibration and Matrix Effects](08-calibration-and-matrix-effects.md): converting counts into defensible composition
- [09 Geochronology Petrochronology and Rock Magnetism](09-geochronology-petrochronology-and-rock-magnetism.md): opportunities and limits
- [10 From Raw Data to a Defensible Result](10-from-raw-data-to-a-defensible-result.md): workflow and quality-control decisions
- [11 Worked Exercises](11-worked-exercises.md): numerical examples with answers
- [12 Glossary and Equation Sheet](12-glossary-and-equation-sheet.md): compact reference
- [14 Sources and Reading Guide](14-sources-and-reading-guide.md): primary papers and official documentation, with access notes

## Conventions

$m$ is ion mass, $z$ is the integer charge state, $q=ze$, $U$ is an accelerating potential, and $R=m/\Delta m$ is resolving power with the width definition stated. Intensities may be counts, count rates, or calibrated analog signal; do not mix them. Unless stated otherwise, uncertainties in worked examples are one standard deviation and count formulas assume ideal independent Poisson arrivals.

All numerical examples marked **synthetic** are teaching calculations, not measured performance of any particular laboratory. Manufacturer values are examples for specified models and settings, checked on 6 October 2026. Actual laboratory configurations can differ. Follow the laboratory’s training and safety procedures; these notes do not authorize changing hardware, gases, laser settings, or software.

## Interactive models

Two offline Three.js viewers accompany the notes: the [instrument viewer](figures/Instrument-3D.html) (mass separation, reflectron with a noisy ensemble, H₂/He collision cell, argon blanker, MagneTOF detector) and the [laser and ablation-cell viewer](figures/Laser-3D.html) (absorption, spontaneous and stimulated emission, two-volume cell). See [Interactive models](models.md).

## Visual reading route

For a diagram-first pass, follow the illustrated notes in order: measurement chain → laser sampling → aerosol transport → plasma/interface → ToF and reflectron → peak resolution → acquisition clocks. Third-party manufacturer and literature figures are linked rather than reproduced; the plots here explain idealized response models. Start with [the illustrations note and offline 3D viewers](15-instrument-illustrations.md).

## Extensions

Further notes address solution/direct aerosol introduction, tuning and mass drift, single particles and non-target screening, and mineral-specific U–Pb/Th–Pb and ore mapping.

- [17 Sample Introduction Beyond Laser Ablation](17-sample-introduction-beyond-laser-ablation.md)
- [18 Tuning Mass Drift and Interference Strategy](18-tuning-mass-drift-and-interference-strategy.md)
- [19 Single Particles Aerosols and Non Target Screening](19-single-particles-aerosols-and-non-target-screening.md)
- [20 Mineral Dates Ore Systems and Internal Standards](20-mineral-dates-ore-systems-and-internal-standards.md)

