"""Module 5 — biến thể tham số (bo_sung)."""
import math, random
from scipy import integrate, optimize
from qb import f, fg, nd
from qh import pm
from orig_m05 import TOP, dmean, dvar, Q
SRC = 'Bổ sung: biến thể tham số của dạng bài §1.7–1.9 / PS 24.5–24.6 (đáp án tính bằng công thức và tích phân số, đối chiếu giải tích)'
def build(B):
    rng = random.Random(1505)
    def P(*a, **k):
        k.setdefault('hi', None); k.setdefault('origin', 'bo_sung'); return pm(B, rng, *a, **k)
    # 1. bảng phân phối rời rạc ngẫu nhiên
    for t in range(8):
        xs = sorted(rng.sample(range(0, 10), rng.choice([4, 5])))
        w = [rng.randint(1, 9) for _ in xs]; s = sum(w); ps = [round(x / s, 3) for x in w]; ps[-1] = round(1 - sum(ps[:-1]), 3)
        m = dmean(xs, ps); v = dvar(xs, ps); ex2 = sum(x * x * p for x, p in zip(xs, ps))
        tab = ', '.join(f'P(X={x}) = {p}' for x, p in zip(xs, ps))
        P(f'X có bảng phân phối: {tab}. Kỳ vọng E(X) là', m, f'E(X) = Σ xᵢpᵢ = {f(m,4)}.', 1, TOP['mean'], SRC, extra=[ex2, sum(xs) / len(xs), m + 1], d=3)
        P(f'X có bảng phân phối: {tab}. Phương sai Var(X) là', v, f'E(X²) = {f(ex2,4)}; Var(X) = {f(ex2,4)} − {f(m*m,4)} = {f(v,4)}.', 2, TOP['var'], SRC, extra=[ex2, math.sqrt(v), ex2 - m], d=3)
    # 2. tìm hằng số k (rời rạc)
    for n, pw in [(4, 2), (5, 2), (6, 3), (3, 3), (5, 1), (7, 1)]:
        tot = sum(x ** pw for x in range(1, n + 1))
        B.mcq(f'f(x) = k·x^{pw} với x = 1, 2, …, {n} là hàm xác suất. Giá trị k là', f'1/{tot}', [f'1/{tot + 3}', f'1/{n}', f'1/{max(2, tot - 2)}'], f'Σ x^{pw} = {tot} nên k = 1/{tot}.', 1, TOP['pmf'], SRC, 'bo_sung')
    # 3. mật độ đa thức c x^a trên [0, L]
    for a, L in [(1, 2), (2, 3), (3, 2), (1, 4), (2, 2), (3, 3)]:
        c = (a + 1) / L ** (a + 1)
        mu = (a + 1) / (a + 2) * L; ex2 = (a + 1) / (a + 3) * L ** 2; v = ex2 - mu * mu
        d = f'f(x) = c·x^{a} trên [0, {L}]' if a > 1 else f'f(x) = c·x trên [0, {L}]'
        P(f'X có mật độ {d} (0 ở ngoài). Hằng số c là', c, f'∫₀^{L} c·x^{a} dx = c·{L}^{a+1}/{a+1} = 1 ⇒ c = {a+1}/{L**(a+1)} = {f(c,5)}.', 1, TOP['pdf'], SRC, extra=[1 / L, a + 1, 1 / L ** a], d=4)
        P(f'X có mật độ {d} với c chuẩn hóa. Kỳ vọng E(X) là', mu, f'E(X) = ∫ x·c·x^{a} dx = {a+1}/{a+2}·{L} = {f(mu,4)}.', 2, TOP['mean'], SRC, extra=[L / 2, L * (a + 1) / (a + 3), c], d=4)
        P(f'X có mật độ {d} với c chuẩn hóa. Phương sai Var(X) là', v, f'E(X²) = {a+1}/{a+3}·{L}² = {f(ex2,4)}; Var = {f(ex2,4)} − {f(mu*mu,4)} = {f(v,4)}.', 3, TOP['var'], SRC, extra=[ex2, mu, math.sqrt(v)], d=4)
    # 4. mũ
    for lam in [0.5, 2, 0.25, 4, 0.1, 3]:
        t = 1.0 / lam
        P(f'Thời gian chờ T có mật độ f(t) = {lam}·e^(−{lam}t), t ≥ 0. Kỳ vọng E(T) là', 1 / lam, f'Mũ tham số λ = {lam}: E(T) = 1/λ = {f(1/lam,4)}.', 1, TOP['mean'], SRC, extra=[lam, 1 / lam ** 2, lam ** 2], d=4)
        P(f'Thời gian chờ T có mật độ f(t) = {lam}·e^(−{lam}t), t ≥ 0. P(T > {fg(t)}) bằng', math.exp(-1), f'P(T > t) = e^(−λt) = e^(−{lam}·{fg(t)}) = e^(−1) = {f(math.exp(-1),4)}.', 2, TOP['pdf'], SRC, extra=[1 - math.exp(-1), 0.5, math.exp(-2)], d=4)
        P(f'T có mật độ f(t) = {lam}·e^(−{lam}t), t ≥ 0. Trung vị m (P(T ≤ m) = 0.5) là', math.log(2) / lam, f'1 − e^(−{lam}m) = 0.5 ⇒ m = ln 2/{lam} = {f(math.log(2)/lam,4)} (nhỏ hơn kỳ vọng {f(1/lam,4)}).', 3, TOP['quant'], SRC, extra=[1 / lam, math.log(2), 0.5 / lam], d=4)
    # 5. đều
    for a, b in [(0, 4), (2, 8), (-3, 3), (10, 20), (1, 7)]:
        P(f'X đều trên [{a}, {b}]. Phương sai Var(X) là', (b - a) ** 2 / 12, f'(b − a)²/12 = {(b-a)**2}/12 = {f((b-a)**2/12,4)}. Kỳ vọng {(a+b)/2:g}.', 2, TOP['var'], SRC, extra=[(b - a) / 12, (b - a) ** 2 / 4, (a + b) / 2], d=4)
        P(f'X đều trên [{a}, {b}]. P({a + (b-a)//4 if (b-a)%4==0 else a} ≤ X ≤ {a + (b-a)//2 if (b-a)%2==0 else b}) bằng', ((a + (b - a) // 2 if (b - a) % 2 == 0 else b) - (a + (b - a) // 4 if (b - a) % 4 == 0 else a)) / (b - a), 'Xác suất bằng độ dài khoảng chia cho (b − a).', 1, TOP['pdf'], SRC, extra=[0.5, 0.25, 0.75], d=4)
    # 6. biến đổi tuyến tính
    for m0, v0, a, b in [(5, 4, 3, 2), (10, 9, -2, 5), (2, 1, 10, -3), (8, 16, 0.5, 1), (0, 1, 4, 4), (3, 6, -1, 0)]:
        P(f'E(X) = {m0}, Var(X) = {v0}. Với Y = {fg(a)}X {"+" if b >= 0 else "−"} {abs(b)}, E(Y) là', a * m0 + b, f'E(Y) = aE(X) + b = {fg(a)}·{m0} {"+" if b >= 0 else "−"} {abs(b)} = {fg(a*m0+b)}.', 1, TOP['mean'], SRC, extra=[a * m0, m0 + b, a * (m0 + b)], d=2, lo=None)
        P(f'E(X) = {m0}, Var(X) = {v0}. Với Y = {fg(a)}X {"+" if b >= 0 else "−"} {abs(b)}, Var(Y) là', a * a * v0, f'Var(Y) = a²Var(X) = {fg(a*a)}·{v0} = {fg(a*a*v0)} (cộng b không đổi độ phân tán).', 2, TOP['var'], SRC, extra=[a * v0, a * a * v0 + b, a * v0 + b], d=2, lo=None)
    # 7. xác suất từ F
    for a, L in [(2, 4), (1, 3), (3, 5), (1, 5)]:
        Fx = lambda x, a=a, L=L: (x - a) ** 2 / (L - a) ** 2
        P(f'F(x) = (x − {a})²/{(L-a)**2} với {a} ≤ x ≤ {L} (0 khi x < {a}, 1 khi x > {L}). P(X ≤ {a + (L-a)/2:g}) bằng', Fx(a + (L - a) / 2), f'F({a + (L-a)/2:g}) = ({(L-a)/2:g})²/{(L-a)**2} = {f(Fx(a+(L-a)/2),4)}.', 1, TOP['pdf'], SRC, extra=[0.5, 0.75, 0.125], d=4)
        med = a + (L - a) / math.sqrt(2)
        P(f'F(x) = (x − {a})²/{(L-a)**2} với {a} ≤ x ≤ {L}. Trung vị m (F(m) = 0.5) là', med, f'(m − {a})² = {(L-a)**2/2:g} ⇒ m = {a} + {L-a}/√2 = {f(med,4)}.', 3, TOP['quant'], SRC, extra=[(a + L) / 2, a + (L - a) / 2, L - (L - a) / math.sqrt(2)], d=4)
