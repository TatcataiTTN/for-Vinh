from hx import *
from scipy import stats as st
def m_(t): return f'\\({t}\\)'
Phi = st.norm.cdf
def module():
    parts = []
    s = []
    s.append(sl('<p>Ba phân phối quan trọng nhất của giáo trình: <b>nhị thức</b> (đếm thành công trong n phép thử), <b>Poisson</b> (đếm biến cố hiếm) và <b>chuẩn</b> (liên tục, trung tâm của thống kê). Câu 1 của mọi đề cuối kỳ là bài chuẩn: tính xác suất và tìm phân vị.</p>' + ul(['B(n, p): μ = np, σ² = np(1 − p)', 'Poisson(μ): μ = σ²; xấp xỉ nhị thức khi p nhỏ', 'N(μ, σ²): chuẩn hóa Z = (X − μ)/σ; bảng A7, A8', 'Xấp xỉ chuẩn của nhị thức (hiệu chỉnh 0.5)']),
                'MODULE 6 · Bài học 1 · Chương 1, mục 1.10 · Kreyszig §24.7–24.8', 'Nhị thức, Poisson và phân phối chuẩn',
                explain='Đếm số lần ra mặt ngửa → nhị thức. Đếm số cuộc gọi đến tổng đài mỗi phút → Poisson. Đo chiều cao, tuổi thọ, sai số → thường xấp xỉ chuẩn.'))
    s.append(sl(formula('Nhị thức X ~ B(n, p)', 'f(x)=P(X=x)=\\binom nx p^x(1-p)^{n-x},\\ x=0,\\dots,n,\\qquad \\mu=np,\\ \\sigma^2=np(1-p)', [('n', 'số phép thử độc lập'), ('p', 'xác suất thành công mỗi lần')])
                + '<p>Ví dụ 1.29: tung súc sắc 4 lần, P(ít nhất hai mặt sáu) = f(2) + f(3) + f(4) = 171/1296 ≈ 13.2%.</p>', 'PHẦN 1 · Nền tảng', 'Phân phối nhị thức',
                explain='Bốn điều kiện: n cố định; mỗi lần chỉ có thành công/thất bại; xác suất p không đổi; các lần độc lập.'))
    s.append(sl(formula('Poisson X ~ P(μ)', 'f(x)=\\dfrac{\\mu^x}{x!}e^{-\\mu},\\ x=0,1,2,\\dots,\\qquad E(X)=\\operatorname{Var}(X)=\\mu', [('\\mu', 'số biến cố trung bình trong khoảng thời gian/không gian xét')])
                + '<p>Ví dụ 1.30: p = 0.01, n = 100 ⇒ μ = np = 1: P(X ≤ 2) ≈ 2.5e⁻¹ = 91.97% (nhị thức đúng: 92.06%).</p>', 'PHẦN 1 · Nền tảng', 'Phân phối Poisson'))
    s.append(sl(sim('binpois'), 'PHẦN 1 · Nền tảng', 'Thực hành: nhị thức so với Poisson và chuẩn'))
    parts.append(dict(title='Nền tảng', bullets=['Nhị thức', 'Poisson', 'Widget so sánh'], slides=s))
    s = []
    s.append(sl(formula('Phân phối chuẩn X ~ N(μ, σ²)', 'f(x)=\\dfrac1{\\sigma\\sqrt{2\\pi}}e^{-\\frac12\\left(\\frac{x-\\mu}\\sigma\\right)^2},\\qquad F(x)=\\Phi\\!\\left(\\dfrac{x-\\mu}\\sigma\\right),\\qquad P(a<X\\le b)=\\Phi\\!\\left(\\dfrac{b-\\mu}\\sigma\\right)-\\Phi\\!\\left(\\dfrac{a-\\mu}\\sigma\\right)',
                        [('\\Phi(z)', 'hàm phân phối chuẩn tắc (bảng A7)'), ('\\Phi(-z)=1-\\Phi(z)', 'đối xứng')]), 'PHẦN 2 · Phương pháp', 'Chuẩn hóa và tra bảng A7',
                explain='Mọi chuẩn đều quy về chuẩn tắc bằng cách đổi X sang Z = (X − μ)/σ (số độ lệch chuẩn so với trung bình).'))
    s.append(sl(callout('info', 'Bài toán ngược: tìm c (bảng A8)', 'P(X ≤ c) = p ⇒ c = μ + σ·z_p, với z_p = Φ⁻¹(p). Hai chiều: P(μ − k < X < μ + k) = γ ⇒ Φ(k/σ) = (1 + γ)/2.')
                + table(['Xác suất', 'z', 'Dùng cho'], [['0.90', '1.282', 'P(X ≤ c) = 90%'], ['0.95', '1.645', 'một phía 5%; khoảng hai phía 90%'], ['0.975', '1.960', 'khoảng hai phía 95%'], ['0.99', '2.326', 'một phía 1%'], ['0.995', '2.576', 'hai phía 99%']])
                + '<p>Câu 1(b) đề HK2: P(X ≥ c) = 1% ⇒ Φ((c − 12.5)/0.809) = 0.99 ⇒ c = 12.5 + 2.326·0.809 = 14.382.</p>', 'PHẦN 2 · Phương pháp', 'Phân vị: bảng A8 (z)'))
    s.append(sl(sim('normcalc'), 'PHẦN 2 · Phương pháp', 'Thực hành: máy tính phân phối chuẩn'))
    s.append(sl(formula('Xấp xỉ chuẩn của nhị thức', 'P(a\\le X\\le b)\\approx\\Phi(\\beta)-\\Phi(\\alpha),\\quad \\alpha=\\dfrac{a-np-0.5}{\\sqrt{np(1-p)}},\\ \\beta=\\dfrac{b-np+0.5}{\\sqrt{np(1-p)}}', [('\\pm0.5', 'hiệu chỉnh liên tục (rời rạc → liên tục)')]) + '<p>Điều kiện: np &gt; 5 và n(1 − p) &gt; 5. Ví dụ 1.33: n = 400, p = 0.8: μ = 320, σ = 8; P(300 ≤ X ≤ 360) ≈ 0.9948.</p>', 'PHẦN 2 · Phương pháp', 'Xấp xỉ chuẩn của nhị thức'))
    parts.append(dict(title='Phương pháp', bullets=['Chuẩn hóa và bảng A7', 'Phân vị: bảng A8', 'Widget chuẩn', 'Xấp xỉ chuẩn'], slides=s))
    s = []
    s.append(sl(callout('info', 'Đề HK2 (3TC) đề số 1, câu 1', 'X ~ N(12.5; 0.809²) — tuổi thọ muỗi (ngày).') + steps([m_('z=\\dfrac{13.7135-12.5}{0.809}=1.5\\Rightarrow P(X\\le13.7135)=\\Phi(1.5)=0.9332'), m_('P(X\\ge c)=0.01\\Rightarrow \\Phi\\!\\left(\\tfrac{c-12.5}{0.809}\\right)=0.99\\Rightarrow \\tfrac{c-12.5}{0.809}=2.326'), m_('c=12.5+2.326\\cdot0.809=14.382')]), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: câu 1 đề cuối kỳ'))
    s.append(sl(callout('info', 'Đề mẫu 03/2024, đề số 1, câu 1', 'X ~ N(μ = 8.3; σ² = 0.16), σ = 0.4. Tìm a = P(X ≤ 8.9) và b = P(X ≥ 8.78).') + steps(['z = (8.9 − 8.3)/0.4 = 1.5 ⇒ a = Φ(1.5) = 0.9332.', 'z = (8.78 − 8.3)/0.4 = 1.2 ⇒ b = 1 − Φ(1.2) = 1 − 0.8849 = 0.1151.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: đề mẫu 2024'))
    s.append(sl(callout('info', 'Đáp án giữa kỳ HK2, câu 3', 'X ~ N(44.4; 7.12²). Tỉ lệ P(44.4 ≤ X ≤ 51.52) rồi xác suất đúng 2 người trong 6.') + steps(['z₁ = 0, z₂ = (51.52 − 44.4)/7.12 = 1 ⇒ p = Φ(1) − Φ(0) = 0.3413.', 'Mỗi người “thuộc khoảng” độc lập với xác suất p ⇒ nhị thức: C(6,2)p²(1 − p)⁴ = 0.3289.']) + '<p>Đây là cách nối chuẩn và nhị thức: xác suất chuẩn trở thành tham số p của nhị thức.</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 3: chuẩn rồi nhị thức (giữa kỳ HK2)'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Câu 1 đề HK2', 'Đề mẫu 2024', 'Chuẩn → nhị thức'], slides=s))
    s = []
    s.append(sl(ul(['<b>Quên chuẩn hóa</b>: dùng σ, không phải σ².', '<b>Nhầm σ² và σ</b>: đề cho phương sai thì lấy căn.', '<b>Tra A7 với z âm</b>: Φ(−z) = 1 − Φ(z).', '<b>P(X ≥ c) = p</b> ⇒ P(X &lt; c) = 1 − p (không phải p).', '<b>Quên hiệu chỉnh 0.5</b> khi xấp xỉ nhị thức bằng chuẩn.', '<b>Dùng Poisson khi p không nhỏ</b> hoặc n không lớn.']), 'PHẦN 4 · Bẫy và mở rộng', 'Sáu bẫy thường gặp'))
    s.append(sl(callout('warn', 'Lỗi in trong giáo trình', 'Ví dụ 1.31(a) in “1.654” (đúng 1.645); Ví dụ 1.33 in β = 7.5625 (đúng 5.0625; kết quả vẫn 0.9948).') + '<p>Các tham số của đề 2021–2022 câu 1(b) cho đáp án chính thức k âm (−1.702 và −2.758): đây là hệ quả của tham số đề (b lớn), ghi nhận ở trang Tài liệu.</p>', 'PHẦN 4 · Bẫy và mở rộng', 'Sai sót đã phát hiện'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Sáu bẫy', 'Lỗi in'], slides=s))
    s = []
    s.append(sl('<p><b>Kiểm soát dung sai.</b> Thanh sắt có đường kính X ~ N(2; 0.008²) in và dung sai 2 ± 0.02 in: xác suất đạt = Φ(2.5) − Φ(−2.5) = 0.9876 ⇒ phế phẩm ≈ 1.25%. Muốn phế phẩm chỉ 4% thì dung sai c = 2.054·0.008 = 0.0164 in. Đây chính là bài toán thiết kế dung sai và nền của biểu đồ kiểm soát (Module 12).</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: dung sai thanh sắt'))
    s.append(sl(ul(['Nhị thức: đếm thành công; Poisson: biến cố hiếm; chuẩn: liên tục đối xứng.', 'P(a < X < b) = Φ(z₂) − Φ(z₁); phân vị c = μ + σz.', 'Xấp xỉ: np > 5 và n(1 − p) > 5 ⇒ chuẩn có hiệu chỉnh 0.5; p nhỏ ⇒ Poisson.']) + callout('good', 'Tiếp theo', 'Chương 2: mẫu ngẫu nhiên, ước lượng điểm và khoảng tin cậy (Module 7–8).'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Dung sai', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §1.10: nhị thức (1.34–1.36), Poisson (1.37–1.38), chuẩn (1.39–1.43, bảng A7/A8), xấp xỉ chuẩn của nhị thức (1.44–1.45). Kreyszig §24.7 (nhị thức, Poisson, siêu bội; PS 24.7 gồm 16 bài) và §24.8 (chuẩn, định lý De Moivre–Laplace; PS 24.8 gồm 15 bài). Ngân hàng câu hỏi có cả 10 câu 1 của các đề cuối kỳ.</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Ví dụ 1.31: tìm c và k', '<p>X ~ N(5; 0.04), σ = 0.2.</p>' + steps(['(a) P(X ≤ c) = 95% ⇒ (c − 5)/0.2 = 1.645 ⇒ c = 5.329.', '(b) P(5 − k ≤ X ≤ 5 + k) = 90% ⇒ Φ(k/0.2) = 0.95 ⇒ k = 0.329.', '(c) P(X ≥ c) = 1% ⇒ (c − 5)/0.2 = 2.326 ⇒ c = 5.465.']))
    notes += ex('2. Ví dụ 1.32: thanh sắt', '<p>(a) Φ(2.5) − Φ(−2.5) = 0.9876 ⇒ phế phẩm 1.24% ≈ 1¼%. (b) 2Φ(c/0.008) − 1 = 0.96 ⇒ c/0.008 = 2.054 ⇒ c = 0.0164 in.</p>')
    notes += ex('3. Kreyszig PS 24.7/14: văn phòng bán vé', '<p>Phục vụ tối đa 4 khách/phút; trung bình 150 khách/giờ ⇒ μ = 2.5 khách/phút. P(phải chờ) = P(X &gt; 4) = 1 − 0.8912 = 0.1088.</p>')
    notes += ex('4. Kreyszig PS 24.8/9: điểm SAT', '<p>X ~ N(480; 100²). Tỉ lệ không đạt 500: P(X &lt; 500) = Φ(0.2) = 0.5793 ≈ 57.9%.</p>')
    notes += ex('5. Bài 1.32 + 1.30: Poisson thay nhị thức', '<p>4% thanh lỗi, bó 100 thanh ⇒ μ = 4: P(0) = 0.0183; P(1) = 0.0733; P(2) = 0.1465; P(3) = 0.1954; P(4) = 0.1954; P(5) = 0.1563.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('normcalc') + sim('binpois')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Từ Bernoulli đến Gauss', 'Nhị thức do Jacob Bernoulli (1713); Poisson (1837) nghiên cứu giới hạn p → 0; De Moivre (1733) tìm xấp xỉ chuẩn của nhị thức, Laplace mở rộng; Gauss dùng phân phối chuẩn mô tả sai số đo (đường cong chuông). Bảng A7/A8 là bản in các giá trị Φ và Φ⁻¹.')
    notes += '<h2>5. Case study</h2><p>Tổng đài (Kreyszig PS 24.7/8): trung bình 300 cuộc/giờ = 5 cuộc/phút, xử lý tối đa 10/phút: xác suất quá tải 1 − P(X ≤ 10) = 0.0137, tức khoảng 1.4% số phút bị tắc nghẽn — đủ thông tin để quyết định có cần nâng công suất.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Viết rõ z trước khi tra bảng; làm tròn z đến 2 chữ số khi tra A7.<br>• Dùng chính xác đáp án từ phần mềm khi đề không yêu cầu bảng.<br>• Nhớ P(X = a) = 0 với biến liên tục: “≤” và “&lt;” cho cùng xác suất.')
    return dict(id='m06', slug='m06-nhi-thuc-poisson-chuan', title='Phân phối nhị thức, Poisson và phân phối chuẩn', subtitle='B(n, p), Poisson(μ), N(μ, σ²), chuẩn tắc, bảng A7/A8, xấp xỉ chuẩn',
                source='Lecture Notes §1.10, Bài 1.32–1.39 · Kreyszig §24.7–24.8 (PS 24.7, 24.8) · Câu 1 các đề cuối kỳ 2021–2024 · Giữa kỳ mẫu câu 1, 7', exam='Câu 1 MỌI đề cuối kỳ; câu 7 đề giữa kỳ mẫu; câu 3 giữa kỳ HK2', time='≈ 5 giờ',
                objectives=['Tính xác suất và phân vị cho nhị thức, Poisson, chuẩn', 'Chuẩn hóa và tra bảng A7 (Φ), A8 (z)', 'Dùng xấp xỉ Poisson và chuẩn (có hiệu chỉnh 0.5) đúng điều kiện', 'Giải đúng dạng câu 1 của đề cuối kỳ (P(X ≤ a) và tìm c)'], parts=parts, notes=notes, sims=['normcalc', 'binpois'])
