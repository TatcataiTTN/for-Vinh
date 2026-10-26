"""Module 5 — mở rộng: câu khái niệm (viết tay) + họ bài tính (đáp án tự tính, nhãn bo_sung)."""
import math, random
from scipy import integrate
from qb import f, fg, nd, ni
from qh import pm
from orig_m05 import TOP, dmean, dvar
SRC = 'Bổ sung: dạng bài §1.7–1.9 / Kreyszig PS 24.5–24.6 (đáp án tự tính bằng công thức, đối chiếu tích phân số)'
def build(B):
    rng = random.Random(2505)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    # ── khái niệm viết tay ──
    C('Biến ngẫu nhiên X là', 'một hàm số gán mỗi kết quả của phép thử một số thực', ['một xác suất của biến cố', 'một tập hợp các kết quả', 'một số cố định biết trước khi thử'], 'Định nghĩa: X: S → ℝ.', 1, 'rv')
    C('BNN nào sau đây là liên tục?', 'Thời gian chờ xe buýt (phút)', ['Số cuộc gọi đến tổng đài trong 1 giờ', 'Số mặt sấp khi tung 3 đồng xu', 'Số lỗi in trên một trang'], 'Thời gian đo được trên một khoảng; còn lại là đếm được (rời rạc).', 1, 'rv')
    C('BNN nào sau đây là rời rạc?', 'Số sinh viên đi học muộn trong một lớp', ['Cân nặng của một sinh viên', 'Nhiệt độ phòng', 'Điện áp đo được'], 'Số sinh viên là số nguyên đếm được.', 1, 'rv')
    C('Với BNN liên tục X, P(X = a) bằng', '0', ['f(a)', '1', 'F(a)'], 'Diện tích dưới đường cong tại một điểm bằng 0; f(a) chỉ là mật độ, không phải xác suất.', 1, 'pdf')
    C('Hàm mật độ f(x) của BNN liên tục', 'có thể nhận giá trị lớn hơn 1', ['luôn nhỏ hơn hoặc bằng 1', 'luôn là hàm tăng', 'bằng xác suất P(X = x)'], 'Chỉ cần f ≥ 0 và ∫f = 1; ví dụ f(x) = 2 trên [0, 0.5].', 2, 'pdf')
    C('Tính chất nào KHÔNG đúng với hàm phân phối F(x)?', 'F(x) có thể giảm', ['F(x) không giảm', 'F(−∞) = 0 và F(+∞) = 1', '0 ≤ F(x) ≤ 1'], 'F là xác suất tích lũy nên không bao giờ giảm.', 1, 'pdf')
    C('Với X rời rạc, đồ thị hàm phân phối F(x) có dạng', 'bậc thang, nhảy tại các giá trị xⱼ', ['đường cong trơn tăng liên tục', 'đường thẳng', 'chuỗi các điểm rời nhau'], 'Bước nhảy tại xⱼ bằng f(xⱼ).', 1, 'pmf')
    C('Công thức đúng để tính P(a < X ≤ b) là', 'F(b) − F(a)', ['F(a) − F(b)', 'F(b) + F(a)', 'f(b) − f(a)'], 'Xác suất khoảng = hiệu của hàm phân phối.', 1, 'pdf')
    C('Phương sai Var(X) được tính nhanh bằng', 'E(X²) − [E(X)]²', ['E(X²) − E(X)', '[E(X)]² − E(X²)', 'E(X) − E(X²)'], 'Var = E(X²) − μ².', 1, 'var')
    C('Phương sai Var(X) luôn', 'không âm', ['dương', 'nhỏ hơn kỳ vọng', 'bằng độ lệch chuẩn'], 'Var là kỳ vọng của bình phương nên ≥ 0, bằng 0 khi X là hằng.', 1, 'var')
    C('Nếu Y = 5X − 3 thì Var(Y) bằng', '25·Var(X)', ['5·Var(X) − 3', '5·Var(X)', '25·Var(X) − 3'], 'Var(aX + b) = a²Var(X).', 1, 'var')
    C('Nếu Y = −2X + 1 thì độ lệch chuẩn σ_Y bằng', '2σ_X', ['−2σ_X', '4σ_X', '2σ_X + 1'], 'σ_Y = |a|σ_X = 2σ_X (độ lệch chuẩn không âm).', 2, 'var')
    C('E(X + Y) = E(X) + E(Y)', 'luôn đúng, không cần X, Y độc lập', ['chỉ đúng khi X, Y độc lập', 'chỉ đúng khi X, Y cùng phân phối', 'chỉ đúng với BNN rời rạc'], 'Tính tuyến tính của kỳ vọng đúng mọi trường hợp.', 2, 'mean')
    C('Với X, Y độc lập, Var(X − Y) bằng', 'Var(X) + Var(Y)', ['Var(X) − Var(Y)', '|Var(X) − Var(Y)|', 'Var(X)·Var(Y)'], 'Phương sai của hiệu độc lập vẫn là tổng các phương sai.', 2, 'var')
    C('Bất đẳng thức Chebyshev cho biết điều gì?', 'Với mọi phân phối, P(|X − μ| < kσ) ≥ 1 − 1/k²', ['P(|X − μ| < kσ) = 1 − 1/k² chính xác', 'Chỉ đúng với phân phối chuẩn', 'P(|X − μ| < kσ) ≤ 1/k²'], 'Là cận dưới đúng cho mọi phân phối có phương sai hữu hạn.', 2, 'var')
    C('Trung vị m của BNN liên tục thỏa', 'F(m) = 0.5', ['f(m) = 0.5', 'F(m) = E(X)', 'm = E(X)'], 'Trung vị chia diện tích dưới mật độ làm hai nửa bằng nhau.', 1, 'quant')
    C('Nếu mật độ đối xứng qua điểm c thì', 'E(X) = c và trung vị = c', ['chỉ E(X) = c', 'chỉ trung vị = c', 'Var(X) = c'], 'Với phân phối đối xứng, kỳ vọng và trung vị đều bằng tâm đối xứng (nếu kỳ vọng tồn tại).', 2, 'quant')
    C('Với phân phối lệch phải (đuôi dài về phía lớn), thường có', 'trung bình > trung vị', ['trung bình < trung vị', 'trung bình = trung vị', 'trung bình = 0'], 'Đuôi phải kéo kỳ vọng lên cao hơn trung vị.', 2, 'quant')
    C('E[g(X)] với X rời rạc là', 'Σ g(xⱼ)f(xⱼ)', ['g(Σ xⱼf(xⱼ))', 'Σ g(xⱼ)', 'Σ xⱼ g(f(xⱼ))'], 'Kỳ vọng của hàm: tính g tại từng giá trị rồi lấy trung bình có trọng số.', 2, 'mean')
    C('Nói chung E(X²) so với [E(X)]² thì', 'E(X²) ≥ [E(X)]²', ['E(X²) ≤ [E(X)]²', 'luôn bằng nhau', 'không so sánh được'], 'Hệ quả của Var(X) = E(X²) − μ² ≥ 0.', 2, 'var')
    C('X ~ đều trên [a, b] thì Var(X) bằng', '(b − a)²/12', ['(b − a)²/4', '(b − a)/12', '(b + a)²/12'], 'Công thức chuẩn của phân phối đều.', 2, 'var')
    C('T ~ mũ tham số λ thì E(T) bằng', '1/λ', ['λ', '1/λ²', 'ln 2/λ'], 'Kỳ vọng của phân phối mũ là 1/λ; ln 2/λ là trung vị.', 1, 'mean')
    C('Với T ~ mũ(λ), tính chất “không nhớ” nghĩa là', 'P(T > s + t | T > s) = P(T > t)', ['P(T > s + t) = P(T > s) + P(T > t)', 'T luôn bằng 1/λ', 'P(T > t) = λt'], 'Đã chờ s rồi, xác suất chờ thêm t không phụ thuộc s.', 3, 'pdf')
    C('Để f(x) = kx trên [0, 2] (0 ngoài đoạn) là mật độ thì k bằng', '1/2', ['1', '1/4', '2'], '∫₀² kx dx = 2k = 1 ⇒ k = 1/2.', 1, 'pdf')
    C('Nếu X rời rạc nhận các giá trị 1, 2, 3 với xác suất 0.2, 0.5, 0.3 thì F(2) bằng', '0.7', ['0.5', '0.2', '1.0'], 'F(2) = P(X ≤ 2) = 0.2 + 0.5 = 0.7.', 1, 'pmf')
    C('Hai BNN có cùng kỳ vọng thì', 'chưa chắc cùng phương sai', ['chắc chắn cùng phương sai', 'chắc chắn cùng phân phối', 'chắc chắn cùng trung vị'], 'Kỳ vọng chỉ là tâm; độ phân tán có thể rất khác.', 1, 'var')
    C('Đơn vị của phương sai Var(X) khi X đo bằng mét là', 'm²', ['m', 'không có đơn vị', 'm³'], 'Phương sai là bình phương độ lệch; σ mới cùng đơn vị với X.', 1, 'var')
    C('Công thức nào đúng với BNN liên tục: f(x) = ?', "F′(x) tại các điểm F khả vi", ['F(x)·x', '∫F(x)dx', 'F(x)²'], 'Mật độ là đạo hàm của hàm phân phối.', 1, 'pdf')
    # ── bảng phân phối ngẫu nhiên: F, khoảng, E(g(X)) ──
    for t in range(12):
        xs = sorted(rng.sample(range(0, 12), rng.choice([4, 5])))
        w = [rng.randint(1, 9) for _ in xs]; s = sum(w); ps = [round(x / s, 2) for x in w]; ps[-1] = round(1 - sum(ps[:-1]), 2)
        if min(ps) <= 0: continue
        tab = ', '.join(f'P(X={x}) = {p}' for x, p in zip(xs, ps))
        i0 = rng.randrange(1, len(xs) - 1); x0 = xs[i0]; Fx = sum(p for x, p in zip(xs, ps) if x <= x0)
        P(f'X có bảng phân phối: {tab}. F({x0}) = P(X ≤ {x0}) bằng', Fx, f'Cộng các xác suất với x ≤ {x0}: {f(Fx,2)}.', 1, TOP['pmf'], SRC, extra=[Fx - ps[i0], 1 - Fx, ps[i0]], d=2)
        a, b = xs[0], xs[-1]; Pab = sum(p for x, p in zip(xs, ps) if a < x <= x0)
        P(f'X có bảng phân phối: {tab}. P({a} < X ≤ {x0}) bằng', Pab, f'F({x0}) − F({a}) = {f(Fx,2)} − {f(ps[0],2)} = {f(Pab,2)}.', 2, TOP['pmf'], SRC, extra=[Fx, Pab + ps[0], 1 - Pab], d=2)
        g = [(lambda x: x * x, 'X²'), (lambda x: 2 * x + 1, '2X + 1'), (lambda x: (x - 3) ** 2, '(X − 3)²')][t % 3]
        eg = sum(g[0](x) * p for x, p in zip(xs, ps))
        P(f'X có bảng phân phối: {tab}. E({g[1]}) bằng', eg, f'E({g[1]}) = Σ g(xᵢ)pᵢ = {f(eg,4)} (không phải g(E(X)) = {f(g[0](dmean(xs,ps)),4)}).', 3, TOP['mean'], SRC, extra=[g[0](dmean(xs, ps)), dmean(xs, ps)], d=3)
    # ── đa thức: phân vị, xác suất, F ──
    for a in [1, 2, 3, 4, 5]:
        # f = (a+1)x^a trên [0,1]  =>  F = x^(a+1)
        for p_ in (0.5, 0.9):
            q = p_ ** (1 / (a + 1))
            P(f'X có mật độ f(x) = {a+1}x^{a} trên [0, 1] (0 ở ngoài). Phân vị mức {int(p_*100)}% (x sao cho F(x) = {p_}) là', q, f'F(x) = x^{a+1} = {p_} ⇒ x = {p_}^(1/{a+1}) = {f(q,4)}.', 3, TOP['quant'], SRC, extra=[p_, p_ / (a + 1), 1 - q], d=4)
        c = 0.6; P(f'X có mật độ f(x) = {a+1}x^{a} trên [0, 1]. P(X > {c}) bằng', 1 - c ** (a + 1), f'1 − F({c}) = 1 − {c}^{a+1} = {f(1-c**(a+1),4)}.', 2, TOP['pdf'], SRC, extra=[c ** (a + 1), (a + 1) * c ** a, 1 - c], d=4)
        mu = (a + 1) / (a + 2); ex2 = (a + 1) / (a + 3); v = ex2 - mu * mu
        P(f'X có mật độ f(x) = {a+1}x^{a} trên [0, 1]. Độ lệch chuẩn σ là', math.sqrt(v), f'E(X) = {a+1}/{a+2}; E(X²) = {a+1}/{a+3}; Var = {f(v,5)}; σ = {f(math.sqrt(v),4)}.', 3, TOP['var'], SRC, extra=[v, mu, ex2], d=4)
    # ── hằng số k trên đoạn [a, b] với mật độ k(x−a)(b−x) ──
    for a, b in [(0, 2), (0, 3), (1, 4), (0, 1), (2, 6), (-1, 1)]:
        k = 6 / (b - a) ** 3; mid = (a + b) / 2; v = (b - a) ** 2 / 20
        P(f'X có mật độ f(x) = k(x − {a})({b} − x) trên [{a}, {b}] (đối xứng). Hằng số k là', k, f'∫ (x−a)(b−x) dx = (b−a)³/6 = {fg((b-a)**3/6)} ⇒ k = {f(k,5)}.', 2, TOP['pdf'], SRC, extra=[1 / (b - a), 6 / (b - a), 1 / ((b - a) ** 3)], d=4)
        P(f'X có mật độ f(x) = k(x − {a})({b} − x) trên [{a}, {b}] với k chuẩn hóa. Var(X) là', v, f'Mật độ này là Beta(2,2) giãn về [{a}, {b}]: Var = (b − a)²/20 = {f(v,4)}; kỳ vọng {fg(mid)}.', 3, TOP['var'], SRC, extra=[(b - a) ** 2 / 12, (b - a) ** 2 / 4, mid], d=4)
    # ── tổng độc lập, hiệu ──
    for k in range(10):
        m1, m2 = rng.randint(2, 12), rng.randint(2, 12); v1, v2 = rng.randint(1, 9), rng.randint(1, 9); a, b = rng.choice([2, 3, 4]), rng.choice([1, 2, 5])
        P(f'X, Y độc lập: E(X) = {m1}, Var(X) = {v1}; E(Y) = {m2}, Var(Y) = {v2}. Với W = {a}X − {b}Y, Var(W) là', a * a * v1 + b * b * v2, f'Var(W) = {a}²·{v1} + {b}²·{v2} = {a*a*v1+b*b*v2} (dấu trừ trước Y vẫn cộng phương sai).', 3, TOP['var'], SRC, extra=[a * a * v1 - b * b * v2, a * v1 + b * v2, a * a * v1 + b * v2], d=2, lo=None)
        P(f'X, Y độc lập: E(X) = {m1}, Var(X) = {v1}; E(Y) = {m2}, Var(Y) = {v2}. Với W = {a}X − {b}Y, E(W) là', a * m1 - b * m2, f'E(W) = {a}·{m1} − {b}·{m2} = {a*m1-b*m2}.', 2, TOP['mean'], SRC, extra=[a * m1 + b * m2, m1 - m2, a * m1], d=2, lo=None)
    # ── Chebyshev ──
    for mu, sg, kk in [(50, 5, 2), (100, 10, 3), (20, 2, 2.5), (60, 8, 1.5), (500, 40, 4), (12, 3, 2)]:
        lb = 1 - 1 / kk ** 2
        P(f'Biết μ = {mu}, σ = {sg} (không biết dạng phân phối). Cận dưới của P({fg(mu-kk*sg)} < X < {fg(mu+kk*sg)}) theo Chebyshev là', lb, f'Khoảng là μ ± {fg(kk)}σ nên P ≥ 1 − 1/{fg(kk)}² = {f(lb,4)}.', 2, TOP['var'], SRC, extra=[1 / kk ** 2, 1 - 1 / kk, 1 - sg / mu], d=4)
    # ── mũ ──
    for lam in [0.2, 0.5, 1, 2, 0.1]:
        for t0 in (1, 3):
            P(f'T ~ mũ(λ = {lam}). P(T > {t0}) bằng', math.exp(-lam * t0), f'P(T > t) = e^(−λt) = e^(−{fg(lam*t0)}) = {f(math.exp(-lam*t0),4)}.', 2, TOP['pdf'], SRC, extra=[1 - math.exp(-lam * t0), lam * t0, math.exp(-lam)], d=4)
        s0, t0 = 2, 3
        P(f'T ~ mũ(λ = {lam}). Biết T > {s0}, xác suất T > {s0 + t0} là', math.exp(-lam * t0), f'Không nhớ: P(T > {s0+t0} | T > {s0}) = P(T > {t0}) = e^(−{fg(lam*t0)}) = {f(math.exp(-lam*t0),4)}.', 3, TOP['pdf'], SRC, extra=[math.exp(-lam * (s0 + t0)), math.exp(-lam * s0), 1 - math.exp(-lam * t0)], d=4)
    # ── đều ──
    for a, b in [(0, 10), (5, 25), (-2, 6), (1, 5), (0, 60), (3, 9)]:
        x1 = a + (b - a) * 0.3; x2 = a + (b - a) * 0.8
        P(f'X đều trên [{a}, {b}]. P({fg(x1)} ≤ X ≤ {fg(x2)}) bằng', 0.5, f'Độ dài {fg(x2-x1)} chia cho {b-a} = 0.5.', 1, TOP['pdf'], SRC, extra=[0.3, 0.8, 0.2], d=3)
        P(f'X đều trên [{a}, {b}]. Độ lệch chuẩn σ là', (b - a) / math.sqrt(12), f'σ = (b − a)/√12 = {b-a}/3.4641 = {f((b-a)/math.sqrt(12),4)}.', 3, TOP['var'], SRC, extra=[(b - a) ** 2 / 12, (b - a) / 12, (b - a) / 2], d=4)
    # ── lãi kỳ vọng ──
    for k in range(10):
        xs = [rng.randint(5, 9) + i for i in range(4)]; w = [rng.randint(1, 5) for _ in xs]; s = sum(w); ps = [round(x / s, 2) for x in w]; ps[-1] = round(1 - sum(ps[:-1]), 2)
        if min(ps) <= 0: continue
        lai = rng.choice([20, 35, 50, 60]); chi = rng.choice([100, 150, 200]); m = dmean(xs, ps)
        tab = ', '.join(f'{x}: {p}' for x, p in zip(xs, ps))
        P(f'Số đơn hàng mỗi ngày X có phân phối (giá trị: xác suất) {tab}. Lãi {lai} nghìn/đơn, chi phí cố định {chi} nghìn/ngày. Lợi nhuận kỳ vọng mỗi ngày (nghìn) là', lai * m - chi, f'E(X) = {f(m,3)}; lợi nhuận = {lai}·{f(m,3)} − {chi} = {f(lai*m-chi,3)}.', 2, TOP['mean'], SRC, extra=[lai * m, lai * xs[0] - chi, (lai - chi) * m], d=3, lo=None)
    # ── chuỗi hình học f(x)=k/2^x, 3^x ──
    for base in (2, 3, 4):
        k = 1 - 1 / base
        P(f'X nhận giá trị 0, 1, 2, … với f(x) = k/{base}^x. Hằng số k là', k, f'Σ k/{base}^x = k·{base}/({base}−1) = 1 ⇒ k = {base-1}/{base}.', 2, TOP['pmf'], SRC, extra=[1 / base, 1 / (base + 1), 1 / (base - 1)], d=4)
        for n in (2, 3):
            P(f'X nhận giá trị 0, 1, 2, … với f(x) = k/{base}^x (k chuẩn hóa). P(X ≥ {n}) bằng', 1 / base ** n, f'P(X ≥ n) = (1/{base})^n = {f(1/base**n,4)}.', 3, TOP['pmf'], SRC, extra=[1 - 1 / base ** n, k / base ** n, 1 / base ** (n + 1)], d=4)
    # ── tự luận mở rộng ──
    B.essay('Cho X có bảng: P(X=1)=0.2, P(X=2)=0.3, P(X=3)=0.4, P(X=4)=0.1. Lập F(x), tính E(X), Var(X), σ và P(1 < X ≤ 3).', 'F: 0 (x<1); 0.2 (1≤x<2); 0.5 (2≤x<3); 0.9 (3≤x<4); 1 (x≥4). E(X) = 0.2+0.6+1.2+0.4 = 2.4; E(X²) = 0.2+1.2+3.6+1.6 = 6.6; Var = 6.6 − 5.76 = 0.84; σ = 0.9165. P(1<X≤3) = F(3) − F(1) = 0.9 − 0.2 = 0.7.', 2, TOP['mean'], SRC, 'bo_sung')
    B.essay('Cho f(x) = c(4 − x²) trên [−2, 2]. (a) Tìm c. (b) Tìm E(X), Var(X). (c) Tính P(|X| < 1).', '(a) ∫₋₂² (4 − x²)dx = 32/3 ⇒ c = 3/32. (b) Đối xứng nên E(X) = 0; E(X²) = c∫x²(4 − x²)dx = (3/32)(2·(4·8/3 − 32/5)) = (3/32)(2·(32/3 − 32/5)) = (3/32)(128/15) = 0.8; Var = 0.8. (c) P(|X|<1) = 2c∫₀¹(4 − x²)dx = 2(3/32)(11/3) = 11/16 = 0.6875.', 3, TOP['pdf'], SRC, 'bo_sung')
    B.essay('Thời gian sống T (năm) của một linh kiện có mật độ f(t) = 0.5e^(−0.5t), t ≥ 0. Tính E(T), σ, P(T > 4), trung vị và xác suất linh kiện đã sống 2 năm sẽ sống thêm ít nhất 4 năm.', 'Mũ λ = 0.5: E(T) = 2, σ = 2; P(T>4) = e^(−2) = 0.1353; trung vị = ln2/0.5 = 1.386; không nhớ: P(T>6 | T>2) = P(T>4) = 0.1353.', 3, TOP['pdf'], SRC, 'bo_sung')
    B.essay('Một trò chơi: tung xúc xắc, nếu ra 6 thắng 30 nghìn, ra 4 hoặc 5 thắng 6 nghìn, còn lại mất 9 nghìn. (a) Lập bảng phân phối lợi nhuận X. (b) Tính E(X), Var(X). (c) Trò chơi có công bằng không?', '(a) X = 30 (1/6), 6 (2/6), −9 (3/6). (b) E(X) = 5 + 2 − 4.5 = 2.5; E(X²) = 150 + 12 + 40.5 = 202.5; Var = 202.5 − 6.25 = 196.25. (c) E(X) = 2.5 > 0: không công bằng, có lợi cho người chơi.', 2, TOP['mean'], SRC, 'bo_sung')
    B.essay('X, Y độc lập với E(X) = 3, Var(X) = 4, E(Y) = −1, Var(Y) = 2. Tính E và Var của Z = 2X − 3Y + 5; tìm cận dưới P(|Z − E(Z)| < 10) theo Chebyshev.', 'E(Z) = 6 + 3 + 5 = 14; Var(Z) = 4·4 + 9·2 = 34; σ = 5.831. 10 = kσ ⇒ k = 1.715; cận dưới 1 − 1/k² = 1 − 0.34 = 0.66.', 3, TOP['var'], SRC, 'bo_sung')
    B.essay('f(x) = 2(1 − x) trên [0, 1]. Tìm F(x), E(X), trung vị và tứ phân vị thứ nhất.', 'F(x) = 2x − x². E(X) = ∫2x(1 − x)dx = 1/3. Trung vị: 2m − m² = 0.5 ⇒ m = 1 − 1/√2 = 0.2929. Q₁: x² − 2x + 0.25 = 0 ⇒ x = 1 − √0.75 = 0.1340.', 3, TOP['quant'], SRC, 'bo_sung')
    from ext_m05b import build as _b; _b(B)
