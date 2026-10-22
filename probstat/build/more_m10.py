"""Module 10 — phần chuyên sâu (số liệu tính bằng SciPy khi dựng trang)."""
import math
from scipy import stats as st
from hx import *
K = 'MODULE 10 · '
U = lambda a: st.norm.ppf(1 - a)
Phi = st.norm.cdf
def parts():
    P = []
    s = []
    s.append(sl(table(['Dạng', 'H₀', 'H₁', 'Bác bỏ H₀ khi', 'p-value'], [['Hai phía', 'μ = μ₀', 'μ ≠ μ₀', '|Z| > U_{α/2}', '2·P(Z > |z|)'], ['Phía phải', 'μ = μ₀', 'μ > μ₀', 'Z > U_α', 'P(Z > z)'], ['Phía trái', 'μ = μ₀', 'μ < μ₀', 'Z < −U_α', 'P(Z < z)']])
                + callout('info', 'Chọn H₁ thế nào?', 'H₁ chứa điều cần CHỨNG MINH (“nhiều hơn”, “thấp hơn”, “khác”). H₀ là trạng thái mặc định, có dấu bằng.'), K + 'PHẦN 1 · Chuyên sâu', 'Ba dạng đối thuyết'))
    mu0, sg, n, xb = 50, 6, 36, 52.4; z = (xb - mu0) / (sg / math.sqrt(n)); pv = 2 * (1 - Phi(abs(z)))
    s.append(sl(callout('info', 'Ví dụ A1 · Kiểm định hai phía (σ biết)', f'Máy đóng gói quy định μ = {mu0} g, σ = {sg}. Mẫu n = {n} có x̄ = {xb}. Kiểm định μ ≠ {mu0} ở α = 0.05.')
                + steps([m(f'H_0:\\mu={mu0};\\ H_1:\\mu\\ne{mu0}'), m(f'Z=\\tfrac{{{xb}-{mu0}}}{{{sg}/\\sqrt{{{n}}}}}={z:.3f}'), m(f'|Z|={abs(z):.3f}>U_{{0.025}}=1.960\\Rightarrow\\text{{bác bỏ }}H_0'), m(f'p=2(1-\\Phi({abs(z):.2f}))={pv:.4f}<0.05')]) + '<p>Kết luận: có bằng chứng thống kê rằng khối lượng trung bình khác 50 g.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định Z hai phía'))
    mu0, sg, n, xb = 100, 15, 49, 96.0; z = (xb - mu0) / (sg / math.sqrt(n)); pv = Phi(z)
    s.append(sl(callout('info', 'Ví dụ A2 · Phía trái', f'Nhà sản xuất cam kết tuổi thọ trung bình {mu0} giờ (σ = {sg}). Mẫu n = {n} có x̄ = {xb}. Có bằng chứng tuổi thọ THẤP hơn cam kết ở α = 0.05?')
                + steps([m(f'H_0:\\mu={mu0};\\ H_1:\\mu<{mu0}'), m(f'Z={z:.3f};\\ -U_{{0.05}}=-1.645'), m(f'Z={z:.3f}<-1.645\\Rightarrow\\text{{bác bỏ }}H_0;\\ p=\\Phi({z:.3f})={pv:.4f}')]), K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định một phía trái'))
    mu0, n, xb, sd = 20, 16, 21.8, 3.2; t = (xb - mu0) / (sd / math.sqrt(n)); tc = st.t.ppf(0.975, n - 1); pv = 2 * (1 - st.t.cdf(abs(t), n - 1))
    s.append(sl(callout('info', 'Ví dụ A3 · Kiểm định t (σ chưa biết)', f'H₀: μ = {mu0}. Mẫu n = {n}, x̄ = {xb}, s = {sd}. α = 0.05, hai phía.')
                + steps([m(f'T=\\tfrac{{{xb}-{mu0}}}{{{sd}/\\sqrt{{{n}}}}}={t:.3f}'), m(f't_{{0.025}}({n-1})={tc:.3f}'), m(f'|T|={abs(t):.3f}<{tc:.3f}\\Rightarrow\\text{{không bác bỏ }}H_0'), m(f'p\\approx{pv:.3f}>0.05')]) + '<p>Không bác bỏ ≠ chứng minh H₀ đúng; chỉ là chưa đủ bằng chứng.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định T một mẫu'))
    P.append(dict(title='Chuyên sâu: kiểm định kỳ vọng', bullets=['Ba dạng đối thuyết', 'Kiểm định Z', 'Kiểm định T'], slides=s))
    s = []
    mu0, mu1, sg, n, a = 50, 53, 6, 36, 0.05
    se = sg / math.sqrt(n); crit = mu0 + U(a) * se; beta = Phi((crit - mu1) / se)
    s.append(sl(callout('info', 'Ví dụ B1 · Sai lầm loại I, II và lực kiểm định', f'H₀: μ = {mu0} so với H₁: μ > {mu0}; σ = {sg}, n = {n}, α = {a}. Nếu thật μ = {mu1}, xác suất sai lầm loại II và lực?')
                + steps([m(f'\\text{{Miền bác bỏ: }}\\bar x>{mu0}+1.645\\cdot1={crit:.3f}'), m(f'\\beta=P(\\bar X\\le{crit:.3f}|\\mu={mu1})=\\Phi\\!\\left(\\tfrac{{{crit:.3f}-{mu1}}}{{1}}\\right)={beta:.4f}'), m(f'\\text{{Lực}}=1-\\beta={1-beta:.4f}')])
                + callout('warn', 'Đánh đổi', 'Giảm α thì β tăng (giữ n). Muốn giảm cả hai phải tăng cỡ mẫu.'), K + 'PHẦN 2 · Chuyên sâu', 'Tính β và lực'))
    s.append(sl(table(['', 'H₀ đúng', 'H₀ sai'], [['Bác bỏ H₀', 'Sai lầm loại I (xác suất α)', 'Quyết định đúng (lực 1 − β)'], ['Không bác bỏ H₀', 'Quyết định đúng (1 − α)', 'Sai lầm loại II (xác suất β)']])
                + '<p>Ví dụ y tế: H₀ “thuốc không hiệu quả”. Loại I: kết luận thuốc hiệu quả khi thực ra không (cho ra thị trường thuốc vô dụng). Loại II: bỏ lỡ một thuốc hiệu quả.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Bảng hai loại sai lầm'))
    p0, n, k = 0.5, 100, 61; ph = k / n; z = (ph - p0) / math.sqrt(p0 * (1 - p0) / n); pv = 1 - Phi(z)
    s.append(sl(callout('info', 'Ví dụ B2 · Kiểm định tỷ lệ', f'Đồng xu nghi ngờ thiên về sấp: {k} sấp trong {n} lần. H₀: p = 0.5; H₁: p > 0.5, α = 0.05.')
                + steps([m(f'\\hat p={ph:.2f},\\ Z=\\tfrac{{{ph}-0.5}}{{\\sqrt{{0.5\\cdot0.5/{n}}}}}={z:.3f}'), m(f'Z>1.645\\Rightarrow\\text{{bác bỏ }}H_0;\\ p={pv:.4f}')]) + '<p>Sai số chuẩn dùng p₀ (không phải p̂) vì dưới H₀ tỷ lệ là p₀.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Kiểm định tỷ lệ'))
    s.append(sl(callout('info', 'Ví dụ B3 · Cùng chênh lệch, khác cỡ mẫu', 'x̄ = 51, μ₀ = 50, σ = 6.')
                + table(['n', 'σ/√n', 'Z', 'p (hai phía)', 'Kết luận α = 0.05'], [[str(n_), f'{6/math.sqrt(n_):.3f}', f'{1/(6/math.sqrt(n_)):.3f}', f'{2*(1-Phi(1/(6/math.sqrt(n_)))):.4f}', 'bác bỏ' if 2 * (1 - Phi(1 / (6 / math.sqrt(n_)))) < 0.05 else 'không bác bỏ'] for n_ in (16, 36, 100, 400)])
                + '<p>Chênh lệch 1 đơn vị không đổi nhưng n lớn làm “có ý nghĩa thống kê”. Ý nghĩa thống kê khác ý nghĩa thực tiễn.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Cỡ mẫu và p-value'))
    P.append(dict(title='Chuyên sâu: sai lầm, lực kiểm định, tỷ lệ', bullets=['β và lực', 'Hai loại sai lầm', 'Tỷ lệ', 'Cỡ mẫu và p-value'], slides=s))
    return P
