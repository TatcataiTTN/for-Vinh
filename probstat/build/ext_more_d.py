"""Đợt mở rộng bổ sung (nhãn bo_sung): hoàn thiện M7, M10, M11, M12, M13 lên 300 câu. Đáp án tính bằng code."""
import math, random, statistics as stt
from scipy import stats as st
from qb import f, fg
from ext_more_a import nump, inte, txt, tp
U = lambda a: st.norm.ppf(1 - a)
Tq = lambda a, d: st.t.ppf(1 - a, d)
def build(mid, B):
    fn = globals().get('b_' + mid)
    if fn: fn(B, random.Random(7400 + int(mid[1:])), tp(mid))
def b_m07(B, rng, T):
    for _ in range(10):
        d = [rng.randint(2, 30) for _ in range(rng.choice([5, 6, 7, 8]))]; v = stt.variance(d)
        nump(B, rng, f'Mẫu: {"; ".join(map(str,d))}. Phương sai mẫu s² (chia n − 1) bằng', v, f'x̄ = {f(stt.mean(d),3)}; s² = {f(v,3)}.', 2, T['sample'], extra=[stt.pvariance(d), math.sqrt(v), stt.mean(d)], d=3, lo=0.0)
    for _ in range(10):
        mu = rng.choice([50, 100, 20]); sg = rng.choice([8, 10, 15]); n = rng.choice([16, 25, 36, 64]); c = mu + rng.choice([1, 2, 3]) * sg / math.sqrt(n) * rng.choice([0.5, 1, 1.5]); v = 1 - st.norm.cdf((c - mu) / (sg / math.sqrt(n)))
        nump(B, rng, f'Tổng thể μ = {mu}, σ = {sg}; mẫu n = {n}. P(X̄ > {f(c,3)}) xấp xỉ', v, f'z = ({f(c,3)} − {mu})/({sg}/{f(math.sqrt(n),2)}) = {f((c-mu)/(sg/math.sqrt(n)),3)}; P = {f(v,4)}.', 3, T['sample'], extra=[1 - st.norm.cdf((c - mu) / sg), st.norm.cdf((c - mu) / (sg / math.sqrt(n))), 2 * v], lo=0.0, hi=1.0)
    for n in (5, 8, 10, 12, 20, 25):
        sg2 = rng.choice([4, 9, 16]); v = (n - 1) / n * sg2
        nump(B, rng, f'σ² = {sg2}. Ước lượng σ̂² = Σ(Xᵢ − X̄)²/n có kỳ vọng E(σ̂²) bằng (cỡ mẫu n = {n})', v, f'E = (n − 1)σ²/n = {f(v,3)} (chệch, thấp hơn σ²).', 3, T['point'], extra=[sg2, sg2 * n / (n - 1), sg2 / n], d=3, lo=0.0)
def b_m10(B, rng, T):
    for _ in range(12):
        mu0 = rng.choice([50, 100, 20]); sg = rng.choice([5, 8, 12]); n = rng.choice([16, 25, 36, 49]); xb = mu0 + rng.choice([-3, -1.5, 1.2, 2.5, 4]); z = (xb - mu0) / (sg / math.sqrt(n))
        nump(B, rng, f'H₀: μ = {mu0}; σ = {sg}, n = {n}, x̄ = {fg(xb)}. Thống kê U = (x̄ − μ₀)/(σ/√n) bằng', z, f'U = ({fg(xb)} − {mu0})/({sg}/{f(math.sqrt(n),2)}) = {f(z,3)}.', 1, T['z'], extra=[(xb - mu0) / sg, (xb - mu0) * math.sqrt(n), (xb - mu0) / (sg * math.sqrt(n))], d=3)
    for _ in range(12):
        mu0 = rng.choice([30, 60, 90]); s = rng.choice([4, 6, 9]); n = rng.choice([9, 12, 16, 25]); xb = mu0 + rng.choice([-2.5, 1.5, 3, 4.5]); t0 = (xb - mu0) / (s / math.sqrt(n))
        nump(B, rng, f'H₀: μ = {mu0}; n = {n}, x̄ = {fg(xb)}, s = {s}. Thống kê T = (x̄ − μ₀)/(s/√n) bằng', t0, f'T = {fg(xb-mu0)}/({s}/{f(math.sqrt(n),2)}) = {f(t0,3)}; bậc tự do {n-1}.', 2, T['t'], extra=[(xb - mu0) / s, (xb - mu0) * math.sqrt(n), (xb - mu0) / (s / n)], d=3)
    for _ in range(10):
        sg = rng.choice([4, 6, 10]); d = rng.choice([2, 3, 4, 5]); a = rng.choice([0.05, 0.01]); b = rng.choice([0.1, 0.2]); n = math.ceil(((U(a) + U(b)) * sg / d) ** 2)
        inte(B, f'Kiểm định một phía μ, σ = {sg}. Cần phát hiện chênh lệch {d} với α = {fg(a)}, β = {fg(b)}. Cỡ mẫu tối thiểu n = ((U_α + U_β)σ/δ)² là', n, [math.ceil((U(a) * sg / d) ** 2), n * 2, n // 2 + 1, math.ceil(((U(a) + U(b)) * sg) ** 2 / d)], f'((U_α + U_β)σ/δ)² = (({f(U(a),3)} + {f(U(b),3)})·{sg}/{d})² = {f(((U(a)+U(b))*sg/d)**2,2)} ⇒ {n}.', 3, T['hyp'])
def b_m11(B, rng, T):
    for _ in range(12):
        n1, n2 = rng.choice([8, 10, 12, 15]), rng.choice([9, 11, 14, 20]); a = rng.choice([0.05, 0.025, 0.01]); v = Tq(a, n1 + n2 - 2)
        nump(B, rng, f'Hai mẫu độc lập n₁ = {n1}, n₂ = {n2}, cùng σ². Giá trị tới hạn t_{{{fg(a)}}} của t gộp (một phía) xấp xỉ', v, f'df = {n1}+{n2}−2 = {n1+n2-2}; t = {f(v,3)}.', 2, T['two'], extra=[Tq(a, n1 + n2 - 1), Tq(a, n1 - 1), Tq(a / 2, n1 + n2 - 2)], d=3)
    for _ in range(12):
        n = rng.choice([10, 15, 20, 25]); a = rng.choice([0.05, 0.1]); lo, hi = st.chi2.ppf(a / 2, n - 1), st.chi2.ppf(1 - a / 2, n - 1)
        nump(B, rng, f'Kiểm định hai phía σ² với n = {n}, α = {fg(a)}. Giá trị tới hạn trên χ²_{{{fg(a/2)}}}({n-1}) (miền bác bỏ χ² > c₂) là', hi, f'SciPy: {f(hi,3)} (cận dưới {f(lo,3)}).', 2, T['var'], extra=[lo, st.chi2.ppf(1 - a, n - 1), st.chi2.ppf(1 - a / 2, n)], d=3, lo=0.0)
        nump(B, rng, f'Kiểm định hai phía σ² với n = {n}, α = {fg(a)}. Giá trị tới hạn dưới χ²_{{{fg(1-a/2)}}}({n-1}) (miền bác bỏ χ² < c₁) là', lo, f'SciPy: {f(lo,3)} (cận trên {f(hi,3)}).', 2, T['var'], extra=[hi, st.chi2.ppf(a, n - 1), st.chi2.ppf(a / 2, n)], d=3, lo=0.0)
    for _ in range(12):
        n1, n2 = rng.choice([8, 10, 12]), rng.choice([9, 12, 15]); s1, s2 = rng.choice([3, 4, 5]), rng.choice([2.5, 3.2, 3.8]); F0 = s1 ** 2 / s2 ** 2; c = st.f.ppf(0.95, n1 - 1, n2 - 1); rej = F0 > c
        txt(B, f'F-test một phía H₁: σ₁² > σ₂²; n₁ = {n1}, s₁ = {s1}; n₂ = {n2}, s₂ = {s2}; α = 0.05. Kết luận là', 'bác bỏ H₀' if rej else 'chưa đủ cơ sở bác bỏ H₀', ['chấp nhận H₁ chắc chắn' if rej else 'bác bỏ H₀', 'chứng minh σ₁² = σ₂²' if not rej else 'chưa đủ dữ kiện', 'chỉ so sánh x̄'], f'F = {f(F0,3)}; F₀.₀₅({n1-1}; {n2-1}) = {f(c,3)} ⇒ {"bác bỏ" if rej else "chưa bác bỏ"} H₀.', 3, T['ftest'])
    for _ in range(12):
        n1, n2 = rng.choice([100, 150, 200]), rng.choice([120, 180, 250]); k1 = round(n1 * rng.choice([0.4, 0.55, 0.65])); k2 = round(n2 * rng.choice([0.3, 0.45, 0.5])); pp = (k1 + k2) / (n1 + n2); z = (k1 / n1 - k2 / n2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)); rej = abs(z) > 1.96
        txt(B, f'H₀: p₁ = p₂ (hai phía, α = 0.05). Mẫu 1: {k1}/{n1}; mẫu 2: {k2}/{n2}. Kết luận là', 'bác bỏ H₀' if rej else 'chưa đủ cơ sở bác bỏ H₀', ['chấp nhận H₁ chắc chắn' if rej else 'bác bỏ H₀', 'chứng minh p₁ = p₂' if not rej else 'chưa đủ dữ kiện', 'chỉ so p̂₁ với p̂₂'], f'U = {f(z,3)}; |U| {">" if rej else "≤"} 1.96 ⇒ {"bác bỏ" if rej else "chưa bác bỏ"} H₀.', 3, T['prop'])
    for q, ok, bad in [('Kiểm định hai phía về σ² dùng hai giá trị tới hạn', 'χ²_{α/2}(n − 1) và χ²_{1−α/2}(n − 1)', ['chỉ χ²_α(n − 1)', 'U_{α/2} và −U_{α/2}', 't_{α/2}(n − 1)']),
                       ('Khi dùng t gộp, nếu hai phương sai mẫu rất khác nhau thì nên', 'kiểm tra lại giả thiết cùng phương sai (F-test)', ['vẫn dùng t gộp bình thường', 'dùng χ² phù hợp', 'bỏ mẫu nhỏ hơn']),
                       ('Dưới H₀: p₁ = p₂ sai số chuẩn của p̂₁ − p̂₂ dùng', 'p̂ gộp: √(p̂(1 − p̂)(1/n₁ + 1/n₂))', ['√(p̂₁(1 − p̂₁)/n₁)', 'p̂₁ − p̂₂', '√(p̂/n₁ + p̂/n₂) không có (1 − p̂)']),
                       ('Số bậc tự do của F-test so sánh hai phương sai (n₁, n₂) là', '(n₁ − 1; n₂ − 1)', ['(n₁; n₂)', 'n₁ + n₂ − 2', '(n₁ + n₂ − 1; 1)'])]:
        txt(B, q, ok, bad, 'Kiến thức §3.3–3.4.', 2, T['theory'])
def b_m12(B, rng, T):
    for lam in (0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 0.7, 1.8):
        k = rng.choice([0, 1, 2, 3]); n = rng.choice([100, 200, 300, 500]); v = n * st.poisson.pmf(k, lam)
        nump(B, rng, f'Phù hợp Poisson(λ = {fg(lam)}), n = {n} quan sát. Tần số kỳ vọng của giá trị {k} là', v, f'E = n·P(X = {k}) = {n}·{f(st.poisson.pmf(k,lam),4)} = {f(v,2)}.', 2, T['gof'], extra=[n * st.poisson.cdf(k, lam), n * lam, n * st.poisson.pmf(k + 1, lam), n * st.poisson.pmf(k, lam) * 2], d=2, lo=0.0)
def b_m13(B, rng, T):
    for _ in range(12):
        a = round(rng.uniform(-5, 15), 2); b = round(rng.uniform(-2, 4), 2); xb = rng.choice([4, 5, 7.5, 10]); yb = a + b * xb
        nump(B, rng, f'Hồi quy mẫu ŷ = {fg(a)} {"+" if b>=0 else "−"} {fg(abs(b))}x có x̄ = {fg(xb)}. Giá trị ŷ tại x = x̄ (và cũng là ȳ) bằng', yb, f'Đường hồi quy qua (x̄, ȳ) nên ŷ(x̄) = {fg(a)} + ({fg(b)})·{fg(xb)} = {f(yb,3)}.', 2, T['reg'], extra=[a, b * xb, a + b, xb], d=3)
