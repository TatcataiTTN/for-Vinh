"""Module 13 — Tương quan và hồi quy tuyến tính đơn. Gốc: Lecture Notes §4.1–4.2 (Ví dụ 4.1, Bài 4.1–4.10), Kreyszig §25.9 (PS 25.9 Prob. 1–10, 12–15; Example 4),
đề cuối kỳ (HK2 câu 4 ×4 hồi quy, 2024 câu 4 ×4 tương quan, 2TC câu 4 ×4 hồi quy, 2021–2022 câu 4 ×2)."""
import math, random
from scipy import stats as st
import numpy as np
from qb import f, fg, nd
from qh import pm
TOP = {'reg': 'Đường hồi quy tuyến tính mẫu', 'corr': 'Hệ số tương quan mẫu', 'pred': 'Dự báo bằng hồi quy', 'test': 'Kiểm định và khoảng tin cậy (mở rộng)', 'theory': 'Lý thuyết'}
def lr(x, y):
    r = st.linregress(x, y); return r.slope, r.intercept, r.rvalue, r
def mine(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n; sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    k1 = sxy / sxx; k0 = my - k1 * mx; return k1, k0, sxy / math.sqrt(sxx * syy)
def build(B):
    rng = random.Random(1313)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 and k.get('prob') else None); k.pop('prob', None); k.setdefault('lo', None); return pm(B_, r_, stem, v, *a, **k)
    def reg(label, x, y, src, xpred=None, lvl=2, full=True):
        k1, k0, rr = mine(x, y); k1b, k0b, rb, _ = lr(x, y); assert abs(k1 - k1b) < 1e-9 and abs(k0 - k0b) < 1e-9 and abs(rr - rb) < 1e-9
        pts = ', '.join(f'({fg(a,4)}; {fg(b,4)})' for a, b in zip(x, y)); mx, my = sum(x) / len(x), sum(y) / len(y)
        P(B, rng, f'{label} Mẫu: {pts}. Hệ số hồi quy (hệ số góc) k₁ = s_xy/s_x² là', k1, f'x̄ = {f(mx,4)}, ȳ = {f(my,4)}; k₁ = Σ(x − x̄)(y − ȳ)/Σ(x − x̄)² = {f(k1,4)}.', lvl, TOP['reg'], src, extra=[rr, 1 / k1 if k1 else 1, k1 * 2], d=4, lo=None)
        P(B, rng, f'{label} Mẫu: {pts}. Hệ số tự do k₀ = ȳ − k₁x̄ của đường hồi quy y = k₀ + k₁x là', k0, f'k₀ = {f(my,4)} − {f(k1,4)}·{f(mx,4)} = {f(k0,4)}.', lvl, TOP['reg'], src, extra=[my, -k0, k0 + k1], d=4, lo=None)
        P(B, rng, f'{label} Mẫu: {pts}. Hệ số tương quan mẫu r = s_xy/(s_x s_y) là', rr, f'r = {f(rr,4)} (|r| ≤ 1; r² = {f(rr*rr,4)} là tỉ lệ phương sai của y được giải thích bởi x).', lvl + 1 if lvl < 3 else 3, TOP['corr'], src, extra=[rr * rr, k1, -rr], d=4, lo=None)
        if xpred is not None:
            yh = k0 + k1 * xpred
            P(B, rng, f'{label} Mẫu: {pts}. Giá trị dự báo của y tại x = {fg(xpred,4)} theo đường hồi quy là', yh, f'y({fg(xpred,4)}) = {f(k0,4)} + {f(k1,4)}·{fg(xpred,4)} = {f(yh,4)}.', lvl, TOP['pred'], src, extra=[my, k1 * xpred, k0 + k1 * (xpred + 1)], d=3, lo=None)
        return k1, k0, rr
    S = 'Lecture Notes '
    # ----- Ví dụ 4.1 -----
    x41 = [4000, 6000, 8000, 10000]; y41 = [2.3, 4.1, 5.7, 6.9]; k1, k0, rr = mine(x41, y41)
    P(B, rng, 'Giảm thể tích da (%) y dưới áp lực x (atm): (4000; 2.3), (6000; 4.1), (8000; 5.7), (10000; 6.9). Hệ số góc k₁ = s_xy/s_x² là (Ví dụ 4.1a)', k1, f's_xy = 15400/3, s_x² = 2·10⁷/3 ⇒ k₁ = 0.00077 = {f(k1,5)}.', 2, TOP['reg'], S + 'Ví dụ 4.1(a)', extra=[0.0077, 0.077, 1.3e-3], d=5)
    P(B, rng, 'Cùng bài (da, x̄ = 7000, ȳ = 4.75, k₁ = 0.00077): thể tích giảm dự báo tại x = 7000 atm là (Ví dụ 4.1a)', k0 + k1 * 7000, 'y(7000) = ȳ = 4.75 (đường hồi quy luôn đi qua (x̄, ȳ)). Phương trình: y = 0.00077x − 0.64.', 2, TOP['pred'], S + 'Ví dụ 4.1(a)', extra=[0.00077 * 7000, 4.74, 5.39], d=2)
    P(B, rng, 'Cùng bài (da): hệ số tương quan mẫu r là (Ví dụ 4.1b)', rr, f's_x = 2581.989, s_y = 1.996 ⇒ r = {f(rr,3)} ≈ 0.996: tương quan thuận rất mạnh.', 2, TOP['corr'], S + 'Ví dụ 4.1(b)', extra=[rr * rr, 0.00077, 0.9], d=3)
    # ----- Bài 4.1–4.10 -----
    reg('Bài 4.1 (số liệu Kreyszig PS 25.9/1):', [0, 2, 4, 6, 8], [1.0, 2.1, 2.9, 3.6, 5.2], S + 'Bài 4.1 / Kreyszig PS 25.9 Prob. 1', 5)
    reg('Bài 4.2 (số liệu Kreyszig PS 25.9/2):', [-2, 1, 3, 5], [3.5, 2.6, 1.3, 0.4], S + 'Bài 4.2 / Kreyszig PS 25.9 Prob. 2', 2)
    reg('Bài 4.3 (Kreyszig PS 25.9/6, mài mòn thép):', [1.1, 3.2, 3.4, 4.5, 5.6], [40, 65, 120, 150, 190], S + 'Bài 4.3 / Kreyszig PS 25.9 Prob. 6', 4)
    reg('Bài 4.4 (vòng quay/phút và công suất động cơ Diesel):', [400, 500, 600, 700, 750], [5800, 10300, 14200, 18800, 21000], S + 'Bài 4.4 / Kreyszig PS 25.9 Prob. 3', 650)
    reg('Bài 4.5 (biến dạng thép và độ cứng Brinell):', [6, 9, 11, 13, 22, 26, 28, 33, 35], [68, 67, 65, 53, 44, 40, 37, 34, 32], S + 'Bài 4.5 / Kreyszig PS 25.9 Prob. 4', 20)
    reg('Bài 4.6 (độ cứng Brinell và sức căng thép):', [200, 300, 400, 500], [110, 150, 190, 280], S + 'Bài 4.6 / Kreyszig PS 25.9 Prob. 5', 350)
    reg('Bài 4.8 (dẫn nhiệt của nước, tìm y tại 66°F):', [32, 50, 100, 150, 212], [0.337, 0.345, 0.365, 0.380, 0.395], S + 'Bài 4.8 / Kreyszig PS 25.9 Prob. 9', 66, 3)
    reg('Bài 4.9 (khoảng cách dừng, tìm y tại 35 mph):', [30, 40, 50, 60], [160, 240, 330, 435], S + 'Bài 4.9 / Kreyszig PS 25.9 Prob. 10', 35)
    reg('Bài 4.10 (độ ẩm không khí và sự nở của gelatin, tìm y tại x = 25%):', [10, 20, 30, 40], [0.8, 1.6, 2.3, 2.8], S + 'Bài 4.10 / Kreyszig PS 25.9', 25)
    reg('Kreyszig PS 25.9/8 (định luật Hooke: lực x, độ giãn y):', [2, 4, 6, 8], [4.1, 7.8, 12.3, 15.8], 'Kreyszig PS 25.9, Prob. 8', 5)
    reg('Bài 4.7 / PS 25.9/7 (định luật Ohm; chú ý giá trị y = 0.0 tại x = 80 là điểm ngoại lai như trong tài liệu):', [40, 40, 80, 80, 110, 110], [5.1, 4.8, 0.0, 10.3, 13.0, 12.7], S + 'Bài 4.7 / Kreyszig PS 25.9 Prob. 7', 100, 3)
    # ----- Đề thi -----
    sets = [('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 1, câu 4', [1.55, 6.55, 11.55, 16.55, 21.55], [13.03, 17.08, 21.03, 25.10, 29.08], 11),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 2, câu 4', [3.55, 8.55, 13.55, 18.55, 23.55], [13.03, 17.08, 21.03, 25.10, 29.08], 12),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 3, câu 4', [4.55, 9.55, 14.55, 19.55, 24.55], [14.03, 18.08, 22.03, 26.10, 30.08], 13),
            ('Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 4, câu 4', [4.85, 9.85, 14.85, 19.85, 24.85], [14.53, 18.58, 22.53, 26.15, 30.58], 15),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 1, câu 4', [1.5, 6.5, 11.5, 16.5, 21.5], [11.03, 15.08, 19.03, 23.10, 27.08], 11),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 2, câu 4', [1.5, 6.5, 11.5, 16.5, 21.5], [13.03, 17.08, 21.03, 25.10, 29.08], 11),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 3, câu 4', [1.5, 6.5, 11.5, 16.5, 21.5], [9.03, 13.08, 17.03, 21.10, 25.08], 11),
            ('Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 4, câu 4', [1.5, 6.5, 11.5, 16.5, 21.5], [12.03, 16.08, 20.03, 24.10, 28.08], 11)]
    for src, x, y, xp in sets:
        k1, k0, rr = reg('Đề thi:', x, y, src, xp, 3)
        if 'HK2' in src and src.endswith('đề số 1, câu 4'): pass
    s24 = [('Đề mẫu 03/2024, đề số 1, câu 4', [1.85, 7.93, 12.55, 18.21, 23.45], [23.03, 27.08, 31.03, 38.12, 30.28]),
           ('Đề mẫu 03/2024, đề số 2, câu 4', [1.85, 7.93, 12.55, 18.21, 23.45], [13.03, 17.08, 31.03, 25.10, 29.08]),
           ('Đề mẫu 03/2024, đề số 3, câu 4', [4.85, 9.93, 16.55, 22.21, 28.45], [13.03, 17.08, 38.92, 25.10, 29.08]),
           ('Đề mẫu 03/2024, đề số 4, câu 4', [3.85, 10.93, 16.55, 23.21, 30.45], [13.03, 17.08, 21.03, 25.10, 29.08])]
    for src, x, y in s24:
        k1, k0, rr = mine(x, y); pts = ', '.join(f'({a}; {b})' for a, b in zip(x, y))
        P(B, rng, f'Mẫu n = 5: {pts}. Hệ số tương quan mẫu r là', rr, f'r = s_xy/(s_x s_y) = {f(rr,4)}.', 3, TOP['corr'], src, extra=[rr * rr, k1, 1 / rr], d=3, lo=None)
        B.mcq(f'Mẫu n = 5: {pts}. Hệ số tương quan mẫu r = {f(rr,3)} cho biết mối quan hệ giữa x và y là', 'Tương quan thuận ' + ('rất mạnh' if rr > 0.9 else 'mạnh vừa' if rr > 0.6 else 'yếu'), ['Tương quan nghịch', 'Không có tương quan', 'Quan hệ hàm số hoàn hảo (r = 1)'] if rr > 0 else ['Tương quan thuận', 'Không có tương quan', 'r = −1'], f'r = {f(rr,3)} > 0 nên thuận; |r| ' + ('> 0.9' if rr > 0.9 else '≈ ' + f(abs(rr), 2)) + '.', 2, TOP['corr'], src)
    for a, b, src in [(9, 2, 'Đáp án đề số 1 thi 22/12/2021, câu 4'), (4, 3, 'Đáp án đề số 2 thi 22/12/2021, câu 4')]:
        x = [1.5, 2.5, 3.5, 4.5, 5 + a]; y = [8.31, 12.29, 16.32, 20.28, 22.3 + 4 * a]
        reg(f'Đề thi (a = {a}):', x, y, src, 3, 3)
    # ----- Ví dụ 4 §25.9 -----
    t = 0.6 * math.sqrt(8) / math.sqrt(1 - 0.36); c = st.t.ppf(0.95, 8)
    P(B, rng, 'Kiểm định H₀: ρ = 0 so với H₁: ρ > 0 từ n = 10 bảng mạch có r = 0.6. Giá trị quan sát t = r√(n − 2)/√(1 − r²) là (Kreyszig §25.9 Example 4)', t, f't = 0.6·√8/√0.64 = {f(t,3)}; t₀.₀₅(8) = {f(c,3)} (sách: 1.86) ⇒ t > c ⇒ bác bỏ H₀: có tương quan dương.', 3, TOP['test'], 'Kreyszig §25.9, Example 4', extra=[0.6, 0.6 * 8, t / 2], d=3)
    # CI hệ số góc: PS 25.9/12 (= bài 2)
    x2 = [-2, 1, 3, 5]; y2 = [3.5, 2.6, 1.3, 0.4]; lg = st.linregress(x2, y2); n2 = 4; sxx = sum((a - sum(x2) / 4) ** 2 for a in x2); resid = sum((b - lg.intercept - lg.slope * a) ** 2 for a, b in zip(x2, y2)); s = math.sqrt(resid / 2); kk = st.t.ppf(0.975, 2) * s / math.sqrt(sxx)
    B.mcq('(Mở rộng) Khoảng tin cậy 95% cho hệ số góc κ₁ ở Bài 4.2 (n = 4) có dạng k₁ ± t₀.₀₂₅(2)·s/√Σ(x − x̄)². Nửa độ rộng k = t·s/√Σ(x − x̄)² xấp xỉ', f(kk, 4), [f(kk * 2, 4), f(kk / 2, 4), f(st.t.ppf(0.975, 4) * s / math.sqrt(sxx), 4)], f'k₁ = {f(lg.slope,4)}; s² = Σ(yᵢ − ŷᵢ)²/(n − 2) = {f(resid/2,4)}; t₀.₀₂₅(2) = 4.303; k = {f(kk,4)} (Kreyszig PS 25.9/12).', 3, TOP['test'], 'Kreyszig PS 25.9, Prob. 12')
    # lý thuyết
    S4 = 'Lecture Notes §4.1–4.2'
    B.mcq('Nguyên lý bình phương tối thiểu chọn đường hồi quy sao cho:', 'Tổng bình phương khoảng cách đứng Σ(yᵢ − k₀ − k₁xᵢ)² nhỏ nhất', ['Tổng khoảng cách đứng Σ|yᵢ − ŷᵢ| nhỏ nhất', 'Đường đi qua điểm đầu và điểm cuối', 'Tổng yᵢ − ŷᵢ lớn nhất'], 'Giải hệ phương trình chuẩn (4.3).', 1, TOP['theory'], S4)
    B.mcq('Hệ số góc k₁ của đường hồi quy mẫu của y theo x là:', 'k₁ = s_xy/s_x², và k₀ = ȳ − k₁x̄', ['k₁ = s_x²/s_xy', 'k₁ = r·s_x/s_y', 'k₁ = s_xy·s_x'], 'Công thức (4.7). Tương đương k₁ = r·s_y/s_x.', 1, TOP['theory'], S4 + ' (4.7)')
    B.mcq('Đường hồi quy mẫu y − ȳ = k₁(x − x̄) luôn đi qua điểm:', '(x̄, ȳ)', ['(0, 0)', '(x₁, y₁)', '(x_max, y_max)'], 'Từ phương trình chuẩn thứ nhất: k₀ = ȳ − k₁x̄.', 1, TOP['theory'], S4)
    B.mcq('Hệ số tương quan mẫu r = s_xy/(s_x s_y) có tính chất nào?', '−1 ≤ r ≤ 1; r = ±1 khi mọi điểm nằm trên một đường thẳng', ['0 ≤ r ≤ 2', 'r luôn dương', 'r bằng k₁'], 'Định lý 4.1.', 1, TOP['theory'], S4 + ' (Định lý 4.1)')
    B.mcq('r ≈ 0 có nghĩa là:', 'Không có quan hệ TUYẾN TÍNH (có thể vẫn có quan hệ phi tuyến)', ['x và y độc lập', 'x và y không có quan hệ nào', 'k₁ = 1'], 'Tương quan đo mức độ tuyến tính; y = x² trên [−1, 1] có r = 0 nhưng phụ thuộc hoàn toàn.', 2, TOP['theory'], S4)
    B.mcq('Với r = −0.9, mối quan hệ giữa x và y là:', 'Tương quan nghịch mạnh (y giảm khi x tăng)', ['Tương quan thuận mạnh', 'Không tương quan', 'Quan hệ nhân quả chắc chắn'], 'r âm: nghịch; |r| gần 1: mạnh. Tương quan không chứng minh nhân quả.', 1, TOP['theory'], S4 + ' (Hình 4.2)')
    B.mcq('Hiệp phương sai lý thuyết và hệ số tương quan lý thuyết của hai BNN X, Y là:', 'σ_XY = E(XY) − E(X)E(Y) và ρ = σ_XY/(σ_X σ_Y)', ['σ_XY = E(X)E(Y) và ρ = σ_XY', 'σ_XY = E(X + Y) và ρ = σ_X σ_Y', 'σ_XY = Var(X)Var(Y)'], 'Công thức (4.9)–(4.10).', 2, TOP['theory'], S4)
    B.essay('Đề HK2 đề 1 câu 4: X = 1.55, 6.55, 11.55, 16.55, 21.55; Y = 13.03, 17.08, 21.03, 25.10, 29.08. Viết phương trình hồi quy và dự báo Y tại X = 11.', f'x̄ = 11.55, ȳ = 21.064; k₁ = {f(mine([1.55,6.55,11.55,16.55,21.55],[13.03,17.08,21.03,25.10,29.08])[0],3)} (đáp án chính thức 0.802); k₀ = {f(mine([1.55,6.55,11.55,16.55,21.55],[13.03,17.08,21.03,25.10,29.08])[1],3)}; y(11) ≈ {f(mine([1.55,6.55,11.55,16.55,21.55],[13.03,17.08,21.03,25.10,29.08])[1]+11*mine([1.55,6.55,11.55,16.55,21.55],[13.03,17.08,21.03,25.10,29.08])[0],3)}.', 2, TOP['reg'], 'Đề cuối kỳ 2022–2023 HK2, đề số 1, câu 4')
    B.essay('Đề mẫu 2024 câu 4: n = 5, X = 1.85, 7.93, 12.55, 18.21, 23.45; Y = 23.03, 27.08, 31.03, 38.12, 30.28. Tính hệ số tương quan mẫu.', f'r = {f(mine(s24[0][1], s24[0][2])[2],4)}.', 2, TOP['corr'], 'Đề mẫu 03/2024, đề số 1, câu 4')
    B.essay('Ví dụ 4.1 (Lecture Notes): giảm thể tích da; tìm đường hồi quy, dự báo tại 7000 atm và hệ số tương quan.', 'x̄ = 7000, ȳ = 4.75; s_x² = 2·10⁷/3, s_xy = 15400/3; k₁ = 0.00077; y = 0.00077x − 0.64; y(7000) = 4.75; r ≈ 0.996.', 2, TOP['reg'], S + 'Ví dụ 4.1')
    B.essay('Bài 4.1–4.3 (Lecture Notes / Kreyszig PS 25.9/1–2, 6): tính r, k₁ và phương trình hồi quy.', 'Bài 4.1 (số liệu Kreyszig): k₁ = ' + f(mine([0,2,4,6,8],[1.0,2.1,2.9,3.6,5.2])[0], 4) + '; Bài 4.2: k₁ = ' + f(mine([-2,1,3,5],[3.5,2.6,1.3,0.4])[0], 4) + '; Bài 4.3: k₁ = ' + f(mine([1.1,3.2,3.4,4.5,5.6],[40,65,120,150,190])[0], 4) + '.', 2, TOP['reg'], S + 'Bài 4.1–4.3')
    B.essay('Kreyszig §25.9 Example 4: kiểm định ρ = 0 với r = 0.6, n = 10.', 't = 0.6√8/√0.64 = 2.12 > t₀.₀₅(8) = 1.86 ⇒ bác bỏ H₀: có tương quan dương.', 3, TOP['test'], 'Kreyszig §25.9 Example 4')
