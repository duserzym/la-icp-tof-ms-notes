---
topic: Geochemistry
tags:
  - geochemistry
  - mass-spectrometry
  - LA-ICP-ToF-MS
---

# Sources and reading guide

[Home](index.md) · [Previous](12-glossary-and-equation-sheet.md)

Checked 6 October 2026 during research and integration. Access descriptions record what was consulted; selected calibration, interference, and Iolite details were rechecked during local integration. Primary experimental papers and official documentation are emphasized. Manufacturer examples establish what a stated system did or advertises; they are not independent head-to-head comparisons. Educational derivations and synthetic exercises in this folder are original explanatory calculations, with assumptions shown.

## Read first

1. [Adamson et al. 2026, Chemical Geology 707, 123325](https://doi.org/10.1016/j.chemgeo.2026.123325), A Mechanistic study of matrix effects in zircon U-Th/Pb geochronology using single-particle laser ablation time-of-flight mass spectrometry. Publisher abstract/highlights consulted; full text was not verified accessible. Most directly tied to zircon matrix-effect fundamentals.
3. [Burger et al. 2017, JAAS 32, 1946–1959](https://doi.org/10.1039/C7JA00236J), Capabilities of laser ablation inductively coupled plasma time-of-flight mass spectrometry. Publisher abstract consulted; full HTML access failed. Compare its steady-state, single-pulse and imaging experiments without generalizing their limits to all setups.
4. [Iolite official documentation](https://iolite.xyz/docs/). Live documentation consulted. Start with [trace elements](https://iolite.xyz/docs/tutorials/traceelements.html), [U–Pb](https://iolite.xyz/docs/tutorials/upb.html), [imaging](https://iolite.xyz/docs/tutorials/imaging.html), and [instrument exports](https://iolite.xyz/docs/import_prep/exporting_data_from_instruments.html).

## Separation physics and detectors

- [Wiley & McLaren 1955, Review of Scientific Instruments 26, 1150–1157](https://doi.org/10.1063/1.1715212), Time-of-Flight Mass Spectrometer with Improved Resolution. [Institution-hosted PDF](https://masspec.scripps.edu/learn/ms/pdf/1955_WileyWC.pdf) was reachable; text extraction was unavailable, so historical description was checked through indexed excerpts. Primary classic on focusing.
- [Mamyrin et al. 1973, Soviet Physics JETP 37, 45–48](https://www.jetp.ras.ru/cgi-bin/dn/e_037_01_0045.pdf), The mass-reflectron, a new nonmagnetic time-of-flight mass spectrometer with high resolution. Full PDF text accessible. Primary classic on electrostatic energy focusing.
- [Myers et al. 1994, JASMS 5, 1008–1016](https://doi.org/10.1016/1044-0305(94)80019-7), An inductively coupled plasma-time-of-flight mass spectrometer for elemental analysis. Part I: Optimization and characteristics. Publisher abstract consulted. Useful for seeing ion-sampling duty cycle as a physical limitation; historical specifications are not modern benchmarks.
- [Gundlach-Graham et al. 2018, Analytical Chemistry 90, 11847–11855](https://doi.org/10.1021/acs.analchem.8b01551), Monte Carlo Simulation of Low-Count Signals in Time-of-Flight Mass Spectrometry and Its Application to Single-Particle Detection. Publisher indexed text and ETH-hosted paper excerpt consulted; direct publisher opening failed. Read for ADC gain statistics and low-count inference.
- [Retzmann et al. 2023, JAAS 38, 2144–2158](https://doi.org/10.1039/D3JA00084B), Performance of second generation ICP-TOFMS for (multi-)isotope ratio analysis. Publisher indexed full-text sections consulted; direct HTML opening was intermittent. Useful warning against assuming a standard mass-fractionation law is transferable.

## Sampling and quantitative geochronology

- [Guillong & Günther 2002, JAAS 17, 831–837](https://doi.org/10.1039/B202988J), Effect of particle size distribution on ICP-induced elemental fractionation in LA-ICP-MS. Publisher abstract consulted. Distinguishes particle generation from ICP processing.
- [Van Malderen et al. 2018, Spectrochimica Acta B](https://doi.org/10.1016/j.sab.2017.11.007), Considerations on data acquisition in laser ablation-inductively coupled plasma-mass spectrometry with low-dispersion interfaces. Publisher abstract/highlights consulted. Relevant to spectral skew and timing artifacts.
- [Davis & Rochin-Banaga 2026, Geochronology 8, 529–545](https://gchron.copernicus.org/articles/8/529/2026/), Causes and mitigation of U–Pb fractionation during LA-ICP-MS analyses of zircon using nanosecond excimer laser systems. Open full text consulted. Compare mechanistic interpretations critically with Adamson et al. (2026).
- [Horstwood et al. 2016, Geostandards and Geoanalytical Research 40, 311–332](https://doi.org/10.1111/j.1751-908X.2016.00379.x), Community-Derived Standards for LA-ICP-MS U-(Th-)Pb Geochronology. [Institutional open PDF](https://nora.nerc.ac.uk/id/eprint/513688/1/Horstwood_et_al-2016-Geostandards_and_Geoanalytical_Research.pdf), abstract/front matter consulted. Key reference for random versus systematic uncertainty and validation/reporting.
- [2026 GSA Connects abstract on LA-ToF zircon imaging](https://gsameetings.secure-platform.com/connects26/solicitations/103015/sessiongallery/schedule/items/96570/application/18891). Conference abstract consulted; not a full methods paper.

## Official instrument and reference resources

- [Nu introduction to ToF-ICP-MS](https://www.nu-ins.com/Products/TOF-ICP-MS/Introduction-to-TOF) and [Vitesse product page](https://www.nu-ins.com/Products/TOF-ICP-MS/Introduction-to-TOF/Vitesse). Pages consulted. The latter listed resolving power 3800 FWHM and acquisition speed below 80 μs per spectrum when checked. Confirm the actual installed configuration; these are vendor specifications, not measured course performance.
- [TOFWERK icpTOF specifications](https://www.tofwerk.com/products/icptof/specifications/). Page consulted. Listed different resolution/sensitivity tradeoffs across R, 2R and S2 models. Do not combine specifications from different models into a hypothetical best-of-all instrument.
- [Nu NT08, spectra accumulation and particle detection](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Notes/App-Note_Vitesse_NT08_Influence-of-spectra-accumulation-speeds.pdf). Full PDF text consulted. Separates extraction from accumulated output and illustrates event merging.
- [Nu NT04, collection and processing parameters](https://edge.sitecorecloud.io/ametekinc1236b-ametekb19a-productiondcfa-1d17/media/Project/Ametek/nu-instruments/Documents/Vitesse/Notes/App-Note_Vitesse_NT04_Optimizing-instrumental-data-collection-and-signal-processing-parameters.pdf). Full PDF text consulted. Cell tuning, transient shape, coincidence and quality checks.
- [ESL–Vitesse technical connection note](https://iolite.xyz/docs/_downloads/d772fcc89f8c6c4ebbd49e58c011b3a1/TvTuner_ESL_Vitesse_Guide.pdf). Full PDF text consulted. Useful for understanding synchronization and transport, not for untrained hardware adjustment.
- [Agilent LA fundamentals](https://www.agilent.com/cs/library/flyers/public/flyer-laser-ablation-basics-icp-ms-5994-5193en-agilent.pdf). Official educational brief, indexed text consulted.
- [NIST isotope masses database](https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses). Individual Fe, Ar, O, Rb, Sr, Hg and Pb tables consulted. Source for the illustrative interference separations; check the underlying mass evaluation/version for precision metrology.

## Detector sources added 10 October 2026

- [ETP 14DM572 MagneTOF Plus datasheet, revision A (2015)](https://a6e5e8fc1ad706fd1969-b6eded4adeadd283a6338023bbf1f6de.r62.cf4.rackcdn.com/eecf54836514652645e0c9909cd7324f18ee5597-14DM572MagneTOFPlusDatasheet.pdf): indexed manufacturer text consulted; direct PDF retrieval timed out. Model-specific pulse width, linear output limits, gain, bias, dark counts, pressure and dimensions. Installed detector model remains unconfirmed.
- [IMI TOF electron multipliers](https://lifescience.imiplc.com/product/tof-electron-multipliers): official supplier page consulted; emphasizes bespoke designs and typical specifications.
- [Simke et al. 2024, Evaluation of MagneTOF detector signals for the determination of many-ion bunches](https://doi.org/10.1016/j.ijms.2024.117337): [open full paper](https://epub.ub.uni-greifswald.de/files/14308/1-s2.0-S1387380624001489-main.pdf) accessed 10 October 2026, superseding the earlier abstract-only access. Identifies 14DM291H and acquisition conditions; distinguishes individual-pulse counting from calibrated integrated response for dense bunches.
- [ETP patent US6982428B2, Particle detection by electron multiplication](https://patents.google.com/patent/US6982428B2/en): primary design description consulted 10 October 2026. Grounding for crossed-field electron focusing, broad-to-small-area transport and the MagneTOF schematic cutaway; it does not establish the installed part's exact construction.
- [Feynman Lectures II, §29–8: motion in crossed electric and magnetic fields](https://www.feynmanlectures.caltech.edu/II_29.html#Ch29-S8): supports the analytic timing-insight view. The full-period, same-origin electron example is distinct from the actual detector's shaped lens.
- [Agilent analysis performance terms](https://icp-ms.help.agilent.com/en/HowTo/Help/Reference/Analysis_performance_terms.htm): official documentation consulted for configuration-dependent pulse/analog crossover and analog-equivalent count rates.
- [Thermo iCAP RQ technical note TN43399](https://tools.thermofisher.com/content/sfs/brochures/TN-43399-ICP-MS-iCAP-RQ-Linear-Dynamic-Range-TN43399-EN.pdf): full PDF text consulted; combined pulse/analog range from 0.1 to >$10^9$ cps equivalent.
- [Agilent 7500cx dynamic-range comparison (2008)](https://www.agilent.com/library/articlereprints/Public/5989_8396EN.pdf): indexed manufacturer text consulted for historical pulse-count-only versus combined pulse/analog ranges.
- [Nu Vitesse brochure (2021)](https://www.nu-ins.com/-/media/ameteknuinstruments/files/products/brochures/vitesse_2021.pdf?la=en&revision=9003d984-cc91-4469-b999-c03acd38b8ae): indexed official brochure text consulted; MagneTOF detection, recovery from over-range signals, and physical beam attenuation. No numerical detector dynamic-range ratio stated in the consulted text.

The **2 GS/s** and reported **200 kHz** settings come from the 2026 GSA Connects short course on ToF, rather than these publications. See [06 Detectors Noise and Interferences](06-detectors-noise-and-interferences.md) for the comparison and explicitly labelled charge-equivalent calculation.

## Argon blanking sources added 10 October 2026

- [Lockwood et al. 2024, Strategies to enhance figures of merit in ICP-ToF-MS](https://doi.org/10.1039/D3JA00288H): publisher-indexed methods and results consulted. Vitesse Bradbury–Nielsen gate location, restricted mass-window operation, and approximately 1 μs switching-related background disturbance in the tested configuration. This is not a universal recovery-time specification.
- [Brunner et al. 2012, A large Bradbury Nielsen ion gate with flexible wire spacing…](https://doi.org/10.1016/j.ijms.2011.09.004), [authors’ institutional PDF](https://web.stanford.edu/group/grattalab/Publications/BrunnerEtAl2012.pdf): indexed primary text consulted. Interleaved wire sets, equal-potential transmission, opposite-potential deflection, localized field and downstream ion interception.
- [Quantitative determination of intracellular miRNA content using dual gold and iron nanoreporters and single particle ICP-ToF–MS (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12129863/): primary instrumentation section consulted. Example Vitesse blanking intervals 24.5–30.5 and 38–47, together with reaction-cell conditions. Not the Adamson et al. (2026) experiment or the course configuration.
- [An electrospray/inductively coupled plasma dual-source time-of-flight mass spectrometer… (2009)](https://doi.org/10.1039/B816732J): indexed primary section on unwanted-ion deflection consulted. Argon-related saturation, adjacent-signal interference and detector lifetime. A different instrument, used to explain why pre-detector rejection is needed.
- [Analytical capabilities of LA-ICP-ToF-MS for ultra-fast 2D quantitative elemental mapping of micrometeorites (2024)](https://doi.org/10.1039/D3JA00335C): indexed primary instrumentation section consulted. TOFWERK upstream quadrupole notch filtering of Ar-related mass regions; distinguish this from the Vitesse timed blanker.

The new blanker animation is an **original idealized nominal-mass timing model**, not manufacturer CAD or a field solution. Gate-arrival times follow $t\propto\sqrt{m/z}$; wire voltages switch ideally; trajectories and interception are schematic. It does not simulate exact-mass discrimination, packet widths, switching-edge dynamics or electronic settling artifacts. Neither the animation nor these sources establishes the blanking settings in Adamson et al. (2026).

## Sources added 16 October 2026

**Detector pulse shape and integration (note 06)**

- [Single-ion area and compound Poisson–lognormal noise in ICP-TOFMS, JAAS 2025](https://pubs.rsc.org/en/content/articlehtml/2025/ja/d5ja00230c): search-indexed text consulted; publisher page blocks automated access. Lognormal single-ion area that varies by element and drifts with time.
- [TOFWERK EWCPS 2025 poster](https://dgm.inventum.de/app/medialibrary/show/eventItem/450e182d-cc54-4a1b-a761-b711b319ab80): indexed text consulted. On-digitizer averaging versus native-rate full-spectrum saving.
- TOF data-acquisition patents [US7084393](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7084393) and [US7800054](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7800054): indexed text consulted. Single-ion threshold data reduction and pulse-height distribution relative to ADC bits.
- [TOF-SPI technical note, JAAS 2024](https://pubs.rsc.org/en/content/articlehtml/2024/ja/d3ja00421j): indexed text consulted. icpTOF data are integrated peak data.

**Argon and the collision/reaction cell (note 06)**

- [Jiménez-Redondo et al. 2014, Ion kinetics in Ar/H₂ cold plasmas, RSC Advances (open PMC copy)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4685740/): full text consulted. Ar⁺ + H₂ total $8.9\times10^{-10}$ cm³ s⁻¹ with 98/2% branching, and ArH⁺ + H₂ → H₃⁺ + Ar at $6.3\times10^{-10}$, both from Anicich 1993.
- [Hexapole collision cell on an orthogonal-acceleration ICP-TOFMS, JAAS 2001](https://pubs.rsc.org/en/content/articlelanding/2001/ja/b004381h): indexed abstract consulted. ⁴⁰Ar⁺ reduced about four orders with H₂.
- [ICP-TOFMS with collision/reaction cell, JAAS 2019](https://pubs.rsc.org/en/Content/ArticleLanding/2019/JA/C8JA00275D): indexed abstract consulted. H₂ suppresses Ar-based ions without improving accuracy for most elements; He changes mass-dependent transit times.
- [NIST Chemistry WebBook: Ar](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440371&Mask=20), [H₂](https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=20), [He](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440597&Mask=20): ionization energies and proton affinities.
- [Vitesse product listing (Labcompare)](https://www.labcompare.com/28-Inductively-Coupled-Plasma-Mass-Spectrometer-ICP-MS/26106665-Vitesse-ICP-MS/): segmented hexapole reaction cell and optional quadrupole pre-cell.

**Arrival times and adjacent-mass leakage (notes 05 and 06)**

- [NIST Atomic Weights and Isotopic Compositions (all elements, ASCII)](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=ascii2&isotype=some): downloaded 16 October 2026. Source of [nuclides-Na-U-NIST.csv](Reference/nuclides-Na-U-NIST.csv).
- [Hendriks et al. 2017, characterization of the icpTOF, JAAS](https://pubs.rsc.org/en/content/articlelanding/2017/ja/c6ja00400h): indexed text consulted. Adjacent-mass abundance sensitivity 6.5 × 10⁻⁴ with a sloping baseline beyond the neighbour.
- [icpTOF-S2 characterization, JAAS 2023](https://pubs.rsc.org/en/content/articlehtml/2023/ja/d2ja00295g): indexed text consulted. Abundance sensitivity around 2000 ppm.
- [Agilent ICP-QQQ handbook, abundance sensitivity](https://read.nxtbook.com/agilent/agilentbooks/icpqqqhandbook/sectionthree_partfour.html): quadrupole value around 10⁻⁷.

**Tuning (note 18)**

- [Agilent ICP-MS Journal 88 (2022), tuning article summary](https://icpms.labrulez.com/paper/19881): indexed summary consulted; official English PDF not located. U/Th and ThO/Th as plasma checks; NIST 612 Th 37.79 and U 37.38 mg kg⁻¹ (values from the official Korean/Chinese editions).
- [Agilent: laser ablation for ICP-MS](https://icp-ms.help.agilent.com/en/HowTo/Help/Reference/Laser_Ablation_for_ICP-MS.htm): official help page. ThO/Th < 1% target on NIST 612; Ar carrier sets ThO/Th, He sets the Th:U bias.

**Laser interaction and two-volume cells (note 02)**

- [HyperPhysics: quantum processes](https://hyperphysics.gsu.edu/hbase/mod5.html): absorption, emission and stimulated emission overview.
- [Two-volume cell with integrated dual concentric injector (Loughborough repository)](https://dspace.lboro.ac.uk/2134/19620): indexed text consulted. 1.5 / 3.2 / 4.9 ms single-pulse widths on NIST 612.
- [Critical evaluation of low-dispersion ablation cells (open PDF)](https://digibuo.uniovi.es/dspace/bitstream/10651/52491/1/Critical%20evaluation.pdf): indexed text consulted. 0.5–30 s conventional washout versus sub-30 ms low-dispersion designs.
- [Instrument facility page describing an ESL TwoVol3 with DCI](https://qbeam.ehi.msu.edu/instruments/laser-ablation-page): vendor-style "<1 ms" washout description, not an independent measurement.

## Reading critically

For every reported resolution, detection limit, precision or imaging speed, ask: which isotope, sample matrix, spot size, fluence, counts, integration duration, calibration, background and uncertainty definition? A number detached from those conditions is poor guidance for designing an experiment.

## Original instrument figures and interactive illustration

See [15 Instrument Illustrations](15-instrument-illustrations.md) for the original Nu Vitesse brochure spread, Mamyrin Figure 1, Nu multicollector photograph, source credit, and a separate Three.js reconstruction. These distinguish instrument-specific layout from idealized response plots.

## Sources added for broader coverage, checked 7 October 2026

- [Stoll et al. 2026, The Cryosphere 20, 663–682](https://tc.copernicus.org/articles/20/663/2026/tc-20-663-2026.html): open primary Vitesse single-particle ice study; methods and limits of chemical/size interpretation.
- [Bolea and Laborda 2024, Spectrochimica Acta B 216, 106941](https://doi.org/10.1016/j.sab.2024.106941): primary authors' metrology analysis distinguishing particle, dissolved-element and solvent transport efficiency; readable publisher content consulted.
- [Vermeesch 2020, Geochronology 2, 119–131](https://gchron.copernicus.org/articles/2/119/2020/): open primary joint U–Th–Pb/common-Pb treatment, including allanite and monazite examples.
- [Chew et al. 2014, accessory-mineral reference standards with variable common Pb](https://www.sciencedirect.com/science/article/abs/pii/S000925411300510X): primary abstract/search metadata consulted for accessory-mineral common-Pb scope; full methods not retrieved.

Iolite's official import, trace-element, U–Pb and imaging tutorials were rechecked. Their datasets/settings are tutorial-specific; a laboratory's own files and in-house workflows remain authoritative. All additional numerical examples and planning worksheets are teaching constructions, not measurements or supplied case-study results.
