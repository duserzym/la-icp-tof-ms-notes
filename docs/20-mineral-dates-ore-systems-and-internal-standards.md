---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Mineral dates, ore systems and internal standards

**Goal:** extend the zircon-focused discussion to the four minerals and trace-metal applications named in the course. The tables below are analytical planning prompts, not universal recipes or reproductions of the course's case studies.

## The missing Th–Pb clock

For radiogenic daughter after common-Pb treatment and the stated equilibrium/closed-system assumptions,

$$R_{\mathrm{Th}}=\frac{^{208}\!Pb^*}{^{232}\!Th}=e^{\lambda_{232}t}-1,
\qquad t=\frac{\ln(1+R_{\mathrm{Th}})}{\lambda_{232}}.$$

Measured $^{208}$Pb is not automatically radiogenic. U–Pb and Th–Pb together can add constraints, but share Pb calibration, common-Pb assumptions and geological history. They are not automatically independent estimates to average. Vermeesch (2020) presents joint U–Th–Pb/common-Pb modelling with covariance and examples including allanite and monazite; applicability depends on cogenetic domains and model assumptions. [Primary paper](https://gchron.copernicus.org/articles/2/119/2020/).

**Synthetic calculation:** $R_{\mathrm{Th}}=0.0500$ and an illustrative $\lambda_{232}=4.9475\times10^{-11}$ yr$^{-1}$ give about 986.2 Ma. A 1% relative ratio uncertainty gives about 9.6 Ma from this ratio alone. This omits decay-constant, common-Pb and response uncertainties. Use the laboratory's documented constants and reporting conventions for real dates.

## Different minerals require different evidence

| Mineral | What a map can help distinguish | Planning checks before reporting dates |
|---|---|---|
| Zircon | Growth zones, inherited domains, inclusions, altered regions | Reference recovery; counts in young Pb channels; discordance; damage/alteration effects and sampling-volume mixing |
| Monazite | Chemically distinct growth/reaction domains, including Th/REE variation | Separate U–Pb and Th–Pb calibration checks; common Pb; phase-matched references; domain context |
| Titanite | Compositional zones and inclusion/alteration boundaries | Common-Pb model; matrix-dependent Pb/U response; domain-specific chemistry and geological meaning |
| Allanite | REE-rich growth/alteration patterns, potential Th–Pb constraints | U/Th/Pb signal adequacy; common Pb and mixed domains; suitable reference materials and model assumptions |

The value of this table is the question set, not a guarantee that every grain exhibits each problem. Chew et al. (2014) explicitly address common-Pb complications in accessory minerals including allanite and titanite. [Primary abstract](https://www.sciencedirect.com/science/article/abs/pii/S000925411300510X). A common-Pb correction needs a measured constraint, justified composition or appropriate regression; an arbitrary constant subtraction is not a substitute.

Define domains from independent texture/chemistry where possible, exclude mixed boundaries by a documented rule, apply time/matrix corrections before pooling, and propagate covariance into ratios and dates. Test independent references in the same acquisition/reduction regime. Pixels that share one standard do not provide independent calibration experiments. See note 09 for the distinction between ratio-of-sums and mean-of-ratios.

## Sulfide and oxide maps: abundance is not yet concentration

A multielement map can show co-located zoning and minor phases. A smooth trace-metal halo might instead arise from washout at a high-signal boundary, saturation, a moving internal-standard assumption or registration error. Compare petrography, line direction, alternative isotopes and raw time series before proposing ore-fluid evolution or exploration vectoring.

A trace spike coincident with several elements can suggest an inclusion. It can also be a transport event or a mixed ablation volume. Test repeat tracks, crater images and mineralogical evidence; do not equate a transient chemical association with crystallographic substitution.

## Choose an internal standard by phase and measured composition

In ratio normalisation, a concentration estimate is proportional to the assumed internal-standard mass fraction. A global Fe, Ca or Si concentration therefore injects a phase-composition model into every pixel. An element that is useful in one phase can be absent, saturated or chemically variable in another.

| Domain | Candidate basis to evaluate | Why one fixed value can fail |
|---|---|---|
| Phase-confirmed pyrite | Independently checked Fe mass fraction | Substitutions, mixed boundaries and non-pyrite inclusions |
| Magnetite/titanomagnetite assemblage | Measured Fe or another suitable major-element basis | Ti substitution, alteration and mixed oxides |
| Ca-bearing silicate | Phase-specific measured Ca | Zoning, inclusions, phases without Ca |
| Mixed sulfide/oxide raster | Phase masks and independently measured values, or another validated strategy | One major-element assumption cannot represent all phases |

**Synthetic pyrite example:** ideal FeS$_2$ with illustrative atomic weights 55.845 and 32.06 gives $w_{\mathrm{Fe}}=55.845/(55.845+2\times32.06)=0.4655$. If a calculation instead assumes 0.70 for the same true signal, concentrations scale by $0.70/0.4655\approx1.50$: a 50% bias before other errors. If that raster crosses into a different mineral, the pyrite assumption itself must be reconsidered. A formula value is not an EMPA measurement.

For a validated internal-standard-free or mass-sum approach, state required detected elements, unknown/unmeasured constituents and the calibration model. Summing a restricted set of mass channels to 100% can manufacture apparent closure. Oxygen and sulfur response, phase-dependent ablation, glass-versus-sulfide calibration and saturation all need explicit evaluation.

**Pilot design:** map one well-characterised zoned grain, acquire independent major-element data, calibrate with an appropriate material and hold another out for validation. Compare the map under independently defensible internal-standard assignments and check whether the proposed geological pattern survives. The official Iolite trace-element tutorial supports phase-specific internal-standard values and independent-reference testing; the choices in this table are proposed extensions to ore/oxide questions. [Official tutorial](https://iolite.xyz/docs/tutorials/traceelements.html).


[Home](index.md)
