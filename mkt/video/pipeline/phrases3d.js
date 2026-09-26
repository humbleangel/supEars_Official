/* phrases3d.js - deterministic 3D flying-text field on canvas 2D (headless-safe).
   Browser global `phraseField`; also module.exports for node checks.
   Pure function of t: no Date.now, no Math.random, no CSS, no per-item state.
   Perf: one fillText per visible item, ordered far->near. Measure with
   performance.now() around the call site when profiling (never in this path);
   ­60 items @ 960x540 stays well under 40ms in headless Chromium. */

var phraseField = (function () {
  'use strict';

  var TAU = 6.283185307179586;

  function hash01(n) {
    n = (n ^ 61) ^ (n >>> 16);
    n = (n + (n << 3)) | 0;
    n = n ^ (n >>> 4);
    n = Math.imul(n, 0x27d4eb2d);
    n = n ^ (n >>> 15);
    return (n >>> 0) / 4294967296;
  }

  function phaseOf(i, seed) {
    return hash01(((i + 1) * 1013904223) ^ (seed | 0)) * TAU;
  }

  function phraseField(ctx, W, H, t, items, cam, opts) {
    if (!ctx || typeof ctx.fillText !== 'function' || !items || !items.length) return;
    opts = opts || {};
    cam = cam || {};

    var fadeNear = opts.fadeNear != null ? opts.fadeNear : 80;
    var fadeFar = opts.fadeFar != null ? opts.fadeFar : 1400;
    var maxAlpha = opts.maxAlpha != null ? opts.maxAlpha : 1;
    var glow = opts.glow != null ? opts.glow : 0;
    var tiltMax = opts.tiltMax != null ? opts.tiltMax : 0.6;
    var seed = opts.seed | 0;
    var camX = cam.x || 0;
    var camY = cam.y || 0;
    var F = 900 * (cam.z > 0 ? cam.z : 1);
    var span = (fadeFar - fadeNear) || 1;
    var cx = W * 0.5;
    var cy = H * 0.5;

    var n = items.length;
    var order = new Array(n);
    for (var i = 0; i < n; i++) order[i] = i;
    if (n > 1) {
      order.sort(function (a, b) {
        return (items[b].z + (items[b].vz || 0) * t) - (items[a].z + (items[a].vz || 0) * t);
      });
    }

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (var k = 0; k < n; k++) {
      var idx = order[k];
      var it = items[idx];
      var z = it.z + (it.vz || 0) * t;
      if (!(z > fadeNear) || z >= fadeFar) continue;

      var a = ((fadeFar - z) / span) * maxAlpha;
      if (a > 1) a = 1; else if (a < 0) a = 0;
      if (a <= 0) continue;

      var scale = F / z;
      var sway = Math.sin(t * 0.6 + phaseOf(idx, seed)) * 3;
      var sx = cx + (it.x + (it.vx || 0) * t + sway - camX) * scale;
      var sy = cy + (it.y + (it.vy || 0) * t - camY) * scale;

      var xScale = scale * Math.max(0.08, Math.abs(Math.cos(it.rotY || 0)));
      var tilt = (it.rotX || 0) * 0.35;
      if (tilt > tiltMax) tilt = tiltMax; else if (tilt < -tiltMax) tilt = -tiltMax;

      var rgb = it.rgb || [255, 255, 255];
      ctx.save();
      ctx.globalAlpha = a;
      ctx.translate(sx, sy);
      ctx.transform(xScale, tilt * scale, 0, scale, 0, 0);
      ctx.font = (it.weight || 400) + ' ' + (it.size || 40) + 'px "Segoe UI", "Segoe UI Variable Text", system-ui, sans-serif';
      ctx.letterSpacing = (it.track || 0) + 'px';
      ctx.fillStyle = 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
      if (glow > 0) {
        ctx.shadowBlur = glow;
        ctx.shadowColor = ctx.fillStyle;
      }
      ctx.fillText(it.text, 0, 0);
      ctx.restore();
    }
    // ponytail: cam.rot is ignored; projection contract defines no roll. Add
    // ctx.translate/rotate around (cx, cy) if the rig ever needs camera roll.
  }

  return phraseField;
})();

if (typeof module !== 'undefined' && module.exports) module.exports = { phraseField: phraseField };
