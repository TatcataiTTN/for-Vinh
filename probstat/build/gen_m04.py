"""Module 4 — biến thể tham số: xác suất toàn phần, Bayes, kiểm tra y tế, kênh nhiễu, hai giai đoạn."""
import random
from qb import f, fg, nd
from qh import pm
from orig_m04 import TOP, tot, post
SRC = 'Bổ sung: biến thể tham số của dạng bài §1.6 (đáp án tự tính bằng công thức toàn phần/Bayes, kiểm bằng phân số chính xác)'
def build(B):
    rng = random.Random(1404); P = lambda *a, **k: pm(B, rng, *a, **k)
    # 1. ba phân xưởng
    for k in range(10):
        a = rng.choice([20, 25, 30, 35, 40, 45, 50]); b = rng.choice([x for x in (15, 20, 25, 30, 35, 40) if a + x < 90]); c = 100 - a - b
        l = [rng.choice([1, 2, 3, 4, 5, 6, 8]) / 100 for _ in range(3)]
        pr = [a / 100, b / 100, c / 100]; T = tot(pr, l); i = rng.randrange(3); nm = ['I', 'II', 'III'][i]
        lt = ', '.join(f'{x * 100:g}%' for x in l)
        P(f'Ba phân xưởng I, II, III sản xuất {a}%, {b}%, {c}% sản lượng với tỉ lệ phế phẩm {lt}. Xác suất một sản phẩm ngẫu nhiên là phế phẩm là', T,
          f'P(B) = ' + ' + '.join(f'{p}·{x}' for p, x in zip(pr, l)) + f' = {f(T,5)}.', 1 if k < 5 else 2, TOP['total'], SRC, extra=[sum(l) / 3, max(l), pr[i] * l[i]], d=4, origin='bo_sung')
        P(f'Ba phân xưởng I, II, III sản xuất {a}%, {b}%, {c}% sản lượng với tỉ lệ phế phẩm {lt}. Biết sản phẩm là phế phẩm, xác suất nó do phân xưởng {nm} sản xuất là', post(pr, l, i),
          f'P(A{i+1} | B) = {pr[i]}·{l[i]}/{f(T,5)} = {f(post(pr,l,i),4)} (tiên nghiệm {pr[i]}).', 2, TOP['bayes'], SRC, extra=[pr[i], l[i], pr[i] * l[i] / max(l)], d=4, origin='bo_sung')
    # 2. xét nghiệm y tế
    for prev, sens, spec in [(0.01, 0.95, 0.90), (0.02, 0.99, 0.95), (0.001, 0.99, 0.99), (0.05, 0.90, 0.92), (0.10, 0.80, 0.90), (0.005, 0.98, 0.97), (0.15, 0.85, 0.95), (0.03, 0.92, 0.88)]:
        pt = prev * sens + (1 - prev) * (1 - spec)
        ppv = prev * sens / pt
        npv = (1 - prev) * spec / (1 - pt)
        P(f'Một bệnh có tỉ lệ mắc {prev*100:g}% trong dân số. Xét nghiệm có độ nhạy {sens*100:g}% (dương tính nếu có bệnh) và độ đặc hiệu {spec*100:g}% (âm tính nếu không bệnh). Xác suất một người chọn ngẫu nhiên có kết quả dương tính là', pt,
          f'P(+) = {prev}·{sens} + {1-prev:g}·{1-spec:.2f} = {f(prev*sens,5)} + {f((1-prev)*(1-spec),5)} = {f(pt,5)}.', 2, TOP['total'], SRC, extra=[sens, prev, prev * sens], d=5, origin='bo_sung')
        P(f'Một bệnh có tỉ lệ mắc {prev*100:g}%. Xét nghiệm có độ nhạy {sens*100:g}% và độ đặc hiệu {spec*100:g}%. Biết một người dương tính, xác suất người đó thật sự có bệnh là', ppv,
          f'Bayes: P(bệnh | +) = {prev}·{sens}/{f(pt,5)} = {f(ppv,4)}. Khi bệnh hiếm, ngay cả xét nghiệm chính xác cũng cho nhiều dương tính giả (sai lầm tỉ lệ nền).', 3, TOP['bayes'], SRC, extra=[sens, spec, prev], d=4, origin='bo_sung')
        if prev in (0.01, 0.1, 0.03):
            P(f'Bệnh mắc {prev*100:g}%, độ nhạy {sens*100:g}%, độ đặc hiệu {spec*100:g}%. Biết một người âm tính, xác suất người đó thật sự không bệnh là', npv,
              f'P(không bệnh | −) = {1-prev:g}·{spec}/(1 − {f(pt,5)}) = {f(npv,5)}.', 3, TOP['bayes'], SRC, extra=[spec, 1 - prev, 1 - sens], d=5, origin='bo_sung')
    # 3. kênh nhiễu
    for p1, e1, e2 in [(0.6, 0.1, 0.2), (0.7, 0.05, 0.1), (0.5, 0.02, 0.04), (0.8, 0.1, 0.3), (0.3, 0.15, 0.05)]:
        pr = [p1, 1 - p1]; lk = [1 - e1, e2]; T = tot(pr, lk)
        P(f'Trạm phát bit 1 với xác suất {p1}, bit 0 với xác suất {1-p1:g}. Nhiễu làm bit 1 bị thu thành 0 với xác suất {e1}, bit 0 bị thu thành 1 với xác suất {e2}. Xác suất thu được bit 1 là', T, f'P(thu 1) = {p1}·{1-e1:.2f} + {1-p1:g}·{e2} = {f(T,5)}.', 2, TOP['total'], SRC, extra=[p1, 1 - e1, e2], d=5, origin='bo_sung')
        P(f'Trạm phát bit 1 với xác suất {p1}, bit 0 với xác suất {1-p1:g}; bit 1 bị đọc nhầm thành 0 với xác suất {e1}, bit 0 bị đọc nhầm thành 1 với xác suất {e2}. Nhận được bit 1, xác suất đã phát bit 1 là', post(pr, lk, 0), f'P(phát 1 | thu 1) = {p1}·{1-e1:.2f}/{f(T,5)} = {f(post(pr,lk,0),4)}.', 3, TOP['bayes'], SRC, extra=[p1, 1 - e1, e2], d=4, origin='bo_sung')
    # 4. hai giai đoạn: chọn hộp rồi rút bi
    for (ra, ba, rb, bb) in [(3, 7, 6, 4), (5, 5, 2, 8), (4, 6, 7, 3), (2, 8, 9, 1), (6, 4, 3, 7)]:
        pa = ra / (ra + ba); pbb = rb / (rb + bb); T = 0.5 * pa + 0.5 * pbb; pst = 0.5 * pa / T
        P(f'Hai hộp: hộp 1 có {ra} bi đỏ, {ba} bi xanh; hộp 2 có {rb} bi đỏ, {bb} bi xanh. Chọn ngẫu nhiên một hộp (xác suất bằng nhau) rồi rút 1 bi. Xác suất bi đỏ là', T, f'P = ½·{ra}/{ra+ba} + ½·{rb}/{rb+bb} = {f(T,4)}.', 1, TOP['tree'], SRC, extra=[(ra + rb) / (ra + ba + rb + bb), pa, pbb], d=4, origin='bo_sung')
        P(f'Hai hộp: hộp 1 có {ra} đỏ, {ba} xanh; hộp 2 có {rb} đỏ, {bb} xanh. Chọn hộp ngẫu nhiên rồi rút 1 bi, được bi đỏ. Xác suất bi lấy từ hộp 1 là', pst, f'P(hộp 1 | đỏ) = ½·{ra}/{ra+ba}/{f(T,4)} = {f(pst,4)}.', 2, TOP['bayes'], SRC, extra=[0.5, pa, pa * 0.5], d=4, origin='bo_sung')
    # 5. hai lần thử, ba đồng xu
    for pcoin in [(0.5, 0.7, 0.9), (0.4, 0.5, 0.6), (0.3, 0.6, 0.8)]:
        pr = [1 / 3] * 3; T = tot(pr, pcoin); i = 2
        P(f'Có 3 đồng xu với xác suất mặt ngửa lần lượt {pcoin[0]}, {pcoin[1]}, {pcoin[2]}. Chọn ngẫu nhiên một đồng xu và tung một lần. Xác suất ra ngửa là', T, f'P = (1/3)({pcoin[0]} + {pcoin[1]} + {pcoin[2]}) = {f(T,4)}.', 1, TOP['total'], SRC, extra=[pcoin[1], max(pcoin), 0.5], d=4, origin='bo_sung')
        P(f'Có 3 đồng xu với xác suất ngửa {pcoin[0]}, {pcoin[1]}, {pcoin[2]}. Chọn ngẫu nhiên một đồng xu, tung được ngửa. Xác suất đó là đồng xu thứ ba là', post(pr, list(pcoin), 2), f'P(đồng 3 | ngửa) = (1/3)·{pcoin[2]}/{f(T,4)} = {f(post(pr,list(pcoin),2),4)}.', 2, TOP['bayes'], SRC, extra=[1 / 3, pcoin[2], pcoin[2] / 3], d=4, origin='bo_sung')
    # 6. hai lần quan sát liên tiếp với đồng xu thiên vị
    for pb_, nflip in [(0.8, 2), (0.9, 3), (0.7, 2), (0.75, 3)]:
        prior = 0.5
        like_biased = pb_ ** nflip; like_fair = 0.5 ** nflip
        T = prior * like_biased + (1 - prior) * like_fair; ps = prior * like_biased / T
        P(f'Một hộp có 2 đồng xu: một cân đối, một thiên vị với xác suất ngửa {pb_}. Chọn ngẫu nhiên một đồng xu và tung {nflip} lần, được {nflip} lần ngửa. Xác suất đó là đồng xu thiên vị là', ps,
          f'Likelihood: {pb_}^{nflip} = {f(like_biased,4)} (thiên vị) và 0.5^{nflip} = {f(like_fair,4)} (cân đối). Bayes: ½·{f(like_biased,4)}/(½·{f(like_biased,4)} + ½·{f(like_fair,4)}) = {f(ps,4)}. Quan sát càng nhiều ngửa, hậu nghiệm càng tăng.', 3, TOP['bayes'], SRC, extra=[0.5, pb_, like_biased], d=4, origin='bo_sung')
        P(f'Hộp 2 đồng xu: một cân đối, một thiên vị (ngửa {pb_}); chọn ngẫu nhiên một đồng và tung {nflip} lần. Xác suất cả {nflip} lần đều ngửa là', T, f'P = ½·{pb_}^{nflip} + ½·0.5^{nflip} = {f(T,4)}.', 2, TOP['total'], SRC, extra=[like_biased, like_fair, pb_], d=4, origin='bo_sung')
    # 7. bộ lọc thư rác
    for spam, w_s, w_h in [(0.4, 0.8, 0.1), (0.2, 0.6, 0.05), (0.5, 0.9, 0.2), (0.3, 0.7, 0.1)]:
        pr = [spam, 1 - spam]; lk = [w_s, w_h]; T = tot(pr, lk)
        P(f'{spam*100:g}% thư đến là spam. Từ “khuyến mãi” xuất hiện trong {w_s*100:g}% thư spam và {w_h*100:g}% thư không phải spam. Nhận một thư có từ này, xác suất nó là spam là', post(pr, lk, 0), f'P(spam | từ) = {spam}·{w_s}/({spam}·{w_s} + {1-spam:g}·{w_h}) = {f(post(pr,lk,0),4)}.', 2, TOP['bayes'], SRC, extra=[w_s, spam, T], d=4, origin='bo_sung')
    # 8. tìm xác suất tiên nghiệm khi biết hậu nghiệm
    B.mcq('Hệ đầy đủ {A₁, A₂} có P(A₁) = 0.3, P(B | A₁) = 0.8, P(B | A₂) = 0.2. Tính P(B).', '0.38', ['0.50', '0.24', '0.56'], 'P(B) = 0.3·0.8 + 0.7·0.2 = 0.24 + 0.14 = 0.38.', 1, TOP['total'], SRC, 'bo_sung')
    B.mcq('Hệ đầy đủ {A₁, A₂} có P(A₁) = 0.3, P(B | A₁) = 0.8, P(B | A₂) = 0.2. Tính P(A₁ | B).', f(0.24 / 0.38, 4), [f(0.3, 4), f(0.8, 4), f(0.14 / 0.38, 4)], 'P(A₁ | B) = 0.24/0.38 = 0.6316 (và P(A₂ | B) = 0.14/0.38 = 0.3684, tổng bằng 1).', 2, TOP['bayes'], SRC, 'bo_sung')
    B.mcq('Nếu P(B | A₁) = P(B | A₂) = … = P(B | Aₙ) = c thì P(Aᵢ | B) bằng:', 'P(Aᵢ) (hậu nghiệm bằng tiên nghiệm)', ['1/n', 'c', '0'], 'P(B) = c·ΣP(Aᵢ) = c ⇒ P(Aᵢ | B) = cP(Aᵢ)/c = P(Aᵢ): thông tin B không giúp phân biệt các giả thuyết (như đề giữa kỳ mẫu câu 5 với tỉ lệ bệnh 0.07 ở cả hai giới).', 3, TOP['theory'], SRC, 'bo_sung')
    B.essay('Xét nghiệm bệnh hiếm: tỉ lệ mắc 1%, độ nhạy 95%, độ đặc hiệu 90%. Tính P(dương tính) và P(có bệnh | dương tính); nhận xét.', f'P(+) = 0.01·0.95 + 0.99·0.10 = 0.1085; P(bệnh | +) = 0.0095/0.1085 = {f(0.0095/0.1085,4)} ≈ 8.8%. Dù xét nghiệm “chính xác”, vì bệnh hiếm nên đa số dương tính là dương tính giả.', 3, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Ba phân xưởng 30%, 30%, 40% sản lượng, phế phẩm 2%, 3%, 4%. Tính P(phế phẩm) và hậu nghiệm cho từng phân xưởng khi gặp một phế phẩm.', f'P(B) = 0.006 + 0.009 + 0.016 = 0.031. Hậu nghiệm: 0.006/0.031 = {f(0.006/0.031,4)}; 0.009/0.031 = {f(0.009/0.031,4)}; 0.016/0.031 = {f(0.016/0.031,4)} (tổng 1).', 2, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Hai hộp bi (3 đỏ 7 xanh; 6 đỏ 4 xanh), chọn hộp ngẫu nhiên rồi rút 1 bi: tính P(đỏ) và P(hộp 1 | đỏ).', f'P(đỏ) = ½·0.3 + ½·0.6 = 0.45; P(hộp 1 | đỏ) = 0.15/0.45 = {f(1/3,4)}.', 2, TOP['tree'], SRC, 'bo_sung')
    B.essay('Đồng xu thiên vị (ngửa 0.8) hoặc cân đối chọn ngẫu nhiên; tung 3 lần được 3 ngửa. Tìm xác suất đó là đồng thiên vị và so sánh với tiên nghiệm.', f'Likelihood 0.512 và 0.125 ⇒ hậu nghiệm = 0.512/(0.512 + 0.125) = {f(0.512/0.637,4)} so với tiên nghiệm 0.5.', 3, TOP['bayes'], SRC, 'bo_sung')
    B.essay('Kênh nhị phân: phát 1 với xác suất 0.6, 0 với 0.4; bit 1 bị lỗi 0.1, bit 0 bị lỗi 0.2. Tính P(thu 1), P(phát 1 | thu 1), P(phát 0 | thu 0).', f'P(thu 1) = 0.6·0.9 + 0.4·0.2 = 0.62; P(phát 1 | thu 1) = 0.54/0.62 = {f(0.54/0.62,4)}; P(thu 0) = 0.38; P(phát 0 | thu 0) = 0.4·0.8/0.38 = {f(0.32/0.38,4)}.', 2, TOP['bayes'], SRC, 'bo_sung')
