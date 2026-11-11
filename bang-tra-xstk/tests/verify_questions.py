"""Kiểm tra ĐỘC LẬP 240 câu luyện: đọc đề (regex) rồi tính lại bằng SciPy, so với đáp số lưu trong data.js (đáp số đọc từ bảng, chỉ được lệch do làm tròn của bảng)."""
import re, json, sys
from scipy import stats as st
src = open('assets/data.js', encoding='utf-8').read()
Q = json.loads(re.search(r'window\.QUESTIONS=(.*);$', src, re.S).group(1))
Phi = st.norm.cdf
def num(s): return float(s.replace('−', '-'))
bad = []; kinds = {}
def chk(q, exact, tol, kind):
    kinds[kind] = kinds.get(kind, 0) + 1
    if abs(q['a'] - exact) > tol: bad.append((kind, q['id'], q['q'][:70], q['a'], round(exact, 5), tol))
for q in Q:
    s = q['q']; m = None
    if m := re.match(r'Tra bảng A7: Φ\(([\d.]+)\)', s): chk(q, Phi(num(m[1])), 5.1e-5, 'A7 Φ(z)')
    elif m := re.match(r'Tra bảng A7: Φ\(−([\d.]+)\)', s): chk(q, Phi(-num(m[1])), 5.1e-5, 'A7 Φ(−z)')
    elif m := re.match(r'Cho Z ~ N\(0, 1\)\. Tính P\(([−\d.]+) < Z < ([−\d.]+)\)', s): chk(q, Phi(num(m[2])) - Phi(num(m[1])), 1.1e-4, 'A7 P(a<Z<b)')
    elif m := re.match(r'X ~ N\(([\d.]+); ([\d.]+)²\)\. Tính P\(([−\d.]+) < X < ([−\d.]+)\)', s):
        mu, sg, lo, hi = [num(x) for x in m.groups()]; z1, z2 = round((lo - mu) / sg, 2), round((hi - mu) / sg, 2)
        chk(q, Phi(z2) - Phi(z1), 1.1e-4, 'A7 chuẩn hóa N(μ,σ²)')
        chk(q, Phi((hi - mu) / sg) - Phi((lo - mu) / sg), 0.006, 'A7 N(μ,σ²) so với không làm tròn z')
    elif m := re.match(r'Tra bảng A8: giá trị tới hạn U_α với α = (\d+)%', s): chk(q, st.norm.ppf(1 - num(m[1]) / 100), 5.1e-4, 'A8 U_α')
    elif m := re.match(r'Tìm z sao cho Φ\(z\) = (\d+)%', s): chk(q, st.norm.ppf(num(m[1]) / 100), 5.1e-4, 'A8 z(Φ)')
    elif m := re.match(r'Tìm z > 0 sao cho P\(\|Z\| < z\) = (\d+)%', s): chk(q, st.norm.ppf((1 + num(m[1]) / 100) / 2), 5.1e-4, 'A8 z(D)')
    elif m := re.match(r'Tra bảng A9: .* (\d+) bậc tự do ứng với F\(z\) = (\d(?:\.\d+)?)', s): chk(q, st.t.ppf(num(m[2]), int(m[1])), 0.0051 if st.t.ppf(num(m[2]), int(m[1])) < 10 else 0.051, 'A9 đọc')
    elif m := re.match(r'Khoảng tin cậy (\d+)% cho μ \(σ chưa biết\) từ mẫu cỡ n = (\d+)', s): chk(q, st.t.ppf((1 + num(m[1]) / 100) / 2, int(m[2]) - 1), 0.0051 if q['a'] < 10 else 0.051, 'A9 γ → t')
    elif m := re.match(r'Tìm giá trị tới hạn t_α với α = ([\d.]+)% của phân bố Student (\d+)', s): chk(q, st.t.ppf(1 - num(m[1]) / 100, int(m[2])), 0.0051 if st.t.ppf(1 - num(m[1]) / 100, int(m[2])) < 10 else 0.051, 'A9 t_α')
    elif m := re.match(r'Student (\d+) bậc tự do, F\(z\) = ([\d.]+)\. Bảng A9 không có', s): chk(q, st.t.ppf(num(m[2]), int(m[1])), 1e-5, 'A9 nội suy (đáp số chính xác)')
    elif m := re.match(r'Tra bảng A10 \(χ²\): với (\d+) bậc tự do, giá trị x ứng với F = (\d(?:\.\d+)?)', s): chk(q, st.chi2.ppf(num(m[2]), int(m[1])), 0.0051 if int(m[1]) <= 20 else 0.051, 'A10 đọc')
    else: bad.append(('KHÔNG NHẬN DẠNG ĐƯỢC', q['id'], s[:80], q['a'], None, None))
print('đã kiểm', sum(kinds.values()), 'phép so sánh trên', len(Q), 'câu'); [print(' ', k, v) for k, v in sorted(kinds.items())]
print('LỆCH:', len(bad)); [print(' ', b) for b in bad[:20]]
# đáp số trùng lặp / dung sai hợp lý
ids = [q['id'] for q in Q]; print('id duy nhất:', len(set(ids)) == len(ids), '| câu trùng đề:', len(Q) - len({q['q'] for q in Q}))
sys.exit(1 if bad else 0)
