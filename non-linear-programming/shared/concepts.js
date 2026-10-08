/* concepts.js — tìm kiếm / mở-thu gọn thẻ khái niệm */
(function(){
  var q = document.getElementById('kn-q'); if (!q) return;
  var cards = [].slice.call(document.querySelectorAll('.concept'));
  function norm(s){ return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/đ/g,'d'); }
  function filt(){
    var t = norm(q.value.trim()), n = 0;
    cards.forEach(function(c){ var ok = !t || norm(c.getAttribute('data-k')).indexOf(t) >= 0 || norm(c.textContent).indexOf(t) >= 0; c.style.display = ok ? '' : 'none'; if (ok) n++; });
    document.getElementById('kn-n').textContent = n + '/' + cards.length + ' thẻ';
    if (t && n === 1) cards.forEach(function(c){ if (c.style.display !== 'none') c.querySelector('details').open = true; });
  }
  q.addEventListener('input', filt);
  function setAll(v){ cards.forEach(function(c){ c.querySelector('details').open = v; }); if (window.nlpRenderMath) window.nlpRenderMath(document.querySelector('.kn-list')); }
  document.getElementById('kn-all').addEventListener('click', function(){ setAll(true); });
  document.getElementById('kn-none').addEventListener('click', function(){ setAll(false); });
  filt();
})();
