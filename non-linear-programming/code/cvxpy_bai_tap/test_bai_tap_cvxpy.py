"""Chấm bài tập cvxpy. Chạy:  pytest -q test_bai_tap_cvxpy.py
Mặc định chấm file bai_tap_cvxpy.py của bạn; đặt biến môi trường NLP_USE_SOLUTIONS=1 để chấm lời giải mẫu (CI dùng cách này)."""
import importlib, os
import numpy as np
import pytest
from scipy.optimize import minimize, nnls

mod = importlib.import_module("solutions" if os.environ.get("NLP_USE_SOLUTIONS") == "1" else "bai_tap_cvxpy")

SIGMA = [[0.01, 0.0120, 0.0040], [0.0120, 0.0225, 0.0270], [0.0040, 0.0270, 0.0400]]   # case study Module 2 (σ = 10%, 15%, 20%)
A_POLY = [[1, 1], [3, 1], [-1, 0], [0, -1]]; B_POLY = [1, 1.5, 0, 0]


def test_kkt_multipliers_example1():
    r = mod.kkt_multipliers_example1()
    assert r["x"] == pytest.approx(0.5, abs=1e-4) and r["y"] == pytest.approx(1.5, abs=1e-4)
    assert r["f"] == pytest.approx(-0.25, abs=1e-5)
    assert r["lambda"] == pytest.approx(0.0, abs=1e-4) and r["mu"] == pytest.approx(1.0, abs=1e-4)


def test_min_variance_portfolio():
    r = mod.min_variance_portfolio(SIGMA)
    w = np.array(r["w"])
    assert abs(w.sum() - 1) < 1e-6 and w.min() >= -1e-6                      # ràng buộc thỏa
    S = np.array(SIGMA)
    ref = minimize(lambda v: v @ S @ v, np.ones(3) / 3, bounds=[(0, 1)] * 3, constraints=[{"type": "eq", "fun": lambda v: v.sum() - 1}], method="SLSQP", options={"ftol": 1e-14})
    assert r["variance"] == pytest.approx(ref.fun, rel=1e-4, abs=1e-8)       # đối chiếu scipy (cách giải khác)
    assert np.allclose(w, ref.x, atol=1e-3)


def test_project_onto_polyhedron_slide3():
    r = mod.project_onto_polyhedron([1, 0.5], A_POLY, B_POLY)
    assert r["x"] == pytest.approx([0.4, 0.3], abs=1e-4)                    # ví dụ slide 3: x* = (0.4, 0.3)
    assert r["distance_sq"] == pytest.approx(0.4, abs=1e-5)


def test_project_inside_point_is_itself():
    r = mod.project_onto_polyhedron([0.1, 0.1], A_POLY, B_POLY)
    assert r["x"] == pytest.approx([0.1, 0.1], abs=1e-5) and r["distance_sq"] == pytest.approx(0.0, abs=1e-8)


def test_nonneg_least_squares():
    rng = np.random.default_rng(7)
    A = rng.normal(size=(8, 4)); b = rng.normal(size=8)
    r = mod.nonneg_least_squares(A.tolist(), b.tolist())
    x_ref, rn = nnls(A, b)                                                  # đối chiếu scipy.optimize.nnls
    assert min(r["x"]) >= -1e-9
    assert np.allclose(r["x"], x_ref, atol=1e-4) and r["residual_sq"] == pytest.approx(rn ** 2, rel=1e-4, abs=1e-8)
