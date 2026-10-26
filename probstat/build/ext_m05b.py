"""Module 5 — mở rộng đợt 2: bảng đồng thời, hàm của BNN, mật độ phân đoạn, mũ, tổ hợp tuyến tính (đáp án tự tính)."""
import math, random
from fractions import Fraction as Fr
from scipy import integrate
from qb import f, fg
from qh import pm
from orig_m05 import TOP, dmean, dvar
SRC = 'Bổ sung: dạng bài §1.7–1.9 mở rộng (bảng đồng thời, hàm của BNN, tổ hợp tuyến tính; đáp án tự tính, đối chiếu tích phân số)'
def build(B):
    rng = random.Random(3505)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Phân phối biên của X từ bảng đồng thời thu được bằng cách', 'cộng xác suất đồng thời theo mọi giá trị của Y', ['nhân xác suất đồng thời với P(Y)', 'chia cho P(Y)', 'lấy giá trị lớn nhất'], 'P(X=x) = Σ_y P(X=x, Y=y).', 1, 'pmf')
    C('X, Y độc lập khi và chỉ khi', 'P(X=x, Y=y) = P(X=x)P(Y=y) với mọi (x, y)', ['Cov(X, Y) = 0', 'E(X) = E(Y)', 'Var(X) = Var(Y)'], 'Cov = 0 chỉ là điều kiện cần.', 2, 'var')
    C('Cov(X, Y) = 0 suy ra', 'chưa chắc X, Y độc lập', ['X, Y độc lập', 'X = Y', 'Var(X+Y) = 0'], 'Không tương quan khác độc lập.', 2, 'var')
    C('Hiệp phương sai Cov(X, Y) bằng', 'E(XY) − E(X)E(Y)', ['E(X)E(Y)', 'E(X+Y)', 'E(XY) + E(X)E(Y)'], 'Công thức tính nhanh.', 1, 'var')
    C('Var(aX + b) bằng', 'a²Var(X)', ['aVar(X) + b', 'a²Var(X) + b²', 'Var(X) + b'], 'Dịch không đổi phương sai; co giãn nhân a².', 1, 'var')
    C('Var(X + Y) với X, Y bất kỳ bằng', 'Var X + Var Y + 2Cov(X, Y)', ['Var X + Var Y', 'Var X · Var Y', 'Var X − Var Y'], 'Chỉ trùng Var X + Var Y khi Cov = 0.', 2, 'var')
    C('Y = g(X) với X rời rạc, nhiều giá trị x cho cùng y thì P(Y = y) bằng', 'tổng P(X = x) trên các x đó', ['tích các P(X = x)', 'giá trị lớn nhất', 'trung bình'], 'Biến cố {Y=y} là hợp của các {X=x}.', 2, 'pmf')
    C('Với BNN liên tục, để tìm mật độ của Y = g(X) đồng biến ta thường', 'viết F_Y(y) = F_X(g⁻¹(y)) rồi đạo hàm', ['thay x bằng g(x) trong f_X', 'nhân f_X với g', 'lấy tích phân f_X'], 'Phải qua hàm phân phối để có hệ số Jacobi.', 3, 'pdf')
    C('Tính chất không nhớ của phân phối mũ nói rằng', 'P(X > s + t | X > s) = P(X > t)', ['P(X > s + t) = P(X > s) + P(X > t)', 'P(X > t) = 1/2', 'E(X) = Var(X)'], 'Đã sống s không đổi xác suất sống thêm t.', 2, 'pdf')
    C('Phân phối mũ tham số λ có kỳ vọng', '1/λ', ['λ', 'λ²', 'ln 2/λ'], 'E = 1/λ và σ = 1/λ; trung vị là ln 2/λ.', 1, 'mean')
    C('Với phân phối lệch phải, thông thường', 'trung bình lớn hơn trung vị', ['trung bình nhỏ hơn trung vị', 'trung bình bằng mốt', 'trung vị bằng 0'], 'Đuôi dài phía lớn kéo trung bình lên.', 2, 'quant')
    C('Bất đẳng thức Chebyshev cho P(|X − μ| ≥ kσ) ≤', '1/k²', ['1/k', 'k²', 'σ/k'], 'Đúng với mọi phân phối có phương sai hữu hạn.', 1, 'var')
    C('Bất đẳng thức Markov P(X ≥ a) ≤ E(X)/a đòi hỏi', 'X không âm và a > 0', ['X chuẩn', 'X độc lập', 'a = E(X)'], 'Điều kiện X ≥ 0 là bắt buộc.', 2, 'mean')
    C('Với n BNN độc lập cùng phân phối (μ, σ), độ lệch chuẩn của trung bình X̄ là', 'σ/√n', ['σ√n', 'σ/n', 'σ'], 'Var(X̄) = σ²/n.', 1, 'var')
    C('Hệ số bất đối xứng dương cho biết phân phối', 'lệch phải', ['lệch trái', 'đối xứng', 'có kỳ vọng bằng 0'], 'γ = E[(X−μ)³]/σ³.', 2, 'var')
    # tìm tham số
    for _ in range(8):
        a = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3]); b = rng.choice([0.15, 0.2, 0.25, 0.3, 0.35]); c = round(1 - a - b - 0.1, 2)
        if c <= 0.04 or abs(a - b) < 1e-9: continue
        xs = [1, 2, 3, 4]; ps = [0.1, a, b, c]; mu = sum(x * p for x, p in zip(xs, ps))
        P(f'X nhận 1, 2, 3, 4 với P = 0.1; a; b; {c} và E(X) = {f(mu,3)}. Giá trị a bằng', a, f'a + b = {f(1-0.1-c,2)} và 2a + 3b = {f(mu-0.1-4*c,3)} ⇒ a = {f(a,2)}.', 3, TOP['mean'], SRC, extra=[b, c, 0.1], d=2)
    # Y = g(X)
    for t in range(8):
        k0 = rng.choice([1, 2, 3]); xs = [-1, 0, 1, 2, 3]; w = [rng.randint(1, 6) for _ in xs]; s = sum(w); ps = [round(x / s, 2) for x in w]; ps[-1] = round(1 - sum(ps[:-1]), 2)
        if min(ps) <= 0: continue
        EY = sum(p * (x - k0) ** 2 for x, p in zip(xs, ps)); EY2 = sum(p * (x - k0) ** 4 for x, p in zip(xs, ps)); V = EY2 - EY * EY
        tab = ', '.join(f'P(X={x}) = {p}' for x, p in zip(xs, ps))
        P(f'X có bảng: {tab}. Y = (X − {k0})². E(Y) bằng', EY, f'Σ (x − {k0})²p = {f(EY,4)}.', 2, TOP['mean'], SRC, extra=[sum((x - k0) * p for x, p in zip(xs, ps)) ** 2 + 0.5, sum(x * p for x, p in zip(xs, ps)), EY + 1], d=4)
        P(f'X có bảng: {tab}. Y = (X − {k0})². Var(Y) bằng', V, f'E(Y²) − [E(Y)]² = {f(EY2,4)} − {f(EY*EY,4)} = {f(V,4)}.', 3, TOP['var'], SRC, extra=[EY2, EY, EY * EY], d=4)
    # bảng đồng thời
    for _ in range(8):
        w = [rng.randint(1, 6) for _ in range(6)]; s = sum(w); J = [w_ / s for w_ in w]
        pxs = (sum(J[:3]), sum(J[3:])); pys = [J[0] + J[3], J[1] + J[4], J[2] + J[5]]
        exy = sum(J[3 + j] * (j + 1) for j in range(3)); ex = pxs[1]; ey = sum((j + 1) * pys[j] for j in range(3)); cov = exy - ex * ey
        tab = f'P(X=0,Y=1..3) = {", ".join(f(x,3) for x in J[:3])}; P(X=1,Y=1..3) = {", ".join(f(x,3) for x in J[3:])}'
        P(f'(X, Y) có phân phối đồng thời: {tab}. P(X = 1) bằng', pxs[1], f'Cộng hàng X=1: {f(pxs[1],4)}.', 1, TOP['pmf'], SRC, extra=[pxs[0], J[3], pys[0]], d=4)
        P(f'(X, Y) có phân phối đồng thời: {tab}. E(XY) bằng', exy, f'Chỉ các ô X = 1 đóng góp: Σ y·P(1, y) = {f(exy,4)}.', 2, TOP['mean'], SRC, extra=[ex * ey, ey, ex], d=4)
        if abs(cov) > 1e-4: P(f'(X, Y) có phân phối đồng thời: {tab}. Cov(X, Y) bằng', cov, f'E(XY) − E(X)E(Y) = {f(exy,4)} − {f(ex,4)}·{f(ey,4)} = {f(cov,4)}.', 3, TOP['var'], SRC, extra=[exy, ex * ey, -cov], d=4, lo=-1)
    # tổ hợp tuyến tính
    for _ in range(10):
        vx = rng.choice([2, 3, 4, 5, 9]); vy = rng.choice([1, 4, 6, 8, 9]); cv = rng.choice([-2, -1, 1, 2, 3]); a = rng.choice([2, 3, -2, 4]); b = rng.choice([-1, 1, 2, -3])
        V = a * a * vx + b * b * vy + 2 * a * b * cv
        if V <= 0: continue
        P(f'Var(X) = {vx}, Var(Y) = {vy}, Cov(X, Y) = {cv}. Var({a}X {"+" if b>0 else "−"} {abs(b)}Y) bằng', V, f'{a*a}·{vx} + {b*b}·{vy} + 2·({a})·({b})·{cv} = {V}.', 3, TOP['var'], SRC, extra=[a * a * vx + b * b * vy, V + 2 * cv, abs(a) * vx + abs(b) * vy], d=1)
    # mũ
    for lam in [0.2, 0.25, 0.5, 1, 2, 0.1, 0.4, 1.5]:
        t = rng.choice([1, 2, 3, 4]); s = rng.choice([1, 2, 5])
        P(f'T ~ Mũ(λ = {lam}). P(T > {t}) bằng', math.exp(-lam * t), f'e^(−λt) = e^(−{fg(lam*t)}) = {f(math.exp(-lam*t),4)}.', 2, TOP['pdf'], SRC, extra=[1 - math.exp(-lam * t), math.exp(-lam), lam * t], d=4)
        P(f'T ~ Mũ(λ = {lam}). Đã sống {s} đơn vị, P(sống thêm hơn {t} đơn vị | T > {s}) bằng', math.exp(-lam * t), f'Không nhớ: e^(−{fg(lam*t)}) = {f(math.exp(-lam*t),4)}.', 3, TOP['pdf'], SRC, extra=[math.exp(-lam * (t + s)), 1 - math.exp(-lam * t), math.exp(-lam * s)], d=4)
        P(f'T ~ Mũ(λ = {lam}). Trung vị của T bằng', math.log(2) / lam, f'ln 2/λ = {f(math.log(2)/lam,4)} (nhỏ hơn E = {f(1/lam,3)}).', 2, TOP['quant'], SRC, extra=[1 / lam, 0.5 / lam, math.log(2) * lam], d=4)
    # Chebyshev / n biến
    for mu, sg, k in [(50, 5, 2), (100, 10, 3), (20, 4, 2), (200, 15, 2.5), (60, 6, 1.5), (30, 3, 4)]:
        P(f'X có μ = {mu}, σ = {sg}. Cận Chebyshev cho P(|X − μ| ≥ {fg(k*sg)}) là', 1 / k ** 2, f'k = {fg(k*sg)}/{sg} = {fg(k)} ⇒ 1/k² = {f(1/k**2,4)}.', 2, TOP['var'], SRC, extra=[1 / k, sg / (k * sg), k * k / 10], d=4)
    for mu, sg, n in [(10, 3, 36), (50, 8, 64), (5, 2, 16), (100, 15, 25), (70, 12, 9), (8, 4, 100)]:
        P(f'X₁…X_{n} độc lập cùng phân phối, μ = {mu}, σ = {sg}. Độ lệch chuẩn của tổng S bằng', sg * math.sqrt(n), f'σ√n = {sg}·√{n} = {f(sg*math.sqrt(n),3)}.', 2, TOP['var'], SRC, extra=[sg / math.sqrt(n), sg * n, sg], d=3)
        P(f'X₁…X_{n} độc lập cùng phân phối, μ = {mu}, σ = {sg}. Độ lệch chuẩn của trung bình X̄ bằng', sg / math.sqrt(n), f'σ/√n = {sg}/√{n} = {f(sg/math.sqrt(n),3)}.', 2, TOP['var'], SRC, extra=[sg * math.sqrt(n), sg / n, sg], d=3)
    # tam giác
    for L in [2, 4, 6, 3, 10]:
        h = 2 / L; mid = L / 2
        P(f'X có mật độ tam giác trên [0, {L}], đỉnh tại x = {fg(mid)} (chiều cao {fg(h,3)}). P(X < {fg(mid)}) bằng', 0.5, 'Đối xứng quanh đỉnh nên P(X < đỉnh) = 0.5.', 1, TOP['pdf'], SRC, extra=[0.25, 1 / L, h], d=2)
        P(f'X có mật độ tam giác trên [0, {L}], đỉnh tại x = {fg(mid)}. E(X) bằng', mid, f'Đối xứng: E(X) = {fg(mid)}.', 1, TOP['mean'], SRC, extra=[mid / 2, L / 3, L], d=2)
        P(f'X có mật độ tam giác trên [0, {L}], đỉnh tại x = {fg(mid)}. Var(X) bằng', L * L / 24, f'Phương sai tam giác cân: L²/24 = {f(L*L/24,4)}.', 3, TOP['var'], SRC, extra=[L * L / 12, L * L / 36, L / 24], d=4)
    B.essay('Bảng đồng thời: P(0,1)=0.1, P(0,2)=0.2, P(0,3)=0.1, P(1,1)=0.2, P(1,2)=0.1, P(1,3)=0.3. Tìm phân phối biên, E(XY), Cov(X, Y), và cho biết X, Y có độc lập không.', 'X: 0.4; 0.6. Y: 0.3; 0.3; 0.4. E(X)=0.6, E(Y)=2.1, E(XY)=0.2·1+0.1·2+0.3·3=1.3, Cov = 1.3 − 1.26 = 0.04. P(0,1)=0.1 ≠ 0.4·0.3=0.12 nên không độc lập.', 3, TOP['var'], SRC, 'bo_sung')
    B.essay('f(x) = x trên [0, 1], f(x) = 2 − x trên (1, 2]. Tìm F(x), P(0.5 < X < 1.5), E(X) và Var(X).', 'F = x²/2 trên [0,1]; 1 − (2−x)²/2 trên (1,2]. P = 0.875 − 0.125 = 0.75. E(X) = 1, Var(X) = 1/6.', 3, TOP['pdf'], SRC, 'bo_sung')
    B.essay('X đều trên [0, 1], Y = X². Tìm F_Y, f_Y, E(Y), Var(Y) và so sánh E(Y) với [E(X)]².', 'F_Y(y) = √y; f_Y = 1/(2√y); E(Y) = 1/3; Var(Y) = 1/5 − 1/9 = 4/45. [E(X)]² = 1/4 ≠ 1/3 nên E(g(X)) ≠ g(E(X)).', 3, TOP['mean'], SRC, 'bo_sung')
    B.essay('Thiệt hại L (triệu): 0 (0.90), 100 (0.08), 500 (0.02); phí bảo hiểm 30 triệu. Tính E(L), σ_L; nhận xét có nên mua.', 'E(L) = 18; E(L²) = 5800; Var = 5476; σ = 74. Chi phí kỳ vọng khi mua (30) cao hơn khi không mua (18) nhưng bảo hiểm loại bỏ rủi ro σ = 74; quyết định phụ thuộc mức ngại rủi ro.', 3, TOP['mean'], SRC, 'bo_sung')
    B.essay('T ~ Mũ(0.5). Tính P(T > 3), P(T > 5 | T > 2), trung vị, E(T). Nêu ý nghĩa của kết quả so sánh hai xác suất đầu.', 'P(T > 3) = e^−1.5 = 0.2231; P(T > 5 | T > 2) = e^−1.5 = 0.2231 (không nhớ). Trung vị = 1.386; E(T) = 2.', 2, TOP['pdf'], SRC, 'bo_sung')
