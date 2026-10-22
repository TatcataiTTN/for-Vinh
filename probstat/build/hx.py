"""Bộ dựng HTML: slide, công thức, callout, ví dụ… (Python -> chuỗi HTML)"""
import html, json, re
def esc(s): return html.escape(str(s),quote=False)
def sl(body,kicker=None,title=None,explain=None):
    h=''
    if kicker: h+=f'<div class="kicker">{kicker}</div>'
    if title: h+=f'<h2>{title}</h2>'
    h+=body
    if explain: h+=f'<details class="slide-explain"><summary>📖 Giải thích cho người mới bắt đầu</summary><div class="slide-explain-body">{explain}</div></details>'
    return h
def formula(label,math,legend=None):
    h=f'<div class="pd-formula"><div class="pd-formula-label">{label}</div><div class="pd-formula-math">\\[{math}\\]</div></div>'
    if legend: h+='<ul class="pd-legend">'+''.join(f'<li><b>\\({k}\\)</b><span>{v}</span></li>' for k,v in legend)+'</ul>'
    return h
def callout(kind,title,body):
    k={'info':'','good':' good','warn':' warn','bad':' bad'}[kind]
    return f'<div class="callout{k}"><b class="t">{title}</b>{body}</div>'
def ex(title,body): return f'<div class="ex"><div class="exh">Ví dụ · {title}</div>{body}</div>'
def table(head,rows,cls=''):
    return f'<table class="t {cls}"><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
def code(t,lang=''): return f'<pre><code>{esc(t)}</code></pre>'
def ul(items,ordered=False):
    t='ol' if ordered else 'ul'; return f'<{t}>'+''.join(f'<li>{i}</li>' for i in items)+f'</{t}>'
def sim(name): return f'<div class="sim" data-sim="{name}"></div>'
def diag(path,alt,cap=''): return f'<div class="diag"><a href="{path}" target="_blank" rel="noopener"><img src="{path}" alt="{esc(alt)}" loading="lazy"></a>'+(f'<div style="font-size:.78rem;color:var(--muted)">{cap}</div>' if cap else '')+'</div>'
def divider(n,total,title,bullets):
    return f'<div class="kicker">PHẦN {n}/{total}</div><div class="part-num">{n:02d}</div><h2>{title}</h2><ul class="part-list">'+''.join(f'<li>{b}</li>' for b in bullets)+'</ul>'
def deck(slides_html,deck_id='d0'):
    """slides_html: list of (html, is_divider)"""
    s=''
    for h,div in slides_html:
        s+=f'<div class="mdeck-slide{" part-divider" if div else ""}">{h}</div>'
    return (f'<div class="mdeck" id="{deck_id}"><div class="mdeck-viewport">{s}</div>'
            '<div class="mdeck-bar"><button class="mdeck-prev" type="button">◀ Trước</button><button class="mdeck-next" type="button">Sau ▶</button>'
            '<span class="mdeck-count"></span><div class="mdeck-dots"></div><button class="mdeck-fs" type="button">⛶ Toàn màn hình</button></div></div>')
def quiz_block(root_id,items,title='Tự kiểm tra nhanh'):
    data=json.dumps(dict(items=[dict(q=i['q'],opts=i['opts'],correct=i['correct'],explain=i['explain']) for i in items]),ensure_ascii=False).replace('</','<\\/')
    return f'<div class="quiz"><div id="{root_id}"></div></div><script type="application/json" class="quiz-data" data-root="{root_id}">{data}</script>'

def m(t): return f'\\({t}\\)'          # công thức inline KaTeX
def dm(t): return f'\\[{t}\\]'          # công thức khối KaTeX
def steps(items):
    """Lời giải từng bước: list các chuỗi HTML."""
    return '<ol class="steps">'+''.join(f'<li>{i}</li>' for i in items)+'</ol>'

import re as _re
_SKIP=_re.compile(r'(\\\(.*?\\\)|\\\[.*?\\\]|<script.*?</script>|<pre.*?</pre>|<code.*?</code>|<svg.*?</svg>|<[^>]+>)',_re.S)
_PAT=[(_re.compile(r'\bq_([LMU])\b'),r'\\(q_\1\\)'),(_re.compile(r'\bf_rel\b'),r'\\(f_{\\text{rel}}\\)'),(_re.compile(r'\bs_([xy])\b'),r'\\(s_\1\\)'),(_re.compile(r'\bx_(min|max)\b'),r'\\(x_{\\text{\1}}\\)')]
_MATH=_re.compile(r'(\\\(.*?\\\)|\\\[.*?\\\])',_re.S)
def safemath(h):
    """'<' thô trong công thức (vd P(a<X\\le b)) bị trình duyệt hiểu là thẻ HTML và làm vỡ cấu trúc trang -> &lt;"""
    return _MATH.sub(lambda mo: mo.group(0).replace('<','&lt;'), h)
def autotex(h):
    """Bọc ký hiệu có chỉ số (q_L, f_rel, s_x, x_max…) thành KaTeX inline, bỏ qua thẻ HTML, công thức sẵn có, pre/code/svg/script."""
    h=safemath(h)
    out=[]
    for part in _SKIP.split(h):
        if part is None: continue
        if _SKIP.fullmatch(part): out.append(part); continue
        for rx,rep in _PAT: part=rx.sub(rep,part)
        out.append(part)
    return ''.join(out)
