"""Module 12 — biến thể tham số (bo_sung)."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
from orig_m12 import TOP, REJ, ACC, C2, U
SRC = 'Bổ sung: biến thể tham số của dạng bài §3.5–3.7 / PS 25.5–25.8 (đáp án tính bằng SciPy)'
def build(B):
    rng = random.Random(1912)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); k.setdefault('origin', 'bo_sung'); return pm(B, rng, stem, v, *a, **k)
    def dec(stem, rej, expl, lvl, topic):
        a, b = (REJ, ACC) if rej else (ACC, REJ); B.mcq(stem, a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], expl, lvl, topic, SRC, 'bo_sung')
    # 1. biểu đồ trung bình
    for mu, sg, n in [(50, 4, 4), (100, 6, 9), (12.5, 0.3, 5), (200, 15, 16), (8, 0.5, 25), (35, 2.4, 6)]:
        d = 3 * sg / math.sqrt(n)
        P(f'Biểu đồ kiểm soát trung bình: μ = {mu}, σ = {sg}, cỡ mẫu n = {n}. UCL = μ + 3σ/√n là', mu + d, f'3σ/√n = 3·{sg}/√{n} = {f(d,4)} ⇒ UCL = {f(mu+d,4)}, LCL = {f(mu-d,4)}.', 1, TOP['qc'], SRC, extra=[mu + 3 * sg, mu + sg / math.sqrt(n), mu + d * 2], d=3, hi=None)
        P(f'Cùng biểu đồ (μ = {mu}, σ = {sg}, n = {n}): độ rộng UCL − LCL là', 2 * d, f'UCL − LCL = 6σ/√n = {f(2*d,4)}.', 2, TOP['qc'], SRC, extra=[d, 6 * sg, 3 * sg], d=3, hi=None)
    for sg, w in [(2, 1.0), (5, 3.0), (0.4, 0.2), (10, 4.0)]:
        n = math.ceil((6 * sg / w) ** 2)
        B.mcq(f'Muốn khoảng UCL − LCL ≤ {w} (quy tắc 3σ, σ = {sg}). Cỡ mẫu n tối thiểu là', str(n), [str(max(1, n // 4)), str(n * 2), str(math.ceil((3 * sg / w) ** 2)), str(n + 25)], f'6σ/√n ≤ {w} ⇒ n ≥ (6·{sg}/{w})² = {(6*sg/w)**2:.2f} ⇒ n = {n}.', 2, TOP['qc'], SRC, 'bo_sung')
    # 2. biểu đồ p
    for p0, n in [(0.05, 100), (0.02, 200), (0.1, 50), (0.03, 150), (0.08, 120)]:
        sd = math.sqrt(p0 * (1 - p0) / n); ucl = p0 + 3 * sd; lcl = max(0, p0 - 3 * sd)
        P(f'Biểu đồ p: p = {p0}, n = {n}. UCL = p + 3√(p(1 − p)/n) là', ucl, f'√({p0}·{1-p0:.2f}/{n}) = {f(sd,4)}; UCL = {f(ucl,4)}; LCL = max(0, {f(p0-3*sd,4)}) = {f(lcl,4)}.', 2, TOP['pc'], SRC, extra=[p0 + sd, p0 + 3 * p0, p0 * 3], d=4)
    # 3. χ² phù hợp
    def gof(stem, obs, exp, df, al, lvl=2):
        chi = sum((o - e) ** 2 / e for o, e in zip(obs, exp)); crit = C2(al, df); rej = chi > crit
        P(stem + ' χ₀² là', chi, f'Σ(b − e)²/e = {f(chi,3)} (e = ' + ', '.join(fg(e, 3) for e in exp) + ').', lvl, TOP['gof'], SRC, extra=[chi / 2, chi * 1.8, sum((o - e) ** 2 for o, e in zip(obs, exp))], d=3)
        dec(stem + f' Mức {al*100:g}%: χ₀² = {f(chi,3)}, χ²_α({df}) = {f(crit,3)}. Kết luận là', rej, f'χ₀² ' + ('>' if rej else '≤') + f' {f(crit,3)} ⇒ ' + (REJ if rej else ACC) + '.', lvl + 1, TOP['gof'])
    for n, obs in [(120, [25, 15, 22, 18, 21, 19]), (90, [20, 12, 18, 10, 14, 16]), (150, [18, 30, 22, 28, 27, 25])]:
        gof(f'Gieo súc sắc {n} lần được tần số các mặt {obs}; H₀: súc sắc cân đối.', obs, [n / 6] * 6, 5, 0.05)
    gof('Lai đậu: tần số 315, 101, 108, 32 (tổng 556); H₀: tỉ lệ 9:3:3:1.', [315, 101, 108, 32], [556 * 9 / 16, 556 * 3 / 16, 556 * 3 / 16, 556 / 16], 3, 0.05)
    gof('Số cuộc gọi mỗi giờ trong 4 khung: 18, 25, 31, 22 (tổng 96); H₀: các khung đều nhau.', [18, 25, 31, 22], [24] * 4, 3, 0.05)
    gof('Hoa 3 màu đỏ/hồng/trắng: 48, 90, 62 (tổng 200); H₀: tỉ lệ 1:2:1.', [48, 90, 62], [50, 100, 50], 2, 0.05)
    for K, r in [(8, 2), (10, 0), (6, 1), (12, 2), (5, 0), (9, 1)]:
        B.mcq(f'Kiểm định χ² phù hợp có K = {K} lớp và ước lượng r = {r} tham số bằng MLE. Số bậc tự do là', str(K - r - 1), [str(K - r), str(K - 1 if r else K), str(K - r - 2), str(K + 1)], f'K − r − 1 = {K} − {r} − 1 = {K-r-1}.', 2, TOP['gof'], SRC, 'bo_sung')
    for a, d in [(0.05, 3), (0.05, 7), (0.01, 5), (0.05, 9), (0.025, 4)]:
        B.mcq(f'Giá trị tới hạn χ²_{{{a}}}({d}) trong kiểm định phù hợp là', f(C2(a, d), 3), [f(C2(1 - a, d), 3), f(C2(a, d + 1), 3), f(C2(a, d - 1), 3)], f'Bảng A10: {f(C2(a,d),3)}.', 1, TOP['gof'], SRC, 'bo_sung')
    # 4. kiểm định dấu
    for n, k in [(10, 9), (12, 10), (15, 12), (8, 7), (20, 15), (9, 8)]:
        p = st.binom.sf(k - 1, n, 0.5)
        P(f'Kiểm định dấu: trong {n} cặp (đã bỏ hòa) có {k} cặp theo hướng H₁ (A tốt hơn B). Xác suất p = P(X ≥ {k}) với X ~ B({n}, 1/2) là', p, f'p = Σ_{{x≥{k}}} C({n},x)/2^{n} = {f(p,4)}; ' + ('p < 0.05 ⇒ bác bỏ H₀.' if p < 0.05 else 'p ≥ 0.05 ⇒ chưa đủ cơ sở bác bỏ H₀.'), 3, TOP['sign'], SRC, extra=[2 * p, 0.5 ** n, k / n], d=4)
    # 5. tần số lý thuyết chuẩn
    for n, mu, sg, a, b in [(100, 364.7, 26.7, 345, 355), (200, 50, 5, 45, 55), (150, 10, 2, 8, 9), (80, 70, 8, 60, 72), (120, 0, 1, -1, 0.5), (500, 100, 15, 85, 130), (60, 12, 3, 9, 12), (300, 5.5, 0.4, 5.1, 5.9)]:
        p = st.norm.cdf((b - mu) / sg) - st.norm.cdf((a - mu) / sg); e = n * p
        P(f'Kiểm định phù hợp chuẩn N({mu}; {sg}²) với n = {n}. Tần số lý thuyết e_j của lớp ({a}; {b}] là', e, f'p_j = Φ(({b} − {mu})/{sg}) − Φ(({a} − {mu})/{sg}) = {f(p,4)}; e_j = n·p_j = {f(e,2)}.', 2, TOP['gof'], SRC, extra=[p, n * (st.norm.cdf((b - mu) / sg)), e * 1.2], d=2, hi=None)
    # 6. kiểm định dấu hai phía / giá trị tới hạn
    for n, k in [(10, 8), (14, 11), (16, 12), (12, 4)]:
        p = 2 * st.binom.sf(max(k, n - k) - 1, n, 0.5)
        P(f'Kiểm định dấu hai phía: {k} dấu dương trong {n} cặp (bỏ hòa). Giá trị p hai phía = 2·P(X ≥ max(k, n − k)) là', p, f'p = 2·{f(st.binom.sf(max(k,n-k)-1,n,0.5),4)} = {f(p,4)}; ' + ('p < 0.05 ⇒ bác bỏ H₀.' if p < 0.05 else 'p ≥ 0.05 ⇒ chưa đủ cơ sở bác bỏ H₀.'), 3, TOP['sign'], SRC, extra=[p / 2, 0.5 ** n, k / n], d=4)
