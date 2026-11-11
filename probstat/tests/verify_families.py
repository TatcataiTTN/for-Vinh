"""Tính lại ĐỘC LẬP các họ câu tham số hóa mới (ext_more_*): đọc đề bằng regex rồi tính bằng NumPy/SciPy/itertools, so với đáp án đúng.
Chạy từ thư mục probstat: python3 tests/verify_families.py"""
import json, re, math, sys, itertools, collections
import numpy as np
from scipy import stats as st
def N(s): return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s.replace('−', '-'))]
def val(o): return float(re.sub(r'[^\d.\-]', '', o.replace('−', '-')))
def pair(o): a = N(o); return a if len(a) == 2 else None
cnt = collections.Counter(); bad = []
def chk(it, exact, tol, kind, iv=False):
    cnt[kind] += 1; o = it['opts'][it['correct']]
    if iv:
        p = pair(o)
        if not p or abs(p[0] - exact[0]) > tol or abs(p[1] - exact[1]) > tol: bad.append((kind, it['id'], o, exact))
    else:
        try: v = val(o)
        except ValueError: bad.append((kind, it['id'], o, 'không phải số')); return
        if abs(v - exact) > tol: bad.append((kind, it['id'], o, round(exact, 5)))
def load(m): return json.load(open(f'data/qbank/{m}.json', encoding='utf-8'))['items']
D = {f'm{i:02d}': load(f'm{i:02d}') for i in range(1, 14)}
t3 = lambda ndp: 0.5 * 10 ** -ndp + 1e-9
for mid, items in D.items():
    for it in items:
        q = it['q'].replace('−', '-') if mid == 'm13' else it['q']; m = None; o = it['opts'][it['correct']]
        dp = len(o.split('.')[-1]) if '.' in o and re.fullmatch(r'[−\-]?\d+\.\d+', o.strip()) else 0
        # ---- M13
        if m := re.match(r'Dữ liệu \(x; y\): (.*)\. Hệ số góc b', q):
            pts = [tuple(map(float, x)) for x in re.findall(r'\(([\d.\-]+); ([\d.\-]+)\)', m[1])]; x, y = zip(*pts); chk(it, np.polyfit(x, y, 1)[0], t3(dp) + 1e-3, 'M13 hệ số góc từ dữ liệu thô')
        elif m := re.match(r'Dữ liệu \(x; y\): (.*)\. Hệ số tương quan', q):
            pts = [tuple(map(float, x)) for x in re.findall(r'\(([\d.\-]+); ([\d.\-]+)\)', m[1])]; x, y = zip(*pts); chk(it, np.corrcoef(x, y)[0, 1], t3(dp) + 1e-3, 'M13 r từ dữ liệu thô')
        elif m := re.match(r'Có S_xx = Σ\(x − x̄\)² = ([\d.]+), S_xy = Σ\(x − x̄\)\(y − ȳ\) = ([\-−\d.]+)', q): chk(it, N(m[2])[0] / float(m[1]), t3(dp), 'M13 b = Sxy/Sxx')
        elif m := re.match(r'r = ([\-−\d.]+), n = (\d+)\. Thống kê T', q): r, n = N(m[1])[0], int(m[2]); chk(it, r * math.sqrt(n - 2) / math.sqrt(1 - r * r), t3(dp), 'M13 T kiểm định r')
        # ---- M8
        elif m := re.match(r'Mẫu: ([\d.; ]+) \(tổng thể chuẩn, σ chưa biết\)\. Khoảng tin cậy (\d+)%', q):
            x = [float(a) for a in m[1].split(';')]; g = int(m[2]) / 100; lo, hi = st.t.interval(g, len(x) - 1, loc=np.mean(x), scale=st.sem(x)); chk(it, (lo, hi), 6e-4, 'M8 KTC từ dữ liệu thô (t)', iv=True)
        elif m := re.match(r'Giá trị tới hạn t_α với α = ([\d.]+)% của phân bố Student (\d+)', q): chk(it, st.t.ppf(1 - float(m[1]) / 100, int(m[2])), t3(3), 'M8 t_α')
        elif m := re.match(r'Giá trị tới hạn U_α \(Φ\(U_α\) = 1 − α\) với α = ([\d.]+)%', q): chk(it, st.norm.ppf(1 - float(m[1]) / 100), t3(3), 'M8 U_α')
        elif m := re.match(r'Mẫu chuẩn cỡ n = (\d+) có s² = ([\d.]+)\. Khoảng tin cậy 95% cho σ²', q):
            n, s2 = int(m[1]), float(m[2]); chk(it, ((n - 1) * s2 / st.chi2.ppf(.975, n - 1), (n - 1) * s2 / st.chi2.ppf(.025, n - 1)), 6e-4, 'M8 KTC σ² (χ²)', iv=True)
        elif m := re.match(r'σ = ([\d.]+), n = (\d+), sai số của khoảng tin cậy cho μ là e = ([\d.]+)\. Độ tin cậy', q):
            sg, n, e = float(m[1]), int(m[2]), float(m[3]); chk(it, 2 * st.norm.cdf(e * math.sqrt(n) / sg) - 1, t3(dp) + 2e-4, 'M8 độ tin cậy từ sai số')
        # ---- M7
        elif m := re.match(r'Mẫu từ phân phối Poisson\(λ\): ([\d, ]+)\.', q): chk(it, np.mean([float(a) for a in m[1].split(',')]), t3(dp), 'M7 MLE Poisson')
        elif m := re.match(r'Mẫu từ phân phối mũ mật độ λe\^\(−λx\): ([\d., ]+)\.', q): x = [float(a) for a in m[1].split(',')]; chk(it, len(x) / sum(x), t3(dp), 'M7 MLE mũ')
        elif m := re.match(r'Mẫu từ N\(μ, σ²\): ([\d., ]+)\. Ước lượng hợp lý cực đại của σ²', q): x = [float(a) for a in m[1].split(',')]; chk(it, np.var(x), t3(dp), 'M7 MLE σ² (chia n)')
        elif m := re.match(r'Mẫu từ phân phối đều U\(0; θ\): ([\d., ]+)\. Ước lượng θ bằng phương pháp moment', q): x = [float(a) for a in m[1].split(',')]; chk(it, 2 * np.mean(x), t3(dp), 'M7 moment U(0,θ)')
        elif m := re.match(r'Mẫu: ([\d; ]+)\. Phương sai mẫu s² \(chia n − 1\) bằng', q): x = [float(a) for a in m[1].split(';')]; chk(it, np.var(x, ddof=1), t3(dp), 'M7 s² dữ liệu thô')
        elif m := re.match(r'Mẫu cỡ n = (\d+) có Σxᵢ = ([\d.]+) và Σxᵢ² = ([\d.]+)\. Phương sai mẫu', q): n, sx, sxx = int(m[1]), float(m[2]), float(m[3]); chk(it, (sxx - sx * sx / n) / (n - 1), t3(dp), 'M7 s² từ Σx, Σx²')
        # ---- M10
        elif m := re.match(r'H₀: μ = ([\d.]+); σ = ([\d.]+), n = (\d+), x̄ = ([\d.]+)\. Thống kê U', q): mu0, sg, n, xb = float(m[1]), float(m[2]), int(m[3]), float(m[4]); chk(it, (xb - mu0) / (sg / math.sqrt(n)), t3(dp), 'M10 thống kê U')
        elif m := re.match(r'H₀: μ = ([\d.]+); n = (\d+), x̄ = ([\d.]+), s = ([\d.]+)\. Thống kê T', q): mu0, n, xb, s = float(m[1]), int(m[2]), float(m[3]), float(m[4]); chk(it, (xb - mu0) / (s / math.sqrt(n)), t3(dp), 'M10 thống kê T')
        elif m := re.match(r'Thống kê kiểm định U = ([\-−\d.]+)\. Giá trị p của kiểm định (phải|trái|hai phía)', q):
            z = N(m[1])[0]; chk(it, {'phải': st.norm.sf(z), 'trái': st.norm.cdf(z), 'hai phía': 2 * st.norm.sf(abs(z))}[m[2]], t3(dp), 'M10 giá trị p')
        elif m := re.match(r'H₀: p = ([\d.]+)\. Mẫu n = (\d+) có (\d+) thành công\. Thống kê U', q): p0, n, k = float(m[1]), int(m[2]), int(m[3]); chk(it, (k / n - p0) / math.sqrt(p0 * (1 - p0) / n), t3(dp), 'M10 U cho tỷ lệ')
        elif m := re.match(r'H₀: μ = (\d+) so với H₁: μ > \d+; σ = (\d+), n = (\d+), α = ([\d.]+)\. Xác suất sai lầm loại II β khi μ thực là (\d+)', q):
            mu0, sg, n, a, mu1 = float(m[1]), float(m[2]), int(m[3]), float(m[4]), float(m[5]); se = sg / math.sqrt(n); chk(it, st.norm.cdf((mu0 + st.norm.ppf(1 - a) * se - mu1) / se), t3(dp), 'M10 β')
        elif m := re.match(r'H₀: μ = (\d+), H₁: μ > \d+; σ = (\d+), n = (\d+), α = ([\d.]+)\. Bác bỏ H₀ khi x̄ > c', q): mu0, sg, n, a = float(m[1]), float(m[2]), int(m[3]), float(m[4]); chk(it, mu0 + st.norm.ppf(1 - a) * sg / math.sqrt(n), t3(dp), 'M10 ngưỡng c')
        # ---- M11
        elif m := re.match(r'Hai mẫu chuẩn: n₁ = \d+, s₁ = ([\d.]+); n₂ = \d+, s₂ = ([\d.]+)\. Thống kê F', q): chk(it, float(m[1]) ** 2 / float(m[2]) ** 2, t3(dp), 'M11 F = s₁²/s₂²')
        elif m := re.match(r'n₁ = (\d+), s₁ = ([\d.]+); n₂ = (\d+), s₂ = ([\d.]+)\. Phương sai gộp', q): n1, s1, n2, s2 = int(m[1]), float(m[2]), int(m[3]), float(m[4]); chk(it, ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2), t3(dp), 'M11 phương sai gộp')
        elif m := re.match(r'Hai nhóm: n₁ = (\d+), x̄₁ = (\d+), s₁ = ([\d.]+); n₂ = (\d+), x̄₂ = (\d+), s₂ = ([\d.]+)', q):
            n1, m1, s1, n2, m2, s2 = int(m[1]), float(m[2]), float(m[3]), int(m[4]), float(m[5]), float(m[6]); r = st.ttest_ind_from_stats(m1, s1, n1, m2, s2, n2, equal_var=True); chk(it, r.statistic, t3(dp), 'M11 t gộp (so với SciPy)')
        elif m := re.match(r'Mẫu 1: (\d+)/(\d+) thành công; mẫu 2: (\d+)/(\d+)\. H₀: p₁ = p₂\. Thống kê U', q):
            k1, n1, k2, n2 = map(int, m.groups()); pp = (k1 + k2) / (n1 + n2); chk(it, (k1 / n1 - k2 / n2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)), t3(dp), 'M11 U hai tỷ lệ')
        elif m := re.match(r'Giá trị tới hạn χ²_\{([\d.]+)\}\((\d+)\) \(P\(χ² > c\) = [\d.]+\) xấp xỉ', q): chk(it, st.chi2.ppf(1 - float(m[1]), int(m[2])), t3(dp), 'M11 χ² tới hạn')
        elif m := re.match(r'Giá trị tới hạn F_\{([\d.]+)\}\((\d+); (\d+)\)', q): chk(it, st.f.ppf(1 - float(m[1]), int(m[2]), int(m[3])), t3(dp), 'M11 F tới hạn')
        # ---- M12
        elif m := re.match(r'Gieo vật (\d+) mặt n = (\d+) lần \(H₀: đồng khả năng\)\. Tần số quan sát ([\d, ]+)\.', q):
            K, n = int(m[1]), int(m[2]); O = [float(a) for a in m[3].split(',')]; chk(it, st.chisquare(O, [n / K] * K).statistic, t3(dp), 'M12 χ² phù hợp (so với SciPy)')
        elif m := re.match(r'Kiểm định dấu: (\d+) cặp không hòa, có (\d+) cặp dương', q): n, k = int(m[1]), int(m[2]); chk(it, min(1, 2 * st.binom.cdf(min(k, n - k), n, .5)), t3(dp), 'M12 p kiểm định dấu')
        elif m := re.match(r'Biểu đồ p: p̄ = ([\d.]+), n = (\d+)\. UCL', q): p, n = float(m[1]), int(m[2]); chk(it, p + 3 * math.sqrt(p * (1 - p) / n), t3(dp), 'M12 UCL biểu đồ p')
        # ---- M3 / M6 / M2
        elif m := re.match(r'Gieo hai con xúc xắc cân đối\. Xác suất tổng số chấm bằng (\d+) là', q): s = int(m[1]); chk(it, sum(1 for a, b in itertools.product(range(1, 7), repeat=2) if a + b == s) / 36, t3(dp), 'M3 tổng hai xúc xắc (liệt kê)')
        elif m := re.match(r'Gieo hai con xúc xắc cân đối\. Biết tổng số chấm ít nhất (\d+), xác suất con thứ nhất ra (\d+)', q):
            s, x0 = int(m[1]), int(m[2]); sp = [(a, b) for a, b in itertools.product(range(1, 7), repeat=2) if a + b >= s]; chk(it, sum(1 for a, b in sp if a == x0) / len(sp), t3(dp), 'M3 xúc xắc có điều kiện (liệt kê)')
        elif m := re.match(r'X ~ B\((\d+); ([\d.]+)\)\. P\(X ≥ (\d+)\)', q): chk(it, st.binom.sf(int(m[3]) - 1, int(m[1]), float(m[2])), t3(dp), 'M6 P(X ≥ k) nhị thức')
        elif m := re.match(r'Số xâu nhị phân độ dài (\d+) có đúng (\d+) chữ số 1', q): chk(it, sum(1 for t in itertools.product('01', repeat=int(m[1])) if t.count('1') == int(m[2])), 0, 'M2 xâu nhị phân (liệt kê)')
        elif m := re.match(r'Số cách xếp các chữ cái của từ “(\w+)”', q):
            w = m[1]; chk(it, len(set(itertools.permutations(w))) if len(w) <= 8 else math.factorial(len(w)) // math.prod(math.factorial(c) for c in collections.Counter(w).values()), 0, 'M2 hoán vị có lặp (liệt kê/đa thức)')
        elif m := re.match(r'Trong các số từ 1 đến (\d+), có bao nhiêu số chia hết cho (\d+) hoặc chia hết cho (\d+)', q): n, a, b = map(int, m.groups()); chk(it, sum(1 for i in range(1, n + 1) if i % a == 0 or i % b == 0), 0, 'M2 bao hàm – loại trừ (đếm trực tiếp)')
        elif m := re.match(r'Một nhóm có (\d+) nam và (\d+) nữ\. Chọn (\d+) người sao cho có ít nhất 1 nữ', q): a, b, k = map(int, m.groups()); chk(it, math.comb(a + b, k) - math.comb(a, k), 0, 'M2 ít nhất 1 nữ')
print('đã tính lại độc lập', sum(cnt.values()), 'câu thuộc', len(cnt), 'họ:'); [print(f'  {v:4d}  {k}') for k, v in sorted(cnt.items())]
print('LỆCH:', len(bad)); [print(' ', b) for b in bad[:25]]
sys.exit(1 if bad else 0)
