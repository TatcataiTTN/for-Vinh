"""Module 2 — biến thể tham số (bo_sung), đáp án tính bằng công thức và kiểm bằng vét cạn khi nhỏ."""
import math, itertools, random
from math import comb, perm, factorial as fac
from collections import Counter
from qb import f, fg, nd, ni
from orig_m02 import TOP, G
SRC = 'Bổ sung: biến thể tham số của dạng bài §1.2–1.3 / PS 24.4 (đáp án tự tính, kiểm vét cạn khi cỡ nhỏ)'
def build(B):
    rng = random.Random(1202)
    def add(stem, ans, wrong, expl, lvl, topic):
        wl = [w for w in wrong if w != ans]
        for w in (ans * 2, max(1, ans // 2), ans + max(1, ans // 9), max(1, ans - max(1, ans // 7)), ans * 3, ans + 1, ans + 2):
            if w != ans and w not in wl and len(set(wl)) < 5: wl.append(w)
        B.mcq(stem, G(ans), [G(w) for w in wl], expl, lvl, topic, SRC, 'bo_sung')
    # 1. Hoán vị có lặp (từ)
    for w in ['STATISTICS', 'MISSISSIPPI', 'PROBABILITY', 'BANANA', 'MATHEMATICS', 'ALGORITHM', 'DATA', 'SAMPLE', 'NORMAL', 'ESTIMATE']:
        c = Counter(w); n = len(w); ans = fac(n)
        for v in c.values(): ans //= fac(v)
        if n <= 8: assert ans == len(set(itertools.permutations(w)))
        rep = ' · '.join(f'{k}×{v}' for k, v in c.items() if v > 1) or 'không có chữ lặp'
        add(f'Có bao nhiêu cách sắp xếp các chữ cái của từ “{w}” (phân biệt các chữ khác nhau, coi các chữ giống nhau là như nhau)?', ans, [fac(n), fac(n) // max(c.values()), comb(n, 2)],
            f'n = {n}; lặp: {rep}. Số hoán vị phân biệt = n!/(n₁!n₂!…) = {G(ans)}.', 2, TOP['perm'])
    # 2. Chỉnh hợp / mật khẩu
    for n, k in [(10, 4), (26, 3), (8, 5), (9, 3), (36, 4), (7, 7)]:
        add(f'Một mật khẩu gồm {k} ký tự lấy từ bảng {n} ký tự, các ký tự đôi một khác nhau. Có bao nhiêu mật khẩu?', perm(n, k), [n ** k, comb(n, k), fac(n)],
            f'Chỉnh hợp không lặp A({n},{k}) = {n}!/({n}−{k})! = {G(perm(n, k))} (nếu cho phép lặp thì là {n}^{k} = {G(n ** k)}).', 1, TOP['perm'])
        add(f'Một mật khẩu gồm {k} ký tự lấy từ bảng {n} ký tự, cho phép lặp. Có bao nhiêu mật khẩu?', n ** k, [perm(n, k), comb(n, k), n * k],
            f'Mỗi vị trí có {n} lựa chọn độc lập ⇒ {n}^{k} = {G(n ** k)} (chỉnh hợp lặp).', 1, TOP['rule'])
    # 3. Tổ hợp
    for n, k in [(12, 5), (20, 3), (40, 6), (15, 4), (30, 2), (49, 6)]:
        add(f'Chọn nhóm {k} người từ {n} người, không phân biệt thứ tự. Có bao nhiêu cách?', comb(n, k), [perm(n, k), n ** k, comb(n, k) * 2],
            f'C({n},{k}) = {n}!/({k}!·{n - k}!) = {G(comb(n, k))}.', 1, TOP['comb'])
    # 4. Chọn nhóm có điều kiện
    for (a, b, x, y) in [(8, 6, 3, 2), (10, 7, 4, 3), (12, 9, 2, 2), (7, 5, 3, 3), (9, 8, 4, 1), (11, 6, 5, 2)]:
        add(f'Lớp có {a} nam và {b} nữ. Chọn nhóm gồm {x} nam và {y} nữ. Có bao nhiêu cách?', comb(a, x) * comb(b, y), [comb(a + b, x + y), comb(a, x) + comb(b, y), perm(a, x) * perm(b, y)],
            f'C({a},{x})·C({b},{y}) = {G(comb(a, x))} · {G(comb(b, y))} = {G(comb(a, x) * comb(b, y))}.', 2, TOP['mix'])
        # ít nhất 1 nữ
        t = x + y
        ans = comb(a + b, t) - comb(a, t)
        brute = sum(comb(b, j) * comb(a, t - j) for j in range(1, t + 1))
        assert ans == brute
        add(f'Lớp có {a} nam và {b} nữ. Chọn nhóm {t} người. Có bao nhiêu cách để nhóm có ÍT NHẤT 1 nữ?', ans, [comb(a + b, t), comb(b, 1) * comb(a + b - 1, t - 1), comb(a + b, t) - comb(b, t)],
            f'Biến cố bù: nhóm toàn nam ⇒ C({a + b},{t}) − C({a},{t}) = {G(comb(a + b, t))} − {G(comb(a, t))} = {G(ans)}. (Cách C(b,1)·C(a+b−1,t−1) đếm trùng.)', 3, TOP['mix'])
    # 5. Xếp chỗ có ràng buộc
    for n in (5, 6, 7, 8):
        ans = fac(n - 1) * 2
        if n <= 7: assert ans == sum(1 for p in itertools.permutations(range(n)) if abs(p.index(0) - p.index(1)) == 1)
        add(f'Xếp {n} người thành một hàng ngang. Có bao nhiêu cách xếp sao cho hai người A và B ngồi cạnh nhau?', ans, [fac(n), fac(n - 1), fac(n) - ans],
            f'Dán A, B thành 1 khối: (n−1)! = {fac(n-1)} cách xếp khối cùng các người còn lại, nhân 2 cho thứ tự trong khối ⇒ {G(ans)}.', 3, TOP['perm'])
        ans2 = fac(n) - ans
        add(f'Xếp {n} người thành một hàng ngang. Có bao nhiêu cách xếp sao cho hai người A và B KHÔNG ngồi cạnh nhau?', ans2, [ans, fac(n - 2) * 2, fac(n) // 2],
            f'Bù: tổng n! = {G(fac(n))} trừ số cách A, B cạnh nhau {G(ans)} ⇒ {G(ans2)}.', 3, TOP['perm'])
    for n in (4, 5, 6, 7, 8):
        add(f'Xếp {n} người ngồi quanh một bàn tròn (các cách xoay vòng coi là như nhau). Số cách là', fac(n - 1), [fac(n), fac(n - 1) * 2, fac(n - 2)],
            f'Hoán vị vòng: (n−1)! = {G(fac(n-1))}.', 2, TOP['perm'])
    # 6. Quy tắc nhân / số tự nhiên
    for d in (3, 4, 5):
        digs = list(range(10))
        ans = 9 * 9 * 8 if d == 3 else 9 * 9 * 8 * 7 if d == 4 else 9 * 9 * 8 * 7 * 6
        if d == 3: assert ans == sum(1 for t in itertools.permutations(digs, 3) if t[0] != 0)
        add(f'Có bao nhiêu số tự nhiên có {d} chữ số, các chữ số đôi một khác nhau?', ans, [10 ** d, 9 * 10 ** (d - 1), perm(10, d)],
            f'Chữ số đầu ≠ 0 (9 cách), các vị trí còn lại lấy tiếp từ các chữ số chưa dùng ⇒ {G(ans)}.', 2, TOP['rule'])
    for n in (10, 12, 20, 30):
        add(f'Từ {n} đội, cần chọn ra một đội trưởng và một đội phó (khác nhau). Có bao nhiêu cách?', n * (n - 1), [comb(n, 2), n * n, 2 * n],
            f'Có thứ tự (hai chức danh khác nhau): A({n},2) = {n}·{n-1} = {n*(n-1)}. (Chọn 2 đội không phân biệt chức danh chỉ có C({n},2) = {comb(n,2)}.)', 1, TOP['perm'])
    # 7. Xác suất cổ điển bằng đếm
    for n, k in [(10, 3), (20, 5), (30, 4), (15, 3)]:
        p = 1 / comb(n, k)
        B.mcq(f'Bốc thăm ngẫu nhiên {k} số trong {n} số (không hoàn lại, không phân biệt thứ tự). Xác suất bốc trúng đúng bộ {k} số đã chọn trước là', f(p, 6), nd(p, rng, 6, extra=[1 / n ** k, 1 / perm(n, k) * 2, k / n]),
              f'P = 1/C({n},{k}) = 1/{G(comb(n, k))} = {f(p, 6)}.', 2, TOP['prob'], SRC, 'bo_sung')
    for tot, good, k in [(20, 5, 3), (30, 8, 4), (50, 10, 5), (12, 4, 3)]:
        p = comb(good, k) / comb(tot, k)
        B.mcq(f'Lô {tot} sản phẩm có {good} sản phẩm lỗi. Chọn ngẫu nhiên {k} sản phẩm. Xác suất cả {k} đều lỗi là', f(p, 5), nd(p, rng, 5, extra=[(good / tot) ** k, k * good / tot, 1 - p]),
              f'P = C({good},{k})/C({tot},{k}) = {G(comb(good, k))}/{G(comb(tot, k))} = {f(p, 5)} (rút có hoàn lại sẽ là ({good}/{tot})^{k} = {f((good/tot)**k, 5)}).', 3, TOP['prob'], SRC, 'bo_sung')
    # 8. Số tập con / biến cố
    for n in (3, 4, 5, 6, 8, 10):
        add(f'Tập S có {n} phần tử. Có bao nhiêu biến cố (tập con) của S, kể cả ∅ và S?', 2 ** n, [n * n, fac(n), 2 * n],
            f'Mỗi phần tử thuộc hoặc không thuộc tập con: 2^{n} = {G(2 ** n)}.', 1, TOP['space'])
    for p_, q_, r_ in [(30, 20, 8), (40, 25, 10), (50, 30, 12), (100, 60, 25)]:
        add(f'Trong {p_ + q_ - r_} sinh viên, {p_} học môn A, {q_} học môn B và {r_} học cả hai (mỗi sinh viên học ít nhất một môn). Tổng số sinh viên theo đếm hợp là |A ∪ B| = ?', p_ + q_ - r_, [p_ + q_, p_ + q_ + r_, p_ * q_ // r_],
            f'|A ∪ B| = |A| + |B| − |A ∩ B| = {p_} + {q_} − {r_} = {p_ + q_ - r_}.', 2, TOP['ops'])
    for t in (4, 6, 8):
        add(f'Gieo {t // 2 + 1} đồng xu cân đối. Số kết cục của không gian mẫu là', 2 ** (t // 2 + 1), [t, (t // 2 + 1) * 2, (t // 2 + 1) ** 2],
            f'Mỗi đồng xu có 2 kết cục: 2^{t // 2 + 1} = {2 ** (t // 2 + 1)}.', 1, TOP['space'])
    for r in (4, 5, 8, 10):
        add(f'Số tổ hợp có lặp chập 3 từ {r} loại đối tượng (ví dụ chọn 3 viên kẹo từ {r} vị, chọn tùy ý số lượng mỗi vị) là', comb(r + 2, 3), [comb(r, 3), r ** 3, perm(r, 3)],
            f'C(n + k − 1, k) = C({r + 2},3) = {G(comb(r + 2, 3))}.', 3, TOP['comb'])
