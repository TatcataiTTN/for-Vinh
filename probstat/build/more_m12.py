"""Module 12 — phần chuyên sâu (số liệu tính bằng SciPy khi dựng trang)."""
import math
from scipy import stats as st
from hx import *
K = 'MODULE 12 · '
def parts():
    P = []
    s = []
    mu, sg, n = 50.0, 2.0, 5; se = sg / math.sqrt(n)
    s.append(sl(callout('info', 'Ví dụ A1 · Biểu đồ kiểm soát trung bình', f'Quy trình ổn định có μ = {mu}, σ = {sg}. Lấy mẫu con n = {n} mỗi giờ. Đường giới hạn 3σ?')
                + steps([m(f'\\sigma_{{\\bar X}}={sg}/\\sqrt{{{n}}}={se:.4f}'), m(f'UCL=\\mu+3\\sigma_{{\\bar X}}={mu+3*se:.3f},\\ LCL={mu-3*se:.3f}'), m(f'P(\\text{{báo động giả}})=2(1-\\Phi(3))={2*(1-st.norm.cdf(3)):.4f}\\approx0.27\\%')])
                + '<p>Điểm nằm ngoài [LCL, UCL] hoặc chuỗi 7–8 điểm cùng một phía là tín hiệu mất kiểm soát.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Giới hạn kiểm soát 3σ'))
    xs = [50.4, 49.7, 50.9, 51.2, 52.9, 50.1]
    s.append(sl(callout('info', 'Ví dụ A2 · Đọc biểu đồ', f'Trung bình mẫu 6 giờ liên tiếp: {", ".join(map(str, xs))}; UCL = {mu+3*se:.3f}.')
                + steps(['Mọi điểm đều trong [LCL, UCL] trừ giờ 5: 52.9 > ' + f'{mu+3*se:.3f}' + ' ⇒ tín hiệu mất kiểm soát.', 'Hành động: dừng và tìm nguyên nhân đặc biệt (nguyên liệu, dụng cụ, người vận hành) trước khi tiếp tục.']) + '<p>Biến động trong giới hạn là biến động ngẫu nhiên thông thường, không cần can thiệp.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Điểm ngoài giới hạn'))
    pb, n = 0.04, 200; sp = math.sqrt(pb * (1 - pb) / n)
    s.append(sl(callout('info', 'Ví dụ A3 · Biểu đồ p', f'Tỉ lệ phế phẩm trung bình p̄ = {pb}, mỗi lô n = {n}.')
                + steps([m(f'\\sigma_{{\\hat p}}=\\sqrt{{{pb}\\cdot{1-pb}/{n}}}={sp:.4f}'), m(f'UCL={pb}+3\\cdot{sp:.4f}={pb+3*sp:.4f}'), m(f'LCL=\\max(0,\\ {pb-3*sp:.4f})={max(0,pb-3*sp):.4f}')]) + '<p>Một lô có 18 phế phẩm: p̂ = 0.09 > UCL = ' + f'{pb+3*sp:.4f}' + ' ⇒ mất kiểm soát.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Giới hạn cho tỷ lệ'))
    P.append(dict(title='Chuyên sâu: biểu đồ kiểm soát', bullets=['Giới hạn 3σ', 'Đọc tín hiệu', 'Biểu đồ p'], slides=s))
    s = []
    obs = [18, 22, 16, 25, 19, 20]; n = sum(obs); e = n / 6; chi = sum((o - e) ** 2 / e for o in obs); c = st.chi2.ppf(.95, 5)
    s.append(sl(callout('info', 'Ví dụ B1 · Súc sắc có cân đối?', f'Gieo {n} lần, số lần mỗi mặt: {obs}. α = 0.05.')
                + table(['Mặt', '1', '2', '3', '4', '5', '6'], [['Quan sát O'] + [str(o) for o in obs], ['Kỳ vọng E'] + [f'{e:.0f}'] * 6, ['(O − E)²/E'] + [f'{(o-e)**2/e:.2f}' for o in obs]])
                + steps([m(f'\\chi^2=\\sum\\tfrac{{(O-E)^2}}{{E}}={chi:.2f}'), m(f'\\text{{df}}=6-1=5,\\ \\chi^2_{{0.05}}(5)={c:.3f}'), m(f'{chi:.2f}<{c:.3f}\\Rightarrow\\text{{không bác bỏ: súc sắc phù hợp cân đối}}')]), K + 'PHẦN 2 · Chuyên sâu', 'Kiểm định phù hợp phân phối đều'))
    o = [315, 108, 101, 32]; r = [9, 3, 3, 1]; n = sum(o); e = [n * x / 16 for x in r]; chi = sum((a - b) ** 2 / b for a, b in zip(o, e)); c = st.chi2.ppf(.95, 3)
    s.append(sl(callout('info', 'Ví dụ B2 · Tỉ lệ Mendel 9:3:3:1', f'Quan sát {o} (tổng {n}). Kỳ vọng theo tỉ lệ 9:3:3:1: ' + ', '.join(f'{x:.2f}' for x in e) + '.')
                + steps([m(f'\\chi^2={chi:.4f}'), m(f'\\text{{df}}=3,\\ \\chi^2_{{0.05}}(3)={c:.3f}'), m(f'{chi:.3f}<{c:.3f}\\Rightarrow\\text{{số liệu phù hợp tỉ lệ 9:3:3:1}}')]), K + 'PHẦN 2 · Chuyên sâu', 'Phù hợp tỉ lệ cho trước'))
    s.append(sl(callout('warn', 'Quy tắc thực hành', 'Mỗi ô nên có kỳ vọng E ≥ 5; nếu không gộp các lớp lân cận. Bậc tự do = số lớp − 1 − (số tham số ước lượng từ mẫu).')
                + '<p>Ví dụ kiểm tra phân phối chuẩn với μ, σ ước lượng từ mẫu và 8 lớp: df = 8 − 1 − 2 = 5.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Bậc tự do của kiểm định phù hợp'))
    n, k = 12, 9; p = 2 * (1 - st.binom.cdf(k - 1, n, .5)); p2 = 1 - st.binom.cdf(k - 1, n, .5)
    s.append(sl(callout('info', 'Ví dụ B3 · Kiểm định dấu', f'12 người so sánh hai loại nước ngọt; {k} người thích loại A, {n-k} thích loại B (không có hòa). H₀: median khác biệt = 0 (p = 0.5).')
                + steps([m(f'X=\\#\\text{{thích A}}\\sim B(12,0.5)\\ \\text{{dưới }}H_0'), m(f'P(X\\ge9)={p2:.4f}'), m(f'\\text{{Hai phía: }}p=2\\cdot{p2:.4f}={p:.4f}>0.05\\Rightarrow\\text{{không bác bỏ}}')]) + '<p>Kiểm định dấu chỉ dùng dấu của chênh lệch, không dùng độ lớn: ít giả định nhưng kém mạnh.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Kiểm định dấu bằng nhị thức'))
    P.append(dict(title='Chuyên sâu: kiểm định phù hợp và dấu', bullets=['Súc sắc', 'Mendel', 'Bậc tự do', 'Kiểm định dấu'], slides=s))
    return P
