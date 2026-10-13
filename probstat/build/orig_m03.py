"""Module 3 — Xác suất cổ điển, quy tắc cộng/bù, có điều kiện, nhân, độc lập.
Gốc: Lecture Notes §1.4–1.5 (Ví dụ 1.14–1.19, Bài 1.11–1.18), Kreyszig PS 24.3 (Prob. 1–19), đề giữa kỳ mẫu câu 3–4."""
import math, itertools, random
from fractions import Fraction as Fr
from math import comb
from qb import f, fg, nd, ni
from qh import pm, frac
TOP = {'def': 'Định nghĩa và tiên đề xác suất', 'add': 'Quy tắc cộng và bù', 'classic': 'Xác suất cổ điển (đếm)', 'cond': 'Xác suất có điều kiện và công thức nhân',
       'indep': 'Sự kiện độc lập', 'seq': 'Rút có/không hoàn lại', 'rel': 'Độ tin cậy hệ thống (nối tiếp/song song)', 'theory': 'Lý thuyết'}
def build(B):
    rng = random.Random(303); P = pm
    d2 = list(itertools.product(range(1, 7), repeat=2)); d3 = list(itertools.product(range(1, 7), repeat=3))
    # ---------- Lecture Notes ví dụ ----------
    S = 'Lecture Notes '
    B.mcq('Gieo con súc sắc cân đối. P(A) với A = {1, 3, 5} (số lẻ) là', '1/2', ['1/3', '1/6', '2/3'], 'P(A) = card(A)/card(S) = 3/6 = 1/2 (Ví dụ 1.14i).', 1, TOP['classic'], S + 'Ví dụ 1.14(i)')
    B.mcq('Gieo con súc sắc cân đối. P(B) với B = {5, 6} là', '1/3', ['1/2', '1/6', '2/3'], 'P(B) = 2/6 = 1/3 (Ví dụ 1.14ii).', 1, TOP['classic'], S + 'Ví dụ 1.14(ii)')
    B.mcq('Tung 5 đồng xu cân đối cùng lúc. Xác suất “ít nhất một mặt sấp” là', '31/32', ['1/32', '1/2', '5/32'], 'Biến cố bù: không có mặt sấp nào, đúng 1 kết cục trong 2⁵ = 32 ⇒ P = 1 − 1/32 = 31/32 (Ví dụ 1.15).', 1, TOP['add'], S + 'Ví dụ 1.15')
    P(B, rng, 'Một gara nhận số xe sửa chữa mỗi ngày: 10–20 xe (xác suất 0.20), 21–30 xe (0.35), 31–40 xe (0.25), trên 40 xe (0.12). Xác suất gara nhận trên 21 xe trong một ngày là', 0.72,
      'Các biến cố xung khắc nên cộng: 0.35 + 0.25 + 0.12 = 0.72 (Ví dụ 1.16). Lưu ý tổng các xác suất đã cho là 0.92; phần 0.08 còn lại ứng với dưới 10 xe.', 1, TOP['add'], S + 'Ví dụ 1.16', extra=[0.20 + 0.35 + 0.25 + 0.12, 0.92, 0.12, 0.60], d=2)
    B.mcq('Gieo súc sắc: A = “số lẻ”, B = “số nhỏ hơn 4”. P(A ∪ B) là', '2/3', ['1/2', '5/6', '1/3'], 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = 3/6 + 3/6 − 2/6 = 4/6 = 2/3 (A ∩ B = {1, 3}).', 2, TOP['add'], S + 'Ví dụ 1.17')
    B.mcq('Lớp 30 bạn (17 nữ, 13 nam); 3 bạn tên Thanh (1 nữ, 2 nam). Gọi ngẫu nhiên 1 bạn. Xác suất bạn đó tên Thanh là', '1/10', ['1/17', '1/3', '3/17'], 'P(A) = 3/30 = 1/10 (Ví dụ 1.18i).', 1, TOP['classic'], S + 'Ví dụ 1.18(i)')
    B.mcq('Cùng lớp đó: xác suất bạn được gọi tên Thanh, BIẾT bạn đó là nữ, là', '1/17', ['1/10', '1/3', '1/30'], 'P(A|B) = P(A ∩ B)/P(B) = (1/30)/(17/30) = 1/17 (Ví dụ 1.18ii).', 2, TOP['cond'], S + 'Ví dụ 1.18(ii)')
    B.mcq('Cùng lớp đó: xác suất bạn được gọi là nữ, BIẾT bạn tên Thanh, là', '1/3', ['1/17', '1/30', '17/30'], 'P(B|A) = P(A ∩ B)/P(A) = (1/30)/(3/30) = 1/3 (Ví dụ 1.18iii). Chú ý P(A|B) ≠ P(B|A).', 2, TOP['cond'], S + 'Ví dụ 1.18(iii)')
    P(B, rng, 'Hộp 10 đinh ốc có 3 cái lỗi. Lấy lần lượt 2 cái, CÓ hoàn lại. Xác suất cả hai không lỗi là', 0.49, 'P(A ∩ B) = (7/10)(7/10) = 0.49 vì hai lần rút độc lập (Ví dụ 1.19i).', 1, TOP['seq'], S + 'Ví dụ 1.19(i)', extra=[0.4667, 0.7, 0.51], d=4)
    P(B, rng, 'Hộp 10 đinh ốc có 3 cái lỗi. Lấy lần lượt 2 cái, KHÔNG hoàn lại. Xác suất cả hai không lỗi là', 7 / 10 * 6 / 9, 'P(A ∩ B) = P(A)·P(B|A) = (7/10)(6/9) = 0.4667 (Ví dụ 1.19ii; giáo trình làm tròn ≈ 0.47).', 2, TOP['seq'], S + 'Ví dụ 1.19(ii)', extra=[0.49, 0.7, 6 / 9])
    # ---------- Bài 1.11–1.18 ----------
    S = 'Lecture Notes '
    p = 1 - comb(90, 3) / comb(100, 3); assert abs(p - (1 - 90 * 89 * 88 / (100 * 99 * 98))) < 1e-12
    P(B, rng, 'Hộp 100 ốc vít có 10 con lỗi. Rút ngẫu nhiên không hoàn lại lần lượt 3 con. Xác suất có ít nhất một con lỗi là (Bài 1.11)', p, f'Bù: không con nào lỗi = (90/100)(89/99)(88/98) = {f(1-p,5)} ⇒ P = {f(p,5)}.', 2, TOP['seq'], S + 'Bài 1.11', extra=[1 - 0.9 ** 3, 0.3, 0.1 * 3, 1 - 0.1 ** 3])
    B.mcq('Gieo đồng thời 4 đồng xu cân đối. Xác suất cả bốn mặt giống nhau (Bài 1.12a) là', '1/8', ['1/16', '1/4', '1/2'], 'Hai khả năng (SSSS, NNNN) trong 16: 2/16 = 1/8.', 1, TOP['classic'], S + 'Bài 1.12(a)')
    B.mcq('Gieo đồng thời 4 đồng xu cân đối. Xác suất có đúng 2 mặt sấp (Bài 1.12b) là', '3/8', ['1/4', '1/2', '1/6'], 'C(4,2)/2⁴ = 6/16 = 3/8.', 1, TOP['classic'], S + 'Bài 1.12(b)')
    B.mcq('Gieo đồng thời 4 đồng xu cân đối. Xác suất có ít nhất hai mặt ngửa (Bài 1.12c) là', '11/16', ['5/16', '1/2', '3/4'], 'Bù: 0 hoặc 1 mặt ngửa: (1 + 4)/16 = 5/16 ⇒ P = 11/16.', 2, TOP['add'], S + 'Bài 1.12(c)')
    c13a = sum(1 for t in d2 if 4 < sum(t) <= 7); c13b = sum(1 for t in d2 if t[0] == t[1] or sum(t) % 2 == 0)
    B.mcq('Gieo 2 súc sắc cân đối. Xác suất để tổng số chấm lớn hơn 4 và nhỏ hơn hoặc bằng 7 (Bài 1.13a) là', '5/12', ['1/3', '1/2', '7/18'], f'Tổng 5, 6, 7 có 4 + 5 + 6 = {c13a} kết cục ⇒ {c13a}/36 = 5/12.', 2, TOP['classic'], S + 'Bài 1.13(a)')
    B.mcq('Gieo 2 súc sắc. Xác suất để số chấm bằng nhau HOẶC tổng là số chẵn (Bài 1.13b) là', '1/2', ['2/3', '1/3', '7/12'], f'Hai mặt bằng nhau thì tổng chẵn nên “bằng nhau” ⊂ “tổng chẵn”; hợp chính là “tổng chẵn”: {c13b}/36 = 1/2.', 2, TOP['add'], S + 'Bài 1.13(b)')
    B.mcq('Lớp 30 HS: 4 giỏi, 8 khá, 10 trung bình, 8 yếu. Chọn 3 người. Xác suất cả ba đều yếu (Bài 1.14a) là', f(comb(8, 3) / comb(30, 3), 4), [f(comb(8, 3) / comb(30, 3) * 2, 4), f((8 / 30) ** 3, 4), f(8 / 30, 4)], f'C(8,3)/C(30,3) = 56/4060 = {f(comb(8,3)/comb(30,3),4)}.', 2, TOP['classic'], S + 'Bài 1.14(a)')
    B.mcq('Lớp 30 HS (4 giỏi, 26 còn lại). Chọn 3 người. Xác suất có ít nhất một học sinh giỏi (Bài 1.14b) là', f(1 - comb(26, 3) / comb(30, 3), 4), [f(comb(26, 3) / comb(30, 3), 4), f(4 / 30 * 3, 4), f(1 - (26 / 30) ** 3, 4)], f'Bù: không có HS giỏi: C(26,3)/C(30,3) = {f(comb(26,3)/comb(30,3),4)} ⇒ P = {f(1-comb(26,3)/comb(30,3),4)}.', 2, TOP['add'], S + 'Bài 1.14(b)')
    B.mcq('Lớp 30 HS (4 giỏi, 26 còn lại). Chọn 3 người. Xác suất có đúng một học sinh giỏi (Bài 1.14c) là', f(4 * comb(26, 2) / comb(30, 3), 4), [f(1 - comb(26, 3) / comb(30, 3), 4), f(4 / 30, 4), f(comb(26, 2) / comb(30, 3), 4)], f'C(4,1)·C(26,2)/C(30,3) = 4·325/4060 = {f(4*comb(26,2)/comb(30,3),4)}.', 3, TOP['classic'], S + 'Bài 1.14(c)')
    P5 = Fr(sum(1 for t in d2 if sum(t) == 6), sum(1 for t in d2 if sum(t) % 2 == 0))
    B.mcq('Gieo hai súc sắc giống nhau. Biết tổng số chấm là số chẵn, xác suất để tổng đó bằng 6 (Bài 1.15) là', '5/18', ['5/36', '1/6', '1/3'], f'P(tổng=6 | tổng chẵn) = (5/36)/(18/36) = {P5}. Không gian mẫu thu hẹp còn 18 kết cục.', 2, TOP['cond'], S + 'Bài 1.15')
    q = 1 - 0.95 ** (1 / 3)
    P(B, rng, 'Mạch có 3 thiết bị đóng ngắt giống nhau mắc nối tiếp, xác suất mạch làm việc trong khoảng T là 95%. Xác suất lỗi của mỗi thiết bị là (Bài 1.16)', q, f'Mạch chạy ⇔ cả ba chạy: (1 − q)³ = 0.95 ⇒ q = 1 − 0.95^(1/3) = {f(q,5)}. (Không phải 0.05/3 = {f(0.05/3,5)}.)', 3, TOP['rel'], S + 'Bài 1.16', extra=[0.05 / 3, 0.05, 0.95 ** 3, 1 - 0.95 / 3], d=5)
    P(B, rng, 'Thiết bị có 4 van giống nhau, chỉ hỏng khi cả 4 van hỏng; mỗi van hỏng với xác suất 3%. Xác suất thiết bị làm việc là (Bài 1.17)', 1 - 0.03 ** 4, 'Làm việc ⇔ không phải cả 4 van hỏng: 1 − 0.03⁴ = 1 − 8.1·10⁻⁷ = 0.99999919.', 2, TOP['rel'], S + 'Bài 1.17', extra=[0.97 ** 4, 1 - 0.03, 0.03 ** 4], d=7)
    B.mcq('Hộp 100 đinh ốc có 10 cái lỗi; lấy lần lượt 3 cái, CÓ hoàn lại. Xác suất cả 3 đều lỗi (Bài 1.18a) là', '0.001', ['0.0007', '0.01', '0.3'], '(10/100)³ = 0.001.', 1, TOP['seq'], S + 'Bài 1.18(a)')
    B.mcq('Hộp 100 đinh ốc có 10 cái lỗi; lấy lần lượt 3 cái, KHÔNG hoàn lại. Xác suất cả 3 đều lỗi (Bài 1.18b) là', f(10 * 9 * 8 / (100 * 99 * 98), 6), [f(0.001, 6), f(10 / 100 * 9 / 99 * 8 / 98 * 2, 6), f(3 * 10 / 100, 6)], f'(10/100)(9/99)(8/98) = {f(10*9*8/(100*99*98),6)} ≈ 0.00074 < 0.001: khi không hoàn lại xác suất nhỏ hơn.', 2, TOP['seq'], S + 'Bài 1.18(b)')
    # ---------- Kreyszig PS 24.3 ----------
    K = 'Kreyszig PS 24.3, Prob. '
    c1 = sum(1 for t in d3 if sum(t) <= 16)
    B.mcq('Gieo 3 súc sắc cân đối. Xác suất tổng không vượt quá 16 (Prob. 1) là', f(c1 / 216, 4), [f(1 - 4 / 216 * 2, 4), f(16 / 18, 4), f(1 / 216, 4)], f'Bù: tổng 17 (3 cách) hoặc 18 (1 cách) ⇒ {216-c1}/216 ⇒ P = {c1}/216 = {f(c1/216,4)}.', 2, TOP['add'], K + '1')
    c2 = sum(1 for t in d2 if 3 < sum(t) <= 6)
    B.mcq('Gieo 2 súc sắc cân đối. Xác suất tổng lớn hơn 3 nhưng không vượt quá 6 (Prob. 2) là', '1/3', ['1/4', '5/12', '5/36'], f'Tổng 4, 5, 6: 3 + 4 + 5 = {c2} kết cục ⇒ 12/36 = 1/3.', 2, TOP['classic'], K + '2')
    P(B, rng, 'Rút 3 ốc vít từ lô 100 ốc có 10 ốc lỗi, CÓ hoàn lại. Xác suất cả 3 đều không lỗi (Prob. 3a) là', 0.9 ** 3, '(90/100)³ = 0.729.', 1, TOP['seq'], K + '3(a)', extra=[0.7265, 0.9, 0.27])
    P(B, rng, 'Rút 3 ốc vít từ lô 100 ốc có 10 ốc lỗi, KHÔNG hoàn lại. Xác suất cả 3 đều không lỗi (Prob. 3b) là', comb(90, 3) / comb(100, 3), f'C(90,3)/C(100,3) = (90·89·88)/(100·99·98) = {f(comb(90,3)/comb(100,3),4)}.', 2, TOP['seq'], K + '3(b)', extra=[0.729, 0.9, 0.7])
    P(B, rng, 'Bài trên (Prob. 3): xác suất E = “ít nhất 1 ốc lỗi” khi rút CÓ hoàn lại (dùng biến cố bù) là', 1 - 0.9 ** 3, 'P(E) = 1 − P(không lỗi) = 1 − 0.729 = 0.271 (Prob. 4a). Trực tiếp: 3·0.1·0.9² + 3·0.1²·0.9 + 0.1³ = 0.243 + 0.027 + 0.001 = 0.271.', 2, TOP['add'], K + '4(a)', extra=[0.729, 0.3, 0.2735])
    P(B, rng, 'Bài trên (Prob. 3): xác suất E = “ít nhất 1 ốc lỗi” khi rút KHÔNG hoàn lại là', 1 - comb(90, 3) / comb(100, 3), f'P(E) = 1 − {f(comb(90,3)/comb(100,3),4)} = {f(1-comb(90,3)/comb(100,3),4)} (Prob. 4b).', 2, TOP['add'], K + '4(b)', extra=[0.271, 0.7265, 0.3])
    P(B, rng, 'Hộp có 10 ốc xoắn trái và 20 ốc xoắn phải. Rút 2 ốc CÓ hoàn lại. Xác suất có ít nhất một ốc xoắn phải (Prob. 5) là', 1 - (1 / 3) ** 2, 'Bù: cả 2 đều trái: (10/30)² = 1/9 ⇒ P = 8/9 ≈ 0.8889.', 2, TOP['add'], K + '5', extra=[2 / 3, 1 / 9, 0.8966])
    p6 = 1 - (10 / 30) * (9 / 29)
    P(B, rng, 'Cùng hộp đó (10 trái, 20 phải), rút 2 ốc KHÔNG hoàn lại. Xác suất có ít nhất một ốc xoắn phải (Prob. 6) là', p6, f'Bù: cả 2 trái: (10/30)(9/29) = {f(10*9/(30*29),5)} ⇒ P = {f(p6,4)} > 0.8889: rút không hoàn lại làm xác suất TĂNG.', 2, TOP['seq'], K + '6', extra=[8 / 9, 1 / 9, 0.1035])
    B.mcq('Khi nào việc rút có hoàn lại và không hoàn lại cho kết quả gần như nhau (Prob. 7)?', 'Khi cỡ lô rất lớn so với cỡ mẫu', ['Khi cỡ mẫu lớn hơn cỡ lô', 'Khi tỉ lệ lỗi bằng 50%', 'Không bao giờ'], 'Khi N ≫ n, việc lấy ra vài phần tử hầu như không đổi thành phần của lô, nên các lần rút gần độc lập.', 2, TOP['seq'], K + '7')
    P(B, rng, 'Lốp xe có tuổi thọ vượt 40 000 dặm với xác suất 0.90. Xác suất một bộ 4 lốp trên xe đều vượt 40 000 dặm (Prob. 8, các lốp độc lập) là', 0.9 ** 4, '(0.9)⁴ = 0.6561.', 1, TOP['indep'], K + '8', extra=[0.9, 0.81, 0.729, 0.9 * 4])
    p9 = comb(498, 5) / comb(500, 5)
    P(B, rng, 'Kiểm tra giấy: rút 5 tờ không hoàn lại từ mỗi ram 500 tờ, biết 0.4% tờ bị vết (2 tờ/ram). Xác suất cả 5 tờ sạch (Prob. 9) là', p9, f'C(498,5)/C(500,5) = (495·494)/(500·499) = {f(p9,5)} (xấp xỉ 0.996⁵ = {f(0.996**5,5)} nếu có hoàn lại).', 3, TOP['seq'], K + '9', extra=[0.996 ** 5, 0.996, 0.98])
    p10 = 1 - (1 + 4) / 16
    P(B, rng, 'Rút liên tiếp có hoàn lại từ 100 phiếu (50 nam, 50 nữ). Xác suất rút được phiếu “nữ” lần thứ 2 TRƯỚC phiếu “nam” lần thứ 3 (Prob. 10) là', p10, 'Điều đó xảy ra ⇔ trong 4 lần rút đầu có ít nhất 2 nữ. Bù: 0 hoặc 1 nữ: (1 + 4)/2⁴ = 5/16 ⇒ P = 11/16 = 0.6875.', 3, TOP['seq'], K + '10', extra=[0.5, 0.3125, 0.75, 0.6875 + 0.0625])
    r_d = 100 / 200 * 99 / 199; r_1 = 2 * 100 / 200 * 100 / 199
    P(B, rng, 'Lô 200 thanh sắt: 50 quá khổ, 50 thiếu khổ, 100 đạt. Rút 2 thanh không hoàn lại. Xác suất cả hai đạt (Prob. 11a) là', r_d, f'(100/200)(99/199) = {f(r_d,5)}.', 2, TOP['seq'], K + '11(a)', extra=[0.25, r_1, 0.5])
    P(B, rng, 'Lô 200 thanh sắt (100 đạt, 100 không đạt). Rút 2 thanh không hoàn lại. Xác suất có đúng một thanh đạt (Prob. 11b) là', r_1, f'Hai thứ tự: 2·(100/200)(100/199) = {f(r_1,5)}.', 3, TOP['seq'], K + '11(b)', extra=[r_d, 0.5, 0.25])
    P(B, rng, 'Lô 200 thanh sắt (100 đạt, 100 không đạt). Rút 2 thanh không hoàn lại. Xác suất không thanh nào đạt (Prob. 11c) là', r_d, f'(100/200)(99/199) = {f(r_d,5)}. Kiểm tra: {f(r_d,5)} + {f(r_1,5)} + {f(r_d,5)} = 1.', 2, TOP['seq'], K + '11(c)', extra=[0.25, r_1, 0.5])
    q12 = 1 - 0.99 ** 0.25
    P(B, rng, 'Mạch có 4 công tắc tự động; muốn xác suất tất cả cùng hoạt động trong khoảng thời gian cho trước là 99%. Xác suất hỏng tối đa cho phép của mỗi công tắc (Prob. 12) là', q12, f'(1 − q)⁴ = 0.99 ⇒ q = 1 − 0.99^(1/4) = {f(q12,6)} (≈ 0.01/4 = 0.0025 chỉ là xấp xỉ).', 3, TOP['rel'], K + '12', extra=[0.0025, 0.01, 0.99 ** 4], d=6)
    P(B, rng, 'Thiết bị áp suất có 3 ống điện tử, hỏng nếu một ống hỏng; mỗi ống hỏng với xác suất 0.04. Xác suất thiết bị hỏng (Prob. 13) là', 1 - 0.96 ** 3, '1 − 0.96³ = 1 − 0.884736 = 0.115264.', 2, TOP['rel'], K + '13', extra=[0.04 * 3, 0.04 ** 3, 0.96 ** 3], d=6)
    for lab, val, ex in (('a', 0.98 ** 2, 'Không có sản phẩm lỗi: 0.98² = 0.9604.'), ('b', 2 * 0.02 * 0.98, 'Đúng một lỗi: 2·0.02·0.98 = 0.0392.'), ('c', 0.02 ** 2, 'Cả hai lỗi: 0.02² = 0.0004.')):
        txt = {'a': 'không có', 'b': 'đúng một', 'c': 'hai'}[lab]
        P(B, rng, f'Tỉ lệ bugi lỗi ổn định 2%; mỗi nửa giờ kiểm tra 2 bugi vừa sản xuất. Xác suất có {txt} bugi lỗi (Prob. 14{lab}) là', val, ex + ' (0.9604 + 0.0392 + 0.0004 = 1.)', 2 if lab != 'c' else 1, TOP['indep'], K + f'14({lab})', extra=[0.02, 0.98, 0.04], d=4)
    B.mcq('Cách nào cho xác suất “trúng ít nhất một lần” lớn nhất (Prob. 15): (a) trúng 1/2, bắn 1 phát; (b) trúng 1/4, bắn 2 phát; (c) trúng 1/8, bắn 4 phát?', '(a): 0.5', ['(b): 0.4375', '(c): 0.4136', 'Cả ba bằng nhau'],
          '(a) 1/2 = 0.5; (b) 1 − (3/4)² = 0.4375; (c) 1 − (7/8)⁴ = 0.4138. Lớn nhất là (a); trực giác “tổng 1/2 như nhau” sai vì các phát không loại trừ nhau.', 2, TOP['indep'], K + '15')
    chips = ['000', '011', '101', '110']
    A_ = {c for c in chips if c[0] == '1'}; B_ = {c for c in chips if c[1] == '1'}; C_ = {c for c in chips if c[2] == '1'}
    pr = lambda E: Fr(len(E), 4)
    assert pr(A_ & B_) == pr(A_) * pr(B_) and pr(A_ & B_ & C_) == 0 != pr(A_) * pr(B_) * pr(C_)
    B.mcq('Rút một chip từ 4 chip 000, 011, 101, 110; A, B, C là biến cố chữ số thứ nhất, hai, ba là 1. Khẳng định đúng (Prob. 16) là:', 'A, B, C độc lập từng đôi nhưng KHÔNG độc lập toàn phần',
          ['A, B, C độc lập toàn phần', 'A và B không độc lập', 'P(A ∩ B ∩ C) = 1/8'], 'P(A) = P(B) = P(C) = 1/2; P(A ∩ B) = 1/4 = P(A)P(B) (chip 110), tương tự các cặp khác. Nhưng A ∩ B ∩ C = ∅ ⇒ P = 0 ≠ 1/8 = P(A)P(B)P(C).', 3, TOP['indep'], K + '16')
    B.mcq('Nếu B ⊂ A thì khẳng định nào đúng (Prob. 17)?', 'P(B) ≤ P(A)', ['P(B) ≥ P(A)', 'P(B) = P(A)', 'P(B) + P(A) = 1'], 'A = B ∪ (A \\ B) với hai phần xung khắc ⇒ P(A) = P(B) + P(A \\ B) ≥ P(B).', 1, TOP['theory'], K + '17')
    B.mcq('Công thức nhân mở rộng cho ba biến cố (Prob. 18) là:', 'P(A ∩ B ∩ C) = P(A)·P(B | A)·P(C | A ∩ B)', ['P(A ∩ B ∩ C) = P(A) + P(B) + P(C)', 'P(A ∩ B ∩ C) = P(A)·P(B)·P(C) luôn đúng', 'P(A ∩ B ∩ C) = P(C | A)·P(B | C)'], 'Áp dụng công thức nhân hai lần: P((A ∩ B) ∩ C) = P(A ∩ B)·P(C | A ∩ B).', 2, TOP['cond'], K + '18')
    # ---------- Đề giữa kỳ mẫu ----------
    B.mcq('Biết P(A) = 0.57. Xác suất của biến cố đối Ā là', '0.43', ['0.57', '0.057', '1.57'], 'P(Ā) = 1 − P(A) = 1 − 0.57 = 0.43 (đề giữa kỳ mẫu, câu 3).', 1, TOP['add'], 'Đề giữa kỳ mẫu LTXSTK, câu 3')
    B.mcq('Xác suất một xạ thủ bắn trúng mục tiêu là 0.57. Xác suất bắn đúng 3 lần trong 3 lần bắn (các lần độc lập) là', f(0.57 ** 3, 6), [f(0.57 * 3, 6), f(0.43 ** 3, 6), f(3 * 0.57 ** 2 * 0.43, 6)], f'(0.57)³ = {f(0.57**3,6)} (đề giữa kỳ mẫu, câu 4; nhị thức với k = n).', 2, TOP['indep'], 'Đề giữa kỳ mẫu LTXSTK, câu 4')
    # ---------- Lý thuyết ----------
    S = 'Lecture Notes §1.4–1.5'
    B.mcq('Tiên đề nào KHÔNG thuộc định nghĩa tổng quát của xác suất?', 'P(A ∩ B) = P(A)P(B) với mọi A, B', ['0 ≤ P(A) ≤ 1', 'P(S) = 1', 'P(A ∪ B) = P(A) + P(B) nếu A ∩ B = ∅'], 'Ba tiên đề: không âm (và ≤ 1), chuẩn hóa P(S) = 1, cộng cho biến cố xung khắc. Công thức nhân chỉ đúng khi A, B độc lập.', 1, TOP['def'], S + ' (Định nghĩa 1.3)')
    B.mcq('Quy tắc phần bù phát biểu:', 'P(Aᶜ) = 1 − P(A)', ['P(Aᶜ) = P(A)', 'P(Aᶜ) = 1/P(A)', 'P(Aᶜ) = 1 + P(A)'], 'A và Aᶜ xung khắc và A ∪ Aᶜ = S ⇒ P(A) + P(Aᶜ) = 1 (Định lý 1.1).', 1, TOP['add'], S + ' (Định lý 1.1)')
    B.mcq('Quy tắc cộng tổng quát cho hai biến cố là:', 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B)', ['P(A ∪ B) = P(A) + P(B)', 'P(A ∪ B) = P(A)P(B)', 'P(A ∪ B) = P(A) + P(B) + P(A ∩ B)'], 'Phần giao bị đếm hai lần nên phải trừ một lần (Định lý 1.3).', 1, TOP['add'], S + ' (Định lý 1.3)')
    B.mcq('Xác suất có điều kiện P(A | B) (với P(B) > 0) được định nghĩa bằng:', 'P(A ∩ B)/P(B)', ['P(A ∩ B)/P(A)', 'P(A)·P(B)', 'P(A) + P(B) − P(A ∩ B)'], 'Khi biết B đã xảy ra, không gian mẫu thu hẹp còn B (Định nghĩa 1.4).', 1, TOP['cond'], S + ' (Định nghĩa 1.4)')
    B.mcq('Hai biến cố A, B (P(A), P(B) > 0) độc lập khi và chỉ khi:', 'P(A ∩ B) = P(A)·P(B), tức P(A | B) = P(A)', ['A ∩ B = ∅', 'P(A ∪ B) = P(A) + P(B)', 'P(A | B) = P(B | A)'], 'Định nghĩa 1.5. Lưu ý: hai biến cố xung khắc có xác suất dương KHÔNG độc lập (biết A xảy ra thì chắc chắn B không xảy ra).', 2, TOP['indep'], S + ' (Định nghĩa 1.5)')
    B.mcq('Nếu A, B xung khắc và cùng có xác suất dương thì', 'A và B KHÔNG độc lập', ['A và B độc lập', 'P(A ∩ B) = P(A)P(B)', 'P(A ∪ B) = 1'], 'P(A ∩ B) = 0 nhưng P(A)P(B) > 0 ⇒ không độc lập.', 2, TOP['indep'], S + ' (hệ quả Định nghĩa 1.5)')
    B.mcq('Công thức nhân xác suất (Định lý 1.4) là:', 'P(A ∩ B) = P(A)·P(B | A) = P(B)·P(A | B)', ['P(A ∩ B) = P(A | B) + P(B | A)', 'P(A ∩ B) = P(A) + P(B)', 'P(A ∩ B) = P(A)/P(B)'], 'Suy trực tiếp từ định nghĩa xác suất có điều kiện.', 1, TOP['cond'], S + ' (Định lý 1.4)')
    B.mcq('Ba biến cố A, B, C được gọi là độc lập nếu:', 'Độc lập từng đôi VÀ P(A ∩ B ∩ C) = P(A)P(B)P(C)', ['Chỉ cần độc lập từng đôi', 'Chỉ cần P(A ∩ B ∩ C) = P(A)P(B)P(C)', 'A, B, C xung khắc từng đôi'], 'Cần đủ 4 đẳng thức (3 cặp + bộ ba) — ví dụ 4 chip của Kreyszig Prob. 16 cho thấy độc lập từng đôi chưa đủ.', 2, TOP['indep'], S + ' (sau Định nghĩa 1.5)')
    B.mcq('Xác suất tính theo tần suất P_rel(A) = (số lần A xảy ra)/(số phép thử) có đặc điểm nào?', 'Là giá trị gần đúng, tiến về xác suất thực khi số phép thử rất lớn', ['Luôn bằng xác suất thật', 'Chỉ dùng được khi các kết cục đồng khả năng', 'Luôn lớn hơn xác suất thật'], 'Định nghĩa bằng tần suất (1.11): xấp xỉ, hội tụ khi số phép thử → ∞ (luật số lớn).', 1, TOP['def'], S + ' (1.11)')
    # ---------- Tự luận ----------
    B.essay('Bài 1.12–1.13 (Lecture Notes): gieo 4 đồng xu và 2 súc sắc — tìm các xác suất được yêu cầu.', 'Bài 1.12: (a) 2/16 = 1/8; (b) C(4,2)/16 = 3/8; (c) 11/16. Bài 1.13: (a) 15/36 = 5/12; (b) 18/36 = 1/2.', 2, TOP['classic'], S + ' Bài 1.12–1.13')
    B.essay('Bài 1.14 (Lecture Notes): lớp 30 HS (4 giỏi, 8 khá, 10 TB, 8 yếu), chọn 3 người: (a) cả ba yếu; (b) ít nhất một giỏi; (c) đúng một giỏi.', f'(a) C(8,3)/C(30,3) = {f(comb(8,3)/comb(30,3),4)}; (b) 1 − C(26,3)/C(30,3) = {f(1-comb(26,3)/comb(30,3),4)}; (c) C(4,1)C(26,2)/C(30,3) = {f(4*comb(26,2)/comb(30,3),4)}.', 3, TOP['classic'], S + ' Bài 1.14')
    B.essay('Bài 1.16–1.17: mạch 3 thiết bị nối tiếp làm việc với xác suất 95%; thiết bị 4 van hỏng khi cả 4 hỏng, mỗi van hỏng 3%.', f'Bài 1.16: (1 − q)³ = 0.95 ⇒ q = {f(q,5)}. Bài 1.17: P(làm việc) = 1 − 0.03⁴ = 0.99999919.', 3, TOP['rel'], S + ' Bài 1.16–1.17')
    B.essay('Kreyszig 24.3/16: chứng minh với 4 chip 000, 011, 101, 110 các biến cố A, B, C độc lập từng đôi nhưng không độc lập toàn phần.', 'P(A) = P(B) = P(C) = 2/4 = 1/2. A ∩ B = {110}, A ∩ C = {101}, B ∩ C = {011} ⇒ mỗi giao có xác suất 1/4 = (1/2)². A ∩ B ∩ C = ∅ ⇒ 0 ≠ 1/8.', 3, TOP['indep'], K + '16')
    B.essay('Kreyszig 24.3/15: so sánh xác suất trúng ít nhất một lần của ba chiến lược (1/2 × 1 phát; 1/4 × 2 phát; 1/8 × 4 phát).', '(a) 0.5; (b) 1 − (3/4)² = 0.4375; (c) 1 − (7/8)⁴ = 0.4138 ⇒ (a) lớn nhất.', 2, TOP['indep'], K + '15')
    B.essay('Kreyszig 24.3/18: chứng minh P(A ∩ B ∩ C) = P(A)P(B | A)P(C | A ∩ B).', 'P(A ∩ B ∩ C) = P((A ∩ B) ∩ C) = P(A ∩ B)·P(C | A ∩ B) = P(A)P(B | A)·P(C | A ∩ B) (hai lần công thức nhân).', 2, TOP['cond'], K + '18')
    B.essay('Bài 1.11 (Lecture Notes): hộp 100 ốc vít có 10 con lỗi; rút không hoàn lại 3 lần. Tính xác suất có ít nhất một con lỗi, bằng hai cách.', f'Cách 1 (bù): 1 − (90/100)(89/99)(88/98) = {f(1-90*89*88/(100*99*98),5)}. Cách 2 (trực tiếp): P(1 lỗi) + P(2 lỗi) + P(3 lỗi) = [C(10,1)C(90,2) + C(10,2)C(90,1) + C(10,3)]/C(100,3) = (40050 + 4050 + 120)/161700 = {f((10*comb(90,2)+comb(10,2)*90+comb(10,3))/comb(100,3),5)}.', 2, TOP['seq'], S + ' Bài 1.11')
    B.essay('Bài 1.18 (Lecture Notes): hộp 100 đinh ốc có 10 cái lỗi, lấy 3 lần. Tính xác suất cả 3 lỗi (a) có hoàn lại, (b) không hoàn lại và so sánh.', '(a) (1/10)³ = 0.001. (b) (10/100)(9/99)(8/98) = 720/970200 ≈ 0.000742. Không hoàn lại cho xác suất nhỏ hơn vì mỗi lần lấy một con lỗi làm giảm tỉ lệ lỗi còn lại.', 2, TOP['seq'], S + ' Bài 1.18')
    B.essay('Kreyszig 24.3/3–4: rút 3 ốc từ lô 100 có 10 lỗi; tìm P(cả 3 không lỗi) và P(ít nhất 1 lỗi) trực tiếp và bằng biến cố bù, có/không hoàn lại.', 'Có hoàn lại: 0.9³ = 0.729; ít nhất 1 lỗi = 0.271 (trực tiếp: 0.243 + 0.027 + 0.001). Không hoàn lại: 0.7265 và 0.2735.', 2, TOP['seq'], K + '3–4')
    B.essay('Kreyszig 24.3/11–13: tính các xác suất cho 200 thanh sắt (50 quá khổ, 50 thiếu khổ, 100 đạt), 4 công tắc, 3 ống điện tử.', f'11: (a) {f(r_d,4)}; (b) {f(r_1,4)}; (c) {f(r_d,4)}. 12: q = 1 − 0.99^(1/4) = {f(q12,6)}. 13: 1 − 0.96³ = 0.115264.', 3, TOP['rel'], K + '11–13')
    B.essay('Kreyszig 24.3/8–9: (a) 4 lốp mỗi lốp vượt 40 000 dặm với xác suất 0.9; (b) 5 tờ giấy từ ram 500 tờ có 0.4% tờ vết.', f'(a) 0.9⁴ = 0.6561. (b) C(498,5)/C(500,5) = {f(p9,5)} ≈ 0.980.', 2, TOP['seq'], K + '8–9')
    B.essay('Kreyszig 24.3/10: rút có hoàn lại từ 100 phiếu (50 nam, 50 nữ). Xác suất rút “nữ” lần thứ 2 trước “nam” lần thứ 3?', 'Xảy ra ⇔ trong 4 lần rút đầu có ít nhất 2 nữ ⇒ 1 − (C(4,0) + C(4,1))/16 = 11/16 = 0.6875.', 3, TOP['seq'], K + '10')
