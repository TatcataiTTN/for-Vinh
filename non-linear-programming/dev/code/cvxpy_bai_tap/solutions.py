"""Lời giải mẫu cho 4 bài tập cvxpy (đặc tả đầu vào/đầu ra ngay trong docstring).
File này dùng để (1) sinh đáp án kỳ vọng, (2) CI kiểm tra rằng đề và đáp án khớp nhau. Người học tự viết trong bai_tap_cvxpy.py."""
import cvxpy as cp
import numpy as np


def kkt_multipliers_example1():
    """Giải Ví dụ 1 (slide 2): min (x-1)^2 + y - 2  s.t.  x + y - 2 <= 0,  x - y + 1 = 0.

    Đầu vào : không có.
    Đầu ra  : dict {"x": float, "y": float, "f": float, "lambda": float, "mu": float}
              (lambda: nhân tử của ràng buộc bất đẳng thức, mu: nhân tử của ràng buộc đẳng thức, cùng quy ước L = f + lambda*g + mu*h).
    """
    x, y = cp.Variable(), cp.Variable()
    g = x + y - 2 <= 0
    h = x - y + 1 == 0
    p = cp.Problem(cp.Minimize((x - 1) ** 2 + y - 2), [g, h])
    p.solve()
    return {"x": float(x.value), "y": float(y.value), "f": float(p.value), "lambda": float(g.dual_value), "mu": float(h.dual_value)}


def min_variance_portfolio(Sigma):
    """Danh mục phương sai nhỏ nhất, không bán khống:  min w' Sigma w  s.t.  sum(w) = 1,  w >= 0.

    Đầu vào : Sigma (list[list[float]]) ma trận hiệp phương sai n x n, đối xứng nửa xác định dương.
    Đầu ra  : dict {"w": list[float] (n tỉ trọng, tổng 1), "variance": float}
    """
    S = np.array(Sigma, float)
    n = S.shape[0]
    w = cp.Variable(n)
    p = cp.Problem(cp.Minimize(cp.quad_form(w, cp.psd_wrap(S))), [cp.sum(w) == 1, w >= 0])
    p.solve()
    return {"w": [float(v) for v in w.value], "variance": float(p.value)}


def project_onto_polyhedron(point, A, b):
    """Điểm gần nhất (khoảng cách Euclid) với `point` trong đa diện {x : A x <= b}  (ví dụ slide 3 tr.69: point = (1, 0.5)).

    Đầu vào : point (list[float]) độ dài n; A (m x n), b (m) — list lồng nhau.
    Đầu ra  : dict {"x": list[float] điểm chiếu, "distance_sq": float = ||x - point||^2}
    """
    n = len(point)
    x = cp.Variable(n)
    p = cp.Problem(cp.Minimize(cp.sum_squares(x - np.array(point, float))), [np.array(A, float) @ x <= np.array(b, float)])
    p.solve()
    return {"x": [float(v) for v in x.value], "distance_sq": float(p.value)}


def nonneg_least_squares(A, b):
    """Bình phương tối thiểu có ràng buộc không âm:  min ||A x - b||^2  s.t.  x >= 0.

    Đầu vào : A (m x n), b (m).
    Đầu ra  : dict {"x": list[float] (n, mọi phần tử >= 0), "residual_sq": float = ||A x - b||^2}
    """
    A = np.array(A, float); b = np.array(b, float)
    x = cp.Variable(A.shape[1])
    p = cp.Problem(cp.Minimize(cp.sum_squares(A @ x - b)), [x >= 0])
    p.solve()
    return {"x": [max(0.0, float(v)) for v in x.value], "residual_sq": float(p.value)}
