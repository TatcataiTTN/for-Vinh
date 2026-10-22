"""Module 2 — mở rộng: khái niệm + họ bài đếm (đáp án tính bằng công thức, kiểm vét cạn khi cỡ nhỏ)."""
import math, itertools, random
from math import comb, perm, factorial as fac
from qb import f, fg
from orig_m02 import TOP, G
SRC = 'Bổ sung: dạng bài §1.2–1.3 / Kreyszig PS 24.4 (đáp án tự tính, kiểm vét cạn khi cỡ nhỏ)'
def build(B):
    rng = random.Random(2502)
    def add(stem, ans, wrong, expl, lvl, topic):
        wl = [w for w in wrong if w != ans]
        for w in (ans * 2, max(1, ans // 2), ans + max(1, ans // 9), max(1, ans - max(1, ans // 7)), ans * 3, ans + 1, ans + 2):
            if w != ans and w not in wl and len(set(wl)) < 5: wl.append(w)
        B.mcq(stem, G(ans), [G(w) for w in wl], expl, lvl, topic, SRC, 'bo_sung')
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Hai biến cố A, B xung khắc nghĩa là', 'A ∩ B = ∅', ['A ∪ B = S', 'A ⊂ B', 'P(A) = P(B)'], 'Không thể cùng xảy ra.', 1, 'ops')
    C('Biến cố đối của “có ít nhất một mặt sấp khi tung 3 đồng xu” là', 'cả ba đều ngửa', ['có đúng một mặt ngửa', 'cả ba đều sấp', 'có ít nhất hai mặt ngửa'], 'Phủ định của “ít nhất một” là “không có”.', 1, 'ops')
    C('(A ∪ B)ᶜ bằng', 'Aᶜ ∩ Bᶜ', ['Aᶜ ∪ Bᶜ', 'A ∩ B', 'Aᶜ'], 'Luật De Morgan.', 1, 'ops')
    C('Nếu A ⊂ B thì A ∩ B bằng', 'A', ['B', '∅', 'S'], 'Giao của tập con với tập chứa nó là chính tập con.', 1, 'ops')
    C('|A ∪ B| bằng', '|A| + |B| − |A ∩ B|', ['|A| + |B|', '|A|·|B|', '|A| − |B|'], 'Công thức bù trừ cho hai tập.', 1, 'ops')
    C('Quy tắc nhân áp dụng khi', 'công việc gồm các giai đoạn liên tiếp đều phải thực hiện', ['các phương án loại trừ nhau', 'chỉ chọn một trong các phương án', 'chọn không quan tâm thứ tự'], 'Các giai đoạn VÀ ⇒ nhân; các phương án HOẶC ⇒ cộng.', 1, 'rule')
    C('Số cách xếp n người khác nhau thành một hàng là', 'n!', ['nⁿ', 'n²', 'C(n, 2)'], 'Hoán vị n phần tử.', 1, 'perm')
    C('Số cách xếp n người quanh một bàn tròn (xoay không tính khác nhau) là', '(n − 1)!', ['n!', 'n', 'n²'], 'Cố định một người để loại phép quay.', 2, 'perm')
    C('Khi nào dùng tổ hợp C(n, k) thay vì chỉnh hợp A(n, k)?', 'Khi không quan tâm thứ tự chọn', ['Khi có lặp', 'Khi k > n', 'Khi n = k'], 'C = A/k!: bỏ đi k! thứ tự.', 1, 'comb')
    C('C(n, k) và C(n, n − k)', 'bằng nhau', ['khác nhau', 'chỉ bằng khi n chẵn', 'tổng bằng n'], 'Chọn k người vào nhóm ⇔ chọn n − k người ra khỏi nhóm.', 1, 'comb')
    C('Công thức Pascal đúng là', 'C(n, k) = C(n − 1, k − 1) + C(n − 1, k)', ['C(n, k) = C(n − 1, k) · C(n − 1, k − 1)', 'C(n, k) = C(n − 1, k − 1) − C(n − 1, k)', 'C(n, k) = C(n, k − 1)'], 'Xét một phần tử cố định được chọn hay không.', 2, 'comb')
    C('Số nghiệm nguyên không âm của x₁ + x₂ + x₃ = 7 là', 'C(9, 2)', ['C(7, 3)', '7³', 'C(10, 3)'], 'Sao và thanh: C(7 + 3 − 1, 3 − 1).', 2, 'comb')
    C('Tổng các hệ số nhị thức Σₖ C(n, k) bằng', '2ⁿ', ['n!', 'n²', '2n'], 'Số tập con của tập n phần tử.', 2, 'comb')
    C('Để tính “ít nhất một” thường nên dùng', 'biến cố đối (phần bù)', ['quy tắc cộng cho từng trường hợp', 'hoán vị', 'chỉnh hợp lặp'], '“Ít nhất một” = 1 − “không có”.', 1, 'prob')
    C('Xác suất cổ điển P(A) = |A|/|S| chỉ đúng khi', 'các kết cục đồng khả năng', ['A, B độc lập', 'S vô hạn', 'luôn luôn'], 'Cần đối xứng: mọi kết cục sơ cấp có cùng khả năng.', 2, 'prob')
    C('Một tập hợp có n phần tử có bao nhiêu tập con?', '2ⁿ', ['n!', 'n²', 'C(n, 2)'], 'Mỗi phần tử có thể thuộc hoặc không thuộc tập con.', 1, 'comb')
    # số có chữ số với ràng buộc, kiểm vét cạn
    for k in (3, 4):
        digs = list(itertools.permutations(range(10), k)); ok = [p for p in digs if p[0] != 0]
        tot = 9 * perm(9, k - 1); assert len(ok) == tot
        add(f'Có bao nhiêu số tự nhiên có {k} chữ số đôi một khác nhau?', tot, [perm(10, k), 9 ** k, 10 ** k], f'Chữ số đầu ≠ 0 (9 cách), các chữ số còn lại A(9, {k-1}) = {G(perm(9, k-1))}: {G(tot)}.', 2, TOP['rule'])
        ev = sum(1 for p in ok if p[-1] % 2 == 0)
        add(f'Có bao nhiêu số tự nhiên có {k} chữ số đôi một khác nhau và là số chẵn?', ev, [tot // 2, tot // 2 + 9, perm(9, k - 1) * 5], f'Chia theo chữ số tận cùng: tận cùng 0 và tận cùng 2,4,6,8 (liệt kê xác nhận {G(ev)}).', 3, TOP['rule'])
        m5 = sum(1 for p in ok if p[-1] % 5 == 0)
        add(f'Có bao nhiêu số tự nhiên có {k} chữ số đôi một khác nhau và chia hết cho 5?', m5, [tot // 5, tot // 5 + 12, perm(9, k - 1) * 2], f'Tận cùng 0 hoặc 5; chữ số đầu khác 0 (liệt kê xác nhận {G(m5)}).', 3, TOP['rule'])
    for a, b in [(5, 4), (6, 3), (7, 5), (8, 2), (4, 4)]:
        add(f'Từ {a} thành phố A đến {b} thành phố B có {a*b} tuyến bay thẳng, mỗi tuyến một hãng. Đi từ A đến B rồi quay về theo tuyến khác nhau. Có bao nhiêu hành trình khứ hồi (đi và về khác tuyến)?', a * b * (a * b - 1), [(a * b) ** 2, a * b, a + b], f'Đi: {a*b} cách; về: {a*b - 1} cách còn lại (khác tuyến đi): {a*b}·{a*b - 1} = {G(a*b*(a*b-1))}.', 2, TOP['rule'])
    # xếp hàng buộc khối
    for n in (5, 6, 7, 8, 9, 10):
        adj = fac(n - 1) * 2; non = fac(n) - adj
        add(f'{n} người xếp thành một hàng. Số cách để hai người A và B đứng cạnh nhau là', adj, [fac(n), fac(n - 1), fac(n - 2) * 2], f'Buộc A, B thành một khối: ({n}−1)!·2! = {G(adj)}.', 2, TOP['perm'])
        add(f'{n} người xếp thành một hàng. Số cách để hai người A và B KHÔNG đứng cạnh nhau là', non, [adj, fac(n) - fac(n - 1), fac(n - 2) * (n - 1) * 2 + 1], f'{n}! − {G(adj)} = {G(non)} (phần bù).', 3, TOP['perm'])
    for n in (4, 5, 6, 7, 8):
        add(f'Có bao nhiêu cách xếp {n} người quanh một bàn tròn (hai cách xếp là một nếu chỉ khác nhau do quay bàn)?', fac(n - 1), [fac(n), fac(n - 2), n], f'({n} − 1)! = {G(fac(n-1))}.', 2, TOP['perm'])
    # ít nhất / nhóm
    for nm, nf, k in [(5, 7, 4), (6, 6, 5), (4, 8, 4), (7, 5, 4), (3, 9, 5), (8, 4, 3)]:
        n = nm + nf; tot = comb(n, k); none = comb(nf, k) if nf >= k else 0
        add(f'Từ {nm} nữ và {nf} nam chọn nhóm {k} người. Có bao nhiêu cách chọn nhóm có ít nhất 1 nữ?', tot - none, [tot, tot - comb(nm, k) if nm >= k else tot - 1, comb(nm, 1) * comb(n - 1, k - 1) - 1], f'Tổng C({n},{k}) = {G(tot)}; trừ nhóm toàn nam C({nf},{k}) = {G(none)}: {G(tot-none)}.', 2, TOP['mix'])
        for e in range(1, min(nm, k)):
            if k - e <= nf:
                add(f'Từ {nm} nữ và {nf} nam chọn nhóm {k} người. Số cách chọn nhóm có đúng {e} nữ là', comb(nm, e) * comb(nf, k - e), [comb(n, k), comb(nm, e) + comb(nf, k - e), comb(nm, e) * comb(nf, k - e) * 2], f'C({nm},{e})·C({nf},{k-e}) = {G(comb(nm,e)*comb(nf,k-e))}.', 2, TOP['mix']); break
    # sao và thanh
    for n, k in [(10, 4), (8, 3), (12, 5), (6, 3), (15, 4), (7, 2)]:
        ans = comb(n + k - 1, k - 1); assert ans == sum(1 for t in itertools.product(range(n + 1), repeat=k - 1) if sum(t) <= n) if k <= 4 and n <= 10 else True
        add(f'Số nghiệm nguyên không âm của phương trình x₁ + … + x_{k} = {n} là', ans, [n ** k, comb(n, k), comb(n + k, k)], f'Sao và thanh: C({n}+{k}−1, {k}−1) = C({n+k-1},{k-1}) = {G(ans)}.', 3, TOP['comb'])
    # bù trừ
    for N, a, b in [(100, 3, 7), (200, 4, 6), (60, 2, 5), (500, 7, 11), (120, 3, 4), (1000, 6, 10)]:
        lc = a * b // math.gcd(a, b)
        ans = N // a + N // b - N // lc; assert ans == sum(1 for t in range(1, N + 1) if t % a == 0 or t % b == 0)
        add(f'Có bao nhiêu số nguyên từ 1 đến {N} chia hết cho {a} hoặc {b}?', ans, [N // a + N // b, N // a * N // b, N // lc], f'⌊{N}/{a}⌋ + ⌊{N}/{b}⌋ − ⌊{N}/{lc}⌋ = {N//a} + {N//b} − {N//lc} = {ans} (bội chung bị đếm hai lần).', 2, TOP['ops'])
    # xác suất cổ điển bằng đếm
    for nm, nf, k, e in [(5, 7, 3, 2), (6, 4, 3, 1), (8, 6, 4, 2), (4, 6, 2, 1), (7, 5, 3, 2), (9, 6, 4, 2)]:
        pr = comb(nm, e) * comb(nf, k - e) / comb(nm + nf, k)
        B.mcq(f'Chọn ngẫu nhiên {k} người từ {nm} nữ và {nf} nam. Xác suất có đúng {e} nữ là', f(pr, 4), [f(comb(nm, e) / comb(nm + nf, k), 4), f(e / k + 0.01, 4), f(1 - pr, 4), f(pr / 2, 4)],
              f'C({nm},{e})·C({nf},{k-e})/C({nm+nf},{k}) = {comb(nm,e)*comb(nf,k-e)}/{comb(nm+nf,k)} = {f(pr,4)}.', 2, TOP['prob'], SRC, 'bo_sung')
    for k in (10, 15, 20, 25, 30, 40):
        pb = 1 - perm(365, k) / 365 ** k
        B.mcq(f'Trong nhóm {k} người (365 ngày, đồng khả năng), xác suất có ít nhất hai người trùng ngày sinh xấp xỉ', f(pb, 4), [f(perm(365, k) / 365 ** k, 4), f(k / 365, 4), f(k * (k - 1) / 2 / 365, 4) if k * (k - 1) / 2 / 365 < 1 else '0.9999'],
              f'1 − A(365,{k})/365^{k} = 1 − {f(perm(365,k)/365**k,4)} = {f(pb,4)}.', 3, TOP['prob'], SRC, 'bo_sung')
    B.essay('Một mã PIN gồm 4 chữ số (0–9). (a) Có bao nhiêu PIN? (b) Có bao nhiêu PIN có 4 chữ số khác nhau? (c) Xác suất đoán mò đúng PIN, biết các chữ số khác nhau?', '(a) 10⁴ = 10 000. (b) A(10, 4) = 5040. (c) 1/5040 ≈ 0.0002.', 1, TOP['rule'], SRC, 'bo_sung')
    B.essay('Một lớp có 12 nam và 8 nữ. Chọn ban cán sự gồm 1 lớp trưởng, 1 lớp phó, 2 ủy viên (ủy viên không phân biệt thứ tự). Bao nhiêu cách nếu (a) không ràng buộc? (b) lớp trưởng và lớp phó khác giới?', '(a) 20·19·C(18, 2) = 380·153 = 58 140. (b) 2·12·8 = 192 cách chọn (trưởng, phó) khác giới, nhân C(18, 2) = 153: 192·153 = 29 376.', 3, TOP['mix'], SRC, 'bo_sung')
    B.essay('Chứng minh C(n, k) = C(n − 1, k − 1) + C(n − 1, k) bằng lập luận đếm.', 'Chọn k người từ n người; cố định một người X. Nhóm có X: chọn thêm k − 1 từ n − 1 còn lại: C(n − 1, k − 1). Nhóm không có X: chọn k từ n − 1: C(n − 1, k). Hai trường hợp xung khắc và đầy đủ nên cộng lại.', 3, TOP['comb'], SRC, 'bo_sung')
    B.essay('Tính xác suất tay 5 lá bài có “cù lũ” (3 lá cùng số + 1 đôi khác số) từ bộ 52 lá.', '13·C(4,3)·12·C(4,2) = 13·4·12·6 = 3744 tay; tổng C(52,5) = 2 598 960; P = 3744/2 598 960 ≈ 0.00144.', 3, TOP['prob'], SRC, 'bo_sung')
