from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Nhiều bài toán cho ta <b>xác suất theo từng nguồn</b> (mỗi phân xưởng, mỗi loại bệnh, mỗi loại tín hiệu) và hỏi <b>xác suất chung</b> (toàn phần) hoặc <b>xác suất ngược</b> (Bayes): biết kết quả B, nguồn nào nhiều khả năng nhất?</p>' + ul(['Hệ đầy đủ các biến cố {A₁, …, Aₙ}', 'Công thức xác suất toàn phần P(B) = ΣP(B|Aᵢ)P(Aᵢ)', 'Công thức Bayes (hậu kiểm) P(Aᵢ|B)', 'Cây xác suất hai giai đoạn']),
                'MODULE 4 · Bài học 1 · Chương 1, mục 1.6 (Lecture Notes)', 'Xác suất toàn phần và công thức Bayes',
                explain='Toàn phần = đi từ nguyên nhân đến kết quả (cộng các nhánh). Bayes = đi ngược từ kết quả về nguyên nhân (chia nhánh liên quan cho tổng).'))
    s.append(sl(formula('Hệ đầy đủ', 'A_i\\cap A_j=\\varnothing\\ (i\\ne j),\\qquad A_1\\cup A_2\\cup\\dots\\cup A_n=S', [('\\{A,A^c\\}', 'luôn là hệ đầy đủ với mọi biến cố A')])
                + '<p>Ví dụ: “sản phẩm do phân xưởng 1, 2 hoặc 3 sản xuất” — mỗi sản phẩm thuộc đúng một phân xưởng; hay “bộ phận I/II chạy hay hỏng” (4 khả năng, ví dụ 1.21).</p>', 'PHẦN 1 · Nền tảng', 'Hệ đầy đủ các sự kiện (Định nghĩa 1.6)'))
    parts.append(dict(title='Nền tảng', bullets=['Vì sao cần toàn phần và Bayes', 'Hệ đầy đủ'], slides=s))
    s = []
    s.append(sl(formula('Công thức xác suất toàn phần', 'P(B)=\\sum_{i=1}^n P(B\\cap A_i)=\\sum_{i=1}^n P(B\\mid A_i)\\,P(A_i)', [('P(A_i)', 'xác suất tiên nghiệm (prior)'), ('P(B\\mid A_i)', 'xác suất có điều kiện (likelihood)')]) + '<p>Ví dụ 1.20: ba nhà máy 35%, 45%, 20% với tỉ lệ phế phẩm 1%, 0.5%, 0.2% ⇒ P(B) = 0.0035 + 0.00225 + 0.0004 = 0.00615.</p>', 'PHẦN 2 · Phương pháp', 'Xác suất toàn phần',
                explain='Một phế phẩm có thể đến từ nhà máy nào cũng được; ta cộng “xác suất đến từ nhà máy i và là phế phẩm” cho cả ba nhà máy.'))
    s.append(sl(formula('Công thức Bayes (hậu kiểm)', 'P(A_i\\mid B)=\\dfrac{P(B\\mid A_i)\\,P(A_i)}{\\sum_{j=1}^n P(B\\mid A_j)\\,P(A_j)}', [('P(A_i\\mid B)', 'xác suất hậu nghiệm sau khi quan sát B')]) + callout('good', 'Kiểm tra nhanh', 'Các hậu nghiệm P(Aᵢ | B) luôn có tổng bằng 1. Mẫu số chính là P(B) vừa tính bằng công thức toàn phần.'), 'PHẦN 2 · Phương pháp', 'Công thức Bayes',
                explain='Bayes cập nhật niềm tin: trước khi biết, xác suất “do nhà máy II” là 45%; sau khi biết sản phẩm là phế phẩm, xác suất đó được tính lại theo tỉ lệ phế phẩm của từng nhà máy (nhà máy II: 0.00225/0.00615 = 36.6%).'))
    s.append(sl(diag('../../img/m04.png', 'Cây xác suất hai giai đoạn', 'Cây xác suất cho đáp án giữa kỳ HK2 2022–2023 câu 1: nhân dọc theo nhánh, cộng các nhánh B, chia để ra hậu nghiệm.'), 'PHẦN 2 · Phương pháp', 'Cây xác suất hai giai đoạn'))
    s.append(sl(sim('bayes'), 'PHẦN 2 · Phương pháp', 'Thực hành: máy tính toàn phần và Bayes'))
    parts.append(dict(title='Phương pháp', bullets=['Toàn phần', 'Bayes', 'Cây xác suất', 'Máy tính tương tác'], slides=s))
    s = []
    s.append(sl(callout('info', 'Bài 1.23 (Lecture Notes)', 'Pít-tông: phân xưởng I, II, III sản xuất 40%, 35%, 25% với phế phẩm 5%, 8%, 4%.') + steps([m_('P(B)=0.4\\cdot0.05+0.35\\cdot0.08+0.25\\cdot0.04=0.058'), m_('P(A_2\\mid B)=\\dfrac{0.35\\cdot0.08}{0.058}=0.4828')]) + '<p>Các hậu nghiệm: I = 0.3448, II = 0.4828, III = 0.1724 (tổng 1).</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 1: ba phân xưởng pít-tông'))
    s.append(sl(callout('info', 'Ví dụ 1.21 (Lecture Notes)', 'Hai bộ phận nối tiếp chạy với xác suất 0.95 và 0.98; thấy mạch ngừng.') + table(['Biến cố', 'Xác suất', 'Mạch ngừng?', 'Hậu nghiệm'], [['A₁ cả hai chạy', '0.931', '0', '0'], ['A₂ chỉ II hỏng', '0.019', '1', '19/69 = 0.2754'], ['A₃ chỉ I hỏng', '0.049', '1', '49/69 = 0.7101'], ['A₄ cả hai hỏng', '0.001', '1', '1/69 = 0.0145']]), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: nguyên nhân mạch ngừng'))
    s.append(sl(callout('info', 'Đáp án giữa kỳ HK2 2022–2023, câu 1', 'P(A) = 0.45, 0.25, 0.3; P(B | A) = 0.636, 0.444, 0.7.') + steps(['Hệ đầy đủ ⇒ P(B) = 0.2862 + 0.1110 + 0.2100 = 0.6072 ≈ 0.607.', 'Bayes: P(A₂ | B) = 0.1110/0.6072 = 0.1828 ≈ 0.183.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 3: câu Bayes của đề giữa kỳ'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Pít-tông', 'Mạch ngừng', 'Đề giữa kỳ'], slides=s))
    s = []
    s.append(sl(ul(['<b>Quên kiểm tra hệ đầy đủ</b>: ΣP(Aᵢ) phải bằng 1.', '<b>Nhầm P(B|A) với P(A|B)</b>: xét nghiệm “nhạy 95%” không có nghĩa dương tính ⇒ 95% có bệnh.', '<b>Bỏ qua tỉ lệ nền</b>: bệnh hiếm thì phần lớn dương tính là dương tính giả.', '<b>Mẫu số của Bayes</b> phải là P(B) đầy đủ, không phải chỉ một số hạng.', '<b>Làm tròn quá sớm</b>: giữ ≥ 4 chữ số trong các bước trung gian (đề yêu cầu ≥ 3 chữ số).']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    s.append(sl(sim('freq'), 'PHẦN 4 · Bẫy và mở rộng', 'Mở rộng: tần suất tự nhiên (10 000 người)'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy', 'Tần suất tự nhiên'], slides=s))
    s = []
    s.append(sl('<p><b>Xét nghiệm bệnh hiếm.</b> Bệnh mắc 1%, độ nhạy 95%, độ đặc hiệu 90%. Trong 10 000 người có 100 người bệnh (95 dương tính) và 9 900 người khỏe (990 dương tính giả). Trong 1 085 người dương tính chỉ có 95 người thật sự bệnh: P(bệnh | +) = 8.8%. Đây là lý do y tế dùng xét nghiệm thứ hai khi sàng lọc bệnh hiếm; cùng cấu trúc với bộ lọc thư rác và nhận dạng tín hiệu.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: xét nghiệm sàng lọc'))
    s.append(sl(ul(['Kiểm tra hệ đầy đủ rồi dùng toàn phần.', 'Bayes = (tích nhánh cần)/(tổng các tích).', 'Vẽ cây xác suất để không sót nhánh.', 'Kiểm tra: hậu nghiệm cộng lại bằng 1.']) + callout('good', 'Tiếp theo', 'Module 5: biến ngẫu nhiên, hàm phân phối, kỳ vọng và phương sai.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Xét nghiệm sàng lọc', 'Tổng kết'], slides=s))
    from notes_m04 import notes as _nt; notes = _nt()
    return dict(id='m04', slug='m04-toan-phan-bayes', title='Công thức xác suất toàn phần và công thức Bayes', subtitle='Hệ đầy đủ, xác suất toàn phần, Bayes (hậu kiểm), cây xác suất',
                source='Lecture Notes §1.6 (Ví dụ 1.20–1.22, Bài 1.19–1.23) · Đề giữa kỳ mẫu câu 5 · Đáp án giữa kỳ HK2 2022–2023 câu 1', exam='Câu 1 đề giữa kỳ HK2 2022–2023 (Bayes ba phân xưởng); câu 5 đề giữa kỳ mẫu', time='≈ 2 giờ',
                objectives=['Nhận ra hệ đầy đủ và dùng xác suất toàn phần', 'Tính hậu nghiệm bằng công thức Bayes', 'Vẽ cây xác suất hai giai đoạn', 'Giải thích sai lầm tỉ lệ nền khi xét nghiệm bệnh hiếm'], parts=parts, notes=notes, sims=['bayes', 'freq'])
