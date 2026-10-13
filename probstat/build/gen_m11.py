"""Module 11 — biến thể tham số (bo_sung): kiểm định phương sai, hai kỳ vọng, F, bảng χ²."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
from orig_m11 import TOP, REJ, ACC, C2, T, U, pooled
SRC = 'Bổ sung: biến thể tham số của dạng bài §3.3–3.4 (đáp án tính bằng SciPy)'
def build(B):
    rng = random.Random(1911)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); k.setdefault('origin', 'bo_sung'); return pm(B, rng, stem, v, *a, **k)
    def dec(stem, rej, expl, lvl, topic):
        a, b = (REJ, ACC) if rej else (ACC, REJ); B.mcq(stem, a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], expl, lvl, topic, SRC, 'bo_sung')
    # 1. χ² một mẫu
    for n, s2, s02, alt, al in [(20, 5.2, 4.0, '>', 0.05), (16, 2.1, 3.0, '<', 0.05), (25, 12.0, 9.0, '≠', 0.05), (30, 0.5, 0.4, '>', 0.01), (12, 6.0, 10.0, '<', 0.05), (21, 18.0, 25.0, '≠', 0.01), (18, 7.5, 5.0, '>', 0.05), (10, 0.9, 1.5, '<', 0.01)]:
        t = (n - 1) * s2 / s02; d = n - 1
        if alt == '>': crit = C2(al, d); rej = t > crit; reg = f'T > {f(crit,3)}'
        elif alt == '<': crit = C2(1 - al, d); rej = t < crit; reg = f'T < {f(crit,3)}'
        else: lo, hi = C2(1 - al / 2, d), C2(al / 2, d); rej = t < lo or t > hi; reg = f'T < {f(lo,3)} hoặc T > {f(hi,3)}'
        tx = f'Mẫu chuẩn n = {n}, s² = {s2}; H₀: σ² = {s02}, H₁: σ² {alt} {s02}, α = {al*100:g}%.'
        P(tx + ' T_qs = (n − 1)s²/σ₀² là', t, f'T = {d}·{s2}/{s02} = {f(t,3)}.', 1, TOP['var'], SRC, extra=[s2 / s02, n * s2 / s02, d * s02 / s2], d=3)
        dec(tx + f' Miền bác bỏ {reg}; T_qs = {f(t,3)}. Kết luận:', rej, f'{reg} (χ² với {d} bậc tự do) ⇒ T_qs ' + ('thuộc' if rej else 'không thuộc') + ' miền bác bỏ.', 3, TOP['var'])
    # 2. bảng χ²
    for a, d in [(0.05, 10), (0.01, 12), (0.025, 20), (0.05, 5), (0.10, 15), (0.95, 14), (0.975, 9), (0.99, 24)]:
        B.mcq(f'Giá trị χ²_{{{a}}}({d}) (P(χ²({d}) > c) = {a}) xấp xỉ bằng', f(C2(a, d), 3), [f(C2(1 - a, d), 3), f(C2(a, d + 2), 3), f(C2(a, d - 1), 3)], f'Bảng A10: {f(C2(a,d),3)}.', 1, TOP['chi'], SRC, 'bo_sung')
    # 3. hai kỳ vọng
    for n1, x1, s1, n2, x2, s2, alt, al in [(12, 52.4, 4.1, 15, 49.1, 4.6, '>', 0.05), (10, 8.2, 1.1, 10, 7.5, 1.0, '≠', 0.05), (20, 75.0, 8.0, 25, 71.5, 9.0, '>', 0.01), (9, 15.6, 2.2, 11, 17.2, 2.4, '<', 0.05), (16, 100, 12, 16, 94, 14, '≠', 0.01), (14, 33.1, 5.0, 18, 30.2, 4.5, '>', 0.05), (25, 6.1, 0.9, 25, 5.7, 1.0, '≠', 0.05), (8, 120, 15, 10, 135, 14, '<', 0.05)]:
        t, sp = pooled(n1, x1, s1, n2, x2, s2); d = n1 + n2 - 2; a_ = al / 2 if alt == '≠' else al; crit = T(a_, d)
        rej = (t > crit) if alt == '>' else (t < -crit) if alt == '<' else abs(t) > crit
        reg = {'>': f'T > {f(crit,3)}', '<': f'T < −{f(crit,3)}', '≠': f'|T| > {f(crit,3)}'}[alt]
        tx = f'Hai mẫu chuẩn cùng σ²: (n₁ = {n1}, x̄₁ = {x1}, s₁ = {s1}), (n₂ = {n2}, x̄₂ = {x2}, s₂ = {s2}); H₀: μ₁ = μ₂, H₁: μ₁ {alt} μ₂, α = {al*100:g}%.'
        P(tx + ' T_qs là', t, f'S = √(((n₁−1)s₁² + (n₂−1)s₂²)/(n₁+n₂−2)) = {f(sp,4)}; T = ({x1} − {x2})/({f(sp,4)}·√(1/{n1} + 1/{n2})) = {f(t,3)}.', 2, TOP['two'], SRC, extra=[-t, (x1 - x2) / sp, t / 2], d=3, lo=None)
        dec(tx + f' Với t({d}) tới hạn {f(crit,3)}: kết luận là', rej, f'{reg}; T_qs = {f(t,3)} ⇒ ' + (REJ if rej else ACC) + '.', 3, TOP['two'])
    # 4. F-test
    for n1, s1, n2, s2, al in [(10, 6.0, 12, 3.0, 0.05), (8, 2.4, 9, 1.8, 0.05), (16, 5.5, 16, 2.5, 0.01), (7, 4.0, 11, 4.2, 0.05)]:
        v0 = s1 / s2; crit = st.f.ppf(1 - al, n1 - 1, n2 - 1); rej = v0 > crit
        P(f'Mẫu 1 (n₁ = {n1}, s₁² = {s1}) và mẫu 2 (n₂ = {n2}, s₂² = {s2}) chuẩn. H₀: σ₁² = σ₂², H₁: σ₁² > σ₂². v₀ = s₁²/s₂² là', v0, f'v₀ = {s1}/{s2} = {f(v0,3)}.', 1, TOP['ftest'], SRC, extra=[s2 / s1, s1 - s2, v0 * 2], d=3)
        P(f'Cùng bài F-test (n₁ = {n1}, n₂ = {n2}, α = {al*100:g}%): giá trị tới hạn F_α({n1-1}, {n2-1}) là', crit, f'Bảng A11: F_{{{al}}}({n1-1}, {n2-1}) = {f(crit,3)}; v₀ = {f(v0,3)} ' + ('> ' if rej else '≤ ') + f'{f(crit,3)} ⇒ ' + (REJ if rej else ACC) + '.', 3, TOP['ftest'], SRC, extra=[st.f.ppf(1 - al, n2 - 1, n1 - 1), T(al, n1 - 1), C2(al, n1 - 1)], d=3)
    # 5. n1 = n2 = n, công thức rút gọn
    for n, x, y, sx2, sy2 in [(8, 25.0, 22.0, 9.0, 11.0), (10, 54.2, 51.0, 16.0, 20.0), (12, 7.8, 8.9, 1.4, 1.1), (9, 100, 96, 25, 30), (15, 3.4, 3.1, 0.36, 0.42), (6, 40, 35, 8, 6)]:
        t = math.sqrt(n) * (x - y) / math.sqrt(sx2 + sy2)
        P(f'Hai mẫu cùng cỡ n = {n}: x̄ = {x}, ȳ = {y}, s_X² = {sx2}, s_Y² = {sy2}. Giá trị T = √n(x̄ − ȳ)/√(s_X² + s_Y²) là', t, f'T = √{n}·({x} − {y})/√({sx2} + {sy2}) = {f(t,3)} (t với 2n − 2 = {2*n-2} bậc tự do).', 2, TOP['two'], SRC, extra=[-t, (x - y) / math.sqrt(sx2 + sy2), t / 2], d=3, lo=None)
    # 6. bậc tự do
    for n1, n2 in [(8, 8), (10, 12), (15, 20), (25, 25)]:
        B.mcq(f'Hai mẫu cỡ n₁ = {n1} và n₂ = {n2}; kiểm định t gộp có số bậc tự do là', str(n1 + n2 - 2), [str(n1 + n2 - 1), str(n1 + n2), str(min(n1, n2) - 1)], f'n₁ + n₂ − 2 = {n1+n2-2}.', 1, TOP['theory'], SRC, 'bo_sung')
    for n in (10, 16, 21, 31):
        B.mcq(f'Kiểm định phương sai với mẫu cỡ n = {n}: số bậc tự do của χ² là', str(n - 1), [str(n), str(n + 1), str(n - 2)], f'(n − 1)S²/σ₀² ~ χ²(n − 1) = χ²({n-1}).', 1, TOP['chi'], SRC, 'bo_sung')
