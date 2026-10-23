# LA-ICP-ToF-MS 3D

A Vite / Three.js teaching viewer, published alongside the MkDocs notes at [3d/](https://duserzym.github.io/la-icp-tof-ms-notes/3d/). The renderer, controls, materials and exploder follow the other mass-spectrometry projects in this account.

| Scene | Explore |
|---|---|
| Nu Vitesse overview | Plasma, interface cones, ion optics, segmented cell, beam attenuator, orthogonal extraction, downstream timed blanker, reflectron and MagneTOF |
| Time of flight | One extraction clock; voltage, effective path length, mass calibration and FWHM resolving power |
| Reflectron | Same mass at three energies; uniform-field mirror penetration and first-order energy focusing |
| Argon blanker | Gate delay and width; nominal Ar-40/Ca-40 co-rejection with adjacent K isotopes for comparison |
| MagneTOF | Exploded conversion/focusing/multiplication chain; secondary yield, overlapping unit-area pulses, ADC phase and numerical charge integration |
| Laser ablation | Ablation and aerosol transport; independent laser, extraction, saved-bin and transient clocks; simultaneous vs sequential sampling |

## Run and verify

Node.js 22 or newer:

```sh
npm ci
npm run dev
npm test
npm run build
npx playwright install chromium
npm run screenshots
```

`npm run build` writes **only** `../site/3d/`. At the repository root, build MkDocs first (`mkdocs build --strict`) and Vite second, as in the Pages workflow. This keeps the existing notes and standalone HTML models in the same deployment.

## Model limits

Geometry, internal fields and trajectories are conceptual constructions, not vendor CAD. Values such as the effective 1 m path, 5 kV energy, detector stage count/yield, mirror field and extraction rates are teaching assumptions, distinguished from manufacturer claims in the UI. Primary references are linked in each scene.

The flight scene uses an effective field-free path. The separate mirror scene solves a uniform retarding field; it does not pretend that the overview's drawn fold defines a calibrated flight path. The blanker uses nominal mass and cannot separate nominal-40 species in that model. Detector pulse FWHM and ADC sampling are shown separately from dead time; no saturation, noise or dead-time correction is implied by the linear pulse-area example. Laser-transient saving uses bin means over repeated extractions, not a proprietary acquisition format.

Code is MIT; the shipped Three.js notice is in `public/THIRD_PARTY_LICENSES.txt`. All modeled geometry and the SVG project icon are code-native artwork.
