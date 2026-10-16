---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Worked exercises

[Home](index.md) · [Previous](10-from-raw-data-to-a-defensible-result.md) · [Next](12-glossary-and-equation-sheet.md)

All examples are synthetic. Work them with a calculator or implement them in Julia/Python. No instrument data or fitted instrument constants are implied.

## 1  Flight-time scaling

An ion at $m/z=50$ takes 10 μs of effective flight time. What time does $m/z=200$ require? What happens if the accelerating potential doubles?

**Answer:** $10\sqrt{200/50}=20$ μs. Doubling voltage divides each time by $\sqrt2$. The measured trigger-to-arrival interval also contains any fixed $t_0$, which must not be scaled blindly.

## 2  Turning timing width into resolving power

At effective flight time 20 μs, a peak has 2 ns FWHM. Find resolving power and mass width at mass 200.

**Answer:** $R=20\times10^{-6}/(2\times2\times10^{-9})=5000$. Then $\Delta m=200/5000=0.040$ Da. This width is not mass accuracy.

## 3  Laser energy and sampled mass

A 20 μm diameter top-hat spot runs at 3 J cm$^{-2}$. What pulse energy does that imply? If diameter halves at fixed fluence and removed depth, what happens to counts and ideal relative counting uncertainty?

**Answer:** area $=\pi(10^{-3}\,\mathrm{cm})^2=3.142\times10^{-6}$ cm², so energy is 9.42 μJ. Half diameter gives quarter area, mass, and counts under the stated assumptions; relative counting uncertainty doubles.

## 4  Washout and cross-talk

A single-shot tail is $e^{-t/\tau}$ with $\tau=2$ ms. Estimate the residual amplitude at the next shot for 100 Hz and 500 Hz. What is the characteristic smear distance at 200 μm s$^{-1}$?

**Answer:** 0.67% and 36.8%, respectively. Smear scale $v\tau=0.4$ μm. These are properties of the assumed exponential model; an instrument’s quoted FWHM is not automatically $\tau$.

## 5  Is the weak isotope the bottleneck?

A pixel yields 100 numerator counts and 10,000 denominator counts, without background. Calculate the ideal ratio precision. Compare doubling the denominator with quadrupling both signals.

**Answer:** initial relative standard deviation is $\sqrt{1/100+1/10000}=10.05\%$. Doubling the denominator gives 10.02%, almost no gain. Quadrupling both signals gives 5.025%. Improving the scarce isotope or pooling a justified domain is more valuable than increasing the already strong channel.

## 6  Blank-subtracted counts

A 10 ms sample window has 120 counts. A 100 ms blank window has 200 counts. Find net counts and their standard deviation using independent Poisson statistics.

**Answer:** $\alpha=0.1$, net $=120-0.1(200)=100$. Variance $=120+0.1^2(200)=122$, standard deviation $\approx11.05$ counts. The naïve $\sqrt{100}=10$ ignores uncertainty contributed by gross counts and blank measurement.

## 7  An internally standardized concentration

Reference analyte concentration: 100 μg g$^{-1}$. Reference internal-standard concentration: 20 wt%. Reference signal ratio: 0.010. Unknown internal standard: 10 wt%. Unknown signal ratio: 0.004. Find the unknown analyte concentration. What if the unknown internal standard was actually 8 wt%?

**Answer:** calculated value is 20 μg g$^{-1}$. With the correct 8 wt%, it is 16 μg g$^{-1}$. The erroneous assumption was 25% too high relative to the true internal standard and therefore made the analyte result 25% too high.

## 8  Pixel pitch versus resolution

You scan at 100 μm s$^{-1}$, save every 5 ms, and use a 5 μm beam. What is the saved pitch? Can you claim 0.5 μm spatial resolution? How long is a 1 mm line before turnaround?

**Answer:** pitch is 0.5 μm, but the beam alone is ten times wider. Independent spatial resolution is not 0.5 μm. The line takes 10 s; a 1 mm × 1 mm area with 5 μm line spacing needs about 200 such lines, approximately 33 minutes before standards, blanks, and overhead. This is a continuous-scan estimate; a pulse-resolved strategy can differ.

## 9  Which uncertainties shrink when pooling?

There are 100 equivalent pixels, each with 10% independent error and the same 2% calibration error. Calculate the uncertainty of the pooled result assuming equal weighting and no other correlation.

**Answer:** independent part is $10/\sqrt{100}=1\%$; combined is $\sqrt{1^2+2^2}=2.24\%$. If transport or smoothing correlates pixels, even the 1% independent estimate can be too optimistic.

## Optional modeling challenges

### A  Simulate spectral skew

Generate a common Gaussian or exponential transient for two isotopes with a fixed true ratio. Sample them either together or at alternating times. Add Poisson counts. Compare ratios calculated from individual bins and from full-event integrals. Separate timing bias from count noise.

### B  Simulate a two-domain grain

Make a one-dimensional composition step, convolve it with a measured-looking asymmetric pulse response, then bin it at several output intervals. Plot the true boundary, recorded signal, and apparent ratio. Reverse scan direction. Ask which features survive a change in scan speed.

### C  Test a regional age estimator

Generate pixels from one ratio and then from two mixed ratios. Compare mean pixel ratio, ratio of summed signals, and a likelihood-based common-ratio estimate. Include background and zero denominator bins. Track how the answer changes with selection thresholds rather than silently dropping failed ratios.

### D  Make systematic error visible

Run a Monte Carlo with independent Poisson counts and one shared calibration multiplier per synthetic session. Compare the variance of a 100-pixel mean with a model that incorrectly redraws calibration independently for every pixel.

These exercises are intentionally small forward models. They are not replacements for the data-reduction workflow supplied with a given dataset.
