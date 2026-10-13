"""Module 7 — biến thể tham số (bo_sung): đặc trưng mẫu, MLE, sai số chuẩn."""
import math, random
import numpy as np
from qb import f, fg, nd
from qh import pm
from orig_m07 import TOP, mean_f, var_f
SRC = 'Bổ sung: biến thể tham số của dạng bài §2.1–2.2 (đáp án tính bằng công thức, đối chiếu numpy)'
def build(B):
    rng = random.Random(1707)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    # 1. mẫu thô: x̄, s², s
    for t in range(8):
        n = rng.randint(6, 10); base = rng.choice([10, 20, 50, 100]); x = [round(base + rng.gauss(0, base / 6), 1) for _ in range(n)]
        m = np.mean(x); v = np.var(x, ddof=1); lst = ', '.join(fg(a, 2) for a in x)
        P(f'Mẫu cỡ n = {n}: {lst}. Trung bình mẫu x̄ là', m, f'x̄ = Σxᵢ/n = {f(sum(x),2)}/{n} = {f(m,4)}.', 1, TOP['sample'], SRC, extra=[float(np.median(x)), sum(x) / (n - 1), m + 1], d=3)
        P(f'Mẫu cỡ n = {n}: {lst}. Phương sai mẫu s² (chia n − 1) là', v, f's² = Σ(xᵢ − x̄)²/(n − 1) = {f(v*(n-1),3)}/{n-1} = {f(v,4)}. (Chia n sẽ ra {f(np.var(x),4)}.)', 2, TOP['sample'], SRC, extra=[float(np.var(x)), math.sqrt(v), v * (n - 1) / (n + 1)], d=3)
    # 2. bảng tần số rời rạc
    for t in range(6):
        xs = sorted(rng.sample(range(1, 15), 5)); ns = [rng.randint(2, 15) for _ in xs]; N = sum(ns); m = mean_f(xs, ns); v = var_f(xs, ns)
        tb = ', '.join(f'{x}:{n}' for x, n in zip(xs, ns))
        P(f'Mẫu (giá trị: tần số) — {tb}. Trung bình mẫu x̄ là', m, f'N = {N}; Σxᵢnᵢ = {sum(a*b for a,b in zip(xs,ns))}; x̄ = {f(m,4)}.', 1, TOP['group'], SRC, extra=[sum(xs) / 5, xs[2], m + 0.5], d=3)
        P(f'Mẫu (giá trị: tần số) — {tb}. Độ lệch chuẩn mẫu s là', math.sqrt(v), f's² = {f(v,4)} ⇒ s = {f(math.sqrt(v),4)}.', 2, TOP['group'], SRC, extra=[v, math.sqrt(sum(n * (x - m) ** 2 for x, n in zip(xs, ns)) / N), 1.0], d=3)
    # 3. bảng lớp
    for t in range(6):
        w = rng.choice([2, 5, 10]); lo = rng.choice([0, 10, 40]); k = 5; ns = [rng.randint(1, 12) for _ in range(k)]; N = sum(ns)
        mids = [lo + w * (i + 0.5) for i in range(k)]; m = mean_f(mids, ns); v = var_f(mids, ns)
        tb = ', '.join(f'{fg(lo + w * i)}–{fg(lo + w * (i + 1))}: {n}' for i, n in enumerate(ns))
        P(f'Bảng lớp (lớp: tần số) — {tb}. Với điểm giữa lớp, trung bình mẫu x̄ là', m, f'N = {N}; x̄ = Σxᵢnᵢ/N = {f(m,4)}.', 2, TOP['group'], SRC, extra=[sum(mids) / k, lo + w * 2.5, m - w / 2], d=3)
        P(f'Bảng lớp (lớp: tần số) — {tb}. Phương sai mẫu s² (điểm giữa lớp, chia N − 1) là', v, f's² = {f(v,4)}.', 3, TOP['group'], SRC, extra=[math.sqrt(v), v * (N - 1) / N, v + w], d=3)
    # 4. MLE
    for t in range(5):
        n = rng.randint(5, 9); xs = [round(rng.expovariate(0.5), 2) for _ in range(n)]; th = n / sum(xs)
        P(f'Mẫu từ mật độ f(x) = θe^(−θx), x ≥ 0: {", ".join(fg(a,2) for a in xs)}. MLE của θ là', th, f'θ̂ = n/Σxᵢ = {n}/{f(sum(xs),2)} = {f(th,4)}.', 2, TOP['mle'], SRC, extra=[sum(xs) / n, 1 / th, th * 2], d=3)
    for t in range(4):
        n = rng.randint(6, 9); xs = [rng.randint(0, 6) for _ in range(n)]; mu = sum(xs) / n
        P(f'Mẫu từ phân phối Poisson(μ): {", ".join(map(str,xs))}. MLE của μ là', mu, f'ln l = −nμ + (Σxᵢ)ln μ − Σln xᵢ! ⇒ μ̂ = x̄ = {sum(xs)}/{n} = {f(mu,4)}.', 2, TOP['mle'], SRC, extra=[mu * (n - 1) / n, math.sqrt(mu), mu + 1], d=3)
    for t in range(4):
        n = rng.choice([20, 40, 50, 100, 200]); k = rng.randint(1, n - 1); p = k / n
        P(f'Trong {n} phép thử độc lập có {k} lần thành công. MLE của xác suất thành công p là', p, f'p̂ = x/n = {k}/{n} = {f(p,4)}.', 1, TOP['mle'], SRC, extra=[1 - p, k / (n - 1), p * 2 if p * 2 <= 1 else p / 2], d=4)
    for t in range(4):
        n = rng.randint(5, 8); xs = [rng.randint(1, 8) for _ in range(n)]; p = n / sum(xs)
        P(f'X là số lần thử cho đến lần thành công đầu tiên, f(x) = p(1 − p)^(x−1). Mẫu: {", ".join(map(str,xs))}. MLE của p là', p, f'p̂ = n/Σxᵢ = {n}/{sum(xs)} = {f(p,4)}.', 2, TOP['mle'], SRC, extra=[sum(xs) / n, 1 - p, p / 2], d=4)
    for t in range(4):
        n = rng.randint(5, 8); xs = [round(rng.gauss(10, 2), 1) for _ in range(n)]; m = np.mean(xs); s2n = float(np.var(xs)); s2 = float(np.var(xs, ddof=1))
        P(f'Mẫu từ N(μ, σ²): {", ".join(fg(a,2) for a in xs)}. MLE của σ² (chia n) là', s2n, f'σ̂² = (1/n)Σ(xᵢ − x̄)² = {f(s2n,4)}; còn s² (chia n − 1) = {f(s2,4)} là ước lượng không chệch.', 3, TOP['mle'], SRC, extra=[s2, math.sqrt(s2n), s2n * 2], d=3)
    # 5. sai số chuẩn
    for sg, n in [(10, 25), (4, 16), (6, 100), (12, 36), (2.5, 50), (8, 64)]:
        P(f'Tổng thể có σ = {sg}. Với mẫu cỡ n = {n}, độ lệch chuẩn của trung bình mẫu x̄ (sai số chuẩn σ/√n) là', sg / math.sqrt(n), f'σ/√n = {sg}/√{n} = {f(sg/math.sqrt(n),4)}.', 1, TOP['point'], SRC, extra=[sg / n, sg * math.sqrt(n), sg ** 2 / n], d=3)
    for sg, n in [(10, 25), (6, 36), (20, 100)]:
        B.mcq(f'Tổng thể có σ = {sg}. Cần tăng cỡ mẫu từ n = {n} lên bao nhiêu để sai số chuẩn của x̄ giảm một nửa?', str(4 * n), [str(2 * n), str(n + n // 2), str(3 * n)], f'σ/√n giảm một nửa ⇒ √n tăng gấp đôi ⇒ n tăng gấp 4: {4*n}.', 2, TOP['point'], SRC, 'bo_sung')
    # 6. không chệch / lý thuyết nhanh
    for stem, ans, wr, ex in [
        ('Ước lượng nào của μ là không chệch?', 'x̄ (trung bình mẫu)', ['x̄ + 1', '2x̄', 'x̄/2'], 'E(x̄) = μ; các lựa chọn khác lệch hệ thống.'),
        ('Với mẫu cỡ n = 1, ước lượng không chệch của μ là:', 'x₁', ['x₁²', 'x₁ + 5', 'không có'], 'Một quan sát duy nhất có kỳ vọng E(x₁) = μ nên x₁ là ước lượng không chệch (dù phương sai lớn).'),
        ('MLE của σ² trong phân phối chuẩn có tính chất:', 'Chệch (E[σ̂²] = (n − 1)σ²/n) nhưng chệch giảm khi n lớn', ['Không chệch với mọi n', 'Chệch nhưng không đổi khi n tăng', 'Luôn bằng s²'], 'Chia n thay vì n − 1 làm σ̂² nhỏ hơn s² một hệ số (n − 1)/n.'),
        ('Nếu θ̂ là MLE của θ thì MLE của g(θ) (g đơn ánh) là:', 'g(θ̂) (tính bất biến)', ['g′(θ̂)', 'θ̂', 'g⁻¹(θ̂)'], 'Ví dụ: MLE của μ = 1/θ là 1/θ̂ = x̄ (Kreyszig PS 25.2/12).')]:
        B.mcq(stem, ans, wr, ex, 2, TOP['point'], SRC, 'bo_sung')
