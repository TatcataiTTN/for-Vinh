// Ung dung luyen tap QHTT / Van tru hoc - 100% chay o trinh duyet, khong backend.
// Cham diem bang so sanh truc tiep voi du lieu da tinh san trong data/*.json
// (khong go tay dap an rieng trong app.js).

(function () {
  "use strict";

  // 4 bo trac nghiem doc lap hoan toan (khoa localStorage rieng), + 1 bo tinh toan.
  var SETS = {
    mcq: {
      dataFile: "data/mcq.json",
      storeKey: "qhtt_progress_v1",
      route: "mcq",
      title: "Trắc nghiệm v1 (100 câu)",
      shortTitle: "v1",
      navLabel: "v1 (100 câu)",
    },
    mcq2: {
      dataFile: "data/mcq_stepbystep.json",
      storeKey: "qhtt_progress_v2_stepbystep",
      route: "mcq2",
      title: "Trắc nghiệm v2 — giải từng bước (100 câu)",
      shortTitle: "v2",
      navLabel: "v2 — giải từng bước",
    },
    mcq3: {
      dataFile: "data/mcq3.json",
      storeKey: "qhtt_progress_v3_final",
      route: "mcq3",
      title: "Trắc nghiệm v3 — trọng tâm cuối kỳ: Mô hình hoá & Đơn hình (100 câu)",
      shortTitle: "v3",
      navLabel: "v3 — Xij & Đơn hình",
    },
    mcq4: {
      dataFile: "data/mcq4.json",
      storeKey: "qhtt_progress_v4_final",
      route: "mcq4",
      title: "Trắc nghiệm v4 — trọng tâm cuối kỳ: Đối ngẫu (100 câu)",
      shortTitle: "v4",
      navLabel: "v4 — Đối ngẫu",
    },
    mcq5: {
      dataFile: "data/mcq5.json",
      storeKey: "vth_progress_v5",
      route: "mcq5",
      title: "Trắc nghiệm v5 — Vận trù học: Mô hình hoá, Đồ thị & Đơn hình (100 câu)",
      shortTitle: "v5",
      navLabel: "v5 — Mô hình hoá & Đồ thị",
    },
    mcq6: {
      dataFile: "data/mcq6.json",
      storeKey: "vth_progress_v6",
      route: "mcq6",
      title: "Trắc nghiệm v6 — Vận trù học: QHTT nhị phân — Knapsack, Phân công, TSP (100 câu)",
      shortTitle: "v6",
      navLabel: "v6 — QHTT nhị phân",
    },
    mcq7: {
      dataFile: "data/mcq7.json",
      storeKey: "vth_progress_v7",
      route: "mcq7",
      title: "Trắc nghiệm v7 — Vận trù học: Vận tải mở rộng, Mạng lưới & Trò chơi (100 câu)",
      shortTitle: "v7",
      navLabel: "v7 — Mạng lưới & Trò chơi",
    },
    mcq8: {
      dataFile: "data/mcq8.json",
      storeKey: "vth_progress_v8",
      route: "mcq8",
      title: "Trắc nghiệm v8 — Vận trù học: Lý thuyết tổng hợp (100 câu)",
      shortTitle: "v8",
      navLabel: "v8 — Lý thuyết tổng hợp",
    },
  };
  var SEEN_V2_KEY = "qhtt_seen_v2_notice";
  var SEEN_V34_KEY = "qhtt_seen_v34_notice";
  var SEEN_V567_KEY = "qhtt_seen_v567_notice";
  var SEEN_V8_KEY = "qhtt_seen_v8_notice";
  var SEEN_CHIENLUOC_KEY = "qhtt_seen_chienluoc_notice";

  var state = {
    data: {}, // { mcq: [...], mcq2: [...], mcq3: [...], mcq4: [...] }
    progress: {}, // { mcq: {id:{selected,correct}}, ... } - moi bo 1 object rieng
    numeric: null,
    numericProgress: loadProgress("qhtt_progress_v1", { numeric: {} }).numeric || {},
  };
  Object.keys(SETS).forEach(function (key) {
    state.progress[key] = loadProgress(SETS[key].storeKey, {})[key === "mcq" ? "mcq" : key] || {};
  });

  function loadProgress(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  // Bo "mcq" (v1) luu chung 1 key voi "numeric" (tuong thich nguoc voi du lieu
  // nguoi dung da co san); cac bo mcq2/mcq3/mcq4 moi bo 1 key rieng, chi chua
  // dung 1 truong cua chinh no.
  function saveSet(key) {
    try {
      if (key === "mcq") {
        localStorage.setItem(SETS.mcq.storeKey, JSON.stringify({ mcq: state.progress.mcq, numeric: state.numericProgress }));
      } else {
        var obj = {};
        obj[key] = state.progress[key];
        localStorage.setItem(SETS[key].storeKey, JSON.stringify(obj));
      }
    } catch (e) {
      /* localStorage khong kha dung (che do an danh, v.v.) - bo qua im lang */
    }
  }
  function saveNumeric() {
    try {
      localStorage.setItem(SETS.mcq.storeKey, JSON.stringify({ mcq: state.progress.mcq, numeric: state.numericProgress }));
    } catch (e) {
      /* im lang */
    }
  }

  function resetSet(key) {
    state.progress[key] = {};
    saveSet(key);
  }
  function resetNumeric() {
    state.numericProgress = {};
    saveNumeric();
  }

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") e.className = attrs[k];
        else if (k === "html") e.innerHTML = attrs[k];
        else e.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      if (typeof c === "string") e.appendChild(document.createTextNode(c));
      else if (c) e.appendChild(c);
    });
    return e;
  }
  HTMLElement.prototype.also = function (fn) {
    fn(this);
    return this;
  };

  function renderMath(root) {
    if (window.renderMathInElement) {
      window.renderMathInElement(root, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
        ],
        throwOnError: false,
      });
    }
  }

  // ---------------- Loading du lieu, co try/catch + timeout ----------------
  function fetchJSON(path, timeoutMs) {
    return new Promise(function (resolve, reject) {
      var ctrl = new AbortController();
      var timer = setTimeout(function () {
        ctrl.abort();
        reject(new Error("Quá thời gian tải " + path));
      }, timeoutMs || 20000);
      fetch(path, { signal: ctrl.signal })
        .then(function (r) {
          clearTimeout(timer);
          if (!r.ok) throw new Error("HTTP " + r.status + " khi tải " + path);
          return r.json();
        })
        .then(resolve)
        .catch(function (err) {
          clearTimeout(timer);
          reject(err);
        });
    });
  }

  function fetchText(path, timeoutMs) {
    return new Promise(function (resolve, reject) {
      var ctrl = new AbortController();
      var timer = setTimeout(function () {
        ctrl.abort();
        reject(new Error("Quá thời gian tải " + path));
      }, timeoutMs || 20000);
      fetch(path, { signal: ctrl.signal })
        .then(function (r) {
          clearTimeout(timer);
          if (!r.ok) throw new Error("HTTP " + r.status + " khi tải " + path);
          return r.text();
        })
        .then(resolve)
        .catch(function (err) {
          clearTimeout(timer);
          reject(err);
        });
    });
  }

  function boot() {
    var app = document.getElementById("app");
    app.innerHTML = "";
    app.appendChild(el("div", { class: "loading" }, ["Đang tải dữ liệu bài tập…"]));

    var setKeys = Object.keys(SETS);
    Promise.all(
      setKeys.map(function (k) { return fetchJSON(SETS[k].dataFile); })
        .concat([fetchJSON("data/numeric.json"), fetchText("data/chienluoc.html")])
    )
      .then(function (res) {
        setKeys.forEach(function (k, i) { state.data[k] = res[i]; });
        state.numeric = res[res.length - 2];
        state.chienluocHtml = res[res.length - 1];
        window.addEventListener("hashchange", route);
        route();
      })
      .catch(function (err) {
        app.innerHTML = "";
        app.appendChild(
          el("div", { class: "err-box" }, [
            el("p", {}, ["Không tải được dữ liệu bài tập: " + err.message]),
            el("button", { class: "btn" }, ["Thử lại"]).also(function (b) {
              b.onclick = boot;
            }),
          ])
        );
      });
  }

  // ---------------------------- Routing ----------------------------
  function route() {
    var hash = location.hash.replace(/^#/, "") || "/";
    var parts = hash.split("/").filter(Boolean);
    updateNav(hash);

    if (parts.length === 0) return renderHome();
    if (SETS[parts[0]]) {
      if (parts.length === 1) return renderSetOverview(parts[0]);
      if (parts.length === 2 && parts[1] === "review") return renderSetReview(parts[0]);
      if (parts.length === 2) return renderSetQuestion(parts[0], parseInt(parts[1], 10));
    }
    if (parts[0] === "numeric" && parts.length === 1) return renderNumericOverview();
    if (parts[0] === "numeric" && parts.length === 2) return renderNumericQuestion(parseInt(parts[1], 10));
    if (parts[0] === "chienluoc") return renderChienLuoc();
    renderHome();
  }

  function updateNav(hash) {
    var firstSeg = "/" + (hash.replace(/^\//, "").split("/")[0] || "");
    document.querySelectorAll("#topnav a").forEach(function (a) {
      var r = a.getAttribute("data-route");
      var active = r === "/" ? (hash === "/" || hash === "") : firstSeg === r;
      a.classList.toggle("active", active);
    });
  }

  function mount(node) {
    var app = document.getElementById("app");
    app.innerHTML = "";
    app.appendChild(node);
    renderMath(app);
    window.scrollTo(0, 0);
  }

  function countStats(key) {
    var p = state.progress[key];
    var done = Object.keys(p).length;
    var correct = Object.keys(p).filter(function (id) { return p[id].correct; }).length;
    var wrong = done - correct;
    return { done: done, correct: correct, wrong: wrong, total: state.data[key] ? state.data[key].length : 100 };
  }

  // ---------------------------- Trang chu ----------------------------
  var BANNER_IDS = {};
  BANNER_IDS[SEEN_V2_KEY] = "v2-banner";
  BANNER_IDS[SEEN_V34_KEY] = "v34-banner";
  BANNER_IDS[SEEN_V567_KEY] = "v567-banner";
  BANNER_IDS[SEEN_V8_KEY] = "v8-banner";
  BANNER_IDS[SEEN_CHIENLUOC_KEY] = "cl-banner";

  function dismissNotice(key) {
    try { localStorage.setItem(key, "1"); } catch (e) { /* im lang */ }
    var b = document.getElementById(BANNER_IDS[key]);
    if (b) b.remove();
  }

  function updateBanner(id, seenKey, targetRoute, title, body) {
    var seen = false;
    try { seen = localStorage.getItem(seenKey) === "1"; } catch (e) { /* im lang */ }
    if (seen) return null;
    var closeBtn = el("button", { class: "banner-close", "aria-label": "Đóng thông báo" }, ["×"]);
    closeBtn.onclick = function () { dismissNotice(seenKey); };
    return el("div", { class: "update-banner", id: id }, [
      el("div", { class: "update-banner-text" }, [el("b", {}, [title]), body]),
      el("a", { class: "btn", href: "#/" + targetRoute, style: "margin:0" }, ["Xem ngay"]).also(function (a) {
        a.addEventListener("click", function () { dismissNotice(seenKey); });
      }),
      closeBtn,
    ]);
  }

  function renderHome() {
    var numDone = Object.keys(state.numericProgress).length;
    var numCorrect = Object.values(state.numericProgress).filter(function (x) { return x.correct; }).length;

    var children = [];
    var b2 = updateBanner("v2-banner", SEEN_V2_KEY, "mcq2", "🆕 Bản cập nhật (v2): ",
      "100 câu trắc nghiệm “giải từng bước” — 10 bài toán lớn, mỗi bài 10 câu tái hiện đúng trình tự lời " +
      "giải tự luận (đơn hình, hai pha, M, đối ngẫu, vận tải). Độc lập hoàn toàn với bộ 100 câu cũ.");
    if (b2) children.push(b2);
    var b34 = updateBanner("v34-banner", SEEN_V34_KEY, "mcq3", "🆕 Bản cập nhật (v3 + v4): ",
      "Thêm 200 câu trọng tâm ôn thi cuối kỳ QHTT — v3 (Xij, mô hình hoá, đơn hình) và v4 (đối ngẫu: phát biểu, " +
      "kiểm tra một cặp phương án có phải là tối ưu).");
    if (b34) children.push(b34);
    var b567 = updateBanner("v567-banner", SEEN_V567_KEY, "mcq5", "🆕 Bản cập nhật mới nhất (v5 + v6 + v7): ",
      "Thêm 300 câu Vận trù học — v5 (mô hình hoá, đồ thị, đơn hình), v6 (QHTT nhị phân: cái túi, phân công, " +
      "TSP), v7 (vận tải mở rộng, mạng lưới MST/Dijkstra/luồng cực đại/CPM, lý thuyết trò chơi). Có kèm hình vẽ " +
      "minh hoạ, nhiều dạng câu hỏi (trắc nghiệm/đúng-sai/điền đáp án/sắp xếp thứ tự).");
    if (b567) children.push(b567);
    var b8 = updateBanner("v8-banner", SEEN_V8_KEY, "mcq8", "🆕 Bản cập nhật mới nhất (v8): ",
      "Thêm 100 câu LÝ THUYẾT Vận trù học — khái niệm, định nghĩa, định lý tổng hợp: đại cương VTH, QHTT & đơn hình, " +
      "đối ngẫu, vận tải/phân công, đồ thị/đường đi ngắn nhất, MST/luồng cực đại, TSP/ba lô, CPM/PERT & lý thuyết trò " +
      "chơi, và tổng hợp so sánh các mô hình. Không tính toán số, tập trung vào bản chất lý thuyết.");
    if (b8) children.push(b8);
    var bcl = updateBanner("cl-banner", SEEN_CHIENLUOC_KEY, "chienluoc", "🆕 Trang mới — Chiến lược thi: ",
      "3 dạng bài trọng tâm cuối kỳ (Xij & khai triển biểu thức, Đơn hình, Đối ngẫu) — bảng chọn phương pháp " +
      "giải NHANH NHẤT cho từng tình huống đề bài, kèm ví dụ giải đầy đủ từng bước (số liệu đã kiểm chứng bằng " +
      "scipy, không gõ tay đáp án). Xem cách trình bày lời giải chuẩn để không bị mất điểm.");
    if (bcl) children.push(bcl);

    var statCells = Object.keys(SETS).map(function (k) {
      var s = countStats(k);
      return el("div", { class: "stat" }, [
        el("b", {}, [s.correct + "/" + s.done + "/" + s.total]),
        el("span", {}, [SETS[k].shortTitle + " đúng/đã làm/tổng"]),
      ]);
    });
    statCells.push(el("div", { class: "stat" }, [
      el("b", {}, [String(numCorrect) + "/" + String(numDone) + "/10"]),
      el("span", {}, ["Tính toán đúng/đã làm/tổng"]),
    ]));

    var quizBtns = Object.keys(SETS).map(function (k) {
      return el("a", { class: "btn", href: "#/" + k }, ["Trắc nghiệm " + SETS[k].navLabel]);
    });

    children.push(
      el("div", { class: "card hero" }, [
        el("h2", {}, ["Luyện tập Quy hoạch tuyến tính & Vận trù học"]),
        el("p", {}, [
          "7 bộ trắc nghiệm (700 câu) độc lập nhau + 10 bài tập tính toán. Chấm điểm ngay lập tức, không " +
          "cần gửi lên server nào. Mỗi bộ có nút “Làm lại từ đầu” và “Ôn lại câu sai” riêng.",
        ]),
        el("div", { class: "stat-row" }, statCells),
        el("div", {}, quizBtns.concat([el("a", { class: "btn secondary", href: "#/numeric" }, ["Bài tập tính toán"])])),
      ]),
      el("div", { class: "card" }, [
        el("h3", {}, ["Cách dùng"]),
        el("ul", {}, [
          el("li", {}, ["Trắc nghiệm: chọn 1 đáp án rồi bấm “Kiểm tra” — hiện ngay đúng/sai + giải thích."]),
          el("li", {}, ["v2/v3/v4: mỗi 10 câu liên tiếp = 1 chủ đề/bài toán lớn."]),
          el("li", {}, ["Nút “Ôn lại câu sai” trên mỗi bộ: xem lại đúng những câu đã làm sai, không lẫn câu đúng/chưa làm."]),
          el("li", {}, ["Nút “Làm lại từ đầu”: xoá toàn bộ tiến độ của riêng bộ đó (không ảnh hưởng các bộ khác)."]),
          el("li", {}, ["Bài tập tính toán: nhập số vào các ô (chấp nhận sai số nhỏ do làm tròn), bấm “Kiểm tra”."]),
          el("li", {}, ["Tiến độ lưu ở trình duyệt này (localStorage) — quay lại vẫn thấy câu đã làm; mất nếu xoá dữ liệu duyệt web."]),
        ]),
      ])
    );

    mount(el("div", {}, children));
  }

  // ---------------------------- Bo trac nghiem (dung chung cho v1..v4) ----------------------------
  function questionCardClass(prevInfo) {
    if (!prevInfo) return "q";
    return "q" + (prevInfo.correct ? " correct" : " wrong");
  }

  function actionRow(key) {
    var s = countStats(key);
    var resetBtn = el("button", { class: "btn secondary" }, ["🔄 Làm lại từ đầu"]);
    var armed = false;
    resetBtn.onclick = function () {
      if (!armed) {
        armed = true;
        resetBtn.textContent = "⚠️ Bấm lần nữa để xoá toàn bộ tiến độ";
        resetBtn.style.color = "#c0392b";
        resetBtn.style.borderColor = "#c0392b";
        setTimeout(function () {
          armed = false;
          resetBtn.textContent = "🔄 Làm lại từ đầu";
          resetBtn.style.color = "";
          resetBtn.style.borderColor = "";
        }, 4000);
        return;
      }
      resetSet(key);
      route();
    };
    var reviewBtn = el("a", { class: "btn secondary", href: "#/" + key + "/review" }, [
      "📌 Ôn lại câu sai (" + s.wrong + ")",
    ]);
    if (s.wrong === 0) reviewBtn.classList.add("disabled-look");
    return el("div", { class: "action-row" }, [reviewBtn, resetBtn]);
  }

  function renderSetOverview(key) {
    var cfg = SETS[key];
    var data = state.data[key];
    var groups = {};
    var groupOrder = [];
    data.forEach(function (q) {
      if (!groups[q.group]) { groups[q.group] = []; groupOrder.push(q.group); }
      groups[q.group].push(q);
    });
    var s = countStats(key);

    var body = [
      el("div", { class: "card" }, [
        el("h2", {}, [cfg.title]),
        el("div", { class: "progress-bar-outer" }, [
          el("div", { class: "progress-bar-inner", style: "width:" + s.done + "%" }),
        ]),
        el("p", {}, [s.done + " / " + s.total + " câu đã làm — " + s.correct + " đúng, " + s.wrong + " sai."]),
        actionRow(key),
      ]),
    ];

    groupOrder.forEach(function (g) {
      var cells = groups[g].map(function (q) {
        var p = state.progress[key][q.id];
        var b = el("button", { class: questionCardClass(p) }, [String(q.id)]);
        b.onclick = function () { location.hash = "#/" + key + "/" + q.id; };
        return b;
      });
      body.push(
        el("div", { class: "card" }, [
          el("h4", { style: "margin-top:0" }, [g]),
          el("div", { class: "qgrid-cells", style: "grid-template-columns:repeat(10,1fr)" }, cells),
        ])
      );
    });

    mount(el("div", {}, body));
  }

  function renderSetReview(key) {
    var cfg = SETS[key];
    var data = state.data[key];
    var p = state.progress[key];
    var wrongIds = Object.keys(p).filter(function (id) { return !p[id].correct; }).map(Number);
    var wrongQs = data.filter(function (q) { return wrongIds.indexOf(q.id) !== -1; });

    var body = [
      el("div", { class: "card" }, [
        el("h2", {}, ["Ôn lại câu sai — " + cfg.title]),
        el("p", {}, [
          wrongQs.length === 0
            ? "Không có câu nào đang sai trong bộ này 🎉 (hoặc bạn chưa làm câu nào)."
            : "Bạn đã làm sai " + wrongQs.length + " câu dưới đây. Bấm vào từng câu để xem lại đề, đáp án đúng và giải thích.",
        ]),
        el("a", { class: "btn secondary", href: "#/" + key }, ["← Quay lại danh sách đầy đủ"]),
      ]),
    ];

    if (wrongQs.length > 0) {
      var byGroup = {};
      var order = [];
      wrongQs.forEach(function (q) {
        if (!byGroup[q.group]) { byGroup[q.group] = []; order.push(q.group); }
        byGroup[q.group].push(q);
      });
      order.forEach(function (g) {
        var cells = byGroup[g].map(function (q) {
          var b = el("button", { class: "q wrong" }, [String(q.id)]);
          b.onclick = function () { location.hash = "#/" + key + "/" + q.id; };
          return b;
        });
        body.push(
          el("div", { class: "card" }, [
            el("h4", { style: "margin-top:0" }, [g]),
            el("div", { class: "qgrid-cells", style: "grid-template-columns:repeat(10,1fr)" }, cells),
          ])
        );
      });
    }
    mount(el("div", {}, body));
  }

  // Moi loai cau hoi (mcq / truefalse / fill / order) chi can cung cap:
  //   buildAnswerUI(q, prev, onSubmit) -> { widget, getAnswer() }
  //   describeAnswer(q, ans) -> chuoi text mo ta lai lua chon cu (khi da lam roi)
  // Phan khung (thanh dieu huong, luoi cau ben phai, luu tien do...) dung chung.
  var TYPE_HANDLERS = {
    mcq: { build: buildMcqUI },
    truefalse: { build: buildTrueFalseUI },
    fill: { build: buildFillUI },
    order: { build: buildOrderUI },
  };

  function buildMcqUI(q, prev, submit) {
    var prevSelected = prev ? (prev.answer ? prev.answer.selected : prev.selected) : null;
    var optWrap = el("div", { class: "options" });
    ["A", "B", "C", "D"].forEach(function (letter) {
      if (!q.options[letter]) return;
      var input = el("input", { type: "radio", name: "opt-mcq", value: letter });
      if (prev) input.disabled = true;
      if (prevSelected === letter) input.checked = true;
      var label = el("label", {}, [input, letter + ". " + q.options[letter]]);
      if (prev) {
        if (letter === q.correct) label.classList.add("correct");
        else if (letter === prevSelected) label.classList.add("wrong");
      }
      optWrap.appendChild(label);
    });
    return {
      widget: optWrap,
      grade: function () {
        var chosen = optWrap.querySelector("input:checked");
        if (!chosen) return null;
        var letter = chosen.value;
        return { answer: { selected: letter }, correct: letter === q.correct };
      },
      resultText: function (ans, correct) {
        return correct ? "✔ Bạn đã trả lời đúng." : "✘ Bạn đã chọn " + ans.selected + " (đáp án đúng: " + q.correct + ").";
      },
    };
  }

  // Cau dung/sai kieu 4 y a) b) c) d) - dung cho toan bo cau moi dung/sai
  function buildTrueFalseUI(q, prev, submit) {
    var wrap = el("div", { class: "options tf-wrap" });
    var rows = q.statements.map(function (st, i) {
      var name = "tf-" + i;
      var prevVal = prev && prev.answer ? prev.answer.values[i] : null;
      var trueInput = el("input", { type: "radio", name: name, value: "true" });
      var falseInput = el("input", { type: "radio", name: name, value: "false" });
      if (prev) { trueInput.disabled = true; falseInput.disabled = true; }
      if (prevVal === true) trueInput.checked = true;
      if (prevVal === false) falseInput.checked = true;
      var row = el("div", { class: "tf-row" }, [
        el("span", { class: "tf-text" }, [st.label + ") " + st.text]),
        el("label", { class: "tf-choice" }, [trueInput, " Đúng"]),
        el("label", { class: "tf-choice" }, [falseInput, " Sai"]),
      ]);
      if (prev) {
        var userVal = prevVal;
        var ok = userVal === st.correct;
        row.classList.add(ok ? "tf-ok" : "tf-bad");
        row.appendChild(el("span", { class: "tf-mark" }, [ok ? "✔" : ("✘ (đúng: " + (st.correct ? "Đúng" : "Sai") + ")")]));
      }
      return { row: row, trueInput: trueInput, falseInput: falseInput };
    });
    rows.forEach(function (r) { wrap.appendChild(r.row); });
    return {
      widget: wrap,
      grade: function () {
        var values = rows.map(function (r) {
          if (r.trueInput.checked) return true;
          if (r.falseInput.checked) return false;
          return null;
        });
        if (values.some(function (v) { return v === null; })) return null;
        var allCorrect = values.every(function (v, i) { return v === q.statements[i].correct; });
        return { answer: { values: values }, correct: allCorrect };
      },
      resultText: function (ans, correct) {
        var nOk = ans.values.filter(function (v, i) { return v === q.statements[i].correct; }).length;
        return correct
          ? "✔ Cả " + ans.values.length + " ý đều đúng."
          : "✘ Đúng " + nOk + "/" + ans.values.length + " ý — xem chi tiết từng ý ở trên.";
      },
    };
  }

  function normalizeFillAnswer(s) {
    return String(s).trim().toLowerCase().replace(/\s+/g, " ");
  }

  // Cau dien dap an: so (so sanh sai so) hoac van ban ngan (so sanh chuoi da chuan hoa)
  function buildFillUI(q, prev, submit) {
    var input = el("input", { type: "text", class: "fill-input", placeholder: q.placeholder || "nhập đáp án…" });
    if (prev) { input.value = prev.answer.text; input.disabled = true; }
    var wrap = el("div", { class: "fill-wrap" }, [input]);
    if (prev) {
      var ok = prev.correct;
      wrap.appendChild(el("span", { class: "fb", style: "margin-left:10px;color:" + (ok ? "#1e7e34" : "#c0392b") }, [
        ok ? "✔" : "✘ (đáp án đúng: " + q.answer + (q.answerType === "number" && q.tolerance ? "" : "") + ")",
      ]));
    }
    // Bam Enter cung nop bai, giong nhu bam nut Kiem tra
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") submit(); });
    return {
      widget: wrap,
      grade: function () {
        var raw = input.value.trim();
        if (raw === "") return null;
        var correct;
        if (q.answerType === "number") {
          var v = parseFloat(raw.replace(",", "."));
          if (isNaN(v)) return { answer: { text: raw }, correct: false };
          correct = Math.abs(v - q.answer) <= (q.tolerance != null ? q.tolerance : 0.01);
        } else {
          var acceptable = Array.isArray(q.answer) ? q.answer : [q.answer];
          correct = acceptable.some(function (a) { return normalizeFillAnswer(a) === normalizeFillAnswer(raw); });
        }
        return { answer: { text: raw }, correct: correct };
      },
      resultText: function (ans, correct) {
        return correct ? "✔ Chính xác." : "✘ Bạn điền “" + ans.text + "” — đáp án đúng: " + (Array.isArray(q.answer) ? q.answer[0] : q.answer) + ".";
      },
    };
  }

  // Cau sap xep thu tu: cac buoc hien theo dung thu tu luu trong q.items (da
  // duoc tron san khi soan du lieu), nguoi dung dung nut len/xuong de sap lai.
  function buildOrderUI(q, prev, submit) {
    var order = prev ? prev.answer.order.slice() : q.items.map(function (it) { return it.id; });
    var listEl = el("div", { class: "order-list" });
    function itemText(itemId) {
      var it = q.items.find(function (x) { return x.id === itemId; });
      return it ? it.text : itemId;
    }
    function render() {
      listEl.innerHTML = "";
      order.forEach(function (itemId, i) {
        var upBtn = el("button", { class: "order-btn", type: "button" }, ["↑"]);
        var downBtn = el("button", { class: "order-btn", type: "button" }, ["↓"]);
        if (prev) { upBtn.disabled = true; downBtn.disabled = true; }
        upBtn.onclick = function () {
          if (i === 0) return;
          var t = order[i - 1]; order[i - 1] = order[i]; order[i] = t;
          render();
        };
        downBtn.onclick = function () {
          if (i === order.length - 1) return;
          var t = order[i + 1]; order[i + 1] = order[i]; order[i] = t;
          render();
        };
        var row = el("div", { class: "order-row" }, [
          el("span", { class: "order-index" }, [String(i + 1) + "."]),
          el("span", { class: "order-text" }, [itemText(itemId)]),
          el("span", { class: "order-btns" }, [upBtn, downBtn]),
        ]);
        if (prev) {
          var correctIdx = q.correctOrder.indexOf(itemId);
          row.classList.add(correctIdx === i ? "tf-ok" : "tf-bad");
        }
        listEl.appendChild(row);
      });
    }
    render();
    return {
      widget: listEl,
      grade: function () {
        var correct = order.every(function (itemId, i) { return q.correctOrder[i] === itemId; });
        return { answer: { order: order }, correct: correct };
      },
      resultText: function (ans, correct) {
        return correct ? "✔ Đúng thứ tự." : "✘ Sai thứ tự — thứ tự đúng được đánh dấu xanh/đỏ ở trên.";
      },
    };
  }

  function renderSetQuestion(key, id) {
    var data = state.data[key];
    var q = data.find(function (x) { return x.id === id; });
    if (!q) return renderSetOverview(key);
    var prev = state.progress[key][id];
    // Tuong thich nguoc: du lieu cu (truoc khi co nhieu loai cau hoi) luu
    // truc tiep {selected, correct} thay vi {answer:{...}, correct}.
    if (prev && !prev.answer) prev = { answer: prev, correct: prev.correct };
    var qType = q.type || "mcq";
    var handler = TYPE_HANDLERS[qType];

    var explain = el("div", { class: "explain" + (prev ? " show" : ""), html: q.explanation });
    var checkBtn = el("button", { class: "btn" }, ["Kiểm tra"]);
    var fbLine = el("p", { class: "result-line" }, []);

    var ui = handler.build(q, prev, function () { checkBtn.click(); });

    if (prev) {
      checkBtn.disabled = true;
      fbLine.textContent = ui.resultText(prev.answer, prev.correct);
      fbLine.style.color = prev.correct ? "#1e7e34" : "#c0392b";
    }

    checkBtn.onclick = function () {
      var g = ui.grade();
      if (!g) { fbLine.textContent = "Hãy hoàn thành câu trả lời trước khi kiểm tra."; return; }
      state.progress[key][id] = { answer: g.answer, correct: g.correct };
      saveSet(key);
      renderSetQuestion(key, id);
    };

    var idx = data.findIndex(function (x) { return x.id === id; });
    var navRow = el("div", { class: "nav-row" }, [
      el("a", { class: "btn secondary", href: idx > 0 ? "#/" + key + "/" + data[idx - 1].id : "#/" + key }, ["← Câu trước"]),
      el("a", { class: "btn secondary", href: "#/" + key }, ["Danh sách"]),
      el("a", { class: "btn", href: idx < data.length - 1 ? "#/" + key + "/" + data[idx + 1].id : "#/" + key }, ["Câu sau →"]),
    ]);

    var typeBadge = { mcq: "Trắc nghiệm", truefalse: "Đúng / Sai", fill: "Điền đáp án", order: "Sắp xếp thứ tự" }[qType];

    var main = el("div", { class: "card" }, [
      el("div", { class: "qgroup-label" }, [q.group + " · Câu " + q.id + "/" + data.length + " · " + typeBadge]),
      el("div", { class: "qtext", html: q.question }),
      q.image ? el("img", { class: "qimg", src: "img/" + q.image, alt: "hình minh họa câu " + q.id }) : null,
      ui.widget,
      checkBtn,
      fbLine,
      explain,
      navRow,
    ]);

    var cells = data.map(function (qq) {
      var p = state.progress[key][qq.id];
      var cls = questionCardClass(p).replace("q", "").trim();
      if (qq.id === id) cls += " current";
      var b = el("button", { class: cls.trim() }, [String(qq.id)]);
      b.onclick = function () { location.hash = "#/" + key + "/" + qq.id; };
      return b;
    });
    var side = el("div", { class: "qgrid" }, [
      el("h4", {}, ["Danh sách câu"]),
      el("div", { class: "qgrid-cells" }, cells),
    ]);

    mount(el("div", { class: "quiz-layout" }, [main, side]));
  }

  // ---------------------------- Trang chien luoc giai nhanh (B1/B2/B3) ----------------------------
  function renderChienLuoc() {
    var wrap = el("div", { class: "card", html: state.chienluocHtml || "<p>Không tải được nội dung.</p>" });
    mount(wrap);
  }

  // ---------------------------- Numeric: tong quan ----------------------------
  function renderNumericOverview() {
    var doneCount = Object.keys(state.numericProgress).length;
    var wrongCount = Object.keys(state.numericProgress).filter(function (id) { return !state.numericProgress[id].correct; }).length;
    var cells = state.numeric.map(function (ex) {
      var p = state.numericProgress[ex.id];
      var card = el("div", { class: "card" }, [
        el("div", { class: "qgroup-label" }, ["Bài " + ex.id + (p ? (p.correct ? " · Đã đúng" : " · Cần làm lại") : "")]),
        el("h4", { style: "margin:4px 0" }, [ex.title]),
        el("a", { class: "btn secondary", href: "#/numeric/" + ex.id }, [p ? "Xem lại" : "Làm bài"]),
      ]);
      return card;
    });
    var resetBtn = el("button", { class: "btn secondary" }, ["🔄 Làm lại từ đầu"]);
    var armed = false;
    resetBtn.onclick = function () {
      if (!armed) {
        armed = true;
        resetBtn.textContent = "⚠️ Bấm lần nữa để xoá toàn bộ tiến độ";
        resetBtn.style.color = "#c0392b";
        setTimeout(function () { armed = false; resetBtn.textContent = "🔄 Làm lại từ đầu"; resetBtn.style.color = ""; }, 4000);
        return;
      }
      resetNumeric();
      route();
    };
    var body = [
      el("div", { class: "card" }, [
        el("h2", {}, ["10 bài tập tính toán"]),
        el("div", { class: "progress-bar-outer" }, [
          el("div", { class: "progress-bar-inner", style: "width:" + doneCount * 10 + "%" }),
        ]),
        el("p", {}, [doneCount + " / 10 bài đã làm (" + wrongCount + " cần làm lại). Kết quả nhập vào được chấp nhận sai số nhỏ (làm tròn)."]),
        el("div", { class: "action-row" }, [resetBtn]),
      ]),
    ].concat(cells);
    mount(el("div", {}, body));
  }

  // ---------------------------- Numeric: 1 bai ----------------------------
  function renderNumericQuestion(id) {
    var ex = state.numeric.find(function (x) { return x.id === id; });
    if (!ex) return renderNumericOverview();
    var prev = state.numericProgress[id];

    var inputs = [];
    var fieldsWrap = el("div", {});
    ex.fields.forEach(function (f, i) {
      var input = el("input", { type: "text", placeholder: "nhập số…" });
      if (prev) { input.value = prev.values[i]; input.disabled = true; }
      var fb = el("span", { class: "fb" }, []);
      if (prev) {
        var ok = Math.abs(parseFloat(prev.values[i]) - f.expected) <= (f.tol || 0.01);
        fb.textContent = ok ? "✔" : "✘ (đúng: " + f.expected + ")";
        fb.style.color = ok ? "#1e7e34" : "#c0392b";
      }
      inputs.push(input);
      fieldsWrap.appendChild(el("div", { class: "field-row" }, [
        el("label", { html: "$" + f.name.replace(/(\d+)/, "_{$1}").replace(/\*/g, "^*") + "$" }),
        input,
        fb,
      ]));
    });

    var checkBtn = el("button", { class: "btn" }, ["Kiểm tra"]);
    var resultLine = el("p", { class: "result-line" }, []);
    if (prev) {
      checkBtn.disabled = true;
      resultLine.textContent = prev.correct ? "✔ Chính xác toàn bộ." : "✘ Còn sai ở 1 hoặc nhiều ô — xem đáp án đúng ở trên.";
      resultLine.style.color = prev.correct ? "#1e7e34" : "#c0392b";
    }
    checkBtn.onclick = function () {
      var vals = inputs.map(function (inp) { return inp.value.trim(); });
      if (vals.some(function (v) { return v === "" || isNaN(parseFloat(v)); })) {
        resultLine.textContent = "Hãy nhập đủ số vào tất cả các ô.";
        resultLine.style.color = "#c0392b";
        return;
      }
      var allOk = ex.fields.every(function (f, i) {
        return Math.abs(parseFloat(vals[i]) - f.expected) <= (f.tol || 0.01);
      });
      state.numericProgress[id] = { values: vals, correct: allOk };
      saveNumeric();
      renderNumericQuestion(id);
    };

    var idx = state.numeric.findIndex(function (x) { return x.id === id; });
    var navRow = el("div", { class: "nav-row" }, [
      el("a", { class: "btn secondary", href: idx > 0 ? "#/numeric/" + state.numeric[idx - 1].id : "#/numeric" }, ["← Bài trước"]),
      el("a", { class: "btn secondary", href: "#/numeric" }, ["Danh sách"]),
      el("a", { class: "btn", href: idx < state.numeric.length - 1 ? "#/numeric/" + state.numeric[idx + 1].id : "#/numeric" }, ["Bài sau →"]),
    ]);

    var card = el("div", { class: "card" }, [
      el("div", { class: "qgroup-label" }, ["Bài tập tính toán " + ex.id + "/10"]),
      el("h3", {}, [ex.title]),
      el("p", { html: ex.prompt }),
      fieldsWrap,
      checkBtn,
      resultLine,
      el("p", { class: "source-note" }, ["Nguồn: " + ex.source]),
      navRow,
    ]);
    mount(card);
  }

  boot();
})();
