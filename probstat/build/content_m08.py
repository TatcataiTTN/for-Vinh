from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Ước lượng điểm cho một con số nhưng không nói độ chính xác. <b>Khoảng tin cậy</b> cho một khoảng [θ₁; θ₂] chứa tham số với độ tin cậy γ (90%, 95%, 99%). Đây là câu 2 của mọi đề cuối kỳ: cho bảng dữ liệu theo lớp, tìm khoảng tin cậy cho trung bình.</p>' + ul(['μ khi σ đã biết (U), khi σ chưa biết (Student)', 'Tỷ lệ p (n lớn); cỡ mẫu tối thiểu', 'Mở rộng: khoảng cho σ² bằng χ²', 'Dữ liệu theo lớp: điểm giữa lớp']),
                'MODULE 8 · Bài học 2 · Chương 2, mục 2.3 · Kreyszig §25.3', 'Ước lượng khoảng',
                explain='“Độ tin cậy 95%” nghĩa là phương pháp dựng khoảng này bắt trúng tham số thật trong 95% các lần lấy mẫu.'))
    s.append(sl(diag('../../img/m08.png', 'Sơ đồ chọn khoảng tin cậy', 'Chọn công thức theo tham số, σ biết hay chưa, cỡ mẫu.'), 'PHẦN 1 · Nền tảng', 'Sơ đồ chọn công thức'))
    s.append(sl(sim('ciplay'), 'PHẦN 1 · Nền tảng', 'Thực hành: ý nghĩa độ tin cậy'))
    parts.append(dict(title='Nền tảng', bullets=['Vì sao cần khoảng', 'Sơ đồ chọn công thức', 'Mô phỏng độ tin cậy'], slides=s))
    s = []
    s.append(sl(formula('σ đã biết', '\\bar x-k\\le\\mu\\le\\bar x+k,\\quad k=\\dfrac{U_{\\alpha/2}\\,\\sigma}{\\sqrt n},\\quad \\alpha=1-\\gamma', [('U_{\\alpha/2}', 'giá trị tới hạn chuẩn: 1.645 (90%), 1.960 (95%), 2.576 (99%)')]) + '<p>Ví dụ 2.5: σ² = 9, n = 100, x̄ = 5, γ = 95%: k = 1.96·3/10 = 0.588 ⇒ [4.412; 5.588]. Cỡ mẫu: L = 2k ⇒ n ≥ (2Uσ/L)².</p>', 'PHẦN 2 · Phương pháp', 'Khoảng cho μ khi σ biết'))
    s.append(sl(formula('σ chưa biết', 'k=\\dfrac{t_{\\alpha/2}(n-1)\\,s}{\\sqrt n},\\quad T=\\dfrac{\\bar X-\\mu}{S/\\sqrt n}\\sim t(n-1)', [('t_{\\alpha/2}(n-1)', 'bảng A9; luôn lớn hơn U ⇒ khoảng rộng hơn')]) + '<p>Ví dụ 2.7: diesel 144, 147, 146, 142, 144: x̄ = 144.6, s² = 3.8; t₀.₀₀₅(4) = 4.604 ⇒ k ≈ 4.0 ⇒ [140.6; 148.6].</p>', 'PHẦN 2 · Phương pháp', 'Khoảng cho μ khi σ chưa biết'))
    s.append(sl(formula('Tỷ lệ p', 'f\\pm U_{\\alpha/2}\\sqrt{\\dfrac{f(1-f)}{n}}', [('f', 'tần suất mẫu = x̄ của dãy 0/1')]) + '<p>Ví dụ 2.8: 960/1600 = 0.6 ⇒ k = 0.024 ⇒ [0.576; 0.624].</p>' + callout('info', 'Dữ liệu theo lớp', 'Bước 1: điểm giữa lớp, N = Σnᵢ. Bước 2: x̄, s. Bước 3: tra U hoặc t(N − 1). Bước 4: x̄ ± k.'), 'PHẦN 2 · Phương pháp', 'Khoảng cho tỷ lệ và bảng lớp'))
    s.append(sl(sim('cicalc'), 'PHẦN 2 · Phương pháp', 'Thực hành: máy tính khoảng tin cậy'))
    parts.append(dict(title='Phương pháp', bullets=['σ biết', 'σ chưa biết', 'Tỷ lệ, bảng lớp', 'Máy tính'], slides=s))
    s = []
    s.append(sl(callout('info', 'Đề HK2 đề 1 câu 2', 'σ = 16, γ = 95%, lớp 70–85…145–160 với tần số 2, 4, 7, 8, 4, 2.') + steps(['Điểm giữa 77.5; …; 152.5; N = 27; x̄ = 3112.5/27 = 115.278.', 'k = 1.96·16/√27 = 6.035.', 'Khoảng: [109.243; 121.313] — trùng đáp án chính thức.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: σ biết, bảng lớp'))
    s.append(sl(callout('info', 'Đề 2TC đề 1 câu 2', 'Cân nặng 51–66 kg theo 6 lớp rộng 2.5 (2, 4, 7, 8, 4, 2), γ = 90%, σ chưa biết.') + steps(['N = 27; x̄ = 59.3; s ≈ 3.7.', 't₀.₀₅(26) = 1.706; k = 1.706·s/√27.', 'Khoảng: x̄ ± k (xem lời giải đầy đủ trong ngân hàng câu).']), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: σ chưa biết, bảng lớp'))
    s.append(sl(callout('info', 'Kreyszig PS 25.3/8', 'K. Pearson tung đồng xu 24 000 lần được 12 012 ngửa. Khoảng 99% cho p.') + steps(['f = 0.5005; k = 2.576√(0.25/24000) = 0.00831.', 'p ∈ [0.4922; 0.5088] chứa 0.5 ⇒ không có bằng chứng đồng xu không công bằng.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 3: đồng xu của Pearson'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['σ biết', 'σ chưa biết', 'Tỷ lệ'], slides=s))
    s = []
    s.append(sl(ul(['<b>Dùng U thay t</b> khi σ chưa biết (khoảng quá hẹp).', '<b>Quên điểm giữa lớp</b> hoặc dùng sai N khi tính s.', '<b>Dùng α thay α/2</b>: hai phía cần U_{α/2}.', '<b>Nhầm độ dài L = 2k</b> khi tìm cỡ mẫu.', '<b>Diễn giải sai</b>: “xác suất μ ở trong khoảng là 95%” không đúng.', '<b>Làm tròn n</b>: luôn làm tròn lên.']), 'PHẦN 4 · Bẫy và mở rộng', 'Sáu bẫy thường gặp'))
    s.append(sl(callout('info', 'Mở rộng: khoảng cho σ² (Kreyszig PS 25.3/13)', 'n = 20, s² = 0.04: [19·0.04/32.852; 19·0.04/8.907] = [0.0231; 0.0853]. Phân phối χ² được học kỹ ở Module 11.'), 'PHẦN 4 · Bẫy và mở rộng', 'Khoảng tin cậy cho phương sai'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Sáu bẫy', 'Khoảng cho σ²'], slides=s))
    s = []
    s.append(sl('<p><b>Thăm dò bầu cử.</b> 960/1600 ủng hộ A ⇒ [57.6%; 62.4%] ở mức 95%; biên sai số 2.4 điểm phần trăm. Muốn biên ±1% (p ≈ 0.6) cần n ≥ 1.96²·0.24/0.01² ≈ 9220 người. Chi phí mẫu tăng theo 1/ε².</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: thăm dò dư luận'))
    s.append(sl(ul(['Chọn đúng U hay t, đúng bậc tự do N − 1.', 'k = (giá trị tới hạn)·(sai số chuẩn).', 'Độ tin cậy ↑ hoặc n ↓ ⇒ khoảng rộng hơn.']) + callout('good', 'Tiếp theo', 'Module 9 ôn tập Chương 1–2 và đề giữa kỳ.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Thăm dò dư luận', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §2.3.1 (σ biết, Định lý 2.1), §2.3.2 (σ chưa biết, Student, Định lý 2.2), §2.3.3 (tỷ lệ, định lý giới hạn trung tâm). Kreyszig §25.3 và PS 25.3 (20 bài, kể cả khoảng cho phương sai). Câu hỏi gốc gồm Ví dụ 2.5–2.8, Bài 2.2b, 2.5–2.16, PS 25.3 và 12 câu 2 của các đề cuối kỳ cùng giữa kỳ.</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Ví dụ 2.6: cỡ mẫu', '<p>σ = 3, γ = 95%, L = 0.4:</p>' + steps([m_('n\\ge\\left(\\dfrac{2\\cdot1.96\\cdot3}{0.4}\\right)^2=864.4'), m_('n=865\\ \\text{(làm tròn lên)}')]))
    notes += ex('2. Bài 2.2(b): bóng đèn', '<p>10 lớp, N = 167, x̄ = 1099.0 giờ, σ = 40: k = 1.96·40/√167 = 6.07 ⇒ [1092.9; 1105.1].</p>')
    notes += ex('3. Bài 2.14: tỷ lệ phế phẩm', '<p>16/400 = 0.04; k = 1.96√(0.04·0.96/400) = 0.0192 ⇒ [0.0208; 0.0592].</p>')
    notes += ex('4. Bài 2.9: ốc vít', '<p>n = 20, x̄ = 20.2, s² = 0.04, γ = 99%:</p>' + steps([m_('t_{0.005}(19)=2.861'), m_('k=\\dfrac{2.861\\cdot0.2}{\\sqrt{20}}=0.128'), m_('\\mu\\in[20.072;\\,20.328]')]))
    notes += ex('5. Kreyszig PS 25.3/7: phanh xe', '<p>126/800 = 0.1575; k = 1.96√(0.1575·0.8425/800) = 0.0252 ⇒ [0.132; 0.183].</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('cicalc') + sim('ciplay')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 “Student”', 'Phân phối t do W. S. Gosset công bố năm 1908 dưới bút danh “Student” khi làm ở nhà máy bia Guinness; khái niệm khoảng tin cậy do Jerzy Neyman đưa ra (1937).')
    notes += '<h2>5. Case study</h2><p>Thăm dò 1600 cử tri: [57.6%; 62.4%]. Biên sai số 2.4% là hàm của cỡ mẫu và độ tin cậy — các hãng thăm dò công bố cả hai con số.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Ghi rõ σ biết hay chưa để chọn U/t.<br>• Đề 2TC/2021 dùng t; đề HK2/2024 cho σ nên dùng U.<br>• Giữ ≥ 3 chữ số thập phân.')
    return dict(id='m08', slug='m08-khoang-tin-cay', title='Ước lượng khoảng cho kỳ vọng và cho tỷ lệ', subtitle='Khoảng tin cậy σ biết (U), σ chưa biết (Student), tỷ lệ p, cỡ mẫu, mở rộng σ²',
                source='Lecture Notes §2.3, Bài 2.2b, 2.5–2.16 · Kreyszig §25.3 (PS 25.3) · Câu 2 các đề cuối kỳ · Giữa kỳ mẫu 9(b),(c)', exam='Câu 2 MỌI đề cuối kỳ; câu 9 giữa kỳ mẫu; câu 4 giữa kỳ HK2', time='≈ 5 giờ',
                objectives=['Chọn đúng khoảng tin cậy theo tham số và σ', 'Tính khoảng từ dữ liệu theo lớp', 'Tìm cỡ mẫu tối thiểu', 'Diễn giải đúng độ tin cậy'], parts=parts, notes=notes, sims=['cicalc', 'ciplay'])
