"""Module 5 — Biến ngẫu nhiên, hàm phân phối/mật độ, kỳ vọng, phương sai.
Gốc: Lecture Notes §1.7–1.9, Bài 1.24–1.31; Kreyszig PS 24.5 (1–15), PS 24.6 (1–19); đề cuối kỳ 2022–2023 HK1 (2TC) câu 1 và HK2 (3TC) câu 5;
đáp án giữa kỳ HK2 2022–2023 câu 2. Mọi tích phân/nghiệm được tính bằng SciPy và đối chiếu giải tích."""
import math, random
from fractions import Fraction as Fr
from scipy import integrate, optimize
from qb import f, fg, nd
from qh import pm
TOP = {'rv': 'Khái niệm biến ngẫu nhiên', 'pmf': 'Hàm xác suất, bảng phân phối (rời rạc)', 'pdf': 'Hàm mật độ và hàm phân phối (liên tục)', 'mean': 'Kỳ vọng', 'var': 'Phương sai, độ lệch chuẩn', 'quant': 'Phân vị, trung vị', 'theory': 'Lý thuyết'}
Q = lambda fn, a, b: integrate.quad(fn, a, b)[0]
def dmean(xs, ps): return sum(x * p for x, p in zip(xs, ps))
def dvar(xs, ps):
    m = dmean(xs, ps); return sum((x - m) ** 2 * p for x, p in zip(xs, ps))
def build(B):
    rng = random.Random(505)
    def P(B_, r_, *a, **k):
        k.setdefault('hi', None); return pm(B_, r_, *a, **k)
    # ================= A. Đề thi thật =================
    sets = [([0.10, 0.20, 0.25, 0.35, 0.06, 0.04], 1), ([0.15, 0.20, 0.20, 0.30, 0.08, 0.07], 2), ([0.05, 0.20, 0.25, 0.35, 0.09, 0.06], 3), ([0.05, 0.15, 0.25, 0.35, 0.13, 0.07], 4)]
    xs = [0, 1, 2, 3, 4, 5]
    for ps, k in sets:
        assert abs(sum(ps) - 1) < 1e-9
        m = dmean(xs, ps); v = dvar(xs, ps); ex2 = sum(x * x * p for x, p in zip(xs, ps))
        tab = 'X = 0, 1, 2, 3, 4, 5 với P = ' + ', '.join(f'{p:.2f}' for p in ps)
        src = f'Đề cuối kỳ 2022–2023 HK1 (2TC, K16), đề số {k}, câu 1'
        P(B, rng, f'Số điểm X của xạ thủ có phân phối: {tab}. Số điểm trung bình E(X) là', m, f'E(X) = Σxᵢpᵢ = {" + ".join(f"{x}·{p:.2f}" for x, p in zip(xs, ps))} = {f(m,3)}.', 1, TOP['mean'], src, extra=[ex2, sum(xs) / 6, m + v], d=3)
        P(B, rng, f'Số điểm X của xạ thủ có phân phối: {tab}. Phương sai Var(X) là', v, f'E(X²) = {f(ex2,3)}; Var(X) = E(X²) − [E(X)]² = {f(ex2,3)} − {f(m*m,4)} = {f(v,4)}.', 2, TOP['var'], src, extra=[ex2, math.sqrt(v), ex2 - m, v * 6 / 5], d=3)
    # pdf HK2 câu 5
    for (c, L, k) in [(6, 1, 1), (0.75, 2, 2), (0.09375, 4, 3), (0.048, 5, 4)]:
        g = lambda x, c=c, L=L: c * (L - x) * x
        assert abs(Q(g, 0, L) - 1) < 1e-9
        mu = Q(lambda x: x * g(x), 0, L); v2 = Q(lambda x: x * x * g(x), 0, L) - mu * mu
        med = optimize.brentq(lambda t: Q(g, 0, t) - 0.5, 0, L)
        assert abs(mu - L / 2) < 1e-9 and abs(med - L / 2) < 1e-9
        src = f'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số {k}, câu 5'
        d = f'f(x) = {c}·({L} − x)·x với 0 ≤ x ≤ {L}, và 0 nơi khác'
        P(B, rng, f'X có hàm mật độ {d}. Kỳ vọng E(X) là', mu, f'∫₀^{L} x·f(x)dx = {c}∫₀^{L}(({L}x² − x³))dx = {f(mu,4)}. Mật độ đối xứng qua x = {L}/2 nên E(X) = {L}/2.', 2, TOP['mean'], src, extra=[L, L / 3, L * 2 / 3, 1 / c], d=4, lo=0)
        P(B, rng, f'X có hàm mật độ {d}. Số m sao cho P(X ≤ m) = 50% (trung vị) là', med, f'F(m) = {c}({L}m²/2 − m³/3) = 0.5 ⇒ m = {f(med,4)} (do đối xứng, trung vị = kỳ vọng).', 3, TOP['quant'], src, extra=[L / 3, L * 0.6, L * 0.4, L], d=4, lo=0)
        P(B, rng, f'X có hàm mật độ {d}. Kiểm tra điều kiện chuẩn hóa: ∫₀^{L} f(x)dx bằng', 1.0, f'{c}·({L}·{L}²/2 − {L}³/3) = {c}·{L**3/6:.5f} = 1.0000 ✓.', 1, TOP['pdf'], src, extra=[c, 0.5, 2.0], d=4)
        P(B, rng, f'X có hàm mật độ {d}. Phương sai Var(X) là', v2, f'E(X²) = {c}∫₀^{L} x²({L} − x)x dx = {f(v2+mu*mu,4)}; Var = E(X²) − μ² = {f(v2,4)}.', 3, TOP['var'], src, extra=[mu * mu, math.sqrt(v2), v2 * 2], d=4, lo=0)
    # Đáp án giữa kỳ HK2 câu 2
    pT = [0.28, 0.1332, 0.3648, 0.222]; xs4 = [0, 1, 2, 3]
    assert abs(sum(pT) - 1) < 1e-12
    K = 'Đáp án giữa kỳ HK2 2022–2023, câu 2 (a=3, b=2, c=2)'
    P(B, rng, 'T nhận các giá trị 0, 1, 2, 3 với P(T=0) = 0.28, P(T=1) = 0.8y − m = 0.1332, P(T=2) = 0.3648, P(T=3) = m = 0.5y, với y = 0.444. Giá trị m là', 0.222, 'Từ y = 0.444: m = 0.5y = 0.222; kiểm tra tổng 0.28 + 0.1332 + 0.3648 + 0.222 = 1 ✓.', 2, TOP['pmf'], K, extra=[0.444, 0.1332, 0.3648], d=3)
    P(B, rng, 'Với P(T=0) = 0.28, P(T=1) = 0.1332, P(T=2) = 0.3648, P(T=3) = 0.222, xác suất P(0.5 < T < 2.5) là', 0.1332 + 0.3648, 'Chỉ có T = 1 và T = 2 nằm trong (0.5; 2.5) ⇒ 0.1332 + 0.3648 = 0.498.', 1, TOP['pmf'], K, extra=[0.28 + 0.222, 0.1332 + 0.3648 + 0.222, 0.3648], d=3)
    P(B, rng, 'Với P(T=0) = 0.28, P(T=1) = 0.1332, P(T=2) = 0.3648, P(T=3) = 0.222, kỳ vọng E(T) là', dmean(xs4, pT), f'E(T) = 0 + 1·0.1332 + 2·0.3648 + 3·0.222 = {f(dmean(xs4,pT),4)}.', 1, TOP['mean'], K, extra=[1.5, 2.0, 0.75], d=4)
    P(B, rng, 'Với P(T=0) = 0.28, P(T=1) = 0.1332, P(T=2) = 0.3648, P(T=3) = 0.222, phương sai σ² = Σ(xᵢ − μ)²pᵢ là', dvar(xs4, pT), f'μ = 1.5288; σ² = (0 − μ)²·0.28 + (1 − μ)²·0.1332 + (2 − μ)²·0.3648 + (3 − μ)²·0.222 = {f(dvar(xs4,pT),5)}.', 2, TOP['var'], K, extra=[math.sqrt(dvar(xs4, pT)), sum(x * x * p for x, p in zip(xs4, pT)), 1.5288], d=5)
    # ================= B. Lecture Notes =================
    S = 'Lecture Notes '
    B.mcq('Biến ngẫu nhiên (Định nghĩa 1.7) là:', 'Một hàm X: S → ℝ gán số thực cho mỗi kết cục của không gian mẫu', ['Một biến mà giá trị chọn tuỳ ý', 'Một xác suất của biến cố', 'Một tập các biến cố'], 'BNN là hàm từ không gian mẫu vào ℝ sao cho P(X = a) và P(X ∈ I) xác định được.', 1, TOP['rv'], S + 'Định nghĩa 1.7')
    B.mcq('Gieo con súc sắc, X là số tiền thưởng (10 000 đ nhân số chấm). X là biến ngẫu nhiên loại nào?', 'Rời rạc (nhận các giá trị 10 000, …, 60 000)', ['Liên tục', 'Không phải biến ngẫu nhiên', 'Vừa rời rạc vừa liên tục'], 'X chỉ nhận 6 giá trị hữu hạn ⇒ rời rạc (Ví dụ 1.23).', 1, TOP['rv'], S + 'Ví dụ 1.23')
    B.mcq('Bắn đạn vào bia bán kính 20 cm, X là khoảng cách từ tâm bia tới điểm trúng. X là biến ngẫu nhiên loại nào?', 'Liên tục (nhận mọi giá trị trong [0, 20])', ['Rời rạc', 'Nhị thức', 'Không xác định'], 'X nhận mọi giá trị trong một khoảng ⇒ liên tục (Ví dụ 1.24).', 1, TOP['rv'], S + 'Ví dụ 1.24')
    B.mcq('Trong bài bắn bia nhận điểm 10, 9, …, 1, 0, số điểm X là biến ngẫu nhiên loại nào?', 'Rời rạc (nhận 11 giá trị 0, 1, …, 10)', ['Liên tục', 'Chuẩn', 'Đồng nhất'], 'Số điểm chỉ nhận các giá trị nguyên 0..10 (Ví dụ 1.24 kịch bản 2).', 1, TOP['rv'], S + 'Ví dụ 1.24(ii)')
    # Bài 1.24
    B.mcq('Biến ngẫu nhiên X có hàm xác suất f(x) = k/2ˣ với x = 0, 1, 2, … (Bài 1.24). Giá trị k là', '1/2', ['1', '1/4', '2'], 'Σ k/2ˣ = k·(1 + 1/2 + 1/4 + …) = 2k = 1 ⇒ k = 1/2.', 2, TOP['pmf'], S + 'Bài 1.24')
    B.mcq('Với f(x) = (1/2)/2ˣ = 1/2^{x+1}, x = 0, 1, 2, … , xác suất P(X ≥ 4) là (Bài 1.24)', '1/16', ['1/8', '1/32', '15/16'], 'P(X ≥ 4) = Σ_{x≥4} 1/2^{x+1} = (1/32)·2 = 1/16 (hoặc 1 − (1/2 + 1/4 + 1/8 + 1/16) = 1/16).', 2, TOP['pmf'], S + 'Bài 1.24')
    # Bài 1.25
    B.mcq('f(x) = kx² với 0 ≤ x ≤ 5 và 0 nơi khác là hàm mật độ. Giá trị k là (Bài 1.25)', '3/125', ['1/25', '1/125', '3/25'], '∫₀⁵ kx² dx = 125k/3 = 1 ⇒ k = 3/125 = 0.024.', 1, TOP['pdf'], S + 'Bài 1.25 / Kreyszig PS 24.5 Prob. 2')
    B.mcq('Hàm phân phối F(x) tương ứng (Bài 1.25) với 0 ≤ x ≤ 5 là', 'F(x) = x³/125', ['F(x) = x²/25', 'F(x) = 3x²/125', 'F(x) = x³/25'], 'F(x) = ∫₀ˣ (3/125)t² dt = x³/125; F(0) = 0, F(5) = 1.', 2, TOP['pdf'], S + 'Bài 1.25')
    # Bài 1.26
    g = lambda c: Q(lambda x: 0.75 * (1 - x * x), -c, c) - 0.95
    c126 = optimize.brentq(g, 0.01, 0.999)
    P(B, rng, 'Độ dài bu-lông L = 200 + X (mm), X có mật độ f(x) = (3/4)(1 − x²) với −1 ≤ x ≤ 1. Tìm c để 95% bu-lông có chiều dài trong [200 − c, 200 + c] (Bài 1.26).', c126, f'P(|X| ≤ c) = 1.5c − 0.5c³ = 0.95 ⇒ c ≈ {f(c126,4)}.', 3, TOP['quant'], S + 'Bài 1.26', extra=[0.95, 0.5, 0.9], d=4, lo=0, hi=1)
    # Bài 1.27 / Kreyszig 8
    x127 = math.log(10) / 3
    P(B, rng, 'F(x) = 1 − e^{−3x} (x > 0). Tìm x sao cho F(x) = 0.9 (Bài 1.27).', x127, f'e^{{−3x}} = 0.1 ⇒ x = ln 10/3 = {f(x127,4)}. Mật độ f(x) = F′(x) = 3e^{{−3x}}.', 2, TOP['quant'], S + 'Bài 1.27 / Kreyszig PS 24.5 Prob. 8', extra=[0.9, math.log(10), math.log(10) / 9, 1 / 3], d=4, lo=0)
    # Bài 1.28 / Kreyszig 12
    B.mcq('F(x) = 0 (x < 2), F(x) = (x² − 4)/5 (2 ≤ x < 3), F(x) = 1 (x ≥ 3). Hàm mật độ trên [2, 3) là (Bài 1.28)', 'f(x) = 2x/5', ['f(x) = (x² − 4)/5', 'f(x) = x/5', 'f(x) = 2/5'], 'f(x) = F′(x) = 2x/5; ∫₂³ 2x/5 dx = (9 − 4)/5 = 1.', 2, TOP['pdf'], S + 'Bài 1.28 / Kreyszig PS 24.5 Prob. 12')
    P(B, rng, 'Với cùng phân phối (tỉ số doanh thu/lợi nhuận), P(2.5 ≤ X ≤ 5) là (Bài 1.28)', 0.55, 'P = F(5) − F(2.5) = 1 − (6.25 − 4)/5 = 1 − 0.45 = 0.55 (với x ≥ 3, F = 1).', 2, TOP['pdf'], S + 'Bài 1.28 / Kreyszig PS 24.5 Prob. 12', extra=[0.45, 0.5, 0.25], d=2)
    # Bài 1.29
    B.mcq('Gieo một con súc sắc đồng chất. Kỳ vọng và phương sai của số chấm X là (Bài 1.29a)', '3.5 và 35/12 ≈ 2.9167', ['3 và 2.5', '3.5 và 1.7078', '3.5 và 91/6'], 'E(X) = 21/6 = 3.5; E(X²) = 91/6; Var = 91/6 − 12.25 = 35/12.', 1, TOP['mean'], S + 'Bài 1.29(a) / Kreyszig PS 24.6 Prob. 2')
    B.mcq('f(0) = 0.512, f(1) = 0.384, f(2) = 0.096, f(3) = 0.008. Kỳ vọng và phương sai (Bài 1.29b) là', '0.6 và 0.48', ['1.5 và 0.75', '0.6 và 0.36', '0.48 và 0.6'], 'E = 0.384 + 0.192 + 0.024 = 0.6; E(X²) = 0.384 + 0.384 + 0.072 = 0.84; Var = 0.84 − 0.36 = 0.48 (đây là B(3, 0.2): np = 0.6, npq = 0.48).', 2, TOP['var'], S + 'Bài 1.29(b)')
    B.mcq('f(x) = 2x trên [0, 1]. Kỳ vọng và phương sai (Bài 1.29c) là', '2/3 và 1/18', ['1/2 và 1/12', '2/3 và 1/9', '1/3 và 1/18'], 'E = ∫2x² = 2/3; E(X²) = ∫2x³ = 1/2; Var = 1/2 − 4/9 = 1/18.', 2, TOP['var'], S + 'Bài 1.29(c)')
    # Bài 1.30 / Kreyszig 15, 16
    v130 = Q(lambda x: (x - 0.5) ** 2 * 6 * x * (1 - x), 0, 1)
    B.mcq('Thể tích xăng bán X (đơn vị 10 000 gallon) có mật độ f(x) = 6x(1 − x) trên [0, 1]. Kỳ vọng, phương sai, độ lệch chuẩn là (Bài 1.30a)', f'0.5; 0.05; {f(math.sqrt(0.05),4)}', [f'0.5; 0.25; 0.5', f'0.6; 0.05; {f(math.sqrt(0.05),4)}', f'0.5; 0.05; 0.05'], f'E = 0.5 (đối xứng); E(X²) = 0.3; Var = 0.3 − 0.25 = {f(v130,4)}; σ = {f(math.sqrt(v130),4)}.', 2, TOP['var'], S + 'Bài 1.30(a) / Kreyszig PS 24.6 Prob. 15')
    c130 = optimize.brentq(lambda c: 3 * c * c - 2 * c ** 3 - 0.95, 0.5, 1)
    P(B, rng, 'Với mật độ f(x) = 6x(1 − x) trên [0, 1], dung tích bể (đơn vị 10 000 gallon) để xác suất bán hết xăng trong một tuần là 5% (Bài 1.30b / Kreyszig 24.6/16) là', c130, f'P(X > c) = 0.05 ⇔ F(c) = 3c² − 2c³ = 0.95 ⇒ c ≈ {f(c130,4)}.', 3, TOP['quant'], S + 'Bài 1.30(b) / Kreyszig PS 24.6 Prob. 16', extra=[0.95, 0.5, 0.9], d=4, lo=0, hi=1)
    # Bài 1.31
    B.mcq('Tung 4 đồng xu đồng chất; X là số mặt ngửa. P(X = 2) và P(X ≥ 1) (Bài 1.31) là', '6/16 và 15/16', ['4/16 và 1/16', '6/16 và 11/16', '1/2 và 15/16'], 'X ~ B(4, 1/2): P(X = k) = C(4,k)/16 = 1, 4, 6, 4, 1 trên 16. P(X ≥ 1) = 1 − 1/16 = 15/16.', 1, TOP['pmf'], S + 'Bài 1.31')
    # ================= C. Kreyszig PS 24.5 =================
    K5 = 'Kreyszig PS 24.5, Prob. '
    B.mcq('f(x) = kx², x = 1, 2, 3, 4, 5 là hàm xác suất. Giá trị k là (Prob. 1)', '1/55', ['1/15', '1/25', '1/30'], 'Σx² = 1 + 4 + 9 + 16 + 25 = 55 ⇒ k = 1/55.', 1, TOP['pmf'], K5 + '1')
    B.mcq('Mật độ đều f(x) = k trên [−2, 2]. Giá trị k và P(0 ≤ X ≤ 2) là (Prob. 3)', 'k = 1/4; P = 1/2', ['k = 1/2; P = 1', 'k = 1/4; P = 1/4', 'k = 1/2; P = 1/2'], '∫_{−2}^{2} k dx = 4k = 1 ⇒ k = 1/4; P(0 ≤ X ≤ 2) = 2·(1/4) = 1/2.', 1, TOP['pdf'], K5 + '3')
    B.mcq('Mật độ đều trên [−2, 2]. Số c sao cho P(−c < X < c) = 95% là (Prob. 4)', '1.9', ['0.95', '1.95', '3.8'], 'P(−c < X < c) = 2c/4 = c/2 = 0.95 ⇒ c = 1.9.', 2, TOP['quant'], K5 + '4')
    B.mcq('f(−2) = f(2) = 1/8, f(−1) = f(1) = 3/8. f có thể nhận thêm giá trị dương tại điểm khác không? (Prob. 5)', 'Không, vì tổng đã bằng 1', ['Có, tại x = 0', 'Có, tại x = 3', 'Chỉ khi f âm ở chỗ khác'], 'Tổng 2·(1/8) + 2·(3/8) = 1; hàm xác suất không âm nên mọi điểm khác phải có f = 0.', 2, TOP['pmf'], K5 + '5')
    nL = 6
    B.mcq('Hộp có 4 ốc xoắn phải và 6 ốc xoắn trái; rút 2 ốc không hoàn lại; X là số ốc xoắn trái. P(X = 0), P(X = 1), P(X = 2) (Prob. 6) lần lượt là', '2/15, 8/15, 5/15', ['1/6, 4/6, 1/6', '4/25, 12/25, 9/25', '1/3, 1/3, 1/3'], 'Siêu bội: P(X = k) = C(6,k)C(4,2−k)/C(10,2) = 6/45, 24/45, 15/45 = 2/15, 8/15, 1/3.', 2, TOP['pmf'], K5 + '6')
    B.mcq('f(x) = kx³ với x = 0, 1, 2, 3, 4 là hàm xác suất. Giá trị k là (Prob. 7)', '0.01', ['0.1', '0.001', '1/64'], 'Σx³ = 0 + 1 + 8 + 27 + 64 = 100 ⇒ k = 1/100.', 1, TOP['pmf'], K5 + '7')
    B.mcq('Đường kính trục (X, mm) có mật độ f(x) = kx trên (0.9; 1.1). Giá trị k là (Prob. 9a)', '5', ['1', '10', '0.5'], '∫ kx dx = k(1.21 − 0.81)/2 = 0.2k = 1 ⇒ k = 5.', 2, TOP['pdf'], K5 + '9')
    P(B, rng, 'Với mật độ f(x) = 5x trên (0.9; 1.1), xác suất bề dày nằm giữa 0.95 và 1.05 là (Prob. 9b)', Q(lambda x: 5 * x, 0.95, 1.05), 'P = 5·(1.05² − 0.95²)/2 = 5·0.1 = 0.5000.', 2, TOP['pdf'], K5 + '9', extra=[0.1, 0.2, 0.25], d=4)
    B.mcq('Đường kính trục có mật độ đều k trên [119.9; 120.1]. Lô 500 trục: xấp xỉ bao nhiêu trục bị lỗi nếu lỗi là mỏng hơn 119.91 hoặc dày hơn 120.09? (Prob. 10)', '50', ['10', '100', '5'], 'k = 1/0.2 = 5. P(lỗi) = 5·0.01 + 5·0.01 = 0.1 ⇒ 500·0.1 = 50.', 2, TOP['pdf'], K5 + '10')
    P(B, rng, 'Tuổi thọ bóng đèn (đơn vị 1000 giờ) có mật độ f(x) = 6[0.25 − (x − 1.5)²], 1 ≤ x ≤ 2. Xác suất cả ba bóng không phải thay trong 1500 giờ đầu (độc lập) là (Prob. 11)', 0.125, 'Mật độ đối xứng quanh 1.5 nên P(X > 1.5) = 0.5 cho mỗi bóng ⇒ 0.5³ = 0.125.', 3, TOP['pdf'], K5 + '11', extra=[0.5, 0.25, 0.875], d=3)
    B.mcq('Hộp đựng dầu: nội dung Y = 100 + X (gallon), X có mật độ f(x) = 1 − |x| với |x| ≤ 1. Trong lô 1000 hộp, khoảng bao nhiêu hộp chứa từ 100 gallon trở lên? (Prob. 13)', '500', ['250', '750', '1000'], 'Mật độ tam giác đối xứng qua 0 nên P(X ≥ 0) = 0.5 ⇒ khoảng 500 hộp.', 2, TOP['pdf'], K5 + '13')
    B.mcq('Với mật độ f(x) = 1 − |x| trên [−1, 1], xác suất hộp chứa ít hơn 99.5 gallon (X < −0.5) là (Prob. 13)', '0.125', ['0.25', '0.5', '0.0625'], 'P(X < −0.5) = ∫_{−1}^{−0.5}(1 + x)dx = 0.5²/2 = 0.125. (Ít hơn 99 gallon: X < −1 ⇒ 0.)', 3, TOP['pdf'], K5 + '13')
    B.mcq('X là số lần gieo súc sắc cho đến khi mặt 6 xuất hiện lần đầu. Hàm xác suất của X (Prob. 14) là', 'f(x) = (5/6)^{x−1}·(1/6), x = 1, 2, 3, …', ['f(x) = (1/6)^{x}', 'f(x) = (5/6)·(1/6)^{x−1}', 'f(x) = C(x,1)(1/6)(5/6)^{x}'], 'x − 1 lần đầu không phải 6 (mỗi lần 5/6) rồi một lần ra 6 (1/6): phân phối hình học; Σ = (1/6)/(1 − 5/6) = 1.', 2, TOP['pmf'], K5 + '14')
    # ================= D. Kreyszig PS 24.6 =================
    K6 = 'Kreyszig PS 24.6, Prob. '
    B.mcq('f(x) = kx trên [0, 2]. Kỳ vọng và phương sai là (Prob. 1)', 'μ = 4/3, σ² = 2/9', ['μ = 1, σ² = 1/3', 'μ = 4/3, σ² = 4/9', 'μ = 2/3, σ² = 2/9'], 'k = 1/2; μ = ∫x²/2 = 4/3; E(X²) = ∫x³/2 = 2; σ² = 2 − 16/9 = 2/9.', 2, TOP['var'], K6 + '1')
    B.mcq('X phân phối đều trên [0, 2π]. Kỳ vọng và phương sai là (Prob. 3)', 'μ = π, σ² = π²/3', ['μ = π/2, σ² = π²/12', 'μ = 2π, σ² = π²/3', 'μ = π, σ² = π²/12'], 'Đều trên [a, b]: μ = (a + b)/2 = π; σ² = (b − a)²/12 = 4π²/12 = π²/3.', 2, TOP['var'], K6 + '3')
    B.mcq('Với Y = √3(X − μ)/π trong đó X đều trên [0, 2π], Y có kỳ vọng và phương sai (Prob. 4)', '0 và 1', ['0 và 3', 'π và 1', '0 và 1/3'], 'Y là chuẩn hoá: E(Y) = 0; Var(Y) = (3/π²)·Var(X) = (3/π²)(π²/3) = 1.', 3, TOP['var'], K6 + '4')
    B.mcq('f(x) = 4e^{−4x} với x ≥ 0. Kỳ vọng và phương sai là (Prob. 5)', 'μ = 1/4, σ² = 1/16', ['μ = 4, σ² = 16', 'μ = 1/4, σ² = 1/4', 'μ = 1/2, σ² = 1/16'], 'Mũ tham số λ = 4: μ = 1/λ, σ² = 1/λ².', 2, TOP['var'], K6 + '5')
    B.mcq('f(x) = k(1 − x²) trên [−1, 1]. Giá trị k, kỳ vọng và phương sai là (Prob. 6)', 'k = 3/4, μ = 0, σ² = 1/5', ['k = 1/2, μ = 0, σ² = 1/3', 'k = 3/4, μ = 1/2, σ² = 1/5', 'k = 3/2, μ = 0, σ² = 1/10'], '∫(1 − x²) = 4/3 ⇒ k = 3/4; hàm chẵn nên μ = 0; E(X²) = (3/4)(2/3 − 2/5) = 1/5.', 3, TOP['var'], K6 + '6')
    P(B, rng, 'f(x) = C·e^{−x²/2} với x ≥ 0. Hằng số C (Prob. 7) là', math.sqrt(2 / math.pi), '∫₀^∞ e^{−x²/2} dx = √(π/2) ⇒ C = √(2/π) ≈ 0.7979 (nửa phân phối chuẩn).', 3, TOP['pdf'], K6 + '7', extra=[1 / math.sqrt(2 * math.pi), 0.5, 1.0], d=4)
    B.mcq('X là số lần tung đồng xu cân đối cho đến khi xuất hiện mặt ngửa đầu tiên. Kỳ vọng μ (Prob. 8) là', '2', ['1', '1/2', '4'], 'Hình học tham số p = 1/2: μ = 1/p = 2 (Σ x·(1/2)^x = 2).', 2, TOP['mean'], K6 + '8')
    k9 = 1 / Q(lambda x: (x - 0.9) * (1.1 - x), 0.9, 1.1)
    B.mcq('f(x) = k(x − 0.9)(1.1 − x) với 0.9 < x < 1.1. Giá trị k, μ và σ² (Prob. 9) là', f'k = {k9:.0f}, μ = 1, σ² = 0.002', ['k = 5, μ = 1, σ² = 0.01', 'k = 750, μ = 1.1, σ² = 0.002', 'k = 750, μ = 1, σ² = 0.2'], f'∫(x − 0.9)(1.1 − x)dx = 0.2³/6 = 1/750 ⇒ k = 750. Đối xứng quanh 1 ⇒ μ = 1; σ² = ∫750(x − 1)²(…) = (0.2)²/20 = 0.002.', 3, TOP['var'], K6 + '9')
    pdef = 1 - Q(lambda x: k9 * (x - 0.9) * (1.1 - x), 0.94, 1.06)
    P(B, rng, 'Với mật độ ở Prob. 9, bu-lông là lỗi nếu lệch quá 0.06 cm so với 1.00 cm. Tỉ lệ lỗi (Prob. 10) là', pdef, f'P(|X − 1| > 0.06) = 1 − ∫_{{0.94}}^{{1.06}} 750(x − 0.9)(1.1 − x)dx = {f(pdef,4)} ≈ {pdef*100:.1f}%.', 3, TOP['pdf'], K6 + '10', extra=[0.06, 0.12, 0.3], d=4)
    B.mcq('Tổng số chấm kỳ vọng khi gieo một súc sắc cân đối 20 lần (Prob. 12) là', '70', ['60', '35', '3.5'], 'E(tổng) = 20·E(X) = 20·3.5 = 70 (tuyến tính của kỳ vọng).', 1, TOP['mean'], K6 + '12')
    B.mcq('Cửa hàng bán X máy lạnh mỗi ngày với P(10) = 0.1, P(11) = 0.3, P(12) = 0.4, P(13) = 0.2. Lợi nhuận mỗi máy $55. Lợi nhuận kỳ vọng mỗi ngày là (Prob. 13)', '$643.50', ['$55.00', '$660.00', '$11.70'], 'E(X) = 1.0 + 3.3 + 4.8 + 2.6 = 11.7 máy; lợi nhuận = 11.7·55 = 643.5.', 2, TOP['mean'], K6 + '13')
    B.mcq('X đều trên [−1, 1]. Kỳ vọng E(X²) (Prob. 14) bằng', '1/3', ['0', '1/2', '1'], 'E(X²) = ∫_{−1}^{1} x²·(1/2)dx = 1/3.', 2, TOP['mean'], K6 + '14')
    B.mcq('James gieo 2 súc sắc; Harry trả k cent với k là tích hai mặt. James phải trả Harry bao nhiêu mỗi ván để công bằng (Prob. 17)?', '12.25 cent', ['21 cent', '3.5 cent', '7 cent'], 'Hai súc sắc độc lập: E(XY) = E(X)E(Y) = 3.5² = 12.25.', 3, TOP['mean'], K6 + '17')
    B.mcq('Tuổi thọ bóng đèn X (giờ) có mật độ f(x) = 0.001e^{−0.001x}, x ≥ 0. Tuổi thọ trung bình là (Prob. 18)', '1000 giờ', ['100 giờ', '0.001 giờ', '10 000 giờ'], 'Mũ λ = 0.001 ⇒ μ = 1/λ = 1000.', 1, TOP['mean'], K6 + '18')
    B.mcq('f(0) = f(3) = 1/8, f(1) = f(2) = 3/8. E(X³) (Prob. 19) bằng', '6.75', ['3.375', '13.5', '1.5'], 'E(X³) = 0·1/8 + 1·3/8 + 8·3/8 + 27·1/8 = (3 + 24 + 27)/8 = 54/8 = 6.75.', 2, TOP['mean'], K6 + '19')
    # lý thuyết
    S2 = 'Lecture Notes §1.8–1.9 / Kreyszig §24.5–24.6'
    B.mcq('Với BNN rời rạc, tính chất nào của hàm xác suất f(x) là bắt buộc?', 'f(xⱼ) ≥ 0 và Σ f(xⱼ) = 1', ['∫f = 1 và f ≤ 1', 'f(x) ≤ 0', 'Σ f(xⱼ) có thể lớn hơn 1'], 'Hàm xác suất không âm và tổng bằng 1.', 1, TOP['pmf'], S2)
    B.mcq('Với BNN liên tục, tính chất nào đúng?', 'f(x) ≥ 0, ∫f = 1 và P(X = a) = 0', ['f(x) ≤ 1 và P(X = a) > 0', 'Σ f = 1', 'F(x) giảm'], 'Mật độ có thể lớn hơn 1 (ví dụ f = 5 ở Prob. 9); xác suất tại một điểm bằng 0, xác suất của khoảng bằng diện tích.', 2, TOP['pdf'], S2)
    B.mcq('Hàm phân phối F(x) = P(X ≤ x) có tính chất nào?', 'Không giảm, F(−∞) = 0, F(+∞) = 1, P(a < X ≤ b) = F(b) − F(a)', ['F giảm dần', 'F(+∞) = 0', 'F(x) ≤ 0'], 'Các tính chất cơ bản của hàm phân phối.', 1, TOP['pdf'], S2)
    B.mcq('Công thức tính nhanh phương sai nào đúng?', 'Var(X) = E(X²) − [E(X)]²', ['Var(X) = E(X) − E(X²)', 'Var(X) = E(X²) + [E(X)]²', 'Var(X) = [E(X)]² − E(X²)'], 'σ² = E[(X − μ)²] = E(X²) − 2μ·μ + μ² = E(X²) − μ² (Kreyszig PS 24.6 Prob. 20a).', 1, TOP['var'], S2)
    B.mcq('Nếu Y = aX + b thì E(Y) và Var(Y) là:', 'E(Y) = aE(X) + b, Var(Y) = a²Var(X)', ['E(Y) = aE(X), Var(Y) = aVar(X) + b', 'E(Y) = aE(X) + b, Var(Y) = aVar(X) + b', 'E(Y) = E(X) + b, Var(Y) = Var(X)'], 'Cộng hằng số không đổi độ phân tán; nhân a nhân phương sai với a².', 2, TOP['var'], S2)
    B.essay('Đề thi 2TC: X = 0..5 với P = 0.10, 0.20, 0.25, 0.35, 0.06, 0.04. Tính E(X) và Var(X).', f'E(X) = {f(dmean(xs,sets[0][0]),3)}; E(X²) = {f(sum(x*x*p for x,p in zip(xs,sets[0][0])),3)}; Var(X) = {f(dvar(xs,sets[0][0]),4)}.', 2, TOP['var'], 'Đề cuối kỳ 2022–2023 HK1, đề số 1, câu 1')
    B.essay('Đề thi HK2 (3TC): f(x) = 6(1 − x)x trên [0, 1]. Tính E(X) và tìm m với P(X ≤ m) = 50%.', 'E(X) = ∫₀¹ 6x²(1 − x)dx = 6(1/3 − 1/4) = 1/2. F(m) = 3m² − 2m³ = 1/2 ⇒ m = 1/2 (mật độ đối xứng qua 1/2).', 2, TOP['mean'], 'Đề cuối kỳ 2022–2023 HK2, đề số 1, câu 5')
    B.essay('Đề thi HK2: f(x) = 0.75(2 − x)x trên [0, 2]. Kiểm tra là mật độ; tính E(X) và trung vị.', 'Chuẩn hóa: 0.75(2·2²/2 − 2³/3) = 0.75·(4 − 8/3) = 1. E(X) = 1, trung vị 1 (đối xứng qua 1).', 2, TOP['mean'], 'Đề cuối kỳ 2022–2023 HK2, đề số 2, câu 5')
    B.essay('Bài 1.26–1.28 (Lecture Notes): tìm c cho mật độ (3/4)(1 − x²); đạo hàm F(x) = 1 − e^{−3x}; mật độ từ F(x) = (x² − 4)/5.', f'1.26: 1.5c − 0.5c³ = 0.95 ⇒ c ≈ {f(c126,4)}. 1.27: f = 3e^{{−3x}}, x = ln 10/3 = {f(x127,4)}. 1.28: f = 2x/5 trên [2,3); P(2.5 ≤ X ≤ 5) = 0.55.', 3, TOP['pdf'], S + 'Bài 1.26–1.28')
    B.essay('Bài 1.29–1.30 (Lecture Notes): tính trung bình và phương sai cho (a) súc sắc; (b) f(0..3) = 0.512, 0.384, 0.096, 0.008; (c) f = 2x trên [0,1]; (d) f = 6x(1 − x).', f'(a) 3.5; 35/12. (b) 0.6; 0.48. (c) 2/3; 1/18. (d) 0.5; {f(v130,4)}, σ = {f(math.sqrt(v130),4)}; dung tích để xác suất bán hết 5%: c ≈ {f(c130,4)}.', 2, TOP['var'], S + 'Bài 1.29–1.30')
    B.essay('Kreyszig PS 24.5/6: hộp 4 ốc phải, 6 ốc trái, rút 2 không hoàn lại; X là số ốc trái. Lập bảng phân phối, tính các xác suất yêu cầu.', 'P(X=0) = 6/45 = 2/15; P(X=1) = 24/45 = 8/15; P(X=2) = 15/45 = 1/3; P(1 ≤ X ≤ 2) = 39/45 = 13/15; P(X ≥ 1) = 13/15; P(X > 1) = 1/3; P(0.5 < X < 10) = 13/15.', 2, TOP['pmf'], K5 + '6')
    B.essay('Kreyszig PS 24.6/9–11: f(x) = k(x − 0.9)(1.1 − x) trên (0.9; 1.1); tìm k, μ, σ², tỉ lệ lỗi khi lệch > 0.06 cm.', f'k = 750; μ = 1; σ² = 0.002; tỉ lệ lỗi = {f(pdef,4)}.', 3, TOP['var'], K6 + '9–11')
