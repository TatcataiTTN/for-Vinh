/* Học tra bảng XSTK: dựng bảng A7/A8/A9/A10, tra thử có tô sáng ô, nội suy, hình chuông, luyện tra bảng. Chạy 100% trong trình duyệt. */
(function () {
'use strict';
var TB = window.TB, QS = window.QUESTIONS || [];
function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h !== undefined) e.innerHTML = h; return e; }
function mn(s) { return String(s).replace(/-/g, '−'); }
function fx(x, d) { return mn(x.toFixed(d)); }
function sb(s) { return String(s).replace(/([UtΦ])_\{([^}]+)\}/g, '$1<sub>$2</sub>').replace(/([Ut])_α/g, '$1<sub>α</sub>'); }

/* ───────────── toán: Φ, t, χ² (độc lập với bảng; để đối chiếu giá trị chính xác) ───────────── */
function lgamma(x) {
  var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  var y = x, t = x + 5.5; t -= (x + 0.5) * Math.log(t); var s = 1.000000000190015;
  for (var j = 0; j < 6; j++) s += c[j] / ++y; return -t + Math.log(2.5066282746310005 * s / x);
}
function gammp(a, x) {
  if (x <= 0) return 0;
  if (x < a + 1) { var ap = a, sum = 1 / a, del = sum; for (var n = 0; n < 500; n++) { ap++; del *= x / ap; sum += del; if (Math.abs(del) < Math.abs(sum) * 1e-15) break; } return sum * Math.exp(-x + a * Math.log(x) - lgamma(a)); }
  var b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
  for (var i = 1; i < 500; i++) { var an = -i * (i - a); b += 2; d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300; c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; var dl = d * c; h *= dl; if (Math.abs(dl - 1) < 1e-15) break; }
  return 1 - Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
}
function betacf(a, b, x) {
  var qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap; if (Math.abs(d) < 1e-300) d = 1e-300; d = 1 / d; var h = d;
  for (var m = 1; m <= 500; m++) { var m2 = 2 * m, aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; var dl = d * c; h *= dl; if (Math.abs(dl - 1) < 1e-15) break; }
  return h;
}
function betai(a, b, x) {
  if (x <= 0) return 0; if (x >= 1) return 1;
  var bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
}
function Phi(x) { var p = gammp(0.5, x * x / 2); return x >= 0 ? 0.5 * (1 + p) : 0.5 * (1 - p); }
function tcdf(t, v) { var p = 0.5 * betai(v / 2, 0.5, v / (v + t * t)); return t > 0 ? 1 - p : p; }
function bis(f, lo, hi) { for (var i = 0; i < 200; i++) { var m = (lo + hi) / 2; if (f(m) < 0) lo = m; else hi = m; } return (lo + hi) / 2; }
function zq(p) { return bis(function (z) { return Phi(z) - p; }, -12, 12); }
function tq(p, v) { return v === Infinity ? zq(p) : bis(function (t) { return tcdf(t, v) - p; }, -1e6, 1e6); }
function chiq(p, v) { return bis(function (x) { return gammp(v / 2, x / 2) - p; }, 0, 5000); }
window.PS = { Phi: Phi, zq: zq, tq: tq, chiq: chiq };

/* ───────────── hình chuông ───────────── */
function bell(host, spec) {
  var W = 360, H = 130, x0 = 20, x1 = W - 20, base = H - 22, top = 14, lo = -4, hi = 4;
  function X(z) { return x0 + (z - lo) / (hi - lo) * (x1 - x0); }
  function Y(z) { return base - Math.exp(-z * z / 2) * (base - top); }
  function path(a, b) { var s = 'M' + X(a).toFixed(1) + ',' + base; for (var z = a; z <= b + 1e-9; z += 0.05) s += 'L' + X(z).toFixed(1) + ',' + Y(z).toFixed(1); return s + 'L' + X(b).toFixed(1) + ',' + base + 'Z'; }
  var shade = '', lab = spec.label || '';
  var clip = function (v) { return Math.max(lo, Math.min(hi, v)); };
  if (spec.mode === 'left') shade = path(lo, clip(spec.z));
  else if (spec.mode === 'right') shade = path(clip(spec.z), hi);
  else if (spec.mode === 'between') shade = path(clip(spec.a), clip(spec.b));
  else if (spec.mode === 'two') shade = path(lo, clip(-spec.z)) + path(clip(spec.z), hi);
  var marks = (spec.marks || []).map(function (m) { return '<line x1="' + X(clip(m)).toFixed(1) + '" y1="' + top + '" x2="' + X(clip(m)).toFixed(1) + '" y2="' + base + '" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="' + X(clip(m)).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="middle" font-size="11" fill="var(--text)">' + mn(m) + '</text>'; }).join('');
  var ticks = [-3, -2, -1, 0, 1, 2, 3].map(function (t) { return '<line x1="' + X(t) + '" y1="' + base + '" x2="' + X(t) + '" y2="' + (base + 4) + '" stroke="var(--muted)"/>'; }).join('');
  host.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Đường chuẩn tắc, vùng tô là xác suất cần tính"><path d="' + shade + '" fill="var(--accent)" fill-opacity=".28" fill-rule="nonzero"/>' +
    '<path d="' + (function () { var s = ''; for (var z = lo; z <= hi + 1e-9; z += 0.05) s += (s ? 'L' : 'M') + X(z).toFixed(1) + ',' + Y(z).toFixed(1); return s; })() + '" fill="none" stroke="var(--accent2)" stroke-width="2"/>' +
    '<line x1="' + x0 + '" y1="' + base + '" x2="' + x1 + '" y2="' + base + '" stroke="var(--muted)"/>' + ticks + marks + (lab ? '<text x="' + (W / 2) + '" y="12" text-anchor="middle" font-size="12" fill="var(--text)">' + lab + '</text>' : '') + '</svg>';
}
function initBells() {
  $$('[data-bell]').forEach(function (h) {
    var p = h.getAttribute('data-bell').split(':'), m = p[0], v = p[1].split(',').map(Number), s = { mode: m, label: h.getAttribute('data-label') || '' };
    if (m === 'between') { s.a = v[0]; s.b = v[1]; s.marks = v; } else { s.z = v[0]; s.marks = [v[0]]; }
    bell(h, s);
  });
}

/* ───────────── dựng bảng ───────────── */
function renderA7(host) {
  var A = TB.A7, h = '<table class="tb a7" id="tbl-a7"><thead><tr>' + new Array(6).join('<th>z</th><th>Φ(z)</th><th class="gap"></th>') + '<th>z</th><th>Φ(z)</th></tr></thead><tbody>';
  for (var r = 0; r < 50; r++) {
    h += '<tr' + (r % 5 === 0 && r ? ' class="blk"' : '') + '>';
    for (var g = 0; g < 6; g++) {
      var z = (g * 50 + r + 1) / 100, k = z.toFixed(2), v = A[k];
      h += '<td class="zc" data-z="' + k + '">' + k + '</td><td data-k="' + k + '">' + v.slice(2) + '</td>' + (g < 5 ? '<td class="gap"></td>' : '');
    }
    h += '</tr>';
  }
  host.innerHTML = '<div class="tbwrap">' + h + '</tbody></table></div><p class="note">Ô in 4 chữ số: hiểu là 0.xxxx (ví dụ 8907 là 0.8907). Φ(0) = 0.5000; z &gt; 3.00 thì Φ(z) ≈ 1.</p>';
}
function a8Rows() {
  return Object.keys(TB.A8).map(Number).sort(function (a, b) { return a - b; });
}
function renderA8(host) {
  var P = a8Rows(), g1 = P.filter(function (p) { return p <= 40; }), g2 = P.filter(function (p) { return p > 40 && p <= 80; }), g3 = P.filter(function (p) { return p > 80; });
  var n = Math.max(g1.length, g2.length, g3.length), h = '<table class="tb a8" id="tbl-a8"><thead><tr>' + new Array(4).join('<th>%</th><th>z(Φ)</th><th>z(D)</th><th class="gap"></th>').slice(0, -'<th class="gap"></th>'.length) + '</tr></thead><tbody>';
  for (var r = 0; r < n; r++) {
    h += '<tr' + (r % 5 === 0 && r ? ' class="blk"' : '') + '>';
    [g1, g2, g3].forEach(function (g, i) {
      var p = g[r];
      if (p === undefined) h += '<td></td><td></td><td></td>' + (i < 2 ? '<td class="gap"></td>' : '');
      else { var v = TB.A8[String(p)]; h += '<td class="zc" data-p="' + p + '">' + p + '</td><td data-p="' + p + '" data-c="0">' + mn(v[0]) + '</td><td data-p="' + p + '" data-c="1">' + v[1] + '</td>' + (i < 2 ? '<td class="gap"></td>' : ''); }
    });
    h += '</tr>';
  }
  host.innerHTML = '<div class="tbwrap">' + h + '</tbody></table></div><p class="note">z(Φ): giá trị z để Φ(z) = P%. z(D): giá trị z để D(z) = Φ(z) − Φ(−z) = P% (xác suất |Z| &lt; z).</p>';
}
function dfLabel(d) { return d === 'inf' ? '∞' : d; }
function renderGrid(host, id, D, head) {
  var h = '<table class="tb grid" id="' + id + '"><thead><tr><th rowspan="2">F(z)</th><th colspan="' + D.df.length + '">Số bậc tự do (m)</th></tr><tr>' + D.df.map(function (d) { return '<th data-df="' + d + '">' + dfLabel(d) + '</th>'; }).join('') + '</tr></thead><tbody>';
  D.F.forEach(function (F, i) {
    h += '<tr' + ((i === 5 && id === 'tbl-a9') || (i === 4 && id === 'tbl-a10') ? ' class="blk"' : '') + '><th class="rh" data-f="' + F + '">' + F + '</th>' + D.v[i].map(function (v, j) { return '<td data-f="' + F + '" data-df="' + D.df[j] + '">' + v + '</td>'; }).join('') + '</tr>';
  });
  host.innerHTML = '<div class="tbwrap">' + h + '</tbody></table></div>' + head;
}
function initTables() {
  $$('[data-table="a7"]').forEach(renderA7); $$('[data-table="a8"]').forEach(renderA8);
  $$('[data-table="a9"]').forEach(function (h) { renderGrid(h, 'tbl-a9', TB.A9, '<p class="note">Cột ∞ ứng với phân phối chuẩn tắc. Ô (∞; 0.95) in 1.65 (1.645 làm tròn lên).</p>'); });
  $$('[data-table="a10"]').forEach(function (h) { renderGrid(h, 'tbl-a10', TB.A10, '<p class="note">Với m &gt; 100 dùng x ≈ ½(h + z)², h = √(2m − 1), z lấy ở bảng A8 (xem trang χ²).</p>'); });
}

/* ───────────── tô sáng ───────────── */
function clearHL() { $$('.hl, .hl-h, .hl-band').forEach(function (e) { e.classList.remove('hl', 'hl-h', 'hl-band'); }); }
function scrollTo(e) {   // chỉ cuộn bên trong khung bảng, không kéo cả trang đi chỗ khác
  var w = e && e.closest ? e.closest('.tbwrap') : null; if (!w) return;
  var er = e.getBoundingClientRect(), wr = w.getBoundingClientRect();
  w.scrollTop += (er.top - wr.top) - w.clientHeight / 2 + er.height / 2; w.scrollLeft += (er.left - wr.left) - w.clientWidth / 2 + er.width / 2;
}
function hlA7(z) {
  var a = Math.abs(z), k = (Math.round(a * 100) / 100).toFixed(2), c = $('#tbl-a7 td[data-k="' + k + '"]'); if (!c) return;
  c.classList.add('hl'); c.previousElementSibling.classList.add('hl-h'); c.parentNode.classList.add('hl-band'); scrollTo(c);
}
function hlA8(P, col) {
  var cells = $$('#tbl-a8 td[data-p="' + P + '"]'); if (!cells.length) return;
  cells.forEach(function (c) { if (c.classList.contains('zc')) c.classList.add('hl-h'); else if (col === undefined || String(col) === c.getAttribute('data-c')) c.classList.add('hl'); });
  cells[0].parentNode.classList.add('hl-band'); scrollTo(cells[1]);
}
function hlGrid(id, F, df) {
  var T = $('#' + id); if (!T) return; var first;
  [].concat(F).forEach(function (f) { [].concat(df).forEach(function (d) {
    var c = $('td[data-f="' + f + '"][data-df="' + d + '"]', T); if (c) { c.classList.add('hl'); first = first || c; }
    var rh = $('th.rh[data-f="' + f + '"]', T), ch = $('th[data-df="' + d + '"]', T); if (rh) rh.classList.add('hl-h'); if (ch) ch.classList.add('hl-h');
  }); });
  if (first) { first.parentNode.classList.add('hl-band'); scrollTo(first); }
}

/* ───────────── nội suy ───────────── */
function bracket(list, x) {   // trả về [lo, hi] kề x trong list tăng dần (nếu x có trong list thì [x, x])
  var lo = null, hi = null;
  for (var i = 0; i < list.length; i++) { if (list[i] === x) return [x, x]; if (list[i] < x) lo = list[i]; if (list[i] > x && hi === null) hi = list[i]; }
  return [lo, hi];
}
function numDf(d) { return d === 'inf' ? Infinity : +d; }
function a9cell(F, d) { var i = TB.A9.F.indexOf(F), j = TB.A9.df.indexOf(d === Infinity ? 'inf' : d); return +TB.A9.v[i][j]; }
function a9interp(df, F) {
  var dfs = TB.A9.df.map(numDf), fb = bracket(TB.A9.F, F), db = bracket(dfs, df);
  if (fb[0] === null || fb[1] === null || db[0] === null || db[1] === null) return null;
  var steps = [], lin = function (x, x0, x1, y0, y1) { return x0 === x1 ? y0 : y0 + (x - x0) / (x1 - x0) * (y1 - y0); };
  var ycol = function (f) {   // nội suy theo df ở hàng f
    var y0 = a9cell(f, db[0]), y1 = a9cell(f, db[1]);
    if (db[0] === db[1]) return y0;
    var x0 = db[0], x1 = db[1] === Infinity ? 1e9 : db[1], v = lin(df, x0, x1, y0, y1);
    steps.push('Hàng F = ' + f + ': giữa cột ' + db[0] + ' (' + y0.toFixed(2) + ') và cột ' + dfLabel(db[1] === Infinity ? 'inf' : db[1]) + ' (' + y1.toFixed(2) + ') → ' + v.toFixed(3));
    return v;
  };
  var v0 = ycol(fb[0]), v1 = fb[0] === fb[1] ? v0 : ycol(fb[1]), v = fb[0] === fb[1] ? v0 : lin(F, fb[0], fb[1], v0, v1);
  if (fb[0] !== fb[1]) steps.push('Nội suy theo F: giữa F = ' + fb[0] + ' (' + v0.toFixed(3) + ') và F = ' + fb[1] + ' (' + v1.toFixed(3) + ') → ' + v.toFixed(3));
  return { v: v, steps: steps, fb: fb, db: db };
}
function a8interp(P) {
  var rows = a8Rows(), b = bracket(rows, P); if (b[0] === null || b[1] === null) return null;
  var y0 = +TB.A8[String(b[0])][0], y1 = +TB.A8[String(b[1])][0];
  return { v: b[0] === b[1] ? y0 : y0 + (P - b[0]) / (b[1] - b[0]) * (y1 - y0), b: b, y0: y0, y1: y1 };
}

/* ───────────── tra thử (widgets) ───────────── */
function num(s) { s = String(s).trim().replace(',', '.').replace('−', '-'); return s === '' || isNaN(+s) ? NaN : +s; }
function widget(host, build) {
  var form = el('div', 'lkform'), out = el('div', 'lkout'); host.appendChild(form); host.appendChild(out); build(form, out);
}
function field(form, label, attrs) { var l = el('label', null, label + ' '); var i = el('input'); for (var k in attrs) i.setAttribute(k, attrs[k]); l.appendChild(i); form.appendChild(l); return i; }
function btn(form, txt, fn) { var b = el('button', 'btn', txt); b.type = 'button'; b.onclick = fn; form.appendChild(b); return b; }
function enter(inputs, fn) { inputs.forEach(function (i) { i.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); fn(); } }); }); }
function ol(items) { return '<ol class="steps">' + items.map(function (i) { return '<li>' + i + '</li>'; }).join('') + '</ol>'; }

function wA7(host) {
  widget(host, function (form, out) {
    var zi = field(form, 'z =', { type: 'text', inputmode: 'decimal', value: '1.23', 'aria-label': 'z' });
    function go() {
      clearHL(); var z = num(zi.value); if (isNaN(z)) { out.innerHTML = '<p class="bad">Nhập một số, ví dụ 1.23 hoặc −0.57.</p>'; return; }
      var a = Math.abs(z), r = Math.round(a * 100) / 100, notes = [], k = r.toFixed(2), exact = Phi(z), res, st = [];
      if (Math.abs(a - r) > 1e-9) notes.push('z có hơn 2 chữ số thập phân nên làm tròn: ' + mn(z) + ' → ' + mn((z < 0 ? -r : r).toFixed(2)) + ' (bảng chỉ có bước 0.01).');
      if (r > 3.0) { res = z > 0 ? 1 : 0; st.push('|z| > 3.00 vượt bảng: Φ(z) ≈ ' + (z > 0 ? '1' : '0') + ' (thực tế ' + exact.toFixed(5) + ').'); }
      else if (r === 0) { res = 0.5; st.push('Φ(0) = 0.5000.'); }
      else {
        var v = +TB.A7[k], pr = int4(v);
        st.push('Chia z = ' + k + ' thành hàng: tìm ô <b>' + k + '</b> ở các cột z của bảng A7 (z tăng dần theo cột, mỗi nhóm 50 giá trị).');
        st.push('Đọc ô Φ(z) bên phải: <b>' + pr + '</b> ⇒ Φ(' + k + ') = <b>' + v.toFixed(4) + '</b>.');
        if (z < 0) { res = 1 - v; st.push('z âm: Φ(−' + k + ') = 1 − Φ(' + k + ') = 1 − ' + v.toFixed(4) + ' = <b>' + res.toFixed(4) + '</b>.'); } else res = v;
        hlA7(r);
      }
      bell(out.bellHost || (out.bellHost = el('div', 'bellbox')), { mode: 'left', z: z, marks: [z], label: 'Vùng tô = Φ(' + mn(z) + ')' });
      out.innerHTML = ''; out.appendChild(out.bellHost);
      var d = el('div', null, (notes.length ? '<p class="note">' + notes.join(' ') + '</p>' : '') + ol(st) + '<p class="ans">Kết quả: Φ(' + mn(z) + ') ≈ <b>' + res.toFixed(4) + '</b> <span class="muted">(máy tính: ' + exact.toFixed(4) + ')</span></p>'); out.appendChild(d);
    }
    btn(form, 'Tra bảng', go); enter([zi], go); go();
  });
}
function int4(v) { return ('0000' + Math.round(v * 10000)).slice(-4); }

function wA8(host) {
  widget(host, function (form, out) {
    var sel = el('select'); sel.innerHTML = '<option value="alpha">U_α: nhập α (%)</option><option value="P">Φ(z) = P%: nhập P (%)</option><option value="D">P(|Z| &lt; z) = D%: nhập D (%)</option>';
    var l = el('label', null, 'Bài toán '); l.appendChild(sel); form.appendChild(l);
    var vi = field(form, 'Giá trị (%) =', { type: 'text', inputmode: 'decimal', value: '7' });
    function go() {
      clearHL(); var m = sel.value, x = num(vi.value); if (isNaN(x) || x <= 0 || x >= 100) { out.innerHTML = '<p class="bad">Nhập số phần trăm trong khoảng (0; 100).</p>'; return; }
      var P = m === 'alpha' ? Math.round((100 - x) * 1e6) / 1e6 : x, col = m === 'D' ? 1 : 0, rows = a8Rows(), st = [], res, exact;
      if (m === 'alpha') st.push('α = ' + x + '% ⇒ Φ(U_α) = 1 − α = ' + P + '%. Phải tìm hàng <b>' + P + '%</b> (đổi α sang P trước khi tra).');
      else if (m === 'P') st.push('Cần Φ(z) = ' + P + '%: vào hàng <b>' + P + '%</b>, cột z(Φ).');
      else st.push('Cần P(|Z| < z) = D(z) = ' + P + '%: vào hàng <b>' + P + '%</b>, cột z(D).');
      if (rows.indexOf(P) >= 0) {
        res = +TB.A8[String(P)][col]; st.push('Đọc ô z(' + (col ? 'D' : 'Φ') + ') ở hàng ' + P + '%: <b>' + mn(res.toFixed(3)) + '</b>.'); hlA8(P, col);
      } else {
        if (col === 0) { var it = a8interp(P); if (!it) { out.innerHTML = '<p class="bad">Ngoài phạm vi bảng (1% đến 99.99%).</p>'; return; } res = it.v; st.push('Hàng ' + P + '% không có trong bảng: nội suy giữa ' + it.b[0] + '% (' + mn(it.y0.toFixed(3)) + ') và ' + it.b[1] + '% (' + mn(it.y1.toFixed(3)) + ') → <b>' + mn(res.toFixed(3)) + '</b>.'); hlA8(it.b[0], 0); hlA8(it.b[1], 0); }
        else { var rb = bracket(rows, P); res = (+TB.A8[String(rb[0])][1]) + (P - rb[0]) / (rb[1] - rb[0]) * ((+TB.A8[String(rb[1])][1]) - (+TB.A8[String(rb[0])][1])); st.push('Hàng ' + P + '% không có: nội suy giữa ' + rb[0] + '% và ' + rb[1] + '% → <b>' + res.toFixed(3) + '</b>.'); hlA8(rb[0], 1); hlA8(rb[1], 1); }
      }
      exact = col === 0 ? zq(P / 100) : zq((1 + P / 100) / 2);
      var z = res; var host2 = out.bellHost || (out.bellHost = el('div', 'bellbox'));
      bell(host2, col === 1 ? { mode: 'between', a: -z, b: z, marks: [-z, z], label: 'Vùng tô = D(z) = ' + P + '%' } : { mode: 'left', z: z, marks: [z], label: 'Vùng tô = Φ(z) = ' + P + '%' });
      out.innerHTML = ''; out.appendChild(host2); out.appendChild(el('div', null, ol(st) + '<p class="ans">Kết quả: z ≈ <b>' + mn(res.toFixed(3)) + '</b> <span class="muted">(máy tính: ' + mn(exact.toFixed(3)) + ')</span></p>'));
    }
    btn(form, 'Tra bảng', go); enter([vi], go); sel.onchange = function () { vi.value = sel.value === 'alpha' ? '7' : sel.value === 'P' ? '30' : '90'; go(); }; go();
  });
}

function wA9(host) {
  widget(host, function (form, out) {
    var sel = el('select'); sel.innerHTML = '<option value="F">F(z) (đọc thẳng)</option><option value="alpha">t_α một phía: nhập α (%)</option><option value="gamma">Khoảng tin cậy: nhập γ (%)</option>';
    var l = el('label', null, 'Bài toán '); l.appendChild(sel); form.appendChild(l);
    var di = field(form, 'Bậc tự do m =', { type: 'text', inputmode: 'numeric', value: '9' }), vi = field(form, 'Giá trị =', { type: 'text', inputmode: 'decimal', value: '0.95' });
    function go() {
      clearHL(); var m = sel.value, df = /^(inf|∞|vô)/i.test(di.value.trim()) ? Infinity : num(di.value), x = num(vi.value);
      if (isNaN(df) || df < 1 || isNaN(x)) { out.innerHTML = '<p class="bad">Nhập bậc tự do (số nguyên ≥ 1, hoặc “inf”) và giá trị.</p>'; return; }
      var F, st = [];
      if (m === 'F') F = x; else if (m === 'alpha') { F = Math.round((1 - x / 100) * 1e6) / 1e6; st.push('t_α với α = ' + x + '% (một phía): F(t_α) = 1 − α = <b>' + F + '</b>.'); }
      else { F = Math.round((1 + x / 100) / 2 * 1e6) / 1e6; st.push('Độ tin cậy γ = ' + x + '% ⇒ α = ' + (100 - x) + '%, α/2 = ' + ((100 - x) / 2) + '% ⇒ F(t_{α/2}) = 1 − α/2 = <b>' + F + '</b> (hai phía).'); }
      if (F <= 0 || F >= 1) { out.innerHTML = '<p class="bad">F phải nằm trong (0; 1).</p>'; return; }
      var inF = TB.A9.F.indexOf(F) >= 0, inDf = TB.A9.df.map(numDf).indexOf(df) >= 0, res, exact = tq(F, df);
      if (inF && inDf) { res = a9cell(F, df); st.push('Vào cột <b>' + dfLabel(df === Infinity ? 'inf' : df) + '</b> bậc tự do và hàng <b>F = ' + F + '</b>: đọc <b>' + res.toFixed(2) + '</b>.'); hlGrid('tbl-a9', F, df === Infinity ? 'inf' : df); }
      else {
        var it = a9interp(df, F);
        if (!it) { out.innerHTML = '<p class="bad">Ngoài phạm vi bảng A9 (F từ 0.5 đến 0.999, m từ 1).</p>'; return; }
        res = it.v; st.push('Bảng A9 ' + (!inDf && !inF ? 'không có cả cột m = ' + df + ' lẫn hàng F = ' + F : !inDf ? 'không có cột m = ' + df : 'không có hàng F = ' + F) + ': dùng hai cột/hàng kề hai bên rồi <b>nội suy tuyến tính</b>.');
        st = st.concat(it.steps); st.push('Kết quả nội suy: <b>' + res.toFixed(3) + '</b>.');
        hlGrid('tbl-a9', [it.fb[0], it.fb[1]], [it.db[0] === Infinity ? 'inf' : it.db[0], it.db[1] === Infinity ? 'inf' : it.db[1]]);
      }
      var err = Math.abs(res - exact);
      out.innerHTML = ol(st) + '<p class="ans">Kết quả: t ≈ <b>' + res.toFixed(inF && inDf ? 2 : 3) + '</b> <span class="muted">(máy tính: ' + exact.toFixed(3) + '; lệch ' + err.toFixed(3) + ')</span></p>' + (!(inF && inDf) && err > 0.01 ? '<p class="note">Bảng A9 chỉ có ít hàng và cột nên nội suy có sai lệch cỡ ' + err.toFixed(2) + '. Nếu đề cho dùng máy tính thì dùng giá trị chính xác.</p>' : '');
    }
    btn(form, 'Tra bảng', go); enter([di, vi], go);
    sel.onchange = function () { vi.value = sel.value === 'F' ? '0.95' : sel.value === 'alpha' ? '7' : '90'; di.value = sel.value === 'F' ? '9' : sel.value === 'alpha' ? '18' : '31'; go(); }; go();
  });
}

function wA10(host) {
  widget(host, function (form, out) {
    var di = field(form, 'Bậc tự do m =', { type: 'text', inputmode: 'numeric', value: '9' }), fi = field(form, 'F(z) =', { type: 'text', inputmode: 'decimal', value: '0.95' });
    function go() {
      clearHL(); var m = num(di.value), F = num(fi.value); if (isNaN(m) || m < 1 || isNaN(F) || F <= 0 || F >= 1) { out.innerHTML = '<p class="bad">Nhập m ≥ 1 và F trong (0; 1).</p>'; return; }
      var inF = TB.A10.F.indexOf(F) >= 0, inDf = TB.A10.df.indexOf(m) >= 0, exact = chiq(F, m), st = [];
      if (inF && inDf) { var v = +TB.A10.v[TB.A10.F.indexOf(F)][TB.A10.df.indexOf(m)]; st.push('Cột <b>' + m + '</b> bậc tự do, hàng <b>F = ' + F + '</b>: đọc <b>' + v + '</b>.'); hlGrid('tbl-a10', F, m); out.innerHTML = ol(st) + '<p class="ans">Kết quả: x ≈ <b>' + v + '</b> <span class="muted">(máy tính: ' + exact.toFixed(3) + ')</span></p>'; }
      else if (m > 100 && inF) { var z = zq(F), h = Math.sqrt(2 * m - 1), ap = 0.5 * (h + z) * (h + z); st.push('m > 100: x ≈ ½(h + z)² với h = √(2m − 1) = ' + h.toFixed(3) + ' và z = ' + mn(z.toFixed(3)) + ' (bảng A8, Φ(z) = F).'); out.innerHTML = ol(st) + '<p class="ans">Kết quả: x ≈ <b>' + ap.toFixed(1) + '</b> <span class="muted">(máy tính: ' + exact.toFixed(1) + ')</span></p>'; }
      else { out.innerHTML = '<p class="note">Bảng A10 chỉ có F ∈ {0.005, 0.01, 0.025, 0.05, 0.95, 0.975, 0.99, 0.995} và m = 1…30, 40, 50, …, 100. Với giá trị khác phải nội suy; giá trị chính xác (máy tính) là <b>' + exact.toFixed(3) + '</b>.</p>'; }
    }
    btn(form, 'Tra bảng', go); enter([di, fi], go); go();
  });
}

/* ───────────── luyện tra bảng ───────────── */
function practice(host) {
  var KEY = 'bangtra-practice-v1', st = { done: {}, tab: 'all' };
  try { st = Object.assign(st, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  var types = [['all', 'Tất cả'], ['a7', 'A7 Φ(z)'], ['a8', 'A8 z, U_α'], ['a9', 'A9 Student'], ['a10', 'A10 χ²']];
  var bar = el('div', 'row'), box = el('div', 'qbox'), prog = el('div', 'quiz-score');
  host.appendChild(bar); host.appendChild(prog); host.appendChild(box);
  var cur = null;
  function pool() { return QS.filter(function (q) { return st.tab === 'all' || q.t === st.tab; }); }
  function stat() { var p = pool(), ok = p.filter(function (q) { return st.done[q.id] === 1; }).length, bad = p.filter(function (q) { return st.done[q.id] === 0; }).length; prog.textContent = 'Nhóm này: ' + p.length + ' câu · đúng ' + ok + ' · sai ' + bad + ' · chưa làm ' + (p.length - ok - bad); }
  function tabs() { bar.innerHTML = ''; types.forEach(function (t) { var b = el('button', 'btn' + (st.tab === t[0] ? '' : ' alt'), t[1]); b.type = 'button'; b.onclick = function () { st.tab = t[0]; save(); tabs(); next(); }; bar.appendChild(b); });
    var r = el('button', 'btn alt', '↺ Làm lại nhóm này'); r.type = 'button'; r.onclick = function () { pool().forEach(function (q) { delete st.done[q.id]; }); save(); next(); }; bar.appendChild(r); }
  function next() {
    clearHL(); var p = pool(), todo = p.filter(function (q) { return st.done[q.id] === undefined; }); stat(); box.innerHTML = '';
    if (!todo.length) { box.innerHTML = '<div class="callout good"><b class="t">Xong nhóm này</b>Bấm “↺ Làm lại nhóm này” để làm lại từ đầu.</div>'; return; }
    cur = todo[Math.floor(Math.random() * todo.length)];
    var q = el('div', 'qitem'); q.appendChild(el('div', 'qtxt', '<b>Câu ' + cur.id + '.</b> ' + sb(cur.q)));
    var inp = el('input', 'rx-in'); inp.type = 'text'; inp.inputMode = 'decimal'; inp.placeholder = 'Đáp số'; inp.autocomplete = 'off'; inp.setAttribute('aria-label', 'Đáp số của bạn');
    var chk = el('button', 'btn', 'Kiểm tra'); chk.type = 'button'; var hint = el('button', 'btn alt', 'Gợi ý'); hint.type = 'button';
    var row = el('div', 'row'); row.appendChild(inp); row.appendChild(chk); row.appendChild(hint); q.appendChild(row);
    var fb = el('div', 'fb'); q.appendChild(fb); box.appendChild(q); inp.focus();
    hint.onclick = function () { fb.innerHTML = '<div class="note">💡 ' + sb(cur.hint) + '</div>'; };
    function check() {
      var v = num(inp.value); if (isNaN(v)) { fb.innerHTML = '<div class="bad">Nhập một số.</div>'; return; }
      var ok = Math.abs(v - cur.a) <= cur.tol + 1e-9; st.done[cur.id] = ok ? 1 : 0; save(); stat(); inp.disabled = true; chk.disabled = true;
      fb.innerHTML = '<div class="' + (ok ? 'good' : 'bad') + '"><b>' + (ok ? '✅ Đúng' : '❌ Sai') + '</b> — đáp số ' + mn(cur.a) + '</div><p>' + sb(mn(cur.ex)) + '</p>';
      var nx = el('button', 'btn', 'Câu tiếp ▶'); nx.type = 'button'; nx.onclick = next; var sv = el('button', 'btn alt', 'Xem ô trên bảng ↓'); sv.type = 'button'; sv.style.marginLeft = '8px'; sv.onclick = function () { var d0 = $('#tbl-' + cur.loc[0][0]); if (d0) d0.scrollIntoView({ behavior: 'smooth', block: 'center' }); }; fb.appendChild(nx); fb.appendChild(sv); setTimeout(function () { nx.focus(); }, 0);
      cur.loc.forEach(function (L) { var id = L[0] === 'a7' ? hlA7(+L[1]) : L[0] === 'a8' ? hlA8(+L[1]) : (function () { var T = L[0] === 'a9' ? TB.A9 : TB.A10, id2 = L[0] === 'a9' ? 'tbl-a9' : 'tbl-a10', fb2 = bracket(T.F, L[1]), db = bracket(T.df.map(numDf), L[2] === null ? Infinity : L[2]); hlGrid(id2, [fb2[0], fb2[1]], [db[0] === Infinity ? 'inf' : db[0], db[1] === Infinity ? 'inf' : db[1]]); })(); });
      var d = $('#tbl-' + cur.loc[0][0]); if (d) { var det = d.closest('details'); if (det) det.open = true; }
    }
    chk.onclick = check; enter([inp], function () { if (!chk.disabled) check(); });
  }
  tabs(); next();
}

/* ───────────── giao diện ───────────── */
function theme() {
  var b = $('#themebtn'); if (!b) return;
  function set(t) { document.documentElement.setAttribute('data-theme', t); try { localStorage.setItem('bangtra-theme', t); } catch (e) {} b.textContent = t === 'dark' ? '☀ Sáng' : '🌙 Tối'; }
  var t = 'light'; try { t = localStorage.getItem('bangtra-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); } catch (e) {}
  set(t); b.onclick = function () { set(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); };
}
function boot() {
  theme(); initTables(); initBells();
  $$('[data-lk="a7"]').forEach(wA7); $$('[data-lk="a8"]').forEach(wA8); $$('[data-lk="a9"]').forEach(wA9); $$('[data-lk="a10"]').forEach(wA10);
  $$('[data-practice]').forEach(practice);
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
