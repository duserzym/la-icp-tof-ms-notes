import { describe, it, expect } from 'vitest';
import { flight, massFromTime, timeFWHM, mirror, gateRejects, sampledPulse } from '../src/physics/tof.js';
describe('ideal time-of-flight physics',()=>{
 it('matches the study-note 5 keV, 1 m examples',()=>{expect(flight(56)*1e6).toBeCloseTo(7.62,2);expect(flight(238)*1e6).toBeCloseTo(15.71,2);});
 it('round-trips the mass axis and charge-state scaling',()=>{for(const mz of [23,56,88,206,238])expect(massFromTime(flight(mz))).toBeCloseTo(mz,10);expect(flight(238/2)/flight(238)).toBeCloseTo(1/Math.sqrt(2),12);});
 it('uses the FWHM convention consistently',()=>expect(timeFWHM(20e-6,5000)).toBeCloseTo(2e-9,16));
 it('has a first-order stationary arrival time at the mirror design energy',()=>{const low=mirror(88,5000,.999),mid=mirror(88),high=mirror(88,5000,1.001);expect(Math.abs(high.total-low.total)/mid.total).toBeLessThan(1e-8);expect(high.depth).toBeGreaterThan(mid.depth);expect(high.reflection).toBeGreaterThan(mid.reflection);expect(low.drift).toBeGreaterThan(mid.drift);});
 it('a narrow nominal-40 gate passes 39 and 41, rejects both nominal-40 species',()=>{expect(gateRejects(40,2e-6,10e-9)).toBe(true);expect(gateRejects(39,2e-6,10e-9)).toBe(false);expect(gateRejects(41,2e-6,10e-9)).toBe(false);});
 it('integrates two overlapped linear unit-area responses at high sampling rate',()=>{for(const separation of [0,.1,1,3])expect(sampledPulse({rate:25,separation}).area).toBeCloseTo(2,6);});
});
