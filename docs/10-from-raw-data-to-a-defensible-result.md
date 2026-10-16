---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# From raw data to a defensible result

[Home](index.md) · [Previous](09-geochronology-petrochronology-and-rock-magnetism.md) · [Next](11-worked-exercises.md)

**Goal:** know what must happen before a colourful image becomes a measurement. Suggested study time: 12 minutes.

## First identify what “raw” means

There are several possible starting points:

- Digitized detector waveform indexed by flight time and extraction event
- Accumulated mass-profile spectra
- Integrated isotope counts or count rates indexed by acquisition time
- Per-shot/per-pixel signals with geometry metadata
- Already calibrated concentration or age maps

These are not interchangeable. If only selected isotope intensities were exported, one cannot necessarily re-fit a mass peak or inspect a newly suspected interference later. Ask what the acquisition archive retains separately from the convenient exported dataset.

## Processing chain and checkpoints

1. **Preserve originals and provenance.** Record instrument/method version, run order, laser settings, gas/cell conditions, standards, reference values, and exports. Keep processing decisions reproducible.
2. **Convert detector data using validated instrument processing.** Inspect baseline, mass calibration/drift, peak shape and integration/deconvolution, saturation, and response corrections. This stage may occur in vendor software before Iolite sees isotope time series.
3. **Check units and timing.** Counts, cps, volts, and calibrated analog equivalents differ. Confirm start times, integration duration, gaps, laser shot triggers, and the delay between ablation and signal arrival.
4. **Define gas blanks and signal regions.** Avoid plume tails in blanks. Inspect whether a single baseline is defensible for the whole run.
5. **Apply the intended response/ratio calibration.** Use the correct reference values and appropriate internal-standard concentrations or U–Pb scheme. Inspect calibration residuals, not only final output.
6. **Validate independent reference materials.** Reconstruct them with the same integration and spatial choices used for unknowns. Report precision and accuracy separately.
7. **Construct spatial geometry.** Associate signal with actual shot/stage coordinates, line direction, spacing, and blank intervals. Test the registration against a sharp known boundary or image feature.
8. **Define geological regions.** Combine chemistry with petrography. Record masks and exclusion reasons before interpreting domain dates or trends.
9. **Estimate uncertainties at the level of the question.** Include shared calibration and background terms. Adjacent pixels may be correlated because they share plume material, smoothing, and corrections.
10. **Export an auditable result.** Include units, analytical detection/quantification limitations, source data identifiers, uncertainties/covariances as appropriate, calibration details, and a map of excluded/saturated pixels.

This is a conceptual workflow. The course’s provided workflow and file formats should determine the actual software steps.

## Iolite preparation that is directly relevant

The official Iolite Vitesse guide describes a NuQuant/CoDaq export route using an imaging conversion and NICE script before downstream import. Consequently, do not assume the hands-on exercise starts from raw flight-time waveforms. The same documentation stresses timing metadata and laser logs for meaningful time-resolved reduction. [Official Vitesse import/export guidance](https://iolite.xyz/docs/import_prep/exporting_data_from_instruments.html#nu-instruments-vitesse)

Iolite’s U–Pb tutorial uses beam time as a proxy for down-hole evolution and examines calibration fits and secondary-reference QA/QC. A spot-based correction should not be transferred automatically to pulse-resolved maps with a different sampling history. Ask which course scheme handles that difference. [Official U–Pb tutorial](https://iolite.xyz/docs/tutorials/upb.html)

The imaging tutorial is the appropriate reference for image construction and regional interrogation; use the sample dataset’s actual geometry rather than a generic assumed raster. [Official imaging tutorial](https://iolite.xyz/docs/tutorials/imaging.html)

## A symptom-driven troubleshooting checklist

- **Horizontal or scan-direction tails:** inspect washout, synchronization, and line turnaround.
- **Periodic stripes:** compare laser repetition, saved-bin intervals, stage speed, and trigger timing.
- **Ratios change with signal intensity in a reference:** test saturation, gain/nonlinearity, and mass/peak-shape drift.
- **All element concentrations move together:** inspect assumed internal standard, ablated mass, and shared drift.
- **Only one isotope misbehaves:** inspect its interferences, peak integration, and background.
- **Dates follow U concentration or pulse history:** investigate matrix/fractionation effects before asserting a geological relationship.
- **Unexpectedly precise region means:** inspect shared systematic uncertainty and pixel correlation.

## Single-particle data need an extra inference layer

A transient multielement event may represent one particle, overlapping particles, or a detection artifact. Event definition, coincidence windows, background thresholds, and dilution affect the result. For a homogeneous spherical particle of known composition and density,

$$m_p=\frac{m_{e,p}}{w_e},\qquad
 d=\left(\frac{6m_p}{\pi\rho}\right)^{1/3}.$$

Here $m_{e,p}$ is calibrated element mass and $w_e$ its mass fraction. Diameter is model-dependent, not directly measured by the ToF flight time. Particle number concentration additionally requires sample uptake, transport efficiency, acquisition time, and detection-efficiency treatment. Keep this distinction in mind for the course’s aerosol session.



For event thresholds, coincidence, particle-number calibration and non-target screening, see [19 Single Particles Aerosols and Non Target Screening](19-single-particles-aerosols-and-non-target-screening.md).
