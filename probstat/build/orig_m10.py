"""Module 10 — Kiểm định giả thuyết về kỳ vọng (σ biết/chưa biết), một/hai phía, sai lầm loại I/II.
Gốc: Lecture Notes §3.1–3.2 (Ví dụ 3.1–3.3, Bài 3.1–3.9), Kreyszig PS 25.4 (Prob. 3–9, 11), đề cuối kỳ (HK2 3TC câu 3 ×4, đề mẫu 2024 câu 3 ×4, 2TC câu 3 ×4, 2021–2022 câu 3 ×2)."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'hyp': 'Giả thuyết, đối thuyết, sai lầm', 'z': 'Kiểm định kỳ vọng, σ đã biết (U)', 't': 'Kiểm định kỳ vọng, σ chưa biết (t)', 'p': 'Kiểm định tỷ lệ (xấp xỉ chuẩn)', 'dec': 'Kết luận (miền bác bỏ)', 'theory': 'Lý thuyết'}
U = lambda a: st.norm.ppf(1 - a); T = lambda a, d: st.t.ppf(1 - a, d)
REJ = 'Bác bỏ H₀, chấp nhận H₁'; ACC = 'Chưa đủ cơ sở bác bỏ H₀ (chấp nhận H₀)'
def gstats(lo, w, ns):
    mids = [lo + w * (i + 0.5) for i in range(len(ns))]; N = sum(ns); m = sum(a * b for a, b in zip(mids, ns)) / N
    return N, m, sum(b * (a - m) ** 2 for a, b in zip(mids, ns)) / (N - 1)
def decide(tq, crit, alt):
    return (tq > crit) if alt == '>' else (tq < -crit) if alt == '<' else (abs(tq) > crit)
def region(alt, name, crit): return {'>': f'T > {crit}', '<': f'T < −{crit}', '≠': f'|T| > {crit}'}[alt]
def build(B):
    rng = random.Random(1010)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); return pm(B_, r_, stem, v, *a, **k)
    def dec(stem, rej, expl, lvl, topic, src, origin='goc'):
        a, b = (REJ, ACC) if rej else (ACC, REJ)
        B.mcq(stem, a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], expl, lvl, topic, src, origin)
    def full(label, mu0, xb, s, n, alt, al, known=None, src='', topic=None, lvl=2, extra=''):
        """Sinh 3 MCQ: giá trị quan sát, giá trị tới hạn, kết luận."""
        tq = (xb - mu0) / ((known if known else s) / math.sqrt(n)); df = n - 1
        crit = U(al if alt != '≠' else al / 2) if known else T(al if alt != '≠' else al / 2, df)
        rej = decide(tq, crit, alt); nm = 'U' if known else 't'
        h1 = {'>': f'μ > {mu0}', '<': f'μ < {mu0}', '≠': f'μ ≠ {mu0}'}[alt]
        tp = topic or (TOP['z'] if known else TOP['t'])
        P(B, rng, f'{label} H₀: μ = {mu0}, H₁: {h1}, n = {n}, x̄ = {fg(xb,4)}, ' + (f'σ = {known}' if known else f's = {fg(s,4)}') + f'. Giá trị quan sát T_qs = (x̄ − μ₀)/(' + ('σ' if known else 's') + '/√n) là', tq,
          f'T_qs = ({fg(xb,4)} − {mu0})/({fg(known if known else s,4)}/√{n}) = {f(tq,3)}. {extra}', lvl, tp, src, extra=[-tq, tq / math.sqrt(n), (xb - mu0) / (known if known else s)], d=3, lo=None)
        P(B, rng, f'{label} Mức ý nghĩa α = {al*100:g}%, {"một" if alt!="≠" else "hai"} phía ({"σ biết" if known else "σ chưa biết, t(n−1) = t(" + str(df) + ")"}). Giá trị tới hạn {nm}' + ('_{α/2}' if alt == '≠' else '_α') + ' là', crit, f'{nm}' + ('_{α/2}' if alt == '≠' else '_α') + f' = {f(crit,3)}: ' + region(alt, nm, f(crit, 3)) + ' là miền bác bỏ.', lvl, tp, src, extra=[U(al) if not known else T(al, df), crit * 1.2, U(al / 2) if not known else T(al / 2, df)], d=3)
        dec(f'{label} H₀: μ = {mu0}, H₁: {h1}; T_qs = {f(tq,3)}, giá trị tới hạn {f(crit,3)} ở mức {al*100:g}%. Kết luận là', rej, f'Miền bác bỏ {region(alt,nm,f(crit,3))}; T_qs = {f(tq,3)} ' + ('thuộc' if rej else 'không thuộc') + ' miền bác bỏ ⇒ ' + (REJ if rej else ACC) + '.', lvl + 1 if lvl < 3 else 3, TOP['dec'], src)
    S = 'Lecture Notes '
    # Ví dụ 3.1
    full('Dây kim loại (Ví dụ 3.1): mẫu', 200, 197, 6, 25, '<', 0.05, None, S + 'Ví dụ 3.1', extra='Giáo trình: T_qs = −2.5 < −1.71 ⇒ bác bỏ H₀.')
    # Ví dụ 3.2: ngưỡng
    k2 = U(0.025) * 3 / math.sqrt(10)
    P(B, rng, 'X chuẩn, σ² = 9, n = 10, kiểm định H₀: μ = 24 so với H₁: μ ≠ 24 ở mức 5%. Bác bỏ H₀ khi x̄ nhỏ hơn bao nhiêu (cận dưới của miền bác bỏ)? (Ví dụ 3.2i)', 24 - k2, f'|x̄ − 24| > 1.96·3/√10 = {f(k2,3)} ⇒ x̄ < {f(24-k2,2)} hoặc x̄ > {f(24+k2,2)}.', 2, TOP['dec'], S + 'Ví dụ 3.2(i)', extra=[24 - 1.645 * 3 / math.sqrt(10), 24 - k2 * 2, 22.14 + 0.1], d=2)
    P(B, rng, 'Cùng bài (σ² = 9, n = 10, μ₀ = 24), đối thiết H₁: μ > 24 ở mức 5%. Bác bỏ H₀ khi x̄ lớn hơn bao nhiêu? (Ví dụ 3.2ii)', 24 + U(0.05) * 3 / math.sqrt(10), f'x̄ > 24 + 1.645·3/√10 = {f(24+U(0.05)*3/math.sqrt(10),2)} (giáo trình in nhầm 25.58 ở phần chấp nhận).', 2, TOP['dec'], S + 'Ví dụ 3.2(ii)', extra=[24 + k2, 24 - 1.645 * 3 / math.sqrt(10), 25.86 + 0.3], d=2)
    P(B, rng, 'Cùng bài, đối thiết H₁: μ < 24 ở mức 5%. Bác bỏ H₀ khi x̄ nhỏ hơn bao nhiêu? (Ví dụ 3.2iii)', 24 - U(0.05) * 3 / math.sqrt(10), f'x̄ < 24 − 1.645·3/√10 = {f(24-U(0.05)*3/math.sqrt(10),2)} ≈ 22.44.', 2, TOP['dec'], S + 'Ví dụ 3.2(iii)', extra=[24 - k2, 24 + 1.645 * 3 / math.sqrt(10), 22.86], d=2)
    # Ví dụ 3.3
    full('Dây thừng (Ví dụ 3.3): mẫu', 4500, 4482, 115, 16, '<', 0.05, None, S + 'Ví dụ 3.3', extra='Giáo trình: t₀.₀₅(15) = 1.75 (A9) ⇒ T_qs = −0.626, chấp nhận H₀.')
    # Bài 3.1
    xs = [0, 1, -1, 3, -8, 6, 1]; n = len(xs); xb = sum(xs) / n; s = math.sqrt(sum((x - xb) ** 2 for x in xs) / (n - 1))
    full('Bài 3.1 (= Kreyszig PS 25.4/3): mẫu 0, 1, −1, 3, −8, 6, 1 (chuẩn);', 0, xb, s, n, '>', 0.05, None, S + 'Bài 3.1 / Kreyszig PS 25.4 Prob. 3', extra=f'x̄ = {f(xb,4)}, s = {f(s,4)}.')
    # Bài 3.2, 3.3, 3.4
    full('Bài 3.2: chuẩn σ² = 9, mẫu n = 20 có x̄ = 58.50;', 60.0, 58.5, 3, 20, '<', 0.05, 3, S + 'Bài 3.2 / Kreyszig PS 25.4 Prob. 6', extra='Đối thiết μ = 57 < 60 ⇒ kiểm định một phía bên trái.')
    full('Bài 3.3: chuẩn σ² = 9, mẫu nhỏ n = 5 có x̄ = 58.05;', 60.0, 58.05, 3, 5, '<', 0.05, 3, S + 'Bài 3.3 / Kreyszig PS 25.4 Prob. 7', lvl=3, extra='Kết luận thay đổi so với n = 20: mẫu nhỏ làm T_qs gần 0.')
    k34 = U(0.025)
    B.mcq('Bài 3.4: với σ² = 9, n = 20, μ₀ = 60, kiểm định hai phía mức 5%, miền bác bỏ của T = (x̄ − 60)/(3/√20) là', '|T| > 1.960', ['T > 1.645', 'T < −1.645', '|T| > 2.576'], 'Hai phía: U_{α/2} = U₀.₀₂₅ = 1.960 (Kreyszig PS 25.4/9).', 1, TOP['dec'], S + 'Bài 3.4 / Kreyszig PS 25.4 Prob. 9')
    # Bài 3.5
    full('Bài 3.5 (= Kreyszig PS 25.4/11): can dầu 5000 g, mẫu n = 51 có x̄ = 4990, s = 20;', 5000, 4990, 20, 51, '≠', 0.05, None, S + 'Bài 3.5 / Kreyszig PS 25.4 Prob. 11')
    # Bài 3.6
    full('Bài 3.6: lốp xe, nhà sản xuất khẳng định > 35 000 dặm; mẫu n = 25 có x̄ = 37 000, s = 5000;', 35000, 37000, 5000, 25, '>', 0.05, None, S + 'Bài 3.6', extra='H₁ là khẳng định của nhà sản xuất; bác bỏ H₀ ủng hộ khẳng định.')
    # Bài 3.7
    dd = [0.4, -0.6, 0.2, 0.0, 1.0, 1.4, 0.4, 1.6]; n7 = 8; xb7 = sum(dd) / n7; s7 = math.sqrt(sum((x - xb7) ** 2 for x in dd) / (n7 - 1))
    full('Bài 3.7: sai khác điện áp hai vôn kế 0.4, −0.6, 0.2, 0.0, 1.0, 1.4, 0.4, 1.6 (chuẩn);', 0, xb7, s7, n7, '≠', 0.05, None, S + 'Bài 3.7', extra=f'x̄ = {f(xb7,3)}, s = {f(s7,3)}.')
    # Bài 3.8, 3.9
    N8, m8, v8 = gstats(98.0, 0.5, [2, 6, 10, 7, 4]); full('Bài 3.8: bao sản phẩm, quy định 100 kg, nghi ngờ đóng thiếu (29 bao, 98–100.5 theo lớp 0.5: 2, 6, 10, 7, 4);', 100, m8, math.sqrt(v8), N8, '<', 0.05, None, S + 'Bài 3.8', extra=f'x̄ = {f(m8,3)}, s = {f(math.sqrt(v8),3)}.')
    N9, m9, v9 = gstats(48.5, 0.5, [4, 10, 9, 3, 2]); full('Bài 3.9: mức tiêu thụ xăng, kỳ vọng 50 lít, nghi giảm (28 xe, 48.5–51 theo lớp 0.5: 4, 10, 9, 3, 2), mức ý nghĩa 2.5%;', 50, m9, math.sqrt(v9), N9, '<', 0.025, None, S + 'Bài 3.9', extra=f'x̄ = {f(m9,3)}, s = {f(math.sqrt(v9),3)}.')
    # Kreyszig 4,5: Buffon, Pearson
    for src, h, n_ in [('Buffon', 2048, 4040), ('Pearson', 6019, 12000)]:
        pf = h / n_; z = (pf - 0.5) / math.sqrt(0.25 / n_); rej = abs(z) > U(0.025)
        P(B, rng, f'{src} tung đồng xu {n_} lần được {h} mặt ngửa. Kiểm định H₀: p = 0.5 (đồng xu công bằng) bằng xấp xỉ chuẩn, giá trị quan sát z = (f − 0.5)/√(0.25/n) là', z, f'f = {f(pf,5)}; z = {f(z,3)}; |z| ' + ('>' if rej else '<') + ' 1.960 ⇒ ' + (REJ if rej else ACC) + ' ở mức 5% (Kreyszig PS 25.4).', 3, TOP['p'], 'Kreyszig PS 25.4, Prob. ' + ('4' if src == 'Buffon' else '5'), extra=[-z, pf - 0.5, z / 2], d=3, lo=None)
        dec(f'{src}: {h} mặt ngửa/{n_} lần. Ở mức 5%, kiểm định hai phía H₀: p = 0.5 cho kết luận:', rej, f'z = {f(z,3)} so với ±1.960 ⇒ ' + (REJ if rej else ACC) + '.', 3, TOP['dec'], 'Kreyszig PS 25.4, Prob. ' + ('4' if src == 'Buffon' else '5'))
    # ===== Đề thi thật =====
    sets = [('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 1, câu 3', 5.75, 5.0, 0.4, [2, 4, 7, 8, 4, 2], 0.05, 'mức tiêu thụ nhiên liệu (lít/100 km)', 4.389),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 2, câu 3', 6.05, 5.5, 0.4, [2, 4, 7, 8, 4, 2], 0.01, 'mức tiêu thụ nhiên liệu (lít/100 km)', None),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 3, câu 3', 4.75, 4.1, 0.4, [3, 4, 7, 8, 4, 3], 0.05, 'mức tiêu thụ nhiên liệu (lít/100 km)', None),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 4, câu 3', 5.05, 4.3, 0.4, [3, 4, 8, 9, 3, 2], 0.01, 'mức tiêu thụ nhiên liệu (lít/100 km)', None),
            ('Đề mẫu 03/2024, đề số 1, câu 3', 5.95, 4.6, 0.6, [2, 3, 8, 9, 5, 4], 0.05, 'mức tiêu thụ nhiên liệu xe 5 năm (lít/100 km)', None),
            ('Đề mẫu 03/2024, đề số 2, câu 3', 5.85, 4.7, 0.6, [2, 3, 8, 9, 5, 4], 0.05, 'mức tiêu thụ nhiên liệu xe 7 năm (lít/100 km)', None),
            ('Đề mẫu 03/2024, đề số 3, câu 3', 5.89, 4.6, 0.6, [2, 4, 9, 8, 4, 4], 0.01, 'mức tiêu thụ nhiên liệu xe 5 năm (lít/100 km)', None),
            ('Đề mẫu 03/2024, đề số 4, câu 3', 6.85, 5.6, 0.6, [2, 3, 8, 9, 5, 4], 0.01, 'mức tiêu thụ nhiên liệu xe 6 năm (lít/100 km)', None),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 1, câu 3', 23, 15.5, 3.5, [2, 4, 7, 8, 4], 0.01, 'chỉ số BMI (kg/m²), nghi nhóm I thừa cân (BMI > 23)', None),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 2, câu 3', 23, 15.5, 3.5, [2, 4, 7, 7, 3], 0.05, 'chỉ số BMI (kg/m²), nghi nhóm I thừa cân', None),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 3, câu 3', 23, 15.5, 3.5, [1, 3, 7, 7, 3], 0.05, 'chỉ số BMI (kg/m²), nghi nhóm I thừa cân', None),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 4, câu 3', 23, 15.5, 3.5, [2, 5, 7, 9, 4], 0.05, 'chỉ số BMI (kg/m²), nghi nhóm I thừa cân', None)]
    for src, mu0, lo_, w, ns_, al, nm, offT in sets:
        N, m, v = gstats(lo_, w, ns_); s = math.sqrt(v); tq = (m - mu0) / (s / math.sqrt(N)); crit = T(al, N - 1); rej = tq > crit
        cls = '; '.join(f'{fg(lo_+w*i)}–{fg(lo_+w*(i+1))}: {c}' for i, c in enumerate(ns_))
        P(B, rng, f'{nm.capitalize()} ~ chuẩn. H₀: μ = {mu0}, H₁: μ > {mu0}; mẫu theo lớp — {cls}. Giá trị quan sát T_qs = (x̄ − μ₀)/(s/√N) là', tq, f'N = {N}; x̄ = {f(m,3)}; s = {f(s,3)}; T_qs = {f(tq,3)}' + (f' (đáp án chính thức {offT}).' if offT else '.'), 3, TOP['t'], src + ' (T_qs)', extra=[-tq, (m - mu0) / s, tq / 2], d=3, lo=None)
        P(B, rng, f'Cùng bài ({nm}, H₁: μ > {mu0}, α = {al*100:g}%, N = {N}). Giá trị tới hạn t_α(N − 1) là', crit, f't_{{{al}}}({N-1}) = {f(crit,3)} (bảng A9 làm tròn: {crit:.2f}); miền bác bỏ T > {f(crit,3)}.', 2, TOP['t'], src + ' (t_α)', extra=[T(al / 2, N - 1), U(al), T(al, N)], d=3)
        dec(f'{nm.capitalize()}, H₀: μ = {mu0}, H₁: μ > {mu0}, mức ý nghĩa {al*100:g}%, N = {N}: T_qs = {f(tq,3)}, t_α = {f(crit,3)}. Kết luận là', rej, f'T_qs {f(tq,3)} ' + ('>' if rej else '≤') + f' {f(crit,3)} ⇒ ' + (REJ if rej else ACC) + '.', 3, TOP['dec'], src + ' (kết luận)')
    for a, b, src in [(9, 2, 'Đáp án đề số 1 thi 22/12/2021, câu 3'), (4, 3, 'Đáp án đề số 2 thi 22/12/2021, câu 3')]:
        xs3 = [3080, 3100, 3150 + a, 3180 + b, 3200]; m3 = sum(xs3) / 5; tq = (m3 - 3150) / (10 / math.sqrt(5)); crit = U(0.01); rej = tq < -crit
        P(B, rng, f'σ = 10, H₀: μ = 3150, H₁: μ < 3150, mẫu 3080, 3100, {3150+a}, {3180+b}, 3200 (a = {a}, b = {b}), α = 1%. Giá trị quan sát T_qs là', tq, f'x̄ = {f(m3,2)}; T_qs = ({f(m3,2)} − 3150)/(10/√5) = {f(tq,4)}; U₀.₀₁ = 2.326; miền bác bỏ T < −2.326.', 2, TOP['z'], src, extra=[-tq, (m3 - 3150) / 10, tq / 2], d=4, lo=None)
        dec(f'Cùng bài (a = {a}, b = {b}): kết luận ở mức 1% là', rej, f'T_qs = {f(tq,3)} ' + ('<' if rej else '≥') + ' −2.326 ⇒ ' + (REJ if rej else ACC) + ' (đáp án chính thức: chấp nhận H₀).', 3, TOP['dec'], src)
    # ===== Lý thuyết =====
    S2 = 'Lecture Notes §3.1–3.2'
    for stem, ans, wr, ex, lvl in [
        ('Sai lầm loại I trong kiểm định là:', 'Bác bỏ H₀ trong khi H₀ đúng; xác suất bằng mức ý nghĩa α', ['Chấp nhận H₀ trong khi H₀ sai', 'Bác bỏ H₁ trong khi H₁ đúng', 'Xác suất bằng β = 1 − α'], 'Mục 3.1.2.', 1),
        ('Sai lầm loại II là:', 'Thừa nhận H₀ trong khi H₁ đúng; xác suất β; lực lượng kiểm định η = 1 − β', ['Bác bỏ H₀ trong khi H₀ đúng', 'Xác suất bằng α', 'Luôn bằng 0'], 'Khi T_qs ∉ W_α nhưng H₁ đúng; η = 1 − β là lực lượng (power).', 1),
        ('Khi giảm α (ví dụ từ 5% xuống 1%) với cùng cỡ mẫu thì xác suất sai lầm loại II β:', 'Tăng lên', ['Giảm xuống', 'Không đổi', 'Bằng 0'], 'Hai loại sai lầm đánh đổi nhau; muốn giảm cả hai cần tăng n.', 2),
        ('Miền bác bỏ của kiểm định một phía bên phải H₁: μ > μ₀ (σ đã biết) ở mức α là:', 'T > U_α', ['|T| > U_{α/2}', 'T < −U_α', 'T > U_{α/2}'], 'Công thức (3.6).', 1),
        ('Miền bác bỏ của kiểm định hai phía H₁: μ ≠ μ₀ (σ chưa biết) là:', '|T| > t_{α/2}(n − 1)', ['T > t_α(n − 1)', 'T < −t_α(n)', '|T| > U_{α/2}'], 'Công thức (3.10).', 1),
        ('Tiêu chuẩn kiểm định cho μ khi σ chưa biết là:', 'T = (X̄ − μ₀)/(S/√n) ~ t(n − 1) nếu H₀ đúng', ['T = (X̄ − μ₀)/(σ/√n) ~ N(0,1)', 'T = (n − 1)S²/σ₀² ~ χ²(n − 1)', 'T = X̄ − μ₀'], 'Định lý 2.2.', 1),
        ('Quy tắc kết luận: nếu T_qs không thuộc miền bác bỏ W_α thì:', 'Chưa đủ cơ sở để bác bỏ H₀ (trên thực tế thừa nhận H₀)', ['Chứng minh được H₀ đúng', 'Chấp nhận H₁', 'Bác bỏ H₀'], 'Bước 7 của thủ tục kiểm định.', 1),
        ('Trong bài “nghi ngờ mức tiêu thụ thực tế CAO HƠN số nhà sản xuất đưa ra (μ₀)”, đối thuyết là:', 'H₁: μ > μ₀', ['H₁: μ < μ₀', 'H₁: μ ≠ μ₀', 'H₁: μ = μ₀'], 'Đối thuyết là điều đang nghi ngờ/cần chứng minh; H₀: μ = μ₀.', 1),
        ('p-value nhỏ hơn α nghĩa là:', 'Bác bỏ H₀ ở mức α', ['Chấp nhận H₀', 'Kiểm định sai', 'Mẫu quá nhỏ'], 'Cùng kết luận với so sánh T_qs và miền bác bỏ.', 2)]:
        B.mcq(stem, ans, wr, ex, lvl, TOP['theory'] if lvl == 1 else TOP['hyp'], S2)
    B.essay('Đề HK2 đề 1 câu 3: Z chuẩn, H₀: μ = 5.75, H₁: μ > 5.75, mẫu theo lớp 5.0–7.4 (2; 4; 7; 8; 4; 2), α = 5%. Trình bày đầy đủ.', 'N = 27; z̄ = 6.207; s² ≈ 0.288 (đáp án chính thức 0.293 do làm tròn x̄ trước khi bình phương); T_qs ≈ 4.43 (chính thức 4.389); t₀.₀₅(26) ≈ 1.71 ⇒ T_qs ∈ W_α ⇒ bác bỏ H₀: mức tiêu thụ thực tế cao hơn.', 2, TOP['t'], 'Đề cuối kỳ 2022–2023 HK2, đề số 1, câu 3')
    B.essay('Ví dụ 3.1 (Lecture Notes): cuộn dây kim loại, H₀: μ = 200, H₁: μ < 200, n = 25, x̄ = 197, s = 6, α = 5%.', 'T = (197 − 200)/(6/√25) = −2.5; t₀.₀₅(24) = 1.711; W_α = {T < −1.711}; T_qs ∈ W_α ⇒ bác bỏ H₀.', 2, TOP['t'], S + 'Ví dụ 3.1')
    B.essay('Bài 3.2–3.3 (Lecture Notes): σ² = 9, H₀: μ = 60, H₁: μ < 60; n = 20 với x̄ = 58.5 và n = 5 với x̄ = 58.05, α = 5%. So sánh hai kết luận.', 'n = 20: T = −2.236 < −1.645 ⇒ bác bỏ. n = 5: T = −1.453 > −1.645 ⇒ chấp nhận. Mẫu nhỏ làm giảm lực lượng kiểm định.', 2, TOP['z'], S + 'Bài 3.2–3.3')
    B.essay('Bài 3.5 (Lecture Notes): can dầu 5000 g, n = 51, x̄ = 4990, s = 20, mức 5%, hai phía.', f'T = −3.536; t₀.₀₂₅(50) = 2.009 ⇒ |T| > 2.009 ⇒ bác bỏ H₀: máy đong lệch khỏi 5000 g.', 2, TOP['t'], S + 'Bài 3.5')
    B.essay('Kreyszig PS 25.4/4: Buffon tung 4040 lần được 2048 ngửa. Đồng xu có công bằng không?', f'f = 0.50693; z = 0.881 < 1.96 ⇒ không bác bỏ H₀: p = 0.5.', 2, TOP['p'], 'Kreyszig PS 25.4, Prob. 4')
