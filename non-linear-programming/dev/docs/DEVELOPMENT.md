# Tài liệu phát triển — site Tối ưu hóa phi tuyến & lồi

Tài liệu này mô tả **cách site được xây, cách chạy lại, cách thêm nội dung và cách kiểm thử**, để người khác (hoặc chính bạn sau vài tuần) tiếp tục được mà không phải đoán.

## 1. Tổng quan kiến trúc

Site là **web tĩnh** (HTML + JS thuần, không backend) host trên GitHub Pages. Mọi nội dung được **sinh từ Python** rồi commit vào repo.

```
Phenikaa - Nonlinear Programming - Convex Optimization/
├── Slides/                     3 slide chính khóa (PDF) — nguồn nội dung
├── for-Vinh/                   clone repo TatcataiTTN/for-Vinh  (thư mục deploy)
│   └── non-linear-programming/
│       ├── index.html, modules/00..03/, kiem-chung/, code/, phat-trien/   (trang đã sinh)
│       ├── shared/             CSS + JS dùng chung (deck.js, quiz.js, widgets.js, pyrunner.js, pyworker.js, KaTeX)
│       ├── assets/             sơ đồ drawio (SVG) và ảnh trang slide gốc
│       └── dev/                bản sao mã nguồn sinh site (xem mục 9)
└── NLP-work/                   mã nguồn và dữ liệu làm việc (KHÔNG nằm trong repo gốc, chỉ có bản sao trong dev/)
    ├── verify/verify_all.py    tính lại mọi con số bằng numpy/scipy/sympy → results.json
    ├── build/                  gen_site.py, helpers.py, qlib.py, c_*.py (nội dung), q_*.py (câu hỏi), gen_diagrams.py
    ├── code/                   script ví dụ, notebook, bài tập lập trình (reference.py, build_exercises.py, test)
    ├── tests/                  kiểm thử trình duyệt (puppeteer) và pytest
    └── docs/DEVELOPMENT.md     (file này)
```

### Luồng dữ liệu

```
Slides/*.pdf ──đọc──▶ c_m*.py (deck + ví dụ) ┐
verify_all.py ──▶ results.json ──────────────┤
q_m*.py (ngân hàng câu hỏi) ─▶ qlib.finalize ┼─▶ gen_site.py ─▶ HTML trong for-Vinh/non-linear-programming/
gen_diagrams.py ─▶ drawio ─▶ SVG ────────────┤
reference.py ─▶ build_exercises.py ─▶ exercises.json ─▶ trang code/
```

Nguyên tắc: **không gõ tay đáp số**. Mọi số trong bài giảng lấy từ `results.json` (do `verify_all.py` tính) hoặc tính ngay lúc build trong `c_*.py`.

## 2. Yêu cầu môi trường

| Thành phần | Dùng để | Cài đặt |
|---|---|---|
| Python 3.10+ | sinh site, kiểm chứng | `pip install numpy scipy sympy cvxpy matplotlib nbformat nbconvert pytest` |
| `pdftoppm` (poppler) | cắt ảnh trang slide | `brew install poppler` |
| drawio CLI | xuất sơ đồ SVG | `brew install drawio` |
| Node + puppeteer-core + Chrome | kiểm thử trình duyệt | `npm i puppeteer-core` (dùng Chrome có sẵn) |
| `git`, `gh` | deploy | `gh auth login` |

## 3. Lệnh thường dùng

```bash
# 1) Tính lại số liệu (khi đổi bài toán/số)
python3 NLP-work/verify/verify_all.py

# 2) Sinh lại sơ đồ drawio → SVG (đã strip light-dark())
python3 NLP-work/build/gen_diagrams.py

# 3) Sinh site (chọn module): m0 m1 m2 m3 home kc code dev
python3 NLP-work/build/gen_site.py m0 m1 m2 m3 home kc code dev

# 4) Sinh bài tập lập trình + notebook
python3 NLP-work/code/exercises/build_exercises.py
python3 NLP-work/code/build_notebook.py

# 5) Kiểm thử
python3 -m pytest -q NLP-work/code/exercises/test_reference.py
(cd for-Vinh && python3 -m http.server 8765 &)
node NLP-work/tests/site_test.js http://localhost:8765/non-linear-programming/ modules/01-tap-loi-ham-loi/index.html code/index.html

# 6) Deploy (đẩy từng phần nhỏ)
cd for-Vinh && git add -A non-linear-programming && git commit -m "..." && git push
gh api repos/TatcataiTTN/for-Vinh/pages/builds/latest -q .status    # đợi "built"
```

## 4. Viết nội dung một module

Mỗi module gồm 2 file trong `NLP-work/build/`:

- `c_mK.py` — nội dung: hằng `LEAD`, `META`, `OBJECTIVES`, danh sách `DECK` (các slide dựng bằng `sl()`, `part()`), danh sách `SECTIONS` (công thức, lịch sử, case study, ví dụ, sơ đồ, công cụ tương tác, bẫy), chuỗi `READING`.
- `q_mK.py` — ngân hàng câu hỏi (mục 5).

Hàm dựng HTML (trong `helpers.py`): `sl(title, body, kicker, img, explain)`, `part(...)`, `formula(label, tex, legend)`, `callout(kind, title, body)`, `steps([...])`, `solution(summary, body)`, `table(headers, rows)`, `fig(name, caption)`, `widget(kind)`.

**Quy ước quan trọng**
- Toán dùng KaTeX với `\( ... \)` và `\[ ... \]` (không dùng `$`). Trong chuỗi Python dùng **raw string** `r'...'` hoặc nhân đôi dấu `\\`.
- Trong f-string, ngoặc nhọn LaTeX phải nhân đôi: `\\{{4,5\\}}`.
- Ký tự `<`/`>` nằm trong công thức được `fixmath()` tự đổi thành `\lt`/`\gt` (nếu không, trình duyệt hiểu `<m` là thẻ HTML).
- Số trang slide gốc: `img='m2:55'` (module:trang) → script cắt ảnh bằng `pdftoppm` 150 dpi vào `assets/slides/`.
- Không dùng dấu `''` (hai nháy đơn) trong raw string `r'...'`: dùng `f^{\prime\prime}`.

## 5. Ngân hàng câu hỏi (`qlib.py`)

```python
bank = Bank('m2')
mc(src, ref, q, correct, wrong[3], explain, group)     # trắc nghiệm (đáp án đúng và 3 nhiễu tách riêng)
tf(src, ref, q, truth, explain, group)                  # đúng/sai
num(src, ref, q, ans, explain, tol, ans_text, group)    # điền số, chấm có dung sai
essay(src, ref, q, model, check[], group)               # tự luận + đáp án mẫu + checklist tự chấm
bank.fix(prefix_của_câu, correct, wrong)                # chỉnh đáp án để cân bằng độ dài
```

`src`: `G` từ nội dung slide · `B` bài tập/ví dụ của slide · `T` tham khảo (Studocu/BTDOC) · `S` biên soạn thêm.

`finalize()` xáo đáp án bằng seed cố định (thử 400 seed, chọn seed cho phân bố vị trí đúng nhất) và **audit thiên lệch**:
- vị trí đáp án đúng (A/B/C/D) — mục tiêu mỗi vị trí ≈ 25%;
- `correct_obviously_longest`: đáp án đúng dài ≥ 1,2× và hơn ≥ 8 ký tự so với mọi nhiễu — mục tiêu < 10%; `finalize` tự rút gọn phần giải thích trong ngoặc/sau “vì”, phần còn lại sửa bằng `bank.fix`;
- tỉ lệ đúng/sai — mục tiêu 45–55%.
Báo cáo ghi ở `NLP-work/verify/quiz_report_mK.json`.

## 6. Kiểm chứng số liệu (`verify/verify_all.py`)

Mỗi mục là một phép tính độc lập (sympy cho đạo hàm/giải hệ, scipy cho `linprog`/`minimize`, brute-force cho bài nhỏ). Khi thấy slide mâu thuẫn với kết quả, ghi vào khóa `errata_*` và hiển thị ở trang `kiem-chung/`. **Không** sửa số cho khớp slide.

## 7. Bài tập lập trình (trang `code/`)

### 7.1 Cách chạy code trên GitHub Pages
GitHub Pages **chỉ phục vụ file tĩnh** — không có máy chủ để biên dịch/chạy code. Giải pháp đang dùng:

| Nhu cầu | Giải pháp | Giới hạn |
|---|---|---|
| Chạy Python ngay trên trang, có chấm tự động | **Pyodide** (CPython biên dịch ra WebAssembly) trong Web Worker; thư viện `numpy`, `sympy` (có `scipy`) | tải ~10–25 MB lần đầu từ CDN jsDelivr; **không có `cvxpy`** |
| Chạy `cvxpy` đầy đủ | **Google Colab** mở thẳng notebook trong repo | cần tài khoản Google |
| Kiểm tra tự động mỗi lần push | **GitHub Actions** (`.github/workflows/nlp-verify.yml`) chạy pytest + sinh lại số liệu | chỉ kiểm, không phục vụ trang |
| Chạy trên máy | `python3 code/scripts/*.py` | cần cài Python |

### 7.2 Thêm một bài mới
1. Viết hàm mẫu có docstring **đầu vào/đầu ra/kiểu dữ liệu** trong `code/exercises/reference.py` (chỉ dùng numpy/sympy).
2. Thêm mục vào danh sách `EX` trong `build_exercises.py`: `id, fn, module, level, title, statement, inp, out, hint, starter, tests`. Mỗi test: `{args:[...], visible:bool, note}`. **Đáp án kỳ vọng không gõ tay**: `build_exercises.py` gọi chính `reference.py`.
3. Thêm test độc lập đối chiếu (scipy/brute-force) vào `test_reference.py`.
4. `python3 build_exercises.py && python3 gen_site.py code`.

### 7.3 Cách chấm (`pyworker.js`)
- Worker nạp Pyodide, `exec` mã người học, gọi `fn(*args)` với **bản sao sâu** của đầu vào.
- Kết quả được chuẩn hóa (numpy → list/float) rồi so sánh đệ quy: số với dung sai tương đối 1e-6, chuỗi/bool/None/int phải khớp tuyệt đối, dict chỉ so các khóa có trong đáp án kỳ vọng.
- Quá 45 giây: `worker.terminate()` và tạo lại (chống vòng lặp vô hạn).
- Test “ẩn” vẫn nằm trong JSON của trang (người rành có thể xem): phù hợp tự học, **không** dùng để thi.

## 8. Kiểm thử

| Tầng | Công cụ | Nội dung |
|---|---|---|
| Số liệu | `verify_all.py`, `test_reference.py` | đối chiếu hai cách tính độc lập |
| Trang | `tests/site_test.js` | số slide, lỗi KaTeX, widget có canvas, slide tràn, ảnh vỡ, quiz (bấm đáp án → có giải thích → nút làm lại) |
| Widget | `tests/widgets_test.js` | active set duyệt từng bước, QP đẳng thức, KKT lab trên mọi điểm gợi ý |
| Bài code | `tests/code_test.js` | nạp Pyodide trong Chrome thật, chạy lời giải mẫu qua trình chấm và xác nhận mọi test ĐẠT; chạy mã sai/để trống xác nhận SAI |
| Production | cùng các script, `base = https://tatcataittn.github.io/for-Vinh/non-linear-programming/` | lặp lại sau mỗi lần deploy |

## 9. Bản sao mã nguồn trong repo (`dev/`)
Để người khác có thể sinh lại site từ repo, `NLP-work/sync_dev.sh` sao chép `build/`, `verify/` (không kèm `results.json` cache lớn), `code/`, `tests/`, `docs/` vào `for-Vinh/non-linear-programming/dev/`. **Nguồn sự thật là `NLP-work/`**; `dev/` chỉ là ảnh chụp (snapshot) — luôn chạy `sync_dev.sh` trước khi commit.

## 10. Lỗi đã gặp và cách tránh

| Lỗi | Nguyên nhân | Cách tránh |
|---|---|---|
| Công thức hiện nguyên `\(...\)` | `<m` trong công thức bị hiểu là thẻ HTML | `fixmath()` trong `helpers.py` |
| Slide “tràn” khi đo bằng test | ảnh `loading=lazy` chưa tải khi đo | `deck.js` chạy lại `fit()` khi ảnh tải xong (sự kiện `load`) |
| GitHub Pages không phục vụ thư mục `_*` | Jekyll bỏ qua | không dùng tên thư mục bắt đầu bằng `_` |
| SVG drawio đổi màu theo hệ điều hành | `light-dark()` nhúng sẵn | `gen_diagrams.py` strip sau khi xuất |
| Câu hỏi bị lệch đáp án | người soạn hay đặt đáp án đúng dài/ở vị trí A | `qlib.finalize` + audit |
| Slide ghi số không khớp tính toán | lỗi chép trong slide | ghi `errata_*`, hiển thị ở `kiem-chung/` |
| Cache GitHub Pages ~10 phút | `Cache-Control: max-age=600` | hard refresh hoặc `?v=2` |
