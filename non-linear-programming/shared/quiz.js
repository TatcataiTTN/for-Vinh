/* quiz.js — ngân hàng câu hỏi: trắc nghiệm (có giải thích ngay), điền số, tự luận (đáp án mẫu + tự chấm).
   Lưu tiến độ localStorage theo module; có lọc theo dạng/nguồn, ôn câu sai, làm lại từng câu và làm lại toàn bộ. */
(function(){
  'use strict';
  var dataEl = document.getElementById('quiz-data');
  if (!dataEl) return;
  var Q = JSON.parse(dataEl.textContent);
  var root = document.getElementById('quiz-root');
  var KEY = 'nlp-quiz-v2-' + (Q.key || location.pathname);
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch(e){ state = {}; }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){} }
  var SRC = {G:'Từ nội dung slide', B:'Bài tập/ví dụ của slide', T:'Tham khảo (Studocu/BTDOC)', S:'Biên soạn thêm'};
  var SRCCLASS = {G:'ok', B:'ok', T:'mid', S:'no'};

  function parseNum(s){
    s = String(s).trim().replace(/\s+/g,'').replace(',', '.').replace('−','-');
    if (s === '') return NaN;
    var m = /^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/.exec(s);
    if (m) return parseFloat(m[1]) / parseFloat(m[2]);
    return /^-?\d*\.?\d+(?:e-?\d+)?$/i.test(s) ? parseFloat(s) : NaN;
  }
  var flt = {type:'all', src:'all', wrong:false};
  function counts(){
    var done=0, ok=0, byType={mcq:[0,0],num:[0,0],essay:[0,0]};
    Q.items.forEach(function(q, i){
      var t = q.t==='num'?'num':(q.t==='essay'?'essay':'mcq'); byType[t][1]++;
      var st=state[i]; if (st){ done++; byType[t][0]++; if (st.ok) ok++; }
    });
    return {done:done, ok:ok, n:Q.items.length, by:byType};
  }
  var scoreEl;
  function updateScore(){
    var c = counts();
    scoreEl.querySelector('.stxt').innerHTML = 'Đã làm <b>'+c.done+'/'+c.n+'</b> · đúng/đạt <b>'+c.ok+'</b>' + (c.done ? ' ('+Math.round(100*c.ok/c.done)+'%)' : '') +
      ' <span style="color:var(--muted);font-size:.85em">— trắc nghiệm '+c.by.mcq[0]+'/'+c.by.mcq[1]+', điền số '+c.by.num[0]+'/'+c.by.num[1]+', tự luận '+c.by.essay[0]+'/'+c.by.essay[1]+'</span>';
  }
  function visible(q, qi){
    var t = q.t==='num'?'num':(q.t==='essay'?'essay':'mcq');
    if (flt.type!=='all' && flt.type!==t) return false;
    if (flt.src==='goc' && !(q.src==='G'||q.src==='B')) return false;
    if (flt.src==='other' && (q.src==='G'||q.src==='B')) return false;
    if (flt.wrong){ var st=state[qi]; if (!(st && !st.ok)) return false; }
    return true;
  }
  function head(q, qi){
    var t = document.createElement('div'); t.className='qtxt';
    t.innerHTML = '<span class="qno">'+(qi+1)+'.</span> ' + q.q;
    var b = document.createElement('div'); b.className='qmeta';
    b.innerHTML = '<span class="badge '+(SRCCLASS[q.src]||'mid')+'">'+(SRC[q.src]||'')+(q.ref?' · '+q.ref:'')+'</span>' + (q.grp?' <span class="tag">'+q.grp+'</span>':'');
    return [b,t];
  }
  function build(){
    root.innerHTML = '';
    var shown = 0;
    Q.items.forEach(function(q, qi){
      if (!visible(q, qi)) return;
      shown++;
      var st = state[qi];
      var box = document.createElement('div'); box.className='qitem'; box.id='q'+(qi+1);
      head(q, qi).forEach(function(n){ box.appendChild(n); });
      var ex = document.createElement('div'); ex.className='explain';
      var retry = document.createElement('button'); retry.type='button'; retry.className='retry'; retry.textContent='↺ Làm lại câu này'; retry.style.display='none';
      retry.addEventListener('click', function(){ delete state[qi]; save(); build(); updateScore(); var el=document.getElementById('q'+(qi+1)); if(el) el.scrollIntoView({block:'center'}); });
      if (q.t === 'num'){
        ex.innerHTML = '<b>Lời giải:</b> ' + q.explain;
        var row = document.createElement('div'); row.className='numrow';
        var inp = document.createElement('input'); inp.className='numin'; inp.type='text'; inp.inputMode='decimal'; inp.placeholder='Nhập số (vd 3.5 hoặc 7/2)';
        var btn = document.createElement('button'); btn.className='chk'; btn.type='button'; btn.textContent='Chấm';
        var res = document.createElement('span'); res.className='badge';
        row.appendChild(inp); row.appendChild(btn); row.appendChild(res); box.appendChild(row);
        var finish = function(val, ok){
          inp.value = val; inp.disabled = true; btn.disabled = true;
          res.className = 'badge ' + (ok?'ok':'no');
          res.innerHTML = ok ? 'Đúng' : ('Sai — đáp án: ' + q.ans_text);
          ex.classList.add('show'); retry.style.display='inline-block';
        };
        if (st) finish(st.val, st.ok);
        btn.addEventListener('click', function(){
          var v = parseNum(inp.value);
          if (isNaN(v)) { res.className='badge mid'; res.textContent='Hãy nhập một số'; return; }
          var ok = Math.abs(v - q.ans) <= (q.tol || 1e-6) * Math.max(1, Math.abs(q.ans));
          state[qi] = {val: inp.value, ok: ok}; save(); finish(inp.value, ok); updateScore();
          if (window.nlpRenderMath) window.nlpRenderMath(box);
        });
        inp.addEventListener('keydown', function(e){ if(e.key==='Enter') btn.click(); });
      } else if (q.t === 'essay'){
        ex.innerHTML = '<b>Đáp án mẫu:</b><div class="essay-model">' + q.explain + '</div>' + (q.check ? '<p><b>Tự kiểm tra:</b></p><ul>' + q.check.map(function(c){return '<li>'+c+'</li>';}).join('') + '</ul>' : '');
        var ta = document.createElement('textarea'); ta.className='essay-ta'; ta.rows=5; ta.placeholder='Viết lời giải của bạn ở đây (chỉ lưu trong trình duyệt này), rồi bấm “Xem đáp án mẫu”.';
        ta.value = (st && st.text) || '';
        box.appendChild(ta);
        var bar = document.createElement('div'); bar.className='numrow';
        var show = document.createElement('button'); show.type='button'; show.className='chk'; show.textContent='Xem đáp án mẫu';
        var good = document.createElement('button'); good.type='button'; good.className='sgood'; good.textContent='✔ Tôi làm đúng';
        var bad = document.createElement('button'); bad.type='button'; bad.className='sbad'; bad.textContent='✘ Chưa đúng';
        good.style.display = bad.style.display = 'none';
        bar.appendChild(show); bar.appendChild(good); bar.appendChild(bad); box.appendChild(bar);
        var mark = document.createElement('span'); mark.className='badge'; bar.appendChild(mark);
        function showMark(){ if (st && st.done){ mark.className='badge '+(st.ok?'ok':'no'); mark.textContent = st.ok?'Đã tự chấm: đạt':'Đã tự chấm: cần làm lại'; retry.style.display='inline-block'; } }
        show.addEventListener('click', function(){ ex.classList.add('show'); good.style.display=bad.style.display='inline-block'; if (window.nlpRenderMath) window.nlpRenderMath(ex); });
        function grade(ok){ state[qi] = {ok:ok, done:true, text:ta.value}; save(); st = state[qi]; showMark(); updateScore(); }
        good.addEventListener('click', function(){ grade(true); });
        bad.addEventListener('click', function(){ grade(false); });
        ta.addEventListener('input', function(){ var cur=state[qi]||{}; cur.text=ta.value; if(cur.done===undefined){ cur.done=false; } state[qi]=cur; save(); });
        if (st && st.done){ ex.classList.add('show'); good.style.display=bad.style.display='inline-block'; showMark(); }
      } else {
        ex.innerHTML = '<b>Giải thích:</b> ' + q.explain;
        q.opts.forEach(function(opt, oi){
          var b = document.createElement('button'); b.className='opt'; b.type='button'; b.innerHTML = opt;
          b.addEventListener('click', function(){
            if (b.dataset.done) return;
            state[qi] = {pick: oi, ok: oi===q.correct}; save(); reveal(box, q, state[qi], retry); updateScore();
          });
          box.appendChild(b);
        });
        if (st) reveal(box, q, st, retry);
      }
      box.appendChild(ex); box.appendChild(retry);
      root.appendChild(box);
    });
    if (!shown){ root.innerHTML = '<p class="out">Không có câu nào khớp bộ lọc hiện tại.</p>'; }
    if (window.nlpRenderMath) window.nlpRenderMath(root);
    if (scoreEl) updateScore();
    var info = document.getElementById('quiz-shown'); if (info) info.textContent = 'Đang hiển thị '+shown+' / '+Q.items.length+' câu';
  }
  function reveal(box, q, st, retry){
    var opts = box.querySelectorAll('.opt');
    opts.forEach(function(o){ o.dataset.done='1'; });
    if (opts[q.correct]) opts[q.correct].classList.add('correct');
    if (!st.ok && opts[st.pick]) opts[st.pick].classList.add('wrong');
    var ex = box.querySelector('.explain'); if (ex) ex.classList.add('show');
    if (retry) retry.style.display='inline-block';
  }
  // ---- thanh lọc ----
  var fbar = document.createElement('div'); fbar.className='qfilter';
  fbar.innerHTML = '<span><b>Lọc:</b> ' +
    '<select id="f-type"><option value="all">Mọi dạng</option><option value="mcq">Trắc nghiệm</option><option value="num">Điền số</option><option value="essay">Tự luận</option></select> ' +
    '<select id="f-src"><option value="all">Mọi nguồn</option><option value="goc">Chỉ câu từ slide</option><option value="other">Tham khảo + biên soạn</option></select> ' +
    '<label><input type="checkbox" id="f-wrong"> chỉ câu làm sai</label></span> <span id="quiz-shown" style="color:var(--muted);font-size:.88em"></span>';
  root.parentNode.insertBefore(fbar, root);
  ['f-type','f-src','f-wrong'].forEach(function(id){
    var e = fbar.querySelector('#'+id);
    e.addEventListener('change', function(){ flt.type=fbar.querySelector('#f-type').value; flt.src=fbar.querySelector('#f-src').value; flt.wrong=fbar.querySelector('#f-wrong').checked; build(); });
  });
  scoreEl = document.createElement('div'); scoreEl.className='score';
  scoreEl.innerHTML = '<span class="stxt"></span><span><button type="button" class="br">↺ Làm lại toàn bộ bài</button></span>';
  root.parentNode.appendChild(scoreEl);
  scoreEl.querySelector('.br').addEventListener('click', function(){
    if (counts().done && !window.confirm('Xóa toàn bộ kết quả đã làm của bộ câu hỏi này và bắt đầu lại?')) return;
    state = {}; save(); flt={type:'all',src:'all',wrong:false};
    fbar.querySelector('#f-type').value='all'; fbar.querySelector('#f-src').value='all'; fbar.querySelector('#f-wrong').checked=false;
    build();
  });
  function start(){ build(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
