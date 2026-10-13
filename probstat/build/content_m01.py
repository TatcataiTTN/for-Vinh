from hx import *
from pskit import *
from qb import f, fg
from orig_m01 import DATA, stem_leaf, nums_text

def ex_full(key, title, extra=''):
    name, x, unit, prob = DATA[key]
    n = len(x); m = mean(x); qL, qM, qU = quartiles(x); R = qU - qL; v = var_s(x); s = sd_s(x); ol = outliers(x)
    sx = sorted(x); lo, hi = qL - 1.5 * R, qU + 1.5 * R
    dd = max((len(str(t).split('.')[1]) if '.' in str(t) else 0) for t in x); D = max(dd + 2, 3)
    body = f'<p><b>Đề.</b> {name}. Dữ liệu (n = {n}): {nums_text(x)}. Tính x̄, qM, qL, qU, IQR, s², s; tìm ngoại lai.</p>'
    body += steps([
        f'Sắp xếp: {nums_text(sx)}.',
        f'Trung bình: {m_("\\bar x=\\dfrac{\\sum x_i}{n}=\\dfrac{" + fg(sum(x),4) + "}{" + str(n) + "}=" + f(m, D) + "")}.',
        f'Trung vị: n = {n} {"lẻ" if n % 2 else "chẵn"} ⇒ qM = {fg(qM, 4)}. Nửa dưới {nums_text(sx[:n//2])} ⇒ qL = {fg(qL, 4)}; nửa trên {nums_text(sx[(n+1)//2:])} ⇒ qU = {fg(qU, 4)}; IQR = {fg(R, 4)}.',
        f'Phương sai: Σ(xᵢ − x̄)² = {f((n-1)*v, D+1)} ⇒ {m_("s^2=\\dfrac{" + f((n-1)*v, D+1) + "}{" + str(n-1) + "}=" + f(v, D) + "")}; {m_("s=\\sqrt{s^2}=" + f(s, D))}.',
        f'Ngưỡng ngoại lai: [{fg(lo, 4)}; {fg(hi, 4)}] ⇒ ' + (f'ngoại lai: {nums_text(ol)}.' if ol else 'không có ngoại lai.'),
    ])
    body += '<pre>' + esc(stem_leaf(x)) + '</pre>' + extra
    return ex(title, body)

def m_(t): return f'\\({t}\\)'

def module():
    parts = []
    # ---------------- PHẦN 1 ----------------
    s = []
    s.append(sl('<p>Dữ liệu thô là một dãy số khó đọc. Ta cần <b>biểu diễn</b> (bảng thân–lá, histogram, boxplot) và <b>tóm tắt</b> (trung bình, trung vị, phương sai, độ lệch chuẩn, tứ phân vị) để thấy <b>trung tâm</b>, <b>độ phân tán</b>, <b>hình dạng</b> và <b>ngoại lai</b>.</p>'
                + ul(['Biểu diễn: stem-and-leaf, histogram, boxplot', 'Trung tâm: trung bình x̄, trung vị qM', 'Phân tán: s², s, IQR, độ rộng R', 'Ngoại lai và quy tắc 68–95–99.7'])
                , 'MODULE 1 · Bài học 1 · Chương 1, mục 1.1 · Kreyszig §24.1', 'Biểu diễn và tóm tắt dữ liệu',
                explain='Giống như xem điểm cả lớp: thay vì đọc 40 con điểm, ta nói “trung bình 6.8, đa số từ 6 đến 8, có một bạn 1 điểm là bất thường”.'))
    s.append(sl('<p>Ví dụ 1.1 của giáo trình: sức căng (kg/mm²) của 14 tấm thép, đã sắp xếp:</p><p class="mono" style="text-align:center">78, 81, 83, 84, 86, 87, 87, 89, 89, 89, 89, 90, 91, 99</p>'
                '<pre>Key: 7|8 = 78\nCAF  Stem | Leaf\n  1    7  | 8\n  4    8  | 1 3 4\n 11    8  | 6 7 7 9 9 9 9\n 13    9  | 0 1\n 14    9  | 9</pre>'
                '<p>Stem = chữ số hàng chục (chia hai nửa 0–4 và 5–9), Leaf = chữ số hàng đơn vị. <b>CAF</b> = tần suất tuyệt đối tích lũy (11 ở dòng thứ ba nghĩa là 11 giá trị đầu tiên).</p>',
                'PHẦN 1 · Nền tảng', 'Biểu đồ thân–lá (stem-and-leaf)',
                explain='Mỗi số được tách thành “thân” (phần đầu) và “lá” (chữ số cuối). Nhìn nghiêng đầu sang trái, các hàng chữ số chính là một histogram nhưng vẫn giữ nguyên từng giá trị.'))
    s.append(sl(formula('Tần suất lớp tương đối', 'f_{\\text{rel}}(x)=\\dfrac{\\text{số phần tử của lớp có điểm giữa }x}{\\text{tổng số phần tử } n}', [('x', 'điểm chính giữa của lớp'), ('n', 'cỡ mẫu')])
                + table(['Lớp', '74.5–79.5', '79.5–84.5', '84.5–89.5', '89.5–94.5', '94.5–99.5'], [['Điểm giữa', '77', '82', '87', '92', '97'], ['f_rel', '0.07', '0.21', '0.50', '0.14', '0.07']])
                + '<p>Tổng các f_rel luôn bằng 1. Histogram vẽ cột có chiều cao f_rel (bảng 1.1, hình 1.2 giáo trình).</p>',
                'PHẦN 1 · Nền tảng', 'Histogram: tần suất lớp tương đối',
                explain='Chia trục số thành các khoảng đều nhau (lớp), đếm số giá trị rơi vào mỗi lớp rồi chia cho n. Cột cao nhất cho biết dữ liệu tập trung nhiều nhất ở đâu.'))
    parts.append(dict(title='Nền tảng', bullets=['Vì sao cần biểu diễn dữ liệu', 'Thân–lá và CAF', 'Histogram và f_rel'], slides=s))

    # ---------------- PHẦN 2 ----------------
    s = []
    s.append(sl(formula('Trung bình, phương sai, độ lệch chuẩn mẫu', '\\bar x=\\dfrac1n\\sum_{i=1}^n x_i,\\quad s^2=\\dfrac1{n-1}\\sum_{i=1}^n (x_i-\\bar x)^2=\\dfrac{n}{n-1}\\left(\\overline{x^2}-\\bar x^{\\,2}\\right),\\quad s=\\sqrt{s^2}',
                        [('\\overline{x^2}', 'trung bình của các bình phương, \\(\\frac1n\\sum x_i^2\\)'), ('s', 'có cùng đơn vị với dữ liệu; s² có đơn vị bình phương')])
                + callout('warn', 'Mẫu số là n − 1', 'Phương sai MẪU chia cho n − 1 (không phải n). Đề thi Phenikaa luôn dùng công thức chia n − 1.'),
                'PHẦN 2 · Phương pháp', 'Trung bình và phương sai mẫu',
                explain='x̄ là “điểm cân bằng” của dữ liệu. s² đo độ lệch bình phương trung bình quanh x̄; chia n−1 để s² là ước lượng không chệch cho phương sai tổng thể (sẽ chứng minh ở Module 7).'))
    s.append(sl(formula('Tứ phân vị, IQR và ngoại lai', 'q_M=\\text{trung vị},\\; q_L,q_U=\\text{trung vị nửa dưới / nửa trên},\\; \\mathrm{IQR}=q_U-q_L',
                        [('q_L', 'trung vị của các phần tử nằm dưới q_M (bỏ q_M nếu n lẻ)'), ('q_U', 'trung vị của các phần tử nằm trên q_M')])
                + callout('info', 'Ngoại lai (outlier)', 'x là ngoại lai nếu x &lt; q_L − 1.5·IQR hoặc x &gt; q_U + 1.5·IQR (khoảng cách tới biên hộp gần nhất lớn hơn 1.5·IQR).')
                + '<p>Với n = 14 ở ví dụ thép: q_L = x₄ = 84, q_M = (87+89)/2 = 88, q_U = x₁₁ = 89, IQR = 5, và q_U + 1.5·IQR = 96.5 &lt; 99 ⇒ 99 là ngoại lai.</p>',
                'PHẦN 2 · Phương pháp', 'Boxplot và tiêu chuẩn ngoại lai',
                explain='Hộp chứa 50% dữ liệu ở giữa. “Râu” kéo ra nhưng không quá 1.5 lần chiều dài hộp; điểm nào xa hơn thì vẽ riêng bằng một chấm và gọi là ngoại lai.'))
    s.append(sl('<svg viewBox="0 0 640 250" style="max-width:100%;width:640px"><path d="M20 200 C120 198,190 34,320 28 C450 34,520 198,620 200 Z" fill="var(--infobg)" stroke="var(--accent2)" stroke-width="2"/>'
                '<g stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="4 3"><line x1="320" y1="28" x2="320" y2="205"/><line x1="236" y1="70" x2="236" y2="205"/><line x1="404" y1="70" x2="404" y2="205"/><line x1="152" y1="150" x2="152" y2="205"/><line x1="488" y1="150" x2="488" y2="205"/><line x1="68" y1="190" x2="68" y2="205"/><line x1="572" y1="190" x2="572" y2="205"/></g>'
                '<g stroke="var(--text)" stroke-width="2"><line x1="236" y1="100" x2="404" y2="100"/><line x1="152" y1="128" x2="488" y2="128"/><line x1="68" y1="156" x2="572" y2="156"/></g>'
                '<g font-size="13" fill="var(--text)" text-anchor="middle" paint-order="stroke" stroke="var(--infobg)" stroke-width="4"><text x="320" y="95" font-weight="bold">68% trong (x̄ ± s)</text><text x="320" y="123" font-weight="bold">95% trong (x̄ ± 2s)</text><text x="320" y="151" font-weight="bold">99.7% trong (x̄ ± 3s)</text></g>'
                '<g font-size="12" fill="var(--text)" text-anchor="middle"><text x="320" y="223">x̄</text><text x="236" y="223">x̄−s</text><text x="404" y="223">x̄+s</text><text x="152" y="223">x̄−2s</text><text x="488" y="223">x̄+2s</text><text x="68" y="223">x̄−3s</text><text x="572" y="223">x̄+3s</text></g></svg>'
                + '<p><b>Quy tắc kinh nghiệm</b> (dữ liệu hình quả chuông): khoảng (x̄−s, x̄+s) chứa ≈ 68%, (x̄−2s, x̄+2s) ≈ 95%, (x̄−3s, x̄+3s) ≈ 99.7% dữ liệu.</p>',
                'PHẦN 2 · Phương pháp', 'Quy tắc 68–95–99.7',
                explain='Nếu điểm thi của lớp hình chuông với x̄ = 7, s = 1 thì khoảng 68% bạn nằm trong 6–8 điểm và 95% nằm trong 5–9 điểm.'))
    s.append(sl(sim('descr'), 'PHẦN 2 · Phương pháp', 'Thực hành: nhập dữ liệu, xem mọi đặc trưng và biểu đồ'))
    parts.append(dict(title='Phương pháp', bullets=['Công thức x̄, s², s', 'Tứ phân vị, IQR, ngoại lai', 'Quy tắc 68–95–99.7', 'Thực hành tương tác'], slides=s))

    # ---------------- PHẦN 3 ----------------
    s = []
    nm, x, un, pr = DATA['LN2']; n = len(x); m = mean(x); v = var_s(x)
    s.append(sl(callout('info', 'Ví dụ giáo trình 1.1', 'Sức căng 14 tấm thép (kg/mm²): 89 84 87 81 89 86 91 90 78 89 87 99 83 89.')
                + steps([f'Σx = {sum(x)} ⇒ {m_("\\bar x=\\frac{" + str(sum(x)) + "}{14}=\\frac{611}{7}\\approx " + f(m, 2))}.',
                         f'{m_("s^2=\\frac{1}{13}\\sum (x_i-\\bar x)^2=\\frac{176}{7}\\approx " + f(v, 2))}, {m_("s\\approx " + f(sd_s(x), 3))} (kg/mm²).',
                         'q_L = 84, q_M = 88, q_U = 89, IQR = 5, R = 99 − 78 = 21.', 'q_U + 1.5·IQR = 96.5 &lt; 99 ⇒ x₁₄ = 99 là ngoại lai.']),
                'PHẦN 3 · Ví dụ', 'Ví dụ 1: sức căng tấm thép (Lecture Notes 1.1)'))
    nm, x, un, pr = DATA['K3']
    s.append(sl(callout('info', 'Kreyszig PS 24.1, Prob. 3 và 13 / Lecture Notes Bài 1.1(b)', 'Huyết áp tâm thu 15 bệnh nhân nữ 20–22 tuổi.')
                + f'<p class="mono">{nums_text(x)}</p>' + steps([f'x̄ = {f(mean(x),3)}; qM = {fg(median(x),4)} ⇒ so sánh: x̄ {"&gt;" if mean(x) > median(x) else "&lt;"} qM.',
                         f's = {f(sd_s(x),3)}; IQR = {fg(iqr(x),4)} (quartiles: {fg(quartiles(x)[0],4)}, {fg(quartiles(x)[2],4)}).', f'Ngoại lai: {nums_text(outliers(x)) if outliers(x) else "không có"}.']),
                'PHẦN 3 · Ví dụ', 'Ví dụ 2: huyết áp 15 bệnh nhân'))
    nm, x, un, pr = DATA['K8']; o = outliers(x); xr = [t for t in x if t not in o]
    s.append(sl(callout('info', 'Kreyszig PS 24.1, Prob. 8 và 18', 'Độ cứng Brinell của 20 tấm đồng (kg/mm²). Ngoại lai chi phối độ lệch chuẩn.')
                + f'<p class="mono">{nums_text(x)}</p>' + steps([f'Với toàn bộ: x̄ = {f(mean(x),3)}, s = {f(sd_s(x),3)}, qM = {fg(median(x),4)}, IQR = {fg(iqr(x),4)}.', f'Ngoại lai: {nums_text(o)}. Bỏ ngoại lai (n = {len(xr)}): x̄ = {f(mean(xr),3)}, s = {f(sd_s(xr),3)}.',
                         f'Chỉ một giá trị bất thường làm s tăng từ {f(sd_s(xr),3)} lên {f(sd_s(x),3)}, trong khi trung vị gần như không đổi ({fg(median(xr),4)} so với {fg(median(x),4)}).']),
                'PHẦN 3 · Ví dụ', 'Ví dụ 3: độ cứng Brinell và ảnh hưởng của ngoại lai'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Sức căng thép', 'Huyết áp', 'Độ cứng Brinell'], slides=s))

    # ---------------- PHẦN 4 ----------------
    s = []
    s.append(sl(ul(['<b>Chia n thay vì n − 1</b> khi tính s² mẫu (đề thi Phenikaa dùng n − 1).',
                    '<b>Tứ phân vị khi n lẻ:</b> bỏ qM rồi lấy trung vị nửa dưới/nửa trên (cách của giáo trình/Kreyszig; phần mềm khác có thể cho kết quả khác).',
                    '<b>Quên căn bậc hai:</b> s² và s khác nhau; s mới cùng đơn vị với dữ liệu.',
                    '<b>Nhầm ngưỡng ngoại lai:</b> so với qL − 1.5·IQR và qU + 1.5·IQR, không phải x̄ ± 1.5s.',
                    '<b>Dữ liệu theo lớp:</b> dùng điểm giữa lớp và nhân với tần số khi tính x̄, s².']), 'PHẦN 4 · Bẫy và mở rộng', 'Năm bẫy thường gặp'))
    s.append(sl(formula('Đổi biến tuyến tính', 'y_i=a x_i+b\\;\\Rightarrow\\;\\bar y=a\\bar x+b,\\quad s_y=|a|\\,s_x,\\quad s_y^2=a^2 s_x^2', [('b', 'hằng số cộng: không làm đổi độ phân tán'), ('a', 'hệ số nhân: nhân độ lệch chuẩn với |a|')])
                + '<p>Ví dụ: x̄ = 20, s = 4 và y = 3x − 5 ⇒ ȳ = 55, s_y = 12.</p>', 'PHẦN 4 · Bẫy và mở rộng', 'Mở rộng: đổi đơn vị'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Năm bẫy', 'Đổi biến tuyến tính'], slides=s))

    # ---------------- PHẦN 5 ----------------
    s = []
    nm, x, un, pr = DATA['K5']
    s.append(sl('<p>Máy rót tự động đóng gói túi 200 g. Kreyszig 24.1/5 cho khối lượng 7 túi: ' + nums_text(x) + f'. x̄ = {f(mean(x),3)} g, s = {f(sd_s(x),3)} g. Nếu quy cách yêu cầu mỗi túi tối thiểu 199 g thì ngay mẫu này đã có một túi 198 g dưới chuẩn: thống kê mô tả là bước kiểm soát chất lượng đầu tiên, trước khi dùng ước lượng và kiểm định (Chương 2–3).</p>',
                'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: kiểm tra khối lượng túi'))
    s.append(sl(ul(['Biểu diễn: thân–lá, histogram (f_rel), boxplot.', 'Đặc trưng: x̄, qM, s², s, IQR, R.', 'Ngoại lai: ngoài [qL − 1.5·IQR, qU + 1.5·IQR].', 'Quy tắc 68–95–99.7 cho dữ liệu hình chuông.']) + callout('good', 'Tiếp theo', 'Module 2: phép thử, không gian mẫu, sự kiện và quy tắc đếm.'),
                'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Case study', 'Tổng kết'], slides=s))

    # ---------------- NỘI DUNG CHI TIẾT ----------------
    notes = '<h2>1. Nội dung chi tiết</h2><p>Giáo trình (Lecture Notes 08/2021, §1.1.1–1.1.2) trình bày hai cách biểu diễn điển hình qua ví dụ 1.1: thân–lá và histogram, sau đó là boxplot cùng các khái niệm trung vị, IQR và ngoại lai. §1.1.2 định nghĩa trung bình, phương sai, độ lệch chuẩn mẫu, công thức tính nhanh (1.5) và quy tắc kinh nghiệm. Kreyszig §24.1 cho cùng nội dung; <b>Problem Set 24.1</b> gồm 10 bộ dữ liệu cần biểu diễn (1–10), tính x̄, s, qM, IQR (11–16) và bốn bài về ngoại lai/trung bình (17–20).</p>'
    notes += '<h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex_full('K1', '1. Kreyszig 24.1/1 và 11: độ dài đinh')
    notes += ex_full('K2', '2. Kreyszig 24.1/2 và 12: số cuộc gọi mỗi phút')
    notes += ex_full('K4', '3. Kreyszig 24.1/4 và 14: hàm lượng sắt Fe₂O₃')
    notes += ex_full('K7', '4. Kreyszig 24.1/7 và 15, Lecture Notes Bài 1.1(c): thời gian nhả rơ-le')
    mids = [7, 9, 11, 13]; cnt = [4, 8, 9, 5]; N = sum(cnt); xb = sum(a * b for a, b in zip(mids, cnt)) / N; s2 = sum(b * (a - xb) ** 2 for a, b in zip(mids, cnt)) / (N - 1)
    notes += ex('5. Đề giữa kỳ mẫu, câu 9(a): dữ liệu theo lớp', '<p>Thời gian điều trị X (ngày): 6–8, 8–10, 10–12, 12–14 với số bệnh nhân 4, 8, 9, 5. Tính x̄ và s².</p>' + steps([
        'Điểm giữa lớp: 7, 9, 11, 13; N = 26.', f'Σnᵢxᵢ = 28 + 72 + 99 + 65 = 264 ⇒ x̄ = 264/26 = {f(xb, 4)}.',
        f'Σnᵢ(xᵢ − x̄)² = {f(sum(b*(a-xb)**2 for a,b in zip(mids,cnt)),4)}; chia N − 1 = 25 ⇒ s² = {f(s2,4)}, s = {f(math.sqrt(s2),4)}.']))
    notes += '<h2>3. Thực hành tương tác</h2><p>Nhập một bộ số bất kỳ (hoặc chọn bộ mẫu từ Kreyszig/giáo trình) để xem x̄, qM, qL, qU, IQR, s², s, ngoại lai, histogram, boxplot và thân–lá.</p>' + sim('descr')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Nguồn gốc các biểu đồ', 'Biểu đồ thân–lá và boxplot do John W. Tukey đề xuất trong sách <i>Exploratory Data Analysis</i> (1977), nhấn mạnh việc “nhìn dữ liệu” trước khi mô hình hoá. Quy tắc loại ngoại lai bằng 1.5·IQR cũng xuất phát từ Tukey. Độ lệch chuẩn được Karl Pearson đặt tên năm 1894; việc chia n − 1 (hiệu chỉnh Bessel) làm s² không chệch.')
    notes += '<h2>5. Case study</h2><p>Một xưởng đóng gói đo khối lượng 7 túi liên tiếp (Kreyszig 24.1/5): 203, 199, 198, 201, 200, 201, 201 g. x̄ = 200.43 g; qM = 201; IQR = ' + fg(iqr(DATA['K5'][1]), 4) + '. Kết luận ban đầu: máy rót hơi dao động quanh 200 g, có một túi thấp 198 g. Bước tiếp theo (Module 8 và 10) là dựng khoảng tin cậy và kiểm định xem trung bình có đúng 200 g hay không.</p>'
    notes += '<h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Đề Phenikaa yêu cầu tính chính xác ít nhất 3 chữ số thập phân.<br>• Với bảng tần số, ghi rõ điểm giữa lớp và tổng N.<br>• Khi n lẻ, loại qM khỏi cả hai nửa trước khi lấy qL, qU.<br>• Luôn nêu đơn vị (s có cùng đơn vị với dữ liệu).')
    return dict(id='m01', slug='m01-bieu-dien-du-lieu', title='Biểu diễn dữ liệu, trung bình, phương sai, tứ phân vị',
                subtitle='Thân–lá, histogram, boxplot, x̄, s², s, IQR, ngoại lai và quy tắc 68–95–99.7',
                source='Lecture Notes §1.1 · Kreyszig §24.1 (PS 24.1) · Đề cương mục 1.1', exam='Đề giữa kỳ mẫu câu 9(a); câu chuẩn bị cho Câu 2–3 mọi đề cuối kỳ', time='≈ 2 giờ',
                objectives=['Biểu diễn dữ liệu bằng thân–lá, histogram, boxplot', 'Tính x̄, qM, qL, qU, IQR, s², s đúng quy ước giáo trình', 'Nhận biết ngoại lai bằng 1.5·IQR và hiểu ảnh hưởng của chúng', 'Tính x̄, s² cho dữ liệu theo lớp (bảng tần số)'],
                parts=parts, notes=notes, sims=['descr'])
