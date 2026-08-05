// ============================================================
// SQL Practice - engine chính
// ============================================================

const STORAGE_KEY = "sqlpractice_progress_v1";

const state = {
  SQL: null,
  dbBytes: {},       // { dbName: Uint8Array }
  questions: [],      // toàn bộ câu hỏi
  byDb: {},           // { dbName: [questions] }
  currentId: null,
  editor: null,
  hintOpen: false,
  solutionOpen: false,
};

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch (e) { return {}; }
}
function saveProgress(p) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
}
function markDone(id, ok) {
  const p = loadProgress();
  p[id] = ok ? "done" : (p[id] === "done" ? "done" : "tried");
  saveProgress(p);
}

const CACHE_NAME = "sqlpractice-assets-v1";
const BOOT_TIMEOUT_MS = 45000;

// Tải một URL thành Uint8Array, có báo tiến độ (loaded, total) và lưu vào
// Cache Storage của trình duyệt để lần mở sau không phải tải lại.
async function fetchWithProgress(url, onProgress) {
  let cache = null;
  try { cache = await caches.open(CACHE_NAME); } catch (e) { /* Cache API không khả dụng, vẫn tải bình thường */ }

  if (cache) {
    const cached = await cache.match(url);
    if (cached) {
      const buf = await cached.arrayBuffer();
      onProgress(buf.byteLength, buf.byteLength, true);
      return new Uint8Array(buf);
    }
  }

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Không tải được "${url}" (mã lỗi HTTP ${res.status}).`);

  const total = Number(res.headers.get("content-length")) || 0;

  if (!res.body || !res.body.getReader) {
    // Trình duyệt không hỗ trợ streaming - tải thẳng, không có tiến độ chi tiết
    const buf = await res.arrayBuffer();
    onProgress(buf.byteLength, buf.byteLength || total, false);
    if (cache) { try { await cache.put(url, new Response(buf.slice(0))); } catch (e) {} }
    return new Uint8Array(buf);
  }

  const reader = res.body.getReader();
  const chunks = [];
  let loaded = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    loaded += value.length;
    onProgress(loaded, total, false);
  }
  const blob = new Blob(chunks);
  const buf = await blob.arrayBuffer();
  if (cache) { try { await cache.put(url, new Response(blob)); } catch (e) {} }
  return new Uint8Array(buf);
}

function fmtMB(bytes) { return (bytes / (1024 * 1024)).toFixed(2); }

function setupBootUI(resources) {
  const list = document.getElementById("boot-progress-list");
  list.innerHTML = resources.map(r => `
    <div class="boot-item" id="boot-item-${r.key}">
      <div class="boot-item-row">
        <span>${r.label}</span>
        <span class="bi-size" id="boot-item-size-${r.key}">chờ tải...</span>
      </div>
      <div class="boot-item-track"><div class="boot-item-fill" id="boot-item-fill-${r.key}" style="width:0%;"></div></div>
    </div>
  `).join("");
}

function updateBootItem(key, loaded, total, fromCache) {
  const fill = document.getElementById(`boot-item-fill-${key}`);
  const sizeEl = document.getElementById(`boot-item-size-${key}`);
  if (!fill || !sizeEl) return;
  const pct = total ? Math.min(100, Math.round((loaded / total) * 100)) : 100;
  fill.style.width = pct + "%";
  if (fromCache) {
    fill.classList.add("done");
    sizeEl.textContent = "✔ đã có sẵn (trong bộ nhớ trình duyệt)";
  } else if (pct >= 100) {
    fill.classList.add("done");
    sizeEl.textContent = `✔ ${fmtMB(loaded)} MB`;
  } else {
    sizeEl.textContent = `${fmtMB(loaded)} / ${total ? fmtMB(total) : "?"} MB`;
  }
}

function updateBootTotal(totalLoaded, totalExpected) {
  const pct = totalExpected ? Math.min(100, Math.round((totalLoaded / totalExpected) * 100)) : 0;
  document.getElementById("boot-total-fill").style.width = pct + "%";
  document.getElementById("boot-total-pct").textContent = pct + "%";
  document.getElementById("boot-total-label").textContent = `${fmtMB(totalLoaded)} / ${fmtMB(totalExpected)} MB`;
}

function showBootError(message) {
  document.getElementById("boot-icon").textContent = "⚠️";
  document.getElementById("boot-title").textContent = "Không tải được trang";
  document.getElementById("boot-error-text").textContent = message;
  document.getElementById("boot-error-box").style.display = "block";
}

async function boot() {
  const resources = [
    { key: "engine", label: "⚙️ Công cụ chạy SQL (SQLite/WebAssembly)", url: "vendor/sqljs/sql-wasm.wasm", expected: 655300 },
    { key: "classicmodels", label: "🚗 Cơ sở dữ liệu Classicmodels", url: "data/classicmodels.sqlite", expected: 311296 },
    { key: "truong_hoc", label: "🏫 Cơ sở dữ liệu Trường Học", url: "data/truong_hoc.sqlite", expected: 212992 },
    { key: "cua_hang_sach", label: "📚 Cơ sở dữ liệu Cửa Hàng Sách", url: "data/cua_hang_sach.sqlite", expected: 40960 },
    { key: "questions", label: "📄 Ngân hàng câu hỏi", url: "data/questions.json", expected: 82542 },
  ];
  const totalExpected = resources.reduce((s, r) => s + r.expected, 0);
  setupBootUI(resources);
  updateBootTotal(0, totalExpected);

  const loadedByKey = {};
  resources.forEach(r => loadedByKey[r.key] = 0);
  function reportTotal() {
    const sum = Object.values(loadedByKey).reduce((a, b) => a + b, 0);
    updateBootTotal(sum, totalExpected);
  }

  const timeoutId = setTimeout(() => {
    showBootError("Quá trình tải mất nhiều thời gian hơn bình thường (quá 45 giây). Có thể do mạng chậm hoặc mất kết nối. Hãy kiểm tra Internet rồi thử lại.");
  }, BOOT_TIMEOUT_MS);

  try {
    const bytesByKey = {};
    for (const r of resources) {
      bytesByKey[r.key] = await fetchWithProgress(r.url, (loaded, total, fromCache) => {
        loadedByKey[r.key] = loaded;
        updateBootItem(r.key, loaded, total || r.expected, fromCache);
        reportTotal();
      });
    }

    state.SQL = await initSqlJs({ wasmBinary: bytesByKey.engine });

    const dbNames = Object.keys(SCHEMAS);
    dbNames.forEach(name => { state.dbBytes[name] = bytesByKey[name]; });

    state.questions = JSON.parse(new TextDecoder("utf-8").decode(bytesByKey.questions));
    dbNames.forEach(name => {
      state.byDb[name] = state.questions.filter(q => q.db === name).sort((a, b) => a.id.localeCompare(b.id));
    });

    clearTimeout(timeoutId);
    renderSidebar();
    window.addEventListener("hashchange", route);
    route();
    document.getElementById("boot-overlay").classList.add("hidden");
  } catch (err) {
    clearTimeout(timeoutId);
    showBootError(err && err.message ? err.message : "Có lỗi không xác định xảy ra khi tải trang.");
  }
}

const retryBtnEl = document.getElementById("boot-retry-btn");
if (retryBtnEl) retryBtnEl.onclick = () => location.reload();

function freshDb(dbName) {
  return new state.SQL.Database(state.dbBytes[dbName]);
}

// ---------------------------------------------------------- Routing
function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  if (!hash || hash === "") {
    renderLanding();
    state.currentId = null;
  } else {
    const q = state.questions.find(x => x.id === hash);
    if (q) {
      state.currentId = q.id;
      renderQuestion(q);
    } else {
      renderLanding();
    }
  }
  renderSidebar();
}

function goTo(id) { location.hash = "#/" + id; }

// ---------------------------------------------------------- Sidebar
function renderSidebar() {
  const progress = loadProgress();
  const totalDone = state.questions.filter(q => progress[q.id] === "done").length;
  const total = state.questions.length || 1;
  const pct = Math.round((totalDone / total) * 100);

  const nav = document.getElementById("sidebar-nav");
  nav.innerHTML = "";

  document.getElementById("progress-fill").style.width = pct + "%";
  document.getElementById("progress-label-num").textContent = `${totalDone}/${total}`;

  Object.keys(SCHEMAS).forEach(dbName => {
    const group = document.createElement("div");
    group.className = "db-group";
    const title = document.createElement("div");
    title.className = "db-group-title";
    title.innerHTML = `<span>${SCHEMAS[dbName].icon}</span><span>${SCHEMAS[dbName].label}</span>`;
    group.appendChild(title);

    (state.byDb[dbName] || []).forEach((q, idx) => {
      const item = document.createElement("div");
      item.className = "q-nav-item" + (q.id === state.currentId ? " active" : "");
      const dotClass = progress[q.id] === "done" ? " done" : "";
      item.innerHTML = `<span class="q-status-dot${dotClass}"></span><span class="qn">${String(idx+1).padStart(2,"0")}</span><span>${q.title}</span>`;
      item.onclick = () => goTo(q.id);
      group.appendChild(item);
    });
    nav.appendChild(group);
  });
}

// ---------------------------------------------------------- Landing
function renderLanding() {
  const main = document.getElementById("main-content");
  const progress = loadProgress();
  const total = state.questions.length;
  const done = state.questions.filter(q => progress[q.id] === "done").length;

  const cards = Object.keys(SCHEMAS).map(dbName => {
    const s = SCHEMAS[dbName];
    const qs = state.byDb[dbName] || [];
    const firstId = qs[0] ? qs[0].id : "";
    const doneInDb = qs.filter(q => progress[q.id] === "done").length;
    return `
      <div class="db-card" onclick="goTo('${firstId}')">
        <div class="icon">${s.icon}</div>
        <h4>${s.label}</h4>
        <p>${s.desc}</p>
        <p style="margin-top:8px;color:#0f9b8e;font-weight:600;">${doneInDb}/${qs.length} câu đã hoàn thành</p>
        <span class="go">Bắt đầu luyện tập →</span>
      </div>`;
  }).join("");

  main.innerHTML = `
    <div class="landing-hero">
      <h2>Luyện SQL cùng dữ liệu thật</h2>
      <p>Mỗi câu hỏi được chấm bằng cách chạy trực tiếp câu lệnh của bạn trong trình duyệt (SQLite/WASM) và so sánh với đáp án đúng. Không cần cài đặt gì, không cần internet sau khi tải trang xong.</p>
      <div class="stat-row">
        <div class="stat-box"><div class="num">${total}</div><div class="lbl">Tổng số câu hỏi</div></div>
        <div class="stat-box"><div class="num">3</div><div class="lbl">Cơ sở dữ liệu khác nhau</div></div>
        <div class="stat-box"><div class="num">${done}</div><div class="lbl">Đã hoàn thành</div></div>
      </div>
    </div>
    <div class="db-card-grid">${cards}</div>
    <p class="footer-note">💾 Tiến trình học được lưu ngay trên trình duyệt này — đóng tab, tắt máy, mở lại đúng đường link vẫn còn nguyên. Chỉ mất nếu bạn xoá dữ liệu trình duyệt (Clear browsing data) hoặc dùng chế độ ẩn danh.<br>Lần mở đầu tiên cần tải khoảng 1,5&nbsp;MB (3 CSDL + công cụ chạy SQL); từ lần thứ hai trở đi trình duyệt đã lưu sẵn nên mở gần như ngay lập tức.</p>
  `;
}

// ---------------------------------------------------------- Question page
function renderQuestion(q) {
  const main = document.getElementById("main-content");
  const list = state.byDb[q.db];
  const idx = list.findIndex(x => x.id === q.id);
  const prevQ = list[idx - 1];
  const nextQ = list[idx + 1];
  const schema = SCHEMAS[q.db];

  const schemaRows = schema.tables.map(t =>
    `<div class="schema-table"><span class="t-name">${t.name}</span> — <span class="t-cols">${t.cols}</span></div>`
  ).join("");

  main.innerHTML = `
    <div class="topbar">
      <h2>${schema.icon} ${q.title}</h2>
      <span class="db-pill">${schema.label} · Câu ${idx+1}/${list.length}</span>
    </div>

    <div class="card">
      <h3><span class="diff-badge diff-${q.difficulty}">${"★".repeat(q.difficulty)}${"☆".repeat(3-q.difficulty)}</span> Đề bài</h3>
      <div class="topic-chip">${q.topic}</div>
      <p class="prompt-text">${q.prompt}</p>
      <div style="margin-top:12px;">
        <span class="schema-toggle" id="schema-toggle">▸ Xem sơ đồ các bảng liên quan</span>
        <div class="schema-box" id="schema-box">${schemaRows}</div>
      </div>
    </div>

    <div class="card">
      <h3>✍️ Bài làm của bạn ${q.type === "dml" ? "(câu lệnh INSERT/UPDATE/DELETE)" : "(câu lệnh SELECT)"}</h3>
      <div class="editor-wrap"><textarea id="sql-editor"></textarea></div>
      <div class="btn-row">
        <button class="btn btn-primary" id="btn-submit">✔ Nộp bài / Chấm điểm</button>
        <button class="btn btn-ghost" id="btn-run">▶ Chạy thử (không chấm)</button>
        <button class="btn btn-ghost" id="btn-hint">💡 Gợi ý</button>
        <button class="btn btn-ghost" id="btn-solution">🔎 Xem lời giải</button>
      </div>
      <div class="hint-box" id="hint-box">${q.hint}</div>
      <div class="solution-box" id="solution-box">${escapeHtml(q.solutionSql)}${q.verifySql ? "\n\n-- Sau khi chạy câu trên, kiểm tra bằng:\n" + escapeHtml(q.verifySql) : ""}</div>
      <div class="result-area" id="result-area"></div>
    </div>

    <div class="btn-row" style="justify-content: space-between;">
      <button class="btn btn-nav" ${prevQ ? "" : "disabled"} id="btn-prev">← Câu trước</button>
      <button class="btn btn-nav" ${nextQ ? "" : "disabled"} id="btn-next">Câu sau →</button>
    </div>
  `;

  // Schema toggle
  document.getElementById("schema-toggle").onclick = () => {
    const box = document.getElementById("schema-box");
    box.classList.toggle("open");
    document.getElementById("schema-toggle").textContent =
      (box.classList.contains("open") ? "▾ " : "▸ ") + "Xem sơ đồ các bảng liên quan";
  };

  // Hint / solution toggles
  document.getElementById("btn-hint").onclick = () => {
    document.getElementById("hint-box").classList.toggle("open");
  };
  document.getElementById("btn-solution").onclick = () => {
    document.getElementById("solution-box").classList.toggle("open");
  };

  // CodeMirror editor
  const draftKey = "draft_" + q.id;
  const savedDraft = localStorage.getItem(draftKey) || "";
  state.editor = CodeMirror.fromTextArea(document.getElementById("sql-editor"), {
    mode: "text/x-sql",
    theme: "eclipse",
    lineNumbers: true,
    indentUnit: 2,
    viewportMargin: Infinity,
  });
  state.editor.setValue(savedDraft);
  state.editor.on("change", () => {
    localStorage.setItem(draftKey, state.editor.getValue());
  });

  document.getElementById("btn-run").onclick = () => runQuery(q, false);
  document.getElementById("btn-submit").onclick = () => runQuery(q, true);
  if (prevQ) document.getElementById("btn-prev").onclick = () => goTo(prevQ.id);
  if (nextQ) document.getElementById("btn-next").onclick = () => goTo(nextQ.id);
}

function escapeHtml(s) {
  return (s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

// ---------------------------------------------------------- Chạy & chấm điểm
function normalizeVal(v) {
  if (v === null || v === undefined) return null;
  if (typeof v === "number") return Math.round(v * 10000) / 10000;
  if (typeof v === "string") {
    const n = Number(v);
    if (v.trim() !== "" && !isNaN(n) && /^-?\d+(\.\d+)?$/.test(v.trim())) {
      return Math.round(n * 10000) / 10000;
    }
    return v.trim();
  }
  return v;
}

function rowsEqual(rowsA, rowsB) {
  if (rowsA.length !== rowsB.length) return false;
  for (let i = 0; i < rowsA.length; i++) {
    const a = rowsA[i], b = rowsB[i];
    if (a.length !== b.length) return false;
    for (let j = 0; j < a.length; j++) {
      if (normalizeVal(a[j]) !== normalizeVal(b[j])) return false;
    }
  }
  return true;
}

function execSqlJsToTable(db, sql) {
  const res = db.exec(sql); // array of {columns, values}
  if (!res || res.length === 0) return null;
  const last = res[res.length - 1];
  return { columns: last.columns, rows: last.values };
}

function renderResultTable(container, columns, rows, limit) {
  if (!columns) {
    container.innerHTML = `<p style="color:#5b6b7c;font-size:13px;">Câu lệnh chạy thành công nhưng không trả về bảng dữ liệu nào để hiển thị.</p>`;
    return;
  }
  const shown = limit ? rows.slice(0, limit) : rows;
  let html = `<div class="result-table-wrap"><table class="result-table"><thead><tr>`;
  columns.forEach(c => html += `<th>${escapeHtml(c)}</th>`);
  html += `</tr></thead><tbody>`;
  shown.forEach(r => {
    html += "<tr>" + r.map(v => `<td>${v === null ? "<i>NULL</i>" : escapeHtml(String(v))}</td>`).join("") + "</tr>";
  });
  html += `</tbody></table></div>`;
  if (limit && rows.length > limit) {
    html += `<p style="font-size:12px;color:#5b6b7c;margin-top:6px;">Hiển thị ${limit}/${rows.length} dòng đầu tiên.</p>`;
  }
  container.innerHTML = html;
}

function runQuery(q, grading) {
  const sql = state.editor.getValue().trim();
  const resultArea = document.getElementById("result-area");
  if (!sql) {
    resultArea.innerHTML = `<div class="verdict err">⚠️ Bạn chưa nhập câu lệnh SQL nào.</div>`;
    return;
  }

  let db;
  try {
    db = freshDb(q.db);
  } catch (e) {
    resultArea.innerHTML = `<div class="verdict err">Lỗi khởi tạo CSDL: ${escapeHtml(e.message)}</div>`;
    return;
  }

  try {
    if (q.type === "dml") {
      db.run(sql);
      const table = execSqlJsToTable(db, q.verifySql);
      if (!grading) {
        resultArea.innerHTML = `<div class="verdict ok">✔ Câu lệnh đã chạy. Đây là dữ liệu sau khi kiểm tra lại:</div>`;
        const box = document.createElement("div");
        renderResultTable(box, table ? table.columns : null, table ? table.rows : [], 50);
        resultArea.appendChild(box);
      } else {
        gradeAndShow(q, table, resultArea);
      }
    } else {
      const table = execSqlJsToTable(db, sql);
      if (!grading) {
        resultArea.innerHTML = `<div class="verdict ok">▶ Kết quả câu lệnh của bạn:</div>`;
        const box = document.createElement("div");
        renderResultTable(box, table ? table.columns : null, table ? table.rows : [], 50);
        resultArea.appendChild(box);
      } else {
        gradeAndShow(q, table, resultArea);
      }
    }
  } catch (e) {
    resultArea.innerHTML = `<div class="verdict err">❌ Lỗi khi chạy SQL: ${escapeHtml(e.message)}</div>`;
    markDone(q.id, false);
    renderSidebar();
  } finally {
    db.close();
  }
}

function gradeAndShow(q, table, resultArea) {
  const expected = q.expected;
  const gotRows = table ? table.rows : [];
  const gotCols = table ? table.columns : [];
  // sql.js không trả về bảng nào cả khi SELECT hợp lệ nhưng có 0 dòng kết quả
  // (không có way nào lấy tên cột trong trường hợp đó) — nên khi đáp án đúng
  // cũng là 0 dòng, chỉ cần học sinh cũng ra 0 dòng là được tính đúng.
  const ok = expected.rows.length === 0
    ? gotRows.length === 0
    : (table && gotCols.length === expected.columns.length && rowsEqual(gotRows, expected.rows));

  markDone(q.id, ok);
  renderSidebar();

  let html = "";
  if (ok) {
    html += `<div class="verdict ok">✅ Chính xác! Kết quả của bạn khớp với đáp án (${expected.rows.length} dòng).</div>`;
  } else {
    html += `<div class="verdict bad">❌ Chưa đúng. Kết quả của bạn khác với đáp án mong đợi — hãy kiểm tra lại điều kiện lọc, JOIN, hoặc GROUP BY/HAVING.</div>`;
  }
  resultArea.innerHTML = html;

  const yourBox = document.createElement("div");
  yourBox.innerHTML = `<p style="font-size:13px;font-weight:600;color:#16324f;margin:10px 0 4px;">Kết quả của bạn (${gotRows.length} dòng):</p>`;
  const t1 = document.createElement("div");
  renderResultTable(t1, gotCols.length ? gotCols : null, gotRows, 30);
  yourBox.appendChild(t1);
  resultArea.appendChild(yourBox);

  if (!ok) {
    const expBox = document.createElement("div");
    expBox.innerHTML = `<p style="font-size:13px;font-weight:600;color:#16324f;margin:14px 0 4px;">Đáp án đúng có ${expected.rows.length} dòng (bấm "Xem lời giải" để biết câu SQL mẫu):</p>`;
    const t2 = document.createElement("div");
    renderResultTable(t2, expected.columns, expected.rows, 10);
    expBox.appendChild(t2);
    resultArea.appendChild(expBox);
  }
}

boot();
