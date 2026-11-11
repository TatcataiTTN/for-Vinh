"""Audit toàn bộ ngân hàng câu hỏi (13 module): cấu trúc, trùng lặp, thiên lệch, đáp án so với giải thích. Chạy: python3 tests/audit_bank.py (từ thư mục probstat)"""
import json, re, glob, collections, math, sys
LET = 'ABCD'; probs = []; tot = 0
def num(s):
    s = s.replace('−', '-').replace(',', '.')
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]
allq = collections.defaultdict(list)
stats = []
for f in sorted(glob.glob('data/qbank/m*.json')):
    d = json.load(open(f, encoding='utf-8')); mid = d['module']; it = d['items']; tot += len(it)
    ids = [i['id'] for i in it]
    if len(set(ids)) != len(ids): probs.append((mid, 'id trùng'))
    pos = collections.Counter(); seen = collections.Counter(); hy = 0; noexp = 0; weird = 0; numbad = []
    for i in it:
        o = i['opts']; c = i['correct']
        if len(o) != 4 or len(set(o)) != 4: probs.append((mid, i['id'], 'không đủ 4 phương án khác nhau', o))
        if not (0 <= c < 4): probs.append((mid, i['id'], 'chỉ số đáp án sai', c))
        if not i['q'].strip() or not i['explain'].strip(): probs.append((mid, i['id'], 'đề hoặc giải thích rỗng'))
        if i['origin'] not in ('goc', 'bo_sung'): probs.append((mid, i['id'], 'origin lạ', i['origin']))
        if not i.get('src') or not i.get('topic'): probs.append((mid, i['id'], 'thiếu src/topic'))
        pos[c] += 1; seen[i['q']] += 1; allq[i['q'] + '||' + o[c]].append(mid)
        txt = i['q'] + ' ' + ' '.join(o) + ' ' + i['explain']
        if re.search(r'(?<![\w)\]}])-\d', i['q'] + ' ' + ' '.join(o)): hy += 1
        if re.search(r'\\\(|\\\[|<[a-z/]|&[a-z]+;|nan|inf\b|None|\{\}', txt): weird += 1; probs.append((mid, i['id'], 'ký tự lạ', txt[:90]))
        # số của đáp án đúng phải xuất hiện trong giải thích (dung sai làm tròn) — chỉ xét câu có đáp án thuần số
        cv = num(o[c]); ev = num(i['explain']) + [int(a) / int(b) for a, b in re.findall(r'(\d+)/(\d+)', i['explain']) if int(b)]
        close = lambda x, y: abs(x - y) <= max(0.0051, abs(x) * 0.0006) or abs(abs(x) - abs(y)) <= max(0.0051, abs(x) * 0.0006)
        if re.fullmatch(r'\(\s*-?[\d.]+;\s*-?[\d.]+\s*\)', o[c].strip()) and len(cv) == 2:      # khoảng (a; b): nửa độ rộng phải khớp sai số e trong giải thích
            if not (any(abs((cv[1] - cv[0]) / 2 - y) <= 0.0011 for y in ev) or all(any(abs(x - y) <= 0.00051 for y in ev) for x in cv)): numbad.append((i['id'], o[c], i['explain'][:70]))
        elif cv and len(cv) <= 2 and re.fullmatch(r'[-−\d.,\s;()]+', o[c].strip()) and not (len(cv) == 1 and cv[0] == int(cv[0]) and abs(cv[0]) <= 10):
            if not all(any(close(x, y) for y in ev) for x in cv): numbad.append((i['id'], o[c], i['explain'][:70]))
    dup = [q for q, k in seen.items() if k > 1]
    n = len(it); exp = n / 4; chi = sum((pos[k] - exp) ** 2 / exp for k in range(4))
    multi = [i for i in it if len({len(x) for x in i['opts']}) > 1]
    lg = sum(1 for i in multi if len(i['opts'][i['correct']]) > max(len(x) for k, x in enumerate(i['opts']) if k != i['correct'])) / max(1, len(multi))
    gc = sum(1 for i in it if i['origin'] == 'goc')
    stats.append((mid, n, gc, len(d['essays']), round(chi, 2), round(lg, 3), len(dup), hy, len(numbad)))
    if dup: probs.append((mid, 'đề trùng trong cùng module', len(dup), dup[:2]))
    if chi > 5: probs.append((mid, 'lệch vị trí đáp án chi2', chi))
    if lg > 0.40: probs.append((mid, 'đáp án đúng quá hay dài nhất', lg))
    for e in d['essays']:
        if not e['q'].strip() or not e['sol'].strip(): probs.append((mid, 'bài tự luận rỗng'))
    if numbad: probs.append((mid, 'đáp án số không thấy trong giải thích', len(numbad), numbad[:3]))
print(f'{"mod":4} {"MCQ":>4} {"gốc":>4} {"luận":>4} {"chi²":>5} {"dài":>5} {"đề trùng":>8} {"gạch-nối":>8} {"số≠giải thích":>13}')
for s in stats: print(f'{s[0]:4} {s[1]:>4} {s[2]:>4} {s[3]:>4} {s[4]:>5} {s[5]:>5} {s[6]:>8} {s[7]:>8} {s[8]:>13}')
print('tổng', tot, 'câu;', sum(s[3] for s in stats), 'tự luận')
cross = [k for k, v in allq.items() if len(v) > 1 and len(set(v)) < len(v)]
print('trùng (đề + đáp án) trong cùng module:', len(cross))
print('VẤN ĐỀ:', len(probs)); [print(' ', p) for p in probs[:25]]
sys.exit(1 if probs else 0)
