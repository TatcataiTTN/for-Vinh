"""Module 10 — biến thể tham số (bo_sung): kiểm định kỳ vọng, tỷ lệ, lực lượng kiểm định."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
from orig_m10 import TOP, U, T, REJ, ACC, decide, region
SRC = 'Bổ sung: biến thể tham số của dạng bài §3.1–3.2 và đề thi (đáp án tính bằng SciPy)'
def build(B):
    rng = random.Random(1910)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); k.setdefault('origin', 'bo_sung'); return pm(B, rng, stem, v, *a, **k)
    cases = [(50, 52.3, 6, 25, '>', 0.05, False), (100, 97, 8, 16, '<', 0.05, False), (20, 20.8, 2.4, 36, '≠', 0.05, False), (75, 71.5, 9, 12, '<', 0.01, False),
             (12, 12.9, 1.5, 30, '>', 0.01, False), (200, 195, 15, 20, '≠', 0.05, False), (3.5, 3.9, 0.8, 9, '>', 0.05, False), (500, 492, 30, 40, '<', 0.05, False),
             (60, 63, 5, 49, '>', 0.05, True), (25, 24.1, 3, 36, '<', 0.05, True), (150, 153, 10, 25, '≠', 0.01, True), (8, 8.6, 2, 64, '>', 0.01, True)]
    for mu0, xb, s, n, alt, al, known in cases:
        tq = (xb - mu0) / (s / math.sqrt(n)); a_ = al / 2 if alt == '≠' else al; crit = U(a_) if known else T(a_, n - 1); rej = decide(tq, crit, alt)
        h1 = {'>': f'μ > {mu0}', '<': f'μ < {mu0}', '≠': f'μ ≠ {mu0}'}[alt]; nm = 'U' if known else 't'
        tx = f'Tổng thể chuẩn. H₀: μ = {mu0}, H₁: {h1}. Mẫu n = {n}, x̄ = {xb}, ' + (f'σ = {s} (đã biết)' if known else f's = {s}') + f'. Mức ý nghĩa {al*100:g}%.'
        P(tx + ' Giá trị quan sát T_qs là', tq, f'T_qs = ({xb} − {mu0})/({s}/√{n}) = {f(tq,3)}.', 1 if known else 2, TOP['z'] if known else TOP['t'], SRC, extra=[-tq, tq / math.sqrt(n), (xb - mu0) / s], d=3, lo=None)
        P(tx + f' Giá trị tới hạn dùng cho miền bác bỏ là', crit, f'{nm} = {f(crit,3)} ' + ('(hai phía: α/2)' if alt == '≠' else '(một phía: α)') + ' ⇒ miền bác bỏ ' + region(alt, nm, f(crit, 3)) + '.', 2, TOP['z'] if known else TOP['t'], SRC, extra=[U(al) if not known else T(al, n - 1), U(al / 2) if not known else T(al / 2, n - 1), crit * 1.15], d=3)
        a, b = (REJ, ACC) if rej else (ACC, REJ)
        B.mcq(tx + f' Kết luận (T_qs = {f(tq,3)}, tới hạn {f(crit,3)}):', a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], f'{region(alt,nm,f(crit,3))}; T_qs = {f(tq,3)} ' + ('thuộc' if rej else 'không thuộc') + ' miền bác bỏ.', 3, TOP['dec'], SRC, 'bo_sung')
    # tỷ lệ
    for n, k_, p0, alt, al in [(200, 118, 0.5, '>', 0.05), (400, 80, 0.25, '<', 0.05), (150, 90, 0.5, '≠', 0.05), (500, 215, 0.4, '≠', 0.01)]:
        fq = k_ / n; z = (fq - p0) / math.sqrt(p0 * (1 - p0) / n); crit = U(al / 2 if alt == '≠' else al); rej = decide(z, crit, alt)
        P(f'H₀: p = {p0}; mẫu n = {n} có {k_} thành công (f = {f(fq,4)}). Giá trị quan sát z = (f − p₀)/√(p₀(1−p₀)/n) là', z, f'z = ({f(fq,4)} − {p0})/√({p0}·{1-p0:.2f}/{n}) = {f(z,3)}.', 2, TOP['p'], SRC, extra=[-z, (fq - p0) / math.sqrt(fq * (1 - fq) / n), z / 2], d=3, lo=None)
        a, b = (REJ, ACC) if rej else (ACC, REJ)
        B.mcq(f'H₀: p = {p0}, H₁: p {alt} {p0}; n = {n}, {k_} thành công, α = {al*100:g}%. Kết luận (z = {f(z,3)}, tới hạn {f(crit,3)}):', a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], f'z = {f(z,3)} so với miền bác bỏ ' + region(alt, 'U', f(crit, 3)) + '.', 3, TOP['dec'], SRC, 'bo_sung')
    # p-value
    for tq, df in [(2.1, 15), (1.5, 24), (-2.5, 24), (3.0, 10)]:
        pv = 1 - st.t.cdf(tq, df) if tq > 0 else st.t.cdf(tq, df)
        P(f'T_qs = {tq} với t({df}); giá trị p một phía (P(T {">" if tq>0 else "<"} {tq})) là', pv, f'p = {f(pv,4)}; với α = 5%: ' + ('p < α ⇒ bác bỏ H₀.' if pv < 0.05 else 'p > α ⇒ không bác bỏ H₀.'), 3, TOP['hyp'], SRC, extra=[2 * pv, 1 - pv, pv / 2], d=4)
    # lực lượng
    for mu0, mu1, sg, n, al in [(100, 105, 10, 25, 0.05), (50, 52, 5, 36, 0.05), (20, 21, 3, 49, 0.01), (0, 0.5, 1, 30, 0.05)]:
        crit_x = mu0 + U(al) * sg / math.sqrt(n); beta = st.norm.cdf((crit_x - mu1) / (sg / math.sqrt(n))); pw = 1 - beta
        P(f'Kiểm định H₀: μ = {mu0} với H₁: μ > {mu0}, σ = {sg}, n = {n}, α = {al*100:g}%. Nếu thực tế μ = {mu1}, lực lượng kiểm định η = 1 − β bằng', pw, f'Bác bỏ khi x̄ > {mu0} + {f(U(al),3)}·{sg}/√{n} = {f(crit_x,3)}; β = P(x̄ ≤ {f(crit_x,3)} | μ = {mu1}) = {f(beta,4)} ⇒ η = {f(pw,4)}.', 3, TOP['hyp'], SRC, extra=[beta, al, 0.5], d=4)
