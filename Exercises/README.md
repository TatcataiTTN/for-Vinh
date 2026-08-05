# Luyện SQL cùng Vinh

Trang web luyện tập SQL tương tác, chấm điểm tự động ngay trong trình duyệt (không cần server, không cần cài đặt gì).

## Cách hoạt động

- Toàn bộ 3 cơ sở dữ liệu mẫu (`data/*.sqlite`) được nạp vào trình duyệt và chạy bằng **sql.js** (SQLite biên dịch sang WebAssembly).
- Học sinh viết câu SQL trong ô soạn thảo (CodeMirror, có tô màu cú pháp), bấm **Nộp bài**.
- Trang chạy câu lệnh đó trên một bản sao sạch của CSDL, so sánh kết quả với đáp án đúng (được tính sẵn trong `data/questions.json`), rồi báo Đúng/Sai.
- Với câu hỏi INSERT/UPDATE/DELETE, sau khi học sinh chạy lệnh, trang chạy thêm một câu kiểm tra (`verifySql`) để xem trạng thái CSDL đã thay đổi đúng như mong đợi chưa.
- Tiến trình làm bài (câu nào đã hoàn thành) được lưu trong `localStorage` của trình duyệt, không lưu lên server.

## Cấu trúc thư mục

```
index.html            Trang chính (single-page app)
css/style.css         Toàn bộ giao diện
js/app.js             Logic chính: routing, chạy SQL, chấm điểm
js/schemas.js         Mô tả cấu trúc bảng của 3 CSDL (hiển thị trong "Xem sơ đồ bảng")
data/*.sqlite         3 cơ sở dữ liệu mẫu (classicmodels, truong_hoc, cua_hang_sach)
data/questions.json   39 câu hỏi kèm đáp án đúng đã tính sẵn
vendor/               sql.js và CodeMirror tải sẵn, chạy offline hoàn toàn
build/                Script Python dùng để SINH RA data/questions.json (không cần khi deploy)
```

## 3 cơ sở dữ liệu luyện tập

1. **Classicmodels** (dữ liệu thật, tiếng Anh) — CSDL bán lẻ xe mô hình, 8 bảng.
2. **Trường Học** (tiếng Việt) — quản lý học sinh, lớp, môn học, điểm số.
3. **Cửa Hàng Sách** (tiếng Việt) — quản lý tác giả, sách, khách hàng, đơn hàng.

Mỗi CSDL có 13 câu hỏi, từ cơ bản (WHERE, LIKE, ORDER BY) đến nâng cao (JOIN, SELF JOIN, GROUP BY/HAVING, Subquery, DML).

## Muốn thêm câu hỏi mới?

1. Mở `build/questions_source.py`, thêm một entry mới vào danh sách `QUESTIONS` (copy một câu có sẵn rồi sửa).
2. Chạy `python3 build/compute_expected.py` — script này sẽ tự chạy `referenceSql` thật trên CSDL để tính đáp án đúng và ghi vào `data/questions.json`. Không tự tay gõ đáp án.
3. Mở lại `index.html` để kiểm tra.

## Chạy thử ở máy local trước khi deploy

```bash
cd for-Vinh-Exercises
python3 -m http.server 8080
# rồi mở http://localhost:8080 trong trình duyệt
```
