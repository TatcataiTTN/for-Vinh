from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Biến ngẫu nhiên (BNN) biến kết quả thực nghiệm thành <b>con số</b> để tính toán. Module này gồm: BNN rời rạc và liên tục, hàm xác suất/mật độ, hàm phân phối F(x), kỳ vọng, phương sai, độ lệch chuẩn và phân vị — nền của mọi phân phối ở Module 6 và của ước lượng, kiểm định.</p>'
                + ul(['BNN là hàm X: S → ℝ; rời rạc và liên tục', 'Bảng phân phối, hàm xác suất; mật độ f(x)', 'Hàm phân phối F(x) = P(X ≤ x)', 'E(X), Var(X), σ; trung vị và phân vị']),
                'MODULE 5 · Bài học 1 · Chương 1, mục 1.7–1.9 · Kreyszig §24.5–24.6', 'Biến ngẫu nhiên và các đặc trưng', explain='Gieo súc sắc xong, X = “số chấm” là một con số ngẫu nhiên. Ta không biết trước X nhưng biết X nhận giá trị nào với xác suất bao nhiêu.'))
    s.append(sl(table(['', 'Rời rạc', 'Liên tục'], [['Giá trị', 'hữu hạn / đếm được', 'lấp đầy một khoảng'], ['Mô tả', 'bảng p(xᵢ), f(x) = P(X = x)', 'mật độ f(x) ≥ 0'], ['Chuẩn hóa', 'Σ f(xᵢ) = 1', '∫ f(x)dx = 1'], ['Xác suất khoảng', 'cộng các f(xᵢ)', 'diện tích dưới f; P(X = a) = 0'], ['Hàm phân phối', 'bậc thang', 'liên tục, F′ = f']]) + formula('Hàm phân phối', 'F(x)=P(X\\le x),\\quad P(a<X\\le b)=F(b)-F(a),\\quad f(x)=F\'(x)'),
                'PHẦN 1 · Nền tảng', 'Rời rạc và liên tục', explain='Rời rạc: đếm được (số điểm xạ thủ). Liên tục: đo được (thời gian, khoảng cách) — xác suất của một giá trị chính xác bằng 0, chỉ khoảng mới có xác suất.'))
    s.append(sl(sim('rv'), 'PHẦN 1 · Nền tảng', 'Thực hành: bảng phân phối → E(X), Var(X), F(x)'))
    parts.append(dict(title='Nền tảng', bullets=['BNN rời rạc và liên tục', 'Hàm phân phối', 'Widget rời rạc'], slides=s))
    s = []
    s.append(sl(formula('Kỳ vọng và phương sai', '\\mu=E(X)=\\sum_j x_jf(x_j)\\ \\text{hoặc}\\ \\int_{-\\infty}^{\\infty}xf(x)dx,\\qquad \\sigma^2=E[(X-\\mu)^2]=E(X^2)-\\mu^2',
                        [('\\mu', 'giá trị trung bình dài hạn'), ('\\sigma^2', 'độ phân tán bình phương; \\(\\sigma=\\sqrt{\\sigma^2}\\)')]) + formula('Biến đổi tuyến tính', 'E(aX+b)=a\\,E(X)+b,\\qquad \\operatorname{Var}(aX+b)=a^2\\operatorname{Var}(X)'), 'PHẦN 2 · Phương pháp', 'Kỳ vọng và phương sai',
                explain='Kỳ vọng là “tâm khối” của phân phối; phương sai đo mức tản mác. Cộng hằng số dịch tâm nhưng không đổi độ tản mác.'))
    s.append(sl(callout('info', 'Quy trình cho mật độ f(x) cho trước (đề thi HK2)', '1) Kiểm tra ∫f = 1 (nếu thiếu hằng số k thì tìm k). 2) E(X) = ∫xf. 3) Trung vị m: giải F(m) = 0.5. 4) Var = ∫x²f − μ².')
                + '<p>Ví dụ: f(x) = 6(1 − x)x, 0 ≤ x ≤ 1: ∫ = 6(1/2 − 1/3) = 1 ✓; E(X) = 6(1/3 − 1/4) = 1/2; F(m) = 3m² − 2m³ = 1/2 ⇒ m = 1/2 (đối xứng).</p>', 'PHẦN 2 · Phương pháp', 'Giải bài mật độ'))
    s.append(sl(sim('pdf'), 'PHẦN 2 · Phương pháp', 'Thực hành: mật độ, diện tích, kỳ vọng, trung vị'))
    parts.append(dict(title='Phương pháp', bullets=['Kỳ vọng, phương sai', 'Quy trình với mật độ', 'Widget liên tục'], slides=s))
    s = []
    s.append(sl(callout('info', 'Đề 2TC (HK1 2022–2023), đề số 1, câu 1', 'X = 0..5 với P = 0.10, 0.20, 0.25, 0.35, 0.06, 0.04.') + steps([m_('E(X)=0\\cdot0.10+1\\cdot0.20+2\\cdot0.25+3\\cdot0.35+4\\cdot0.06+5\\cdot0.04=2.19'), m_('E(X^2)=0.2+1.0+3.15+0.96+1.0=6.31'), m_('\\operatorname{Var}(X)=6.31-2.19^2=1.5139')]), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: số điểm của xạ thủ'))
    s.append(sl(callout('info', 'Đề HK2 (3TC), câu 5', 'f(x) = 0.75(2 − x)x, 0 ≤ x ≤ 2.') + steps(['Chuẩn hóa: 0.75(4 − 8/3) = 1 ✓.', 'E(X) = 0.75∫₀²(2x² − x³)dx = 0.75(16/3 − 4) = 1.', 'Trung vị: F(m) = 0.75(m² − m³/3) = 0.5 ⇒ m = 1 (đối xứng qua x = 1).']), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: mật độ đối xứng'))
    s.append(sl(callout('info', 'Đáp án giữa kỳ HK2, câu 2', 'T ∈ {0, 1, 2, 3}: P = 0.28; 0.1332; 0.3648; 0.222 (m = 0.222).') + steps(['P(0.5 < T < 2.5) = 0.1332 + 0.3648 = 0.498.', 'E(T) = 0.1332 + 0.7296 + 0.666 = 1.5288.', 'σ² = Σ(xᵢ − μ)²pᵢ = 1.2532.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 3: bảng phân phối có tham số (giữa kỳ)'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Số điểm xạ thủ', 'Mật độ đối xứng', 'Bảng phân phối giữa kỳ'], slides=s))
    s = []
    s.append(sl(ul(['<b>Quên chuẩn hóa</b>: kiểm tra Σp = 1 hoặc ∫f = 1 (tìm k trước).', '<b>Var = E(X²) − μ²</b>, không phải E(X²) − E(X) hay E(X) − E(X²).', '<b>Mật độ f(x) có thể &gt; 1</b> (không phải xác suất); P(X = a) = 0 nhưng f(a) có thể dương.', '<b>Cận tích phân</b>: chỉ lấy trên miền f ≠ 0.', '<b>Biến đổi tuyến tính</b>: Var(aX + b) = a²Var(X), không cộng b.']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    s.append(sl(formula('Mô-men mở rộng', 'E(g(X))=\\sum g(x_j)f(x_j)\\ \\text{hoặc}\\ \\int g(x)f(x)dx,\\quad E(X^k),\\ E[(X-\\mu)^k]', [('E[(X-\\mu)^3]/\\sigma^3', 'hệ số bất đối xứng (skewness) — bằng 0 khi phân phối đối xứng')]) + '<p>Kreyszig PS 24.6/19: f(0) = f(3) = 1/8, f(1) = f(2) = 3/8 ⇒ E(X³) = (0 + 3 + 24 + 27)/8 = 6.75.</p>', 'PHẦN 4 · Bẫy và mở rộng', 'Kỳ vọng của g(X) và mô-men'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy', 'Mô-men'], slides=s))
    s = []
    s.append(sl('<p><b>Định giá kỳ vọng.</b> Cửa hàng máy lạnh (Kreyszig PS 24.6/13): số máy bán mỗi ngày X ∈ {10, 11, 12, 13} với xác suất 0.1, 0.3, 0.4, 0.2 và lãi $55/máy. E(X) = 11.7 ⇒ lãi kỳ vọng $643.50/ngày. Kỳ vọng dùng để so sánh các phương án dưới bất định (bảo hiểm, kinh doanh, kiểm soát chất lượng); phương sai cho biết rủi ro.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: lãi kỳ vọng mỗi ngày'))
    s.append(sl(ul(['Bảng phân phối: Σp = 1; E = Σxp; Var = Σx²p − μ².', 'Mật độ: ∫f = 1; E = ∫xf; F(m) = 0.5 cho trung vị.', 'Y = aX + b: E = aμ + b, Var = a²σ².']) + callout('good', 'Tiếp theo', 'Module 6: nhị thức, Poisson và phân phối chuẩn.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Lãi kỳ vọng', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §1.7 (khái niệm BNN, Định nghĩa 1.7), §1.8 (bảng phân phối, hàm phân phối, hàm mật độ), §1.9 (kỳ vọng, phương sai, độ lệch chuẩn). Kreyszig §24.5 (hàm xác suất/mật độ và F, PS 24.5 gồm 15 bài) và §24.6 (kỳ vọng, phương sai, mô-men, PS 24.6 gồm 20 bài). Bài 1.24–1.31 của giáo trình và các câu 1, 5 của đề cuối kỳ được dùng làm câu gốc.</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Bài 1.24 (đã đối chiếu ảnh trang)', '<p>f(x) = k/2ˣ, x = 0, 1, 2, … (văn bản trích tự động làm rơi phân số nên chúng tôi kiểm lại ảnh trang). Σk/2ˣ = 2k = 1 ⇒ k = 1/2. P(X ≥ 4) = Σ_{x≥4} 1/2^{x+1} = 1/16.</p>')
    notes += ex('2. Bài 1.25: hàm phân phối', '<p>f(x) = kx² trên [0, 5]: ∫ = 125k/3 = 1 ⇒ k = 3/125. F(x) = x³/125 với 0 ≤ x ≤ 5 (0 khi x &lt; 0, 1 khi x &gt; 5).</p>')
    notes += ex('3. Bài 1.28 / Kreyszig 24.5/12', '<p>F(x) = (x² − 4)/5 trên [2, 3). Mật độ f = 2x/5. P(2.5 ≤ X ≤ 5) = 1 − F(2.5) = 1 − 0.45 = 0.55.</p>')
    notes += ex('4. Bài 1.30: trạm xăng', '<p>f(x) = 6x(1 − x): μ = 0.5, σ² = 0.05, σ = 0.2236. Dung tích c để P(bán hết) = 5%: F(c) = 3c² − 2c³ = 0.95 ⇒ c ≈ 0.8647 (đơn vị 10 000 gallon).</p>')
    notes += ex('5. Kreyszig PS 24.6/9: mật độ parabol', '<p>f(x) = k(x − 0.9)(1.1 − x): ∫ = 0.2³/6 ⇒ k = 750; μ = 1; σ² = (0.2)²/20 = 0.002; bu-lông lỗi nếu lệch &gt; 0.06 cm: P = 1 − ∫_{0.94}^{1.06} f ≈ 0.2080.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('rv') + sim('pdf')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Kỳ vọng', 'Khái niệm “giá trị kỳ vọng” xuất hiện trong bài toán chia tiền cược của Pascal–Fermat và được Huygens hệ thống hóa (1657). Khái niệm biến ngẫu nhiên và hàm phân phối tổng quát được hoàn thiện bởi Kolmogorov (1933).')
    notes += '<h2>5. Case study</h2><p>Xạ thủ thi bắn (đề 2TC): E(X) = 2.19 điểm, σ = 1.23. Hai xạ thủ có cùng E(X) nhưng σ khác nhau cho kết quả ổn định khác nhau — vì thế tuyển chọn thường xét cả kỳ vọng và phương sai.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Viết rõ công thức rồi thay số; làm tròn ≥ 3 chữ số thập phân.<br>• Với mật độ đối xứng, kỳ vọng = trung vị = tâm đối xứng (kiểm tra nhanh).<br>• Giữ nhiều chữ số ở E(X²) để tránh sai số khi trừ μ².')
    return dict(id='m05', slug='m05-bien-ngau-nhien', title='Biến ngẫu nhiên, hàm phân phối, hàm mật độ, kỳ vọng, phương sai', subtitle='BNN rời rạc/liên tục, bảng phân phối, F(x), f(x), E(X), Var(X), trung vị',
                source='Lecture Notes §1.7–1.9, Bài 1.24–1.31 · Kreyszig §24.5–24.6 (PS 24.5, 24.6) · Đề cuối kỳ 2022–2023 (2TC câu 1, 3TC câu 5) · Đáp án giữa kỳ HK2 câu 2', exam='Câu 1 đề 2TC; Câu 5 đề HK2; Câu 2 giữa kỳ HK2', time='≈ 4 giờ',
                objectives=['Phân biệt BNN rời rạc và liên tục, kiểm tra hàm xác suất/mật độ', 'Tính F(x), P(a < X < b) từ bảng hoặc mật độ', 'Tính E(X), Var(X), σ và trung vị cho cả hai loại', 'Dùng biến đổi tuyến tính của kỳ vọng và phương sai'], parts=parts, notes=notes, sims=['rv', 'pdf'])
