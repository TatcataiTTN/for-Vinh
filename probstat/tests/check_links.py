"""Kiểm tra liên kết tĩnh: mọi href/src nội bộ trong HTML đã dựng phải trỏ tới tệp tồn tại; neo #id phải có trong trang đích.
Dùng: python3 tests/check_links.py <thư mục site> [thư mục gốc repo]   (liên kết đi ra ngoài thư mục site được kiểm trong gốc repo)"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
root = os.path.abspath(sys.argv[1]); repo = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else root
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links = []; s.ids = set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if tag == 'a' and a.get('name'): s.ids.add(a['name'])
        for k in ('href', 'src'):
            if k in a and a[k]: s.links.append((tag, k, a[k]))
cache = {}
def parse(path):
    if path not in cache:
        p = P(); p.feed(open(path, encoding='utf-8', errors='replace').read()); cache[path] = p
    return cache[path]
pages = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in ('node_modules', '.git', 'tests', 'build', 'data')]
    pages += [os.path.join(dp, f) for f in fn if f.endswith('.html')]
bad = []; n = 0; ext = 0
for pg in sorted(pages):
    for tag, k, h in parse(pg).links:
        u = urlparse(h)
        if u.scheme in ('http', 'https'): ext += 1; continue
        if u.scheme in ('mailto', 'data', 'javascript', 'tel'): continue
        n += 1
        tgt = os.path.normpath(os.path.join(os.path.dirname(pg), unquote(u.path))) if u.path else pg
        if os.path.isdir(tgt): tgt = os.path.join(tgt, 'index.html')
        if not os.path.exists(tgt): bad.append((os.path.relpath(pg, root), h, 'tệp không tồn tại')); continue
        if u.fragment and tgt.endswith('.html') and u.fragment not in parse(tgt).ids: bad.append((os.path.relpath(pg, root), h, 'neo không có'))
print(f'{len(pages)} trang HTML, {n} liên kết/tài nguyên nội bộ, {ext} liên kết ngoài (không kiểm); LỖI: {len(bad)}')
for b in bad[:25]: print(' ', b)
sys.exit(1 if bad else 0)
