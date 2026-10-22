"""Module 7 — mở rộng: khái niệm + họ bài tính (đáp án tự tính)."""
import math, random
from scipy import stats as st
from qb import f, fg
from qh import pm
from pskit import mean, var_s, var_p
from orig_m07 import TOP
SRC = 'Bổ sung: dạng bài §2.1–2.2 (đáp án tự tính bằng công thức, đối chiếu numpy/scipy)'
def build(B):
    rng = random.Random(2507)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Ước lượng θ̂ gọi là không chệch nếu', 'E(θ̂) = θ', ['Var(θ̂) = 0', 'θ̂ = θ', 'E(θ̂) = 0'], 'Trung bình của ước lượng qua nhiều mẫu bằng tham số thật.', 1, 'point')
    C('Trung bình mẫu X̄ là ước lượng không chệch của', 'kỳ vọng μ', ['phương sai σ²', 'độ lệch chuẩn σ', 'trung vị'], 'E(X̄) = μ.', 1, 'point')
    C('Phương sai mẫu S² = Σ(Xᵢ − X̄)²/(n − 1) là ước lượng', 'không chệch của σ²', ['chệch cao của σ²', 'không chệch của σ', 'của μ'], 'E(S²) = σ².', 1, 'point')
    C('Sai số chuẩn của X̄ là', 'σ/√n', ['σ/n', 'σ²/n', 'σ·√n'], 'Var(X̄) = σ²/n.', 1, 'sample')
    C('Tăng cỡ mẫu lên gấp 4 thì sai số chuẩn của X̄', 'giảm một nửa', ['giảm còn 1/4', 'không đổi', 'tăng gấp đôi'], 'σ/√(4n) = (σ/√n)/2.', 2, 'sample')
    C('Định lý giới hạn trung tâm nói với n đủ lớn', 'X̄ xấp xỉ chuẩn bất kể phân phối của tổng thể', ['X̄ luôn bằng μ', 'tổng thể phải chuẩn', 'S² = σ²'], 'Ứng dụng cho mẫu lớn.', 2, 'sample')
    C('Hàm hợp lý L(θ) là', 'tích các mật độ (hoặc xác suất) của các quan sát tại tham số θ', ['tổng các quan sát', 'mật độ của X̄', 'đạo hàm của f'], 'L(θ) = Π f(xᵢ; θ) với mẫu độc lập.', 1, 'mle')
    C('Vì sao thường lấy logarit hàm hợp lý?', 'biến tích thành tổng, dễ đạo hàm, cực trị không đổi', ['để L âm', 'để loại bỏ θ', 'để L lớn hơn'], 'ln đơn điệu tăng.', 1, 'mle')
    C('MLE của p trong mẫu Bernoulli là', 'tỷ lệ thành công của mẫu k/n', ['k·n', '1/n', 'k/(n − 1)'], 'p̂ = k/n.', 1, 'mle')
    C('MLE của λ cho mẫu Poisson là', 'trung bình mẫu x̄', ['1/x̄', 's²', 'x̄²'], 'Đạo hàm ℓ cho λ̂ = x̄.', 1, 'mle')
    C('MLE của λ cho mẫu mũ (f = λe^(−λt)) là', '1/x̄', ['x̄', 'x̄²', 'n·x̄'], 'ℓ′ = n/λ − Σtᵢ = 0.', 2, 'mle')
    C('MLE của σ² trong mẫu chuẩn chia cho', 'n', ['n − 1', 'n + 1', 'n − 2'], 'σ̂² = Σ(xᵢ − x̄)²/n (chệch).', 2, 'mle')
    C('Nếu θ̂ là MLE của θ thì MLE của g(θ) là', 'g(θ̂)', ['g′(θ̂)', 'θ̂', '1/g(θ̂)'], 'Tính bất biến của MLE.', 2, 'mle')
    C('MSE của ước lượng bằng', 'phương sai + (chệch)²', ['phương sai − chệch', 'chệch', 'phương sai·chệch'], 'MSE = Var + Bias².', 3, 'point')
    C('Ước lượng vững nghĩa là', 'θ̂ tiến về θ khi n tăng', ['θ̂ không đổi', 'Var(θ̂) = 0 với mọi n', 'θ̂ = x̄'], 'Hội tụ theo xác suất.', 2, 'point')
    # sai số chuẩn
    for sg, n in [(12, 36), (10, 25), (8, 64), (5, 100), (20, 16), (3, 9), (15, 50), (6, 144)]:
        P(f'Tổng thể có σ = {sg}. Mẫu n = {n}. Sai số chuẩn của X̄ là', sg / math.sqrt(n), f'σ/√n = {sg}/{f(math.sqrt(n),3)} = {f(sg/math.sqrt(n),4)}.', 1, TOP['sample'], SRC, extra=[sg / n, sg * math.sqrt(n), sg ** 2 / n], d=4, hi=None)
    for sg, n, d_ in [(12, 36, 3), (10, 25, 2), (8, 64, 1), (5, 100, 1), (20, 16, 6), (15, 50, 4)]:
        se = sg / math.sqrt(n); pr = 2 * st.norm.cdf(d_ / se) - 1
        P(f'Tổng thể có σ = {sg}. Mẫu n = {n}. P(|X̄ − μ| < {d_}) xấp xỉ bằng', pr, f'σ_X̄ = {f(se,3)}; z = {f(d_/se,3)}; P = 2Φ(z) − 1 = {f(pr,4)}.', 3, TOP['sample'], SRC, extra=[st.norm.cdf(d_ / se), 1 - pr, 2 * st.norm.cdf(d_ / sg) - 1], d=4)
    for sg, e, z, zs in [(10, 2, 1.96, '95%'), (15, 3, 1.645, '90%'), (8, 1, 2.576, '99%'), (20, 4, 1.96, '95%'), (5, 0.5, 1.96, '95%'), (12, 2, 2.326, '98%')]:
        nn = (z * sg / e) ** 2
        B.mcq(f'σ = {sg}. Cỡ mẫu nhỏ nhất để P(|X̄ − μ| < {e}) ≥ {zs} (z = {z}) là', str(math.ceil(nn)), [str(round(nn)) if round(nn) != math.ceil(nn) else str(math.ceil(nn) + 1), str(math.ceil(nn / 2)), str(math.ceil(z * sg / e)), str(math.ceil(nn) * 2)],
              f'n ≥ (zσ/e)² = ({z}·{sg}/{e})² = {f(nn,2)} ⇒ n = {math.ceil(nn)} (làm tròn lên).', 3, TOP['sample'], SRC, 'bo_sung')
    # MLE dữ liệu
    for k in range(8):
        n = rng.randint(6, 10); x = [round(rng.uniform(1, 20), 1) for _ in range(n)]; xb = mean(x)
        P(f'Mẫu mũ (mật độ λe^(−λt)): {", ".join(map(str,x))}. MLE của λ là', 1 / xb, f'λ̂ = 1/t̄ = 1/{f(xb,4)} = {f(1/xb,5)}.', 2, TOP['mle'], SRC, extra=[xb, 1 / (xb * 2), n / (sum(x) + 1)], d=5)
        P(f'Mẫu chuẩn: {", ".join(map(str,x))}. MLE của σ² (chia n) là', var_p(x), f'Σ(x − x̄)²/n = {f(var_p(x)*n,3)}/{n} = {f(var_p(x),3)} (s² = {f(var_s(x),3)}).', 3, TOP['mle'], SRC, extra=[var_s(x), math.sqrt(var_p(x)), var_p(x) * (n + 1) / n], d=3)
    for n, kk in [(50, 18), (100, 37), (80, 12), (200, 90), (40, 7), (120, 45)]:
        P(f'Trong {n} lần thử có {kk} thành công. MLE của p là', kk / n, f'p̂ = k/n = {kk}/{n} = {f(kk/n,4)}.', 1, TOP['mle'], SRC, extra=[kk / (n - 1), (n - kk) / n, kk / n / 2], d=4)
        pp = kk / n; se = math.sqrt(pp * (1 - pp) / n)
        P(f'Trong {n} lần thử có {kk} thành công. Sai số chuẩn ước lượng của p̂ là √(p̂(1 − p̂)/n) =', se, f'√({f(pp,4)}·{f(1-pp,4)}/{n}) = {f(se,4)}.', 2, TOP['point'], SRC, extra=[pp * (1 - pp) / n, math.sqrt(pp / n), se * 2], d=4)
    for xs in ([2, 0, 3, 1, 4, 2, 1, 3], [5, 3, 4, 6, 2, 5], [0, 1, 0, 2, 1, 0, 1], [7, 9, 6, 8, 10], [3, 3, 2, 4, 5, 1]):
        lam = mean(xs)
        P(f'Mẫu Poisson: {", ".join(map(str,xs))}. MLE của λ và P̂(X = 0) = e^(−λ̂) bằng', math.exp(-lam), f'λ̂ = x̄ = {f(lam,3)}; e^(−λ̂) = {f(math.exp(-lam),4)} (bất biến MLE).', 3, TOP['mle'], SRC, extra=[lam, 1 / lam, math.exp(lam) / 100], d=4)
    for xm, xs_ in [(3.1, 7.4), (2.0, 9.5), (1.2, 4.8)]:
        pass
    B.essay('Mẫu mũ: 12.5, 8.1, 20.3, 15.0, 6.9, 9.2 giờ. Tìm MLE của λ và ước lượng P(T > 20).', 'Σt = 72.0; t̄ = 12; λ̂ = 1/12 = 0.0833; P̂(T > 20) = e^(−20/12) = 0.1889.', 2, TOP['mle'], SRC, 'bo_sung')
    B.essay('Chứng minh S² = Σ(Xᵢ − X̄)²/(n − 1) không chệch cho σ².', 'Σ(Xᵢ − X̄)² = Σ(Xᵢ − μ)² − n(X̄ − μ)². Lấy kỳ vọng: nσ² − n·σ²/n = (n − 1)σ². Chia n − 1 được σ².', 3, TOP['point'], SRC, 'bo_sung')
    B.essay('Mẫu U[0, θ]: 3.1, 7.4, 5.0, 6.2. Tìm MLE θ̂ và giải thích vì sao chệch; đề xuất ước lượng không chệch.', 'L = θ^(−4) khi θ ≥ 7.4 giảm theo θ ⇒ θ̂ = 7.4. E(max) = nθ/(n+1) < θ nên chệch thấp; ước lượng không chệch (n+1)/n·max = 9.25.', 3, TOP['mle'], SRC, 'bo_sung')
    B.essay('σ = 12, cần sai số chuẩn không quá 1.5. Tìm n nhỏ nhất; với n đó P(|X̄ − μ| < 3) bằng bao nhiêu?', 'σ/√n ≤ 1.5 ⇒ n ≥ 64. Với n = 64: σ_X̄ = 1.5; P(|Z| < 2) = 0.9545.', 2, TOP['sample'], SRC, 'bo_sung')
