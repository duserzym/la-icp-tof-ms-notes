---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Plasma interface and ion optics

[Home](index.md) · [Previous](03-aerosol-transport-and-temporal-resolution.md) · [Next](05-time-of-flight-from-first-principles.md)

**Goal:** understand how solid particles become a usable ion beam and why the beam is not an unbiased miniature of the rock. Suggested study time: 12 minutes.

## What the ICP does

The RF field sustains an argon plasma. Material entering the central channel is heated, vaporized, atomized, and ionized through collisional processes. These are different steps: a hot plasma does not guarantee that every large particle is completely vaporized within its finite residence time.

The output is predominantly useful atomic positive ions for many analytes, plus neutrals, plasma/background ions, molecular ions, and multiply charged ions. Ionization fraction depends on the element and conditions. The ICP largely destroys the original mineral’s molecular structure. An elemental Fe measurement is not a measurement of Fe²⁺/Fe³⁺ in the original solid, nor of magnetization.

Primary work on doubly charged ion production discusses the high-temperature analytical zone and the dependence of charge-state populations on ionization energy and plasma conditions. [Study](https://doi.org/10.1016/S0584-8547(01)00301-9)

## Saha equilibrium as physical intuition

For the first ionization stage under local thermodynamic equilibrium,

$$
\frac{n_{M^+}n_e}{n_{M^0}}
=\frac{2Z_{M^+}}{Z_{M^0}}
\left(\frac{2\pi m_e k_BT}{h^2}\right)^{3/2}
\exp\left(-\frac{\chi_1}{k_BT}\right).
$$

$n_e$ is electron number density, $Z$ are partition functions, and $\chi_1$ is first ionization energy. This displays why temperature and electron density matter, and why different elements do not have identical ionization fractions.

**Interpret carefully:** this is not a turnkey quantitative ICP-MS calibration equation. The sampled plasma is spatially structured, particles have finite heating times, and extraction can alter what reaches the analyzer. Equilibrium assumptions and effective temperature definitions must be examined. Direct optical and mass-spectrometric measurements have been used to test such assumptions near the sampler. [Primary comparison](https://www.sciencedirect.com/science/article/pii/S0584854701002026)

**Synthetic intuition:** $k_BT$ is approximately 0.60 eV at 7000 K. That does not mean a 7 eV ionization threshold prevents ion formation: the electron energy distribution has a tail, and the full equilibrium relation contains more than the exponential. Do not equate $k_BT$ with a hard maximum collision energy.

## Getting from atmospheric pressure to high vacuum

A sampler cone admits a small part of the plasma into a pumped region. Expansion through the interface produces a directed jet; a skimmer samples it, and ion optics transmit a useful beam toward the analyzer. Differential pumping makes this pressure transition possible. Most of the original material never becomes a detected ion. [Official cone overview](https://www.agilent.com/en/promotions/icp-ms-cone-selection-guide)

Electrostatic lenses act on charged particles, allowing focusing and deflection away from many neutrals and photons. Transmission depends on ion energy and angular distributions, not just elemental concentration.

Space-charge forces are Coulomb repulsion within a dense beam. Strong matrix ion populations can affect analyte trajectories and transmission. The susceptibility is mass-, energy-, and design-dependent; it is unsafe to assume a single correction factor fixes all matrices.

## Original instrument layout: plasma, interface and optics

*Figure not reproduced here: see Nu's [Vitesse brochure, pages 4–5](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Brochure/Brochure_Vitesse.pdf).* Nu’s original Vitesse cutaway shows the source-to-analyser sequence and focusing optics; it is not a detailed pressure-stage or cone cross-section. Original artwork © Nu Instruments / AMETEK, brochure pages 4–5. [Manufacturer PDF](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Brochure/Brochure_Vitesse.pdf).

Explore the clickable components and original sources in [15 Instrument Illustrations](15-instrument-illustrations.md).

## Collision/reaction cells and mass filters

A collision cell can reduce kinetic-energy spread and some interferences. A reaction cell changes ion chemistry and may move an analyte to a product-ion mass. These benefits come with possible scattering losses, new products, and temporal broadening. A broad multielement method must find conditions that work acceptably for many channels together.

The Vitesse uses a segmented reaction-cell design; Nu’s single-particle study shows that cell optimization affects both low-mass transmission and transient shape. [Manufacturer’s measured example](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Notes/App-Note_Vitesse_NT04_Optimizing-instrumental-data-collection-and-signal-processing-parameters.pdf)

## Removing the argon load: pumping, chemistry and ion blanking

“Blanking argon” does **not** mean interrupting the carrier-gas flow or switching off the plasma. Differential pumping removes most of the sampled gas, while electrostatic optics transmit the charged beam. The remaining beam can still contain enough plasma-derived ions to overload the detector. Gas removal and selective ion rejection solve different problems.

In the documented **Vitesse** architecture, a **Bradbury–Nielsen ion blanker lies between orthogonal extraction and the reflectron**. Flight-time separation makes it possible to apply a deflecting electric field when an unwanted mass-to-charge packet crosses the gate. The rejected ions leave the accepted beam path before reaching the MagneTOF. This is distinct from the general upstream beam attenuator shown in Nu’s brochure. [Primary Vitesse study](https://doi.org/10.1039/D3JA00288H)

The sequence is: **ICP → sampler/skimmer and pumping → ion optics / reaction cell → attenuator → orthogonal extraction → timed ion blanker → reflectron → detector**. The exact installed configuration and settings must still be confirmed; the full methods of Adamson et al. (2026) have not been verified accessible.

A reaction cell can reduce selected argon-based interferences by chemistry before extraction; a blanker rejects ions by their arrival time after extraction. These are complementary. A mass-40 blanking window can suppress calcium as well as argon; chemistry may permit measurement of an analyte that a broad gate window would exclude. [Nu’s interference-removal discussion](https://www.nu-ins.com/Products/TOF-ICP-MS/Introduction-to-TOF)

Other architectures differ: TOFWERK icpTOF uses a **quadrupole notch filter upstream of ToF extraction** to selectively excite and attenuate chosen mass regions in the continuous beam. Do not identify that filter with Vitesse’s timed wire gate. [Primary notch-filter description](https://doi.org/10.1039/D3JA00084B)

For the full gate physics, timing derivation, limitations and method-recording checklist, see [How the argon ion blanker works](06-detectors-noise-and-interferences.md#how-the-argon-ion-blanker-works). Explore **Argon blanker** in [the 3D model](15-instrument-illustrations.md) to vary the pulse delay and width and watch neighboring ions being transmitted or rejected.

**Useful tuning questions:** Which oxide and doubly charged ratios are monitored? Are those checks made in solution or during ablation? Which mass ranges are attenuated or excluded? Does the tuning target maximum counts, isotope-ratio stability, fast washout, or a compromise?

Related: [06 Detectors Noise and Interferences](06-detectors-noise-and-interferences.md), [08 Calibration and Matrix Effects](08-calibration-and-matrix-effects.md).
