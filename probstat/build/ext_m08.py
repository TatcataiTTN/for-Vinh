"""Module 8 — mở rộng: khái niệm + họ bài khoảng tin cậy (đáp án tự tính bằng SciPy)."""
import math, random
from scipy import stats as st
from qb import f, fg
from orig_m08 import TOP, U, T, ci_pair
SRC = 'Bổ sung: dạng bài §2.3 và đề thi (đáp án tự tính bằng SciPy)'
def build(B):
    rng = random.Random(2508)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    def ci(stem, c, k, expl, lvl, topic, wrongk):
        ans = ci_pair(c, k); ws = []
        for kk in list(wrongk) + [k * 1.15, k * 0.85, k * 2, k / 2]:
            p = ci_pair(c, kk)
            if p != ans and p not in ws: ws.append(p)
        B.mcq(stem, ans, ws, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Khoảng tin cậy 95% cho μ có nghĩa là', 'khoảng 95% số khoảng dựng từ các mẫu lặp lại chứa μ', ['μ nằm trong khoảng với xác suất 95%', '95% dữ liệu nằm trong khoảng', 'x̄ nằm trong khoảng với xác suất 95%'], 'Tính ngẫu nhiên nằm ở khoảng, không ở μ.', 2, 'theory')
    C('Tăng độ tin cậy (giữ n) thì khoảng', 'rộng ra', ['hẹp lại', 'không đổi', 'dịch sang phải'], 'Giá trị tới hạn tăng.', 1, 'z')
    C('Tăng cỡ mẫu (giữ độ tin cậy) thì khoảng', 'hẹp lại', ['rộng ra', 'không đổi', 'đổi tâm'], 'Sai số chuẩn giảm theo √n.', 1, 'z')
    C('Dùng phân phối Student thay vì chuẩn khi', 'σ chưa biết, dùng s', ['σ đã biết', 'n rất lớn', 'ước lượng tỷ lệ'], 'Thêm bất định do ước lượng σ.', 1, 't')
    C('Số bậc tự do của t khi ước lượng μ từ mẫu n là', 'n − 1', ['n', 'n − 2', 'n + 1'], 'Mất một bậc tự do khi tính x̄.', 1, 't')
    C('Với cùng độ tin cậy và n nhỏ, t_{α/2}(n−1) so với U_{α/2}', 'lớn hơn', ['nhỏ hơn', 'bằng', 'không so sánh'], 'Đuôi t dày hơn chuẩn.', 1, 't')
    C('Giá trị U_{0.025} xấp xỉ', '1.96', ['1.645', '2.326', '1.28'], 'Khoảng hai phía 95%.', 1, 'z')
    C('Khoảng tin cậy hai phía cho μ (σ biết) là', 'x̄ ± U_{α/2}·σ/√n', ['x̄ ± U_α·σ', 'x̄ ± σ/√n', 'x̄ ± t·σ'], 'Tâm x̄, sai số U σ/√n.', 1, 'z')
    C('Khoảng tin cậy cho tỷ lệ p dùng sai số chuẩn', '√(p̂(1 − p̂)/n)', ['p̂(1 − p̂)/n', '√(p̂/n)', 'p̂/√n'], 'Phương sai nhị thức chia n.', 1, 'p')
    C('Khi chưa biết gì về p, để có cỡ mẫu an toàn ta lấy p(1 − p) bằng', '0.25', ['1', '0.5', '0.1'], 'Cực đại tại p = 0.5.', 2, 'n')
    C('Muốn sai số của khoảng giảm một nửa thì cỡ mẫu phải', 'tăng gấp 4', ['tăng gấp 2', 'giữ nguyên', 'tăng gấp 8'], 'e ∝ 1/√n.', 2, 'n')
    C('Cỡ mẫu tối thiểu tính ra là 96.04 thì chọn', '97', ['96', '96.04', '100 chắc chắn đúng nhất'], 'Làm tròn lên để đảm bảo sai số.', 1, 'n')
    C('Khoảng tin cậy cho σ² dựa trên phân phối', 'χ²', ['chuẩn', 't', 'đều'], '(n−1)S²/σ² ~ χ²(n−1).', 2, 'var')
    # σ biết
    for k in range(12):
        n = rng.choice([16, 25, 36, 49, 64, 100]); sg = rng.choice([2, 3, 4, 5, 8, 10]); xb = rng.choice([20, 35.5, 50, 72.4, 100]); c = rng.choice([0.90, 0.95, 0.99])
        a = 1 - c; z = U(a / 2); e = z * sg / math.sqrt(n)
        ci(f'Mẫu n = {n}, x̄ = {xb}, σ = {sg} (đã biết). Khoảng tin cậy {int(c*100)}% cho μ là', xb, e, f'e = U_{{{fg(a/2,4)}}}·σ/√n = {f(z,3)}·{sg}/{f(math.sqrt(n),2)} = {f(e,3)}.', 2, TOP['z'], [e * U(a) / z, sg * z, z * sg / n])
    # σ chưa biết
    for k in range(12):
        n = rng.choice([8, 10, 12, 16, 20, 25]); s = rng.choice([1.5, 2.2, 3.4, 5, 6.5]); xb = rng.choice([10, 24.6, 48, 80.2]); c = rng.choice([0.90, 0.95, 0.99])
        a = 1 - c; t = T(a / 2, n - 1); e = t * s / math.sqrt(n)
        ci(f'Mẫu n = {n}, x̄ = {xb}, s = {s} (σ chưa biết). Khoảng tin cậy {int(c*100)}% cho μ là', xb, e, f't_{{{fg(a/2,4)}}}({n-1}) = {f(t,3)}; e = {f(t,3)}·{s}/{f(math.sqrt(n),2)} = {f(e,3)}.', 3, TOP['t'], [U(a / 2) * s / math.sqrt(n), t * s, T(a / 2, n) * s / math.sqrt(n)])
    # tỷ lệ
    for k in range(10):
        n = rng.choice([100, 200, 400, 500, 800, 1000]); p = rng.choice([0.3, 0.45, 0.55, 0.62, 0.8]); kk = round(n * p); ph = kk / n; c = rng.choice([0.90, 0.95, 0.99])
        a = 1 - c; z = U(a / 2); e = z * math.sqrt(ph * (1 - ph) / n)
        ci(f'Trong {n} người khảo sát có {kk} người đồng ý. Khoảng tin cậy {int(c*100)}% cho tỷ lệ p là', ph, e, f'p̂ = {f(ph,3)}; e = {f(z,3)}·√({f(ph,3)}·{f(1-ph,3)}/{n}) = {f(e,4)}.', 2, TOP['p'], [z * math.sqrt(ph / n), z * ph * (1 - ph) / n, e * 2])
    # cỡ mẫu
    for sg, e, c in [(10, 2, 0.95), (15, 3, 0.9), (8, 1, 0.99), (20, 4, 0.95), (5, 0.5, 0.95), (12, 2, 0.98), (6, 1.5, 0.9), (25, 5, 0.99)]:
        z = U((1 - c) / 2); nn = (z * sg / e) ** 2
        B.mcq(f'σ ≈ {sg}, sai số tối đa {e}, độ tin cậy {int(c*100)}%. Cỡ mẫu tối thiểu để ước lượng μ là', str(math.ceil(nn)), [str(math.ceil(nn / 2)), str(math.ceil(nn) + 7), str(math.ceil(z * sg / e)), str(math.ceil(nn * 2))],
              f'n ≥ (U·σ/e)² = ({f(z,3)}·{sg}/{e})² = {f(nn,2)} ⇒ {math.ceil(nn)}.', 2, TOP['n'], SRC, 'bo_sung')
    for e, c in [(0.03, 0.95), (0.05, 0.95), (0.02, 0.9), (0.04, 0.99), (0.01, 0.95), (0.05, 0.9)]:
        z = U((1 - c) / 2); nn = z * z * 0.25 / e ** 2
        B.mcq(f'Ước lượng tỷ lệ p (chưa biết p) với sai số tối đa {e} ở độ tin cậy {int(c*100)}%: cỡ mẫu tối thiểu là', str(math.ceil(nn)), [str(math.ceil(nn / 2)), str(math.ceil(nn * 4)), str(math.ceil(nn) - 20), str(math.ceil(nn) + 25)],
              f'n ≥ U²·0.25/e² = {f(z*z,3)}·0.25/{e}² = {f(nn,1)} ⇒ {math.ceil(nn)}.', 3, TOP['n'], SRC, 'bo_sung')
    # độ rộng
    for n, s, c in [(25, 5, 0.95), (36, 6, 0.95), (100, 10, 0.99), (16, 4, 0.9), (49, 7, 0.95), (64, 8, 0.99)]:
        z = U((1 - c) / 2); w = 2 * z * s / math.sqrt(n)
        B.mcq(f'Mẫu n = {n}, σ = {s}. Độ rộng (độ dài) khoảng tin cậy {int(c*100)}% cho μ là', f(w, 3), [f(w / 2, 3), f(w * 2, 3), f(z * s / n, 3), f(2 * s / math.sqrt(n), 3)], f'Độ rộng = 2·U·σ/√n = 2·{f(z,3)}·{s}/{f(math.sqrt(n),2)} = {f(w,3)}.', 2, TOP['z'], SRC, 'bo_sung')
    B.essay('Mẫu n = 25 có x̄ = 48.2, s = 3.5. (a) Khoảng tin cậy 95% cho μ. (b) Cỡ mẫu cần để sai số ≤ 1 (dùng s thay σ).', f'(a) t₀.₀₂₅(24) = {T(0.025,24):.3f}; e = {T(0.025,24)*3.5/5:.3f}; ({48.2-T(0.025,24)*3.5/5:.2f}; {48.2+T(0.025,24)*3.5/5:.2f}). (b) n ≥ (1.96·3.5)² = {(1.96*3.5)**2:.1f} ⇒ 48.', 2, TOP['t'], SRC, 'bo_sung')
    B.essay('Khảo sát 500 cử tri, 285 ủng hộ ứng viên A. Khoảng tin cậy 95% cho tỷ lệ ủng hộ? Có thể kết luận A thắng (p > 0.5) không?', f'p̂ = 0.57; e = 1.96√(0.57·0.43/500) = {1.96*math.sqrt(.57*.43/500):.4f}; khoảng ({.57-1.96*math.sqrt(.57*.43/500):.4f}; {.57+1.96*math.sqrt(.57*.43/500):.4f}). Cận dưới > 0.5 nên có bằng chứng A dẫn trước.', 3, TOP['p'], SRC, 'bo_sung')
    B.essay('Giải thích vì sao khoảng tin cậy dùng t rộng hơn khoảng dùng chuẩn với cùng x̄, s, n, và khi nào hai khoảng gần như bằng nhau.', 'Dùng s thay σ làm tăng bất định nên giá trị tới hạn t > U (đuôi dày hơn). Khi n tăng, t(n − 1) → U nên với n ≥ 30 khoảng gần như trùng.', 2, TOP['t'], SRC, 'bo_sung')
