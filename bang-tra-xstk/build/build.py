"""Dựng site 'Học tra bảng XSTK' (tĩnh) vào thư mục bang-tra-xstk/. Chạy: python3 build/build.py"""
import os, json, math, html, sys
from scipy import stats as st
sys.path.insert(0, os.path.dirname(__file__))
import tables as T, questions as Qm

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
D = T.data(); Phi = st.norm.cdf
def esc(s): return html.escape(str(s), quote=False)
def mn(s): return str(s).replace('-', '−')
def fx(x, d=4): return mn(f'{x:.{d}f}')

NAV = [('Trang chủ', ''), ('Chuẩn tắc A7–A8', 'chuan-tac/'), ('Student A9', 'student/'), ('χ² A10', 'chi-binh-phuong/'), ('Luyện tra bảng', 'luyen-tra/'), ('Đề thật HK2.2', 'de-that/'), ('In bảng', 'in-bang/')]

def page(slug, title, body, desc='', scripts=True):
    depth = slug.count('/') if slug else 0
    r = '../' * depth
    nav = ''.join(f'<a href="{r}{u}index.html" class="{"on" if u == slug else ""}">{t}</a>' for t, u in NAV)
    sc = f'<script src="{r}assets/data.js"></script><script src="{r}assets/app.js"></script>' if scripts else ''
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Học tra bảng XSTK</title><meta name="description" content="{esc(desc)}">
<script>try{{var t=localStorage.getItem('bangtra-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%276%27 fill=%27%23b3122f%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 text-anchor=%27middle%27 fill=%27white%27%3EΦ%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="{r}assets/site.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}index.html">📐 Học tra bảng XSTK</a><nav>{nav}<button id="themebtn" type="button">🌙 Tối</button></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p>Các bảng A7, A8, A9, A10 dựng lại đúng như phụ lục bảng của giáo trình (Kreyszig, <i>Advanced Engineering Mathematics</i>, App. 5, trang A101–A104, đi kèm Lecture Notes XSTK). Mỗi ô được tính bằng SciPy và đối chiếu từng ô với bản in (1014 ô). Trang tự học, dùng cùng site <a href="{r}../probstat/vi/index.html">Lý thuyết xác suất thống kê</a>.</p></div></footer>
{sc}</body></html>'''

def write(rel, content):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(content)
def callout(kind, title, body): return f'<div class="callout {kind}"><b class="t">{title}</b>{body}</div>'
def ex(title, body): return f'<div class="eg"><div class="egh">{title}</div>{body}</div>'
def ol(items): return '<ol class="steps">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
def lk(kind, label): return f'<div class="lk"><div class="lkh">✍ Tra thử · {label}</div><div data-lk="{kind}"></div></div>'
def bell(spec, label=''): return f'<div class="bellbox" data-bell="{spec}" data-label="{label}"></div>'
def table(head, rows, cls=''):
    return f'<div class="scroll"><table class="t {cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table></div>'

# ───────── giá trị theo bảng (để ví dụ khớp tuyệt đối với bảng in)
def a7(z):
    z = round(z, 2)
    if z == 0: return 0.5
    v = float(D['A7'][f'{abs(z):.2f}']); return round(v if z > 0 else 1 - v, 4)
def a8(P, c=0): return float(D['A8'][f'{P:g}'][c])
def a9(F, df): return float(D['A9']['v'][T.A9_F.index(F)][T.A9_DF.index(df)])
def interp9(df, F):
    """Nội suy tuyến tính hai chiều như JS: theo df trước (tại hai hàng F kề), rồi theo F."""
    dfs = [d if d is not None else math.inf for d in T.A9_DF]
    def br(lst, x):
        lo = hi = None
        for v in lst:
            if v == x: return (x, x)
            if v < x: lo = v
            if v > x and hi is None: hi = v
        return (lo, hi)
    fb = br(T.A9_F, F); db = br(dfs, df)
    def cell(f, d): return a9(f, None if d == math.inf else d)
    def col(f):
        if db[0] == db[1]: return cell(f, db[0])
        x1 = 1e9 if db[1] == math.inf else db[1]
        return cell(f, db[0]) + (df - db[0]) / (x1 - db[0]) * (cell(f, db[1]) - cell(f, db[0]))
    v0 = col(fb[0]); v1 = v0 if fb[0] == fb[1] else col(fb[1])
    return v0 if fb[0] == fb[1] else v0 + (F - fb[0]) / (fb[1] - fb[0]) * (v1 - v0)

# ═════════ TRANG CHỦ
def home():
    cards = [('A7', 'Φ(z) và xác suất chuẩn', 'Đọc Φ(1.23), Φ(−0.57), P(a &lt; Z &lt; b), chuẩn hoá X ~ N(μ, σ²).', 'chuan-tac/index.html#a7'),
             ('A8', 'U<sub>α</sub> và tìm z khi biết xác suất', 'Giá trị tới hạn U_α (α = 7% ⇒ hàng 93%), z(Φ), z(D).', 'chuan-tac/index.html#a8'),
             ('A9', 'Student: t<sub>α</sub> và t<sub>α/2</sub>', 'Cột bậc tự do, hàng F; đổi độ tin cậy sang F; nội suy khi không có ô.', 'student/index.html'),
             ('A10', 'χ²', 'Cột bậc tự do, hàng F; công thức khi m &gt; 100.', 'chi-binh-phuong/index.html'),
             ('LUYỆN', '240 câu luyện tra bảng', 'Đáp số đọc từ bảng, tô sáng ô đúng, làm lại được.', 'luyen-tra/index.html'),
             ('ĐỀ THẬT', 'Tra bảng cho 10 mã đề HK2.2', 'Từng câu cần tra gì, ở ô nào, đọc ra bao nhiêu, sai lệch so với máy tính.', 'de-that/index.html'),
             ('IN', 'In bảng A7–A10', 'Bản in gọn để mang theo khi làm bài.', 'in-bang/index.html')]
    cs = ''.join(f'<a class="card" href="{h}"><div class="num">{a}</div><h3>{t}</h3><p>{d}</p></a>' for a, t, d, h in cards)
    z = ''
    body = f'''<h1>Học tra bảng XSTK: chuẩn tắc, Student, χ²</h1>
<p class="lead">Dành cho người chưa hiểu cách đọc các bảng phân phối đi kèm đề thi: bảng chuẩn tắc (A7, A8), bảng Student (A9) và bảng χ² (A10). Mỗi bảng có hướng dẫn từng bước, ô tra thử tô sáng đúng hàng cột và bài luyện.</p>
{callout('good', 'Ba điều cần nhớ trước khi tra', '<ol><li><b>Mọi bảng ở đây cho diện tích bên TRÁI</b>: Φ(z) = P(Z ≤ z) và F(z) = P(T ≤ z). Còn α trong “giá trị tới hạn U<sub>α</sub>, t<sub>α</sub>” là diện tích bên <b>phải</b>, nên phải đổi: <b>F = 1 − α</b>.</li><li><b>Bảng A7 chỉ có z ≥ 0.</b> Với z âm dùng Φ(−z) = 1 − Φ(z).</li><li><b>Bảng A9 thưa</b> (chỉ vài hàng F và vài cột bậc tự do). Khi giá trị cần không có thì <b>nội suy tuyến tính</b> giữa hai ô kề hai bên.</li></ol>')}
<h2>Bạn đang cần tra gì?</h2><div class="grid">{cs}</div>
<h2>Quy trình 4 bước cho mọi lần tra bảng</h2>
{ol(['<b>Đọc kỹ đề</b>: đề hỏi Φ(z), U<sub>α</sub>, t<sub>α</sub>, t<sub>α/2</sub> hay χ²?', '<b>Đổi về F</b>: Φ(z) = F; U<sub>α</sub> ⇒ F = 1 − α; khoảng tin cậy γ ⇒ F = (1 + γ)/2; kiểm định hai phía ⇒ F = 1 − α/2.', '<b>Chọn bảng và tra</b>: A7 (biết z, tìm Φ), A8 (biết xác suất, tìm z), A9 (Student: cột = bậc tự do, hàng = F), A10 (χ²).', '<b>Kiểm tra hợp lý</b>: U<sub>0.05</sub> = 1.645; U<sub>0.025</sub> = 1.96; t luôn lớn hơn U cùng mức; Φ(z) &gt; 0.5 khi z &gt; 0.'])}
<h2>Đề hỏi gì thì tra bảng nào</h2>
{table(['Câu trong đề giữa kỳ thật', 'Đổi như thế nào', 'Tra bảng', 'Kết quả (mã đề Ak1)'], [
    ['“Tính giá trị tới hạn U<sub>α</sub> với α = 7%”', 'Φ(U<sub>α</sub>) = 1 − 7% = 93%', 'A8, hàng 93%, cột z(Φ)', '1.476'],
    ['“P(4.0 ≤ X ≤ 4.29)”, X ~ N(4.13; 0.13²)', 'z₁ = 1.23; z₀ = −1.00; Φ(z₁) − Φ(z₀)', 'A7 hai lần', '0.8907 − 0.1587 = 0.7320'],
    ['“Giá trị tới hạn t<sub>α</sub>, α = 7%, Student 18 bậc tự do”', 'F = 1 − 0.07 = 0.93', 'A9, cột 18; F = 0.93 không có hàng ⇒ nội suy giữa 0.9 và 0.95', '≈ 1.57 (chính xác 1.544)'],
    ['“Khoảng tin cậy 90%, σ = 0.5”', 'α/2 = 5% ⇒ Φ(U) = 95%', 'A8, hàng 95%', 'U = 1.645'],
    ['“Khoảng tin cậy 90%, σ chưa biết”, n = 32', 'F = 0.95; bậc tự do 31', 'A9, hàng 0.95; cột 31 không có ⇒ nội suy giữa 30 và 40', '≈ 1.698 (chính xác 1.696)']], 'left')}
<p class="note">Các con số trên được tính bằng chương trình rồi đối chiếu với bảng; xem chi tiết 10 mã đề ở trang <a href="de-that/index.html">Đề thật HK2.2</a>.</p>'''
    # kiểm các số trong bảng "Đề hỏi gì"
    assert a8(93) == 1.476 and a7(1.23) == 0.8907 and a7(-1.0) == 0.1587 and abs(a7(1.23) - a7(-1.0) - 0.7320) < 1e-9
    assert abs(interp9(18, 0.93) - 1.57) < 0.005 and abs(float(st.t.ppf(.93, 18)) - 1.544) < 0.0005
    assert abs(interp9(31, 0.95) - 1.698) < 0.0005 and abs(float(st.t.ppf(.95, 31)) - 1.696) < 0.0005
    write('index.html', page('', 'Học tra bảng XSTK', body, 'Cách đọc bảng chuẩn tắc, Student, χ² từng bước, có ô tra thử và bài luyện', scripts=True))

# ═════════ CHUẨN TẮC
def chuan_tac():
    ph = lambda z: a7(z)
    p1 = ph(1.23); p2 = a7(-0.57); p3 = round(ph(2.05) - a7(-1.20), 4); p4 = round(1 - ph(1.64), 4)
    z1, z2 = round((90 - 100) / 15, 2), round((120 - 100) / 15, 2); p5 = round(a7(z2) - a7(z1), 4)
    assert (p1, p2, p3, p4) == (0.8907, 0.2843, 0.8647, 0.0505), (p1, p2, p3, p4)
    assert (z1, z2) == (-0.67, 1.33) and p5 == round(0.9082 - (1 - 0.7486), 4)
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Bảng chuẩn tắc</div>
<h1>Bảng chuẩn tắc: A7 (Φ) và A8 (z)</h1>
<p class="lead">Hai bảng cho cùng một đường cong chuẩn tắc N(0; 1). A7 đi từ <b>z đến xác suất</b>; A8 đi ngược từ <b>xác suất đến z</b>.</p>
<h2 id="y-nghia">1. Φ(z) là gì</h2>
<div class="fig"><div>{bell('left:1.23', 'Φ(1.23) = P(Z ≤ 1.23)')}</div><div>
<p>Φ(z) là <b>diện tích bên trái</b> điểm z dưới đường chuẩn tắc, tức xác suất P(Z ≤ z). Đường chuẩn tắc đối xứng quanh 0 nên:</p>
<ul><li>Φ(0) = 0.5</li><li>Φ(−z) = 1 − Φ(z)</li><li>P(Z &gt; z) = 1 − Φ(z)</li><li>P(a &lt; Z &lt; b) = Φ(b) − Φ(a)</li></ul></div></div>
<h2 id="a7">2. Bảng A7: biết z, tìm Φ(z)</h2>
<p>Bảng có 6 nhóm cột. Mỗi nhóm gồm cột <b>z</b> (bước 0.01) và cột <b>Φ(z)</b>. Tìm z ở cột z rồi đọc ô bên phải. Ô in 4 chữ số, hiểu là 0.xxxx.</p>
{ex('Ví dụ đọc Φ(1.23)', ol(['Tìm ô <b>1.23</b> ở các cột z (nằm trong nhóm thứ ba: 1.01 đến 1.50).', 'Đọc ô Φ(z) ngay bên phải: <b>8907</b>.', 'Vậy Φ(1.23) = <b>0.8907</b>.']))}
{lk('a7', 'Φ(z) bằng bảng A7')}
<details class="tbd" open><summary>Bảng A7 đầy đủ (kéo để xem)</summary><div data-table="a7"></div></details>
<h3>Năm dạng bài với A7</h3>
{ex('Dạng 1 · Φ(z) với z dương', f'<p>Φ(1.23) = <b>{p1:.4f}</b> (đọc thẳng).</p>')}
{ex('Dạng 2 · Φ(z) với z âm', f'<p>Φ(−0.57) = 1 − Φ(0.57) = 1 − {a7(0.57):.4f} = <b>{p2:.4f}</b>.</p>' + bell('left:-0.57', 'Φ(−0.57)'))}
{ex('Dạng 3 · P(a &lt; Z &lt; b)', f'<p>P(−1.20 &lt; Z &lt; 2.05) = Φ(2.05) − Φ(−1.20) = {ph(2.05):.4f} − (1 − {ph(1.20):.4f}) = {ph(2.05):.4f} − {a7(-1.20):.4f} = <b>{p3:.4f}</b>.</p>' + bell('between:-1.2,2.05', 'P(−1.20 &lt; Z &lt; 2.05)'))}
{ex('Dạng 4 · Đuôi phải', f'<p>P(Z &gt; 1.64) = 1 − Φ(1.64) = 1 − {ph(1.64):.4f} = <b>{p4:.4f}</b>.</p>')}
{ex('Dạng 5 · X ~ N(μ; σ²): chuẩn hoá rồi tra', ol([f'X ~ N(100; 15²). Tính P(90 &lt; X &lt; 120).', 'Đổi z = (x − μ)/σ: z₁ = (90 − 100)/15 = −0.67; z₂ = (120 − 100)/15 = 1.33.', f'Φ(1.33) = {ph(1.33):.4f}; Φ(−0.67) = 1 − Φ(0.67) = 1 − {ph(0.67):.4f} = {a7(-0.67):.4f}.', f'P = {ph(1.33):.4f} − {a7(-0.67):.4f} = <b>{p5:.4f}</b>.']) + '<p class="note">Chia cho σ (độ lệch chuẩn), không phải σ². Nếu z có nhiều hơn 2 chữ số thập phân thì làm tròn đến 2 chữ số rồi mới tra (ví dụ 1.2308 → 1.23).</p>')}
<h2 id="a8">3. Bảng A8: biết xác suất, tìm z</h2>
<p>Mỗi hàng ứng với một xác suất <b>P (%)</b>. Có hai cột kết quả:</p>
{table(['Cột', 'Nghĩa', 'Dùng khi'], [['z(Φ)', 'z sao cho Φ(z) = P%', 'giá trị tới hạn U<sub>α</sub> (P = 100 − α), tìm c để P(X ≤ c) cho trước'], ['z(D)', 'z sao cho P(|Z| &lt; z) = P% (D(z) = Φ(z) − Φ(−z))', 'xác suất hai phía, tìm khoảng đối xứng quanh 0']], 'left')}
{callout('warn', 'Chú ý dấu', '<p>Với P &lt; 50% thì z(Φ) <b>âm</b> (Φ(z) nhỏ hơn 0.5 nghĩa là z nằm bên trái 0). Với P = 50% thì z = 0. Cột z(D) luôn dương.</p>')}
{ex('Ví dụ · U<sub>α</sub> với α = 7% (đề giữa kỳ thật, mã Ak1)', ol(['U<sub>α</sub> thoả Φ(U<sub>α</sub>) = 1 − α = 1 − 7% = <b>93%</b>.', 'Vào hàng <b>93</b> của bảng A8, đọc cột z(Φ): <b>1.476</b>.', 'Vậy U<sub>7%</sub> = 1.476. Hình dưới: diện tích bên phải điểm đó là 7%.']) + bell('left:1.476', 'Φ(U) = 93%'))}
{ex('Ví dụ · tìm c với Φ(c) = 30%', ol(['Hàng <b>30</b>, cột z(Φ): <b>−0.524</b> (âm vì 30% &lt; 50%).']))}
{ex('Ví dụ · khoảng đối xứng chứa 90% xác suất', ol(['Cột z(D), hàng <b>90</b>: <b>1.645</b>. Vậy P(−1.645 &lt; Z &lt; 1.645) = 90%.']) + bell('between:-1.645,1.645', 'D(z) = 90%'))}
{lk('a8', 'z từ xác suất (A8)')}
<details class="tbd" open><summary>Bảng A8 đầy đủ (kéo để xem)</summary><div data-table="a8"></div></details>
<h2>4. Giá trị hay dùng (nên thuộc)</h2>
{table(['Độ tin cậy γ', 'α/2', 'U<sub>α/2</sub> (A8, hàng 1 − α/2)'], [['90%', '5%', '1.645 (hàng 95)'], ['95%', '2.5%', '1.960 (hàng 97.5)'], ['99%', '0.5%', '2.576 (hàng 99.5)']])}
<h2>5. Lỗi hay gặp</h2>
{callout('bad', 'Những chỗ sai nhiều nhất', '<ul><li>Tra thẳng hàng α% thay vì hàng (100 − α)%: α = 7% phải tra hàng 93, không phải hàng 7 (hàng 7 cho −1.476).</li><li>Nhầm U<sub>α</sub> với U<sub>α/2</sub>: câu “giá trị tới hạn U<sub>α</sub>” không chia đôi; chỉ khoảng tin cậy hai phía mới dùng α/2.</li><li>Quên đổi z âm: Φ(−1.00) = 0.1587, không phải 0.8413.</li><li>Dùng cột z(D) khi cần z(Φ) (hai cột khác nhau).</li><li>Chia cho σ² thay vì σ khi chuẩn hoá.</li></ul>')}'''
    write('chuan-tac/index.html', page('chuan-tac/', 'Bảng chuẩn tắc A7 và A8', body, 'Cách đọc bảng Φ(z) A7 và bảng z A8 từng bước'))

# ═════════ STUDENT
def student():
    df, F = 9, 0.95
    assert a9(0.95, 9) == 1.83
    c = interp9(31, 0.95); e = float(st.t.ppf(.95, 31)); c2 = interp9(18, 0.93); e2 = float(st.t.ppf(.93, 18))
    rows = [['90%', '10%', '5%', '0.95'], ['95%', '5%', '2.5%', '0.975'], ['98%', '2%', '1%', '0.99'], ['99%', '1%', '0.5%', '0.995'], ['99.8%', '0.2%', '0.1%', '0.999']]
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Bảng Student</div>
<h1>Bảng Student A9</h1>
<p class="lead">Bảng cho giá trị t sao cho <b>F(t) = P(T ≤ t)</b> với T có phân phối Student m bậc tự do. Hàng là F, cột là bậc tự do m.</p>
<h2>1. Cách đọc</h2>
<p>Ví dụ trong chính bảng: 9 bậc tự do, F = 0.95 ⇒ t = 1.83.</p>
{ex('Ví dụ đọc', ol(['Tìm cột <b>9</b> (bậc tự do) ở dòng tiêu đề.', 'Tìm hàng <b>F = 0.95</b> ở cột trái.', 'Ô giao nhau: <b>1.83</b>.']))}
{lk('a9', 'Student, có nội suy')}
<details class="tbd" open><summary>Bảng A9 đầy đủ (kéo để xem)</summary><div data-table="a9"></div></details>
<h2>2. Đổi đề bài về F (bước quan trọng nhất)</h2>
<p>Bảng chỉ có F, trong khi đề cho α hoặc độ tin cậy. Hai cách đổi khác nhau:</p>
{table(['Đề hỏi', 'Mức', 'F cần tra', 'Ví dụ'], [
    ['Giá trị tới hạn t<sub>α</sub> (một phía)', 'diện tích phải α', 'F = 1 − α', 'α = 7% ⇒ F = 0.93'],
    ['Khoảng tin cậy độ tin cậy γ (hai phía)', 'mỗi đuôi α/2', 'F = 1 − α/2 = (1 + γ)/2', 'γ = 90% ⇒ F = 0.95'],
    ['Kiểm định hai phía mức α', 'mỗi đuôi α/2', 'F = 1 − α/2', 'α = 5% ⇒ F = 0.975'],
    ['Kiểm định một phía mức α', 'một đuôi α', 'F = 1 − α', 'α = 5% ⇒ F = 0.95']], 'left')}
<h3>Bảng quy đổi độ tin cậy sang F (khoảng tin cậy)</h3>
{table(['Độ tin cậy γ', 'α', 'α/2', 'F = (1 + γ)/2'], rows)}
<p>Bậc tự do của khoảng tin cậy cho μ (σ chưa biết) là <b>n − 1</b>. Mẫu 16 phần tử ⇒ 15 bậc tự do.</p>
{ex('Ví dụ · khoảng tin cậy 95%, n = 16', ol(['Bậc tự do = 16 − 1 = <b>15</b>.', 'γ = 95% ⇒ F = (1 + 0.95)/2 = <b>0.975</b>.', f'Cột 15, hàng 0.975: <b>{a9(0.975, 15):.2f}</b>. Vậy t<sub>α/2</sub> = {a9(0.975, 15):.2f}.']))}
<h2>3. Khi bảng không có ô cần tìm: nội suy</h2>
<p>Bảng A9 chỉ có cột 1 đến 20, rồi 22, 24, 26, 28, 30, 40, 50, 100, 200, ∞; hàng F chỉ là 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999. Nếu df hoặc F cần tìm nằm giữa hai giá trị trong bảng thì <b>nội suy tuyến tính</b>:</p>
<p style="text-align:center"><b>y ≈ y₀ + (x − x₀)/(x₁ − x₀) · (y₁ − y₀)</b></p>
{ex('Ví dụ 1 · thiếu cột: df = 31, F = 0.95 (khoảng tin cậy 90%, n = 32)', ol([f'Cột 31 không có; hai cột kề là 30 (t = {a9(0.95,30):.2f}) và 40 (t = {a9(0.95,40):.2f}).', f'Nội suy: {a9(0.95,30):.2f} + (31 − 30)/(40 − 30) · ({a9(0.95,40):.2f} − {a9(0.95,30):.2f}) = <b>{c:.3f}</b>.', f'Giá trị chính xác (máy tính): {e:.3f}. Lệch {abs(c-e):.3f}, đủ tốt.']))}
{ex('Ví dụ 2 · thiếu hàng: df = 18, F = 0.93 (t<sub>α</sub> với α = 7%)', ol([f'Hàng F = 0.93 không có; hai hàng kề là 0.9 (t = {a9(0.9,18):.2f}) và 0.95 (t = {a9(0.95,18):.2f}).', f'Nội suy: {a9(0.9,18):.2f} + (0.93 − 0.90)/(0.95 − 0.90) · ({a9(0.95,18):.2f} − {a9(0.9,18):.2f}) = <b>{c2:.3f}</b>.', f'Giá trị chính xác: {e2:.3f}. Lệch {abs(c2-e2):.3f}.']) + '<p class="note">Sai lệch lớn hơn vì t tăng nhanh ở vùng đuôi (giữa F = 0.9 và 0.95). Nếu đề cho dùng máy tính thì lấy giá trị chính xác; nếu chỉ có bảng thì nội suy như trên và ghi rõ cách làm.</p>')}
<h2>4. Nhận xét và kiểm tra nhanh</h2>
<ul><li>Cùng F, df càng lớn thì t càng nhỏ, tiến dần về giá trị chuẩn tắc (cột ∞). Ví dụ F = 0.95: 6.31 (df 1), 1.83 (df 9), 1.72 (df 20), 1.65 (∞).</li><li>Cùng df, F lớn hơn thì t lớn hơn.</li><li>t luôn lớn hơn U cùng mức (đuôi dày hơn): t<sub>0.05</sub>(18) = 1.73 &gt; U<sub>0.05</sub> = 1.645.</li><li>Hàng F = 0.5 toàn 0.00 vì Student đối xứng quanh 0.</li></ul>
{callout('bad', 'Lỗi hay gặp', '<ul><li>Tra F = α (hoặc F = γ) thay vì F = 1 − α (hoặc (1 + γ)/2): ví dụ 90% phải vào hàng 0.95, không phải 0.9.</li><li>Dùng n thay vì n − 1 làm bậc tự do.</li><li>Dùng bảng chuẩn (A8) khi σ chưa biết.</li><li>Đọc nhầm cột khi bảng chia ba khối (1–10, 11–20, 22–∞): xem đúng dòng tiêu đề của khối.</li></ul>')}'''
    write('student/index.html', page('student/', 'Bảng Student A9', body, 'Cách đọc bảng Student A9, đổi α hoặc độ tin cậy sang F, nội suy'))

# ═════════ CHI BINH PHUONG
def chi2():
    v = float(D['A10']['v'][T.A10_F.index(0.99)][T.A10_DF.index(3)]); assert v == 11.34
    m = 150; h = math.sqrt(2 * m - 1); z = float(st.norm.ppf(0.95)); ap = 0.5 * (h + z) ** 2; ex_ = float(st.chi2.ppf(0.95, m))
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Bảng χ²</div>
<h1>Bảng χ² (A10)</h1>
<p class="lead">Cho x sao cho F(x) = P(χ² ≤ x) với χ² có m bậc tự do. Hàng là F (0.005 đến 0.995), cột là m (1 đến 30, rồi 40, 50, …, 100).</p>
{ex('Ví dụ trong bảng', ol(['3 bậc tự do, F = 0.99.', 'Cột <b>3</b>, hàng <b>0.99</b>: <b>11.34</b>.']))}
{callout('info', 'Hai đuôi của χ²', '<p>χ² không đối xứng nên khoảng hai phía cần <b>hai</b> giá trị: χ²<sub>α/2</sub> (đuôi phải, F = 1 − α/2) và χ²<sub>1−α/2</sub> (đuôi trái, F = α/2). Ví dụ α = 5%: F = 0.975 và F = 0.025.</p>')}
{lk('a10', 'χ² (A10)')}
<details class="tbd" open><summary>Bảng A10 đầy đủ (kéo để xem)</summary><div data-table="a10"></div></details>
<h2>Khi m &gt; 100</h2>
<p>Dùng xấp xỉ <b>x ≈ ½(h + z)²</b> với h = √(2m − 1) và z là giá trị chuẩn tắc ứng với F (tra A8, cột z(Φ)).</p>
{ex(f'Ví dụ · m = 150, F = 0.95', ol([f'h = √(2·150 − 1) = √299 = {h:.3f}.', 'F = 0.95 ⇒ z = 1.645 (A8, hàng 95).', f'x ≈ ½({h:.3f} + 1.645)² = <b>{0.5*(h+1.645)**2:.1f}</b> (chính xác {ex_:.1f}).']))}
{callout('bad', 'Lỗi hay gặp', '<ul><li>Dùng đuôi sai: cận trên của khoảng tin cậy σ² dùng χ² nhỏ (F = α/2), cận dưới dùng χ² lớn (F = 1 − α/2).</li><li>Bậc tự do m = n − 1 trong kiểm định phương sai (không phải n).</li><li>Từ cột 21 trở đi bảng in 1 chữ số thập phân: không đọc thành 2 chữ số.</li></ul>')}'''
    assert abs(0.5 * (h + 1.645) ** 2 - ap) < 0.2
    write('chi-binh-phuong/index.html', page('chi-binh-phuong/', 'Bảng χ² A10', body, 'Cách đọc bảng χ² A10'))

# ═════════ LUYỆN
def luyen():
    n = len(Qm.build())
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Luyện tra bảng</div>
<h1>Luyện tra bảng</h1>
<p class="lead">{n} câu: đáp số là giá trị <b>đọc từ bảng</b> (đúng như bản in). Sau khi kiểm tra, ô đúng được tô sáng trong bảng bên dưới. Có gợi ý, nút làm lại, tiến độ lưu trong trình duyệt.</p>
<div data-practice></div>
<h2>Bảng để tra (mở đúng bảng cần dùng)</h2>
<details class="tbd" open><summary>A7 · Φ(z)</summary><div data-table="a7"></div></details>
<details class="tbd"><summary>A8 · z cho xác suất</summary><div data-table="a8"></div></details>
<details class="tbd"><summary>A9 · Student</summary><div data-table="a9"></div></details>
<details class="tbd"><summary>A10 · χ²</summary><div data-table="a10"></div></details>'''
    write('luyen-tra/index.html', page('luyen-tra/', 'Luyện tra bảng', body, 'Bài luyện đọc bảng chuẩn tắc, Student, χ²'))

# ═════════ ĐỀ THẬT
sys.path.insert(0, os.path.dirname(__file__))
REAL = [('Ak1Bm1Zn5', 7, 4.13, 0.13, 4.29, 18, [4, 7, 16, 5]), ('Ak2Bm2Zn4', 8, 4.14, 0.14, 4.31, 19, [4, 8, 14, 5]), ('Ak3Bm3Zn3', 9, 4.15, 0.15, 4.33, 20, [4, 9, 12, 5]),
        ('Ak4Bm4Zn2', 10, 4.16, 0.16, 4.35, 21, [4, 10, 10, 5]), ('Ak5Bm5Zn1', 11, 4.17, 0.17, 4.37, 22, [4, 11, 8, 5]), ('Ak6Bm6Zn10', 22, 4.38, 0.38, 4.84, 43, [4, 22, 36, 5]),
        ('Ak7Bm7Zn9', 23, 4.39, 0.39, 4.86, 44, [4, 23, 34, 5]), ('Ak8Bm8Zn8', 24, 4.4, 0.4, 4.88, 45, [4, 24, 32, 5]), ('Ak9Bm9Zn7', 25, 4.41, 0.41, 4.9, 46, [4, 25, 30, 5]), ('Ak10Bm10Zn6', 26, 4.42, 0.42, 4.92, 47, [4, 26, 28, 5])]
def de_that():
    secs = []; summ = []
    for code, a, mu, sg, up, df, fr in REAL:
        P = 100 - a; z1 = round((up - mu) / sg, 2); z0 = round((4.0 - mu) / sg, 2)
        q1t = a8(P); q1e = float(st.norm.ppf(1 - a / 100))
        pt = round(a7(z1) - a7(z0), 4); pe = float(Phi((up - mu) / sg) - Phi((4.0 - mu) / sg))
        F = round(1 - a / 100, 4); inF = F in T.A9_F; inDf = df in T.A9_DF
        q8t = a9(F, df) if (inF and inDf) else interp9(df, F); q8e = float(st.t.ppf(F, df))
        n = sum(fr); xb = sum(k * m for k, m in zip(fr, [7, 9, 11, 13])) / n; s2 = (sum(k * m * m for k, m in zip(fr, [7, 9, 11, 13])) - n * xb * xb) / (n - 1); s = math.sqrt(s2)
        ub = a8(95); ue = float(st.norm.ppf(0.975 - 0.025)); tcd = n - 1; tt = interp9(tcd, 0.95) if tcd not in T.A9_DF else a9(0.95, tcd); te = float(st.t.ppf(0.95, tcd))
        eb_t, eb_e = ub * 0.5 / math.sqrt(n), 1.6448536269514722 * 0.5 / math.sqrt(n); ec_t, ec_e = tt * s / math.sqrt(n), te * s / math.sqrt(n)
        assert abs(ub - ue) < 0.001
        loc8 = (f'cột {df}' if inDf else f'cột {df} không có (giữa {max(d for d in T.A9_DF if d is not None and d < df)} và {min(d for d in T.A9_DF if d is not None and d > df) if df < 200 else "∞"})') + ', ' + (f'hàng F = {F:g}' if inF else f'hàng F = {F:g} không có (nội suy hai hàng kề)')
        rows = [
            ['1', f'U<sub>{a}%</sub>: Φ(U) = {P}%', f'A8 · hàng {P}%, cột z(Φ)', f'<b>{q1t:.3f}</b>', f'{q1e:.3f}'],
            ['7', f'z₁ = ({up:g} − {mu:g})/{sg:g} = {z1:.2f}; z₀ = (4 − {mu:g})/{sg:g} = {mn(f"{z0:.2f}")}', f'A7 · Φ({z1:.2f}) = {a7(z1):.4f}; Φ({mn(f"{z0:.2f}")}) = 1 − {a7(abs(z0)):.4f} = {a7(z0):.4f}', f'<b>{pt:.4f}</b>', f'{pe:.4f}'],
            ['8', f't<sub>{a}%</sub>({df}): F = 1 − {a/100:g} = {F:g}', f'A9 · {loc8}', f'<b>{q8t:.3f}</b>', f'{q8e:.3f}'],
            ['9b', 'U<sub>0.05</sub> (σ = 0.5): Φ(U) = 95%', 'A8 · hàng 95%, cột z(Φ)', f'<b>{ub:.3f}</b> ⇒ e = {eb_t:.4f}', f'e = {eb_e:.4f}'],
            ['9c', f't<sub>0.05</sub>({tcd}): F = 0.95', 'A9 · hàng 0.95, ' + (f'cột {tcd}' if tcd in T.A9_DF else f'cột {tcd} không có (nội suy cột kề)'), f'<b>{tt:.3f}</b> ⇒ e = {ec_t:.4f}', f'{te:.3f}; e = {ec_e:.4f}']]
        secs.append(f'<details class="tbd"><summary>Mã đề {code}</summary>' + table(['Câu', 'Cần tra', 'Bảng và vị trí', 'Đọc từ bảng', 'Máy tính'], rows, 'left') + f'<p class="note">Khoảng tin cậy (c): x̄ = {xb:.4f}, s = {s:.4f}, n = {n}.</p></details>')
        summ.append([code, f'{a}%', f'{df}', f'{F:g}', ('có' if (inF and inDf) else 'nội suy'), f'{q8t:.3f}', f'{q8e:.3f}', f'{abs(q8t-q8e):.3f}'])
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Đề thật HK2.2</div>
<h1>Tra bảng cho 10 mã đề giữa kỳ thật HK2.2</h1>
<p class="lead">Với mỗi mã đề: câu nào cần tra, tra ở bảng nào, hàng cột nào, đọc ra bao nhiêu, và so với giá trị chính xác của máy tính. Số liệu mã đề lấy từ file PDF 10 mã đề của học kỳ này.</p>
{callout('info', 'Câu cần tra bảng trong đề', '<ul><li><b>Câu 1</b>: U<sub>α</sub> ⇒ bảng A8 (hàng 100 − α), đọc thẳng, không nội suy.</li><li><b>Câu 7</b>: xác suất chuẩn ⇒ bảng A7 hai lần.</li><li><b>Câu 8</b>: t<sub>α</sub> Student ⇒ bảng A9, <b>luôn phải nội suy</b> (F = 1 − α hầu như không có hàng trong A9, trừ mã Ak4 với F = 0.9; nhiều mã đề còn thiếu cả cột bậc tự do).</li><li><b>Câu 9b</b>: U<sub>0.05</sub> = 1.645 (A8 hàng 95).</li><li><b>Câu 9c</b>: t<sub>0.05</sub>(n − 1) (A9 hàng 0.95, cột n − 1 thường phải nội suy).</li></ul>')}
<h2>Câu 8: bảng A9 cho bao nhiêu so với máy tính</h2>
{table(['Mã đề', 'α', 'Bậc tự do', 'F = 1 − α', 'Ô trong bảng', 'Nội suy từ bảng', 'Chính xác', 'Lệch'], summ)}
<p class="note">Nội suy tuyến tính hai chiều (theo bậc tự do rồi theo F) có thể lệch tới vài phần trăm ở vùng đuôi. Thang chấm do giảng viên quyết định; nếu cần, trình bày rõ cách nội suy.</p>
<h2>Chi tiết từng mã đề</h2>{''.join(secs)}'''
    write('de-that/index.html', page('de-that/', 'Tra bảng cho đề thật HK2.2', body, 'Câu nào tra bảng nào, hàng cột nào, kết quả so với máy tính, cho 10 mã đề HK2.2'))

# ═════════ IN
def in_bang():
    body = '''<h1>In bảng A7, A8, A9, A10</h1><p class="lead noprint">Bấm Ctrl + P (hoặc Cmd + P) để in hoặc lưu PDF. Mỗi bảng bắt đầu một trang.</p>
<h2>Bảng A7 · Φ(z)</h2><div data-table="a7"></div><h2>Bảng A8 · z cho xác suất</h2><div data-table="a8"></div><h2>Bảng A9 · Student</h2><div data-table="a9"></div><h2>Bảng A10 · χ²</h2><div data-table="a10"></div>'''
    write('in-bang/index.html', page('in-bang/', 'In bảng', body, 'Bản in gọn các bảng A7 đến A10'))

if __name__ == '__main__':
    write('assets/data.js', 'window.TB=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';window.QUESTIONS=' + json.dumps(Qm.build(), ensure_ascii=False, separators=(',', ':')) + ';')
    home(); chuan_tac(); student(); chi2(); luyen(); de_that(); in_bang()
    print('ok', len(Qm.build()), 'câu')
