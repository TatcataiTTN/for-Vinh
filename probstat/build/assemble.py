"""Ghép ngân hàng câu hỏi mỗi module: câu GỐC trước; bổ sung chỉ để phủ chủ đề (>= TOPIC_MIN câu/chủ đề) và đạt sàn MIN_TOTAL.
Cân bằng vị trí đáp án đúng, audit lệch vị trí/độ dài. Ghi ../data/qbank/<mid>.json"""
import sys, os, json, random, collections, importlib
sys.path.insert(0, os.path.dirname(__file__))
from qb import QB, fm
from modules import MODS
MIN_TOTAL = 240; CAP = 300; TOPIC_MIN = 8
LET = 'ABCD'
def audit(items):
    pos = collections.Counter(it['correct'] for it in items); n = len(items); exp = max(n, 1) / 4
    chi = sum((pos.get(i, 0) - exp) ** 2 / exp for i in range(4))
    multi = [it for it in items if len(set(len(o) for o in it['opts'])) > 1]
    longest = sum(1 for it in multi if len(it['opts'][it['correct']]) > max(len(o) for i, o in enumerate(it['opts']) if i != it['correct']))
    return dict(n=n, pos={LET[i]: pos.get(i, 0) for i in range(4)}, chi2=round(chi, 2), longest=round(longest / max(1, len(multi)), 3), n_multi=len(multi))
def run(mid):
    seed = int(mid[1:])
    Bo = QB(mid, seed); Bg = QB(mid + 'g', seed + 50)
    try: om = importlib.import_module('orig_' + mid)
    except ModuleNotFoundError: om = None
    try: gm = importlib.import_module('gen_' + mid)
    except ModuleNotFoundError: gm = None
    try: xm = importlib.import_module('ext_' + mid)
    except ModuleNotFoundError: xm = None
    if om: om.build(Bo)
    if gm: gm.build(Bg)
    if xm: xm.build(Bg)
    items = list(Bo.items); ess = list(Bo.essays)
    seen = {(i['q'], i['opts'][i['correct']]) for i in items}
    rng = random.Random(seed * 31)
    pool = [i for i in Bg.items if (i['q'], i['opts'][i['correct']]) not in seen]
    rng.shuffle(pool)
    cnt = collections.Counter(i['topic'] for i in items)
    add = []
    for it in list(pool):
        if cnt[it['topic']] < TOPIC_MIN: add.append(it); cnt[it['topic']] += 1; pool.remove(it)
    while len(items) + len(add) < MIN_TOTAL and pool: add.append(pool.pop())
    items += add
    for e in Bg.essays:
        if len(ess) < 24: ess.append(e)
    if len(items) > CAP:
        og = [i for i in items if i['origin'] == 'goc']; bs = [i for i in items if i['origin'] != 'goc']
        rng.shuffle(og); items = og[:CAP] if len(og) >= CAP else og + bs[:CAP - len(og)]
    targets = [i % 4 for i in range(len(items))]; rng.shuffle(targets)
    for it, t in zip(items, targets):
        c = it['correct']
        if c != t: it['opts'][c], it['opts'][t] = it['opts'][t], it['opts'][c]; it['correct'] = t
        assert len(set(it['opts'])) == 4, (mid, it['q'][:60], it['opts'])
    rng.shuffle(items)
    for it in items:
        if len(it['explain']) < 40: it['explain'] = it['explain'].rstrip() + ' Đáp án đúng: ' + it['opts'][it['correct']] + '.'
    for k, it in enumerate(items): it['id'] = f'{mid}-{k+1:03d}'
    for k, e in enumerate(ess): e['id'] = f'{mid}-E{k+1:02d}'
    meta = next(m for m in MODS if m['id'] == mid)
    out = dict(module=mid, name=meta['short'], items=items, essays=ess)
    p = os.path.join(os.path.dirname(__file__), '..', 'data', 'qbank', mid + '.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    a = audit(items); no = sum(1 for i in items if i['origin'] == 'goc')
    return dict(n=len(items), goc=no, bo_sung=len(items) - no, essays=len(ess), **{k: a[k] for k in ('pos', 'chi2', 'longest', 'n_multi')})
if __name__ == '__main__':
    ids = sys.argv[1:] or [m['id'] for m in MODS]
    rep = {}
    for mid in ids:
        if not os.path.exists(os.path.join(os.path.dirname(__file__), f'orig_{mid}.py')): continue
        rep[mid] = run(mid); print(mid, rep[mid])
    ap = os.path.join(os.path.dirname(__file__), '..', 'data', 'qbank', '_audit.json')
    old = json.load(open(ap)) if os.path.exists(ap) else {}
    old.update(rep); json.dump(old, open(ap, 'w'), ensure_ascii=False, indent=1)
