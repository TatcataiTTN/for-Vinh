"""03 — Ví dụ Slide 3: null space (tr.56-58) và active set (tr.69-79, 81), viết lại bằng numpy.

Chạy: python3 03_qp_vi_du_slide3.py        Cần: pip install numpy scipy
"""
import numpy as np
from scipy.optimize import minimize


def null_space_qp(Q, c, A, b, xbar):
    """Giải min 1/2 x'Qx + c'x  s.t.  Ax = b  qua hệ KKT đối xứng (4.2):  [Q A'; A 0][d; mu] = [-g; b - A xbar]."""
    m, n = A.shape
    g = Q @ xbar + c
    K = np.block([[Q, A.T], [A, np.zeros((m, m))]])
    sol = np.linalg.solve(K, np.concatenate([-g, b - A @ xbar]))
    return xbar + sol[:n], sol[n:]


def active_set(Q, c, A, b, x0, W0):
    """Active set cho min 1/2 x'Qx + c'x  s.t.  A x <= b  (Q đối xứng xác định dương). Chỉ số ràng buộc tính từ 1."""
    x = np.array(x0, float)
    W = [i - 1 for i in W0]
    for k in range(50):
        g = Q @ x + c
        if W:                                         # bài toán con: min 1/2 d'Qd + g'd  s.t. a_i'd = 0, i in W
            Aw = A[W]
            K = np.block([[Q, Aw.T], [Aw, np.zeros((len(W), len(W)))]])
            sol = np.linalg.solve(K, np.concatenate([-g, np.zeros(len(W))]))
            d, mu = sol[:len(x)], sol[len(x):]
        else:
            d, mu = np.linalg.solve(Q, -g), np.array([])
        print(f"  k={k}: x={np.round(x, 4)}, W={[i + 1 for i in W]}, g={np.round(g, 4)}, d={np.round(d, 4)}", end="")
        if np.linalg.norm(d) < 1e-9:                   # d = 0: xét nhân tử Lagrange
            print(f", mu={dict(zip([i + 1 for i in W], np.round(mu, 4)))}")
            if len(W) == 0 or mu.min() >= -1e-9:
                print("  => DỪNG: mọi nhân tử >= 0.")
                return x
            j = int(np.argmin(mu))
            print(f"     loại ràng buộc {W[j] + 1} (nhân tử âm nhất {mu[j]:.4f})")
            W.pop(j)
        else:                                          # d != 0: đi một bước alpha, gặp ràng buộc cản thì thêm vào W
            alpha, block = 1.0, None
            for i in range(len(b)):
                if i not in W and A[i] @ d > 1e-12:
                    t = (b[i] - A[i] @ x) / (A[i] @ d)
                    if t < alpha - 1e-12:
                        alpha, block = t, i
            print(f", alpha={alpha:.4f}" + (f", ràng buộc cản {block + 1}" if block is not None else ""))
            x = x + alpha * d
            if block is not None:
                W.append(block)
    return x


print("NULL SPACE (slide tr.56-58) — Q, c như slide")
Q = np.array([[2, -2, -1], [-2, 2, 1], [-1, 1, 5.]])
c = np.array([10, -26, -2.])
A = np.array([[1, 1, 0], [1, 0, 1.]])
b = np.array([4, 10.])
xs, mu = null_space_qp(Q, c, A, b, np.zeros(3))
print("  x* =", np.round(xs, 4), " mu* =", np.round(mu, 4), " 1/2x'Qx+c'x =", round(float(0.5 * xs @ Q @ xs + c @ xs), 4))
r = minimize(lambda v: 0.5 * v @ Q @ v + c @ v, np.zeros(3), constraints=[{"type": "eq", "fun": lambda v: A @ v - b}], method="SLSQP")
print("  đối chiếu scipy:", np.round(r.x, 4))

print("\nBÀI TẬP 1 (slide tr.59), ràng buộc x1+x3=3, x2+x3=0 (khớp ĐS (2,-1,1))")
Q1 = np.array([[6, 2, 1], [2, 5, 2], [1, 2, 4.]])
c1 = np.array([-8, -3, -3.])
A1 = np.array([[1, 0, 1], [0, 1, 1.]])
x1, mu1 = null_space_qp(Q1, c1, A1, np.array([3, 0.]), np.zeros(3))
print("  x* =", np.round(x1, 4), " mu* =", np.round(mu1, 4))

print("\nACTIVE SET — ví dụ slide tr.69: min (x1-1)^2+(x2-0.5)^2")
Qa, ca = 2 * np.eye(2), np.array([-2, -1.])
Aa = np.array([[1, 1], [3, 1], [-1, 0], [0, -1.]])
ba = np.array([1, 1.5, 0, 0])
xa = active_set(Qa, ca, Aa, ba, [0, 0], [3, 4])
print("  => x* =", np.round(xa, 4), " f =", round(float((xa[0] - 1) ** 2 + (xa[1] - 0.5) ** 2), 4))

print("\nACTIVE SET — bài tập slide tr.81: min (x1-4.5)^2+(x2-3)^2")
Ab = np.array([[2, -3], [1, 1], [-3, 5], [-1, 0], [0, -1.]])
bb = np.array([6, 5, 15, 0, 0.])
xb = active_set(2 * np.eye(2), np.array([-9, -6.]), Ab, bb, [0, 0], [4, 5])
print("  => x* =", np.round(xb, 4))
