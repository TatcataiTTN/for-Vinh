"""Kiểm tra ĐỘC LẬP trang đề thật HK2.2: (1) tham số 10 mã đề = nội dung PDF gốc (đọc lại bằng pdftotext); (2) đáp số trên trang tính lại bằng cách khác
(math.erf, tích phân số mật độ chuẩn và Student viết tay, statistics) chứ không dùng lại SciPy.stats của mã sinh.
Dùng: python3 tests/verify_realexam.py <đường dẫn PDF>"""
import re, json, math, statistics, subprocess, sys, html
from scipy.integrate import quad
pdf = sys.argv[1]
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
pages = [p for p in txt.split('\f') if p.strip()]
page_html = open('vi/de-thi-that-hk22/index.html', encoding='utf-8').read()
D = json.loads(html.unescape(re.search(r'<script type="application/json" id="realexam-data">(.*?)</script>', page_html, re.S).group(1)).replace('<\\/', '</'))
bad = []; n = 0
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
def phi_inv(p):
    lo, hi = -10, 10
    for _ in range(200):
        m = (lo + hi) / 2
        if Phi(m) < p: lo = m
        else: hi = m
    return (lo + hi) / 2
def tpdf(x, v): return math.exp(math.lgamma((v + 1) / 2) - math.lgamma(v / 2)) / math.sqrt(v * math.pi) * (1 + x * x / v) ** (-(v + 1) / 2)
def tcdf(x, v): return 0.5 + (quad(lambda t: tpdf(t, v), 0, x)[0] if x >= 0 else -quad(lambda t: tpdf(t, v), x, 0)[0])
def tq(p, v):
    lo, hi = 0.0, 50.0
    for _ in range(80):
        m = (lo + hi) / 2
        if tcdf(m, v) < p: lo = m
        else: hi = m
    return (lo + hi) / 2
for k, pg in enumerate(pages):
    code = re.search(r'Mã đề: (\S+)', pg)[1]; d = D[k]
    assert d['code'] == code and d['real'], (d['code'], code)
    a = int(re.search(r'Uα với α = (\d+)%', pg)[1]); nm, nu = map(int, re.search(r'có (\d+) bạn nam và (\d+) bạn nữ', pg).groups())
    pA = float(re.search(r'P \(A\) = (0\.\d+)', pg)[1]); pm, pf = map(float, re.search(r'lần lượt là ([\d.]+) và ([\d.]+)\. Một', pg).groups())
    row = re.search(r'P\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+k', pg).groups(); mu, sg = map(float, re.search(r'µ = ([\d.]+) và độ lệch chuẩn σ = (0\.\d+)', pg).groups())
    up = float(re.search(r'từ 4\.0 đến (\d\.\d+)', pg)[1]); df = int(re.search(r'Student (\d+) bậc tự do', pg)[1]); fr = list(map(int, re.search(r'Số bệnh nhân\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', pg).groups()))
    # (1) tham số trong mã đề trên trang = PDF
    s = ' '.join(d['stems']) + ' ' + d['essay']
    for lab, v in [('α', a), ('nam', nm), ('nữ', nu), ('P(A)', pA), ('bệnh nam', pm), ('bệnh nữ', pf), ('p₅', float(row[2])), ('μ', mu), ('σ', sg), ('cận trên', up), ('df', df)]:
        n += 1
        if not re.search(r'(?<![\d.])' + re.escape(f'{v:g}') + r'(?![\d])', s): bad.append((code, 'tham số không thấy trên trang', lab, v))
    for i, t in enumerate(fr):
        n += 1
        if not re.search(r'(?<![\d.])' + str(t) + r'(?![\d])', d['essay']): bad.append((code, 'tần số lớp', i, t))
    # (2) đáp số tính lại bằng cách khác
    ex = [phi_inv(1 - a / 100), math.comb(nm, 2) * math.comb(nu, 3), 1 - pA, pA ** 3, 0.55 * pm + 0.45 * pf, 1 - (pm + pf + float(row[2])),
          Phi((up - mu) / sg) - Phi((4.0 - mu) / sg), tq(1 - a / 100, df)]
    for i, (e, got) in enumerate(zip(ex, d['ans'])):
        n += 1
        if abs(e - got) > 2e-5 * max(1, abs(e)): bad.append((code, f'câu {i+1}', got, e))
    data = [x for x, k in zip([7, 9, 11, 13], fr) for _ in range(k)]; N_ = len(data); xb = statistics.fmean(data); s2 = statistics.variance(data); s = math.sqrt(s2)
    u = phi_inv(0.95); t = tq(0.95, N_ - 1)
    exp = dict(xb=xb, s2=s2, b=[xb - u * 0.5 / math.sqrt(N_), xb + u * 0.5 / math.sqrt(N_)], c=[xb - t * s / math.sqrt(N_), xb + t * s / math.sqrt(N_)])
    for key in ('xb', 's2'):
        n += 1
        if abs(exp[key] - d['eans'][key]) > 2e-5: bad.append((code, key, d['eans'][key], exp[key]))
    for key in ('b', 'c'):
        for j in (0, 1):
            n += 1
            if abs(exp[key][j] - d['eans'][key][j]) > 2e-4: bad.append((code, key, j, d['eans'][key][j], exp[key][j]))
print('mã đề thật trong PDF:', len(pages), '| mã đề trên trang:', len(D), '(10 thật + 30 mới) | phép so sánh:', n)
print('LỆCH:', len(bad)); [print(' ', b) for b in bad[:20]]
# (3) 30 mã đề mới: đọc tham số từ chính đề hiển thị trên trang rồi tính lại bằng cách khác
bad2 = []; n2 = 0
for d in D[10:]:
    S = d['stems']; E = d['essay']; P = ' '.join(d['parts'])
    a = int(re.search(r'α = (\d+)%', S[0])[1]); nm, nu = map(int, re.search(r'có (\d+) bạn nam và (\d+) bạn nữ', S[1]).groups()); pA = float(re.search(r'P\(A\) = (\d+(?:\.\d+)?)', S[2])[1])
    pm, pf = map(float, re.search(r'lần lượt là (\d+(?:\.\d+)?) và (\d+(?:\.\d+)?)', S[4]).groups()); p5 = float(re.search(r'P = [\d.]+, [\d.]+, (\d+(?:\.\d+)?), k', S[5])[1])
    mu, sg, up = map(float, re.search(r'μ = (\d+(?:\.\d+)?) và độ lệch chuẩn σ = (\d+(?:\.\d+)?)\..*đến (\d+(?:\.\d+)?)\.', S[6]).groups()); df = int(re.search(r'Student (\d+) bậc', S[7])[1])
    fr = list(map(int, re.findall(r': (\d+) bệnh nhân|; \d+–\d+: (\d+)', E)[0][:1] + [x[1] for x in re.findall(r': (\d+) bệnh nhân|; \d+–\d+: (\d+)', E)[1:]])) if False else list(map(int, re.findall(r'(?:6–8|8–10|10–12|12–14): (\d+)', E)))
    conf = int(re.search(r'độ tin cậy (\d+)%', P)[1]) / 100; sig = float(re.search(r'σ = (\d+(?:\.\d+)?) \(ngày\)', P)[1])
    ex = [phi_inv(1 - a / 100), math.comb(nm, 2) * math.comb(nu, 3), 1 - pA, pA ** 3, 0.55 * pm + 0.45 * pf, 1 - (pm + pf + p5), Phi((up - mu) / sg) - Phi((4.0 - mu) / sg), tq(1 - a / 100, df)]
    for i, (e, g) in enumerate(zip(ex, d['ans'])):
        n2 += 1
        if abs(e - g) > 2e-5 * max(1, abs(e)): bad2.append((d['code'], f'câu {i+1}', g, e))
    data = [x for x, k in zip([7, 9, 11, 13], fr) for _ in range(k)]; N_ = len(data); xb = statistics.fmean(data); s2 = statistics.variance(data); s = math.sqrt(s2)
    u = phi_inv(1 - (1 - conf) / 2); t = tq(1 - (1 - conf) / 2, N_ - 1)
    for key, got, e in [('x̄', d['eans']['xb'], xb), ('s²', d['eans']['s2'], s2), ('b0', d['eans']['b'][0], xb - u * sig / math.sqrt(N_)), ('b1', d['eans']['b'][1], xb + u * sig / math.sqrt(N_)), ('c0', d['eans']['c'][0], xb - t * s / math.sqrt(N_)), ('c1', d['eans']['c'][1], xb + t * s / math.sqrt(N_))]:
        n2 += 1
        if abs(e - got) > 2e-4: bad2.append((d['code'], key, got, e))
print('30 mã đề mới: phép so sánh', n2, '| LỆCH', len(bad2)); [print(' ', b) for b in bad2[:10]]
sys.exit(1 if (bad or bad2) else 0)
