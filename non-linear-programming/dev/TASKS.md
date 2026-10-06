# TASKS — site Tối ưu hóa phi tuyến & lồi

Site: https://tatcataittn.github.io/for-Vinh/non-linear-programming/ · repo local: `for-Vinh/` (clone của TatcataiTTN/for-Vinh, thư mục con `non-linear-programming/`)
Mã nguồn sinh site (không nằm trong repo): `NLP-work/build/` · số liệu kiểm chứng: `NLP-work/verify/` · kiểm thử trình duyệt: `NLP-work/tests/`

## Module

| # | Module | Nguồn | Deck | Câu hỏi | Trạng thái |
|---|---|---|---|---|---|
| 0 | Kiến thức tiên quyết | nền + BTDOC (tham khảo) | 30 slide | 156 | 🟢 đã push + kiểm production |
| 1 | Tập lồi & hàm lồi | Slide 1 (54 tr.) | 30 slide | 149 | 🟢 |
| 2 | Ràng buộc & KKT | Slide 2 (68 tr.) | 26 slide | 157 | 🟢 |
| 3 | Quy hoạch toàn phương | Slide 3 (81 tr.) | 40 slide | 185 | 🟢 |

Tổng: 647 câu (trắc nghiệm + đúng/sai + điền số + tự luận). Mỗi câu có nhãn nguồn (từ slide / bài tập của slide / tham khảo / biên soạn thêm).

## Đã làm
- [x] Kiểm chứng số liệu bằng code (`verify_all.py` → `results.json`), phát hiện 11 chỗ slide chưa khớp → trang `kiem-chung/`
- [x] 6 sơ đồ drawio (xuất SVG, đã strip `light-dark()`), 8 công cụ tương tác (Hessian, Jensen, tập lồi, KKT, active set, QP đẳng thức, gradient, LP)
- [x] Audit thiên lệch câu hỏi: vị trí đáp án đúng ~đều 4 vị trí; "đáp án đúng dài hẳn" ≤ 7,4 %; đúng/sai ~45–55 % đúng
- [x] Kiểm thử puppeteer local + production (30 slide/module không tràn, KaTeX không lỗi, quiz + nút làm lại hoạt động)

## Code (đã làm)
- [x] Trang `code/`: bài mẫu từ `tam thoi la vay.docx` (md + ảnh), 3 script ví dụ slide (cvxpy/sympy/numpy) kèm kết quả thật
- [x] 7 bài tập chấm tự động trên web (Pyodide + Web Worker; ĐÚNG/SAI KẾT QUẢ/LỖI CHẠY/QUÁ GIỜ), test puppeteer `tests/code_test.js`
- [x] 4 bài tập cvxpy (pytest + notebook Colab tự chấm), đối chiếu scipy
- [x] GitHub Actions `.github/workflows/nlp-verify.yml`; trang `phat-trien/` + `docs/DEVELOPMENT.md`; `sync_dev.sh` sao mã nguồn vào `dev/`

## Chưa làm / gợi ý
- [ ] Slide chính khóa còn thiếu: tối ưu không ràng buộc (buổi 4), SQP, điểm trong (buổi 7–8) — chưa có slide trong `Slides/`
- [ ] Đa ngôn ngữ (chỉ tiếng Việt), notebook Python đối chiếu, thuyết minh giọng nói
- [ ] Hỏi giảng viên các chỗ trong `kiem-chung/` (Ví dụ 2 slide 2, ví dụ null-space, Bài tập 1, Hệ quả 4…)

## Quy trình cập nhật
1. Sửa nội dung `NLP-work/build/c_m*.py` / `q_m*.py` (số liệu mới → `verify_all.py`).
2. `python3 NLP-work/build/gen_site.py m0 m1 m2 m3 home kc`
3. `node NLP-work/tests/site_test.js http://localhost:8765/non-linear-programming/ modules/...` (server: `python3 -m http.server 8765` trong `for-Vinh/`)
4. `git add/commit/push` trong `for-Vinh/`, đợi `gh api repos/TatcataiTTN/for-Vinh/pages/builds/latest -q .status` = `built`, kiểm production.
