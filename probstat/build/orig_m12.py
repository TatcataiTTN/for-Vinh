"""Module 12 — Biểu đồ kiểm soát (quality control), kiểm định χ² mức độ phù hợp, kiểm định phi tham số (dấu).
Gốc: Lecture Notes §3.5–3.7 (mục tùy chọn: quy trình §3.6), Kreyszig §25.5 (PS 25.5), §25.7 (Ví dụ 1, PS 25.7), §25.8 (PS 25.8)."""
import math, random
from scipy import stats as st
from qb import f, fg, nd
from qh import pm
TOP = {'qc': 'Biểu đồ kiểm soát trung bình', 'pc': 'Biểu đồ kiểm soát tỷ lệ phế phẩm', 'gof': 'Kiểm định χ² mức độ phù hợp', 'sign': 'Kiểm định dấu (phi tham số)', 'theory': 'Lý thuyết'}
REJ = 'Bác bỏ H₀, chấp nhận H₁'; ACC = 'Chưa đủ cơ sở bác bỏ H₀ (chấp nhận H₀)'
C2 = lambda a, d: st.chi2.ppf(1 - a, d); U = lambda a: st.norm.ppf(1 - a)
def build(B):
    rng = random.Random(1212)
    def P(B_, r_, stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None if v < 0 else 0.0); return pm(B_, r_, stem, v, *a, **k)
    def dec(stem, rej, expl, lvl, topic, src, origin='goc'):
        a, b = (REJ, ACC) if rej else (ACC, REJ)
        B.mcq(stem, a, [b, 'Cần tăng cỡ mẫu rồi mới kết luận được', 'Không kết luận được vì thiếu giá trị p'], expl, lvl, topic, src, origin)
    K = 'Kreyszig PS 25.5, Prob. '
    # ===== Biểu đồ kiểm soát =====
    P(B, rng, 'Máy rót dầu bôi trơn rót theo phân phối chuẩn có trung bình 1 gal, σ = 0.02. Mẫu cỡ n = 4 (mỗi lần). Giới hạn dưới LCL = μ − 3σ/√n của biểu đồ trung bình là (Kreyszig PS 25.5/1–2)', 1 - 3 * 0.02 / 2, 'LCL = 1 − 3·0.02/√4 = 1 − 0.03 = 0.97 gal; UCL = 1.03 gal (mức ý nghĩa ≈ 0.3%).', 1, TOP['qc'], K + '1–2', extra=[1 - 0.02, 1 - 3 * 0.02, 1 - 0.015], d=3)
    P(B, rng, 'Cùng máy rót (μ = 1, σ = 0.02): xác suất một trung bình mẫu rơi ngoài [μ − 3σ/√n; μ + 3σ/√n] khi quy trình tốt (mức ý nghĩa α) là (Kreyszig PS 25.5/2)', 2 * (1 - st.norm.cdf(3)), '2·(1 − Φ(3)) = 2·0.00135 = 0.0027 ≈ 0.3%.', 2, TOP['qc'], K + '2', extra=[0.05, 0.01, 0.0013], d=4)
    B.mcq('Máy rót (σ = 0.02), muốn UCL − LCL = 0.02 mà vẫn dùng 3σ/√n (Kreyszig PS 25.5/3). Cỡ mẫu n cần chọn là', '36', ['9', '4', '16'], 'UCL − LCL = 6σ/√n = 0.02 ⇒ √n = 6·0.02/0.02 = 6 ⇒ n = 36.', 2, TOP['qc'], K + '3')
    B.mcq('Nếu gấp đôi cỡ mẫu n, độ rộng UCL − LCL (3σ) của biểu đồ trung bình thay đổi thế nào? (Kreyszig PS 25.5/4)', 'Giảm đi √2 lần', ['Giảm một nửa', 'Gấp đôi', 'Không đổi'], 'UCL − LCL = 6σ/√n ⇒ n → 2n làm độ rộng chia √2.', 1, TOP['qc'], K + '4')
    B.mcq('Chuyển mức ý nghĩa từ α = 1% sang α = 5% (cùng n) thì UCL − LCL = 2·U_{α/2}σ/√n thay đổi thế nào? (Kreyszig PS 25.5/4)', 'Hẹp lại (từ 2·2.576 xuống 2·1.960)', ['Rộng ra', 'Không đổi', 'Bằng 0'], 'U₀.₀₀₅ = 2.576 > U₀.₀₂₅ = 1.960: α lớn hơn cho giới hạn hẹp hơn nhưng nhiều báo động nhầm hơn.', 2, TOP['qc'], K + '4')
    B.mcq('Muốn UCL − LCL giảm còn một nửa (cùng α) thì cỡ mẫu n phải:', 'Tăng gấp 4', ['Tăng gấp đôi', 'Giảm một nửa', 'Không đổi'], 'Độ rộng ∝ 1/√n ⇒ giảm một nửa cần √n gấp đôi ⇒ n gấp 4 (Kreyszig PS 25.5/5).', 2, TOP['qc'], K + '5')
    LCL6, UCL6 = 5 - 3 * 1.16 / 2, 5 + 3 * 1.16 / 2
    P(B, rng, 'Độ dày gioăng chuẩn μ = 5, σ = 1.16; lấy mẫu cỡ n = 4. Giới hạn kiểm soát trên UCL = μ + 3σ/√n là (Kreyszig PS 25.5/6)', UCL6, f'UCL = 5 + 3·1.16/2 = {f(UCL6,2)}; LCL = {f(LCL6,2)}.', 1, TOP['qc'], K + '6', extra=[5 + 1.16, 5 + 3 * 1.16, LCL6], d=2)
    means = [(5 + 2 + 5 + 6) / 4, (7 + 5 + 4 + 4) / 4, (7 + 3 + 6 + 5) / 4, (4 + 4 + 3 + 6) / 4, (5 + 6 + 4 + 6) / 4, (6 + 4 + 6 + 4) / 4, (5 + 5 + 6 + 4) / 4, (5 + 2 + 5 + 3) / 4, (3 + 4 + 8 + 4) / 4, (3 + 6 + 6 + 8) / 4]
    out = [m for m in means if m < LCL6 or m > UCL6]
    B.mcq('Mười mẫu cỡ 4 (10:00–19:00) có trung bình 4.5; 5.0; 5.25; 4.25; 5.25; 5.0; 5.0; 3.75; 4.75; 5.75, giới hạn [3.26; 6.74]. Có bao nhiêu mẫu ngoài giới hạn kiểm soát? (Kreyszig PS 25.5/6)', str(len(out)), ['1', '2', '3'] if len(out) == 0 else ['0', '1', '2'], f'Mọi trung bình nằm trong [{f(LCL6,2)}; {f(UCL6,2)}] ⇒ quy trình “trong kiểm soát”.', 2, TOP['qc'], K + '6')
    sg9 = 0.02; n9 = 2; L9, U9 = 3.5 - 3 * sg9 / math.sqrt(n9), 3.5 + 3 * sg9 / math.sqrt(n9)
    P(B, rng, 'Tám mẫu cỡ 2 từ lô đinh ốc (chiều dài inch), quần thể chuẩn μ = 3.500, σ² = 0.0004 (σ = 0.02). Giới hạn kiểm soát dưới LCL = μ − 3σ/√n là (Kreyszig PS 25.5/9)', L9, f'LCL = 3.500 − 3·0.02/√2 = {f(L9,4)}; UCL = {f(U9,4)}.', 2, TOP['qc'], K + '9', extra=[3.5 - 0.06, 3.5 - 0.02, 3.5 - 3 * 0.02 / 2], d=4)
    # p-chart
    p0, nn = 0.04, 100; sdp = math.sqrt(p0 * (1 - p0) / nn); UCLp = p0 + 3 * sdp
    P(B, rng, 'Biểu đồ p (tỷ lệ phế phẩm): p = 4%, cỡ mẫu 100. Giới hạn kiểm soát trên UCL = p + 3√(p(1 − p)/n) là (Kreyszig PS 25.5/10)', UCLp, f'√(0.04·0.96/100) = {f(sdp,4)}; UCL = 0.04 + 3·{f(sdp,4)} = {f(UCLp,4)}; LCL = 0.04 − {f(3*sdp,4)} < 0 ⇒ lấy LCL = 0.', 2, TOP['pc'], K + '10', extra=[p0 + sdp, 0.04 + 3 * 0.04, 0.04 * 3], d=4)
    d10 = [1, 4, 5, 4, 9, 7, 0, 5, 6, 13, 0, 2, 1, 12, 8]; ex10 = [x for x in d10 if x / 100 > UCLp]
    B.mcq('15 mẫu cỡ 100 có số phế phẩm 1, 4, 5, 4, 9, 7, 0, 5, 6, 13, 0, 2, 1, 12, 8; UCL = 9.88%. Bao nhiêu mẫu vượt UCL? (Kreyszig PS 25.5/10)', str(len(ex10)), [str(x) for x in range(0, 5) if x != len(ex10)][:3], f'Các mẫu 13 và 12 phế phẩm (13%, 12%) vượt 9.88% ⇒ {len(ex10)} báo động: quy trình có thể mất kiểm soát.', 3, TOP['pc'], K + '10')
    # lý thuyết
    S = 'Kreyszig §25.5'
    B.mcq('Biểu đồ kiểm soát cho trung bình (control chart for mean) dùng các đường nào?', 'Đường giữa μ₀, giới hạn dưới LCL và giới hạn trên UCL', ['Chỉ đường giữa', 'Hai đường σ² và μ', 'Đường hồi quy'], 'Lấy mẫu định kỳ, vẽ x̄ lên biểu đồ; điểm ngoài [LCL; UCL] báo hiệu có nguyên nhân bất thường.', 1, TOP['theory'], S)
    B.mcq('“Quy tắc 3σ” của biểu đồ kiểm soát có nghĩa là:', 'LCL = μ − 3σ/√n, UCL = μ + 3σ/√n, mức ý nghĩa ≈ 0.3%', ['LCL = μ − 3σ², UCL = μ + 3σ²', 'LCL = 0, UCL = 3σ', 'Mức ý nghĩa 3%'], 'P(|Z| > 3) = 0.0027.', 1, TOP['theory'], S)
    B.mcq('Biểu đồ kiểm soát phát hiện “mất kiểm soát” khi:', 'Một trung bình mẫu rơi ngoài [LCL; UCL]', ['Mọi trung bình nằm trong giới hạn', 'Số mẫu bằng 3', 'σ bằng 0'], 'Điểm ngoài giới hạn là bằng chứng quy trình đã thay đổi (bác bỏ H₀: μ = μ₀).', 1, TOP['theory'], S)
    # ===== χ² phù hợp =====
    S7 = 'Kreyszig §25.7 / Lecture Notes §3.6'
    ej = [6.81, 6.54, 9.61, 12.98, 14.46, 14.77, 12.47, 9.44, 6.37, 6.55]; bj = [6, 6, 11, 14, 16, 15, 8, 10, 8, 6]; chi_ex = sum((b - e) ** 2 / e for b, e in zip(bj, ej))
    P(B, rng, 'Mẫu 100 giá trị độ bền, x̄ = 364.7, s = 26.7, chia 10 lớp. Tần số quan sát b_j = 6, 6, 11, 14, 16, 15, 8, 10, 8, 6; tần số lý thuyết chuẩn e_j = 6.81, 6.54, 9.61, 12.98, 14.46, 14.77, 12.47, 9.44, 6.37, 6.55. χ₀² = Σ(b_j − e_j)²/e_j là (Kreyszig Example 1, Bảng 25.10)', chi_ex, f'Các số hạng: 0.096; 0.045; 0.201; 0.080; 0.164; 0.0004; 1.602; 0.033; 0.417; 0.046 ⇒ χ₀² = {f(chi_ex,3)} (sách: 2.688).', 3, TOP['gof'], S7 + ' (Example 1)', extra=[sum(bj) / 10, 14.067, chi_ex * 2], d=3)
    B.mcq('Với K = 10 lớp và hai tham số (μ, σ) được ước lượng, số bậc tự do của χ² trong kiểm định chuẩn là', '7', ['9', '8', '10'], 'K − r − 1 = 10 − 2 − 1 = 7 (Lecture Notes: nếu r tham số chưa biết dùng K − r − 1).', 2, TOP['gof'], S7)
    dec(f'Kiểm định chuẩn ở mức 5%: χ₀² = {f(chi_ex,3)} và χ²₀.₀₅(7) = {f(C2(0.05,7),3)}. Kết luận là', chi_ex > C2(0.05, 7), f'χ₀² ≤ {f(C2(0.05,7),3)} ⇒ ' + ACC + ': dữ liệu phù hợp phân phối chuẩn.', 2, TOP['gof'], S7 + ' (Example 1)')
    def gof(stem, obs, exp, df, al, src, lvl=2):
        chi = sum((o - e) ** 2 / e for o, e in zip(obs, exp)); crit = C2(al, df); rej = chi > crit
        P(B, rng, stem + ' χ₀² = Σ(b_j − e_j)²/e_j là', chi, f'e_j = ' + ', '.join(fg(e, 4) for e in exp) + f'; χ₀² = {f(chi,3)}.', lvl, TOP['gof'], src, extra=[chi / 2, chi * 2, sum(abs(o - e) for o, e in zip(obs, exp))], d=3)
        dec(stem + f' Ở mức {al*100:g}%: χ₀² = {f(chi,3)}, χ²_α({df}) = {f(crit,3)}. Kết luận là', rej, f'χ₀² ' + ('>' if rej else '≤') + f' {f(crit,3)} ⇒ ' + (REJ if rej else ACC) + '.', lvl + 1, TOP['gof'], src)
    K7 = 'Kreyszig PS 25.7, Prob. '
    gof('Tung đồng xu 100 lần được 40 ngửa, 60 sấp; H₀: đồng xu công bằng (Prob. 3).', [40, 60], [50, 50], 1, 0.05, K7 + '3')
    gof('Tung đồng xu 10 lần được 4 ngửa, 6 sấp; H₀: đồng xu công bằng (Prob. 4: cùng tỉ lệ nhưng cỡ mẫu nhỏ).', [4, 6], [5, 5], 1, 0.05, K7 + '4')
    gof('Gieo súc sắc 60 lần được tần số các mặt 1..6: 10, 13, 9, 11, 9, 8; H₀: súc sắc cân đối (Prob. 5).', [10, 13, 9, 11, 9, 8], [10] * 6, 5, 0.05, K7 + '5')
    gof('Gieo súc sắc 180 lần được: 33, 27, 29, 35, 25, 31; H₀: súc sắc cân đối (Prob. 6).', [33, 27, 29, 35, 25, 31], [30] * 6, 5, 0.05, K7 + '6')
    gof('Số xe phục vụ mỗi ngày: 60, 49, 56, 46, 68, 39; H₀: các ngày có cùng xác suất (Prob. 7).', [60, 49, 56, 46, 68, 39], [318 / 6] * 6, 5, 0.05, K7 + '7')
    gof('Thép: 25% thanh gãy dưới tải 5000 lb với quy trình cũ; quy trình mới thử 80 thanh có 27 gãy. H₀: tỉ lệ gãy vẫn 25% (Prob. 2).', [27, 53], [20, 60], 1, 0.05, K7 + '2')
    z8 = (17 - 10) / math.sqrt(400 * 0.025 * 0.975)
    P(B, rng, 'Máy khoan: nhà sản xuất khẳng định chỉ 2.5% mũi khoan bị cùn; mẫu 400 mũi có 17 cùn. H₀: p = 0.025, H₁: p > 0.025. Giá trị quan sát z = (X − np₀)/√(np₀(1 − p₀)) là (Kreyszig PS 25.7/8)', z8, f'np₀ = 10; √(400·0.025·0.975) = 3.122; z = 7/3.122 = {f(z8,3)} > U₀.₀₅ = 1.645 ⇒ bác bỏ H₀.', 3, TOP['gof'], K7 + '8', extra=[-z8, 7, z8 / 2], d=3, lo=None)
    B.mcq('Điều kiện thực hành khi dùng kiểm định χ² mức độ phù hợp là:', 'Mỗi lớp (khoảng) có tần số quan sát/lý thuyết ít nhất 5', ['Cỡ mẫu nhỏ hơn 10', 'Mỗi lớp chỉ có một giá trị', 'Không cần chia lớp'], 'Lecture Notes §3.6 Bước 1: mỗi khoảng chứa ít nhất 5 giá trị mẫu; nếu không thì gộp lớp.', 1, TOP['theory'], S7)
    B.mcq('Thống kê χ₀² trong kiểm định phù hợp là:', 'Σ_j (b_j − e_j)²/e_j với b_j quan sát và e_j = n·p_j lý thuyết', ['Σ(b_j − e_j)', 'Σ b_j·e_j', 'Σ(b_j − e_j)²'], 'Công thức (3.31). Bác bỏ khi χ₀² > c = χ²_α(K − r − 1).', 1, TOP['theory'], S7 + ' (3.31)')
    # ===== Kiểm định dấu =====
    K8 = 'Kreyszig PS 25.8, Prob. '
    p3 = st.binom.sf(6, 8, 0.5)
    P(B, rng, 'Bộ lọc dầu: trong 11 lần thử, A sạch hơn B ở 7 lần, B sạch hơn A ở 1 lần, 3 lần như nhau (bỏ). Kiểm định dấu H₀: P(A hơn) = 0.5 so với H₁: A tốt hơn; xác suất P(X ≥ 7) với X ~ B(8, 0.5) là (Prob. 3)', p3, f'(C(8,7) + C(8,8))/2⁸ = 9/256 = {f(p3,4)} < 0.05 ⇒ bác bỏ H₀: A tốt hơn.', 3, TOP['sign'], K8 + '3', extra=[0.5 ** 8, 7 / 8, 0.1445], d=4)
    p10 = st.binom.sf(7, 9, 0.5)
    P(B, rng, 'Công tắc nhiệt cần đặt 50°C; mẫu 9 giá trị có 8 giá trị dưới 50°C và 1 trên. Kiểm định dấu H₁: đặt quá thấp; P(X ≥ 8) với X ~ B(9, 0.5) là (Prob. 10)', p10, f'(C(9,8) + C(9,9))/2⁹ = 10/512 = {f(p10,4)} < 0.05 ⇒ bác bỏ H₀: công tắc đặt quá thấp.', 3, TOP['sign'], K8 + '10', extra=[1 / 512, 9 / 512, 0.5], d=4)
    dec('Kiểm định dấu cho công tắc nhiệt (8 dưới, 1 trên) ở mức 5% có kết luận:', True, f'p = {f(p10,4)} < 0.05 ⇒ ' + REJ + '.', 3, TOP['sign'], K8 + '10')
    B.mcq('Kiểm định dấu là kiểm định phi tham số vì:', 'Không cần giả thiết dạng phân phối (chuẩn); chỉ đếm dấu +/−', ['Cần phân phối chuẩn', 'Cần biết σ', 'Dùng hồi quy'], 'Chỉ dựa vào số lần X > μ₀ (dấu dương), có phân phối nhị thức B(n, 1/2) khi H₀ đúng.', 1, TOP['theory'], 'Kreyszig §25.8')
    B.mcq('Trong kiểm định dấu, các cặp có hiệu bằng 0 (hòa) được xử lý thế nào?', 'Bỏ đi (n giảm)', ['Tính là dấu dương', 'Tính là dấu âm', 'Tính hai lần'], 'Chỉ các cặp khác nhau mới mang thông tin về hướng.', 1, TOP['theory'], 'Kreyszig §25.8 / PS 25.8 Prob. 3')
    B.mcq('Dưới H₀: median μ̃ = μ̃₀, số giá trị lớn hơn μ̃₀ trong n giá trị (bỏ hòa) có phân phối:', 'Nhị thức B(n, 1/2)', ['Chuẩn N(0, 1)', 'Student t(n − 1)', 'χ²(n)'], 'Mỗi giá trị lớn hơn hoặc nhỏ hơn μ̃₀ với xác suất 1/2.', 2, TOP['theory'], 'Kreyszig §25.8')
    B.essay('Kreyszig Example 1 §25.7: kiểm tra χ² cho dữ liệu độ bền (n = 100, x̄ = 364.7, s = 26.7, 10 lớp).', f'χ₀² = {f(chi_ex,3)}; bậc tự do 10 − 2 − 1 = 7; χ²₀.₀₅(7) = 14.067 ⇒ chấp nhận chuẩn.', 3, TOP['gof'], 'Kreyszig §25.7 Example 1')
    B.essay('Kreyszig PS 25.7/3–6: kiểm tra đồng xu (40/60) và hai súc sắc (60 và 180 lần).', 'Đồng xu 40/60: χ₀² = 4 > 3.841 ⇒ bác bỏ công bằng. 4/6 (n = 10): χ₀² = 0.4 ⇒ chấp nhận. Súc sắc 60 lần: 1.6; 180 lần: 2.3 ⇒ cả hai chấp nhận (χ²₀.₀₅(5) = 11.07).', 2, TOP['gof'], K7 + '3–6')
    B.essay('Kreyszig PS 25.5/1–5: thiết kế biểu đồ kiểm soát cho máy rót (μ = 1, σ = 0.02, n = 4).', 'LCL = 0.97, UCL = 1.03 (3σ). n = 36 để UCL − LCL = 0.02. Gấp đôi n ⇒ độ rộng giảm √2 lần; muốn độ rộng giảm nửa cần n gấp 4.', 2, TOP['qc'], K + '1–5')
    B.essay('Kreyszig PS 25.5/10: biểu đồ p cho 15 mẫu cỡ 100, p = 4%.', f'UCL = 0.04 + 3·0.0196 = {f(UCLp,4)}; LCL = 0. Các mẫu có 13 và 12 phế phẩm vượt UCL (9.88%) ⇒ mất kiểm soát.', 3, TOP['pc'], K + '10')
