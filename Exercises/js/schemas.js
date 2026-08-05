// Mô tả cấu trúc bảng của từng CSDL, dùng để hiển thị trong khung "Xem sơ đồ bảng"
const SCHEMAS = {
  classicmodels: {
    label: "Classicmodels",
    icon: "🚗",
    desc: "CSDL bán lẻ xe mô hình (dữ liệu thật, tiếng Anh) — 8 bảng, hơn 3.800 dòng dữ liệu.",
    tables: [
      { name: "offices", cols: "officeCode PK, city, phone, addressLine1, country, postalCode, territory" },
      { name: "employees", cols: "employeeNumber PK, lastName, firstName, email, officeCode FK, reportsTo FK, jobTitle" },
      { name: "customers", cols: "customerNumber PK, customerName, city, country, salesRepEmployeeNumber FK, creditLimit" },
      { name: "productlines", cols: "productLine PK, textDescription" },
      { name: "products", cols: "productCode PK, productName, productLine FK, buyPrice, MSRP, quantityInStock" },
      { name: "orders", cols: "orderNumber PK, orderDate, shippedDate, status, customerNumber FK" },
      { name: "orderdetails", cols: "orderNumber FK, productCode FK, quantityOrdered, priceEach, orderLineNumber" },
      { name: "payments", cols: "customerNumber FK, checkNumber, paymentDate, amount" },
    ],
  },
  truong_hoc: {
    label: "Trường Học",
    icon: "🏫",
    desc: "CSDL quản lý điểm số trường phổ thông (tiếng Việt) — 5 bảng, gần 3.000 dòng điểm.",
    tables: [
      { name: "GiaoVien", cols: "MaGV PK, HoTen, MonDay, ChucVu, MaQuanLy FK (tự tham chiếu)" },
      { name: "LopHoc", cols: "MaLop PK, TenLop, Khoi, MaGVCN FK -> GiaoVien" },
      { name: "MonHoc", cols: "MaMon PK, TenMon, SoTietTuan" },
      { name: "HocSinh", cols: "MaHS PK, HoTen, NgaySinh, GioiTinh, MaLop FK -> LopHoc" },
      { name: "DiemSo", cols: "MaHS FK, MaMon FK, HocKy, LoaiDiem, Diem" },
    ],
  },
  cua_hang_sach: {
    label: "Cửa Hàng Sách",
    icon: "📚",
    desc: "CSDL bán sách trực tuyến (tiếng Việt) — 5 bảng, mô hình tương tự Classicmodels.",
    tables: [
      { name: "TacGia", cols: "MaTG PK, HoTen, QuocGia" },
      { name: "Sach", cols: "MaSach PK, TenSach, MaTG FK, TheLoai, GiaBan, SoLuongTon, NamXuatBan" },
      { name: "KhachHang", cols: "MaKH PK, HoTen, ThanhPho, Email" },
      { name: "DonHang", cols: "MaDH PK, MaKH FK, NgayDat, TrangThai" },
      { name: "ChiTietDonHang", cols: "MaDH FK, MaSach FK, SoLuong, DonGia" },
    ],
  },
};
