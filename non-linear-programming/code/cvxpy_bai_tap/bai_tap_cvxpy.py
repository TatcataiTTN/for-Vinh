"""BÀI TẬP CVXPY — điền vào các chỗ TODO rồi chạy:  pytest -q test_bai_tap_cvxpy.py   (hoặc mở notebook trên Colab).

Cài đặt: pip install cvxpy numpy pytest
Mỗi hàm có đặc tả đầu vào/đầu ra trong docstring; test so sánh với đáp án do lời giải mẫu (solutions.py) và đối chiếu scipy.
"""
import cvxpy as cp
import numpy as np


def kkt_multipliers_example1():
    """Ví dụ 1 slide 2: min (x-1)^2 + y - 2  s.t.  x + y - 2 <= 0,  x - y + 1 = 0.

    Đầu ra: dict {"x","y","f","lambda","mu"} (float). Gợi ý: constraint.dual_value là nhân tử.
    """
    # TODO
    raise NotImplementedError


def min_variance_portfolio(Sigma):
    """min w' Sigma w  s.t.  sum(w) = 1, w >= 0.

    Đầu vào: Sigma (list[list[float]]). Đầu ra: dict {"w": list[float], "variance": float}.
    Gợi ý: cp.quad_form(w, cp.psd_wrap(S)).
    """
    # TODO
    raise NotImplementedError


def project_onto_polyhedron(point, A, b):
    """Điểm gần nhất với point trong {x : A x <= b}.

    Đầu vào: point (list[float]), A (m x n), b (m). Đầu ra: dict {"x": list[float], "distance_sq": float}.
    Gợi ý: cp.sum_squares(x - point).
    """
    # TODO
    raise NotImplementedError


def nonneg_least_squares(A, b):
    """min ||A x - b||^2  s.t.  x >= 0.

    Đầu vào: A (m x n), b (m). Đầu ra: dict {"x": list[float], "residual_sq": float}.
    """
    # TODO
    raise NotImplementedError
