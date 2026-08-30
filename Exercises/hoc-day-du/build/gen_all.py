# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from slidegen import (cover_slide, agenda_slide, code_slide, code_two_col_slide,
                       detail_slide, timeline_slide, split_slide, quote_slide,
                       closing_slide, build_deck)

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.dirname(HERE)  # .../hoc-day-du/
HEAD = os.path.join(HERE, "shell_head.html")
FOOT = os.path.join(HERE, "shell_foot.html")

BAI_META = [
    ("Cài Đặt MySQL & Quản Lý CSDL", "Cài đặt MySQL Server, kết nối, tạo và xóa cơ sở dữ liệu đầu tiên"),
    ("Kiểu Dữ Liệu & Định Nghĩa Bảng", "CREATE/ALTER/DROP TABLE, ràng buộc dữ liệu, phân loại lệnh DDL/DML/DCL/TCL"),
    ("Tổng Quan SQL & Truy Vấn Cơ Bản", "Lịch sử SQL, cấu trúc SELECT–FROM–WHERE, toán tử so sánh và logic"),
    ("Truy Vấn Cơ Bản (Phần 2)", "IN, BETWEEN, LIKE, thuộc tính suy diễn, ORDER BY, UNION"),
    ("Hàm Nhóm & Truy Vấn Nhóm", "LIMIT, MIN, MAX, COUNT, SUM, AVG, GROUP BY, HAVING"),
    ("Các Phép Nối Bảng (JOIN)", "INNER JOIN, LEFT JOIN, SELF JOIN, cách dùng alias"),
    ("Truy Vấn Con (Subquery)", "Subquery không tương quan và tương quan, EXISTS, subquery ở SELECT/FROM/WHERE"),
    ("Thêm, Sửa, Xóa Dữ Liệu", "INSERT, UPDATE, DELETE, ràng buộc khóa ngoại khi xóa dữ liệu"),
    ("Ôn Tập Tổng Hợp SQL", "Kết hợp toàn bộ kiến thức: lọc, JOIN, GROUP BY, subquery, UNION"),
    ("Nối Bảng Nâng Cao — 20 Bài Tập", "Luyện tổng hợp INNER JOIN, hàm tổng hợp, và LEFT JOIN"),
]

def deck_path(n):
    return os.path.join(OUT_DIR, f"bai-{n}.html")

# Câu hỏi SQL tương tác khớp chủ đề nhất cho từng bài (id trong data/questions.json,
# đều thuộc CSDL classicmodels để nhất quán với ví dụ trong slide). Bài 1-2 chưa có
# bài tập DDL tương tác nên trỏ về trang chủ luyện tập.
PRACTICE_HREF = {
    1: "../index.html",
    2: "../index.html",
    3: "../index.html#/cm01",
    4: "../index.html#/cm02",
    5: "../index.html#/cm07",
    6: "../index.html#/cm04",
    7: "../index.html#/cm09",
    8: "../index.html#/cm12",
    9: "../index.html#/cm01",
    10: "../index.html#/cm14",
}

def nav_closing(n, extra_sub=""):
    total = len(BAI_META)
    practice_href = PRACTICE_HREF[n]
    if n < total:
        nxt_title = BAI_META[n][0].replace("&", "&")
        return closing_slide(
            f"Hoàn Thành Bài {n}",
            f"Tiếp theo: Bài {n+1} — {nxt_title}. {extra_sub}",
            f"Sang Bài {n+1} →", f"bai-{n+1}.html",
            f'🧪 Luyện tập ngay chủ đề này: <a href="{practice_href}" style="color:inherit;">bấm vào đây</a>'
        )
    else:
        return closing_slide(
            "Hoàn Thành 10 Bài",
            f"Đã học hết lý thuyết. {extra_sub} Giờ vào phần luyện tập để chấm điểm tự động.",
            "Vào Luyện Tập Tương Tác →", "../index.html",
            'Ôn lại từ đầu: <a href="bai-1.html" style="color:inherit;">Bài 1</a> · Xem lại <a href="index.html" style="color:inherit;">mục lục 10 bài</a>'
        )

def cover(n):
    title, sub = BAI_META[n-1]
    return cover_slide(
        "Giáo Trình Điện Tử", [f"Bài {n}", title.replace("&", "&")], sub,
        f"Bài {n} / {len(BAI_META)}", "Cơ Sở Dữ Liệu — Phenikaa"
    )

# ============================================================ BÀI 1
def gen_bai1():
    slides = [
        cover(1),
        agenda_slide("Bài 1", [
            ("Cài đặt MySQL Server", "Tải và cài đặt MySQL Community Server, đặt mật khẩu root."),
            ("Cấu trúc thư mục MySQL", "File cấu hình my.ini/my.cnf và ý nghĩa các thư mục bin, data, share."),
            ("Kết nối tới MySQL Server", "Dùng chương trình khách mysql.exe hoặc MySQL Workbench."),
            ("Tạo và xóa cơ sở dữ liệu", "CREATE DATABASE, SHOW DATABASES, USE, DROP DATABASE."),
        ]),
        code_slide("Bài 1", "Kết Nối MySQL Server", "Đăng nhập bằng chương trình khách dòng lệnh",
            [("Kết nối tới server", "mysql -u root -p\n# Nhập mật khẩu khi được hỏi\n\nSHOW DATABASES;\nUSE classicmodels;\nSHOW TABLES;")],
            explain="Ngầm định, hệ quản trị CSDL có một tài khoản quản trị <b>username là root</b>. Sau khi kết nối, <b>SHOW DATABASES</b> liệt kê toàn bộ CSDL trên server, <b>USE</b> chọn CSDL để làm việc."),
        code_two_col_slide("Bài 1", "Tạo & Xóa Cơ Sở Dữ Liệu", "Hai câu lệnh nền tảng nhất của MySQL",
            ("Tạo CSDL", "CREATE DATABASE\n  [IF NOT EXISTS] classicmodels;"),
            ("Xóa CSDL", "DROP DATABASE\n  [IF EXISTS] classicmodels;"),
            explain="Tùy chọn <b>IF NOT EXISTS</b> / <b>IF EXISTS</b> giúp tránh báo lỗi khi CSDL đã tồn tại hoặc không tồn tại. Xóa CSDL là <b>xóa vĩnh viễn</b> toàn bộ dữ liệu bên trong."),
        detail_slide("Bài 1", "Cấu Trúc Thư Mục MySQL", "Mỗi thư mục cài đặt đảm nhận một vai trò riêng",
            [("bin — chương trình", ["mysqld: chương trình server", "mysql: công cụ khách chạy câu lệnh SQL", "mysqladmin: quản trị (tắt server, xem trạng thái)"]),
             ("data — dữ liệu", ["Nơi MySQL đọc/ghi toàn bộ dữ liệu thật", "Chứa cả các file log của server"])],
            [("scripts & share", ["mysql_install_db: khởi tạo file dữ liệu và tài khoản", "share: SQL script sửa đặc quyền, file ngôn ngữ"]),
             ("Công cụ dòng lệnh khác", ["mysqldump: sao lưu CSDL ra file ngoài", "mysqlimport: nhập dữ liệu vào bảng từ file", "mysqlshow: xem nhanh thông tin CSDL/bảng/cột"])]),
        quote_slide(
            "Người dùng nên tách riêng thư mục làm việc và thư mục lưu trữ dữ liệu so với cài đặt ngầm định để tăng tính bảo mật của hệ thống.",
            "Ghi nhớ khi cấu hình MySQL"),
        nav_closing(1),
    ]
    build_deck(slides, deck_path(1), HEAD, FOOT, "Bài 1 — Cài Đặt MySQL", practice_href=PRACTICE_HREF[1])

# ============================================================ BÀI 2
def gen_bai2():
    slides = [
        cover(2),
        agenda_slide("Bài 2", [
            ("Các kiểu dữ liệu MySQL", "Kiểu số, kiểu chuỗi, kiểu ngày giờ và dung lượng lưu trữ."),
            ("Tạo bảng với CREATE TABLE", "Khai báo cột, kiểu dữ liệu, giá trị ngầm định."),
            ("Ràng buộc dữ liệu", "PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK."),
            ("Sửa và xóa bảng", "ALTER TABLE (ADD/MODIFY/DROP COLUMN), DROP TABLE."),
        ]),
        detail_slide("Bài 2", "Kiểu Dữ Liệu MySQL", "Ba nhóm kiểu dữ liệu thường dùng nhất",
            [("Số (numeric)", ["TINYINT (1 byte), SMALLINT (2 byte)", "INT/INTEGER (4 byte), BIGINT (8 byte)", "FLOAT, DOUBLE, DECIMAL(p,s)"]),
             ("Chuỗi (string)", ["CHAR(n): độ dài cố định", "VARCHAR(n): độ dài thay đổi", "TEXT/BLOB: văn bản hoặc nhị phân lớn"])],
            [("Ngày giờ (datetime)", ["DATE: 'YYYY-MM-DD'", "TIME: 'hh:mm:ss'", "DATETIME: 'YYYY-MM-DD hh:mm:ss'", "TIMESTAMP: tự động cập nhật khi sửa dòng"]),
             ("4 nhóm câu lệnh SQL", ["DDL: CREATE, ALTER, DROP, TRUNCATE, RENAME", "DML: SELECT, INSERT, UPDATE, DELETE", "DCL: GRANT, REVOKE (phân quyền)", "TCL: COMMIT, ROLLBACK, SAVEPOINT"])]),
        code_slide("Bài 2", "CREATE TABLE", "Tạo bảng kèm ràng buộc khóa chính và khóa ngoại",
            [("Khai báo khóa chính mức cột", "CREATE TABLE employees (\n  employeeNumber INT NOT NULL PRIMARY KEY,\n  lastName VARCHAR(50) NOT NULL,\n  officeCode VARCHAR(10) NOT NULL,\n  reportsTo INT DEFAULT NULL,\n  jobTitle VARCHAR(50) NOT NULL\n) ENGINE=InnoDB;"),
             ("Khai báo khóa ngoại có đặt tên", "CREATE TABLE city (\n  city_id SMALLINT NOT NULL AUTO_INCREMENT,\n  country_id SMALLINT NOT NULL,\n  PRIMARY KEY (city_id),\n  CONSTRAINT fk_city_country\n    FOREIGN KEY (country_id)\n    REFERENCES country (country_id)\n    ON DELETE RESTRICT ON UPDATE CASCADE\n);")],
            explain="<b>ON DELETE RESTRICT</b>: không cho xóa dòng cha nếu còn dòng con tham chiếu tới. <b>ON UPDATE CASCADE</b>: sửa khóa ở bảng cha thì bảng con tự cập nhật theo."),
        code_two_col_slide("Bài 2", "ALTER TABLE & DROP TABLE", "Sửa cấu trúc bảng đã tồn tại",
            ("Thêm / sửa / xóa cột", "ALTER TABLE employees\n  ADD salary INT(10) NOT NULL;\n\nALTER TABLE employees\n  MODIFY salary DECIMAL(15,2);\n\nALTER TABLE employees\n  DROP officeCode;"),
            ("Xóa bảng", "DROP TABLE [IF EXISTS] employees;\n\n-- Xóa vĩnh viễn cả\n-- cấu trúc lẫn dữ liệu"),
            explain="Có thể kiểm tra cấu trúc bảng bất cứ lúc nào bằng <b>DESCRIBE table_name;</b> hoặc <b>SHOW CREATE TABLE table_name;</b>"),
        quote_slide(
            "Nếu chỉ muốn thay đổi một dòng của một bảng, nhưng quên mệnh đề WHERE ở lệnh UPDATE/DELETE, sẽ cập nhật hoặc xóa toàn bộ bảng.",
            "Cảnh báo quan trọng nhất chương này"),
        nav_closing(2),
    ]
    build_deck(slides, deck_path(2), HEAD, FOOT, "Bài 2 — Kiểu Dữ Liệu & Bảng", practice_href=PRACTICE_HREF[2])

# ============================================================ BÀI 3
def gen_bai3():
    slides = [
        cover(3),
        agenda_slide("Bài 3", [
            ("SQL là gì?", "Ngôn ngữ truy vấn cấp cao, chuẩn hóa qua SQL-86/92/99."),
            ("Cấu trúc SELECT cơ bản", "SELECT – FROM – WHERE và tương ứng với đại số quan hệ."),
            ("Toán tử so sánh & logic", "=, >, <, <>, AND, OR, NOT, kết hợp nhiều điều kiện."),
            ("DISTINCT & ORDER BY", "Loại bỏ trùng lặp và sắp xếp kết quả truy vấn."),
        ]),
        detail_slide("Bài 3", "SQL Là Gì?", "Ngôn ngữ truy vấn có cấu trúc, ra đời từ 1970s",
            [("Lịch sử", ["Phát triển bởi IBM những năm 1970, ban đầu gọi là SEQUEL", "Được ANSI công nhận thành chuẩn: SQL-86, SQL-92, SQL-99"]),
             ("SQL gồm những gì", ["Định nghĩa dữ liệu (DDL)", "Thao tác dữ liệu (DML)", "Định nghĩa khung nhìn (View)", "Ràng buộc toàn vẹn, phân quyền, giao dịch"])],
            [("Thuật ngữ SQL vs Đại số quan hệ", ["Bảng (table) ~ quan hệ (relation)", "Cột (column) ~ thuộc tính (attribute)", "Dòng (row) ~ bộ (tuple)"]),
             ("Vì sao cần SQL", ["Người dùng chỉ cần nêu YÊU CẦU (khai báo)", "Không cần viết thuật toán truy xuất dữ liệu như ngôn ngữ lập trình thường"])]),
        code_slide("Bài 3", "Cấu Trúc SELECT Cơ Bản", "Ba mệnh đề nền tảng của mọi truy vấn",
            [("Cú pháp chuẩn", "SELECT <danh sách cột>\nFROM <danh sách bảng>\nWHERE <điều kiện>;"),
             ("Ví dụ thật trên classicmodels", "SELECT *\nFROM employees\nWHERE officeCode = 5;")],
            explain="Mệnh đề WHERE là biểu thức boolean nối bằng AND/OR/NOT, dùng các toán tử <, >, =, LIKE, BETWEEN để xác định dòng nào được lấy ra."),
        code_slide("Bài 3", "Toán Tử Logic Kết Hợp", "AND / OR / NOT và thứ tự ưu tiên bằng dấu ngoặc",
            [("Kết hợp AND/OR/NOT", "SELECT * FROM city\nWHERE (country_id = 105)\n  AND ((city = 'Hanoi') OR (city = 'Vinh'));\n\nSELECT * FROM city\nWHERE NOT (country_id = 105)\n  AND NOT (country_id = 20);")],
            explain="Biểu thức trong dấu <b>()</b> luôn được tính trước. DISTINCT dùng để loại giá trị trùng: <b>SELECT DISTINCT country FROM customers;</b>"),
        quote_slide(
            "Thứ tự xuất hiện của các từ khoá WHERE, GROUP BY, HAVING, ORDER BY và LIMIT phải theo đúng thứ tự đó — viết sai thứ tự sẽ báo lỗi cú pháp.",
            "Quy tắc bắt buộc phải nhớ"),
        nav_closing(3),
    ]
    build_deck(slides, deck_path(3), HEAD, FOOT, "Bài 3 — Tổng Quan SQL", practice_href=PRACTICE_HREF[3])

# ============================================================ BÀI 4
def gen_bai4():
    slides = [
        cover(4),
        agenda_slide("Bài 4", [
            ("Toán tử IN", "Chọn giá trị phù hợp từ một tập giá trị cho trước."),
            ("Toán tử BETWEEN", "Lấy giá trị trong một phạm vi cụ thể."),
            ("Toán tử LIKE", "Tìm kiếm theo mẫu ký tự với % và _."),
            ("Thuộc tính suy diễn, ORDER BY, UNION", "Tạo cột tính toán, sắp xếp, và hợp nhiều kết quả truy vấn."),
        ]),
        code_two_col_slide("Bài 4", "IN & BETWEEN", "Hai toán tử lọc theo tập giá trị / khoảng giá trị",
            ("Toán tử IN", "SELECT officeCode, city, phone\nFROM offices\nWHERE country IN ('USA','France');\n\n-- Phủ định:\nWHERE country NOT IN ('USA','France')"),
            ("Toán tử BETWEEN", "SELECT productCode, productName, buyPrice\nFROM products\nWHERE buyPrice BETWEEN 90 AND 100\nORDER BY buyPrice DESC;"),
            explain="<b>IN</b> thay thế cho nhiều điều kiện OR liên tiếp trên cùng một cột. <b>BETWEEN a AND b</b> tương đương <b>cột >= a AND cột <= b</b>."),
        code_slide("Bài 4", "Toán Tử LIKE", "Tìm kiếm theo mẫu ký tự với % và _",
            [("Ví dụ thực tế", "-- Ho bat dau bang 'a'\nSELECT * FROM employees\nWHERE firstName LIKE 'a%';\n\n-- Ho chua cum 'on'\nSELECT * FROM employees\nWHERE lastName LIKE '%on%';\n\n-- Phu dinh\nWHERE lastName NOT LIKE 'B%';")],
            explain="Ký tự <b>%</b> đại diện cho một chuỗi bất kỳ (kể cả rỗng); <b>_</b> đại diện cho đúng một ký tự. Muốn tìm ký tự % hoặc _ theo nghĩa đen, thêm dấu <b>\\</b> phía trước."),
        code_two_col_slide("Bài 4", "Thuộc Tính Suy Diễn & UNION", "Tạo cột tính toán và hợp hai kết quả truy vấn",
            ("Thuộc tính suy diễn", "SELECT orderNumber,\n  (priceEach * quantityOrdered)\n  AS lineTotal\nFROM orderdetails;"),
            ("UNION hai bảng", "SELECT customerNumber id,\n  contactLastname name\nFROM customers\nUNION\nSELECT employeeNumber id,\n  firstname name\nFROM employees;"),
            explain="UNION yêu cầu số cột của các câu SELECT phải bằng nhau. Mặc định UNION tự loại bỏ dòng trùng lặp; dùng <b>UNION ALL</b> nếu muốn giữ lại."),
        quote_slide(
            "ORDER BY mặc định sắp xếp tăng dần (ASC). Có thể sắp theo nhiều cột cùng lúc, mỗi cột một chiều tăng/giảm riêng.",
            "Mẹo dùng ORDER BY nhiều cột"),
        nav_closing(4),
    ]
    build_deck(slides, deck_path(4), HEAD, FOOT, "Bài 4 — Truy Vấn Cơ Bản Phần 2", practice_href=PRACTICE_HREF[4])

# ============================================================ BÀI 5
def gen_bai5():
    slides = [
        cover(5),
        agenda_slide("Bài 5", [
            ("LIMIT", "Giới hạn số dòng kết quả trả về."),
            ("Hàm nhóm: MIN, MAX, COUNT, SUM, AVG", "Tính toán trên một tập giá trị của một cột."),
            ("Mệnh đề GROUP BY", "Gộp các bản ghi có cùng giá trị thành một nhóm."),
            ("Mệnh đề HAVING", "Lọc điều kiện trên kết quả đã gộp nhóm."),
        ]),
        code_two_col_slide("Bài 5", "LIMIT & Các Hàm Nhóm", "Giới hạn số dòng, và 4 hàm tính toán cơ bản",
            ("LIMIT", "SELECT * FROM payment\nWHERE amount > 2\nORDER BY staff_id\nLIMIT 10;"),
            ("MIN / MAX / SUM / AVG", "SELECT MIN(buyPrice), MAX(buyPrice)\nFROM products;\n\nSELECT SUM(quantityInStock)\nFROM products;\n\nSELECT AVG(buyPrice)\nFROM products;"),
            explain="<b>COUNT(*)</b> đếm số dòng; <b>COUNT(cột)</b> chỉ đếm giá trị khác NULL; <b>COUNT(DISTINCT cột)</b> đếm số giá trị khác nhau."),
        code_slide("Bài 5", "GROUP BY", "Gộp bản ghi theo một hoặc nhiều cột",
            [("Đếm và tính tổng theo nhóm", "SELECT status, COUNT(*)\nFROM orders\nGROUP BY status;\n\nSELECT productCode,\n  SUM(priceEach * quantityOrdered) AS total\nFROM orderdetails\nGROUP BY productCode\nORDER BY total DESC;")],
            explain="Hàm nhóm được tính riêng cho từng nhóm bản ghi có cùng giá trị tại cột GROUP BY, không còn tính trên toàn bảng nữa."),
        code_slide("Bài 5", "HAVING — Lọc Trên Kết Quả Nhóm", "Khác biệt cốt lõi giữa WHERE và HAVING",
            [("Lọc nhóm với HAVING", "SELECT orderNumber,\n  SUM(priceEach * quantityOrdered) AS total\nFROM orderdetails\nGROUP BY orderNumber\nHAVING total > 1000;")],
            explain="<b>WHERE</b> lọc từng dòng dữ liệu thô, chạy TRƯỚC khi gộp nhóm. <b>HAVING</b> lọc trên kết quả đã gộp, chạy SAU GROUP BY — vì vậy HAVING mới được dùng cùng hàm nhóm như SUM/COUNT."),
        quote_slide(
            "Nếu HAVING không đi kèm với GROUP BY, nó có ý nghĩa như WHERE. Nhưng WHERE không bao giờ được chứa hàm nhóm như SUM hay COUNT.",
            "Ghi nhớ để tránh lỗi 'Invalid use of group function'"),
        nav_closing(5),
    ]
    build_deck(slides, deck_path(5), HEAD, FOOT, "Bài 5 — Hàm Nhóm & GROUP BY", practice_href=PRACTICE_HREF[5])

# ============================================================ BÀI 6
def gen_bai6():
    slides = [
        cover(6),
        agenda_slide("Bài 6", [
            ("INNER JOIN", "Chỉ lấy các dòng thỏa điều kiện nối ở cả hai bảng."),
            ("LEFT JOIN", "Giữ lại toàn bộ bảng trái, kể cả không khớp bảng phải."),
            ("SELF JOIN", "Nối một bảng với chính nó — quan hệ phân cấp."),
            ("Alias & JOIN nhiều bảng", "Bí danh bảng và cách nối từ ba bảng trở lên."),
        ]),
        code_slide("Bài 6", "INNER JOIN", "Chỉ trả về các bản ghi khớp điều kiện ở cả hai bảng",
            [("Nối 2 bảng", "SELECT p.productCode, p.productName, o.orderNumber\nFROM products p\nINNER JOIN orderdetails o\n  ON p.productCode = o.productCode;"),
             ("Nối 3 bảng liên tiếp", "SELECT c.customerName,\n  SUM(od.priceEach*od.quantityOrdered) AS total\nFROM customers c\nINNER JOIN orders o ON c.customerNumber = o.customerNumber\nINNER JOIN orderdetails od ON o.orderNumber = od.orderNumber\nGROUP BY c.customerName;")],
            explain="<b>Alias</b> (p, o, c...) giúp rút gọn tên bảng và bắt buộc phải dùng khi các bảng có cột trùng tên, tránh lỗi 'ambiguous column'."),
        code_slide("Bài 6", "LEFT JOIN", "Giữ toàn bộ bảng trái, kể cả không có bản ghi khớp",
            [("Tìm khách hàng chưa có đơn hàng", "SELECT c.customerNumber, c.customerName,\n  o.orderNumber, o.status\nFROM customers c\nLEFT JOIN orders o\n  ON c.customerNumber = o.customerNumber\nWHERE o.orderNumber IS NULL;")],
            explain="Khi không tìm được dòng khớp ở bảng phải, các cột của bảng phải nhận giá trị <b>NULL</b> — đây chính là cách để lọc ra bản ghi 'chưa từng có quan hệ'."),
        code_slide("Bài 6", "SELF JOIN", "Nối một bảng với chính nó",
            [("Nhân viên và người quản lý", "SELECT\n  CONCAT(e1.lastName,' ',e1.firstName) AS NhanVien,\n  CONCAT(e2.lastName,' ',e2.firstName) AS QuanLy\nFROM employees e1\nLEFT JOIN employees e2\n  ON e1.reportsTo = e2.employeeNumber;")],
            explain="Bảng employees có khóa ngoại <b>reportsTo</b> tham chiếu tới chính khóa chính <b>employeeNumber</b> của nó — bắt buộc phải đặt 2 alias khác nhau cho cùng một bảng."),
        quote_slide(
            "MySQL không có FULL JOIN riêng, nhưng có thể mô phỏng bằng LEFT JOIN UNION RIGHT JOIN.",
            "Kiến thức mở rộng hay bị hỏi trong đề thi"),
        nav_closing(6),
    ]
    build_deck(slides, deck_path(6), HEAD, FOOT, "Bài 6 — Các Phép Nối Bảng", practice_href=PRACTICE_HREF[6])

# ============================================================ BÀI 7
def gen_bai7():
    slides = [
        cover(7),
        agenda_slide("Bài 7", [
            ("Khái niệm truy vấn con", "Một câu SELECT nằm bên trong câu lệnh khác."),
            ("Subquery không tương quan", "Chạy độc lập, chỉ một lần cho toàn bộ câu lệnh."),
            ("Subquery tương quan", "Dùng giá trị từ truy vấn ngoài, chạy lại cho mỗi dòng."),
            ("Subquery ở SELECT / FROM", "Không chỉ dùng được trong WHERE."),
        ]),
        code_slide("Bài 7", "Subquery Không Tương Quan", "Chạy độc lập, một lần duy nhất",
            [("Sản phẩm chưa từng bán được", "SELECT * FROM products\nWHERE productCode NOT IN (\n  SELECT productCode FROM orderdetails\n);"),
             ("Đơn hàng gần nhất", "SELECT * FROM orders\nWHERE orderDate = (\n  SELECT MAX(orderDate) FROM orders\n);")],
            explain="Truy vấn con bên trong được tính TRƯỚC, kết quả của nó được điền vào truy vấn ngoài, rồi mới thực thi truy vấn ngoài."),
        code_slide("Bài 7", "Subquery Tương Quan", "Sử dụng giá trị của truy vấn ngoài trong WHERE",
            [("So sánh với trung bình cùng loại", "SELECT * FROM products p\nWHERE quantityInStock > (\n  SELECT AVG(quantityInStock) FROM products\n  WHERE productLine = p.productLine\n);"),
             ("Dùng EXISTS thay cho IN", "SELECT * FROM products p\nWHERE EXISTS (\n  SELECT productCode FROM orderdetails\n  WHERE productCode = p.productCode\n);")],
            explain="Với mỗi dòng của truy vấn ngoài, truy vấn con chạy lại và dùng giá trị <b>p.productLine</b>/<b>p.productCode</b> của chính dòng đó — nên gọi là 'tương quan'."),
        code_slide("Bài 7", "Subquery Ở SELECT Và FROM", "Truy vấn con không chỉ dùng trong WHERE",
            [("Ở mệnh đề SELECT", "SELECT orderNumber, quantityOrdered,\n  (SELECT productName FROM products\n   WHERE productCode = o.productCode) AS Ten\nFROM orderdetails o;"),
             ("Ở mệnh đề FROM (như 1 bảng tạm)", "SELECT T.nam_thang, COUNT(*)\nFROM (\n  SELECT orderNumber,\n    SUBSTR(orderdate,1,7) AS nam_thang\n  FROM orders\n) AS T\nGROUP BY T.nam_thang;")],
            explain="Khi subquery đứng ở mệnh đề FROM, kết quả của nó được coi như một bảng dữ liệu tạm thời để truy vấn ngoài tiếp tục xử lý."),
        quote_slide(
            "Truy vấn con tương quan thường chạy chậm hơn vì phải thực thi lại nhiều lần — nên cân nhắc viết lại bằng JOIN nếu có thể.",
            "Lưu ý về hiệu năng"),
        nav_closing(7),
    ]
    build_deck(slides, deck_path(7), HEAD, FOOT, "Bài 7 — Truy Vấn Con", practice_href=PRACTICE_HREF[7])

# ============================================================ BÀI 8
def gen_bai8():
    slides = [
        cover(8),
        agenda_slide("Bài 8", [
            ("Câu lệnh INSERT", "Thêm một hoặc nhiều dòng, hoặc thêm từ kết quả SELECT."),
            ("Câu lệnh UPDATE", "Cập nhật giá trị đã tồn tại, luôn cần mệnh đề WHERE."),
            ("Câu lệnh DELETE", "Xóa dòng dữ liệu theo điều kiện."),
            ("Ràng buộc khi xóa dữ liệu", "Khóa ngoại có thể chặn thao tác DELETE."),
        ]),
        code_two_col_slide("Bài 8", "INSERT", "Hai cách thêm dữ liệu vào bảng",
            ("Thêm giá trị trực tiếp", "INSERT INTO offices\n  (officeCode, city, country)\nVALUES\n  ('8','Ha Noi','Vietnam'),\n  ('9','Boston','USA');"),
            ("Thêm từ SELECT (nhiều dòng)", "CREATE TABLE temp_offices LIKE offices;\n\nINSERT INTO temp_offices\nSELECT * FROM offices\nWHERE country = 'USA';"),
            explain="Luôn nên liệt kê rõ tên cột khi INSERT — nếu thứ tự cột trong bảng thay đổi, không xác định tên cột có thể khiến giá trị bị gán sai vị trí."),
        code_slide("Bài 8", "UPDATE & DELETE", "Hai lệnh nguy hiểm nhất nếu quên WHERE",
            [("UPDATE có điều kiện", "UPDATE employees\nSET email = 'diane-murphy@classicmodelcars.com'\nWHERE employeeNumber = 1002;"),
             ("DELETE nhiều bảng cùng lúc", "DELETE employees, offices\nFROM employees, offices\nWHERE employees.officeCode = offices.officeCode\n  AND offices.officeCode = 1;")],
            explain="Trước khi chạy UPDATE/DELETE thật, nên chạy thử một câu SELECT với đúng điều kiện WHERE đó để xem trước những dòng sẽ bị ảnh hưởng."),
        detail_slide("Bài 8", "Ràng Buộc Khi Xóa Dữ Liệu", "Khóa ngoại có thể chặn hoặc tự động lan truyền DELETE",
            [("ON DELETE RESTRICT (mặc định)", ["Không cho xóa dòng cha nếu còn dòng con tham chiếu tới", "MySQL báo lỗi 'Cannot delete or update a parent row'"])],
            [("ON DELETE CASCADE", ["Tự động xóa luôn các dòng con liên quan", "Cần khai báo tường minh khi tạo khóa ngoại"]),
             ("ON DELETE SET NULL", ["Khóa ngoại của dòng con được gán về NULL", "Dòng con vẫn tồn tại nhưng mất liên kết"])]),
        quote_slide(
            "Nên luôn luôn kiểm tra điều kiện WHERE trong một câu lệnh SELECT trước khi thực hiện lệnh UPDATE hoặc DELETE.",
            "Quy tắc an toàn bắt buộc"),
        nav_closing(8, extra_sub="Bài này khớp với bộ 10 câu ôn tập GROUP BY/HAVING/JOIN/SUBQUERY đã có lời giải chi tiết."),
    ]
    build_deck(slides, deck_path(8), HEAD, FOOT, "Bài 8 — Thêm Sửa Xóa Dữ Liệu", practice_href=PRACTICE_HREF[8])

# ============================================================ BÀI 9
def gen_bai9():
    slides = [
        cover(9),
        agenda_slide("Bài 9", [
            ("Ôn lại truy vấn cơ bản", "SELECT/WHERE/LIKE/ORDER BY trên nhiều bảng."),
            ("Ôn lại JOIN & GROUP BY", "Tính tổng, đếm, tìm trung bình theo nhóm."),
            ("Ôn lại Subquery", "NOT IN / NOT EXISTS, so sánh với giá trị trung bình."),
            ("UNION & UPDATE+REPLACE", "Kết hợp danh sách từ 2 bảng, thay thế chuỗi trong dữ liệu."),
        ]),
        code_slide("Bài 9", "20 Câu Ôn Tập — Dạng Câu Hỏi", "Đề ôn tập tổng hợp toàn bộ kiến thức đã học",
            [("5 câu đầu — lọc dữ liệu cơ bản", "-- Bai 2: Khach hang o USA, sap xep theo ten\nSELECT * FROM customers\nWHERE country = 'USA'\nORDER BY customerName ASC;\n\n-- Bai 7: Ten bat dau bang chu A\nSELECT * FROM customers\nWHERE customerName LIKE 'A%';")],
            explain="Câu 1-10 của bộ ôn tập chỉ dùng một bảng: lọc theo quốc gia, dòng sản phẩm, năm đặt hàng, chức danh, khoảng giá — luyện phản xạ WHERE/LIKE/ORDER BY/LIMIT."),
        code_slide("Bài 9", "Nhóm Câu JOIN + GROUP BY + Subquery", "Câu 11-17: kết hợp nhiều bảng và tính toán",
            [("Đếm đơn hàng theo khách, chỉ giữ >=3", "SELECT c.customerNumber, c.customerName,\n  COUNT(o.orderNumber) AS SoDon\nFROM customers c\nJOIN orders o ON c.customerNumber=o.customerNumber\nWHERE YEAR(o.orderDate)=2004\nGROUP BY c.customerNumber, c.customerName\nHAVING COUNT(o.orderNumber) >= 3;"),
             ("Khách hàng chưa từng đặt hàng", "SELECT * FROM customers c\nWHERE NOT EXISTS (\n  SELECT 1 FROM orders o\n  WHERE o.customerNumber = c.customerNumber\n);")],
            explain="Câu 17 (đơn hàng có totalAmount lớn hơn trung bình) là dạng subquery so sánh trung bình — mẫu bài đã luyện ở Bài 7."),
        code_two_col_slide("Bài 9", "UNION & UPDATE + REPLACE", "Hai câu cuối của bộ ôn tập",
            ("UNION danh sách city", "SELECT city FROM customers\nUNION\nSELECT city FROM offices;"),
            ("UPDATE + REPLACE", "SET SQL_SAFE_UPDATES = 0;\nUPDATE offices\nSET city = REPLACE(city,'NYC','New York');\nSET SQL_SAFE_UPDATES = 1;"),
            explain="REPLACE(cột, chuỗi_cần_tìm, chuỗi_thay_thế) phân biệt hoa-thường khi tìm kiếm."),
        quote_slide(
            "Các bạn ôn lại các notes, làm lại toàn bộ.",
            "Nguyên văn ghi chú của giảng viên ở buổi ôn tập này"),
        nav_closing(9),
    ]
    build_deck(slides, deck_path(9), HEAD, FOOT, "Bài 9 — Ôn Tập Tổng Hợp", practice_href=PRACTICE_HREF[9])

# ============================================================ BÀI 10
def gen_bai10():
    slides = [
        cover(10),
        agenda_slide("Bài 10", [
            ("INNER JOIN cơ bản", "5 bài: nối 2-4 bảng, chưa cần tính toán."),
            ("INNER JOIN + hàm tổng hợp", "7 bài: SUM/COUNT theo nhóm, TOP N, HAVING."),
            ("LEFT JOIN", "8 bài: giữ toàn bộ bảng trái, xử lý giá trị 0/NULL."),
            ("Chuẩn bị thi thực hành", "Đúng cấu trúc 20 câu như đề thi tổng kết."),
        ]),
        code_slide("Bài 10", "Phần B — INNER JOIN Cơ Bản", "5 bài đầu: chỉ cần nối bảng đúng, chưa tính toán",
            [("Bài 3 — Nhân viên phụ trách khách hàng", "SELECT e.employeeNumber, e.lastName, e.firstName,\n  c.customerNumber, c.customerName, c.country\nFROM employees e\nJOIN customers c\n  ON e.employeeNumber = c.salesRepEmployeeNumber\nORDER BY e.lastName, e.firstName;")],
            explain="Mẹo làm nhanh: luôn xác định đúng CỘT NỐI trước (ở đây là employeeNumber ↔ salesRepEmployeeNumber), rồi mới thêm SELECT/ORDER BY."),
        code_slide("Bài 10", "Phần C — JOIN + Hàm Tổng Hợp", "7 bài: SUM/COUNT theo nhóm, TOP N, HAVING",
            [("Bài 9 — Khách hàng có >=3 đơn hàng", "SELECT c.customerNumber, c.customerName,\n  COUNT(o.orderNumber) AS orderCount\nFROM customers c\nJOIN orders o ON c.customerNumber = o.customerNumber\nGROUP BY c.customerNumber, c.customerName\nHAVING COUNT(o.orderNumber) >= 3;"),
             ("Bài 7 — Top 10 sản phẩm bán chạy", "SELECT productCode, productName,\n  SUM(quantityOrdered) AS totalQuantityOrdered\nFROM products JOIN orderdetails USING(productCode)\nGROUP BY productCode, productName\nORDER BY totalQuantityOrdered DESC\nLIMIT 10;")],
            exam_badge=True,
            explain="Cấu trúc y hệt đề thi thật: JOIN → GROUP BY → HAVING/ORDER BY/LIMIT."),
        code_slide("Bài 10", "Phần D — LEFT JOIN", "8 bài: giữ toàn bộ bảng trái, xử lý NULL/0",
            [("Bài 20 — Tổng giá trị đơn hàng, kể cả 0", "SELECT c.customerNumber, c.customerName,\n  COALESCE(SUM(od.quantityOrdered*od.priceEach),0)\n  AS totalOrderValue\nFROM customers c\nLEFT JOIN orders o ON c.customerNumber=o.customerNumber\nLEFT JOIN orderdetails od ON o.orderNumber=od.orderNumber\nGROUP BY c.customerNumber, c.customerName;")],
            explain="<b>COALESCE(x, 0)</b> thay NULL bằng 0 — bắt buộc phải dùng khi đề yêu cầu khách hàng chưa có đơn hàng vẫn phải hiện ra với giá trị 0, không phải NULL."),
        split_slide("Bài 10", "Tổng Kết 20 Bài", "Phân bổ độ khó giống hệt cấu trúc đề thi thật",
            ["5 bài INNER JOIN cơ bản — chỉ cần nối đúng bảng, chưa tính toán.",
             "7 bài INNER JOIN kết hợp SUM/COUNT — cần thêm GROUP BY, HAVING, ORDER BY, LIMIT.",
             "8 bài LEFT JOIN — kỹ năng khó nhất: giữ dữ liệu bên trái, xử lý NULL bằng COALESCE hoặc IS NULL."],
            "20 bài này đã có sẵn dưới dạng bài tập chấm điểm tự động trên website luyện tập.",
            "Xem ngay tại mục Classicmodels",
            [("20", "Bài tập JOIN"), ("3", "Nhóm độ khó"), ("100%", "Đã có lời giải")]),
        nav_closing(10, extra_sub="20 bài JOIN này (mã cm14-cm33) đã có sẵn để luyện tương tác, chấm điểm ngay."),
    ]
    build_deck(slides, deck_path(10), HEAD, FOOT, "Bài 10 — Nối Bảng Nâng Cao", practice_href=PRACTICE_HREF[10])


ALL_GENERATORS = [gen_bai1, gen_bai2, gen_bai3, gen_bai4, gen_bai5,
                  gen_bai6, gen_bai7, gen_bai8, gen_bai9, gen_bai10]

if __name__ == "__main__":
    for g in ALL_GENERATORS:
        g()
    print(f"\nDA SINH {len(ALL_GENERATORS)} BAI GIANG.")
