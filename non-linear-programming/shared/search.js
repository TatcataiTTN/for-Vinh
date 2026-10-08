/* search.js — thanh tra cứu khái niệm toàn site (7.10): so khớp xuyên VI+EN, bỏ dấu, 5 bậc điểm, fuzzy dự phòng. */
(function(){
  'use strict';
  if (typeof NLP_G === 'undefined') return;
  var inp = document.getElementById('site-q'), box = document.getElementById('site-res'); if (!inp || !box) return;
  var script = document.querySelector('script[data-up]'), UP = script ? script.getAttribute('data-up') : '';
  function norm(s){ return String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/đ/g,'d').replace(/\s+/g,' ').trim(); }
  var DB = NLP_G.map(function(g){
    return { g: g,
      term: norm(g.term + ' ' + g.en),
      full: norm([g.term, g.en, g.nomna, g.short, g.dn.join(' '), g.hay].join(' ')) };
  });
  function lev(a, b){ // khoảng cách sửa chữ, cho gõ sai nhẹ
    var m = a.length, n = b.length; if (Math.abs(m-n) > 2) return 9; var d = [], i, j;
    for (i=0;i<=m;i++){ d[i]=[i]; } for (j=1;j<=n;j++) d[0][j]=j;
    for (i=1;i<=m;i++) for (j=1;j<=n;j++) d[i][j] = Math.min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+(a[i-1]===b[j-1]?0:1));
    return d[m][n];
  }
  function search(q, limit){
    q = norm(q); if (!q) return [];
    var tokens = q.split(' ').filter(Boolean), out = [];
    DB.forEach(function(r){
      var s = -1;
      if (r.term.indexOf(q) === 0) s = 0;
      else if (r.term.indexOf(q) > 0) s = 1;
      else if (r.full.indexOf(q) >= 0) s = 2;
      else if (tokens.length > 1 && tokens.every(function(t){ return r.full.indexOf(t) >= 0; })) s = 3;
      else if (tokens.some(function(t){ return t.length >= 3 && r.full.indexOf(t) >= 0; })) s = 4;
      else if (tokens.some(function(t){ return t.length >= 4 && r.term.split(' ').some(function(w){ return lev(t, w) <= 1; }); })) s = 5;   // gõ sai một ký tự
      if (s >= 0) out.push({r: r, s: s});
    });
    out.sort(function(a,b){ return a.s - b.s; });
    return out.slice(0, limit || 8);
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function render(){
    var res = search(inp.value);
    if (!inp.value.trim()){ box.style.display = 'none'; return; }
    box.style.display = 'block';
    if (!res.length){ box.innerHTML = '<div class="sr-none">Không thấy. Thử từ khác (tiếng Việt hoặc tiếng Anh, có dấu hay không đều được).</div>'; return; }
    box.innerHTML = res.map(function(x){
      var g = x.r.g, m = NLP_MODS[g.mod] || {};
      return '<a class="sr" href="' + UP + 'modules/' + m.slug + '/index.html#kn-' + g.id + '"><b>' + esc(g.term) + '</b> <span class="sr-k">' + esc(g.kind) + ' · Module ' + m.num + '</span><span class="sr-n">🗣️ ' + esc(g.nomna.slice(0, 150)) + (g.nomna.length > 150 ? '…' : '') + '</span></a>';
    }).join('');
  }
  inp.addEventListener('input', render);
  inp.addEventListener('focus', render);
  document.addEventListener('click', function(e){ if (!e.target.closest || !e.target.closest('.sitesearch')) box.style.display = 'none'; });
  inp.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){ box.style.display = 'none'; inp.blur(); }
    if (e.key === 'Enter'){ var a = box.querySelector('a.sr'); if (a) location.href = a.href; }
  });
  document.addEventListener('keydown', function(e){ if (e.key === '/' && document.activeElement !== inp && !/INPUT|TEXTAREA|SELECT/.test((document.activeElement||{}).tagName||'')){ e.preventDefault(); inp.focus(); } });
  window.nlpSearch = search;   // phục vụ kiểm thử
})();
