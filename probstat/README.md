# Xác suất thống kê · Phenikaa (probstat)

Site tự học tĩnh cho học phần FFS703010: 13 module (slide, ví dụ, widget, ngân hàng câu hỏi), luyện đề, bảng tra.

Dựng lại: `cd build && python3 assemble.py && python3 build_site.py` (cần numpy, scipy). Sơ đồ drawio: `python3 dg_mXX.py` (cần CLI drawio).
Kiểm thử: `cd tests && npm i puppeteer-core && python3 gen_cases.py && node verify_ps.js && node site_test.js http://localhost:PORT/vi/`.
Nguyên tắc: câu gốc ghi nguồn từng câu; đáp án tính bằng chương trình; `build/crosscheck.py` đối chiếu với đáp án chính thức trong tài liệu.
