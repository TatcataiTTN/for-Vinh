"""Trích số IN trong giáo trình (text layer của PDF) thành tests/printed.json: nguồn ĐỘC LẬP với build/tables.py (không tính gì, chỉ chép số in).
Dùng: python3 tests/gen_printed.py <đường dẫn LN_layout.txt>"""
import re, json, sys
t = open(sys.argv[1], encoding='utf-8').read()
i7 = t.index('Table A7    Normal'); i8 = t.index('Table A8   Normal'); i9 = t.index('Table A9    t-Dist'); i10 = t.index('Table A10     Chi-square')
A7 = {z: v for z, v in re.findall(r'(\d\.\d\d)\s+(\d{4})(?=\s|$)', t[i7:i8])}
A8 = {}
for line in t[i8:i9].splitlines():
    for P, a, d in re.findall(r'(\d{1,2}(?:\.\d{1,2})?)\s+(\d\.\d{3})\s+(\d\.\d{3})', line): A8[P] = [a, d]
def grid(txt, Fs, dfsets):
    out = {}
    for blk, dfs in zip(re.split(r'Number of Degrees of Freedom', txt)[1:], dfsets):
        for F in Fs:
            m = re.search(r'(?m)^\s*' + re.escape(str(F)) + r'\s+((?:[\d.]+\s+){%d})([\d.]+)' % (len(dfs) - 1), blk)
            vals = (m.group(1) + m.group(2)).split()
            for d, v in zip(dfs, vals): out[f'{F}|{d}'] = v
    return out
A9 = grid(t[i9:i10], [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999], [list(range(1, 11)), list(range(11, 21)), [22, 24, 26, 28, 30, 40, 50, 100, 200, 'inf']])
A10 = grid(t[i10:], [0.005, 0.01, 0.025, 0.05, 0.95, 0.975, 0.99, 0.995], [list(range(1, 11)), list(range(11, 21)), list(range(21, 31)), [40, 50, 60, 70, 80, 90, 100]])
json.dump(dict(A7=A7, A8=A8, A9=A9, A10=A10), open('tests/printed.json', 'w'), ensure_ascii=False)
print(len(A7), 'A7;', len(A8), 'A8;', len(A9), 'A9;', len(A10), 'A10')
