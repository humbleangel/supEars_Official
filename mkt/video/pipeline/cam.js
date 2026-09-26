function camTrack(t, keys) {
  var F = ['x', 'y', 'z', 'rot', 'shake'];
  if (!keys || !keys.length) return { x: 0, y: 0, z: 1, rot: 0, shake: 0 };
  var held = { x: 0, y: 0, z: 1, rot: 0, shake: 0 };
  var ks = [];
  for (var i = 0; i < keys.length; i++) {
    var k = keys[i];
    for (var j = 0; j < F.length; j++) if (k[F[j]] !== undefined) held[F[j]] = k[F[j]];
    ks.push({ t: k.t, ease: k.ease || 'smooth', v: { x: held.x, y: held.y, z: held.z, rot: held.rot, shake: held.shake } });
  }
  var last = ks[ks.length - 1].v;
  if (t <= ks[0].t) return { x: ks[0].v.x, y: ks[0].v.y, z: ks[0].v.z, rot: ks[0].v.rot, shake: ks[0].v.shake };
  if (t >= ks[ks.length - 1].t) return { x: last.x, y: last.y, z: last.z, rot: last.rot, shake: last.shake };
  for (var s = 0; s < ks.length - 1; s++) {
    var a = ks[s], b = ks[s + 1];
    if (t >= a.t && t <= b.t) {
      var u = b.t > a.t ? (t - a.t) / (b.t - a.t) : 1;
      var e = a.ease;
      u = e === 'linear' ? u : e === 'in' ? u * u : e === 'out' ? 1 - (1 - u) * (1 - u) : u * u * (3 - 2 * u);
      return {
        x: a.v.x + (b.v.x - a.v.x) * u,
        y: a.v.y + (b.v.y - a.v.y) * u,
        z: a.v.z + (b.v.z - a.v.z) * u,
        rot: a.v.rot + (b.v.rot - a.v.rot) * u,
        shake: a.v.shake + (b.v.shake - a.v.shake) * u
      };
    }
  }
  return { x: last.x, y: last.y, z: last.z, rot: last.rot, shake: last.shake };
}

function camApply(x, cam, W, H) {
  x.save();
  x.translate(W / 2, H / 2);
  x.scale(cam.z, cam.z);
  x.rotate(cam.rot);
  x.translate(-W / 2 + cam.x, -H / 2 + cam.y);
}

function camReset(x) {
  x.restore();
}

function parallax(cam, depth) {
  var d = depth < 0 ? 0 : depth > 1 ? 1 : depth;
  var r = 0.25 + 0.75 * d;
  return { dx: cam.x * r, dy: cam.y * r, dz: 1 + (cam.z - 1) * r };
}

function camShake(t, amp, freq) {
  var f = freq || 1;
  var a = amp || 0;
  return {
    dx: a * (0.6 * Math.sin(t * f * 12.566) + 0.4 * Math.sin(t * f * 23.25 + 1.3)),
    dy: a * (0.6 * Math.sin(t * f * 16.34 + 2.1) + 0.4 * Math.sin(t * f * 27.02 + 0.7)),
    rot: a * 0.012 * (0.7 * Math.sin(t * f * 11.94 + 0.5) + 0.3 * Math.sin(t * f * 19.48 + 1.9))
  };
}

function dollyBlur(x, speed) {
  var s = speed < 0 ? 0 : speed > 1 ? 1 : speed;
  x.save();
  x.filter = 'blur(' + (s * 12).toFixed(2) + 'px)';
}

function dollyBlurEnd(x) {
  x.restore();
}
