"""Module 12 — mở rộng: khái niệm + họ bài biểu đồ kiểm soát, χ² phù hợp, kiểm định dấu."""
import math, random
from scipy import stats as st
from qb import f, fg
from qh import pm
from orig_m12 import TOP, REJ, ACC, C2, U
SRC = 'Bổ sung: dạng bài §3.5–3.7 / Kreyszig PS 25.5, 25.7, 25.8 (đáp án tự tính bằng SciPy)'
def build(B):
    rng = random.Random(2512)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Giới hạn kiểm soát trên cho biểu đồ x̄ là', 'μ + 3σ/√n', ['μ + 3σ', 'μ + σ/√n', 'μ + 3σ/n'], 'Độ lệch chuẩn của trung bình mẫu là σ/√n.', 1, 'qc')
    C('Điểm nằm ngoài giới hạn 3σ cho thấy', 'quy trình có thể mất kiểm soát, cần tìm nguyên nhân đặc biệt', ['quy trình chắc chắn tốt', 'dữ liệu sai', 'cần tăng n'], 'Xác suất báo động giả chỉ ≈ 0.27%.', 1, 'qc')
    C('Biến động thông thường (nằm trong giới hạn) do', 'nguyên nhân ngẫu nhiên vốn có', ['lỗi người vận hành', 'máy hỏng', 'nguyên liệu sai'], 'Không cần can thiệp.', 1, 'qc')
    C('Biểu đồ p dùng để theo dõi', 'tỷ lệ phế phẩm', ['trung bình', 'phương sai', 'trung vị'], 'Giới hạn p̄ ± 3√(p̄(1 − p̄)/n).', 1, 'pc')
    C('Giới hạn dưới của biểu đồ p nếu tính ra âm thì lấy', '0', ['giá trị âm đó', '1', 'p̄'], 'Tỷ lệ không thể âm.', 1, 'pc')
    C('Thống kê χ² phù hợp là', 'Σ(O − E)²/E', ['Σ(O − E)/E', 'Σ(O − E)²', 'Σ O²/E'], 'Tổng bình phương chênh lệch chuẩn hóa.', 1, 'gof')
    C('Bậc tự do của χ² phù hợp với k lớp, không ước lượng tham số là', 'k − 1', ['k', 'k − 2', '2k'], 'Tổng các tần số bị ràng buộc.', 1, 'gof')
    C('Kiểm định χ² phù hợp yêu cầu kỳ vọng mỗi ô', 'E ≥ 5 (gộp lớp nếu nhỏ hơn)', ['E ≤ 1', 'E bằng nhau', 'E nguyên'], 'Xấp xỉ χ² cần E đủ lớn.', 2, 'gof')
    C('Miền bác bỏ của χ² phù hợp là', 'χ² > χ²_α(df)', ['χ² < χ²_α', '|χ²| < 1', 'χ² = 0'], 'Chỉ bác bỏ khi chênh lệch lớn (đuôi phải).', 2, 'gof')
    C('Kiểm định dấu là kiểm định', 'phi tham số, chỉ dùng dấu của chênh lệch', ['tham số dùng độ lớn', 'chỉ cho dữ liệu chuẩn', 'tương đương t'], 'Ít giả định nhưng kém mạnh hơn t.', 1, 'sign')
    C('Dưới H₀ trong kiểm định dấu, số dấu dương có phân phối', 'B(n, 0.5)', ['chuẩn tắc', 'Poisson', 'χ²'], 'Mỗi chênh lệch dương/âm đồng khả năng.', 2, 'sign')
    # biểu đồ x̄
    for mu, sg, n in [(50, 2, 4), (100, 6, 9), (12.5, 0.4, 5), (200, 15, 25), (8, 0.3, 6), (75, 5, 10), (30, 3, 16), (500, 20, 8)]:
        se = sg / math.sqrt(n)
        P(f'Quy trình μ = {mu}, σ = {sg}; mẫu con n = {n}. Giới hạn kiểm soát trên UCL (3σ) bằng', mu + 3 * se, f'UCL = μ + 3σ/√n = {mu} + 3·{sg}/{f(math.sqrt(n),3)} = {f(mu+3*se,4)}.', 1, TOP['qc'], SRC, extra=[mu + 3 * sg, mu + 2 * se, mu - 3 * se], d=4, lo=None)
        P(f'Quy trình μ = {mu}, σ = {sg}; mẫu con n = {n}. Giới hạn dưới LCL (3σ) bằng', mu - 3 * se, f'LCL = μ − 3σ/√n = {f(mu-3*se,4)}.', 1, TOP['qc'], SRC, extra=[mu - 3 * sg, mu + 3 * se, mu - se], d=4, lo=None)
    # biểu đồ p
    for pb, n in [(0.05, 100), (0.03, 200), (0.1, 150), (0.02, 500), (0.08, 250), (0.04, 400)]:
        sp = math.sqrt(pb * (1 - pb) / n)
        P(f'Tỷ lệ phế phẩm trung bình p̄ = {pb}, cỡ lô n = {n}. UCL của biểu đồ p (3σ) là', pb + 3 * sp, f'p̄ + 3√(p̄(1 − p̄)/n) = {pb} + 3·{f(sp,4)} = {f(pb+3*sp,4)}.', 2, TOP['pc'], SRC, extra=[pb + 3 * math.sqrt(pb / n), pb + 2 * sp, pb + 3 * pb * (1 - pb) / n], d=4)
    # χ² phù hợp
    for k in range(10):
        nc = rng.choice([4, 5, 6]); tot = rng.choice([120, 150, 200, 240]); w = [rng.randint(1, 4) for _ in range(nc)]
        pr = [1 / nc] * nc; E = [tot / nc] * nc
        obs = [round(e + rng.randint(-8, 8)) for e in E]; obs[-1] += tot - sum(obs)
        chi = sum((o - e) ** 2 / e for o, e in zip(obs, E)); c = C2(0.05, nc - 1); dec = REJ if chi > c else ACC
        if k % 2 == 0:
            P(f'Gieo {tot} lần một vật {nc} mặt; số lần quan sát {obs}. Với giả thiết đồng khả năng, thống kê χ² bằng', chi, f'E = {fg(tot/nc)} mỗi mặt; χ² = Σ(O − E)²/E = {f(chi,3)}.', 2, TOP['gof'], SRC, extra=[chi / (nc - 1), sum(abs(o - e) for o, e in zip(obs, E)), chi * 2], d=3)
        else:
            B.mcq(f'Gieo {tot} lần một vật {nc} mặt; số lần quan sát {obs}. Kiểm định đồng khả năng ở α = 0.05. Kết luận:', dec, [ACC if dec == REJ else REJ, 'Dùng phân phối chuẩn', 'Không kết luận được'], f'χ² = {f(chi,3)}; χ²₀.₀₅({nc-1}) = {f(c,3)} ⇒ {dec}.', 3, TOP['gof'], SRC, 'bo_sung')
    for k_, ne in [(5, 1), (8, 2), (10, 0), (6, 1), (7, 2), (12, 2)]:
        P(f'Kiểm định phân phối với {k_} lớp, ước lượng {ne} tham số từ mẫu. Số bậc tự do của χ² là', k_ - 1 - ne, f'df = số lớp − 1 − số tham số ước lượng = {k_} − 1 − {ne} = {k_-1-ne}.', 2, TOP['gof'], SRC, extra=[k_ - 1, k_, k_ - ne], d=0, lo=0)
    # kiểm định dấu
    for n, kk in [(12, 9), (10, 8), (15, 4), (20, 15), (9, 8), (16, 5)]:
        pv = 2 * min(st.binom.cdf(kk, n, .5), 1 - st.binom.cdf(kk - 1, n, .5))
        P(f'Kiểm định dấu: {n} chênh lệch (không hòa), có {kk} dấu dương. p-value hai phía bằng', min(pv, 1), f'Dưới H₀: X ~ B({n}; 0.5); p = 2·min(P(X ≤ {kk}), P(X ≥ {kk})) = {f(min(pv,1),4)}.', 3, TOP['sign'], SRC, extra=[pv / 2, 1 - pv, st.binom.pmf(kk, n, .5)], d=4)
    B.essay('Máy rót chai có μ = 500 ml, σ = 4. Mẫu con n = 4 mỗi giờ. (a) Giới hạn 3σ? (b) Trung bình các giờ: 499, 502, 505, 508. Có tín hiệu nào?', '(a) σ_X̄ = 2; UCL = 506, LCL = 494. (b) 508 > 506 ⇒ tín hiệu mất kiểm soát ở giờ thứ 4; còn xu hướng tăng liên tục cũng đáng lưu ý.', 2, TOP['qc'], SRC, 'bo_sung')
    B.essay('Một phân phối Poisson được kiểm tra bằng 100 quan sát chia thành 5 lớp (0,1,2,3,≥4), λ ước lượng từ mẫu. Tìm số bậc tự do và nêu quy tắc gộp lớp.', 'df = 5 − 1 − 1 = 3. Gộp các lớp có E < 5 vào lớp kề để thỏa E ≥ 5, rồi tính lại df theo số lớp sau gộp.', 2, TOP['gof'], SRC, 'bo_sung')
    B.essay('Ưu và nhược điểm của kiểm định dấu so với kiểm định t.', 'Ưu: không cần giả thiết chuẩn, chịu được ngoại lai, dùng được dữ liệu thứ bậc. Nhược: bỏ qua độ lớn chênh lệch nên lực kiểm định thấp hơn khi dữ liệu thật sự chuẩn.', 2, TOP['sign'], SRC, 'bo_sung')
