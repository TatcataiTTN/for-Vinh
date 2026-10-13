from drawio_util import D
import os
ROOT = os.path.join(os.path.dirname(__file__), '..')
d = D(1000, 560)
d.text(20, 8, 960, 34, 'Cây xác suất hai giai đoạn: toàn phần (cộng nhánh) và Bayes (nhánh chia tổng)', 20, True)
d.text(20, 48, 960, 24, 'Ví dụ: đáp án giữa kỳ HK2 2022–2023, câu 1', 14, color='#5d6678')
r = d.box(20, 250, 110, 56, 'Chọn\nsản phẩm', 'dark', 16, True)
ys = [110, 250, 390]
pri = [('A₁', '0.45', 0.636), ('A₂', '0.25', 0.444), ('A₃', '0.30', 0.7)]
cols = ['blue', 'green', 'orange']
for (nm, p, l), y, c in zip(pri, ys, cols):
    a = d.box(280, y, 190, 56, f'Phân xưởng {'123'[ys.index(y)]}  ({nm})\nP({nm}) = {p}', c, 15, True)
    d.edge(r, a, p, size=14, exit=(1, 0.5), entry=(0, 0.5))
    b = d.box(560, y - 28, 160, 44, f'B: phế phẩm\nP(B|{nm}) = {l}', 'red', 14)
    nb = d.box(560, y + 40, 160, 44, f'B̄: đạt\n1 − {l} = {1-l:.3f}', 'gray', 14)
    d.edge(a, b, f'{l}', size=13, exit=(1, 0.5), entry=(0, 0.5)); d.edge(a, nb, f'{1-l:.3f}', size=13, dashed=True, exit=(1, 0.5), entry=(0, 0.5))
    d.box(790, y - 28, 190, 44, f'P({nm}∩B) = {float(p)*l:.4f}', c, 14, True)
d.box(20, 480, 960, 62, 'Toàn phần: P(B) = Σ P(Aᵢ)P(B|Aᵢ) = 0.2862 + 0.1110 + 0.2100 = 0.6072        |        Bayes: P(A₂|B) = 0.1110 / 0.6072 = 0.1828', 'yellow', 16, True)
d.save(os.path.join(ROOT, 'drawio', 'm04.drawio'), os.path.join(ROOT, 'img', 'm04.png'))
