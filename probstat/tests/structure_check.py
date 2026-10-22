"""Kiểm tra cấu trúc HTML mọi trang module: thẻ cân bằng và thanh điều khiển nằm trong .mdeck (lỗi '<' thô trong công thức)."""
import glob, sys
from html.parser import HTMLParser
VOID={'br','img','input','hr','meta','link','path','circle','line','rect','polyline','polygon','ellipse','source'}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.bad=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append((t,s.getpos()))
    def handle_endtag(s,t):
        if t in VOID: return
        if s.st and s.st[-1][0]==t: s.st.pop()
        else:
            s.bad.append((t,s.getpos()))
            for i in range(len(s.st)-1,-1,-1):
                if s.st[i][0]==t: del s.st[i:]; break
fail=0
for f in sorted(glob.glob('vi/**/index.html',recursive=True)):
    p=P(); p.feed(open(f).read())
    if p.bad or p.st: fail+=1; print('LỖI',f,p.bad[:2],p.st[:2])
print('cấu trúc HTML:', 'OK' if not fail else f'{fail} trang lỗi'); sys.exit(1 if fail else 0)
