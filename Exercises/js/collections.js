// Đăng ký toàn bộ "bộ sưu tập" câu hỏi hiển thị trong sidebar, theo đúng thứ tự xuất hiện.
// kind: "sql" (chấm bằng sql.js, dùng SCHEMAS) | "mcq" (trắc nghiệm, chấm bằng JS thuần)
//       | "essay" (tự luận, tự chấm bằng cách so với đáp án mẫu + rubric)
const COLLECTIONS = [
  { id: "classicmodels", kind: "sql", icon: "🚗", label: "Classicmodels", desc: SCHEMAS_DESC("classicmodels") },
  { id: "truong_hoc", kind: "sql", icon: "🏫", label: "Trường Học", desc: SCHEMAS_DESC("truong_hoc") },
  { id: "cua_hang_sach", kind: "sql", icon: "📚", label: "Cửa Hàng Sách", desc: SCHEMAS_DESC("cua_hang_sach") },
  {
    id: "mcqsql", kind: "mcq", icon: "🧠", label: "Trắc Nghiệm SQL Thực Hành",
    desc: "220 câu trắc nghiệm về cú pháp SELECT/JOIN/GROUP BY..., chia theo 6 buổi thực hành.",
    groupLabel: (n) => `Buổi thực hành ${n}`,
  },
  {
    id: "mcqtheory", kind: "mcq", icon: "📖", label: "Trắc Nghiệm Lý Thuyết CSDL",
    desc: "194 câu trắc nghiệm lý thuyết: tổng quan CSDL, ERD, mô hình quan hệ, chuẩn hóa, SQL, cấu trúc nâng cao.",
    groupLabel: (n) => `Chương ${n}`,
  },
  {
    id: "essay", kind: "essay", icon: "✍️", label: "Tự Luận (ERD · Trigger · Chuẩn hóa)",
    desc: "Các dạng bài tự luận giống hệt đề thi thật: thiết kế ERD, chuyển mô hình quan hệ, dự đoán hành vi TRIGGER/VIEW, chuẩn hóa, tìm khóa ứng viên.",
  },
];

function SCHEMAS_DESC(id) {
  // Gọi lười (lazy) vì SCHEMAS được định nghĩa trong schemas.js nạp trước file này.
  return (typeof SCHEMAS !== "undefined" && SCHEMAS[id]) ? SCHEMAS[id].desc : "";
}

const CHAPTER_THEORY_NAMES = {
  1: "Tổng quan về Cơ sở dữ liệu",
  2: "Mô hình Thực thể Liên kết (ERD)",
  3: "Mô hình quan hệ & Phụ thuộc hàm",
  4: "Chuẩn hóa cơ sở dữ liệu",
  5: "Ngôn ngữ SQL",
  6: "Cấu trúc nâng cao (View, Trigger, Index, Transaction)",
};
const LAB_SQL_NAMES = {
  3: "Truy vấn cơ bản (SELECT, WHERE, ORDER BY)",
  4: "Nối bảng (JOIN)",
  5: "Gom nhóm (GROUP BY, HAVING)",
  6: "Truy vấn con (Subquery)",
  7: "Thao tác dữ liệu (INSERT/UPDATE/DELETE)",
  8: "View, Trigger, Index",
};
