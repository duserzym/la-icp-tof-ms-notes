---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# The measurement chain

[Home](index.md) · [Next](02-laser-ablation-and-particle-production.md)

**Goal:** connect every attractive feature in a map to the physical transformations that produced it. Suggested study time: 8 minutes.

## What is being measured

The common ordering is LA–ICP–ToF–MS: laser ablation supplies sample, an inductively coupled plasma supplies ions, and time-of-flight analysis sorts ions by mass-to-charge ratio. “LA–ToF–ICP–MS” is also encountered informally, but it does not mean ions pass through ToF before the plasma.

```text
Mineral and spatial domain
    ↓ laser–solid coupling
Particles, droplets, vapour, and condensate
    ↓ carrier gas and transfer system
Aerosol arriving at the plasma
    ↓ vaporization, atomization, ionization
Mixture of atomic ions, neutrals, and molecular species
    ↓ sampler, skimmer, lenses, optional cell/filter
Continuous ion beam
    ↓ repeated orthogonal extraction
Ion packets sorted by flight time
    ↓ detector and electronics
Mass spectra indexed by acquisition time
    ↓ calibration, synchronization, quality control
Concentration maps, isotope ratios, and interpreted dates
```

The laser pulse is a sample-generation event. The ToF extraction pulse is a mass-analysis event. There are generally many extraction pulses per laser event. Confusing these is the fastest route to misunderstanding an instrument’s advertised speed.

## Original manufacturer layout: Nu Vitesse

*Figure not reproduced here (© Nu Instruments / AMETEK): see the [Vitesse brochure, printed pages 4–5](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Brochure/Brochure_Vitesse.pdf).* The drawing begins at the ICP; the laser ablation cell is upstream and outside this cutaway. Follow plasma → focusing optics → quadrupole/bypass → reaction cell → attenuator → folded ToF analyser. [Original manufacturer PDF](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Brochure/Brochure_Vitesse.pdf).

Explore the clickable components and original sources in [15 Instrument Illustrations](15-instrument-illustrations.md).

## A useful forward model

Imagine a homogeneous small volume with ablated mass rate $\dot m$, elemental mass fraction $C_e$, isotope fraction $f_i$, and element molar mass $M_e$. The ideal detected rate for isotope $i$ has the scale

$$
I_i \approx \dot m\,C_e\,\frac{N_A}{M_e}\,f_i\,
\eta_{\rm transport,i}\eta_{\rm ion,i}\eta_{\rm interface,i}
\eta_{\rm optics,i}\eta_{\rm sampling,i}\eta_{\rm detection,i}.
$$

Consistent units matter: if $\dot m$ is g s$^{-1}$, use $M_e$ in g mol$^{-1}$. The efficiencies are not necessarily constant or independent. This factorization is a bookkeeping model, not a claim that the apparatus can be perfectly decomposed into separately measured efficiencies.

For a changing sample, add a response function:

$$
y_i(t)=b_i(t)+\int h_i(t-t')\,s_i(t')\,dt'+\epsilon_i(t).
$$

Here $s_i$ represents the ideal isotope input, $h_i$ combines transport and instrument response, $b_i$ is background, and $\epsilon_i$ is measurement noise. This linear model is a first approximation; saturation, changing plasma load, and matrix-dependent ablation can make it fail.

## Why this helps with experimental design

- A small crater constrains the sampled volume, but poor washout can mix it with the previous crater’s signal.
- More efficient ablation may produce more material but also change particle sizes and plasma loading.
- More counts can improve counting precision while leaving an incorrect relative sensitivity unchanged.
- A flat background subtraction cannot remove an overlapping oxide peak that changes with the sample.
- A ratio cancels shared multiplicative variation only to the extent that its numerator and denominator genuinely share it.

Your U–Pb intuition remains useful: traceability, blank control, isotope-ratio uncertainty, and standards still matter. The extra issue here is a time-dependent solid-sampling transfer function. A ToF analyzer does not remove that transfer function.

**Check yourself:** if a U signal falls halfway through an ablation, name four possible causes before deciding that U concentration fell. Examples: lower ablated mass, transport change, ionization/transmission change, and real zoning.

Related: [03 Aerosol Transport and Temporal Resolution](03-aerosol-transport-and-temporal-resolution.md), [08 Calibration and Matrix Effects](08-calibration-and-matrix-effects.md).

Sources for the basic physical chain: [Agilent’s LA-ICP-MS fundamentals](https://www.agilent.com/cs/library/flyers/public/flyer-laser-ablation-basics-icp-ms-5994-5193en-agilent.pdf). The equations and diagnostic examples above are explanatory models developed here.
