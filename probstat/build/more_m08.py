"""Module 8 — phần chuyên sâu (số liệu tính bằng SciPy khi dựng trang)."""
import math
from scipy import stats as st
from hx import *
from qb import fg, f
K = 'MODULE 8 · '
U = lambda a: st.norm.ppf(1 - a)
T = lambda a, d: st.t.ppf(1 - a, d)
def parts():
    P = []
    s = []
    s.append(sl(table(['Độ tin cậy 1 − α', 'α/2', 'U(α/2)', 'Ý nghĩa'], [[f'{c}%', f'{(100-c)/200:.4f}', f'{U((100-c)/200):.4f}', f'khoảng ±{U((100-c)/200):.2f} σ_X̄'] for c in (90, 95, 98, 99)])
                + callout('info', 'Cách hiểu đúng', 'Độ tin cậy 95% nghĩa: nếu lặp lại việc lấy mẫu và dựng khoảng nhiều lần, khoảng 95% số lần chứa μ thật. Không nói “μ nằm trong khoảng này với xác suất 95%” (μ cố định, khoảng mới là ngẫu nhiên).'), K + 'PHẦN 1 · Chuyên sâu', 'Độ tin cậy và giá trị tới hạn'))
    x, n, sg = 52.3, 36, 6.0; z = U(0.025); e = z * sg / math.sqrt(n)
    s.append(sl(callout('info', 'Ví dụ A1 · σ biết', f'Mẫu n = {n}, x̄ = {x}, σ = {sg}. Khoảng tin cậy 95% cho μ.')
                + steps([m(f'\\sigma_{{\\bar X}}={sg}/\\sqrt{{{n}}}=1'), m(f'e=U_{{0.025}}\\cdot1={z:.4f}'), m(f'\\mu\\in({x-e:.3f};\\ {x+e:.3f})')]) + '<p>Độ rộng khoảng = 2e = ' + f'{2*e:.3f}.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Khoảng cho μ khi σ biết'))
    x, s_, n = 52.3, 6.4, 16; t = T(0.025, n - 1); e = t * s_ / math.sqrt(n)
    s.append(sl(callout('info', 'Ví dụ A2 · σ chưa biết', f'Mẫu n = {n}, x̄ = {x}, s = {s_}. Khoảng 95% cho μ.')
                + steps([m(f'\\text{{df}}={n-1},\\ t_{{0.025}}({n-1})={t:.3f}'), m(f'e={t:.3f}\\cdot\\tfrac{{{s_}}}{{\\sqrt{{{n}}}}}={e:.3f}'), m(f'\\mu\\in({x-e:.3f};\\ {x+e:.3f})')]) + f'<p>Nếu dùng U₀.₀₂₅ = 1.960 sẽ được e = {1.96*s_/math.sqrt(n):.3f}, hẹp hơn một cách sai lầm; t rộng hơn vì s là ước lượng.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Khoảng cho μ khi σ chưa biết (Student)'))
    s.append(sl(table(['df', '5', '10', '15', '30', '100', '∞ (chuẩn)'], [['t₀.₀₂₅(df)'] + [f'{T(0.025, d):.3f}' for d in (5, 10, 15, 30, 100)] + [f'{U(0.025):.3f}']])
                + '<p>Khi n tăng, t tiến về chuẩn; n ≥ 30 thì khác biệt nhỏ.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Student so với chuẩn'))
    P.append(dict(title='Chuyên sâu: khoảng tin cậy cho kỳ vọng', bullets=['Độ tin cậy', 'σ biết', 'σ chưa biết', 'Student'], slides=s))
    s = []
    n, k = 400, 232; p = k / n; z = U(0.025); e = z * math.sqrt(p * (1 - p) / n)
    s.append(sl(callout('info', 'Ví dụ B1 · Khoảng cho tỷ lệ', f'Khảo sát {n} người, {k} ủng hộ. Khoảng tin cậy 95% cho tỷ lệ p.')
                + steps([m(f'\\hat p={k}/{n}={p:.3f}'), m(f'e=1.96\\sqrt{{\\tfrac{{{p:.3f}\\cdot{1-p:.3f}}}{{{n}}}}}={e:.4f}'), m(f'p\\in({p-e:.4f};\\ {p+e:.4f})')]) + '<p>Điều kiện: np̂ ≥ 5 và n(1 − p̂) ≥ 5.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Thăm dò dư luận'))
    e0 = 0.03; n0 = (z / e0) ** 2 * 0.25
    s.append(sl(callout('info', 'Ví dụ B2 · Cỡ mẫu cho tỷ lệ', 'Muốn sai số ±3% ở độ tin cậy 95% (chưa biết p).')
                + steps([m('n\\ge\\left(\\tfrac{U_{\\alpha/2}}{e}\\right)^2p(1-p),\\ \\text{lấy }p=0.5\\text{ cho trường hợp xấu nhất}'), m(f'n\\ge\\left(\\tfrac{{1.96}}{{0.03}}\\right)^2\\cdot0.25={n0:.2f}\\Rightarrow n={math.ceil(n0)}')]) + '<p>Cỡ mẫu khoảng 1068 cho cuộc thăm dò ±3% — đó là lý do các cuộc thăm dò thường dùng ~1000 người.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Cỡ mẫu tối thiểu'))
    s1, n1 = 10, 25; e1 = 2
    nn = (z * s1 / e1) ** 2
    s.append(sl(callout('info', 'Ví dụ B3 · Cỡ mẫu cho kỳ vọng', 'σ ≈ 10, sai số tối đa 2, độ tin cậy 95%.')
                + steps([m(f'n\\ge(U\\sigma/e)^2=(1.96\\cdot10/2)^2={nn:.2f}\\Rightarrow n={math.ceil(nn)}')]) + '<p>Muốn sai số một nửa thì cần n gấp 4 lần.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Cỡ mẫu và sai số'))
    s.append(sl(table(['Điều cần đổi', 'Độ rộng khoảng', 'Lý do'], [['Tăng độ tin cậy', 'rộng hơn', 'U lớn hơn'], ['Tăng cỡ mẫu n', 'hẹp hơn', 'σ/√n nhỏ hơn'], ['σ (hoặc s) nhỏ hơn', 'hẹp hơn', 'dữ liệu ít phân tán']])
                + callout('warn', 'Đánh đổi', 'Không thể vừa tăng độ tin cậy vừa thu hẹp khoảng nếu giữ nguyên n; chỉ tăng n mới được cả hai.'), K + 'PHẦN 2 · Chuyên sâu', 'Điều gì quyết định độ rộng'))
    P.append(dict(title='Chuyên sâu: tỷ lệ và cỡ mẫu', bullets=['Khoảng cho p', 'Cỡ mẫu cho p và μ', 'Độ rộng'], slides=s))
    return P
