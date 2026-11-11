"""Tính lại ĐỘC LẬP mọi câu IQR / ngoại lai / x̄ / s / s² của M1 và M9 từ dữ liệu trong đề (numpy), so với đáp án đúng."""
import json, re, sys, numpy as np
def nums(s): return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]
def halves(x):
    x = sorted(x); n = len(x); lo = x[:n // 2]; hi = x[(n + 1) // 2:]
    return float(np.median(lo)), float(np.median(x)), float(np.median(hi))
bad = []; chk = collections = 0
for mid in ('m01', 'm09'):
    for it in json.load(open(f'data/qbank/{mid}.json', encoding='utf-8'))['items']:
        q = it['q']; ok = it['opts'][it['correct']].replace('−', '-')
        m = re.search(r'(?:n = \d+(?: giá trị)?[:)]|Dữ liệu \(n = \d+\):)\s*([\d.,\s\-]+?)\.?(?:\n|$)', q)
        if not m: continue
        x = nums(m.group(1))
        if len(x) < 5: continue
        qL, qM, qU = halves(x); R = qU - qL; lo, hi = qL - 1.5 * R, qU + 1.5 * R
        if 'IQR' in q and 'Tính IQR' in q or 'khoảng biến thiên tứ phân vị IQR' in q:
            chk += 1
            try: v = float(ok)
            except ValueError: bad.append((it['id'], 'đáp án không phải số', ok)); continue
            if abs(v - R) > 1e-9 + 0.5 * 10 ** -(len(ok.split('.')[-1]) if '.' in ok else 0): bad.append((it['id'], 'IQR', ok, round(R, 5)))
            elif abs(v - R) > 1e-6: bad.append((it['id'], 'IQR làm tròn thiếu chữ số', ok, round(R, 5)))
        elif 'bao nhiêu giá trị ngoại lai' in q:
            chk += 1; n_out = sum(1 for t in x if t < lo or t > hi)
            if str(n_out) != ok: bad.append((it['id'], 'số ngoại lai', ok, n_out))
        elif 'Tính trung bình mẫu' in q:
            chk += 1
            if abs(float(ok) - np.mean(x)) > 0.0006: bad.append((it['id'], 'x̄', ok, round(float(np.mean(x)), 4)))
        elif 'độ lệch chuẩn mẫu s' in q and 'Tính' in q:
            chk += 1
            if abs(float(ok) - np.std(x, ddof=1)) > 0.0006: bad.append((it['id'], 's', ok, round(float(np.std(x, ddof=1)), 4)))
        elif 'Tính phương sai mẫu' in q:
            chk += 1
            if abs(float(ok) - np.var(x, ddof=1)) > 0.0006: bad.append((it['id'], 's²', ok, round(float(np.var(x, ddof=1)), 4)))
print('đã tính lại', chk, 'câu; lệch', len(bad)); [print(' ', b) for b in bad[:20]]
sys.exit(1 if bad else 0)
