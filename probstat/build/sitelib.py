import os, json, html
from hx import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))   # .../probstat
from modules import MODS, BY
SITE = 'Xác suất thống kê · Phenikaa'
NAV = [('Trang chủ', '{r}vi/index.html'), ('Lộ trình', '{r}vi/index.html#lo-trinh'), ('Luyện đề', '{r}vi/luyen-de/index.html'), ('Cấu trúc đề', '{r}vi/cau-truc-de/index.html'), ('Đề giữa kỳ', '{r}vi/de-giua-ky/index.html'), ('Đề giữa kỳ 2', '{r}vi/de-giua-ky-2/index.html'), ('Bài mẫu tự luận', '{r}vi/bai-mau-tu-luan/index.html'),
       ('Bảng tra', '{r}vi/bang-tra/index.html'), ('Tài liệu', '{r}vi/tai-lieu/index.html')]
SRC = [('Lecture Notes XSTK — Cao Hoàng Nam & Vũ Hữu Nhự (08/2021)', 'giáo trình tiếng Việt, 4 chương + bài tập'),
       ('Kreyszig — Advanced Engineering Mathematics, Part G (Ch. 24–25)', 'giáo trình chính [1] trong đề cương'),
       ('Đề cương chi tiết học phần FFS703010', 'cấu trúc 5 bài học, đánh giá'),
       ('Đề giữa kỳ mẫu (LTXSTK) và đáp án giữa kỳ HK2 2022–2023', 'đề ảnh, đã OCR/đọc lại thủ công'),
       ('Đề thi và đáp án cuối kỳ 2021–2022 (3TC), 2022–2023 HK1 (2TC, K16), 2022–2023 HK2 (3TC), đề mẫu FFS703010 (03/2024)', 'đề gốc và đáp án chấm')]
def src_list():
    return ''.join(f'<li>{html.escape(n)} · {html.escape(d)}</li>' for n, d in SRC)
def page(title, body, depth, desc='', scripts=(), math=True):
    r = '../' * depth
    nav = ''.join(f'<a href="{u.format(r=r)}">{t}</a>' for t, u in NAV)
    sc = ''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    km = ''
    kb = ''
    if math:
        km = f'<link rel="stylesheet" href="{r}_shared/katex/katex.min.css">'
        kb = (f'<script src="{r}_shared/katex/katex.min.js"></script><script src="{r}_shared/katex/auto-render.min.js"></script>'
              '<script>document.addEventListener("DOMContentLoaded",function(){try{renderMathInElement(document.body,{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}],ignoredClasses:["quiz","qitem"],throwOnError:false})}catch(e){}})</script>')
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · {SITE}</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%276%27 fill=%27%23b3122f%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 text-anchor=%27middle%27 fill=%27white%27%3E%CF%83%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="{r}_shared/common.css">{km}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}vi/index.html">📊 Xác suất thống kê · Phenikaa</a><nav>{nav}
<details class="menu"><summary>🎨 Giao diện</summary><div class="pop"><button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr><button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button></div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p><b>Nguồn tài liệu</b> (học phần Lý thuyết xác suất thống kê, mã FFS703010, Đại học Phenikaa):</p><ul style="margin:.3em 0 .8em;padding-left:1.2em">{src_list()}</ul>
<p>Tài liệu tự học không chính thức của người học, dựa trên các nguồn trên. Mọi đáp án số đều được tính bằng chương trình (Python/SciPy) và đối chiếu độc lập; câu có nhãn “📎 Câu gốc” lấy từ tài liệu, câu có nhãn “➕ Bổ sung” là biến thể do người biên soạn tạo thêm. Nếu phát hiện sai sót vui lòng báo lại; đối chiếu đề cương chính thức của giảng viên khi cần. Nội dung gốc thuộc Đại học Phenikaa và các tác giả tương ứng.</p></div></footer>
<script src="{r}_shared/theme.js"></script>{kb}{sc}</body></html>'''
def write(relpath, content):
    p = os.path.join(ROOT, relpath); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)
def load_bank(mid): return json.load(open(os.path.join(ROOT, 'data', 'qbank', mid + '.json'), encoding='utf-8'))
