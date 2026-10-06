"""Sinh exercises.json cho trang 'Thực hành code': đề bài, mã khởi đầu, test (đầu vào + đáp án kỳ vọng tính từ reference.py).

Chạy: python3 build_exercises.py        -> ghi exercises.json (cùng thư mục) và bản sao vào site
Không gõ tay đáp án: expected = reference.<hàm>(*args).
"""
import inspect, json, os
import reference as R

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SITE_OUT = os.path.join(ROOT, "for-Vinh", "non-linear-programming", "code", "exercises.json")

A_ex = [[1, 1], [3, 1], [-1, 0], [0, -1]]; b_ex = [1, 1.5, 0, 0]
A_bt = [[2, -3], [1, 1], [-3, 5], [-1, 0], [0, -1]]; b_bt = [6, 5, 15, 0, 0]
Q2 = [[2, 0], [0, 2]]

def T(args, visible=True, note=""):
    return {"args": args, "visible": visible, "note": note}

EX = [
 dict(id="gradhess", fn="gradient_hessian", module="Module 0", level="Dễ", title="Gradient và Hessian bằng sympy",
      statement="Viết hàm tính gradient và ma trận Hessian của f tại một điểm. Biểu thức f được cho dưới dạng chuỗi Python theo các biến <code>x</code>, <code>y</code> (và <code>z</code>).",
      inp="<code>f_str</code> (str): biểu thức, ví dụ <code>\"x**2*y + 3*x*y**2 - 2*x\"</code>; <code>point</code> (list[float]): tọa độ điểm, độ dài 2 hoặc 3.",
      out="Tuple <code>(grad, hess)</code>: <code>grad</code> là list[float] độ dài n; <code>hess</code> là list[list[float]] cỡ n×n (số, không phải biểu thức).",
      hint="Dùng <code>sympy.symbols</code>, <code>sympy.sympify</code>, <code>diff</code>, <code>subs</code>; ép kiểu <code>float()</code>.",
      starter="import sympy as sp\n\ndef gradient_hessian(f_str, point):\n    \"\"\"Trả về (grad, hess) tại point.\"\"\"\n    # TODO\n    pass\n",
      tests=[T(["x**2*y + 3*x*y**2 - 2*x", [1, 2]], True, "ví dụ Module 0: kỳ vọng grad (14,13), H = [[4,14],[14,6]]"),
             T(["x**2 + x*y + y**2 - 3*x", [2, -1]], True), T(["x**3 - 3*x + y**2", [-1, 0]], False), T(["x*y*z + x**2", [1, 2, 3]], False)]),
 dict(id="taylor2", fn="taylor2", module="Module 0", level="Dễ", title="Xấp xỉ Taylor bậc hai",
      statement="Tính giá trị xấp xỉ Taylor bậc hai \\(f(p)+\\nabla f(p)^\\top d+\\tfrac12d^\\top\\nabla^2f(p)d\\) của một hàm tại điểm p với bước d.",
      inp="<code>f_str</code> (str), <code>point</code> (list[float]), <code>d</code> (list[float]) cùng độ dài với point.",
      out="Một số thực (float). Sai số cho phép 1e-6.",
      hint="Có thể gọi lại hàm ở bài 1; hàm exp, log của sympy được nhận trong chuỗi.",
      starter="import numpy as np\nimport sympy as sp\n\ndef taylor2(f_str, point, d):\n    \"\"\"Trả về giá trị xấp xỉ bậc hai (float).\"\"\"\n    # TODO\n    pass\n",
      tests=[T(["exp(x) + y**2", [0, 0], [0.1, 0.2]], True, "kỳ vọng 1.145"), T(["x**2*y", [1, 1], [0.1, -0.1]], True), T(["log(x) + y**2", [1, 0], [0.1, 0.3]], False)]),
 dict(id="classify", fn="classify_matrix", module="Module 1", level="Dễ", title="Phân loại dấu ma trận đối xứng",
      statement="Cho ma trận đối xứng A, xác định A là xác định dương, nửa xác định dương, xác định âm, nửa xác định âm hay không xác định (dùng giá trị riêng, không dùng minor dẫn đầu).",
      inp="<code>A</code> (list[list[float]]): ma trận đối xứng n×n; <code>tol</code> (float, mặc định 1e-9).",
      out="Một trong các chuỗi: <code>\"PD\"</code>, <code>\"PSD\"</code> (nửa xác định dương nhưng không PD), <code>\"ND\"</code>, <code>\"NSD\"</code>, <code>\"INDEFINITE\"</code>.",
      hint="<code>numpy.linalg.eigvalsh</code> trả giá trị riêng của ma trận đối xứng; so sánh với tol.",
      starter="import numpy as np\n\ndef classify_matrix(A, tol=1e-9):\n    \"\"\"Trả về 'PD' | 'PSD' | 'ND' | 'NSD' | 'INDEFINITE'.\"\"\"\n    # TODO\n    pass\n",
      tests=[T([[[2, 1], [1, 2]]], True), T([[[1, 1], [1, 1]]], True, "PSD, det = 0"), T([[[0, 1], [1, 0]]], True), T([[[-2, 0], [0, -1]]], False), T([[[0, 0], [0, -1]]], False, "bẫy minor dẫn đầu"),
             T([[[6, -4], [-4, 6]]], False), T([[[2, -1, 0], [-1, 2, -1], [0, -1, 2]]], False)]),
 dict(id="kkt", fn="check_kkt", module="Module 2", level="Vừa", title="Kiểm tra điểm KKT",
      statement="Cho dữ liệu tại một điểm x của bài \\(\\min f\\) s.t. \\(g_i\\le0,\\ h_j=0\\): gradient của f, giá trị và gradient của từng ràng buộc. Hãy xác định x có khả thi không, những ràng buộc nào chặt, giải nhân tử \\(\\lambda,\\mu\\) bằng bình phương tối thiểu và kết luận có phải điểm KKT không.",
      inp="<code>grad_f</code> (list[float]); <code>ineq</code> (list[[g_i, grad_g_i]]); <code>eq</code> (list[[h_j, grad_h_j]]); <code>tol</code> (float, mặc định 1e-6).",
      out="dict với các khóa: <code>feasible</code> (bool), <code>active</code> (list[int], chỉ số từ 0), <code>lambda</code> (list[float], theo thứ tự active), <code>mu</code> (list[float]), <code>residual</code> (float), <code>is_kkt</code> (bool).",
      hint="Ghép các gradient ràng buộc chặt thành các cột của ma trận M, giải \\(M[\\lambda;\\mu]=-\\nabla f\\) bằng <code>numpy.linalg.lstsq</code>; KKT khi khả thi, residual ≈ 0 và mọi λ ≥ 0.",
      starter="import numpy as np\n\ndef check_kkt(grad_f, ineq, eq, tol=1e-6):\n    \"\"\"Trả về dict {'feasible','active','lambda','mu','residual','is_kkt'}.\"\"\"\n    # TODO\n    pass\n",
      tests=[T([[-1, 1], [[0, [1, 1]]], [[0, [1, -1]]]], True, "Ví dụ 1 slide 2: (λ, μ) = (0, 1)"), T([[-1, 1], [[0, [2, -2]]], []], True, "Ví dụ 3 tại (1,-1): λ = 1/2"),
             T([[1, 1], [[0, [2, 2]]], []], True, "Ví dụ 3 tại (1,1): λ = -1/2 ⇒ không KKT"), T([[0, 0], [[-2, [0, 0]]], []], False, "(0,0): ràng buộc lỏng"),
             T([[4, 4], [[6, [4, 4]]], []], False, "điểm không khả thi"), T([[2, 2], [[0, [-1, -1]], [-2, [2, 2]]], []], False, "bài C9 tại (1,1)")]),
 dict(id="eqqp", fn="solve_eq_qp", module="Module 3", level="Vừa", title="QP ràng buộc đẳng thức qua hệ KKT",
      statement="Giải \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) s.t. \\(Ax=b\\) bằng cách lập và giải hệ KKT đối xứng \\(\\begin{pmatrix}Q&A^\\top\\\\A&0\\end{pmatrix}\\begin{pmatrix}x\\\\\\mu\\end{pmatrix}=\\begin{pmatrix}-c\\\\b\\end{pmatrix}\\).",
      inp="<code>Q</code> (n×n, đối xứng), <code>c</code> (n), <code>A</code> (m×n, rank m), <code>b</code> (m) — list lồng nhau; giả sử hệ KKT không suy biến.",
      out="Tuple <code>(x, mu, f)</code>: <code>x</code> list[float] độ dài n; <code>mu</code> list[float] độ dài m; <code>f</code> float = ½xᵀQx + cᵀx. Dung sai 1e-6.",
      hint="<code>numpy.block</code> để ghép ma trận khối; <code>numpy.linalg.solve</code>.",
      starter="import numpy as np\n\ndef solve_eq_qp(Q, c, A, b):\n    \"\"\"Trả về (x, mu, f).\"\"\"\n    # TODO\n    pass\n",
      tests=[T([[[2, -2, -1], [-2, 2, 1], [-1, 1, 5]], [10, -26, -2], [[1, 1, 0], [1, 0, 1]], [4, 10]], True, "ví dụ null space slide 3: x* = (3.0588, 0.9412, 6.9412)"),
             T([[[6, 2, 1], [2, 5, 2], [1, 2, 4]], [-8, -3, -3], [[1, 0, 1], [0, 1, 1]], [3, 0]], True, "Bài tập 1 với b = (3, 0): x* = (2, -1, 1)"),
             T([Q2, [0, 0], [[1, 1]], [2]], False), T([[[4, 1], [1, 3]], [-1, -2], [[1, 2]], [1]], False)]),
 dict(id="steplen", fn="step_length", module="Module 3", level="Vừa", title="Độ dài bước α của tập hoạt động",
      statement="Cho điểm khả thi x, hướng d và tập làm việc W, tính \\(\\alpha=\\min\\{1,\\ \\min_{i\\notin W,\\ a_i^\\top d>0}(b_i-a_i^\\top x)/(a_i^\\top d)\\}\\) và chỉ số ràng buộc cản.",
      inp="<code>A</code> (m×n), <code>b</code> (m), <code>x</code> (n), <code>d</code> (n), <code>W</code> (list[int], chỉ số từ 0).",
      out="Tuple <code>(alpha, blocking)</code>: <code>alpha</code> float trong [0,1]; <code>blocking</code> int (chỉ số từ 0 của ràng buộc cản) hoặc <code>None</code> nếu α = 1 không bị cản.",
      hint="Bỏ qua i ∈ W và các i có \\(a_i^\\top d\\le0\\). Dùng ngưỡng 1e-12 khi so sánh.",
      starter="import numpy as np\n\ndef step_length(A, b, x, d, W):\n    \"\"\"Trả về (alpha, blocking).\"\"\"\n    # TODO\n    pass\n",
      tests=[T([A_ex, b_ex, [0, 0], [1, 0], [3]], True, "vòng k=1 của ví dụ slide: α = 0.5, cản bởi ràng buộc chỉ số 1"), T([A_ex, b_ex, [0.5, 0], [-0.1, 0.3], [1]], True, "vòng k=3: α = 1, không bị cản"),
             T([A_bt, b_bt, [0, 0], [4.5, 0], [4]], False, "bài tập tr.81 vòng 1: α = 2/3"), T([A_bt, b_bt, [3, 0], [2.4230769, 1.6153846], [0]], False)]),
 dict(id="activeset", fn="active_set_qp", module="Module 3", level="Khó", title="Thuật toán tập hoạt động hoàn chỉnh",
      statement="Cài đặt thuật toán tập hoạt động cho \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) s.t. \\(Ax\\le b\\) (Q đối xứng xác định dương, x0 khả thi). Mỗi vòng: giải bài toán con \\(\\min\\tfrac12d^\\top Qd+g^\\top d\\) s.t. \\(a_i^\\top d=0\\ (i\\in W)\\); nếu \\(d\\ne0\\) đi bước \\(\\alpha\\) và thêm ràng buộc cản; nếu \\(d=0\\) tính nhân tử, dừng nếu mọi \\(\\hat\\mu\\ge0\\), ngược lại loại chỉ số có nhân tử âm nhất.",
      inp="<code>Q</code> (n×n), <code>c</code> (n), <code>A</code> (m×n), <code>b</code> (m), <code>x0</code> (n), <code>W0</code> (list[int], chỉ số từ 0, tập chặt tại x0), <code>max_iter</code> (int, mặc định 50).",
      out="Tuple <code>(x, iterations)</code>: <code>x</code> list[float] nghiệm; <code>iterations</code> int = số vòng k đã chạy, tính cả vòng dừng.",
      hint="Bài toán con chính là hệ KKT bài 5 với \\(A_W\\), vế phải \\(-g\\) và 0; nhân tử \\(\\hat\\mu\\) là phần nghiệm sau khối \\(d\\). Tái sử dụng hàm bài 6.",
      starter="import numpy as np\n\ndef active_set_qp(Q, c, A, b, x0, W0, max_iter=50):\n    \"\"\"Trả về (x, iterations).\"\"\"\n    # TODO\n    pass\n",
      tests=[T([Q2, [-2, -1], A_ex, b_ex, [0, 0], [2, 3]], True, "ví dụ slide tr.69: x* = (0.4, 0.3), 5 vòng"), T([Q2, [-9, -6], A_bt, b_bt, [0, 0], [3, 4]], True, "bài tập tr.81: x* = (3.25, 1.75), 7 vòng"),
             T([Q2, [-4, -4], [[1, 1], [-1, 0], [0, -1]], [2, 0, 0], [0, 0], [1, 2]], False), T([Q2, [-1, -1], [[1, 1], [-1, 0], [0, -1]], [4, 0, 0], [0, 0], [1, 2]], False, "nghiệm nằm trong miền")]),
]

def jsonable(o):
    if isinstance(o, tuple): return [jsonable(v) for v in o]
    if isinstance(o, list): return [jsonable(v) for v in o]
    if isinstance(o, dict): return {k: jsonable(v) for k, v in o.items()}
    return o

def main():
    out = []
    for e in EX:
        fn = getattr(R, e["fn"])
        tests = []
        for t in e["tests"]:
            exp = jsonable(fn(*t["args"]))
            tests.append({"args": t["args"], "expected": exp, "visible": t["visible"], "note": t["note"]})
        item = {k: v for k, v in e.items() if k != "tests"}
        item["tests"] = tests
        deps = {"active_set_qp": ["step_length"], "taylor2": ["gradient_hessian"]}.get(e["fn"], [])
        needs_sympy = e["id"] in ("gradhess", "taylor2")
        item["reference"] = "import numpy as np\n" + ("import sympy as sp\n" if needs_sympy else "") + "\n\n" + "\n\n".join(inspect.getsource(getattr(R, d)) for d in deps + [e["fn"]])
        item["packages"] = ["numpy", "sympy"] if e["id"] in ("gradhess", "taylor2") else ["numpy"]
        out.append(item)
    os.makedirs(os.path.dirname(SITE_OUT), exist_ok=True)
    for p in (os.path.join(HERE, "exercises.json"), SITE_OUT):
        json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("đã sinh", len(out), "bài,", sum(len(e["tests"]) for e in out), "test")

if __name__ == "__main__":
    main()
