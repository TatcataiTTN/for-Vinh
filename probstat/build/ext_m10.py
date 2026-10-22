"""Module 10 — mở rộng: khái niệm + họ bài kiểm định (đáp án tự tính bằng SciPy)."""
import math, random
from scipy import stats as st
from qb import f, fg
from qh import pm
from orig_m10 import TOP, U, T, REJ, ACC
SRC = 'Bổ sung: dạng bài §3.1–3.2 / Kreyszig PS 25.4 (đáp án tự tính bằng SciPy)'
Phi = st.norm.cdf
def build(B):
    rng = random.Random(2510)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 else None); k.setdefault('lo', None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='hyp'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Giả thuyết không H₀ thường', 'chứa dấu bằng và là trạng thái mặc định', ['chứa điều cần chứng minh', 'luôn là μ ≠ μ₀', 'là đối thuyết'], 'H₁ chứa điều cần chứng minh.')
    C('Sai lầm loại I là', 'bác bỏ H₀ khi H₀ đúng', ['không bác bỏ H₀ khi H₀ sai', 'chấp nhận H₁ khi H₁ đúng', 'tính sai thống kê'], 'Xác suất là α (mức ý nghĩa).')
    C('Sai lầm loại II là', 'không bác bỏ H₀ khi H₀ sai', ['bác bỏ H₀ khi H₀ đúng', 'bác bỏ H₁', 'chọn sai α'], 'Xác suất là β.')
    C('Lực kiểm định bằng', '1 − β', ['1 − α', 'α', 'β'], 'Xác suất bác bỏ H₀ khi H₀ sai.', 2)
    C('Khi giảm mức ý nghĩa α (giữ n) thì', 'β tăng', ['β giảm', 'lực tăng', 'miền bác bỏ rộng ra'], 'Đánh đổi giữa hai loại sai lầm.', 2)
    C('p-value là', 'xác suất (dưới H₀) quan sát thống kê cực đoan bằng hoặc hơn giá trị đã thấy', ['xác suất H₀ đúng', 'xác suất H₁ đúng', 'mức ý nghĩa α'], 'Không phải xác suất của giả thuyết.', 2, 'dec')
    C('Bác bỏ H₀ khi', 'p-value < α', ['p-value > α', 'p-value = 1', 'α < 0.01'], 'So p-value với mức ý nghĩa.', 1, 'dec')
    C('Không bác bỏ H₀ có nghĩa là', 'chưa đủ bằng chứng chống lại H₀', ['đã chứng minh H₀ đúng', 'H₁ sai', 'p-value = 0'], 'Thiếu bằng chứng ≠ chứng minh.', 2, 'dec')
    C('Kiểm định hai phía dùng giá trị tới hạn', 'U_{α/2}', ['U_α', 'U_{2α}', '1 − α'], 'Chia α cho hai đuôi.', 1, 'z')
    C('Kiểm định T một mẫu có số bậc tự do', 'n − 1', ['n', 'n − 2', '2n'], 'Dùng s thay σ.', 1, 't')
    C('Kiểm định tỷ lệ dùng thống kê Z = (p̂ − p₀)/√(p₀(1 − p₀)/n) vì', 'dưới H₀ tỷ lệ thật là p₀', ['p̂ chính xác hơn', 'luôn dùng p̂', 'để Z âm'], 'Sai số chuẩn tính tại H₀.', 2, 'p')
    C('Tăng cỡ mẫu (giữ α) thì lực kiểm định', 'tăng', ['giảm', 'không đổi', 'bằng α'], 'Sai số chuẩn giảm.', 1)
    # Z-test
    for k in range(12):
        mu0 = rng.choice([50, 100, 20, 12.5, 8.3]); sg = rng.choice([2, 4, 6, 10, 15]); n = rng.choice([16, 25, 36, 49, 64]); d = rng.choice([-2, -1, 1, 1.5, 2, 3]) * sg / math.sqrt(n) * rng.choice([1, 1.5]); xb = mu0 + d
        z = (xb - mu0) / (sg / math.sqrt(n)); kind = k % 3
        if kind == 0:
            P(f'H₀: μ = {fg(mu0)}; σ = {sg}. Mẫu n = {n} có x̄ = {fg(xb,4)}. Giá trị thống kê Z là', z, f'Z = (x̄ − μ₀)/(σ/√n) = {fg(xb-mu0,4)}/{f(sg/math.sqrt(n),3)} = {f(z,3)}.', 1, TOP['z'], SRC, extra=[-z, z * math.sqrt(n), (xb - mu0) / sg], d=3)
        elif kind == 1:
            a = rng.choice([0.05, 0.01]); crit = U(a / 2); dec = REJ if abs(z) > crit else ACC
            B.mcq(f'H₀: μ = {fg(mu0)} so với H₁: μ ≠ {fg(mu0)}; σ = {sg}, n = {n}, x̄ = {fg(xb,4)}, α = {a}. Kết luận:', dec, [ACC if dec == REJ else REJ, 'Cần thêm thông tin về s', 'Không kết luận được vì n nhỏ'],
                  f'Z = {f(z,3)}; U_{{{fg(a/2,4)}}} = {f(crit,3)}; |Z| {">" if abs(z)>crit else "≤"} {f(crit,3)} ⇒ {dec}.', 2, TOP['dec'], SRC, 'bo_sung')
        else:
            pv = 2 * (1 - Phi(abs(z)))
            P(f'H₀: μ = {fg(mu0)} so với H₁: μ ≠ {fg(mu0)}; σ = {sg}, n = {n}, x̄ = {fg(xb,4)}. p-value (hai phía) bằng', pv, f'Z = {f(z,3)}; p = 2(1 − Φ(|Z|)) = {f(pv,4)}.', 3, TOP['dec'], SRC, extra=[pv / 2, 1 - pv, Phi(z)], d=4)
    # một phía
    for k in range(8):
        mu0 = rng.choice([100, 40, 25]); sg = rng.choice([5, 8, 12]); n = rng.choice([25, 36, 64]); xb = mu0 + rng.choice([-1, 1]) * rng.choice([1.2, 1.8, 2.5]) * sg / math.sqrt(n)
        z = (xb - mu0) / (sg / math.sqrt(n)); right = z > 0; crit = U(0.05)
        H1 = f'μ > {mu0}' if right else f'μ < {mu0}'
        rej = (z > crit) if right else (z < -crit)
        B.mcq(f'H₀: μ = {mu0} so với H₁: {H1}; σ = {sg}, n = {n}, x̄ = {fg(xb,4)}, α = 0.05. Kết luận:', REJ if rej else ACC, [ACC if rej else REJ, 'Cần dùng phân phối t', 'Không đủ dữ kiện'],
              f'Z = {f(z,3)}; ngưỡng {"+" if right else "−"}{f(crit,3)} ⇒ {REJ if rej else ACC}.', 2, TOP['dec'], SRC, 'bo_sung')
    # T
    for k in range(10):
        mu0 = rng.choice([20, 50, 8]); n = rng.choice([9, 12, 16, 20, 25]); s = rng.choice([1.5, 2.5, 4]); xb = mu0 + rng.choice([-1.4, -0.8, 0.8, 1.4, 2]) * s / math.sqrt(n) * rng.choice([1, 2])
        t = (xb - mu0) / (s / math.sqrt(n)); tc = st.t.ppf(0.975, n - 1)
        if k % 2 == 0:
            P(f'H₀: μ = {mu0}. Mẫu n = {n}, x̄ = {fg(xb,4)}, s = {s}. Thống kê T bằng', t, f'T = ({fg(xb,4)} − {mu0})/({s}/√{n}) = {f(t,3)}.', 2, TOP['t'], SRC, extra=[-t, (xb - mu0) / s, t * math.sqrt(n)], d=3)
        else:
            dec = REJ if abs(t) > tc else ACC
            B.mcq(f'H₀: μ = {mu0} so với H₁: μ ≠ {mu0}; n = {n}, x̄ = {fg(xb,4)}, s = {s}, α = 0.05. Kết luận (dùng t):', dec, [ACC if dec == REJ else REJ, 'Dùng Z vì n nhỏ', 'Không kết luận được'],
                  f'T = {f(t,3)}; t₀.₀₂₅({n-1}) = {f(tc,3)} ⇒ {dec}.', 3, TOP['t'], SRC, 'bo_sung')
    # tỷ lệ
    for n, k, p0 in [(100, 61, 0.5), (200, 90, 0.4), (400, 230, 0.5), (150, 30, 0.25), (500, 275, 0.5), (80, 24, 0.3)]:
        ph = k / n; z = (ph - p0) / math.sqrt(p0 * (1 - p0) / n)
        P(f'H₀: p = {p0}. Mẫu n = {n} có {k} thành công. Thống kê Z cho tỷ lệ bằng', z, f'p̂ = {f(ph,3)}; Z = ({f(ph,3)} − {p0})/√({p0}·{fg(1-p0)}/{n}) = {f(z,3)}.', 2, TOP['p'], SRC, extra=[(ph - p0) / math.sqrt(ph * (1 - ph) / n), -z, (ph - p0)], d=3)
    # β
    for mu0, mu1, sg, n in [(50, 53, 6, 36), (100, 104, 10, 25), (20, 22, 5, 49), (60, 63, 9, 36), (8, 8.5, 1, 16), (75, 80, 12, 64)]:
        se = sg / math.sqrt(n); crit = mu0 + U(0.05) * se; beta = Phi((crit - mu1) / se)
        P(f'H₀: μ = {mu0} so với H₁: μ > {mu0}; σ = {sg}, n = {n}, α = 0.05. Nếu thật μ = {mu1}, lực kiểm định (1 − β) bằng', 1 - beta, f'Ngưỡng x̄ = {f(crit,3)}; β = Φ(({f(crit,3)} − {mu1})/{f(se,3)}) = {f(beta,4)}; lực = {f(1-beta,4)}.', 3, TOP['hyp'], SRC, extra=[beta, 0.05, 1 - Phi((mu1 - mu0) / se)], d=4)
    B.essay('Dây kim loại có độ bền trung bình quy định 360 kg, σ = 24. Mẫu 36 dây cho x̄ = 352. Kiểm định μ < 360 ở α = 0.05 và tính p-value.', f'Z = (352 − 360)/(24/6) = −2.0 < −1.645 ⇒ bác bỏ H₀. p = Φ(−2) = {Phi(-2):.4f}.', 2, TOP['z'], SRC, 'bo_sung')
    B.essay('Thời gian phản hồi hệ thống trung bình 2.0 giây. Sau nâng cấp, mẫu 16 lần đo có x̄ = 1.8, s = 0.4. Kiểm định “nhanh hơn” ở α = 0.05.', f'H₁: μ < 2.0. T = (1.8 − 2.0)/(0.4/4) = −2.0; −t₀.₀₅(15) = −{st.t.ppf(.95,15):.3f} ⇒ −2.0 < −1.753 ⇒ bác bỏ H₀: có bằng chứng nhanh hơn.', 2, TOP['t'], SRC, 'bo_sung')
    B.essay('Giải thích vì sao không nên kết luận “H₀ đúng” khi p-value = 0.20, và nêu cách tăng lực kiểm định.', 'p = 0.20 chỉ cho thấy dữ liệu không đủ mạnh để bác bỏ H₀; có thể do cỡ mẫu nhỏ (β lớn). Lực tăng khi tăng n, tăng α, hoặc khi chênh lệch thật lớn hơn.', 2, TOP['dec'], SRC, 'bo_sung')
    B.essay('Khảo sát 400 người, 232 ủng hộ. Kiểm định H₀: p = 0.5 so với H₁: p > 0.5 ở α = 0.05.', f'p̂ = 0.58; Z = 0.08/0.025 = 3.2 > 1.645 ⇒ bác bỏ H₀; p = {1-Phi(3.2):.4f}.', 2, TOP['p'], SRC, 'bo_sung')
