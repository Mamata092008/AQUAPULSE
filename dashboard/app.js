/**
 * AQUAPULSE: Live SCADA Dashboard & Triangulation Engine
 * Team TECHTONICS | Vishwakarma Awards 2026-27 | Host: IIT Hyderabad
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const btnSimulate = document.getElementById('btn-simulate');
  const alertBadge = document.getElementById('alert-badge');
  const leakOverlay = document.getElementById('leak-overlay-card');
  const btnDispatch = document.getElementById('btn-dispatch');
  const ticketStatus = document.getElementById('ticket-status');
  
  const mapCanvas = document.getElementById('pipeline-map-canvas');
  const mapCtx = mapCanvas.getContext('2d');
  
  const waveCanvas = document.getElementById('waveform-canvas');
  const waveCtx = waveCanvas.getContext('2d');

  // Simulation State
  let isLeakActive = false;
  let leakProgress = 0;
  let leakPosNorm = 0.456; // 68.4m along 150m span = 45.6%
  let animationFrameId = null;

  // Pipeline Topology (6 Municipal Nodes)
  const nodes = [
    { id: 1, name: "Node #1", x: 60, y: 180, label: "Valve #01" },
    { id: 2, name: "Node #2", x: 180, y: 180, label: "Meter #02" },
    { id: 3, name: "Node #3", x: 300, y: 140, label: "Hydrant #03" },
    { id: 4, name: "Node #4", x: 420, y: 140, label: "Valve #04" },
    { id: 5, name: "Node #5", x: 570, y: 220, label: "Hydrant #05" },
    { id: 6, name: "Node #6", x: 700, y: 220, label: "Valve #06" }
  ];

  function resizeCanvases() {
    mapCanvas.width = mapCanvas.clientWidth * window.devicePixelRatio;
    mapCanvas.height = mapCanvas.clientHeight * window.devicePixelRatio;
    mapCtx.scale(window.devicePixelRatio, window.devicePixelRatio);

    waveCanvas.width = waveCanvas.clientWidth * window.devicePixelRatio;
    waveCanvas.height = waveCanvas.clientHeight * window.devicePixelRatio;
    waveCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  window.addEventListener('resize', resizeCanvases);
  resizeCanvases();

  // Draw Map
  function drawMap(time) {
    const w = mapCanvas.clientWidth;
    const h = mapCanvas.clientHeight;
    mapCtx.clearRect(0, 0, w, h);

    // Draw background city grid lines
    mapCtx.strokeStyle = 'rgba(31, 41, 55, 0.4)';
    mapCtx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
      mapCtx.beginPath();
      mapCtx.moveTo(x, 0);
      mapCtx.lineTo(x, h);
      mapCtx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
      mapCtx.beginPath();
      mapCtx.moveTo(0, y);
      mapCtx.lineTo(w, y);
      mapCtx.stroke();
    }

    // Scale nodes to fit canvas width
    const scaleX = w / 800;
    const scaleY = h / 360;

    // Draw Pipeline Segments
    for (let i = 0; i < nodes.length - 1; i++) {
      const n1 = nodes[i];
      const n2 = nodes[i + 1];
      const x1 = n1.x * scaleX;
      const y1 = n1.y * scaleY;
      const x2 = n2.x * scaleX;
      const y2 = n2.y * scaleY;

      // Pipe outer casing
      mapCtx.strokeStyle = '#374151';
      mapCtx.lineWidth = 10;
      mapCtx.beginPath();
      mapCtx.moveTo(x1, y1);
      mapCtx.lineTo(x2, y2);
      mapCtx.stroke();

      // Pipe water flow inner line
      mapCtx.strokeStyle = (isLeakActive && (i === 3)) ? '#EF4444' : '#0284C7';
      mapCtx.lineWidth = 6;
      mapCtx.beginPath();
      mapCtx.moveTo(x1, y1);
      mapCtx.lineTo(x2, y2);
      mapCtx.stroke();
    }

    // Draw Nodes
    nodes.forEach((n, idx) => {
      const nx = n.x * scaleX;
      const ny = n.y * scaleY;

      // Node base circle
      mapCtx.fillStyle = (isLeakActive && (n.id === 4 || n.id === 5)) ? '#D97706' : '#0284C7';
      mapCtx.beginPath();
      mapCtx.arc(nx, ny, 9, 0, Math.PI * 2);
      mapCtx.fill();

      // Ring
      mapCtx.strokeStyle = '#FFFFFF';
      mapCtx.lineWidth = 2;
      mapCtx.stroke();

      // Label
      mapCtx.fillStyle = '#E5E7EB';
      mapCtx.font = '600 11px Plus Jakarta Sans';
      mapCtx.fillText(n.name, nx - 20, ny - 16);
      mapCtx.fillStyle = '#9CA3AF';
      mapCtx.font = '400 9px Plus Jakarta Sans';
      mapCtx.fillText(n.label, nx - 20, ny + 22);
    });

    // Draw Leak Spot if active
    if (isLeakActive) {
      const n4 = nodes[3];
      const n5 = nodes[4];
      const lx = (n4.x + (n5.x - n4.x) * leakPosNorm) * scaleX;
      const ly = (n4.y + (n5.y - n4.y) * leakPosNorm) * scaleY;

      // Pulsing alert rings
      const pulseRadius = 14 + (Math.sin(time * 0.006) + 1) * 12;
      mapCtx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
      mapCtx.lineWidth = 2;
      mapCtx.beginPath();
      mapCtx.arc(lx, ly, pulseRadius, 0, Math.PI * 2);
      mapCtx.stroke();

      // Pinpoint center marker
      mapCtx.fillStyle = '#DC2626';
      mapCtx.beginPath();
      mapCtx.arc(lx, ly, 7, 0, Math.PI * 2);
      mapCtx.fill();
      mapCtx.strokeStyle = '#FFFFFF';
      mapCtx.lineWidth = 2;
      mapCtx.stroke();

      // Flag label
      mapCtx.fillStyle = '#FEF2F2';
      mapCtx.font = '700 10px JetBrains Mono';
      mapCtx.fillText('LEAK (68.4m)', lx - 30, ly - 22);
    }
  }

  // Draw Waveforms
  let phase = 0;
  function drawWaveforms() {
    const w = waveCanvas.clientWidth;
    const h = waveCanvas.clientHeight;
    waveCtx.clearRect(0, 0, w, h);

    const centerY1 = h * 0.25;
    const centerY2 = h * 0.55;
    const centerY3 = h * 0.85;

    // Grid centerlines
    waveCtx.strokeStyle = '#1F2937';
    waveCtx.lineWidth = 1;
    [centerY1, centerY2, centerY3].forEach(cy => {
      waveCtx.beginPath();
      waveCtx.moveTo(0, cy);
      waveCtx.lineTo(w, cy);
      waveCtx.stroke();
    });

    phase += 0.08;

    // 1. Node #4 Waveform
    waveCtx.strokeStyle = '#0284C7';
    waveCtx.lineWidth = 1.5;
    waveCtx.beginPath();
    for (let x = 0; x < w; x++) {
      let amp = isLeakActive ? 22 : 6;
      let freq = isLeakActive ? 0.045 : 0.02;
      let y = centerY1 + Math.sin(x * freq + phase) * amp + (Math.random() - 0.5) * (isLeakActive ? 12 : 4);
      if (x === 0) waveCtx.moveTo(x, y); else waveCtx.lineTo(x, y);
    }
    waveCtx.stroke();

    // 2. Node #5 Waveform (Delayed by ~50ms lag)
    waveCtx.strokeStyle = '#D97706';
    waveCtx.lineWidth = 1.5;
    waveCtx.beginPath();
    const lagOffset = isLeakActive ? 24 : 0;
    for (let x = 0; x < w; x++) {
      let amp = isLeakActive ? 16 : 6;
      let freq = isLeakActive ? 0.045 : 0.02;
      let y = centerY2 + Math.sin((x - lagOffset) * freq + phase) * amp + (Math.random() - 0.5) * (isLeakActive ? 12 : 4);
      if (x === 0) waveCtx.moveTo(x, y); else waveCtx.lineTo(x, y);
    }
    waveCtx.stroke();

    // 3. Cross-Correlation Function R_AB(tau)
    waveCtx.strokeStyle = '#10B981';
    waveCtx.lineWidth = 2;
    waveCtx.beginPath();
    const peakX = w * 0.5 + (isLeakActive ? 52 : 0);
    for (let x = 0; x < w; x++) {
      let distFromPeak = Math.abs(x - peakX);
      let y = centerY3;
      if (isLeakActive) {
        let envelope = Math.exp(-0.5 * Math.pow(distFromPeak / 18, 2));
        y -= envelope * 32 * Math.cos(distFromPeak * 0.2);
      } else {
        y += (Math.random() - 0.5) * 6;
      }
      if (x === 0) waveCtx.moveTo(x, y); else waveCtx.lineTo(x, y);
    }
    waveCtx.stroke();

    // Peak Marker
    if (isLeakActive) {
      waveCtx.strokeStyle = '#DC2626';
      waveCtx.setLineDash([4, 4]);
      waveCtx.beginPath();
      waveCtx.moveTo(peakX, centerY3 - 35);
      waveCtx.lineTo(peakX, centerY3 + 15);
      waveCtx.stroke();
      waveCtx.setLineDash([]);

      waveCtx.fillStyle = '#EF4444';
      waveCtx.font = '700 9px JetBrains Mono';
      waveCtx.fillText('PEAK TAU = +50.56ms', peakX + 6, centerY3 - 20);
    }
  }

  function loop(time) {
    drawMap(time);
    drawWaveforms();
    animationFrameId = requestAnimationFrame(loop);
  }

  animationFrameId = requestAnimationFrame(loop);

  // Simulation Trigger
  btnSimulate.addEventListener('click', () => {
    isLeakActive = !isLeakActive;

    if (isLeakActive) {
      btnSimulate.textContent = 'RESET MONITORING';
      btnSimulate.style.background = '#4B5563';
      alertBadge.textContent = 'LEAK CONFIRMED';
      alertBadge.style.color = '#EF4444';
      alertBadge.style.background = 'rgba(239, 68, 68, 0.2)';

      leakOverlay.classList.remove('hidden');
      btnDispatch.disabled = false;
      ticketStatus.textContent = 'PENDING DISPATCH';
      ticketStatus.style.color = '#EF4444';

      document.getElementById('status-node-4').textContent = 'EVENT FLAGGED';
      document.getElementById('status-node-4').className = 'status-alert';
      document.getElementById('noise-node-4').textContent = '74 dB (BURST)';

      document.getElementById('status-node-5').textContent = 'EVENT FLAGGED';
      document.getElementById('status-node-5').className = 'status-alert';
      document.getElementById('noise-node-5').textContent = '68 dB (BURST)';
    } else {
      btnSimulate.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path></svg> SIMULATE PIPE LEAK';
      btnSimulate.style.background = 'linear-gradient(135deg, #DC2626, #B91C1C)';
      alertBadge.textContent = 'NORMAL MONITORING';
      alertBadge.style.color = '#10B981';
      alertBadge.style.background = 'rgba(16, 185, 129, 0.2)';

      leakOverlay.classList.add('hidden');
      btnDispatch.disabled = true;
      ticketStatus.textContent = 'STANDBY';
      ticketStatus.style.color = '#9CA3AF';

      document.getElementById('status-node-4').textContent = 'LISTENING';
      document.getElementById('status-node-4').className = 'status-ok';
      document.getElementById('noise-node-4').textContent = '44 dB';

      document.getElementById('status-node-5').textContent = 'LISTENING';
      document.getElementById('status-node-5').className = 'status-ok';
      document.getElementById('noise-node-5').textContent = '45 dB';
    }
  });

  btnDispatch.addEventListener('click', () => {
    ticketStatus.textContent = 'CREW EN ROUTE (GPS DISPATCHED)';
    ticketStatus.style.color = '#38BDF8';
    btnDispatch.textContent = 'CREW ASSIGNED: TRUCK #14 (ETA 18 MINS)';
    btnDispatch.style.background = '#059669';
    alert("Municipal Work Order Dispatched!\nExcavation Crew assigned to: 68.4 m East of Valve Chamber #04.\nTarget pinpointed with zero trial trenching!");
  });
});
