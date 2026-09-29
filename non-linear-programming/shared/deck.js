/* deck.js — mini slide deck, tự co giãn cỡ chữ, theme, KaTeX. Dùng chung mọi module. */
(function(){
  'use strict';
  // ---- theme ----
  function applyTheme(t){ if(t==='dark') document.documentElement.setAttribute('data-theme','dark'); else document.documentElement.removeAttribute('data-theme'); }
  var tbtn = document.getElementById('theme-btn');
  if (tbtn) tbtn.addEventListener('click', function(){
    var dark = document.documentElement.getAttribute('data-theme')==='dark';
    var nt = dark ? 'light' : 'dark'; applyTheme(nt);
    try{ localStorage.setItem('nlp-theme', nt);}catch(e){}
  });
  // ---- KaTeX ----
  function renderMath(root){
    if (typeof renderMathInElement !== 'function') return;
    try{
      renderMathInElement(root||document.body, {
        delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],
        throwOnError:false, strict:false
      });
    }catch(e){ console.error('katex', e); }
  }
  window.nlpRenderMath = renderMath;

  // ---- decks ----
  var decks = document.querySelectorAll('.mdeck');
  var pageKey = 'nlp-deck-' + location.pathname;
  decks.forEach(function(deck, di){
    var slides = Array.prototype.slice.call(deck.querySelectorAll('.mdeck-slide'));
    var bar = deck.querySelector('.mdeck-bar');
    var prevBtn = bar.querySelector('.mdeck-prev'), nextBtn = bar.querySelector('.mdeck-next');
    var count = bar.querySelector('.mdeck-count'), dotsWrap = bar.querySelector('.mdeck-dots');
    var fsBtn = bar.querySelector('.mdeck-fs');
    var i = 0;
    try{ var saved = parseInt(localStorage.getItem(pageKey+di),10); if(!isNaN(saved) && saved>=0 && saved<slides.length) i = saved; }catch(e){}
    slides.forEach(function(s, idx){
      var d = document.createElement('button'); d.type='button';
      d.title = (s.getAttribute('data-title')||('Slide '+(idx+1)));
      if (s.classList.contains('part-divider')) d.classList.add('dv');
      d.addEventListener('click', function(){ go(idx); });
      dotsWrap.appendChild(d);
    });
    var dots = Array.prototype.slice.call(dotsWrap.children);
    function isFs(){ return document.fullscreenElement === deck || document.webkitFullscreenElement === deck; }
    function frameHeight(){ return Math.max(420, Math.min(780, Math.round(window.innerHeight*0.68))); }
    function fit(){
      var fs = isFs();
      slides.forEach(function(s){ s.style.fontSize=''; s.style.height=''; });
      var s = slides[i];
      if (!fs) s.style.height = frameHeight()+'px';
      var lo = fs ? 13 : 12, hi = fs ? 34 : 22;
      if (s.classList.contains('part-divider')) { lo = fs?18:16; hi = fs?36:24; }
      var guard = 0;
      while (hi - lo > 0.5 && guard++ < 12){
        var mid = (lo+hi)/2; s.style.fontSize = mid+'px';
        if (s.scrollHeight <= s.clientHeight + 1) lo = mid; else hi = mid;
      }
      s.style.fontSize = lo+'px';
    }
    function fitSoon(){ requestAnimationFrame(function(){ requestAnimationFrame(fit); }); }
    function render(){
      slides.forEach(function(s, idx){ s.classList.toggle('active', idx===i); });
      dots.forEach(function(d, idx){ d.classList.toggle('on', idx===i); });
      count.textContent = (i+1)+' / '+slides.length;
      prevBtn.disabled = (i===0); nextBtn.disabled = (i===slides.length-1);
      try{ localStorage.setItem(pageKey+di, String(i)); }catch(e){}
      fitSoon();
    }
    function go(n){ i = Math.max(0, Math.min(slides.length-1, n)); render(); }
    prevBtn.addEventListener('click', function(){ go(i-1); });
    nextBtn.addEventListener('click', function(){ go(i+1); });
    deck.tabIndex = 0;
    deck.addEventListener('keydown', function(e){
      if (e.key==='ArrowRight' || e.key==='PageDown') { go(i+1); e.preventDefault(); }
      if (e.key==='ArrowLeft' || e.key==='PageUp') { go(i-1); e.preventDefault(); }
      if (e.key==='Home') go(0);
      if (e.key==='End') go(slides.length-1);
    });
    if (fsBtn) fsBtn.addEventListener('click', function(){
      if (!isFs()) { (deck.requestFullscreen||deck.webkitRequestFullscreen||function(){}).call(deck); }
      else { (document.exitFullscreen||document.webkitExitFullscreen||function(){}).call(document); }
    });
    deck.addEventListener('toggle', fitSoon, true);
    document.addEventListener('fullscreenchange', fitSoon);
    document.addEventListener('webkitfullscreenchange', fitSoon);
    window.addEventListener('resize', fitSoon);
    // ảnh nạp xong có thể đổi chiều cao
    deck.addEventListener('load', fitSoon, true);
    deck._go = go;
    deck._render = render;
    // hash #s=N để nhảy tới slide
    var m = /[#&]s=(\d+)/.exec(location.hash||'');
    if (m && di===0) i = Math.max(0, Math.min(slides.length-1, parseInt(m[1],10)-1));
    render();
  });

  function boot(){
    renderMath(document.body);
    decks.forEach(function(d){ if (d._render) d._render(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ decks.forEach(function(d){ d._render&&d._render(); }); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
