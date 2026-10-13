from hx import *
from math import comb

def m_(t): return f'\\({t}\\)'

def module():
    parts = []
    s = []
    s.append(sl('<p>Xác suất là con số trong [0, 1] đo khả năng một biến cố xảy ra. Module này dạy: định nghĩa cổ điển, tiên đề, quy tắc bù/cộng, <b>xác suất có điều kiện</b>, công thức nhân và <b>độc lập</b> — cùng nền tảng tính hầu hết xác suất ở đề thi.</p>'
                + ul(['Định nghĩa cổ điển P(A) = |A|/|S| và định nghĩa tần suất', 'Ba tiên đề, quy tắc bù và quy tắc cộng', 'P(A | B), công thức nhân, rút có/không hoàn lại', 'Độc lập: từng đôi và toàn phần; hệ nối tiếp/song song']),
                'MODULE 3 · Bài học 1 · Chương 1, mục 1.4–1.5 · Kreyszig §24.3', 'Xác suất, xác suất có điều kiện và độc lập',
                explain='“Xác suất 0.3” nghĩa là nếu lặp lại phép thử rất nhiều lần, khoảng 30% lần sẽ xảy ra. Xác suất có điều kiện là xác suất sau khi đã biết thêm một thông tin.'))
    s.append(sl(formula('Hai cách định nghĩa', 'P(A)=\\dfrac{\\operatorname{card}(A)}{\\operatorname{card}(S)}\\ (\\text{đồng khả năng}),\\qquad P_{\\text{rel}}(A)=\\dfrac{\\text{số lần }A\\text{ xảy ra}}{\\text{số phép thử}}',
                        [('card', 'số điểm mẫu'), ('P_{\\text{rel}}', 'tần suất: xấp xỉ, tiến về P(A) khi số phép thử → ∞')])
                + formula('Ba tiên đề', '0\\le P(A)\\le 1,\\qquad P(S)=1,\\qquad A\\cap B=\\varnothing\\Rightarrow P(A\\cup B)=P(A)+P(B)')
                + '<p>Ví dụ 1.14: gieo súc sắc, P({1,3,5}) = 3/6 = 1/2; P({5,6}) = 2/6 = 1/3.</p>', 'PHẦN 1 · Nền tảng', 'Định nghĩa và tiên đề',
                explain='Định nghĩa cổ điển chỉ dùng khi các kết cục “công bằng như nhau” (súc sắc, đồng xu cân đối). Khi không đối xứng, ta ước lượng xác suất bằng tần suất.'))
    s.append(sl(sim('lln'), 'PHẦN 1 · Nền tảng', 'Thực hành: luật số lớn'))
    parts.append(dict(title='Nền tảng', bullets=['Định nghĩa cổ điển và tần suất', 'Ba tiên đề', 'Luật số lớn (mô phỏng)'], slides=s))

    s = []
    s.append(sl(formula('Quy tắc bù và cộng', 'P(A^c)=1-P(A),\\qquad P(A\\cup B)=P(A)+P(B)-P(A\\cap B)',
                        [('A^c', 'biến cố đối'), ('A\\cap B', 'phần giao bị đếm hai lần')]) + callout('good', 'Mẹo “ít nhất một”', 'P(ít nhất một) = 1 − P(không có cái nào). Ví dụ 1.15: tung 5 đồng xu, P(ít nhất 1 sấp) = 1 − 1/32 = 31/32.'),
                'PHẦN 2 · Phương pháp', 'Quy tắc bù và quy tắc cộng',
                explain='Nếu “ít nhất một” phải xét nhiều trường hợp, hãy đếm trường hợp đối lập duy nhất: “không có cái nào”, rồi lấy 1 trừ đi.'))
    s.append(sl(formula('Xác suất có điều kiện và công thức nhân', 'P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)},\\qquad P(A\\cap B)=P(A)\\,P(B\\mid A)=P(B)\\,P(A\\mid B)', [('P(A\\mid B)', 'xác suất của A khi biết B đã xảy ra (P(B)>0)')])
                + '<p>Biết B nên không gian mẫu thu hẹp từ S xuống B và A thu hẹp thành A ∩ B. Ví dụ 1.18: lớp 30 bạn, bạn tên Thanh: P(Thanh | nữ) = (1/30)/(17/30) = 1/17 nhưng P(nữ | Thanh) = (1/30)/(3/30) = 1/3.</p>', 'PHẦN 2 · Phương pháp', 'Xác suất có điều kiện',
                explain='P(A|B) và P(B|A) khác nhau: “biết là nữ thì tên Thanh” (1/17) khác “biết tên Thanh thì là nữ” (1/3).'))
    s.append(sl(formula('Độc lập', 'A,B\\text{ độc lập}\\iff P(A\\cap B)=P(A)P(B)\\iff P(A\\mid B)=P(A)', [('A,B,C', 'độc lập toàn phần nếu đúng cả 3 cặp và P(A∩B∩C)=P(A)P(B)P(C)')])
                + callout('warn', 'Xung khắc ≠ độc lập', 'Hai biến cố xung khắc có xác suất dương không bao giờ độc lập: biết A xảy ra thì chắc chắn B không xảy ra.')
                + '<p>Hệ <b>nối tiếp</b>: hoạt động ⇔ mọi bộ phận hoạt động ⇒ nhân xác suất. Hệ <b>song song</b>: hỏng ⇔ mọi bộ phận hỏng ⇒ 1 − ∏(1 − pᵢ).</p>', 'PHẦN 2 · Phương pháp', 'Sự kiện độc lập và độ tin cậy hệ thống',
                explain='Độc lập nghĩa là thông tin về A không thay đổi xác suất của B. Hai lần tung đồng xu độc lập; rút bi không hoàn lại thì không độc lập.'))
    s.append(sl(sim('cond'), 'PHẦN 2 · Phương pháp', 'Thực hành: bảng 2×2, P(A|B) và kiểm tra độc lập'))
    parts.append(dict(title='Phương pháp', bullets=['Bù và cộng', 'Có điều kiện, nhân', 'Độc lập, nối tiếp/song song', 'Widget 2×2'], slides=s))

    s = []
    s.append(sl(callout('info', 'Ví dụ 1.19 (có/không hoàn lại)', 'Hộp 10 đinh ốc có 3 cái lỗi; lấy lần lượt 2 cái. Xác suất cả hai không lỗi?')
                + table(['Cách lấy', 'P(B | A)', 'P(A ∩ B)'], [['Có hoàn lại (độc lập)', '7/10', '(7/10)(7/10) = 0.49'], ['Không hoàn lại', '6/9', '(7/10)(6/9) = 0.4667']])
                + '<p>Không hoàn lại thì sau lần đầu chỉ còn 9 ốc, trong đó 6 ốc tốt ⇒ P(B | A) = 6/9.</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 1: có hoàn lại và không hoàn lại'))
    s.append(sl(callout('info', 'Bài 1.14 (Lecture Notes)', 'Lớp 30 HS: 4 giỏi, 8 khá, 10 trung bình, 8 yếu. Chọn 3 người.')
                + table(['Biến cố', 'Phép tính', 'Xác suất'], [['Cả 3 yếu', 'C(8,3)/C(30,3) = 56/4060', '0.0138'], ['Ít nhất 1 giỏi', '1 − C(26,3)/C(30,3) = 1 − 2600/4060', '0.3596'], ['Đúng 1 giỏi', 'C(4,1)C(26,2)/C(30,3) = 1300/4060', '0.3202']]),
                'PHẦN 3 · Ví dụ', 'Ví dụ 2: chọn 3 học sinh'))
    s.append(sl(callout('info', 'Kreyszig PS 24.3/15', 'Cách nào cho xác suất trúng ít nhất một lần lớn nhất?')
                + table(['Chiến lược', 'Xác suất ít nhất một lần'], [['(a) p = 1/2, 1 phát', '0.5000'], ['(b) p = 1/4, 2 phát', '1 − (3/4)² = 0.4375'], ['(c) p = 1/8, 4 phát', '1 − (7/8)⁴ = 0.4138']])
                + '<p>Dù “tổng khả năng” đều là 1/2, chiến lược (a) tốt nhất vì nhiều phát độc lập có thể trùng nhau (không loại trừ).</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 3: ba chiến lược bắn'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Có/không hoàn lại', 'Chọn 3 học sinh', 'Ba chiến lược bắn'], slides=s))

    s = []
    s.append(sl(ul(['<b>Nhầm P(A|B) với P(B|A)</b> (Thanh/nữ: 1/17 so với 1/3).', '<b>Xung khắc = độc lập</b>: sai; xung khắc dương ⇒ phụ thuộc.', '<b>Quên hoàn lại hay không</b>: mẫu số giảm sau mỗi lần rút không hoàn lại.', '<b>Chia xác suất lỗi</b>: (1 − q)³ = 0.95 cho q = 0.01695, không phải 0.05/3.', '<b>Độc lập từng đôi ≠ độc lập toàn phần</b> (4 chip của Kreyszig 24.3/16).', '<b>Cộng xác suất của hai biến cố không xung khắc</b> mà không trừ giao.']),
                'PHẦN 4 · Bẫy và mở rộng', 'Sáu bẫy thường gặp'))
    s.append(sl(callout('info', 'Kreyszig 24.3/16: độc lập từng đôi nhưng không toàn phần', 'Rút một chip trong {000, 011, 101, 110}; A, B, C: chữ số 1, 2, 3 bằng 1. P(A) = P(B) = P(C) = 1/2; mọi giao hai biến cố = 1/4 = (1/2)²; nhưng A ∩ B ∩ C = ∅ ⇒ 0 ≠ 1/8.'), 'PHẦN 4 · Bẫy và mở rộng', 'Phản ví dụ về độc lập'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Sáu bẫy', 'Phản ví dụ 4 chip'], slides=s))

    s = []
    s.append(sl('<p><b>Độ tin cậy hệ thống.</b> Một bộ cảm biến gồm hai bộ phận nối tiếp có xác suất hoạt động 0.95 và 0.98: cả hệ hoạt động với xác suất 0.931. Thêm một bộ phận dự phòng song song (0.95) cho nhánh yếu nhất làm xác suất hỏng của nhánh giảm từ 0.05 xuống 0.0025. Quy tắc nhân (nối tiếp) và 1 − ∏(1 − pᵢ) (song song) là cơ sở của thiết kế dự phòng (redundancy).</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: thiết kế dự phòng'))
    s.append(sl(ul(['P(Aᶜ) = 1 − P(A); P(A ∪ B) = P(A) + P(B) − P(A ∩ B).', 'P(A|B) = P(A ∩ B)/P(B); P(A ∩ B) = P(A)P(B|A).', 'Độc lập ⇔ P(A ∩ B) = P(A)P(B); xung khắc ≠ độc lập.', 'Ít nhất một ⇒ biến cố bù.']) + callout('good', 'Tiếp theo', 'Module 4: công thức xác suất toàn phần và công thức Bayes.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Thiết kế dự phòng', 'Tổng kết'], slides=s))

    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §1.4 gồm định nghĩa cổ điển (1.10) và tần suất (1.11), ba tiên đề (1.12–1.14), quy tắc bù (Định lý 1.1), quy tắc cộng cho biến cố xung khắc (Định lý 1.2) và tổng quát (Định lý 1.3). §1.5 trình bày xác suất có điều kiện (1.19), công thức nhân (1.21), độc lập (1.22–1.23). Kreyszig §24.3 cho cùng nội dung; <b>Problem Set 24.3</b> có 19 bài (1–15 tính toán, 16–19 lý thuyết).</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Bài 1.15: hai súc sắc, điều kiện tổng chẵn', '<p>Biết tổng hai súc sắc là số chẵn, tìm xác suất tổng bằng 6 (Bài 1.15).</p>' + steps(['Số kết cục có tổng chẵn: 18 (một nửa của 36).', 'Có 5 kết cục tổng 6: (1,5), (2,4), (3,3), (4,2), (5,1).', 'P = 5/18 ≈ 0.2778.']))
    notes += ex('2. Bài 1.16: tính xác suất lỗi mỗi thiết bị', '<p>3 thiết bị đóng ngắt giống nhau nối tiếp; xác suất mạch làm việc là 0.95.</p>' + steps([m_('(1-q)^3=0.95'), m_('1-q=0.95^{1/3}=0.98305'), m_('q\\approx 0.01695')]) + '<p>Chú ý q ≠ 0.05/3 = 0.01667.</p>')
    notes += ex('3. Kreyszig PS 24.3/11: 200 thanh sắt', '<p>50 quá khổ, 50 thiếu khổ, 100 đạt; rút 2 không hoàn lại.</p>' + table(['Biến cố', 'Phép tính', 'Xác suất'], [['Cả hai đạt', '(100/200)(99/199)', '0.2487'], ['Đúng một đạt', '2(100/200)(100/199)', '0.5025'], ['Không đạt', '(100/200)(99/199)', '0.2487']]) + '<p>Tổng 0.2487 + 0.5025 + 0.2487 = 1.</p>')
    notes += ex('4. Kreyszig PS 24.3/14: bugi lỗi 2%', '<p>Mỗi nửa giờ kiểm tra 2 bugi độc lập.</p>' + table(['Số lỗi', 'Phép tính', 'Xác suất'], [['0', '0.98²', '0.9604'], ['1', '2·0.02·0.98', '0.0392'], ['2', '0.02²', '0.0004']]) + '<p>Tổng bằng 1 — đây là mầm của phân phối nhị thức (Module 6).</p>')
    notes += ex('5. Đề giữa kỳ mẫu, câu 3–4', '<p>P(Ā) = 1 − 0.57 = 0.43. Xạ thủ bắn trúng 0.57; bắn đúng 3 lần trong 3 lần (độc lập): 0.57³ = 0.185193.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('lln') + sim('cond')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Từ cờ bạc đến tiên đề', 'Pascal–Fermat (1654) và Huygens (1657) đặt nền; Laplace phát biểu định nghĩa cổ điển (1812); Kolmogorov (1933) công bố hệ tiên đề chặt chẽ dựa trên lý thuyết độ đo. Bernoulli chứng minh dạng đầu của luật số lớn (1713): tần suất tiến về xác suất.')
    notes += '<h2>5. Case study</h2><p>Dây chuyền kiểm tra bugi (Kreyszig 24.3/14): tỉ lệ lỗi 2%, kiểm tra 2 bugi mỗi nửa giờ. Xác suất cả hai cùng lỗi 0.0004 (cứ khoảng 2500 lần kiểm tra mới có 1 lần) nên nếu thấy hai bugi lỗi liên tiếp, nhiều khả năng tỉ lệ lỗi thực đã tăng — ý tưởng của kiểm định giả thuyết (Chương 3).</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Xác định rõ có hoàn lại hay không.<br>• “Biết rằng …” ⇒ xác suất có điều kiện, thu hẹp không gian mẫu.<br>• Với nhiều biến cố độc lập: P(ít nhất một) = 1 − ∏(1 − pᵢ).')
    return dict(id='m03', slug='m03-xac-suat-dieu-kien-doc-lap', title='Định nghĩa xác suất, xác suất có điều kiện, sự kiện độc lập', subtitle='Định nghĩa cổ điển, tiên đề, bù/cộng, P(A|B), công thức nhân, độc lập, độ tin cậy hệ thống',
                source='Lecture Notes §1.4–1.5, Bài 1.11–1.18 · Kreyszig §24.3 (PS 24.3) · Đề giữa kỳ mẫu câu 3–4', exam='Đề giữa kỳ mẫu câu 3, 4; nền cho Bayes (Câu 1 giữa kỳ HK2 2022–2023)', time='≈ 3 giờ',
                objectives=['Tính xác suất cổ điển bằng phép đếm', 'Dùng biến cố bù cho “ít nhất một”', 'Phân biệt P(A|B), P(B|A) và dùng công thức nhân', 'Kiểm tra độc lập và tính độ tin cậy hệ nối tiếp/song song'], parts=parts, notes=notes, sims=['lln', 'cond'])
