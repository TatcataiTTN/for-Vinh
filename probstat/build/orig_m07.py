"""Module 7 — Mẫu ngẫu nhiên, đặc trưng mẫu, ước lượng điểm, hợp lý cực đại.
Gốc: Lecture Notes §2.1–2.2 (Ví dụ 2.2–2.4, Bài 2.1–2.4, 2.15–2.16), Kreyszig PS 25.2 (Prob. 3, 5, 8, 10–12), đề cuối kỳ (2024 câu 5 ×4; 2021–2022 câu 5 ×2)."""
import math, random
from qb import f, fg, nd
from qh import pm
TOP = {'sample': 'Mẫu và đặc trưng mẫu', 'group': 'Bảng tần số, dữ liệu theo lớp', 'point': 'Ước lượng điểm, tính không chệch', 'mle': 'Hợp lý cực đại (MLE)', 'theory': 'Lý thuyết'}
def mean_f(xs, ns): N = sum(ns); return sum(x * n for x, n in zip(xs, ns)) / N
def var_f(xs, ns):
    N = sum(ns); m = mean_f(xs, ns); return sum(n * (x - m) ** 2 for x, n in zip(xs, ns)) / (N - 1)
def build(B):
    rng = random.Random(707)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None)
        return pm(B_, r_, stem, v, *a, **k)
    S = 'Lecture Notes '
    # ---- Ví dụ 2.2: chiều cao 400 cây con ----
    mids = [7, 10.5, 12.5, 15, 18, 21, 24.5, 28]; rr = [18, 58, 62, 72, 57, 42, 36, 55]
    m = mean_f(mids, rr); v = var_f(mids, rr)
    tab = '[4.5; 9.5]: 18; (9.5; 11.5]: 58; (11.5; 13.5]: 62; (13.5; 16.5]: 72; (16.5; 19.5]: 57; (19.5; 22.5]: 42; (22.5; 26.5]: 36; (26.5; 29.5]: 55'
    P(B, rng, f'Chiều cao 400 cây con theo lớp (lớp: tần số) — {tab}. Điểm đại diện các lớp là 7, 10.5, 12.5, 15, 18, 21, 24.5, 28. Trung bình mẫu x̄ (cm) là', m, f'x̄ = (1/n)Σ xᵢrᵢ = 6920/400 = {f(m,2)} cm (Ví dụ 2.2).', 2, TOP['group'], S + 'Ví dụ 2.2', extra=[sum(mids) / 8, 15, 19.5], d=2)
    P(B, rng, f'Cùng mẫu 400 cây con (8 lớp, điểm đại diện 7; 10.5; 12.5; 15; 18; 21; 24.5; 28). Phương sai mẫu s² (cm²) là', v, f's² = (1/(n−1))Σ rᵢ(xᵢ − x̄)² = {f(sum(r*(x-m)**2 for x,r in zip(mids,rr)),2)}/399 = {f(v,2)} cm² (Ví dụ 2.2).', 3, TOP['group'], S + 'Ví dụ 2.2', extra=[sum(r * (x - m) ** 2 for x, r in zip(mids, rr)) / 400, math.sqrt(v), v + 1], d=2)
    # ---- Bài 2.1 ----
    xs = [21, 24, 26, 27, 29, 30, 32, 33]; ns = [10, 11, 13, 17, 20, 18, 15, 12]
    m1 = mean_f(xs, ns); v1 = var_f(xs, ns)
    P(B, rng, 'Mẫu (giá trị: tần số) 21:10, 24:11, 26:13, 27:17, 29:20, 30:18, 32:15, 33:12. Trung bình mẫu x̄ (Bài 2.1) là', m1, f'N = 116; Σxᵢnᵢ = {sum(a*b for a,b in zip(xs,ns))}; x̄ = {f(m1,4)}.', 2, TOP['group'], S + 'Bài 2.1', extra=[sum(xs) / 8, 29, 27.5], d=4)
    P(B, rng, 'Mẫu 21:10, 24:11, 26:13, 27:17, 29:20, 30:18, 32:15, 33:12. Độ lệch chuẩn mẫu s (Bài 2.1) là', math.sqrt(v1), f's² = {f(v1,4)}; s = {f(math.sqrt(v1),4)}.', 2, TOP['group'], S + 'Bài 2.1', extra=[v1, math.sqrt(sum(n * (x - m1) ** 2 for x, n in zip(xs, ns)) / 116), 3.0], d=4)
    # ---- Bài 2.2(a): tuổi thọ bóng đèn ----
    mids2 = [1010 + 20 * i for i in range(10)]; n2 = [3, 4, 7, 20, 40, 39, 25, 18, 9, 2]
    m2 = mean_f(mids2, n2); s2 = math.sqrt(var_f(mids2, n2))
    P(B, rng, 'Tuổi thọ bóng đèn (giờ): 1000–1020: 3; 1020–1040: 4; 1040–1060: 7; 1060–1080: 20; 1080–1100: 40; 1100–1120: 39; 1120–1140: 25; 1140–1160: 18; 1160–1180: 9; 1180–1200: 2. Trung bình mẫu x̄ là (Bài 2.2a)', m2, f'Điểm giữa lớp 1010, 1030, …, 1190; N = 167; x̄ = {f(m2,3)} giờ.', 2, TOP['group'], S + 'Bài 2.2(a)', extra=[1100, 1090, sum(mids2) / 10], d=3)
    P(B, rng, 'Cùng bảng tuổi thọ bóng đèn (10 lớp, N = 167). Độ lệch chuẩn mẫu s (giờ) là (Bài 2.2a)', s2, f's = {f(s2,3)} giờ (s² = {f(s2**2,2)}).', 3, TOP['group'], S + 'Bài 2.2(a)', extra=[s2 ** 2, 40.0, s2 * 1.1], d=3)
    # ---- Bài 2.15, 2.16 ----
    for nm, lo_, w, ns_, src in [('hao phí nhiên liệu (gram)', 19.0, 0.2, [7, 8, 18, 10], 'Bài 2.15'), ('chiều cao cây con (cm)', 16.5, 0.5, [3, 5, 11, 12, 6, 3], 'Bài 2.16')]:
        mids_ = [lo_ + w * (i + 0.5) for i in range(len(ns_))]; mm = mean_f(mids_, ns_); vv = var_f(mids_, ns_)
        P(B, rng, f'Bảng {nm}: các lớp rộng {w} bắt đầu từ {lo_} với tần số {", ".join(map(str,ns_))} (N = {sum(ns_)}). Trung bình mẫu x̄ là', mm, f'Điểm giữa lớp: {", ".join(fg(x,3) for x in mids_)}; x̄ = {f(mm,4)} ({src}).', 2, TOP['group'], S + src, extra=[sum(mids_) / len(mids_), lo_ + w * 2, mm + w / 2], d=4)
        P(B, rng, f'Bảng {nm}: các lớp rộng {w} bắt đầu từ {lo_} với tần số {", ".join(map(str,ns_))}. Phương sai mẫu s² là', vv, f's² = Σnᵢ(xᵢ − x̄)²/(N − 1) = {f(vv,5)} ({src}).', 3, TOP['group'], S + src, extra=[math.sqrt(vv), sum(n * (x - mm) ** 2 for x, n in zip(mids_, ns_)) / sum(ns_), vv * 2], d=5)
    # ---- MLE lý thuyết (Ví dụ 2.3, 2.4) ----
    B.mcq('Ước lượng hợp lý cực đại của xác suất p (hàm xác suất f(x; p) = pˣ(1 − p)^{1−x}, x ∈ {0, 1}) từ mẫu cỡ n là:', 'p̂ = x̄ = (x₁ + … + xₙ)/n (tần suất mẫu)', ['p̂ = 1 − x̄', 'p̂ = x̄/n', 'p̂ = x₁'], 'ln l = Σ[xᵢ ln p + (1 − xᵢ) ln(1 − p)]; đạo hàm bằng 0 ⇒ p = x̄ (Ví dụ 2.3).', 2, TOP['mle'], S + 'Ví dụ 2.3')
    B.mcq('MLE của μ và σ² của phân phối chuẩn từ mẫu cỡ n là:', 'μ̂ = x̄ và σ̂² = (1/n)Σ(xᵢ − x̄)² = s²(n − 1)/n', ['μ̂ = x̄ và σ̂² = s²', 'μ̂ = x̄ và σ̂² = (1/(n − 1))Σ(xᵢ − x̄)²', 'μ̂ = trung vị và σ̂² = s²'], 'Giải ∂ln l/∂μ = 0, ∂ln l/∂σ = 0 (Ví dụ 2.4): σ̂² chia cho n; vì thế MLE của σ² chệch, còn s² (chia n − 1) không chệch.', 3, TOP['mle'], S + 'Ví dụ 2.4 / Kreyszig PS 25.2 Prob. 1')
    B.mcq('Hàm hợp lý l(x₁, …, xₙ; θ) của một mẫu ngẫu nhiên (độc lập) được xác định bằng:', 'f(x₁; θ)·f(x₂; θ)·…·f(xₙ; θ)', ['f(x₁; θ) + … + f(xₙ; θ)', 'f(x̄; θ)', 'max f(xᵢ; θ)'], 'Các quan sát độc lập nên xác suất đồng thời là tích (công thức 2.3).', 1, TOP['mle'], S + '(2.3)')
    B.mcq('Điều kiện cần để θ̂ là ước lượng hợp lý cực đại là:', '∂l/∂θ = 0 (tương đương ∂ln l/∂θ = 0) tại θ̂', ['l(θ̂) = 0', '∂²l/∂θ² = 0', 'θ̂ = x̄ luôn luôn'], 'Công thức (2.4); dùng ln vì tích thành tổng và ln đơn điệu.', 1, TOP['mle'], S + '(2.4)')
    # ---- Bài 2.3, 2.4 ----
    B.mcq('X là số phép thử độc lập cho đến khi biến cố A xuất hiện, f(x) = p(1 − p)^{x−1}, x = 1, 2, …. MLE của p từ mẫu (x₁, …, xₙ) là (Bài 2.3 / Kreyszig PS 25.2/8)', 'p̂ = n/(x₁ + … + xₙ) = 1/x̄', ['p̂ = x̄', 'p̂ = 1 − 1/x̄', 'p̂ = n·x̄'], 'ln l = n ln p + (Σxᵢ − n) ln(1 − p); đạo hàm: n/p − (Σxᵢ − n)/(1 − p) = 0 ⇒ p̂ = n/Σxᵢ.', 3, TOP['mle'], S + 'Bài 2.3 / Kreyszig PS 25.2 Prob. 8')
    th = 5 / (0.5 + 0.7 + 0.1 + 1.1 + 0.1)
    P(B, rng, 'X có mật độ f(x) = θe^{−θx} (x ≥ 0); mẫu ngẫu nhiên 0.5; 0.7; 0.1; 1.1; 0.1. MLE của θ (Bài 2.4) là', th, f'θ̂ = n/Σxᵢ = 5/2.5 = {f(th,3)}.', 2, TOP['mle'], S + 'Bài 2.4', extra=[2.5, 0.5, 0.4], d=3)
    # ---- Kreyszig PS 25.2 ----
    K = 'Kreyszig PS 25.2, Prob. '
    B.mcq('Kreyszig 25.2/5: MLE của p của phân phối nhị thức từ x thành công trong n phép thử là', 'p̂ = x/n', ['p̂ = n/x', 'p̂ = x', 'p̂ = x/(n − 1)'], 'l = C(n,x)pˣ(1 − p)^{n−x}; ∂ln l/∂p = x/p − (n − x)/(1 − p) = 0 ⇒ p̂ = x/n.', 2, TOP['mle'], K + '5')
    P(B, rng, 'Gieo súc sắc: lần đầu ra “Sáu” ở lần gieo thứ 7, lần thứ hai ra ở lần thứ 6. Ước lượng hợp lý cực đại của p (xác suất ra Sáu) là (Kreyszig 25.2/10)', 2 / 13, 'Geometric: p̂ = n/Σxᵢ = 2/(7 + 6) = 2/13 ≈ 0.1538.', 2, TOP['mle'], K + '10', extra=[1 / 6, 1 / 7, 2 / 7], d=4)
    B.mcq('Mật độ f(x) = θe^{−θx} (x ≥ 0). Kỳ vọng μ = 1/θ. MLE của μ (Kreyszig 25.2/11–12) là', 'μ̂ = x̄ (bằng 1/θ̂, tính bất biến của MLE)', ['μ̂ = 1/x̄', 'μ̂ = x̄²', 'μ̂ = n·x̄'], 'θ̂ = 1/x̄ ⇒ μ̂ = 1/θ̂ = x̄: giống ước lượng trực tiếp trung bình mẫu.', 2, TOP['mle'], K + '11–12')
    # ---- Đề thi: MLE ----
    ys = [1.15, 2.05, 3.14, 4.22, 5.21, 6.04]; th6 = len(ys) / sum(ys)
    for k in (1, 2, 3, 4):
        P(B, rng, f'Y có mật độ f(x) = θe^{{−θx}} (x ≥ 0). P(Y ≤ {k}) theo θ bằng', 1 - math.exp(-th6 * k), f'P(Y ≤ {k}) = 1 − e^(−{k}θ) (tại θ̂ = {f(th6,4)}: {f(1-math.exp(-th6*k),4)}). Biểu thức theo θ: 1 − e^(−{k}θ).', 1, TOP['mle'], f'Đề mẫu 03/2024, đề số {k}, câu 5(a)', extra=[math.exp(-th6 * k), th6 * k, 1 - math.exp(-th6)], d=4) if False else B.mcq(f'Y có mật độ f(x) = θe^{{−θx}} (x ≥ 0). P(Y ≤ {k}) theo θ bằng', f'1 − e^(−{k}θ)' if k > 1 else '1 − e^(−θ)', [f'e^(−{k}θ)' if k > 1 else 'e^(−θ)', f'{k}θe^(−{k}θ)' if k > 1 else 'θe^(−θ)', f'1 − e^({k}θ)' if k > 1 else '1 − e^(θ)'], f'F(y) = ∫₀^{k} θe^(−θx)dx = 1 − e^(−{k}θ).', 1, TOP['mle'], f'Đề mẫu 03/2024, đề số {k}, câu 5(a)', 'goc')
    P(B, rng, 'Mẫu ngẫu nhiên của Y (mật độ θe^{−θx}): 1.15; 2.05; 3.14; 4.22; 5.21; 6.04. Ước lượng hợp lý cực đại của θ là', th6, f'θ̂ = n/Σyᵢ = 6/{f(sum(ys),2)} = {f(th6,4)} (đề mẫu 03/2024, cùng mẫu cho cả 4 đề).', 2, TOP['mle'], 'Đề mẫu 03/2024, đề số 1–4, câu 5(b)', extra=[sum(ys) / 6, 1 / 6, 6 / 21.81 * 2], d=4)
    for (a, b, src) in [(9, 2, 'Đáp án đề số 1 thi 22/12/2021'), (4, 3, 'Đáp án đề số 2 thi 22/12/2021')]:
        xs5 = [1.5, 2.5 + a, 3.5 + b, 4, 5, 6]; xb = sum(xs5) / 6; th5 = 1 / (2 * (xb - 1))
        P(B, rng, f'X có mật độ f(x) = 2θe^{{−2θ(x−1)}} (x ≥ 1). Mẫu: 1.5; {2.5+a}; {3.5+b}; 4; 5; 6. MLE của θ là (a = {a}, b = {b})', th5, f'ln l = n ln 2 + n ln θ − 2nθ(x̄ − 1) ⇒ θ̂ = 1/(2(x̄ − 1)); x̄ = {f(xb,4)} ⇒ θ̂ = {f(th5,4)} (đáp án chính thức {th5:.3f}).', 3, TOP['mle'], src + ', Câu 5', extra=[1 / xb, 1 / (xb - 1), 1 / (2 * xb)], d=3)
    # ---- Lý thuyết ước lượng ----
    S2 = 'Lecture Notes §2.1–2.2'
    B.mcq('Phương sai mẫu s² = (1/(n − 1))Σ(xᵢ − x̄)² là ước lượng của phương sai tổng thể σ² với tính chất:', 'Không chệch: E(s²) = σ²', ['Chệch xuống: E(s²) = (n − 1)σ²/n', 'Chệch lên: E(s²) = nσ²/(n − 1)', 'Luôn bằng σ²'], 'Chia cho n − 1 làm kỳ vọng của s² đúng bằng σ²; chia cho n thì chệch.', 2, TOP['point'], S2)
    B.mcq('Trung bình mẫu x̄ có kỳ vọng và phương sai (mẫu cỡ n từ tổng thể có μ, σ²):', 'E(x̄) = μ và Var(x̄) = σ²/n', ['E(x̄) = μ/n và Var(x̄) = σ²', 'E(x̄) = μ và Var(x̄) = σ²', 'E(x̄) = nμ và Var(x̄) = nσ²'], 'Định lý 2.1(b): x̄ ~ N(μ, σ²/n) khi các Xᵢ chuẩn độc lập.', 2, TOP['point'], S2 + ' (Định lý 2.1)')
    B.mcq('Tần suất mẫu f = (số lần A xảy ra)/n là ước lượng điểm của đại lượng nào?', 'Xác suất tổng thể p = P(A)', ['Phương sai tổng thể', 'Trung vị tổng thể', 'Cỡ mẫu'], 'Mục 2.2.3: với X = 1 nếu A xảy ra thì x̄ = f ước lượng p = E(X).', 1, TOP['point'], S2 + '§2.2.3')
    B.mcq('Khi cỡ mẫu n tăng, độ chính xác của ước lượng x̄ cho μ thay đổi thế nào (σ cố định)?', 'Tăng: độ lệch chuẩn của x̄ là σ/√n giảm', ['Giảm', 'Không đổi', 'Chỉ đổi khi σ đổi'], 'Sai số chuẩn σ/√n giảm theo √n: muốn giảm một nửa sai số phải tăng gấp 4 lần cỡ mẫu.', 1, TOP['point'], S2)
    B.mcq('“Tập nền” (tập hợp chính) và “mẫu” khác nhau ở chỗ:', 'Mẫu là một phần lấy từ tập nền, mang thông tin có thể khác nhau ở các mẫu khác nhau', ['Mẫu luôn lớn hơn tập nền', 'Tập nền do người nghiên cứu chọn', 'Hai khái niệm đồng nghĩa'], 'Nghiên cứu toàn bộ tập nền thường tốn kém hoặc không khả thi nên dùng mẫu (Mục 2.1.1).', 1, TOP['sample'], S2 + '§2.1.1')
    B.mcq('Ước lượng điểm của kỳ vọng μ của tổng thể từ mẫu x₁, …, xₙ là:', 'x̄ = (x₁ + … + xₙ)/n', ['s²', 'trung vị của n', 'x₁'], 'Theo mục 2.2.1: μ̂ = x̄ = (x₁ + … + xₙ)/n — dùng đặc trưng mẫu tương ứng làm ước lượng điểm.', 1, TOP['point'], S2 + ' (§2.2.1)')
    B.essay('Ví dụ 2.2 (Lecture Notes): mẫu 400 cây con theo 8 lớp; tính x̄ và s².', f'Điểm đại diện 7; 10.5; 12.5; 15; 18; 21; 24.5; 28. x̄ = 6920/400 = 17.3 cm; s² = {f(sum(r*(x-m)**2 for x,r in zip(mids,rr))/399,2)} cm².', 2, TOP['group'], S + 'Ví dụ 2.2')
    B.essay('Bài 2.1–2.2 (Lecture Notes): tính trung bình mẫu và độ lệch chuẩn cho hai bảng tần số.', f'2.1: x̄ = {f(m1,4)}, s = {f(math.sqrt(v1),4)}. 2.2(a): x̄ = {f(m2,3)} giờ, s = {f(s2,3)} giờ.', 2, TOP['group'], S + 'Bài 2.1–2.2')
    B.essay('Bài 2.3 và 2.4 (Lecture Notes): tìm MLE của p (hình học) và của θ (mũ) với mẫu 0.5, 0.7, 0.1, 1.1, 0.1.', 'Hình học: ln l = n ln p + (Σxᵢ − n) ln(1 − p) ⇒ p̂ = n/Σxᵢ. Mũ: ln l = n ln θ − θΣxᵢ ⇒ θ̂ = n/Σxᵢ = 5/2.5 = 2.', 3, TOP['mle'], S + 'Bài 2.3–2.4')
    B.essay('Đề mẫu 03/2024 câu 5: Y có mật độ θe^{−θx}; (a) P(Y ≤ 1) theo θ; (b) MLE của θ từ mẫu 1.15, 2.05, 3.14, 4.22, 5.21, 6.04.', f'(a) P(Y ≤ 1) = 1 − e^(−θ). (b) l(θ) = θⁿe^{{−θΣyᵢ}}; ln l = n ln θ − θΣyᵢ; θ̂ = n/Σyᵢ = 6/21.81 = {f(th6,4)}.', 2, TOP['mle'], 'Đề mẫu 03/2024, câu 5')
    B.essay('Đề 2021–2022 câu 5: f(x) = 2θe^{−2θ(x−1)} (x ≥ 1), mẫu 1.5; 2.5 + a; 3.5 + b; 4; 5; 6. Tìm MLE của θ.', f'ln l = n ln 2 + n ln θ − 2θΣ(xᵢ − 1) ⇒ θ̂ = n/(2Σ(xᵢ − 1)) = 1/(2(x̄ − 1)). Với a = 9, b = 2: x̄ = 5.5833 ⇒ θ̂ = 0.109.', 3, TOP['mle'], 'Đề cuối kỳ 2021–2022, câu 5')
    B.essay('Kreyszig PS 25.2/10–12: ước lượng p khi “Sáu” đầu tiên ở lần 7 và lần 6; MLE của μ = 1/θ.', 'p̂ = 2/(7 + 6) = 2/13 ≈ 0.154. θ̂ = 1/x̄ ⇒ μ̂ = 1/θ̂ = x̄ (bất biến của MLE).', 2, TOP['mle'], K + '10–12')
