"""Công cụ thống kê dùng chung (kiểm chứng độc lập: tự cài + đối chiếu numpy/scipy)."""
import math, statistics
import numpy as np
from scipy import stats as st

def mean(x): return sum(x) / len(x)
def median(x):
    s = sorted(x); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
def quartiles(x):
    """Quy ước giáo trình/Kreyszig: qL, qU = trung vị nửa dưới / nửa trên (loại qM khi n lẻ)."""
    s = sorted(x); n = len(s)
    lo = s[:n // 2]; hi = s[(n + 1) // 2:]
    return median(lo), median(s), median(hi)
def var_s(x):
    m = mean(x); return sum((v - m) ** 2 for v in x) / (len(x) - 1)
def var_p(x):
    m = mean(x); return sum((v - m) ** 2 for v in x) / len(x)
def sd_s(x): return math.sqrt(var_s(x))
def iqr(x):
    a, b, c = quartiles(x); return c - a
def outliers(x):
    a, b, c = quartiles(x); r = c - a
    return [v for v in sorted(x) if v < a - 1.5 * r or v > c + 1.5 * r]
def mode(x):
    c = {}
    for v in x: c[v] = c.get(v, 0) + 1
    m = max(c.values()); return sorted(k for k, v in c.items() if v == m), m

def check_basic(x):
    """Đối chiếu với numpy/statistics: bắt lỗi cài đặt."""
    assert abs(mean(x) - float(np.mean(x))) < 1e-9
    assert abs(median(x) - float(np.median(x))) < 1e-9
    assert abs(var_s(x) - float(np.var(x, ddof=1))) < 1e-9
    assert abs(var_p(x) - float(np.var(x))) < 1e-9
    return True

# ---- phân phối: giá trị bảng A7 (Φ), A8 (z), A9 (t) ----
Phi = st.norm.cdf
def zq(p): return st.norm.ppf(p)               # P(Z <= z) = p
def U(alpha): return st.norm.ppf(1 - alpha)    # giá trị tới hạn U_alpha: P(Z > U_a) = alpha
def T(alpha, df): return st.t.ppf(1 - alpha, df)   # t_alpha(df)
def C2(alpha, df): return st.chi2.ppf(1 - alpha, df)  # chi2_alpha(df): P(chi2 > c) = alpha
def r4(x): return round(x + 0.0, 4)
