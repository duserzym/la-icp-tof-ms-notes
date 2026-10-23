// SI internally. These are ideal teaching models, not Vitesse operating settings.
export const E = 1.602176634e-19;
export const U = 1.66053906660e-27;
export const IONS = [
  { mz: 23, name: '²³Na⁺', color: '#5ab0ff' },
  { mz: 56, name: '⁵⁶Fe⁺', color: '#4fd6a1' },
  { mz: 88, name: '⁸⁸Sr⁺', color: '#ffb24a' },
  { mz: 206, name: '²⁰⁶Pb⁺', color: '#ff6f91' },
  { mz: 238, name: '²³⁸U⁺', color: '#c59bff' },
];
export function speed(mz, volts = 5000) { return Math.sqrt(2 * E * volts / (mz * U)); }
export function flight(mz, length = 1, volts = 5000) { return length / speed(mz, volts); }
export function massFromTime(seconds, length = 1, volts = 5000) { return 2 * E * volts * (seconds / length) ** 2 / U; }
export const timeFWHM = (seconds, resolvingPower) => seconds / (2 * resolvingPower);
export const gateArrival = (mz) => 2e-6 * Math.sqrt(mz / 40);
export const gateRejects = (mz, delay, width) => Math.abs(gateArrival(mz) - delay) <= width / 2;
export function mirror(mz, volts = 5000, energyRatio = 1, driftLength = 1.2, fieldRatio = 1) {
  const mass = mz * U, energy = E * volts * energyRatio;
  const field = 4 * volts / driftLength * fieldRatio;
  const v = Math.sqrt(2 * energy / mass), accel = E * field / mass;
  const drift = driftLength / v, reflection = 2 * v / accel;
  return { v, accel, field, depth: energy / (E * field), drift, reflection, total: drift + reflection };
}
export function gaussian(t, center, fwhm) {
  const sigma = fwhm / (2 * Math.sqrt(2 * Math.log(2)));
  return Math.exp(-0.5 * ((t - center) / sigma) ** 2) / (sigma * Math.sqrt(2 * Math.PI));
}
export function sampledPulse({ fwhm = 0.5, separation = 1, rate = 2, phase = 0 } = {}) {
  const x = [], y = [], dt = 1 / rate;
  for (let t = phase * dt; t <= 10; t += dt) { x.push(t); y.push(gaussian(t, 3, fwhm) + gaussian(t, 3 + separation, fwhm)); }
  const area = y.slice(1).reduce((s, v, i) => s + (v + y[i]) * dt / 2, 0);
  return { x, y, area };
}
export const multiplierGain = (yieldPerStage, stages) => yieldPerStage ** stages;
export const transient = (t, center = 0, sigma = 0.002) => Math.exp(-0.5 * ((t - center) / sigma) ** 2);
