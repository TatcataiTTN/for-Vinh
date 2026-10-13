"""Ngân hàng câu hỏi XSTK: mỗi câu có nguồn, nhãn gốc/bổ sung, đáp án tự tính + giải thích.
Văn bản thuần (không HTML): bank.js chèn bằng textContent."""
import random, hashlib, re, math

def fm(s):
    return re.sub(r'(?<![\w\)\]\}])-(?=[\d(])', '−', s) if isinstance(s, str) else s

def f(x, d=3):
    """Định dạng số: d chữ số thập phân, dấu trừ chuẩn, bỏ '-0'."""
    s = f"{x:.{d}f}"
    if float(s) == 0: s = f"{0:.{d}f}"
    return s.replace('-', '−')

def fg(x, d=4):
    """Số gọn (bỏ số 0 thừa)."""
    s = f"{x:.{d}f}".rstrip('0').rstrip('.')
    if s in ('', '-0'): s = '0'
    return s.replace('-', '−')

def nd(ans, rng, d=3, k=3, extra=(), lo=None, hi=None):
    """Sinh phương án nhiễu số thực quanh ans: lỗi thường gặp (extra) rồi các số lân cận cùng định dạng."""
    out = []
    key = f(ans, d)
    def push(v):
        if v is None or not math.isfinite(v): return
        if lo is not None and v < lo: return
        if hi is not None and v > hi: return
        s = f(v, d)
        if s != key and s not in out: out.append(s)
    for v in extra: push(v)
    step = 10 ** (-d)
    scale = max(abs(ans), 1e-9)
    tries = 0
    while len(out) < max(k + 3, 6) and tries < 400:
        tries += 1
        c = rng.choice([1, 2, 3, 5, 10, 20, 50])
        sgn = rng.choice([-1, 1])
        v = ans + sgn * (c * step * max(1, round(scale * 10 ** d / 200)))
        push(v)
    return out

def ni(ans, rng, k=3, extra=(), lo=0):
    """Phương án nhiễu số nguyên."""
    out = []
    def push(v):
        v = int(round(v))
        if v < lo or v == ans or str(v) in out: return
        out.append(str(v))
    for v in extra: push(v)
    tries = 0
    spread = max(2, abs(ans) // 8 + 1)
    while len(out) < k + 3 and tries < 300:
        tries += 1
        push(ans + rng.choice([-3, -2, -1, 1, 2, 3, rng.randint(-spread, spread) or 1]))
    return out

class QB:
    def __init__(self, mid, seed=1):
        self.mid = mid
        self.rng = random.Random(seed * 1000 + 7)
        self.items = []
        self.essays = []
        self.seen = set()

    def mcq(self, stem, correct, wrong, explain, level=1, topic='', src='', origin='goc'):
        stem = fm(stem); explain = fm(explain); correct = fm(str(correct))
        wrong = [fm(str(w)) for w in wrong]
        uniq = []
        for w in wrong:
            if w != correct and w not in uniq: uniq.append(w)
        if len(uniq) < 3:
            raise ValueError(f'{self.mid}: thiếu phương án nhiễu: {stem[:60]} | {correct} | {uniq}')
        key = hashlib.md5((stem + '||' + correct).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key)
        opts = [correct] + uniq[:3]
        self.rng.shuffle(opts)
        self.items.append(dict(q=stem, opts=opts, correct=opts.index(correct), explain=explain,
                               level=level, topic=topic, src=src, origin=origin))
        return True

    def tf(self, stem, truth, explain, level=1, topic='', src='', origin='goc'):
        """Câu đúng/sai: 4 phương án cố định để dùng chung khung A–D."""
        opts_true = ['Đúng', 'Sai']
        wrong = ['Chỉ đúng một phần', 'Không đủ dữ kiện để kết luận']
        return self.mcq(stem, 'Đúng' if truth else 'Sai', ['Sai' if truth else 'Đúng'] + wrong, explain, level, topic, src, origin)

    def essay(self, stem, sol, level=2, topic='', src='', origin='goc'):
        stem = fm(stem); sol = fm(sol)
        key = hashlib.md5(('E' + stem).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key)
        self.essays.append(dict(q=stem, sol=sol, level=level, topic=topic, src=src, origin=origin))
        return True
