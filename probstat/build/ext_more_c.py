"""Đợt mở rộng ngân hàng câu hỏi (nhãn bo_sung) cho M12, M13. Đáp án tính bằng code (NumPy/SciPy)."""
import math, random
import numpy as np
from scipy import stats as st
from qb import f, fg
from ext_more_a import nump, inte, txt, tp
SRC = 'Bổ sung: họ bài tham số hóa theo dạng đề (đáp án tự tính bằng chương trình)'

def build(mid, B):
    fn = globals().get('b_' + mid)
    if fn: fn(B, random.Random(7300 + int(mid[1:])), tp(mid))

# ───────────── M12
def b_m12(B, rng, T):
    for _ in range(14):   # giới hạn x̄-chart
        mu = rng.choice([50, 100, 12, 8.5]); sg = rng.choice([2, 3, 4, 0.5]); n = rng.choice([4, 5, 9, 16, 25]); se = sg / math.sqrt(n)
        nump(B, rng, f'Biểu đồ kiểm soát trung bình: μ = {fg(mu)}, σ = {fg(sg)}, cỡ mẫu con n = {n}. Giới hạn kiểm soát trên UCL = μ + 3σ/√n bằng', mu + 3 * se, f'UCL = {fg(mu)} + 3·{fg(sg)}/{f(math.sqrt(n),3)} = {f(mu+3*se,3)}.', 1, T['qc'], extra=[mu + 3 * sg, mu + 2 * se, mu + 3 * se * math.sqrt(n), mu - 3 * se], d=3)
        nump(B, rng, f'Biểu đồ kiểm soát trung bình: μ = {fg(mu)}, σ = {fg(sg)}, n = {n}. Độ rộng UCL − LCL bằng', 6 * se, f'UCL − LCL = 6σ/√n = {f(6*se,3)}.', 2, T['qc'], extra=[3 * se, 6 * sg, 6 * se * n], d=3)
    for k in (1, 1.5, 2, 2.5, 3, 3.5, 4):
        v = 2 * (1 - st.norm.cdf(k))
        nump(B, rng, f'Quy trình ổn định, đặc trưng chuẩn. Xác suất một điểm trung bình vượt giới hạn {fg(k)}σ (hai phía) là', v, f'2(1 − Φ({fg(k)})) = {f(v,4)}.', 2, T['qc'], extra=[1 - st.norm.cdf(k), 1 - v, v / 2], d=4, lo=0.0, hi=1.0)
        nump(B, rng, f'Với giới hạn {fg(k)}σ (hai phía), số điểm trung bình (ARL = 1/xác suất) trước khi có báo động sai là', 1 / v, f'ARL = 1/{f(v,4)} = {f(1/v,1)}.', 3, T['qc'], extra=[v, 1 / (1 - v), 1 / (v / 2), 100 * v], d=1, lo=0.0)
    for _ in range(14):   # p-chart
        p = rng.choice([0.02, 0.03, 0.05, 0.08, 0.1]); n = rng.choice([50, 100, 200, 400]); se = math.sqrt(p * (1 - p) / n)
        nump(B, rng, f'Biểu đồ p: p̄ = {fg(p)}, n = {n}. UCL = p̄ + 3√(p̄(1 − p̄)/n) bằng', p + 3 * se, f'UCL = {fg(p)} + 3·{f(se,4)} = {f(p+3*se,4)}.', 2, T['pc'], extra=[p + 3 * math.sqrt(p / n), p + 3 * p * (1 - p) / n, p + 2 * se, p - 3 * se], d=4, lo=0.0)
        lcl = p - 3 * se
        txt(B, f'Biểu đồ p: p̄ = {fg(p)}, n = {n}. Giới hạn dưới LCL = p̄ − 3√(p̄(1 − p̄)/n) là', f'{f(max(lcl,0),4)}' if lcl > 0 else '0 (lấy bằng 0 vì LCL âm)', [f'{f(lcl,4)} (giữ nguyên số âm)' if lcl <= 0 else f'{f(p+3*se,4)}', f'{f(p,4)}', f'{f(3*se,4)}'], f'p̄ − 3√(…) = {f(lcl,4)}; xác suất không thể âm nên LCL = max(0, ·).', 3, T['pc'])
    for _ in range(14):   # tần số kỳ vọng
        n = rng.choice([60, 100, 120, 200, 300]); K = rng.choice([4, 5, 6]); w = [rng.randint(1, 5) for _ in range(K)]; s = sum(w); pr = [x / s for x in w]; j = rng.randrange(K)
        B.mcq(f'Kiểm định phù hợp với {K} lớp, xác suất lý thuyết {", ".join(f(p,3) for p in pr)}, n = {n}. Tần số kỳ vọng của lớp {j+1} là', f(n * pr[j], 2), [f(n / K, 2), f(pr[j], 2), f(n * pr[j] + 1, 2), f(n * pr[j] - 1, 2), f(n * pr[j] * 1.5, 2)], f'Eⱼ = n·pⱼ = {n}·{f(pr[j],3)} = {f(n*pr[j],2)}.', 1, T['gof'], SRC, 'bo_sung')
    for _ in range(16):   # χ² thống kê
        K = rng.choice([3, 4, 5, 6]); n = rng.choice([60, 100, 150, 200]); E = [n / K] * K; O = [int(round(e + rng.randint(-8, 8))) for e in E]; O[-1] += n - sum(O); chi = sum((o - e) ** 2 / e for o, e in zip(O, E))
        nump(B, rng, f'Gieo vật {K} mặt n = {n} lần (H₀: đồng khả năng). Tần số quan sát {", ".join(map(str,O))}. Thống kê χ² = Σ(O − E)²/E bằng', chi, f'E = {f(n/K,2)}; χ² = {f(chi,3)}; bậc tự do {K-1}.', 2, T['gof'], extra=[sum((o - e) ** 2 for o, e in zip(O, E)), sum(abs(o - e) for o, e in zip(O, E)) / (n / K), chi / K, sum((o - e) ** 2 / o for o, e in zip(O, E))], d=3, lo=0.0)
    for K, m in [(4, 0), (5, 0), (6, 0), (5, 1), (6, 1), (7, 1), (8, 2), (6, 2), (10, 2), (9, 1), (7, 2), (12, 1)]:
        inte(B, f'Kiểm định χ² phù hợp có K = {K} lớp (sau gộp) và phải ước lượng m = {m} tham số. Số bậc tự do là', K - 1 - m, [K - m, K - 1, K + m - 1, K - 2 - m], f'df = K − 1 − m = {K} − 1 − {m} = {K-1-m}.', 2, T['gof'])
    for df, a in [(2, 0.05), (3, 0.05), (4, 0.05), (5, 0.05), (3, 0.01), (5, 0.01), (6, 0.05), (7, 0.025), (9, 0.1), (11, 0.05)]:
        v = st.chi2.ppf(1 - a, df)
        nump(B, rng, f'Giá trị tới hạn χ²_{{{fg(a)}}}({df}) dùng trong kiểm định phù hợp xấp xỉ', v, f'SciPy: {f(v,3)}.', 2, T['gof'], extra=[st.chi2.ppf(1 - a, df - 1), st.chi2.ppf(1 - a, df + 1), st.chi2.ppf(a, df)], d=3, lo=0.0)
    for _ in range(14):   # kiểm định dấu
        n = rng.choice([10, 12, 15, 16, 20]); k = rng.randint(1, n - 1)
        pv = min(1.0, 2 * st.binom.cdf(min(k, n - k), n, 0.5))
        nump(B, rng, f'Kiểm định dấu: {n} cặp không hòa, có {k} cặp dương. Giá trị p hai phía = 2·P(Bin({n}; 0.5) ≤ min(k, n − k)) bằng', pv, f'min = {min(k,n-k)}; p = {f(pv,4)}.', 3, T['sign'], extra=[st.binom.cdf(min(k, n - k), n, 0.5), st.binom.pmf(k, n, 0.5), 1 - pv], d=4, lo=0.0, hi=1.0)
    for _ in range(12):   # xấp xỉ chuẩn của kiểm định dấu
        n = rng.choice([30, 36, 40, 50, 64, 100]); k = round(n / 2 + rng.choice([-1, 1]) * rng.choice([0.1, 0.15, 0.2, 0.25]) * n); z = (k - n / 2) / (math.sqrt(n) / 2)
        nump(B, rng, f'Kiểm định dấu: n = {n} cặp, có {k} dương. Dưới H₀: p = 0.5, thống kê chuẩn hóa z = (k − n/2)/(√n/2) bằng', z, f'z = ({k} − {fg(n/2)})/({f(math.sqrt(n)/2,3)}) = {f(z,3)}.', 3, T['sign'], extra=[(k - n / 2) / math.sqrt(n), (k - n / 2) / (n / 4), k / n], d=3)
    for s, ok, bad in [('Biểu đồ kiểm soát phát hiện', 'dấu hiệu quy trình mất ổn định', ['sai số đo của máy', 'số bậc tự do', 'giá trị tối ưu']),
                       ('Một điểm nằm ngoài giới hạn kiểm soát cho thấy', 'có thể có nguyên nhân đặc biệt', ['quy trình chắc chắn tốt', 'cần tăng cỡ mẫu', 'sai số loại II bằng 0']),
                       ('Kiểm định χ² phù hợp yêu cầu tần số kỳ vọng mỗi lớp', 'không quá nhỏ (thường ≥ 5)', ['luôn bằng nhau', 'đúng bằng quan sát', 'bằng 1']),
                       ('Kiểm định dấu không đòi hỏi', 'tổng thể có dạng phân phối chuẩn', ['các cặp quan sát độc lập', 'bỏ cặp hòa', 'dữ liệu là cặp']),
                       ('Tần số quan sát gần tần số kỳ vọng thì χ²', 'nhỏ, khó bác bỏ H₀', ['lớn, bác bỏ H₀', 'âm', 'bằng đúng 1'])]:
        txt(B, s, ok, bad, 'Kiến thức §3.5–3.7.', 1, T['theory'])

# ───────────── M13
def b_m13(B, rng, T):
    for _ in range(15):   # hệ số từ tổng
        n = rng.choice([8, 10, 12, 15]); xb = rng.choice([4, 5, 6.5]); yb = rng.choice([20, 30, 45]); sxx = rng.choice([20, 36, 50, 64]); sxy = rng.choice([30, 48, -40, 72, -25])
        b = sxy / sxx; a = yb - b * xb
        nump(B, rng, f'Có S_xx = Σ(x − x̄)² = {sxx}, S_xy = Σ(x − x̄)(y − ȳ) = {sxy}. Hệ số góc của hồi quy y theo x là', b, f'b = S_xy/S_xx = {sxy}/{sxx} = {f(b,4)}.', 1, T['reg'], extra=[sxx / sxy, sxy, sxy / math.sqrt(sxx)], d=4)
        nump(B, rng, f'Hồi quy y theo x có hệ số góc b = {f(b,4)}, x̄ = {fg(xb)}, ȳ = {fg(yb)}. Hệ số chặn a bằng', a, f'a = ȳ − b·x̄ = {fg(yb)} − {f(b,4)}·{fg(xb)} = {f(a,4)}.', 1, T['reg'], extra=[yb + b * xb, yb / b if b else 1, b * xb], d=4)
    for _ in range(15):   # dự báo
        a = round(rng.uniform(-5, 20), 2); b = round(rng.uniform(-3, 5), 2); x0 = rng.choice([2, 5, 8, 10, 12.5]); y0 = a + b * x0
        nump(B, rng, f'Đường hồi quy mẫu ŷ = {fg(a)} {"+" if b>=0 else "−"} {fg(abs(b))}x. Dự báo ŷ tại x = {fg(x0)} là', y0, f'ŷ = {fg(a)} + ({fg(b)})·{fg(x0)} = {f(y0,3)}.', 1, T['pred'], extra=[a * x0 + b, a + b, b * x0, a - b * x0], d=3)
        yy = y0 + rng.choice([-3, -1.5, 2, 4]); nump(B, rng, f'Đường hồi quy ŷ = {fg(a)} {"+" if b>=0 else "−"} {fg(abs(b))}x. Tại x = {fg(x0)} quan sát được y = {f(yy,3)}. Phần dư e = y − ŷ bằng', yy - y0, f'e = {f(yy,3)} − {f(y0,3)} = {f(yy-y0,3)}.', 2, T['pred'], extra=[y0 - yy, yy, y0, abs(yy - y0) / 2], d=3)
    for _ in range(12):   # r từ tổng
        sxx, syy = rng.choice([25, 36, 49, 64]), rng.choice([16, 25, 49, 81]); r = rng.choice([0.6, 0.8, -0.7, -0.5, 0.9, -0.85]); sxy = r * math.sqrt(sxx * syy)
        nump(B, rng, f'S_xx = {sxx}, S_yy = {syy}, S_xy = {f(sxy,3)}. Hệ số tương quan mẫu r bằng', r, f'r = S_xy/√(S_xx·S_yy) = {f(sxy,3)}/{f(math.sqrt(sxx*syy),3)} = {f(r,4)}.', 2, T['corr'], extra=[sxy / (sxx * syy), sxy / sxx, r * r, -r], d=4, lo=-1.0, hi=1.0)
    for r in (0.3, 0.5, 0.6, 0.7, 0.8, 0.9, -0.4, -0.6, -0.8, -0.95):
        nump(B, rng, f'Hệ số tương quan r = {fg(r)}. Hệ số xác định r² bằng', r * r, f'r² = {f(r*r,4)} (tỉ lệ biến thiên của y được giải thích bởi x).', 1, T['corr'], extra=[abs(r), 2 * r, 1 - r * r, math.sqrt(abs(r))], d=4, lo=0.0, hi=1.0)
    for _ in range(12):   # r từ hệ số góc
        b = rng.choice([0.5, 1.2, -0.8, 2.0, -1.5]); sx = rng.choice([2, 3, 4]); sy = rng.choice([4, 5, 8, 10]); r = b * sx / sy
        if abs(r) >= 1: continue
        nump(B, rng, f'Hồi quy y theo x có hệ số góc b = {fg(b)}; s_x = {sx}, s_y = {sy}. Hệ số tương quan r = b·s_x/s_y bằng', r, f'r = {fg(b)}·{sx}/{sy} = {f(r,4)}.', 3, T['corr'], extra=[b * sy / sx, b, b * sx * sy], d=4, lo=-1.0, hi=1.0)
    for _ in range(18):   # số liệu thô
        n = rng.choice([5, 6]); x = sorted(rng.sample(range(1, 15), n)); y = [round(2 * xi + rng.uniform(-4, 4), 1) for xi in x]
        b, a = np.polyfit(x, y, 1); r = float(np.corrcoef(x, y)[0, 1])
        nump(B, rng, f'Dữ liệu (x; y): {", ".join(f"({u}; {v})" for u,v in zip(x,y))}. Hệ số góc b của hồi quy y theo x là', float(b), f'b = S_xy/S_xx = {f(float(b),4)} (tính bằng NumPy, đối chiếu công thức).', 3, T['reg'], extra=[float(a), r, float(np.polyfit(y, x, 1)[0])], d=3)
        nump(B, rng, f'Dữ liệu (x; y): {", ".join(f"({u}; {v})" for u,v in zip(x,y))}. Hệ số tương quan mẫu r là', r, f'r = {f(r,4)} (dương: y tăng theo x).', 3, T['corr'], extra=[float(b), r * r, -r], d=3, lo=-1.0, hi=1.0)
    for _ in range(12):   # đổi đơn vị
        b = rng.choice([0.5, 1.5, 2, 3]); k = rng.choice([10, 100, 1000, 0.1])
        nump(B, rng, f'Hồi quy y theo x có hệ số góc b = {fg(b)}. Nếu đổi y sang đơn vị nhỏ hơn k = {fg(k)} lần (y′ = {fg(k)}·y) thì hệ số góc mới bằng', b * k, f'b′ = k·b = {fg(k)}·{fg(b)} = {fg(b*k)} (r không đổi).', 3, T['reg'], extra=[b / k, b, b + k], d=4)
    for _ in range(12):   # kiểm định r
        n = rng.choice([10, 12, 15, 20, 25]); r = rng.choice([0.45, 0.6, 0.7, 0.8, -0.55]); t0 = r * math.sqrt(n - 2) / math.sqrt(1 - r * r)
        nump(B, rng, f'r = {fg(r)}, n = {n}. Thống kê T = r√(n − 2)/√(1 − r²) bằng', t0, f'T = {fg(r)}·√{n-2}/√(1 − {fg(r*r)}) = {f(t0,3)}; so với t_{{0.025}}({n-2}) = {f(st.t.ppf(0.975,n-2),3)}.', 3, T['test'], extra=[r * math.sqrt(n) / math.sqrt(1 - r * r), r * math.sqrt(n - 2), r / math.sqrt(1 - r * r)], d=3)
    for s, ok, bad in [('Hệ số tương quan r luôn nằm trong', '[−1; 1]', ['[0; 1]', '(−∞; +∞)', '[0; 100]']),
                       ('r = 0 cho biết', 'không có quan hệ tuyến tính (có thể có quan hệ phi tuyến)', ['x và y độc lập chắc chắn', 'đường thẳng nằm ngang cắt gốc', 'y = 0']),
                       ('Hệ số góc b và r luôn', 'cùng dấu', ['trái dấu', 'bằng nhau', 'không liên quan']),
                       ('Đường hồi quy mẫu luôn đi qua điểm', '(x̄, ȳ)', ['(0, 0)', '(x̄, 0)', '(0, ȳ)']),
                       ('Tổng các phần dư của hồi quy bình phương nhỏ nhất bằng', '0', ['1', 'n', 'S_yy']),
                       ('Tương quan mạnh giữa x và y', 'không chứng minh quan hệ nhân quả', ['chứng minh x gây ra y', 'chứng minh y gây ra x', 'luôn cho r = 1']),
                       ('Ngoại suy ngoài miền dữ liệu x thường', 'kém tin cậy', ['luôn chính xác', 'cho sai số bằng 0', 'bắt buộc dùng']),
                       ('Phương pháp bình phương nhỏ nhất chọn a, b để', 'Σ(yᵢ − a − bxᵢ)² nhỏ nhất', ['Σ|yᵢ − a − bxᵢ| lớn nhất', 'Σ xᵢyᵢ nhỏ nhất', 'r lớn nhất'])]:
        txt(B, s, ok, bad, 'Kiến thức §4.1–4.2.', 1, T['theory'])
