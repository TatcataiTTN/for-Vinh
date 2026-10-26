"""Module 4 — mở rộng đợt 2: odds, cập nhật liên tiếp, bảng đếm, tỉ lệ nền, đoán mò (đáp án tự tính)."""
import random
from qb import f, fg
from qh import pm
from orig_m04 import TOP, tot, post
SRC = 'Bổ sung: dạng bài §1.6 mở rộng (Bayes dạng odds, cập nhật liên tiếp, bảng đếm; đáp án tự tính bằng công thức Bayes)'
def build(B):
    rng = random.Random(3504)
    def P(*a, **k):
        k.setdefault('origin', 'bo_sung'); k.setdefault('hi', None); return pm(B, rng, *a, **k)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOP[topic], SRC, 'bo_sung')
    C('Odds của biến cố H có xác suất p là', 'p/(1 − p)', ['p·(1 − p)', '1/p', 'p − (1 − p)'], 'Odds = xác suất xảy ra / xác suất không xảy ra.', 1, 'bayes')
    C('Dạng odds của Bayes: odds hậu nghiệm bằng', 'odds tiên nghiệm × tỉ số hợp lý', ['odds tiên nghiệm + tỉ số hợp lý', 'tỉ số hợp lý / odds tiên nghiệm', 'odds tiên nghiệm²'], 'Nhân từng bằng chứng một.', 2, 'bayes')
    C('Tỉ số hợp lý của kết quả dương tính là', 'độ nhạy / (1 − độ đặc hiệu)', ['độ nhạy × độ đặc hiệu', '(1 − độ nhạy)/độ đặc hiệu', 'độ nhạy + độ đặc hiệu'], 'LR₊ = P(+|bệnh)/P(+|khỏe).', 2, 'bayes')
    C('Tỉ số hợp lý LR = 1 nghĩa là', 'bằng chứng không làm đổi xác suất', ['chắc chắn có bệnh', 'chắc chắn không bệnh', 'xét nghiệm hoàn hảo'], 'Odds hậu nghiệm = odds tiên nghiệm.', 2, 'bayes')
    C('Nếu hai bằng chứng độc lập có điều kiện thì tỉ số hợp lý chung bằng', 'tích hai tỉ số hợp lý', ['tổng hai tỉ số hợp lý', 'tỉ số hợp lý lớn hơn', 'trung bình hai tỉ số'], 'Nhân các LR.', 2, 'bayes')
    C('Ngụy biện của công tố viên là việc', 'nhầm P(bằng chứng | vô tội) với P(vô tội | bằng chứng)', ['bỏ qua bằng chứng', 'dùng sai xác suất toàn phần', 'cộng thay vì nhân xác suất'], 'Đảo sai chiều điều kiện, bỏ qua tỉ lệ nền.', 2, 'bayes')
    C('“Bỏ qua tỉ lệ nền” nghĩa là', 'không dùng xác suất tiên nghiệm khi suy luận', ['dùng quá nhiều biến cố', 'chỉ dùng xác suất toàn phần', 'chia cho P(B) hai lần'], 'Tiên nghiệm nhỏ làm hậu nghiệm nhỏ dù bằng chứng mạnh.', 1, 'bayes')
    C('Nghịch lý Simpson là hiện tượng', 'xu hướng ở từng nhóm đảo ngược khi gộp các nhóm', ['xác suất lớn hơn 1', 'hai biến cố vừa độc lập vừa xung khắc', 'Bayes cho tổng hậu nghiệm khác 1'], 'Do trọng số nhóm khác nhau (biến ẩn).', 2, 'total')
    C('Trong bài Monty Hall (người dẫn biết xe), đổi cửa thắng với xác suất', '2/3', ['1/2', '1/3', '3/4'], 'Người dẫn mở cửa dê có điều kiện nên đổi cửa có lợi.', 2, 'bayes')
    C('Bốn nguyên nhân A₁…A₄ tạo hệ đầy đủ. Muốn có hậu nghiệm của A₂ ta cần', 'P(Aᵢ) và P(B|Aᵢ) cho cả bốn nguyên nhân', ['chỉ P(A₂) và P(B|A₂)', 'chỉ P(B)', 'chỉ P(B|A₂)'], 'Mẫu số P(B) cần tổng cả bốn.', 2, 'bayes')
    C('Xét nghiệm lặp độc lập, kết quả lần hai dùng làm tiên nghiệm', 'chính là hậu nghiệm sau lần một', ['là tiên nghiệm gốc', 'bằng 0.5', 'bằng độ nhạy'], 'Cập nhật liên tiếp: hậu nghiệm hôm nay là tiên nghiệm ngày mai.', 2, 'bayes')
    C('Với bảng đếm, P(A|B) bằng', 'số phần tử A∩B / số phần tử B', ['số phần tử A∩B / số phần tử A', 'số phần tử A / tổng', 'số phần tử B / số phần tử A'], 'Thu hẹp không gian mẫu vào B.', 1, 'bayes')
    C('Nếu P(Aᵢ | B) > P(Aᵢ) thì', 'bằng chứng B ủng hộ nguyên nhân Aᵢ', ['B và Aᵢ độc lập', 'Aᵢ không thể xảy ra', 'P(B | Aᵢ) < P(B)'], 'P(B|Aᵢ) > P(B) tương đương.', 2, 'bayes')
    C('Tổng các xác suất tiên nghiệm của một hệ đầy đủ bằng', '1', ['0', 'P(B)', 'số nguyên nhân'], 'Hệ đầy đủ chia toàn bộ không gian mẫu.', 1, 'system')
    C('Xác suất của một đường đi trong cây hai giai đoạn: nhánh thứ hai ghi', 'xác suất có điều kiện theo nhánh thứ nhất', ['xác suất không điều kiện', 'xác suất tiên nghiệm', 'xác suất hậu nghiệm'], 'Công thức nhân: P(A)·P(B|A).', 1, 'tree')
    # odds / LR
    for pr, se, sp in [(0.01, 0.95, 0.9), (0.02, 0.9, 0.95), (0.05, 0.8, 0.9), (0.1, 0.9, 0.9), (0.001, 0.99, 0.99), (0.2, 0.85, 0.9), (0.03, 0.95, 0.8), (0.15, 0.9, 0.85), (0.01, 0.99, 0.95), (0.04, 0.9, 0.9)]:
        LR = se / (1 - sp); o = pr / (1 - pr) * LR; p1 = o / (1 + o)
        P(f'Bệnh có tỉ lệ mắc {fg(pr*100)}%; xét nghiệm nhạy {fg(se*100)}%, đặc hiệu {fg(sp*100)}%. Tỉ số hợp lý của kết quả dương tính (LR₊) bằng', LR, f'LR₊ = {fg(se)}/{fg(1-sp)} = {f(LR,3)}.', 2, TOP['bayes'], SRC, extra=[se / sp, se * sp, 1 / LR], d=3)
        P(f'Bệnh có tỉ lệ mắc {fg(pr*100)}%; xét nghiệm nhạy {fg(se*100)}%, đặc hiệu {fg(sp*100)}%. Dùng odds: P(bệnh | dương tính) bằng', p1, f'Odds tiên nghiệm = {f(pr/(1-pr),4)}; ×LR₊ = {f(o,4)}; P = o/(1+o) = {f(p1,4)}.', 3, TOP['bayes'], SRC, extra=[pr, se, o], d=4)
        o2 = o * LR; p2 = o2 / (1 + o2)
        P(f'Bệnh có tỉ lệ mắc {fg(pr*100)}%; xét nghiệm nhạy {fg(se*100)}%, đặc hiệu {fg(sp*100)}%. Làm lại độc lập và dương tính lần hai. P(bệnh | hai lần dương tính) bằng', p2, f'Odds = {f(pr/(1-pr),4)}·{f(LR,3)}² = {f(o2,4)} ⇒ P = {f(p2,4)}.', 3, TOP['bayes'], SRC, extra=[p1, se, 1 - p2], d=4)
    # đoán mò
    for pk, mopt in [(0.6, 4), (0.5, 4), (0.7, 5), (0.4, 4), (0.8, 3), (0.3, 5), (0.9, 4), (0.5, 2), (0.6, 3), (0.2, 4)]:
        pc = pk + (1 - pk) / mopt; ph = pk / pc
        P(f'Sinh viên biết bài với xác suất {fg(pk)}; nếu không biết thì đoán ngẫu nhiên trong {mopt} đáp án. P(trả lời đúng) bằng', pc, f'{fg(pk)} + {fg(1-pk)}/{mopt} = {f(pc,4)}.', 2, TOP['total'], SRC, extra=[pk, (1 - pk) / mopt, 1 / mopt], d=4)
        P(f'Sinh viên biết bài với xác suất {fg(pk)}; nếu không biết thì đoán ngẫu nhiên trong {mopt} đáp án. Biết trả lời đúng, P(thật sự biết) bằng', ph, f'{fg(pk)}/{f(pc,4)} = {f(ph,4)}.', 3, TOP['bayes'], SRC, extra=[pk, pc, 1 - ph], d=4)
    # tỉ lệ nền
    for pb, acc in [(0.15, 0.8), (0.1, 0.9), (0.05, 0.95), (0.3, 0.7), (0.02, 0.9), (0.25, 0.85), (0.4, 0.75), (0.12, 0.8)]:
        pt = pb * acc / (pb * acc + (1 - pb) * (1 - acc))
        P(f'{fg((1-pb)*100)}% taxi xanh lá, {fg(pb*100)}% taxi xanh dương. Nhân chứng nhận màu đúng {fg(acc*100)}% (cả hai màu). Nhân chứng nói taxi màu xanh dương. P(đúng là xanh dương) bằng', pt, f'{fg(pb*acc)}/({fg(pb*acc)} + {fg((1-pb)*(1-acc))}) = {f(pt,4)}.', 3, TOP['bayes'], SRC, extra=[acc, pb, 1 - pt], d=4)
    # bảng đếm
    for _ in range(10):
        a1, a2 = rng.randint(60, 150), rng.randint(60, 150); y1, y2 = rng.randint(10, a1 - 5), rng.randint(5, a2 - 5)
        pA1 = y1 / (y1 + y2)
        P(f'Nhóm A có {a1} người, nhóm B có {a2} người. Số người trả lời “có”: A {y1}, B {y2}. Chọn ngẫu nhiên một người trả lời “có”, P(thuộc nhóm A) bằng', pA1, f'{y1}/({y1}+{y2}) = {f(pA1,4)}.', 2, TOP['bayes'], SRC, extra=[y1 / a1, a1 / (a1 + a2), y1 / (a1 + a2)], d=4)
    # đường đi trong cây
    for _ in range(8):
        p1 = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7]); q1 = rng.choice([0.9, 0.95, 0.8, 0.85]); q2 = rng.choice([0.6, 0.7, 0.75, 0.5, 0.65])
        T = p1 * q1 + (1 - p1) * q2; ph = (1 - p1) * q2 / T
        P(f'Cây hai giai đoạn: máy 1 (xác suất {p1}) cho sản phẩm tốt với xác suất {q1}; máy 2 cho sản phẩm tốt với xác suất {q2}. Biết sản phẩm tốt, P(từ máy 2) bằng', ph, f'P(tốt) = {f(T,4)}; ({fg(1-p1)}·{q2})/{f(T,4)} = {f(ph,4)}.', 3, TOP['bayes'], SRC, extra=[1 - p1, q2, (1 - p1) * q2], d=4)
    B.essay('Bệnh có tỉ lệ 2%; xét nghiệm nhạy 90%, đặc hiệu 95%. (a) Tính LR₊. (b) Dùng odds tìm P(bệnh | dương tính). (c) Nếu làm lại độc lập và lại dương tính, P(bệnh) là bao nhiêu?', 'LR₊ = 0.9/0.05 = 18. Odds tiên nghiệm = 0.02/0.98 = 0.02041; hậu nghiệm = 0.3673 ⇒ P = 0.2687. Lần hai: odds = 0.3673·18 = 6.612 ⇒ P = 0.8686.', 3, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Giải thích bằng công thức vì sao trong nghịch lý Simpson phương pháp A tốt hơn ở từng nhóm nhưng B tốt hơn khi gộp (dùng số liệu 81/87, 192/263 và 234/270, 55/80).', 'A: 93.1% và 73.0%; B: 86.7% và 68.8%; A tốt hơn ở cả hai. Gộp: A 273/350 = 78%, B 289/350 = 82.6%. Tỉ lệ gộp là trung bình có trọng số: A dùng nhiều ở nhóm khó (263/350 sỏi lớn), B dùng nhiều ở nhóm dễ (270/350 sỏi nhỏ), nên trọng số khác nhau đảo kết luận.', 3, TOP['total'], SRC, 'bo_sung')
    B.essay('Một thư có từ “trúng thưởng”: 40% thư là rác; từ này xuất hiện ở 50% thư rác và 2% thư thường. (a) Tính P(rác | có từ). (b) Nếu thêm từ “miễn phí” (40% rác, 5% thường, độc lập có điều kiện) thì P(rác) mới là bao nhiêu?', '(a) 0.2/(0.2 + 0.012) = 0.9434. (b) Tử 0.4·0.5·0.4 = 0.08; mẫu 0.08 + 0.6·0.02·0.05 = 0.0806 ⇒ 0.9926.', 3, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Ba tấm thẻ: đỏ–đỏ, đỏ–xanh, xanh–xanh. Rút một thẻ, thấy một mặt đỏ. Tính xác suất mặt kia đỏ bằng hai cách (liệt kê mặt và Bayes).', 'Liệt kê: 3 mặt đỏ đồng khả năng, 2 mặt thuộc thẻ đỏ–đỏ ⇒ 2/3. Bayes: (1/3·1)/(1/3·1 + 1/3·1/2) = 2/3.', 2, TOP['bayes'], SRC, 'bo_sung')
