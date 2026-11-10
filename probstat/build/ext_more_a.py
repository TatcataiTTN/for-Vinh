"""Đợt mở rộng ngân hàng câu hỏi (nhãn bo_sung) cho M1, M2, M3, M6, M7. Đáp án tính bằng code (math/itertools/SciPy)."""
import math, random, itertools, statistics as stt
from fractions import Fraction as Fr
from scipy import stats as st
from qb import f, fg, ni
from qh import pm
import importlib
SRC = 'Bổ sung: họ bài tham số hóa theo dạng đề (đáp án tự tính bằng chương trình)'
def tp(mid):
    o = importlib.import_module('orig_' + mid); return getattr(o, 'TOP', None) or getattr(o, 'TOPIC')

def build(mid, B):
    fn = globals().get('b_' + mid)
    if fn: fn(B, random.Random(7100 + int(mid[1:])), tp(mid))

def nump(B, rng, stem, v, expl, lvl, topic, extra=(), d=4, lo=None, hi=None):
    pm(B, rng, stem, v, expl, lvl, topic, SRC, extra=extra, d=d, origin='bo_sung', lo=lo, hi=hi)
def inte(B, stem, a, wrong, expl, lvl, topic):
    wr = []
    for w in list(wrong) + [a + 1, a - 1, a + 2, a * 2, a + 10, max(1, a // 2) + 3]:
        w = str(w)
        if w != str(a) and w not in wr and not w.startswith('-') and w != '0': wr.append(w)
    B.mcq(stem, str(a), wr[:3] if len(wr) >= 3 else wr, expl, lvl, topic, SRC, 'bo_sung')
def txt(B, stem, ok, bad, expl, lvl, topic): B.mcq(stem, ok, bad, expl, lvl, topic, SRC, 'bo_sung')

# ───────────── M1
def b_m01(B, rng, T):
    for _ in range(12):   # biến đổi tuyến tính
        xb = rng.choice([12, 20, 35, 48, 60]); s = rng.choice([2, 3, 4, 5, 6]); a = rng.choice([2, 3, 5, 0.5, -1, 10]); b = rng.choice([1, 5, 10, -4, 20])
        nump(B, rng, f'Mẫu X có trung bình {xb} và độ lệch chuẩn {s}. Đặt Y = {fg(a)}X {"+" if b>=0 else "−"} {abs(b)}. Trung bình của Y là', a * xb + b, f'ȳ = a·x̄ + b = {fg(a)}·{xb} + ({b}) = {fg(a*xb+b)}.', 1, T['mean'], extra=[xb + b, a * xb, a * (xb + b)], d=2)
        nump(B, rng, f'Mẫu X có độ lệch chuẩn {s}. Đặt Y = {fg(a)}X {"+" if b>=0 else "−"} {abs(b)}. Độ lệch chuẩn của Y là', abs(a) * s, f's_Y = |a|·s_X = {fg(abs(a))}·{s} = {fg(abs(a)*s)} (hằng số cộng không đổi độ phân tán).', 2, T['spread'], extra=[a * s + b, abs(a) * s + b, a * a * s, s], d=2)
    for _ in range(10):   # trung bình gộp
        n1, n2 = rng.choice([10, 20, 30, 40]), rng.choice([15, 25, 50, 60]); m1, m2 = rng.choice([60, 65, 70, 72]), rng.choice([75, 80, 85, 90])
        v = (n1 * m1 + n2 * m2) / (n1 + n2)
        nump(B, rng, f'Nhóm 1 có {n1} người, điểm trung bình {m1}; nhóm 2 có {n2} người, điểm trung bình {m2}. Điểm trung bình chung của cả hai nhóm là', v, f'x̄ = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂) = ({n1}·{m1} + {n2}·{m2})/{n1+n2} = {f(v,3)}.', 2, T['mean'], extra=[(m1 + m2) / 2, (n1 + n2) / 2], d=3)
    for k in (2, 3, 4, 2.5, 5, 6, 1.5, 3.5, 4.5, 8):   # Chebyshev
        v = 1 - 1 / k ** 2
        nump(B, rng, f'Theo bất đẳng thức Chebyshev, tỉ lệ dữ liệu nằm trong khoảng x̄ ± {fg(k)}s ít nhất là', v, f'1 − 1/k² = 1 − 1/{fg(k)}² = {f(v,4)}.', 3, T['theory'], extra=[1 / k ** 2, 1 - 1 / k, 0.95, 0.68], d=4, lo=0.0, hi=1.0)
    for _ in range(10):   # hệ số biến thiên
        m = rng.choice([20, 40, 50, 80, 120]); s = rng.choice([2, 4, 5, 6, 10, 16]); v = s / m * 100
        nump(B, rng, f'Mẫu có x̄ = {m}, s = {s}. Hệ số biến thiên CV = s/x̄ (theo %) bằng', v, f'CV = {s}/{m}·100% = {f(v,2)}%.', 1, T['spread'], extra=[m / s, s / m, s * m / 100, s ** 2 / m * 100], d=2)
    for _ in range(10):   # tần suất tích lũy
        fr = [rng.randint(2, 14) for _ in range(4)]; n = sum(fr); k = rng.choice([1, 2, 3]); v = sum(fr[:k + 1]) / n
        nump(B, rng, f'Bảng tần số 4 lớp: {fr[0]}, {fr[1]}, {fr[2]}, {fr[3]} (n = {n}). Tần suất tích lũy đến hết lớp thứ {k+1} là', v, f'({"+".join(map(str,fr[:k+1]))})/{n} = {f(v,4)}.', 1, T['group'], extra=[fr[k] / n, sum(fr[:k]) / n, sum(fr[:k + 1]), 1 - v], d=4, lo=0.0, hi=1.0)
    for _ in range(8):    # tổng bình phương độ lệch
        d = [rng.randint(3, 20) for _ in range(rng.choice([5, 6, 7]))]; m = stt.mean(d); ss = sum((x - m) ** 2 for x in d)
        nump(B, rng, f'Mẫu: {"; ".join(map(str,d))}. Tổng bình phương độ lệch Σ(xᵢ − x̄)² bằng', ss, f'x̄ = {f(m,3)}; Σ(xᵢ − x̄)² = {f(ss,3)}; chia n − 1 = {len(d)-1} mới ra s² = {f(ss/(len(d)-1),3)}.', 2, T['spread'], extra=[ss / (len(d) - 1), ss / len(d), math.sqrt(ss), sum(d)], d=3)

# ───────────── M2
def b_m02(B, rng, T):
    for w in ['TOÁN', 'XÁC', 'SUẤT', 'LEVEL', 'BANANA', 'ANNA', 'MAMMA', 'STATISTICS', 'MISSISSIPPI', 'ARRANGE', 'BOOKKEEPER', 'PROBABILITY']:
        cnt = {}
        for c in w: cnt[c] = cnt.get(c, 0) + 1
        v = math.factorial(len(w)); den = 1
        for c in cnt.values(): den *= math.factorial(c)
        v //= den
        inte(B, f'Số cách xếp các chữ cái của từ “{w}” thành một dãy (phân biệt theo vị trí, các chữ giống nhau không phân biệt) là', v, [math.factorial(len(w)), v * 2, max(1, v // 2), math.factorial(len(w)) // max(cnt.values())], f'n!/(Π kᵢ!) = {len(w)}!/{"·".join(str(math.factorial(c)) for c in cnt.values() if c>1) or "1"} = {v}.', 2, T['perm'])
    for n in (5, 6, 7, 8, 9, 10, 12, 4):
        v = math.factorial(n - 1)
        inte(B, f'{n} người ngồi quanh một bàn tròn (coi hai cách xếp khác nhau khi không thể đưa về nhau bằng phép xoay). Số cách là', v, [math.factorial(n), v // 2, math.factorial(n - 2), n * v], f'Cố định một người: ({n}−1)! = {v}.', 2, T['perm'])
    for n in (6, 8, 10, 12, 15, 20, 25, 30):
        v = n * (n - 1) // 2
        inte(B, f'Trong một buổi họp có {n} người, mỗi hai người bắt tay đúng một lần. Số cái bắt tay là', v, [n * (n - 1), n * n, v + n, n], f'C({n},2) = {v}.', 1, T['comb'])
    for n, k in [(8, 3), (10, 4), (12, 5), (9, 2), (10, 5), (15, 3), (7, 3), (11, 4)]:
        v = math.comb(n, k)
        inte(B, f'Số xâu nhị phân độ dài {n} có đúng {k} chữ số 1 là', v, [math.perm(n, k), 2 ** n, math.comb(n, k + 1), v + n], f'Chọn {k} vị trí trong {n}: C({n},{k}) = {v}.', 1, T['comb'])
    for m, w, k in [(6, 4, 4), (7, 5, 4), (5, 5, 3), (8, 4, 5), (6, 6, 4), (9, 3, 4), (10, 5, 5), (7, 4, 3), (8, 6, 4), (6, 3, 3)]:
        v = math.comb(m + w, k) - math.comb(m, k)
        inte(B, f'Một nhóm có {m} nam và {w} nữ. Chọn {k} người sao cho có ít nhất 1 nữ. Số cách là', v, [math.comb(m + w, k), math.comb(w, 1) * math.comb(m + w - 1, k - 1), math.comb(m, k), v + m], f'Tổng trừ trường hợp toàn nam: C({m+w},{k}) − C({m},{k}) = {v}.', 2, T['mix'])
    for n in (4, 5, 6, 7, 8, 9):
        v = 2 * math.factorial(n - 1)
        inte(B, f'Xếp {n} người vào một hàng, hai người A và B phải ngồi cạnh nhau. Số cách là', v, [math.factorial(n), math.factorial(n - 1), math.factorial(n) - v, v * n], f'Gộp A, B: (n−1)!·2! = {math.factorial(n-1)}·2 = {v}.', 2, T['perm'])
    for dd in (4, 3, 5):
        for digs in ('0123456789', '0123456', '123456789'):
            v = sum(1 for p in itertools.permutations(digs, dd) if p[0] != '0')
            inte(B, f'Số các số tự nhiên có {dd} chữ số đôi một khác nhau lập từ các chữ số {", ".join(digs)} là', v, [math.perm(len(digs), dd), len(digs) ** dd, v + len(digs), math.comb(len(digs), dd)], f'Đếm bằng liệt kê và loại các số bắt đầu bằng 0: {v}.', 2, T['perm'])
    for N, a, b in [(100, 3, 5), (200, 4, 6), (500, 7, 11), (1000, 6, 8), (300, 5, 9), (120, 4, 10), (999, 2, 3), (250, 6, 15)]:
        v = N // a + N // b - N // (a * b // math.gcd(a, b))
        inte(B, f'Trong các số từ 1 đến {N}, có bao nhiêu số chia hết cho {a} hoặc chia hết cho {b}?', v, [N // a + N // b, (N // a) * (N // b) // max(1, N // 10), N // a, v + N // b], f'Bao hàm – loại trừ: ⌊{N}/{a}⌋ + ⌊{N}/{b}⌋ − ⌊{N}/bội chung nhỏ nhất⌋ = {v}.', 3, T['rule'])

# ───────────── M3
def b_m03(B, rng, T):
    for _ in range(10):
        p = rng.choice([0.1, 0.2, 0.3, 0.4, 0.55, 0.65, 0.8]); n = rng.choice([2, 3, 4, 5, 6]); v = 1 - (1 - p) ** n
        nump(B, rng, f'Mỗi lần thử thành công với xác suất {fg(p)}, các lần độc lập. Xác suất có ít nhất một thành công trong {n} lần thử là', v, f'1 − (1 − {fg(p)})^{n} = {f(v,4)}.', 2, T['indep'], extra=[n * p, p ** n, (1 - p) ** n, 1 - p ** n], lo=0.0, hi=1.0)
    for s in (5, 6, 7, 8, 9, 10, 4, 11):
        pairs = [(x, y) for x in range(1, 7) for y in range(1, 7)]; ev = [(x, y) for x, y in pairs if x + y == s]; v = len(ev) / 36
        nump(B, rng, f'Gieo hai con xúc xắc cân đối. Xác suất tổng số chấm bằng {s} là', v, f'{len(ev)} cặp thuận lợi / 36 = {f(v,4)}.', 1, T['classic'], extra=[1 / 36, len(ev) / 6, len(ev) / 12, (len(ev) + 1) / 36], lo=0.0, hi=1.0)
    for s in (7, 8, 9, 10, 6):
        for x0 in (3, 4):
            sp = [(x, y) for x in range(1, 7) for y in range(1, 7) if x + y >= s]; both = [t for t in sp if t[0] == x0]
            if not sp or not both: continue
            v = len(both) / len(sp)
            nump(B, rng, f'Gieo hai con xúc xắc cân đối. Biết tổng số chấm ít nhất {s}, xác suất con thứ nhất ra {x0} là', v, f'P = {len(both)}/{len(sp)} = {f(v,4)} (thu hẹp không gian mẫu).', 3, T['cond'], extra=[1 / 6, len(both) / 36, len(sp) / 36], lo=0.0, hi=1.0)
    for _ in range(10):   # bảng chéo
        a, b, c, d = [rng.randint(5, 40) for _ in range(4)]; n = a + b + c + d
        v = a / (a + c)
        nump(B, rng, f'Khảo sát {n} người, bảng chéo (có hút thuốc, bị bệnh): hút & bệnh = {a}; hút & không bệnh = {b}; không hút & bệnh = {c}; không hút & không bệnh = {d}. Xác suất để người đó hút thuốc, biết người đó bị bệnh, tức P(hút | bệnh), bằng', v, f'P(hút|bệnh) = {a}/({a}+{c}) = {f(v,4)}.', 2, T['cond'], extra=[a / (a + b), a / n, (a + b) / n, c / (a + c)], lo=0.0, hi=1.0)
    for _ in range(10):
        pa, pb = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6]), rng.choice([0.25, 0.35, 0.45, 0.55]); indep = rng.random() < 0.5
        pab = round(pa * pb, 4) if indep else round(pa * pb + rng.choice([-0.05, 0.05, 0.08]), 4)
        if pab <= 0 or pab >= min(pa, pb): pab = round(pa * pb, 4); indep = True
        txt(B, f'P(A) = {fg(pa)}, P(B) = {fg(pb)}, P(A ∩ B) = {fg(pab)}. Hai biến cố A và B', 'độc lập' if indep else 'không độc lập', ['xung khắc với nhau', 'đối lập nhau', 'chưa đủ dữ kiện kết luận'] if indep else ['độc lập với nhau', 'xung khắc với nhau', 'đối lập nhau'], f'P(A)P(B) = {fg(pa*pb)} {"=" if indep else "≠"} P(A∩B) = {fg(pab)}.', 2, T['indep'])
    for _ in range(10):
        pa, pb = rng.choice([0.3, 0.4, 0.5, 0.6]), rng.choice([0.2, 0.35, 0.45]); pab = round(rng.uniform(0.05, min(pa, pb) - 0.01), 2); v = pa + pb - pab
        nump(B, rng, f'P(A) = {fg(pa)}, P(B) = {fg(pb)}, P(A ∩ B) = {fg(pab)}. P(A ∪ B) bằng', v, f'P(A∪B) = {fg(pa)} + {fg(pb)} − {fg(pab)} = {f(v,3)}.', 1, T['add'], extra=[pa + pb, pa * pb, pa + pb + pab, 1 - v], d=3, lo=0.0, hi=1.0)
        nump(B, rng, f'P(A) = {fg(pa)}, P(B) = {fg(pb)}, P(A ∩ B) = {fg(pab)}. P(A | B) bằng', pab / pb, f'P(A|B) = P(A∩B)/P(B) = {fg(pab)}/{fg(pb)} = {f(pab/pb,4)}.', 2, T['cond'], extra=[pab / pa, pa, pab * pb, pab], lo=0.0, hi=1.0)
    for _ in range(10):   # rút không hoàn lại
        r, b = rng.randint(3, 9), rng.randint(3, 9); n = r + b; v = r / n * (r - 1) / (n - 1)
        nump(B, rng, f'Hộp có {r} bi đỏ và {b} bi xanh. Rút lần lượt 2 bi không hoàn lại. Xác suất cả hai đỏ là', v, f'({r}/{n})·({r-1}/{n-1}) = {f(v,4)}.', 1, T['seq'], extra=[(r / n) ** 2, r / n, math.comb(r, 2) / math.comb(n, 3), (r / n) * (r / (n - 1))], lo=0.0, hi=1.0)
    for _ in range(8):   # nối tiếp / song song
        ps = [rng.choice([0.8, 0.85, 0.9, 0.95, 0.99, 0.7]) for _ in range(rng.choice([2, 3]))]
        ser = math.prod(ps); par = 1 - math.prod(1 - p for p in ps)
        nump(B, rng, f'Hệ gồm các linh kiện độc lập có độ tin cậy {", ".join(map(fg,ps))}. Độ tin cậy của hệ NỐI TIẾP là', ser, f'Tích: {" × ".join(map(fg,ps))} = {f(ser,4)}.', 1, T['rel'], extra=[par, sum(ps) / len(ps), min(ps)], lo=0.0, hi=1.0)
        nump(B, rng, f'Hệ gồm các linh kiện độc lập có độ tin cậy {", ".join(map(fg,ps))}. Độ tin cậy của hệ SONG SONG là', par, f'1 − Π(1 − pᵢ) = {f(par,4)}.', 2, T['rel'], extra=[ser, max(ps), sum(ps)], lo=0.0, hi=1.0)

# ───────────── M6
def b_m06(B, rng, T):
    for k in (1, 1.5, 1.96, 2, 2.5, 3, 0.5, 1.28, 1.645, 0.8):
        v = 2 * st.norm.cdf(k) - 1
        nump(B, rng, f'X ~ N(μ, σ²). Xác suất |X − μ| < {fg(k)}σ là', v, f'2Φ({fg(k)}) − 1 = {f(v,4)}.', 1, T['normp'], extra=[st.norm.cdf(k), 1 - v, 2 * st.norm.cdf(k)], lo=0.0, hi=1.0)
    for n, p, k in [(10, 0.3, 4), (12, 0.5, 8), (15, 0.2, 5), (8, 0.6, 6), (20, 0.1, 3), (10, 0.5, 7), (9, 0.4, 5), (14, 0.35, 6), (16, 0.25, 7), (11, 0.45, 4)]:
        v = 1 - st.binom.cdf(k - 1, n, p)
        nump(B, rng, f'X ~ B({n}; {fg(p)}). P(X ≥ {k}) bằng', v, f'1 − P(X ≤ {k-1}) = {f(v,4)} (tính bằng SciPy).', 2, T['binom'], extra=[st.binom.cdf(k, n, p), st.binom.pmf(k, n, p), 1 - st.binom.cdf(k, n, p)], lo=0.0, hi=1.0)

# ───────────── M7
def b_m07(B, rng, T):
    for _ in range(12):   # σ/√n, trung bình mẫu
        mu = rng.choice([50, 100, 12, 8]); sg = rng.choice([4, 6, 10, 15]); n = rng.choice([9, 16, 25, 36, 64, 100]); c = rng.choice([1, 2, 3]) * sg / math.sqrt(n)
        v = 2 * st.norm.cdf(c / (sg / math.sqrt(n))) - 1
        nump(B, rng, f'Tổng thể có μ = {mu}, σ = {sg}. Với mẫu cỡ n = {n}, xấp xỉ chuẩn, xác suất |X̄ − μ| < {f(c,3)} là', v, f'P = 2Φ(c√n/σ) − 1 = 2Φ({f(c/(sg/math.sqrt(n)),2)}) − 1 = {f(v,4)}.', 3, T['sample'], extra=[2 * st.norm.cdf(c / sg) - 1, st.norm.cdf(c / (sg / math.sqrt(n))), 1 - v], lo=0.0, hi=1.0)
    for _ in range(12):   # Poisson MLE
        d = [rng.randint(0, 8) for _ in range(rng.choice([6, 8, 10]))]; v = sum(d) / len(d)
        nump(B, rng, f'Mẫu từ phân phối Poisson(λ): {", ".join(map(str,d))}. Ước lượng hợp lý cực đại của λ là', v, f'λ̂ = x̄ = {sum(d)}/{len(d)} = {f(v,3)}.', 2, T['mle'], extra=[1 / v if v else 1, v ** 2, stt.variance(d), sum(d)], d=3, lo=0.0)
    for _ in range(12):   # MLE mũ
        d = [round(rng.uniform(0.2, 6), 1) for _ in range(rng.choice([5, 6, 8]))]; v = len(d) / sum(d)
        nump(B, rng, f'Mẫu từ phân phối mũ mật độ λe^(−λx): {", ".join(map(str,d))}. Ước lượng hợp lý cực đại λ̂ là', v, f'λ̂ = n/Σxᵢ = {len(d)}/{f(sum(d),2)} = {f(v,4)}.', 2, T['mle'], extra=[sum(d) / len(d), sum(d), len(d) * sum(d), 1 / math.sqrt(v)], d=4, lo=0.0)
    for _ in range(10):   # MLE σ² chuẩn
        d = [round(rng.uniform(5, 15), 1) for _ in range(rng.choice([5, 6, 8]))]; m = stt.mean(d); v = sum((x - m) ** 2 for x in d) / len(d)
        nump(B, rng, f'Mẫu từ N(μ, σ²): {", ".join(map(str,d))}. Ước lượng hợp lý cực đại của σ² (chia cho n) bằng', v, f'σ̂² = Σ(xᵢ − x̄)²/n = {f(v,4)}; còn s² (chia n − 1) = {f(stt.variance(d),4)}.', 3, T['mle'], extra=[stt.variance(d), math.sqrt(v), m], d=4, lo=0.0)
    for _ in range(10):   # moments uniform
        d = [round(rng.uniform(0.5, 9), 1) for _ in range(rng.choice([5, 6, 7]))]; v = 2 * stt.mean(d)
        nump(B, rng, f'Mẫu từ phân phối đều U(0; θ): {", ".join(map(str,d))}. Ước lượng θ bằng phương pháp moment (E(X) = θ/2) là', v, f'θ̂ = 2x̄ = 2·{f(stt.mean(d),3)} = {f(v,3)}.', 2, T['point'], extra=[max(d), stt.mean(d), stt.mean(d) / 2, 2 * max(d)], d=3, lo=0.0)
    for _ in range(12):   # từ Σx, Σx²
        n = rng.choice([10, 12, 15, 20, 25]); xb = rng.choice([4, 5.5, 8, 10]); s2 = rng.choice([2.5, 4, 6.25, 9]); sx = n * xb; sxx = (n - 1) * s2 + n * xb ** 2
        nump(B, rng, f'Mẫu cỡ n = {n} có Σxᵢ = {fg(sx)} và Σxᵢ² = {fg(sxx)}. Phương sai mẫu s² (chia n − 1) bằng', s2, f's² = (Σx² − n·x̄²)/(n − 1) = ({fg(sxx)} − {n}·{fg(xb)}²)/{n-1} = {f(s2,4)}.', 3, T['sample'], extra=[(sxx - n * xb ** 2) / n, sxx / (n - 1) - xb ** 2, sxx / n - xb ** 2 + 1], d=4, lo=0.0)
    for _ in range(10):   # ghép 5 lớp
        w = rng.choice([4, 5, 10]); lo0 = rng.choice([0, 10, 20]); fr = [rng.randint(3, 20) for _ in range(5)]; n = sum(fr); mids = [lo0 + w * (i + .5) for i in range(5)]
        xb = sum(k * m for k, m in zip(fr, mids)) / n; s2 = sum(k * (m - xb) ** 2 for k, m in zip(fr, mids)) / (n - 1)
        nump(B, rng, f'Bảng 5 lớp độ rộng {w}, bắt đầu từ {lo0}: tần số {", ".join(map(str,fr))} (n = {n}). Phương sai mẫu s² (dùng trung điểm lớp) bằng', s2, f'Trung điểm {", ".join(fg(m) for m in mids)}; x̄ = {f(xb,3)}; s² = Σf(m − x̄)²/(n − 1) = {f(s2,3)}.', 3, T['group'], extra=[s2 * (n - 1) / n, xb, math.sqrt(s2)], d=3, lo=0.0)
    for _ in range(10):   # p̂ và sai số chuẩn
        n = rng.choice([50, 100, 200, 400]); k = round(n * rng.choice([0.2, 0.35, 0.5, 0.64])); ph = k / n; v = math.sqrt(ph * (1 - ph) / n)
        nump(B, rng, f'Trong {n} quan sát có {k} thành công. Sai số chuẩn của p̂ là', v, f'√(p̂(1 − p̂)/n) = √({f(ph,3)}·{f(1-ph,3)}/{n}) = {f(v,4)}.', 2, T['sample'], extra=[ph * (1 - ph) / n, math.sqrt(ph / n), ph], d=4, lo=0.0)
    txts = [('Ước lượng T của θ gọi là không chệch khi', 'E(T) = θ', ['Var(T) = 0', 'T = θ với mọi mẫu', 'T là trung bình mẫu']),
            ('Phương sai mẫu chia cho n (thay vì n − 1) là ước lượng', 'chệch (trung bình nhỏ hơn σ²)', ['không chệch', 'chệch (trung bình lớn hơn σ²)', 'không xác định được']),
            ('Trung bình mẫu x̄ là ước lượng không chệch của', 'kỳ vọng μ', ['phương sai σ²', 'độ lệch chuẩn σ', 'trung vị']),
            ('Với hai ước lượng không chệch, ước lượng tốt hơn là cái có', 'phương sai nhỏ hơn', ['phương sai lớn hơn', 'giá trị lớn hơn', 'cỡ mẫu nhỏ hơn']),
            ('Khi n tăng, sai số chuẩn σ/√n của x̄', 'giảm', ['tăng', 'không đổi', 'bằng σ']),
            ('Hàm hợp lý L(θ) của mẫu độc lập là', 'tích các mật độ f(xᵢ; θ)', ['tổng các mật độ', 'trung bình các xᵢ', 'tích các xᵢ']),
            ('Để tìm MLE thường lấy đạo hàm của', 'ln L(θ) rồi cho bằng 0', ['L(θ) rồi cho bằng 1', 'θ rồi cho bằng 0', 'xᵢ rồi cho bằng 0']),
            ('Phương pháp moment cho ước lượng bằng cách', 'cho moment mẫu bằng moment lý thuyết', ['cực đại hàm hợp lý', 'cực tiểu phương sai', 'lấy trung vị mẫu']),
            ('Nếu mẫu X₁,…,Xₙ độc lập cùng phân phối với phương sai σ² thì Var(X̄) bằng', 'σ²/n', ['σ²', 'σ/√n', 'nσ²']),
            ('Định lý giới hạn trung tâm nói với n lớn, X̄ xấp xỉ', 'chuẩn N(μ, σ²/n)', ['đều', 'mũ', 'nhị thức'])]
    for s, ok, bad in txts: txt(B, s, ok, bad, 'Kiến thức §2.1–2.2.', 1, T['theory'])
