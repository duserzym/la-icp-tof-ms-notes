import * as THREE from 'three';
import { M } from '../core/materials.js';
import { mesh, roundedBox, rod, wire, plateWithHole, tubeShell } from '../core/geom.js';
import { part } from './parts.js';

export const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const colorMat = (color) => new THREE.MeshPhysicalMaterial({ color, metalness: 0.25, roughness: 0.38 });
export function block(group, size, pos, mat, name = '') {
  const o = mesh(roundedBox(...size, Math.min(...size) * 0.12), mat, { name });
  o.position.set(...pos); group.add(o); return o;
}
export function rings(group, { count = 10, start = 0, step = 0.026, y = 0.12, z = 0, radius = 0.055, axis = 'x', mat = M.steel() } = {}) {
  const assembly = new THREE.Group(); group.add(assembly);
  for (let i = 0; i < count; i++) {
    const p = mesh(plateWithHole(radius * 2.3, radius * 2.3, 0.004, radius), mat);
    if (axis === 'x') { p.rotation.y = Math.PI / 2; p.position.set(start + i * step, y, z); }
    else p.position.set(start, y, z + i * step);
    assembly.add(p);
  }
  return assembly;
}
export function buildMirror({ start = 0.2, y = 0.16, z = 0, count = 13, radius = 0.09 } = {}) {
  const group = new THREE.Group(), parts = [];
  const electrodes = rings(group, { start, y, z, count, radius, step: 0.022, mat: M.copper() });
  parts.push(part(electrodes, [0.08, 0.09, 0], 'Reflectron electrode ladder', 'A graded electrostatic potential decelerates positive ions, stops their forward motion and accelerates them back. Faster ions penetrate deeper and spend longer inside.', { order: 0.45 }));
  const back = block(group, [0.012, radius * 2.55, radius * 2.55], [start + count * 0.022, y, z], M.steel());
  parts.push(part(back, [0.18, 0, 0], 'Retarding end plate', 'The mirror is electrostatic, not magnetic. Its potentials are a teaching schematic; no operating voltages are specified.', { order: 0.65 }));
  const cover = block(group, [count * 0.022 + 0.08, 0.015, radius * 2.8], [start + count * 0.011, y + radius * 1.5, z], M.panel(0xa9b7c6));
  parts.push(part(cover, [0, 0.28, 0], 'Reflectron housing', 'Explode or enable X-ray to inspect the electrode stack.', { order: 0, shell: true }));
  return { group, parts, electrodes };
}
export function buildGate({ x = 0, y = 0.16, z = 0 } = {}) {
  const group = new THREE.Group(), parts = [];
  group.position.set(x, y, z);
  const frame = mesh(plateWithHole(0.18, 0.18, 0.009, 0.064), M.steel()); frame.rotation.y = Math.PI / 2; group.add(frame);
  parts.push(part(frame, [0.045, 0.05, 0], 'Bradbury–Nielsen gate frame', 'The Vitesse timed blanker lies after extraction, before the reflectron. It rejects selected arrival-time windows rather than interrupting the argon gas flow.', { order: 0.2 }));
  const banks = [new THREE.Group(), new THREE.Group()]; group.add(...banks);
  for (let i = 0; i < 11; i++) {
    const z0 = (i - 5) * 0.009;
    banks[i % 2].add(rod(V(0, -0.05, z0), V(0, 0.05, z0), 0.0009, i % 2 ? M.gold() : M.copper()));
  }
  banks.forEach((b, i) => parts.push(part(b, [i ? -0.04 : 0.04, 0.03, i ? -0.04 : 0.04], 'Alternating wire bank ' + (i + 1), 'At equal potential the beam passes. Opposite wire potentials generate transverse fields in neighboring gaps. A timed pulse deflects the selected mass packet outside downstream acceptance.', { order: 0.55 })));
  return { group, parts, banks };
}
export function buildDetector() {
  const group = new THREE.Group(), parts = [], anchors = [], markers = [];
  const mark=(parent,p=V(0,0,0))=>{const o=new THREE.Object3D();o.position.copy(p);parent.add(o);markers.push(o);};
  const floor = block(group, [0.48, 0.025, 0.30], [0, 0.015, 0], M.aluminium());
  parts.push(part(floor, [0, -0.07, 0], 'Detector base', 'Schematic MagneTOF-type electron multiplier. The installed detector model and internal dimensions are not inferred from the course settings.', { order: 0.1 }));
  const impact = block(group, [0.012, 0.12, 0.12], [-0.19, 0.13, 0], M.dynode());
  parts.push(part(impact, [-0.11, 0.03, 0], 'Ion conversion surface', 'An ion impact releases secondary electrons. The impact time begins the detector response; the ion is consumed here.', { order: 0.3 }));
  anchors.push(V(-0.18, 0.13, 0));mark(impact);
  const paths = [V(-0.12, 0.22, 0), V(-0.02, 0.23, 0), V(0.035, 0.15, 0)];
  const lens = wire([anchors[0], ...paths], 0.004, M.gold()); group.add(lens);
  parts.push(part(lens, [0, 0.12, -0.08], 'Electron focusing path', 'Shaped electric and magnetic fields guide secondary electrons to the multiplier while limiting their transit-time spread. This curve shows the concept, not a solved manufacturer field map.', { order: 0.5 }));
  anchors.push(...paths);paths.forEach(p=>mark(lens,p));
  for (let i = 0; i < 7; i++) {
    const p = V(0.055 + i * 0.022, 0.10 + (i % 2) * 0.06, 0);
    const d = block(group, [0.018, 0.018, 0.06], p.toArray(), M.dynode());
    d.rotation.z = i % 2 ? -0.5 : 0.5;
    parts.push(part(d, [0, 0.03 + i * 0.009, (i % 2 ? -1 : 1) * 0.07], `Multiplier dynode ${i + 1}`, 'Impact produces additional secondary electrons. Gain is the product of stage yields; illustrated stages and yields are not an installed-detector specification.', { order: 0.65 }));
    anchors.push(p);mark(d);
  }
  const anode = block(group, [0.012, 0.07, 0.08], [0.23, 0.12, 0], M.gold());
  parts.push(part(anode, [0.10, 0, 0], 'Anode & waveform output', 'The arriving electron cloud produces an electrical pulse. An ADC samples the waveform; linear integration can preserve charge even when individual pulses overlap.', { order: 0.8 }));
  anchors.push(V(0.23, 0.12, 0));mark(anode);
  for (const side of [-1, 1]) {
    const pole = block(group, [0.28, 0.19, 0.025], [-0.05, 0.13, side * 0.105], M.magnetNdFe());
    parts.push(part(pole, [0, 0.06, side * 0.17], 'Magnetic pole piece', 'The magnetic field bends electron motion without doing work. Shaped fields and electrodes govern focusing; exact construction is schematic.', { order: 0.2 }));
  }
  const lid = block(group, [0.50, 0.015, 0.32], [0, 0.28, 0], M.panel());
  parts.push(part(lid, [0, 0.25, 0], 'Detector cover', 'Explode to reveal conversion, focusing, dynodes and anode.', { order: 0, shell: true }));
  return { group, parts, anchors, markers, impact, anode, lens };
}
export function buildInstrument({ qct = false } = {}) {
  const group = new THREE.Group(), parts = [], features = {};
  const base = block(group, [1.95, 0.04, 0.81], [0, 0.02, 0], M.panel(0xc8d0da));
  parts.push(part(base, [0, -0.15, 0], 'Instrument chassis', 'Schematic Nu Vitesse ion-optical sequence from the study notes and manufacturer documentation. Layout and dimensions are explanatory.', { order: 0.1 }));
  const H = 0.24;
  const torch = new THREE.Group(); group.add(torch);
  for (const r of [0.024, 0.032, 0.041]) { const t = mesh(tubeShell(r, r - 0.002, 0.19), M.quartz()); t.rotation.z = Math.PI / 2; t.position.set(-0.82, H, -0.19); torch.add(t); }
  const plasma = mesh(new THREE.SphereGeometry(0.045, 24, 18), new THREE.MeshBasicMaterial({ color: 0xffc09a, transparent: true, opacity: 0.8, toneMapped: false })); plasma.scale.set(1.7, 0.55, 0.55); plasma.position.set(-0.72, H, -0.19); torch.add(plasma);
  parts.push(part(torch, [-0.17, 0.12, 0], 'ICP torch & plasma', 'Laser-generated aerosol enters the argon ICP, where particles are vaporized, atomized and ionized. The plasma is continuous; the ToF pusher supplies repeated start times.', { order: 0.3 })); features.torch = torch;
  for (let i = 0; i < 3; i++) { const ring = mesh(new THREE.TorusGeometry(0.052, 0.005, 8, 28), M.coil()); ring.rotation.y = Math.PI / 2; ring.position.set(-0.83 + i * 0.025, H, -0.19); group.add(ring); parts.push(part(ring, [0, 0.16, 0], 'RF coil', 'An oscillating RF field sustains the argon discharge.', { order: 0.4 })); }
  const cones = new THREE.Group(); group.add(cones);
  for (let i = 0; i < 2; i++) { const c = mesh(new THREE.ConeGeometry(0.045 - i * 0.013, 0.065, 32, 1, true), M.steel()); c.rotation.z = -Math.PI / 2; c.position.set(-0.64 + i * 0.08, H, -0.19); cones.add(c); }
  parts.push(part(cones, [-0.06, 0.12, -0.13], 'Sampler & skimmer', 'Differentially pumped cones sample the plasma and form a directed ion beam; most of the incoming gas is pumped away.', { order: 0.45 })); features.cones = cones;
  const optics = rings(group, { count: 5, start: -0.49, y: H, z: -0.19, radius: 0.027 });
  parts.push(part(optics, [0, 0.13, -0.15], 'Extraction & focusing lenses', 'Electrostatic lenses focus positive ions into the cell. Neutrals are not focused by the electric field.', { order: 0.55 }));
  if (qct) {
    const q = new THREE.Group(); group.add(q);
    for (const [dy, dz] of [[0.02,0],[-0.02,0],[0,0.02],[0,-0.02]]) q.add(rod(V(-0.36,H+dy,-0.19+dz),V(-0.21,H+dy,-0.19+dz),0.006,M.gold()));
    parts.push(part(q, [0,0.15,-0.1], 'Optional QCT quadrupole', 'The optional full-size quadrupole precedes the reaction cell and selects precursor ions. This differs from scanning a quadrupole as the final analyzer.', { order: 0.6 })); features.quad = q;
  }
  const cell = rings(group, { count: 8, start: -0.18, step: 0.022, y: H, z: -0.19, radius: 0.035, mat: M.gold() });
  parts.push(part(cell, [0,0.15,-0.1], 'Segmented reaction cell', 'Cell gases can alter ion chemistry and kinetic energy distributions. Scattering losses, reaction products and temporal broadening depend on method conditions.', { order: 0.65 })); features.cell = cell;
  const atten = block(group,[0.008,0.11,0.11],[0.06,H,-0.19],M.graphite());
  parts.push(part(atten,[0,0.15,-0.12],'Upstream beam attenuator','Reduces overall beam load before extraction. It is distinct from the arrival-time-selective blanker in the ToF flight path.',{order:0.6}));
  const pusher = new THREE.Group(); group.add(pusher);
  for (const side of [-1,1]) block(pusher,[0.15,0.008,0.11],[0.19,H+side*0.05,-0.19],M.copper());
  parts.push(part(pusher,[0,0.18,0],'Orthogonal accelerator','An extraction pulse accelerates a slice of the continuous beam into the perpendicular ToF direction. Different m/z ions receive the same energy per charge, not the same speed.',{order:0.7})); features.pusher=pusher;
  // Flight axis turns into +Z; the reflectron returns ions on a neighboring leg.
  const mirror = buildMirror({start:0.30,y:H,z:0.18,radius:0.19}); mirror.group.rotation.y=-Math.PI/2; mirror.group.position.set(0.53,0,0.25); group.add(mirror.group); parts.push(...mirror.parts); features.mirror=mirror.group;
  const gate=buildGate(); gate.group.rotation.y=Math.PI/2; gate.group.position.set(0.19,H,0.06); group.add(gate.group); parts.push(...gate.parts); features.gate=gate.group;
  const detector=block(group,[0.14,0.12,0.11],[0.51,H,-0.19],M.black());
  parts.push(part(detector,[0.18,0.07,0],'MagneTOF detector','Ions release secondary electrons at a conversion surface; shaped fields guide them into multiplication stages. Open the detector scene to inspect the signal chain.',{order:0.75})); features.detector=detector;
  const cover=block(group,[1.55,0.012,0.72],[0.12,0.43,0.02],M.panel(0xdfe4eb));
  parts.push(part(cover,[0,0.43,-0.12],'Vacuum-chamber cover','Enable X-ray or explode to see the ion optics. The physical flight path is folded; the geometry shown here is schematic.',{order:0,shell:true}));
  const pump=block(group,[0.17,0.16,0.15],[-0.50,0.12,0.19],M.steel());
  parts.push(part(pump,[0,-0.12,0.16],'Differential pumping','Maintains the source-to-analyzer pressure gradient. Ion blanking rejects selected charged particles; it does not remove the carrier gas.',{order:0.35}));
  const sourcePath=[V(-0.91,H,-0.19),V(-0.63,H,-0.19),V(0.19,H,-0.19)];
  const flightPath=[V(0.19,H,-0.19),V(0.19,H,0.55),V(0.35,H,0.80),V(0.51,H,0.55),V(0.51,H,-0.19)];
  return {group,parts,features,sourcePath,flightPath};
}
