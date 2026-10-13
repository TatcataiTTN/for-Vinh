"""Module 8 — biến thể tham số (bo_sung): khoảng tin cậy, cỡ mẫu, tỷ lệ, bảng lớp."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from orig_m08 import TOP, U, T, gstats, ci_pair
SRC = 'Bổ sung: biến thể tham số của dạng bài §2.3 và đề thi (đáp án tính bằng SciPy)'
def build(B):
    rng = random.Random(1808)
    def ci(stem, c, k, expl, lvl, topic, wrongk):
        ans = ci_pair(c, k); ws = []
        for kk in list(wrongk) + [k * 1.15, k * 0.85, k * 2, k / 2]:
            p = ci_pair(c, kk)
            if p != ans and p not in ws: ws.append(p)
        B.mcq(stem, ans, ws, expl, lvl, topic, SRC, 'bo_sung')
    # 1. σ biết, tóm tắt
    for xb, sg, n, g in [(50, 8, 36, 0.95), (120, 15, 25, 0.90), (7.5, 1.2, 64, 0.99), (35, 4, 100, 0.95), (200, 30, 49, 0.90), (15.2, 2.5, 40, 0.99), (88, 10, 16, 0.95), (3.4, 0.6, 81, 0.90)]:
        z = U((1 - g) / 2); k = z * sg / math.sqrt(n)
        ci(f'Tổng thể chuẩn σ = {sg}; mẫu n = {n}, x̄ = {xb}. Khoảng tin cậy {int(g*100)}% cho μ là', xb, k, f'z = {f(z,3)}; k = {f(z,3)}·{sg}/√{n} = {f(k,4)}.', 1, TOP['z'], [T((1 - g) / 2, n - 1) * sg / math.sqrt(n), z * sg, z * sg / n])
    # 2. σ chưa biết, tóm tắt
    for xb, s, n, g in [(50, 8, 16, 0.95), (120, 15, 25, 0.99), (7.5, 1.2, 10, 0.90), (35, 4, 20, 0.95), (200, 30, 12, 0.99), (15.2, 2.5, 30, 0.90), (88, 10, 9, 0.95), (3.4, 0.6, 18, 0.95)]:
        t = T((1 - g) / 2, n - 1); k = t * s / math.sqrt(n)
        ci(f'Tổng thể chuẩn, σ chưa biết; mẫu n = {n}, x̄ = {xb}, s = {s}. Khoảng tin cậy {int(g*100)}% cho μ là', xb, k, f't_{{{(1-g)/2:g}}}({n-1}) = {f(t,3)}; k = {f(t,3)}·{s}/√{n} = {f(k,4)}.', 2, TOP['t'], [U((1 - g) / 2) * s / math.sqrt(n), T((1 - g) / 2, n) * s / math.sqrt(n), t * s])
    # 3. tỷ lệ
    for n, k_, g in [(200, 30, 0.95), (500, 120, 0.95), (1000, 380, 0.99), (400, 60, 0.90), (150, 45, 0.95), (800, 96, 0.99), (300, 42, 0.90)]:
        fq = k_ / n; z = U((1 - g) / 2); kk = z * math.sqrt(fq * (1 - fq) / n)
        ci(f'Khảo sát {n} sản phẩm có {k_} sản phẩm đạt yêu cầu. Khoảng tin cậy {int(g*100)}% cho tỷ lệ đạt là', fq, kk, f'f = {k_}/{n} = {f(fq,4)}; k = {f(z,3)}·√({f(fq,4)}·{f(1-fq,4)}/{n}) = {f(kk,4)}.', 2, TOP['p'], [z * math.sqrt(fq * (1 - fq)), z * fq / math.sqrt(n), U(0.05) * math.sqrt(fq * (1 - fq) / n)])
    # 4. cỡ mẫu
    for sg, L, g in [(6, 2.0, 0.95), (10, 4.0, 0.99), (3, 1.0, 0.90), (15, 5.0, 0.95), (8, 2.5, 0.99), (2.5, 0.8, 0.95)]:
        z = U((1 - g) / 2); n = math.ceil((2 * z * sg / L) ** 2)
        B.mcq(f'σ = {sg}, độ tin cậy {int(g*100)}%. Cỡ mẫu nhỏ nhất để khoảng tin cậy cho μ có độ dài không quá {L} là', str(n), [str(n + 10), str(max(1, n // 2)), str(math.ceil((z * sg / L) ** 2))], f'n ≥ (2·{f(z,3)}·{sg}/{L})² = {(2*z*sg/L)**2:.2f} ⇒ n = {n}.', 2, TOP['n'], SRC, 'bo_sung')
    for e, g, p in [(0.03, 0.95, 0.5), (0.02, 0.95, 0.3), (0.05, 0.99, 0.5), (0.04, 0.90, 0.2)]:
        z = U((1 - g) / 2); n = math.ceil(z * z * p * (1 - p) / e ** 2)
        B.mcq(f'Muốn ước lượng tỷ lệ p với sai số tối đa {e} ở độ tin cậy {int(g*100)}% (dự đoán p ≈ {p}). Cỡ mẫu tối thiểu là', str(n), [str(n + 150), str(max(1, n // 2)), str(math.ceil(z * z * 0.25 / e ** 2) + 300)], f'k = z√(p(1−p)/n) ≤ {e} ⇒ n ≥ z²p(1−p)/e² = {f(z*z*p*(1-p)/e**2,1)} ⇒ n = {n}.', 3, TOP['n'], SRC, 'bo_sung')
    # 5. bảng lớp σ chưa biết / biết
    for lo, w, ns, g, sg in [(10, 5, [2, 5, 9, 6, 3], 0.95, None), (100, 10, [3, 6, 10, 8, 2], 0.90, 12), (0, 2, [1, 4, 8, 5, 2], 0.99, None), (50, 20, [4, 9, 14, 7, 1], 0.95, 25), (20, 4, [2, 3, 7, 6, 2], 0.90, None), (200, 25, [5, 8, 12, 9, 4], 0.95, 30)]:
        N, m, v = gstats(lo, w, ns)
        tab = '; '.join(f'{lo+w*i}–{lo+w*(i+1)}: {c}' for i, c in enumerate(ns))
        if sg is None:
            t = T((1 - g) / 2, N - 1); k = t * math.sqrt(v) / math.sqrt(N)
            ci(f'Bảng lớp (lớp: tần số) — {tab}; biến chuẩn, σ chưa biết. Khoảng tin cậy {int(g*100)}% cho trung bình là', m, k, f'N = {N}; x̄ = {f(m,3)}; s = {f(math.sqrt(v),3)}; t = {f(t,3)}; k = {f(k,3)}.', 3, TOP['t'], [U((1 - g) / 2) * math.sqrt(v) / math.sqrt(N), T((1 - g) / 2, N) * math.sqrt(v) / math.sqrt(N), t * math.sqrt(v)])
        else:
            z = U((1 - g) / 2); k = z * sg / math.sqrt(N)
            ci(f'Bảng lớp (lớp: tần số) — {tab}; biến chuẩn, σ = {sg}. Khoảng tin cậy {int(g*100)}% cho trung bình là', m, k, f'N = {N}; x̄ = {f(m,3)}; k = {f(z,3)}·{sg}/√{N} = {f(k,3)}.', 2, TOP['z'], [T((1 - g) / 2, N - 1) * math.sqrt(v) / math.sqrt(N), z * math.sqrt(v) / math.sqrt(N), z * sg])
    # 6. khoảng cho phương sai
    for n, s2, g in [(15, 4.0, 0.95), (25, 9.0, 0.90), (10, 2.5, 0.99), (30, 16.0, 0.95)]:
        a = 1 - g; lo = (n - 1) * s2 / st.chi2.ppf(1 - a / 2, n - 1); hi = (n - 1) * s2 / st.chi2.ppf(a / 2, n - 1)
        B.mcq(f'(Mở rộng χ²) Mẫu chuẩn cỡ n = {n} có s² = {s2}. Khoảng tin cậy {int(g*100)}% cho σ² là', f'({f(lo,3)}; {f(hi,3)})', [f'({f(s2*0.6,3)}; {f(s2*1.9,3)})', f'({f((n-1)*s2/st.chi2.ppf(g,n-1),3)}; {f((n-1)*s2/st.chi2.ppf(1-g,n-1),3)})', f'({f(lo*1.3,3)}; {f(hi*0.8,3)})'], f'[(n−1)s²/χ²_{{α/2}}({n-1}); (n−1)s²/χ²_{{1−α/2}}({n-1})] = [{f(lo,3)}; {f(hi,3)}].', 3, TOP['var'], SRC, 'bo_sung')
    # 7. so sánh độ rộng
    for g1, g2 in [(0.90, 0.95), (0.95, 0.99), (0.90, 0.99)]:
        r = U((1 - g2) / 2) / U((1 - g1) / 2)
        B.mcq(f'Với σ biết, cùng n: độ dài khoảng tin cậy {int(g2*100)}% gấp bao nhiêu lần khoảng {int(g1*100)}%?', f(r, 3), [f(1 / r, 3), f(r * r, 3), f(g2 / g1, 3)], f'Tỉ số = U_{{{(1-g2)/2:g}}}/U_{{{(1-g1)/2:g}}} = {f(U((1-g2)/2),3)}/{f(U((1-g1)/2),3)} = {f(r,3)}.', 2, TOP['theory'], SRC, 'bo_sung')
