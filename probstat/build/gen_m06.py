"""Module 6 — biến thể tham số (bo_sung): nhị thức, Poisson, chuẩn, xấp xỉ."""
import math, random
from math import comb
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
from orig_m06 import TOP, Phi, PhiI
SRC = 'Bổ sung: biến thể tham số của dạng bài §1.10 / PS 24.7–24.8 và đề thi (đáp án tính bằng SciPy)'
def build(B):
    rng = random.Random(1606)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    # nhị thức
    for n, p, kx in [(10, 0.3, 4), (8, 0.5, 5), (12, 0.2, 2), (20, 0.1, 3), (6, 0.6, 4), (15, 0.25, 5), (10, 0.5, 7), (9, 0.4, 3)]:
        v = st.binom.pmf(kx, n, p); cdf = st.binom.cdf(kx, n, p)
        P(f'X ~ B(n = {n}, p = {p}). P(X = {kx}) bằng', v, f'C({n},{kx})·{p}^{kx}·{1-p:.2f}^{n-kx} = {comb(n,kx)}·{p**kx:.6f}·{(1-p)**(n-kx):.6f} = {f(v,4)}.', 1 if n <= 10 else 2, TOP['binom'], SRC, extra=[cdf, n * p / n, st.binom.pmf(kx + 1, n, p)], d=4)
        P(f'X ~ B(n = {n}, p = {p}). P(X ≤ {kx}) bằng', cdf, f'Cộng P(X = 0..{kx}) = {f(cdf,4)}.', 2, TOP['binom'], SRC, extra=[v, 1 - cdf, st.binom.cdf(kx - 1, n, p)], d=4)
        B.mcq(f'X ~ B(n = {n}, p = {p}). Kỳ vọng và phương sai là', f'{fg(n*p)} và {fg(n*p*(1-p))}', [f'{fg(n*p)} và {fg(n*p)}', f'{fg(n*(1-p))} và {fg(n*p*(1-p))}', f'{fg(p)} và {fg(p*(1-p))}', f'{fg(n*p)} và {fg(n*p*(1-p)+1)}'], f'μ = np = {fg(n*p)}; σ² = np(1 − p) = {fg(n*p*(1-p))}.', 1, TOP['binom'], SRC, 'bo_sung')
    # Poisson
    for mu, kx in [(2, 1), (3, 4), (0.5, 0), (4, 6), (1.5, 2), (6, 8), (2.5, 3)]:
        v = st.poisson.pmf(kx, mu); c = st.poisson.cdf(kx, mu)
        P(f'X ~ Poisson(μ = {mu}). P(X = {kx}) bằng', v, f'e^(−{mu})·{mu}^{kx}/{kx}! = {f(v,4)}.', 1, TOP['pois'], SRC, extra=[c, st.poisson.pmf(kx + 1, mu), math.exp(-mu)], d=4)
        P(f'X ~ Poisson(μ = {mu}). P(X ≥ {kx + 1}) bằng', 1 - c, f'1 − P(X ≤ {kx}) = 1 − {f(c,4)} = {f(1-c,4)}.', 2, TOP['pois'], SRC, extra=[c, v, st.poisson.pmf(kx + 1, mu)], d=4)
    # chuẩn: xác suất
    for mu, sg, a, b in [(50, 5, 45, 60), (100, 15, 85, 130), (20, 2, 18, 21), (0, 1, -1, 2), (75, 8, 70, 90), (12, 3, 9, 15), (170, 6, 160, 176), (5.5, 0.4, 5, 6)]:
        v = Phi((b - mu) / sg) - Phi((a - mu) / sg)
        P(f'X ~ N(μ = {mu}; σ = {sg}). P({a} < X < {b}) bằng', v, f'Φ(({b} − {mu})/{sg}) − Φ(({a} − {mu})/{sg}) = Φ({(b-mu)/sg:.2f}) − Φ({(a-mu)/sg:.2f}) = {f(v,4)}.', 2, TOP['normp'], SRC, extra=[Phi((b - mu) / sg), 1 - v, Phi((b - mu) / sg) + Phi((a - mu) / sg)], d=4)
        P(f'X ~ N(μ = {mu}; σ = {sg}). P(X > {b}) bằng', 1 - Phi((b - mu) / sg), f'z = {(b-mu)/sg:.2f} ⇒ 1 − Φ({(b-mu)/sg:.2f}) = {f(1-Phi((b-mu)/sg),4)}.', 1, TOP['normp'], SRC, extra=[Phi((b - mu) / sg), 0.5, 1 - Phi(a)], d=4)
    # chuẩn: phân vị
    for mu, sg, pr in [(50, 5, 0.95), (100, 15, 0.9), (20, 2, 0.99), (75, 8, 0.975), (12, 3, 0.8), (170, 6, 0.1)]:
        c = mu + sg * PhiI(pr)
        P(f'X ~ N(μ = {mu}; σ = {sg}). Tìm c với P(X ≤ c) = {pr}.', c, f'z = {PhiI(pr):.3f} ⇒ c = {mu} + {PhiI(pr):.3f}·{sg} = {f(c,3)}.', 2, TOP['normq'], SRC, extra=[mu + sg * PhiI(1 - pr), mu + PhiI(pr), mu + sg * 1.96], d=3)
        k = sg * PhiI((1 + pr) / 2)
        P(f'X ~ N(μ = {mu}; σ = {sg}). Tìm k với P(μ − k < X < μ + k) = {pr}.', k, f'2Φ(k/σ) − 1 = {pr} ⇒ k/σ = z_{{{(1+pr)/2:.4f}}} = {PhiI((1+pr)/2):.3f} ⇒ k = {f(k,3)}.', 3, TOP['normq'], SRC, extra=[sg * PhiI(pr), sg * 1.96, k / 2], d=3)
    # xấp xỉ
    for n, p, a, b in [(100, 0.5, 45, 60), (400, 0.8, 300, 340), (200, 0.3, 50, 70), (150, 0.4, 50, 70), (1000, 0.5, 480, 520)]:
        mu = n * p; sg = math.sqrt(n * p * (1 - p)); ap = Phi((b - mu + 0.5) / sg) - Phi((a - mu - 0.5) / sg); ex = st.binom.cdf(b, n, p) - st.binom.cdf(a - 1, n, p)
        P(f'X ~ B({n}; {p}). Dùng xấp xỉ chuẩn có hiệu chỉnh 0.5, P({a} ≤ X ≤ {b}) ≈', ap, f'μ = {fg(mu)}, σ = {sg:.3f}; α = ({a} − {fg(mu)} − 0.5)/{sg:.3f}, β = ({b} − {fg(mu)} + 0.5)/{sg:.3f} ⇒ Φ(β) − Φ(α) = {f(ap,4)} (đúng: {f(ex,4)}).', 3, TOP['approx'], SRC, extra=[Phi((b - mu) / sg) - Phi((a - mu) / sg), ex + 0.02, 1 - ap], d=4)
    for n, p in [(200, 0.01), (500, 0.004), (1000, 0.002), (300, 0.01)]:
        mu = n * p
        P(f'Lô {n} sản phẩm, mỗi sản phẩm lỗi độc lập với p = {p}. Xấp xỉ Poisson (μ = {fg(mu)}), P(X ≤ 1) ≈', st.poisson.cdf(1, mu), f'e^(−{fg(mu)})(1 + {fg(mu)}) = {f(st.poisson.cdf(1,mu),4)} (nhị thức đúng: {f(st.binom.cdf(1,n,p),4)}).', 2, TOP['approx'], SRC, extra=[st.binom.cdf(1, n, p) + 0.03, st.poisson.pmf(1, mu), 1 - st.poisson.cdf(1, mu)], d=4)
    B.mcq('Với X ~ N(μ, σ²), xác suất P(μ − 2σ < X < μ + 2σ) xấp xỉ bằng', '0.9545', ['0.6827', '0.9973', '0.5'], '2Φ(2) − 1 = 0.9545 (quy tắc 68–95–99.7 ở Module 1).', 1, TOP['theory'], SRC, 'bo_sung')
    B.mcq('Giá trị z₀.₉₇₅ (Φ(z) = 0.975) xấp xỉ bằng', '1.960', ['1.645', '2.326', '1.282'], 'Tra bảng A8: z₀.₉₇₅ = 1.960 (dùng cho khoảng tin cậy 95%).', 1, TOP['theory'], SRC, 'bo_sung')
    B.mcq('Giá trị z₀.₉₅ (Φ(z) = 0.95) xấp xỉ bằng', '1.645', ['1.960', '2.326', '1.282'], 'Tra bảng A8: z₀.₉₅ = 1.645 (dùng cho kiểm định một phía mức 5%).', 1, TOP['theory'], SRC, 'bo_sung')
    B.mcq('Giá trị z₀.₉₉ (Φ(z) = 0.99) xấp xỉ bằng', '2.326', ['1.960', '1.645', '2.576'], 'Tra bảng A8: z₀.₉₉ = 2.326 (một phía mức 1%).', 1, TOP['theory'], SRC, 'bo_sung')
