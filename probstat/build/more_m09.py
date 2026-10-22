"""Module 9 — phần chuyên sâu: sơ đồ chọn phương pháp và chiến lược làm bài giữa kỳ."""
from hx import *
K = 'MODULE 9 · '
def parts():
    s = []
    s.append(sl(table(['Dấu hiệu trong đề', 'Dạng bài', 'Công cụ', 'Module'],
                      [['“x̄, s, tứ phân vị, ngoại lai”', 'thống kê mô tả', 'pskit/bảng, 1.5·IQR', '1'], ['“có bao nhiêu cách”, “chọn”, “xếp”', 'đếm', 'A, C, quy tắc nhân', '2'], ['“biết rằng”, “với điều kiện”', 'có điều kiện', 'P(A|B) = P(AB)/P(B)', '3'],
                       ['“nguyên nhân”, “nhà máy”, “xét nghiệm”', 'toàn phần / Bayes', 'cây xác suất', '4'], ['bảng P(X = x) hoặc f(x)', 'BNN', 'E, Var, F', '5'], ['“N(μ, σ²)”, “tìm c”', 'chuẩn', 'Φ, Φ⁻¹', '6'],
                       ['“ước lượng”, “hợp lý cực đại”', 'MLE', 'đạo hàm ln L', '7'], ['“khoảng tin cậy”, “cỡ mẫu”', 'ước lượng khoảng', 'U, t', '8']]),
                K + 'PHẦN 1 · Chuyên sâu', 'Bản đồ nhận dạng dạng bài', explain='Đọc từ khóa trong đề trước khi tính: 80% thời gian làm đề là nhận ra đúng dạng.'))
    s.append(sl(ul(['<b>Phân bổ thời gian</b>: câu chuẩn (câu 1) và câu đếm/xác suất làm trước — chắc điểm.', '<b>Viết công thức trước, thay số sau</b>: có điểm ngay cả khi sai tính toán.', '<b>Làm tròn</b> giữ ≥ 4 chữ số ở bước trung gian; đáp án ghi 3–4 chữ số thập phân.', '<b>Kiểm tra hợp lý</b>: xác suất ∈ [0, 1]; phương sai ≥ 0; khoảng tin cậy chứa x̄ ở chính giữa.', '<b>Bảng tra</b>: nhớ z₀.₉₅ = 1.645, z₀.₉₇₅ = 1.96, z₀.₉₉ = 2.326.']), K + 'PHẦN 1 · Chuyên sâu', 'Chiến lược làm đề'))
    s.append(sl(table(['Lỗi hay gặp', 'Biểu hiện', 'Cách phòng'], [['Quên chuẩn hóa', 'dùng thẳng giá trị x với bảng Φ', 'luôn viết z = (x − μ)/σ'], ['Nhầm σ², σ', 'chia cho phương sai', 'đề cho σ² thì lấy căn'], ['Quên n − 1', 's² chia n', 'mẫu thô: n − 1'], ['Nhầm một phía/hai phía', 'dùng U_α thay U_{α/2}', 'xác định dạng đề trước'], ['Cộng thay nhân', 'P(AB) = P(A) + P(B)', 'hỏi: độc lập hay xung khắc?']]), K + 'PHẦN 1 · Chuyên sâu', 'Lỗi mất điểm nhiều nhất'))
    return [dict(title='Chuyên sâu: chiến lược ôn thi', bullets=['Bản đồ dạng bài', 'Chiến lược', 'Lỗi mất điểm'], slides=s)]
