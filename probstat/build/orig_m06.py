"""Module 6 — Nhị thức, Poisson, Chuẩn.
Gốc: Lecture Notes §1.10 (Ví dụ 1.29–1.33, Bài 1.32–1.39); Kreyszig PS 24.7 (Prob. 5–15), PS 24.8 (Prob. 1–13); đề cuối kỳ (HK2 2022–2023 câu 1 ×4, đề mẫu 03/2024 câu 1 ×4,
2021–2022 câu 1 ×2); đề giữa kỳ mẫu câu 1, 7; đáp án giữa kỳ HK2 câu 3. Đáp án tính bằng SciPy (chính xác) và so với giá trị tra bảng đã làm tròn."""
import math, random
from math import comb
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'binom': 'Phân phối nhị thức', 'pois': 'Phân phối Poisson', 'normp': 'Chuẩn: tính xác suất', 'normq': 'Chuẩn: tìm giá trị (phân vị)', 'approx': 'Xấp xỉ chuẩn và Poisson', 'theory': 'Lý thuyết và bảng tra'}
Phi = st.norm.cdf; PhiI = st.norm.ppf
def build(B):
    rng = random.Random(606)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', 0.0 if v >= 0 else None)
        return pm(B_, r_, stem, v, *a, **k)
    S = 'Lecture Notes '
    # ============ Nhị thức ============
    p129 = sum(comb(4, x) * (1 / 6) ** x * (5 / 6) ** (4 - x) for x in (2, 3, 4)); assert abs(p129 - 171 / 1296) < 1e-12
    P(B, rng, 'Tung con súc sắc đồng chất 4 lần. Xác suất nhận được ít nhất hai mặt sáu điểm (Ví dụ 1.29) là', p129, 'X ~ B(4, 1/6): P(X ≥ 2) = f(2) + f(3) + f(4) = 150/1296 + 20/1296 + 1/1296 = 171/1296 ≈ 0.1319.', 2, TOP['binom'], S + 'Ví dụ 1.29', extra=[1 - (5 / 6) ** 4, 4 / 6, 0.5], d=4)
    B.mcq('X ~ B(n, p). Kỳ vọng và phương sai là', 'μ = np và σ² = np(1 − p)', ['μ = np và σ² = np', 'μ = n/p và σ² = n(1 − p)', 'μ = p và σ² = p(1 − p)'], 'Công thức (1.35)–(1.36) của giáo trình.', 1, TOP['binom'], S + '§1.10.1')
    B.mcq('Trong thực nghiệm đối xứng p = 1/2 của B(n, 1/2), kỳ vọng và phương sai là', 'μ = n/2 và σ² = n/4', ['μ = n/2 và σ² = n/2', 'μ = n và σ² = n/4', 'μ = 1/2 và σ² = 1/4'], 'np = n/2 và np(1 − p) = n/4.', 1, TOP['binom'], S + '§1.10.1')
    P(B, rng, 'Mỗi lần thi, 4 đồng xu cân đối được tung. Số mặt ngửa X ~ B(4, 1/2) (Bài 1.31). P(X ≥ 1) bằng', 15 / 16, 'P(X ≥ 1) = 1 − P(X = 0) = 1 − 1/16 = 0.9375.', 1, TOP['binom'], S + 'Bài 1.31', extra=[1 / 16, 0.5, 11 / 16], d=4)
    P(B, rng, '5 đồng xu cân đối được tung. X là số mặt ngửa. P(X = 0) (không có mặt ngửa) là (Kreyszig PS 24.7/5)', 1 / 32, 'X ~ B(5, 1/2): P(0) = (1/2)⁵ = 1/32 = 0.03125.', 1, TOP['binom'], 'Kreyszig PS 24.7, Prob. 5', extra=[1 / 5, 0.5, 5 / 32], d=5)
    P(B, rng, '5 đồng xu cân đối được tung. P(đúng 1 mặt ngửa) là (Kreyszig PS 24.7/5)', 5 / 32, 'C(5,1)/32 = 5/32 = 0.15625.', 1, TOP['binom'], 'Kreyszig PS 24.7, Prob. 5', extra=[1 / 32, 10 / 32, 0.2], d=5)
    P(B, rng, '5 đồng xu cân đối được tung. P(ít nhất 1 mặt ngửa) là (Kreyszig PS 24.7/5)', 31 / 32, '1 − P(0) = 1 − 1/32 = 31/32 = 0.96875.', 1, TOP['binom'], 'Kreyszig PS 24.7, Prob. 5', extra=[1 / 32, 0.5, 5 / 32], d=5)
    P(B, rng, '5 đồng xu cân đối được tung. P(không quá 4 mặt ngửa) là (Kreyszig PS 24.7/5)', 31 / 32, 'P(X ≤ 4) = 1 − P(X = 5) = 1 − 1/32 = 31/32.', 2, TOP['binom'], 'Kreyszig PS 24.7, Prob. 5', extra=[1 / 32, 26 / 32, 0.5], d=5)
    P(B, rng, 'Xác suất bóng đèn hỏng trong thử nghiệm 24 giờ là p = 2%. Biển hiệu gồm 15 bóng. Xác suất cả 15 bóng sáng đủ 24 giờ không hỏng cái nào (Kreyszig PS 24.7/10) là', 0.98 ** 15, '(0.98)¹⁵ = 0.7386 (nhị thức B(15, 0.02) tại x = 0).', 2, TOP['binom'], 'Kreyszig PS 24.7, Prob. 10', extra=[1 - 0.98 ** 15, 0.98, 0.02 ** 15], d=4)
    P(B, rng, 'Với p = 2% mỗi bóng hỏng, biển hiệu gồm 100 bóng. Xác suất không bóng nào hỏng (Kreyszig PS 24.7/11) là', 0.98 ** 100, '(0.98)¹⁰⁰ = 0.1326 — nhỏ hơn nhiều so với biển 15 bóng (0.7386).', 2, TOP['binom'], 'Kreyszig PS 24.7, Prob. 11', extra=[0.98, 0.7386, 1 - 0.98 ** 100], d=4)
    p13 = [comb(3, k) * comb(10, 3 - k) / comb(13, 3) for k in range(4)]
    P(B, rng, 'Người đoán ESP phải gọi tên 3 lá bài (không phân biệt thứ tự) rút ngẫu nhiên từ bộ 13 lá. Xác suất đoán đúng đúng 2 lá chỉ do ngẫu nhiên (Kreyszig PS 24.7/13) là', p13[2], f'Siêu bội: C(3,2)C(10,1)/C(13,3) = 30/286 = {f(p13[2],4)}. (P0 = {f(p13[0],4)}, P1 = {f(p13[1],4)}, P3 = {f(p13[3],4)}; tổng = 1.)', 3, TOP['binom'], 'Kreyszig PS 24.7, Prob. 13', extra=[p13[1], p13[0], p13[3]], d=4)
    P(B, rng, 'Trong bài ESP (13 lá, chọn 3 lá), xác suất đoán đúng cả 3 lá chỉ do ngẫu nhiên là', p13[3], '1/C(13,3) = 1/286 ≈ 0.0035.', 2, TOP['binom'], 'Kreyszig PS 24.7, Prob. 13(d)', extra=[1 / 13, p13[2], 1 / 3], d=4)
    # ============ Poisson ============
    B.mcq('X ~ Poisson(μ). Kỳ vọng và phương sai là', 'Cả hai đều bằng μ', ['μ và μ²', 'μ và √μ', 'μ và 1/μ'], 'Phương sai của Poisson bằng μ (1.38).', 1, TOP['pois'], S + '§1.10.2')
    pb = st.binom.cdf(2, 100, 0.01); pp = st.poisson.cdf(2, 1)
    P(B, rng, 'Xác suất sản phẩm lỗi p = 0.01; trong 100 sản phẩm, xấp xỉ Poisson (μ = np = 1) cho xác suất có không quá 2 sản phẩm lỗi (Ví dụ 1.30) là', pp, f'P(X ≤ 2) ≈ (1 + 1 + 1/2)e⁻¹ = 2.5e⁻¹ = {f(pp,4)} ≈ 91.97%. (Nhị thức đúng: {f(pb,4)} ≈ 92.06%.)', 2, TOP['pois'], S + 'Ví dụ 1.30', extra=[pb, math.exp(-1), 2.5 * math.exp(-1) + 0.01], d=4)
    for x in range(0, 6):
        v = st.poisson.pmf(x, 4)
        P(B, rng, f'4% thanh thép lỗi; mỗi bó 100 thanh. Dùng xấp xỉ Poisson (μ = 4), xác suất bó có đúng x = {x} thanh lỗi (Bài 1.32) là', v, f'f({x}) = 4^{x}e⁻⁴/{x}! = {f(v,4)}.', 2, TOP['pois'], S + 'Bài 1.32 / Kreyszig PS 24.7 Prob. 6', extra=[st.binom.pmf(x, 100, 0.04), st.poisson.pmf(x + 1, 4), st.poisson.pmf(max(x - 1, 0), 4) if x else 0.4], d=4)
    P(B, rng, 'Số ô tô qua điểm A trong một phút ~ Poisson, trung bình 5. Xác suất quan sát nhiều nhất 4 xe trong một phút (Bài 1.33 / Kreyszig PS 24.7/7) là', st.poisson.cdf(4, 5), 'P(X ≤ 4) = e⁻⁵(1 + 5 + 12.5 + 20.833 + 26.042) = 0.4405.', 2, TOP['pois'], S + 'Bài 1.33 / Kreyszig PS 24.7 Prob. 7', extra=[st.poisson.pmf(4, 5), st.poisson.cdf(5, 5), 1 - st.poisson.cdf(4, 5) + 0.01], d=4)
    P(B, rng, 'Tổng đài trung bình 300 cuộc gọi/giờ và chỉ xử lý tối đa 10 cuộc/phút. Xác suất quá tải trong một phút (μ = 5) là (Kreyszig PS 24.7/8)', 1 - st.poisson.cdf(10, 5), 'P(X > 10) = 1 − P(X ≤ 10) = 1 − 0.9863 = 0.0137.', 3, TOP['pois'], 'Kreyszig PS 24.7, Prob. 8', extra=[1 - st.poisson.cdf(9, 5), st.poisson.cdf(10, 5), 0.05], d=4)
    P(B, rng, 'Số hạt alpha mỗi giây ~ Poisson, trung bình 0.5. Xác suất quan sát ít nhất hai hạt trong một giây (Rutherford–Geiger, Kreyszig PS 24.7/9) là', 1 - st.poisson.cdf(1, 0.5), 'P(X ≥ 2) = 1 − e^{−0.5}(1 + 0.5) = 1 − 0.9098 = 0.0902.', 2, TOP['pois'], 'Kreyszig PS 24.7, Prob. 9', extra=[st.poisson.cdf(1, 0.5), st.poisson.pmf(2, 0.5), 0.25], d=4)
    P(B, rng, 'Băng từ trung bình 2 lỗi/100 m. Cuộn dài 300 m (μ = 6). Xác suất không có lỗi nào là (Kreyszig PS 24.7/12b)', math.exp(-6), 'P(X = 0) = e⁻⁶ ≈ 0.002479.', 2, TOP['pois'], 'Kreyszig PS 24.7, Prob. 12(b)', extra=[math.exp(-2), 6 * math.exp(-6), math.exp(-3)], d=6)
    P(B, rng, 'Văn phòng bán vé phục vụ tối đa 4 khách/phút; trung bình 150 khách/giờ (μ = 2.5/phút). Xác suất một phút có khách phải chờ (X > 4) là (Kreyszig PS 24.7/14)', 1 - st.poisson.cdf(4, 2.5), 'P(X > 4) = 1 − P(X ≤ 4) = 1 − 0.8912 = 0.1088.', 3, TOP['pois'], 'Kreyszig PS 24.7, Prob. 14', extra=[st.poisson.cdf(4, 2.5), 1 - st.poisson.cdf(3, 2.5), 0.05], d=4)
    P(B, rng, 'Điện trở bán theo lô 200 với cam kết không có điện trở hỏng; xác suất mỗi điện trở hỏng là 0.1%. Dùng Poisson (μ = 0.2), xác suất lô vi phạm cam kết (X ≥ 1) là (Kreyszig PS 24.7/15)', 1 - math.exp(-0.2), '1 − e^{−0.2} = 0.1813 (nhị thức đúng: 1 − 0.999²⁰⁰ = 0.1814).', 2, TOP['pois'], 'Kreyszig PS 24.7, Prob. 15', extra=[math.exp(-0.2), 0.001 * 200, 0.2], d=4)
    # ============ Chuẩn: tính xác suất ============
    B.mcq('Với X ~ N(μ, σ²), công thức nào đúng?', 'P(a < X ≤ b) = Φ((b − μ)/σ) − Φ((a − μ)/σ)', ['P(a < X ≤ b) = Φ(b − a)', 'P(a < X ≤ b) = Φ(b) − Φ(a)', 'P(a < X ≤ b) = Φ((b − a)/σ)'], 'Chuẩn hóa Z = (X − μ)/σ (Định lý 1.10–1.11).', 1, TOP['theory'], S + 'Định lý 1.11')
    B.mcq('Tính chất nào của hàm Φ đúng với mọi z?', 'Φ(−z) = 1 − Φ(z)', ['Φ(−z) = −Φ(z)', 'Φ(−z) = Φ(z)', 'Φ(−z) = 1 + Φ(z)'], 'Mật độ chuẩn tắc đối xứng qua 0 nên Φ(−z) = 1 − Φ(z).', 1, TOP['theory'], S + '§1.10.3')
    ex = [('Bài 1.34(i)', 'X ~ N(10, 4) (σ = 2): P(X < 10)', Phi(0), 'z = 0 ⇒ Φ(0) = 0.5.'), ('Bài 1.34(ii)', 'X ~ N(10, 4): P(X > 12)', 1 - Phi(1), 'z = (12 − 10)/2 = 1 ⇒ 1 − Φ(1) = 0.1587.'), ('Bài 1.34(iii)', 'X ~ N(10, 4): P(9 < X < 13)', Phi(1.5) - Phi(-0.5), 'Φ(1.5) − Φ(−0.5) = 0.9332 − 0.3085 = 0.6247.')]
    for src, stem, v, e in ex:
        P(B, rng, stem + ' là', v, e, 1 if 'ii)' not in src and 'iii' not in src else 2, TOP['normp'], S + src + ' / Kreyszig PS 24.8 Prob. 1', extra=[1 - v, 0.5, v / 2, 2 * v], d=4)
    for src, mu, sg, a_, b_, desc in [('Bài 1.37 (chi phí bảo trì)', 12000, 2000, 15000, None, 'chi phí bảo trì > $15 000'), ('Bài 1.39(a)', 150, 5, 148, 152, 'điện trở từ 148 Ω đến 152 Ω'), ('Bài 1.39(b)', 150, 5, 140, 160, 'điện trở từ 140 Ω đến 160 Ω')]:
        v = (1 - Phi((a_ - mu) / sg)) if b_ is None else Phi((b_ - mu) / sg) - Phi((a_ - mu) / sg)
        P(B, rng, f'X ~ N({mu}, {sg}²). Xác suất {desc} là', v, f'Chuẩn hóa: ' + (f'z = ({a_} − {mu})/{sg} = {(a_-mu)/sg:g} ⇒ P = 1 − Φ({(a_-mu)/sg:g}) = {f(v,4)}.' if b_ is None else f'Φ(({b_} − {mu})/{sg}) − Φ(({a_} − {mu})/{sg}) = Φ({(b_-mu)/sg:g}) − Φ({(a_-mu)/sg:g}) = {f(v,4)}.'), 2, TOP['normp'], S + src, extra=[1 - v, v / 2, 0.5], d=4)
    p138 = Phi(1) - Phi(-1)
    P(B, rng, 'Điện trở dây loại B ~ N(0.01; 0.001²) Ω. Trong 1000 dây, trung bình bao nhiêu dây có điện trở trong [0.009; 0.011] Ω? (Bài 1.38 / Kreyszig PS 24.8/13)', p138 * 1000, f'P(|X − μ| ≤ σ) = 2Φ(1) − 1 = {f(p138,4)} ⇒ 1000·{f(p138,4)} ≈ {round(p138*1000)} dây.', 2, TOP['normp'], S + 'Bài 1.38 / Kreyszig PS 24.8 Prob. 13', extra=[950, 997, 500, 840], d=0)
    p132 = 2 * Phi(2.5) - 1
    P(B, rng, 'Đường kính thanh sắt ~ N(2; 0.008²) in, dung sai 2 ± 0.02 in. Xác suất thanh đạt (không phế phẩm) là (Ví dụ 1.32a)', p132, f'Φ((2.02 − 2)/0.008) − Φ((1.98 − 2)/0.008) = Φ(2.5) − Φ(−2.5) = {f(p132,4)} ⇒ phế phẩm {f(1-p132,4)} ≈ 1.25% (giáo trình ghi 1¼%).', 2, TOP['normp'], S + 'Ví dụ 1.32(a)', extra=[1 - p132, Phi(2.5), 0.5], d=4)
    p134 = 1 - (Phi(0.0) * 0 + 1 - Phi((4 - 4) / 1))  # placeholder not used
    P(B, rng, 'Tuổi thọ ắc-quy ~ N(4 năm; 1²). Nhà sản xuất bảo đảm không dưới 4 năm: tỉ lệ ắc-quy phải thay thế (tuổi thọ < 4) là (Bài 1.36)', 0.5, 'P(X < 4) = Φ(0) = 0.5 = 50%. Tuổi thọ bảo đảm trùng với trung bình nên nửa số pin không đạt.', 1, TOP['normp'], S + 'Bài 1.36', extra=[0.1587, 0.25, 0.9], d=2)
    p5 = Phi((4 - 5) / 1)
    P(B, rng, 'Ắc-quy ~ N(5 năm; 1²), bảo đảm 4 năm. Tỉ lệ phải thay thế là (Kreyszig PS 24.8/5)', p5, f'P(X < 4) = Φ(−1) = {f(p5,4)} ≈ 15.9%.', 2, TOP['normp'], 'Kreyszig PS 24.8, Prob. 5', extra=[1 - p5, 0.5, 0.0228], d=4)
    p5b = Phi((4 - 5) / 0.5)
    P(B, rng, 'Nếu độ lệch chuẩn nhỏ hơn (0.5 năm) với cùng trung bình 5 năm, tỉ lệ phải thay thế (tuổi thọ < 4 năm) là (Kreyszig PS 24.8/6)', p5b, f'Φ(−2) = {f(p5b,4)} ≈ 2.3% nhỏ hơn 15.9%: σ nhỏ làm đuôi mỏng hơn nên giảm tỉ lệ pin dưới bảo hành.', 2, TOP['normp'], 'Kreyszig PS 24.8, Prob. 6', extra=[p5, Phi(-0.5), 0.5], d=4)
    P(B, rng, 'Khối kiểm tra: X ~ N(105, 25) (σ = 5). Tính P(X ≤ 112.5) (Kreyszig PS 24.8/2) là', Phi(1.5), 'z = (112.5 − 105)/5 = 1.5 ⇒ Φ(1.5) = 0.9332.', 1, TOP['normp'], 'Kreyszig PS 24.8, Prob. 2', extra=[1 - Phi(1.5), 0.5, Phi(1)], d=4)
    P(B, rng, 'X ~ N(105, 25). Tính P(X > 100) (Kreyszig PS 24.8/2) là', Phi(1), 'z = (100 − 105)/5 = −1 ⇒ P(X > 100) = 1 − Φ(−1) = Φ(1) = 0.8413.', 1, TOP['normp'], 'Kreyszig PS 24.8, Prob. 2', extra=[1 - Phi(1), 0.5, Phi(0)], d=4)
    P(B, rng, 'X ~ N(105, 25). Tính P(110.5 < X < 111.25) (Kreyszig PS 24.8/2) là', Phi(1.25) - Phi(1.1), 'z từ 1.1 đến 1.25: Φ(1.25) − Φ(1.1) = 0.8944 − 0.8643 = 0.0301.', 2, TOP['normp'], 'Kreyszig PS 24.8, Prob. 2', extra=[0.0301 * 2, 1 - Phi(1.25), 0.05], d=4)
    p9 = Phi((500 - 480) / 100)
    P(B, rng, 'Điểm Toán SAT ~ N(480; 100²). Tỉ lệ sinh viên KHÔNG đạt điểm ≥ 500 (tức X < 500) là (Kreyszig PS 24.8/9)', p9, f'Φ((500 − 480)/100) = Φ(0.2) = {f(p9,4)} ≈ 57.9%.', 2, TOP['normp'], 'Kreyszig PS 24.8, Prob. 9', extra=[1 - p9, 0.2, 0.5], d=4)
    p11 = PhiI(0.8)
    # ============ Chuẩn: phân vị ============
    c1 = PhiI(0.95) * 0.2 + 5
    P(B, rng, 'X ~ N(5; 0.04) (σ = 0.2). Tìm c sao cho P(X ≤ c) = 95% (Ví dụ 1.31a) là', c1, f'(c − 5)/0.2 = z₀.₉₅ = 1.645 ⇒ c = 5 + 0.329 = {f(c1,3)}. (Giáo trình in nhầm 1.654 nhưng kết quả c = 5.329 đúng với 1.645.)', 2, TOP['normq'], S + 'Ví dụ 1.31(a)', extra=[5 + 1.96 * 0.2, 5 + 1.28 * 0.2, 5.2], d=3)
    k1 = PhiI(0.95) * 0.2
    P(B, rng, 'X ~ N(5; 0.04). Tìm k sao cho P(5 − k ≤ X ≤ 5 + k) = 90% (Ví dụ 1.31b) là', k1, f'2Φ(k/0.2) − 1 = 0.9 ⇒ Φ(k/0.2) = 0.95 ⇒ k = 1.645·0.2 = {f(k1,3)}.', 2, TOP['normq'], S + 'Ví dụ 1.31(b)', extra=[PhiI(0.9) * 0.2, 0.2, 1.96 * 0.2], d=3)
    c3 = 5 + PhiI(0.99) * 0.2
    P(B, rng, 'X ~ N(5; 0.04). Tìm c sao cho P(X ≥ c) = 1% (Ví dụ 1.31c) là', c3, f'P(X ≤ c) = 0.99 ⇒ (c − 5)/0.2 = 2.326 ⇒ c = {f(c3,3)}.', 2, TOP['normq'], S + 'Ví dụ 1.31(c)', extra=[5 + 1.645 * 0.2, 5 - 2.326 * 0.2, 5.329], d=3)
    c132 = 0.008 * PhiI(0.98)
    P(B, rng, 'Đường kính ~ N(2; 0.008²) in. Dung sai c (đối xứng quanh 2) để tỉ lệ phế phẩm là 4% (Ví dụ 1.32b) là', c132, f'Φ(c/0.008) = 0.98 ⇒ c/0.008 = 2.054 ⇒ c = {f(c132,4)} in.', 3, TOP['normq'], S + 'Ví dụ 1.32(b)', extra=[0.008 * 1.96, 0.008 * 1.645, 0.02], d=4)
    # Bài 1.35
    P(B, rng, 'X ~ N(50, 9) (σ = 3). Số c với P(X < c) = 5% (Bài 1.35i) là', 50 + 3 * PhiI(0.05), 'z = −1.645 ⇒ c = 50 − 4.935 = 45.065.', 2, TOP['normq'], S + 'Bài 1.35(i) / Kreyszig PS 24.8 Prob. 3', extra=[50 + 4.935, 50 - 3 * 1.96, 45.0], d=3)
    P(B, rng, 'X ~ N(50, 9). Số c với P(X > c) = 1% (Bài 1.35ii) là', 50 + 3 * PhiI(0.99), 'z = 2.326 ⇒ c = 50 + 6.979 = 56.979.', 2, TOP['normq'], S + 'Bài 1.35(ii) / Kreyszig PS 24.8 Prob. 3', extra=[50 - 6.979, 50 + 3 * 1.645, 56.0], d=3)
    P(B, rng, 'X ~ N(50, 9). Số c với P(−c < X − 50 < c) = 50% (Bài 1.35iii) là', 3 * PhiI(0.75), 'Φ(c/3) = 0.75 ⇒ c/3 = 0.6745 ⇒ c = 2.0235.', 3, TOP['normq'], S + 'Bài 1.35(iii)', extra=[3 * 0.5, 0.6745, 3 * 1.0], d=3)
    P(B, rng, 'X ~ N(3.6; 0.01) (σ = 0.1). Số c với P(X ≤ c) = 99.9% (Kreyszig PS 24.8/4) là', 3.6 + 0.1 * PhiI(0.999), 'z = 3.090 ⇒ c = 3.6 + 0.309 = 3.909.', 2, TOP['normq'], 'Kreyszig PS 24.8, Prob. 4', extra=[3.6 + 0.1 * 2.326, 3.6 + 0.1 * 1.645, 3.9], d=3)
    P(B, rng, 'Độ bền X (kg) ~ N(1500; 50²). Tải trọng tối đa để chỉ mong có ≤ 5% khối bị vỡ (P(X < c) = 5%) là (Kreyszig PS 24.8/8)', 1500 + 50 * PhiI(0.05), 'c = 1500 − 1.645·50 = 1417.75 kg.', 2, TOP['normq'], 'Kreyszig PS 24.8, Prob. 8', extra=[1500 + 82.25, 1500 - 50 * 1.96, 1450.0], d=2)
    P(B, rng, 'Thời gian nghỉ ốm X ~ N(1000; 100²) giờ/tháng. Ngân sách t sao cho xác suất vượt t chỉ 20% (Kreyszig PS 24.8/11) là', 1000 + 100 * PhiI(0.8), 'P(X > t) = 0.2 ⇒ z = 0.8416 ⇒ t = 1084.2 giờ.', 2, TOP['normq'], 'Kreyszig PS 24.8, Prob. 11', extra=[1000 + 84.16 * 2, 1000 - 84.16, 1100.0], d=1)
    # ============ Xấp xỉ chuẩn ============
    a_, b_, n_, p_ = 300, 360, 400, 0.8; sg_ = math.sqrt(n_ * p_ * (1 - p_)); mu_ = n_ * p_
    P(B, rng, 'Mỗi cây sống sau thời gian trồng T với p = 0.8; trồng 400 cây. Xác suất sống từ 300 đến 360 cây (xấp xỉ chuẩn có hiệu chỉnh 0.5, Ví dụ 1.33) là', Phi((b_ - mu_ + 0.5) / sg_) - Phi((a_ - mu_ - 0.5) / sg_), f'μ = 320, σ = 8; α = (300 − 320 − 0.5)/8 = −2.5625; β = (360 − 320 + 0.5)/8 = 5.0625 (giáo trình ghi 7.5625). P ≈ Φ(β) − Φ(α) = 1 − 0.0052 = 0.9948.', 3, TOP['approx'], S + 'Ví dụ 1.33', extra=[0.0052, 0.5, 0.95], d=4)
    ex1 = st.binom.cdf(35, 100, 0.5) if False else None
    B.mcq('Điều kiện thường dùng để xấp xỉ B(n, p) bằng chuẩn là:', 'np > 5 và n(1 − p) > 5 (và np(1 − p) khá lớn)', ['n > 5', 'p < 0.05', 'np < 5'], 'Công thức xấp xỉ (1.45): μ = np, σ² = np(1 − p), hiệu chỉnh ±0.5.', 1, TOP['approx'], S + '§1.10.4')
    B.mcq('Xấp xỉ Poisson của B(n, p) tốt khi:', 'p nhỏ, n lớn, μ = np hữu hạn', ['p gần 1/2', 'n nhỏ, p lớn', 'p = 0.5 và n = 10'], 'Poisson là giới hạn của nhị thức khi p → 0, n → ∞ với np → μ.', 1, TOP['approx'], S + '§1.10.2')
    # ============ Đề thi thật ============
    exam = [  # (μ, σ, a_value, p_b, nguồn, ký hiệu)
        (12.5, 0.809, 13.7135, 0.01, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 1, câu 1', 'tuổi thọ muỗi (ngày)', 'không quá', 'không bé hơn'),
        (25.5, 1.809, 28.0326, 0.01, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 2, câu 1', 'chiều cao cây (cm)', 'không quá', 'không bé hơn'),
        (40.5, 2.708, 44.0204, 0.01, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 3, câu 1', 'chiều cao cây (cm)', 'không quá', 'không bé hơn'),
        (15.5, 0.969, 16.6628, 0.01, 'Đề cuối kỳ 2022–2023 HK2 (3TC), đề số 4, câu 1', 'tuổi thọ muỗi (ngày)', 'không quá', 'không bé hơn')]
    for mu, sg, av, pb_, src, qty, w1, w2 in exam:
        z = (av - mu) / sg; assert abs(z - round(z, 2)) < 1e-3
        pa = Phi(z); cq = mu + sg * PhiI(1 - pb_)
        P(B, rng, f'{qty.capitalize()} X ~ N(μ = {mu}; σ = {sg}). Xác suất X {w1} {av} là', pa, f'z = ({av} − {mu})/{sg} = {z:.2f} ⇒ Φ({z:.2f}) = {f(pa,4)} (tra bảng A7).', 1, TOP['normp'], src + '(a)', extra=[1 - pa, Phi(z / 2), Phi(z + 0.5)], d=4)
        P(B, rng, f'{qty.capitalize()} X ~ N(μ = {mu}; σ = {sg}). Tìm c để xác suất X {w2} c là 1% (P(X ≥ c) = 0.01).', cq, f'P(X < c) = 0.99 ⇒ (c − {mu})/{sg} = 2.326 (bảng A8) ⇒ c = {mu} + 2.326·{sg} = {f(cq,3)}.', 2, TOP['normq'], src + '(b)', extra=[mu + sg * 1.645, mu - sg * 2.326, mu + sg * 1.96], d=3)
    for mu, var, a1, b1, src in [(8.3, 0.16, 8.9, 8.78, 'Đề mẫu 03/2024, đề số 1, câu 1'), (9.7, 0.25, 10.4, 10.3, 'Đề mẫu 03/2024, đề số 2, câu 1'), (5.4, 0.64, 6.84, 6.28, 'Đề mẫu 03/2024, đề số 3, câu 1'), (5.2, 0.81, 6.19, 6.55, 'Đề mẫu 03/2024, đề số 4, câu 1')]:
        sg = math.sqrt(var); za = (a1 - mu) / sg; zb = (b1 - mu) / sg; pa = Phi(za); pbv = 1 - Phi(zb)
        P(B, rng, f'X ~ N(μ = {mu}; σ² = {var}). Tính a = P(X ≤ {a1}).', pa, f'σ = {sg:g}; z = ({a1} − {mu})/{sg:g} = {za:.2f} ⇒ a = Φ({za:.2f}) = {f(pa,4)}.', 1, TOP['normp'], src + '(a)', extra=[1 - pa, Phi(za / 2), Phi(za + 0.3)], d=4)
        P(B, rng, f'X ~ N(μ = {mu}; σ² = {var}). Tính b = P(X ≥ {b1}).', pbv, f'z = ({b1} − {mu})/{sg:g} = {zb:.2f} ⇒ b = 1 − Φ({zb:.2f}) = {f(pbv,4)}.', 1, TOP['normp'], src + '(b)', extra=[1 - pbv, Phi(-zb / 2), Phi(zb)], d=4)
    for a, b, src in [(9, 2, 'Đáp án đề số 1, thi 22/12/2021'), (4, 3, 'Đáp án đề số 2, thi 22/12/2021')]:
        mu, sg2 = 7.5, 0.09; sg = 0.3; z = (a + 1) * sg2 / sg; m = Phi(z)
        pk = (50 + 2 * a) / 100; zk = PhiI((1 + pk) / 2); k = zk * sg - b
        P(B, rng, f'X ~ N(7.5; σ² = 0.09), a = {a}. Tìm m = P(X ≤ μ + (a + 1)σ²).', m, f'(X − μ)/σ ≤ (a + 1)σ²/σ = {a+1}·0.3 = {z:.1f} ⇒ m = Φ({z:.1f}) = {f(m,4)}.', 2, TOP['normp'], src + ', Câu 1(a)', extra=[Phi(z / 2), 1 - m, Phi(a + 1)], d=4)
        B.mcq(f'X ~ N(7.5; 0.09), a = {a}, b = {b}. Tìm k từ P(−k − b < X − μ < k + b) = (50 + 2a)% = {int(pk*100)}% (đáp án chính thức).', f(k, 3), [f(zk * sg, 3), f(k + 2 * b, 3), f(-k, 3)],
              f'2Φ((k + b)/σ) − 1 = {pk} ⇒ Φ = {(1+pk)/2:.2f} ⇒ (k + b)/σ = {zk:.3f} ⇒ k = {zk:.3f}·0.3 − {b} = {f(k,3)} (âm: tham số của đề làm k + b nhỏ hơn b; đáp án chính thức vẫn là {f(k,3)}).', 3, TOP['normq'], src + ', Câu 1(b)', 'goc')
    # Đề giữa kỳ mẫu
    B.mcq('Giá trị tới hạn U_α với α = 8% (P(Z > U_α) = 0.08) là (đề giữa kỳ mẫu, câu 1)', f(PhiI(0.92), 3), [f(PhiI(0.98), 3), f(PhiI(0.9), 3), f(PhiI(0.08), 3)], f'Φ(U_α) = 1 − α = 0.92 ⇒ U₀.₀₈ = {f(PhiI(0.92),3)} (bảng A8: 1.405).', 1, TOP['normq'], 'Đề giữa kỳ mẫu LTXSTK, câu 1', 'goc')
    pm7 = Phi((4.29 - 4.13) / 0.13) - Phi((4.0 - 4.13) / 0.13)
    P(B, rng, 'Điểm Toán ~ N(μ = 4.13; σ = 0.13). Xác suất một sinh viên có điểm từ 4.0 đến 4.29 là', pm7, f'z₁ = (4.0 − 4.13)/0.13 = −1.00; z₂ = (4.29 − 4.13)/0.13 = 1.23 ⇒ Φ(1.23) − Φ(−1) = {f(Phi(1.23),4)} − {f(Phi(-1),4)} = {f(pm7,4)} (đúng với z₂ = 1.2308 chưa làm tròn: {f(pm7,4)}).', 2, TOP['normp'], 'Đề giữa kỳ mẫu LTXSTK, câu 7', extra=[Phi(1.23), 1 - pm7, 0.5], d=4)
    # đáp án giữa kỳ HK2 câu 3
    mu3, sg3 = 44.4, 7.12; pp3 = Phi(1) - Phi(0)
    P(B, rng, 'X ~ N(μ = 44.4; σ = 7.12). Tỉ lệ P(44.4 ≤ X ≤ 51.52) là (đáp án giữa kỳ HK2, câu 3.1)', pp3, 'z₁ = 0, z₂ = (51.52 − 44.4)/7.12 = 1 ⇒ Φ(1) − Φ(0) = 0.8413 − 0.5 = 0.3413.', 1, TOP['normp'], 'Đáp án giữa kỳ HK2 2022–2023, câu 3 (a=3, b=2, c=2)', extra=[0.8413, 0.6826, 0.5], d=4)
    p6 = comb(6, 2) * pp3 ** 2 * (1 - pp3) ** 4
    P(B, rng, 'Chọn 6 người; mỗi người thuộc khoảng trên với xác suất p = 0.3413. Xác suất đúng 2 người trong 6 là (đáp án giữa kỳ HK2, câu 3.2)', p6, f'Nhị thức B(6; 0.3413): C(6,2)·0.3413²·(1 − 0.3413)⁴ = 15·0.11649·0.18826 = {f(p6,4)} (đáp án chính thức 0.3289).', 2, TOP['binom'], 'Đáp án giữa kỳ HK2 2022–2023, câu 3 (a=3, b=2, c=2)', extra=[comb(6, 2) * 0.3413 ** 2, 0.3413 ** 2, 15 * 0.3413 * 0.6587], d=4)
    B.essay('Đề HK2 (3TC) câu 1: X ~ N(12.5; 0.809²). (a) P(X ≤ 13.7135). (b) c sao cho P(X ≥ c) = 1%.', f'(a) z = 1.5 ⇒ Φ(1.5) = 0.9332. (b) Φ((c − 12.5)/0.809) = 0.99 ⇒ z = 2.326 ⇒ c = 12.5 + 2.326·0.809 = {f(12.5+2.326*0.809,3)}.', 2, TOP['normq'], 'Đề cuối kỳ 2022–2023 HK2, đề số 1, câu 1')
    B.essay('Đề mẫu 03/2024 câu 1: X ~ N(8.3; 0.16). Tìm a = P(X ≤ 8.9) và b = P(X ≥ 8.78).', f'σ = 0.4. a = Φ(1.5) = 0.9332. z = (8.78 − 8.3)/0.4 = 1.2 ⇒ b = 1 − Φ(1.2) = {f(1-Phi(1.2),4)}.', 2, TOP['normp'], 'Đề mẫu 03/2024, đề số 1, câu 1')
    B.essay('Bài 1.34–1.35 (Lecture Notes): X ~ N(10, 4): P(X < 10), P(X > 12), P(9 < X < 13); X ~ N(50, 9): c với P(X < c) = 5%, P(X > c) = 1%, P(|X − 50| < c) = 50%.', 'P = 0.5; 0.1587; 0.6247. c = 45.065; 56.979; 2.0235.', 2, TOP['normq'], S + 'Bài 1.34–1.35')
    B.essay('Bài 1.38–1.39 (Lecture Notes): điện trở dây N(0.01; 0.001²): số dây trong 1000 có điện trở ∈ [0.009; 0.011]; điện trở N(150; 5²): P(148–152), P(140–160).', f'{round(p138*1000)} dây (±1σ). P(148 < X < 152) = {f(Phi(0.4)-Phi(-0.4),4)}; P(140 < X < 160) = {f(Phi(2)-Phi(-2),4)}.', 2, TOP['normp'], S + 'Bài 1.38–1.39')
    B.essay('Kreyszig PS 24.7/12–15: băng từ (2 lỗi/100 m, cuộn 300 m), 4 khách/phút, lô 200 điện trở với p = 0.1% — tính bằng Poisson.', f'12: μ = 6; P(X = x) = 6ˣe⁻⁶/x!; P(0) = {f(math.exp(-6),6)}. 14: μ = 2.5; P(X > 4) = 0.1088. 15: μ = 0.2; P(X ≥ 1) = {f(1-math.exp(-0.2),4)}.', 3, TOP['pois'], 'Kreyszig PS 24.7, Prob. 12–15')
    B.essay('Ví dụ 1.33 (Lecture Notes): n = 400, p = 0.8; P(300 ≤ X ≤ 360) bằng xấp xỉ chuẩn có hiệu chỉnh.', 'μ = 320, σ = 8. α = (299.5 − 320)/8 = −2.5625, β = (360.5 − 320)/8 = 5.0625 ⇒ P ≈ Φ(β) − Φ(α) ≈ 1 − 0.0052 = 0.9948.', 3, TOP['approx'], S + 'Ví dụ 1.33')
