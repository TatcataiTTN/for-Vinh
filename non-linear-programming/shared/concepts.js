/* concepts.js — lọc/mở thẻ khái niệm. Trang module: chỉ nút mở/thu gọn; trang Tra cứu: thêm ô tìm toàn khoá. */
(function(){
  var cards = [].slice.call(document.querySelectorAll('.concept')); if (!cards.length) return;
  var q = document.getElementById('kn-q'), cnt = document.getElementById('kn-n');
  function norm(s){ return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/đ/g,'d'); }
  cards.forEach(function(c){ c._t = norm(c.getAttribute('data-k') || ''); c._f = norm(c.textContent); });
  function filt(){
    var t = q ? norm(q.value.trim()) : '', toks = t.split(/\s+/).filter(Boolean), n = 0;
    cards.forEach(function(c){
      var ok = !toks.length || toks.every(function(w){ return c._f.indexOf(w) >= 0; });
      c.style.display = ok ? '' : 'none'; if (ok) n++;
    });
    document.querySelectorAll('.kn-list > h2').forEach(function(h){   // ẩn tiêu đề module nếu hết thẻ
      var el = h.nextElementSibling, any = false;
      while (el && el.tagName !== 'H2'){ if (el.classList && el.classList.contains('concept') && el.style.display !== 'none') any = true; el = el.nextElementSibling; }
      h.style.display = any || !toks.length ? '' : 'none';
      var lk = h.nextElementSibling; if (lk && lk.classList.contains('when')) lk.style.display = h.style.display;
    });
    if (cnt) cnt.textContent = n + '/' + cards.length + ' thẻ';
    if (toks.length && n > 0 && n <= 3) cards.forEach(function(c){ if (c.style.display !== 'none') c.querySelector('details').open = true; });
  }
  if (q) q.addEventListener('input', filt);
  function setAll(v){ cards.forEach(function(c){ if (c.style.display !== 'none') c.querySelector('details').open = v; }); if (window.nlpRenderMath) window.nlpRenderMath(document.querySelector('.kn-list')); }
  var a = document.getElementById('kn-all'), b = document.getElementById('kn-none');
  if (a) a.addEventListener('click', function(){ setAll(true); });
  if (b) b.addEventListener('click', function(){ setAll(false); });
  function hashCard(){ var h = (location.hash || '').slice(1); if (h.indexOf('kn-') !== 0) return; var c = document.getElementById(h); if (c && document.getElementById('kn-q')){ c.querySelector('details').open = true; if (window.nlpRenderMath) window.nlpRenderMath(c); c.classList.add('hl'); c.scrollIntoView({block:'start'}); } }
  filt(); hashCard();
})();
