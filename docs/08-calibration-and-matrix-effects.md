---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Calibration and matrix effects

[Home](index.md) · [Previous](07-simultaneity-duty-cycle-and-mapping.md) · [Next](09-geochronology-petrochronology-and-rock-magnetism.md)

**Goal:** keep three calibrations separate and identify what each can correct. Suggested study time: 12 minutes.

## Three distinct calibrations

1. **Mass-axis calibration:** flight time → $m/z$. It places peaks correctly.
2. **Response calibration:** signal → elemental concentration or amount. It accounts for sensitivity and sampling.
3. **Ratio calibration:** measured isotope/element ratio → reference-traceable ratio. It accounts for mass bias and, for Pb/U, relative elemental fractionation.

Perfect mass calibration does not imply accurate concentration, and precise repeated ratios can all share the same offset.

## Internal-standard normalization

Let background-corrected intensity obey $I_i=gk_iC_i$, with shared sampling factor $g$ and element-specific response $k_i$. For an internal standard $s$,

$$\frac{I_i}{I_s}=\frac{k_i}{k_s}\frac{C_i}{C_s}.$$

Using a reference material and an independently known internal-standard concentration in the unknown,

$$
C_{i,u}=C_{s,u}
\frac{(I_i/I_s)_u}{(I_i/I_s)_{rm}}
\frac{C_{i,rm}}{C_{s,rm}}.
$$

The derivation reveals the assumption: relative response $k_i/k_s$ must transfer from reference to unknown, with drift appropriately interpolated. Dividing by an internal standard does not force that assumption to be true.

**Synthetic example:** the reference contains 100 μg g$^{-1}$ analyte and 20 wt% internal-standard element; its signal ratio is 0.010. The unknown has independently established 10 wt% internal standard and a ratio of 0.004. Then the analyte concentration is $100\times(10/20)\times(0.004/0.010)=20$ μg g$^{-1}$. Concentration units within each corresponding ratio must match.

If the assumed unknown internal-standard concentration is 20% too high, its calculated analyte concentration is also 20% too high under this model. An internal standard varying across a multiphase map therefore needs phase- or pixel-appropriate treatment.

## External normalization and drift

Repeated reference measurements bracket unknowns in time. Fit a response-versus-time model justified by the data. A flexible spline can follow noise; a straight line can miss a step change. Inspect residuals and use independent validation materials that were not used to define the correction.

Iolite’s Trace Elements DRS provides background subtraction, external standardization, and optional internal-standard normalization. Its official guided example uses multiple minerals and independent reference materials, making it a useful pre-course processing exercise. [Official guide](https://iolite.xyz/docs/tutorials/traceelements.html)

## Pb/U calibration is not just isotope mass bias

A useful schematic for a ratio is

$$R_{\rm obs}(t,d)=R_{\rm true}\,b_{\rm instrument}(t)\,b_{\rm sample}(d,\mathrm{matrix},\mathrm{laser}),$$

with session time $t$ and pulse-history/depth coordinate $d$. Real dependencies can interact. Standard-sample bracketing constrains the product for the reference; applying it to an unknown assumes that the relevant sample-dependent part transfers.

For isotopes of one element, an empirical mass-fractionation law might be written $r_{\rm obs}=r_{\rm true}(m_1/m_2)^\beta$. That is a chosen calibration law, not a universal description of all LA fractionation. It does not by itself correct different ablation or ionization of Pb and U.

For zircon, similar major-element composition does not prove identical physical behaviour. Radiation damage, inclusions, crater evolution, and microstructure can matter. Adamson et al.’s (2026) particle study is directly relevant to testing this assumption; see [02 Laser Ablation and Particle Production](02-laser-ablation-and-particle-production.md).

## Tests that can falsify a reassuring calibration

- Treat a second reference material as unknown, with the same geometry and pixel/binning choices.
- Compare residual ratios against signal size, U concentration, ablation time, and run order.
- Reprocess with defensible alternative background and integration windows.
- Check whether apparent chemistry changes after correcting an overlap or excluding saturated channels.
- Validate every mineral/matrix for which quantitative claims are made.
- Retain raw signals so rejected hypotheses can be revisited.

Do not call a map “quantitative” merely because its colour scale says ppm. State standards, assumed internal concentrations, drift treatment, interference treatment, and validation performance.


## A ToF-specific caution about isotope correction laws

Retzmann et al. (2023) found that isotope fractionation in their second-generation ICP-ToF measurements of B, Sr, and Pb did not consistently follow familiar mass-dependent laws. Standard-sample bracketing produced reliable ratios in the tested solutions. This supports a practical rule: validate the chosen correction for the instrument and isotope system rather than importing a TIMS or MC-ICP-MS law untested. It is not evidence that every ToF configuration has the same bias. [Primary study](https://doi.org/10.1039/D3JA00084B)
