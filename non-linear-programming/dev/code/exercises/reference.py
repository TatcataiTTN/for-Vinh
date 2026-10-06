"""Lời giải mẫu (reference) cho các bài tập lập trình của site.

Mỗi hàm có: đầu vào/đầu ra rõ ràng (kiểu dữ liệu), chỉ dùng numpy/scipy/sympy (chạy được trong trình duyệt bằng Pyodide).
File này là NGUỒN SỰ THẬT: `build_exercises.py` dùng nó để sinh đáp án kỳ vọng của test (không gõ tay),
và `test_reference.py` đối chiếu với scipy/sympy độc lập.
"""
import numpy as np
import sympy as sp


# ---------------------------------------------------------------- Bài 1
def gradient_hessian(f_str, point):
    """Tính gradient và Hessian của f tại một điểm.

    Đầu vào : f_str (str)   biểu thức theo các biến x, y (và z nếu có), cú pháp Python, ví dụ "x**2*y + 3*x*y**2 - 2*x"
              point (list[float])  tọa độ điểm, độ dài = số biến dùng (2 hoặc 3)
    Đầu ra  : (grad, hess) với grad: list[float] độ dài n; hess: list[list[float]] cỡ n x n
    """
    names = ["x", "y", "z"][: len(point)]
    vs = sp.symbols(names)
    f = sp.sympify(f_str, locals=dict(zip(names, vs)))
    sub = dict(zip(vs, point))
    grad = [float(sp.diff(f, v).subs(sub)) for v in vs]
    hess = [[float(sp.diff(f, a, b).subs(sub)) for b in vs] for a in vs]
    return grad, hess


# ---------------------------------------------------------------- Bài 2
def taylor2(f_str, point, d):
    """Giá trị xấp xỉ Taylor bậc hai f(p) + grad'd + 1/2 d'Hd.

    Đầu vào : f_str (str), point (list[float]) điểm p, d (list[float]) bước dịch chuyển (cùng độ dài với point)
    Đầu ra  : float
    """
    g, H = gradient_hessian(f_str, point)
    names = ["x", "y", "z"][: len(point)]
    vs = sp.symbols(names)
    f0 = float(sp.sympify(f_str, locals=dict(zip(names, vs))).subs(dict(zip(vs, point))))
    d = np.array(d, float)
    return float(f0 + np.dot(g, d) + 0.5 * d @ np.array(H) @ d)


# ---------------------------------------------------------------- Bài 3
def classify_matrix(A, tol=1e-9):
    """Phân loại dấu ma trận đối xứng bằng giá trị riêng.

    Đầu vào : A (list[list[float]]) ma trận đối xứng n x n
    Đầu ra  : một trong 5 chuỗi: "PD" (xác định dương), "PSD" (nửa xác định dương, không PD),
              "ND" (xác định âm), "NSD" (nửa xác định âm, không ND), "INDEFINITE" (không xác định)
    """
    ev = np.linalg.eigvalsh(np.array(A, float))
    if np.all(ev > tol):
        return "PD"
    if np.all(ev >= -tol):
        return "PSD"
    if np.all(ev < -tol):
        return "ND"
    if np.all(ev <= tol):
        return "NSD"
    return "INDEFINITE"


# ---------------------------------------------------------------- Bài 4
def check_kkt(grad_f, ineq, eq, tol=1e-6):
    """Kiểm tra một điểm có phải điểm KKT của bài min f s.t. g_i <= 0, h_j = 0 (dữ liệu đã tính tại điểm đó).

    Đầu vào : grad_f (list[float])       gradient của f tại điểm
              ineq   (list[[g_i, grad_g_i]])  mỗi phần tử: giá trị g_i tại điểm và gradient (list[float])
              eq     (list[[h_j, grad_h_j]])  tương tự cho ràng buộc đẳng thức
              tol    (float)             dung sai (chặt nếu |g_i| <= tol)
    Đầu ra  : dict gồm
              "feasible": bool, "active": list[int] chỉ số (từ 0) các bất đẳng thức chặt,
              "lambda": list[float] cho các bất đẳng thức chặt (cùng thứ tự active),
              "mu": list[float] cho các đẳng thức, "residual": float (|| grad_f + sum lam*grad_g + sum mu*grad_h ||),
              "is_kkt": bool  (khả thi, residual <= 1e-6, mọi lambda >= -tol)
    Gợi ý  : giải bình phương tối thiểu  [grad_g_active | grad_h] * [lam; mu] = -grad_f.
    """
    gf = np.array(grad_f, float)
    feasible = all(g <= tol for g, _ in ineq) and all(abs(h) <= tol for h, _ in eq)
    active = [i for i, (g, _) in enumerate(ineq) if abs(g) <= tol]
    cols = [np.array(ineq[i][1], float) for i in active] + [np.array(gr, float) for _, gr in eq]
    if cols:
        M = np.column_stack(cols)
        sol, *_ = np.linalg.lstsq(M, -gf, rcond=None)
        res = float(np.linalg.norm(M @ sol + gf))
    else:
        sol, res = np.array([]), float(np.linalg.norm(gf))
    lam = [float(v) for v in sol[: len(active)]]
    mu = [float(v) for v in sol[len(active):]]
    is_kkt = bool(feasible and res <= 1e-6 and all(v >= -tol for v in lam))
    return {"feasible": bool(feasible), "active": active, "lambda": lam, "mu": mu, "residual": res, "is_kkt": is_kkt}


# ---------------------------------------------------------------- Bài 5
def solve_eq_qp(Q, c, A, b):
    """Giải min 1/2 x'Qx + c'x  s.t.  Ax = b  qua hệ KKT [Q A'; A 0][x; mu] = [-c; b]  (Q đối xứng, nghiệm duy nhất).

    Đầu vào : Q (n x n), c (n), A (m x n), b (m) — list lồng nhau
    Đầu ra  : (x, mu, f) với x: list[float], mu: list[float], f: float = 1/2 x'Qx + c'x
    """
    Q, c, A, b = (np.array(v, float) for v in (Q, c, A, b))
    n, m = len(c), len(b)
    K = np.block([[Q, A.T], [A, np.zeros((m, m))]])
    sol = np.linalg.solve(K, np.concatenate([-c, b]))
    x, mu = sol[:n], sol[n:]
    return x.tolist(), mu.tolist(), float(0.5 * x @ Q @ x + c @ x)


# ---------------------------------------------------------------- Bài 6
def step_length(A, b, x, d, W):
    """Độ dài bước alpha của active set:  alpha = min{1, min_{i not in W, a_i'd > 0} (b_i - a_i'x)/(a_i'd)}.

    Đầu vào : A (m x n), b (m), x (n) điểm khả thi, d (n) hướng, W (list[int]) tập làm việc, chỉ số TỪ 0
    Đầu ra  : (alpha, blocking) với alpha: float, blocking: int chỉ số (từ 0) của ràng buộc cản, hoặc None nếu alpha = 1 không bị cản
    """
    A, b, x, d = (np.array(v, float) for v in (A, b, x, d))
    alpha, block = 1.0, None
    for i in range(len(b)):
        if i in W:
            continue
        ad = float(A[i] @ d)
        if ad > 1e-12:
            t = float((b[i] - A[i] @ x) / ad)
            if t < alpha - 1e-12:
                alpha, block = t, i
    return alpha, block


# ---------------------------------------------------------------- Bài 7
def active_set_qp(Q, c, A, b, x0, W0, max_iter=50):
    """Thuật toán tập hoạt động cho min 1/2 x'Qx + c'x  s.t.  Ax <= b  (Q đối xứng xác định dương, x0 khả thi).

    Đầu vào : Q (n x n), c (n), A (m x n), b (m), x0 (n) khả thi, W0 (list[int]) tập làm việc ban đầu, chỉ số TỪ 0
    Đầu ra  : (x, iterations) với x: list[float] nghiệm, iterations: int = số vòng lặp k đã chạy (tính cả vòng dừng)
    """
    Q, c, A, b = (np.array(v, float) for v in (Q, c, A, b))
    x = np.array(x0, float)
    W = list(W0)
    n = len(x)
    for k in range(max_iter):
        g = Q @ x + c
        if W:
            Aw = A[W]
            K = np.block([[Q, Aw.T], [Aw, np.zeros((len(W), len(W)))]])
            sol = np.linalg.solve(K, np.concatenate([-g, np.zeros(len(W))]))
            d, mu = sol[:n], sol[n:]
        else:
            d, mu = np.linalg.solve(Q, -g), np.array([])
        if np.linalg.norm(d) < 1e-9:
            if len(W) == 0 or mu.min() >= -1e-9:
                return x.tolist(), k + 1
            W.pop(int(np.argmin(mu)))
        else:
            alpha, block = step_length(A, b, x, d, W)
            x = x + alpha * d
            if block is not None:
                W.append(block)
    return x.tolist(), max_iter
