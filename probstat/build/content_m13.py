from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Chương cuối: quan sát <b>đồng thời hai đại lượng</b> (x, y). <b>Hồi quy</b> xây hàm dự báo y từ x; <b>tương quan</b> đo mức độ phụ thuộc tuyến tính giữa hai đại lượng. Đây là câu 4 của mọi đề cuối kỳ (hồi quy hoặc hệ số tương quan mẫu).</p>' + ul(['Đường hồi quy mẫu y = k₀ + k₁x (bình phương tối thiểu)', 'Hiệp phương sai mẫu s_xy và hệ số tương quan mẫu r', 'Dự báo ŷ tại x₀; ý nghĩa của r và r²', 'Mở rộng: kiểm định ρ = 0 và khoảng tin cậy cho hệ số góc']), 'MODULE 13 · Bài học 5 · Chương 4, mục 4.1–4.2 · Kreyszig §25.9', 'Tương quan và hồi quy tuyến tính đơn', explain='Hồi quy trả lời “nếu x = 11 thì y khoảng bao nhiêu?”. Tương quan trả lời “x và y đi cùng nhau chặt đến đâu?”.'))
    s.append(sl(sim('regress'), 'PHẦN 1 · Nền tảng', 'Thực hành: nhập dữ liệu, xem đường hồi quy và r'))
    parts.append(dict(title='Nền tảng', bullets=['Hồi quy và tương quan', 'Widget hồi quy'], slides=s))
    s = []
    s.append(sl(formula('Đường hồi quy mẫu', 'k_1=\\dfrac{s_{xy}}{s_x^2}=\\dfrac{n(\\overline{xy}-\\bar x\\bar y)}{(n-1)s_x^2},\\quad k_0=\\bar y-k_1\\bar x,\\quad y=k_0+k_1x', [('s_{xy}', 'hiệp phương sai mẫu = (1/(n−1))Σ(xᵢ−x̄)(yᵢ−ȳ)'), ('k_1', 'hệ số hồi quy (hệ số xác định)')]) + '<p>Nguyên lý bình phương tối thiểu: chọn k₀, k₁ làm nhỏ nhất q = Σ(yᵢ − k₀ − k₁xᵢ)². Đường hồi quy luôn đi qua (x̄, ȳ).</p>', 'PHẦN 2 · Phương pháp', 'Đường hồi quy tuyến tính mẫu'))
    s.append(sl(formula('Hệ số tương quan mẫu', 'r=\\dfrac{s_{xy}}{s_xs_y},\\quad -1\\le r\\le1,\\quad r=\\pm1\\iff\\text{mọi điểm cùng nằm trên một đường thẳng}') + '<p>r &gt; 0: thuận; r &lt; 0: nghịch; |r| gần 1: mạnh; r ≈ 0: không có quan hệ TUYẾN TÍNH. Mối liên hệ: k₁ = r·s_y/s_x; r² là phần phương sai của y được x giải thích.</p>', 'PHẦN 2 · Phương pháp', 'Hệ số tương quan mẫu'))
    s.append(sl(callout('good', 'Quy trình đề thi', '1) Lập bảng x, y, x², xy (hoặc dùng x̄, ȳ). 2) x̄, ȳ, x², xy trung bình. 3) k₁ = (xy̅ − x̄ȳ)/(x̅² − x̄²) (giống s_xy/s_x²). 4) k₀ = ȳ − k₁x̄. 5) Thay x₀ để dự báo; hoặc r = s_xy/(s_xs_y).'), 'PHẦN 2 · Phương pháp', 'Cách làm bài trong đề'))
    parts.append(dict(title='Phương pháp', bullets=['Hồi quy', 'Tương quan', 'Quy trình đề thi'], slides=s))
    s = []
    s.append(sl(callout('info', 'Đề HK2 đề 1 câu 4', 'X = 1.55, 6.55, 11.55, 16.55, 21.55; Y = 13.03, 17.08, 21.03, 25.10, 29.08; dự báo tại X = 11.') + steps(['x̄ = 11.55; ȳ = 21.064.', 'k₁ = 0.8024 (đáp án chính thức 0.802).', 'k₀ = 11.836 ⇒ y = 11.836 + 0.8024x; y(11) = 20.663.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: đề cuối kỳ HK2'))
    s.append(sl(callout('info', 'Ví dụ 4.1 (Lecture Notes)', 'Giảm thể tích da: (4000; 2.3), (6000; 4.1), (8000; 5.7), (10000; 6.9).') + steps(['x̄ = 7000, ȳ = 4.75; s_x² = 2·10⁷/3; s_xy = 15400/3.', 'k₁ = 0.00077; y = 0.00077x − 0.64; y(7000) = 4.75.', 'r = 0.996.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 2: da bị nén'))
    s.append(sl(callout('info', 'Đề mẫu 2024 câu 4', 'X = 1.85, 7.93, 12.55, 18.21, 23.45; Y = 23.03, 27.08, 31.03, 38.12, 30.28: tính r.') + '<p>r = 0.728 (tương quan thuận khá mạnh); điểm (23.45; 30.28) kéo r xuống. Với bộ 3 và 4 của đề, r thay đổi mạnh.</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 3: hệ số tương quan'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Đề HK2', 'Ví dụ 4.1', 'Đề 2024'], slides=s))
    s = []
    s.append(sl(ul(['<b>Nhầm hồi quy y theo x với x theo y</b>: hai đường khác nhau.', '<b>r bằng k₁</b>: sai; k₁ = r·s_y/s_x.', '<b>Tương quan ≠ nhân quả.</b>', '<b>Ngoại suy</b> xa khỏi miền dữ liệu.', '<b>Một điểm ngoại lai</b> làm thay đổi mạnh r và k₁ (Ohm: y = 0 tại x = 80).']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    s.append(sl(callout('info', 'Mở rộng (Kreyszig §25.9)', 'Kiểm định H₀: ρ = 0: t = r√(n − 2)/√(1 − r²) ~ t(n − 2). Ví dụ: r = 0.6, n = 10 ⇒ t = 2.12 > 1.86 ⇒ bác bỏ. Khoảng tin cậy cho hệ số góc: k₁ ± t_{α/2}(n − 2)·s/√Σ(x − x̄)² với s² = Σ(y − ŷ)²/(n − 2).'), 'PHẦN 4 · Bẫy và mở rộng', 'Kiểm định ρ và khoảng tin cậy cho k₁'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy', 'Kiểm định ρ'], slides=s))
    s = []
    s.append(sl('<p><b>Định luật Hooke</b> (Kreyszig PS 25.9/8): lực x = 2, 4, 6, 8; độ giãn y = 4.1, 7.8, 12.3, 15.8 ⇒ k₁ = 1.98 (độ giãn/lực) ⇒ hằng số lò xo = 1/k₁ ≈ 0.505. Hồi quy biến dữ liệu đo thành hằng số vật lý, cùng cách mô hình hóa ở định luật Ohm và quãng đường phanh.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: hằng số lò xo'))
    s.append(sl(ul(['k₁ = s_xy/s_x²; k₀ = ȳ − k₁x̄; r = s_xy/(s_xs_y).', 'Đường hồi quy đi qua (x̄, ȳ).', 'r² = phần phương sai giải thích; tương quan ≠ nhân quả.']) + callout('good', 'Hoàn thành', 'Hết 13 module. Vào Luyện đề để làm đề tổng hợp tính giờ.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Hằng số lò xo', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §4.1 (hồi quy tuyến tính đơn, bình phương tối thiểu, hệ phương trình chuẩn (4.3), k₁ = s_xy/s_x²) và §4.2 (hiệp phương sai, hệ số tương quan mẫu và lý thuyết, Định lý 4.1–4.2, Ví dụ 4.1, Bài 4.1–4.10). Kreyszig §25.9 và PS 25.9 (Prob. 1–10, khoảng tin cậy 12–15; Example 4 kiểm định ρ).</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Bài 4.5: biến dạng thép và độ cứng Brinell', '<p>x = 6, 9, 11, 13, 22, 26, 28, 33, 35; y = 68, 67, 65, 53, 44, 40, 37, 34, 32: k₁ = −1.3196 (nghịch), k₀ = 75.72, r = −0.9773; dự báo y(20) ≈ 49.3.</p>')
    notes += ex('2. Bài 4.9: quãng đường dừng', '<p>v = 30, 40, 50, 60 mph; s = 160, 240, 330, 435 ft: k₁ = 9.15, k₀ = −120.5, r = 0.998; y(35) ≈ 199.75 ft.</p>')
    notes += ex('3. Bài 4.6: độ cứng và sức căng', '<p>x = 200, 300, 400, 500; y = 110, 150, 190, 280: k₁ = 0.55, k₀ = −10, r = 0.976.</p>')
    notes += ex('4. Đề 2TC đề 2 câu 4', '<p>X = 1.5, 6.5, 11.5, 16.5, 21.5; Y = 13.03, 17.08, 21.03, 25.10, 29.08: k₁ = 0.8024; y(11) = 20.66.</p>')
    notes += ex('5. Đề 2021–2022 câu 4 (a = 9)', '<p>X = 1.5, 2.5, 3.5, 4.5, 14; Y = 8.31, 12.29, 16.32, 20.28, 58.3: k₁ = 4 (đáp án chính thức), k₀ = 2.3; y(3) = 14.3.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('regress')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Galton, Pearson, Gauss', 'Hồi quy do Francis Galton đặt tên (1886) khi nghiên cứu chiều cao cha con; hệ số tương quan do Karl Pearson (1896); phương pháp bình phương tối thiểu do Legendre (1805) và Gauss.')
    notes += '<h2>5. Case study</h2><p>Quãng đường phanh theo tốc độ: hồi quy dự báo 35 mph ⇒ ≈ 200 ft; nhưng quan hệ thực là bậc hai nên ngoại suy xa là rủi ro.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Giữ ≥ 4 chữ số ở trung gian.<br>• Ghi rõ y theo x.<br>• Dự báo chỉ tin cậy trong miền dữ liệu.')
    return dict(id='m13', slug='m13-tuong-quan-hoi-quy', title='Hệ số tương quan và hồi quy tuyến tính đơn', subtitle='Bình phương tối thiểu, k₀, k₁, hiệp phương sai, hệ số tương quan mẫu, dự báo',
                source='Lecture Notes §4.1–4.2, Bài 4.1–4.10 · Kreyszig §25.9 (PS 25.9) · Câu 4 mọi đề cuối kỳ', exam='Câu 4 MỌI đề cuối kỳ (hồi quy hoặc hệ số tương quan mẫu)', time='≈ 4 giờ',
                objectives=['Tính k₀, k₁ của đường hồi quy mẫu', 'Tính hệ số tương quan mẫu và hiểu r, r²', 'Dự báo y tại x₀', 'Phân biệt tương quan với nhân quả và nhận biết ngoại lai'], parts=parts, notes=notes, sims=['regress'])
