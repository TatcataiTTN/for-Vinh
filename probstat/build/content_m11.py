from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Hai kiểm định mới: <b>phương sai</b> của tổng thể chuẩn (phân phối χ²) và <b>so sánh hai kỳ vọng</b> (t gộp). Kreyszig §25.4 bổ sung kiểm định F so sánh hai phương sai. Các bài này hiện ra trong Bài 3.10–3.15 và PS 25.4/12–20.</p>' + ul(['χ²(m): đuôi phải, bảng A10', 'Kiểm định σ² = σ₀² (3 dạng)', 'So sánh μ₁ = μ₂: T ~ t(n₁ + n₂ − 2)', 'Kiểm định F: s₁²/s₂² ~ F(n₁ − 1, n₂ − 1)']), 'MODULE 11 · Bài học 4 · Chương 3, mục 3.3–3.4 · Kreyszig §25.4', 'Kiểm định phương sai và so sánh hai kỳ vọng', explain='Độ ổn định (phương sai) quan trọng không kém trung bình: một máy trung bình đúng nhưng dao động lớn vẫn cho sản phẩm hỏng.'))
    s.append(sl(formula('Phân phối χ² và định lý', 'Y=\\dfrac{(n-1)S^2}{\\sigma^2}\\sim\\chi^2(n-1)', [('\\chi^2_\\alpha(m)', 'P(χ² > c) = α; bảng A10; giá trị ≥ 0, lệch phải')]), 'PHẦN 1 · Nền tảng', 'Phân phối χ²', explain='χ²(m) là tổng bình phương m biến chuẩn tắc độc lập; tâm quanh m và lệch phải.'))
    parts.append(dict(title='Nền tảng', bullets=['Phân phối χ²'], slides=s))
    s = []
    s.append(sl(formula('Kiểm định phương sai', 'T=\\dfrac{(n-1)S^2}{\\sigma_0^2},\\ H_1:\\sigma^2>\\sigma_0^2\\Rightarrow T>\\chi^2_\\alpha;\\ \\sigma^2<\\sigma_0^2\\Rightarrow T<\\chi^2_{1-\\alpha};\\ \\ne\\Rightarrow T<\\chi^2_{1-\\alpha/2}\\text{ hoặc }T>\\chi^2_{\\alpha/2}') + '<p>Ví dụ 3.4: n = 15, s² = 13, σ₀² = 10: T = 18.2 ≤ χ²₀.₀₅(14) = 23.68 ⇒ chấp nhận H₀.</p>', 'PHẦN 2 · Phương pháp', 'Ba dạng kiểm định phương sai'))
    s.append(sl(sim('chi2'), 'PHẦN 2 · Phương pháp', 'Thực hành: kiểm định χ²'))
    s.append(sl(formula('So sánh hai kỳ vọng', 'T=\\dfrac{\\bar X-\\bar Y}{S\\sqrt{\\frac1{n_1}+\\frac1{n_2}}}\\sim t(n_1+n_2-2),\\quad S^2=\\dfrac{(n_1-1)S_X^2+(n_2-1)S_Y^2}{n_1+n_2-2}') + '<p>Khi n₁ = n₂ = n: T = √n(x̄ − ȳ)/√(s_X² + s_Y²) ~ t(2n − 2) (Ví dụ 3.5).</p>' + callout('info', 'Kiểm định F', 'H₁: σ_X² > σ_Y²: v₀ = s_X²/s_Y² > F_α(n₁ − 1, n₂ − 1) ⇒ bác bỏ. Ví dụ 6 Kreyszig: v₀ = 1.26 < 3.79 ⇒ chấp nhận cùng phương sai.'), 'PHẦN 2 · Phương pháp', 'So sánh hai kỳ vọng và kiểm định F'))
    s.append(sl(sim('twomean'), 'PHẦN 2 · Phương pháp', 'Thực hành: so sánh hai kỳ vọng'))
    parts.append(dict(title='Phương pháp', bullets=['Phương sai', 'Hai kỳ vọng', 'Hai widget'], slides=s))
    s = []
    s.append(sl(callout('info', 'Ví dụ 3.5', 'Sản lượng hai môi trường (n₁ = n₂ = 8): x̄ = 105.125, ȳ = 97.5; s_X² = 106.125, s_Y² = 84.') + steps([m_('T=\\sqrt8\\cdot\\dfrac{7.625}{\\sqrt{190.125}}=1.564'), 't₀.₀₂₅(14) = 2.145 ⇒ |T| ≤ 2.145 ⇒ chấp nhận H₀: hai trung bình bằng nhau.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: hai môi trường làm việc'))
    s.append(sl(callout('info', 'Bài 3.11 (pin)', 'H₁: σ < 5; n = 28, s = 3.5, α = 5%.') + steps([m_('T=\\dfrac{27\\cdot3.5^2}{25}=13.23'), 'Miền bác bỏ T < χ²₀.₉₅(27) = 16.151 ⇒ bác bỏ H₀: σ < 5 giờ ⇒ nên thay pin theo chu kỳ cố định.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: độ lệch chuẩn tuổi thọ pin'))
    s.append(sl(callout('info', 'Bài 3.13 (xăng A, B)', 'A: n = 16, x̄ = 19.6, s = 0.4; B: n = 16, x̄ = 20.2, s = 0.6; H₁: μ_B > μ_A, α = 5%.') + steps(['S = 0.5099; T = 0.6/(0.5099·√(1/8)) = 3.328.', 't₀.₀₅(30) = 1.697 ⇒ bác bỏ H₀: xăng B tốt hơn.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 3: hai loại xăng'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Hai môi trường', 'Pin', 'Hai loại xăng'], slides=s))
    s = []
    s.append(sl(ul(['<b>Nhầm hướng đuôi χ²</b>: σ² < σ₀² dùng χ²_{1−α} (đuôi trái).', '<b>Bậc tự do</b>: n − 1 (một mẫu), n₁ + n₂ − 2 (hai mẫu).', '<b>Dùng s thay s²</b> trong T.', '<b>Quên điều kiện cùng phương sai</b>: kiểm tra bằng F.', '<b>Kết luận</b>: nói rõ “bác bỏ” hay “chưa đủ cơ sở bác bỏ”.']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy'], slides=s))
    s = []
    s.append(sl('<p><b>Máy đóng gói.</b> Độ lệch chuẩn khối lượng gói trước đây 0.8 oz; mẫu 20 gói có s = 1.0: T = 29.69 &lt; 30.14 ⇒ chưa đủ bằng chứng σ tăng (Kreyszig PS 25.4/15). Phân biệt “không có bằng chứng” và “có bằng chứng không đổi”.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: máy đóng gói'))
    s.append(sl(ul(['σ²: T = (n − 1)s²/σ₀² ~ χ²(n − 1).', 'μ₁ vs μ₂: t gộp, n₁ + n₂ − 2 bậc tự do.', 'F: s₁²/s₂² ~ F(n₁ − 1, n₂ − 1).']) + callout('good', 'Tiếp theo', 'Module 12: biểu đồ kiểm soát, χ² phù hợp, phi tham số.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Máy đóng gói', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §3.3 (phân phối χ², Định lý 3.1, kiểm định σ², Bài toán 1–3, Ví dụ 3.4) và §3.4 (so sánh kỳ vọng, t gộp, Ví dụ 3.5). Kreyszig §25.4: Ví dụ 5–6 (F). Câu hỏi gốc: Bài 3.10–3.15 và PS 25.4/12–20.</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Bài 3.10', '<p>σ = 0.8, n = 20, s = 1.0: T = 19/0.64 = 29.69; χ²₀.₀₅(19) = 30.14 ⇒ chấp nhận H₀.</p>')
    notes += ex('2. Bài 3.12', '<p>σ = 1, n = 30, s = 1.1, α = 0.01 hai phía: T = 29·1.21 = 35.09 ∈ [13.12; 52.34] ⇒ chấp nhận H₀.</p>')
    notes += ex('3. Bài 3.14: hai loại bi', '<p>x̄₁ = 2.6325, x̄₂ = 2.59375; T gộp = 2.611 vs t₀.₀₂₅(14) = 2.145 ⇒ bác bỏ H₀ ở mức 5% (đường kính hai loại bi khác nhau).</p>')
    notes += ex('4. Bài 3.15: trẻ sơ sinh', '<p>S = 0.3536; T = 0.2/(0.3536·√(2/500)) = 8.94 ≫ 1.646 ⇒ bác bỏ H₀.</p>')
    notes += ex('5. Kreyszig PS 25.4/20', '<p>σ = 3 chung, n = 12, 18, x̄ = 10, 14: z = −3.578; |z| > 1.96 ⇒ bác bỏ H₀.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('chi2') + sim('twomean')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Pearson, Fisher', 'Karl Pearson đưa phân phối χ² (1900); Fisher phát triển F (1924) và phân tích phương sai; t gộp cho hai mẫu là công trình của Gosset/Fisher.')
    notes += '<h2>5. Case study</h2><p>Kiểm soát chất lượng: so sánh hai dây chuyền bằng t gộp nhưng trước hết dùng F để kiểm tra cùng phương sai.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Tra đúng bậc tự do.<br>• T < giá trị χ² trái cũng có thể là miền bác bỏ.<br>• Nêu rõ giả thiết cùng phương sai.')
    return dict(id='m11', slug='m11-chi-binh-phuong-hai-mau', title='Phân phối χ², kiểm định phương sai, so sánh kỳ vọng hai phân phối chuẩn', subtitle='χ²(n − 1), σ² = σ₀², t gộp cho hai kỳ vọng, kiểm định F',
                source='Lecture Notes §3.3–3.4, Bài 3.10–3.15 · Kreyszig §25.4 (Ví dụ 5–6, PS 25.4/12–20)', exam='Không thuộc cấu trúc đề thi đã công bố nhưng thuộc đề cương Chương 3', time='≈ 4 giờ',
                objectives=['Dùng χ² với đúng bậc tự do và đuôi', 'Kiểm định σ² một phía và hai phía', 'So sánh hai kỳ vọng với t gộp', 'Dùng F so sánh hai phương sai'], parts=parts, notes=notes, sims=['chi2', 'twomean'])
