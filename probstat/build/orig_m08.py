"""Module 8 — Khoảng tin cậy cho kỳ vọng (σ biết/chưa biết), cho tỷ lệ, cỡ mẫu; mở rộng: khoảng tin cậy cho phương sai (Kreyszig §25.3).
Gốc: Lecture Notes §2.3 (Ví dụ 2.5–2.8, Bài 2.2b, 2.5–2.16); Kreyszig PS 25.3 (Prob. 2–11, 13–17, 19–20); đề cuối kỳ (HK2 3TC câu 2 ×4, đề mẫu 03/2024 câu 2 ×4,
HK1 2TC câu 2 ×4, 2021–2022 câu 2 ×2); đề giữa kỳ mẫu câu 9(b),(c); đáp án giữa kỳ HK2 câu 4. Đáp án chính xác bằng SciPy; đề thi ghi thêm giá trị chính thức khi có."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'z': 'Khoảng tin cậy cho μ (σ đã biết)', 't': 'Khoảng tin cậy cho μ (σ chưa biết, Student)', 'p': 'Khoảng tin cậy cho tỷ lệ p', 'n': 'Cỡ mẫu tối thiểu', 'var': 'Khoảng tin cậy cho σ² (mở rộng χ²)', 'theory': 'Lý thuyết và bảng tra'}
U = lambda a: st.norm.ppf(1 - a)
T = lambda a, d: st.t.ppf(1 - a, d)
def gstats(lo, w, ns):
    mids = [lo + w * (i + 0.5) for i in range(len(ns))]; N = sum(ns); m = sum(a * b for a, b in zip(mids, ns)) / N
    v = sum(b * (a - m) ** 2 for a, b in zip(mids, ns)) / (N - 1); return N, m, v
def ci_pair(c, k): return f'({f(c - k, 3)}; {f(c + k, 3)})'
def build(B):
    rng = random.Random(808)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None)
        return pm(B_, r_, stem, v, *a, **k)
    def ci(stem, c, k, expl, lvl, topic, src, wrongk=None, origin='goc'):
        """MCQ khoảng tin cậy: phương án nhiễu là lỗi thường gặp (z thay t, n thay n−1, nhân đôi, khoảng một phía)."""
        ans = ci_pair(c, k); ws = []
        for kk in (wrongk or []):
            p = ci_pair(c, kk)
            if p != ans and p not in ws: ws.append(p)
        for kk in (k * 1.15, k * 0.85, k * 2, k / 2, k * 1.3):
            p = ci_pair(c, kk)
            if p != ans and p not in ws and len(ws) < 6: ws.append(p)
        B.mcq(stem, ans, ws, expl, lvl, topic, src, origin)
    S = 'Lecture Notes '
    # ============ Ví dụ giáo trình ============
    k25 = U(0.025) * 3 / 10
    ci('Chuẩn, σ² = 9, mẫu n = 100 có x̄ = 5. Khoảng tin cậy 95% cho μ (Ví dụ 2.5) là', 5, k25, f'U₀.₀₂₅ = 1.960; k = 1.960·3/√100 = {f(k25,3)} ⇒ [4.412; 5.588].', 1, TOP['z'], S + 'Ví dụ 2.5', wrongk=[1.645 * 0.3, 2.576 * 0.3, 1.96 * 0.9])
    n26 = math.ceil((2 * 1.96 * 3 / 0.4) ** 2)
    B.mcq('Với σ = 3, độ tin cậy 95%, cỡ mẫu nhỏ nhất để khoảng tin cậy có độ dài L = 0.4 (Ví dụ 2.6) là', str(n26), [str(n26 - 100), str(n26 * 2), '216'], f'L = 2·U·σ/√n ⇒ n ≥ (2·1.96·3/0.4)² = {(2*1.96*3/0.4)**2:.1f} ⇒ n = {n26}.', 2, TOP['n'], S + 'Ví dụ 2.6')
    xb7 = sum([144, 147, 146, 142, 144]) / 5; s7 = math.sqrt(sum((x - xb7) ** 2 for x in [144, 147, 146, 142, 144]) / 4); k7 = T(0.005, 4) * s7 / math.sqrt(5)
    ci('Nhiệt độ điểm cháy dầu Diesel (°F): 144, 147, 146, 142, 144, chuẩn. Khoảng tin cậy 99% cho μ (Ví dụ 2.7) là', xb7, k7, f'x̄ = 144.6; s² = 3.8; t₀.₀₀₅(4) = 4.604; k = 4.604·√3.8/√5 = {f(k7,3)}. (Giáo trình: 4.60 ⇒ k = 4.01, [140.59; 148.61].)', 2, TOP['t'], S + 'Ví dụ 2.7', wrongk=[U(0.005) * s7 / math.sqrt(5), T(0.025, 4) * s7 / math.sqrt(5), T(0.005, 5) * s7 / math.sqrt(5)])
    fp = 0.6; kp = U(0.025) * math.sqrt(fp * (1 - fp) / 1600)
    ci('Bầu cử: phỏng vấn 1600 cử tri, 960 người bầu cho A. Khoảng tin cậy 95% cho tỷ lệ p (Ví dụ 2.8) là', fp, kp, f'f = 0.6; k = 1.960·√(0.6·0.4/1600) = {f(kp,4)} ⇒ [0.576; 0.624].', 2, TOP['p'], S + 'Ví dụ 2.8', wrongk=[U(0.05) * math.sqrt(0.24 / 1600), 1.96 * 0.24 / 40, 1.96 * math.sqrt(0.24) / 1600])
    # ============ Bài tập chương 2 ============
    mids = [1010 + 20 * i for i in range(10)]; n2 = [3, 4, 7, 20, 40, 39, 25, 18, 9, 2]; N2 = sum(n2); m2 = sum(a * b for a, b in zip(mids, n2)) / N2; k2 = U(0.025) * 40 / math.sqrt(N2)
    ci('Tuổi thọ bóng đèn (10 lớp, N = 167, x̄ ≈ 1099.0 giờ), σ = 40 giờ. Khoảng tin cậy 95% của tuổi thọ trung bình (Bài 2.2b) là', m2, k2, f'k = 1.96·40/√167 = {f(k2,3)}; x̄ = {f(m2,3)} ⇒ [{f(m2-k2,3)}; {f(m2+k2,3)}].', 2, TOP['z'], S + 'Bài 2.2(b)', wrongk=[T(0.025, 166) * 40 / math.sqrt(N2), 1.96 * 40, 1.645 * 40 / math.sqrt(N2)])
    x25 = [30, 42, 40, 34, 48, 50]; xb25 = sum(x25) / 6; k25b = U(0.025) * 4 / math.sqrt(6)
    ci('Chuẩn, σ = 4.00, mẫu 30, 42, 40, 34, 48, 50. Khoảng tin cậy 95% cho μ (Bài 2.5) là', xb25, k25b, f'x̄ = {f(xb25,3)}; k = 1.96·4/√6 = {f(k25b,3)}.', 1, TOP['z'], S + 'Bài 2.5', wrongk=[T(0.025, 5) * 4 / math.sqrt(6), 1.645 * 4 / math.sqrt(6), 1.96 * 4])
    k26 = U(0.05) * 0.5 / 10
    ci('Chuẩn, σ² = 0.25, n = 100, x̄ = 212.3. Khoảng tin cậy 90% cho μ (Bài 2.6) là', 212.3, k26, f'σ = 0.5; U₀.₀₅ = 1.645; k = 1.645·0.5/10 = {f(k26,4)}.', 1, TOP['z'], S + 'Bài 2.6', wrongk=[1.96 * 0.05, 1.645 * 0.25 / 10, 2.576 * 0.05])
    B.mcq('Cỡ mẫu nhỏ nhất để khoảng tin cậy 95% cho μ của phân phối chuẩn có độ dài không vượt 2σ (Bài 2.7) là', '4', ['16', '2', '1'], 'L = 2·1.96σ/√n ≤ 2σ ⇒ √n ≥ 1.96 ⇒ n ≥ 3.84 ⇒ n = 4.', 2, TOP['n'], S + 'Bài 2.7')
    n28 = math.ceil((2 * U(0.005) * 5 / 2) ** 2)
    B.mcq('σ² = 25, độ tin cậy 99%: cỡ mẫu nhỏ nhất để khoảng tin cậy có độ dài không vượt quá 2.0 (Bài 2.8 / Kreyszig PS 25.3/6) là', str(n28), [str(n28 - 40), str(n28 + 60), '83'], f'(2·2.576·5/2)² = {(2*2.576*5/2)**2:.1f} ⇒ n = {n28} (với 2.5758: {math.ceil((2*U(0.005)*5/2)**2)}).', 2, TOP['n'], S + 'Bài 2.8 / Kreyszig PS 25.3 Prob. 6')
    def tci(xs, g):
        n = len(xs); xb = sum(xs) / n; s = math.sqrt(sum((x - xb) ** 2 for x in xs) / (n - 1)); kk = T((1 - g) / 2, n - 1) * s / math.sqrt(n); return xb, s, kk
    # Bài 2.9
    n9, xb9, s9 = 20, 20.2, 0.2; k9 = T(0.005, 19) * s9 / math.sqrt(n9)
    ci('Đo 20 con ốc vít: x̄ = 20.2 cm, s² = 0.04 cm², chuẩn. Khoảng tin cậy 99% cho chiều dài trung bình (Bài 2.9 / Kreyszig PS 25.3/13 bối cảnh) là', xb9, k9, f't₀.₀₀₅(19) = 2.861; k = 2.861·0.2/√20 = {f(k9,4)}.', 2, TOP['t'], S + 'Bài 2.9', wrongk=[U(0.005) * 0.2 / math.sqrt(20), T(0.025, 19) * 0.2 / math.sqrt(20), 2.861 * 0.04 / math.sqrt(20)])
    for nm, xs, src in [('độ cứng Knoop (N/m²) 9500, 9800, 9750, 9200, 9400, 9550', [9500, 9800, 9750, 9200, 9400, 9550], 'Bài 2.10 / Kreyszig PS 25.3 Prob. 11'), ('nhiệt độ nóng chảy nhôm (°C) 660, 667, 654, 663, 662', [660, 667, 654, 663, 662], 'Bài 2.11 / Kreyszig PS 25.3 Prob. 10'),
                        ('lượng CO (g/mile) 17.3, 17.7, 18.0, 17.7, 18.2, 17.4, 17.6, 18.1', [17.3, 17.7, 18.0, 17.7, 18.2, 17.4, 17.6, 18.1], 'Bài 2.12 / Kreyszig PS 25.3 Prob. 14')]:
        xb, s, kk = tci(xs, 0.99); n = len(xs)
        ci(f'Mẫu {nm}, chuẩn. Khoảng tin cậy 99% cho trung bình là', xb, kk, f'n = {n}; x̄ = {f(xb,4)}; s = {f(s,4)}; t₀.₀₀₅({n-1}) = {f(T(0.005,n-1),3)}; k = {f(kk,4)}.', 2, TOP['t'], 'Lecture Notes ' + src, wrongk=[U(0.005) * s / math.sqrt(n), T(0.025, n - 1) * s / math.sqrt(n), T(0.005, n) * s / math.sqrt(n)])
    # Bài 2.13: cá trong hồ — ước lượng tỷ lệ có dấu 53/400
    fq = 53 / 400; kq = U(0.025) * math.sqrt(fq * (1 - fq) / 400); N_lo = 2000 / (fq + kq); N_hi = 2000 / (fq - kq)
    ci('Bắt 2000 cá đánh dấu thả lại; bắt lần hai 400 con thấy 53 con có dấu. Khoảng tin cậy 95% cho tỷ lệ cá có dấu p trong hồ (Bài 2.13) là', fq, kq, f'f = 53/400 = {f(fq,4)}; k = 1.96√(f(1−f)/400) = {f(kq,4)}. Số cá N = 2000/p nằm trong [{N_lo:.0f}; {N_hi:.0f}].', 3, TOP['p'], S + 'Bài 2.13', wrongk=[1.96 * math.sqrt(fq * (1 - fq)), 1.645 * math.sqrt(fq * (1 - fq) / 400), 2.576 * math.sqrt(fq * (1 - fq) / 400)])
    B.mcq('Từ khoảng tin cậy 95% của p = tỷ lệ cá có dấu, ước lượng số cá N trong hồ (2000 cá đã đánh dấu) trong khoảng nào? (Bài 2.13)', f'từ {N_lo:.0f} đến {N_hi:.0f} con', [f'từ {N_lo/2:.0f} đến {N_hi/2:.0f} con', f'từ {2000*0.9:.0f} đến {2000*1.1:.0f} con', f'từ {2000/fq*0.5:.0f} đến {2000/fq*0.6:.0f} con'], f'p = 2000/N ⇒ N = 2000/p; cận p lớn ↔ N nhỏ: N ∈ [2000/{f(fq+kq,4)}; 2000/{f(fq-kq,4)}] = [{N_lo:.0f}; {N_hi:.0f}].', 3, TOP['p'], S + 'Bài 2.13')
    f14 = 16 / 400; k14 = U(0.025) * math.sqrt(f14 * (1 - f14) / 400)
    ci('Kiểm tra 400 sản phẩm có 16 phế phẩm. Khoảng tin cậy 95% cho tỷ lệ phế phẩm của lô (Bài 2.14) là', f14, k14, f'f = 0.04; k = 1.96√(0.04·0.96/400) = {f(k14,4)} ⇒ tối thiểu {f(f14-k14,4)}, tối đa {f(f14+k14,4)}.', 2, TOP['p'], S + 'Bài 2.14', wrongk=[1.645 * math.sqrt(0.0384 / 400), 1.96 * math.sqrt(0.0384), 2.576 * math.sqrt(0.0384 / 400)])
    # Bài 2.15, 2.16
    N15, m15, v15 = gstats(19.0, 0.2, [7, 8, 18, 10]); k15a = U(0.025) * 0.02 / math.sqrt(N15); k15b = T(0.005, N15 - 1) * math.sqrt(v15) / math.sqrt(N15)
    ci('Hao phí nhiên liệu (gram) theo lớp 19–19.2: 7; 19.2–19.4: 8; 19.4–19.6: 18; 19.6–19.8: 10 (N = 43), σ = 0.02. Khoảng tin cậy 95% cho trung bình (Bài 2.15a) là', m15, k15a, f'x̄ = {f(m15,4)}; k = 1.96·0.02/√43 = {f(k15a,4)}.', 2, TOP['z'], S + 'Bài 2.15(a)', wrongk=[T(0.025, 42) * 0.02 / math.sqrt(43), 1.645 * 0.02 / math.sqrt(43), 1.96 * math.sqrt(v15) / math.sqrt(43)])
    ci('Cùng bảng hao phí nhiên liệu nhưng không biết σ; khoảng tin cậy 99% cho trung bình (Bài 2.15b) là', m15, k15b, f's = {f(math.sqrt(v15),4)}; t₀.₀₀₅(42) = {f(T(0.005,42),3)}; k = {f(k15b,4)}.', 3, TOP['t'], S + 'Bài 2.15(b)', wrongk=[U(0.005) * math.sqrt(v15) / math.sqrt(43), T(0.025, 42) * math.sqrt(v15) / math.sqrt(43), 2.576 * 0.02 / math.sqrt(43)])
    N16, m16, v16 = gstats(16.5, 0.5, [3, 5, 11, 12, 6, 3]); k16a = T(0.05, N16 - 1) * math.sqrt(v16) / math.sqrt(N16)
    ci('Chiều cao 40 cây con theo lớp 16.5–17: 3; 17–17.5: 5; 17.5–18: 11; 18–18.5: 12; 18.5–19: 6; 19–19.5: 3. Khoảng tin cậy 90% cho trung bình (σ chưa biết, Bài 2.16a) là', m16, k16a, f'x̄ = {f(m16,4)}; s = {f(math.sqrt(v16),4)}; t₀.₀₅(39) = {f(T(0.05,39),3)}; k = {f(k16a,4)}.', 2, TOP['t'], S + 'Bài 2.16(a)', wrongk=[U(0.05) * math.sqrt(v16) / math.sqrt(40), T(0.025, 39) * math.sqrt(v16) / math.sqrt(40), 1.645 * math.sqrt(v16)])
    n16b = math.ceil((2 * U(0.05) * 2.0 / 0.1 / 2) ** 2) if False else math.ceil((U(0.05) * 2.0 / 0.05) ** 2)
    B.mcq('Chiều cao chuẩn với σ = 2.0 cm. Muốn khoảng tin cậy (độ tin cậy 90%, theo ý (a)) có sai số ε = 0.1 (độ dài không quá 2ε hay k ≤ 0.1) thì cần ít nhất bao nhiêu mẫu? (Bài 2.16b)', str(math.ceil((U(0.05) * 2.0 / 0.1) ** 2)), [str(math.ceil((U(0.05) * 2.0 / 0.1) ** 2) // 4), str(math.ceil((U(0.025) * 2.0 / 0.1) ** 2)), '400'], f'k = U₀.₀₅σ/√n ≤ 0.1 ⇒ n ≥ (1.645·2/0.1)² = {(U(0.05)*2/0.1)**2:.1f} ⇒ n = {math.ceil((U(0.05)*2/0.1)**2)}. (Nếu ε = 0.1 là cả độ dài thì k ≤ 0.05: n = {n16b}.)', 3, TOP['n'], S + 'Bài 2.16(b)')
    # ============ Kreyszig PS 25.3 ============
    K = 'Kreyszig PS 25.3, Prob. '
    xs2 = [39, 51, 49, 43, 57, 59]; xb2 = sum(xs2) / 6; k2k = U(0.025) * 4 / math.sqrt(6)
    ci('Mẫu 39, 51, 49, 43, 57, 59 từ quần thể chuẩn có σ = 4.00. Khoảng tin cậy 95% cho μ (Prob. 2) là', xb2, k2k, f'x̄ = {f(xb2,2)}; k = 1.96·4/√6 = {f(k2k,3)}.', 1, TOP['z'], K + '2', wrongk=[T(0.025, 5) * 4 / math.sqrt(6), 1.645 * 4 / math.sqrt(6), 1.96 * 4])
    B.mcq('Với cùng mẫu, nếu tăng độ tin cậy từ 95% lên 99% thì độ dài khoảng thay đổi thế nào (Prob. 2)?', 'Dài hơn khoảng 2.576/1.960 = 1.314 lần', ['Ngắn hơn', 'Không đổi', 'Dài hơn gấp đôi'], 'Độ tin cậy càng cao, giá trị tới hạn càng lớn (2.576 > 1.960) nên khoảng càng rộng.', 1, TOP['theory'], K + '2')
    B.mcq('Nếu gấp đôi cỡ mẫu thì độ dài khoảng tin cậy (σ biết) thay đổi như thế nào? (Prob. 3)', 'Giảm đi √2 lần (nhân với 1/√2 ≈ 0.707)', ['Giảm một nửa', 'Không đổi', 'Giảm 4 lần'], 'L = 2Uσ/√n nên n → 2n làm L → L/√2.', 1, TOP['theory'], K + '3')
    k4 = U(0.025) * 4 / math.sqrt(200)
    ci('Chuẩn, σ² = 16, n = 200, x̄ = 74.81. Khoảng tin cậy 95% cho μ (Prob. 4) là', 74.81, k4, f'k = 1.96·4/√200 = {f(k4,4)} ⇒ [74.256; 75.364].', 1, TOP['z'], K + '4', wrongk=[1.96 * 16 / math.sqrt(200), 1.645 * 4 / math.sqrt(200), 2.576 * 4 / math.sqrt(200)])
    B.mcq('Cỡ mẫu để khoảng tin cậy 95% cho μ có độ dài 2σ là (Prob. 5)', '4', ['16', '8', '2'], '2·1.96σ/√n = 2σ ⇒ √n = 1.96 ⇒ n = 3.84 ⇒ 4; với độ dài σ: n = 15.4 ⇒ 16.', 2, TOP['n'], K + '5')
    B.mcq('Cỡ mẫu để khoảng tin cậy 95% cho μ có độ dài σ (một nửa độ dài ở trên) là (Prob. 5)', '16', ['4', '8', '2'], '2·1.96σ/√n = σ ⇒ √n = 3.92 ⇒ n = 15.37 ⇒ n = 16 (độ dài giảm một nửa cần n gấp 4).', 2, TOP['n'], K + '5')
    f7 = 126 / 800; k7p = U(0.025) * math.sqrt(f7 * (1 - f7) / 800)
    ci('Chọn ngẫu nhiên 800 xe trên đường, có 126 xe bị điều chỉnh phanh kém. Khoảng tin cậy 95% cho tỷ lệ xe phanh kém (Prob. 7) là', f7, k7p, f'f = 126/800 = {f(f7,4)}; k = 1.96√(f(1−f)/800) = {f(k7p,4)}.', 2, TOP['p'], K + '7', wrongk=[1.645 * math.sqrt(f7 * (1 - f7) / 800), 2.576 * math.sqrt(f7 * (1 - f7) / 800), 1.96 * math.sqrt(f7 * (1 - f7))])
    f8 = 12012 / 24000; k8 = U(0.005) * math.sqrt(f8 * (1 - f8) / 24000)
    ci('K. Pearson tung 24 000 lần được 12 012 mặt ngửa. Khoảng tin cậy 99% cho p của đồng xu (Prob. 8) là', f8, k8, f'f = 0.5005; k = 2.576√(f(1−f)/24000) = {f(k8,4)} ⇒ [{f(f8-k8,4)}; {f(f8+k8,4)}] chứa 0.5: đồng xu có thể công bằng.', 3, TOP['p'], K + '8', wrongk=[1.96 * math.sqrt(0.25 / 24000), 2.576 * math.sqrt(0.25), 1.645 * math.sqrt(0.25 / 24000)])
    # bài 9: copper
    cu = [66, 66, 65, 64, 66, 67, 64, 65, 63, 64]; xb, s, kk = tci(cu, 0.99)
    ci('Hàm lượng đồng (%) của đồng thau: 66, 66, 65, 64, 66, 67, 64, 65, 63, 64. Khoảng tin cậy 99% cho trung bình (Prob. 9) là', xb, kk, f'n = 10; x̄ = {f(xb,2)}; s = {f(s,4)}; t₀.₀₀₅(9) = {f(T(0.005,9),3)}; k = {f(kk,4)}.', 2, TOP['t'], K + '9', wrongk=[U(0.005) * s / math.sqrt(10), T(0.025, 9) * s / math.sqrt(10), T(0.005, 10) * s / math.sqrt(10)])
    # bài 13–17 phương sai
    def vci(n, s2, g):
        a = 1 - g; lo = (n - 1) * s2 / st.chi2.ppf(1 - a / 2, n - 1); hi = (n - 1) * s2 / st.chi2.ppf(a / 2, n - 1); return lo, hi
    lo13, hi13 = vci(20, 0.04, 0.95)
    B.mcq('(Mở rộng χ²) 20 bu-lông có s² = 0.04 cm². Khoảng tin cậy 95% cho phương sai σ² (Kreyszig Prob. 13) là', f'({f(lo13,4)}; {f(hi13,4)})', [f'({f(0.04*0.8,4)}; {f(0.04*1.6,4)})', f'({f(19*0.04/st.chi2.ppf(0.95,19),4)}; {f(19*0.04/st.chi2.ppf(0.05,19),4)})', f'({f(lo13*1.3,4)}; {f(hi13*0.8,4)})'], f'[(n−1)s²/χ²₀.₀₂₅(19); (n−1)s²/χ²₀.₉₇₅(19)] = [0.76/{f(st.chi2.ppf(0.975,19),3)}; 0.76/{f(st.chi2.ppf(0.025,19),3)}] = [{f(lo13,4)}; {f(hi13,4)}]. (Hai phía: dùng χ² ở hai đuôi.)', 3, TOP['var'], K + '13')
    xs14 = [17.3, 17.7, 18.0, 17.7, 18.2, 17.4, 17.6, 18.1]; s214 = sum((x - sum(xs14) / 8) ** 2 for x in xs14) / 7; lo14, hi14 = vci(8, s214, 0.95)
    B.mcq('(Mở rộng χ²) Mẫu CO: 17.3, 17.7, 18.0, 17.7, 18.2, 17.4, 17.6, 18.1. Khoảng tin cậy 95% cho σ² (Prob. 14) là', f'({f(lo14,4)}; {f(hi14,4)})', [f'({f(s214*0.7,4)}; {f(s214*1.5,4)})', f'({f(7*s214/st.chi2.ppf(0.95,7),4)}; {f(7*s214/st.chi2.ppf(0.05,7),4)})', f'({f(lo14*1.5,4)}; {f(hi14*0.7,4)})'], f's² = {f(s214,5)}; χ²₀.₀₂₅(7) = {f(st.chi2.ppf(0.975,7),3)}, χ²₀.₉₇₅(7) = {f(st.chi2.ppf(0.025,7),3)} ⇒ [{f(lo14,4)}; {f(hi14,4)}].', 3, TOP['var'], K + '14')
    # 16: tensile strength
    xs16 = [251, 255, 258, 253, 253, 252, 250, 252, 255, 256]; s216 = sum((x - sum(xs16) / 10) ** 2 for x in xs16) / 9; lo16, hi16 = vci(10, s216, 0.95)
    B.mcq('(Mở rộng χ²) Độ bền kéo (ksi): 251, 255, 258, 253, 253, 252, 250, 252, 255, 256. Khoảng tin cậy 95% cho σ² (Prob. 16) là', f'({f(lo16,3)}; {f(hi16,3)})', [f'({f(s216*0.8,3)}; {f(s216*1.9,3)})', f'({f(9*s216/st.chi2.ppf(0.95,9),3)}; {f(9*s216/st.chi2.ppf(0.05,9),3)})', f'({f(lo16*1.4,3)}; {f(hi16*0.7,3)})'], f's² = {f(s216,4)}; χ²₀.₀₂₅(9) = 19.023, χ²₀.₉₇₅(9) = 2.700 ⇒ [{f(lo16,3)}; {f(hi16,3)}].', 3, TOP['var'], K + '16')
    B.mcq('Khoảng tin cậy cho phương sai σ² của quần thể chuẩn dựa trên phân phối nào?', 'Chi-bình phương: (n − 1)s²/σ² ~ χ²(n − 1)', ['Student t(n − 1)', 'Chuẩn tắc N(0,1)', 'Nhị thức'], 'Khoảng hai phía: [(n−1)s²/χ²_{α/2}(n−1); (n−1)s²/χ²_{1−α/2}(n−1)] — nội dung này được xây tiếp ở Module 11.', 2, TOP['var'], K + '13–17')
    # ============ Đề thi thật: σ biết (HK2, 2024) ============
    ks = [('HK2', 1, 70, 15, [2, 4, 7, 8, 4, 2], 16, 0.95, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 1, câu 2', 'tuổi thọ thiết bị (tháng)', (109.243, 121.313)),
          ('HK2', 2, 60, 15, [2, 4, 7, 8, 5, 1], 14, 0.90, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 2, câu 2', 'tuổi thọ thiết bị (tháng)', None),
          ('HK2', 3, 50, 15, [3, 4, 7, 7, 4, 2], 11, 0.95, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 3, câu 2', 'tuổi thọ thiết bị (tháng)', None),
          ('HK2', 4, 40, 15, [3, 5, 8, 7, 3, 2], 10, 0.95, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 4, câu 2', 'tuổi thọ thiết bị (tháng)', None),
          ('24', 1, 401, 20, [2, 4, 7, 8, 4, 2], 36, 0.95, 'Đề mẫu 03/2024, đề số 1, câu 2', 'tuổi thọ chuột (ngày)', None),
          ('24', 2, 405, 20, [2, 5, 8, 7, 4, 2], 40, 0.90, 'Đề mẫu 03/2024, đề số 2, câu 2', 'tuổi thọ gặm nhấm (ngày)', None),
          ('24', 3, 402, 20, [2, 4, 7, 8, 4, 2], 38, 0.95, 'Đề mẫu 03/2024, đề số 3, câu 2', 'tuổi thọ chuột (ngày)', None),
          ('24', 4, 406, 20, [2, 5, 8, 7, 4, 2], 42, 0.90, 'Đề mẫu 03/2024, đề số 4, câu 2', 'tuổi thọ gặm nhấm (ngày)', None)]
    for ty, no, lo_, w, ns_, sg, g, src, nm, official in ks:
        N, m, v = gstats(lo_, w, ns_); z = U((1 - g) / 2); k = z * sg / math.sqrt(N)
        cls = '; '.join(f'{lo_+w*i}–{lo_+w*(i+1)}: {c}' for i, c in enumerate(ns_))
        extra = f' (đáp án chính thức: [{official[0]}; {official[1]}])' if official else ''
        ci(f'{nm.capitalize()} ~ chuẩn, σ = {sg}. Mẫu theo lớp (lớp: số lượng) — {cls}. Khoảng tin cậy {int(g*100)}% cho trung bình là', m, k, f'N = {N}; điểm giữa lớp; x̄ = {f(m,3)}; z = {f(z,3)}; k = z·σ/√N = {f(z,3)}·{sg}/√{N} = {f(k,3)} ⇒ [{f(m-k,3)}; {f(m+k,3)}]{extra}.', 2, TOP['z'], src, wrongk=[T((1 - g) / 2, N - 1) * math.sqrt(v) / math.sqrt(N), z * math.sqrt(v) / math.sqrt(N), z * sg])
    # ============ Đề thi thật: σ chưa biết (2TC, 2021–22) ============
    for no, g, ns_, src in [(1, 0.90, [2, 4, 7, 8, 4, 2], 'Đề cuối kỳ 2022–2023 HK1 (2TC, K16), đề số 1, câu 2'), (2, 0.95, [2, 4, 7, 7, 3, 2], 'Đề cuối kỳ 2022–2023 HK1 (2TC, K16), đề số 2, câu 2'), (3, 0.99, [1, 3, 7, 7, 3, 2], 'Đề cuối kỳ 2022–2023 HK1 (2TC, K16), đề số 3, câu 2'), (4, 0.90, [2, 5, 7, 9, 4, 2], 'Đề cuối kỳ 2022–2023 HK1 (2TC, K16), đề số 4, câu 2')]:
        N, m, v = gstats(51.0, 2.5, ns_); t = T((1 - g) / 2, N - 1); k = t * math.sqrt(v) / math.sqrt(N)
        cls = '; '.join(f'{51+2.5*i:g}–{51+2.5*(i+1):g}: {c}' for i, c in enumerate(ns_))
        ci(f'Cân nặng Y (kg) người 20 tuổi ~ chuẩn. Mẫu theo lớp — {cls}. Khoảng tin cậy {int(g*100)}% cho cân nặng trung bình (σ chưa biết) là', m, k, f'N = {N}; x̄ = {f(m,3)}; s = {f(math.sqrt(v),3)}; t_{{{(1-g)/2:g}}}({N-1}) = {f(t,3)} (bảng A9); k = t·s/√N = {f(k,3)} ⇒ [{f(m-k,3)}; {f(m+k,3)}].', 3, TOP['t'], src, wrongk=[U((1 - g) / 2) * math.sqrt(v) / math.sqrt(N), T((1 - g) / 2, N) * math.sqrt(v) / math.sqrt(N), t * math.sqrt(v)])
    for a, b, src, off in [(9, 2, 'Đáp án đề số 1 thi 22/12/2021, câu 2', (174.315, 175.685)), (4, 3, 'Đáp án đề số 2 thi 22/12/2021, câu 2', (174.271, 175.863))]:
        ns_ = [3, 5, 8 + a, 5 + b, 2]; N, m, v = gstats(171.0, 2.0, ns_); t = T(0.025, N - 1); k = t * math.sqrt(v) / math.sqrt(N)
        cls = '; '.join(f'{170+2*i}–{172+2*i}: {c}' for i, c in enumerate(ns_))
        ci(f'Chiều cao Y (cm) người 18 tuổi ~ chuẩn; a = {a}, b = {b}: {cls}. Khoảng tin cậy 95% cho chiều cao trung bình là', m, k, f'N = {N}; x̄ = {f(m,3)}; s = {f(math.sqrt(v),3)}; t₀.₀₂₅({N-1}) = {f(t,3)}; k = {f(k,3)} ⇒ [{f(m-k,3)}; {f(m+k,3)}] (đáp án chính thức dùng t làm tròn: [{off[0]}; {off[1]}]).', 3, TOP['t'], src, wrongk=[U(0.025) * math.sqrt(v) / math.sqrt(N), T(0.05, N - 1) * math.sqrt(v) / math.sqrt(N), t * math.sqrt(v)])
    # giữa kỳ HK2 câu 4 (tổng hợp)
    n4, ybar, s4 = 22, 173.455, 2.38502; t4 = 1.72; k4t = t4 * s4 / math.sqrt(n4)
    ci('Chiều cao của 22 người: ȳ = 173.455, s = 2.385; độ tin cậy 90.5% (α = 0.095), t_{α/2}(21) = 1.72 (bảng). Khoảng tin cậy là (giữa kỳ HK2, câu 4)', ybar, k4t, f'k = t·s/√n = 1.72·2.385/√22 = {f(k4t,4)} ⇒ [{f(ybar-k4t,3)}; {f(ybar+k4t,3)}] (đáp án chính thức [172.58; 174.329]).', 3, TOP['t'], 'Đáp án giữa kỳ HK2 2022–2023, câu 4 (a=3, b=2, c=2)', wrongk=[1.96 * s4 / math.sqrt(22), t4 * s4, T(0.025, 21) * s4 / math.sqrt(22) * 1.3])
    # giữa kỳ mẫu 9(b), (c)
    N9, m9, v9 = gstats(7, 2, [4, 8, 9, 5]); k9b = U(0.05) * 0.5 / math.sqrt(N9); k9c = T(0.05, N9 - 1) * math.sqrt(v9) / math.sqrt(N9)
    ci('Thời gian điều trị (ngày) theo lớp 6–8: 4; 8–10: 8; 10–12: 9; 12–14: 5, chuẩn, σ = 0.5. Khoảng tin cậy 90% cho trung bình là (giữa kỳ mẫu, 9b)', m9, k9b, f'N = 26; x̄ = {f(m9,4)}; U₀.₀₅ = 1.645; k = 1.645·0.5/√26 = {f(k9b,4)}.', 2, TOP['z'], 'Đề giữa kỳ mẫu LTXSTK, câu 9(b)', wrongk=[T(0.05, 25) * 0.5 / math.sqrt(26), 1.96 * 0.5 / math.sqrt(26), 1.645 * 0.5])
    ci('Cùng mẫu thời gian điều trị (26 bệnh nhân) nhưng σ chưa biết; khoảng tin cậy 90% cho trung bình là (giữa kỳ mẫu, 9c)', m9, k9c, f's = {f(math.sqrt(v9),4)}; t₀.₀₅(25) = {f(T(0.05,25),3)}; k = {f(k9c,4)} ⇒ rộng hơn câu (b) vì σ phải ước lượng.', 3, TOP['t'], 'Đề giữa kỳ mẫu LTXSTK, câu 9(c)', wrongk=[U(0.05) * math.sqrt(v9) / math.sqrt(26), T(0.025, 25) * math.sqrt(v9) / math.sqrt(26), 1.645 * 0.5 / math.sqrt(26)])
    # lý thuyết
    S2 = 'Lecture Notes §2.3'
    B.mcq('Khoảng tin cậy cho μ (σ đã biết) có dạng:', 'x̄ − k ≤ μ ≤ x̄ + k với k = U_{α/2}·σ/√n', ['x̄ ± σ', 'x̄ ± U_α·s', 'x̄ ± t·σ²/n'], 'Công thức (2.7).', 1, TOP['theory'], S2 + ' (2.7)')
    B.mcq('Khoảng tin cậy cho μ (σ chưa biết) có dạng:', 'x̄ − k ≤ μ ≤ x̄ + k với k = t_{α/2}(n − 1)·s/√n', ['x̄ ± U_{α/2}·σ/√n', 'x̄ ± t_{α/2}(n)·s', 'x̄ ± t·s²/√n'], 'Công thức (2.12): dùng phân phối Student với n − 1 bậc tự do.', 1, TOP['theory'], S2 + ' (2.12)')
    B.mcq('Khoảng tin cậy cho xác suất p (n lớn) là:', 'f ± U_{α/2}·√(f(1 − f)/n)', ['f ± U_{α/2}·f/√n', 'f ± t·√n', 'f ± √(f(1 − f))'], 'Công thức (2.16), dựa trên định lý giới hạn trung tâm.', 1, TOP['theory'], S2 + ' (2.16)')
    B.mcq('Giá trị tới hạn U_{α/2} cho độ tin cậy 90%, 95%, 99% lần lượt là:', '1.645; 1.960; 2.576', ['1.282; 1.645; 2.326', '1.960; 2.326; 2.576', '1.645; 1.960; 2.326'], 'Bảng 2.1: α/2 = 5%, 2.5%, 0.5% ⇒ 1.645, 1.960, 2.576.', 1, TOP['theory'], S2 + ' (Bảng 2.1)')
    B.mcq('Độ tin cậy γ = 95% của một khoảng tin cậy có nghĩa là:', 'Nếu lặp lại việc lấy mẫu nhiều lần, khoảng 95% các khoảng dựng được sẽ chứa tham số thật', ['Xác suất μ nằm trong khoảng cụ thể này là 95%', 'Có 95% dữ liệu nằm trong khoảng', 'μ chắc chắn nằm trong khoảng'], 'Tham số là hằng số; tính ngẫu nhiên nằm ở khoảng (qua mẫu). Đây là ý nghĩa tần suất (Mục 2.3).', 2, TOP['theory'], S2)
    B.mcq('Khoảng tin cậy rộng hơn khi:', 'Độ tin cậy cao hơn, σ (hoặc s) lớn hơn, hoặc n nhỏ hơn', ['Độ tin cậy thấp hơn', 'n lớn hơn', 'σ nhỏ hơn'], 'k = U·σ/√n tăng theo U (độ tin cậy) và σ, giảm theo √n.', 1, TOP['theory'], S2)
    B.mcq('Với cùng x̄, s, n và độ tin cậy, khoảng t (σ chưa biết) so với khoảng z (dùng s thay σ) thì:', 'Khoảng t rộng hơn vì t_{α/2}(n − 1) > U_{α/2}', ['Khoảng t hẹp hơn', 'Hai khoảng bằng nhau', 'Không so sánh được'], 'Student có đuôi nặng hơn chuẩn; t → U khi n → ∞.', 2, TOP['theory'], S2)
    B.essay('Đề cuối kỳ HK2 đề 1 câu 2: Y chuẩn σ = 16, mẫu theo lớp (70–85: 2; …; 145–160: 2), độ tin cậy 95%.', f'N = 27; x̄ = {f(gstats(70,15,[2,4,7,8,4,2])[1],3)}; k = 1.96·16/√27 = {f(1.96*16/math.sqrt(27),3)} ⇒ [109.243; 121.313] (khớp đáp án chính thức).', 2, TOP['z'], 'Đề cuối kỳ 2022–2023 HK2, đề số 1, câu 2')
    B.essay('Đề 2TC đề 1 câu 2: cân nặng 51–66 kg theo 6 lớp rộng 2.5 (2; 4; 7; 8; 4; 2); độ tin cậy 90%, σ chưa biết.', f'N = 27; x̄ = {f(gstats(51,2.5,[2,4,7,8,4,2])[1],3)}; s = {f(math.sqrt(gstats(51,2.5,[2,4,7,8,4,2])[2]),3)}; t₀.₀₅(26) = 1.706; k = t·s/√N.', 2, TOP['t'], 'Đề cuối kỳ 2022–2023 HK1 (2TC), đề số 1, câu 2')
    B.essay('Lecture Notes Ví dụ 2.5–2.8: lập khoảng tin cậy khi σ biết (σ² = 9, n = 100, x̄ = 5), cỡ mẫu cho L = 0.4, khoảng t cho dầu Diesel, khoảng cho tỷ lệ bầu cử.', f'2.5: [4.412; 5.588]. 2.6: n = 865. 2.7: [{f(xb7-k7,2)}; {f(xb7+k7,2)}] (giáo trình dùng t = 4.60 ⇒ [140.59; 148.61]). 2.8: [0.576; 0.624].', 2, TOP['z'], S + 'Ví dụ 2.5–2.8')
    B.essay('Bài 2.13–2.14 (Lecture Notes): ước lượng số cá trong hồ (53/400 có dấu, 2000 đã đánh dấu) và tỷ lệ phế phẩm (16/400).', f'2.13: p ∈ [{f(fq-kq,4)}; {f(fq+kq,4)}] ⇒ N ∈ [{N_lo:.0f}; {N_hi:.0f}]. 2.14: p ∈ [{f(f14-k14,4)}; {f(f14+k14,4)}].', 3, TOP['p'], S + 'Bài 2.13–2.14')
    B.essay('Kreyszig PS 25.3/8: Pearson tung 24 000 lần được 12 012 mặt ngửa; khoảng tin cậy 99% cho p; đồng xu có công bằng không?', f'f = 0.5005; k = {f(k8,4)}; p ∈ [{f(f8-k8,4)}; {f(f8+k8,4)}] chứa 0.5 ⇒ không có bằng chứng đồng xu không công bằng.', 2, TOP['p'], K + '8')
    B.essay('Kreyszig PS 25.3/13: khoảng tin cậy 95% cho σ² từ mẫu 20 bu-lông có s² = 0.04 cm².', f'[19·0.04/32.852; 19·0.04/8.907] = [{f(lo13,4)}; {f(hi13,4)}] (χ²₀.₀₂₅(19) = 32.852; χ²₀.₉₇₅(19) = 8.907).', 3, TOP['var'], K + '13')
