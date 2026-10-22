"""Module 9 — câu ôn tập tổng hợp Chương 1–2 (khái niệm, nhãn bo_sung)."""
from orig_m09 import TOP
SRC = 'Bổ sung: câu ôn tập tổng hợp Chương 1–2 (lý thuyết, đáp án đối chiếu giáo trình)'
def build(B):
    def C(stem, ok, bad, expl, lvl=1, topic='on'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Đề hỏi “biết kết quả B, xác suất do nguyên nhân Aᵢ” thì dùng', 'công thức Bayes', ['quy tắc cộng', 'công thức toàn phần', 'quy tắc nhân độc lập'], 'Đảo chiều điều kiện.')
    C('Đề hỏi tìm c để P(X ≤ c) = 0.95 với X chuẩn thì', 'c = μ + σ·z₀.₉₅', ['c = 0.95', 'c = (μ − 0.95)/σ', 'c = μ·σ'], 'Phân vị của chuẩn.')
    C('Phương sai mẫu của dữ liệu thô chia cho', 'n − 1', ['n', 'n + 1', '2n'], 'Ước lượng không chệch.')
    C('P(A ∩ B) = P(A)P(B) khi', 'A, B độc lập', ['A, B xung khắc', 'A, B đối lập', 'luôn luôn'], 'Định nghĩa độc lập.')
    C('Số cách chọn 3 người từ 10 người là', '120', ['720', '30', '1000'], 'C(10, 3) = 120.')
    C('Với X ~ B(10, 0.4), kỳ vọng là', '4', ['0.4', '2.4', '10'], 'np.')
    C('Với X ~ B(10, 0.4), phương sai là', '2.4', ['4', '0.24', '6'], 'np(1 − p).')
    C('Nếu X ~ N(100, 15²) thì P(X > 100) bằng', '0.5', ['0', '1', '0.84'], 'Đối xứng quanh μ.')
    C('Nhân mọi số liệu với 2 thì trung vị', 'nhân với 2', ['không đổi', 'cộng 2', 'bình phương'], 'Tính chất tuyến tính.')
    C('Hai biến cố xung khắc với P(A) > 0, P(B) > 0', 'không độc lập', ['độc lập', 'đối lập', 'bằng nhau'], 'P(AB) = 0.')
    C('Để khoảng tin cậy hẹp hơn nên', 'tăng cỡ mẫu', ['tăng độ tin cậy', 'giảm cỡ mẫu', 'tăng σ'], 'Sai số chuẩn giảm.')
    C('MLE của p cho mẫu Bernoulli k/n là', 'k/n', ['n/k', 'k·n', '(n − k)/n'], 'Đạo hàm log-likelihood.')
    C('Nếu Y = 3X + 5 thì Var(Y) =', '9Var(X)', ['3Var(X) + 5', '9Var(X) + 5', '3Var(X)'], 'a²Var.')
    C('Hàm mật độ f(x) thỏa', '∫f(x)dx = 1', ['f(x) ≤ 1', 'f(x) = P(X = x)', 'f đơn điệu'], 'Chuẩn hóa.')
    C('Poisson xấp xỉ nhị thức khi', 'n lớn, p nhỏ', ['n nhỏ, p lớn', 'p = 0.5', 'n = 2'], 'μ = np.')
    C('Độ tin cậy 95% ⇒ giá trị tới hạn hai phía là', '1.96', ['1.645', '2.576', '1.28'], 'U₀.₀₂₅.')
