'use strict';
// Deterministic canvas-2D promo FX. Pure functions of time args only.
// No wall-clock, no RNG, no stylesheets. All state changes wrapped in save/restore.
function fract(v) { return v - Math.floor(v); }
function hash(i) { return fract(Math.sin(i * 127.1) * 43758.5453); }
function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
function easeInOut(p) { p = clamp01(p); return p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; }
function prog(t, t0, dur) { if (!(dur > 0)) return t >= t0 ? 1 : 0; return clamp01((t - t0) / dur); }
function lerp(a, b, t) { return a + (b - a) * t; }

// Full-screen directional motion-blur streak wipe. dir=0 horizontal, dir=1 vertical.
function whip(x, W, H, t, t0, dur, dir, rgb) {
  var p = prog(t, t0, dur);
  if (p <= 0 || p >= 1) return;
  var env = Math.sin(Math.PI * p), e = easeInOut(p), N = 60, i, h, L, head, a;
  x.save();
  try {
    if (dir === 1) {
      for (i = 0; i < N; i++) {
        h = hash(i);
        L = (0.15 + hash(i + 23) * 0.35) * H;
        head = -L + e * (H + 2 * L) + (hash(i + 37) - 0.5) * 80;
        a = env * (0.25 + 0.75 * hash(i + 53));
        x.fillStyle = 'rgba(' + rgb + ',' + a.toFixed(4) + ')';
        x.fillRect(h * W, head - L, 2 + hash(i + 11) * 10, L);
      }
    } else {
      for (i = 0; i < N; i++) {
        h = hash(i);
        L = (0.15 + hash(i + 23) * 0.35) * W;
        head = -L + e * (W + 2 * L) + (hash(i + 37) - 0.5) * 80;
        a = env * (0.25 + 0.75 * hash(i + 53));
        x.fillStyle = 'rgba(' + rgb + ',' + a.toFixed(4) + ')';
        x.fillRect(head - L, h * H, L, 2 + hash(i + 11) * 10);
      }
    }
  } finally { x.restore(); }
}

// Circle iris mask reveal. Clips everything drawn after until irisEnd. Uses canvas size for invert.
function iris(x, cx, cy, r0, r1, t, t0, dur, invert) {
  var p = prog(t, t0, dur);
  var r = Math.max(lerp(r0, r1, easeInOut(p)), 0.001);
  x.save();
  x.beginPath();
  if (invert) {
    var W = x.canvas.width, H = x.canvas.height;
    x.rect(0, 0, W, H);
    x.moveTo(cx + r, cy);
    x.arc(cx, cy, r, 0, Math.PI * 2, true);
    x.clip('evenodd');
  } else {
    x.moveTo(cx + r, cy);
    x.arc(cx, cy, r, 0, Math.PI * 2);
    x.clip();
  }
}
function irisEnd(x) { x.restore(); }

// nBars sliding vertical bars with per-bar stagger. Returns coverage 0..1.
function barWipe(x, W, H, t, t0, dur, nBars, rgb) {
  var p = prog(t, t0, dur);
  nBars = Math.max(1, Math.floor(nBars));
  var bw = W / nBars, SPAN = 0.35, sum = 0, i, pi, ei;
  x.save();
  try {
    x.fillStyle = 'rgb(' + rgb + ')';
    for (i = 0; i < nBars; i++) {
      pi = clamp01((p - hash(i) * SPAN) / (1 - SPAN));
      ei = easeInOut(pi);
      sum += ei;
      if (ei > 0) x.fillRect(i * bw, H - ei * H, bw + 1, ei * H);
    }
  } finally { x.restore(); }
  return sum / nBars;
}

// Diagonal wipe with glowing leading edge.
function diagWipe(x, W, H, t, t0, dur, rgb) {
  var p = prog(t, t0, dur);
  if (p <= 0) return;
  var d = lerp(-H, W + H, easeInOut(p));
  x.save();
  try {
    x.fillStyle = 'rgb(' + rgb + ')';
    x.beginPath();
    x.moveTo(0, 0); x.lineTo(d, 0); x.lineTo(d - H, H); x.lineTo(0, H);
    x.closePath(); x.fill();
    if (p > 0 && p < 1) {
      x.save();
      try {
        x.strokeStyle = 'rgba(255,255,255,0.95)';
        x.lineWidth = 6;
        x.shadowColor = 'rgba(255,255,255,0.9)';
        x.shadowBlur = 30;
        x.beginPath(); x.moveTo(d, 0); x.lineTo(d - H, H); x.stroke();
      } finally { x.restore(); }
    }
  } finally { x.restore(); }
}

// Motion blur for any drawing fn. drawFn(time) closes over ctx.
function ghost(x, drawFn, t, dt, steps, alpha) {
  steps = Math.max(1, Math.floor(steps));
  var k, tk;
  x.save();
  try {
    for (k = steps - 1; k >= 0; k--) {
      tk = t - k * dt / steps;
      x.save();
      try {
        x.globalAlpha = alpha * (1 - k / steps);
        drawFn(tk);
      } finally { x.restore(); }
    }
  } finally { x.restore(); }
}

var FX = { whip: whip, iris: iris, irisEnd: irisEnd, barWipe: barWipe, diagWipe: diagWipe, ghost: ghost };
if (typeof module !== 'undefined' && module.exports) module.exports = FX;
if (typeof globalThis !== 'undefined') globalThis.FX = FX;
