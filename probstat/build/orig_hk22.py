"""Câu GỐC từ đề giữa kỳ thật HK2.2 2025–2026 (10 mã đề, file LTXSTK_HK2.2_20252026_alltests.pdf) chuyển thành MCQ/tự luận cho từng module.
Số liệu đọc từ PDF (real_exam.REAL); đáp án tính bằng SciPy; phương án nhiễu là các lỗi thường gặp."""
import math, random
from scipy import stats as st
from qb import f, fg, nd, ni
from qh import pm
import real_exam as R
Phi = st.norm.cdf
SRC = lambda code, q: f'Đề giữa kỳ thật HK2.2 2025–2026, mã đề {code}, {q}'
T = {'m02': 'Hoán vị, chỉnh hợp, tổ hợp', 'm03': 'Quy tắc cộng và bù', 'm04': 'Xác suất toàn phần', 'm05': 'Hàm xác suất, bảng phân phối (rời rạc)',
     'm06': 'Chuẩn: tính xác suất', 'm07': 'Bảng tần số, dữ liệu theo lớp', 'm08': 'Lý thuyết và bảng tra'}
def topic(mid):
    import importlib; return importlib.import_module('orig_' + mid).TOP
def ci(c, e): return f'({f(c - e, 3)}; {f(c + e, 3)})'
def build(mid, B):
    if mid not in ('m02', 'm03', 'm04', 'm05', 'm06', 'm07', 'm08'): return
    rng = random.Random(2025 + int(mid[1:])); TOP = topic(mid); V = [v for v in R.variants() if v['real']]
    for idx, v in enumerate(V):
        r = R.solve(v); S, E, P = R.stems(v); ex = R.explains(v, r); q = r['q']; code = v['code']; a = v['a'] / 100
        def N(k, val, d, extra, tkey, lvl=1, lo=0.0, hi=1.0):
            pm(B, rng, S[k], val, ex[k], lvl, TOP[tkey], SRC(code, f'câu {k+1}'), extra=extra, d=d, lo=lo, hi=hi)
        if mid == 'm08':
            N(0, q[0], 3, [st.norm.ppf(1 - a / 2), -q[0], st.norm.ppf(1 - 2 * a), st.norm.ppf(a / 2) * -1.0 + 0.1], 'theory', 1, lo=None, hi=None)
            N(7, q[7], 3, [st.norm.ppf(1 - a), st.t.ppf(1 - a / 2, v['df']), st.t.ppf(1 - a, v['df'] - 1), st.t.ppf(1 - a, v['df'] + 2)], 'theory', 2, lo=None, hi=None)
            tp = TOP['z']; tt = TOP['t']
            # câu 9b, 9c: khoảng tin cậy
            xb, s, n = r['xb'], r['s'], r['n']; u = r['u']; t = r['t']; sg = v['sig']; pc = int(round(v['conf'] * 100))
            stem = f'Mẫu thời gian điều trị theo lớp 6–8, 8–10, 10–12, 12–14 với {v["fr"][0]}, {v["fr"][1]}, {v["fr"][2]}, {v["fr"][3]} bệnh nhân (n = {n}; điểm đại diện 7, 9, 11, 13; x̄ = {f(xb,4)}, s² = {f(r["s2"],4)}). Khoảng tin cậy {pc}% cho thời gian điều trị trung bình, biết σ = {fg(sg)}, là'
            B.mcq(stem, ci(xb, r['eb']), [ci(xb, t * sg / math.sqrt(n)), ci(xb, u * s / math.sqrt(n)), ci(xb, u * sg), ci(xb, st.norm.ppf(1 - (1 - v['conf'])) * sg / math.sqrt(n))],
                  f'σ đã biết ⇒ dùng U_{{α/2}} = {f(u,3)}; e = U·σ/√n = {f(u,3)}·{fg(sg)}/√{n} = {f(r["eb"],4)}; khoảng = x̄ ± e.', 2, tp, SRC(code, 'câu 9b'), 'goc')
            stem = f'Cùng mẫu trên (n = {n}, x̄ = {f(xb,4)}, s = {f(s,4)}), σ chưa biết. Khoảng tin cậy {pc}% cho thời gian điều trị trung bình là'
            B.mcq(stem, ci(xb, r['ec']), [ci(xb, u * s / math.sqrt(n)), ci(xb, t * sg / math.sqrt(n)), ci(xb, st.t.ppf(1 - (1 - v['conf']) / 2, n) * s / math.sqrt(n)), ci(xb, t * s)],
                  f'σ chưa biết ⇒ dùng t_{{α/2}}({n-1}) = {f(t,3)}; e = t·s/√n = {f(t,3)}·{f(s,4)}/√{n} = {f(r["ec"],4)}.', 3, tt, SRC(code, 'câu 9c'), 'goc')
            B.essay(f'Đề giữa kỳ thật HK2.2 2025–2026, mã đề {code}, câu 9 (6 điểm). {E} ' + ' '.join(P),
                    f'(a) x̄ = {f(r["xb"],4)}; s² = {f(r["s2"],4)}. (b) U = {f(u,3)}; e = {f(r["eb"],4)}; khoảng ({f(r["b"][0],3)}; {f(r["b"][1],3)}). (c) t({n-1}) = {f(t,3)}; e = {f(r["ec"],4)}; khoảng ({f(r["c"][0],3)}; {f(r["c"][1],3)}).',
                    3, tt, SRC(code, 'câu 9'), 'goc')
        elif mid == 'm02':
            c2 = q[1]; nm, nu = v['nm'], v['nu']
            B.mcq(S[1], str(c2), [str(math.perm(nm, 2) * math.perm(nu, 3)), str(math.comb(nm + nu, 5)), str(math.comb(nm, 3) * math.comb(nu, 2)), str(math.comb(nm, 2) + math.comb(nu, 3))], ex[1], 1, TOP['perm'], SRC(code, 'câu 2'), 'goc')
        elif mid == 'm03':
            if idx in (0, 3, 7): N(2, q[2], 2, [v['pA'], 1 + v['pA'], v['pA'] ** 2], 'add')
            if idx % 2 == 0: N(3, q[3], 4, [3 * v['pA'], 1 - (1 - v['pA']) ** 3, v['pA'] ** 2, 1 - v['pA'] ** 3], 'cond', 1)
        elif mid == 'm04':
            N(4, q[4], 4, [0.45 * v['pm'] + 0.55 * v['pf'], (v['pm'] + v['pf']) / 2, v['pm'] + v['pf'], v['pm'] * v['pf']], 'total', 1)
        elif mid == 'm05':
            N(5, q[5], 2, [v['pm'] + v['pf'] + v['p3'], 1 - v['pm'] - v['pf'], 1 - v['p3'], q[5] + 0.1], 'pmf', 1)
        elif mid == 'm06':
            z1, z0 = r['z1'], r['z0']
            N(6, q[6], 4, [Phi(z1), 1 - Phi(z0), Phi(z1) + Phi(z0) - 1 + 0.2, Phi((v['up'] - v['mu']) / v['sg'] ** 2) - Phi((4 - v['mu']) / v['sg'] ** 2)], 'normp', 2)
        elif mid == 'm07':
            n, xb, s2 = r['n'], r['xb'], r['s2']; fr = v['fr']
            ends = [6, 8, 10, 12]
            xe = sum(k * e for k, e in zip(fr, ends)) / n
            wrong = [f'x̄ = {f(xb,4)}, s² = {f(s2*(n-1)/n,4)}', f'x̄ = {f(xe,4)}, s² = {f(s2,4)}', f'x̄ = {f(xb,4)}, s² = {f(math.sqrt(s2),4)}']
            B.mcq(f'Thời gian điều trị theo lớp 6–8, 8–10, 10–12, 12–14 với {fr[0]}, {fr[1]}, {fr[2]}, {fr[3]} bệnh nhân (n = {n}; trung điểm 7, 9, 11, 13). Trung bình mẫu x̄ và phương sai mẫu s² là',
                  f'x̄ = {f(xb,4)}, s² = {f(s2,4)}', wrong, f'x̄ = Σf·m/n = {r["sxm"]}/{n} = {f(xb,4)}; s² = (Σf·m² − n·x̄²)/(n − 1) = ({r["sxm2"]} − {n}·{f(xb,4)}²)/{n-1} = {f(s2,4)}.', 2, TOP['group'], SRC(code, 'câu 9a'), 'goc')
