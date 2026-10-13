from hx import *
def m_(t): return f'\\({t}\\)'
def module():
    parts = []
    s = []
    s.append(sl('<p>Ba chủ đề “tùy chọn” của đề cương: <b>biểu đồ kiểm soát</b> (kiểm định liên tục trong sản xuất), <b>kiểm định χ² mức độ phù hợp</b> (dữ liệu có đúng một mô hình phân phối không) và <b>kiểm định phi tham số</b> (kiểm định dấu). Giáo trình tiếng Việt chỉ ghi quy trình §3.6; nội dung chi tiết lấy từ Kreyszig §25.5, §25.7, §25.8.</p>' + ul(['Biểu đồ kiểm soát μ và p: LCL, UCL = ± 3σ/√n', 'χ₀² = Σ(b − e)²/e, bậc tự do K − r − 1', 'Kiểm định dấu: X ~ B(n, 1/2)']), 'MODULE 12 · Bài học 4 · Chương 3, mục 3.5–3.7 · Kreyszig §25.5, §25.7, §25.8', 'Kiểm soát chất lượng, χ² phù hợp, phi tham số', explain='Biểu đồ kiểm soát là “kiểm định mỗi giờ”. χ² phù hợp hỏi “mô hình này có khớp dữ liệu không”. Kiểm định dấu chỉ cần đếm dấu cộng/trừ.'))
    s.append(sl(sim('control'), 'PHẦN 1 · Nền tảng', 'Thực hành: biểu đồ kiểm soát trung bình'))
    parts.append(dict(title='Nền tảng', bullets=['Ba chủ đề', 'Biểu đồ kiểm soát'], slides=s))
    s = []
    s.append(sl(formula('Biểu đồ kiểm soát', '\\text{LCL}=\\mu_0-\\dfrac{3\\sigma}{\\sqrt n},\\ \\text{UCL}=\\mu_0+\\dfrac{3\\sigma}{\\sqrt n};\\quad \\text{biểu đồ p: }p\\pm3\\sqrt{\\dfrac{p(1-p)}n}') + '<p>Máy rót μ = 1 gal, σ = 0.02, n = 4: [0.97; 1.03], mức ý nghĩa ≈ 0.3% (Kreyszig PS 25.5/1–2). Biểu đồ p: p = 4%, n = 100 ⇒ UCL = 9.88%, LCL = 0.</p>', 'PHẦN 2 · Phương pháp', 'Biểu đồ kiểm soát μ và p'))
    s.append(sl(formula('Kiểm định χ² phù hợp', '\\chi_0^2=\\sum_{j=1}^K\\dfrac{(b_j-e_j)^2}{e_j},\\quad e_j=np_j,\\quad \\text{bậc tự do }K-r-1') + '<p>Bước: chia K lớp (mỗi lớp ≥ 5 quan sát), tính p_j theo F, e_j, χ₀², tra χ²_α(K − r − 1). Nếu χ₀² > c bác bỏ H₀: F phù hợp.</p>', 'PHẦN 2 · Phương pháp', 'Kiểm định mức độ phù hợp'))
    s.append(sl(sim('gof'), 'PHẦN 2 · Phương pháp', 'Thực hành: χ² phù hợp'))
    s.append(sl(callout('info', 'Kiểm định dấu', 'H₀: median = μ̃₀. Đếm số X giá trị lớn hơn μ̃₀ (bỏ hòa): X ~ B(n, 1/2). Với X ≥ k: p = P(B(n, 1/2) ≥ k). Ví dụ công tắc nhiệt (8 dưới, 1 trên): p = 10/512 = 0.0195 < 0.05 ⇒ bác bỏ: đặt quá thấp.'), 'PHẦN 2 · Phương pháp', 'Kiểm định dấu'))
    parts.append(dict(title='Phương pháp', bullets=['Biểu đồ kiểm soát', 'χ² phù hợp', 'Widget', 'Kiểm định dấu'], slides=s))
    s = []
    s.append(sl(callout('info', 'Kreyszig §25.7 Example 1', '100 giá trị độ bền (x̄ = 364.7, s = 26.7), 10 lớp: b_j = 6, 6, 11, 14, 16, 15, 8, 10, 8, 6; e_j chuẩn = 6.81, …, 6.55.') + steps(['χ₀² = 0.096 + 0.045 + 0.201 + 0.080 + 0.164 + 0.0004 + 1.602 + 0.033 + 0.417 + 0.046 = 2.684 (sách 2.688).', 'Bậc tự do 10 − 2 − 1 = 7; χ²₀.₀₅(7) = 14.067 ⇒ chấp nhận chuẩn.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: kiểm tra phân phối chuẩn'))
    s.append(sl(callout('info', 'Kreyszig PS 25.7/3', 'Tung 100 lần được 40 ngửa, 60 sấp.') + steps(['e = 50, 50; χ₀² = 2·(10²/50) = 4.', 'χ²₀.₀₅(1) = 3.841 ⇒ bác bỏ: đồng xu không công bằng.']) + '<p>Prob. 4 (4 ngửa, 6 sấp): χ₀² = 0.4 ⇒ chấp nhận — cùng tỉ lệ nhưng cỡ mẫu nhỏ cho kết luận khác.</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 2: đồng xu và cỡ mẫu'))
    s.append(sl(callout('info', 'Kreyszig PS 25.5/10: biểu đồ p', '15 mẫu cỡ 100 với số phế phẩm 1, 4, 5, 4, 9, 7, 0, 5, 6, 13, 0, 2, 1, 12, 8; p = 4%.') + steps(['UCL = 0.04 + 3·√(0.04·0.96/100) = 0.0988.', 'Mẫu 13% và 12% vượt UCL ⇒ quy trình mất kiểm soát.']), 'PHẦN 3 · Ví dụ', 'Ví dụ 3: biểu đồ tỷ lệ phế phẩm'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Chuẩn', 'Đồng xu', 'Biểu đồ p'], slides=s))
    s = []
    s.append(sl(ul(['<b>Quên giảm bậc tự do</b> khi ước lượng tham số (K − r − 1).', '<b>Lớp có tần số &lt; 5</b>: phải gộp lớp.', '<b>Biểu đồ kiểm soát</b>: dùng σ/√n, không phải σ.', '<b>Kiểm định dấu</b>: bỏ các cặp hòa trước khi đếm n.', '<b>Chấp nhận phù hợp</b> không chứng minh mô hình đúng, chỉ chưa bác bỏ.']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy'], slides=s))
    s = []
    s.append(sl('<p><b>Kiểm soát quy trình.</b> Mỗi giờ lấy 4 chiếc từ máy rót; điểm nào ngoài [0.97; 1.03] báo hiệu cần dừng máy và tìm nguyên nhân. Biểu đồ giảm chi phí phát hiện lỗi hơn kiểm tra toàn bộ lô.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: kiểm soát máy rót'))
    s.append(sl(ul(['LCL/UCL = μ ± 3σ/√n; p ± 3√(p(1 − p)/n).', 'χ₀² = Σ(b − e)²/e; K − r − 1 bậc tự do.', 'Dấu: X ~ B(n, 1/2).']) + callout('good', 'Tiếp theo', 'Module 13: tương quan và hồi quy.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Máy rót', 'Tổng kết'], slides=s))
    notes = '<h2>1. Nội dung chi tiết</h2><p>Đề cương mục 3.5 (biểu đồ kiểm định cho trung bình), 3.6 (χ² phù hợp) và 3.7 (phi tham số) là nội dung tự chọn; Lecture Notes chỉ ghi quy trình 5 bước của §3.6 (các mục 3.5, 3.7 để trống). Kreyszig §25.5 (Quality Control), §25.7 (Goodness of Fit), §25.8 (Nonparametric Tests) cung cấp lý thuyết và các Problem Set 25.5, 25.7, 25.8 làm câu gốc.</p><h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. PS 25.5/6: gioăng', '<p>μ = 5, σ = 1.16, n = 4: [3.26; 6.74]; 10 trung bình mẫu đều nằm trong ⇒ trong kiểm soát.</p>')
    notes += ex('2. PS 25.5/3', '<p>UCL − LCL = 6σ/√n = 0.02 với σ = 0.02 ⇒ n = 36.</p>')
    notes += ex('3. PS 25.7/5–6: súc sắc', '<p>60 lần: 10, 13, 9, 11, 9, 8 ⇒ χ₀² = 1.6; 180 lần: 33, 27, 29, 35, 25, 31 ⇒ 2.3; cả hai < 11.07 ⇒ cân đối.</p>')
    notes += ex('4. PS 25.7/8: mũi khoan', '<p>17/400 cùn, p₀ = 0.025: z = 7/3.122 = 2.24 > 1.645 ⇒ bác bỏ: tỉ lệ cùn lớn hơn 2.5%.</p>')
    notes += ex('5. PS 25.8/3: bộ lọc dầu', '<p>7 lần A sạch hơn, 1 lần B hơn (bỏ 3 hòa): p = 9/256 = 0.035 < 0.05 ⇒ bác bỏ: A tốt hơn B.</p>')
    notes += '<h2>3. Thực hành tương tác</h2>' + sim('control') + sim('gof')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Shewhart', 'Walter Shewhart (Bell Labs, 1924) phát minh biểu đồ kiểm soát; Pearson (1900) công bố kiểm định χ² phù hợp; kiểm định dấu là kiểm định phi tham số cổ điển (Arbuthnot, 1710).')
    notes += '<h2>5. Case study</h2><p>Kiểm soát chất lượng giữa dây chuyền: quy tắc 3σ làm báo động nhầm chỉ 0.27%.</p><h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Ghi rõ K, r, bậc tự do.<br>• Gộp lớp có e_j &lt; 5.<br>• Bỏ cặp hòa khi dùng kiểm định dấu.')
    return dict(id='m12', slug='m12-chat-luong-phu-hop-phi-tham-so', title='Biểu đồ kiểm soát, kiểm định χ² mức độ phù hợp và kiểm định phi tham số', subtitle='LCL/UCL (3σ), χ₀² = Σ(b − e)²/e, kiểm định dấu',
                source='Đề cương 3.5–3.7 · Lecture Notes §3.6 · Kreyszig §25.5, §25.7, §25.8 (PS 25.5, 25.7, 25.8)', exam='Nội dung tự chọn; không có trong các đề đã công bố', time='≈ 3 giờ',
                objectives=['Dựng giới hạn kiểm soát cho μ và p', 'Tính χ₀² và dùng bậc tự do K − r − 1', 'Làm kiểm định dấu bằng nhị thức B(n, 1/2)', 'Phân biệt kiểm định tham số và phi tham số'], parts=parts, notes=notes, sims=['control', 'gof'])
