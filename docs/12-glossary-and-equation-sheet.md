---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Glossary and equation sheet

[Home](index.md) · [Previous](11-worked-exercises.md) · [Next](14-sources-and-reading-guide.md)

## Language that prevents misunderstandings

- **Ablation:** removing solid material by laser irradiation.
- **Aerosol:** particles/droplets carried in gas; not necessarily representative of the bulk at every size.
- **Fluence:** laser energy per area per pulse.
- **Irradiance:** power per area; for a simple pulse-average, fluence divided by pulse duration.
- **Washout:** temporal decay/clearance of material from the introduction system; report its definition.
- **Impulse response:** signal produced by a sufficiently brief input event.
- **ICP:** inductively coupled plasma, used here as an atomization/ionization source.
- **Sampler/skimmer:** interface elements that admit and transmit a small sampled plasma flow into vacuum.
- **Space charge:** electrostatic interaction within an ion population, affecting trajectories/transmission.
- **$m/z$:** mass-to-charge ratio, not mass alone.
- **Orthogonal acceleration:** pulsed extraction perpendicular to a continuously travelling ion beam.
- **Reflectron:** electrostatic ion mirror that can compensate flight-time dispersion caused by energy spread.
- **Extraction period:** interval between ToF start pulses.
- **Saved integration:** time accumulated into one stored spectrum or signal point.
- **Duty cycle:** an ambiguous phrase; specify mass coverage, ion sampling, or recording live time.
- **FWHM:** full width at half maximum of a peak.
- **Resolving power:** peak mass divided by its width under a stated criterion.
- **Mass accuracy:** closeness of assigned mass to the correct value.
- **Abundance sensitivity:** contamination near a strong mass peak by its tails.
- **Spectral skew:** ratio distortion from measuring changing signals at different times.
- **Dynamic range:** usable signal range under stated conditions; distinguish single-event from run-level range.
- **TDC/ADC:** time-to-digital / analog-to-digital conversion of detector output.
- **Isobaric interference:** ions with nearly identical mass-to-charge that overlap analytically.
- **Polyatomic interference:** a molecular ion overlapping an analyte channel.
- **Internal standard:** a sample component of known or assumed concentration used to normalize response.
- **External reference material:** measured material with assigned values used to calibrate unknowns.
- **Secondary reference material:** independent validation material; not merely another repeat of the calibrant.
- **Matrix effect:** response changes due to properties/composition of the material accompanying the analyte.
- **Mass bias/instrumental isotopic fractionation:** unequal instrumental response to isotopes.
- **Elemental fractionation:** unequal sampling/transport/processing of different elements, relevant to Pb/U.
- **DRS:** data reduction scheme in Iolite.
- **ROI:** region of interest; a geometric selection that still requires a geological justification.
- **Precision versus accuracy:** repeatability versus closeness to an accepted/true value.
- **Detection limit versus quantification limit:** evidence that a signal is present versus evidence that it can be quantified at the required reliability; criteria are method-specific.

## Equations to recognize

$$F=E_p/[\pi(d/2)^2],\qquad m_{\rm removed}=\rho\pi(d/2)^2h$$

$$y_i(t)=b_i(t)+(h_i*s_i)(t)+\epsilon_i(t)$$

$$\tfrac12mv^2=zeU,\qquad t_f=L\sqrt{m/(2zeU)}$$

$$m/z=[(t-t_0)/a]^2,\qquad R\simeq(t-t_0)/(2\Delta t)$$

$$D\sim\min(1,f_{\rm ext}\ell/v_z)\quad\text{simple orthogonal-sampling model}$$

$$p_x=v_s\Delta t_{\rm output},\qquad\ell_{\rm tail}\sim v_s\tau$$

$$\sigma_N/N=N^{-1/2},\qquad (\sigma_R/R)^2\simeq1/A+1/B$$

$$N_{\rm net}=S-\alpha B,\qquad\sigma_{\rm net}^2\simeq S+\alpha^2B$$

$$C_{i,u}=C_{s,u}\frac{(I_i/I_s)_u}{(I_i/I_s)_{rm}}\frac{C_{i,rm}}{C_{s,rm}}$$

$$t=\ln(1+R)/\lambda,\qquad\sigma_t\simeq\sigma_R/[\lambda(1+R)]$$

**Before using an equation, check its assumptions.** The Poisson expressions require suitable counting statistics; the concentration expression requires transferable relative response; the age expression requires a corrected radiogenic ratio and an appropriate geological system.
