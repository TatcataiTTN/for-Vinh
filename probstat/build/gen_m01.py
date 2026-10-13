"""Module 1 — biến thể tham số (nhãn bo_sung), đáp án tính bằng pskit."""
import random, math
from pskit import *
from qb import f, fg, nd, ni
from orig_m01 import TOPIC, nums_text

SRC = 'Bổ sung: biến thể tham số của dạng bài §1.1 / PS 24.1 (đáp án tự tính, đối chiếu numpy)'
def build(B):
    rng = random.Random(1101)
    ctx = [('thời gian chạy một chương trình (giây)', 1), ('số khách đến quầy trong 10 phút', 0), ('điểm kiểm tra giữa kỳ của một nhóm sinh viên', 1),
           ('chiều cao cây giống (cm)', 1), ('số lỗi in trên một trang', 0), ('điện áp đo được (V)', 1)]
    for k in range(12):
        c, dd = ctx[k % len(ctx)]
        n = rng.randint(7, 12)
        base = rng.choice([4, 6, 8, 12, 20, 50])
        x = [round(base + rng.gauss(0, base / 4), dd) if dd else max(0, int(round(base + rng.gauss(0, base / 3)))) for _ in range(n)]
        if k % 3 == 0: x[rng.randrange(n)] = round(max(x) * 1.9 + 3, dd) if dd else int(max(x) * 2 + 5)
        check_basic(x)
        m = mean(x); s = sd_s(x); qL, qM, qU = quartiles(x); R = qU - qL; ol = outliers(x)
        D = 3; dd2 = max(dd, 1)
        stem = f'Đo {c}, được n = {n} giá trị: {nums_text(x)}.'
        B.mcq(stem + '\nTính trung bình mẫu x̄.', f(m, D), nd(m, rng, D, extra=[qM, sum(x) / (n - 1)]),
              f'x̄ = {fg(sum(x),4)}/{n} = {f(m,D)}.', 1, TOPIC['mean'], SRC, 'bo_sung')
        B.mcq(stem + '\nTính độ lệch chuẩn mẫu s.', f(s, D), nd(s, rng, D, extra=[math.sqrt(var_p(x)), var_s(x), R]),
              f's² = Σ(xᵢ−x̄)²/(n−1) = {f(var_s(x),D+1)}; s = {f(s,D)} (chia cho n sẽ cho {f(math.sqrt(var_p(x)),D)}).', 2, TOPIC['spread'], SRC, 'bo_sung')
        B.mcq(stem + '\nTính IQR (qL, qU là trung vị nửa dưới, nửa trên; bỏ qM khi n lẻ).', f(R, dd2), nd(R, rng, dd2, extra=[max(x) - min(x), qU - qM]),
              f'qL = {fg(qL,4)}, qM = {fg(qM,4)}, qU = {fg(qU,4)} ⇒ IQR = {fg(R,4)}.', 2, TOPIC['quart'], SRC, 'bo_sung')
        B.mcq(stem + '\nCó bao nhiêu giá trị ngoại lai theo tiêu chuẩn 1.5·IQR?', str(len(ol)), [str(i) for i in range(4) if i != len(ol)] + ['4'],
              f'Ngưỡng [{fg(qL-1.5*R,4)}; {fg(qU+1.5*R,4)}]; ' + (f'ngoại lai: {nums_text(ol)}.' if ol else 'không có giá trị nào vượt ngưỡng.'), 3, TOPIC['quart'], SRC, 'bo_sung')
    # biến đổi tuyến tính y = a x + b
    for k in range(6):
        m0 = rng.choice([12, 15, 20, 30, 45]); s0 = rng.choice([2, 3, 4, 5]); a = rng.choice([2, 3, -2, 0.5, 10]); b = rng.choice([-5, 1, 10, 100])
        mm = a * m0 + b; ss = abs(a) * s0; vv = a * a * s0 * s0
        B.mcq(f'Một mẫu có x̄ = {m0}, s = {s0}. Đổi biến yᵢ = {fg(a)}·xᵢ {"+" if b>=0 else "−"} {abs(b)}. Độ lệch chuẩn s_y là bao nhiêu?', fg(ss), [fg(a*s0+b), fg(vv), fg(s0 + b), fg(ss * 2), fg(ss + 1), fg(ss + 3)],
              f'Cộng hằng số b không đổi độ phân tán; nhân với a nhân s với |a|: s_y = |{fg(a)}|·{s0} = {fg(ss)}. (Trung bình mới ȳ = {fg(a)}·{m0} {"+" if b>=0 else "−"} {abs(b)} = {fg(mm)}.)', 2, TOPIC['spread'], SRC, 'bo_sung')
        B.mcq(f'Một mẫu có x̄ = {m0}, s = {s0}. Đổi biến yᵢ = {fg(a)}·xᵢ {"+" if b>=0 else "−"} {abs(b)}. Trung bình ȳ là bao nhiêu?', fg(mm), [fg(a*m0), fg(m0 + b), fg(a * (m0 + b)), fg(mm + 1), fg(mm - 2)],
              f'ȳ = a·x̄ + b = {fg(a)}·{m0} {"+" if b>=0 else "−"} {abs(b)} = {fg(mm)}.', 1, TOPIC['mean'], SRC, 'bo_sung')
    # dữ liệu theo lớp
    for k in range(6):
        w = rng.choice([2, 5, 10]); st0 = rng.choice([0, 10, 20, 50]); m_ = 4
        cnt = [rng.randint(2, 12) for _ in range(m_)]
        mids = [st0 + w * (i + 0.5) for i in range(m_)]
        N = sum(cnt); xb = sum(a * b for a, b in zip(mids, cnt)) / N
        s2 = sum(b * (a - xb) ** 2 for a, b in zip(mids, cnt)) / (N - 1)
        tab = ', '.join(f'{fg(st0+w*i)}–{fg(st0+w*(i+1))}: {c}' for i, c in enumerate(cnt))
        B.mcq(f'Bảng tần số (lớp: số quan sát) — {tab}. Lấy điểm giữa của lớp, tính trung bình mẫu x̄.', f(xb, 3), nd(xb, rng, 3, extra=[sum(a*b for a,b in zip(mids,cnt))/(N-1), st0 + w * 2]),
              f'N = {N}; điểm giữa {nums_text(mids)}; x̄ = Σnᵢxᵢ/N = {fg(sum(a*b for a,b in zip(mids,cnt)),4)}/{N} = {f(xb,3)}.', 2, TOPIC['group'], SRC, 'bo_sung')
        B.mcq(f'Bảng tần số (lớp: số quan sát) — {tab}. Tính phương sai mẫu s² theo điểm giữa lớp.', f(s2, 3), nd(s2, rng, 3, extra=[sum(b*(a-xb)**2 for a,b in zip(mids,cnt))/N, math.sqrt(s2)]),
              f's² = Σnᵢ(xᵢ−x̄)²/(N−1) = {f(sum(b*(a-xb)**2 for a,b in zip(mids,cnt)),3)}/{N-1} = {f(s2,3)}.', 3, TOPIC['group'], SRC, 'bo_sung')
    # 5 số tóm tắt
    for k in range(6):
        mn = rng.randint(1, 20); a_ = mn + rng.randint(3, 10); b_ = a_ + rng.randint(2, 8); c_ = b_ + rng.randint(3, 10); mx = c_ + rng.randint(5, 40)
        R = c_ - a_; lo = a_ - 1.5 * R; hi = c_ + 1.5 * R
        nout = (mx > hi) + (mn < lo)
        B.mcq(f'Boxplot có min = {mn}, qL = {a_}, qM = {b_}, qU = {c_}, max = {mx}. Ngưỡng ngoại lai phía trên qU + 1.5·IQR bằng bao nhiêu?', fg(hi), [fg(c_ + R), fg(c_ + 3 * R), fg(mx + 1.5 * R)],
              f'IQR = {c_} − {a_} = {R}; qU + 1.5·IQR = {c_} + {fg(1.5*R)} = {fg(hi)}. ' + (f'Vì max = {mx} > {fg(hi)} nên max là ngoại lai.' if mx > hi else f'max = {mx} ≤ {fg(hi)} nên không có ngoại lai phía trên.'), 2, TOPIC['quart'], SRC, 'bo_sung')
