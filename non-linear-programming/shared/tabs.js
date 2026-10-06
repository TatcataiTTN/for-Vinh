/* tabs.js — chuyển tab trong trang module; nhớ tab theo #hash; bắn resize để deck tự co chữ khi hiện. */
(function(){
  var bar = document.querySelector('.tabs'); if (!bar) return;
  var btns = [].slice.call(bar.querySelectorAll('button')), panes = [].slice.call(document.querySelectorAll('.tabpane'));
  function show(id, noHash){
    var ok = panes.some(function(p){ return p.id === id; }); if (!ok) id = panes[0].id;
    panes.forEach(function(p){ p.classList.toggle('on', p.id === id); });
    btns.forEach(function(b){ b.classList.toggle('on', b.dataset.tab === id); });
    if (!noHash) { try { history.replaceState(null, '', '#' + id); } catch(e){} }
    if (window.nlpRenderMath) window.nlpRenderMath(document.getElementById(id));
    window.dispatchEvent(new Event('resize'));
  }
  btns.forEach(function(b){ b.addEventListener('click', function(){ show(b.dataset.tab); window.scrollTo({top: bar.offsetTop - 50}); }); });
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[data-goto]'); if (!a) return;
    e.preventDefault(); show(a.dataset.goto);
  });
  var h = (location.hash || '').slice(1);
  show(panes.some(function(p){ return p.id === h; }) ? h : panes[0].id, true);
})();
