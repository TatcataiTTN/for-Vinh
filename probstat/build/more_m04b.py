"""Module 4 — chuyên sâu đợt 2: dạng odds, cập nhật liên tiếp, nghịch lý, ứng dụng. Số tính bằng phân số chính xác."""
import itertools
from fractions import Fraction as Fr
from hx import *
K = 'MODULE 4 · '
def pc(x, d=2): return f'{float(x)*100:.{d}f}%'
def fl(x, d=4): return f'{float(x):.{d}f}'
def parts():
    P = []
    sens, spec, prev = Fr(95, 100), Fr(90, 100), Fr(1, 100)
    LR = sens / (1 - spec)
    # ───────── D. Dạng odds và cập nhật liên tiếp ─────────
    s = []
    po = prev / (1 - prev); post_o = po * LR; pp = post_o / (1 + post_o)
    assert pp == sens * prev / (sens * prev + (1 - spec) * (1 - prev))
    s.append(sl(callout('info', 'Dạng odds của Bayes', 'Odds = P/(1−P). Công thức Bayes viết gọn: <b>odds hậu nghiệm = odds tiên nghiệm × tỉ số hợp lý (LR)</b>.')
                + formula('Odds', '\\underbrace{\\tfrac{P(H|E)}{P(\\bar H|E)}}_{\\text{hậu nghiệm}}=\\underbrace{\\tfrac{P(H)}{P(\\bar H)}}_{\\text{tiên nghiệm}}\\times\\underbrace{\\tfrac{P(E|H)}{P(E|\\bar H)}}_{\\mathrm{LR}}')
                + steps(['Xét nghiệm có độ nhạy 95%, độ đặc hiệu 90%: LR dương = 0.95/0.10 = ' + fl(LR, 1) + '.', m(f'\\text{{Odds tiên nghiệm}}=\\tfrac{{0.01}}{{0.99}}={fl(po,5)}'), m(f'\\text{{Odds hậu nghiệm}}={fl(po,5)}\\times{fl(LR,1)}={fl(post_o,5)}'), m(f'P=\\tfrac{{\\text{{odds}}}}{{1+\\text{{odds}}}}={fl(pp,4)}')])
                + '<p>Trùng kết quả 0.0876 của công thức Bayes thông thường, nhưng chỉ cần một phép nhân.</p>', K + 'PHẦN 4 · Chuyên sâu', 'Bayes dạng odds và tỉ số hợp lý'))
    seq = [prev]
    for _ in range(3):
        o = seq[-1] / (1 - seq[-1]) * LR; seq.append(o / (1 + o))
    s.append(sl(callout('info', 'Ví dụ D1 · Dương tính liên tiếp', 'Cùng xét nghiệm (nhạy 95%, đặc hiệu 90%, tỉ lệ mắc 1%), làm lại độc lập nhiều lần và đều dương tính.')
                + table(['Số lần dương tính', 'Odds', 'Xác suất bệnh'], [[str(k), fl(x / (1 - x), 4), pc(x, 2)] for k, x in enumerate(seq)])
                + '<p>Mỗi lần dương tính nhân odds với 9.5. Sau lần hai xác suất gần 48%; sau lần ba đã gần 90%.</p>', K + 'PHẦN 4 · Chuyên sâu', 'Cập nhật niềm tin qua nhiều lần quan sát'))
    ppn = ((1 - spec) / 1) ; LRneg = (1 - sens) / spec
    o2 = prev / (1 - prev) * LR * LRneg; p2 = o2 / (1 + o2)
    s.append(sl(callout('info', 'Ví dụ D2 · Dương tính rồi âm tính', 'Lần một dương tính, lần hai (độc lập) âm tính. Xác suất bệnh?')
                + steps([m(f'\\mathrm{{LR}}_+={fl(LR,1)},\\ \\mathrm{{LR}}_-=\\tfrac{{1-0.95}}{{0.90}}={fl(LRneg,4)}'), m(f'\\text{{Odds}}={fl(prev/(1-prev),5)}\\times{fl(LR,1)}\\times{fl(LRneg,4)}={fl(o2,5)}'), m(f'P(\\text{{bệnh}})={fl(p2,4)}')])
                + '<p>Kết quả âm tính “kéo” xác suất xuống dưới mức tiên nghiệm 1% (còn ' + pc(p2, 2) + '): một lần âm tính (LR nhỏ hơn 1) đảo ngược tác động của lần dương tính.</p>', K + 'PHẦN 4 · Chuyên sâu', 'Bằng chứng ngược chiều'))
    pri4 = [Fr(40, 100), Fr(30, 100), Fr(20, 100), Fr(10, 100)]; lk4 = [Fr(1, 100), Fr(2, 100), Fr(4, 100), Fr(10, 100)]
    T4 = sum(p * l for p, l in zip(pri4, lk4)); po4 = [p * l / T4 for p, l in zip(pri4, lk4)]; assert sum(po4) == 1
    s.append(sl(callout('info', 'Ví dụ D3 · Bốn nhà máy', 'Bốn nhà máy cung cấp 40%, 30%, 20%, 10% linh kiện; tỉ lệ lỗi 1%, 2%, 4%, 10%. Linh kiện lấy ra bị lỗi: nhà máy nào đáng nghi nhất?')
                + table(['Nhà máy', 'Tiên nghiệm', 'Tỉ lệ lỗi', 'Tích', 'Hậu nghiệm'], [[str(i + 1), pc(p, 0), pc(l, 0), fl(p * l, 3), pc(q, 2)] for i, (p, l, q) in enumerate(zip(pri4, lk4, po4))] + [['Tổng', '100%', '', fl(T4, 3), '100%']])
                + '<p>Nhà máy 4 chỉ cung cấp 10% nhưng chịu trách nhiệm ' + pc(po4[3], 1) + ' số lỗi (0.010/0.028); thứ tự hậu nghiệm đảo ngược hoàn toàn so với tiên nghiệm (nhà máy 1 từ 40% xuống còn ' + pc(po4[0], 1) + ').</p>', K + 'PHẦN 4 · Chuyên sâu', 'Nhiều nguyên nhân: xếp hạng lại sau bằng chứng'))
    # bảng hai chiều
    N = {('A', '+'): 120, ('A', '-'): 80, ('B', '+'): 45, ('B', '-'): 255}
    nb = N[('A', '+')] + N[('B', '+')]
    s.append(sl(callout('info', 'Ví dụ D4 · Bayes từ bảng đếm', 'Khảo sát 500 người: nhóm A (200 người) và nhóm B (300 người). Số người trả lời “có”: A 120, B 45.')
                + table(['', 'Có', 'Không', 'Tổng'], [['Nhóm A', '120', '80', '200'], ['Nhóm B', '45', '255', '300'], ['Tổng', '165', '335', '500']])
                + steps([m('P(A)=0.4,\\ P(\\text{có}|A)=0.6,\\ P(\\text{có}|B)=0.15'), m('P(\\text{có})=0.4\\cdot0.6+0.6\\cdot0.15=0.33=\\tfrac{165}{500}'), m(f'P(A|\\text{{có}})=\\tfrac{{0.24}}{{0.33}}=\\tfrac{{120}}{{165}}={fl(Fr(120,165),4)}')])
                + '<p>Khi có bảng đếm, Bayes chỉ là “thu hẹp sang cột ‘có’ rồi lấy tỉ lệ”: 120/165.</p>', K + 'PHẦN 4 · Chuyên sâu', 'Bayes bằng cách thu hẹp không gian mẫu'))
    P.append(dict(title='Chuyên sâu: odds, cập nhật liên tiếp, nhiều nguyên nhân', bullets=['Bayes dạng odds', 'Dương tính liên tiếp', 'Bằng chứng ngược chiều', 'Bốn nhà máy', 'Bảng đếm'], slides=s))
    # ───────── E. Nghịch lý ─────────
    s = []
    cards = [('R', 'R'), ('R', 'B'), ('B', 'B')]; num = den = 0
    for c in cards:
        for side in (0, 1):
            if c[side] == 'R':
                den += 1
                if c[1 - side] == 'R': num += 1
    assert Fr(num, den) == Fr(2, 3)
    s.append(sl(callout('info', 'Ví dụ E1 · Ba tấm thẻ (hộp Bertrand)', 'Ba thẻ: (đỏ–đỏ), (đỏ–xanh), (xanh–xanh). Rút ngẫu nhiên một thẻ, nhìn một mặt thấy đỏ. Xác suất mặt kia cũng đỏ?')
                + steps(['Trực giác hay sai: “còn hai thẻ nên 1/2”.', 'Liệt kê 6 mặt, 3 mặt đỏ đều đồng khả năng; trong đó 2 mặt đỏ thuộc thẻ đỏ–đỏ.', m('P=\\tfrac{P(\\text{đỏ–đỏ})\\cdot1}{P(\\text{đỏ–đỏ})\\cdot1+P(\\text{đỏ–xanh})\\cdot\\tfrac12}=\\tfrac{1/3}{1/3+1/6}=\\tfrac23')])
                + f'<p>Đã kiểm chứng bằng liệt kê: {num}/{den} mặt đỏ thuộc thẻ đỏ–đỏ. Điểm mấu chốt: thẻ đỏ–đỏ có hai “cơ hội” cho mặt đỏ.</p>', K + 'PHẦN 5 · Nghịch lý và bẫy', 'Hộp Bertrand: trực giác sai'))
    pi = Fr(1, 3); mh = pi * 1 / (pi * 1 + pi * Fr(1, 2) + pi * 0)
    assert mh == Fr(2, 3)
    s.append(sl(callout('info', 'Ví dụ E2 · Monty Hall bằng công thức Bayes', 'Xe ở cửa 1, 2, 3 với xác suất 1/3. Bạn chọn cửa 1; người dẫn mở cửa 3 (dê). Xác suất xe ở cửa 2?')
                + steps([m('P(\\text{mở 3}|\\text{xe ở 1})=\\tfrac12,\\ P(\\text{mở 3}|\\text{xe ở 2})=1,\\ P(\\text{mở 3}|\\text{xe ở 3})=0'), m('P(\\text{mở 3})=\\tfrac13\\cdot\\tfrac12+\\tfrac13\\cdot1+0=\\tfrac12'), m('P(\\text{xe ở 2}|\\text{mở 3})=\\tfrac{1/3}{1/2}=\\tfrac23,\\quad P(\\text{xe ở 1}|\\text{mở 3})=\\tfrac13')])
                + '<p>Tổng hậu nghiệm 2/3 + 1/3 = 1. Đổi cửa thắng với xác suất 2/3 — mấu chốt là người dẫn <b>biết</b> chỗ xe nên khả năng “mở cửa 3” khác nhau theo từng giả thuyết.</p>', K + 'PHẦN 5 · Nghịch lý và bẫy', 'Monty Hall: lời giải Bayes'))
    pg = Fr(1, 100001); fm = Fr(1, 10000)
    ph = pg / (pg + (1 - pg) * fm)
    s.append(sl(callout('warn', 'Ví dụ E3 · Nhầm P(A|B) với P(B|A) trước toà', 'Dấu vết DNA khớp với nghi phạm. Xác suất khớp ngẫu nhiên với người vô tội là 1/10 000. Trong thành phố 100 001 người có 1 thủ phạm. Có kết luận “nghi phạm vô tội chỉ 1/10 000”?')
                + steps([m('P(\\text{khớp}|\\text{vô tội})=10^{-4}\\ \\text{không phải}\\ P(\\text{vô tội}|\\text{khớp})'), m(f'\\text{{Khoảng }}100000\\times10^{{-4}}=10\\text{{ người vô tội cũng khớp, cộng 1 thủ phạm}}'), m(f'P(\\text{{thủ phạm}}|\\text{{khớp}})=\\tfrac{{1}}{{1+10}}\\approx{fl(ph,4)}')])
                + '<p>Nếu chỉ có bằng chứng này (không có điều tra bổ sung), xác suất nghi phạm có tội chỉ khoảng 9%, không phải 99.99%. Đây là “ngụy biện của công tố viên”.</p>', K + 'PHẦN 5 · Nghịch lý và bẫy', 'Ngụy biện của công tố viên'))
    pbl = Fr(15, 100); acc = Fr(80, 100)
    pt = pbl * acc / (pbl * acc + (1 - pbl) * (1 - acc))
    s.append(sl(callout('info', 'Ví dụ E4 · Bài taxi (bỏ qua tỉ lệ nền)', 'Thành phố có 85% taxi xanh, 15% taxi xanh dương. Nhân chứng nhận đúng màu 80%. Nhân chứng nói taxi gây tai nạn màu xanh dương. Xác suất đúng là taxi xanh dương?')
                + steps([m('P(\\text{nói XD})=0.15\\cdot0.8+0.85\\cdot0.2=0.29'), m(f'P(\\text{{XD}}|\\text{{nói XD}})=\\tfrac{{0.12}}{{0.29}}={fl(pt,4)}')])
                + '<p>Nhiều người trả lời 80%. Bỏ qua tỉ lệ nền (15%) là lỗi phổ biến nhất khi dùng Bayes.</p>', K + 'PHẦN 5 · Nghịch lý và bẫy', 'Bỏ qua tỉ lệ nền'))
    A = (81, 87, 192, 263); B_ = (234, 270, 55, 80)
    ra = Fr(A[0] + A[2], A[1] + A[3]); rb = Fr(B_[0] + B_[2], B_[1] + B_[3])
    assert Fr(A[0], A[1]) > Fr(B_[0], B_[1]) and Fr(A[2], A[3]) > Fr(B_[2], B_[3]) and ra < rb
    s.append(sl(callout('warn', 'Ví dụ E5 · Nghịch lý Simpson (số liệu kinh điển)', 'So sánh hai phương pháp điều trị sỏi thận, tỉ lệ thành công (dữ liệu của Charig và cộng sự, 1986).')
                + table(['', 'Sỏi nhỏ', 'Sỏi lớn', 'Chung'], [['Phương pháp A', '81/87 = ' + pc(Fr(81, 87), 0), '192/263 = ' + pc(Fr(192, 263), 0), '273/350 = ' + pc(ra, 0)], ['Phương pháp B', '234/270 = ' + pc(Fr(234, 270), 0), '55/80 = ' + pc(Fr(55, 80), 0), '289/350 = ' + pc(rb, 0)]])
                + '<p>A tốt hơn ở <b>cả hai</b> nhóm nhưng B tốt hơn khi gộp, vì A được dùng nhiều cho ca khó (sỏi lớn). Biến ẩn (kích thước sỏi) làm đảo chiều; xác suất toàn phần với trọng số khác nhau giải thích hiện tượng.</p>', K + 'PHẦN 5 · Nghịch lý và bẫy', 'Nghịch lý Simpson'))
    P.append(dict(title='Nghịch lý và bẫy kinh điển của Bayes', bullets=['Hộp Bertrand', 'Monty Hall', 'Ngụy biện của công tố viên', 'Bỏ qua tỉ lệ nền', 'Nghịch lý Simpson'], slides=s))
    # ───────── F. Ứng dụng ─────────
    s = []
    ps, w1s, w1h, w2s, w2h = Fr(40, 100), Fr(50, 100), Fr(2, 100), Fr(40, 100), Fr(5, 100)
    a1 = ps * w1s / (ps * w1s + (1 - ps) * w1h)
    n2 = ps * w1s * w2s; d2 = n2 + (1 - ps) * w1h * w2h; a2 = n2 / d2
    s.append(sl(callout('info', 'Ví dụ F1 · Lọc thư rác (số liệu minh họa, giả định)', 'Giả sử 40% thư là rác. Từ “trúng thưởng” xuất hiện trong 50% thư rác và 2% thư thường; từ “miễn phí” xuất hiện trong 40% thư rác và 5% thư thường (coi hai từ độc lập có điều kiện).')
                + steps([m(f'P(\\text{{rác}}|\\text{{trúng thưởng}})=\\tfrac{{0.4\\cdot0.5}}{{0.4\\cdot0.5+0.6\\cdot0.02}}={fl(a1,4)}'), m(f'P(\\text{{rác}}|\\text{{cả hai từ}})=\\tfrac{{0.4\\cdot0.5\\cdot0.4}}{{0.4\\cdot0.5\\cdot0.4+0.6\\cdot0.02\\cdot0.05}}={fl(a2,4)}')])
                + '<p>Đây là ý tưởng của bộ lọc Bayes “ngây thơ”: nhân các tỉ số hợp lý của từng từ. Giả thiết độc lập có điều kiện thường chỉ gần đúng.</p>', K + 'PHẦN 6 · Ứng dụng', 'Bộ lọc thư rác'))
    pk = Fr(6, 10); gk = pk / (pk + (1 - pk) * Fr(1, 4))
    s.append(sl(callout('info', 'Ví dụ F2 · Thi trắc nghiệm đoán mò', 'Một sinh viên biết bài với xác suất 0.6; nếu không biết thì đoán ngẫu nhiên giữa 4 đáp án. Anh ta trả lời đúng. Xác suất anh ta thật sự biết bài?')
                + steps([m('P(\\text{đúng})=0.6\\cdot1+0.4\\cdot0.25=0.7'), m(f'P(\\text{{biết}}|\\text{{đúng}})=\\tfrac{{0.6}}{{0.7}}={fl(gk,4)}')])
                + '<p>Nếu đề có 2 đáp án, xác suất giảm còn 0.6/(0.6+0.2) = 0.75; số phương án càng ít, đoán mò càng khó loại trừ.</p>', K + 'PHẦN 6 · Ứng dụng', 'Biết thật hay đoán đúng'))
    cp = [Fr(5, 10), Fr(3, 10), Fr(2, 10)]; cf = [Fr(2, 100), Fr(5, 100), Fr(10, 100)]
    TT = sum(a * b for a, b in zip(cp, cf)); pq = [a * b / TT for a, b in zip(cp, cf)]
    s.append(sl(callout('info', 'Ví dụ F3 · Thiết bị hỏng, linh kiện nào?', 'Một thiết bị gồm linh kiện 1, 2, 3 chiếm 50%, 30%, 20% số lần hỏng giả định; xác suất “hỏng nặng” khi hỏng là 2%, 5%, 10%. Quan sát hỏng nặng: nguyên nhân?')
                + table(['Linh kiện', 'P(Aᵢ)', 'P(nặng|Aᵢ)', 'Hậu nghiệm'], [[str(i + 1), pc(a, 0), pc(b, 0), pc(q, 2)] for i, (a, b, q) in enumerate(zip(cp, cf, pq))])
                + '<p>P(nặng) = ' + pc(TT, 1) + '. Linh kiện 3 vừa ít gặp vừa dễ hỏng nặng, hậu nghiệm đạt ' + pc(pq[2], 1) + '.</p>', K + 'PHẦN 6 · Ứng dụng', 'Chẩn đoán nguyên nhân hỏng hóc'))
    s.append(sl(table(['Tình huống', 'Dùng gì', 'Dấu hiệu trong đề'], [['Xác suất kết quả chung', 'Toàn phần', '“chọn ngẫu nhiên một …, xác suất …”'], ['Nguyên nhân khi biết kết quả', 'Bayes', '“biết rằng …, xác suất do …”'], ['Nhiều bằng chứng độc lập', 'Nhân LR / cập nhật liên tiếp', '“làm lại”, “lần hai cũng …”'], ['Tỉ lệ nền nhỏ', 'Bayes + cẩn trọng', '“bệnh hiếm”, “tỉ lệ rất nhỏ”'], ['Có bảng đếm', 'Thu hẹp không gian mẫu', 'cho số lượng trong từng ô']])
                + callout('warn', 'Ba lỗi hay mất điểm', '1) Quên chuẩn hóa mẫu số (P(B)). 2) Dùng tiên nghiệm không đủ 100%. 3) Nhầm P(A|B) với P(B|A).'), K + 'PHẦN 6 · Ứng dụng', 'Bảng chọn công thức'))
    P.append(dict(title='Ứng dụng Bayes và bảng chọn công thức', bullets=['Thư rác', 'Biết thật hay đoán đúng', 'Chẩn đoán hỏng hóc', 'Bảng chọn công thức'], slides=s))
    return P
