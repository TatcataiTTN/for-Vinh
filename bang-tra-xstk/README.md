# Học tra bảng XSTK

Site tĩnh dạy cách đọc các bảng phân phối đi kèm đề thi XSTK (FFS703010, Phenikaa): chuẩn tắc A7, A8; Student A9; χ² A10 (Kreyszig, App. 5, trang A101–A104).

- `python3 build/build.py` dựng toàn bộ trang và `assets/data.js` (bảng + 240 câu luyện).
- `build/tables.py`: tính lại từng ô bằng SciPy; `python3 build/tables.py <LN_layout.txt>` đối chiếu 1014 ô với bản in (OCR text layer).
- `assets/app.js`: bảng, tra thử có tô sáng, nội suy, hình chuông, luyện tập; hàm Φ, t, χ² tự cài đặt (kiểm bằng `tests/vectors.json`).
- Kiểm thử: `python3 -m http.server 18434` rồi `node tests/site_test.js` (dùng puppeteer-core của `probstat/tests`).
- Trang: chuan-tac, student, chi-binh-phuong, luyen-tra, de-that (tra bảng cho 10 mã đề HK2.2), in-bang.
