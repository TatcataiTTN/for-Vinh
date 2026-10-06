"""Sinh notebook Colab 'nlp_cvxpy_vi_du.ipynb' (có kết quả đã chạy) từ các script trong thư mục này.
Chạy: python3 build_notebook.py   -> notebooks/nlp_cvxpy_vi_du.ipynb (đã execute)"""
import os, nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

HERE = os.path.dirname(os.path.abspath(__file__))
nb = nbf.v4.new_notebook()
C = nbf.v4.new_code_cell; M = nbf.v4.new_markdown_cell
cells = [
 M("# Tối ưu hóa: giải ví dụ của slide bằng code (cvxpy)\n\nNotebook này đi kèm site *Tối ưu hóa phi tuyến & lồi* (Phenikaa). "
   "Mở trên **Google Colab** bằng nút “Open in Colab”; Colab có sẵn Python nên chạy được cả `cvxpy` (điều mà trình duyệt thuần không làm được).\n\n"
   "**Quy ước nhân tử:** `cvxpy` trả `constraint.dual_value`; với ràng buộc dạng `g <= 0` đó chính là λ ≥ 0 trong `L = f + Σ λ_i g_i + Σ μ_j h_j`."),
 C("try:\n    import cvxpy as cp\nexcept ImportError:\n    %pip install -q cvxpy\n    import cvxpy as cp\nimport numpy as np, sympy as sp, itertools\nprint('cvxpy', cp.__version__)"),
 M("## 1. Bài mẫu trong file `tam thoi la vay.docx`\n\n`min (x-3)² + (y-4)² - 2` với `x² + y² ≤ 36`, `x ≥ 0`, `y ≥ 0`. Hàm mục tiêu và miền đều lồi (DCP), không cần `qcp=True`."),
 C("x, y = cp.Variable(), cp.Variable()\nobjective = cp.Minimize((x - 3)**2 + (y - 4)**2 - 2)\nconstraints = [x**2 + y**2 <= 36, x >= 0, y >= 0]\nproblem = cp.Problem(objective, constraints)\nprint('DCP (lồi theo quy tắc cvxpy):', problem.is_dcp())\nproblem.solve()\nprint('f* =', round(problem.value, 6), '| x =', round(float(x.value), 6), '| y =', round(float(y.value), 6))\nprint('nhân tử:', [round(abs(float(c.dual_value)), 6) for c in constraints])"),
 M("**Kiểm tra bằng tay (3 dòng):** cực tiểu không ràng buộc là (3,4), `3²+4² = 25 ≤ 36` nên khả thi, mọi ràng buộc lỏng ⇒ mọi nhân tử bằng 0 ⇒ nghiệm (3,4), f* = −2."),
 M("## 2. Ví dụ 1 của slide 2 (tr.55): bài toán lồi, nhân tử (λ, μ) = (0, 1)"),
 C("x, y = cp.Variable(), cp.Variable()\ng = x + y - 2 <= 0\nh = x - y + 1 == 0\np = cp.Problem(cp.Minimize((x - 1)**2 + y - 2), [g, h]); p.solve()\nprint('x*, y* =', round(float(x.value), 4), round(float(y.value), 4), '| f* =', round(p.value, 4))\nprint('lambda =', round(float(g.dual_value), 4), '| mu =', round(float(h.dual_value), 4))"),
 M("## 3. Ví dụ 3 (tr.60): bài toán KHÔNG lồi — liệt kê điểm KKT bằng sympy\n\nThay cho bảng dài viết tay: chia trường hợp *ràng buộc chặt / lỏng*, giải hệ dừng + bù, rồi lọc nghiệm khả thi có λ ≥ 0."),
 C("def kkt_enumerate(f, ineq, eq, vars_):\n    lam = sp.symbols(f'l1:{len(ineq)+1}', real=True)\n    mu = sp.symbols(f'm1:{len(eq)+1}', real=True)\n    L = f + sum(l*g for l, g in zip(lam, ineq)) + sum(m*h for m, h in zip(mu, eq))\n    out = []\n    for active in itertools.product([False, True], repeat=len(ineq)):\n        eqs = [sp.diff(L, v) for v in vars_] + list(eq)\n        for a, l, g in zip(active, lam, ineq):\n            eqs.append(g if a else l)          # chặt: g=0 ; lỏng: lambda=0\n        for sol in sp.solve(eqs, list(vars_) + list(lam) + list(mu), dict=True):\n            if not all(v.is_real for v in sol.values()): continue\n            feasible = all(g.subs(sol) <= 1e-9 for g in ineq)\n            ok = feasible and all(sol[l] >= -1e-9 for l in lam)\n            out.append(({v: sol[v] for v in vars_}, {str(l): sol[l] for l in lam}, ok))\n    return out\n\nX, Y = sp.symbols('x y', real=True)\nfor pt, lam, ok in kkt_enumerate(X*Y, [X**2 + Y**2 - 2], [], (X, Y)):\n    print(pt, lam, 'f =', pt[X]*pt[Y], '->', 'KKT hợp lệ' if ok else 'loại')"),
 M("## 4. Ví dụ 2 (tr.57): kiểm chứng điểm (1/3, 8/3)\n\nBài `min −(x²+y²+4x−6y)` với `x+y ≤ 3`, `−2x+y ≤ 2`."),
 C("F = -(X**2 + Y**2 + 4*X - 6*Y)\nfor pt, lam, ok in kkt_enumerate(F, [X + Y - 3, -2*X + Y - 2], [], (X, Y)):\n    print(pt, lam, 'HỢP LỆ' if ok else 'loại')\nprint('Điểm (1/3, 8/3) có lambda_2 = -16/9 < 0 nên KHÔNG phải điểm KKT.')"),
 M("## 5. Ví dụ 4 (tr.61): quy hoạch tuyến tính"),
 C("x, y = cp.Variable(), cp.Variable()\ncons = [3*x + y <= 6, x + y <= 4, x >= 0, y >= 0]\nfor sense in (cp.Minimize, cp.Maximize):\n    p = cp.Problem(sense(2*x + y), cons); p.solve()\n    print(sense.__name__, '->', (round(float(x.value), 4), round(float(y.value), 4)), 'f* =', round(p.value, 4))"),
 M("## 6. Tự làm\n\nĐổi bài toán ở mục 1 thành `x² + y² ≤ 4` (miền nhỏ hơn). Nghiệm có còn là (3,4) không? Ràng buộc nào chặt, nhân tử bằng bao nhiêu? Dự đoán trước bằng tay (chiếu điểm (3,4) lên hình tròn bán kính 2), rồi kiểm bằng code."),
 C("# TODO: viết code của bạn ở đây\n"),
]
nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "colab": {"provenance": []}}
ExecutePreprocessor(timeout=300, kernel_name="python3").preprocess(nb, {"metadata": {"path": HERE}})
out = os.path.join(HERE, "notebooks", "nlp_cvxpy_vi_du.ipynb")
nbf.write(nb, out)
print("ghi", out)
