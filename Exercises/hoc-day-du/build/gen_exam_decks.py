# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from slidegen import (cover_slide, agenda_slide, code_slide, code_two_col_slide,
                       detail_slide, timeline_slide, split_slide, quote_slide,
                       closing_slide, erd_slide, mcq_sample_slide, build_deck)

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.dirname(HERE)  # .../hoc-day-du/
HEAD = os.path.join(HERE, "shell_head.html")
FOOT = os.path.join(HERE, "shell_foot.html")

sql_pool = json.load(open("/tmp/deexam/sql_pool.json", encoding="utf-8"))
ch3_pool = json.load(open("/tmp/deexam/ch3_pool.json", encoding="utf-8"))
ch4_pool = json.load(open("/tmp/deexam/ch4_pool.json", encoding="utf-8"))

def sample_from(pool, start, count=3):
    return [(q["question"], q["options"], q["correctIndex"]) for q in pool[start:start+count]]

def deck_path(n):
    return os.path.join(OUT_DIR, f"de-mau-{n}.html")

EXAMS = [
    {
        "num": 1,
        "title": "Đề Mẫu Số 01",
        "sub": "28 câu trắc nghiệm + tự luận thiết kế ERD — chủ đề Quản lý Gara Ô Tô",
        "sql_start": 0, "th_start_ch3": 0, "th_start_ch4": 0,
        "center": ("XE", ["Mã Xe [khóa]", "Tên Xe"]),
        "side_nn": ("THỢ SỬA", ["Mã Thợ Sửa [khóa]", "Tên Thợ Sửa"]),
        "side_1n": ("KHÁCH HÀNG", ["Mã Khách Hàng [khóa]", "Tên Khách Hàng"]),
        "rel_nn": "SỬA CHỮA", "rel_1n": "SỞ HỮU",
        "erd_prompt": "Một gara ô tô có nhiều thợ sửa xe; một thợ sửa nhiều xe, một xe được nhiều thợ cùng sửa qua các lần khác nhau. Mỗi xe thuộc quyền sở hữu của đúng một khách hàng; một khách hàng có thể sở hữu nhiều xe.",
        "rel_code": ("Mô hình quan hệ", "KhachHang(MaKH [PK], TenKH)\nThoSua(MaTho [PK], TenTho)\nXe(MaXe [PK], TenXe,\n   MaKH [FK -> KhachHang])\nSuaChua(MaTho [PK,FK], MaXe [PK,FK])"),
        "cau2_title": "Trigger kiểm tra chi phí sửa chữa",
        "cau2_code": ("PhieuSuaChua_HanMuc", "DELIMITER //\nCREATE TRIGGER PhieuSuaChua_HanMuc\nBEFORE INSERT ON PhieuSuaChua\nFOR EACH ROW\nBEGIN\n  IF NEW.ChiPhi > 20000000 THEN\n    SIGNAL SQLSTATE '45000'\n    SET MESSAGE_TEXT =\n      'Vuot han muc cho phep.';\n  END IF;\nEND //\nDELIMITER ;"),
        "cau2_explain": "ChiPhi = <b>5.000.000</b> → không &gt; 20.000.000 → INSERT thành công.<br>ChiPhi = <b>25.000.000</b> → 25tr &gt; 20tr → trigger chặn, INSERT bị hủy.",
    },
    {
        "num": 2,
        "title": "Đề Mẫu Số 02",
        "sub": "28 câu trắc nghiệm + tự luận thiết kế ERD — chủ đề Quản lý Thư Viện",
        "sql_start": 14, "th_start_ch3": 7, "th_start_ch4": 7,
        "center": ("SÁCH", ["Mã Sách [khóa]", "Tên Sách"]),
        "side_nn": ("ĐỘC GIẢ", ["Mã Độc Giả [khóa]", "Tên Độc Giả"]),
        "side_1n": ("NHÀ XUẤT BẢN", ["Mã NXB [khóa]", "Tên NXB"]),
        "rel_nn": "MƯỢN", "rel_1n": "XUẤT BẢN",
        "erd_prompt": "Một thư viện có nhiều độc giả; một độc giả mượn nhiều sách, một sách được nhiều độc giả mượn qua các lượt khác nhau. Mỗi sách do đúng một nhà xuất bản phát hành; một nhà xuất bản phát hành nhiều sách.",
        "rel_code": ("Mô hình quan hệ", "DocGia(MaDG [PK], TenDG)\nNhaXuatBan(MaNXB [PK], TenNXB)\nSach(MaSach [PK], TenSach,\n     MaNXB [FK -> NhaXuatBan])\nMuon(MaDG [PK,FK], MaSach [PK,FK])"),
        "cau2_title": "Trigger kiểm tra số sách mượn tối đa",
        "cau2_code": ("Muon_GioiHan", "DELIMITER //\nCREATE TRIGGER Muon_GioiHan\nBEFORE INSERT ON Muon\nFOR EACH ROW\nBEGIN\n  DECLARE v INT;\n  SELECT COUNT(*) INTO v\n    FROM Muon WHERE MaDG=NEW.MaDG;\n  IF v >= 5 THEN\n    SIGNAL SQLSTATE '45000'\n    SET MESSAGE_TEXT = 'Da toi da 5 cuon.';\n  END IF;\nEND //\nDELIMITER ;"),
        "cau2_explain": "Độc giả đang có <b>4</b> cuốn → mượn thêm: đếm được 4, chưa &gt;=5 → thành công (giờ có 5).<br>Mượn tiếp lần nữa (đang có <b>5</b>): đếm được 5 → &gt;=5 → bị chặn.",
    },
    {
        "num": 3,
        "title": "Đề Mẫu Số 03",
        "sub": "28 câu trắc nghiệm + tự luận thiết kế ERD — chủ đề Quản lý Phòng Khám",
        "sql_start": 28, "th_start_ch3": 14, "th_start_ch4": 14,
        "center": ("BÁC SĨ", ["Mã Bác Sĩ [khóa]", "Tên Bác Sĩ"]),
        "side_nn": ("BỆNH NHÂN", ["Mã Bệnh Nhân [khóa]", "Tên Bệnh Nhân"]),
        "side_1n": ("PHÒNG KHÁM", ["Mã Phòng Khám [khóa]", "Tên Phòng Khám"]),
        "rel_nn": "KHÁM", "rel_1n": "LÀM VIỆC TẠI",
        "erd_prompt": "Một phòng khám có nhiều bác sĩ làm việc; mỗi bác sĩ chỉ làm việc cố định tại một phòng khám. Một bác sĩ khám nhiều bệnh nhân, một bệnh nhân được nhiều bác sĩ khám qua các lượt khác nhau.",
        "rel_code": ("Mô hình quan hệ", "PhongKham(MaPK [PK], TenPK)\nBenhNhan(MaBN [PK], TenBN)\nBacSi(MaBS [PK], TenBS,\n      MaPK [FK -> PhongKham])\nKham(MaBS [PK,FK], MaBN [PK,FK])"),
        "cau2_title": "So sánh AS SELECT và LIKE",
        "cau2_code": ("2 cách tạo bảng tạm", "CREATE TABLE Temp_BenhNhanA\nAS SELECT * FROM BenhNhan\nWHERE MaPK = 'PK01';\n\nCREATE TABLE Temp_BenhNhanB\nLIKE BenhNhan;"),
        "cau2_explain": "<b>AS SELECT</b>: có ngay dữ liệu lọc, KHÔNG có PK/index.<br><b>LIKE</b>: bảng RỖNG, có ĐẦY ĐỦ ràng buộc/PK/index như bảng gốc.",
    },
]

def gen_exam_deck(ex):
    n = ex["num"]
    sql_samples = sample_from(sql_pool, ex["sql_start"], 3)
    th_samples = sample_from(ch3_pool, ex["th_start_ch3"], 2) + sample_from(ch4_pool, ex["th_start_ch4"], 1)

    slides = [
        cover_slide("Đề Ôn Thi Mẫu", [ex["title"]], ex["sub"], f"Đề Mẫu {n} / 3", "Cơ Sở Dữ Liệu — Phenikaa"),
        agenda_slide(f"Đề Mẫu {n}", [
            ("Phần 1.A — Truy vấn SQL", "14 câu trắc nghiệm (3.5 điểm) — SELECT, WHERE, JOIN, GROUP BY..."),
            ("Phần 1.B — Chuẩn hóa & Phụ thuộc hàm", "14 câu trắc nghiệm (3.5 điểm) — đại số quan hệ, khóa, dạng chuẩn."),
            ("Câu 1 Tự luận — Thiết kế ERD", "2 điểm — mô hình thực thể liên kết + chuyển sang mô hình quan hệ."),
            ("Câu 2 Tự luận", f"1 điểm — {ex['cau2_title'].lower()}."),
        ]),
        mcq_sample_slide(f"Đề Mẫu {n}", "Phần 1.A — Ví Dụ Trắc Nghiệm SQL", "3 câu minh họa (trong tổng số 14 câu)", sql_samples),
        mcq_sample_slide(f"Đề Mẫu {n}", "Phần 1.B — Ví Dụ Chuẩn Hóa & Phụ Thuộc Hàm", "3 câu minh họa (trong tổng số 14 câu)", th_samples),
        erd_slide(f"Đề Mẫu {n}", "Câu 1a — Thiết Kế ERD (1 điểm)", ex["erd_prompt"],
                   ex["center"], ex["side_nn"], ex["side_1n"], ex["rel_nn"], ex["rel_1n"]),
        code_slide(f"Đề Mẫu {n}", "Câu 1b — Chuyển Sang Mô Hình Quan Hệ (1 điểm)",
                   "N-N → bảng trung gian, 1-N → khóa ngoại trong bảng phía N",
                   [ex["rel_code"]],
                   explain=f"Quan hệ <b>{ex['rel_nn']}</b> (N-N) bắt buộc tách bảng trung gian riêng. Quan hệ <b>{ex['rel_1n']}</b> (1-N) chỉ cần thêm khóa ngoại, không tách bảng."),
        code_slide(f"Đề Mẫu {n}", f"Câu 2 — {ex['cau2_title']} (1 điểm)", "Dự đoán kết quả khi chạy đoạn lệnh sau",
                   [ex["cau2_code"]], explain=ex["cau2_explain"]),
        quote_slide(
            "Đọc kỹ đề trước khi viết: xác định đúng bản số N-N hay 1-N từ chính câu chữ trong đề — đây là điểm mất nhiều nhất trong phần tự luận.",
            f"Ghi nhớ khi làm Đề Mẫu {n}"),
        closing_slide(
            f"Hoàn Thành Đề Mẫu {n}",
            "Xem đề đầy đủ (28 câu trắc nghiệm + đáp án chi tiết) trong file Markdown đi kèm, hoặc quay lại ôn từng chủ đề.",
            "Về Trang Học Đầy Đủ →", "index.html",
            'Ôn tập tương tác: <a href="../index.html" style="color:inherit;">Luyện Tập Tương Tác</a>'
                + (f' · <a href="de-mau-{n+1}.html" style="color:inherit;">Đề Mẫu {n+1} →</a>' if n < 3 else "")
        ),
    ]
    build_deck(slides, deck_path(n), HEAD, FOOT, f"{ex['title']} — Cơ Sở Dữ Liệu")

if __name__ == "__main__":
    for ex in EXAMS:
        gen_exam_deck(ex)
    print("\nDA SINH 3 DE MAU SLIDE.")
