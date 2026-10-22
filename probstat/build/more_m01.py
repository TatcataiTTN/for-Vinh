"""Module 1 — phần chuyên sâu: số liệu trong các ví dụ đều được TÍNH bằng pskit lúc dựng trang."""
import math
from hx import *
from pskit import *
from qb import fg, f
K = 'MODULE 1 · '
def L(x): return ', '.join(fg(v, 3) for v in x)
def parts():
    P = []
    # ───────── A. Loại dữ liệu và bảng tần số ─────────
    s = []
    s.append(sl(table(['Loại dữ liệu', 'Thang đo', 'Ví dụ', 'Tóm tắt phù hợp'],
                      [['Định tính', 'danh nghĩa', 'nhóm máu, ngành học', 'tần số, mốt, biểu đồ cột/tròn'], ['Định tính', 'thứ bậc', 'xếp loại giỏi/khá/TB', 'tần số, trung vị, mốt'],
                       ['Định lượng rời rạc', 'tỉ lệ', 'số lỗi, số khách', 'trung bình, s, boxplot, biểu đồ thân–lá'], ['Định lượng liên tục', 'khoảng/tỉ lệ', 'chiều cao, thời gian, điện áp', 'histogram, trung bình, s, tứ phân vị']])
                + callout('info', 'Vì sao quan trọng?', 'Không tính trung bình cho dữ liệu danh nghĩa (nhóm máu); chỉ định lượng mới có x̄, s và phép trừ có ý nghĩa.'),
                K + 'PHẦN 1 · Chuyên sâu', 'Phân loại dữ liệu và chọn cách tóm tắt', explain='Hỏi trước: dữ liệu này đếm hay đo? có thứ tự không? Câu trả lời quyết định biểu đồ và thống kê dùng được.'))
    x1 = [52, 61, 58, 70, 66, 74, 49, 63, 68, 71, 55, 60, 77, 64, 59, 82, 67, 62, 73, 57]
    n = len(x1); k = 5; w = 10; lo = 45
    bins = [(lo + i * w, lo + (i + 1) * w) for i in range(k)]
    cnt = [sum(1 for v in x1 if a <= v < b) for a, b in bins]
    rel = [c / n for c in cnt]; cum = [sum(rel[:i + 1]) for i in range(k)]
    s.append(sl(callout('info', 'Ví dụ A1 · Điểm 20 sinh viên', 'Dữ liệu: ' + L(x1) + '. Lập bảng tần số với 5 lớp độ rộng 10, bắt đầu từ 45.')
                + steps(['Khoảng biến thiên R = ' + fg(max(x1)) + ' − ' + fg(min(x1)) + ' = ' + fg(max(x1) - min(x1)) + '; số lớp k ≈ 1 + 3.3·log₁₀20 ≈ 5 (quy tắc Sturges).', 'Độ rộng lớp w ≈ R/k = ' + f((max(x1) - min(x1)) / k, 1) + ' ⇒ chọn w = 10 cho số tròn.', 'Quy ước lớp [a, b): giá trị bằng đầu mút phải thuộc lớp kế tiếp.'])
                + table(['Lớp', 'Tần số', 'Tần suất tương đối', 'Tích lũy'], [[f'[{a}, {b})', str(c), f(r, 2), f(cu, 2)] for (a, b), c, r, cu in zip(bins, cnt, rel, cum)]) + f'<p>Tổng tần số = {sum(cnt)} = n ✓; tổng tần suất = 1.</p>',
                K + 'PHẦN 1 · Chuyên sâu', 'Lập bảng tần số từng bước'))
    mids = [(a + b) / 2 for a, b in bins]
    xb_g = sum(c * m_ for c, m_ in zip(cnt, mids)) / n
    s2_g = sum(c * (m_ - xb_g) ** 2 for c, m_ in zip(cnt, mids)) / (n - 1)
    s.append(sl(callout('info', 'Ví dụ A2 · Trung bình và s² từ bảng tần số', 'Dùng bảng của Ví dụ A1 với điểm giữa lớp mᵢ, so với giá trị tính từ dữ liệu thô.')
                + table(['Lớp', 'mᵢ', 'nᵢ', 'nᵢmᵢ', 'nᵢ(mᵢ − x̄)²'], [[f'[{a}, {b})', fg(m_), str(c), fg(c * m_), f(c * (m_ - xb_g) ** 2, 2)] for (a, b), m_, c in zip(bins, mids, cnt)])
                + steps(['x̄ ≈ Σnᵢmᵢ/n = ' + fg(sum(c * m_ for c, m_ in zip(cnt, mids))) + '/' + str(n) + ' = ' + f(xb_g, 2), 's² ≈ Σnᵢ(mᵢ − x̄)²/(n − 1) = ' + f(s2_g * (n - 1), 2) + '/' + str(n - 1) + ' = ' + f(s2_g, 2) + ', s ≈ ' + f(math.sqrt(s2_g), 2),
                         'Dữ liệu thô: x̄ = ' + f(mean(x1), 2) + ', s = ' + f(sd_s(x1), 2) + ' — bảng gom lớp chỉ cho xấp xỉ.']), K + 'PHẦN 1 · Chuyên sâu', 'Tính từ dữ liệu theo lớp'))
    s.append(sl(callout('warn', 'Chọn số lớp', 'Quá ít lớp: mất hình dạng. Quá nhiều lớp: nhiễu. Thường k = 5–15; dùng Sturges k ≈ 1 + 3.3 log₁₀ n như điểm xuất phát.')
                + table(['n', '20', '50', '100', '500', '1000'], [['k (Sturges)'] + [fg(round(1 + 3.3 * math.log10(v))) for v in (20, 50, 100, 500, 1000)]])
                + '<p>Độ rộng lớp nên bằng nhau để chiều cao cột so sánh được trực tiếp với tần suất; nếu độ rộng khác nhau phải dùng mật độ (tần suất/độ rộng).</p>', K + 'PHẦN 1 · Chuyên sâu', 'Bao nhiêu lớp là hợp lý?'))
    P.append(dict(title='Chuyên sâu: dữ liệu và bảng tần số', bullets=['Loại dữ liệu', 'Lập bảng tần số', 'Tính từ bảng', 'Số lớp'], slides=s))
    # ───────── B. Đo vị trí và độ phân tán ─────────
    s = []
    xa = [12, 15, 14, 10, 18, 20, 16, 13, 17]       # n lẻ
    xb = [12, 15, 14, 10, 18, 20, 16, 13]           # n chẵn
    qa, qb = quartiles(xa), quartiles(xb)
    s.append(sl(callout('info', 'Ví dụ B1 · Tứ phân vị khi n lẻ', 'Dữ liệu (n = 9): ' + L(xa) + '.')
                + steps(['Sắp xếp: ' + L(sorted(xa)) + '.', 'Trung vị qM là giá trị thứ 5: ' + fg(qa[1]) + '.', 'Nửa dưới (bỏ qM): ' + L(sorted(xa)[:4]) + ' ⇒ qL = ' + fg(qa[0]) + '. Nửa trên: ' + L(sorted(xa)[5:]) + ' ⇒ qU = ' + fg(qa[2]) + '.', 'IQR = qU − qL = ' + fg(qa[2] - qa[0]) + '.'])
                + callout('warn', 'Quy ước giáo trình', 'Khi n lẻ, loại qM khỏi hai nửa. Phần mềm khác (Excel, numpy) có thể nội suy và cho kết quả hơi khác.'), K + 'PHẦN 2 · Chuyên sâu', 'Tứ phân vị, n lẻ'))
    s.append(sl(callout('info', 'Ví dụ B2 · Tứ phân vị khi n chẵn', 'Dữ liệu (n = 8): ' + L(xb) + '.')
                + steps(['Sắp xếp: ' + L(sorted(xb)) + '.', 'qM = (4 giá trị thứ 4 và 5)/2 = ' + fg(qb[1]) + '.', 'Nửa dưới ' + L(sorted(xb)[:4]) + ' ⇒ qL = ' + fg(qb[0]) + '; nửa trên ' + L(sorted(xb)[4:]) + ' ⇒ qU = ' + fg(qb[2]) + '.', 'IQR = ' + fg(qb[2] - qb[0]) + '.']), K + 'PHẦN 2 · Chuyên sâu', 'Tứ phân vị, n chẵn'))
    xs = [4, 5, 5, 6, 6, 7, 7, 8, 38]
    xs2 = xs[:-1]
    s.append(sl(callout('info', 'Ví dụ B3 · Trung bình nhạy với ngoại lai, trung vị thì không', 'Thời gian chạy (giây) của 9 lần: ' + L(xs) + '.')
                + table(['', 'Có giá trị 38', 'Bỏ giá trị 38'], [['Trung bình x̄', f(mean(xs), 3), f(mean(xs2), 3)], ['Trung vị', fg(median(xs)), fg(median(xs2))], ['Độ lệch chuẩn s', f(sd_s(xs), 3), f(sd_s(xs2), 3)], ['IQR', fg(iqr(xs)), fg(iqr(xs2))]])
                + '<p>Một giá trị 38 kéo x̄ từ ' + f(mean(xs2), 2) + ' lên ' + f(mean(xs), 2) + ' và s từ ' + f(sd_s(xs2), 2) + ' lên ' + f(sd_s(xs), 2) + ', trong khi trung vị và IQR gần như không đổi: dữ liệu lệch thì dùng trung vị và IQR.</p>'
                + callout('good', 'Tiêu chuẩn ngoại lai', 'Ngưỡng 1.5·IQR: [' + fg(quartiles(xs)[0] - 1.5 * iqr(xs)) + '; ' + fg(quartiles(xs)[2] + 1.5 * iqr(xs)) + '] ⇒ giá trị 38 là ngoại lai.'), K + 'PHẦN 2 · Chuyên sâu', 'Độ bền vững của trung vị'))
    xv = [4, 8, 6, 5, 3, 7]
    m = mean(xv)
    s.append(sl(callout('info', 'Ví dụ B4 · Tính phương sai mẫu từng bước', 'Dữ liệu: ' + L(xv) + '.')
                + table(['xᵢ', 'xᵢ − x̄', '(xᵢ − x̄)²'], [[fg(v), f(v - m, 2), f((v - m) ** 2, 2)] for v in xv] + [['Tổng', f(sum(v - m for v in xv), 2), f(sum((v - m) ** 2 for v in xv), 2)]])
                + steps(['x̄ = ' + fg(sum(xv)) + '/' + str(len(xv)) + ' = ' + f(m, 2) + ' (tổng độ lệch luôn bằng 0).', 's² = ' + f(sum((v - m) ** 2 for v in xv), 2) + '/(n − 1) = ' + f(var_s(xv), 3) + ', s = ' + f(sd_s(xv), 3) + '.', 'Công thức nhanh: s² = (Σxᵢ² − n·x̄²)/(n − 1) = (' + fg(sum(v * v for v in xv)) + ' − ' + f(len(xv) * m * m, 2) + ')/' + str(len(xv) - 1) + ' = ' + f(var_s(xv), 3) + '.']),
                K + 'PHẦN 2 · Chuyên sâu', 'Phương sai mẫu: hai cách tính', explain='Chia cho n − 1 (không phải n) vì ta đã dùng dữ liệu để tính x̄, mất một “bậc tự do”; chia n − 1 cho ước lượng không chệch của σ².'))
    s.append(sl(formula('Hệ số biến thiên và điểm chuẩn hóa', 'CV=\\dfrac{s}{\\bar x}\\times100\\%,\\qquad z_i=\\dfrac{x_i-\\bar x}{s}')
                + callout('info', 'Ví dụ B5', 'Lớp A: x̄ = 70, s = 7. Lớp B: x̄ = 50, s = 6. Điểm 77 của A có z = 1.0; điểm 62 của B có z = 2.0. Dù điểm thô thấp hơn, em ở B giỏi hơn so với lớp mình. CV: A = 10%, B = 12% (B phân tán tương đối nhiều hơn).'), K + 'PHẦN 2 · Chuyên sâu', 'So sánh bằng CV và điểm z'))
    P.append(dict(title='Chuyên sâu: vị trí và độ phân tán', bullets=['Tứ phân vị n lẻ/chẵn', 'Ngoại lai', 'Phương sai từng bước', 'CV và z'], slides=s))
    # ───────── C. Biểu đồ và so sánh ─────────
    s = []
    ca = [41, 44, 45, 47, 48, 49, 50, 50, 51, 52, 53, 55, 57]
    cb = [38, 42, 46, 49, 50, 51, 53, 55, 58, 60, 63, 66, 71]
    s.append(sl(callout('info', 'Ví dụ C1 · So sánh hai ca sản xuất bằng boxplot', 'Khối lượng (g) mẫu từ hai ca (n = 13 mỗi ca).')
                + table(['', 'min', 'qL', 'qM', 'qU', 'max', 'IQR', 'x̄', 's'], [[nm] + [fg(min(d)), fg(quartiles(d)[0]), fg(quartiles(d)[1]), fg(quartiles(d)[2]), fg(max(d)), fg(iqr(d)), f(mean(d), 2), f(sd_s(d), 2)] for nm, d in (('Ca A', ca), ('Ca B', cb))])
                + '<p>Hai ca có trung vị ' + fg(median(ca)) + ' và ' + fg(median(cb)) + ' gần nhau nhưng ca B có IQR ' + fg(iqr(cb)) + ' lớn gấp ' + f(iqr(cb) / iqr(ca), 1) + ' lần ca A: ca B kém ổn định hơn. Boxplot đặt cạnh nhau cho thấy điều này ngay lập tức.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Đọc và so sánh boxplot'))
    s.append(sl(table(['Hình dạng', 'Dấu hiệu', 'Quan hệ x̄ và trung vị', 'Ví dụ'], [['Đối xứng', 'hai đuôi cân', 'x̄ ≈ qM', 'chiều cao, sai số đo'], ['Lệch phải', 'đuôi dài về giá trị lớn', 'x̄ > qM', 'thu nhập, thời gian chờ'], ['Lệch trái', 'đuôi dài về giá trị nhỏ', 'x̄ < qM', 'điểm thi dễ, tuổi thọ']])
                + '<p>Boxplot: khoảng cách qM − qL và qU − qM không bằng nhau, hoặc “râu” một bên dài hơn, là dấu hiệu lệch.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Nhận biết hình dạng phân phối'))
    xe = [31, 35, 36, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 52, 55]
    s.append(sl(callout('info', 'Ví dụ C2 · Biểu đồ thân–lá', 'Điểm 15 sinh viên: ' + L(xe) + '.')
                + '<pre><code>' + '\n'.join(f'{st_} | ' + ' '.join(str(v % 10) for v in xe if v // 10 == st_) for st_ in range(3, 6)) + '</code></pre>'
                + '<p>Thân là hàng chục, lá là hàng đơn vị. Từ biểu đồ đọc ngay: ' + 'min ' + fg(min(xe)) + ', max ' + fg(max(xe)) + ', trung vị ' + fg(median(xe)) + ' (giá trị thứ 8), nhóm tập trung ở thân 4.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Thân–lá giữ nguyên dữ liệu'))
    s.append(sl(callout('info', 'Ví dụ C3 · Quy tắc 68–95–99.7 áp dụng', 'Chiều cao nam trưởng thành x̄ = 168 cm, s = 6 cm, phân phối hình chuông.')
                + steps(['Khoảng x̄ ± s = [162, 174]: khoảng 68%.', 'Khoảng x̄ ± 2s = [156, 180]: khoảng 95%.', 'Khoảng x̄ ± 3s = [150, 186]: khoảng 99.7%.', 'Người cao 186 cm: z = 3 — hiếm (khoảng 0.15% mỗi phía).'])
                + callout('warn', 'Điều kiện', 'Chỉ dùng cho dữ liệu hình chuông. Với dữ liệu bất kỳ, chỉ có Chebyshev: ít nhất 75% trong x̄ ± 2s (Module 5).'), K + 'PHẦN 3 · Chuyên sâu', 'Quy tắc 68–95–99.7'))
    P.append(dict(title='Chuyên sâu: biểu đồ và so sánh', bullets=['Boxplot so sánh', 'Hình dạng phân phối', 'Thân–lá', 'Quy tắc 68–95–99.7'], slides=s))
    return P
