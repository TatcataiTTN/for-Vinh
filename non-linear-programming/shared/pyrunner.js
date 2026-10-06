/* pyrunner.js — giao diện bài tập lập trình: soạn code, chạy test trong trình duyệt (Pyodide), chấm tự động.
   Dữ liệu bài nằm trong <script type="application/json" id="code-data"> (sinh từ exercises.json). */
(function(){
  'use strict';
  var dataEl = document.getElementById('code-data'); if (!dataEl) return;
  var EX = JSON.parse(dataEl.textContent);
  var root = document.getElementById('code-root');
  var worker = null, seq = 0, pending = {}, LOAD_TIMEOUT = 120000, RUN_TIMEOUT = 10000;
  function esc(s){ return String(s).replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
  function getW(){
    if (!worker){
      worker = new Worker(root.getAttribute('data-worker') || '../shared/pyworker.js');
      worker.onmessage = function(ev){ var m = ev.data, p = pending[m.id]; if (!p) return;
        if (m.type === 'status') p.status(m.text);
        else if (m.type === 'running'){ p.status(m.text); clearTimeout(p.timer); p.timer = setTimeout(function(){ p.tle(); }, RUN_TIMEOUT); }   // đồng hồ chạy bắt đầu SAU khi môi trường sẵn sàng
        else { clearTimeout(p.timer); delete pending[m.id]; p.finish(m); } };
      worker.onerror = function(e){ Object.keys(pending).forEach(function(k){ var p=pending[k]; clearTimeout(p.timer); delete pending[k]; p.finish({type:'fatal', error:'Worker lỗi: '+(e.message||'không tải được pyworker.js (kiểm tra mạng/CDN)')}); }); worker = null; };
    }
    return worker;
  }
  function run(code, ex, tests, status){
    return new Promise(function(resolve){
      var id = ++seq, w = getW();
      var p = {status: status, finish: resolve};
      p.tle = function(){ delete pending[id]; try{ worker.terminate(); }catch(e){} worker = null;
        resolve({type:'tle', error:'Quá ' + (RUN_TIMEOUT/1000) + ' giây (vòng lặp vô hạn hoặc thuật toán quá chậm). Đã dừng Python; lần chạy sau sẽ khởi động lại.'}); };
      p.timer = setTimeout(function(){ delete pending[id]; try{ worker.terminate(); }catch(e){} worker = null;
        resolve({type:'fatal', error:'Không tải được Python sau ' + (LOAD_TIMEOUT/1000) + ' giây: kiểm tra mạng (cần tải Pyodide từ cdn.jsdelivr.net) rồi thử lại.'}); }, LOAD_TIMEOUT);
      pending[id] = p;
      w.postMessage({id: id, code: code, fn: ex.fn, tests: tests, packages: ex.packages});
    });
  }
  var KEY = 'nlp-code-v1-';
  function load(id, k){ try{ return localStorage.getItem(KEY + id + '-' + k); }catch(e){ return null; } }
  function save(id, k, v){ try{ localStorage.setItem(KEY + id + '-' + k, v); }catch(e){} }
  function short(v){ var s = JSON.stringify(v); return s.length > 90 ? s.slice(0, 90) + '…' : s; }

  EX.forEach(function(ex){
    var card = document.createElement('div'); card.className = 'card code-card'; card.id = 'bai-' + ex.id;
    var done = load(ex.id, 'pass') === '1';
    card.innerHTML =
      '<div class="meta"><span class="tag">' + esc(ex.module) + '</span><span class="tag">' + esc(ex.level) + '</span><span class="tag">hàm <code>' + esc(ex.fn) + '</code></span><span class="badge ' + (done ? 'ok' : 'mid') + ' pass-badge">' + (done ? 'Đã đạt toàn bộ test' : 'Chưa đạt') + '</span></div>' +
      '<h3>' + esc(ex.title) + '</h3><p>' + ex.statement + '</p>' +
      '<table class="spec"><tr><th>Đầu vào</th><td>' + ex.inp + '</td></tr><tr><th>Đầu ra</th><td>' + ex.out + '</td></tr></table>' +
      '<details class="solution"><summary>Gợi ý</summary><div class="body">' + ex.hint + '</div></details>' +
      '<textarea class="code-ta" spellcheck="false" rows="14"></textarea>' +
      '<div class="numrow"><button class="chk b-vis" type="button">▶ Chạy test hiển thị</button><button class="chk b-all" type="button" style="background:#136f3a;border-color:#136f3a">✔ Chấm tất cả (cả test ẩn)</button><button class="b-custom" type="button">🧪 Đầu vào riêng</button><button class="b-reset" type="button">↺ Mã khởi đầu</button><span class="run-status" style="color:var(--muted);font-size:.9rem"></span></div>' +
      '<div class="custom" style="display:none"><p style="margin:.4em 0">Nhập danh sách đối số dạng JSON, ví dụ <code>' + esc(JSON.stringify(ex.tests[0].args)) + '</code></p><textarea class="code-ta custom-in" rows="3" spellcheck="false"></textarea><button class="chk b-crun" type="button">Chạy</button></div>' +
      '<div class="out res" style="display:none"></div>' +
      '<details class="solution"><summary>Lời giải mẫu (chỉ xem sau khi thử)</summary><div class="body"><pre class="code-pre"></pre></div></details>';
    root.appendChild(card);
    var ta = card.querySelector('.code-ta'); ta.value = load(ex.id, 'code') || ex.starter;
    card.querySelector('.code-pre').textContent = ex.reference;
    ta.addEventListener('input', function(){ save(ex.id, 'code', ta.value); });
    ta.addEventListener('keydown', function(e){ if (e.key === 'Tab'){ e.preventDefault(); var s = ta.selectionStart; ta.value = ta.value.slice(0, s) + '    ' + ta.value.slice(ta.selectionEnd); ta.selectionStart = ta.selectionEnd = s + 4; ta.dispatchEvent(new Event('input')); } });
    var st = card.querySelector('.run-status'), res = card.querySelector('.res');
    function doRun(all){
      var tests = ex.tests.filter(function(t){ return all || t.visible; });
      var btns = card.querySelectorAll('button.chk'); btns.forEach(function(b){ b.disabled = true; });
      st.textContent = 'Đang chuẩn bị…'; res.style.display = 'none'; res.innerHTML = '';
      run(ta.value, ex, tests, function(t){ st.textContent = t; }).then(function(m){
        btns.forEach(function(b){ b.disabled = false; }); st.textContent = '';
        res.style.display = 'block';
        if (m.type === 'tle'){ res.innerHTML = '<span class="badge no">⏱ QUÁ GIỜ (TLE)</span> ' + esc(m.error); return; }
        if (m.type === 'fatal'){ res.innerHTML = '<span class="badge no">Lỗi hệ thống</span> ' + esc(m.error); return; }
        var okN = 0, rows = m.results.map(function(r, i){
          var t = tests[i]; if (r.ok) okN++;
          return '<tr><td>' + (i + 1) + (t.visible ? '' : ' (ẩn)') + '</td><td><code>' + esc(short(t.args)) + '</code>' + (t.note && t.visible ? '<br><span style="color:var(--muted);font-size:.85em">' + esc(t.note) + '</span>' : '') + '</td><td>' + (t.visible ? '<code>' + esc(short(t.expected)) + '</code>' : '<i>ẩn</i>') + '</td><td>' + (r.error ? '<span class="badge no">' + esc(r.error) + '</span>' : '<code>' + esc(r.got) + '</code>') + '</td><td><span class="badge ' + (r.ok ? 'ok' : 'no') + '">' + (r.ok ? '✅ ĐÚNG' : (r.error ? '💥 LỖI CHẠY' : '❌ SAI KẾT QUẢ')) + '</span></td></tr>';
        }).join('');
        var allPass = okN === tests.length;
        res.innerHTML = '<p><b>' + okN + '/' + tests.length + ' test đạt</b>' + (all ? ' (đã gồm test ẩn)' : ' (chỉ test hiển thị)') + '</p><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Đầu vào</th><th>Kỳ vọng</th><th>Kết quả của bạn</th><th></th></tr></thead><tbody>' + rows + '</tbody></table></div>';
        if (all && allPass){ save(ex.id, 'pass', '1'); var b = card.querySelector('.pass-badge'); b.className = 'badge ok pass-badge'; b.textContent = 'Đã đạt toàn bộ test'; }
      });
    }
    card.querySelector('.b-custom').addEventListener('click', function(){ var c = card.querySelector('.custom'); c.style.display = c.style.display === 'none' ? 'block' : 'none'; var ci = card.querySelector('.custom-in'); if (!ci.value) ci.value = JSON.stringify(ex.tests[0].args); });
    card.querySelector('.b-crun').addEventListener('click', function(){
      var args; try{ args = JSON.parse(card.querySelector('.custom-in').value); }catch(e){ res.style.display = 'block'; res.innerHTML = '<span class="badge no">JSON không hợp lệ</span> ' + esc(e.message); return; }
      st.textContent = 'Đang chuẩn bị…'; res.style.display = 'none'; res.innerHTML = '';
      run(ta.value, ex, [{args: args, expected: null}], function(t){ st.textContent = t; }).then(function(m){ st.textContent = ''; res.style.display = 'block';
        if (m.type !== 'done'){ res.innerHTML = '<span class="badge no">' + (m.type === 'tle' ? '⏱ QUÁ GIỜ' : 'Lỗi') + '</span> ' + esc(m.error); return; }
        var r0 = m.results[0]; res.innerHTML = r0.error ? '<span class="badge no">💥 LỖI CHẠY</span> ' + esc(r0.error) : '<p>Kết quả của hàm: <code>' + esc(r0.got) + '</code></p>'; });
    });
    card.querySelector('.b-vis').addEventListener('click', function(){ doRun(false); });
    card.querySelector('.b-all').addEventListener('click', function(){ doRun(true); });
    card.querySelector('.b-reset').addEventListener('click', function(){ if (window.confirm('Xóa mã bạn đã viết ở bài này và quay về mã khởi đầu?')){ ta.value = ex.starter; save(ex.id, 'code', ex.starter); } });
  });
  if (window.nlpRenderMath) window.nlpRenderMath(root);
  window.__nlpCodeRun = run;   // phục vụ kiểm thử tự động
})();
