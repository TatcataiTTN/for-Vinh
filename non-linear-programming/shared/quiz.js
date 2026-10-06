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
  function tkey(q){ return q.t==='num'||q.t==='essay'||q.t==='match'||q.t==='fill' ? q.t : 'mcq'; }
  var flt = {type:'all', src:'all', wrong:false};
  function counts(){
    var done=0, ok=0, byType={mcq:[0,0],num:[0,0],essay:[0,0],match:[0,0],fill:[0,0]};
    Q.items.forEach(function(q, i){
      var t = tkey(q); byType[t][1]++;
      var st=state[i]; if (st){ done++; byType[t][0]++; if (st.ok) ok++; }
    });
    return {done:done, ok:ok, n:Q.items.length, by:byType};
  }
  var scoreEl;
  function updateScore(){
    var c = counts();
    scoreEl.querySelector('.stxt').innerHTML = 'Đã làm <b>'+c.done+'/'+c.n+'</b> · đúng/đạt <b>'+c.ok+'</b>' + (c.done ? ' ('+Math.round(100*c.ok/c.done)+'%)' : '') +
      ' <span style="color:var(--muted);font-size:.85em">— trắc nghiệm '+c.by.mcq[0]+'/'+c.by.mcq[1]+', điền số '+c.by.num[0]+'/'+c.by.num[1]+', nối '+c.by.match[0]+'/'+c.by.match[1]+', điền từ '+c.by.fill[0]+'/'+c.by.fill[1]+', tự luận '+c.by.essay[0]+'/'+c.by.essay[1]+'</span>';
  }
  function visible(q, qi){
    var t = tkey(q);
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
      } else if (q.t === 'match'){
        ex.innerHTML = '<b>Giải thích:</b> ' + q.explain;
        var rights = q.pairs.map(function(p){ return p[1]; });
        var order = rights.map(function(_, i){ return i; });
        // thứ tự hiển thị cố định theo chỉ số câu (xoay vòng), tránh trùng thứ tự vế trái
        var rot = (qi % (order.length - 1 || 1)) + 1; order = order.map(function(_, i){ return order[(i + rot) % order.length]; });
        var LET = 'ABCDEF';
        var leg = document.createElement('div'); leg.className = 'matchleg';
        order.forEach(function(ri){ var d = document.createElement('div'); d.innerHTML = '<b>' + LET[ri] + '.</b> ' + rights[ri]; leg.appendChild(d); });
        box.appendChild(leg);
        var tbl = document.createElement('div'); tbl.className = 'matchtbl';
        var sels = [];
        q.pairs.forEach(function(p, pi){
          var row = document.createElement('div'); row.className = 'matchrow';
          var l = document.createElement('div'); l.className = 'ml'; l.innerHTML = p[0];
          var sel = document.createElement('select'); sel.className = 'msel';
          var o0 = document.createElement('option'); o0.value = ''; o0.textContent = '— chọn —'; sel.appendChild(o0);
          order.forEach(function(ri){ var o = document.createElement('option'); o.value = String(ri); o.textContent = LET[ri]; sel.appendChild(o); });
          var mk = document.createElement('span'); mk.className = 'mk';
          row.appendChild(l); row.appendChild(sel); row.appendChild(mk); tbl.appendChild(row); sels.push({sel: sel, mk: mk, row: row});
        });
        box.appendChild(tbl);
        var bar = document.createElement('div'); bar.className = 'numrow';
        var btn = document.createElement('button'); btn.className = 'chk'; btn.type = 'button'; btn.textContent = 'Chấm';
        var res = document.createElement('span'); res.className = 'badge'; bar.appendChild(btn); bar.appendChild(res); box.appendChild(bar);
        var finishM = function(picks){
          var good = 0;
          sels.forEach(function(o, i){
            o.sel.value = picks[i]; o.sel.disabled = true;
            var ok = String(picks[i]) === String(i); if (ok) good++;
            o.mk.className = 'mk ' + (ok ? 'okm' : 'nom');
            o.mk.innerHTML = ok ? '✔' : ('✘ đúng là: ' + LET[i] + '. ' + rights[i]);
          });
          btn.disabled = true; var all = good === q.pairs.length;
          res.className = 'badge ' + (all ? 'ok' : 'no'); res.textContent = all ? 'Đúng hết' : ('Đúng ' + good + '/' + q.pairs.length);
          ex.classList.add('show'); retry.style.display = 'inline-block';
          if (window.nlpRenderMath) window.nlpRenderMath(box);
          return all;
        };
        if (st) finishM(st.picks);
        btn.addEventListener('click', function(){
          var picks = sels.map(function(o){ return o.sel.value; });
          if (picks.some(function(v){ return v === ''; })){ res.className = 'badge mid'; res.textContent = 'Hãy chọn đủ mọi hàng'; return; }
          var all = picks.every(function(v, i){ return String(v) === String(i); });
          state[qi] = {picks: picks, ok: all}; save(); finishM(picks); updateScore();
        });
      } else if (q.t === 'fill'){
        ex.innerHTML = '<b>Lời giải:</b> ' + q.explain;
        var box2 = document.createElement('div'); box2.className = 'fillbox';
        var parts = q.text.split(/\{(\d+)\}/); var inputs = [];
        parts.forEach(function(seg, i){
          if (i % 2 === 0){ var sp = document.createElement('span'); sp.innerHTML = seg; box2.appendChild(sp); }
          else { var inp = document.createElement('input'); inp.type = 'text'; inp.className = 'fillin'; inp.size = 8; inp.autocomplete = 'off'; inp.setAttribute('aria-label', 'chỗ trống ' + (+seg + 1)); box2.appendChild(inp); inputs[+seg] = inp; }
        });
        box.appendChild(box2);
        if (q.bank){ var bk = document.createElement('div'); bk.className = 'fillbank'; bk.innerHTML = '<i>Từ gợi ý:</i> ' + q.bank.map(function(w){ return '<span class="tag">' + w + '</span>'; }).join(' '); box.appendChild(bk); }
        var bar2 = document.createElement('div'); bar2.className = 'numrow';
        var btn2 = document.createElement('button'); btn2.className = 'chk'; btn2.type = 'button'; btn2.textContent = 'Chấm';
        var res2 = document.createElement('span'); res2.className = 'badge'; bar2.appendChild(btn2); bar2.appendChild(res2); box.appendChild(bar2);
        function norm(x){ return String(x).toLowerCase().replace(/\s+/g, '').replace('−', '-').replace(',', '.'); }
        function okFill(i, v){ return q.answers[i].some(function(a){ return norm(a) === norm(v); }); }
        var finishF = function(vals){
          var good = 0;
          inputs.forEach(function(inp, i){ inp.value = vals[i]; inp.disabled = true; var ok = okFill(i, vals[i]); if (ok) good++; inp.classList.add(ok ? 'okin' : 'noin'); if (!ok){ inp.title = 'Đáp án: ' + q.answers[i][0]; var h = document.createElement('span'); h.className = 'hint'; h.textContent = ' [' + q.answers[i][0] + '] '; inp.parentNode.insertBefore(h, inp.nextSibling); } });
          btn2.disabled = true; var all = good === inputs.length;
          res2.className = 'badge ' + (all ? 'ok' : 'no'); res2.textContent = all ? 'Đúng hết' : ('Đúng ' + good + '/' + inputs.length);
          ex.classList.add('show'); retry.style.display = 'inline-block';
          if (window.nlpRenderMath) window.nlpRenderMath(box);
          return all;
        };
        if (st) finishF(st.vals);
        btn2.addEventListener('click', function(){
          var vals = inputs.map(function(i){ return i.value; });
          if (vals.some(function(v){ return v.trim() === ''; })){ res2.className = 'badge mid'; res2.textContent = 'Hãy điền đủ mọi chỗ trống'; return; }
          var all = vals.every(function(v, i){ return okFill(i, v); });
          state[qi] = {vals: vals, ok: all}; save(); finishF(vals); updateScore();
        });
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
    '<select id="f-type"><option value="all">Mọi dạng</option><option value="mcq">Trắc nghiệm</option><option value="num">Điền số</option><option value="match">Nối cặp</option><option value="fill">Điền từ</option><option value="essay">Tự luận</option></select> ' +
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
