"""Dựng toàn bộ site tĩnh: python3 build_site.py  (chạy assemble.py trước để có data/qbank/*.json)."""
import re, os, sys, json, glob, importlib, html
sys.path.insert(0, os.path.dirname(__file__))
from sitelib import *
from modules import MODS, BY
from errata import ERRATA

SIMJS = ['ps.js', 'simlib.js'] + sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '_shared', 'w_*.js'))) + ['sim.js']
def have(mid): return os.path.exists(os.path.join(os.path.dirname(__file__), f'content_{mid}.py')) and os.path.exists(os.path.join(ROOT, 'data', 'qbank', mid + '.json'))
def audit_all():
    p = os.path.join(ROOT, 'data', 'qbank', '_audit.json')
    return json.load(open(p)) if os.path.exists(p) else {}

def pick_quiz(items, n=10):
    import random
    rng = random.Random(7)
    goc = [i for i in items if i['origin'] == 'goc'] or items
    by = {1: [], 2: [], 3: []}
    for i in goc: by[i['level']].append(i)
    out = []
    for lv, k in ((1, 3), (2, 4), (3, 3)):
        pool = by[lv][:]; rng.shuffle(pool); out += pool[:k]
    rest = [i for i in goc if i not in out]; rng.shuffle(rest)
    while len(out) < n and rest: out.append(rest.pop())
    rng.shuffle(out)
    return out[:n]

def build_module(mid):
    c = importlib.import_module('content_' + mid).module()
    meta = BY[mid]; bank = load_bank(mid); au = audit_all().get(mid, {})
    idx = [m['id'] for m in MODS].index(mid)
    nsl = []
    try:   # phần chuyên sâu viết thêm (more_<mid>.py) chèn trước phần 'Bẫy'
        extra = importlib.import_module('more_' + mid).parts()
        cut = next((k for k, p in enumerate(c['parts']) if p['title'].startswith('Bẫy')), len(c['parts']) - 1)
        c['parts'] = c['parts'][:cut] + extra + c['parts'][cut:]
    except ModuleNotFoundError: pass
    total = len(c['parts'])
    for pi, p in enumerate(c['parts']):
        nsl.append((divider(pi + 1, total, p['title'], p['bullets']), True))
        for s in p['slides']: nsl.append((re.sub(r'PHẦN \d+', f'PHẦN {pi + 1}', autotex(s), count=1), False))
    quiz = pick_quiz(bank['items'])
    prev = next((m for m in reversed(MODS[:idx]) if have(m['id'])), None)
    nxt = next((m for m in MODS[idx + 1:] if have(m['id'])), None)
    nav = '<div class="modnav">' + (f'<a href="../{prev["slug"]}/index.html">← Module {prev["id"][1:]}: {esc(prev["short"])}</a>' if prev else '<span></span>') + \
          (f'<a href="../{nxt["slug"]}/index.html">Module {nxt["id"][1:]}: {esc(nxt["short"])} →</a>' if nxt else '<span></span>') + '</div>'
    ng, nb = au.get('goc', 0), au.get('bo_sung', 0)
    diagram = ''
    dp = os.path.join(ROOT, 'img', f'{mid}.png')
    if os.path.exists(dp): diagram = '<h2>Sơ đồ tóm tắt</h2>' + diag(f'../../img/{mid}.png', c['title'], 'Sơ đồ vẽ bằng drawio, tóm tắt các bước của module.')
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Module {mid[1:]}</div>
<h1>Module {mid[1:]}. {esc(c['title'])}</h1><p class="lead">{esc(c['subtitle'])}</p>
<p><span class="tag">{esc(meta['buoi'])}</span><span class="tag">Mục {esc(meta['sec'])}</span><span class="tag">Kreyszig {esc(meta['krey'])}</span><span class="tag">{esc(c['time'])}</span><span class="tag exam">{ng + nb} câu hỏi ({ng} gốc)</span></p>
<p style="font-size:.85rem;color:var(--muted)">Nguồn: {esc(c['source'])} · Liên quan đề thi: {esc(c['exam'])}</p>
{callout('good', '🎯 Sau module này bạn sẽ', ul(c['objectives']))}
<h2>Bài giảng (slide)</h2>{deck(nsl, 'd-' + mid)}{diagram}
<h2>Nội dung chi tiết, ví dụ và thực hành</h2>{autotex(c['notes'])}
<h2>Tự kiểm tra nhanh (10 câu)</h2><p class="lead">Chọn đáp án để chấm ngay; mỗi câu đều có giải thích; có nút làm lại từng câu và cả bài.</p>{quiz_block('q-' + mid, quiz)}
<h2>Luyện tập sâu</h2>{callout('info', f'Ngân hàng {len(bank["items"])} câu trắc nghiệm + {len(bank["essays"])} bài tự luận', f'<p>Câu gốc lấy từ giáo trình Lecture Notes, Kreyszig Problem Set và đề thi; lọc theo nguồn/mức/chủ đề, phản hồi tức thì có giải thích, có nút <b>↺ làm lại</b>. <a class="btn" href="luyen-tap/index.html">Vào luyện tập Module {mid[1:]} →</a></p>')}
{nav}'''
    write(f'vi/{meta["slug"]}/index.html', page(f'Module {mid[1:]}: {c["title"]}', body, 2, c['subtitle'], scripts=['deck.js', 'quiz.js'] + (SIMJS if c.get('sims') else [])))
    data = json.dumps(dict(module=mid, items=bank['items'], essays=bank['essays']), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    bb = f'''<div class="crumbs"><a href="../../index.html">Trang chủ</a> › <a href="../index.html">Module {mid[1:]}</a> › Luyện tập</div>
<h1>Luyện tập · Module {mid[1:]}: {esc(meta['short'])}</h1>
<p class="lead">{len(bank['items'])} câu trắc nghiệm ({ng} câu gốc từ tài liệu, {nb} câu bổ sung) và {len(bank['essays'])} bài tự luận có lời giải. Tiến độ lưu trong trình duyệt của bạn (localStorage).</p>
<div id="bank"></div><script type="application/json" id="bank-data">{data}</script>'''
    write(f'vi/{meta["slug"]}/luyen-tap/index.html', page(f'Luyện tập Module {mid[1:]}', bb, 3, 'Ngân hàng câu hỏi', scripts=['bank.js'], math=False))

def build_home():
    au = audit_all(); cards = ''; cur = None
    for m in MODS:
        if m['buoi'] != cur:
            if cur: cards += '</div>'
            cur = m['buoi']; cards += f'<h3>{esc(cur)}</h3><div class="grid">'
        a = au.get(m['id'])
        if have(m['id']):
            cards += f'<a class="mod-card" href="{m["slug"]}/index.html"><div class="num">MODULE {m["id"][1:]} · mục {esc(m["sec"])}</div><h3>{esc(m["title"])}</h3><p>{a["n"]} câu trắc nghiệm ({a["goc"]} gốc) · {a["essays"]} tự luận</p><p>Kreyszig {esc(m["krey"])}</p></a>'
        else:
            cards += f'<div class="mod-card" style="opacity:.55"><div class="num">MODULE {m["id"][1:]} · mục {esc(m["sec"])}</div><h3>{esc(m["title"])}</h3><p>Đang biên soạn…</p></div>'
    cards += '</div>'
    ndone = sum(1 for m in MODS if have(m['id'])); tot_q = sum(au.get(m['id'], {}).get('n', 0) for m in MODS)
    body = f'''<h1>Lý thuyết xác suất thống kê · Phenikaa</h1>
<p class="lead">Hệ thống tự học mở, tương tác cho học phần FFS703010 — bám đề cương, giáo trình Lecture Notes (Vũ Hữu Nhự), Kreyszig <i>Advanced Engineering Mathematics</i> Part G và các đề thi thật. Mỗi module có slide, ví dụ có lời giải, mô phỏng tương tác, ngân hàng 100–300 câu hỏi (ưu tiên câu gốc từ tài liệu) và tự luận.</p>
<p><span class="tag">{ndone}/{len(MODS)} module đã xong</span><span class="tag">{tot_q} câu trắc nghiệm</span><span class="tag">Công thức KaTeX · chạy 100% trong trình duyệt</span></p>
{callout('info', 'Cách học', '<ol><li>Xem slide của module (←/→, toàn màn hình).</li><li>Đọc ví dụ chi tiết và thử widget tương tác.</li><li>Làm quiz nhanh 10 câu, rồi vào ngân hàng luyện tập sâu.</li><li>Gần ngày thi: vào <a href="luyen-de/index.html">Luyện đề</a>; dùng <a href="bang-tra/index.html">Bảng tra</a> thay bảng A7/A8/A9.</li></ol>')}
<h2 id="lo-trinh">Lộ trình theo đề cương (5 bài học → 13 module)</h2>{cards}'''
    write('vi/index.html', page('Trang chủ', body, 1, 'Tự học xác suất thống kê Phenikaa'))
    write('index.html', '<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=vi/index.html"><title>Xác suất thống kê</title></head><body><a href="vi/index.html">Vào trang học xác suất thống kê</a></body></html>')

def build_tables():
    body = '''<h1>Bảng tra điện tử</h1><p class="lead">Thay cho các bảng A7 (hàm Φ), A8 (giá trị z), A9 (phân phối Student) kèm đề thi; thêm χ². Tính trực tiếp bằng thuật toán đã đối chiếu SciPy (3000 phép so, sai khác &lt; 10⁻⁷).</p><div class="sim" data-sim="tables"></div>
<h2>Một số giá trị hay dùng</h2><table class="t"><tr><th>α</th><th>U_α</th><th>U_{α/2}</th></tr>''' + ''.join(f'<tr><td>{a}</td><td>{PSV.U(a):.4f}</td><td>{PSV.U(a/2):.4f}</td></tr>' for a in (0.1, 0.05, 0.025, 0.01, 0.005)) + '</table>'
    write('vi/bang-tra/index.html', page('Bảng tra', body, 2, 'Bảng tra Φ, z, t, χ²', scripts=SIMJS, math=False))

def build_docs():
    rows = ''.join(f'<li>{html.escape(n)} — <i>{html.escape(d)}</i></li>' for n, d in SRC)
    au = audit_all()
    audit_tbl = '<table class="t left"><tr><th>Module</th><th>Trắc nghiệm</th><th>Gốc</th><th>Bổ sung</th><th>Tự luận</th></tr>' + ''.join(f'<tr><td>M{m["id"][1:]} {html.escape(m["short"])}</td><td>{au[m["id"]]["n"]}</td><td>{au[m["id"]]["goc"]}</td><td>{au[m["id"]]["bo_sung"]}</td><td>{au[m["id"]]["essays"]}</td></tr>' for m in MODS if m['id'] in au) + '</table><p>Module 4, 7, 11, 12 có ít câu gốc vì tài liệu về các chủ đề này mỏng (Kreyszig không có mục Bayes; Chương 3 mục tùy chọn trong giáo trình tiếng Việt để trống); phần còn lại là biến thể tham số, được gắn nhãn “➕ Bổ sung”.</p>'
    err = ''.join(f'<li>{html.escape(e)}</li>' for e in ERRATA)
    body = f'''<h1>Tài liệu nguồn và ghi chú kiểm chứng</h1><ul>{rows}</ul>
<h2>Số câu gốc và câu bổ sung theo module</h2>{audit_tbl}<h2>Cách xử lý nguồn</h2><ul><li>Văn bản PDF có lớp chữ được trích bằng pdftotext/PyMuPDF; ký hiệu toán (dấu trừ, ∪, ∩…) bị mất khi trích nên mọi câu có ký hiệu đều được đối chiếu với ảnh trang.</li>
<li>Đề giữa kỳ mẫu là ảnh (không có lớp chữ): đã OCR bằng Tesseract (vie+eng) và đối chiếu thủ công vì OCR bỏ sót câu 3, 4, 8.</li><li>Ảnh minh hoạ trong giáo trình (đồ thị phân phối, vùng bác bỏ, scatter r) đã được xem và đối chiếu với nội dung văn bản.</li>
<li>Đáp án của mọi câu trắc nghiệm do chương trình tính (Python/SciPy, tự cài đặt đối chiếu numpy); các tài liệu gốc không có đáp án cho Problem Set của Kreyszig nên đáp án là do người biên soạn tính.</li></ul>
<h2>Sai sót phát hiện trong tài liệu gốc</h2><ul id="errata">{err}</ul>'''
    write('vi/tai-lieu/index.html', page('Tài liệu', body, 2, 'Nguồn và kiểm chứng', math=False))

def build_exams():
    import random
    from crosscheck import rows
    groups = [('Đề 1 · Chương 1 (M1–M3)', ['m01','m02','m03']), ('Đề 2 · Chương 1 (M4–M6)', ['m04','m05','m06']), ('Đề 3 · Chương 2 (M7–M8)', ['m07','m08']),
              ('Đề 4 · Chương 3 (M10–M12)', ['m10','m11','m12']), ('Đề 5 · Chương 4 + kiểm định (M10, M13)', ['m10','m13']),
              ('Đề 6 · Tổng hợp', None), ('Đề 7 · Tổng hợp', None), ('Đề 8 · Tổng hợp', None)]
    banks = {m['id']: load_bank(m['id'])['items'] for m in MODS if have(m['id'])}
    sets = []
    for gi, (nm, mods) in enumerate(groups):
        rng = random.Random(500 + gi); mods = mods or [k for k in banks if k != 'm09']; pool = []
        for mid in mods:
            its = [i for i in banks.get(mid, []) if i['origin'] == 'goc' and len(i['q']) < 420]
            rng.shuffle(its); pool += [(mid, i) for i in its[:max(3, 15 // len(mods) + 2)]]
        rng.shuffle(pool); pick = pool[:15]
        sets.append([dict(q=i['q'], opts=i['opts'], correct=i['correct'], explain=i['explain'], src=f'{mid.upper()} · ' + i['src']) for mid, i in pick])
    data = json.dumps(dict(sets=sets), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    body = '<h1>Luyện đề</h1><p class="lead">Tám đề trắc nghiệm 15 câu, 30 phút, tạo từ câu gốc của các module (đề 1–5 theo chương, 6–8 tổng hợp). Sau khi nộp bài có điểm thang 10 và giải thích từng câu; có nút làm lại.</p><div id="exam"></div><script type="application/json" id="exam-data">' + data + '</script>'
    write('vi/luyen-de/index.html', page('Luyện đề', body, 2, 'Luyện đề trắc nghiệm', scripts=['exam.js'], math=False))
    rs = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{o}</td><td>{float(c):.5g}</td><td>{"✓" if ok else "≈"}</td></tr>' for a, b, o, c, ok in rows())
    body = f'''<h1>Cấu trúc đề thi và đối chiếu đáp án chính thức</h1><p class="lead">Mọi đề cuối kỳ đã công bố (2021–2022; 2022–2023 HK1 2TC và HK2 3TC; đề mẫu 03/2024) có cùng khung 4–5 câu. Giữa kỳ: 8 câu trắc nghiệm + 1 câu tự luận (đề mẫu); đáp án giữa kỳ HK2 có 4 câu tham số hóa.</p>
<table class="t left"><tr><th>Câu</th><th>Nội dung</th><th>Module</th></tr><tr><td>1</td><td>Phân phối chuẩn: P(X ≤ a) và tìm c (hoặc bảng phân phối rời rạc ở đề 2TC)</td><td><a href="../m06-nhi-thuc-poisson-chuan/index.html">M6</a> / <a href="../m05-bien-ngau-nhien/index.html">M5</a></td></tr><tr><td>2</td><td>Khoảng tin cậy cho trung bình, dữ liệu theo lớp (σ biết hoặc t)</td><td><a href="../m08-khoang-tin-cay/index.html">M8</a></td></tr><tr><td>3</td><td>Kiểm định kỳ vọng, đối thuyết μ &gt; μ₀ (hoặc μ &lt; μ₀)</td><td><a href="../m10-kiem-dinh-ky-vong/index.html">M10</a></td></tr><tr><td>4</td><td>Hồi quy tuyến tính mẫu và dự báo, hoặc hệ số tương quan mẫu</td><td><a href="../m13-tuong-quan-hoi-quy/index.html">M13</a></td></tr><tr><td>5</td><td>Hàm mật độ (E, trung vị) hoặc MLE</td><td><a href="../m05-bien-ngau-nhien/index.html">M5</a> / <a href="../m07-mau-uoc-luong-diem/index.html">M7</a></td></tr></table>
<h2>Đối chiếu kết quả tự tính với đáp án chính thức</h2><p>Chương trình tính lại các đáp án có trong tài liệu và so sánh. “≈” nghĩa là đáp án chính thức đã làm tròn trung gian (ví dụ HK2 đề 1 câu 3: s² chính thức 0.293 vì làm tròn x̄ trước khi bình phương; chính xác 0.288), kết luận không đổi.</p><div style="overflow:auto"><table class="t left"><tr><th>Đề</th><th>Mục</th><th>Chính thức</th><th>Tự tính</th><th></th></tr>{rs}</table></div>'''
    write('vi/cau-truc-de/index.html', page('Cấu trúc đề thi', body, 2, 'Cấu trúc đề và đối chiếu', math=False))
    write('vi/de-giua-ky/index.html', page('Đề giữa kỳ tự soạn', open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'de_giua_ky_body.html'), encoding='utf-8').read(), 2, 'Ba đề giữa kỳ mục 1.1–1.5', math=False))

def build_exam_placeholder():
    body = '<h1>Luyện đề</h1><p class="lead">Đang biên soạn: đề trắc nghiệm tổng hợp tính giờ từ ngân hàng câu gốc và phân tích cấu trúc đề thi cuối kỳ các năm.</p>'
    write('vi/luyen-de/index.html', page('Luyện đề', body, 2, 'Luyện đề', math=False))

class PSV:
    import math
    from scipy import stats as _st
    @staticmethod
    def U(a): return PSV._st.norm.ppf(1 - a)

if __name__ == '__main__':
    for m in MODS:
        if have(m['id']): build_module(m['id'])
    build_home(); build_tables(); build_docs()
    build_exams()
    print('built')
