function ktype(x, text, cx, cy, size, t, t0, dur, opts) {
  opts = opts || {};
  var weight = opts.weight || 800;
  var track = opts.track || 0;
  var rgb = opts.rgb || [255, 255, 255];
  var glow = opts.glow || null;
  var extrude = Math.max(0, Math.min(12, Math.floor(opts.extrude || 0)));
  var jitter = Math.max(0, Math.min(1, +opts.jitter || 0));
  var cps = opts.cps || Math.max(8, Math.min(40, 1200 / size));
  var hold = (opts.hold == null) ? 0.8 : Math.max(0, Math.min(0.99, +opts.hold));
  var align = opts.align || "center";
  var s = String(text == null ? "" : text);
  if (!s || !(size > 0) || !(dur > 0)) return;
  var el = t - t0;
  if (el < 0 || el > dur) return;
  var p = el / dur;
  var chars = Array.from(s);
  var count = chars.length;
  if (!count) return;
  var shown = Math.min(count, Math.floor(el * cps) + 1);
  var STACK = '"Segoe UI", Inter, system-ui, sans-serif';
  x.save();
  x.textAlign = "center";
  x.textBaseline = "middle";
  x.font = weight + " " + size + 'px ' + STACK;
  var widths = new Array(count);
  var total = 0;
  var i;
  for (i = 0; i < count; i++) { widths[i] = x.measureText(chars[i]).width; total += widths[i]; }
  total += track * (count - 1);
  var startX = align === "left" ? cx : align === "right" ? cx - total : cx - total / 2;
  var fadeP = p <= hold ? 0 : (p - hold) / (1 - hold);
  var gA = 1 - fadeP;
  var zoom = 1 + 0.12 * fadeP * fadeP;
  var baseA = x.globalAlpha == null ? 1 : x.globalAlpha;
  var c1 = 1.70158, c3 = c1 + 1;
  var acc = 0;
  for (i = 0; i < shown; i++) {
    var age = el - i / cps;
    if (age < 0) { acc += widths[i] + track; continue; }
    var k = age >= 0.16 ? 1 : age / 0.16;
    var om = k - 1;
    var ease = 1 + c3 * om * om * om + c1 * om * om;
    var csc = 1.35 - 0.35 * ease;
    var cA = age >= 0.08 ? 1 : age / 0.08;
    var jy = jitter ? jitter * size * 0.1 * Math.sin(t * 6 + i * 0.9) : 0;
    var px = startX + acc + widths[i] / 2;
    acc += widths[i] + track;
    var zx = cx + (px - cx) * zoom;
    var zy = cy + jy * zoom;
    var fs = size * csc * zoom;
    if (fs <= 0) continue;
    x.font = weight + " " + fs + 'px ' + STACK;
    x.globalAlpha = baseA * gA * cA;
    x.shadowBlur = 0;
    var e, f, st;
    if (extrude > 0) {
      st = Math.max(1, fs * 0.035);
      for (e = extrude; e >= 1; e--) {
        f = 0.3 * (1 - e / (extrude + 2));
        x.fillStyle = "rgb(" + Math.round(rgb[0] * f) + "," + Math.round(rgb[1] * f) + "," + Math.round(rgb[2] * f) + ")";
        x.fillText(chars[i], zx + e * st, zy + e * st);
      }
    }
    x.fillStyle = "rgb(" + (rgb[0] | 0) + "," + (rgb[1] | 0) + "," + (rgb[2] | 0) + ")";
    if (glow) {
      x.shadowColor = "rgb(" + (glow[0] | 0) + "," + (glow[1] | 0) + "," + (glow[2] | 0) + ")";
      x.shadowBlur = fs * 0.35;
    }
    x.fillText(chars[i], zx, zy);
    x.shadowBlur = 0;
  }
  x.restore();
}
if (typeof globalThis !== "undefined") globalThis.ktype = ktype;
if (typeof module !== "undefined" && module.exports) module.exports = ktype;
