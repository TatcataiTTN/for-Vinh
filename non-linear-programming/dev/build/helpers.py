"""helpers.py — hàm dựng HTML cho nội dung module (dùng chung gen_site và c_*.py)."""
import os, json, subprocess, html, shutil
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'for-Vinh', 'non-linear-programming')
R = json.load(open(os.path.join(ROOT, 'NLP-work', 'verify', 'results.json'), encoding='utf-8'))
SLIDE_PDF = {
    'm1': os.path.join(ROOT, 'Slides', '1_Kien thuc ve ham loi va tap loi_250418.pdf'),
    'm2': os.path.join(ROOT, 'Slides', '2_NonlinearProgram_KKT_250418.pdf'),
    'm3': os.path.join(ROOT, 'Slides', '3_QuadraticPrograming_250419a.pdf'),
}
# ------------------------------------------------------------------ helpers nội dung
def esc(s): return html.escape(s, quote=True)

def callout(kind, title, body):
    return f'<div class="callout {kind}"><span class="ct"><b>{title}</b></span>{body}</div>'

def formula(label, tex, legend=None):
    h = f'<div class="pd-formula"><div class="pd-formula-label">{label}</div>\\[{tex}\\]</div>'
    if legend:
        h += '<ul class="pd-legend">' + ''.join(f'<li><b>\\({s}\\)</b><span>{t}</span></li>' for s, t in legend) + '</ul>'
    return h

def steps(items):
    return '<ol class="steps">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

def solution(summary, body, open_=False):
    return f'<details class="solution"{" open" if open_ else ""}><summary>{summary}</summary><div class="body">{body}</div></details>'

def table(headers, rows, cls=''):
    h = '<div class="tbl-wrap"><table class="%s"><thead><tr>' % cls + ''.join(f'<th>{x}</th>' for x in headers) + '</tr></thead><tbody>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>'
    return h + '</tbody></table></div>'

def fig(name, caption, up=2):
    pre = '../' * up
    return f'<figure class="diagram"><img src="{pre}assets/diagrams/{name}.svg" alt="{esc(caption)}" loading="lazy"/><figcaption>{caption}</figcaption></figure>'

def widget(kind, extra=''):
    return f'<div class="widget" data-widget="{kind}">{extra}</div>'

# ---- ảnh gốc slide: render từ PDF ở 150dpi -> JPEG
_imgcache = set()
def slide_img(spec):
    """spec = 'm1:26' -> trả về đường dẫn tương đối từ modules/<slug>/ """
    key, page = spec.split(':'); page = int(page)
    name = f'{key}_p{page:02d}.jpg'
    dst = os.path.join(SITE, 'assets', 'slides', name)
    if name not in _imgcache and not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        tmp = os.path.join(ROOT, 'NLP-work', 'pages', f'_tmp_{key}')
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', '150', '-jpeg', '-jpegopt', 'quality=82', SLIDE_PDF[key], tmp], check=True)
        cand = [f for f in os.listdir(os.path.dirname(tmp)) if f.startswith(f'_tmp_{key}') and f.endswith('.jpg')]
        shutil.move(os.path.join(os.path.dirname(tmp), cand[0]), dst)
    _imgcache.add(name)
    return f'../../assets/slides/{name}'

def sl(title, body, kicker='', img=None, explain=None, cls=''):
    """slide nội dung. img='m1:26' (trang slide gốc), explain=HTML giải thích cho người mới."""
    h = f'<div class="mdeck-slide {cls}" data-title="{esc(title)}">'
    if kicker: h += f'<div class="kicker">{kicker}</div>'
    h += f'<h2>{title}</h2>{body}'
    if img:
        src = slide_img(img); pg = img.split(':')[1]
        h += f'<figure class="slide-fig"><a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="Slide gốc trang {pg}" loading="lazy"/></a><figcaption>Slide gốc, trang {pg} — bấm để phóng to</figcaption></figure>'
    if explain:
        h += f'<details class="slide-explain"><summary>📖 Giải thích cho người mới bắt đầu</summary><div class="slide-explain-body">{explain}</div></details>'
    return h + '</div>'

def part(n, total, title, bullets, mod=''):
    li = ''.join(f'<li>{b}</li>' for b in bullets)
    return (f'<div class="mdeck-slide part-divider" data-title="Phần {n}: {esc(title)}"><div class="kicker">{mod} · PHẦN {n}/{total}</div>'
            f'<div class="part-num">{n:02d}</div><h2>{title}</h2><ul class="part-list">{li}</ul></div>')

def deck(slides):
    return ('<div class="mdeck"><div class="mdeck-viewport">' + ''.join(slides) + '</div>'
            '<div class="mdeck-bar"><button class="mdeck-prev" type="button">◀ Trước</button><button class="mdeck-next" type="button">Sau ▶</button>'
            '<span class="mdeck-count"></span><div class="mdeck-dots"></div><button class="mdeck-fs" type="button">⛶ Toàn màn hình</button></div></div>')



import re as _re
def fixmath(s):
    """Trong đoạn toán \\( ... \\) hoặc \\[ ... \\], thay < và > bằng \\lt, \\gt để trình duyệt không hiểu nhầm là thẻ HTML."""
    if not isinstance(s, str): return s
    def rep(m):
        body = m.group(0)
        return body.replace('<', '\\lt ').replace('>', '\\gt ')
    return _re.sub(r'\\\((.+?)\\\)|\\\[(.+?)\\\]', rep, s, flags=_re.S)

def fixmath_obj(o):
    if isinstance(o, str): return fixmath(o)
    if isinstance(o, list): return [fixmath_obj(x) for x in o]
    if isinstance(o, dict): return {k: (fixmath_obj(v) if k in ('q', 'opts', 'explain', 'check', 'ans_text', 'grp', 'ref') else v) for k, v in o.items()}
    return o
