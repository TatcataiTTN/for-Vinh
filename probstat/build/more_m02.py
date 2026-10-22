"""Module 2 — phần chuyên sâu: mọi kết quả đếm được kiểm chứng bằng liệt kê (itertools) khi dựng trang."""
import itertools
from math import comb, perm, factorial as fac
from hx import *
K = 'MODULE 2 · '
def parts():
    P = []
    # kiểm chứng bằng liệt kê
    d3 = [p for p in itertools.permutations(range(10), 3) if p[0] != 0]
    assert len(d3) == 9 * 9 * 8 == 648
    n_even = sum(1 for p in d3 if p[2] % 2 == 0); n5 = sum(1 for p in d3 if p[2] % 5 == 0)
    assert (n_even, n5) == (328, 136)
    assert sum(1 for n in range(1, 101) if n % 2 == 0 or n % 3 == 0 or n % 5 == 0) == 74
    assert sum(1 for a in range(11) for b in range(11) for c in range(11) for d in range(11) if a + b + c + d == 10) == comb(13, 3)
    # ───────── A. Đại số biến cố ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ A1 · Biến cố trên bộ bài', 'Rút một lá từ bộ 52 lá. A = “lá cơ” (13), B = “lá J, Q, K” (12), C = “lá đỏ” (26).')
                + steps([m('A\\cap B=\\{J♥,Q♥,K♥\\}\\Rightarrow|A\\cap B|=3'), m('|A\\cup B|=13+12-3=22\\quad(\\text{công thức bù trừ})'), m('A\\subset C\\ \\text{vì mọi lá cơ đều đỏ};\\ A\\cap C=A'), m('|C^c|=52-26=26\\ (\\text{lá đen})')])
                + '<p>A và B không xung khắc (có chung 3 lá); A và “lá bích” xung khắc.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Phép toán trên biến cố: bộ bài'))
    s.append(sl(callout('info', 'Ví dụ A2 · Luật De Morgan', 'Một hệ gồm hai bộ phận. A = “bộ phận 1 hỏng”, B = “bộ phận 2 hỏng”. Biểu diễn bằng A, B các biến cố: (a) cả hệ hoạt động nếu chạy nối tiếp; (b) hệ chạy song song hỏng.')
                + steps([m('\\text{(a) Nối tiếp hoạt động khi cả hai tốt: }A^c\\cap B^c=(A\\cup B)^c'), m('\\text{(b) Song song hỏng khi cả hai hỏng: }A\\cap B'), m('(A\\cap B)^c=A^c\\cup B^c:\\ \\text{“không phải cả hai hỏng” = “ít nhất một bộ phận tốt”}')]),
                K + 'PHẦN 1 · Chuyên sâu', 'De Morgan trong độ tin cậy hệ thống'))
    s.append(sl(table(['Thuật ngữ', 'Ý nghĩa', 'Kiểm tra bằng tập hợp'], [['Xung khắc', 'không cùng xảy ra', 'A ∩ B = ∅'], ['Hệ đầy đủ', 'luôn có đúng một xảy ra', 'Aᵢ đôi một xung khắc và ∪Aᵢ = S'], ['Biến cố sơ cấp', 'chỉ chứa một kết cục', '{ω}'], ['Biến cố kéo theo', 'A xảy ra thì B xảy ra', 'A ⊂ B']])
                + callout('warn', 'Xung khắc ≠ độc lập', 'Hai biến cố có xác suất dương mà xung khắc thì KHÔNG độc lập (biết A xảy ra thì chắc chắn B không xảy ra). Sẽ thấy rõ ở Module 3.'), K + 'PHẦN 1 · Chuyên sâu', 'Bốn khái niệm hay nhầm'))
    P.append(dict(title='Chuyên sâu: đại số biến cố', bullets=['Biến cố trên bộ bài', 'De Morgan trong độ tin cậy', 'Xung khắc, hệ đầy đủ'], slides=s))
    # ───────── B. Đếm có điều kiện ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ B1 · Số có 3 chữ số khác nhau', 'Lập số có 3 chữ số khác nhau từ 0–9. Có bao nhiêu số? bao nhiêu số chẵn? bao nhiêu số chia hết cho 5?')
                + steps([m('\\text{Tổng: }9\\cdot9\\cdot8=648\\ (\\text{hàng trăm}\\ne0)'), m('\\text{Chẵn: chia theo chữ số tận cùng. Tận cùng 0: }9\\cdot8=72;\\ \\text{tận cùng 2,4,6,8: }4\\cdot8\\cdot8=256;\\ \\text{tổng }328'), m('\\text{Chia hết cho 5: tận cùng 0: }72;\\ \\text{tận cùng 5: }8\\cdot8=64;\\ \\text{tổng }136')])
                + '<p>Bẫy: khi có ràng buộc, đếm vị trí bị ràng buộc trước (chữ số tận cùng), rồi mới đếm các vị trí còn lại. Kết quả đã được kiểm chứng bằng liệt kê 648 số.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Đếm số với ràng buộc: ưu tiên vị trí khó'))
    s.append(sl(callout('info', 'Ví dụ B2 · Biển số xe', 'Biển số gồm 2 chữ cái (26 chữ) rồi 4 chữ số. Có bao nhiêu biển? Nếu chữ cái không lặp và chữ số đầu khác 0?')
                + steps([m('26^2\\cdot10^4=6\\,760\\,000'), m('26\\cdot25\\cdot9\\cdot10^3=5\\,850\\,000')]), K + 'PHẦN 2 · Chuyên sâu', 'Quy tắc nhân với có lặp và không lặp'))
    s.append(sl(callout('info', 'Ví dụ B3 · Xếp hàng', '6 người xếp thành một hàng. (a) Tổng cách? (b) A và B đứng cạnh nhau? (c) A và B không đứng cạnh nhau? (d) Xếp quanh bàn tròn?')
                + steps([m('6!=720'), m('\\text{Buộc A, B thành một “khối”: }5!\\cdot2!=240'), m('720-240=480\\ (\\text{phần bù})'), m('(6-1)!=120\\ (\\text{bàn tròn})')]), K + 'PHẦN 2 · Chuyên sâu', 'Xếp hàng và kỹ thuật “buộc khối”'))
    s.append(sl(callout('info', 'Ví dụ B4 · Hoán vị có phần tử giống nhau', 'Có bao nhiêu cách sắp xếp các chữ cái của từ MISSISSIPPI? Của từ STATISTICS?')
                + steps([m('\\text{MISSISSIPPI: 11 chữ (M×1, I×4, S×4, P×2): }\\tfrac{11!}{1!\\,4!\\,4!\\,2!}=34\\,650'), m('\\text{STATISTICS: 10 chữ (S×3, T×3, A×1, I×2, C×1): }\\tfrac{10!}{3!\\,3!\\,1!\\,2!\\,1!}=50\\,400')]),
                K + 'PHẦN 2 · Chuyên sâu', 'Chia cho giai thừa các nhóm giống nhau'))
    s.append(sl(callout('info', 'Ví dụ B5 · Chọn nhóm có điều kiện', 'Từ 5 nữ và 7 nam chọn nhóm 5 người. (a) Tổng cách? (b) Có ít nhất 2 nữ? (c) Có đúng 3 nam?')
                + steps([m('\\binom{12}5=792'), m('\\text{Dùng phần bù: }792-\\binom75-\\binom51\\binom74=792-21-175=596'), m('\\binom73\\binom52=35\\cdot10=350')]) + '<p>“Ít nhất” thường tính bằng phần bù (trừ các trường hợp “không có” và “chỉ có 1”).</p>', K + 'PHẦN 2 · Chuyên sâu', 'Tổ hợp với “ít nhất”: dùng phần bù'))
    s.append(sl(callout('info', 'Ví dụ B6 · Chia vật vào hộp (sao và thanh)', 'Chia 10 viên kẹo giống nhau cho 4 em (có thể có em không nhận). Bao nhiêu cách? Nếu mỗi em ít nhất 1 viên?')
                + steps([m('\\text{Nghiệm không âm của }x_1+x_2+x_3+x_4=10:\\ \\binom{10+4-1}{4-1}=\\binom{13}3=286'), m('\\text{Mỗi em ≥ 1: đặt }y_i=x_i-1\\Rightarrow\\sum y_i=6:\\ \\binom{9}3=84')]) + '<p>Hình dung 10 “sao” và 3 “thanh” ngăn cách 4 em: chọn vị trí 3 thanh trong 13 chỗ.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Tổ hợp lặp: sao và thanh'))
    s.append(sl(callout('info', 'Ví dụ B7 · Nguyên lý bù trừ', 'Bao nhiêu số từ 1 đến 100 chia hết cho 2 hoặc 3 hoặc 5?')
                + steps([m('|A_2|=50,\\ |A_3|=33,\\ |A_5|=20'), m('|A_2\\cap A_3|=16,\\ |A_2\\cap A_5|=10,\\ |A_3\\cap A_5|=6,\\ |A_2\\cap A_3\\cap A_5|=3'), m('50+33+20-16-10-6+3=74')]) + '<p>Đã kiểm chứng bằng liệt kê trực tiếp: 74 số. Công thức tổng quát: cộng các tập đơn, trừ giao đôi, cộng giao ba, …</p>', K + 'PHẦN 2 · Chuyên sâu', 'Bù trừ cho ba tập'))
    P.append(dict(title='Chuyên sâu: đếm có điều kiện', bullets=['Ràng buộc vị trí', 'Xếp hàng, kỹ thuật khối', 'Hoán vị có lặp', 'Phần bù, sao và thanh, bù trừ'], slides=s))
    # ───────── C. Bài đếm kinh điển ─────────
    s = []
    n5 = comb(52, 5)
    s.append(sl(callout('info', 'Ví dụ C1 · Poker: đếm các tay bài 5 lá', f'Tổng số tay bài: C(52, 5) = {n5:,}.'.replace(',', ' '))
                + table(['Tay bài', 'Số cách', 'Cách đếm', 'Xác suất'],
                        [['Bốn lá giống', '624', '13 · C(48, 1)', f'{624/n5:.6f}'], ['Cù lũ (3 + 2)', '3744', '13·C(4,3)·12·C(4,2)', f'{3744/n5:.6f}'], ['Thùng (5 cùng chất, kể cả sảnh)', '5148', '4·C(13, 5)', f'{5148/n5:.6f}'], ['Một đôi', '1 098 240', '13·C(4,2)·C(12,3)·4³', f'{1098240/n5:.4f}']])
                + '<p>Mẫu số chung là số tay bài tổ hợp (không thứ tự); mỗi tử số cũng đếm tổ hợp. Kết quả cù lũ 3744 được đối chiếu độc lập.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Đếm các tay bài poker'))
    s.append(sl(callout('info', 'Ví dụ C2 · Ngày sinh', 'Trong nhóm k người, xác suất ít nhất hai người trùng ngày sinh (365 ngày, đồng khả năng).')
                + formula('Phần bù', 'P(\\text{trùng})=1-\\dfrac{365\\cdot364\\cdots(365-k+1)}{365^k}')
                + table(['k', '10', '20', '23', '30', '50', '70'], [['P(trùng)'] + [f'{1 - perm(365, k) / 365 ** k:.4f}' for k in (10, 20, 23, 30, 50, 70)]])
                + '<p>Chỉ cần 23 người đã vượt 50% (0.5073). Lý do: có C(23, 2) = 253 cặp người để trùng.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Bài toán ngày sinh'))
    s.append(sl(callout('info', 'Ví dụ C3 · Xác suất cổ điển (xem trước Module 3)', 'Chọn ngẫu nhiên 3 người từ 5 nữ và 7 nam. P(đúng 2 nữ)?')
                + steps([m('|S|=\\binom{12}3=220'), m('|A|=\\binom52\\binom71=10\\cdot7=70'), m('P(A)=\\tfrac{70}{220}=\\tfrac7{22}\\approx0.3182')]) + '<p>Cùng một cách đếm (tổ hợp) cho tử và mẫu — đây là mẫu của xác suất cổ điển P = |A|/|S|.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Từ đếm đến xác suất'))
    P.append(dict(title='Chuyên sâu: bài đếm kinh điển', bullets=['Poker', 'Ngày sinh', 'Từ đếm đến xác suất'], slides=s))
    return P
