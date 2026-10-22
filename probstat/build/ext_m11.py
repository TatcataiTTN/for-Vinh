"""Module 11 — mở rộng: khái niệm + họ bài χ², t gộp, F (đáp án tự tính bằng SciPy)."""
import math, random
from scipy import stats as st
from qb import f, fg
from qh import pm
from orig_m11 import TOP, REJ, ACC, C2, T, U
SRC = 'Bổ sung: dạng bài §3.3–3.4 / Kreyszig PS 25.4–25.6 (đáp án tự tính bằng SciPy)'
def build(B):
    rng = random.Random(2511)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Thống kê kiểm định phương sai là', '(n − 1)S²/σ₀²', ['S²/σ₀', '(n − 1)S/σ₀²', 'nS²/(n − 1)'], 'Phân phối χ²(n − 1) dưới H₀.', 1, 'var')
    C('Phân phối χ² có đặc điểm', 'chỉ nhận giá trị không âm và lệch phải', ['đối xứng quanh 0', 'nhận cả giá trị âm', 'giống chuẩn tắc'], 'Tổng bình phương.', 1, 'chi')
    C('Kỳ vọng của χ²(k) là', 'k', ['2k', 'k²', '0'], 'Var = 2k.', 1, 'chi')
    C('Kiểm định F so sánh hai phương sai dùng thống kê', 's₁²/s₂²', ['s₁ − s₂', 's₁/s₂²', 'x̄₁/x̄₂'], 'F(n₁ − 1, n₂ − 1).', 1, 'ftest')
    C('Kiểm định F thường được dùng để', 'kiểm tra giả thiết phương sai bằng nhau trước t gộp', ['so sánh hai trung bình trực tiếp', 'kiểm định tỷ lệ', 'tính cỡ mẫu'], 'Điều kiện của t gộp.', 2, 'ftest')
    C('Số bậc tự do của t gộp hai mẫu là', 'n₁ + n₂ − 2', ['n₁ + n₂', 'n₁ + n₂ − 1', 'n₁·n₂'], 'Mất hai bậc cho hai trung bình.', 1, 'two')
    C('Phương sai gộp s_p² là', 'trung bình có trọng số (n−1) của hai phương sai mẫu', ['tổng hai phương sai', 'trung bình cộng đơn giản', 'tích hai phương sai'], '[(n₁−1)s₁² + (n₂−1)s₂²]/(n₁+n₂−2).', 2, 'two')
    C('Mẫu ghép cặp nên kiểm định bằng', 't một mẫu trên các hiệu dᵢ', ['t gộp hai mẫu độc lập', 'F', 'χ²'], 'Cặp có tương quan.', 2, 'two')
    C('Kiểm định tỷ lệ hai mẫu dùng tỷ lệ gộp', 'dưới H₀: p₁ = p₂', ['luôn p̂₁', 'luôn p̂₂', 'không cần'], 'p̂ = (k₁ + k₂)/(n₁ + n₂).', 3, 'prop')
    C('Khi tăng cỡ mẫu, giá trị tới hạn χ²_{α}(n − 1)/(n − 1)', 'tiến về 1', ['tiến về 0', 'tiến ra vô cùng', 'bằng α'], 'χ² tập trung quanh df.', 3, 'chi')
    # χ² thống kê
    for k in range(14):
        n = rng.choice([10, 12, 16, 20, 25, 30]); sg0 = rng.choice([4, 9, 16, 25, 0.25]); s2 = sg0 * rng.choice([0.5, 0.7, 1.3, 1.6, 2.0])
        chi = (n - 1) * s2 / sg0; a = 0.05; kind = k % 2
        if kind == 0:
            P(f'H₀: σ² = {fg(sg0)}. Mẫu n = {n} có s² = {fg(s2,4)}. Thống kê χ² bằng', chi, f'χ² = (n − 1)s²/σ₀² = {n-1}·{fg(s2,4)}/{fg(sg0)} = {f(chi,3)}.', 1, TOP['var'], SRC, extra=[n * s2 / sg0, s2 / sg0, (n - 1) * s2 / math.sqrt(sg0)], d=3)
        else:
            lo, hi = C2(1 - a / 2, n - 1), C2(a / 2, n - 1); dec = REJ if (chi < lo or chi > hi) else ACC
            B.mcq(f'H₀: σ² = {fg(sg0)} so với H₁: σ² ≠ {fg(sg0)}; n = {n}, s² = {fg(s2,4)}, α = 0.05. Kết luận:', dec, [ACC if dec == REJ else REJ, 'Dùng phân phối chuẩn', 'Không kết luận được'],
                  f'χ² = {f(chi,3)}; miền chấp nhận [{f(lo,3)}; {f(hi,3)}] ⇒ {dec}.', 2, TOP['var'], SRC, 'bo_sung')
    # phía phải
    for n, sg0, s2 in [(20, 4, 6.5), (25, 9, 14), (16, 1, 1.9), (30, 25, 40), (12, 2, 3.5), (21, 16, 26)]:
        chi = (n - 1) * s2 / sg0; c = C2(0.05, n - 1); dec = REJ if chi > c else ACC
        B.mcq(f'H₀: σ² = {sg0} so với H₁: σ² > {sg0}; n = {n}, s² = {s2}, α = 0.05. Kết luận:', dec, [ACC if dec == REJ else REJ, 'Dùng t', 'Không đủ dữ kiện'], f'χ² = {f(chi,3)}; χ²₀.₀₅({n-1}) = {f(c,3)} ⇒ {dec}.', 2, TOP['var'], SRC, 'bo_sung')
    # t gộp
    for k in range(10):
        n1, n2 = rng.choice([8, 10, 12, 15]), rng.choice([9, 11, 14, 18]); x1 = rng.choice([50, 70, 80]) + rng.random() * 4; x2 = x1 - rng.choice([-4, -2, 2, 3, 5]); s1 = rng.choice([3, 4.5, 6]); s2 = rng.choice([3.5, 5, 6.5])
        sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)); t = (x1 - x2) / (sp * math.sqrt(1 / n1 + 1 / n2)); tc = T(0.025, n1 + n2 - 2)
        if k % 2 == 0:
            P(f'Nhóm 1: n = {n1}, x̄ = {f(x1,2)}, s = {s1}; nhóm 2: n = {n2}, x̄ = {f(x2,2)}, s = {s2}. Độ lệch chuẩn gộp s_p bằng', sp, f's_p² = [{n1-1}·{fg(s1*s1)} + {n2-1}·{fg(s2*s2)}]/{n1+n2-2}; s_p = {f(sp,3)}.', 2, TOP['two'], SRC, extra=[(s1 + s2) / 2, math.sqrt((s1 ** 2 + s2 ** 2) / 2) + 0.3, sp ** 2], d=3)
        else:
            dec = REJ if abs(t) > tc else ACC
            B.mcq(f'Nhóm 1: n = {n1}, x̄ = {f(x1,2)}, s = {s1}; nhóm 2: n = {n2}, x̄ = {f(x2,2)}, s = {s2}. H₀: μ₁ = μ₂ (hai phía, α = 0.05, t gộp). Kết luận:', dec, [ACC if dec == REJ else REJ, 'Dùng χ²', 'Không đủ dữ kiện'], f'T = {f(t,3)}; t₀.₀₂₅({n1+n2-2}) = {f(tc,3)} ⇒ {dec}.', 3, TOP['two'], SRC, 'bo_sung')
    # F
    for n1, s1, n2, s2 in [(10, 4.0, 12, 2.5), (15, 3.2, 10, 3.0), (8, 5.0, 14, 2.4), (20, 2.2, 16, 3.4), (12, 6.0, 12, 3.0), (9, 1.8, 11, 2.0)]:
        if s1 < s2: n1, s1, n2, s2 = n2, s2, n1, s1
        F = s1 ** 2 / s2 ** 2; fc = st.f.ppf(0.975, n1 - 1, n2 - 1); dec = REJ if F > fc else ACC
        B.mcq(f'Mẫu 1: n = {n1}, s = {s1}; mẫu 2: n = {n2}, s = {s2}. Kiểm định σ₁² = σ₂² (hai phía, α = 0.05) bằng F = s₁²/s₂². Kết luận:', dec, [ACC if dec == REJ else REJ, 'Dùng t', 'Không đủ dữ kiện'], f'F = {f(F,3)}; F₀.₀₂₅({n1-1}, {n2-1}) = {f(fc,3)} ⇒ {dec}.', 3, TOP['ftest'], SRC, 'bo_sung')
    B.essay('Quy định σ = 0.05 mm. Mẫu 20 chi tiết có s = 0.07 mm. Kiểm định σ > 0.05 ở α = 0.05.', f'χ² = 19·0.0049/0.0025 = 37.24; χ²₀.₀₅(19) = {C2(0.05,19):.3f} ⇒ 37.24 > 30.14 bác bỏ H₀: độ biến thiên vượt quy định.', 2, TOP['var'], SRC, 'bo_sung')
    B.essay('Hai loại xăng: loại A (n = 10) x̄ = 25.4, s = 1.2; loại B (n = 12) x̄ = 24.1, s = 1.5 (km/l). Kiểm định μ_A > μ_B ở α = 0.05 (phương sai bằng nhau).', f's_p² = (9·1.44 + 11·2.25)/20 = 1.8855, s_p = 1.373; T = 1.3/(1.373·√(1/10 + 1/12)) = {1.3/(1.373*math.sqrt(1/10+1/12)):.3f}; t₀.₀₅(20) = {T(0.05,20):.3f} ⇒ bác bỏ nếu T > 1.725.', 3, TOP['two'], SRC, 'bo_sung')
    B.essay('Vì sao nên kiểm tra phương sai bằng nhau (F) trước khi dùng t gộp? Nếu bị bác bỏ thì dùng gì?', 'T gộp giả thiết σ₁² = σ₂². Nếu F bác bỏ, dùng kiểm định t Welch (bậc tự do hiệu chỉnh) không giả định phương sai bằng nhau.', 2, TOP['ftest'], SRC, 'bo_sung')
