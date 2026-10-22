"""Module 11 — phần chuyên sâu (số liệu tính bằng SciPy khi dựng trang)."""
import math
from scipy import stats as st
from hx import *
K = 'MODULE 11 · '
def parts():
    P = []
    s = []
    s.append(sl(table(['df', '5', '10', '15', '20', '30'], [['χ²₀.₀₂₅(df)'] + [f'{st.chi2.ppf(.975, d):.3f}' for d in (5, 10, 15, 20, 30)], ['χ²₀.₉₇₅(df)'] + [f'{st.chi2.ppf(.025, d):.3f}' for d in (5, 10, 15, 20, 30)]])
                + ul(['χ² ≥ 0, lệch phải, trung bình = df, phương sai = 2·df.', 'Nếu Z₁…Z_k chuẩn tắc độc lập thì ΣZᵢ² ~ χ²(k).', '(n − 1)S²/σ² ~ χ²(n − 1) khi mẫu chuẩn.']), K + 'PHẦN 1 · Chuyên sâu', 'Phân phối χ² và bảng giá trị'))
    n, s2, sg0 = 16, 18.5, 12; chi = (n - 1) * s2 / sg0; lo = st.chi2.ppf(.025, n - 1); hi = st.chi2.ppf(.975, n - 1)
    s.append(sl(callout('info', 'Ví dụ A1 · Kiểm định phương sai hai phía', f'H₀: σ² = {sg0}; H₁: σ² ≠ {sg0}. Mẫu n = {n}, s² = {s2}. α = 0.05.')
                + steps([m(f'\\chi^2=\\tfrac{{(n-1)s^2}}{{\\sigma_0^2}}=\\tfrac{{15\\cdot{s2}}}{{{sg0}}}={chi:.3f}'), m(f'\\text{{Miền chấp nhận }}[{lo:.3f};\\ {hi:.3f}]'), m(f'{chi:.3f}\\in[{lo:.3f};{hi:.3f}]\\Rightarrow\\text{{không bác bỏ }}H_0')]), K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định σ² (hai phía)'))
    n, s2, sg0 = 25, 0.0064, 0.0049; chi = (n - 1) * s2 / sg0; c = st.chi2.ppf(.95, n - 1)
    s.append(sl(callout('info', 'Ví dụ A2 · Phía phải', f'Quy định σ² = {sg0} (σ = 0.07). Mẫu n = {n} có s² = {s2}. H₁: σ² > {sg0}, α = 0.05.')
                + steps([m(f'\\chi^2=\\tfrac{{24\\cdot{s2}}}{{{sg0}}}={chi:.3f}'), m(f'\\chi^2_{{0.05}}(24)={c:.3f}'), m(f'{chi:.3f}<{c:.3f}\\Rightarrow\\text{{chưa bác bỏ }}H_0')]), K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định σ² (phía phải)'))
    P.append(dict(title='Chuyên sâu: χ² và kiểm định phương sai', bullets=['Phân phối χ²', 'Hai phía', 'Phía phải'], slides=s))
    s = []
    n1, n2, x1, x2, s1, s2_ = 12, 15, 78.4, 72.9, 6.1, 7.4
    sp2 = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2_ ** 2) / (n1 + n2 - 2); sp = math.sqrt(sp2); t = (x1 - x2) / (sp * math.sqrt(1 / n1 + 1 / n2)); tc = st.t.ppf(.975, n1 + n2 - 2)
    s.append(sl(callout('info', 'Ví dụ B1 · So sánh hai kỳ vọng (t gộp)', f'Nhóm 1: n = {n1}, x̄ = {x1}, s = {s1}. Nhóm 2: n = {n2}, x̄ = {x2}, s = {s2_}. H₀: μ₁ = μ₂; H₁: μ₁ ≠ μ₂; α = 0.05; phương sai bằng nhau.')
                + steps([m(f's_p^2=\\tfrac{{11\\cdot{s1}^2+14\\cdot{s2_}^2}}{{25}}={sp2:.3f},\\ s_p={sp:.3f}'), m(f'T=\\tfrac{{{x1}-{x2}}}{{{sp:.3f}\\sqrt{{1/{n1}+1/{n2}}}}}={t:.3f}'), m(f't_{{0.025}}(25)={tc:.3f}'), m(f'|T|={abs(t):.3f}>{tc:.3f}\\Rightarrow\\text{{bác bỏ }}H_0' if abs(t) > tc else f'|T|={abs(t):.3f}<{tc:.3f}\\Rightarrow\\text{{không bác bỏ }}H_0')]), K + 'PHẦN 2 · Chuyên sâu', 'T gộp cho hai mẫu độc lập'))
    F = s2_ ** 2 / s1 ** 2; fc = st.f.ppf(.975, n2 - 1, n1 - 1)
    s.append(sl(callout('info', 'Ví dụ B2 · Kiểm định F để so sánh phương sai', f'Cùng số liệu Ví dụ B1: kiểm định H₀: σ₁² = σ₂² ở α = 0.05 (hai phía).')
                + steps([m(f'F=\\tfrac{{s_2^2}}{{s_1^2}}=\\tfrac{{{s2_**2:.2f}}}{{{s1**2:.2f}}}={F:.3f}\\ (\\text{{lấy phương sai lớn / nhỏ}})'), m(f'F_{{0.025}}(14,11)={fc:.3f}'), m(f'{F:.3f}<{fc:.3f}\\Rightarrow\\text{{không bác bỏ: có thể coi phương sai bằng nhau}}')]) + '<p>Đây là điều kiện cần kiểm tra trước khi dùng t gộp.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Kiểm định F'))
    d = [3, 1, 4, 0, 2, 3, 5, 1]; nd = len(d); dm = sum(d) / nd; sd = math.sqrt(sum((v - dm) ** 2 for v in d) / (nd - 1)); t = dm / (sd / math.sqrt(nd)); tc = st.t.ppf(.975, nd - 1)
    s.append(sl(callout('info', 'Ví dụ B3 · Mẫu ghép cặp', 'Điểm trước và sau khóa học của 8 học viên; hiệu (sau − trước): ' + ', '.join(map(str, d)) + '.')
                + steps([m(f'\\bar d={dm:.3f},\\ s_d={sd:.3f}'), m(f'T=\\tfrac{{\\bar d}}{{s_d/\\sqrt8}}={t:.3f}'), m(f't_{{0.025}}(7)={tc:.3f}\\Rightarrow\\text{{bác bỏ }}H_0:\\ \\mu_d=0')]) + '<p>Ghép cặp = kiểm định T một mẫu trên các hiệu; mạnh hơn mẫu độc lập khi có tương quan cặp.</p>', K + 'PHẦN 2 · Chuyên sâu', 'So sánh ghép cặp'))
    s.append(sl(table(['Tình huống', 'Phương pháp', 'Thống kê'], [['σ² so với giá trị cho trước', 'χ²', '(n−1)s²/σ₀²'], ['Hai phương sai', 'F', 's₁²/s₂²'], ['Hai kỳ vọng, hai mẫu độc lập, σ chưa biết, bằng nhau', 't gộp', '(x̄₁−x̄₂)/(s_p√(1/n₁+1/n₂))'], ['Hai kỳ vọng, cùng đối tượng đo hai lần', 't ghép cặp', 'd̄/(s_d/√n)']]), K + 'PHẦN 2 · Chuyên sâu', 'Chọn kiểm định nào?'))
    P.append(dict(title='Chuyên sâu: so sánh hai kỳ vọng và hai phương sai', bullets=['t gộp', 'F', 'Ghép cặp', 'Chọn phương pháp'], slides=s))
    return P
