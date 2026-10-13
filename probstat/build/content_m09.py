from hx import *
def module():
    parts = []
    s = []
    s.append(sl('<p>Bài học 3 của đề cương là <b>Kiểm tra bài 1</b> (giữa kỳ, hình thức tự luận và trắc nghiệm, chiếm 30% điểm học phần). Module này gom Chương 1–2: bảng công thức, bản đồ câu hỏi, đề giữa kỳ mẫu có lời giải và ngân hàng ôn tập chọn lại từ câu gốc của Module 1–8.</p>' + ul(['Bản đồ: câu hỏi đề ↔ module', 'Bảng công thức tổng hợp Chương 1–2', 'Đề giữa kỳ mẫu: 8 câu trắc nghiệm + 1 câu tự luận 6 điểm', 'Ngân hàng ôn tập (gồm câu thuộc đề giữa kỳ)']), 'MODULE 9 · Bài học 3 · Kiểm tra bài 1', 'Ôn tập Chương 1–2 và đề giữa kỳ', explain='Giữa kỳ có 9 câu: 8 câu trắc nghiệm 0.5 điểm và 1 câu tự luận 6 điểm (ước lượng khoảng).'))
    s.append(sl(diag('../../img/m09.png', 'Bản đồ ôn tập', 'Mỗi câu của đề thuộc module nào.'), 'PHẦN 1 · Nền tảng', 'Bản đồ câu hỏi đề thi'))
    parts.append(dict(title='Nền tảng', bullets=['Cấu trúc kiểm tra', 'Bản đồ ôn tập'], slides=s))
    s = []
    s.append(sl(table(['Chủ đề', 'Công thức chính'], [['Mẫu', 'x̄ = Σx/n; s² = Σ(x − x̄)²/(n − 1); IQR = qU − qL'], ['Đếm', 'A(n,k) = n!/(n−k)!; C(n,k) = n!/(k!(n−k)!)'], ['Xác suất', 'P(A∪B) = P(A) + P(B) − P(A∩B); P(A|B) = P(A∩B)/P(B)'], ['Toàn phần/Bayes', 'P(B) = ΣP(B|Aᵢ)P(Aᵢ); P(Aᵢ|B) = P(B|Aᵢ)P(Aᵢ)/P(B)'], ['BNN', 'E(X) = Σxp = ∫xf; Var = E(X²) − μ²'], ['Nhị thức', 'P(X=k) = C(n,k)pᵏ(1−p)ⁿ⁻ᵏ; μ = np; σ² = np(1−p)'], ['Chuẩn', 'P(a\\lt X\\lt b) = Φ((b−μ)/σ) − Φ((a−μ)/σ)'], ['MLE', 'ln l = Σln f; ∂/∂θ = 0'], ['CI (σ biết)', 'x̄ ± U·σ/√n'], ['CI (σ chưa biết)', 'x̄ ± t(n−1)·s/√n']]), 'PHẦN 2 · Phương pháp', 'Bảng công thức Chương 1–2'))
    s.append(sl(formula('Hai công thức hay sai nhất', 'P(A_i\\mid B)=\\dfrac{P(B\\mid A_i)P(A_i)}{\\sum_jP(B\\mid A_j)P(A_j)},\\qquad \\bar x\\pm t_{\\alpha/2}(n-1)\\dfrac{s}{\\sqrt n}') + '<p>Bayes: mẫu số là P(B) đầy đủ. CI: bậc tự do n − 1, α/2 mỗi phía.</p>', 'PHẦN 2 · Phương pháp', 'Hai công thức cần thuộc'))
    s.append(sl(formula('Chuẩn hoá', 'z=\\dfrac{x-\\mu}{\\sigma},\\quad P(a\\lt X\\lt b)=\\Phi\\!\\left(\\dfrac{b-\\mu}\\sigma\\right)-\\Phi\\!\\left(\\dfrac{a-\\mu}\\sigma\\right)') + '<p>Tìm c: c = μ + σ·z_p với Φ(z_p) = p (bảng A8).</p>', 'PHẦN 2 · Phương pháp', 'Chuẩn hoá và phân vị'))
    s.append(sl(sim('tables'), 'PHẦN 2 · Phương pháp', 'Bảng tra điện tử A7, A8, A9'))
    parts.append(dict(title='Phương pháp', bullets=['Bảng công thức', 'Bảng tra'], slides=s))
    s = []
    s.append(sl(callout('info', 'Đề giữa kỳ mẫu, câu 1–4', 'U₀.₀₈ = 1.405; C(13,2)·C(17,3) = 53 040; P(Ā) = 0.43; 0.57³ = 0.185193.'), 'PHẦN 3 · Ví dụ', 'Lời giải câu 1–4'))
    s.append(sl(callout('info', 'Đề giữa kỳ mẫu, câu 5–8', 'Câu 5: P = 0.07; câu 6: k = 0.68; câu 7: P(4.0 < X < 4.29) = 0.7320 (z từ −1 đến 1.23); câu 8: t₀.₀₈(18) ≈ 1.466.'), 'PHẦN 3 · Ví dụ', 'Lời giải câu 5–8'))
    s.append(sl(callout('info', 'Đề giữa kỳ mẫu, câu 9 (6 điểm)', 'x̄ = 10.1538; s² = 3.8954; khoảng 90% với σ = 0.5: x̄ ± 0.161; không biết σ: x̄ ± t₀.₀₅(25)·s/√26 = x̄ ± 0.661.'), 'PHẦN 3 · Ví dụ', 'Lời giải câu 9'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Câu 1–4', 'Câu 5–8', 'Câu 9'], slides=s))
    s = []
    s.append(sl(ul(['Làm đủ tối thiểu 3 chữ số thập phân.', 'Không dùng μ ± σ cho phương sai: đọc “σ² = …”.', 'Bayes: kiểm tra hậu nghiệm cộng bằng 1.', 'CI: điểm giữa lớp và N chuẩn trước khi tra bảng.']), 'PHẦN 4 · Bẫy và mở rộng', 'Checklist ôn thi'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Checklist'], slides=s))
    s = []
    s.append(sl(ul(['Làm lại đề giữa kỳ mẫu trong 45 phút.', 'Vào ngân hàng ôn tập (136 câu).', 'Chuyển sang Chương 3: kiểm định giả thuyết.']), 'PHẦN 5 · Ứng dụng và tổng kết', 'Kế hoạch cuối'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Kế hoạch ôn'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Bài học 3 của đề cương là kiểm tra giữa kỳ (B1, 30%). Tài liệu có: <b>đề giữa kỳ mẫu</b> (ảnh, đã OCR và đối chiếu thủ công) và <b>đáp án giữa kỳ HK2 2022–2023</b> (xlsx với tham số a, b, c). Ngân hàng ôn tập của module chọn lại các câu gốc quan trọng từ Module 1–8.</p><h2>2. Đề giữa kỳ mẫu có lời giải</h2>'
    notes += ex('Câu 1–9', '<ol><li>U₀.₀₈ = 1.405.</li><li>C(13,2)C(17,3) = 78·680 = 53 040.</li><li>P(Ā) = 0.43.</li><li>P = 0.57³ = 0.1852.</li><li>P = 0.07.</li><li>k = 0.68.</li><li>Φ(1.23) − Φ(−1) = 0.7320.</li><li>t₀.₀₈(18) ≈ 1.466.</li><li>(a) x̄ = 10.1538, s² = 3.8954; (b) ±0.161; (c) ±0.661.</li></ol>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('tables')
    notes += '<h2>4. Bối cảnh</h2><p>Hai đề giữa kỳ có tham số học sinh (a, b, c) nên số liệu mỗi sinh viên khác nhau; câu hỏi cùng dạng với các câu trong ngân hàng.</p><h2>5. Case study</h2><p>Dùng đáp án giữa kỳ HK2 như một đề mẫu: bốn câu bao quát Bayes, bảng phân phối, chuẩn + nhị thức và khoảng tin cậy t.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', 'Chú ý đơn vị và làm tròn; giữ các giá trị trung gian đủ chữ số.')
    return dict(id='m09', slug='m09-on-tap-giua-ky', title='Ôn tập Chương 1–2 và luyện đề giữa kỳ', subtitle='Bản đồ ôn tập, bảng công thức, lời giải đề giữa kỳ mẫu, ngân hàng ôn tập',
                source='Đề giữa kỳ mẫu LTXSTK (ảnh, OCR + kiểm tay) · Đáp án giữa kỳ HK2 2022–2023 · câu gốc Module 1–8', exam='Toàn bộ đề giữa kỳ', time='≈ 3 giờ',
                objectives=['Biết cấu trúc đề giữa kỳ', 'Giải đề giữa kỳ mẫu từ đầu đến cuối', 'Ôn nhanh bằng bảng công thức và bảng tra', 'Luyện ngân hàng ôn tập'], parts=parts, notes=notes, sims=['tables'])
