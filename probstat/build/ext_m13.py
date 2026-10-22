"""Module 13 — mở rộng: khái niệm + họ bài hồi quy (đáp án tự tính bằng numpy/scipy)."""
import math, random
import numpy as np
from scipy import stats as st
from qb import f, fg
from qh import pm
from orig_m13 import TOP
SRC = 'Bổ sung: dạng bài §4 / Kreyszig PS 25.9 (đáp án tự tính bằng numpy, đối chiếu công thức)'
def build(B):
    rng = random.Random(2513)
    def P(stem, v, *a, **k):
        k.setdefault('hi', 1.0 if 0 <= v <= 1 and k.get('unit', True) else None); k.pop('unit', None); k.setdefault('lo', None); k.setdefault('origin', 'bo_sung')
        return pm(B, rng, stem, v, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Hệ số tương quan mẫu r luôn nằm trong khoảng', '[−1, 1]', ['[0, 1]', '(−∞, ∞)', '[0, 100]'], 'Bất đẳng thức Cauchy–Schwarz.', 1, 'corr')
    C('r = −0.95 cho biết', 'quan hệ tuyến tính nghịch rất chặt', ['quan hệ yếu', 'không có quan hệ', 'quan hệ thuận'], 'Dấu: chiều; độ lớn: mức chặt.', 1, 'corr')
    C('r = 0 có nghĩa là', 'không có quan hệ TUYẾN TÍNH (có thể có quan hệ phi tuyến)', ['x, y độc lập chắc chắn', 'x = y', 'y = 0'], 'Quan hệ parabol có r ≈ 0.', 2, 'corr')
    C('Tương quan cao giữa x và y', 'không chứng minh quan hệ nhân quả', ['chứng minh x gây ra y', 'chứng minh y gây ra x', 'luôn do ngẫu nhiên'], 'Có thể do biến thứ ba.', 1, 'corr')
    C('Đường hồi quy bình phương tối thiểu cực tiểu hóa', 'tổng bình phương phần dư Σ(yᵢ − ŷᵢ)²', ['tổng phần dư Σ(yᵢ − ŷᵢ)', 'tổng |x − y|', 'r'], 'Tên gọi: least squares.', 1, 'reg')
    C('Độ dốc b của đường hồi quy y theo x là', 's_xy/s_xx', ['s_xy/s_yy', 's_xx/s_xy', 'r'], 'b = Σ(x − x̄)(y − ȳ)/Σ(x − x̄)².', 1, 'reg')
    C('Đường hồi quy luôn đi qua điểm', '(x̄, ȳ)', ['(0, 0)', '(x_max, y_max)', '(median x, median y)'], 'a = ȳ − b x̄.', 1, 'reg')
    C('Tổng các phần dư của hồi quy có hằng số bằng', '0', ['1', 'SSE', 'n'], 'Hệ quả của điều kiện cực tiểu.', 2, 'reg')
    C('R² = r² cho biết', 'tỉ lệ biến thiên của y được giải thích bởi x', ['xác suất bác bỏ H₀', 'độ dốc', 'sai số chuẩn'], 'R² = 1 − SSE/SST.', 1, 'corr')
    C('Dự báo với x ngoài miền dữ liệu gọi là', 'ngoại suy, kém tin cậy', ['nội suy, rất tin cậy', 'chuẩn hóa', 'hồi quy bội'], 'Quan hệ có thể không còn tuyến tính.', 2, 'pred')
    C('Đổi đơn vị x (nhân x với 10) thì r', 'không đổi', ['nhân 10', 'chia 10', 'đổi dấu'], 'r bất biến với phép đổi tuyến tính dương.', 2, 'corr')
    C('Đổi đơn vị x (nhân x với 10) thì độ dốc b', 'chia cho 10', ['nhân 10', 'không đổi', 'bằng r'], 'b′ = b/10.', 2, 'reg')
    C('Một ngoại lai xa so với đám điểm có thể', 'làm thay đổi mạnh đường hồi quy và r', ['không ảnh hưởng gì', 'chỉ đổi a', 'luôn làm r = 1'], 'Bình phương tối thiểu nhạy với điểm xa.', 2, 'reg')
    C('Kiểm định ρ = 0 dùng thống kê T = r√(n − 2)/√(1 − r²) với số bậc tự do', 'n − 2', ['n − 1', 'n', 'n − 3'], 'Hai tham số a, b ước lượng.', 2, 'test')
    # hồi quy dữ liệu ngẫu nhiên
    for k in range(10):
        n = rng.randint(6, 9); a0 = rng.choice([-2, 0, 3, 10]); b0 = rng.choice([0.5, 1.5, 2, -1.2, 3]); x = list(range(1, n + 1)); y = [round(a0 + b0 * v + rng.gauss(0, 0.8), 1) for v in x]
        xa, ya = np.array(x, float), np.array(y)
        sxx = ((xa - xa.mean()) ** 2).sum(); sxy = ((xa - xa.mean()) * (ya - ya.mean())).sum(); syy = ((ya - ya.mean()) ** 2).sum()
        b = sxy / sxx; a = ya.mean() - b * xa.mean(); r = sxy / math.sqrt(sxx * syy)
        data = ', '.join(f'({u}; {v})' for u, v in zip(x, y)); kind = k % 3
        if kind == 0:
            P(f'Dữ liệu (x; y): {data}. Độ dốc b của đường hồi quy y theo x bằng', float(b), f's_xy = {f(sxy,3)}, s_xx = {f(sxx,3)}; b = {f(b,4)}.', 2, TOP['reg'], SRC, extra=[float(sxy / syy), float(r), float(a)], d=4, unit=False)
        elif kind == 1:
            P(f'Dữ liệu (x; y): {data}. Hệ số tương quan mẫu r bằng', float(r), f'r = s_xy/√(s_xx·s_yy) = {f(sxy,3)}/√({f(sxx,3)}·{f(syy,3)}) = {f(r,4)}.', 2, TOP['corr'], SRC, extra=[float(r * r), float(b), float(-r)], d=4, unit=False)
        else:
            x0 = n + 2
            P(f'Dữ liệu (x; y): {data}. Dự báo y tại x = {x0} theo đường hồi quy là', float(a + b * x0), f'b = {f(b,4)}, a = ȳ − b·x̄ = {f(a,4)}; ŷ({x0}) = {f(a+b*x0,3)} (ngoại suy nhẹ).', 3, TOP['pred'], SRC, extra=[float(a + b * n), float(b * x0), float(ya.mean())], d=3, unit=False)
    for r in (0.5, 0.8, -0.6, 0.95, 0.3, -0.9):
        P(f'Hệ số tương quan mẫu r = {r}. Hệ số xác định R² bằng', r * r, f'R² = r² = {f(r*r,4)}.', 1, TOP['corr'], SRC, extra=[abs(r), r, 1 - r * r], d=4)
    for r, n in [(0.6, 12), (0.8, 10), (-0.5, 20), (0.35, 30), (0.7, 8), (-0.85, 15)]:
        t = r * math.sqrt(n - 2) / math.sqrt(1 - r * r)
        P(f'r = {r}, n = {n}. Thống kê T = r√(n − 2)/√(1 − r²) bằng', t, f'T = {r}·√{n-2}/√(1 − {fg(r*r)}) = {f(t,3)}.', 2, TOP['test'], SRC, extra=[r * math.sqrt(n), r * math.sqrt(n - 1) / math.sqrt(1 - r * r), -t if r > 0 else abs(t)], d=3, unit=False)
    B.essay('Dữ liệu (x; y): (1; 2.1), (2; 3.9), (3; 6.2), (4; 7.8), (5; 10.1), (6; 12.2). Tìm đường hồi quy, r và dự báo y tại x = 7.', 'x̄ = 3.5, ȳ = 7.05; s_xx = 17.5, s_xy = 35.35; b = 2.02; a = −0.02; r = 0.9991; ŷ(7) = 14.12.', 2, TOP['reg'], SRC, 'bo_sung')
    B.essay('Cho r = 0.82 với n = 12. Kiểm định ρ = 0 ở α = 0.05.', f'T = 0.82·√10/√(1 − 0.6724) = {0.82*math.sqrt(10)/math.sqrt(1-0.6724):.2f}; t₀.₀₂₅(10) = 2.228 ⇒ bác bỏ H₀: có tương quan tuyến tính.', 2, TOP['test'], SRC, 'bo_sung')
    B.essay('Vì sao “tương quan cao” giữa doanh số kem và số vụ đuối nước không có nghĩa kem gây đuối nước? Nêu một biến gây nhiễu.', 'Cả hai cùng tăng vào mùa nóng: nhiệt độ là biến thứ ba (gây nhiễu). Tương quan chỉ mô tả cùng biến thiên, không chứng minh nhân quả.', 2, TOP['corr'], SRC, 'bo_sung')
