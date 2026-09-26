const EMERALD = [16, 185, 129];
const GOLD = [201, 162, 39];
const BG3D_SEED = 0x1B873593;

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    var t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function h01(i, salt) {
  var h = (Math.imul(i + 1, 374761393) + Math.imul(salt + 1, 668265263)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967295;
}

function rgba(c, a) {
  return "rgba(" + (c[0] | 0) + "," + (c[1] | 0) + "," + (c[2] | 0) + "," + a.toFixed(3) + ")";
}

var __bg3dCache = null;
function __bg3dSprites() {
  if (__bg3dCache) return __bg3dCache;
  function dot(c) {
    var s = 48, cv = document.createElement("canvas");
    cv.width = s; cv.height = s;
    var g = cv.getContext("2d");
    var rg = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
    rg.addColorStop(0, rgba(c, 1));
    rg.addColorStop(0.35, rgba(c, 0.55));
    rg.addColorStop(1, rgba(c, 0));
    g.fillStyle = rg;
    g.fillRect(0, 0, s, s);
    return cv;
  }
  __bg3dCache = { e: dot(EMERALD), g: dot(GOLD) };
  return __bg3dCache;
}

function drawBackdrop(x, W, H, t, m0, m1, m2, m3) {
  var frame = Math.floor(t*30);
  var rng = mulberry32(BG3D_SEED + Math.floor(t*30));
  var shimmer = 0.85 + 0.30 * rng();
  var cx = W * 0.5, cy = H * 0.52;
  var maxR = Math.sqrt(W * W + H * H) * 0.5;

  x.save();
  x.lineJoin = "round";
  x.lineCap = "round";

  // soft inky center aura (additive, no clearing)
  var auraW = (m0 + m1 + m2 + m3);
  if (auraW > 0.01) {
    x.save();
    x.globalCompositeOperation = "lighter";
    var ag = x.createRadialGradient(cx, cy, 0, cx, cy, maxR);
    ag.addColorStop(0, rgba(EMERALD, 0.10 * Math.min(1, auraW) * shimmer));
    ag.addColorStop(0.55, rgba(GOLD, 0.05 * Math.min(1, auraW)));
    ag.addColorStop(1, "rgba(0,0,0,0)");
    x.fillStyle = ag;
    x.beginPath();
    x.arc(cx, cy, maxR, 0, 6.28318530718);
    x.fill();
    x.restore();
  }

  // mode 0: concentric rings
  if (m0 > 0.01) {
    x.save();
    x.globalCompositeOperation = "lighter";
    var N0 = 14, k, r, prog;
    for (k = 0; k < N0; k++) {
      prog = ((k / N0) + t * 0.045 + frame * 0.0) % 1;
      if (prog < 0) prog += 1;
      r = 20 + prog * (maxR - 20);
      var fade = (1 - prog) * m0 * 0.42 * shimmer;
      if (fade < 0.004) continue;
      x.beginPath();
      x.arc(cx, cy, r, t * 0.15 + k * 0.35, t * 0.15 + k * 0.35 + 5.1);
      x.lineWidth = 1 + 3 * (1 - prog);
      x.strokeStyle = (k % 3 === 2) ? rgba(GOLD, fade) : rgba(EMERALD, fade);
      x.shadowBlur = (k < 2) ? 16 : 0;
      x.shadowColor = (k % 3 === 2) ? rgba(GOLD, 0.8) : rgba(EMERALD, 0.8);
      x.stroke();
    }
    x.restore();
  }

  // mode 1: sine-wave field
  if (m1 > 0.01) {
    x.save();
    x.globalCompositeOperation = "lighter";
    var lines = 20, segs = 44, j, s, px, py, yB, amp;
    var lg = x.createLinearGradient(0, 0, W, 0);
    lg.addColorStop(0, rgba(EMERALD, 0.55 * m1));
    lg.addColorStop(0.5, rgba(GOLD, 0.45 * m1));
    lg.addColorStop(1, rgba(EMERALD, 0.55 * m1));
    x.strokeStyle = lg;
    x.shadowBlur = 0;
    x.lineWidth = 1.6;
    for (j = 0; j < lines; j++) {
      yB = ((j + 0.5) / lines) * H;
      amp = (8 + 30 * h01(j, 7)) * (0.35 + 0.65 * m1);
      x.globalAlpha = (0.10 + 0.30 * (1 - Math.abs(j / lines - 0.52) * 2)) * m1 * shimmer + 0.02;
      if (x.globalAlpha < 0.01) continue;
      x.beginPath();
      for (s = 0; s <= segs; s++) {
        px = (s / segs) * W;
        py = yB + Math.sin(px * 0.006 + t * 1.7 + j * 0.75) * amp
               + Math.sin(px * 0.0017 - t * 0.9 + j * 1.3) * amp * 0.6;
        if (s === 0) x.moveTo(px, py);
        else x.lineTo(px, py);
      }
      x.stroke();
    }
    x.restore();
  }

  // mode 2: perspective-grid floor
  if (m2 > 0.01) {
    x.save();
    x.globalCompositeOperation = "lighter";
    x.shadowBlur = 0;
    var hy = H * 0.52, vx = W * 0.5, i, bx;
    x.lineWidth = 1.4;
    x.strokeStyle = rgba(EMERALD, 0.34 * m2 * shimmer);
    x.beginPath();
    for (i = -11; i <= 11; i++) {
      bx = vx + i * W * 0.11 + Math.sin(t * 0.4) * 6;
      x.moveTo(vx, hy);
      x.lineTo(bx, H + 20);
    }
    x.stroke();
    x.strokeStyle = rgba(GOLD, 0.30 * m2);
    x.beginPath();
    x.moveTo(0, hy);
    x.lineTo(W, hy);
    x.stroke();
    var rows = 10, rk, p, yy;
    x.lineWidth = 1.2;
    for (rk = 0; rk < rows; rk++) {
      p = ((rk / rows) + t * 0.14) % 1;
      if (p < 0) p += 1;
      yy = hy + (H - hy) * p * p;
      x.globalAlpha = (0.08 + 0.30 * p) * m2;
      x.strokeStyle = (rk % 3 === 1) ? rgba(GOLD, 0.32 * m2 * (0.3 + 0.7 * p)) : rgba(EMERALD, 0.32 * m2 * (0.3 + 0.7 * p));
      x.beginPath();
      x.moveTo(0, yy);
      x.lineTo(W, yy);
      x.stroke();
    }
    x.restore();
  }

  // mode 3: particle streaks (stable hash positions, motion via t only)
  if (m3 > 0.01) {
    x.save();
    x.globalCompositeOperation = "lighter";
    x.shadowBlur = 0;
    var N3 = 130, pi;
    var spd = H * 0.12;
    x.lineWidth = 2;
    // emerald batch
    x.strokeStyle = rgba(EMERALD, 0.55 * m3);
    x.beginPath();
    for (pi = 0; pi < N3; pi += 2) {
      var bx0 = h01(pi, 11) * W;
      var by0 = h01(pi, 23) * (H + 200);
      var yy3 = ((by0 - t * spd * (0.5 + h01(pi, 5))) % (H + 200) + (H + 200)) % (H + 200) - 100;
      var xx3 = bx0 + Math.sin(t * 0.8 + pi * 1.7) * 24;
      var len = 14 + h01(pi, 31) * 46;
      x.moveTo(xx3, yy3);
      x.lineTo(xx3 - 6, yy3 + len);
    }
    x.stroke();
    // gold batch
    x.strokeStyle = rgba(GOLD, 0.5 * m3 * shimmer);
    x.beginPath();
    for (pi = 1; pi < N3; pi += 2) {
      var bx1 = h01(pi, 11) * W;
      var by1 = h01(pi, 23) * (H + 200);
      var yy4 = ((by1 - t * spd * (0.5 + h01(pi, 5))) % (H + 200) + (H + 200)) % (H + 200) - 100;
      var xx4 = bx1 + Math.cos(t * 0.7 + pi * 2.1) * 24;
      var len2 = 14 + h01(pi, 31) * 46;
      x.moveTo(xx4, yy4);
      x.lineTo(xx4 + 6, yy4 + len2);
    }
    x.stroke();
    // sprite heads for brightest few (drawImage of tiny offscreen canvas)
    try {
      var sp = __bg3dSprites();
      var heads = 36;
      for (pi = 0; pi < heads; pi++) {
        var hxp = h01(pi * 3, 41) * W;
        var hyp = h01(pi * 3, 53) * (H + 200);
        var hyy = ((hyp - t * spd * (0.5 + h01(pi * 3, 5))) % (H + 200) + (H + 200)) % (H + 200) - 100;
        var hxx = hxp + Math.sin(t * 0.8 + pi * 3 * 1.7) * 24;
        var sz = 8 + h01(pi * 3, 61) * 18;
        x.globalAlpha = 0.35 * m3 + 0.1 * rng() * m3;
        var img = (pi % 3 === 1) ? sp.g : sp.e;
        x.drawImage(img, hxx - sz / 2, hyy - sz / 2, sz, sz);
      }
    } catch (e) {}
    x.restore();
  }

  x.restore();
}
