# Tối ưu hóa phi tuyến & lồi (CSE703057, Phenikaa)

Site tĩnh (không backend). Trang: `index.html` → `modules/00..03/` → `kiem-chung/`.
- `shared/`: CSS, KaTeX (vendor), `deck.js` (slide tự co chữ), `quiz.js` (trắc nghiệm/điền số/tự luận, lưu localStorage), `widgets.js` (công cụ tương tác)
- `assets/diagrams/`: sơ đồ drawio xuất SVG; `assets/slides/`: ảnh trang slide gốc
Mã sinh site và script kiểm chứng số liệu nằm ngoài repo, trong thư mục dự án `NLP-work/` (build, verify, tests).

## Thực hành code
- `code/`: script ví dụ (`scripts/`), bài tập cvxpy (`cvxpy_bai_tap/`), notebook Colab (`notebooks/`), dữ liệu bài chấm trên web (`exercises.json`)
- `shared/pyworker.js`, `shared/pyrunner.js`: chạy và chấm Python trong trình duyệt (Pyodide, Web Worker)
- `dev/`: ảnh chụp mã nguồn sinh site; `.github/workflows/nlp-verify.yml` (ở gốc repo): kiểm tra tự động
- Hướng dẫn phát triển: trang `phat-trien/` hoặc `dev/docs/DEVELOPMENT.md`
