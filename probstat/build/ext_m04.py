"""Module 4 — mở rộng: khái niệm + họ bài toàn phần/Bayes (đáp án tự tính)."""
import random
from qb import f, fg
from qh import pm
from orig_m04 import TOP, tot, post
SRC = 'Bổ sung: dạng bài §1.6 / Lecture Notes 1.20–1.23 (đáp án tự tính bằng công thức toàn phần/Bayes)'
def build(B):
    rng = random.Random(2504)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Hệ đầy đủ các biến cố A₁, …, Aₙ phải thỏa', 'đôi một xung khắc và tổng xác suất bằng 1', ['độc lập đôi một', 'có xác suất bằng nhau', 'có hợp bằng ∅'], 'Chia không gian mẫu thành các phần không chồng lấn.', 1, 'system')
    C('Công thức xác suất toàn phần là', 'P(B) = Σ P(Aᵢ)P(B | Aᵢ)', ['P(B) = Σ P(Aᵢ | B)', 'P(B) = Π P(B | Aᵢ)', 'P(B) = Σ P(Aᵢ)/P(B | Aᵢ)'], 'Trung bình có trọng số của P(B|Aᵢ).', 1, 'total')
    C('Công thức Bayes P(Aᵢ | B) bằng', 'P(Aᵢ)P(B | Aᵢ)/P(B)', ['P(B | Aᵢ)/P(Aᵢ)', 'P(Aᵢ)P(B)', 'P(B | Aᵢ) + P(Aᵢ)'], 'Đảo chiều điều kiện.', 1, 'bayes')
    C('Xác suất hậu nghiệm là', 'xác suất của nguyên nhân sau khi biết kết quả', ['xác suất của kết quả trước thí nghiệm', 'xác suất của biến cố đối', 'xác suất độc lập'], 'P(Aᵢ | B) với B đã quan sát.', 1, 'bayes')
    C('Tổng các xác suất hậu nghiệm Σᵢ P(Aᵢ | B) luôn bằng', '1', ['0', 'P(B)', 'n'], 'Hệ đầy đủ: B chắc chắn thuộc một nguyên nhân.', 1, 'bayes')
    C('Độ nhạy của xét nghiệm là', 'P(dương tính | có bệnh)', ['P(có bệnh | dương tính)', 'P(âm tính | có bệnh)', 'P(dương tính)'], 'Khả năng phát hiện người bệnh.', 1, 'bayes')
    C('Độ đặc hiệu của xét nghiệm là', 'P(âm tính | không bệnh)', ['P(dương tính | bệnh)', 'P(bệnh | âm tính)', '1 − độ nhạy'], 'Khả năng loại trừ người khỏe.', 1, 'bayes')
    C('Bệnh hiếm, xét nghiệm tốt nhưng người dương tính vẫn thường khỏe vì', 'tiên nghiệm (tỉ lệ mắc) rất nhỏ', ['xét nghiệm luôn sai', 'độ nhạy bằng 0', 'Bayes không áp dụng'], 'Số dương tính giả từ nhóm khỏe đông áp đảo.', 2, 'bayes')
    C('Với P(A | B) = 0.9, kết luận nào đúng?', 'Chưa suy ra được P(B | A) nếu thiếu P(A), P(B)', ['P(B | A) = 0.9', 'P(B | A) = 0.1', 'A, B độc lập'], 'P(A|B) ≠ P(B|A) nói chung.', 2, 'bayes')
    C('Trong cây xác suất, xác suất một đường đi bằng', 'tích các xác suất trên các nhánh', ['tổng các xác suất trên các nhánh', 'xác suất nhánh cuối', 'trung bình các nhánh'], 'Công thức nhân.', 1, 'tree')
    C('Để có P(B) từ cây xác suất ta', 'cộng xác suất các đường đi dẫn tới B', ['nhân các đường đi', 'chọn đường lớn nhất', 'lấy trung bình'], 'Các đường đi xung khắc.', 1, 'tree')
    C('Nếu P(Aᵢ) bằng nhau với mọi i thì P(Aᵢ | B) tỉ lệ với', 'P(B | Aᵢ)', ['P(B)', '1/P(B | Aᵢ)', 'P(Aᵢ)²'], 'Tiên nghiệm triệt tiêu khỏi tỉ số.', 2, 'bayes')
    # ba phân xưởng
    for k in range(14):
        a = rng.choice([20, 25, 30, 35, 40, 45, 50]); b = rng.choice([x for x in (15, 20, 25, 30, 35) if a + x < 90]); c = 100 - a - b
        pri = [a / 100, b / 100, c / 100]; lk = [rng.choice([1, 2, 3, 4, 5, 6, 8]) / 100 for _ in range(3)]
        if len(set(lk)) < 2: lk[1] += 0.01
        T = tot(pri, lk); i = rng.randrange(3); ph = post(pri, lk, i)
        desc = f'Ba phân xưởng sản xuất {a}%, {b}%, {c}% sản lượng với tỉ lệ phế phẩm {", ".join(fg(l*100)+"%" for l in lk)}.'
        if k % 2 == 0:
            P(desc + ' P(một sản phẩm ngẫu nhiên là phế phẩm) bằng', T, f'Σ P(Aᵢ)P(B|Aᵢ) = {f(T,4)}.', 1, TOP['total'], SRC, extra=[sum(lk) / 3, max(lk), sum(pri[j] for j in range(3)) * 0 + lk[i]], d=4)
        else:
            P(desc + f' Biết sản phẩm là phế phẩm, xác suất nó do phân xưởng {i+1} làm là', ph, f'P(A{i+1}|B) = {fg(pri[i],3)}·{fg(lk[i],3)}/{f(T,4)} = {f(ph,4)}.', 2, TOP['bayes'], SRC, extra=[pri[i], lk[i], pri[i] * lk[i]], d=4)
    # xét nghiệm
    for prev, se, sp in [(0.01, 0.95, 0.9), (0.02, 0.9, 0.95), (0.005, 0.99, 0.98), (0.1, 0.8, 0.9), (0.05, 0.95, 0.85), (0.001, 0.99, 0.99), (0.2, 0.9, 0.9), (0.03, 0.85, 0.92)]:
        pp = se * prev + (1 - sp) * (1 - prev); ppv = se * prev / pp
        npv = sp * (1 - prev) / (sp * (1 - prev) + (1 - se) * prev)
        P(f'Bệnh có tỉ lệ mắc {prev*100:g}%; xét nghiệm có độ nhạy {se*100:g}% và độ đặc hiệu {sp*100:g}%. P(dương tính) bằng', pp, f'{se}·{prev} + {fg(1-sp)}·{fg(1-prev)} = {f(pp,5)}.', 2, TOP['total'], SRC, extra=[se, se * prev, 1 - sp], d=4)
        P(f'Bệnh có tỉ lệ mắc {prev*100:g}%; xét nghiệm có độ nhạy {se*100:g}% và độ đặc hiệu {sp*100:g}%. P(bệnh | dương tính) bằng', ppv, f'{f(se*prev,5)}/{f(pp,5)} = {f(ppv,4)}.', 3, TOP['bayes'], SRC, extra=[se, prev, 1 - ppv], d=4)
        P(f'Bệnh có tỉ lệ mắc {prev*100:g}%; xét nghiệm có độ nhạy {se*100:g}% và độ đặc hiệu {sp*100:g}%. P(không bệnh | âm tính) bằng', npv, f'{f(sp*(1-prev),5)}/{f(sp*(1-prev)+(1-se)*prev,5)} = {f(npv,4)}.', 3, TOP['bayes'], SRC, extra=[sp, 1 - npv, 1 - prev], d=4)
    # hai hộp
    for (w1, b1, w2, b2, p1) in [(3, 2, 2, 4, 0.5), (5, 5, 1, 9, 0.5), (4, 1, 3, 3, 0.6), (2, 8, 6, 4, 0.3), (7, 3, 2, 8, 0.4), (1, 4, 4, 1, 0.5)]:
        q1, q2 = w1 / (w1 + b1), w2 / (w2 + b2); T = p1 * q1 + (1 - p1) * q2; ph = p1 * q1 / T
        P(f'Hộp I: {w1} trắng {b1} đen; hộp II: {w2} trắng {b2} đen. Chọn hộp I với xác suất {p1}, rồi rút một bi. P(bi trắng) bằng', T, f'{p1}·{f(q1,4)} + {fg(1-p1)}·{f(q2,4)} = {f(T,4)}.', 2, TOP['total'], SRC, extra=[(q1 + q2) / 2, q1, q2], d=4)
        P(f'Hộp I: {w1} trắng {b1} đen; hộp II: {w2} trắng {b2} đen. Chọn hộp I với xác suất {p1}, rồi rút một bi. Biết bi trắng, P(từ hộp I) bằng', ph, f'{f(p1*q1,4)}/{f(T,4)} = {f(ph,4)}.', 3, TOP['bayes'], SRC, extra=[p1, q1, 1 - ph], d=4)
    # kênh nhiễu
    for p1, e in [(0.6, 0.1), (0.5, 0.05), (0.7, 0.2), (0.4, 0.15), (0.8, 0.1), (0.3, 0.05)]:
        r1 = p1 * (1 - e) + (1 - p1) * e; ph = p1 * (1 - e) / r1
        P(f'Nguồn gửi bit 1 với xác suất {p1}; kênh lật bit với xác suất {e}. Biết nhận được bit 1, P(đã gửi 1) bằng', ph, f'P(nhận 1) = {f(r1,4)}; Bayes: {f(p1*(1-e),4)}/{f(r1,4)} = {f(ph,4)}.', 3, TOP['bayes'], SRC, extra=[1 - e, p1, r1], d=4)
    B.essay('Ba máy A, B, C làm 40%, 35%, 25% tổng số chi tiết với tỉ lệ lỗi 1%, 2%, 4%. (a) P(chi tiết lỗi)? (b) Chi tiết lỗi, xác suất do C?', '(a) 0.4·0.01 + 0.35·0.02 + 0.25·0.04 = 0.004 + 0.007 + 0.010 = 0.021. (b) 0.010/0.021 = 0.4762.', 2, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Một bệnh có tỉ lệ 0.5%. Xét nghiệm có độ nhạy 98% và độ đặc hiệu 97%. Tính giá trị tiên đoán dương và giải thích vì sao thấp.', 'P(+) = 0.98·0.005 + 0.03·0.995 = 0.0049 + 0.02985 = 0.03475; PPV = 0.0049/0.03475 = 0.141. Thấp vì bệnh hiếm: người khỏe dương tính giả (2.985%) đông hơn người bệnh thật (0.49%).', 3, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Vẽ cây xác suất cho: chọn máy 1 (70%) hoặc máy 2 (30%); mỗi máy cho sản phẩm loại tốt với xác suất 0.95 và 0.90. Tính P(tốt) và P(máy 2 | không tốt).', 'P(tốt) = 0.665 + 0.27 = 0.935. P(không tốt) = 0.065; P(máy 2 | không tốt) = 0.03/0.065 = 0.4615.', 2, TOP['tree'], SRC, 'bo_sung')
