#!/usr/bin/env python3
"""Sinh site tĩnh non-linear-programming từ nội dung Python. Không gõ tay số liệu: dùng verify/results.json.
Chạy: python3 NLP-work/build/gen_site.py [m0 m1 m2 m3 home]"""
import os, sys, json, subprocess, html, importlib, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'for-Vinh', 'non-linear-programming')
BUILD = os.path.join(ROOT, 'NLP-work', 'build')
sys.path.insert(0, BUILD)
R = json.load(open(os.path.join(ROOT, 'NLP-work', 'verify', 'results.json'), encoding='utf-8'))
import qlib

SLIDE_PDF = {
    'm1': os.path.join(ROOT, 'Slides', '1_Kien thuc ve ham loi va tap loi_250418.pdf'),
    'm2': os.path.join(ROOT, 'Slides', '2_NonlinearProgram_KKT_250418.pdf'),
    'm3': os.path.join(ROOT, 'Slides', '3_QuadraticPrograming_250419a.pdf'),
}
MODULES = [
    dict(key='m0', slug='00-tien-quyet', num=0, title='Kiến thức tiên quyết', short='Đại số tuyến tính, giải tích nhiều biến, ngôn ngữ tối ưu, ôn QHTT'),
    dict(key='m1', slug='01-tap-loi-ham-loi', num=1, title='Tập lồi và hàm lồi', short='Slide 1 (54 tr.): tập lồi, bao lồi, siêu phẳng, hàm lồi, Hessian'),
    dict(key='m2', slug='02-rang-buoc-kkt', num=2, title='Tối ưu có ràng buộc và điều kiện KKT', short='Slide 2 (68 tr.): Lagrange, KKT, Slater, điều kiện cần và đủ'),
    dict(key='m3', slug='03-quy-hoach-toan-phuong', num=3, title='Quy hoạch toàn phương', short='Slide 3 (81 tr.): tồn tại nghiệm, null space, tập hoạt động'),
]

from helpers import *

# ------------------------------------------------------------------ khung trang
HEAD = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Tối ưu hóa phi tuyến & lồi</title>
<meta name="description" content="{desc}"><link rel="icon" href="data:,">
<script>(function(){{try{{var t=localStorage.getItem('nlp-theme');if(t==='dark')document.documentElement.setAttribute('data-theme','dark');}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{up}shared/katex/katex.min.css">
<link rel="stylesheet" href="{up}shared/common.css">
</head><body>
<header class="topbar"><a class="brand" href="{up}index.html">∇ Tối ưu hóa</a>
<nav>{nav}</nav><button id="theme-btn" type="button" title="Đổi giao diện sáng/tối">◐</button></header>
<main>'''
FOOT = '''</main>
<script src="{up}shared/katex/katex.min.js"></script>
<script src="{up}shared/katex/auto-render.min.js"></script>
<script src="{up}shared/deck.js"></script>
<script src="{up}shared/widgets.js"></script>
{quizjs}
</body></html>'''

def ready(m): return os.path.exists(os.path.join(BUILD, 'c_' + m['key'] + '.py'))

def nav(up, active):
    links = [('index.html', 'Trang chủ', 'home')] + [(f'modules/{m["slug"]}/index.html', f'Module {m["num"]}', m['key']) for m in MODULES if ready(m)] + [('code/index.html', 'Code', 'code'), ('kiem-chung/index.html', 'Kiểm chứng', 'kc'), ('phat-trien/index.html', 'Phát triển', 'dev')]
    return ''.join(f'<a href="{up}{h}" class="{"on" if k == active else ""}">{t}</a>' for h, t, k in links)

def page(path, title, desc, body, active, up, quiz=None):
    quizjs = ''
    if quiz is not None:
        quiz = dict(quiz, items=[fixmath_obj(i) for i in quiz['items']])
        quizjs = f'<script type="application/json" id="quiz-data">{json.dumps(quiz, ensure_ascii=False).replace("</", "<\\/")}</script>\n<script src="{up}shared/quiz.js"></script>'
    body = fixmath(body)
    out = HEAD.format(title=esc(title), desc=esc(desc), up=up, nav=nav(up, active)) + body + FOOT.format(up=up, quizjs=quizjs)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(out)

# ------------------------------------------------------------------ module page
def build_module(meta):
    mod = importlib.import_module('c_' + meta['key'])
    importlib.reload(mod)
    qmod = importlib.import_module('q_' + meta['key'])
    importlib.reload(qmod)
    items, rep = qlib.finalize(qmod.bank)
    print(meta['key'], 'câu hỏi:', json.dumps(rep, ensure_ascii=False))
    json.dump(rep, open(os.path.join(ROOT, 'NLP-work', 'verify', f'quiz_report_{meta["key"]}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    RM = [m for m in MODULES if ready(m)]
    idx = RM.index(meta)
    prev_l = f'<a href="../{RM[idx-1]["slug"]}/index.html">← Module {RM[idx-1]["num"]}: {RM[idx-1]["title"]}</a>' if idx > 0 else '<span></span>'
    next_l = f'<a href="../{RM[idx+1]["slug"]}/index.html">Module {RM[idx+1]["num"]}: {RM[idx+1]["title"]} →</a>' if idx < len(RM) - 1 else '<span></span>'
    toc = [('bai-giang', 'Bài giảng (deck)')] + [(sid, st) for sid, st, _ in mod.SECTIONS] + [('quiz', f'Ngân hàng {rep["n_total"]} câu hỏi')]
    b = f'<p class="tag">MODULE {meta["num"]}</p><h1>{meta["title"]}</h1><p class="lead">{mod.LEAD}</p>'
    b += '<div class="meta">' + ''.join(f'<span class="tag">{m}</span>' for m in mod.META) + '</div>'
    b += '<div class="toc">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in toc) + '</div>'
    b += callout('info', 'Mục tiêu học tập', '<ul>' + ''.join(f'<li>{o}</li>' for o in mod.OBJECTIVES) + '</ul>')
    b += '<h2 id="bai-giang">Bài giảng</h2><p style="color:var(--muted);font-size:.9rem">Dùng phím ← → hoặc các nút để chuyển slide; bấm chấm tròn để nhảy tới slide bất kỳ; “Toàn màn hình” để trình chiếu. Mỗi slide có khung “📖 Giải thích cho người mới bắt đầu”' + (' và ảnh gốc trang slide của giảng viên' if meta['key'] != 'm0' else '') + '.</p>'
    b += deck(mod.DECK)
    for sid, st, html_ in mod.SECTIONS:
        b += f'<h2 id="{sid}">{st}</h2>{html_}'
    b += f'<h2 id="quiz">Ngân hàng câu hỏi ({rep["n_total"]} câu)</h2>'
    b += (f'<p>Gồm <b>{rep["n_mcq4"] + rep["n_tf"]}</b> câu trắc nghiệm (gồm {rep["n_tf"]} câu đúng/sai), <b>{rep["n_num"]}</b> câu điền số và <b>{rep["n_essay"]}</b> câu tự luận có đáp án mẫu. '
          'Bấm một đáp án là biết đúng/sai ngay và có <b>giải thích</b>; mỗi câu có nút “↺ Làm lại câu này”, cuối bài có “↺ Làm lại toàn bộ bài”. '
          'Mỗi câu gắn nhãn nguồn: <span class="badge ok">từ slide</span> · <span class="badge mid">tham khảo</span> · <span class="badge no">biên soạn thêm</span>.</p>')
    b += '<div class="quiz"><div id="quiz-root"></div></div>'
    b += f'<div class="callout hist"><span class="ct"><b>Đọc thêm</b></span>{mod.READING}</div>'
    b += f'<p style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:30px">{prev_l}{next_l}</p>'
    b += '<div class="foot">Nội dung bám sát slide của ORLab (Phenikaa) và giáo trình Boyd &amp; Vandenberghe. Mọi con số được sinh từ script kiểm chứng (thư mục <code>NLP-work/verify</code> trong dự án).</div>'
    page(os.path.join(SITE, 'modules', meta['slug'], 'index.html'), f'Module {meta["num"]}: {meta["title"]}', meta['short'], b, meta['key'], '../../',
         quiz={'key': meta['key'], 'items': items})
    return rep

def build_home(reps):
    hm = importlib.import_module('c_home'); importlib.reload(hm)
    b = hm.body(MODULES, reps, fig('d5-lo-trinh', 'Lộ trình bốn module', up=0))
    page(os.path.join(SITE, 'index.html'), 'Tối ưu hóa phi tuyến và tối ưu lồi', 'Bài giảng tự học 4 module bám slide ORLab Phenikaa: tập lồi, hàm lồi, KKT, quy hoạch toàn phương.', b, 'home', '')

def build_verify():
    kc = importlib.import_module('c_kc'); importlib.reload(kc)
    page(os.path.join(SITE, 'kiem-chung', 'index.html'), 'Kiểm chứng số liệu và ghi chú về slide', 'Các chỗ slide chưa khớp khi kiểm chứng bằng code, nguồn tài liệu.', kc.body(R), 'kc', '../')

def build_code():
    cc = importlib.import_module('c_code'); importlib.reload(cc)
    b, ex = cc.body()
    page(os.path.join(SITE, 'code', 'index.html'), 'Thực hành code', 'Giải bài tối ưu bằng Python, cvxpy, scipy: ví dụ slide, bài tập chấm tự động.', b, 'code', '../')
    # nạp pyrunner sau quiz: chèn script
    p = os.path.join(SITE, 'code', 'index.html'); h = open(p, encoding='utf-8').read()
    h = h.replace('</body>', cc.data_script(ex) + '\n<script src="../shared/pyrunner.js"></script>\n</body>'); open(p, 'w', encoding='utf-8').write(h)

def build_dev():
    cd = importlib.import_module('c_dev'); importlib.reload(cd)
    page(os.path.join(SITE, 'phat-trien', 'index.html'), 'Tài liệu phát triển', 'Kiến trúc, quy trình sinh site, thêm nội dung, kiểm thử và deploy.', cd.body(), 'dev', '../')

if __name__ == '__main__':
    want = sys.argv[1:] or ['m0', 'm1', 'm2', 'm3', 'home', 'kc', 'code', 'dev']
    reps = {}
    for m in MODULES:
        p = os.path.join(ROOT, 'NLP-work', 'verify', f'quiz_report_{m["key"]}.json')
        if os.path.exists(p): reps[m['key']] = json.load(open(p, encoding='utf-8'))
    for m in MODULES:
        if m['key'] in want and ready(m):
            reps[m['key']] = build_module(m)
    if 'home' in want: build_home(reps)
    if 'kc' in want: build_verify()
    if 'code' in want: build_code()
    if 'dev' in want: build_dev()
    print('xong')
