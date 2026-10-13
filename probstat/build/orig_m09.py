"""Module 9 — Ôn tập Chương 1–2 và đề giữa kỳ: câu của đề giữa kỳ mẫu + ngân hàng ôn tập chọn lại từ Module 1–8 (câu gốc, ưu tiên câu thuộc đề giữa kỳ/đáp án giữa kỳ)."""
import json, os, random, math
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'gk': 'Đề giữa kỳ mẫu', 'on': 'Ôn tập tổng hợp Chương 1–2'}
HERE = os.path.dirname(__file__)
def build(B):
    rng = random.Random(909)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None); return pm(B_, r_, stem, v, *a, **k)
    S = 'Đề giữa kỳ mẫu LTXSTK, '
    P(B, rng, 'BNN X có bảng phân bố xác suất: x = 2, 3, 5, 6 với P = 0.07, 0.07, 0.18, k. Giá trị k là (câu 6)', 0.68, 'Σp = 1 ⇒ k = 1 − (0.07 + 0.07 + 0.18) = 0.68.', 1, TOP['gk'], S + 'câu 6', extra=[0.32, 0.18, 0.07], d=2)
    t8 = st.t.ppf(1 - 0.08, 18)
    P(B, rng, 'Giá trị tới hạn t_α với α = 8% và phân bố Student 18 bậc tự do (P(T > t_α) = 0.08) là (câu 8)', t8, f'Tra bảng A9: t₀.₀₈(18) ≈ {f(t8,3)} (giữa t₀.₁₀ = 1.330 và t₀.₀₅ = 1.734).', 1, TOP['gk'], S + 'câu 8', extra=[1.734, 1.330, st.norm.ppf(0.92)], d=3)
    N, m, v = 26, sum(a * b for a, b in zip([7, 9, 11, 13], [4, 8, 9, 5])) / 26, 0
    v = sum(b * (a - m) ** 2 for a, b in zip([7, 9, 11, 13], [4, 8, 9, 5])) / 25
    B.mcq('Câu 9 (tự luận) đề giữa kỳ mẫu: thời gian điều trị theo lớp 6–8, 8–10, 10–12, 12–14 với 4, 8, 9, 5 bệnh nhân. Điểm số đúng cho phần (a) “tính x̄ và s²” là:', f'x̄ = {f(m,4)}, s² = {f(v,4)}', [f'x̄ = {f(m,4)}, s² = {f(v*25/26,4)}', f'x̄ = {f(sum([7,9,11,13])/4,4)}, s² = {f(v,4)}', f'x̄ = {f(m,4)}, s = {f(v,4)}'], 'Điểm giữa lớp 7, 9, 11, 13; N = 26; x̄ = 264/26; s² chia N − 1 = 25.', 2, TOP['gk'], S + 'câu 9(a)')
    # ôn tập: nạp lại từ M1–M8
    pool = []
    for mid in ['m01', 'm02', 'm03', 'm04', 'm05', 'm06', 'm07', 'm08']:
        p = os.path.join(HERE, '..', 'data', 'qbank', mid + '.json')
        if not os.path.exists(p): continue
        d = json.load(open(p, encoding='utf-8'))
        for it in d['items']:
            if it['origin'] != 'goc': continue
            pool.append((mid, it))
    pri = [x for x in pool if 'giữa kỳ' in x[1]['src'].lower()]
    rest = [x for x in pool if x not in pri]; rng.shuffle(rest)
    by = {}
    for mid, it in rest: by.setdefault(mid, []).append(it)
    chosen = [it for _, it in pri]
    per = 14
    for mid, lst in by.items(): chosen += lst[:per]
    seen = set()
    for it in chosen:
        key = it['q']
        if key in seen: continue
        seen.add(key)
        o = list(it['opts']); c = o[it['correct']]
        wrong = [x for x in o if x != c]
        B.mcq(it['q'], c, wrong, it['explain'], it['level'], TOP['on'], 'Ôn tập · ' + it['src'], 'goc')
    B.essay('Đề giữa kỳ mẫu — làm trọn câu 9: (a) x̄, s²; (b) khoảng tin cậy 90% với σ = 0.5; (c) khoảng tin cậy 90% khi σ chưa biết.', f'(a) x̄ = {f(m,4)}; s² = {f(v,4)}. (b) k = 1.645·0.5/√26 = {f(1.645*0.5/math.sqrt(26),4)} ⇒ [{f(m-1.645*0.5/math.sqrt(26),3)}; {f(m+1.645*0.5/math.sqrt(26),3)}]. (c) t₀.₀₅(25) = {f(st.t.ppf(0.95,25),3)}; k = t·s/√26 = {f(st.t.ppf(0.95,25)*math.sqrt(v)/math.sqrt(26),4)}.', 2, TOP['gk'], S + 'câu 9')
    B.essay('Đáp án giữa kỳ HK2 2022–2023 (a = 3, b = 2, c = 2): tóm tắt cách giải bốn câu (Bayes; bảng phân phối rời rạc; chuẩn rồi nhị thức; khoảng tin cậy t).', 'Câu 1: P(B) = 0.607; P(A₂|B) = 0.183. Câu 2: m = 0.222; P(0.5 < T < 2.5) = 0.498; E(T) = 1.5288; σ² = 1.25317. Câu 3: Φ(1) − Φ(0) = 0.3413; C(6,2)p²(1 − p)⁴ = 0.3289. Câu 4: n = 22, ȳ = 173.455, s = 2.385, t = 1.72 ⇒ [172.58; 174.329].', 2, TOP['gk'], 'Đáp án giữa kỳ HK2 2022–2023')
