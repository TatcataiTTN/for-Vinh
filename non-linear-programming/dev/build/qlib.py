"""qlib — khai báo câu hỏi, xáo đáp án bằng seed cố định, audit thiên lệch.
Nguồn (src): G = gốc, lấy trực tiếp từ nội dung slide; B = bài tập/ví dụ gốc trong slide;
             T = tham khảo (Studocu/BTDOC, không tin cấu trúc đề); S = biên soạn thêm (chỉ khi thật cần)."""
import random, math, re
from collections import Counter

class Bank:
    def __init__(self, key):
        self.key = key; self.items = []

    # trắc nghiệm: correct = chuỗi đúng, wrong = list chuỗi sai
    def mc(self, src, ref, q, correct, wrong, explain, grp=None):
        assert 1 <= len(wrong) <= 3, q
        self.items.append(dict(t='mcq', src=src, ref=ref, q=q, correct_txt=correct, wrong=list(wrong), explain=explain, grp=grp))

    def tf(self, src, ref, q, truth, explain, grp=None):
        """Đúng/Sai: 2 lựa chọn cố định thứ tự Đúng, Sai (không xáo để tránh nhầm)."""
        self.items.append(dict(t='tf', src=src, ref=ref, q=q, truth=bool(truth), explain=explain, grp=grp))

    def num(self, src, ref, q, ans, explain, tol=1e-6, ans_text=None, grp=None):
        self.items.append(dict(t='num', src=src, ref=ref, q=q, ans=float(ans), tol=tol,
                               ans_text=ans_text if ans_text is not None else fmt(ans), explain=explain, grp=grp))

    def fix(self, q_prefix, correct=None, wrong=None):
        """Chỉnh đáp án của câu MCQ đã khai báo (dùng để cân bằng độ dài mà không sửa lời giải thích)."""
        hits = [i for i in self.items if i['t'] == 'mcq' and i['q'].startswith(q_prefix)]
        assert len(hits) == 1, (q_prefix, len(hits))
        if correct is not None: hits[0]['correct_txt'] = correct
        if wrong is not None: hits[0]['wrong'] = list(wrong)

    def essay(self, src, ref, q, model, check=None, grp=None):
        self.items.append(dict(t='essay', src=src, ref=ref, q=q, explain=model, check=check, grp=grp))

def fmt(x):
    if abs(x - round(x)) < 1e-9: return str(int(round(x)))
    return ('%.4f' % x).rstrip('0').rstrip('.')

def _plain(s):
    return re.sub(r'\\\(|\\\)|\\\[|\\\]|<[^>]+>|\\[a-zA-Z]+|[{}_^]', '', s)


def _len(o): return len(_plain(o))

def _trim_variants(t):
    """Các cách rút gọn đáp án ĐÚNG mà không mất nghĩa cốt lõi (phần giải thích đã nằm ở explain)."""
    outs = []
    m = re.sub(r'\s*\((?!\\)[^()]*\)\s*$', '', t)            # bỏ ngoặc chú thích cuối câu (không phải toán)
    if m != t and len(m) > 3: outs.append(m)
    for sep in [', vì ', ' vì ', ', nên ', ', do ', ' — ', ': ', '; ']:
        i = t.find(sep)
        if i > 6: outs.append(t[:i])
    return outs

def _flag(opts, c):
    L = [_len(o) for o in opts]
    others = [x for i, x in enumerate(L) if i != c]
    return L[c] >= 1.2 * max(others) and L[c] - max(others) >= 8

def finalize(bank, tries=400):
    """Xáo đáp án MCQ: chọn seed cho phân bố vị trí đúng đều nhất. Trả về (items_json, report)."""
    mcq = [i for i in bank.items if i['t'] == 'mcq']
    for it in mcq:
        opts0 = [it['correct_txt']] + it['wrong']
        if _flag(opts0, 0):
            for v in _trim_variants(it['correct_txt']):
                if not _flag([v] + it['wrong'], 0):
                    it['correct_txt'] = v; it['_trimmed'] = True; break
    best = None
    for seed in range(tries):
        rng = random.Random(seed * 7919 + 13)
        pos = Counter(); layout = []
        for it in mcq:
            opts = [it['correct_txt']] + it['wrong']
            rng.shuffle(opts)
            c = opts.index(it['correct_txt'])
            layout.append((opts, c)); pos[c] += 1
        n = len(mcq); k = 4
        dev = max(abs(pos.get(p, 0) - n / k) for p in range(k))
        if best is None or dev < best[0]:
            best = (dev, seed, layout, pos)
    _, seed, layout, pos = best
    out = []; li = 0
    for it in bank.items:
        d = dict(src=it['src'], ref=it.get('ref'), q=it['q'], grp=it.get('grp'))
        if it['t'] == 'mcq':
            opts, c = layout[li]; li += 1
            d.update(t='mcq', opts=opts, correct=c, explain=it['explain'])
        elif it['t'] == 'tf':
            d.update(t='mcq', opts=['Đúng', 'Sai'], correct=0 if it['truth'] else 1, explain=it['explain'])
        elif it['t'] == 'num':
            d.update(t='num', ans=it['ans'], tol=it['tol'], ans_text=it['ans_text'], explain=it['explain'])
        else:
            d.update(t='essay', explain=it['explain'], check=it.get('check'))
        out.append(d)
    # audit
    n4 = [it for it in out if it['t'] == 'mcq' and len(it['opts']) >= 3]
    longest = 0; ratios = []
    for it in n4:
        L = [len(_plain(o)) for o in it['opts']]
        others = [x for i, x in enumerate(L) if i != it['correct']]
        if L[it['correct']] >= 1.2 * max(others) and L[it['correct']] - max(others) >= 8: longest += 1
        it['_flag'] = L[it['correct']] >= 1.2 * max(others) and L[it['correct']] - max(others) >= 8
        ratios.append(L[it['correct']] / max(1, sum(others) / len(others)))
    tfs = [it for it in bank.items if it['t'] == 'tf']
    rep = dict(n_total=len(out), n_mcq4=len(n4), n_tf=len(tfs), n_num=sum(1 for i in out if i['t'] == 'num'),
               n_essay=sum(1 for i in out if i['t'] == 'essay'), seed=seed,
               pos={p: pos.get(p, 0) for p in range(4)},
               correct_obviously_longest=round(100 * longest / max(1, len(n4)), 1),
               mean_len_ratio=round(sum(ratios) / max(1, len(ratios)), 2),
               tf_true_pct=round(100 * sum(1 for t in tfs if t['truth']) / max(1, len(tfs)), 1),
               by_src=dict(Counter(i['src'] for i in bank.items)))
    return out, rep
