# ĐỀ MẪU SỐ 03 — Cơ sở dữ liệu

**Đề thi gồm 30 câu; 4 trang** · **Thời gian làm bài: 90 phút** · Đề thi KHÔNG ĐƯỢC sử dụng tài liệu

Họ và tên sinh viên: ........................................ Số báo danh: ....................

---

## Phần 1: Trắc nghiệm (7 điểm, gồm 28 câu, mỗi câu trả lời đúng được 0.25 điểm)

### Phần 1.A – Truy vấn SQL (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 1.** Tìm khách hàng đã được gán nhân viên đại diện chăm sóc (salesRepEmployeeNumber khác NULL).
A. SELECT * FROM customers WHERE salesRepEmployeeNumber <> NULL;
B. SELECT * FROM customers WHERE salesRepEmployeeNumber IS NOT NULL;
C. SELECT * FROM customers WHERE NOT salesRepEmployeeNumber IS NULL;
D. SELECT * FROM customers WHERE salesRepEmployeeNumber != NULL;

**Câu 2.** Tìm các đơn hàng chưa được vận chuyển (trường shippedDate có giá trị NULL).
A. SELECT * FROM orders WHERE shippedDate IS NULL;
B. SELECT * FROM orders WHERE shippedDate IS EMPTY;
C. SELECT * FROM orders WHERE shippedDate = NULL;
D. SELECT * FROM orders WHERE shippedDate = '';

**Câu 3.** Làm thế nào để lấy danh sách các quốc gia khác nhau của khách hàng (không trùng lặp)?
A. SELECT DISTINCT country FROM customers;
B. Cả A và C đều đúng
C. SELECT UNIQUE country FROM customers;
D. SELECT country FROM customers GROUP BY country;

**Câu 4.** Tìm danh sách các tiểu bang (state) khác nhau của khách hàng sinh sống tại nước Mỹ ('USA').
A. SELECT state FROM customers WHERE country = 'USA' GROUP BY state;
B. Cả A và C đều đúng
C. SELECT DISTINCT state FROM customers WHERE country = 'USA';
D. SELECT UNIQUE state FROM customers WHERE country = 'USA';

**Câu 5.** Đưa ra danh sách các nhóm sản phẩm (productLine) khác nhau hiện có trong bảng products.
A. Cả A và C đều đúng
B. SELECT UNIQUE productLine FROM products;
C. SELECT productLine FROM products GROUP BY productLine;
D. SELECT DISTINCT productLine FROM products;

**Câu 6.** Tìm các trạng thái (status) đơn hàng khác nhau hiện có trong bảng orders.
A. SELECT DISTINCT status FROM orders;
B. Cả A và C đều đúng
C. SELECT status FROM orders GROUP BY status;
D. SELECT UNIQUE status FROM orders;

**Câu 7.** Hiển thị danh sách các mã nhân viên bán hàng (salesRepEmployeeNumber) khác nhau hiện diện trong bảng khách hàng (loại bỏ NULL).
A. Tất cả các đáp án trên đều đúng
B. SELECT DISTINCT salesRepEmployeeNumber FROM customers WHERE salesRepEmployeeNumber IS NOT NULL;
C. SELECT salesRepEmployeeNumber FROM customers WHERE salesRepEmployeeNumber IS NOT NULL GROUP BY salesRepEmployeeNumber;
D. SELECT UNIQUE salesRepEmployeeNumber FROM customers WHERE salesRepEmployeeNumber IS NOT NULL;

**Câu 8.** Làm thế nào để lấy ra thông tin của 10 sản phẩm đầu tiên trong hệ thống?
A. SELECT * FROM products FETCH FIRST 10 ROWS ONLY;
B. SELECT * FROM products LIMIT 10;
C. SELECT * FROM products WHERE ROWNUM <= 10;
D. SELECT * FROM products TOP 10;

**Câu 9.** Lấy ra thông tin của 5 đơn đặt hàng đầu tiên trong bảng `orders`.
A. SELECT * FROM orders WHERE ROWNUM <= 5;
B. SELECT * FROM orders LIMIT 5;
C. SELECT * FROM orders FETCH FIRST 5 ROWS ONLY;
D. SELECT * FROM orders TOP 5;

**Câu 10.** Viết câu lệnh để lấy thông tin khách hàng từ vị trí thứ 11 đến vị trí thứ 15 (lấy 5 bản ghi).
A. SELECT * FROM customers LIMIT 5, 10;
B. SELECT * FROM customers LIMIT 10, 5;
C. Cả A và B đều đúng
D. SELECT * FROM customers LIMIT 5 OFFSET 10;

**Câu 11.** Lấy ra thông tin của 3 nhân viên đầu tiên có chức vụ công việc là 'Sales Rep'.
A. SELECT * FROM employees WHERE jobTitle = 'Sales Rep' AND ROWNUM <= 3;
B. SELECT * FROM employees WHERE jobTitle = 'Sales Rep' TOP 3;
C. SELECT * FROM employees WHERE jobTitle = 'Sales Rep' LIMIT 3;
D. SELECT * FROM employees WHERE jobTitle = 'Sales Rep' FETCH FIRST 3 ROWS ONLY;

**Câu 12.** Đưa ra danh sách thông tin của 8 sản phẩm đầu tiên thuộc nhóm sản phẩm 'Motorcycles'.
A. SELECT * FROM products WHERE productLine = 'Motorcycles' FETCH FIRST 8 ROWS ONLY;
B. SELECT * FROM products WHERE productLine = 'Motorcycles' LIMIT 8;
C. SELECT * FROM products WHERE productLine = 'Motorcycles' AND ROWNUM <= 8;
D. SELECT * FROM products WHERE productLine = 'Motorcycles' TOP 8;

**Câu 13.** Dùng toán tử IN để tìm các khách hàng ở các quốc gia 'USA', 'France', 'Canada'.
A. Cả A và B đều đúng
B. SELECT * FROM customers WHERE country ALL ('USA', 'France', 'Canada');
C. SELECT * FROM customers WHERE country IN ('USA', 'France', 'Canada');
D. SELECT * FROM customers WHERE country = 'USA' OR country = 'France' OR country = 'Canada';

**Câu 14.** Tìm khách hàng KHÔNG cư trú ở các thành phố 'Nantes', 'Paris', 'Lyon'.
A. SELECT * FROM customers WHERE city <> 'Nantes' AND city <> 'Paris' AND city <> 'Lyon';
B. Tất cả các đáp án trên đều đúng
C. SELECT * FROM customers WHERE NOT (city = 'Nantes' OR city = 'Paris' OR city = 'Lyon');
D. SELECT * FROM customers WHERE city NOT IN ('Nantes', 'Paris', 'Lyon');

### Phần 1.B – Suy diễn, bao đóng, khóa, chuẩn hóa (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 15.** Phép kết nối bằng (Equi-join) là trường hợp đặc biệt của phép toán nào?
A. Cross Join
B. Theta Join (với điều kiện là dấu bằng =)
C. Natural Join
D. Outer Join

**Câu 16.** Trong SQL, phép Left Outer Join sẽ trả về kết quả như thế nào?
A. Chỉ những bản ghi khớp nhau ở cả hai bảng.
B. Tất cả bản ghi của cả hai bảng.
C. Tất cả bản ghi của bảng bên phải, các cột bên trái điền NULL nếu không khớp.
D. Tất cả bản ghi của bảng bên trái, các cột bên phải điền NULL nếu không có dữ liệu khớp.

**Câu 17.** Phép Right Outer Join sẽ giữ lại những bản ghi nào?
A. Tất cả bản ghi bảng bên phải.
B. Tất cả bản ghi bảng bên trái.
C. Chỉ bản ghi trùng nhau.
D. Không giữ lại bản ghi nào.

**Câu 18.** Phép Full Outer Join mang lại kết quả tương đương với việc thực hiện những phép toán nào kết hợp lại?
A. Inner Join và Cross Join
B. Left Outer Join UNION Right Outer Join
C. Left Outer Join INTERSECT Right Outer Join
D. Chỉ Inner Join

**Câu 19.** Trong câu lệnh SELECT, từ khóa DISTINCT được sử dụng để làm gì?
A. Loại bỏ các dòng có giá trị trùng lặp trong tập kết quả.
B. Đếm số dòng.
C. Sắp xếp dữ liệu.
D. Giới hạn số dòng trả về.

**Câu 20.** Mệnh đề GROUP BY trong SQL dùng để làm gì?
A. Lọc các dòng trước khi truy vấn.
B. Sắp xếp kết quả.
C. Nhóm các dòng có cùng giá trị ở một hoặc nhiều cột để sử dụng với hàm tập hợp.
D. Gộp các bảng lại với nhau.

**Câu 21.** Sự khác biệt cơ bản giữa mệnh đề HAVING và mệnh đề WHERE là gì?
A. WHERE lọc dữ liệu sau khi nhóm.
B. HAVING dùng cho chuỗi, WHERE dùng cho số.
C. Không có sự khác biệt, dùng thay thế nhau được.
D. HAVING lọc dữ liệu sau khi đã nhóm (GROUP BY), còn WHERE lọc trước khi nhóm.

**Câu 22.** Khi ánh xạ một cấu trúc phân cấp (Superclass/Subclass) thành một bảng duy nhất (Single Table) cho toàn bộ, ta bắt buộc phải thêm một cột để làm gì?
A. Làm thuộc tính phân loại (Discriminator attribute) để phân biệt các Subclass.
B. Để tính toán chi phí.
C. Để đếm số lượng bản ghi.
D. Làm khóa chính.

**Câu 23.** Nhược điểm lớn nhất của việc ánh xạ toàn bộ mô hình Superclass/Subclass thành một bảng duy nhất là gì?
A. Bị mất dữ liệu chung.
B. Bảng có quá ít cột.
C. Khó truy vấn.
D. Có thể tạo ra rất nhiều giá trị NULL ở các cột dành riêng cho từng subclass.

**Câu 24.** Nếu chọn cách tạo bảng riêng cho từng Subclass, khóa chính của các bảng Subclass sẽ là gì?
A. Tất cả các thuộc tính của Subclass.
B. Chính là khóa chính của bảng Superclass.
C. Khóa ngoại trỏ đến bảng khác.
D. Tự động sinh ra ID mới.

**Câu 25.** Khóa chính của bảng tạo ra từ một thuộc tính đa trị của một thực thể mạnh gồm những gì?
A. Chỉ là giá trị của thuộc tính đa trị.
B. Một trường ID tự động tăng.
C. Chỉ là khóa chính của bảng gốc.
D. Khóa chính của thực thể mạnh và bản thân giá trị của thuộc tính đa trị đó.

**Câu 26.** Khẳng định nào sau đây là ĐÚNG về việc chuyển đổi mối quan hệ từ ER sang bảng?
A. Tất cả các mối quan hệ đều bị xóa đi.
B. Mọi mối quan hệ đều phải tạo ra bảng mới.
C. Quan hệ 1:N và 1:1 thường không cần tạo bảng mới, chỉ cần dùng khóa ngoại.
D. Quan hệ N:M không cần tạo bảng mới.

**Câu 27.** Mối quan hệ ISA trong mô hình thực thể liên kết mở rộng (EER) đại diện cho khái niệm nào?
A. Tính đa hình.
B. Tính đóng gói.
C. Tính kế thừa / phân lớp cha - con.
D. Tính liên kết.

**Câu 28.** Việc ánh xạ mối quan hệ n-ary (n > 2) luôn luôn dẫn đến kết quả nào?
A. Việc tạo ra một quan hệ (bảng) mới để thể hiện mối quan hệ đó.
B. Việc xóa bớt 1 thực thể.
C. Việc thêm khóa ngoại vào 1 bảng hiện có.
D. Không thể thực hiện được trong SQL.

---

## Phần 2: Tự luận (3 điểm)

### Câu 1. (2 điểm) Thiết kế Mô hình quản lý Phòng Khám

Một phòng khám có nhiều bác sĩ làm việc; mỗi bác sĩ chỉ làm việc cố định tại một phòng khám. Một bác sĩ khám cho nhiều bệnh nhân, một bệnh nhân có thể được nhiều bác sĩ khác nhau khám qua các lượt khác nhau. Thiết kế mô hình chỉ với 3 đối tượng chính:

Phòng Khám: Mã Phòng Khám, Tên Phòng Khám
Bác Sĩ: Mã Bác Sĩ, Tên Bác Sĩ
Bệnh Nhân: Mã Bệnh Nhân, Tên Bệnh Nhân

Yêu cầu xây dựng mô hình cơ sở dữ liệu:
a) Mô hình thực thể liên kết (1 điểm)
b) Mô hình quan hệ từ mô hình thực thể liên kết (1 điểm)

### Câu 2. (1 điểm) So sánh hai cách tạo bảng tạm từ SELECT

Cho hai câu lệnh sau, cùng chạy trên CSDL phòng khám:

Câu lệnh 1: `CREATE TABLE Temp_BenhNhanA AS SELECT * FROM BenhNhan WHERE MaPK = 'PK01';`
Câu lệnh 2: `CREATE TABLE Temp_BenhNhanB LIKE BenhNhan;`

Hai bảng Temp_BenhNhanA và Temp_BenhNhanB giống và khác nhau ở điểm nào? (Xét cả cấu trúc cột lẫn dữ liệu bên trong, và ràng buộc như khóa chính nếu có).

---

## ĐÁP ÁN

### Phần 1 — Đáp án trắc nghiệm

**1.B** · **2.A** · **3.B** · **4.B** · **5.A** · **6.B** · **7.A** · **8.B** · **9.B** · **10.C** · **11.C** · **12.B** · **13.A** · **14.B** · **15.B** · **16.D** · **17.A** · **18.B** · **19.A** · **20.C** · **21.D** · **22.A** · **23.D** · **24.B** · **25.D** · **26.C** · **27.C** · **28.A**

### Phần 2 — Đáp án tự luận

**Câu 1 — Mô hình quản lý Phòng Khám**

Ba thực thể: PHÒNG KHÁM(Mã Phòng Khám [khóa], Tên Phòng Khám), BÁC SĨ(Mã Bác Sĩ [khóa], Tên Bác Sĩ), BỆNH NHÂN(Mã Bệnh Nhân [khóa], Tên Bệnh Nhân).

Hai mối kết hợp:
- KHÁM giữa BÁC SĨ và BỆNH NHÂN: bản số N-N (một bác sĩ khám nhiều bệnh nhân, một bệnh nhân được nhiều bác sĩ khám qua các lượt khác nhau).
- LÀM VIỆC TẠI giữa PHÒNG KHÁM và BÁC SĨ: bản số 1-N (một phòng khám có nhiều bác sĩ làm việc, nhưng mỗi bác sĩ chỉ thuộc một phòng khám cố định — phía PHÒNG KHÁM là 1, phía BÁC SĨ là N).

Mô hình quan hệ (4 bảng):
- PhongKham(MaPK [PK], TenPK)
- BenhNhan(MaBN [PK], TenBN)
- BacSi(MaBS [PK], TenBS, MaPK [FK→PhongKham]) — quan hệ LÀM VIỆC TẠI là 1-N nên khóa ngoại MaPK nằm ngay trong bảng BacSi, không tạo bảng riêng.
- Kham(MaBS [PK, FK→BacSi], MaBN [PK, FK→BenhNhan]) — bảng trung gian bắt buộc vì quan hệ KHÁM là N-N, khóa chính là cặp (MaBS, MaBN).

Thang điểm chi tiết (2 điểm):
- Đầy đủ 3 thực thể + đúng thuộc tính + khóa chính (0.5 điểm)
- Xác định đúng 2 mối kết hợp và đúng bản số N-N / 1-N (0.5 điểm)
- Chuyển đúng bảng Kham (N-N → bảng trung gian) (0.5 điểm)
- Chuyển đúng khóa ngoại MaPK trong bảng BacSi (1-N → không tách bảng) (0.5 điểm)

**Câu 2 — So sánh hai cách tạo bảng tạm từ SELECT**

Giống nhau: cả hai đều tạo bảng mới có cùng danh sách cột (tên và kiểu dữ liệu cơ bản) với bảng BenhNhan.

Khác nhau:
1. Dữ liệu: Temp_BenhNhanA (AS SELECT) tạo bảng VÀ chèn ngay dữ liệu là kết quả của SELECT (chỉ bệnh nhân thuộc phòng khám PK01). Temp_BenhNhanB (LIKE) chỉ sao chép cấu trúc, hoàn toàn RỖNG, không có dòng dữ liệu nào.
2. Ràng buộc: AS SELECT KHÔNG sao chép khóa chính, khóa ngoại, chỉ mục của bảng gốc. LIKE sao chép ĐẦY ĐỦ cấu trúc kể cả khóa chính, chỉ mục, AUTO_INCREMENT (nhưng không sao chép khóa ngoại tham chiếu bảng khác).
3. Vì vậy nếu muốn có bảng tạm rỗng nhưng giữ đúng ràng buộc để insert dữ liệu vào sau, nên dùng LIKE; nếu muốn có ngay một tập con dữ liệu, dùng AS SELECT.

Thang điểm chi tiết (1 điểm):
- Nêu đúng điểm giống (cùng cấu trúc cột cơ bản) (0.2 điểm)
- Nêu đúng khác biệt về dữ liệu (có/không có dữ liệu, lọc WHERE) (0.4 điểm)
- Nêu đúng khác biệt về ràng buộc (PK/index có hay không) (0.4 điểm)
