"""Module 3 — mở rộng: khái niệm + họ bài tính (phân số chính xác / vét cạn)."""
import math, itertools, random
from fractions import Fraction as Fr
from math import comb
from qb import f, fg
from qh import pm
from orig_m03 import TOP
SRC = 'Bổ sung: dạng bài §1.4–1.5 / Kreyszig PS 24.3 (đáp án tự tính bằng phân số chính xác hoặc vét cạn)'
def build(B):
    rng = random.Random(2503)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Tiên đề nào KHÔNG thuộc hệ tiên đề Kolmogorov?', 'P(A) < 1 với mọi biến cố A', ['P(A) ≥ 0', 'P(S) = 1', 'P(A ∪ B) = P(A) + P(B) khi A, B xung khắc'], 'Biến cố chắc chắn có P = 1.', 1, 'def')
    C('P(Aᶜ) bằng', '1 − P(A)', ['P(A) − 1', '1/P(A)', 'P(A)²'], 'Quy tắc bù.', 1, 'add')
    C('P(A ∪ B) với A, B bất kỳ bằng', 'P(A) + P(B) − P(A ∩ B)', ['P(A) + P(B)', 'P(A)P(B)', 'P(A) + P(B) + P(A ∩ B)'], 'Trừ phần giao đếm hai lần.', 1, 'add')
    C('P(A | B) được định nghĩa (P(B) > 0) là', 'P(A ∩ B)/P(B)', ['P(A ∩ B)/P(A)', 'P(A)P(B)', 'P(A)/P(B)'], 'Thu hẹp không gian mẫu về B.', 1, 'cond')
    C('Công thức nhân đúng là', 'P(A ∩ B) = P(A)·P(B | A)', ['P(A ∩ B) = P(A) + P(B | A)', 'P(A ∩ B) = P(A)/P(B)', 'P(A ∩ B) = P(A | B) + P(B)'], 'Từ định nghĩa xác suất có điều kiện.', 1, 'cond')
    C('A, B độc lập khi và chỉ khi', 'P(A ∩ B) = P(A)P(B)', ['P(A ∩ B) = 0', 'P(A ∪ B) = P(A) + P(B)', 'P(A) = P(B)'], 'Định nghĩa độc lập.', 1, 'indep')
    C('Nếu A, B độc lập và P(B) > 0 thì P(A | B) bằng', 'P(A)', ['P(B)', '0', '1'], 'Biết B không cung cấp thông tin về A.', 1, 'indep')
    C('Hai biến cố xung khắc có xác suất dương', 'không bao giờ độc lập', ['luôn độc lập', 'độc lập khi P(A) = P(B)', 'độc lập khi chúng đối lập'], 'P(AB) = 0 ≠ P(A)P(B) > 0.', 2, 'indep')
    C('Nếu A, B độc lập thì Aᶜ và B', 'cũng độc lập', ['xung khắc', 'không độc lập', 'đối lập'], 'Độc lập bảo toàn khi lấy phần bù.', 2, 'indep')
    C('Hệ nối tiếp hoạt động khi', 'tất cả các bộ phận hoạt động', ['ít nhất một bộ phận hoạt động', 'đúng một bộ phận hoạt động', 'đa số bộ phận hoạt động'], 'Một mắt xích hỏng là cả hệ hỏng.', 1, 'rel')
    C('Hệ song song hỏng khi', 'tất cả các bộ phận hỏng', ['một bộ phận hỏng', 'đa số hỏng', 'bộ phận đầu hỏng'], 'Dự phòng: chỉ cần một bộ phận tốt.', 1, 'rel')
    C('Rút hai lá không hoàn lại thì biến cố “lá thứ hai là át” và “lá thứ nhất là át”', 'không độc lập', ['độc lập', 'xung khắc', 'đối lập'], 'Xác suất lá thứ hai phụ thuộc kết quả lần một.', 2, 'seq')
    C('Rút có hoàn lại thì các lần rút', 'độc lập', ['phụ thuộc', 'xung khắc', 'đối lập'], 'Trạng thái hộp được phục hồi sau mỗi lần.', 1, 'seq')
    C('Luật số lớn nói rằng', 'tần suất tương đối hội tụ về xác suất khi số lần thử tăng', ['xác suất thay đổi theo số lần thử', 'sau chuỗi sấp sẽ có ngửa để bù', 'tần suất luôn bằng xác suất'], 'Không có “bù trừ” (ngụy biện con bạc).', 2, 'def')
    C('Đồng xu cân đối vừa ra 5 mặt sấp liên tiếp. Xác suất lần thứ 6 ra sấp là', '1/2', ['nhỏ hơn 1/2', 'lớn hơn 1/2', '1/64'], 'Các lần tung độc lập.', 2, 'indep')
    C('Xác suất cổ điển yêu cầu', 'các kết cục sơ cấp đồng khả năng', ['A và B độc lập', 'không gian mẫu vô hạn', 'P(A) < 1/2'], 'Chia số kết cục thuận lợi cho tổng số.', 1, 'classic')
    # bảng 2x2 ngẫu nhiên
    for k in range(10):
        a, b, c, d = [rng.randint(5, 40) for _ in range(4)]; n = a + b + c + d
        kind = k % 3
        if kind == 0:
            P(f'Khảo sát {n} người theo hai tiêu chí A và B: A∩B = {a}, A∩Bᶜ = {b}, Aᶜ∩B = {c}, Aᶜ∩Bᶜ = {d}. P(A | B) bằng', a / (a + c), f'P(A|B) = n(A∩B)/n(B) = {a}/{a+c} = {f(a/(a+c),4)}.', 1, TOP['cond'], SRC, extra=[a / (a + b), a / n, (a + c) / n], d=4)
        elif kind == 1:
            P(f'Khảo sát {n} người theo hai tiêu chí A và B: A∩B = {a}, A∩Bᶜ = {b}, Aᶜ∩B = {c}, Aᶜ∩Bᶜ = {d}. P(B | A) bằng', a / (a + b), f'P(B|A) = n(A∩B)/n(A) = {a}/{a+b} = {f(a/(a+b),4)}.', 1, TOP['cond'], SRC, extra=[a / (a + c), a / n, (a + b) / n], d=4)
        else:
            P(f'Khảo sát {n} người theo hai tiêu chí A và B: A∩B = {a}, A∩Bᶜ = {b}, Aᶜ∩B = {c}, Aᶜ∩Bᶜ = {d}. P(A ∪ B) bằng', (a + b + c) / n, f'P(A∪B) = 1 − P(Aᶜ∩Bᶜ) = 1 − {d}/{n} = {f((a+b+c)/n,4)}.', 2, TOP['add'], SRC, extra=[(a + b + c + a) / n, a / n, 1 - a / n], d=4)
    # độc lập kiểm tra
    for pa, pb, pab in [(0.4, 0.5, 0.2), (0.3, 0.6, 0.18), (0.5, 0.5, 0.3), (0.2, 0.7, 0.14), (0.6, 0.3, 0.2), (0.25, 0.8, 0.2)]:
        ind = abs(pa * pb - pab) < 1e-9
        B.mcq(f'P(A) = {pa}, P(B) = {pb}, P(A ∩ B) = {pab}. Hai biến cố A và B', 'độc lập' if ind else 'không độc lập', ['xung khắc', 'đối lập', 'không độc lập' if ind else 'độc lập'] if True else [],
              f'P(A)P(B) = {fg(pa*pb)} {"=" if ind else "≠"} {pab} ⇒ {"độc lập" if ind else "không độc lập"} (xung khắc cần P(AB) = 0).', 1, TOP['indep'], SRC, 'bo_sung')
    # hai biến cố: P(A∪B) khi độc lập
    for pa, pb in [(0.3, 0.4), (0.5, 0.2), (0.6, 0.5), (0.1, 0.9), (0.25, 0.35), (0.7, 0.2)]:
        P(f'A, B độc lập, P(A) = {pa}, P(B) = {pb}. P(A ∪ B) bằng', pa + pb - pa * pb, f'P(A)+P(B)−P(A)P(B) = {fg(pa)}+{fg(pb)}−{fg(pa*pb)} = {f(pa+pb-pa*pb,4)}.', 2, TOP['indep'], SRC, extra=[pa + pb, pa * pb, 1 - pa * pb * 0 - pa], d=4)
    # hệ thống
    for ps in [(0.9, 0.8), (0.95, 0.9, 0.85), (0.99, 0.98), (0.7, 0.8, 0.9), (0.6, 0.7), (0.92, 0.88, 0.95, 0.9)]:
        rs = math.prod(ps); rp = 1 - math.prod(1 - p for p in ps); tag = ', '.join(map(str, ps))
        P(f'Các linh kiện độc lập có độ tin cậy {tag}. Hệ NỐI TIẾP có độ tin cậy', rs, f'Tích: {f(rs,4)}.', 1, TOP['rel'], SRC, extra=[rp, min(ps), sum(ps) / len(ps)], d=4)
        P(f'Các linh kiện độc lập có độ tin cậy {tag}. Hệ SONG SONG có độ tin cậy', rp, f'1 − tích các xác suất hỏng = 1 − {f(math.prod(1-p for p in ps),5)} = {f(rp,4)}.', 2, TOP['rel'], SRC, extra=[rs, max(ps), 1 - min(ps)], d=4)
    for p1, p2, p3 in [(0.9, 0.8, 0.7), (0.95, 0.9, 0.9), (0.8, 0.6, 0.5), (0.99, 0.9, 0.9)]:
        r = p1 * (1 - (1 - p2) * (1 - p3))
        P(f'Linh kiện 1 (độ tin cậy {p1}) nối tiếp với khối gồm linh kiện 2 ({p2}) song song với linh kiện 3 ({p3}). Độ tin cậy cả hệ là', r, f'{p1}·[1 − {fg(1-p2)}·{fg(1-p3)}] = {f(r,4)}.', 3, TOP['rel'], SRC, extra=[p1 * p2 * p3, 1 - (1 - p1) * (1 - p2) * (1 - p3), p1 * p2], d=4)
    # ít nhất một
    for n, p in [(3, 0.2), (5, 0.1), (4, 0.3), (6, 0.15), (10, 0.05), (8, 0.25), (3, 0.5), (7, 0.1)]:
        P(f'{n} phép thử độc lập, mỗi phép thành công với xác suất {p}. P(có ít nhất một thành công) bằng', 1 - (1 - p) ** n, f'1 − (1 − {p})^{n} = 1 − {f((1-p)**n,4)} = {f(1-(1-p)**n,4)}.', 2, TOP['add'], SRC, extra=[n * p, (1 - p) ** n, p ** n], d=4)
        P(f'{n} phép thử độc lập, mỗi phép thành công với xác suất {p}. P(đúng một thành công) bằng', n * p * (1 - p) ** (n - 1), f'n·p·(1−p)^(n−1) = {n}·{p}·{fg((1-p)**(n-1),5)} = {f(n*p*(1-p)**(n-1),4)}.', 3, TOP['indep'], SRC, extra=[1 - (1 - p) ** n, p * (1 - p) ** (n - 1), (1 - p) ** n], d=4)
    # rút không hoàn lại
    for r, bl, k in [(5, 3, 2), (6, 4, 2), (4, 6, 3), (7, 3, 3), (8, 2, 2), (5, 5, 3)]:
        n = r + bl
        pr = Fr(comb(r, k), comb(n, k)); pb = float(pr)
        seq = 1.0
        for i in range(k): seq *= (r - i) / (n - i)
        assert abs(seq - pb) < 1e-12
        P(f'Hộp có {r} bi đỏ và {bl} bi xanh. Rút lần lượt {k} bi KHÔNG hoàn lại. P(tất cả đỏ) bằng', pb, f'Tích ' + ' · '.join(f'{r-i}/{n-i}' for i in range(k)) + f' = {pr} ≈ {f(pb,4)}.', 2, TOP['seq'], SRC, extra=[(r / n) ** k, 1 - pb, r / n], d=4)
        P(f'Hộp có {r} bi đỏ và {bl} bi xanh. Rút lần lượt {k} bi CÓ hoàn lại. P(tất cả đỏ) bằng', (r / n) ** k, f'Độc lập: ({r}/{n})^{k} = {f((r/n)**k,4)} (không hoàn lại sẽ là {f(pb,4)}).', 1, TOP['seq'], SRC, extra=[pb, 1 - (r / n) ** k, r / n], d=4)
    # hai súc sắc vét cạn
    d2 = list(itertools.product(range(1, 7), repeat=2))
    for thr in (7, 8, 9, 10):
        A = [t for t in d2 if sum(t) >= thr]; B6 = [t for t in A if 6 in t]
        P(f'Gieo hai súc sắc. Biết tổng ≥ {thr}, xác suất có ít nhất một mặt 6 là', len(B6) / len(A), f'Không gian thu hẹp {len(A)} kết cục, trong đó {len(B6)} có mặt 6 ⇒ {len(B6)}/{len(A)} = {f(len(B6)/len(A),4)}.', 2, TOP['cond'], SRC, extra=[11 / 36, len(A) / 36, len(B6) / 36], d=4)
    B.essay('Hộp I có 3 bi trắng 2 bi đen; hộp II có 2 bi trắng 4 bi đen. Chọn ngẫu nhiên một hộp rồi rút một bi. Tính P(bi trắng) (công thức toàn phần sẽ học ở Module 4) và P(rút từ hộp I | bi trắng).', 'P(T) = ½·3/5 + ½·2/6 = 0.3 + 0.1667 = 0.4667. P(I|T) = 0.3/0.4667 = 0.6429.', 2, TOP['cond'], SRC, 'bo_sung')
    B.essay('Một hệ gồm hai nhánh song song; nhánh 1 có 2 linh kiện nối tiếp (0.9; 0.8), nhánh 2 có 1 linh kiện (0.85). Tính độ tin cậy của hệ.', 'Nhánh 1: 0.72. Hệ: 1 − (1 − 0.72)(1 − 0.85) = 1 − 0.28·0.15 = 0.958.', 2, TOP['rel'], SRC, 'bo_sung')
    B.essay('Chứng minh nếu A và B độc lập thì Aᶜ và B độc lập.', 'P(Aᶜ ∩ B) = P(B) − P(A ∩ B) = P(B) − P(A)P(B) = P(B)(1 − P(A)) = P(Aᶜ)P(B).', 2, TOP['indep'], SRC, 'bo_sung')
    B.essay('Rút 2 lá từ bộ 52 lá không hoàn lại. Tính P(cả hai là cơ), P(lá thứ hai là cơ) và so sánh.', 'P(cả hai cơ) = 13/52·12/51 = 1/17 = 0.0588. P(lá thứ hai là cơ) = 13/52·12/51 + 39/52·13/51 = 0.25 (bằng P(lá đầu là cơ): đối xứng).', 3, TOP['seq'], SRC, 'bo_sung')
