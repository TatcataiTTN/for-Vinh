# ĐỀ MẪU SỐ 01 — Cơ sở dữ liệu

**Đề thi gồm 30 câu; 4 trang** · **Thời gian làm bài: 90 phút** · Đề thi KHÔNG ĐƯỢC sử dụng tài liệu

Họ và tên sinh viên: ........................................ Số báo danh: ....................

---

## Phần 1: Trắc nghiệm (7 điểm, gồm 28 câu, mỗi câu trả lời đúng được 0.25 điểm)

### Phần 1.A – Truy vấn SQL (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 1.** Làm thế nào để lấy tất cả thông tin của các nhân viên trong bảng `employees`?
A. SELECT * FROM employees;
B. SELECT ALL FROM employees;
C. FETCH * FROM employees;
D. GET * FROM employees;

**Câu 2.** Viết câu lệnh để hiển thị `lastName`, `firstName` và `email` của toàn bộ nhân viên.
A. SELECT COLUMNS(lastName, firstName, email) FROM employees;
B. SELECT (lastName, firstName, email) FROM employees;
C. SELECT lastName, firstName, email FROM employees;
D. SHOW lastName, firstName, email FROM employees;

**Câu 3.** Làm thế nào để lấy danh sách các mã văn phòng (officeCode) từ bảng nhân viên?
A. SELECT COLUMN officeCode FROM employees;
B. LIST officeCode FROM employees;
C. SHOW officeCode FROM employees;
D. SELECT officeCode FROM employees;

**Câu 4.** Hiển thị mã khách hàng, tên khách hàng và số điện thoại của tất cả khách hàng.
A. SELECT customerNumber, customerName, phone FROM customers;
B. SELECT customerNumber, customerName, phone FROM clients;
C. LIST customerNumber, customerName, phone FROM customers;
D. SHOW customerNumber, customerName, phone FROM customers;

**Câu 5.** Hiển thị mã sản phẩm, tên sản phẩm và giá bán lẻ đề xuất (MSRP) của tất cả sản phẩm.
A. GET productCode, productName, MSRP FROM products;
B. SELECT productCode, productName, MSRP FROM items;
C. SHOW productCode, productName, MSRP FROM products;
D. SELECT productCode, productName, MSRP FROM products;

**Câu 6.** Làm thế nào để tìm các nhân viên có vị trí công việc (jobTitle) là 'Sales Rep'?
A. SELECT * FROM employees HAVING jobTitle = 'Sales Rep';
B. SELECT * FROM employees WHERE jobTitle = 'Sales Rep';
C. SELECT * FROM employees WHERE jobTitle IS 'Sales Rep';
D. SELECT * FROM employees WITH jobTitle = 'Sales Rep';

**Câu 7.** Làm thế nào để tìm tất cả các khách hàng có quốc gia (country) là 'France'?
A. SELECT * FROM customers WHERE country IS 'France';
B. SELECT * FROM customers FILTER country = 'France';
C. SELECT * FROM customers WHERE country = 'France';
D. SELECT * FROM customers HAVING country = 'France';

**Câu 8.** Tìm các sản phẩm có tỷ lệ xích (productScale) là '1:10'.
A. SELECT * FROM products WHERE productScale IS '1:10';
B. SELECT * FROM products WITH productScale = '1:10';
C. SELECT * FROM products HAVING productScale = '1:10';
D. SELECT * FROM products WHERE productScale = '1:10';

**Câu 9.** Tìm các thanh toán (payments) có số tiền giao dịch (amount) lớn hơn 100,000.
A. SELECT * FROM payments WHERE amount > '100000';
B. SELECT * FROM payments WHERE amount > 100000;
C. SELECT * FROM payments HAVING amount > 100000;
D. SELECT * FROM payments WHERE amount >= 100000;

**Câu 10.** Tìm các khách hàng có hạn mức tín dụng (creditLimit) nhỏ hơn hoặc bằng 20,000.
A. SELECT * FROM customers HAVING creditLimit <= 20000;
B. SELECT * FROM customers WHERE creditLimit <= 20000;
C. SELECT * FROM customers WHERE creditLimit =< 20000;
D. SELECT * FROM customers WHERE creditLimit < 20000;

**Câu 11.** Hiển thị thông tin chi tiết của văn phòng đặt tại thành phố 'San Francisco'.
A. SELECT * FROM offices HAVING city = 'San Francisco';
B. SELECT * FROM offices WHERE city = 'San Francisco';
C. SELECT * FROM offices WITH city = 'San Francisco';
D. SELECT * FROM offices WHERE city IS 'San Francisco';

**Câu 12.** Viết câu lệnh tìm các nhân viên có mã người quản lý trực tiếp (reportsTo) là 1143.
A. SELECT * FROM employees WHERE reportsTo = 1143;
B. SELECT * FROM employees HAVING reportsTo = 1143;
C. SELECT * FROM employees WHERE reportsTo IS 1143;
D. SELECT * FROM employees WITH reportsTo = 1143;

**Câu 13.** Đưa ra danh sách các đơn hàng có trạng thái (status) khác 'Shipped'.
A. SELECT * FROM orders WHERE NOT status = 'Shipped';
B. SELECT * FROM orders WHERE status <> 'Shipped';
C. Tất cả các đáp án trên đều đúng
D. SELECT * FROM orders WHERE status != 'Shipped';

**Câu 14.** Tìm tất cả sản phẩm có số lượng trong kho (quantityInStock) dưới 100 sản phẩm.
A. SELECT * FROM products WHERE quantityInStock < 100;
B. SELECT * FROM products WHERE quantityInStock < '100';
C. SELECT * FROM products WHERE quantityInStock <= 100;
D. SELECT * FROM products HAVING quantityInStock < 100;

### Phần 1.B – Suy diễn, bao đóng, khóa, chuẩn hóa (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 15.** Phép toán nào trong đại số quan hệ được sử dụng để chọn các bộ (hàng) thỏa mãn một điều kiện nhất định?
A. Phép chọn (σ)
B. Phép kết nối (⨝)
C. Phép chiếu (π)
D. Phép hợp (∪)

**Câu 16.** Phép toán nào trong đại số quan hệ được sử dụng để chọn ra các thuộc tính (cột) từ một quan hệ?
A. Phép chọn (σ)
B. Phép chiếu (π)
C. Phép chia (÷)
D. Phép trừ (−)

**Câu 17.** Trong SQL, mệnh đề nào tương ứng với phép chọn (σ) trong đại số quan hệ?
A. SELECT
B. WHERE
C. GROUP BY
D. FROM

**Câu 18.** Trong SQL, mệnh đề nào tương ứng với phép chiếu (π) trong đại số quan hệ?
A. WHERE
B. ORDER BY
C. SELECT
D. FROM

**Câu 19.** Phép kết nối tự nhiên (Natural Join) giữa hai quan hệ R và S dựa trên điều kiện nào?
A. Các thuộc tính có cùng tên và cùng kiểu dữ liệu.
B. Khóa chính của R và khóa ngoại của S.
C. Tất cả các thuộc tính.
D. Không có điều kiện nào.

**Câu 20.** Toán tử LIKE trong SQL được dùng để làm gì?
A. So khớp chuỗi theo một mẫu.
B. So sánh lớn hơn.
C. So sánh bằng.
D. Kiểm tra giá trị NULL.

**Câu 21.** Để sắp xếp kết quả truy vấn theo thứ tự giảm dần, ta dùng từ khóa nào sau ORDER BY?
A. ASC
B. DESC
C. REVERSE
D. DOWN

**Câu 22.** Khi chuyển một thực thể mạnh trong ERD sang mô hình quan hệ, nó sẽ trở thành gì?
A. Một khóa ngoại.
B. Một mối quan hệ.
C. Một bảng (quan hệ).
D. Một thuộc tính.

**Câu 23.** Mối quan hệ 'nhiều-nhiều' (M:N) trong ERD được chuyển sang mô hình quan hệ như thế nào?
A. Thêm khóa chính của một thực thể vào thực thể kia làm khóa ngoại.
B. Tạo một bảng mới cho mối quan hệ đó, với khóa chính là sự kết hợp của các khóa chính từ hai thực thể tham gia.
C. Không thể chuyển đổi.
D. Chỉ cần thêm một thuộc tính vào một trong hai thực thể.

**Câu 24.** Khi chuyển mối quan hệ 1-N, khóa ngoại được đặt ở phía nào?
A. Phía '1' (một)
B. Cả hai phía
C. Phía 'N' (nhiều)
D. Tạo một bảng riêng

**Câu 25.** Một thuộc tính đa trị (ví dụ: 'SoDienThoai' của một nhân viên) được chuyển sang mô hình quan hệ như thế nào?
A. Tạo một bảng mới riêng cho thuộc tính đó, chứa khóa chính của bảng gốc.
B. Bỏ qua thuộc tính đó.
C. Lưu trữ các giá trị trong một cột, cách nhau bởi dấu phẩy.
D. Chỉ lưu giá trị đầu tiên.

**Câu 26.** Khi chuyển đổi một thuộc tính phức hợp sang mô hình quan hệ, phương pháp phổ biến là gì?
A. Tạo bảng mới.
B. Bỏ qua thuộc tính phức hợp đó.
C. Tạo các cột (thuộc tính) riêng lẻ cho từng thành phần của nó, loại bỏ tên thuộc tính phức hợp chung.
D. Gộp tất cả thành 1 chuỗi.

**Câu 27.** Đối với mối quan hệ Một-Một (1:1), khóa ngoại (Foreign Key) nên được đặt ở bảng nào để hạn chế tối đa giá trị NULL?
A. Bảng tham gia bán phần.
B. Phải tạo bảng thứ 3.
C. Bảng nào cũng được.
D. Bảng tham gia toàn phần.

**Câu 28.** Một mối quan hệ đệ quy (Recursive) 1:N được chuyển sang mô hình quan hệ như thế nào?
A. Chỉ cần dùng mảng.
B. Tạo thêm 2 bảng mới.
C. Không thể chuyển được.
D. Thêm một thuộc tính làm khóa ngoại vào chính bảng đó, tham chiếu đến khóa chính của nó.

---

## Phần 2: Tự luận (3 điểm)

### Câu 1. (2 điểm) Thiết kế Mô hình quản lý Gara Ô Tô

Một gara ô tô có nhiều thợ sửa xe. Một thợ sửa nhiều xe khác nhau, một xe có thể được nhiều thợ cùng sửa qua các lần khác nhau. Mỗi xe thuộc quyền sở hữu của đúng một khách hàng; một khách hàng có thể sở hữu nhiều xe. Thiết kế mô hình chỉ với 3 đối tượng chính:

Khách Hàng: Mã Khách Hàng, Tên Khách Hàng
Xe: Mã Xe, Tên Xe (biển số/loại xe)
Thợ Sửa: Mã Thợ Sửa, Tên Thợ Sửa

Yêu cầu xây dựng mô hình cơ sở dữ liệu:
a) Mô hình thực thể liên kết (1 điểm)
b) Mô hình quan hệ từ mô hình thực thể liên kết (1 điểm)

### Câu 2. (1 điểm) Trigger kiểm tra chi phí sửa chữa

Cho một TRIGGER được khởi tạo như sau trên bảng PhieuSuaChua (MaPhieu, MaXe, ChiPhi):

```sql
DELIMITER //
CREATE TRIGGER PhieuSuaChua_HanMuc BEFORE INSERT
ON PhieuSuaChua
FOR EACH ROW
BEGIN
  IF NEW.ChiPhi > 20000000 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Chi phi sua chua vuot han muc cho phep.';
  END IF;
END //
DELIMITER ;
```

Điều gì xảy ra khi thêm một phiếu sửa chữa với ChiPhi là 5.000.000? Và điều gì xảy ra nếu ChiPhi là 25.000.000? Giải thích.

---

## ĐÁP ÁN

### Phần 1 — Đáp án trắc nghiệm

**1.A** · **2.C** · **3.D** · **4.A** · **5.D** · **6.B** · **7.C** · **8.D** · **9.B** · **10.B** · **11.B** · **12.A** · **13.C** · **14.A** · **15.A** · **16.B** · **17.B** · **18.C** · **19.A** · **20.A** · **21.B** · **22.C** · **23.B** · **24.C** · **25.A** · **26.C** · **27.D** · **28.D**

### Phần 2 — Đáp án tự luận

**Câu 1 — Mô hình quản lý Gara Ô Tô**

Ba thực thể: KHÁCH HÀNG(Mã Khách Hàng [khóa], Tên Khách Hàng), XE(Mã Xe [khóa], Tên Xe), THỢ SỬA(Mã Thợ Sửa [khóa], Tên Thợ Sửa).

Hai mối kết hợp:
- SỬA CHỮA giữa THỢ SỬA và XE: bản số N-N (một thợ sửa nhiều xe, một xe được nhiều thợ cùng sửa qua các lần khác nhau).
- SỞ HỮU giữa KHÁCH HÀNG và XE: bản số 1-N (một khách hàng sở hữu nhiều xe, nhưng mỗi xe chỉ thuộc một khách hàng — phía KHÁCH HÀNG là 1, phía XE là N).

Mô hình quan hệ (4 bảng):
- KhachHang(MaKH [PK], TenKH)
- ThoSua(MaTho [PK], TenTho)
- Xe(MaXe [PK], TenXe, MaKH [FK→KhachHang]) — quan hệ SỞ HỮU là 1-N nên khóa ngoại MaKH nằm ngay trong bảng Xe, không tạo bảng riêng.
- SuaChua(MaTho [PK, FK→ThoSua], MaXe [PK, FK→Xe]) — bảng trung gian bắt buộc vì quan hệ SỬA CHỮA là N-N, khóa chính là cặp (MaTho, MaXe).

Thang điểm chi tiết (2 điểm):
- Đầy đủ 3 thực thể + đúng thuộc tính + khóa chính (0.5 điểm)
- Xác định đúng 2 mối kết hợp và đúng bản số N-N / 1-N (0.5 điểm)
- Chuyển đúng bảng SuaChua (N-N → bảng trung gian) (0.5 điểm)
- Chuyển đúng khóa ngoại MaKH trong bảng Xe (1-N → không tách bảng) (0.5 điểm)

**Câu 2 — Trigger kiểm tra chi phí sửa chữa**

Trường hợp ChiPhi = 5.000.000: vì 5.000.000 không lớn hơn 20.000.000, điều kiện IF sai (FALSE), khối SIGNAL không thực thi, câu lệnh INSERT thành công bình thường.

Trường hợp ChiPhi = 25.000.000: vì 25.000.000 > 20.000.000, điều kiện IF đúng, trigger phát tín hiệu lỗi SQLSTATE 45000 với nội dung "Chi phi sua chua vuot han muc cho phep.", câu lệnh INSERT bị hủy bỏ, không có dòng nào được thêm vào bảng PhieuSuaChua.

Thang điểm chi tiết (1 điểm):
- Trường hợp 5.000.000: kết luận đúng insert thành công, nêu đúng lý do (0.5 điểm)
- Trường hợp 25.000.000: kết luận đúng bị chặn, nêu đúng lý do (0.5 điểm)
