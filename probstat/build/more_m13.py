"""Module 13 — phần chuyên sâu (hồi quy tính bằng numpy khi dựng trang)."""
import math
import numpy as np
from scipy import stats as st
from hx import *
K = 'MODULE 13 · '
def fit(x, y):
    x = np.array(x, float); y = np.array(y, float); n = len(x)
    sxx = ((x - x.mean()) ** 2).sum(); sxy = ((x - x.mean()) * (y - y.mean())).sum(); syy = ((y - y.mean()) ** 2).sum()
    b = sxy / sxx; a = y.mean() - b * x.mean(); r = sxy / math.sqrt(sxx * syy)
    return n, x.mean(), y.mean(), sxx, sxy, syy, b, a, r
def parts():
    P = []
    s = []
    x = [1, 2, 3, 4, 5, 6]; y = [2.1, 3.9, 6.2, 7.8, 10.1, 12.2]
    n, xb, yb, sxx, sxy, syy, b, a, r = fit(x, y)
    s.append(sl(callout('info', 'Ví dụ A1 · Đường hồi quy từng bước', 'x = giờ ôn tập, y = điểm. Dữ liệu: ' + ', '.join(f'({u}; {v})' for u, v in zip(x, y)) + '.')
                + table(['x', 'y', 'x − x̄', 'y − ȳ', '(x − x̄)²', '(x − x̄)(y − ȳ)'], [[str(u), str(v), f'{u-xb:.2f}', f'{v-yb:.2f}', f'{(u-xb)**2:.2f}', f'{(u-xb)*(v-yb):.3f}'] for u, v in zip(x, y)])
                + steps([m(f'\\bar x={xb:.2f},\\ \\bar y={yb:.3f}'), m(f's_{{xx}}={sxx:.3f},\\ s_{{xy}}={sxy:.3f}'), m(f'b=\\tfrac{{s_{{xy}}}}{{s_{{xx}}}}={b:.4f},\\ a=\\bar y-b\\bar x={a:.4f}'), m(f'\\hat y={a:.4f}+{b:.4f}\\,x')]) + f'<p>Dự báo x = 7 giờ: ŷ = {a+b*7:.3f} điểm.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Tính hệ số hồi quy', explain='Độ dốc b nói: tăng 1 giờ ôn thì điểm tăng trung bình b điểm. a là điểm dự báo khi x = 0 (có thể vô nghĩa nếu x = 0 nằm ngoài dữ liệu).'))
    s.append(sl(callout('info', 'Ví dụ A2 · Hệ số tương quan và R²', 'Cùng dữ liệu Ví dụ A1.')
                + steps([m(f'r=\\tfrac{{s_{{xy}}}}{{\\sqrt{{s_{{xx}}s_{{yy}}}}}}={r:.5f}'), m(f'R^2=r^2={r*r:.4f}'), 'Khoảng 99.8% biến thiên của y được giải thích bởi quan hệ tuyến tính với x.']) + '<p>r gần 1: quan hệ tuyến tính dương rất chặt.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Mức độ tuyến tính'))
    t = r * math.sqrt(n - 2) / math.sqrt(1 - r * r); tc = st.t.ppf(.975, n - 2)
    s.append(sl(callout('info', 'Ví dụ A3 · Kiểm định ρ = 0', 'H₀: ρ = 0 so với H₁: ρ ≠ 0, α = 0.05.')
                + steps([m(f'T=\\tfrac{{r\\sqrt{{n-2}}}}{{\\sqrt{{1-r^2}}}}={t:.2f}'), m(f't_{{0.025}}({n-2})={tc:.3f}\\Rightarrow|T|>t\\Rightarrow\\text{{bác bỏ }}H_0')]) + '<p>Có bằng chứng về tương quan tuyến tính; chưa chứng minh quan hệ nhân quả.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Kiểm định tương quan'))
    P.append(dict(title='Chuyên sâu: hồi quy từng bước', bullets=['Tính a, b', 'r và R²', 'Kiểm định ρ'], slides=s))
    s = []
    s.append(sl(table(['r', 'Diễn giải thường dùng'], [['0.9 – 1', 'rất mạnh'], ['0.7 – 0.9', 'mạnh'], ['0.4 – 0.7', 'trung bình'], ['0.2 – 0.4', 'yếu'], ['< 0.2', 'gần như không tuyến tính']])
                + callout('warn', 'Bẫy', 'r nhỏ chưa chắc không có quan hệ: quan hệ có thể phi tuyến (parabol có r ≈ 0). Luôn vẽ biểu đồ phân tán trước. Tương quan ≠ nhân quả.'), K + 'PHẦN 2 · Chuyên sâu', 'Đọc hệ số tương quan'))
    xo = [1, 2, 3, 4, 5, 6, 7, 8]; yo = [3, 5, 7, 9, 11, 13, 15, 60]
    r1 = fit(xo, yo)[-1]; r2 = fit(xo[:-1], yo[:-1])[-1]
    s.append(sl(callout('info', 'Ví dụ B1 · Một ngoại lai phá hỏng hồi quy', 'Dữ liệu y = 2x + 1 với x = 1..7 và thêm điểm (8; 60) thay vì (8; 17).')
                + steps([f'Có điểm ngoại lai: r = {r1:.4f}, b = {fit(xo,yo)[6]:.3f}.', f'Bỏ điểm ngoại lai: r = {r2:.4f}, b = {fit(xo[:-1],yo[:-1])[6]:.3f} (đúng bằng 2).']) + '<p>Hồi quy bình phương tối thiểu rất nhạy với điểm xa (đòn bẩy). Cần kiểm tra biểu đồ phân tán.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Ngoại lai và đòn bẩy'))
    s.append(sl(formula('Dự báo và phần dư', '\\hat y_i=a+bx_i,\\qquad e_i=y_i-\\hat y_i,\\qquad \\sum e_i=0,\\qquad SSE=\\sum e_i^2')
                + callout('info', 'Ví dụ B2', 'Với đường ŷ = −0.02 + 2.02x (Ví dụ A1): tại x = 3, y = 6.2: ŷ = 6.04, phần dư e = 0.16. Dự báo ngoài miền dữ liệu (ngoại suy) kém tin cậy.'), K + 'PHẦN 2 · Chuyên sâu', 'Phần dư'))
    s.append(sl(callout('info', 'Ví dụ B3 · Đổi đơn vị', 'Nếu x đổi từ giờ sang phút (x′ = 60x) thì độ dốc b′ = b/60; r không đổi.')
                + '<p>r không phụ thuộc đơn vị và không phụ thuộc phép đổi tuyến tính dương. Đổi vai trò x, y: r không đổi nhưng hai đường hồi quy khác nhau.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Tính bất biến của r'))
    P.append(dict(title='Chuyên sâu: diễn giải và bẫy', bullets=['Mức độ r', 'Ngoại lai', 'Phần dư', 'Đổi đơn vị'], slides=s))
    return P
