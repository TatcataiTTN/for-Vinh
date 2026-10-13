"""Module 11 — Phân phối χ², kiểm định phương sai, so sánh kỳ vọng hai phân phối chuẩn (và kiểm định F phương sai, mở rộng Kreyszig).
Gốc: Lecture Notes §3.3–3.4 (Ví dụ 3.4–3.5, Bài 3.10–3.15), Kreyszig §25.4 (Ví dụ 6) và PS 25.4 (Prob. 12–20)."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'chi': 'Phân phối χ² và bảng A10', 'var': 'Kiểm định phương sai (χ²)', 'two': 'So sánh hai kỳ vọng (t gộp)', 'ftest': 'Kiểm định F so sánh hai phương sai', 'prop': 'Kiểm định tỷ lệ', 'theory': 'Lý thuyết'}
REJ = 'Bác bỏ H₀, chấp nhận H₁'; ACC = 'Chưa đủ cơ sở bác bỏ H₀ (chấp nhận H₀)'
C2 = lambda a, d: st.chi2.ppf(1 - a, d); T = lambda a, d: st.t.ppf(1 - a, d); U = lambda a: st.norm.ppf(1 - a)
def pooled(n1, x1, s1, n2, x2, s2):
    sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)); return (x1 - x2) / (sp * math.sqrt(1 / n1 + 1 / n2)), sp
def build(B):
    rng = random.Random(1111)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); return pm(B_, r_, stem, v, *a, **k)
    def dec(stem, rej, expl, lvl, topic, src, origin='goc'):
        a, b = (REJ, ACC) if rej else (ACC, REJ)
        B.mcq(stem, a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], expl, lvl, topic, src, origin)
    S = 'Lecture Notes '
    # ---- χ² lý thuyết ----
    B.mcq('Nếu X₁, …, Xₙ độc lập cùng N(μ, σ²) thì (n − 1)S²/σ² có phân phối:', 'χ²(n − 1) (khi-bình phương n − 1 bậc tự do)', ['Student t(n − 1)', 'Chuẩn tắc N(0, 1)', 'χ²(n)'], 'Định lý 3.1: Y = (n − 1)S²/σ² ~ χ²(n − 1).', 1, TOP['chi'], S + 'Định lý 3.1')
    B.mcq('Phân phối χ²(m) nhận giá trị trong khoảng nào và có dạng gì?', 'x ≥ 0, lệch phải (đuôi dài bên phải)', ['Mọi số thực, đối xứng', 'Từ −1 đến 1', '0 ≤ x ≤ m, đối xứng'], 'Hàm mật độ χ² chỉ dương với x ≥ 0 (Hình 3.8).', 1, TOP['chi'], S + 'Định nghĩa 3.1')
    B.mcq('Kiểm định hai phía H₀: σ² = σ₀² có miền bác bỏ:', 'T < χ²_{1−α/2}(n − 1) hoặc T > χ²_{α/2}(n − 1), với T = (n − 1)S²/σ₀²', ['|T| > U_{α/2}', 'T > t_α(n − 1)', 'T < χ²_α(n)'], 'Công thức (3.20): hai đuôi của χ².', 2, TOP['var'], S + '(3.20)')
    B.mcq('Kiểm định một phía phải H₁: σ² > σ₀² có miền bác bỏ:', 'T > χ²_α(n − 1)', ['T < χ²_{1−α}(n − 1)', '|T| > χ²_{α/2}', 'T > t_α'], 'Công thức (3.22).', 1, TOP['var'], S + '(3.22)')
    B.mcq('Kiểm định một phía trái H₁: σ² < σ₀² có miền bác bỏ:', 'T < χ²_{1−α}(n − 1)', ['T > χ²_α(n − 1)', 'T < −χ²_α', '|T| < χ²_{α/2}'], 'Công thức (3.24): đuôi trái của χ².', 2, TOP['var'], S + '(3.24)')
    for a, d in [(0.05, 14), (0.05, 19), (0.05, 27), (0.01, 29), (0.025, 9)]:
        B.mcq(f'Giá trị tới hạn χ²_{{{a}}}({d}) (P(χ² > c) = {a}) là', f(C2(a, d), 3), [f(C2(1 - a, d), 3), f(C2(a, d + 1), 3), f(C2(a / 2, d), 3)], f'Tra bảng A10 với {d} bậc tự do, phần đuôi phải {a}: {f(C2(a,d),3)}.', 1, TOP['chi'], S + 'bảng A10 (bậc tự do cho trước)')
    # ---- Ví dụ 3.4 ----
    t34 = 14 * 13 / 10
    P(B, rng, 'Mẫu n = 15, s² = 13 từ tập nền chuẩn; kiểm định H₀: σ² = 10 với H₁: σ² > 10 ở mức 5%. Giá trị quan sát T_qs = (n − 1)s²/σ₀² là (Ví dụ 3.4)', t34, f'T = 14·13/10 = {f(t34,1)}.', 1, TOP['var'], S + 'Ví dụ 3.4', extra=[13 / 10, 15 * 13 / 10, 14 * 10 / 13], d=1)
    P(B, rng, 'Cùng bài (n = 15, H₁: σ² > 10, α = 5%): giá trị tới hạn χ²_{0.05}(14) (A10) là', C2(0.05, 14), f'χ²₀.₀₅(14) = {f(C2(0.05,14),2)} (giáo trình: 23.68).', 1, TOP['var'], S + 'Ví dụ 3.4', extra=[C2(0.05, 15), C2(0.95, 14), C2(0.025, 14)], d=2)
    dec('Cùng bài (T_qs = 18.2, χ²₀.₀₅(14) = 23.68): kết luận là', False, 'T_qs = 18.2 ≤ 23.68 ⇒ T_qs ∉ W_α ⇒ chấp nhận H₀ (Ví dụ 3.4).', 2, TOP['var'], S + 'Ví dụ 3.4')
    # ---- Ví dụ 3.5 hai mẫu ----
    X = [105, 108, 86, 103, 103, 107, 124, 105]; Y = [89, 92, 84, 97, 103, 107, 111, 97]
    xb, yb = sum(X) / 8, sum(Y) / 8; sx2 = sum((a - xb) ** 2 for a in X) / 7; sy2 = sum((a - yb) ** 2 for a in Y) / 7; t35 = math.sqrt(8) * (xb - yb) / math.sqrt(sx2 + sy2)
    P(B, rng, 'Sản lượng công nhân hai môi trường: X = 105, 108, 86, 103, 103, 107, 124, 105; Y = 89, 92, 84, 97, 103, 107, 111, 97 (cùng phương sai chuẩn). Giá trị quan sát T_qs = √n(x̄ − ȳ)/√(s_X² + s_Y²) (n₁ = n₂ = 8) là (Ví dụ 3.5)', t35, f'x̄ = {f(xb,3)}, ȳ = {f(yb,3)}, s_X² = {f(sx2,3)}, s_Y² = {f(sy2,3)}; T = √8·{f(xb-yb,3)}/√{f(sx2+sy2,3)} = {f(t35,3)} (giáo trình 1.56).', 3, TOP['two'], S + 'Ví dụ 3.5', extra=[xb - yb, -t35, t35 / 2], d=3, lo=None)
    P(B, rng, 'Cùng bài hai môi trường làm việc, hai phía ở mức 5%, bậc tự do n₁ + n₂ − 2 = 14. Giá trị tới hạn t_{α/2}(14) là', T(0.025, 14), f't₀.₀₂₅(14) = {f(T(0.025,14),3)} (giáo trình: 2.14).', 2, TOP['two'], S + 'Ví dụ 3.5', extra=[T(0.05, 14), T(0.025, 15), U(0.025)], d=3)
    dec('Hai môi trường làm việc: T_qs = 1.564, t₀.₀₂₅(14) = 2.145. Kết luận về sản lượng trung bình (hai phía, 5%) là', False, '|T_qs| = 1.564 ≤ 2.145 ⇒ chấp nhận H₀: μ_X = μ_Y (Ví dụ 3.5).', 2, TOP['two'], S + 'Ví dụ 3.5')
    # ---- Kreyszig Ex 6 F-test ----
    v0 = sx2 / sy2; c = st.f.ppf(0.95, 7, 7)
    P(B, rng, 'Với hai mẫu trên (s_X² = 106.125, s_Y² = 84.000), kiểm định H₀: σ_X² = σ_Y² với H₁: σ_X² > σ_Y² ở mức 5%: giá trị quan sát v₀ = s_X²/s_Y² là (Kreyszig Example 6)', v0, f'v₀ = 106.125/84.000 = {f(v0,3)} (giáo trình: 1.26).', 2, TOP['ftest'], 'Kreyszig §25.4, Example 6', extra=[1 / v0, v0 ** 2, sx2 - sy2], d=3)
    P(B, rng, 'Giá trị tới hạn F_{0.05}(7, 7) trong ví dụ trên là (Kreyszig Example 6)', c, f'Bảng A11: c = {f(c,2)} (3.79); v₀ = 1.26 ≤ c ⇒ chấp nhận H₀ (hai phương sai bằng nhau, hợp lý với giả thiết cùng σ của t gộp).', 3, TOP['ftest'], 'Kreyszig §25.4, Example 6', extra=[T(0.05, 7), C2(0.05, 7), 2.14], d=2)
    # ---- Bài 3.10 ----
    t310 = 19 * 1.0 ** 2 / 0.8 ** 2; c310 = C2(0.05, 19); rej = t310 > c310
    P(B, rng, 'Máy đóng gói: σ trước đây 0.8 oz. Mẫu n = 20 có s = 1.0 oz. H₀: σ = 0.8, H₁: σ > 0.8. T_qs = (n − 1)s²/σ₀² là (Bài 3.10 / Kreyszig PS 25.4/15)', t310, f'T = 19·1.0²/0.8² = {f(t310,3)}; χ²₀.₀₅(19) = {f(c310,3)}.', 2, TOP['var'], S + 'Bài 3.10 / Kreyszig PS 25.4 Prob. 15', extra=[1 / 0.64, 20 / 0.64, 19 * 0.8 / 1], d=3)
    dec('Bài 3.10: T_qs = 29.688, χ²₀.₀₅(19) = 30.144. Kết luận ở mức 5% (H₁: σ > 0.8) là', rej, f'T_qs {f(t310,3)} ' + ('>' if rej else '≤') + f' {f(c310,3)} ⇒ ' + (REJ if rej else ACC) + ': chưa đủ bằng chứng độ lệch chuẩn tăng.', 3, TOP['var'], S + 'Bài 3.10 / Kreyszig PS 25.4 Prob. 15')
    # ---- Bài 3.11 ----
    t311 = 27 * 3.5 ** 2 / 25; c311 = C2(0.95, 27); rej = t311 < c311
    P(B, rng, 'Pin: H₀: σ = 5, H₁: σ < 5; n = 28, s = 3.5 giờ. T_qs = (n − 1)s²/σ₀² là (Bài 3.11 / Kreyszig PS 25.4/16)', t311, f'T = 27·3.5²/25 = {f(t311,3)}; miền bác bỏ T < χ²₀.₉₅(27) = {f(c311,3)}.', 2, TOP['var'], S + 'Bài 3.11 / Kreyszig PS 25.4 Prob. 16', extra=[28 * 12.25 / 25, 27 * 3.5 / 5, 12.25 / 25], d=3)
    dec('Bài 3.11: T_qs = 13.23 và χ²₀.₉₅(27) = 16.151 (miền T < 16.151). Kết luận là', rej, f'T_qs {f(t311,2)} ' + ('<' if rej else '≥') + f' {f(c311,2)} ⇒ ' + (REJ if rej else ACC) + ': σ < 5 giờ ⇒ thay pin theo chu kỳ cố định là kinh tế hơn.', 3, TOP['var'], S + 'Bài 3.11 / Kreyszig PS 25.4 Prob. 16')
    # ---- Bài 3.12 ----
    t312 = 29 * 1.1 ** 2 / 1.0; c312 = C2(0.01, 29); rej = t312 > c312
    P(B, rng, 'Máy móc bình thường có σ = 1 kg; mẫu 30 sản phẩm có s = 1.1 kg. H₀: σ = 1, α = 0.01 (hai phía). T_qs là (Bài 3.12)', t312, f'T = 29·1.21 = {f(t312,3)}; hai phía: χ²₀.₀₀₅(29) = {f(C2(0.005,29),3)}, χ²₀.₉₉₅(29) = {f(C2(0.995,29),3)}.', 2, TOP['var'], S + 'Bài 3.12', extra=[30 * 1.21, 29 * 1.1, 1.21], d=3)
    lo312, hi312 = C2(0.995, 29), C2(0.005, 29)
    dec(f'Bài 3.12: T_qs = {f(t312,3)}; miền bác bỏ hai phía T < {f(lo312,3)} hoặc T > {f(hi312,3)}. Kết luận là', not (lo312 <= t312 <= hi312), f'T_qs nằm trong [{f(lo312,3)}; {f(hi312,3)}] ⇒ ' + ACC + ': máy còn hoạt động tốt.', 3, TOP['var'], S + 'Bài 3.12')
    # ---- Bài 3.13 ----
    t313, sp313 = pooled(16, 20.2, 0.6, 16, 19.6, 0.4); c313 = T(0.05, 30)
    P(B, rng, 'Xăng B (n = 16, x̄ = 20.2, s = 0.6) so với xăng A (n = 16, x̄ = 19.6, s = 0.4), cùng phương sai; H₀: μ_B = μ_A, H₁: μ_B > μ_A. T_qs = (x̄_B − x̄_A)/(S√(1/n₁ + 1/n₂)) là (Bài 3.13 / Kreyszig PS 25.4/17)', t313, f'S = √((15·0.36 + 15·0.16)/30) = {f(sp313,4)}; T = 0.6/({f(sp313,4)}·√(1/8)) = {f(t313,3)}; t₀.₀₅(30) = {f(c313,3)}.', 3, TOP['two'], S + 'Bài 3.13 / Kreyszig PS 25.4 Prob. 17', extra=[0.6, 0.6 / sp313, t313 / 2], d=3)
    dec(f'Bài 3.13: T_qs = {f(t313,3)}, t₀.₀₅(30) = {f(c313,3)} (H₁: μ_B > μ_A). Kết luận là', t313 > c313, f'T_qs ' + ('>' if t313 > c313 else '≤') + f' {f(c313,3)} ⇒ ' + (REJ if t313 > c313 else ACC) + ': xăng B tốt hơn xăng A.', 3, TOP['two'], S + 'Bài 3.13 / Kreyszig PS 25.4 Prob. 17')
    # ---- Bài 3.14 ----
    X14 = [2.66, 2.68, 2.63, 2.60, 2.67, 2.59, 2.62, 2.61]; Y14 = [2.63, 2.60, 2.57, 2.56, 2.58, 2.58, 2.61, 2.62]
    r14 = st.ttest_ind(X14, Y14, equal_var=True); t14 = float(r14.statistic); c14 = T(0.025, 14)
    P(B, rng, 'Bi thép loại I: 2.66, 2.68, 2.63, 2.60, 2.67, 2.59, 2.62, 2.61; loại II: 2.63, 2.60, 2.57, 2.56, 2.58, 2.58, 2.61, 2.62 (chuẩn, cùng σ²). Kiểm định H₀: μ₁ = μ₂ hai phía; T_qs là (Bài 3.14)', t14, f'x̄₁ = {f(sum(X14)/8,4)}, x̄₂ = {f(sum(Y14)/8,4)}; T = {f(t14,3)} (t gộp 14 bậc tự do; đối chiếu SciPy).', 3, TOP['two'], S + 'Bài 3.14', extra=[-t14, t14 / 2, t14 * 1.5], d=3, lo=None)
    dec(f'Bài 3.14: T_qs = {f(t14,3)}, t₀.₀₂₅(14) = {f(c14,3)}. Kết luận (5%, hai phía) là', abs(t14) > c14, f'|T_qs| ' + ('>' if abs(t14) > c14 else '≤') + f' {f(c14,3)} ⇒ ' + (REJ if abs(t14) > c14 else ACC) + '.', 3, TOP['two'], S + 'Bài 3.14')
    # ---- Bài 3.15 ----
    t315, sp315 = pooled(500, 3.2, 0.3, 500, 3.0, 0.4); c315 = T(0.05, 998)
    P(B, rng, 'Trẻ sơ sinh: thành thị (n = 500, x̄ = 3.2, s = 0.3), nông thôn (n = 500, x̄ = 3.0, s = 0.4); H₁: μ_thành thị > μ_nông thôn. T_qs là (Bài 3.15)', t315, f'S = √((499·0.09 + 499·0.16)/998) = {f(sp315,4)}; T = 0.2/({f(sp315,4)}·√(2/500)) = {f(t315,3)}; t₀.₀₅(998) ≈ {f(c315,3)}.', 3, TOP['two'], S + 'Bài 3.15', extra=[0.2, 0.2 / sp315, t315 / 2], d=3)
    dec(f'Bài 3.15: T_qs = {f(t315,2)} so với t₀.₀₅(998) = {f(c315,3)}. Kết luận (5%) là', True, 'T_qs ≫ 1.646 ⇒ bác bỏ H₀: trọng lượng trẻ thành thị cao hơn nông thôn.', 2, TOP['two'], S + 'Bài 3.15')
    # ---- Kreyszig 14, 18, 20 ----
    f14 = 310 / 400; z14 = (f14 - 0.75) / math.sqrt(0.75 * 0.25 / 400)
    P(B, rng, 'Thuốc cũ chữa khỏi 75% bệnh nhân; thuốc mới chữa khỏi 310/400. H₀: p = 0.75, H₁: p > 0.75. Giá trị quan sát z = (f − p₀)/√(p₀(1 − p₀)/n) là (Kreyszig PS 25.4/14)', z14, f'f = 0.775; z = {f(z14,3)} < U₀.₀₅ = 1.645 ⇒ chưa đủ bằng chứng thuốc mới tốt hơn.', 3, TOP['prop'], 'Kreyszig PS 25.4, Prob. 14', extra=[-z14, 0.025, z14 / 2], d=3, lo=None)
    dec(f'Thuốc mới: z = {f(z14,3)}; U₀.₀₅ = 1.645 (H₁: p > 0.75). Kết luận ở 5% là', z14 > 1.645, 'z < 1.645 ⇒ ' + ACC + '.', 3, TOP['prop'], 'Kreyszig PS 25.4, Prob. 14')
    z20 = (10 - 14) / (3 * math.sqrt(1 / 12 + 1 / 18))
    P(B, rng, 'Hai mẫu cỡ 12 và 18 có trung bình 10 và 14, σ chung = 3 (đã biết). Kiểm định H₀: μ₁ = μ₂ hai phía; z = (x̄₁ − x̄₂)/(σ√(1/n₁ + 1/n₂)) là (Kreyszig PS 25.4/20)', z20, f'z = −4/(3·√(1/12 + 1/18)) = {f(z20,3)}; |z| > 1.960 ⇒ bác bỏ H₀.', 3, TOP['two'], 'Kreyszig PS 25.4, Prob. 20', extra=[-z20, 4 / 3, z20 / 2], d=3, lo=None)
    A18 = [70, 80, 30, 70, 60, 80]; B18 = [140, 120, 130, 130, 120]; v1 = sum((a - sum(A18) / 6) ** 2 for a in A18) / 5; v2 = sum((a - sum(B18) / 5) ** 2 for a in B18) / 4
    P(B, rng, 'Nhiệt độ sắt từ hai nồi nấu: mẫu 1: 70, 80, 30, 70, 60, 80; mẫu 2: 140, 120, 130, 130, 120. Phương sai mẫu s₁² là (Kreyszig PS 25.4/18)', v1, f'x̄ = {f(sum(A18)/6,3)}; s₁² = {f(v1,3)}; (mẫu 2: s₂² = {f(v2,3)}).', 2, TOP['ftest'], 'Kreyszig PS 25.4, Prob. 18', extra=[math.sqrt(v1), v2, v1 * 5 / 6], d=3)
    # ---- Lý thuyết hai mẫu ----
    B.mcq('Khi so sánh hai kỳ vọng với cùng phương sai chưa biết, tiêu chuẩn kiểm định là:', 'T = (X̄ − Ȳ)/(S√(1/n₁ + 1/n₂)) ~ t(n₁ + n₂ − 2), S² = ((n₁ − 1)S_X² + (n₂ − 1)S_Y²)/(n₁ + n₂ − 2)', ['T = (X̄ − Ȳ)/√(S_X² + S_Y²) ~ N(0, 1)', 'T = S_X²/S_Y² ~ χ²', 'T = X̄ − Ȳ ~ t(n₁)'], 'Mục 3.4; với n₁ = n₂ = n: T = √n(X̄ − Ȳ)/√(S_X² + S_Y²) ~ t(2n − 2).', 2, TOP['theory'], S + '§3.4')
    B.mcq('Khi n₁ = n₂ = n, bậc tự do của Student trong so sánh hai kỳ vọng là:', '2n − 2', ['n − 1', '2n', 'n'], 'n₁ + n₂ − 2 = 2n − 2.', 1, TOP['theory'], S + '§3.4')
    B.mcq('Điều kiện của phép so sánh hai kỳ vọng trong §3.4 là:', 'Hai tổng thể chuẩn, độc lập, cùng phương sai (σ_X = σ_Y, có thể chưa biết)', ['Hai tổng thể có cùng kỳ vọng', 'Hai mẫu phụ thuộc từng cặp', 'Mẫu rất lớn'], 'Giả thiết của mục 3.4; nếu phương sai khác nhau cần phương pháp khác (Welch).', 2, TOP['theory'], S + '§3.4')
    B.mcq('Kiểm định F: để so sánh hai phương sai σ_X², σ_Y² (H₁: σ_X² > σ_Y²) ta dùng thống kê:', 'v₀ = s_X²/s_Y² so với F_α(n₁ − 1, n₂ − 1)', ['v₀ = s_X − s_Y so với U_α', 'v₀ = s_X²·s_Y²', 'v₀ = (x̄ − ȳ)/s'], 'Kreyszig §25.4: v₀ ~ F(n₁ − 1, n₂ − 1) khi H₀ đúng.', 2, TOP['ftest'], 'Kreyszig §25.4 (F-test)')
    B.essay('Ví dụ 3.4 và Bài 3.10 (Lecture Notes): kiểm định phương sai; Ví dụ 3.4: n = 15, s² = 13, H₀: σ² = 10 (σ² > 10), α = 5%.', 'T = 14·13/10 = 18.2; χ²₀.₀₅(14) = 23.685; T ∉ W_α ⇒ chấp nhận H₀. Bài 3.10: T = 29.688 < 30.144 ⇒ chấp nhận H₀.', 2, TOP['var'], S + 'Ví dụ 3.4, Bài 3.10')
    B.essay('Ví dụ 3.5 (Lecture Notes): so sánh sản lượng hai môi trường (n₁ = n₂ = 8).', f'x̄ = 105.125, ȳ = 97.5; s_X² = 106.125, s_Y² = 84; T = √8·7.625/√190.125 = {f(t35,3)}; t₀.₀₂₅(14) = 2.145 ⇒ chấp nhận H₀ (hai sản lượng trung bình không khác biệt).', 3, TOP['two'], S + 'Ví dụ 3.5')
    B.essay('Bài 3.13 và 3.15 (Lecture Notes): so sánh hai xăng (16 xe mỗi loại); so sánh trẻ sơ sinh thành thị và nông thôn.', f'3.13: S = {f(sp313,3)}; T = {f(t313,3)} > 1.697 ⇒ xăng B tốt hơn. 3.15: S = {f(sp315,3)}; T = {f(t315,2)} > 1.646 ⇒ thành thị cao hơn.', 3, TOP['two'], S + 'Bài 3.13, 3.15')
    B.essay('Bài 3.11–3.12 (Lecture Notes): phương sai pin (n = 28, s = 3.5, σ < 5) và máy đóng gói (n = 30, s = 1.1, σ = 1, α = 0.01).', f'3.11: T = 13.23 < χ²₀.₉₅(27) = 16.15 ⇒ bác bỏ H₀ (σ < 5). 3.12: T = {f(t312,2)} ∈ [{f(lo312,2)}; {f(hi312,2)}] ⇒ chấp nhận H₀.', 3, TOP['var'], S + 'Bài 3.11–3.12')
