"""Đối chiếu độc lập các lời giải mẫu (reference.py) bằng scipy/sympy/brute-force. Chạy: pytest -q test_reference.py"""
import numpy as np
from scipy.optimize import minimize
import reference as R
import build_exercises as B


def test_gradient_hessian_matches_finite_differences():
    f = lambda v: v[0] ** 2 * v[1] + 3 * v[0] * v[1] ** 2 - 2 * v[0]
    g, H = R.gradient_hessian("x**2*y + 3*x*y**2 - 2*x", [1, 2])
    e = 1e-5
    num_g = [(f([1 + e, 2]) - f([1 - e, 2])) / (2 * e), (f([1, 2 + e]) - f([1, 2 - e])) / (2 * e)]
    assert np.allclose(g, num_g, atol=1e-4) and np.allclose(H, np.array(H).T)


def test_taylor_error_is_third_order():
    exact = float(np.exp(0.1) + 0.2 ** 2)
    assert abs(R.taylor2("exp(x)+y**2", [0, 0], [0.1, 0.2]) - exact) < 5e-4


def test_classify_random_matrices():
    rng = np.random.default_rng(1)
    for _ in range(50):
        M = rng.normal(size=(3, 3)); S = M @ M.T + 0.1 * np.eye(3)
        assert R.classify_matrix(S) == "PD" and R.classify_matrix(-S) == "ND"
    assert R.classify_matrix([[0, 0], [0, -1]]) == "NSD"


def test_kkt_examples():
    r = R.check_kkt([-1, 1], [[0, [1, 1]]], [[0, [1, -1]]])
    assert r["is_kkt"] and abs(r["mu"][0] - 1) < 1e-9
    assert not R.check_kkt([1, 1], [[0, [2, 2]]], [])["is_kkt"]


def test_eq_qp_vs_slsqp():
    Q = [[2, -2, -1], [-2, 2, 1], [-1, 1, 5]]; c = [10, -26, -2]; A = [[1, 1, 0], [1, 0, 1]]; b = [4, 10]
    x, mu, f = R.solve_eq_qp(Q, c, A, b)
    r = minimize(lambda v: 0.5 * np.array(v) @ Q @ np.array(v) + np.dot(c, v), np.zeros(3), constraints=[{"type": "eq", "fun": lambda v: np.array(A) @ v - b}], method="SLSQP")
    assert np.allclose(x, r.x, atol=1e-4) and abs(f - r.fun) < 1e-4


def test_step_length_bruteforce():
    A, b, x, d = B.A_ex, B.b_ex, [0.0, 0.0], [1.0, 0.0]
    alpha, blk = R.step_length(A, b, x, d, [3])
    grid = np.linspace(0, 1, 100001)
    ok = [t for t in grid if all(np.dot(a, np.array(x) + t * np.array(d)) <= bi + 1e-12 for a, bi in zip(A, b) if True)]
    assert abs(alpha - max(ok)) < 1e-4 and blk == 1


def test_active_set_vs_slsqp():
    for Q, c, A, b, x0, W0 in [(B.Q2, [-2, -1], B.A_ex, B.b_ex, [0, 0], [2, 3]), (B.Q2, [-9, -6], B.A_bt, B.b_bt, [0, 0], [3, 4])]:
        x, it = R.active_set_qp(Q, c, A, b, x0, W0)
        r = minimize(lambda v: 0.5 * np.array(v) @ Q @ np.array(v) + np.dot(c, v), x0, constraints=[{"type": "ineq", "fun": lambda v: np.array(b) - np.array(A) @ v}], method="SLSQP", options={"ftol": 1e-14})
        assert np.allclose(x, r.x, atol=1e-4) and it >= 1
