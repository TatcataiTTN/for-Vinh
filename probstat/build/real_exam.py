"""Đề giữa kỳ thật HK2.2 2025–2026 (10 mã đề cùng một mẫu, đổi số) + bộ mã đề mới cùng mẫu.
Mọi đáp số tính bằng SciPy/math.comb và đối chiếu độc lập bằng NumPy; không gõ tay."""
import math, random
import numpy as np
from scipy import stats as st
from qb import f, fg

# (mã đề, α%, nam, nữ, P(A), tỉ lệ bệnh nam, nữ, p₅ trong bảng, μ, σ, cận trên, bậc tự do t, tần số 4 lớp) — đọc từ PDF gốc, đã đối chiếu từng trang
REAL = [
 ('Ak1Bm1Zn5', 7, 11, 20, 0.25, 0.04, 0.12, 0.18, 4.13, 0.13, 4.29, 18, [4, 7, 16, 5]),
 ('Ak2Bm2Zn4', 8, 12, 19, 0.38, 0.05, 0.11, 0.18, 4.14, 0.14, 4.31, 19, [4, 8, 14, 5]),
 ('Ak3Bm3Zn3', 9, 13, 18, 0.5, 0.07, 0.09, 0.18, 4.15, 0.15, 4.33, 20, [4, 9, 12, 5]),
 ('Ak4Bm4Zn2', 10, 14, 17, 0.62, 0.09, 0.07, 0.18, 4.16, 0.16, 4.35, 21, [4, 10, 10, 5]),
 ('Ak5Bm5Zn1', 11, 15, 16, 0.75, 0.11, 0.05, 0.18, 4.17, 0.17, 4.37, 22, [4, 11, 8, 5]),
 ('Ak6Bm6Zn10', 22, 16, 25, 0.39, 0.11, 0.18, 0.15, 4.38, 0.38, 4.84, 43, [4, 22, 36, 5]),
 ('Ak7Bm7Zn9', 23, 17, 24, 0.44, 0.12, 0.17, 0.15, 4.39, 0.39, 4.86, 44, [4, 23, 34, 5]),
 ('Ak8Bm8Zn8', 24, 18, 23, 0.5, 0.14, 0.15, 0.15, 4.4, 0.4, 4.88, 45, [4, 24, 32, 5]),
 ('Ak9Bm9Zn7', 25, 19, 22, 0.56, 0.15, 0.14, 0.15, 4.41, 0.41, 4.9, 46, [4, 25, 30, 5]),
 ('Ak10Bm10Zn6', 26, 20, 21, 0.61, 0.17, 0.12, 0.15, 4.42, 0.42, 4.92, 47, [4, 26, 28, 5]),
]
MIDS = [7, 9, 11, 13]
Phi = st.norm.cdf

def make_new(n=30, seed=2026):
    """Mã đề mới: giữ nguyên khung 9 câu; đổi tham số trong khoảng giống đề thật. 20 đề đầu độ tin cậy 90%, 10 đề cuối 95% và σ khác."""
    rng = random.Random(seed); out = []
    for i in range(n):
        a = rng.randint(5, 30); tot = rng.choice([31, 36, 41, 45]); nm = rng.randint(10, tot - 10)
        pA = rng.choice([x / 100 for x in range(15, 91)])
        pm = round(rng.uniform(0.03, 0.2), 2); pf = round(rng.uniform(0.03, 0.2), 2)
        p3 = rng.choice([0.12, 0.15, 0.18, 0.2])
        sg = round(rng.uniform(0.1, 0.45), 2); mu = round(4 + sg, 2); up = round(mu + sg * rng.uniform(1.1, 1.7), 2)
        df = rng.randint(10, 60)
        fr = [rng.randint(3, 6), rng.randint(5, 30), rng.randint(6, 36), rng.randint(3, 7)]
        out.append(dict(code=f'M{i+1:02d}', real=False, a=a, nm=nm, nu=tot - nm, pA=pA, pm=pm, pf=pf, p3=p3, mu=mu, sg=sg, up=up, df=df, fr=fr,
                        conf=0.90 if i < 20 else 0.95, sig=0.5 if i < 20 else rng.choice([0.4, 0.6, 0.8])))
    return out

def variants():
    V = []
    for c, a, nm, nu, pA, pm, pf, p3, mu, sg, up, df, fr in REAL:
        V.append(dict(code=c, real=True, a=a, nm=nm, nu=nu, pA=pA, pm=pm, pf=pf, p3=p3, mu=mu, sg=sg, up=up, df=df, fr=fr, conf=0.90, sig=0.5))
    return V + make_new()

def solve(v):
    """Trả về dict đáp số + lời giải; có assert đối chiếu độc lập."""
    a = v['a'] / 100
    q1 = float(st.norm.ppf(1 - a))
    q2 = math.comb(v['nm'], 2) * math.comb(v['nu'], 3)
    q3 = 1 - v['pA']; q4 = v['pA'] ** 3
    q5 = 0.55 * v['pm'] + 0.45 * v['pf']
    q6 = 1 - (v['pm'] + v['pf'] + v['p3'])
    z1 = (v['up'] - v['mu']) / v['sg']; z0 = (4.0 - v['mu']) / v['sg']
    q7 = float(Phi(z1) - Phi(z0))
    q8 = float(st.t.ppf(1 - a, v['df']))
    # đối chiếu độc lập
    assert abs(Phi(q1) - (1 - a)) < 1e-12 and abs(st.t.cdf(q8, v['df']) - (1 - a)) < 1e-9
    assert q2 == math.factorial(v['nm']) // (2 * math.factorial(v['nm'] - 2)) * (v['nu'] * (v['nu'] - 1) * (v['nu'] - 2) // 6)
    assert q6 > 0 and 0 < q7 < 1
    assert abs(st.norm(v['mu'], v['sg']).cdf(v['up']) - st.norm(v['mu'], v['sg']).cdf(4.0) - q7) < 1e-12
    fr = v['fr']; n = sum(fr)
    data = np.repeat(MIDS, fr); xb = float(data.mean()); s2 = float(data.var(ddof=1))
    sxm = sum(k * m for k, m in zip(fr, MIDS)); sxm2 = sum(k * m * m for k, m in zip(fr, MIDS))
    assert abs(xb - sxm / n) < 1e-12 and abs(s2 - (sxm2 - n * xb * xb) / (n - 1)) < 1e-9
    s = math.sqrt(s2); al = 1 - v['conf']; u = float(st.norm.ppf(1 - al / 2)); tt = float(st.t.ppf(1 - al / 2, n - 1))
    eb = u * v['sig'] / math.sqrt(n); ec = tt * s / math.sqrt(n)
    lo_t, hi_t = st.t.interval(v['conf'], n - 1, loc=xb, scale=s / math.sqrt(n)); assert abs(lo_t - (xb - ec)) < 1e-9 and abs(hi_t - (xb + ec)) < 1e-9
    return dict(q=[q1, q2, q3, q4, q5, q6, q7, q8], z1=z1, z0=z0, n=n, xb=xb, s2=s2, s=s, u=u, t=tt, eb=eb, ec=ec, sxm=sxm, sxm2=sxm2,
                b=(float(xb - eb), float(xb + eb)), c=(float(xb - ec), float(xb + ec)))

def stems(v):
    a = v['a']; g = lambda x, d=4: fg(x, d)
    pc = int(round(v['conf'] * 100))
    S = [f'Tính giá trị tới hạn U_α với α = {a}%.',
         f'Một lớp học có {v["nm"]} bạn nam và {v["nu"]} bạn nữ. Có bao nhiêu cách chọn một nhóm gồm 2 bạn nam và 3 bạn nữ trong lớp đó?',
         f'Biết rằng P(A) = {g(v["pA"])}. Tính xác suất của biến cố Ā.',
         f'Biết rằng xác suất để một xạ thủ bắn trúng mục tiêu là {g(v["pA"])}. Tính xác suất để xạ thủ đó bắn trúng mục tiêu đúng 3 lần trong 3 lần bắn?',
         f'Biết rằng tỷ lệ mắc bệnh A ở nam và nữ lần lượt là {g(v["pm"])} và {g(v["pf"])}. Một vùng dân cư có tỷ lệ nam và nữ lần lượt là 55% và 45%. Chọn ngẫu nhiên một người ở vùng đó, tính xác suất để người đó mắc bệnh A?',
         f'Cho BNN X có bảng phân bố xác suất: X = 2, 3, 5, 6 với P = {g(v["pm"])}, {g(v["pf"])}, {g(v["p3"])}, k. Giá trị của k bằng bao nhiêu?',
         f'Biết rằng điểm thi môn Toán của sinh viên một trường đại học tuân theo phân bố chuẩn với kỳ vọng μ = {g(v["mu"])} và độ lệch chuẩn σ = {g(v["sg"])}. Chọn ngẫu nhiên 1 sinh viên, tính xác suất để bạn đó có điểm thi môn Toán từ 4.0 đến {g(v["up"])}.',
         f'Tính giá trị tới hạn t_α với α = {a}% của phân bố Student {v["df"]} bậc tự do.']
    fr = v['fr']
    E = (f'Giả sử thời gian điều trị X một loại bệnh A là biến ngẫu nhiên có phân bố chuẩn với độ lệch chuẩn σ (đã biết hoặc chưa biết). Số liệu mẫu: '
         f'X (ngày) 6–8: {fr[0]} bệnh nhân; 8–10: {fr[1]}; 10–12: {fr[2]}; 12–14: {fr[3]}.')
    P = [f'(a) Tính trung bình mẫu x̄ và phương sai mẫu s².',
         f'(b) Với độ tin cậy {pc}%, tìm khoảng ước lượng cho thời gian điều trị trung bình của loại bệnh A, biết rằng σ = {g(v["sig"])} (ngày).',
         f'(c) Với độ tin cậy {pc}%, tìm khoảng ước lượng cho thời gian điều trị trung bình của loại bệnh A (σ chưa biết).']
    return S, E, P

def explains(v, r):
    a = v['a']; pc = int(round(v['conf'] * 100)); q = r['q']
    z1 = r['z1']; z0 = r['z0']
    E = [f'U_α thoả Φ(U_α) = 1 − α (đuôi phải α, không chia đôi). α = {a}% ⇒ Φ(U) = {f(1-a/100,2)} ⇒ U ≈ {f(q[0],3)}.',
         f'Chọn 2 trong {v["nm"]} nam và 3 trong {v["nu"]} nữ: C({v["nm"]},2)·C({v["nu"]},3) = {math.comb(v["nm"],2)}·{math.comb(v["nu"],3)} = {q[1]}.',
         f'P(Ā) = 1 − P(A) = 1 − {fg(v["pA"])} = {f(q[2],4)}.',
         f'Các lần bắn độc lập: P = p³ = {fg(v["pA"])}³ = {f(q[3],4)}.',
         f'Công thức xác suất toàn phần: 0.55·{fg(v["pm"])} + 0.45·{fg(v["pf"])} = {f(0.55*v["pm"],4)} + {f(0.45*v["pf"],4)} = {f(q[4],4)}.',
         f'Tổng xác suất bằng 1: k = 1 − ({fg(v["pm"])} + {fg(v["pf"])} + {fg(v["p3"])}) = {f(q[5],2)}.',
         f'P(4.0 ≤ X ≤ {fg(v["up"])}) = Φ(({fg(v["up"])} − {fg(v["mu"])})/{fg(v["sg"])}) − Φ((4.0 − {fg(v["mu"])})/{fg(v["sg"])}) = Φ({f(z1,3)}) − Φ({f(z0,3)}) = {f(Phi(z1),4)} − {f(Phi(z0),4)} = {f(q[6],4)}.',
         f't_α(n) thoả P(T > t_α) = α, tức F(t_α) = 1 − α = {f(1-a/100,2)} với {v["df"]} bậc tự do ⇒ t_α ≈ {f(q[7],3)} (lớn hơn U_α = {f(q[0],3)} vì đuôi t dày hơn).']
    return E

def essay_html(v, r):
    fr = v['fr']; n = r['n']; pc = int(round(v['conf'] * 100)); al = 1 - v['conf']
    rows = ''.join(f'<tr><td>{lab}</td><td>{k}</td><td>{m}</td><td>{k*m}</td><td>{k*m*m}</td></tr>' for lab, k, m in zip(['6–8', '8–10', '10–12', '12–14'], fr, MIDS))
    rows += f'<tr><td><b>Tổng</b></td><td><b>{n}</b></td><td></td><td><b>{r["sxm"]}</b></td><td><b>{r["sxm2"]}</b></td></tr>'
    h = (f'<p><b>(a)</b> Dùng trung điểm lớp (7, 9, 11, 13):</p><table class="t"><tr><th>Lớp</th><th>f</th><th>m</th><th>f·m</th><th>f·m²</th></tr>{rows}</table>'
         f'<p>x̄ = {r["sxm"]}/{n} = <b>{f(r["xb"],4)}</b>. s² = (Σf·m² − n·x̄²)/(n − 1) = ({r["sxm2"]} − {n}·{f(r["xb"],4)}²)/{n-1} = <b>{f(r["s2"],4)}</b> (s = {f(r["s"],4)}). Chú ý chia cho n − 1.</p>'
         f'<p><b>(b)</b> σ đã biết ⇒ dùng U: giá trị tới hạn U<sub>{fg(al/2,3)}</sub> = {f(r["u"],3)}. Sai số e = U·σ/√n = {f(r["u"],3)}·{fg(v["sig"])}/√{n} = {f(r["eb"],4)}. '
         f'Khoảng tin cậy {pc}%: x̄ ± e = <b>({f(r["b"][0],3)}; {f(r["b"][1],3)})</b>.</p>'
         f'<p><b>(c)</b> σ chưa biết ⇒ thay σ bằng s và dùng Student {n-1} bậc tự do: t<sub>{fg(al/2,3)}</sub>({n-1}) = {f(r["t"],3)}. e = t·s/√n = {f(r["t"],3)}·{f(r["s"],4)}/√{n} = {f(r["ec"],4)}. '
         f'Khoảng tin cậy {pc}%: <b>({f(r["c"][0],3)}; {f(r["c"][1],3)})</b>.</p>'
         f'<p>Bẫy: ở (c) không dùng σ = {fg(v["sig"])} của câu (b); mức tới hạn là α/2 = {fg(al/2,3)} (hai phía) khác với câu 1 và 8 (đuôi phải α).</p>')
    return h

def payload():
    """Dữ liệu cho trang: mỗi mã đề đủ đề, đáp số, giải thích, lời giải tự luận."""
    out = []
    for v in variants():
        r = solve(v); S, E, P = stems(v); ex = explains(v, r)
        tol = [0.01, 0, 0.0005, 0.0005, 0.0005, 0.0005, 0.005, 0.01]
        out.append(dict(code=v['code'], real=v['real'], stems=S, ans=[round(x, 6) for x in r['q']], tol=tol, expl=ex, essay=E, parts=P,
                        eans=dict(xb=round(r['xb'], 6), s2=round(r['s2'], 6), b=[round(x, 6) for x in r['b']], c=[round(x, 6) for x in r['c']]),
                        etol=dict(xb=0.005, s2=0.01, b=0.01, c=0.02), esol=essay_html(v, r), n=r['n'], conf=int(round(v['conf'] * 100))))
    return out

if __name__ == '__main__':
    P = payload(); print(len(P), 'mã đề'); p = P[0]
    print(p['ans'], p['eans']); print(p['stems'][0], p['stems'][7]); print(p['expl'][0]); print(p['expl'][6])
    for x in P[:10]: print(x['code'], [round(a, 4) for a in x['ans']], x['n'])

def build_page():
    import json, html as _h
    from sitelib import page, write
    from hx import callout, ul, table
    P = payload()
    data = json.dumps(P, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    struct = table(['Câu', 'Dạng', 'Module', 'Công thức cần nhớ', 'Bẫy hay gặp'], [
        ['1', 'Giá trị tới hạn \\(U_\\alpha\\)', '<a href="../m08-khoang-tin-cay/index.html">M8</a>', '\\(\\Phi(U_\\alpha)=1-\\alpha\\)', 'Chia đôi α (đó là \\(U_{\\alpha/2}\\) của khoảng tin cậy, không phải câu này)'],
        ['2', 'Chọn nhóm 2 nam 3 nữ', '<a href="../m02-phep-thu-su-kien-dem/index.html">M2</a>', '\\(C_m^2\\cdot C_n^3\\)', 'Dùng chỉnh hợp, hoặc \\(C_{m+n}^5\\), hoặc cộng thay vì nhân'],
        ['3', 'Biến cố đối', '<a href="../m03-xac-suat-dieu-kien-doc-lap/index.html">M3</a>', '\\(P(\\bar A)=1-P(A)\\)', 'Đọc nhầm số'],
        ['4', 'Bắn trúng đúng 3 lần trong 3 lần', '<a href="../m03-xac-suat-dieu-kien-doc-lap/index.html">M3</a>', '\\(p^3\\) (độc lập)', 'Nhân nhầm thành \\(3p\\) hoặc dùng \\(1-(1-p)^3\\)'],
        ['5', 'Xác suất toàn phần theo giới tính', '<a href="../m04-toan-phan-bayes/index.html">M4</a>', '\\(0.55\\,p_{nam}+0.45\\,p_{nữ}\\)', 'Đảo trọng số nam và nữ'],
        ['6', 'Tìm k trong bảng phân bố', '<a href="../m05-bien-ngau-nhien/index.html">M5</a>', '\\(\\sum p_i=1\\)', 'Bỏ sót một xác suất khi cộng'],
        ['7', 'Xác suất chuẩn trong khoảng [4.0; b]', '<a href="../m06-nhi-thuc-poisson-chuan/index.html">M6</a>', '\\(\\Phi(\\tfrac{b-\\mu}{\\sigma})-\\Phi(\\tfrac{4-\\mu}{\\sigma})\\)', 'Quên trừ, hoặc chia cho σ² thay vì σ'],
        ['8', 'Giá trị tới hạn \\(t_\\alpha\\) Student', '<a href="../m08-khoang-tin-cay/index.html">M8</a>', '\\(F(t_\\alpha)=1-\\alpha\\), bậc tự do đã cho', 'Dùng bảng chuẩn thay vì Student, hoặc lấy sai hàng bậc tự do'],
        ['9a', 'x̄, s² từ bảng ghép lớp', '<a href="../m01-bieu-dien-du-lieu/index.html">M1</a>, <a href="../m07-mau-uoc-luong-diem/index.html">M7</a>', 'trung điểm lớp; \\(s^2=\\tfrac{\\sum f m^2-n\\bar x^2}{n-1}\\)', 'Chia cho n thay vì n − 1'],
        ['9b', 'Khoảng tin cậy, σ đã biết', '<a href="../m08-khoang-tin-cay/index.html">M8</a>', '\\(\\bar x\\pm U_{\\alpha/2}\\sigma/\\sqrt n\\)', 'Dùng t thay cho U'],
        ['9c', 'Khoảng tin cậy, σ chưa biết', '<a href="../m08-khoang-tin-cay/index.html">M8</a>', '\\(\\bar x\\pm t_{\\alpha/2}(n-1)\\,s/\\sqrt n\\)', 'Dùng σ của câu (b), hoặc bậc tự do n thay vì n − 1']], 'left')
    ans = ''.join('<tr><td>' + p['code'] + '</td>' + ''.join(f'<td>{(str(a) if isinstance(a, int) else f(a, 4))}</td>' for a in p['ans']) +
                  f'<td>{f(p["eans"]["xb"],3)}</td><td>{f(p["eans"]["s2"],3)}</td></tr>' for p in P if p['real'])
    ansT = '<div style="overflow:auto"><table class="t"><tr><th>Mã đề</th><th>C1</th><th>C2</th><th>C3</th><th>C4</th><th>C5</th><th>C6</th><th>C7</th><th>C8</th><th>x̄</th><th>s²</th></tr>' + ans + '</table></div>'
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › <a href="../kho-de/index.html">Kho đề</a> › Đề giữa kỳ thật HK2.2</div>
<h1>Đề giữa kỳ thật HK2.2 2025–2026: 10 mã đề và luyện tập</h1>
<p class="lead">Tài liệu mới nhất: 10 mã đề giữa kỳ của học kỳ này (Ak1Bm1Zn5 … Ak10Bm10Zn6). Các mã đề <b>cùng một khung 9 câu</b>, chỉ đổi số liệu, nên học một mã đề tức là học cả mười. Trang này cho phép điền đáp số, chấm ngay có giải thích, làm câu 9 có lời giải từng bước, và thêm 30 mã đề mới cùng mẫu (đổi số liệu; 10 mã cuối đổi độ tin cậy 95% và σ).</p>
{callout('good', 'Khung đề (đúng như PDF)', ul(['Thời gian 60 phút. Câu 1–8 điền đáp số, mỗi câu 0,5 điểm. Câu 9 tự luận 6 điểm.', 'Phạm vi: Chương 1 và ước lượng khoảng (mục 1.1 đến 2.3), tức Module 1–8.', 'Tất cả đáp số dưới đây do chương trình tính bằng SciPy và đối chiếu độc lập; quy ước giá trị tới hạn theo giáo trình: \\(\\Phi(U_\\alpha)=1-\\alpha\\), \\(F(t_\\alpha)=1-\\alpha\\).']))}
<h2>Chín dạng câu, công thức và bẫy</h2><div style="overflow:auto">{struct}</div>
<h2>Luyện tập (điền đáp số, chấm ngay)</h2>
<p>Chọn mã đề, làm, bấm <b>Chấm bài</b>. Đáp số nhập dấu chấm hoặc dấu phẩy đều được; sai số cho phép nhỏ để chấp nhận đáp số tra bảng làm tròn. Điểm cao nhất mỗi mã đề được nhớ trong trình duyệt của bạn. <b>Lưu ý:</b> đáp số nằm trong mã nguồn của trang, nên đây là trang tự học, không dùng để thi lấy điểm.</p>
<div id="realexam" class="rx"></div><script type="application/json" id="realexam-data">{data}</script>
<h2>Bảng đáp số 10 mã đề thật</h2><details><summary>Mở bảng đáp số (nên làm trước rồi mới đối chiếu)</summary>{ansT}</details>
<h2>Gợi ý học theo bảng điểm lần 1</h2>{callout('warn', 'Đúng điểm yếu đã chấm', ul(['Câu 9 là 6/10 điểm và bài làm lần 1 bỏ trống phần tự luận: làm câu 9 trước, bấm giờ 20 phút.', 'Phương sai mẫu s²: nhớ chia n − 1, lập bảng f, m, f·m, f·m².', 'Phần còn lại: <a href="../bai-mau-tu-luan/index.html">bài mẫu tự luận</a>, <a href="../m08-khoang-tin-cay/index.html">Module 8</a> (khoảng tin cậy) và <a href="../bang-tra/index.html">bảng tra</a>.']))}
<p style="font-size:.85rem;color:var(--muted)">Nguồn: file “LTXSTK_HK2.2_20252026_alltests.pdf” (10 trang, 10 mã đề); mẫu đề này trùng với đề giữa kỳ mẫu trong thư mục 02. Mã đề mới do người biên soạn tạo, không phải đề chính thức.</p>'''
    write('vi/de-thi-that-hk22/index.html', page('Đề giữa kỳ thật HK2.2 2025–2026', body, 2, '10 mã đề giữa kỳ thật cùng mẫu và 30 mã đề mới, chấm tự động', scripts=['realexam.js']))
    print('de-thi-that ok', len(P), 'mã đề')
