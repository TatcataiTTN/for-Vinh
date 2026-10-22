"""Module 6 — mở rộng: câu khái niệm (viết tay) + họ bài tính (đáp án tự tính bằng SciPy, nhãn bo_sung)."""
import math, random
from scipy import stats as st
from qb import f, fg
from qh import pm
from orig_m06 import TOP
SRC = 'Bổ sung: dạng bài §1.10 / Kreyszig PS 24.7–24.8 (đáp án tự tính bằng SciPy; chuẩn hóa z làm tròn 2 chữ số chỉ để minh họa)'
Phi = st.norm.cdf
def build(B):
    rng = random.Random(2506)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    # ── khái niệm ──
    C('Điều kiện KHÔNG thuộc phân phối nhị thức là', 'số phép thử n thay đổi ngẫu nhiên', ['các phép thử độc lập', 'xác suất thành công p không đổi', 'mỗi phép thử có hai kết quả'], 'Nhị thức đòi hỏi n cố định.', 1, 'binom')
    C('X ~ B(n, p) thì phương sai bằng', 'np(1 − p)', ['np', 'n(1 − p)', 'p(1 − p)'], 'Var = np(1 − p); np là kỳ vọng.', 1, 'binom')
    C('Rút 5 lá bài không hoàn lại từ bộ 52 lá, đếm số lá cơ. Biến này', 'không phải nhị thức vì các lần rút không độc lập', ['là nhị thức B(5, 1/4)', 'là Poisson', 'là chuẩn'], 'Không hoàn lại làm p thay đổi: đây là siêu bội.', 2, 'binom')
    C('Phân phối Poisson có đặc điểm nào sau đây?', 'Kỳ vọng bằng phương sai', ['Kỳ vọng gấp đôi phương sai', 'Phương sai bằng bình phương kỳ vọng', 'Kỳ vọng luôn bằng 1'], 'E(X) = Var(X) = μ.', 1, 'pois')
    C('Nếu trung bình 4 cuộc gọi/phút thì số cuộc gọi trong 3 phút có μ bằng', '12', ['4', '7', '1.33'], 'μ tỉ lệ với độ dài khoảng quan sát: 4 × 3 = 12.', 1, 'pois')
    C('Poisson xấp xỉ tốt nhị thức B(n, p) khi', 'n lớn và p nhỏ', ['n nhỏ và p lớn', 'p = 0.5', 'n = 1'], 'Giới hạn n → ∞, p → 0, np = μ.', 1, 'approx')
    C('Chuẩn tắc Z có', 'kỳ vọng 0 và phương sai 1', ['kỳ vọng 1 và phương sai 0', 'kỳ vọng 0 và phương sai 0', 'kỳ vọng 1 và phương sai 1'], 'Z ~ N(0, 1).', 1, 'normp')
    C('Với X ~ N(μ, σ²), chuẩn hóa là', 'Z = (X − μ)/σ', ['Z = (X − μ)/σ²', 'Z = (X − σ)/μ', 'Z = X/σ'], 'Chia cho độ lệch chuẩn σ, không phải σ².', 1, 'normp')
    C('Φ(−1.5) bằng', '1 − Φ(1.5)', ['Φ(1.5)', '−Φ(1.5)', '1 + Φ(1.5)'], 'Tính đối xứng của chuẩn tắc.', 1, 'normp')
    C('Với X liên tục, P(X ≤ 3) so với P(X < 3) thì', 'bằng nhau', ['P(X ≤ 3) lớn hơn', 'P(X < 3) lớn hơn', 'khác nhau tùy phân phối'], 'P(X = 3) = 0 với biến liên tục.', 1, 'normp')
    C('Khoảng μ ± 2σ của phân phối chuẩn chứa khoảng', '95% xác suất', ['68% xác suất', '99.7% xác suất', '50% xác suất'], 'Quy tắc 68–95–99.7: 2σ ⇒ 0.9545.', 1, 'theory')
    C('Muốn tìm c sao cho P(X ≥ c) = 0.01 với X chuẩn, ta giải', 'Φ((c − μ)/σ) = 0.99', ['Φ((c − μ)/σ) = 0.01', 'Φ(c) = 0.99', '(c − μ)/σ = 0.01'], 'P(X ≥ c) = 0.01 ⇒ P(X < c) = 0.99.', 2, 'normq')
    C('Giá trị tới hạn z để P(Z ≤ z) = 0.975 là', '1.96', ['1.645', '2.326', '2.576'], 'z₀.₉₇₅ = 1.96 (khoảng hai phía 95%).', 1, 'normq')
    C('Hiệu chỉnh liên tục khi xấp xỉ P(a ≤ X ≤ b) của nhị thức bằng chuẩn là', 'trừ 0.5 ở a, cộng 0.5 ở b', ['cộng 0.5 ở a, trừ 0.5 ở b', 'không cần hiệu chỉnh', 'nhân với 0.5'], 'Rời rạc x tương ứng khoảng [x − 0.5, x + 0.5].', 2, 'approx')
    C('Điều kiện thường dùng để xấp xỉ nhị thức bằng chuẩn là', 'np > 5 và n(1 − p) > 5', ['n < 30', 'p < 0.01', 'np = 1'], 'Cả hai đuôi đủ dài để đường chuông phù hợp.', 2, 'approx')
    C('Nếu X ~ N(10, 3²) và Y ~ N(5, 4²) độc lập thì X + Y có độ lệch chuẩn', '5', ['7', '25', '3.5'], 'Phương sai cộng: 9 + 16 = 25 ⇒ σ = 5.', 2, 'normp')
    C('Nếu X ~ N(10, 3²) và Y ~ N(5, 4²) độc lập thì X − Y có kỳ vọng và phương sai', '5 và 25', ['5 và −7', '15 và 25', '5 và 7'], 'Kỳ vọng trừ, phương sai vẫn cộng.', 2, 'normp')
    C('Trong phân phối chuẩn, tăng σ (giữ μ) làm đường chuông', 'thấp hơn và rộng hơn', ['cao hơn và hẹp hơn', 'dịch sang phải', 'không đổi'], 'Diện tích luôn bằng 1 nên σ lớn thì phân tán hơn, đỉnh thấp hơn.', 1, 'theory')
    C('Với B(100, 0.5), kỳ vọng và độ lệch chuẩn là', '50 và 5', ['50 và 25', '25 và 5', '50 và 50'], 'μ = np = 50; σ = √(100·0.25) = 5.', 1, 'binom')
    C('Đồ thị của B(n, 0.5) có dạng', 'đối xứng', ['lệch phải', 'lệch trái', 'đều'], 'p = 0.5 cho phân phối đối xứng quanh n/2.', 2, 'binom')
    # ── nhị thức ──
    for k in range(18):
        n = rng.choice([8, 10, 12, 15, 20, 25]); p = rng.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); x = rng.randint(1, n - 2)
        D = st.binom(n, p)
        kind = k % 3
        if kind == 0:
            P(f'X ~ B({n}; {p}). P(X = {x}) bằng', D.pmf(x), f'C({n},{x})·{p}^{x}·{fg(1-p)}^{n-x} = {f(D.pmf(x),4)}.', 1, TOP['binom'], SRC, extra=[D.cdf(x), D.sf(x), D.pmf(x + 1)], d=4)
        elif kind == 1:
            P(f'X ~ B({n}; {p}). P(X ≤ {x}) bằng', D.cdf(x), f'Cộng f(0) + … + f({x}) = {f(D.cdf(x),4)}.', 2, TOP['binom'], SRC, extra=[D.pmf(x), D.sf(x), D.cdf(x - 1)], d=4)
        else:
            P(f'X ~ B({n}; {p}). P(X ≥ {x}) bằng', D.sf(x - 1), f'1 − P(X ≤ {x-1}) = 1 − {f(D.cdf(x-1),4)} = {f(D.sf(x-1),4)}.', 2, TOP['binom'], SRC, extra=[D.sf(x), D.cdf(x), D.pmf(x)], d=4)
    for n, p in [(10, 0.3), (20, 0.25), (50, 0.1), (36, 0.5), (80, 0.05), (64, 0.25)]:
        P(f'X ~ B({n}; {p}). Độ lệch chuẩn σ bằng', math.sqrt(n * p * (1 - p)), f'σ = √(np(1 − p)) = √({fg(n*p*(1-p))}) = {f(math.sqrt(n*p*(1-p)),4)}.', 2, TOP['binom'], SRC, extra=[n * p * (1 - p), n * p, math.sqrt(n * p)], d=4)
    # ── Poisson ──
    for k in range(18):
        mu = rng.choice([0.5, 1, 1.5, 2, 3, 4, 6]); x = rng.randint(1, 5)
        D = st.poisson(mu); kind = k % 3
        if kind == 0:
            P(f'X ~ Poisson(μ = {mu}). P(X = {x}) bằng', D.pmf(x), f'μ^x e^(−μ)/x! = {fg(mu)}^{x}·e^(−{fg(mu)})/{math.factorial(x)} = {f(D.pmf(x),4)}.', 1, TOP['pois'], SRC, extra=[D.cdf(x), D.pmf(x - 1), D.sf(x)], d=4)
        elif kind == 1:
            P(f'X ~ Poisson(μ = {mu}). P(X ≤ {x}) bằng', D.cdf(x), f'Cộng f(0) … f({x}) = {f(D.cdf(x),4)}.', 2, TOP['pois'], SRC, extra=[D.pmf(x), D.sf(x), D.cdf(x - 1)], d=4)
        else:
            P(f'X ~ Poisson(μ = {mu}). P(X ≥ 1) bằng', 1 - math.exp(-mu), f'1 − P(X = 0) = 1 − e^(−{fg(mu)}) = {f(1-math.exp(-mu),4)}.', 2, TOP['pois'], SRC, extra=[math.exp(-mu), mu * math.exp(-mu), 1 - D.pmf(1)], d=4)
    for lam, t, x in [(2, 3, 4), (1.5, 2, 2), (0.5, 4, 1), (3, 0.5, 2), (4, 2, 6), (2.5, 4, 8)]:
        mu = lam * t; D = st.poisson(mu)
        P(f'Trung bình {lam} biến cố mỗi đơn vị thời gian. Xác suất đúng {x} biến cố trong {t} đơn vị thời gian là', D.pmf(x), f'μ = {lam}·{t} = {fg(mu)}; P(X = {x}) = {f(D.pmf(x),4)}.', 2, TOP['pois'], SRC, extra=[st.poisson(lam).pmf(x), D.cdf(x), D.pmf(x + 1)], d=4)
    for n, p in [(200, 0.01), (500, 0.004), (1000, 0.002), (150, 0.02), (300, 0.01), (120, 0.025)]:
        mu = n * p; x = int(round(mu)) + 1
        P(f'B({n}; {p}) xấp xỉ Poisson(np). P(X ≤ {x}) xấp xỉ bằng', st.poisson(mu).cdf(x), f'μ = np = {fg(mu)}; Poisson: P(X ≤ {x}) = {f(st.poisson(mu).cdf(x),4)} (nhị thức đúng {f(st.binom(n,p).cdf(x),4)}).', 2, TOP['approx'], SRC, extra=[st.binom(n, p).cdf(x - 1), st.poisson(mu).pmf(x), st.poisson(mu).cdf(x - 1)], d=4)
    # ── chuẩn: xác suất ──
    for k in range(24):
        mu = rng.choice([10, 50, 100, 12.5, 8.3, 44.4, 500]); sg = rng.choice([1, 2, 5, 0.8, 7.12, 15, 40]); sg = sg if sg < mu / 2 else mu / 8
        a = mu + rng.choice([-1.5, -1, -0.5, 0.5, 1, 1.5, 2]) * sg; b = a + rng.choice([0.5, 1, 1.5]) * sg
        kind = k % 3; za, zb = (a - mu) / sg, (b - mu) / sg
        D = st.norm(mu, sg)
        if kind == 0:
            P(f'X ~ N(μ = {fg(mu)}; σ = {fg(sg)}). P(X ≤ {fg(a,3)}) bằng', D.cdf(a), f'z = ({fg(a,3)} − {fg(mu)})/{fg(sg)} = {f(za,3)} ⇒ Φ(z) = {f(D.cdf(a),4)}.', 1, TOP['normp'], SRC, extra=[D.sf(a), Phi(-za), 0.5], d=4)
        elif kind == 1:
            P(f'X ~ N(μ = {fg(mu)}; σ = {fg(sg)}). P(X > {fg(a,3)}) bằng', D.sf(a), f'z = {f(za,3)} ⇒ 1 − Φ(z) = {f(D.sf(a),4)}.', 1, TOP['normp'], SRC, extra=[D.cdf(a), 0.5, Phi(za) - 0.5], d=4)
        else:
            P(f'X ~ N(μ = {fg(mu)}; σ = {fg(sg)}). P({fg(a,3)} < X < {fg(b,3)}) bằng', D.cdf(b) - D.cdf(a), f'z₁ = {f(za,3)}, z₂ = {f(zb,3)} ⇒ Φ(z₂) − Φ(z₁) = {f(D.cdf(b)-D.cdf(a),4)}.', 2, TOP['normp'], SRC, extra=[D.cdf(b), 1 - (D.cdf(b) - D.cdf(a)), D.sf(a)], d=4)
    # ── chuẩn: phân vị ──
    for k in range(16):
        mu = rng.choice([100, 12.5, 5, 50, 70, 8.3, 480]); sg = rng.choice([0.2, 0.4, 0.809, 2, 5, 15, 100]); sg = sg if sg < mu / 3 else mu / 10
        p = rng.choice([0.9, 0.95, 0.975, 0.99, 0.8, 0.7]); z = st.norm.ppf(p)
        if k % 2 == 0:
            P(f'X ~ N(μ = {fg(mu)}; σ = {fg(sg)}). Tìm c sao cho P(X ≤ c) = {p}', mu + sg * z, f'z = Φ⁻¹({p}) = {f(z,3)} ⇒ c = {fg(mu)} + {fg(sg)}·{f(z,3)} = {f(mu+sg*z,4)}.', 2, TOP['normq'], SRC, extra=[mu - sg * z, mu + sg * st.norm.ppf(1 - p), mu + z], d=4, lo=None)
        else:
            q = 1 - p
            P(f'X ~ N(μ = {fg(mu)}; σ = {fg(sg)}). Tìm c sao cho P(X ≥ c) = {f(q,3)}', mu + sg * z, f'P(X < c) = {f(p,3)} ⇒ z = {f(z,3)} ⇒ c = {f(mu+sg*z,4)}.', 3, TOP['normq'], SRC, extra=[mu - sg * z, mu + sg * st.norm.ppf(q), mu + sg * st.norm.ppf(q) + sg], d=4, lo=None)
    for mu, sg, g in [(50, 4, 0.9), (50, 4, 0.95), (100, 15, 0.99), (20, 2, 0.8), (7, 0.5, 0.95), (30, 6, 0.9)]:
        z = st.norm.ppf((1 + g) / 2)
        P(f'X ~ N(μ = {mu}; σ = {sg}). Tìm k sao cho P({mu} − k < X < {mu} + k) = {g}', sg * z, f'Φ(k/σ) = (1 + {g})/2 = {f((1+g)/2,3)} ⇒ k/σ = {f(z,3)} ⇒ k = {f(sg*z,4)}.', 3, TOP['normq'], SRC, extra=[sg * st.norm.ppf(g), z, sg * st.norm.ppf(g) / 2], d=4)
    # ── xấp xỉ chuẩn của nhị thức ──
    for n, p, a, b in [(100, 0.5, 45, 55), (400, 0.8, 300, 340), (200, 0.3, 50, 70), (150, 0.4, 55, 65), (64, 0.25, 12, 20), (300, 0.2, 50, 70), (80, 0.5, 35, 45), (500, 0.1, 40, 60)]:
        mu = n * p; sg = math.sqrt(n * p * (1 - p)); ap = Phi((b + 0.5 - mu) / sg) - Phi((a - 0.5 - mu) / sg)
        no = Phi((b - mu) / sg) - Phi((a - mu) / sg)
        P(f'X ~ B({n}; {p}). Dùng xấp xỉ chuẩn có hiệu chỉnh 0.5, P({a} ≤ X ≤ {b}) xấp xỉ bằng', ap, f'μ = {fg(mu)}, σ = {f(sg,3)}; Φ(({b}.5 − μ)/σ) − Φ(({a} − 0.5 − μ)/σ) = {f(ap,4)} (không hiệu chỉnh {f(no,4)}; đúng {f(st.binom(n,p).cdf(b)-st.binom(n,p).cdf(a-1),4)}).', 3, TOP['approx'], SRC, extra=[no, st.binom(n, p).cdf(b) - st.binom(n, p).cdf(a - 1) + 0.03, 1 - ap], d=4)
    # ── tổng chuẩn ──
    for m1, s1, m2, s2, c in [(20, 3, 30, 4, 55), (10, 2, 15, 3, 30), (100, 8, 50, 6, 160), (5, 1, 7, 2, 14), (60, 5, 40, 12, 90), (12, 2, 8, 1.5, 24)]:
        mt = m1 + m2; st_ = math.sqrt(s1 * s1 + s2 * s2)
        P(f'X ~ N({m1}; {s1}²) và Y ~ N({m2}; {s2}²) độc lập. P(X + Y > {c}) bằng', 1 - Phi((c - mt) / st_), f'X + Y ~ N({mt}; {fg(s1*s1+s2*s2)}), σ = {f(st_,3)}; z = {f((c-mt)/st_,3)}; P = {f(1-Phi((c-mt)/st_),4)}.', 3, TOP['normp'], SRC, extra=[Phi((c - mt) / st_), 1 - Phi((c - mt) / (s1 + s2)), 1 - Phi((c - mt) / (s1 * s1 + s2 * s2))], d=4)
    # ── tự luận ──
    B.essay('Một xạ thủ bắn trúng bia với xác suất 0.7 mỗi lần, độc lập. Bắn 10 lần. Tính P(trúng đúng 7), P(trúng ít nhất 8), E, σ và số lần trúng có khả năng nhất.', 'X ~ B(10, 0.7). P(7) = 120·0.7⁷·0.3³ = 0.2668. P(≥8) = 0.2335 + 0.1211 + 0.0282 = 0.3828. E = 7, σ = √2.1 = 1.449. Mode = ⌊11·0.7⌋ = 7.', 2, TOP['binom'], SRC, 'bo_sung')
    B.essay('Mỗi ngày trung bình có 3 xe vào một bãi đỗ nhỏ trong mỗi giờ cao điểm. (a) P(không có xe nào trong 30 phút)? (b) P(ít nhất 5 xe trong 2 giờ)?', '(a) μ = 1.5: P(0) = e^(−1.5) = 0.2231. (b) μ = 6: P(X ≥ 5) = 1 − P(X ≤ 4) = 1 − 0.2851 = 0.7149.', 2, TOP['pois'], SRC, 'bo_sung')
    B.essay('Cân nặng gói đường X ~ N(1000; 8²) gam. (a) Xác suất gói nhẹ hơn 985 g? (b) Cần đặt mức tối thiểu c để chỉ 2% gói nhẹ hơn c? (c) Xác suất trong 3 gói ngẫu nhiên có đúng 1 gói dưới 985 g?', '(a) z = −1.875, Φ = 0.0304. (b) z = −2.054, c = 1000 − 2.054·8 = 983.57 g. (c) B(3; 0.0304): 3·0.0304·0.9696² = 0.0857.', 3, TOP['normq'], SRC, 'bo_sung')
    B.essay('Tung đồng xu cân đối 200 lần. Dùng xấp xỉ chuẩn (hiệu chỉnh 0.5) tính P(90 ≤ X ≤ 110) và so với giá trị nhị thức đúng.', 'μ = 100, σ = √50 = 7.071. P ≈ Φ(1.485) − Φ(−1.485) = 0.8624 (đúng 0.8626; không hiệu chỉnh: 0.8427).', 3, TOP['approx'], SRC, 'bo_sung')
    B.essay('Lô hàng có 2% phế phẩm. Kiểm 150 sản phẩm: (a) Dùng Poisson tính P(không quá 2 phế phẩm). (b) So với nhị thức đúng.', 'μ = 3; Poisson: P(X ≤ 2) = e^(−3)(1 + 3 + 4.5) = 0.4232. Nhị thức B(150; 0.02) đúng: 0.4209. Hai kết quả khá gần nhau (sai khác 0.002).', 2, TOP['approx'], SRC, 'bo_sung')
