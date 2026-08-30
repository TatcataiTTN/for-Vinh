// ============================================================
// Luyện tập CSDL - engine chính (SQL có sql.js, Trắc nghiệm, Tự luận)
// ============================================================

const STORAGE_KEY = "sqlpractice_progress_v1";

// Suy ra bài giảng lý thuyết (hoc-day-du/bai-N.html) khớp nhất với 1 câu hỏi SQL,
// dựa trên từ khóa trong "topic". Dùng chung cho cả 3 CSDL (classicmodels/truong_hoc/
// cua_hang_sach) vì các topic được đặt tên nhất quán theo dạng bài, không theo CSDL.
function topicToLecture(topic) {
  if (!topic) return null;
  const t = topic;
  if (/Bài 10/.test(t)) return 10;
  if (/JOIN/.test(t)) return 6;
  if (/Subquery/.test(t)) return 7;
  if (/GROUP BY|HAVING/.test(t)) return 5;
  if (/DML/.test(t)) return 8;
  if (/LIKE|ORDER BY|BETWEEN|\bIN\b/.test(t)) return 4;
  if (/WHERE/.test(t)) return 3;
  return null;
}

const state = {
  SQL: null,
  dbBytes: {},         // { dbName: Uint8Array }
  questions: [],        // toàn bộ câu hỏi, mọi loại, đã gắn collectionId + kind
  byCollection: {},      // { collectionId: [questions...] }
  currentId: null,
  editor: null,
  uiExpanded: {},        // { collectionId: bool } - chỉ tồn tại trong phiên, không lưu
};

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; } catch (e) { return {}; }
}
function saveProgress(p) { localStorage.setItem(STORAGE_KEY, JSON.stringify(p)); }
function markDone(id, ok) {
  const p = loadProgress();
  p[id] = ok ? "done" : (p[id] === "done" ? "done" : "tried");
  saveProgress(p);
}

// ---------------------------------------------------------- Tải trang lần đầu (xem loading-ux)
const CACHE_NAME = "sqlpractice-assets-v2";
const BOOT_TIMEOUT_MS = 45000;

async function fetchWithProgress(url, onProgress) {
  let cache = null;
  try { cache = await caches.open(CACHE_NAME); } catch (e) {}

  if (cache) {
    const cached = await cache.match(url);
    if (cached) {
      const buf = await cached.arrayBuffer();
      onProgress(buf.byteLength, buf.byteLength, true);
      return buf;
    }
  }

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Không tải được "${url}" (mã lỗi HTTP ${res.status}).`);
  const total = Number(res.headers.get("content-length")) || 0;

  if (!res.body || !res.body.getReader) {
    const buf = await res.arrayBuffer();
    onProgress(buf.byteLength, buf.byteLength || total, false);
    if (cache) { try { await cache.put(url, new Response(buf.slice(0))); } catch (e) {} }
    return buf;
  }

  const reader = res.body.getReader();
  const chunks = []; let loaded = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value); loaded += value.length;
    onProgress(loaded, total, false);
  }
  const blob = new Blob(chunks);
  const buf = await blob.arrayBuffer();
  if (cache) { try { await cache.put(url, new Response(blob)); } catch (e) {} }
  return buf;
}

function fmtMB(bytes) { return (bytes / (1024 * 1024)).toFixed(2); }

function setupBootUI(resources) {
  document.getElementById("boot-progress-list").innerHTML = resources.map(r => `
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
  if (fromCache) { fill.classList.add("done"); sizeEl.textContent = "✔ đã có sẵn (trong bộ nhớ trình duyệt)"; }
  else if (pct >= 100) { fill.classList.add("done"); sizeEl.textContent = `✔ ${fmtMB(loaded)} MB`; }
  else { sizeEl.textContent = `${fmtMB(loaded)} / ${total ? fmtMB(total) : "?"} MB`; }
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
    { key: "engine", label: "⚙️ Công cụ chạy SQL (SQLite/WebAssembly)", url: "vendor/sqljs/sql-wasm.wasm", expected: 655300, kind: "bin" },
    { key: "classicmodels", label: "🚗 Cơ sở dữ liệu Classicmodels", url: "data/classicmodels.sqlite", expected: 311296, kind: "bin" },
    { key: "truong_hoc", label: "🏫 Cơ sở dữ liệu Trường Học", url: "data/truong_hoc.sqlite", expected: 212992, kind: "bin" },
    { key: "cua_hang_sach", label: "📚 Cơ sở dữ liệu Cửa Hàng Sách", url: "data/cua_hang_sach.sqlite", expected: 40960, kind: "bin" },
    { key: "questions", label: "📄 Ngân hàng câu hỏi SQL", url: "data/questions.json", expected: 1311694, kind: "json" },
    { key: "mcqsql", label: "🧠 Trắc nghiệm SQL thực hành", url: "data/mcq_sql.json", expected: 129336, kind: "json" },
    { key: "mcqtheory", label: "📖 Trắc nghiệm lý thuyết CSDL", url: "data/mcq_theory.json", expected: 82961, kind: "json" },
    { key: "essays", label: "✍️ Ngân hàng câu tự luận", url: "data/essays.json", expected: 23616, kind: "json" },
  ];
  const totalExpected = resources.reduce((s, r) => s + r.expected, 0);
  setupBootUI(resources);
  updateBootTotal(0, totalExpected);

  const loadedByKey = {};
  resources.forEach(r => loadedByKey[r.key] = 0);
  function reportTotal() {
    updateBootTotal(Object.values(loadedByKey).reduce((a, b) => a + b, 0), totalExpected);
  }

  const timeoutId = setTimeout(() => {
    showBootError("Quá trình tải mất nhiều thời gian hơn bình thường (quá 45 giây). Có thể do mạng chậm hoặc mất kết nối. Hãy kiểm tra Internet rồi thử lại.");
  }, BOOT_TIMEOUT_MS);

  try {
    const buffersByKey = {};
    for (const r of resources) {
      buffersByKey[r.key] = await fetchWithProgress(r.url, (loaded, total, fromCache) => {
        loadedByKey[r.key] = loaded;
        updateBootItem(r.key, loaded, total || r.expected, fromCache);
        reportTotal();
      });
    }

    state.SQL = await initSqlJs({ wasmBinary: buffersByKey.engine });

    ["classicmodels", "truong_hoc", "cua_hang_sach"].forEach(name => {
      state.dbBytes[name] = new Uint8Array(buffersByKey[name]);
    });

    const dec = (buf) => new TextDecoder("utf-8").decode(buf);
    const sqlQuestions = JSON.parse(dec(buffersByKey.questions)).map(q => ({ ...q, kind: "sql", collectionId: q.db }));
    const mcqSql = JSON.parse(dec(buffersByKey.mcqsql)).map(q => ({ ...q, kind: "mcq", collectionId: "mcqsql" }));
    const mcqTheory = JSON.parse(dec(buffersByKey.mcqtheory)).map(q => ({ ...q, kind: "mcq", collectionId: "mcqtheory" }));
    const essays = JSON.parse(dec(buffersByKey.essays)).map(q => ({ ...q, kind: "essay", collectionId: "essay" }));

    state.questions = [...sqlQuestions, ...mcqSql, ...mcqTheory, ...essays];
    COLLECTIONS.forEach(c => {
      state.byCollection[c.id] = state.questions
        .filter(q => q.collectionId === c.id)
        .sort((a, b) => (a.group || 0) - (b.group || 0) || a.id.localeCompare(b.id));
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

function freshDb(dbName) { return new state.SQL.Database(state.dbBytes[dbName]); }

// ---------------------------------------------------------- Routing
function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  if (!hash) {
    renderLanding();
    state.currentId = null;
  } else {
    const q = state.questions.find(x => x.id === hash);
    if (q) { state.currentId = q.id; renderQuestionAny(q); }
    else renderLanding();
  }
  renderSidebar();
}
function goTo(id) { location.hash = "#/" + id; }

// ---------------------------------------------------------- Sidebar
function renderSidebar() {
  const progress = loadProgress();
  const totalDone = state.questions.filter(q => progress[q.id] === "done").length;
  const total = state.questions.length || 1;
  document.getElementById("progress-fill").style.width = Math.round((totalDone / total) * 100) + "%";
  document.getElementById("progress-label-num").textContent = `${totalDone}/${total}`;

  const nav = document.getElementById("sidebar-nav");
  nav.innerHTML = "";

  COLLECTIONS.forEach(col => {
    const list = state.byCollection[col.id] || [];
    if (list.length === 0) return;
    const doneInCol = list.filter(q => progress[q.id] === "done").length;
    const containsCurrent = list.some(q => q.id === state.currentId);
    const expanded = state.uiExpanded[col.id] !== undefined ? state.uiExpanded[col.id] : containsCurrent;

    const group = document.createElement("div");
    group.className = "db-group";

    const title = document.createElement("div");
    title.className = "db-group-title";
    title.style.cursor = "pointer";
    title.innerHTML = `<span>${expanded ? "▾" : "▸"}</span><span>${col.icon}</span><span>${col.label}</span><span style="margin-left:auto;opacity:.7;">${doneInCol}/${list.length}</span>`;
    title.onclick = () => { state.uiExpanded[col.id] = !expanded; renderSidebar(); };
    group.appendChild(title);

    if (expanded) {
      if (col.kind === "mcq") {
        let lastGroup = null;
        list.forEach((q, idxInCol) => {
          if (q.group !== lastGroup) {
            lastGroup = q.group;
            const sub = document.createElement("div");
            sub.className = "sidebar-subheader";
            sub.textContent = col.groupLabel ? col.groupLabel(q.group) : `Nhóm ${q.group}`;
            group.appendChild(sub);
          }
          const item = document.createElement("div");
          item.className = "q-nav-item" + (q.id === state.currentId ? " active" : "");
          const dotClass = progress[q.id] === "done" ? " done" : "";
          const numInGroup = list.filter(x => x.group === q.group).indexOf(q) + 1;
          item.innerHTML = `<span class="q-status-dot${dotClass}"></span><span class="qn">${numInGroup}</span><span>${escapeHtml(q.question.slice(0, 46))}${q.question.length > 46 ? "…" : ""}</span>`;
          item.onclick = () => goTo(q.id);
          group.appendChild(item);
        });
      } else {
        list.forEach((q, idx) => {
          const item = document.createElement("div");
          item.className = "q-nav-item" + (q.id === state.currentId ? " active" : "");
          const dotClass = progress[q.id] === "done" ? " done" : "";
          item.innerHTML = `<span class="q-status-dot${dotClass}"></span><span class="qn">${String(idx + 1).padStart(2, "0")}</span><span>${escapeHtml(q.title)}</span>`;
          item.onclick = () => goTo(q.id);
          group.appendChild(item);
        });
      }
    }
    nav.appendChild(group);
  });
}

// ---------------------------------------------------------- Landing
function renderLanding() {
  const main = document.getElementById("main-content");
  const progress = loadProgress();
  const total = state.questions.length;
  const done = state.questions.filter(q => progress[q.id] === "done").length;

  const cards = COLLECTIONS.map(col => {
    const list = state.byCollection[col.id] || [];
    if (list.length === 0) return "";
    const firstId = list[0] ? list[0].id : "";
    const doneInCol = list.filter(q => progress[q.id] === "done").length;
    return `
      <div class="db-card" onclick="goTo('${firstId}')">
        <div class="icon">${col.icon}</div>
        <h4>${col.label}</h4>
        <p>${col.desc}</p>
        <p style="margin-top:8px;color:#0f9b8e;font-weight:600;">${doneInCol}/${list.length} câu đã hoàn thành</p>
        <span class="go">Bắt đầu luyện tập →</span>
      </div>`;
  }).join("");

  main.innerHTML = `
    <div class="landing-hero">
      <h2>Luyện SQL &amp; Cơ sở dữ liệu cùng dữ liệu thật</h2>
      <p>Câu hỏi SQL được chấm bằng cách chạy trực tiếp câu lệnh của bạn trong trình duyệt (SQLite/WASM). Trắc nghiệm chấm ngay tức thì. Tự luận (thiết kế ERD, dự đoán TRIGGER, chuẩn hóa...) cho bạn tự so với đáp án mẫu có thang điểm chi tiết, giống hệt cách chấm trong đề thi thật.</p>
      <div class="stat-row">
        <div class="stat-box"><div class="num">${total}</div><div class="lbl">Tổng số câu hỏi</div></div>
        <div class="stat-box"><div class="num">${COLLECTIONS.length}</div><div class="lbl">Bộ sưu tập khác nhau</div></div>
        <div class="stat-box"><div class="num">${done}</div><div class="lbl">Đã hoàn thành</div></div>
      </div>
    </div>
    <div class="card" style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;background:linear-gradient(135deg,#eef2f7,#f0fdfa);">
      <div>
        <h3 style="margin:0 0 4px;">📖 Chưa nắm chắc lý thuyết? Học đầy đủ trước đã.</h3>
        <p style="margin:0;color:var(--text-soft);font-size:13.5px;">10 bài giảng dạng slide, bám sát đúng nội dung các buổi học thật — từ cài đặt MySQL tới JOIN và Subquery.</p>
      </div>
      <a href="hoc-day-du/index.html" class="btn btn-primary" style="text-decoration:none;flex-shrink:0;">Vào học đầy đủ →</a>
    </div>
    <div class="db-card-grid">${cards}</div>
    <p class="footer-note">💾 Tiến trình học được lưu ngay trên trình duyệt này — đóng tab, tắt máy, mở lại đúng đường link vẫn còn nguyên. Chỉ mất nếu bạn xoá dữ liệu trình duyệt (Clear browsing data) hoặc dùng chế độ ẩn danh.<br>Lần mở đầu tiên cần tải dữ liệu về máy; từ lần thứ hai trở đi trình duyệt đã lưu sẵn nên mở gần như ngay lập tức.</p>
  `;
}

function escapeHtml(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ---------------------------------------------------------- Điều phối theo loại câu hỏi
function renderQuestionAny(q) {
  if (q.kind === "sql") renderSqlQuestion(q);
  else if (q.kind === "mcq") renderMcqQuestion(q);
  else if (q.kind === "essay") renderEssayQuestion(q);
}

function navButtons(list, q) {
  const idx = list.findIndex(x => x.id === q.id);
  const prevQ = list[idx - 1], nextQ = list[idx + 1];
  return `
    <div class="btn-row" style="justify-content: space-between;">
      <button class="btn btn-nav" ${prevQ ? "" : "disabled"} id="btn-prev">← Câu trước</button>
      <button class="btn btn-nav" ${nextQ ? "" : "disabled"} id="btn-next">Câu sau →</button>
    </div>`;
}
function wireNavButtons(list, q) {
  const idx = list.findIndex(x => x.id === q.id);
  const prevQ = list[idx - 1], nextQ = list[idx + 1];
  if (prevQ) document.getElementById("btn-prev").onclick = () => goTo(prevQ.id);
  if (nextQ) document.getElementById("btn-next").onclick = () => goTo(nextQ.id);
}

// ---------------------------------------------------------- CÂU HỎI SQL
function renderSqlQuestion(q) {
  const main = document.getElementById("main-content");
  const list = state.byCollection[q.db];
  const idx = list.findIndex(x => x.id === q.id);
  const schema = SCHEMAS[q.db];

  const schemaRows = schema.tables.map(t =>
    `<div class="schema-table"><span class="t-name">${t.name}</span> — <span class="t-cols">${t.cols}</span></div>`
  ).join("");

  const lecture = topicToLecture(q.topic);
  const lectureLink = lecture
    ? `<a class="btn btn-ghost" style="text-decoration:none;" href="hoc-day-du/bai-${lecture}.html">📖 Xem lý thuyết Bài ${lecture}</a>`
    : "";

  main.innerHTML = `
    <div class="topbar">
      <h2>${schema.icon} ${q.title}</h2>
      <span class="db-pill">${schema.label} · Câu ${idx + 1}/${list.length}</span>
    </div>
    <div class="card">
      <h3><span class="diff-badge diff-${q.difficulty}">${"★".repeat(q.difficulty)}${"☆".repeat(3 - q.difficulty)}</span> Đề bài</h3>
      <div class="topic-chip">${q.topic}</div>
      ${lectureLink ? `<div style="margin:6px 0 2px;">${lectureLink}</div>` : ""}
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
    ${navButtons(list, q)}
  `;

  document.getElementById("schema-toggle").onclick = () => {
    const box = document.getElementById("schema-box");
    box.classList.toggle("open");
    document.getElementById("schema-toggle").textContent = (box.classList.contains("open") ? "▾ " : "▸ ") + "Xem sơ đồ các bảng liên quan";
  };
  document.getElementById("btn-hint").onclick = () => document.getElementById("hint-box").classList.toggle("open");
  document.getElementById("btn-solution").onclick = () => document.getElementById("solution-box").classList.toggle("open");

  const draftKey = "draft_" + q.id;
  state.editor = CodeMirror.fromTextArea(document.getElementById("sql-editor"), {
    mode: "text/x-sql", theme: "eclipse", lineNumbers: true, indentUnit: 2, viewportMargin: Infinity,
  });
  state.editor.setValue(localStorage.getItem(draftKey) || "");
  state.editor.on("change", () => localStorage.setItem(draftKey, state.editor.getValue()));

  document.getElementById("btn-run").onclick = () => runQuery(q, false);
  document.getElementById("btn-submit").onclick = () => runQuery(q, true);
  wireNavButtons(list, q);
}

function normalizeVal(v) {
  if (v === null || v === undefined) return null;
  if (typeof v === "number") return Math.round(v * 10000) / 10000;
  if (typeof v === "string") {
    const n = Number(v);
    if (v.trim() !== "" && !isNaN(n) && /^-?\d+(\.\d+)?$/.test(v.trim())) return Math.round(n * 10000) / 10000;
    return v.trim();
  }
  return v;
}
function rowsEqual(rowsA, rowsB) {
  if (rowsA.length !== rowsB.length) return false;
  for (let i = 0; i < rowsA.length; i++) {
    const a = rowsA[i], b = rowsB[i];
    if (a.length !== b.length) return false;
    for (let j = 0; j < a.length; j++) if (normalizeVal(a[j]) !== normalizeVal(b[j])) return false;
  }
  return true;
}
function execSqlJsToTable(db, sql) {
  const res = db.exec(sql);
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
  shown.forEach(r => { html += "<tr>" + r.map(v => `<td>${v === null ? "<i>NULL</i>" : escapeHtml(String(v))}</td>`).join("") + "</tr>"; });
  html += `</tbody></table></div>`;
  if (limit && rows.length > limit) html += `<p style="font-size:12px;color:#5b6b7c;margin-top:6px;">Hiển thị ${limit}/${rows.length} dòng đầu tiên.</p>`;
  container.innerHTML = html;
}

function runQuery(q, grading) {
  const sql = state.editor.getValue().trim();
  const resultArea = document.getElementById("result-area");
  if (!sql) { resultArea.innerHTML = `<div class="verdict err">⚠️ Bạn chưa nhập câu lệnh SQL nào.</div>`; return; }

  let db;
  try { db = freshDb(q.db); }
  catch (e) { resultArea.innerHTML = `<div class="verdict err">Lỗi khởi tạo CSDL: ${escapeHtml(e.message)}</div>`; return; }

  try {
    let table;
    if (q.type === "dml") { db.run(sql); table = execSqlJsToTable(db, q.verifySql); }
    else table = execSqlJsToTable(db, sql);

    if (!grading) {
      resultArea.innerHTML = `<div class="verdict ok">${q.type === "dml" ? "✔ Câu lệnh đã chạy. Đây là dữ liệu sau khi kiểm tra lại:" : "▶ Kết quả câu lệnh của bạn:"}</div>`;
      const box = document.createElement("div");
      renderResultTable(box, table ? table.columns : null, table ? table.rows : [], 50);
      resultArea.appendChild(box);
    } else {
      gradeAndShow(q, table, resultArea);
    }
  } catch (e) {
    resultArea.innerHTML = `<div class="verdict err">❌ Lỗi khi chạy SQL: ${escapeHtml(e.message)}</div>`;
    markDone(q.id, false); renderSidebar();
  } finally { db.close(); }
}

function gradeAndShow(q, table, resultArea) {
  const expected = q.expected;
  const gotRows = table ? table.rows : [];
  const gotCols = table ? table.columns : [];
  const ok = expected.rows.length === 0
    ? gotRows.length === 0
    : (table && gotCols.length === expected.columns.length && rowsEqual(gotRows, expected.rows));

  markDone(q.id, ok); renderSidebar();

  resultArea.innerHTML = ok
    ? `<div class="verdict ok">✅ Chính xác! Kết quả của bạn khớp với đáp án (${expected.rows.length} dòng).</div>`
    : `<div class="verdict bad">❌ Chưa đúng. Kết quả của bạn khác với đáp án mong đợi — hãy kiểm tra lại điều kiện lọc, JOIN, hoặc GROUP BY/HAVING.</div>`;

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

// ---------------------------------------------------------- CÂU HỎI TRẮC NGHIỆM (MCQ)
function renderMcqQuestion(q) {
  const main = document.getElementById("main-content");
  const col = COLLECTIONS.find(c => c.id === q.collectionId);
  const list = state.byCollection[q.collectionId];
  const idx = list.findIndex(x => x.id === q.id);
  const groupLabel = col.groupLabel ? col.groupLabel(q.group) : `Nhóm ${q.group}`;

  const optionsHtml = q.options.map((opt, i) => `
    <label class="mcq-option" id="mcq-opt-${i}">
      <input type="radio" name="mcq" value="${i}" />
      <span class="mcq-letter">${String.fromCharCode(65 + i)}</span>
      <span class="mcq-text">${escapeHtml(opt)}</span>
    </label>
  `).join("");

  main.innerHTML = `
    <div class="topbar">
      <h2>${col.icon} ${groupLabel}</h2>
      <span class="db-pill">${col.label} · Câu ${idx + 1}/${list.length}</span>
    </div>
    <div class="card">
      <h3>Câu hỏi</h3>
      <p class="prompt-text">${escapeHtml(q.question)}</p>
      <div class="mcq-options">${optionsHtml}</div>
      <div class="btn-row">
        <button class="btn btn-primary" id="btn-submit-mcq" disabled>✔ Nộp câu trả lời</button>
      </div>
      <div class="result-area" id="result-area"></div>
    </div>
    ${navButtons(list, q)}
  `;

  let selected = null;
  q.options.forEach((_, i) => {
    document.getElementById(`mcq-opt-${i}`).onclick = () => {
      selected = i;
      q.options.forEach((__, j) => document.getElementById(`mcq-opt-${j}`).classList.remove("selected"));
      document.getElementById(`mcq-opt-${i}`).classList.add("selected");
      document.getElementById("btn-submit-mcq").disabled = false;
    };
  });

  document.getElementById("btn-submit-mcq").onclick = () => {
    if (selected === null) return;
    const ok = selected === q.correctIndex;
    markDone(q.id, ok); renderSidebar();
    q.options.forEach((__, j) => {
      const el = document.getElementById(`mcq-opt-${j}`);
      if (j === q.correctIndex) el.classList.add("correct");
      else if (j === selected) el.classList.add("wrong");
    });
    document.getElementById("result-area").innerHTML = ok
      ? `<div class="verdict ok">✅ Chính xác!</div>`
      : `<div class="verdict bad">❌ Chưa đúng. Đáp án đúng là <b>${String.fromCharCode(65 + q.correctIndex)}. ${escapeHtml(q.options[q.correctIndex])}</b></div>`;
  };

  wireNavButtons(list, q);
}

// ---------------------------------------------------------- CÂU HỎI TỰ LUẬN (ESSAY)
function renderEssayQuestion(q) {
  const main = document.getElementById("main-content");
  const col = COLLECTIONS.find(c => c.id === q.collectionId);
  const list = state.byCollection[q.collectionId];
  const idx = list.findIndex(x => x.id === q.id);

  const rubricHtml = q.rubric.map(r => `<li>${escapeHtml(r.criterion)} <b>(${r.points} điểm)</b></li>`).join("");

  main.innerHTML = `
    <div class="topbar">
      <h2>${col.icon} ${q.title}</h2>
      <span class="db-pill">${col.label} · Câu ${idx + 1}/${list.length}</span>
    </div>
    <div class="card">
      <h3><span class="diff-badge diff-${q.difficulty}">${"★".repeat(q.difficulty)}${"☆".repeat(3 - q.difficulty)}</span> Đề bài</h3>
      <div class="topic-chip">${q.topic} · Thang điểm ${q.totalPoints}</div>
      <p class="prompt-text" style="white-space:pre-wrap;">${escapeHtml(q.prompt)}</p>
    </div>
    <div class="card">
      <h3>✍️ Bài làm của bạn (viết bằng lời, không cần đúng định dạng)</h3>
      <textarea id="essay-editor" style="width:100%;min-height:160px;padding:12px;border:1px solid var(--border);border-radius:10px;font-family:inherit;font-size:14.5px;box-sizing:border-box;" placeholder="Trình bày bài làm của bạn ở đây trước khi xem đáp án mẫu..."></textarea>
      <div class="btn-row">
        <button class="btn btn-primary" id="btn-reveal">🔎 Xem đáp án mẫu &amp; tự chấm</button>
        <button class="btn btn-ghost" id="btn-hint">💡 Gợi ý cách trình bày</button>
      </div>
      <div class="hint-box" id="hint-box">${escapeHtml(q.guidance)}</div>
      <div class="result-area" id="result-area"></div>
    </div>
    ${navButtons(list, q)}
  `;

  const draftKey = "essay_draft_" + q.id;
  const editor = document.getElementById("essay-editor");
  editor.value = localStorage.getItem(draftKey) || "";
  editor.addEventListener("input", () => localStorage.setItem(draftKey, editor.value));

  document.getElementById("btn-hint").onclick = () => document.getElementById("hint-box").classList.toggle("open");

  document.getElementById("btn-reveal").onclick = () => {
    markDone(q.id, true); // tự luận: đã xem đáp án & tự chấm coi như đã hoàn thành lượt ôn tập này
    renderSidebar();
    document.getElementById("result-area").innerHTML = `
      <div class="verdict ok">📋 Đáp án mẫu — tự so sánh với bài làm của bạn và tự chấm theo thang điểm bên dưới:</div>
      <div class="solution-box open" style="white-space:pre-wrap;">${escapeHtml(q.modelAnswer)}</div>
      <p style="font-size:13px;font-weight:600;color:#16324f;margin:14px 0 6px;">Thang điểm chi tiết (tổng ${q.totalPoints} điểm):</p>
      <ul style="font-size:13.5px;line-height:1.7;padding-left:20px;">${rubricHtml}</ul>
    `;
  };

  wireNavButtons(list, q);
}

boot();
