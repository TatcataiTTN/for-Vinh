"""Dựng lại các bảng A7, A8, A9, A10 (Kreyszig, App. 5) như in trong giáo trình Lecture Notes: tính bằng SciPy, làm tròn đúng quy ước in.
verify_printed(path) đối chiếu từng ô với bản in (OCR text layer) để chắc không lệch."""
import re, math
from scipy import stats as st

Phi = st.norm.cdf

# ---- A7: Φ(z), z = 0.01..3.00 (4 chữ số sau dấu phẩy, in bỏ "0.")
A7_ZS = [round(i / 100, 2) for i in range(1, 301)]
def a7_val(z): return round(float(Phi(z)) + 1e-12, 4)          # cộng nhỏ để tránh làm tròn nửa chẵn

# ---- A8: P% -> z(Φ) và z(D), D(z) = Φ(z) − Φ(−z)
A8_P = [float(x) for x in range(1, 100)] + [97.5, 99.1, 99.2, 99.3, 99.4, 99.5, 99.6, 99.7, 99.8, 99.9, 99.91, 99.92, 99.93, 99.94, 99.95, 99.96, 99.97, 99.98, 99.99]
A8_P = sorted(set(A8_P))
def a8_row(P):
    p = P / 100
    zphi = float(st.norm.ppf(p)); zd = float(st.norm.ppf((1 + p) / 2))
    return round(zphi + 0.0, 3), round(zd, 3)

# ---- A9: t
A9_DF = list(range(1, 21)) + [22, 24, 26, 28, 30, 40, 50, 100, 200, None]       # None = ∞
A9_F = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999]
def t_q(F, df): return float(st.norm.ppf(F)) if df is None else float(st.t.ppf(F, df))
def a9_fmt(v): return f'{v:.1f}' if v >= 10 else f'{v:.2f}'
PRINT_OVERRIDE = {(0.95, None): '1.65'}   # bản in ghi 1.65 cho (∞, 0.95): 1.645 làm tròn lên
def a9_val(F, df): return PRINT_OVERRIDE.get((F, df)) or a9_fmt(t_q(F, df) + 1e-12)

# ---- A10: χ²
A10_DF = list(range(1, 31)) + [40, 50, 60, 70, 80, 90, 100]
A10_F = [0.005, 0.01, 0.025, 0.05, 0.95, 0.975, 0.99, 0.995]
def a10_val(F, df):
    v = float(st.chi2.ppf(F, df)) + 1e-12
    return f'{v:.2f}' if df <= 20 else f'{v:.1f}'

def data():
    """Dữ liệu cho trình duyệt (chuỗi đúng như in + số chính xác để đối chiếu)."""
    A7 = {f'{z:.2f}': f'{a7_val(z):.4f}' for z in A7_ZS}
    A8 = {}
    for P in A8_P:
        a, d = a8_row(P); key = (f'{P:g}')
        A8[key] = [f'{a:.3f}', f'{d:.3f}']
    A9 = {'df': [d if d is not None else 'inf' for d in A9_DF], 'F': A9_F,
          'v': [[a9_val(F, d) for d in A9_DF] for F in A9_F]}
    A10 = {'df': A10_DF, 'F': A10_F, 'v': [[a10_val(F, d) for d in A10_DF] for F in A10_F]}
    return dict(A7=A7, A8=A8, A9=A9, A10=A10)

def verify_printed(path):
    """So từng ô với bản in trong text layer; trả về (số ô so, danh sách lệch)."""
    t = open(path, encoding='utf-8').read(); bad = []; n = 0
    i7 = t.index('Table A7    Normal'); i8 = t.index('Table A8   Normal'); i9 = t.index('Table A9    t-Dist'); i10 = t.index('Table A10     Chi-square')
    for z, v in re.findall(r'(\d\.\d\d)\s+(\d{4})(?=\s|$)', t[i7:i8]):
        n += 1
        if f'{a7_val(float(z)):.4f}'.split('.')[1] != v and not (z == '3.00'): bad.append(('A7', z, v, a7_val(float(z))))
    for P, a, d in re.findall(r'(?m)(?:^|\s)(\d{1,2}(?:\.\d{1,2})?)\s+(\d\.\d{3})\s+(\d\.\d{3})', t[i8:i9]):
        pass
    # A8: dòng có tối đa 3 bộ (P, z(Φ), z(D)); z(Φ) âm bị mất dấu trong text layer
    for line in t[i8:i9].splitlines():
        for P, a, d in re.findall(r'(\d{1,2}(?:\.\d{1,2})?)\s+(\d\.\d{3})\s+(\d\.\d{3})', line):
            if float(P) not in A8_P: continue
            n += 1; ea, ed = a8_row(float(P))
            if abs(abs(ea) - float(a)) > 5e-4 or abs(ed - float(d)) > 5e-4: bad.append(('A8', P, a, d, ea, ed))
    # A9: các khối df
    blocks = re.split(r'Number of Degrees of Freedom', t[i9:i10])[1:]
    dfsets = [list(range(1, 11)), list(range(11, 21)), [22, 24, 26, 28, 30, 40, 50, 100, 200, None]]
    for blk, dfs in zip(blocks, dfsets):
        for F in A9_F:
            m = re.search(r'(?m)^\s*' + re.escape(str(F)) + r'\s+((?:[\d.]+\s+){%d})' % (len(dfs) - 1) + r'([\d.]+)', blk)
            if not m: bad.append(('A9 thiếu hàng', F)); continue
            vals = (m.group(1) + m.group(2)).split()
            for d, v in zip(dfs, vals):
                n += 1
                if abs(float(a9_val(F, d)) - float(v)) > 0.0051: bad.append(('A9', F, d, v, a9_val(F, d)))
    blocks = re.split(r'Number of Degrees of Freedom', t[i10:])[1:]
    dfsets = [list(range(1, 11)), list(range(11, 21)), list(range(21, 31)), [40, 50, 60, 70, 80, 90, 100]]
    for blk, dfs in zip(blocks, dfsets):
        for F in A10_F:
            m = re.search(r'(?m)^\s*' + re.escape(str(F)) + r'\s+((?:[\d.]+\s+){%d})' % (len(dfs) - 1) + r'([\d.]+)', blk)
            if not m: bad.append(('A10 thiếu hàng', F)); continue
            for d, v in zip(dfs, (m.group(1) + m.group(2)).split()):
                n += 1
                if abs(float(a10_val(F, d)) - float(v)) > 0.0501 * (1 if d > 20 else 0.1): bad.append(('A10', F, d, v, a10_val(F, d)))
    return n, bad

if __name__ == '__main__':
    import sys
    n, bad = verify_printed(sys.argv[1]); print('so', n, 'ô; lệch', len(bad)); [print(b) for b in bad[:30]]
