from drawio_util import D
import os
ROOT = os.path.join(os.path.dirname(__file__), '..')
d = D(1000, 640)
d.text(20, 8, 960, 34, 'Quy trình kiểm định giả thuyết (7 bước)', 22, True)
steps = [('1  H₀: θ = θ₀', 'blue'), ('2  H₁: θ <, ≠, > θ₀', 'blue'), ('3  Chọn mức ý nghĩa α\n(5%, 1%)', 'yellow'), ('4  Tiêu chuẩn T\n(U hay t? χ²?)', 'yellow'), ('5  Miền bác bỏ W_α', 'orange'), ('6  Tính T_qs từ mẫu', 'green'), ('7  T_qs ∈ W_α ?', 'dark')]
ids = []
x = 20
for i, (t, c) in enumerate(steps):
    ids.append(d.box(x, 90, 125, 80, t, c, 14, True)); x += 138
for a, b in zip(ids, ids[1:]): d.edge(a, b, '', exit=(1, 0.5), entry=(0, 0.5))
yes = d.box(330, 250, 300, 90, 'Có: bác bỏ H₀,\nthừa nhận H₁', 'red', 17, True)
no = d.box(690, 250, 300, 90, 'Không: chưa đủ cơ sở\nbác bỏ H₀ (chấp nhận H₀)', 'green', 17, True)
d.edge(ids[-1], yes, 'T_qs ∈ W_α', exit=(0.3, 1), entry=(0.5, 0)); d.edge(ids[-1], no, 'T_qs ∉ W_α', exit=(0.8, 1), entry=(0.5, 0))
d.box(20, 410, 300, 150, 'σ đã biết:\nT = (x̄ − μ₀)/(σ/√n) ~ N(0,1)\nH₁ >: T > U_α\nH₁ <: T < −U_α\nH₁ ≠: |T| > U(α/2)', 'yellow', 14, True)
d.box(350, 410, 300, 150, 'σ chưa biết:\nT = (x̄ − μ₀)/(s/√n) ~ t(n−1)\nH₁ >: T > t_α\nH₁ <: T < −t_α\nH₁ ≠: |T| > t(α/2)', 'yellow', 14, True)
d.box(680, 410, 300, 150, 'Hai sai lầm:\nLoại I: bác bỏ H₀ đúng, xác suất α\nLoại II: nhận H₀ sai, xác suất β\nLực lượng η = 1 − β', 'purple', 14, True)
d.save(os.path.join(ROOT, 'drawio', 'm10.drawio'), os.path.join(ROOT, 'img', 'm10.png'))
