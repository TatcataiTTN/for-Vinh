from hx import *
K = 'MODULE 6 · '
def module():
    parts = []
    # ───────── PHẦN 1: NHỊ THỨC ─────────
    s = []
    s.append(sl('<p>Ba phân phối quan trọng nhất của giáo trình: <b>nhị thức</b> (đếm thành công trong n phép thử), <b>Poisson</b> (đếm biến cố hiếm) và <b>chuẩn</b> (liên tục, trung tâm của thống kê). Câu 1 của mọi đề cuối kỳ là bài chuẩn: tính xác suất và tìm phân vị.</p>'
                + ul(['B(n, p): μ = np, σ² = np(1 − p)', 'Poisson(μ): μ = σ²; xấp xỉ nhị thức khi p nhỏ', 'N(μ, σ²): chuẩn hóa Z = (X − μ)/σ; bảng A7, A8', 'Xấp xỉ chuẩn của nhị thức (hiệu chỉnh 0.5); chọn mô hình đúng']),
                K + 'Bài học 1 · Chương 1, mục 1.10 · Kreyszig §24.7–24.8', 'Nhị thức, Poisson và phân phối chuẩn',
                explain='Đếm số lần ra mặt ngửa → nhị thức. Đếm số cuộc gọi đến tổng đài mỗi phút → Poisson. Đo chiều cao, tuổi thọ, sai số → thường xấp xỉ chuẩn.'))
    s.append(sl(ul(['<b>n cố định</b> số phép thử.', 'Mỗi lần chỉ có <b>hai kết quả</b>: thành công / thất bại.', 'Xác suất thành công <b>p không đổi</b> qua các lần.', 'Các lần thử <b>độc lập</b>.'])
                + table(['Tình huống', 'Nhị thức?', 'Vì sao'], [['Tung 10 lần đồng xu, đếm số mặt sấp', 'Có', 'n = 10, p = 0.5, độc lập'], ['Rút 5 thẻ không hoàn lại từ 20 thẻ, đếm thẻ đỏ', 'Không (siêu bội)', 'p thay đổi, không độc lập'], ['Kiểm 30 sản phẩm từ lô rất lớn, đếm lỗi', 'Gần đúng', 'n nhỏ so với lô nên p gần như không đổi'], ['Đếm số lần tung đến khi ra mặt sấp', 'Không (hình học)', 'n không cố định']]),
                K + 'PHẦN 1 · Nhị thức', 'Bốn điều kiện của nhị thức', explain='Nếu một trong bốn điều kiện sai thì dùng mô hình khác. Lấy mẫu không hoàn lại từ tổng thể nhỏ là bẫy phổ biến.'))
    s.append(sl(formula('Nhị thức X ~ B(n, p)', 'f(x)=P(X=x)=\\binom nx p^x(1-p)^{n-x},\\ x=0,\\dots,n,\\qquad \\mu=np,\\ \\sigma^2=np(1-p)', [('n', 'số phép thử độc lập'), ('p', 'xác suất thành công mỗi lần'), ('\\binom nx', 'số cách chọn x lần thành công trong n lần')])
                + '<p>Lý do μ = np: X = X₁ + … + Xₙ với Xᵢ ~ Bernoulli(p) độc lập; E(Xᵢ) = p, Var(Xᵢ) = p(1 − p), cộng n lần.</p>', K + 'PHẦN 1 · Nhị thức', 'Công thức nhị thức'))
    s.append(sl(wb('Ví dụ 1 · Bài 1.29: súc sắc 4 lần', 'Tung súc sắc cân đối 4 lần. Tính xác suất có ít nhất hai mặt sáu.',
                   [m('X\\sim B(4,\\tfrac16)'), m('P(X=0)=(\\tfrac56)^4=\\tfrac{625}{1296},\\ P(X=1)=4\\cdot\\tfrac16(\\tfrac56)^3=\\tfrac{500}{1296}'), m('P(X\\ge2)=1-\\tfrac{625+500}{1296}=\\tfrac{171}{1296}\\approx0.1319')],
                   '<p>Dùng biến cố đối “nhiều nhất 1 mặt sáu” cho nhanh: 1 − P(X ≤ 1).</p>'), K + 'PHẦN 1 · Nhị thức', 'Ít nhất hai mặt sáu'))
    s.append(sl(wb('Ví dụ 2 · Trắc nghiệm đoán mò', 'Đề 10 câu, mỗi câu 4 đáp án, một đúng. Sinh viên chọn bừa. Tính P(đúng ít nhất 6 câu), kỳ vọng và độ lệch chuẩn số câu đúng.',
                   [m('X\\sim B(10,0.25)'), m('E(X)=2.5,\\ \\sigma=\\sqrt{10\\cdot0.25\\cdot0.75}=1.369'), m('P(X\\ge6)=1-F(5)=1-0.9803=0.0197')],
                   '<p>Đoán mò gần như không thể đạt 6/10 (chỉ 2%). Trung bình chỉ 2.5 câu đúng.</p>'), K + 'PHẦN 1 · Nhị thức', 'Đoán mò 10 câu'))
    s.append(sl(wb('Ví dụ 3 · Kiểm tra lô hàng', 'Lô có 5% sản phẩm lỗi. Lấy ngẫu nhiên 20 sản phẩm. Tính P(không lỗi), P(đúng 1 lỗi), P(ít nhất 2 lỗi).',
                   [m('X\\sim B(20,0.05)'), m('P(0)=0.95^{20}=0.3585'), m('P(1)=20\\cdot0.05\\cdot0.95^{19}=0.3774'), m('P(X\\ge2)=1-0.3585-0.3774=0.2642')],
                   '<p>Số lỗi kỳ vọng np = 1; nhưng chỉ 36% khả năng lấy 20 cái mà không gặp lỗi nào.</p>'), K + 'PHẦN 1 · Nhị thức', 'Kiểm lô 20 sản phẩm'))
    s.append(sl(formula('Tính nhanh các giá trị liên tiếp', '\\dfrac{f(x+1)}{f(x)}=\\dfrac{(n-x)\\,p}{(x+1)(1-p)},\\qquad \\text{mode}=\\lfloor (n+1)p\\rfloor')
                + '<p>Ví dụ: B(10, 0.25) có f(0) = 0.0563; f(1) = f(0)·(10·0.25)/(1·0.75) = 0.1877; f(2) = f(1)·(9·0.25)/(2·0.75) = 0.2816 (đỉnh: ⌊11·0.25⌋ = 2).</p>', K + 'PHẦN 1 · Nhị thức', 'Công thức truy hồi và giá trị có khả năng nhất'))
    s.append(sl(sim('binpois'), K + 'PHẦN 1 · Nhị thức', 'Thực hành: nhị thức so với Poisson và chuẩn'))
    parts.append(dict(title='Phân phối nhị thức', bullets=['Điều kiện nhị thức', 'Công thức, μ, σ²', 'Ba ví dụ', 'Truy hồi, mode'], slides=s))
    # ───────── PHẦN 2: POISSON ─────────
    s = []
    s.append(sl(formula('Poisson X ~ P(μ)', 'f(x)=\\dfrac{\\mu^x}{x!}e^{-\\mu},\\ x=0,1,2,\\dots,\\qquad E(X)=\\operatorname{Var}(X)=\\mu', [('\\mu', 'số biến cố trung bình trong khoảng thời gian/không gian xét')])
                + ul(['Đếm biến cố xảy ra ngẫu nhiên, độc lập, với tốc độ trung bình không đổi.', 'Ví dụ: cuộc gọi đến, lỗi in trên trang, hạt phóng xạ, tai nạn trong ngày.', 'Dấu hiệu nhận biết: μ = σ² (trung bình bằng phương sai).']),
                K + 'PHẦN 2 · Poisson', 'Phân phối Poisson', explain='Poisson là giới hạn của nhị thức khi n rất lớn và p rất nhỏ nhưng np = μ giữ nguyên.'))
    s.append(sl(wb('Ví dụ 4 · Tổng đài (Kreyszig PS 24.7/8)', 'Trung bình 300 cuộc/giờ (5 cuộc/phút), tổng đài xử lý tối đa 10 cuộc/phút. Tính P(X = 3), P(quá tải).',
                   [m('X\\sim P(5)'), m('P(X=3)=\\tfrac{5^3}{3!}e^{-5}=0.1404'), m('P(\\text{quá tải})=P(X>10)=1-0.9863=0.0137')],
                   '<p>Khoảng 1.4% số phút bị quá tải — đủ thông tin để quyết định có nâng công suất.</p>'), K + 'PHẦN 2 · Poisson', 'Tổng đài'))
    s.append(sl(wb('Ví dụ 5 · Văn phòng bán vé (Kreyszig PS 24.7/14)', 'Phục vụ tối đa 4 khách/phút; trung bình 150 khách/giờ. Xác suất phải chờ?',
                   [m('\\mu=150/60=2.5\\ \\text{khách/phút}'), m('P(X>4)=1-P(X\\le4)=1-0.8912=0.1088')], '<p>Khoảng 10.9% số phút có người phải chờ.</p>'), K + 'PHẦN 2 · Poisson', 'Văn phòng bán vé'))
    s.append(sl(wb('Ví dụ 6 · Đổi khoảng thời gian', 'Trung bình 2 lỗi in trên một trang. Tính P(một trang không lỗi), và P(3 trang liên tiếp có tổng không quá 3 lỗi).',
                   [m('\\text{Một trang: }\\mu=2,\\ P(0)=e^{-2}=0.1353'), m('\\text{Ba trang: }\\mu=3\\cdot2=6'), m('P(X\\le3)=e^{-6}(1+6+18+36)=0.1512')], '<p>Quy tắc: μ tỉ lệ với độ dài khoảng quan sát; luôn đổi μ theo khoảng xét trước khi tính.</p>'), K + 'PHẦN 2 · Poisson', 'Đổi μ theo khoảng quan sát'))
    s.append(sl(callout('info', 'Điều kiện xấp xỉ nhị thức bằng Poisson', 'n lớn (≥ 100), p nhỏ (≤ 0.01) hoặc np ≤ 10; khi đó B(n, p) ≈ P(μ = np).')
                + wb('Ví dụ 7 · Bài 1.30', 'p = 0.01, n = 100. Tính P(X ≤ 2).',
                     [m('\\mu=np=1'), m('P(X\\le2)\\approx e^{-1}(1+1+\\tfrac12)=2.5e^{-1}=0.9197'), m('\\text{Nhị thức đúng: }0.9206')], '<p>Sai khác chỉ 0.0009 — xấp xỉ tốt.</p>'), K + 'PHẦN 2 · Poisson', 'Poisson xấp xỉ nhị thức'))
    s.append(sl(wb('Ví dụ 8 · Bài 1.32: bó 100 thanh, 4% lỗi', 'Số thanh lỗi trong bó xấp xỉ Poisson μ = 4.', [m('P(k)=\\tfrac{4^k}{k!}e^{-4}')],
                   table(['k', '0', '1', '2', '3', '4', '5'], [['P(X = k)', '0.0183', '0.0733', '0.1465', '0.1954', '0.1954', '0.1563']]) + '<p>Mode kép tại 3 và 4 (khi μ nguyên, f(μ − 1) = f(μ)). Tổng 6 giá trị đầu 0.7852.</p>'), K + 'PHẦN 2 · Poisson', 'Bảng xác suất Poisson(4)'))
    parts.append(dict(title='Phân phối Poisson', bullets=['Công thức', 'Tổng đài, bán vé', 'Đổi khoảng', 'Xấp xỉ nhị thức'], slides=s))
    # ───────── PHẦN 3: CHUẨN ─────────
    s = []
    s.append(sl(formula('Phân phối chuẩn X ~ N(μ, σ²)', 'f(x)=\\dfrac1{\\sigma\\sqrt{2\\pi}}e^{-\\frac12\\left(\\frac{x-\\mu}\\sigma\\right)^2},\\qquad F(x)=\\Phi\\!\\left(\\dfrac{x-\\mu}\\sigma\\right),\\qquad P(a<X\\le b)=\\Phi\\!\\left(\\dfrac{b-\\mu}\\sigma\\right)-\\Phi\\!\\left(\\dfrac{a-\\mu}\\sigma\\right)',
                        [('\\Phi(z)', 'hàm phân phối chuẩn tắc (bảng A7)'), ('\\Phi(-z)=1-\\Phi(z)', 'đối xứng')])
                + ul(['Đường chuông đối xứng qua μ; σ càng lớn càng thấp và rộng.', 'Quy tắc 68–95–99.7: P(|X − μ| < σ) = 0.6827; < 2σ: 0.9545; < 3σ: 0.9973.']),
                K + 'PHẦN 3 · Phân phối chuẩn', 'Phân phối chuẩn và bảng A7', explain='Mọi chuẩn đều quy về chuẩn tắc bằng cách đổi X sang Z = (X − μ)/σ (số độ lệch chuẩn so với trung bình).'))
    s.append(sl(table(['z', 'Φ(z)', 'z', 'Φ(z)'], [['0', '0.5000', '1.5', '0.9332'], ['0.5', '0.6915', '1.96', '0.9750'], ['1.0', '0.8413', '2.0', '0.9772'], ['1.2', '0.8849', '2.5', '0.9938']])
                + ul(['Z âm: Φ(−z) = 1 − Φ(z).', 'P(Z > z) = 1 − Φ(z).', 'P(a < Z < b) = Φ(b) − Φ(a).', 'Dùng trang “Bảng tra” hoặc widget để có giá trị chính xác.']), K + 'PHẦN 3 · Phân phối chuẩn', 'Cách đọc bảng A7'))
    s.append(sl(wb('Ví dụ 9 · IQ', 'X ~ N(100, 15²). Tính P(X > 130) và P(85 < X < 115).',
                   [m('z=\\tfrac{130-100}{15}=2\\Rightarrow P(X>130)=1-\\Phi(2)=0.0228'), m('z_1=-1,\\ z_2=1\\Rightarrow P=\\Phi(1)-\\Phi(-1)=2(0.8413)-1=0.6827')], '<p>Khoảng 2.3% dân số có IQ trên 130; 68% nằm trong ±1σ.</p>'), K + 'PHẦN 3 · Phân phối chuẩn', 'Tính xác suất bằng chuẩn hóa'))
    s.append(sl(callout('info', 'Bài toán ngược: tìm c (bảng A8)', 'P(X ≤ c) = p ⇒ c = μ + σ·z_p, với z_p = Φ⁻¹(p). Hai chiều: P(μ − k < X < μ + k) = γ ⇒ Φ(k/σ) = (1 + γ)/2.')
                + table(['Xác suất', 'z', 'Dùng cho'], [['0.90', '1.282', 'P(X ≤ c) = 90%'], ['0.95', '1.645', 'một phía 5%; khoảng hai phía 90%'], ['0.975', '1.960', 'khoảng hai phía 95%'], ['0.99', '2.326', 'một phía 1%'], ['0.995', '2.576', 'hai phía 99%']])
                + '<p>Ví dụ 10: IQ top 10% bắt đầu từ c = 100 + 1.2816·15 = 119.22.</p>', K + 'PHẦN 3 · Phân phối chuẩn', 'Phân vị: bảng A8 (z)'))
    s.append(sl(wb('Ví dụ 11 · Bài 1.31', 'X ~ N(5; 0.04), σ = 0.2. (a) Tìm c: P(X ≤ c) = 95%. (b) Tìm k: P(5 − k ≤ X ≤ 5 + k) = 90%. (c) Tìm c: P(X ≥ c) = 1%.',
                   ['(a) (c − 5)/0.2 = 1.645 ⇒ c = 5.329.', '(b) Φ(k/0.2) = 0.95 ⇒ k/0.2 = 1.645 ⇒ k = 0.329.', '(c) P(X < c) = 0.99 ⇒ (c − 5)/0.2 = 2.326 ⇒ c = 5.465.'], '<p>Lưu ý: P(X ≥ c) = 1% nghĩa là P(X &lt; c) = 99%.</p>'), K + 'PHẦN 3 · Phân phối chuẩn', 'Ba dạng tìm c và k'))
    s.append(sl(wb('Ví dụ 12 · Bài 1.32: thanh sắt', 'Đường kính X ~ N(2; 0.008²) in. Dung sai 2 ± 0.02 in. (a) Tỉ lệ phế phẩm? (b) Muốn phế phẩm chỉ 4%, dung sai c bằng bao nhiêu?',
                   [m('P(\\text{đạt})=\\Phi(2.5)-\\Phi(-2.5)=0.9876\\Rightarrow\\text{phế phẩm }1.24\\%'), m('2\\Phi(c/0.008)-1=0.96\\Rightarrow c/0.008=2.054\\Rightarrow c=0.0164\\ \\text{in}')], '<p>Dung sai càng chặt, phế phẩm càng nhiều: đánh đổi giữa chất lượng và chi phí.</p>'), K + 'PHẦN 3 · Phân phối chuẩn', 'Thiết kế dung sai'))
    s.append(sl(formula('Tổ hợp tuyến tính của chuẩn độc lập', 'X\\sim N(\\mu_1,\\sigma_1^2),\\ Y\\sim N(\\mu_2,\\sigma_2^2)\\ \\text{độc lập}\\Rightarrow aX+bY\\sim N(a\\mu_1+b\\mu_2,\\ a^2\\sigma_1^2+b^2\\sigma_2^2)')
                + wb('Ví dụ 13', 'Thời gian công đoạn A ~ N(20, 3²) phút, công đoạn B ~ N(30, 4²) phút (độc lập). P(tổng > 55)?',
                     [m('T=X+Y\\sim N(50,\\ 9+16=25),\\ \\sigma=5'), m('P(T>55)=1-\\Phi(1)=0.1587')], '<p>Phương sai cộng (không phải độ lệch chuẩn): σ_T = √(3² + 4²) = 5.</p>'), K + 'PHẦN 3 · Phân phối chuẩn', 'Tổng của hai chuẩn'))
    s.append(sl(sim('normcalc'), K + 'PHẦN 3 · Phân phối chuẩn', 'Thực hành: máy tính phân phối chuẩn'))
    parts.append(dict(title='Phân phối chuẩn', bullets=['Chuẩn hóa, bảng A7', 'Tìm phân vị, bảng A8', 'Dung sai', 'Tổ hợp tuyến tính'], slides=s))
    # ───────── PHẦN 4: XẤP XỈ ─────────
    s = []
    s.append(sl(formula('Xấp xỉ chuẩn của nhị thức', 'P(a\\le X\\le b)\\approx\\Phi(\\beta)-\\Phi(\\alpha),\\quad \\alpha=\\dfrac{a-np-0.5}{\\sqrt{np(1-p)}},\\ \\beta=\\dfrac{b-np+0.5}{\\sqrt{np(1-p)}}', [('\\pm0.5', 'hiệu chỉnh liên tục (rời rạc → liên tục)')])
                + '<p>Điều kiện: np &gt; 5 và n(1 − p) &gt; 5. Lý do hiệu chỉnh 0.5: giá trị rời rạc x được “trải” thành khoảng [x − 0.5, x + 0.5] trên trục liên tục.</p>', K + 'PHẦN 4 · Xấp xỉ', 'Xấp xỉ chuẩn của nhị thức'))
    s.append(sl(wb('Ví dụ 14 · Ví dụ 1.33', 'n = 400, p = 0.8. Tính P(300 ≤ X ≤ 360).',
                   [m('\\mu=320,\\ \\sigma=\\sqrt{400\\cdot0.8\\cdot0.2}=8'), m('\\alpha=\\tfrac{299.5-320}{8}=-2.5625,\\ \\beta=\\tfrac{360.5-320}{8}=5.0625'), m('P\\approx\\Phi(5.0625)-\\Phi(-2.5625)=1-0.0052=0.9948')], '<p>Giá trị nhị thức đúng: 0.9938. Giáo trình in β = 7.5625 (lỗi in; đúng 5.0625) nhưng kết quả cuối vẫn 0.9948.</p>'), K + 'PHẦN 4 · Xấp xỉ', 'Xấp xỉ có hiệu chỉnh'))
    s.append(sl(wb('Ví dụ 15 · Đồng xu', 'Tung đồng xu cân đối 100 lần. Tính P(45 ≤ X ≤ 55).',
                   [m('\\mu=50,\\ \\sigma=5'), m('P\\approx\\Phi(\\tfrac{55.5-50}5)-\\Phi(\\tfrac{44.5-50}5)=\\Phi(1.1)-\\Phi(-1.1)=0.7286'), m('\\text{Đúng: }0.7287;\\ \\text{không hiệu chỉnh: }2\\Phi(1)-1=0.6827\\ (\\text{sai nhiều})')], '<p>Quên hiệu chỉnh 0.5 làm kết quả lệch 4%.</p>'), K + 'PHẦN 4 · Xấp xỉ', 'Tác dụng của hiệu chỉnh 0.5'))
    s.append(sl(table(['Tình huống', 'Mô hình', 'Điều kiện'],
                      [['Đếm thành công trong n lần thử độc lập', 'B(n, p)', 'n cố định, p không đổi'], ['Đếm biến cố hiếm theo thời gian/không gian', 'Poisson(μ)', 'μ = tốc độ × độ dài'], ['B(n, p) với n lớn, p nhỏ', 'Poisson(np)', 'n ≥ 100, p ≤ 0.01 hoặc np ≤ 10'], ['B(n, p) với np, n(1 − p) > 5', 'N(np, np(1 − p))', 'có hiệu chỉnh ±0.5'], ['Đại lượng liên tục đo được, đối xứng', 'N(μ, σ²)', 'dữ liệu hình chuông']]), K + 'PHẦN 4 · Xấp xỉ', 'Chọn mô hình nào?'))
    parts.append(dict(title='Xấp xỉ và chọn mô hình', bullets=['Hiệu chỉnh 0.5', 'Ví dụ 1.33', 'Chọn mô hình'], slides=s))
    # ───────── PHẦN 5: BÀI THẬT ─────────
    s = []
    s.append(sl(wb('Đề HK2 (3TC) đề số 1, câu 1', 'X ~ N(12.5; 0.809²) — tuổi thọ muỗi (ngày). (a) P(X ≤ 13.7135). (b) Tìm c để P(X ≥ c) = 1%.',
                   [m('z=\\dfrac{13.7135-12.5}{0.809}=1.5\\Rightarrow P(X\\le13.7135)=\\Phi(1.5)=0.9332'), m('P(X\\ge c)=0.01\\Rightarrow \\Phi\\!\\left(\\tfrac{c-12.5}{0.809}\\right)=0.99\\Rightarrow \\tfrac{c-12.5}{0.809}=2.326'), m('c=12.5+2.326\\cdot0.809=14.382')]), K + 'PHẦN 5 · Bài thật có lời giải', 'Câu 1 đề cuối kỳ HK2'))
    s.append(sl(wb('Đề mẫu 03/2024, đề số 1, câu 1', 'X ~ N(μ = 8.3; σ² = 0.16), σ = 0.4. Tìm a = P(X ≤ 8.9) và b = P(X ≥ 8.78).',
                   ['z = (8.9 − 8.3)/0.4 = 1.5 ⇒ a = Φ(1.5) = 0.9332.', 'z = (8.78 − 8.3)/0.4 = 1.2 ⇒ b = 1 − Φ(1.2) = 1 − 0.8849 = 0.1151.']), K + 'PHẦN 5 · Bài thật có lời giải', 'Đề mẫu 2024'))
    s.append(sl(wb('Đáp án giữa kỳ HK2, câu 3', 'X ~ N(44.4; 7.12²). Tỉ lệ P(44.4 ≤ X ≤ 51.52) rồi xác suất đúng 2 người trong 6.',
                   ['z₁ = 0, z₂ = (51.52 − 44.4)/7.12 = 1 ⇒ p = Φ(1) − Φ(0) = 0.3413.', 'Mỗi người “thuộc khoảng” độc lập với xác suất p ⇒ nhị thức: C(6,2)p²(1 − p)⁴ = 0.3289.'], '<p>Đây là cách nối chuẩn và nhị thức: xác suất chuẩn trở thành tham số p của nhị thức.</p>'), K + 'PHẦN 5 · Bài thật có lời giải', 'Chuẩn rồi nhị thức (giữa kỳ HK2)'))
    s.append(sl(wb('Kreyszig PS 24.8/9 · Điểm SAT', 'X ~ N(480; 100²). Tỉ lệ thí sinh không đạt 500 điểm?', [m('z=\\tfrac{500-480}{100}=0.2'), m('P(X<500)=\\Phi(0.2)=0.5793\\approx57.9\\%')]), K + 'PHẦN 5 · Bài thật có lời giải', 'Kreyszig 24.8/9: điểm SAT'))
    parts.append(dict(title='Bài thật có lời giải', bullets=['Câu 1 đề HK2', 'Đề mẫu 2024', 'Chuẩn → nhị thức', 'SAT'], slides=s))
    # ───────── PHẦN 6: BẪY ─────────
    s = []
    s.append(sl(ul(['<b>Quên chuẩn hóa</b>: dùng σ, không phải σ².', '<b>Nhầm σ² và σ</b>: đề cho phương sai thì lấy căn.', '<b>Tra A7 với z âm</b>: Φ(−z) = 1 − Φ(z).', '<b>P(X ≥ c) = p</b> ⇒ P(X &lt; c) = 1 − p (không phải p).', '<b>Quên hiệu chỉnh 0.5</b> khi xấp xỉ nhị thức bằng chuẩn.', '<b>Dùng Poisson khi p không nhỏ</b> hoặc n không lớn.', '<b>Chuẩn hóa tổng</b>: cộng phương sai chứ không cộng σ.']), K + 'PHẦN 6 · Bẫy, tổng kết', 'Bảy bẫy thường gặp'))
    s.append(sl(callout('warn', 'Lỗi in trong giáo trình', 'Ví dụ 1.31(a) in “1.654” (đúng 1.645); Ví dụ 1.33 in β = 7.5625 (đúng 5.0625; kết quả vẫn 0.9948).') + '<p>Các tham số của đề 2021–2022 câu 1(b) cho đáp án chính thức k âm (−1.702 và −2.758): đây là hệ quả của tham số đề (b lớn), ghi nhận ở trang Tài liệu.</p>', K + 'PHẦN 6 · Bẫy, tổng kết', 'Sai sót đã phát hiện'))
    s.append(sl('<p><b>Case study: kiểm soát chất lượng.</b> Dây chuyền đóng gói gạo, khối lượng mỗi túi X ~ N(500, 4²) gam. Cần đặt mức tối thiểu c sao cho chỉ 1% túi nhẹ hơn c: c = 500 − 2.326·4 = 490.7 g. Nếu giảm σ xuống 2 g thì c = 495.3 g — nhà sản xuất có thể ghi nhãn nặng hơn mà ít lỗ hơn. Đó là lý do công nghiệp theo đuổi giảm σ (nền của biểu đồ kiểm soát, Module 12).</p>', K + 'PHẦN 6 · Bẫy, tổng kết', 'Case study: đóng gói gạo'))
    s.append(sl(ul(['Nhị thức: đếm thành công; Poisson: biến cố hiếm; chuẩn: liên tục đối xứng.', 'P(a < X < b) = Φ(z₂) − Φ(z₁); phân vị c = μ + σz.', 'Xấp xỉ: np > 5 và n(1 − p) > 5 ⇒ chuẩn có hiệu chỉnh 0.5; p nhỏ ⇒ Poisson.']) + callout('good', 'Tiếp theo', 'Chương 2: mẫu ngẫu nhiên, ước lượng điểm và khoảng tin cậy (Module 7–8).'), K + 'PHẦN 6 · Bẫy, tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Bẫy, ứng dụng và tổng kết', bullets=['Bảy bẫy', 'Lỗi in', 'Case study', 'Tổng kết'], slides=s))
    notes = ('<h2>Đọc kèm giáo trình</h2><p>Lecture Notes §1.10: nhị thức (1.34–1.36), Poisson (1.37–1.38), chuẩn (1.39–1.43, bảng A7/A8), xấp xỉ chuẩn của nhị thức (1.44–1.45). Kreyszig §24.7 (nhị thức, Poisson, siêu bội; PS 24.7 gồm 16 bài) và §24.8 (chuẩn, định lý De Moivre–Laplace; PS 24.8 gồm 15 bài). Ngân hàng câu hỏi có cả 10 câu 1 của các đề cuối kỳ.</p>'
             '<h2>Thực hành tương tác</h2>' + sim('normcalc') + sim('binpois')
             + '<h2>Bối cảnh lịch sử</h2>' + callout('info', '📜 Từ Bernoulli đến Gauss', 'Nhị thức do Jacob Bernoulli (1713); Poisson (1837) nghiên cứu giới hạn p → 0; De Moivre (1733) tìm xấp xỉ chuẩn của nhị thức, Laplace mở rộng; Gauss dùng phân phối chuẩn mô tả sai số đo (đường cong chuông). Bảng A7/A8 là bản in các giá trị Φ và Φ⁻¹.')
             + callout('warn', 'Chú ý khi làm bài', '• Viết rõ z trước khi tra bảng; làm tròn z đến 2 chữ số khi tra A7.<br>• Dùng chính xác đáp án từ phần mềm khi đề không yêu cầu bảng.<br>• Nhớ P(X = a) = 0 với biến liên tục: “≤” và “&lt;” cho cùng xác suất.'))
    return dict(id='m06', slug='m06-nhi-thuc-poisson-chuan', title='Phân phối nhị thức, Poisson và phân phối chuẩn', subtitle='B(n, p), Poisson(μ), N(μ, σ²), chuẩn tắc, bảng A7/A8, xấp xỉ chuẩn',
                source='Lecture Notes §1.10, Bài 1.32–1.39 · Kreyszig §24.7–24.8 (PS 24.7, 24.8) · Câu 1 các đề cuối kỳ 2021–2024 · Giữa kỳ mẫu câu 1, 7', exam='Câu 1 MỌI đề cuối kỳ; câu 7 đề giữa kỳ mẫu; câu 3 giữa kỳ HK2', time='≈ 5 giờ',
                objectives=['Tính xác suất và phân vị cho nhị thức, Poisson, chuẩn', 'Chuẩn hóa và tra bảng A7 (Φ), A8 (z)', 'Dùng xấp xỉ Poisson và chuẩn (có hiệu chỉnh 0.5) đúng điều kiện', 'Giải đúng dạng câu 1 của đề cuối kỳ (P(X ≤ a) và tìm c)'], parts=parts, notes=notes, sims=['normcalc', 'binpois'])
