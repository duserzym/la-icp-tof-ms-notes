import * as THREE from 'three';
import { Exploder } from '../core/explode.js';
import { IonBeam, PolylineCurve } from '../core/beam.js';
import { Chart } from '../core/chart.js';
import { section, slider, select, segmented, readouts, note, para, table, sources, buttons, h } from '../core/ui.js';
import { M } from '../core/materials.js';
import { mesh, wire, roundedBox, rod } from '../core/geom.js';
import { registerParts } from '../components/parts.js';
import { buildInstrument, buildMirror, buildGate, buildDetector, block, V } from '../components/tof.js';
import { buildAblationCell } from '../components/laser.js';
import { IONS, flight, timeFWHM, mirror, gateArrival, gateRejects, gaussian, sampledPulse, multiplierGain, transient } from '../physics/tof.js';
import { SRC } from '../sources.js';

function dots(root, colors, radius = 0.012) {
  const group = new THREE.Group(); group.userData.beam = true; root.add(group);
  return colors.map((c) => { const m=mesh(new THREE.SphereGeometry(radius,16,12),new THREE.MeshBasicMaterial({color:c,toneMapped:false})); group.add(m); return m; });
}
function line(root, points, color='#5ab0ff', radius=.002) { const m=wire(points,radius,new THREE.MeshBasicMaterial({color,transparent:true,opacity:.65})); m.userData.beam=true; root.add(m); return m; }
function info(title, text, refs = [SRC.notes], more = '') { const c=section(title,{icon:'ℹ'}); c.body.append(para(text), more ? note(more) : '', sources(refs)); return c; }
function playback(duration=1, unit='µs') {
  const S={t:0, playing:true, duration};
  const card=section('Packet replay',{icon:'▶'});
  const time=slider({label:'Replay time',min:0,max:duration,value:0,unit,onInput:v=>{S.t=v;S.playing=false;sync();}});
  const controls=buttons([{label:'Pause',onClick:()=>{S.playing=!S.playing;sync();}},{label:'Restart',onClick:()=>{S.t=0;S.playing=true;sync();}}]);
  function sync(){controls.els[0].textContent=S.playing?'Pause':'Play';time.set(S.t);}
  card.body.append(controls.el,time.el,para('One extraction is replayed slowly. The time readout is the physical teaching-model clock; the animation speed is for inspection.'));
  return {card,S,update(dt){if(S.playing){S.t=(S.t+dt*S.duration/8)%(S.duration*1.12);time.set(Math.min(S.t,S.duration));}},setDuration(v){S.duration=v;time.input.max=v;S.t=0;},sync};
}
function closeups(ctx, list) { return buttons(list.map(([label,obj])=>({label,onClick:()=>ctx.app.focusOn(obj)}))).el; }

export const instrument={
 id:'instrument',title:'Nu Vitesse · inside the machine',group:'Instrument',icon:'⌬',blurb:'Plasma → interface → cell → pusher → timed blanker → reflectron → MagneTOF',
 async create(ctx){
  const root=new THREE.Group(), ex=new Exploder(), S={qct:false};
  const inst=buildInstrument(); root.add(inst.group); registerParts(ex,inst.parts);
  const source=new IonBeam(inst.sourcePath,{radius:.003,particles:22,speed:.35,size:.012});root.add(source);
  const beam=new IonBeam(inst.flightPath,{radius:.002,particles:12,speed:.4,size:.009,color:0xffb24a});root.add(beam);
  const f=inst.features;
  ctx.label(f.torch,'Argon ICP',{offset:[-.77,.32,-.19]});
  ctx.label(f.cell,'Reaction cell',{offset:[-.10,.36,-.19]});
  ctx.label(f.pusher,'Orthogonal pusher',{offset:[.19,.33,-.19]});
  ctx.label(f.gate,'Timed blanker',{offset:[0,.15,0]});
  ctx.label(f.mirror,'Reflectron',{offset:[.48,.40,.18]});
  ctx.label(f.detector,'MagneTOF',{offset:[0,.12,0]});
  const intro=info('From aerosol to a full spectrum','Follow the continuous beam through plasma, cones, ion optics and the segmented cell. The pusher extracts packets sideways; flight time separates m/z. The blanker is <b>after extraction, before the reflectron</b>. It is separate from the upstream beam attenuator.',[SRC.nu,SRC.gate,SRC.notes]);
  intro.body.append(closeups(ctx,[['Source close-up',f.cones],['Pusher & gate',f.gate],['Reflectron',f.mirror],['Detector',f.detector]]),buttons([{label:'Open detector internals →',onClick:()=>{location.hash='scene=detector';}}]).el);
  const spec=section('What is known / what is drawn',{open:false,icon:'✓'});
  spec.body.append(table(['Item','Basis'],[['Architecture','Nu manufacturer layout and accompanying notes'],['Optional QCT','A quadrupole can precede the reaction cell; not shown in this standard configuration'],['Geometry & beam curves','Schematic; no vendor CAD or proprietary field map'],['Flight-path animation','Continuous tracers for orientation; open the flight-time scene for one timed packet'],['Published resolving power','3800 FWHM on the linked manufacturer product page; not the result of this geometry']]),sources([SRC.nu]));
  return{root,exploder:ex,scale:1.8,defaults:{xray:true},camera:{position:[1.60,1.60,-2.15],target:[-.02,.22,.18]},panel:[intro.el,spec.el],update(dt){source.update(dt);beam.update(dt);}};
 }
};

export const tof={
 id:'tof',title:'Time of flight · one extraction',group:'Ion optics',icon:'⏱',blurb:'Equal energy per charge · different velocities · t ∝ √(m/z)',
 async create(ctx){
  const root=new THREE.Group(),ex=new Exploder(), S={volts:5000,length:1,R:4000};
  const path=[V(-.62,.16,-.17),V(.28,.16,-.17),V(.46,.16,0),V(.28,.16,.17),V(-.62,.16,.17)];
  const curve=new PolylineCurve(path); line(root,path,'#9fb3cf');
  const mirrorAssembly=buildMirror({start:.22,z:0,radius:.19});root.add(mirrorAssembly.group);registerParts(ex,mirrorAssembly.parts);
  const start=block(root,[.025,.15,.13],[-.62,.16,-.17],M.copper());ex.add(start,[-.12,.08,0],{name:'Pusher start plane',info:'Each ion starts on the same extraction trigger. The teaching calculation uses an effective field-free path; the drawn fold is schematic.'});
  const det=block(root,[.018,.14,.14],[-.62,.16,.17],M.black());ex.add(det,[-.1,0,.07],{name:'Detector arrival plane',info:'A full spectrum consists of successive mass peaks from one extracted ion population, not all masses arriving at the same instant.'});
  const particles=dots(root,IONS.map(i=>i.color),.014);
  ctx.label(start,'Extraction · t = 0',{offset:[0,.12,0]});ctx.label(det,'Arrival times',{offset:[0,.12,0]});
  particles.forEach((p,i)=>ctx.label(p,IONS[i].name,{offset:[0,.035,0]}));
  const intro=info('Why light ions arrive first','At potential U, <b>½mv² = zeU</b>. Thus v = √(2zeU/m) and <b>t = L√(m/2zeU)</b>. One extraction samples many m/z channels together, but their peaks arrive at different times. Here L is an <b>effective field-free length</b>; mirror dwell time belongs to the next scene.',[SRC.notes,SRC.mirror],'The default 1 m and 5 kV are teaching assumptions. They are not the Vitesse folded-path length or installed accelerating potential.');
  const ctl=section('Flight conditions',{icon:'⚙'}), replay=playback(20);
  const ro=readouts([{id:'slow',label:'²³⁸U⁺ flight'},{id:'width',label:'²⁰⁶Pb⁺ time FWHM'}]);
  const chartCard=section('Arrival-time spectrum',{icon:'∿'}), chart=new Chart(chartCard.body,{height:190,xLabel:'time / µs',yLabel:'relative intensity',yMin:0,yMax:1.1,legend:false});
  const rows=h('div');
  function refresh(){const max=flight(238,S.length,S.volts)*1e6;replay.setDuration(max*1.08);ro.slow.set(max.toFixed(3)+' µs');ro.width.set((timeFWHM(flight(206,S.length,S.volts),S.R)*1e9).toFixed(2)+' ns');
   rows.replaceChildren(table(['Ion','t / µs','FWHM / ns'],IONS.map(i=>[i.name,(flight(i.mz,S.length,S.volts)*1e6).toFixed(3),(timeFWHM(flight(i.mz,S.length,S.volts),S.R)*1e9).toFixed(2)])));
   chart.setSeries(IONS.map(i=>{const t=flight(i.mz,S.length,S.volts)*1e6;const x=Array.from({length:121},(_,j)=>t+(j-60)*max*.0003);const sigma=timeFWHM(t,S.R)/2.355;return{name:i.name,color:i.color,x,y:x.map(v=>Math.exp(-.5*((v-t)/sigma)**2))};}));chart.setOptions({xMin:0,xMax:max*1.08});
  }
  ctl.body.append(slider({label:'Acceleration potential (assumed)',min:1000,max:10000,step:100,value:S.volts,unit:'V',onInput:v=>{S.volts=v;refresh();}}).el,slider({label:'Effective path (assumed)',min:.5,max:2,step:.05,value:S.length,unit:'m',onInput:v=>{S.length=v;refresh();}}).el,slider({label:'Resolving power R (assumed)',min:500,max:10000,step:100,value:S.R,onInput:v=>{S.R=v;refresh();}}).el,ro.el);
  chartCard.body.append(rows,para('Gaussian peaks use Δt = t/(2R). Equal peak heights are illustrative, not abundances or sensitivity. Narrow peaks may be subpixel in the full-range chart; read widths in the table.'));refresh();
  return{root,exploder:ex,scale:1.2,camera:{position:[-1.20,1.15,1.60],target:[-.12,.14,0]},panel:[intro.el,ctl.el,replay.card.el,chartCard.el],update(dt){replay.update(dt);particles.forEach((p,i)=>{const t=flight(IONS[i].mz,S.length,S.volts)*1e6;curve.getPoint(Math.min(1,replay.S.t/t),p.position);p.position.y+=i*.009;});},dispose(){chart.dispose();}};
 }
};

export const reflectron={
 id:'reflectron',title:'Reflectron · energy focusing',group:'Ion optics',icon:'↶',blurb:'Faster ions turn deeper · compare three energies on one clock',
 async create(ctx){
  const root=new THREE.Group(),ex=new Exploder(),S={spread:.1,fieldRatio:1};
  const assembly=buildMirror({start:0,y:.16,z:0,count:16});root.add(assembly.group);registerParts(ex,assembly.parts);
  const colors=['#5ab0ff','#ffb24a','#ff6f91'], particles=dots(root,colors), replay=playback(25);
  const energy=[1-S.spread,1,1+S.spread];
  for(const z of [-.055,0,.055]) line(root,[V(-.6,.16,z),V(.30,.16,z)],'#73849b',.001);
  ctx.label(assembly.electrodes,'Retarding potential',{offset:[.15,.32,.10]});particles.forEach((p,i)=>ctx.label(p,['Lower energy','Design energy','Higher energy'][i],{offset:[0,.03,0]}));
  const intro=info('Compensating the energy spread','These ions have the <b>same mass (⁸⁸Sr⁺)</b> and different energies. A fast ion gains time in the drift, penetrates farther, then spends longer in the retarding field. The uniform-field mirror gives t = Ld√(m/2K) + 2√(2mK)/(qEr). At <b>Ld = 4K/(qEr)</b>, dt/dK = 0 to first order.',[SRC.mirror,SRC.notes],'The three lanes are visual offsets, not separate mirror channels. Initial position, angles, space charge and realistic fringe fields are omitted.');
  const ctl=section('Tune a teaching mirror',{icon:'⚙'}),ro=readouts([{id:'field',label:'Mirror field'},{id:'spread',label:'Total arrival-time spread'}]);
  const rows=h('div'),c=section('Energy versus flight time',{icon:'∿'}),chart=new Chart(c.body,{height:190,xLabel:'K / K₀',yLabel:'time / µs',legendPos:'br'});
  function refresh(){energy.splice(0,3,1-S.spread,1,1+S.spread);const ms=energy.map(e=>mirror(88,5000,e,1.2,S.fieldRatio));ro.field.set((ms[1].field/1000).toFixed(2)+' kV/m');ro.spread.set(((Math.max(...ms.map(m=>m.total))-Math.min(...ms.map(m=>m.total)))*1e9).toFixed(2)+' ns');rows.replaceChildren(table(['Energy','Turn depth','Arrival'],ms.map((m,i)=>[(energy[i]*100).toFixed(0)+'%',(m.depth*100).toFixed(2)+' cm',(m.total*1e6).toFixed(4)+' µs'])));replay.setDuration(Math.max(...ms.map(m=>m.total))*1e6*1.04);const x=Array.from({length:121},(_,i)=>.7+i*.005);chart.setSeries([{name:'Drift',color:colors[0],x,y:x.map(e=>mirror(88,5000,e,1.2,S.fieldRatio).drift*1e6)},{name:'Mirror',color:colors[2],x,y:x.map(e=>mirror(88,5000,e,1.2,S.fieldRatio).reflection*1e6)},{name:'Total',color:colors[1],x,y:x.map(e=>mirror(88,5000,e,1.2,S.fieldRatio).total*1e6),width:3}]);}
  const field=slider({label:'Field / first-order focus field',min:.65,max:1.4,step:.01,value:1,onInput:v=>{S.fieldRatio=v;refresh();}});
  ctl.body.append(slider({label:'Energy spread ±',min:.01,max:.25,step:.01,value:S.spread,fmt:v=>(100*v).toFixed(0)+'%',onInput:v=>{S.spread=v;refresh();}}).el,field.el,buttons([{label:'Restore first-order focus',onClick:()=>field.set(1,true)}]).el,ro.el,rows);
  refresh();
  return{root,exploder:ex,scale:1.1,defaults:{xray:true},camera:{position:[.45,.85,1.30],target:[-.12,.18,0]},panel:[intro.el,ctl.el,replay.card.el,c.el],update(dt){replay.update(dt);energy.forEach((e,i)=>{const m=mirror(88,5000,e,1.2,S.fieldRatio);let t=replay.S.t*1e-6,x;if(t<m.drift/2)x=-.6+m.v*t;else if(t<m.drift/2+m.reflection){const s=t-m.drift/2;x=m.v*s-.5*m.accel*s*s;}else x=-m.v*Math.min(m.drift/2,t-m.drift/2-m.reflection);particles[i].position.set(x,.16,(i-1)*.055);});},dispose(){chart.dispose();}};
 }
};

export const blanker={
 id:'blanker',title:'Argon blanker · a timed wire gate',group:'Ion optics',icon:'⊣',blurb:'Delay & width · rejected Ar-40 also removes nominal Ca-40',
 async create(ctx){
  const root=new THREE.Group(),ex=new Exploder(),gate=buildGate();root.add(gate.group);registerParts(ex,gate.parts);
  const S={delay:2e-6,width:150e-9,enabled:true}, replay=playback(4);
  const ions=[{mz:23,name:'²³Na⁺',color:'#5ab0ff'},{mz:39,name:'³⁹K⁺',color:'#ffb24a'},{mz:40,name:'⁴⁰Ar⁺',color:'#ff6f91'},{mz:40,name:'⁴⁰Ca⁺',color:'#c59bff'},{mz:41,name:'⁴¹K⁺',color:'#4fd6a1'},{mz:88,name:'⁸⁸Sr⁺',color:'#7fe0ff'}];
  const particles=dots(root,ions.map(i=>i.color),.010);
  const dump=block(root,[.32,.025,.22],[.19,.04,0],M.graphite());ex.add(dump,[0,-.1,0],{name:'Rejected-ion interception (schematic)',info:'A rejected packet leaves downstream optical acceptance. These interception surfaces are illustrative, not vendor CAD.'});
  line(root,[V(-.55,.16,0),V(.60,.16,0)],'#839ab9',.002);
  particles.forEach((p,i)=>ctx.label(p,ions[i].name,{offset:[0,.025,0]}));ctx.label(gate.group,'Timed gate',{offset:[0,.14,0]});
  const intro=info('Use flight time to reject a mass window','When both wire banks share a potential, ions pass. During the blanking pulse, opposite wire potentials deflect the passing packet. The gate is downstream of the orthogonal accelerator. A gate at nominal <b>mass 40 rejects both Ar and Ca</b> in this nominal-mass model.',[SRC.gate,SRC.notes],'Gate arrivals use t = 2√((m/z)/40) µs, corresponding to an assumed 5 keV drift. Point packets and instantaneous switching omit packet width, jitter, ringing and settling.');
  const ctl=section('Blanking pulse',{icon:'⚙'}),ro=readouts([{id:'state',label:'Gate now'},{id:'pass',label:'Passed gate / displayed species'}]);
  const outcomes=h('div'),c=section('Arrival window at the gate',{icon:'⏱'}),chart=new Chart(c.body,{height:170,xLabel:'gate arrival / µs',yLabel:'packet marker',yMin:0,yMax:1.3,legend:false,xMin:1.4,xMax:3.2});
  function refresh(){outcomes.replaceChildren(table(['Ion','Arrival / µs','Gate outcome'],ions.map(i=>[i.name, (gateArrival(i.mz)*1e6).toFixed(3),S.enabled&&gateRejects(i.mz,S.delay,S.width)?'Rejected':'Passed gate'])));chart.setSeries(ions.map((i,k)=>({name:i.name,color:i.color,type:'scatter',r:5,x:[gateArrival(i.mz)*1e6],y:[.3+k*.13]})));chart.setMarks(S.enabled?[{x0:(S.delay-S.width/2)*1e6,x1:(S.delay+S.width/2)*1e6,color:'#ef4444',alpha:.2}]:[]);}
  ctl.body.append(segmented({value:'on',options:[{value:'on',label:'Timed blanking'},{value:'off',label:'Gate open'}],onChange:v=>{S.enabled=v==='on';refresh();}}).el,slider({label:'Pulse center',min:1.5,max:2.7,step:.005,value:2,unit:'µs',onInput:v=>{S.delay=v*1e-6;refresh();}}).el,slider({label:'Pulse width',min:10,max:700,step:5,value:150,unit:'ns',onInput:v=>{S.width=v*1e-9;refresh();}}).el,ro.el,outcomes);refresh();
  return{root,exploder:ex,scale:1.1,camera:{position:[.45,.80,1.15],target:[0,.16,0]},panel:[intro.el,ctl.el,replay.card.el,c.el],update(dt){replay.update(dt);const t=replay.S.t*1e-6;const active=S.enabled&&Math.abs(t-S.delay)<=S.width/2;ro.state.set(active?'Deflecting':'Transmitting',active?'warn':'good');let passed=0;particles.forEach((p,i)=>{const arrival=gateArrival(ions[i].mz),reject=S.enabled&&gateRejects(ions[i].mz,S.delay,S.width);const progress=t/arrival;const x=Math.min(.60,-.55+progress*.55);p.position.set(x,.16,(i-2.5)*.011);if(progress>1){if(reject){p.position.x=Math.min(.3,(progress-1)*.20);p.position.y=Math.max(.06,.16-(progress-1)*.22);}else passed++;}});ro.pass.set(`${passed} / ${ions.length}`);gate.banks.forEach(b=>b.traverse(o=>{if(o.isMesh)o.material.emissive?.set(active?0x992c1a:0x000000);}));}};
 }
};

export const detector={
 id:'detector',title:'MagneTOF · from ion to waveform',group:'Detection',icon:'◉',blurb:'Conversion surface → electron focusing → dynodes → ADC & charge integration',
 async create(ctx){
  const root=new THREE.Group(),ex=new Exploder(),d=buildDetector();root.add(d.group);registerParts(ex,d.parts);
  const particles=dots(root,Array(18).fill('#7fe0ff'),.004);
  let run=true,phase=0;const S={yield:3,stages:7,fwhm:.5,separation:1,rate:2,samplePhase:0};
  ctx.label(d.impact,'Ion → secondary electrons',{offset:[0,.10,0]});ctx.label(d.lens,'Shaped E & B fields',{offset:[0,.06,0]});ctx.label(d.anode,'Anode → ADC',{offset:[0,.08,0]});
  const intro=info('The detector is a signal chain','An ion strikes the conversion surface. Secondary electrons follow shaped electric and magnetic fields into a multiplier; impacts on successive dynodes amplify the cloud. The anode pulse is digitized. <b>Pulse width, sample interval, dead time and overload recovery are different quantities.</b>',[SRC.detector,SRC.simke,SRC.notes],'The exploded layout and electron replay are conceptual, with no calibrated internal transit time. Stage number, yields and pulse shape below are illustrative, not installed-detector specifications.');
  intro.body.append(closeups(ctx,[['Conversion surface',d.impact],['Electron focusing',d.lens],['Multiplier & anode',d.anode]]),buttons([{label:'Pause cascade',onClick:b=>{run=!run;b.textContent=run?'Pause cascade':'Play cascade';}},{label:'Replay cascade',onClick:()=>{phase=0;run=true;}}]).el);
  const ctl=section('Multiplication & signal formation',{icon:'⚙'}),ro=readouts([{id:'gain',label:'Illustrative gain δⁿ'},{id:'step',label:'ADC sample interval'},{id:'area',label:'Sampled area / two ions'}]);
  const c=section('Two ions: overlapping electrical pulses',{icon:'∿'}),chart=new Chart(c.body,{height:200,xLabel:'time / ns',yLabel:'charge density / ns⁻¹',xMin:0,xMax:8,legendPos:'tr'});
  function refresh(){const x=Array.from({length:1001},(_,i)=>i*.01),sample=sampledPulse({fwhm:S.fwhm,separation:S.separation,rate:S.rate,phase:S.samplePhase});ro.gain.set(multiplierGain(S.yield,S.stages).toLocaleString(undefined,{maximumFractionDigits:0})+' e⁻ / starting electron');ro.step.set((1/S.rate).toFixed(3)+' ns');ro.area.set(sample.area.toFixed(3)+' (ideal: 2)');chart.setSeries([{name:'Ion 1 + ion 2',color:'#5ab0ff',x,y:x.map(t=>gaussian(t,3,S.fwhm)+gaussian(t,3+S.separation,S.fwhm)),width:2},{name:'ADC samples',color:'#ffb24a',x:sample.x,y:sample.y,type:'scatter',r:2.7}]);}
  ctl.body.append(slider({label:'Secondary yield per stage δ',min:2,max:5,step:.1,value:3,onInput:v=>{S.yield=v;refresh();}}).el,slider({label:'Stage count n (gain model)',min:5,max:12,step:1,value:7,onInput:v=>{S.stages=v;refresh();}}).el,slider({label:'Single-ion response FWHM',min:.3,max:2,step:.05,value:.5,unit:'ns',onInput:v=>{S.fwhm=v;refresh();}}).el,slider({label:'Ion arrival separation',min:0,max:3,step:.05,value:1,unit:'ns',onInput:v=>{S.separation=v;refresh();}}).el,slider({label:'Digitizer sampling rate',min:2,max:25,step:1,value:2,unit:'GS/s',onInput:v=>{S.rate=v;refresh();}}).el,slider({label:'Sampling phase / sample interval',min:0,max:.99,step:.01,value:0,onInput:v=>{S.samplePhase=v;refresh();}}).el,ro.el);
  c.body.append(para('Each Gaussian has unit area. Their continuous sum integrates to two ions even when they overlap, provided the chain is linear. The numerical area uses a trapezoidal sum over 0–10 ns. No clipping, gain fluctuation, noise, bandwidth limit or dead-time model is included.'));refresh();
  return{root,exploder:ex,scale:.65,defaults:{xray:true},camera:{position:[.70,.65,.85],target:[0,.14,0]},panel:[intro.el,ctl.el,c.el],update(dt){if(run)phase=(phase+dt*.13)%1.2;root.updateMatrixWorld(true);const curve=new PolylineCurve(d.markers.map(o=>root.worldToLocal(o.getWorldPosition(new THREE.Vector3()))));particles.forEach((p,i)=>{const u=Math.max(0,Math.min(1,phase-i*.008));curve.getPoint(u,p.position);const spread=u>.5?.006:.002;p.position.z+=Math.sin(i*2.4)*spread;p.visible=ctx.app.state.beams&&phase>=i*.008;});},dispose(){chart.dispose();}};
 }
};

export const coupled={
 id:'laser',title:'Laser ablation · four acquisition clocks',group:'Workflow',icon:'⇄',blurb:'Ablation cell → aerosol → ICP → full spectra → saved pixels',
 async create(ctx){
  const root=new THREE.Group(),ex=new Exploder(),cell=buildAblationCell();cell.group.scale.setScalar(3);cell.group.position.set(-.58,.025,0);root.add(cell.group);registerParts(ex,cell.parts,{scale:3});
  const torch=block(root,[.16,.12,.15],[.03,.15,0],M.quartz());ex.add(torch,[0,.13,0],{name:'Continuous argon ICP',info:'Aerosol is vaporized, atomized and ionized. The laser repetition rate does not define the ToF extraction or saved-spectrum rate.'});
  const analyzer=block(root,[.44,.18,.30],[.51,.14,0],M.panel());ex.add(analyzer,[0,.22,0],{name:'ToF analyzer & data accumulation',info:'Repeated extractions capture full mass spectra. Multiple extractions can be accumulated before a saved spectrum or pixel is written.',shell:true});
  const route=[V(-.40,.11,0),V(-.23,.18,.08),V(-.10,.18,.08),V(.02,.15,0)];line(root,route,'#7fe0ff',.005);const beam=new IonBeam(route,{radius:.002,particles:18,speed:.15,color:0xffb24a,size:.009});root.add(beam);
  line(root,[V(-.58,.65,0),V(-.58,.07,0)],'#b797ff',.004);
  ctx.label(cell.group,'Two-volume ablation cell',{offset:[0,.065,0]});ctx.label(torch,'ICP',{offset:[0,.12,0]});ctx.label(analyzer,'Full-spectrum acquisition',{offset:[0,.17,0]});
  const S={rep:20,extraction:20,save:1,width:2,channels:5},intro=info('Which clock controls what?','The laser launches material; cell washout shapes the aerosol transient; the ToF pusher repeatedly samples the ion beam; saved spectra accumulate extractions. A map pixel is a later sampling decision. Full-spectrum sampling avoids quadrupole peak hopping, but <b>does not remove transport mixing or low-count uncertainty</b>.',[SRC.nu,SRC.notes],'All rates and Gaussian transients here are independent teaching controls. A reported 200 kHz course clock is not assumed to be an established full-mass-range extraction rate.');
  const ctl=section('Transient sampling experiment',{icon:'⚙'}),ro=readouts([{id:'shots',label:'Extractions / saved spectrum'},{id:'laser',label:'Laser-pulse interval'},{id:'bins',label:'Saved spectra / FWHM'},{id:'mass',label:'²³⁸U⁺ full flight at 1 m, 5 kV'}]);
  const c=section('Same transient, different sampling times',{icon:'∿'}),chart=new Chart(c.body,{height:210,xLabel:'time / ms',yLabel:'relative signal',yMin:0,yMax:1.15,legendPos:'br'});
  function refresh(){const x=Array.from({length:601},(_,i)=>-10+i/30),sigma=S.width/2.355;const series=[{name:'Aerosol transient',color:'#9ab0cb',x,y:x.map(t=>transient(t,0,sigma)),width:2}];for(let k=0;k<S.channels;k++){const tx=[];for(let t=-10+k*S.save/S.channels;t<=10;t+=S.save)tx.push(t);series.push({name:k===0?'Sequential m/z samples':'',color:IONS[k].color,x:tx,y:tx.map(t=>transient(t,0,sigma)),type:'scatter',r:2});}const xs=[];for(let t=-10;t<=10;t+=S.save)xs.push(t);series.push({name:'ToF saved-bin mean (all m/z)',color:'#8b5cf6',x:xs,y:xs.map(t=>{let sum=0;const n=Math.max(1,Math.round(S.extraction*S.save));for(let j=0;j<n;j++)sum+=transient(t+(j+.5)/n*S.save,0,sigma);return sum/n;}),width:2});chart.setSeries(series);ro.shots.set((S.extraction*S.save).toFixed(0));ro.laser.set((1000/S.rep).toFixed(1)+' ms');ro.bins.set((S.width/S.save).toFixed(1));ro.mass.set((flight(238)*1e6).toFixed(2)+' µs');}
  ctl.body.append(slider({label:'Laser repetition',min:1,max:200,step:1,value:20,unit:'Hz',onInput:v=>{S.rep=v;refresh();}}).el,slider({label:'ToF extraction rate (assumed)',min:5,max:40,step:1,value:20,unit:'kHz',onInput:v=>{S.extraction=v;refresh();}}).el,slider({label:'Saved-spectrum bin width',min:.1,max:5,step:.1,value:1,unit:'ms',onInput:v=>{S.save=v;refresh();}}).el,slider({label:'Single aerosol transient FWHM',min:.3,max:8,step:.1,value:2,unit:'ms',onInput:v=>{S.width=v;refresh();}}).el,ro.el);c.body.append(para('Colored points show five sequential m/z dwells across one comparison sweep equal to the saved-bin width. The ToF curve averages the same transient over each bin, with all m/z channels sharing the same bin. It illustrates timing offsets, not different elemental sensitivities.'));refresh();
  return{root,exploder:ex,scale:1.5,defaults:{xray:true},camera:{position:[.75,1.30,1.65],target:[-.05,.12,0]},panel:[intro.el,ctl.el,c.el],update(dt){beam.update(dt);},dispose(){chart.dispose();}};
 }
};
