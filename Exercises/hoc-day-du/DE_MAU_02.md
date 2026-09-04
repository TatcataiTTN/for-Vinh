# ĐỀ MẪU SỐ 02 — Cơ sở dữ liệu

**Đề thi gồm 30 câu; 4 trang** · **Thời gian làm bài: 90 phút** · Đề thi KHÔNG ĐƯỢC sử dụng tài liệu

Họ và tên sinh viên: ........................................ Số báo danh: ....................

---

## Phần 1: Trắc nghiệm (7 điểm, gồm 28 câu, mỗi câu trả lời đúng được 0.25 điểm)

### Phần 1.A – Truy vấn SQL (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 1.** Đưa ra các giao dịch thanh toán được thực hiện sau ngày '2004-11-01'.
A. SELECT * FROM payments WHERE paymentDate >= '2004-11-01';
B. SELECT * FROM payments HAVING paymentDate > '2004-11-01';
C. SELECT * FROM payments WHERE paymentDate AFTER '2004-11-01';
D. SELECT * FROM payments WHERE paymentDate > '2004-11-01';

**Câu 2.** Tìm khách hàng ở Mỹ ('USA') VÀ có hạn mức tín dụng (creditLimit) trên 100,000.
A. SELECT * FROM customers WHERE country = 'USA' OR creditLimit > 100000;
B. SELECT * FROM customers WHERE country = 'USA' AND creditLimit > 100000;
C. SELECT * FROM customers WHERE country = 'USA', creditLimit > 100000;
D. SELECT * FROM customers WHERE country = 'USA' THEN creditLimit > 100000;

**Câu 3.** Tìm nhân viên làm việc tại văn phòng số '1' HOẶC văn phòng số '2'.
A. SELECT * FROM employees WHERE officeCode = '1' OR officeCode = '2';
B. SELECT * FROM employees WHERE officeCode IN ('1', '2');
C. Cả A và C đều đúng
D. SELECT * FROM employees WHERE officeCode = '1' AND officeCode = '2';

**Câu 4.** Tìm các sản phẩm thuộc nhóm sản phẩm 'Classic Cars' có giá mua (buyPrice) trên 90.
A. SELECT * FROM products WHERE productLine = 'Classic Cars' WITH buyPrice > 90;
B. SELECT * FROM products WHERE productLine = 'Classic Cars' HAVING buyPrice > 90;
C. SELECT * FROM products WHERE productLine = 'Classic Cars' OR buyPrice > 90;
D. SELECT * FROM products WHERE productLine = 'Classic Cars' AND buyPrice > 90;

**Câu 5.** Đưa ra danh sách đơn hàng được đặt từ ngày '2005-04-01' đến ngày '2005-04-30'.
A. Cả A và B đều đúng
B. SELECT * FROM orders WHERE orderDate BETWEEN '2005-04-01' AND '2005-04-30';
C. SELECT * FROM orders WHERE orderDate IN ('2005-04-01', '2005-04-30');
D. SELECT * FROM orders WHERE orderDate >= '2005-04-01' AND orderDate <= '2005-04-30';

**Câu 6.** Đưa ra danh sách các khách hàng ở các thành phố 'Nantes', 'Paris' hoặc 'Lyon' của Pháp.
A. Cả A và B đều đúng
B. SELECT * FROM customers WHERE city IN ('Nantes', 'Paris', 'Lyon');
C. SELECT * FROM customers WHERE city = 'Nantes' AND city = 'Paris' AND city = 'Lyon';
D. SELECT * FROM customers WHERE city = 'Nantes' OR city = 'Paris' OR city = 'Lyon';

**Câu 7.** Tìm các sản phẩm được cung cấp bởi nhà cung cấp 'Classic Metal Creations' hoặc 'Exoto Designs'.
A. SELECT * FROM products WHERE productVendor IN ('Classic Metal Creations', 'Exoto Designs');
B. SELECT * FROM products WHERE productVendor = 'Classic Metal Creations' OR productVendor = 'Exoto Designs';
C. SELECT * FROM products WHERE productVendor = 'Classic Metal Creations' AND productVendor = 'Exoto Designs';
D. Cả A và B đều đúng

**Câu 8.** Tìm các đơn hàng có trạng thái là 'On Hold' HOẶC 'Disputed'.
A. SELECT * FROM orders WHERE status = 'On Hold' OR status = 'Disputed';
B. SELECT * FROM orders WHERE status = 'On Hold' AND status = 'Disputed';
C. SELECT * FROM orders WHERE status IN ('On Hold', 'Disputed');
D. Cả A và B đều đúng

**Câu 9.** Tìm khách hàng ở quốc gia 'Canada' có hạn mức tín dụng lớn hơn 50,000.
A. SELECT * FROM customers WHERE country = 'Canada' WITH creditLimit > 50000;
B. SELECT * FROM customers WHERE country = 'Canada' AND creditLimit > 50000;
C. SELECT * FROM customers WHERE country = 'Canada', creditLimit > 50000;
D. SELECT * FROM customers WHERE country = 'Canada' OR creditLimit > 50000;

**Câu 10.** Tìm nhân viên có chức vụ công việc là 'VP Sales' hoặc 'VP Marketing'.
A. SELECT * FROM employees WHERE jobTitle IN ('VP Sales', 'VP Marketing');
B. SELECT * FROM employees WHERE jobTitle = 'VP Sales' OR jobTitle = 'VP Marketing';
C. Cả A và B đều đúng
D. SELECT * FROM employees WHERE jobTitle = 'VP Sales' AND jobTitle = 'VP Marketing';

**Câu 11.** Đưa ra các chi tiết đơn hàng (orderdetails) có số lượng đặt trên 50 VÀ giá mỗi sản phẩm nhỏ hơn 50.
A. SELECT * FROM orderdetails WHERE quantityOrdered > 50 OR priceEach < 50;
B. SELECT * FROM orderdetails WHERE quantityOrdered > 50 WITH priceEach < 50;
C. SELECT * FROM orderdetails WHERE quantityOrdered > 50 AND priceEach < 50;
D. SELECT * FROM orderdetails WHERE quantityOrdered > 50, priceEach < 50;

**Câu 12.** Làm thế nào để lấy danh sách các nhân viên có trường `reportsTo` chưa được xác định?
A. SELECT * FROM employees WHERE reportsTo IS NULL;
B. SELECT * FROM employees WHERE reportsTo = '';
C. SELECT * FROM employees WHERE reportsTo = NULL;
D. SELECT * FROM employees WHERE reportsTo IS EMPTY;

**Câu 13.** Đưa ra danh sách các khách hàng có tiểu bang (state) chưa xác định.
A. SELECT * FROM customers WHERE state = NULL;
B. SELECT * FROM customers WHERE state IS NULL;
C. SELECT * FROM customers WHERE state IS EMPTY;
D. SELECT * FROM customers WHERE state = '';

**Câu 14.** Đưa ra danh sách các đơn hàng đã được vận chuyển (trường shippedDate khác NULL).
A. SELECT * FROM orders WHERE shippedDate != NULL;
B. SELECT * FROM orders WHERE shippedDate <> NULL;
C. SELECT * FROM orders WHERE NOT shippedDate IS NULL;
D. SELECT * FROM orders WHERE shippedDate IS NOT NULL;

### Phần 1.B – Suy diễn, bao đóng, khóa, chuẩn hóa (3.5 điểm, 14 câu, mỗi câu 0.25 điểm)

**Câu 15.** Phép toán HỢP (UNION) của hai quan hệ R và S yêu cầu điều gì?
A. R và S phải khả hợp (cùng số lượng thuộc tính và kiểu dữ liệu tương ứng).
B. Không yêu cầu gì.
C. R và S phải có ít nhất một thuộc tính chung.
D. R và S phải có cùng khóa chính.

**Câu 16.** Sự khác biệt giữa UNION và UNION ALL là gì?
A. Không có sự khác biệt.
B. UNION ALL nhanh hơn UNION.
C. UNION chỉ dùng cho số, UNION ALL dùng cho chuỗi.
D. UNION loại bỏ các bộ trùng lặp, UNION ALL thì không.

**Câu 17.** Phép toán Tích Đề-các (Cartesian Product) kết hợp quan hệ R (m hàng) và S (n hàng) sẽ tạo ra bao nhiêu hàng?
A. MAX(m, n) hàng
B. m + n hàng
C. m * n hàng
D. m - n hàng

**Câu 18.** Phép trừ (Difference) giữa hai quan hệ R và S (Ký hiệu: R - S) trả về kết quả gì?
A. Tất cả các bộ của R và S.
B. Các bộ thuộc cả R và S.
C. Các bộ thuộc R nhưng không thuộc S.
D. Các bộ thuộc S nhưng không thuộc R.

**Câu 19.** Phép giao (Intersection) của hai quan hệ R và S trả về kết quả gì?
A. Các bộ có giá trị NULL.
B. Các bộ vừa thuộc R vừa thuộc S.
C. Tất cả các bộ.
D. Các bộ thuộc R nhưng không thuộc S.

**Câu 20.** Yêu cầu bắt buộc để hai quan hệ có thể thực hiện phép Hợp (Union), Giao (Intersect) và Trừ (Difference) là gì?
A. Chúng phải có cùng số dòng.
B. Khóa chính phải giống nhau.
C. Chúng phải có cùng tên.
D. Chúng phải khả hợp (union-compatible).

**Câu 21.** Phép kết nối Theta (Theta Join) kết hợp hai quan hệ dựa trên điều kiện gì?
A. Chỉ điều kiện bằng (=).
B. Một điều kiện so sánh bất kỳ (như =, <, >, <=, >=, <>).
C. Điều kiện cùng tên cột.
D. Điều kiện khóa chính - khóa ngoại.

**Câu 22.** Khóa chính của bảng được tạo ra từ một thực thể yếu (Weak Entity) bao gồm những thành phần nào?
A. Khóa chính của thực thể chủ kết hợp với khóa cục bộ của thực thể yếu.
B. Khóa cục bộ của nó.
C. Một ID tự tăng.
D. Khóa chính của thực thể chủ.

**Câu 23.** Thuộc tính dẫn xuất (Derived attribute) trong sơ đồ ER khi chuyển sang lược đồ quan hệ sẽ được xử lý như thế nào?
A. Luôn được lưu thành cột bắt buộc.
B. Trở thành khóa chính.
C. Tạo thành một bảng mới.
D. Thường không được lưu trữ vật lý thành cột, mà sẽ được tính toán qua câu truy vấn (View/SQL).

**Câu 24.** Khi chuyển đổi một mối quan hệ bậc 3 (Ternary), thông thường ta sẽ tạo ra điều gì?
A. Không tạo gì cả.
B. Ba bảng mới.
C. Thêm cột vào 1 trong 3 thực thể.
D. Một bảng mới chứa 3 khóa ngoại tham chiếu đến 3 thực thể tham gia.

**Câu 25.** Khóa chính của một bảng sinh ra từ mối quan hệ Nhiều-Nhiều (M:N) thường là gì?
A. Không có khóa chính.
B. Một cột ID tự sinh mới hoàn toàn.
C. Sự kết hợp của tất cả các khóa ngoại tham chiếu đến các bảng tham gia.
D. Khóa của một trong hai bảng tham gia.

**Câu 26.** Nếu một thực thể có thuộc tính đa trị, theo nguyên tắc chuẩn, ta phải làm gì?
A. Dùng kiểu dữ liệu mảng (nếu RDBMS không hỗ trợ thì gộp chuỗi).
B. Ghi vào một file log.
C. Bỏ qua thuộc tính đa trị.
D. Tạo một bảng mới chứa khóa chính của thực thể và thuộc tính đa trị đó.

**Câu 27.** Trong quan hệ 1:N giữa PHONGBAN (1) và NHANVIEN (N), khóa ngoại sẽ được đặt ở bảng nào?
A. Bảng trung gian
B. Không có khóa ngoại
C. NHANVIEN
D. PHONGBAN

**Câu 28.** Trong trường hợp cả hai thực thể trong quan hệ 1:1 đều có sự tham gia toàn phần (Total Participation), cách tối ưu nhất thường là gì?
A. Gộp chung cả hai thực thể vào một bảng duy nhất.
B. Bỏ qua mối quan hệ này.
C. Giữ nguyên 2 bảng và đặt khóa ngoại ở 2 bên.
D. Tạo 3 bảng.

---

## Phần 2: Tự luận (3 điểm)

### Câu 1. (2 điểm) Thiết kế Mô hình quản lý Thư Viện

Một thư viện có nhiều độc giả. Một độc giả mượn nhiều sách khác nhau, một sách có thể được nhiều độc giả mượn qua các lượt khác nhau. Mỗi sách do đúng một nhà xuất bản phát hành; một nhà xuất bản phát hành nhiều sách. Thiết kế mô hình chỉ với 3 đối tượng chính:

Độc Giả: Mã Độc Giả, Tên Độc Giả
Sách: Mã Sách, Tên Sách
Nhà Xuất Bản: Mã NXB, Tên NXB

Yêu cầu xây dựng mô hình cơ sở dữ liệu:
a) Mô hình thực thể liên kết (1 điểm)
b) Mô hình quan hệ từ mô hình thực thể liên kết (1 điểm)

### Câu 2. (1 điểm) Trigger kiểm tra số sách mượn tối đa

Cho một TRIGGER được khởi tạo như sau trên bảng Muon (MaDG, MaSach, NgayMuon), giả sử độc giả 'DG001' hiện đang mượn 4 cuốn sách chưa trả:

```sql
DELIMITER //
CREATE TRIGGER Muon_GioiHan BEFORE INSERT
ON Muon
FOR EACH ROW
BEGIN
  DECLARE v_soluong INT;
  SELECT COUNT(*) INTO v_soluong FROM Muon WHERE MaDG = NEW.MaDG;
  IF v_soluong >= 5 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Da muon toi da 5 cuon sach, khong the muon them.';
  END IF;
END //
DELIMITER ;
```

Điều gì xảy ra khi độc giả 'DG001' (đang mượn 4 cuốn) thực hiện mượn thêm 1 cuốn sách nữa? Và điều gì xảy ra nếu độc giả này tiếp tục mượn thêm 1 cuốn nữa sau đó (lúc này đã có 5 cuốn)? Giải thích.

---

## ĐÁP ÁN

### Phần 1 — Đáp án trắc nghiệm

**1.D** · **2.B** · **3.C** · **4.D** · **5.A** · **6.A** · **7.D** · **8.D** · **9.B** · **10.C** · **11.C** · **12.A** · **13.B** · **14.D** · **15.A** · **16.D** · **17.C** · **18.C** · **19.B** · **20.D** · **21.B** · **22.A** · **23.D** · **24.D** · **25.C** · **26.D** · **27.C** · **28.A**

### Phần 2 — Đáp án tự luận

**Câu 1 — Mô hình quản lý Thư Viện**

Ba thực thể: ĐỘC GIẢ(Mã Độc Giả [khóa], Tên Độc Giả), SÁCH(Mã Sách [khóa], Tên Sách), NHÀ XUẤT BẢN(Mã NXB [khóa], Tên NXB).

Hai mối kết hợp:
- MƯỢN giữa ĐỘC GIẢ và SÁCH: bản số N-N (một độc giả mượn nhiều sách, một sách được nhiều độc giả mượn qua các lượt khác nhau).
- XUẤT BẢN giữa NHÀ XUẤT BẢN và SÁCH: bản số 1-N (một nhà xuất bản phát hành nhiều sách, nhưng mỗi sách chỉ do một nhà xuất bản phát hành — phía NHÀ XUẤT BẢN là 1, phía SÁCH là N).

Mô hình quan hệ (4 bảng):
- DocGia(MaDG [PK], TenDG)
- NhaXuatBan(MaNXB [PK], TenNXB)
- Sach(MaSach [PK], TenSach, MaNXB [FK→NhaXuatBan]) — quan hệ XUẤT BẢN là 1-N nên khóa ngoại MaNXB nằm ngay trong bảng Sach, không tạo bảng riêng.
- Muon(MaDG [PK, FK→DocGia], MaSach [PK, FK→Sach]) — bảng trung gian bắt buộc vì quan hệ MƯỢN là N-N, khóa chính là cặp (MaDG, MaSach).

Thang điểm chi tiết (2 điểm):
- Đầy đủ 3 thực thể + đúng thuộc tính + khóa chính (0.5 điểm)
- Xác định đúng 2 mối kết hợp và đúng bản số N-N / 1-N (0.5 điểm)
- Chuyển đúng bảng Muon (N-N → bảng trung gian) (0.5 điểm)
- Chuyển đúng khóa ngoại MaNXB trong bảng Sach (1-N → không tách bảng) (0.5 điểm)

**Câu 2 — Trigger kiểm tra số sách mượn tối đa**

Lần mượn thứ 5 (khi đang có 4 cuốn): trước khi INSERT, trigger đếm v_soluong = 4 (số dòng hiện có của MaDG='DG001' trong bảng Muon). Vì 4 không lớn hơn hoặc bằng 5, điều kiện IF sai, INSERT được thực hiện thành công, độc giả này giờ có 5 cuốn.

Lần mượn thứ 6 (khi đang có 5 cuốn): trigger đếm lại v_soluong = 5. Vì 5 >= 5, điều kiện IF đúng, trigger phát tín hiệu lỗi SQLSTATE 45000, INSERT bị hủy, độc giả không mượn thêm được cuốn thứ 6.

Lưu ý: trigger đếm số dòng TRƯỚC khi dòng mới được thêm (NEW chưa được ghi vào bảng tại thời điểm BEFORE INSERT), nên điều kiện >= 5 mới đúng là chặn ở lần mượn thứ 6, không phải thứ 5.

Thang điểm chi tiết (1 điểm):
- Lần mượn thứ 5: kết luận đúng thành công, nêu đúng lý do (đếm được 4) (0.4 điểm)
- Lần mượn thứ 6: kết luận đúng bị chặn, nêu đúng lý do (đếm được 5) (0.4 điểm)
- Giải thích đúng thời điểm đếm là TRƯỚC khi dòng mới được ghi (BEFORE INSERT) (0.2 điểm)
