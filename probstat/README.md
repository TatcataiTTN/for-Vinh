# Xác suất thống kê · Phenikaa (probstat)

Site tự học tĩnh cho học phần FFS703010: 13 module (slide, ví dụ, widget, ngân hàng câu hỏi), luyện đề, bảng tra.

Dựng lại: `cd build && python3 assemble.py && python3 build_site.py` (cần numpy, scipy). Sơ đồ drawio: `python3 dg_mXX.py` (cần CLI drawio).
Kiểm thử: `cd tests && npm i puppeteer-core && python3 gen_cases.py && node verify_ps.js && node site_test.js http://localhost:PORT/vi/`.
Nguyên tắc: câu gốc ghi nguồn từng câu; đáp án tính bằng chương trình; `build/crosscheck.py` đối chiếu với đáp án chính thức trong tài liệu.

## Đề thi và ngân hàng câu hỏi (cập nhật 11/2026)
- `vi/kho-de/` (build/kho_de.py): trang tổng hợp mọi bộ đề, phạm vi và lộ trình ôn.
- `vi/de-thi-that-hk22/` (build/real_exam.py, _shared/realexam.js): 10 mã đề giữa kỳ thật HK2.2 2025–2026 + 30 mã mới cùng mẫu; đáp số tính bằng SciPy, chấm tự động; kiểm thử `tests/realexam_test.js`.
- `build/orig_hk22.py`: chuyển câu của đề thật thành câu gốc trong ngân hàng M2–M8 (và tự luận câu 9 ở M8; M9 tự nạp lại).
- `build/ext_more_a.py … ext_more_d.py`: họ câu hỏi bổ sung tham số hóa để mỗi module đạt 300 câu; chạy `python3 build/assemble.py` rồi `python3 build/build_site.py`.
