/* uiwin.js — deterministic canvas-2D "fake desktop windows" for promo films.
 * Browser globals, no modules, no CSS, no timers, no RNG: every draw is a pure
 * function of the clock t, so renders are reproducible frame for frame.
 *
 * Design space: 1920x1080 (scale 0.5 for 960x540). Strokes stay >= 1.5px and
 * callers should pass body size >= 22px so the picture still reads at 50%.
 *
 *   uiWindow(x, cx, cy, w, h, opts) -> {x, y, w, h} content rect
 *     opts {title, dark=true, accent:[r,g,b], shadow:0..1, alpha, win, titleSize}
 *   uiText(x, text, x0, y0, size, t, t0, cps, opts)
 *     opts {rgb, caret:[r,g,b], wrapW, lineH, alpha, hl:[r,g,b]}
 *   uiCursor(x, px, py, click, t)
 *   uiPasteFlash(x, cx, cy, w, h, p, rgb)
 *   uiZoomFrame(x, contentFn, cx, cy, w, h, zoom, alpha)
 */
(function (G) {
  'use strict';

  var UI = '"Segoe UI", "SF Pro Text", system-ui, sans-serif';
  var MONO = '"Cascadia Mono", Consolas, "Courier New", monospace';
  var HAIR = 1.5;

  function rr(x, l, t, w, h, r) {
    r = Math.max(0, Math.min(r, w * 0.5, h * 0.5));
    x.beginPath();
    x.moveTo(l + r, t);
    x.arcTo(l + w, t, l + w, t + h, r);
    x.arcTo(l + w, t + h, l, t + h, r);
    x.arcTo(l, t + h, l, t, r);
    x.arcTo(l, t, l + w, t, r);
    x.closePath();
  }

  function uiWindow(x, cx, cy, w, h, opts) {
    opts = opts || {};
    var dark = opts.dark !== false;
    var l = cx - w * 0.5, t = cy - h * 0.5, r = 14;
    var tb = Math.max(32, Math.min(56, h * 0.09));
    var pad = Math.max(14, Math.min(32, Math.min(w, h) * 0.045));
    var ink = dark ? 'rgba(236,237,242,0.92)' : 'rgba(28,29,34,0.88)';
    var bg = dark ? '#1b1c22' : '#f6f7f9';
    var sh = opts.shadow == null ? 0.35 : Math.max(0, opts.shadow);

    x.save();
    x.globalAlpha *= opts.alpha == null ? 1 : opts.alpha;

    if (sh > 0) {
      x.shadowColor = 'rgba(0,0,0,' + Math.min(1, sh * 0.62).toFixed(3) + ')';
      x.shadowBlur = 26 * sh;
      x.shadowOffsetY = 11 * sh;
      x.fillStyle = bg;
      rr(x, l, t, w, h, r);
      x.fill();
      x.shadowColor = 'rgba(0,0,0,0)';
      x.shadowBlur = 0;
      x.shadowOffsetY = 0;
    }

    x.fillStyle = bg;
    rr(x, l, t, w, h, r);
    x.fill();

    x.save();
    rr(x, l, t, w, h, r);
    x.clip();
    x.fillStyle = dark ? '#26272e' : '#eceef2';
    x.fillRect(l, t, w, tb);
    x.restore();

    var my = t + tb * 0.5, i;
    if (opts.win) {
      var gs = Math.max(9, Math.min(13, tb * 0.21));
      var st = gs * 2.7, gx = l + w - pad * 0.9;
      x.strokeStyle = ink;
      x.lineWidth = HAIR;
      x.lineCap = 'round';
      x.lineJoin = 'round';
      x.beginPath();
      x.moveTo(gx - 2 * st - gs * 0.5, my);
      x.lineTo(gx - 2 * st + gs * 0.5, my);
      x.stroke();
      x.strokeRect(gx - st - gs * 0.5, my - gs * 0.5, gs, gs);
      x.beginPath();
      x.moveTo(gx - gs * 0.5, my - gs * 0.5);
      x.lineTo(gx + gs * 0.5, my + gs * 0.5);
      x.moveTo(gx + gs * 0.5, my - gs * 0.5);
      x.lineTo(gx - gs * 0.5, my + gs * 0.5);
      x.stroke();
    } else {
      var dr = Math.max(5.5, Math.min(8, tb * 0.12));
      var dx = l + pad * 1.05 + dr;
      var cols = ['#ff5f57', '#febc2e', '#28c840'];
      for (i = 0; i < 3; i++) {
        x.fillStyle = cols[i];
        x.beginPath();
        x.arc(dx + i * dr * 3.1, my, dr, 0, Math.PI * 2);
        x.fill();
      }
    }

    if (opts.title) {
      x.fillStyle = ink;
      x.font = '600 ' + (opts.titleSize || Math.max(15, Math.min(22, tb * 0.4))) + 'px ' + UI;
      x.textAlign = 'center';
      x.textBaseline = 'middle';
      x.fillText(opts.title, cx, my, w - pad * 4);
    }

    if (opts.accent) {
      var a = opts.accent;
      x.fillStyle = 'rgba(' + a[0] + ',' + a[1] + ',' + a[2] + ',0.9)';
      rr(x, l + r + 4, t + 2, w - 2 * (r + 4), 6, 3);
      x.fill();
    }

    x.strokeStyle = dark ? 'rgba(255,255,255,0.16)' : 'rgba(20,21,26,0.18)';
    x.lineWidth = HAIR;
    rr(x, l + HAIR * 0.5, t + HAIR * 0.5, w - HAIR, h - HAIR, r);
    x.stroke();
    x.restore();

    return {
      x: l + pad,
      y: t + tb + pad * 0.55,
      w: w - pad * 2,
      h: Math.max(0, h - tb - pad * 1.55)
    };
  }

  function wrapPara(x, text, a, b, wrapW, out) {
    if (wrapW <= 0) {
      out.push({ a: a, b: b });
      return;
    }
    var i = a;
    while (i < b) {
      var end = fit(x, text, i, b, wrapW);
      out.push({ a: i, b: end });
      i = end;
    }
  }

  function fit(x, text, a, b, wrapW) {
    var lo = a + 1, hi = b, best = a + 1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (x.measureText(text.substring(a, mid)).width <= wrapW) {
        best = mid;
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
    if (best < b) {
      var sp = text.lastIndexOf(' ', best);
      if (sp >= a) return sp + 1;
    }
    return best;
  }

  function wrapLines(x, text, wrapW) {
    var out = [], start = 0, p;
    for (p = 0; p <= text.length; p++) {
      if (p === text.length || text.charCodeAt(p) === 10) {
        wrapPara(x, text, start, p, wrapW, out);
        start = p + 1;
      }
    }
    if (!out.length) out.push({ a: 0, b: 0 });
    return out;
  }

  function uiText(x, text, x0, y0, size, t, t0, cps, opts) {
    opts = opts || {};
    if (!text || t < t0) return;
    var alpha = opts.alpha == null ? 1 : opts.alpha;
    if (alpha <= 0) return;
    var rgb = opts.rgb || [232, 233, 238];
    var ink = 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
    var lh = opts.lineH || Math.round(size * 1.5);
    var n = cps > 0 ? Math.floor((t - t0) * cps) : text.length;
    if (n < 0) n = 0;
    if (n > text.length) n = text.length;

    x.save();
    x.globalAlpha *= alpha;
    x.font = size + 'px ' + MONO;
    x.textAlign = 'left';
    x.textBaseline = 'top';

    var lines = wrapLines(x, text, opts.wrapW || 0);
    var caretW = Math.round(x.measureText('M').width);
    var active = 0, k;
    for (k = 0; k < lines.length; k++) {
      if (lines[k].a <= n) active = k;
    }

    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i];
      var show = Math.max(0, Math.min(n - ln.a, ln.b - ln.a));
      if (show <= 0 && i !== active) continue;
      var y = y0 + i * lh;
      var vis = text.substr(ln.a, show);

      if (opts.hl && i === active && show > 0) {
        var ws = vis.replace(/\s+$/, '');
        var idx = ws.lastIndexOf(' ') + 1;
        var hx = x.measureText(ws.substr(0, idx)).width;
        var hw = x.measureText(ws.substr(idx)).width;
        x.fillStyle = 'rgba(' + opts.hl[0] + ',' + opts.hl[1] + ',' + opts.hl[2] + ',0.30)';
        x.fillRect(x0 + hx - 3, y - 2, hw + 6, Math.round(size * 1.3) + 4);
      }

      if (show > 0) {
        x.fillStyle = ink;
        x.fillText(vis, x0, y);
      }

      if (i === active && Math.floor(t * 2.2) % 2 === 0) {
        var cc = opts.caret || rgb;
        x.fillStyle = 'rgb(' + cc[0] + ',' + cc[1] + ',' + cc[2] + ')';
        x.fillRect(
          x0 + x.measureText(vis).width,
          y - Math.round(size * 0.06),
          caretW,
          Math.round(size * 1.3)
        );
      }
    }
    x.restore();
  }

  var ARROW = [[0, 0], [0, 17.4], [4.5, 13.2], [7.4, 19.8], [10.4, 18.4], [7.7, 12.1], [13.1, 12.1]];

  function uiCursor(x, px, py, click, t) {
    var s = 1.6, i;
    x.save();
    x.translate(px, py);
    x.scale(s, s);
    x.beginPath();
    x.moveTo(ARROW[0][0], ARROW[0][1]);
    for (i = 1; i < ARROW.length; i++) x.lineTo(ARROW[i][0], ARROW[i][1]);
    x.closePath();
    x.fillStyle = '#ffffff';
    x.fill();
    x.lineJoin = 'round';
    x.strokeStyle = 'rgba(10,10,12,0.9)';
    x.lineWidth = HAIR;
    x.stroke();
    x.restore();

    if (click > 0 && click <= 1) {
      var al = 1 - click;
      var rad = (7 + 24 * click) * s;
      x.save();
      x.beginPath();
      x.arc(px, py, rad, 0, Math.PI * 2);
      x.lineWidth = 4.6;
      x.strokeStyle = 'rgba(12,13,16,' + (0.32 * al).toFixed(3) + ')';
      x.stroke();
      x.beginPath();
      x.arc(px, py, rad, 0, Math.PI * 2);
      x.lineWidth = 2.2;
      x.strokeStyle = 'rgba(255,255,255,' + (0.95 * al).toFixed(3) + ')';
      x.stroke();
      x.restore();
    }
  }

  function uiPasteFlash(x, cx, cy, w, h, p, rgb) {
    if (!rgb || p <= 0 || p >= 1) return;
    var a = Math.sin(Math.PI * p);
    var l = cx - w * 0.5, t = cy - h * 0.5;
    var bw = w * 0.38, sk = h * 0.35;
    var x0 = l - bw + p * (w + 2 * bw);
    var c = 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',';

    x.save();
    var g = x.createLinearGradient(x0, 0, x0 + bw, 0);
    g.addColorStop(0, c + '0)');
    g.addColorStop(0.5, c + (0.40 * a).toFixed(3) + ')');
    g.addColorStop(1, c + '0)');
    x.fillStyle = g;
    x.beginPath();
    x.moveTo(x0, t);
    x.lineTo(x0 + bw, t);
    x.lineTo(x0 + bw - sk, t + h);
    x.lineTo(x0 - sk, t + h);
    x.closePath();
    x.fill();

    x.strokeStyle = c + (0.55 * a).toFixed(3) + ')';
    x.lineWidth = HAIR;
    rr(x, l + HAIR * 0.5, t + HAIR * 0.5, w - HAIR, h - HAIR, 10);
    x.stroke();
    x.restore();
  }

  function uiZoomFrame(x, contentFn, cx, cy, w, h, zoom, alpha) {
    x.save();
    if (alpha != null) x.globalAlpha *= alpha;
    rr(x, cx - w * 0.5, cy - h * 0.5, w, h, 14);
    x.clip();
    x.translate(cx, cy);
    x.scale(zoom, zoom);
    x.translate(-cx, -cy);
    contentFn(alpha == null ? 1 : alpha);
    x.restore();
  }

  G.uiWindow = uiWindow;
  G.uiText = uiText;
  G.uiCursor = uiCursor;
  G.uiPasteFlash = uiPasteFlash;
  G.uiZoomFrame = uiZoomFrame;
})(typeof globalThis !== 'undefined' ? globalThis : this);
