"""Module 3 — biến thể tham số (bo_sung): xác suất cổ điển, bù, có điều kiện, nhân, độc lập, hệ thống nối tiếp/song song."""
import math, itertools, random
from fractions import Fraction as Fr
from math import comb
from qb import f, fg, nd, ni
from qh import pm
from orig_m03 import TOP
SRC = 'Bổ sung: biến thể tham số của dạng bài §1.4–1.5 / PS 24.3 (đáp án tự tính, kiểm bằng vét cạn hoặc phân số chính xác)'
def build(B):
    rng = random.Random(1303)
    P = lambda *a, **k: pm(B, rng, *a, **k)
    d2 = list(itertools.product(range(1, 7), repeat=2))
    # 1. Hai súc sắc: P(tổng = s)
    for s in (4, 5, 6, 8, 9, 10, 11):
        c = sum(1 for t in d2 if sum(t) == s)
        P(f'Gieo hai súc sắc cân đối. Xác suất tổng số chấm bằng {s} là', c / 36, f'Có {c} cặp (a, b) có tổng {s} trong 36 kết cục ⇒ P = {c}/36 = {f(c/36,4)}.', 1, TOP['classic'], SRC, extra=[1 / 36, c / 6, (c + 1) / 36, (c - 1) / 36], origin='bo_sung')
    # 2. Điều kiện trên hai súc sắc
    for (s, cond, fn_s, fn_c) in [(8, 'có ít nhất một mặt 6', lambda t: sum(t) == 8, lambda t: 6 in t), (7, 'hai mặt khác nhau', lambda t: sum(t) == 7, lambda t: t[0] != t[1]),
                                  (5, 'súc sắc thứ nhất ra số lẻ', lambda t: sum(t) == 5, lambda t: t[0] % 2 == 1), (9, 'tổng chia hết cho 3', lambda t: sum(t) == 9, lambda t: sum(t) % 3 == 0),
                                  (6, 'ít nhất một mặt ≥ 5', lambda t: sum(t) == 6, lambda t: max(t) >= 5)]:
        A = sum(1 for t in d2 if fn_s(t) and fn_c(t)); Cc = sum(1 for t in d2 if fn_c(t)); fr = Fr(A, Cc)
        P(f'Gieo hai súc sắc cân đối. Biết {cond}, xác suất tổng bằng {s} là', A / Cc, f'Không gian mẫu thu hẹp còn {Cc} kết cục; trong đó {A} có tổng {s} ⇒ P = {A}/{Cc} = {fr} ≈ {f(A/Cc,4)}.', 2, TOP['cond'], SRC, extra=[sum(1 for t in d2 if fn_s(t)) / 36, A / 36, Cc / 36], origin='bo_sung')
    # 3. Bảng 2x2: P(A|B), độc lập?
    for a, b, c_, d in [(30, 20, 15, 35), (12, 18, 28, 42), (40, 10, 20, 30), (25, 25, 25, 25), (9, 21, 15, 35), (18, 12, 30, 40)]:
        n = a + b + c_ + d; pa = (a + b) / n; pb = (a + c_) / n; pab = a / n
        indep = abs(pab - pa * pb) < 1e-12
        tb = f'Khảo sát {n} người: có cả hai thuộc tính A và B: {a}; chỉ A: {b}; chỉ B: {c_}; không có thuộc tính nào: {d}.'
        P(tb + ' P(A | B) bằng', a / (a + c_), f'P(A | B) = P(A ∩ B)/P(B) = {a}/{a + c_} = {f(a/(a+c_),4)}.', 1, TOP['cond'], SRC, extra=[a / n, (a + b) / n, a / (a + b)], origin='bo_sung')
        B.mcq(tb + ' A và B có độc lập không?', 'Độc lập' if indep else 'Không độc lập', ['Không độc lập' if indep else 'Độc lập', 'Xung khắc', 'Không thể kết luận'],
              f'P(A) = {f(pa,4)}, P(B) = {f(pb,4)}, P(A)P(B) = {f(pa*pb,4)}, P(A ∩ B) = {f(pab,4)} ⇒ ' + ('bằng nhau nên độc lập.' if indep else 'khác nhau nên không độc lập.'), 2, TOP['indep'], SRC, 'bo_sung')
    # 4. Quy tắc cộng
    for pa, pb, pab in [(0.5, 0.4, 0.2), (0.6, 0.3, 0.1), (0.35, 0.45, 0.15), (0.7, 0.5, 0.4), (0.25, 0.25, 0.0), (0.8, 0.6, 0.5)]:
        P(f'P(A) = {pa}, P(B) = {pb}, P(A ∩ B) = {pab}. Tính P(A ∪ B).', pa + pb - pab, f'P(A ∪ B) = {pa} + {pb} − {pab} = {f(pa+pb-pab,4)}.', 1, TOP['add'], SRC, extra=[pa + pb, pa * pb, pa + pb + pab], d=3, origin='bo_sung')
        if pab > 0: P(f'P(A) = {pa}, P(B) = {pb}, P(A ∩ B) = {pab}. Tính P(A | B).', pab / pb, f'P(A | B) = P(A ∩ B)/P(B) = {pab}/{pb} = {f(pab/pb,4)}.', 1, TOP['cond'], SRC, extra=[pab / pa, pa, pab], d=4, origin='bo_sung')
    for pa, pb in [(0.3, 0.4), (0.6, 0.5), (0.2, 0.9), (0.45, 0.35)]:
        P(f'A, B độc lập với P(A) = {pa}, P(B) = {pb}. Tính P(A ∪ B).', pa + pb - pa * pb, f'P(A ∩ B) = P(A)P(B) = {f(pa*pb,4)} ⇒ P(A ∪ B) = {pa} + {pb} − {f(pa*pb,4)} = {f(pa+pb-pa*pb,4)}.', 2, TOP['indep'], SRC, extra=[pa + pb, pa * pb, 1 - pa * pb], d=4, origin='bo_sung')
        P(f'A, B độc lập với P(A) = {pa}, P(B) = {pb}. Xác suất “xảy ra đúng một trong hai biến cố” là', pa * (1 - pb) + pb * (1 - pa), f'P(A)(1−P(B)) + P(B)(1−P(A)) = {pa}·{1-pb:.2f} + {pb}·{1-pa:.2f} = {f(pa*(1-pb)+pb*(1-pa),4)}.', 3, TOP['indep'], SRC, extra=[pa + pb - pa * pb, pa * pb, pa + pb], d=4, origin='bo_sung')
    # 5. Rút có/không hoàn lại
    for N, D, k in [(50, 5, 3), (20, 4, 2), (30, 6, 4), (12, 3, 3), (40, 8, 3), (25, 5, 2)]:
        pw = ((N - D) / N) ** k; pwo = comb(N - D, k) / comb(N, k)
        P(f'Lô {N} sản phẩm có {D} phế phẩm. Rút {k} sản phẩm CÓ hoàn lại. Xác suất cả {k} đều tốt là', pw, f'(({N}−{D})/{N})^{k} = {f(pw,5)}.', 1, TOP['seq'], SRC, extra=[pwo, 1 - pw, (N - D) / N], d=4, origin='bo_sung')
        P(f'Lô {N} sản phẩm có {D} phế phẩm. Rút {k} sản phẩm KHÔNG hoàn lại. Xác suất cả {k} đều tốt là', pwo, f'C({N-D},{k})/C({N},{k}) = {f(pwo,5)} (khác trường hợp có hoàn lại {f(pw,5)}).', 2, TOP['seq'], SRC, extra=[pw, 1 - pwo, (N - D) / N], d=4, origin='bo_sung')
    # 6. Độ tin cậy hệ thống
    for ps in [(0.9, 0.95), (0.8, 0.9, 0.95), (0.99, 0.98), (0.9, 0.9, 0.9, 0.9), (0.95, 0.97, 0.99)]:
        ser = math.prod(ps); par = 1 - math.prod(1 - p for p in ps)
        lst = ', '.join(str(p) for p in ps)
        P(f'Hệ thống gồm các bộ phận độc lập, xác suất mỗi bộ phận hoạt động: {lst}. Mắc NỐI TIẾP (hỏng một bộ phận là cả hệ hỏng): xác suất hệ hoạt động là', ser, f'Tích các xác suất: {" × ".join(str(p) for p in ps)} = {f(ser,5)}.', 2, TOP['rel'], SRC, extra=[par, min(ps), sum(ps) / len(ps)], d=5, origin='bo_sung')
        P(f'Hệ thống gồm các bộ phận độc lập, xác suất mỗi bộ phận hoạt động: {lst}. Mắc SONG SONG (chỉ cần một bộ phận hoạt động): xác suất hệ hoạt động là', par, f'Bù: tất cả cùng hỏng: {" × ".join(f"{1-p:.2f}" for p in ps)} = {f(1-par,6)} ⇒ P = {f(par,6)}.', 2, TOP['rel'], SRC, extra=[ser, max(ps), 1 - min(ps)], d=6, origin='bo_sung')
    # 7. Bù, “ít nhất một”
    for p, n in [(0.1, 5), (0.05, 10), (0.2, 3), (0.02, 20), (0.3, 4), (0.5, 6)]:
        P(f'Mỗi phép thử độc lập thành công với xác suất {p}. Xác suất có ÍT NHẤT một thành công trong {n} phép thử là', 1 - (1 - p) ** n, f'Bù: không thành công lần nào: (1 − {p})^{n} = {f((1-p)**n,5)} ⇒ P = {f(1-(1-p)**n,5)}.', 2, TOP['add'], SRC, extra=[n * p, (1 - p) ** n, p ** n], d=4, origin='bo_sung')
    for p in (0.5, 0.2, 0.05):
        n = math.ceil(math.log(0.01) / math.log(1 - p))
        B.mcq(f'Mỗi phép thử độc lập thành công với xác suất {p}. Cần ít nhất bao nhiêu phép thử để xác suất có ít nhất một thành công vượt 99%?', str(n), [str(n + 3), str(max(1, n - 2)), str(int(1 / p))],
              f'Cần 1 − (1 − {p})ⁿ > 0.99 ⇔ n > ln 0.01 / ln(1 − {p}) = {math.log(0.01)/math.log(1-p):.3f} ⇒ n = {n}. (Kiểm tra: n = {n}: {1-(1-p)**n:.5f}; n = {n-1}: {1-(1-p)**(n-1):.5f}.)', 3, TOP['add'], SRC, 'bo_sung')
    # 8. Công thức nhân hoàn trả
    for a, b, c_ in [(4, 6, 3), (5, 5, 2), (3, 7, 3), (6, 4, 2)]:
        n = a + b
        pw = Fr(a, n) * Fr(a - 1, n - 1)
        P(f'Túi có {a} bi đỏ và {b} bi xanh. Rút lần lượt 2 bi không hoàn lại. Xác suất cả hai bi đều đỏ là', float(pw), f'P = ({a}/{n})·({a-1}/{n-1}) = {pw} ≈ {f(float(pw),4)}. (Có hoàn lại sẽ là ({a}/{n})² = {f((a/n)**2,4)}.)', 2, TOP['seq'], SRC, extra=[(a / n) ** 2, a / n, 1 - float(pw)], origin='bo_sung')
        P(f'Túi có {a} bi đỏ và {b} bi xanh. Rút lần lượt 2 bi không hoàn lại. Biết bi thứ nhất đỏ, xác suất bi thứ hai đỏ là', (a - 1) / (n - 1), f'Sau khi lấy 1 bi đỏ còn {n-1} bi, trong đó {a-1} đỏ ⇒ P(B | A) = {a-1}/{n-1} = {f((a-1)/(n-1),4)}.', 1, TOP['cond'], SRC, extra=[a / n, (a - 1) / n, 1 / (n - 1)], origin='bo_sung')
