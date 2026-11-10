"""Đợt mở rộng ngân hàng câu hỏi (nhãn bo_sung) cho M8, M10, M11. Đáp án tính bằng SciPy."""
import math, random, statistics as stt
from scipy import stats as st
from qb import f, fg
from ext_more_a import nump, inte, txt, tp
U = lambda a: st.norm.ppf(1 - a)
Tq = lambda a, d: st.t.ppf(1 - a, d)
def pair(c, e): return f'({f(c - e, 3)}; {f(c + e, 3)})'

def build(mid, B):
    fn = globals().get('b_' + mid)
    if fn: fn(B, random.Random(7200 + int(mid[1:])), tp(mid))

# ───────────── M8
def b_m08(B, rng, T):
    for a in (0.01, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.15, 0.2, 0.22, 0.25):
        nump(B, rng, f'Giá trị tới hạn U_α (Φ(U_α) = 1 − α) với α = {fg(a*100)}% xấp xỉ', U(a), f'Φ(U) = {f(1-a,3)} ⇒ U ≈ {f(U(a),3)}.', 1, T['theory'], extra=[U(a / 2), -U(a), U(2 * a)], d=3)
    for df, a in [(5, 0.05), (9, 0.025), (14, 0.05), (18, 0.1), (20, 0.025), (24, 0.05), (29, 0.01), (10, 0.05), (12, 0.1), (16, 0.025), (30, 0.05), (40, 0.025), (8, 0.05), (15, 0.01), (22, 0.025), (35, 0.05), (45, 0.1), (60, 0.025)]:
        nump(B, rng, f'Giá trị tới hạn t_α với α = {fg(a*100)}% của phân bố Student {df} bậc tự do (F(t_α) = 1 − α) xấp xỉ', Tq(a, df), f'Tra bảng/SciPy: t_{{{fg(a)}}}({df}) = {f(Tq(a,df),3)} (lớn hơn U_α = {f(U(a),3)}).', 2, T['theory'], extra=[U(a), Tq(a, df - 1), Tq(a / 2, df), Tq(a, df + 3)], d=3)
    for _ in range(14):   # tìm tâm và sai số từ khoảng
        lo = round(rng.uniform(10, 60), 2); w = round(rng.uniform(1, 6), 2); hi = round(lo + 2 * w, 2); c = (lo + hi) / 2
        nump(B, rng, f'Khoảng tin cậy cho μ là ({fg(lo)}; {fg(hi)}). Trung bình mẫu x̄ bằng', c, f'x̄ = (cận dưới + cận trên)/2 = {f(c,3)}; sai số e = {f(w,3)}.', 1, T['z'], extra=[w, hi - lo, lo], d=3)
        nump(B, rng, f'Khoảng tin cậy cho μ là ({fg(lo)}; {fg(hi)}). Sai số tối đa (nửa độ rộng) e bằng', w, f'e = (cận trên − cận dưới)/2 = {f(w,3)}.', 1, T['z'], extra=[2 * w, c, lo], d=3)
    for _ in range(12):   # tìm độ tin cậy từ sai số
        sg = rng.choice([4, 5, 8, 10]); n = rng.choice([25, 36, 49, 64, 100]); z = rng.choice([1.0, 1.28, 1.645, 1.96, 2.33, 2.576]); e = z * sg / math.sqrt(n)
        conf = 2 * st.norm.cdf(z) - 1
        nump(B, rng, f'σ = {sg}, n = {n}, sai số của khoảng tin cậy cho μ là e = {f(e,3)}. Độ tin cậy tương ứng là', conf, f'U = e√n/σ = {f(z,3)} ⇒ γ = 2Φ({f(z,3)}) − 1 = {f(conf,4)}.', 3, T['z'], extra=[st.norm.cdf(z), 1 - conf, 1 - 2 * (1 - st.norm.cdf(z)) / 2 - 0.02], d=4, lo=0.0, hi=1.0)
    for _ in range(12):   # cận trên một phía
        n = rng.choice([16, 25, 36, 49, 100]); sg = rng.choice([3, 5, 8, 12]); xb = rng.choice([30, 45.5, 80, 120]); g = rng.choice([0.9, 0.95, 0.99]); b = xb + U(1 - g) * sg / math.sqrt(n)
        nump(B, rng, f'x̄ = {fg(xb)}, σ = {sg}, n = {n}. Cận trên một phía với độ tin cậy {int(g*100)}% cho μ (dùng U_α, α = {fg(1-g)}) là', b, f'x̄ + U_{{{fg(1-g)}}}·σ/√n = {fg(xb)} + {f(U(1-g),3)}·{sg}/{f(math.sqrt(n),2)} = {f(b,3)}.', 3, T['z'], extra=[xb + U((1 - g) / 2) * sg / math.sqrt(n), xb + U(1 - g) * sg, xb - U(1 - g) * sg / math.sqrt(n)], d=3)
    for _ in range(12):   # CI từ dữ liệu thô (σ chưa biết)
        d = [round(rng.uniform(20, 40), 1) for _ in range(rng.choice([6, 7, 8]))]; n = len(d); xb = stt.mean(d); s = stt.stdev(d); g = rng.choice([0.9, 0.95]); e = Tq((1 - g) / 2, n - 1) * s / math.sqrt(n)
        B.mcq(f'Mẫu: {"; ".join(map(str,d))} (tổng thể chuẩn, σ chưa biết). Khoảng tin cậy {int(g*100)}% cho μ là', pair(xb, e),
              [pair(xb, U((1 - g) / 2) * s / math.sqrt(n)), pair(xb, Tq((1 - g) / 2, n) * s / math.sqrt(n)), pair(xb, Tq((1 - g) / 2, n - 1) * s)], f'x̄ = {f(xb,3)}, s = {f(s,3)}, t_{{{fg((1-g)/2)}}}({n-1}) = {f(Tq((1-g)/2,n-1),3)}; e = t·s/√n = {f(e,3)}.', 3, T['t'], 'Bổ sung: họ bài tham số hóa theo dạng đề (đáp án tự tính bằng chương trình)', 'bo_sung')
    for _ in range(10):   # cỡ mẫu theo tỷ lệ với p đã biết
        p = rng.choice([0.2, 0.3, 0.4, 0.6, 0.8]); e = rng.choice([0.02, 0.03, 0.04, 0.05]); g = rng.choice([0.9, 0.95, 0.99]); z = U((1 - g) / 2); n = math.ceil(z * z * p * (1 - p) / e ** 2)
        inte(B, f'Cần ước lượng tỷ lệ p (biết sơ bộ p ≈ {fg(p)}) với sai số không quá {fg(e)}, độ tin cậy {int(g*100)}%. Cỡ mẫu tối thiểu là', n, [math.ceil(z * z * 0.25 / e ** 2), n // 2, n + 25, math.ceil(z * p * (1 - p) / e)], f'n ≥ z²p(1 − p)/e² = {f(z,3)}²·{fg(p)}·{fg(1-p)}/{fg(e)}² = {f(z*z*p*(1-p)/e**2,2)} ⇒ {n}.', 3, T['n'])
    for _ in range(8):    # khoảng tin cậy σ² (χ²)
        n = rng.choice([10, 15, 20, 25]); s2 = rng.choice([4, 9, 16, 2.5]); g = 0.95; lo = (n - 1) * s2 / st.chi2.ppf(1 - (1 - g) / 2, n - 1); hi = (n - 1) * s2 / st.chi2.ppf((1 - g) / 2, n - 1)
        B.mcq(f'Mẫu chuẩn cỡ n = {n} có s² = {fg(s2)}. Khoảng tin cậy 95% cho σ² là', f'({f(lo,3)}; {f(hi,3)})',
              [f'({f((n-1)*s2/st.chi2.ppf(1-0.05/2,n),3)}; {f((n-1)*s2/st.chi2.ppf(0.05/2,n),3)})', f'({f(s2-1.96*s2/math.sqrt(n),3)}; {f(s2+1.96*s2/math.sqrt(n),3)})', f'({f(n*s2/st.chi2.ppf(0.975,n-1),3)}; {f(n*s2/st.chi2.ppf(0.025,n-1),3)})'],
              f'(n − 1)s²/χ²_{{0.025}}({n-1}) và (n − 1)s²/χ²_{{0.975}}({n-1}): cận dưới chia cho χ² lớn.', 3, T['var'], 'Bổ sung: họ bài tham số hóa theo dạng đề (đáp án tự tính bằng chương trình)', 'bo_sung')
    for s, ok, bad in [('Độ tin cậy 99% so với 95% (cùng mẫu) cho khoảng', 'rộng hơn', ['hẹp hơn', 'bằng nhau', 'lệch sang trái']),
                       ('Giá trị tới hạn t_{α/2}(n − 1) khi n tăng dần', 'giảm dần về U_{α/2}', ['tăng dần', 'không đổi', 'bằng 0']),
                       ('Sai số của khoảng tin cậy cho μ (σ biết) tỉ lệ với', 'σ/√n', ['σ·n', 'n/σ', 'σ²']),
                       ('Khoảng tin cậy hai phía 90% có mức tới hạn dùng là', 'U_{0.05} ≈ 1.645', ['U_{0.10} ≈ 1.282', 'U_{0.025} ≈ 1.96', 'U_{0.01} ≈ 2.326']),
                       ('Câu “giá trị tới hạn U_α với α = 7%” theo giáo trình có nghĩa Φ(U_α) bằng', '0.93', ['0.07', '0.965', '0.035']),
                       ('Câu “giá trị tới hạn t_α” theo giáo trình: F(t_α) bằng', '1 − α', ['α', '1 − α/2', 'α/2']),
                       ('Để thu hẹp khoảng tin cậy mà không đổi độ tin cậy ta cần', 'tăng cỡ mẫu', ['giảm cỡ mẫu', 'tăng σ', 'giảm n và tăng σ']),
                       ('Nếu σ chưa biết và n nhỏ, tổng thể chuẩn, khoảng tin cậy cho μ dùng', 'phân phối Student n − 1 bậc tự do', ['chuẩn tắc', 'χ² n bậc tự do', 'Student n bậc tự do'])]:
        txt(B, s, ok, bad, 'Kiến thức §2.3.', 1, T['theory'])

# ───────────── M10
def b_m10(B, rng, T):
    for _ in range(14):   # ngưỡng bác bỏ x̄
        mu0 = rng.choice([50, 100, 20, 8]); sg = rng.choice([4, 6, 10, 15]); n = rng.choice([16, 25, 36, 64]); a = rng.choice([0.01, 0.05, 0.1])
        c = mu0 + U(a) * sg / math.sqrt(n)
        nump(B, rng, f'H₀: μ = {mu0}, H₁: μ > {mu0}; σ = {sg}, n = {n}, α = {fg(a)}. Bác bỏ H₀ khi x̄ > c với c bằng', c, f'c = μ₀ + U_α·σ/√n = {mu0} + {f(U(a),3)}·{sg}/{f(math.sqrt(n),2)} = {f(c,3)}.', 3, T['dec'], extra=[mu0 + U(a / 2) * sg / math.sqrt(n), mu0 + U(a) * sg, mu0 - U(a) * sg / math.sqrt(n)], d=3)
    for _ in range(14):   # p-value z
        z = round(rng.uniform(0.5, 3.0), 2); kind = rng.choice(['phải', 'trái', 'hai phía'])
        v = {'phải': 1 - st.norm.cdf(z), 'trái': st.norm.cdf(-z), 'hai phía': 2 * (1 - st.norm.cdf(z))}[kind]
        zz = z if kind != 'trái' else -z
        nump(B, rng, f'Thống kê kiểm định U = {fg(zz)}. Giá trị p của kiểm định {kind} là', v, f'{"P(U > z)" if kind=="phải" else "P(U < z)" if kind=="trái" else "2·P(U > |z|)"} = {f(v,4)}.', 2, T['dec'], extra=[1 - v, st.norm.cdf(z), 2 * v, v / 2], d=4, lo=0.0, hi=1.0)
    for _ in range(14):   # sức mạnh kiểm định, sai lầm loại II
        mu0 = rng.choice([50, 100]); mu1 = mu0 + rng.choice([2, 3, 4, 5]); sg = rng.choice([6, 8, 10]); n = rng.choice([25, 36, 49, 64]); a = rng.choice([0.05, 0.01]); se = sg / math.sqrt(n)
        c = mu0 + U(a) * se; beta = st.norm.cdf((c - mu1) / se)
        nump(B, rng, f'H₀: μ = {mu0} so với H₁: μ > {mu0}; σ = {sg}, n = {n}, α = {fg(a)}. Xác suất sai lầm loại II β khi μ thực là {mu1} bằng', beta, f'c = {f(c,3)}; β = P(x̄ ≤ c | μ = {mu1}) = Φ(({f(c,3)} − {mu1})/{f(se,3)}) = {f(beta,4)}.', 3, T['hyp'], extra=[1 - beta, st.norm.cdf((c - mu0) / se), a], d=4, lo=0.0, hi=1.0)
        nump(B, rng, f'H₀: μ = {mu0} so với H₁: μ > {mu0}; σ = {sg}, n = {n}, α = {fg(a)}. Sức mạnh (power) của kiểm định khi μ thực là {mu1} bằng', 1 - beta, f'Power = 1 − β = 1 − {f(beta,4)} = {f(1-beta,4)}.', 3, T['hyp'], extra=[beta, a, 1 - a], d=4, lo=0.0, hi=1.0)
    for _ in range(14):   # quyết định t
        n = rng.choice([8, 10, 12, 16, 20]); mu0 = rng.choice([30, 50, 72]); s = rng.choice([3, 5, 8]); xb = mu0 + rng.choice([-1, 1, 2, 3]) * s / math.sqrt(n) * rng.choice([0.5, 1.2, 2.0, 2.8])
        T0 = (xb - mu0) / (s / math.sqrt(n)); a = 0.05; crit = Tq(a / 2, n - 1); rej = abs(T0) > crit
        txt(B, f'H₀: μ = {mu0}, H₁: μ ≠ {mu0}; n = {n}, x̄ = {f(xb,3)}, s = {s}, α = 0.05. Kết luận là', 'bác bỏ H₀' if rej else 'chưa đủ cơ sở bác bỏ H₀',
            ['chấp nhận H₁ chắc chắn' if rej else 'bác bỏ H₀', 'không thể kết luận vì n nhỏ', 'chấp nhận H₁'] if rej else ['bác bỏ H₀', 'chứng minh H₀ đúng', 'chấp nhận H₁'],
            f'T = {f(T0,3)}; t_{{0.025}}({n-1}) = {f(crit,3)}; |T| {">" if rej else "≤"} t ⇒ {"bác bỏ" if rej else "chưa bác bỏ"} H₀.', 3, T['dec'])
    for _ in range(12):   # kiểm định tỷ lệ
        n = rng.choice([100, 200, 400, 500]); p0 = rng.choice([0.3, 0.4, 0.5, 0.6]); k = round(n * (p0 + rng.choice([-0.06, 0.05, 0.08, -0.03]))); ph = k / n; z = (ph - p0) / math.sqrt(p0 * (1 - p0) / n)
        nump(B, rng, f'H₀: p = {fg(p0)}. Mẫu n = {n} có {k} thành công. Thống kê U = (p̂ − p₀)/√(p₀(1 − p₀)/n) bằng', z, f'p̂ = {f(ph,4)}; U = {f(z,3)}.', 2, T['p'], extra=[(ph - p0) / math.sqrt(ph * (1 - ph) / n), (ph - p0) * math.sqrt(n), (ph - p0) / (p0 * (1 - p0) / n)], d=3)
    for s, ok, bad in [('Sai lầm loại I là', 'bác bỏ H₀ khi H₀ đúng', ['chấp nhận H₀ khi H₀ sai', 'bác bỏ H₀ khi H₀ sai', 'chấp nhận H₁ khi H₁ đúng']),
                       ('Sai lầm loại II là', 'không bác bỏ H₀ khi H₀ sai', ['bác bỏ H₀ khi H₀ đúng', 'bác bỏ H₀ khi H₀ sai', 'chấp nhận H₁ khi H₀ đúng']),
                       ('Mức ý nghĩa α bằng', 'xác suất sai lầm loại I', ['xác suất sai lầm loại II', 'sức mạnh kiểm định', 'xác suất H₀ đúng']),
                       ('Khi giảm α (giữ n) thì xác suất sai lầm loại II', 'tăng', ['giảm', 'không đổi', 'bằng 0']),
                       ('Tăng cỡ mẫu n (giữ α) thì sức mạnh kiểm định', 'tăng', ['giảm', 'không đổi', 'bằng α']),
                       ('Giá trị p nhỏ hơn α nghĩa là', 'bác bỏ H₀ ở mức α', ['chấp nhận H₀', 'H₀ chắc chắn đúng', 'cần thêm dữ liệu chắc chắn']),
                       ('Kiểm định hai phía dùng giá trị tới hạn', 'U_{α/2} hoặc t_{α/2}', ['U_α', 'U_{2α}', 'chỉ t_α'])]:
        txt(B, s, ok, bad, 'Kiến thức §3.1–3.2.', 1, T['theory'])

# ───────────── M11
def b_m11(B, rng, T):
    SRC = 'Bổ sung: họ bài tham số hóa theo dạng đề (đáp án tự tính bằng chương trình)'
    for df, a in [(4, 0.05), (9, 0.05), (14, 0.025), (19, 0.05), (24, 0.1), (29, 0.025), (10, 0.01), (15, 0.05), (7, 0.975), (12, 0.95), (20, 0.9), (25, 0.975)]:
        v = st.chi2.ppf(1 - a, df)
        nump(B, rng, f'Giá trị tới hạn χ²_{{{fg(a)}}}({df}) (P(χ² > c) = {fg(a)}) xấp xỉ', v, f'SciPy: {f(v,3)}.', 2, T['chi'], extra=[st.chi2.ppf(a, df), st.chi2.ppf(1 - a, df + 1), st.chi2.ppf(1 - a / 2, df), df], d=3, lo=0.0)
    for n1, n2, a in [(8, 10, 0.05), (10, 12, 0.05), (15, 20, 0.05), (6, 9, 0.05), (12, 8, 0.05), (20, 25, 0.05), (9, 9, 0.025), (16, 11, 0.05), (7, 14, 0.1), (10, 10, 0.05), (13, 17, 0.025), (5, 8, 0.05)]:
        v = st.f.ppf(1 - a, n1 - 1, n2 - 1)
        nump(B, rng, f'Giá trị tới hạn F_{{{fg(a)}}}({n1-1}; {n2-1}) (P(F > c) = {fg(a)}) xấp xỉ', v, f'SciPy: {f(v,3)}.', 3, T['ftest'], extra=[st.f.ppf(1 - a, n2 - 1, n1 - 1), st.f.ppf(1 - a, n1, n2), 1 / v], d=3, lo=0.0)
    for _ in range(14):   # F quan sát và quyết định
        n1, n2 = rng.choice([8, 10, 12, 15]), rng.choice([9, 11, 14, 20]); s1, s2 = rng.choice([3.1, 4.2, 5.0, 6.4]), rng.choice([2.2, 2.9, 3.5, 4.0]); F0 = s1 ** 2 / s2 ** 2
        nump(B, rng, f'Hai mẫu chuẩn: n₁ = {n1}, s₁ = {s1}; n₂ = {n2}, s₂ = {s2}. Thống kê F = s₁²/s₂² bằng', F0, f'F = {s1}²/{s2}² = {f(F0,3)}.', 2, T['ftest'], extra=[s1 / s2, s2 ** 2 / s1 ** 2, s1 ** 2 - s2 ** 2], d=3, lo=0.0)
    for _ in range(14):   # phương sai gộp
        n1, n2 = rng.choice([8, 10, 12, 15]), rng.choice([9, 11, 14, 20]); s1, s2 = rng.choice([3.1, 4.2, 5.0]), rng.choice([2.2, 2.9, 3.5]); sp2 = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
        nump(B, rng, f'n₁ = {n1}, s₁ = {s1}; n₂ = {n2}, s₂ = {s2}. Phương sai gộp s_p² bằng', sp2, f's_p² = [({n1}−1)·{s1}² + ({n2}−1)·{s2}²]/({n1}+{n2}−2) = {f(sp2,3)}.', 2, T['two'], extra=[(s1 ** 2 + s2 ** 2) / 2, ((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2), ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2)], d=3, lo=0.0)
    for _ in range(14):   # t gộp
        n1, n2 = rng.choice([8, 10, 12, 15]), rng.choice([9, 11, 14, 18]); m1, m2 = rng.choice([52, 60, 75]), rng.choice([48, 55, 70]); s1, s2 = rng.choice([4, 5, 6]), rng.choice([3, 4.5, 5.5])
        sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)); t0 = (m1 - m2) / (sp * math.sqrt(1 / n1 + 1 / n2))
        nump(B, rng, f'Hai nhóm: n₁ = {n1}, x̄₁ = {m1}, s₁ = {s1}; n₂ = {n2}, x̄₂ = {m2}, s₂ = {s2} (cùng σ²). Thống kê t gộp bằng', t0, f's_p = {f(sp,3)}; t = (x̄₁ − x̄₂)/(s_p√(1/n₁ + 1/n₂)) = {f(t0,3)}.', 3, T['two'], extra=[(m1 - m2) / (sp / math.sqrt(n1)), (m1 - m2) / math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2) + 0.2, (m1 - m2) / sp], d=3)
    for _ in range(12):   # ghép cặp
        n = rng.choice([8, 10, 12, 16]); dbar = rng.choice([1.2, 2.5, 3.1, 4.0]); sd = rng.choice([2, 3.2, 4.5]); t0 = dbar / (sd / math.sqrt(n))
        nump(B, rng, f'Mẫu ghép cặp n = {n} có trung bình hiệu d̄ = {dbar}, độ lệch chuẩn hiệu s_d = {sd}. Thống kê t = d̄/(s_d/√n) bằng', t0, f't = {dbar}/({sd}/{f(math.sqrt(n),3)}) = {f(t0,3)}; bậc tự do n − 1 = {n-1}.', 2, T['two'], extra=[dbar / sd, dbar * math.sqrt(n), dbar / (sd / n)], d=3)
    for _ in range(14):   # hai tỷ lệ
        n1, n2 = rng.choice([100, 150, 200]), rng.choice([120, 180, 250]); k1 = round(n1 * rng.choice([0.4, 0.5, 0.6])); k2 = round(n2 * rng.choice([0.3, 0.42, 0.5])); p1, p2 = k1 / n1, k2 / n2; pp = (k1 + k2) / (n1 + n2)
        z = (p1 - p2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
        nump(B, rng, f'Mẫu 1: {k1}/{n1} thành công; mẫu 2: {k2}/{n2}. H₀: p₁ = p₂. Thống kê U (dùng tỷ lệ gộp) bằng', z, f'p̂ = {f(pp,4)}; U = {f(z,3)}.', 3, T['prop'], extra=[(p1 - p2) / math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2), p1 - p2, (p1 - p2) / math.sqrt(pp * (1 - pp))], d=3)
    for _ in range(14):   # quyết định χ² phương sai
        n = rng.choice([10, 15, 20, 25]); s02 = rng.choice([4, 9, 16]); s2 = s02 * rng.choice([0.4, 0.6, 1.5, 2.0, 2.4]); a = 0.05; chi = (n - 1) * s2 / s02; side = rng.choice(['>', '<'])
        crit = st.chi2.ppf(1 - a, n - 1) if side == '>' else st.chi2.ppf(a, n - 1); rej = chi > crit if side == '>' else chi < crit
        txt(B, f'H₀: σ² = {s02}, H₁: σ² {side} {s02}; n = {n}, s² = {fg(s2)}, α = 0.05. Kết luận là', 'bác bỏ H₀' if rej else 'chưa đủ cơ sở bác bỏ H₀', ['chấp nhận H₁ chắc chắn' if rej else 'bác bỏ H₀', 'chứng minh H₀ đúng' if not rej else 'chưa đủ dữ kiện', 'chỉ kết luận khi n > 30'],
            f'χ² = (n−1)s²/σ₀² = {f(chi,3)}; giá trị tới hạn {f(crit,3)} ⇒ {"bác bỏ" if rej else "chưa bác bỏ"} H₀.', 3, T['var'])
    for s, ok, bad in [('Thống kê χ² = (n − 1)S²/σ₀² có bậc tự do', 'n − 1', ['n', 'n − 2', '2(n − 1)']),
                       ('Phân phối F với (k₁; k₂) bậc tự do và 1/F có quan hệ', 'F(k₂; k₁)', ['F(k₁; k₁)', 'chuẩn', 't(k₂)']),
                       ('Kiểm định t gộp cần điều kiện', 'hai tổng thể chuẩn, cùng phương sai, mẫu độc lập', ['chỉ cần cùng cỡ mẫu', 'chỉ cần σ đã biết', 'mẫu phụ thuộc nhau']),
                       ('Mẫu trước–sau trên cùng đối tượng nên dùng', 't ghép cặp', ['t gộp độc lập', 'F', 'χ² phù hợp']),
                       ('So sánh hai tỷ lệ dưới H₀ dùng ước lượng gộp', 'p̂ = (k₁ + k₂)/(n₁ + n₂)', ['p̂ = k₁/n₁', 'p̂ = (p̂₁ + p̂₂)/2 luôn', 'p̂ = k₁k₂']),
                       ('Kiểm định F so sánh phương sai thường đặt phương sai lớn hơn ở', 'tử số', ['mẫu số', 'cả hai', 'không quan trọng chắc chắn'])]:
        txt(B, s, ok, bad, 'Kiến thức §3.3–3.4.', 1, T['theory'])
