from hx import *
K = 'MODULE 5 · '
def module():
    parts = []
    # ───────── PHẦN 1 ─────────
    s = []
    s.append(sl('<p>Biến ngẫu nhiên (BNN) biến kết quả của một phép thử thành <b>con số</b> để tính toán. Module này gồm: BNN rời rạc và liên tục, hàm xác suất / hàm mật độ, hàm phân phối F(x), kỳ vọng, phương sai, độ lệch chuẩn, trung vị và phân vị — nền tảng của mọi phân phối ở Module 6 và của ước lượng, kiểm định ở các module sau.</p>'
                + ul(['BNN là hàm X: S → ℝ; phân biệt rời rạc và liên tục', 'Bảng phân phối, hàm xác suất; hàm mật độ f(x)', 'Hàm phân phối F(x) = P(X ≤ x) và cách dùng để tính xác suất khoảng', 'E(X), Var(X), σ; tính chất tuyến tính; bất đẳng thức Chebyshev', 'Trung vị, phân vị; kỳ vọng của g(X); hai mật độ hay gặp (đều, mũ)']),
                K + 'Bài học 1 · Chương 1, mục 1.7–1.9 · Kreyszig §24.5–24.6', 'Biến ngẫu nhiên và các đặc trưng',
                explain='Gieo súc sắc xong, X = “số chấm” là một con số ngẫu nhiên. Ta không biết trước X nhưng biết X nhận giá trị nào với xác suất bao nhiêu — đó là toàn bộ thông tin cần thiết.'))
    s.append(sl(table(['Phép thử', 'Biến ngẫu nhiên X', 'Giá trị có thể', 'Loại'],
                      [['Tung 2 đồng xu', 'X = số mặt sấp', '0, 1, 2', 'rời rạc'], ['Gieo 1 súc sắc', 'X = số chấm', '1, 2, …, 6', 'rời rạc'], ['Số cuộc gọi đến tổng đài trong 1 giờ', 'X = số cuộc gọi', '0, 1, 2, …', 'rời rạc (đếm được)'],
                       ['Chờ xe buýt', 'X = thời gian chờ (phút)', '[0, ∞)', 'liên tục'], ['Đo chiều cao sinh viên', 'X = chiều cao (cm)', 'một khoảng', 'liên tục']])
                + callout('info', 'Định nghĩa', 'BNN là hàm số gán mỗi kết quả ω của không gian mẫu S một số thực X(ω). Biến cố “X ≤ x” là tập các ω thỏa X(ω) ≤ x, nên có xác suất P(X ≤ x).'),
                K + 'PHẦN 1 · Nền tảng', 'BNN là gì? Năm ví dụ', explain='Chữ “ngẫu nhiên” chỉ cái ta chưa biết trước khi làm thí nghiệm; sau khi làm xong, X là một con số cụ thể.'))
    s.append(sl(table(['', 'Rời rạc', 'Liên tục'], [['Giá trị', 'hữu hạn / đếm được', 'lấp đầy một khoảng'], ['Mô tả', 'bảng p(xᵢ), f(x) = P(X = x)', 'mật độ f(x) ≥ 0'], ['Chuẩn hóa', 'Σ f(xᵢ) = 1', '∫ f(x)dx = 1'], ['Xác suất khoảng', 'cộng các f(xᵢ)', 'diện tích dưới f; P(X = a) = 0'], ['Hàm phân phối', 'bậc thang', 'liên tục, F′ = f']])
                + formula('Hàm phân phối', 'F(x)=P(X\\le x),\\quad P(a<X\\le b)=F(b)-F(a),\\quad f(x)=F\'(x)'),
                K + 'PHẦN 1 · Nền tảng', 'Rời rạc và liên tục', explain='Rời rạc: đếm được (số điểm xạ thủ). Liên tục: đo được (thời gian, khoảng cách) — xác suất của một giá trị chính xác bằng 0, chỉ khoảng mới có xác suất.'))
    s.append(sl(callout('info', 'Ví dụ 1 · Tung hai đồng xu cân đối', 'X = số mặt sấp. Lập bảng phân phối.')
                + table(['Kết quả', 'SS', 'SN', 'NS', 'NN'], [['X', '2', '1', '1', '0']])
                + steps([m('P(X=0)=P(NN)=\\tfrac14'), m('P(X=1)=P(SN)+P(NS)=\\tfrac14+\\tfrac14=\\tfrac12'), m('P(X=2)=P(SS)=\\tfrac14')])
                + table(['x', '0', '1', '2'], [['f(x)', '1/4', '1/2', '1/4']]) + '<p>Kiểm tra: 1/4 + 1/2 + 1/4 = 1 ✓.</p>',
                K + 'PHẦN 1 · Nền tảng', 'Lập bảng phân phối', explain='Bước then chốt: liệt kê các kết quả đồng khả năng rồi nhóm theo giá trị của X.'))
    s.append(sl(callout('info', 'Ví dụ 2 · Tổng hai súc sắc', 'X = tổng số chấm khi gieo hai súc sắc cân đối (36 kết quả đồng khả năng).')
                + table(['x', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], [['36·f(x)', '1', '2', '3', '4', '5', '6', '5', '4', '3', '2', '1']])
                + steps(['Số cách có tổng x là 6 − |x − 7| nên f(x) = (6 − |x − 7|)/36.', m('P(X\\ge 10)=\\tfrac{3+2+1}{36}=\\tfrac16')]) + '<p>Tổng các tử số: 1+2+3+4+5+6+5+4+3+2+1 = 36 ✓.</p>',
                K + 'PHẦN 1 · Nền tảng', 'Hàm xác suất của tổng hai súc sắc'))
    s.append(sl(callout('info', 'Ví dụ 3 · Tìm hằng số k (rời rạc)', 'f(x) = k·x với x = 1, 2, 3, 4, 5 là hàm xác suất. Tìm k và P(X ≤ 2).')
                + steps([m('\\sum_{x=1}^5 kx=15k=1\\Rightarrow k=\\tfrac1{15}'), m('P(X\\le 2)=f(1)+f(2)=\\tfrac1{15}+\\tfrac2{15}=\\tfrac15')])
                + callout('warn', 'Quy tắc', 'Luôn bắt đầu bằng điều kiện chuẩn hóa: tổng các xác suất bằng 1 (rời rạc) hoặc tích phân bằng 1 (liên tục).'),
                K + 'PHẦN 1 · Nền tảng', 'Chuẩn hóa tìm k (rời rạc)'))
    s.append(sl(formula('Hàm mật độ f(x) của BNN liên tục', 'f(x)\\ge 0,\\quad \\int_{-\\infty}^{\\infty}f(x)\\,dx=1,\\quad P(a\\le X\\le b)=\\int_a^b f(x)\\,dx',
                        [('f(x)', 'không phải xác suất; có thể > 1'), ('P(X=a)', 'bằng 0 với mọi a — chỉ khoảng mới có xác suất')])
                + callout('info', 'Ví dụ 4 · Tìm k (liên tục)', 'f(x) = kx² trên [0, 3], bằng 0 ngoài đoạn. Tìm k, tính P(1 < X < 2).')
                + steps([m('\\int_0^3 kx^2dx=9k=1\\Rightarrow k=\\tfrac19'), m('P(1<X<2)=\\int_1^2\\tfrac{x^2}{9}dx=\\tfrac{8-1}{27}=\\tfrac7{27}\\approx0.2593')]),
                K + 'PHẦN 1 · Nền tảng', 'Hàm mật độ và diện tích', explain='Hình dung mật độ như độ “đậm” của khối lượng xác suất; xác suất của một khoảng là diện tích bên dưới đường cong trên khoảng đó.'))
    s.append(sl(formula('Hàm phân phối F(x) và tính chất', 'F(x)=P(X\\le x)=\\begin{cases}\\sum_{x_j\\le x}f(x_j)&\\text{rời rạc}\\\\ \\int_{-\\infty}^xf(t)\\,dt&\\text{liên tục}\\end{cases}')
                + ul(['0 ≤ F(x) ≤ 1, F không giảm; F(−∞) = 0, F(+∞) = 1.', 'F liên tục phải; rời rạc: bước nhảy tại xⱼ bằng f(xⱼ).', 'P(a < X ≤ b) = F(b) − F(a); P(X > a) = 1 − F(a).', 'Liên tục: f(x) = F′(x) tại các điểm F khả vi.']),
                K + 'PHẦN 1 · Nền tảng', 'Hàm phân phối', explain='F(x) là “xác suất tích lũy đến x”. Nó luôn đi từ 0 lên 1 và không bao giờ giảm.'))
    s.append(sl(callout('info', 'Ví dụ 5 · F của bảng phân phối (hai đồng xu)', 'Từ bảng f(0) = 1/4, f(1) = 1/2, f(2) = 1/4.')
                + table(['x', 'x < 0', '0 ≤ x < 1', '1 ≤ x < 2', 'x ≥ 2'], [['F(x)', '0', '1/4', '3/4', '1']])
                + steps([m('P(X>0.5)=1-F(0.5)=1-\\tfrac14=\\tfrac34'), m('P(0<X\\le1)=F(1)-F(0)=\\tfrac34-\\tfrac14=\\tfrac12=f(1)')]) + '<p>Đồ thị F là bậc thang, nhảy 1/4, 1/2, 1/4 tại x = 0, 1, 2.</p>',
                K + 'PHẦN 1 · Nền tảng', 'F của BNN rời rạc là bậc thang'))
    s.append(sl(callout('info', 'Ví dụ 6 · F của mật độ (liên tục)', 'f(x) = 3x² trên [0, 1]. Tìm F và P(0.5 < X < 0.8).')
                + steps([m('F(x)=\\int_0^x3t^2dt=x^3\\quad(0\\le x\\le1);\\ F=0\\ (x<0),\\ F=1\\ (x>1)'), m('P(0.5<X<0.8)=F(0.8)-F(0.5)=0.512-0.125=0.387')])
                + '<p>Kiểm tra ngược: F′(x) = 3x² = f(x) ✓.</p>', K + 'PHẦN 1 · Nền tảng', 'F từ mật độ (liên tục)'))
    s.append(sl(sim('rv'), K + 'PHẦN 1 · Nền tảng', 'Thực hành: bảng phân phối → E(X), Var(X), F(x)'))
    parts.append(dict(title='Nền tảng: BNN, hàm xác suất, mật độ, F(x)', bullets=['BNN rời rạc và liên tục', 'Lập bảng, tìm hằng số k', 'Hàm mật độ, hàm phân phối', 'Widget rời rạc'], slides=s))
    # ───────── PHẦN 2 ─────────
    s = []
    s.append(sl(formula('Kỳ vọng và phương sai', '\\mu=E(X)=\\sum_j x_jf(x_j)\\ \\text{hoặc}\\ \\int_{-\\infty}^{\\infty}xf(x)dx,\\qquad \\sigma^2=E[(X-\\mu)^2]=E(X^2)-\\mu^2',
                        [('\\mu', 'giá trị trung bình dài hạn'), ('\\sigma^2', 'độ phân tán bình phương; \\(\\sigma=\\sqrt{\\sigma^2}\\)')])
                + formula('Công thức tính nhanh', '\\operatorname{Var}(X)=E(X^2)-[E(X)]^2,\\qquad E(X^2)=\\sum x_j^2f(x_j)\\ \\text{hoặc}\\ \\int x^2f(x)dx'),
                K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Kỳ vọng và phương sai',
                explain='Kỳ vọng là “tâm khối” của phân phối; phương sai đo mức tản mác quanh tâm. Cộng hằng số dịch tâm nhưng không đổi độ tản mác.'))
    s.append(sl(callout('info', 'Ví dụ 7 · Kỳ vọng của một súc sắc', 'X = số chấm, f(x) = 1/6, x = 1..6.')
                + steps([m('E(X)=\\tfrac{1+2+3+4+5+6}{6}=3.5'), m('E(X^2)=\\tfrac{1+4+9+16+25+36}{6}=\\tfrac{91}6\\approx15.1667'), m('\\operatorname{Var}(X)=\\tfrac{91}{6}-3.5^2=\\tfrac{35}{12}\\approx2.9167,\\ \\sigma\\approx1.7078')])
                + '<p>Giá trị 3.5 không phải mặt nào của súc sắc: kỳ vọng là trung bình dài hạn, không nhất thiết là giá trị có thể xảy ra.</p>', K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Súc sắc: E = 3.5, Var = 35/12'))
    s.append(sl(callout('info', 'Ví dụ 8 · Đề 2TC (HK1 2022–2023), đề 1, câu 1', 'X = số điểm của xạ thủ, X = 0..5 với P = 0.10, 0.20, 0.25, 0.35, 0.06, 0.04.')
                + steps([m('E(X)=0\\cdot0.10+1\\cdot0.20+2\\cdot0.25+3\\cdot0.35+4\\cdot0.06+5\\cdot0.04=2.19'), m('E(X^2)=0.2+1.0+3.15+0.96+1.0=6.31'), m('\\operatorname{Var}(X)=6.31-2.19^2=1.5139,\\ \\sigma\\approx1.2304')]),
                K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Số điểm của xạ thủ'))
    s.append(sl(callout('info', 'Ví dụ 9 · Kỳ vọng và phương sai liên tục', 'f(x) = 3x² trên [0, 1].')
                + steps([m('E(X)=\\int_0^1x\\cdot3x^2dx=\\tfrac34'), m('E(X^2)=\\int_0^1x^2\\cdot3x^2dx=\\tfrac35'), m('\\operatorname{Var}(X)=\\tfrac35-\\tfrac9{16}=\\tfrac3{80}=0.0375,\\ \\sigma\\approx0.1936')])
                + '<p>Mật độ lệch về phía 1 (f tăng) nên kỳ vọng 0.75 lớn hơn trung điểm 0.5.</p>', K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Trường hợp liên tục'))
    s.append(sl(formula('Biến đổi tuyến tính', 'E(aX+b)=a\\,E(X)+b,\\qquad \\operatorname{Var}(aX+b)=a^2\\operatorname{Var}(X),\\qquad \\sigma_{aX+b}=|a|\\sigma')
                + callout('info', 'Ví dụ 10', 'Với xạ thủ ở Ví dụ 8, Y = 3X + 2 (điểm thưởng).')
                + steps([m('E(Y)=3\\cdot2.19+2=8.57'), m('\\operatorname{Var}(Y)=3^2\\cdot1.5139=13.6251,\\ \\sigma_Y=3\\cdot1.2304=3.691')])
                + '<p>Cộng 2 chỉ dịch tâm, không làm đổi độ phân tán; nhân 3 nhân độ lệch chuẩn lên 3 và phương sai lên 9.</p>', K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Biến đổi tuyến tính'))
    s.append(sl(formula('Tính chất của tổng', 'E(X+Y)=E(X)+E(Y)\\ \\text{(luôn đúng)},\\qquad \\operatorname{Var}(X+Y)=\\operatorname{Var}(X)+\\operatorname{Var}(Y)\\ \\text{(nếu X, Y độc lập)}')
                + callout('info', 'Ví dụ 11', 'Hai máy độc lập, E(X) = 5, Var(X) = 4; E(Y) = 7, Var(Y) = 9. Với T = X + Y: E(T) = 12, Var(T) = 13, σ_T = 3.606. Với D = X − Y: E(D) = −2 nhưng Var(D) = 4 + 9 = 13 (phương sai vẫn cộng).')
                + callout('warn', 'Bẫy', 'Var(X − Y) = Var(X) + Var(Y), không phải Var(X) − Var(Y).'), K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Tổng của hai BNN'))
    s.append(sl(formula('Bất đẳng thức Chebyshev', 'P(|X-\\mu|<k\\sigma)\\ge 1-\\dfrac1{k^2}\\quad(k>1)')
                + callout('info', 'Ví dụ 12', 'Thời gian giao hàng có μ = 50 phút, σ = 5 phút (không biết dạng phân phối). Với k = 2: P(40 < X < 60) ≥ 1 − 1/4 = 0.75. Với k = 3: P(35 < X < 65) ≥ 1 − 1/9 ≈ 0.889.')
                + '<p>Chebyshev đúng cho mọi phân phối nên khá “rộng”; với chuẩn, xác suất thật là 0.9545 (k = 2) — xem Module 6.</p>', K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Chebyshev: dùng khi chỉ biết μ và σ'))
    s.append(sl(sim('pdf'), K + 'PHẦN 2 · Kỳ vọng, phương sai', 'Thực hành: mật độ, diện tích, kỳ vọng, trung vị'))
    parts.append(dict(title='Kỳ vọng, phương sai, độ lệch chuẩn', bullets=['E(X), Var(X) rời rạc và liên tục', 'Tuyến tính, tổng, Chebyshev', 'Widget liên tục'], slides=s))
    # ───────── PHẦN 3 ─────────
    s = []
    s.append(sl(callout('info', 'Quy trình cho mật độ f(x) cho trước (đề thi HK2)', '1) Tìm k từ ∫f = 1. 2) F(x) = ∫f. 3) E(X) = ∫xf, E(X²) = ∫x²f. 4) Var = E(X²) − μ². 5) Trung vị m: giải F(m) = 0.5; phân vị p: F(x_p) = p.')
                + callout('info', 'Ví dụ 13 · Trung vị của f(x) = 2x trên [0, 1]', 'F(x) = x² (0 ≤ x ≤ 1).')
                + steps([m('F(m)=m^2=0.5\\Rightarrow m=\\tfrac1{\\sqrt2}\\approx0.7071'), m('Q_1:\\ x^2=0.25\\Rightarrow0.5;\\quad Q_3:\\ x^2=0.75\\Rightarrow0.8660'), m('E(X)=\\int_0^1x\\cdot2x\\,dx=\\tfrac23\\approx0.667')])
                + '<p>Trung vị (0.707) &gt; kỳ vọng (0.667) khi mật độ lệch trái — dấu hiệu bất đối xứng.</p>', K + 'PHẦN 3 · Trung vị, phân vị, mô-men', 'Trung vị và tứ phân vị', explain='Trung vị chia diện tích dưới mật độ làm hai nửa bằng nhau: F(m) = 0.5.'))
    s.append(sl(callout('info', 'Ví dụ 14 · Mật độ đối xứng f(x) = 6x(1 − x), 0 ≤ x ≤ 1', 'Kiểm tra ∫f = 1; tính E(X), Var(X), trung vị.')
                + steps([m('\\int_0^16(x-x^2)dx=6(\\tfrac12-\\tfrac13)=1\\ \\checkmark'), m('E(X)=6(\\tfrac13-\\tfrac14)=\\tfrac12'), m('E(X^2)=6(\\tfrac14-\\tfrac15)=0.3,\\ \\operatorname{Var}=0.3-0.25=0.05,\\ \\sigma=0.2236'), m('F(m)=3m^2-2m^3=\\tfrac12\\Rightarrow m=\\tfrac12\\ (\\text{đối xứng})')]),
                K + 'PHẦN 3 · Trung vị, phân vị, mô-men', 'Mật độ đối xứng'))
    s.append(sl(formula('Kỳ vọng của g(X) và mô-men', 'E(g(X))=\\sum g(x_j)f(x_j)\\ \\text{hoặc}\\ \\int g(x)f(x)dx,\\quad E(X^k),\\ E[(X-\\mu)^k]', [('E[(X-\\mu)^3]/\\sigma^3', 'hệ số bất đối xứng (skewness) — bằng 0 khi phân phối đối xứng')])
                + callout('info', 'Ví dụ 15 · Kreyszig PS 24.6/19', 'f(0) = f(3) = 1/8, f(1) = f(2) = 3/8.') + steps([m('E(X^3)=0^3\\cdot\\tfrac18+1^3\\cdot\\tfrac38+2^3\\cdot\\tfrac38+3^3\\cdot\\tfrac18=\\tfrac{0+3+24+27}{8}=6.75')]),
                K + 'PHẦN 3 · Trung vị, phân vị, mô-men', 'E(g(X)) và mô-men'))
    s.append(sl(table(['Phân phối', 'Mật độ', 'F(x)', 'E(X)', 'Var(X)'],
                      [['Đều U[a, b]', '1/(b − a)', '(x − a)/(b − a)', '(a + b)/2', '(b − a)²/12'], ['Mũ Exp(λ)', 'λe^(−λx), x ≥ 0', '1 − e^(−λx)', '1/λ', '1/λ²']])
                + callout('info', 'Ví dụ 16', 'T ~ Exp(0.5) (đơn vị phút). E(T) = 2; Var(T) = 4; P(T > 2) = e^(−1) ≈ 0.3679; trung vị m = ln 2/0.5 ≈ 1.386 (nhỏ hơn kỳ vọng 2 vì phân phối lệch phải).')
                + callout('info', 'Ví dụ 17', 'X đều trên [2, 8]: E = 5, Var = 36/12 = 3, P(3 ≤ X ≤ 5) = 2/6 = 1/3.'), K + 'PHẦN 3 · Trung vị, phân vị, mô-men', 'Hai mật độ hay gặp: đều và mũ'))
    parts.append(dict(title='Trung vị, phân vị, mô-men, đều và mũ', bullets=['Trung vị, tứ phân vị', 'Mô-men, skewness', 'Đều và mũ'], slides=s))
    # ───────── PHẦN 4: bài thật ─────────
    s = []
    s.append(sl(callout('info', 'Đề HK2 (3TC), câu 5', 'f(x) = 0.75(2 − x)x, 0 ≤ x ≤ 2.')
                + steps([m('\\int_0^20.75(2x-x^2)dx=0.75(4-\\tfrac83)=1\\ \\checkmark'), m('E(X)=0.75\\int_0^2(2x^2-x^3)dx=0.75(\\tfrac{16}3-4)=1'), m('F(m)=0.75(m^2-\\tfrac{m^3}3)=0.5\\Rightarrow m=1\\ (\\text{đối xứng qua }x=1)')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Đề HK2 câu 5: mật độ đối xứng'))
    s.append(sl(callout('info', 'Đáp án giữa kỳ HK2, câu 2', 'T ∈ {0, 1, 2, 3}: P = 0.28; 0.1332; 0.3648; m, trong đó m = 0.222.')
                + steps(['Chuẩn hóa: m = 1 − 0.28 − 0.1332 − 0.3648 = 0.222.', 'P(0.5 < T < 2.5) = 0.1332 + 0.3648 = 0.498.', 'E(T) = 0.1332 + 2·0.3648 + 3·0.222 = 1.5288.', 'σ² = Σ(xᵢ − μ)²pᵢ = 1.2532.']),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Giữa kỳ HK2 câu 2: bảng có tham số'))
    s.append(sl(callout('info', 'Bài 1.24 (đã đối chiếu ảnh trang)', 'f(x) = k/2ˣ, x = 0, 1, 2, … (văn bản trích tự động làm rơi phân số nên kiểm lại ảnh trang).')
                + steps([m('\\sum_{x=0}^\\infty \\tfrac{k}{2^x}=2k=1\\Rightarrow k=\\tfrac12'), m('P(X\\ge4)=\\sum_{x\\ge4}\\tfrac1{2^{x+1}}=\\tfrac1{2^5}\\cdot2=\\tfrac1{16}')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Bài 1.24: chuỗi hình học'))
    s.append(sl(callout('info', 'Bài 1.25 · Hàm phân phối', 'f(x) = kx² trên [0, 5].')
                + steps([m('\\int_0^5kx^2dx=\\tfrac{125k}3=1\\Rightarrow k=\\tfrac3{125}'), m('F(x)=\\tfrac{x^3}{125}\\ (0\\le x\\le5);\\ 0\\ (x<0);\\ 1\\ (x>5)'), m('P(1<X<3)=\\tfrac{27-1}{125}=0.208')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Bài 1.25: tìm k, F(x)'))
    s.append(sl(callout('info', 'Bài 1.28 / Kreyszig 24.5/12', 'F(x) = (x² − 4)/5 với 2 ≤ x < 3 (F = 0 khi x < 2, F = 1 khi x ≥ 3).')
                + steps([m('f(x)=F\'(x)=\\tfrac{2x}5\\ (2\\le x\\le3)'), m('P(2.5\\le X\\le5)=1-F(2.5)=1-\\tfrac{6.25-4}5=1-0.45=0.55')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Bài 1.28: từ F suy ra f'))
    s.append(sl(callout('info', 'Bài 1.30 · Trạm xăng', 'X = lượng xăng bán trong tuần (đơn vị 10 000 gallon), f(x) = 6x(1 − x). Dung tích bể c để xác suất hết xăng 5%.')
                + steps([m('\\mu=0.5,\\ \\sigma^2=0.05,\\ \\sigma=0.2236'), m('P(X>c)=0.05\\Rightarrow F(c)=3c^2-2c^3=0.95'), m('\\text{Giải số: }c\\approx0.8647\\ (\\approx 8647\\text{ gallon})')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Bài 1.30: chọn dung tích'))
    s.append(sl(callout('info', 'Kreyszig PS 24.6/9 · Mật độ parabol', 'f(x) = k(x − 0.9)(1.1 − x) trên [0.9, 1.1] (đường kính bu-lông, cm). Bu-lông lỗi nếu lệch quá 0.06 cm so với 1.')
                + steps([m('\\int_{0.9}^{1.1}(x-0.9)(1.1-x)dx=\\tfrac{0.2^3}6\\Rightarrow k=750'), m('\\mu=1\\ (\\text{đối xứng}),\\ \\sigma^2=\\tfrac{0.2^2}{20}=0.002'), m('P(\\text{lỗi})=1-\\int_{0.94}^{1.06}f\\,dx\\approx0.2080')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Kreyszig 24.6/9: tỉ lệ bu-lông lỗi'))
    s.append(sl(callout('info', 'Kreyszig PS 24.6/13 · Cửa hàng máy lạnh', 'Số máy bán mỗi ngày X ∈ {10, 11, 12, 13} với xác suất 0.1, 0.3, 0.4, 0.2; lãi $55/máy.')
                + steps([m('E(X)=1+3.3+4.8+2.6=11.7'), m('E(\\text{lãi})=55\\cdot11.7=\\$643.50\\text{ mỗi ngày}'), m('E(X^2)=10^2\\cdot0.1+11^2\\cdot0.3+12^2\\cdot0.4+13^2\\cdot0.2=137.9;\\ \\operatorname{Var}=137.9-136.89=1.01')]),
                K + 'PHẦN 4 · Bài thật có lời giải', 'Kreyszig 24.6/13: lãi kỳ vọng'))
    parts.append(dict(title='Bài thật có lời giải', bullets=['Đề HK2, giữa kỳ HK2', 'Bài 1.24–1.30', 'Kreyszig 24.6/9, 24.6/13'], slides=s))
    # ───────── PHẦN 5: bẫy + ứng dụng ─────────
    s = []
    s.append(sl(ul(['<b>Quên chuẩn hóa</b>: kiểm tra Σp = 1 hoặc ∫f = 1 (tìm k trước).', '<b>Var = E(X²) − μ²</b>, không phải E(X²) − E(X) hay E(X) − E(X²).', '<b>Mật độ f(x) có thể &gt; 1</b> (không phải xác suất); P(X = a) = 0 nhưng f(a) có thể dương.', '<b>Cận tích phân</b>: chỉ lấy trên miền f ≠ 0.', '<b>Biến đổi tuyến tính</b>: Var(aX + b) = a²Var(X), không cộng b.', '<b>Var(X − Y)</b> = Var(X) + Var(Y) khi độc lập.']), K + 'PHẦN 5 · Bẫy và ứng dụng', 'Sáu bẫy thường gặp'))
    s.append(sl(callout('warn', 'Làm tròn', 'Giữ nhiều chữ số ở E(X²) trước khi trừ μ²: nếu làm tròn E(X²) = 6.31 thành 6.3 sẽ thu được Var sai 0.01 (đáp án chấm ±0.001).')
                + callout('good', 'Kiểm tra nhanh', 'Var ≥ 0 luôn; với mật độ đối xứng, kỳ vọng = trung vị = tâm đối xứng; kỳ vọng nằm trong khoảng giá trị của X.'), K + 'PHẦN 5 · Bẫy và ứng dụng', 'Kiểm tra kết quả'))
    s.append(sl('<p><b>Định giá kỳ vọng.</b> Một trò chơi trả 10 nghìn với xác suất 0.2, 0 với xác suất 0.8. Kỳ vọng thu về 2 nghìn mỗi lượt; muốn trò chơi “công bằng” thì phí chơi phải là 2 nghìn. Công ty bảo hiểm dùng đúng nguyên lý này: phí bảo hiểm = bồi thường kỳ vọng + chi phí + lợi nhuận.</p>'
                + '<p><b>Rủi ro.</b> Hai dự án đều có lợi nhuận kỳ vọng 100 triệu nhưng độ lệch chuẩn 10 và 80 triệu: dự án thứ hai rủi ro hơn nhiều. Vì vậy khi so sánh ta xét cả E(X) và σ.</p>', K + 'PHẦN 5 · Bẫy và ứng dụng', 'Ứng dụng: định giá và rủi ro'))
    s.append(sl('<p><b>Case study: xạ thủ thi bắn (đề 2TC).</b> E(X) = 2.19 điểm, σ = 1.23. Hai xạ thủ có cùng E(X) nhưng σ khác nhau cho kết quả ổn định khác nhau — vì thế tuyển chọn thường xét cả kỳ vọng và phương sai.</p>'
                + '<p><b>Tham khảo lịch sử.</b> “Giá trị kỳ vọng” xuất hiện trong bài toán chia tiền cược của Pascal–Fermat (1654), được Huygens hệ thống hóa (1657); khái niệm BNN và hàm phân phối tổng quát được hoàn thiện bởi Kolmogorov (1933).</p>', K + 'PHẦN 5 · Bẫy và ứng dụng', 'Case study và bối cảnh lịch sử'))
    s.append(sl(ul(['Bảng phân phối: Σp = 1; E = Σxp; Var = Σx²p − μ².', 'Mật độ: ∫f = 1; E = ∫xf; F(m) = 0.5 cho trung vị.', 'Y = aX + b: E = aμ + b, Var = a²σ².', 'Tổng độc lập: Var cộng; Chebyshev: P(|X − μ| < kσ) ≥ 1 − 1/k².', 'Đều: (a + b)/2, (b − a)²/12; mũ: 1/λ, 1/λ².']) + callout('good', 'Tiếp theo', 'Module 6: nhị thức, Poisson và phân phối chuẩn.'), K + 'PHẦN 5 · Bẫy và ứng dụng', 'Tổng kết module'))
    parts.append(dict(title='Bẫy, ứng dụng và tổng kết', bullets=['Sáu bẫy', 'Định giá và rủi ro', 'Tổng kết'], slides=s))
    from notes_m05 import notes as _nt; notes = _nt()
    return dict(id='m05', slug='m05-bien-ngau-nhien', title='Biến ngẫu nhiên, hàm phân phối, hàm mật độ, kỳ vọng, phương sai', subtitle='BNN rời rạc/liên tục, bảng phân phối, F(x), f(x), E(X), Var(X), trung vị',
                source='Lecture Notes §1.7–1.9, Bài 1.24–1.31 · Kreyszig §24.5–24.6 (PS 24.5, 24.6) · Đề cuối kỳ 2022–2023 (2TC câu 1, 3TC câu 5) · Đáp án giữa kỳ HK2 câu 2', exam='Câu 1 đề 2TC; Câu 5 đề HK2; Câu 2 giữa kỳ HK2', time='≈ 4 giờ',
                objectives=['Phân biệt BNN rời rạc và liên tục, kiểm tra hàm xác suất/mật độ', 'Tính F(x), P(a < X < b) từ bảng hoặc mật độ', 'Tính E(X), Var(X), σ và trung vị cho cả hai loại', 'Dùng biến đổi tuyến tính, tính chất tổng và Chebyshev'], parts=parts, notes=notes, sims=['rv', 'pdf'])
