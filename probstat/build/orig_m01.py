"""Module 1 — Biểu diễn dữ liệu: câu GỐC từ Lecture Notes (§1.1, Bài 1.1–1.3), Kreyszig PS 24.1, đề giữa kỳ mẫu,
cộng các biến thể tham số (nhãn bo_sung). Mọi đáp án tính bằng pskit và đối chiếu numpy."""
import random, math
from pskit import *
from qb import f, fg, nd, ni

DATA = {
 'K1': ('Kreyszig PS 24.1, Prob. 1 (độ dài đinh, mm)', [19, 21, 19, 20, 19, 20, 21, 20], 'mm', 11),
 'K2': ('Kreyszig PS 24.1, Prob. 2 (số cuộc gọi/phút)', [6, 6, 4, 2, 1, 7, 0, 4, 6, 7], 'cuộc', 12),
 'K3': ('Kreyszig PS 24.1, Prob. 3 = Lecture Notes Bài 1.1(b) (huyết áp tâm thu 15 bệnh nhân nữ 20–22 tuổi)',
        [156, 158, 154, 133, 141, 130, 144, 137, 151, 146, 156, 138, 138, 149, 139], 'mmHg', 13),
 'K4': ('Kreyszig PS 24.1, Prob. 4 (hàm lượng sắt Fe₂O₃, %, 15 mẫu hermatit)',
        [72.8, 70.4, 71.2, 69.2, 70.3, 68.9, 71.1, 69.8, 71.5, 69.7, 70.5, 71.3, 69.1, 70.9, 70.6], '%', 14),
 'K5': ('Kreyszig PS 24.1, Prob. 5 (khối lượng túi đóng gói, g)', [203, 199, 198, 201, 200, 201, 201], 'g', None),
 'K6': ('Kreyszig PS 24.1, Prob. 6 (mức tiêu thụ xăng, dặm/gallon)', [15.0, 15.5, 14.5, 15.0, 15.5, 15.0], 'mpg', None),
 'K7': ('Kreyszig PS 24.1, Prob. 7 = Lecture Notes Bài 1.1(c) (thời gian nhả rơ-le, s)',
        [1.3, 1.2, 1.4, 1.5, 1.3, 1.3, 1.4, 1.1, 1.5, 1.4, 1.6, 1.3, 1.5, 1.1, 1.4, 1.2, 1.3, 1.5, 1.4, 1.4], 's', 15),
 'K8': ('Kreyszig PS 24.1, Prob. 8 (độ cứng Brinell của 20 tấm đồng, kg/mm²)',
        [86, 86, 87, 89, 76, 85, 82, 86, 87, 85, 90, 88, 89, 90, 88, 80, 84, 89, 90, 89], 'kg/mm²', 16),
 'K9': ('Kreyszig PS 24.1, Prob. 9 (hiệu suất 7 tuabin Francis, %)', [91.8, 89.1, 89.9, 92.5, 90.7, 91.2, 91.0], '%', None),
 'K10': ('Kreyszig PS 24.1, Prob. 10', [-0.51, 0.12, -0.47, 0.95, 0.25, -0.18, -0.54], '', None),
 'LN1': ('Lecture Notes Bài 1.1(a) (độ dài móng tay, mm)', [20, 21, 21, 19, 20, 19, 21, 19], 'mm', None),
 'LN2': ('Lecture Notes Ví dụ 1.1 (sức căng 14 tấm thép, kg/mm²)', [89, 84, 87, 81, 89, 86, 91, 90, 78, 89, 87, 99, 83, 89], 'kg/mm²', None),
}
TOPIC = {'mean': 'Trung bình và trung vị', 'spread': 'Phương sai, độ lệch chuẩn', 'quart': 'Tứ phân vị, boxplot, ngoại lai',
         'repr': 'Stem-and-leaf, histogram', 'theory': 'Lý thuyết và quy tắc 68–95–99.7', 'group': 'Dữ liệu theo lớp (bảng tần số)'}

def nums_text(x, d=None):
    return ', '.join(fg(v, 3) if d is None else f(v, d) for v in x)

def dec_of(x):
    return max((len(str(v).split('.')[1]) if '.' in str(v) else 0) for v in x)

def build(B):
    rng = random.Random(101)
    for key, (name, x, unit, prob) in DATA.items():
        check_basic(x)
        n = len(x); m = mean(x); md = median(x); s = sd_s(x); v = var_s(x)
        qL, qM, qU = quartiles(x); R = qU - qL; ol = outliers(x)
        dd = dec_of(x); D = max(dd + 2, 3)
        stem = f'{name}.\nDữ liệu (n = {n}): {nums_text(x)}'
        src = name.split(' (')[0] if prob is None else name.split(' (')[0]
        tag = lambda extra='': f'{src}{extra}'
        u = f' {unit}' if unit else ''
        # 1. trung bình
        B.mcq(stem + '\nTính trung bình mẫu x̄.', f(m, D), nd(m, rng, D, extra=[md, sum(x) / (n - 1), (min(x) + max(x)) / 2]),
              f'x̄ = Σxᵢ/n = {fg(sum(x), 4)}/{n} = {f(m, D)}. Nhầm thường gặp: chia cho n−1 (ra {f(sum(x)/(n-1), D)}), hoặc lấy trung vị {fg(md, 4)} thay cho trung bình.',
              1, TOPIC['mean'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 2. trung vị
        B.mcq(stem + '\nTìm trung vị qM của dữ liệu.', f(md, max(dd, 1)), nd(md, rng, max(dd, 1), extra=[m, (min(x) + max(x)) / 2, sorted(x)[n // 2 - 1] if n % 2 == 0 else sorted(x)[n // 2 + 1]]),
              f'Sắp xếp: {nums_text(sorted(x))}. n = {n} {"lẻ nên qM là phần tử thứ (n+1)/2 = " + str((n+1)//2) if n % 2 else "chẵn nên qM = (x_{n/2} + x_{n/2+1})/2 với n/2 = " + str(n//2)} ⇒ qM = {fg(md, 4)}.',
              1, TOPIC['mean'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 3. độ lệch chuẩn
        B.mcq(stem + '\nTính độ lệch chuẩn mẫu s (công thức chia n−1).', f(s, D), nd(s, rng, D, extra=[math.sqrt(var_p(x)), v, R, (max(x) - min(x)) / 4]),
              f'Σ(xᵢ−x̄)² = {f((n-1)*v, D+1)}; s² = {f(v, D+1)}; s = √s² = {f(s, D)}. Nếu chia cho n (phương sai tổng thể) sẽ ra {f(math.sqrt(var_p(x)), D)} — không phải s mẫu.',
              2, TOPIC['spread'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 4. phương sai
        B.mcq(stem + '\nTính phương sai mẫu s².', f(v, D), nd(v, rng, D, extra=[var_p(x), s, v * n / (n + 1)]),
              f's² = Σ(xᵢ−x̄)²/(n−1) = {f((n-1)*v, D+1)}/{n-1} = {f(v, D)}. Công thức nhanh: s² = n/(n−1)·(x̄² − x̄²) với x̄² là trung bình bình phương: Σxᵢ²/n = {f(sum(t*t for t in x)/n, D)}.',
              2, TOPIC['spread'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 5. tứ phân vị
        B.mcq(stem + '\nTìm khoảng biến thiên tứ phân vị IQR = qU − qL (qL, qU là trung vị của nửa dưới, nửa trên sau khi bỏ qM nếu n lẻ).',
              f(R, max(dd, 1)), nd(R, rng, max(dd, 1), extra=[qU - qM, qM - qL, max(x) - min(x), (max(x) - min(x)) / 2]),
              f'Nửa dưới: {nums_text(sorted(x)[:n//2])} ⇒ qL = {fg(qL, 4)}. Nửa trên: {nums_text(sorted(x)[(n+1)//2:])} ⇒ qU = {fg(qU, 4)}. IQR = {fg(qU, 4)} − {fg(qL, 4)} = {fg(R, 4)}.',
              2, TOPIC['quart'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 6. khoảng biến thiên
        rg = max(x) - min(x)
        B.mcq(stem + '\nTìm độ rộng (khoảng biến thiên) R = x_max − x_min.', f(rg, max(dd, 1)), nd(rg, rng, max(dd, 1), extra=[R, rg / 2, max(x)]),
              f'x_max = {fg(max(x), 4)}, x_min = {fg(min(x), 4)} ⇒ R = {fg(rg, 4)}. (Khác IQR = {fg(R, 4)}.)', 1, TOPIC['quart'],
              tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 7. ngoại lai
        lo, hi = qL - 1.5 * R, qU + 1.5 * R
        wr = [str(i) for i in range(0, 4) if i != len(ol)]
        B.mcq(stem + '\nDùng tiêu chuẩn 1.5·IQR (ngoại lai nếu x < qL − 1.5·IQR hoặc x > qU + 1.5·IQR). Dữ liệu có bao nhiêu giá trị ngoại lai?',
              str(len(ol)), wr + [str(len(ol) + 4)],
              f'qL = {fg(qL,4)}, qU = {fg(qU,4)}, IQR = {fg(R,4)} ⇒ ngưỡng [{fg(lo,4)}; {fg(hi,4)}]. ' + (f'Ngoại lai: {nums_text(ol)}.' if ol else 'Không giá trị nào nằm ngoài ngưỡng ⇒ 0 ngoại lai.'),
              3, TOPIC['quart'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 8. so sánh trung bình – trung vị
        diff = m - md
        ans = 'x̄ > qM' if diff > 1e-9 else ('x̄ < qM' if diff < -1e-9 else 'x̄ = qM')
        opts = ['x̄ > qM', 'x̄ < qM', 'x̄ = qM', 'Không thể so sánh']
        B.mcq(stem + '\nSo sánh trung bình x̄ và trung vị qM của dữ liệu (đề Kreyszig 11–16 yêu cầu “find the mean and compare it with the median”).',
              ans, [o for o in opts if o != ans],
              f'x̄ = {f(m, D)}, qM = {fg(md, 4)} ⇒ {ans}. Dữ liệu lệch phải (đuôi bên lớn) kéo trung bình lên cao hơn trung vị; lệch trái thì ngược lại.',
              2, TOPIC['mean'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # 9. quy tắc thực nghiệm: số điểm trong (x̄ - s, x̄ + s)
        c1 = sum(1 for t in x if m - s < t < m + s)
        B.mcq(stem + '\nCó bao nhiêu giá trị nằm trong khoảng (x̄ − s, x̄ + s)?', str(c1), ni(c1, rng, extra=[n, n - 1, round(0.68 * n)], lo=0),
              f'x̄ = {f(m, D)}, s = {f(s, D)} ⇒ khoảng ({f(m - s, D)}; {f(m + s, D)}). Đếm các giá trị nằm trong: {c1}/{n} ({100*c1/n:.0f}%). Quy tắc kinh nghiệm cho dữ liệu hình chuông là xấp xỉ 68%.',
              2, TOPIC['theory'], tag(' – chuyển thành trắc nghiệm' if prob is None else f' → Prob. {prob}'))
        # essay (chỉ cho các tập có yêu cầu biểu diễn)
        B.essay(stem + '\nBiểu diễn dữ liệu bằng stem-and-leaf, tính x̄, qM, s, IQR và tìm ngoại lai.',
                f'n = {n}; x̄ = {f(m, D)}; qL = {fg(qL,4)}, qM = {fg(md,4)}, qU = {fg(qU,4)}; IQR = {fg(R,4)}; s² = {f(v, D)}, s = {f(s, D)}; ngưỡng ngoại lai [{fg(lo,4)}; {fg(hi,4)}] ⇒ ' + (f'ngoại lai: {nums_text(ol)}.' if ol else 'không có ngoại lai.') + '\n' + stem_leaf(x),
                2, TOPIC['repr'], tag())

    # ---- Lecture Notes §1.1: các câu hỏi về stem-and-leaf / histogram / boxplot của ví dụ 1.1 ----
    x = DATA['LN2'][1]; sx = sorted(x)
    src = 'Lecture Notes Ví dụ 1.1 (§1.1.1)'
    B.mcq('Dữ liệu sức căng 14 tấm thép (kg/mm²): 78, 81, 83, 84, 86, 87, 87, 89, 89, 89, 89, 90, 91, 99. Tần suất tuyệt đối của giá trị 89 là bao nhiêu?',
          '4', ['3', '5', '2'], 'Trong dữ liệu đã sắp xếp (1.2) có bốn số 89 ⇒ tần suất tuyệt đối của 89 là 4.', 1, TOPIC['repr'], src)
    B.mcq('Trong biểu đồ stem-and-leaf của dữ liệu sức căng thép (nhóm 75–79, 80–84, 85–89, 90–94, 95–99), cột “CAF” (tần suất tuyệt đối tích lũy) ở dòng thứ ba (nhóm 85–89) có giá trị bao nhiêu?',
          '11', ['7', '4', '13'], 'Nhóm 75–79 có 1 giá trị (78); 80–84 có 3 giá trị (81, 83, 84); 85–89 có 7 giá trị (86, 87, 87, 89, 89, 89, 89). CAF = 1 + 3 + 7 = 11.', 2, TOPIC['repr'], src)
    B.mcq('Với dữ liệu sức căng thép (n = 14), chia thành các lớp độ rộng 5 có điểm giữa 77, 82, 87, 92, 97. Tần suất tương đối của lớp có điểm giữa 87 (84.5–89.5) là bao nhiêu?',
          '0.50', ['0.21', '0.14', '0.07'], 'Lớp 84.5–89.5 chứa 86, 87, 87, 89, 89, 89, 89 ⇒ 7 giá trị; f_rel = 7/14 = 0.5 (bảng 1.1 của giáo trình).', 2, TOPIC['repr'], src)
    B.mcq('Cũng với dữ liệu trên, tần suất tương đối của lớp 79.5–84.5 là bao nhiêu?',
          '0.21', ['0.07', '0.14', '0.50'], 'Lớp 79.5–84.5 chứa 81, 83, 84 ⇒ 3 giá trị ⇒ 3/14 ≈ 0.21.', 1, TOPIC['repr'], src)
    B.mcq('Tổng các tần suất lớp tương đối của một histogram luôn bằng bao nhiêu?', '1', ['0.5', '100', 'Tuỳ dữ liệu'],
          'Mỗi lớp có f_rel = (số phần tử lớp)/n, các lớp phân hoạch toàn bộ dữ liệu nên tổng = n/n = 1.', 1, TOPIC['repr'], 'Lecture Notes §1.1.1')
    B.mcq('Với dữ liệu sức căng thép, trung vị qM bằng bao nhiêu?', '88.0', ['87.0', '89.0', '87.3'],
          'n = 14 chẵn: qM = (x₇ + x₈)/2 = (87 + 89)/2 = 88.', 1, TOPIC['mean'], src)
    B.mcq('Với dữ liệu sức căng thép: qL = 84, qU = 89. IQR bằng bao nhiêu và x = 99 có phải ngoại lai không?',
          'IQR = 5; ngưỡng trên 96.5 < 99 nên là ngoại lai', ['IQR = 5; 99 không phải ngoại lai vì 99 − 89 = 10 < 21', 'IQR = 21; 99 là ngoại lai', 'IQR = 15; 99 không phải ngoại lai'],
          'IQR = 89 − 84 = 5. qU + 1.5·IQR = 89 + 7.5 = 96.5 < 99 = x₁₄ ⇒ 99 là ngoại lai (giáo trình).', 3, TOPIC['quart'], src)
    B.mcq('Với dữ liệu sức căng thép, x̄ = 611/7 ≈ 87.3 và s² = 176/7. Độ lệch chuẩn s xấp xỉ bao nhiêu?', '5.014', ['25.143', '4.813', '3.357'],
          's = √(176/7) = √25.1429 ≈ 5.014 (kg/mm²).', 2, TOPIC['spread'], src)

    # ---- Lý thuyết (Nhận xét 1.1, định nghĩa) ----
    src = 'Lecture Notes §1.1.2'
    B.mcq('Theo quy tắc kinh nghiệm (empirical rule) cho dữ liệu hình quả chuông, khoảng (x̄ − 2s, x̄ + 2s) chứa xấp xỉ bao nhiêu phần trăm dữ liệu?', '95%', ['68%', '99.7%', '50%'],
          '(x̄ ± s): 68%; (x̄ ± 2s): 95%; (x̄ ± 3s): 99.7% (Nhận xét 1.1).', 1, TOPIC['theory'], src)
    B.mcq('Theo quy tắc kinh nghiệm, khoảng (x̄ − 3s, x̄ + 3s) chứa xấp xỉ bao nhiêu phần trăm dữ liệu hình chuông?', '99.7%', ['68%', '95%', '100%'],
          'Quy tắc 68–95–99.7.', 1, TOPIC['theory'], src)
    B.mcq('Độ lệch chuẩn mẫu s có đơn vị như thế nào?', 'Cùng đơn vị với dữ liệu', ['Bình phương đơn vị của dữ liệu', 'Không có đơn vị', 'Phần trăm'],
          's = √s² nên có cùng đơn vị với dữ liệu; s² có đơn vị bình phương.', 1, TOPIC['spread'], src)
    B.mcq('Phương sai mẫu s² có đơn vị như thế nào nếu dữ liệu đo bằng kg/mm²?', '(kg/mm²)²', ['kg/mm²', 'Không có đơn vị', 'mm²'],
          's² = Σ(xᵢ − x̄)²/(n−1) có đơn vị bình phương của dữ liệu.', 1, TOPIC['spread'], src)
    B.mcq('Công thức tính nhanh phương sai mẫu theo giáo trình là:', 's² = n/(n−1)·(trung bình bình phương − bình phương trung bình)',
          ['s² = (trung bình bình phương) − x̄', 's² = Σ|xᵢ − x̄|/(n−1)', 's² = Σ(xᵢ − x̄)²/n'],
          'Từ (1.5): s² = n/(n−1)·(x̄² − (x̄)²) với x̄² = (1/n)Σxᵢ². Mẫu số là n−1 (không phải n) và dùng bình phương độ lệch.', 2, TOPIC['spread'], src)
    B.mcq('Một giá trị dữ liệu được gọi là ngoại lai (outlier) khi:', 'Khoảng cách từ nó tới biên gần nhất của hộp lớn hơn 1.5 lần IQR',
          ['Nó lớn hơn trung bình', 'Nó lớn hơn 3 lần độ lệch chuẩn so với trung vị', 'Nó là giá trị lớn nhất của dữ liệu'],
          'Định nghĩa của giáo trình: khoảng cách tới biên gần nhất của hộp (qL hoặc qU) > 1.5·IQR.', 2, TOPIC['quart'], 'Lecture Notes §1.1.1 (boxplot)')
    B.mcq('Biểu đồ hộp (boxplot) biểu diễn 5 vị trí nào của dữ liệu?', 'min, qL, qM, qU, max', ['x̄, s, min, max, n', 'min, x̄, qM, max, s', 'qL, qU, x̄, s², IQR'],
          'Năm số tóm tắt: giá trị nhỏ nhất, tứ vị phân thứ nhất, trung vị, tứ vị phân thứ ba, giá trị lớn nhất.', 1, TOPIC['quart'], 'Lecture Notes §1.1.1')
    B.mcq('Với n lẻ, qL được tính như thế nào theo giáo trình?', 'Trung vị của các phần tử nằm dưới qM (không gồm qM)',
          ['Phần tử thứ n/4', 'Trung bình của x₁ và qM', 'Trung vị của toàn bộ dữ liệu'],
          'qL = trung vị của các phần tử nằm dưới giá trị qM; qU = trung vị của các phần tử nằm trên qM.', 2, TOPIC['quart'], 'Lecture Notes §1.1.1')
    B.mcq('Khi thêm vào bộ dữ liệu một giá trị ngoại lai cực lớn, đại lượng nào dưới đây thay đổi ÍT nhất?', 'Trung vị qM',
          ['Trung bình x̄', 'Độ lệch chuẩn s', 'Độ rộng R = x_max − x_min'],
          'Trung bình và độ lệch chuẩn nhạy với ngoại lai; R chắc chắn tăng mạnh; trung vị (và IQR) là các thống kê bền vững, chỉ dịch chuyển nhiều nhất một vị trí.', 3, TOPIC['theory'], 'Kreyszig PS 24.1, Prob. 17–18 (ý nghĩa)')

    # ---- Kreyszig 17–20 ----
    d = [4, 1, 3, 10, 2]; d2 = [4, 1, 3, 2]
    sA, sB = sd_s(d), sd_s(d2)
    B.mcq('Tính s cho dữ liệu 4, 1, 3, 10, 2 rồi xoá ngoại lai (10) và tính lại s. Cặp (s trước, s sau) là:', f'({f(sA,3)}; {f(sB,3)})',
          [f'({f(sB,3)}; {f(sA,3)})', f'({f(sA,3)}; {f(sA,3)})', f'({f(math.sqrt(var_p(d)),3)}; {f(math.sqrt(var_p(d2)),3)})'],
          f'Trước: x̄ = {fg(mean(d))}, s = {f(sA,3)}. Sau khi bỏ 10: x̄ = {fg(mean(d2))}, s = {f(sB,3)}. Một ngoại lai làm s tăng mạnh (≈{sA/sB:.1f} lần).', 3, TOPIC['spread'], 'Kreyszig PS 24.1, Prob. 17')
    d8 = DATA['K8'][1]; d8r = [t for t in d8 if t not in outliers(d8)]
    B.mcq('Với dữ liệu độ cứng Brinell (Prob. 8, ngoại lai là 76), độ lệch chuẩn s trước và sau khi xoá các ngoại lai là:',
          f'({f(sd_s(d8),3)}; {f(sd_s(d8r),3)})', [f'({f(sd_s(d8r),3)}; {f(sd_s(d8),3)})', f'({f(sd_s(d8),3)}; {f(sd_s(d8),3)})', f'({f(sd_s(d8r),3)}; {f(sd_s(d8r),3)})'],
          f'Ngoại lai theo 1.5·IQR: {nums_text(outliers(d8))}. n giảm từ {len(d8)} xuống {len(d8r)}; s giảm từ {f(sd_s(d8),3)} xuống {f(sd_s(d8r),3)}.', 3, TOPIC['spread'], 'Kreyszig PS 24.1, Prob. 18')
    B.mcq('Bài 19 (Kreyszig): bộ dữ liệu đơn giản nhất có x̄ = 100 nhưng qM = 0 gồm 5 số 0, 0, 0, 0, 500 (n = 5, Σ = 500). Ý nghĩa của bài này là gì?',
          'Trung bình và trung vị có thể rất khác nhau; chỉ riêng trung bình không mô tả được dữ liệu lệch',
          ['Trung bình luôn bằng trung vị', 'Trung vị luôn lớn hơn trung bình', 'Dữ liệu này không thể có độ lệch chuẩn'],
          f'x̄ = 500/5 = 100, qM = 0. Dữ liệu lệch mạnh về phải bởi một giá trị lớn nên trung bình bị kéo lên; cần mô tả kèm trung vị và độ phân tán.', 3, TOPIC['mean'], 'Kreyszig PS 24.1, Prob. 19')
    B.mcq('Bài 20 (Kreyszig): khẳng định nào đúng về trung bình mẫu x̄?', 'min xᵢ ≤ x̄ ≤ max xᵢ',
          ['x̄ luôn bằng một giá trị của dữ liệu', 'x̄ luôn nhỏ hơn max xᵢ một cách chặt', 'x̄ luôn bằng trung vị'],
          'x̄ = Σxᵢ/n ≥ n·min/n = min và ≤ max. Dấu “=” xảy ra khi mọi xᵢ bằng nhau (nên không phải luôn “chặt”).', 2, TOPIC['mean'], 'Kreyszig PS 24.1, Prob. 20')

    # ---- Đề giữa kỳ mẫu câu 9(a): dữ liệu theo lớp ----
    mids = [7, 9, 11, 13]; cnt = [4, 8, 9, 5]; N = sum(cnt)
    xb = sum(a * b for a, b in zip(mids, cnt)) / N
    s2 = sum(b * (a - xb) ** 2 for a, b in zip(mids, cnt)) / (N - 1)
    src = 'Đề giữa kỳ mẫu LTXSTK, câu 9(a)'
    st9 = 'Thời gian điều trị X (ngày) của bệnh A: lớp 6–8, 8–10, 10–12, 12–14 với số bệnh nhân 4, 8, 9, 5. Lấy điểm giữa của mỗi lớp (7, 9, 11, 13).'
    B.mcq(st9 + '\nTính trung bình mẫu x̄.', f(xb, 4), nd(xb, rng, 4, extra=[sum(a*b for a,b in zip(mids,cnt))/(N-1), 10, 10.5]),
          f'N = {N}; Σnᵢxᵢ = 4·7 + 8·9 + 9·11 + 5·13 = {sum(a*b for a,b in zip(mids,cnt))}; x̄ = {sum(a*b for a,b in zip(mids,cnt))}/{N} = {f(xb,4)}.', 2, TOPIC['group'], src)
    B.mcq(st9 + '\nTính phương sai mẫu s² (chia N−1).', f(s2, 4), nd(s2, rng, 4, extra=[sum(b*(a-xb)**2 for a,b in zip(mids,cnt))/N, math.sqrt(s2)]),
          f's² = Σnᵢ(xᵢ − x̄)²/(N−1) = {f(sum(b*(a-xb)**2 for a,b in zip(mids,cnt)),4)}/{N-1} = {f(s2,4)}; s = {f(math.sqrt(s2),4)}.', 3, TOPIC['group'], src)
    B.essay(st9 + '\n(a) Tính x̄ và s².', f'x̄ = {f(xb,4)}; s² = {f(s2,4)}; s = {f(math.sqrt(s2),4)}. (Lời giải mẫu: dùng điểm giữa lớp, N = {N}.)', 2, TOPIC['group'], src)

    # ---- Tự luận Lecture Notes Bài 1.1–1.3 ----
    for key in ('LN1', 'K3', 'K7'):
        nm, x, unit, prob = DATA[key]
        qL, qM, qU = quartiles(x); R = qU - qL
        B.essay(f'Lecture Notes Bài 1.1–1.3: {nm}. Biểu diễn bằng stem-and-leaf, vẽ boxplot, tìm ngoại lai và tính x̄, s², s.',
                f'x̄ = {f(mean(x),3)}, s² = {f(var_s(x),3)}, s = {f(sd_s(x),3)}; qL = {fg(qL,4)}, qM = {fg(qM,4)}, qU = {fg(qU,4)}, IQR = {fg(R,4)}; ngoại lai: ' + (nums_text(outliers(x)) if outliers(x) else 'không có') + '.\n' + stem_leaf(x),
                2, TOPIC['repr'], f'Lecture Notes Bài 1.1–1.3 / Kreyszig PS 24.1')

def stem_leaf(x):
    """Biểu đồ thân–lá dạng văn bản (số nguyên: thân = hàng chục; số thập phân 1 chữ số: thân = phần nguyên)."""
    dec = dec_of(x)
    rows = {}
    for v in sorted(x):
        if dec == 0:
            st, lf = divmod(int(v), 10) if v >= 0 else (-(abs(int(v)) // 10), abs(int(v)) % 10)
        else:
            t = round(abs(v) * 10 ** dec)
            st, lf = divmod(t, 10 ** dec); st = -st if v < 0 else st
        rows.setdefault(st, []).append(str(lf))
    return 'Stem | Leaf\n' + '\n'.join(f'{k:>4} | ' + ' '.join(v) for k, v in sorted(rows.items()))
