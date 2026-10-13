from hx import *
from math import comb, perm, factorial as fac
import itertools
from orig_m02 import G

def m_(t): return f'\\({t}\\)'

def module():
    parts = []
    # ---------- PHẦN 1 ----------
    s = []
    s.append(sl('<p>Xác suất bắt đầu bằng việc <b>mô tả chính xác điều có thể xảy ra</b> và <b>đếm</b> các khả năng. Module này có hai nửa: (1) ngôn ngữ tập hợp của biến cố; (2) năm quy tắc đếm làm nền cho xác suất cổ điển ở Module 3.</p>'
                + ul(['Thực nghiệm, phép thử, kết cục, không gian mẫu S', 'Biến cố: hợp, giao, đối lập, xung khắc', 'Quy tắc cộng, quy tắc nhân', 'Hoán vị, chỉnh hợp, tổ hợp (có lặp, không lặp)']),
                'MODULE 2 · Bài học 1 · Chương 1, mục 1.2–1.3 · Kreyszig §24.2, §24.4', 'Phép thử, biến cố và nghệ thuật đếm',
                explain='Trước khi nói “xác suất bao nhiêu”, ta phải biết có bao nhiêu khả năng và bao nhiêu khả năng thuận lợi. Phần lớn lỗi sai trong xác suất thực ra là lỗi đếm.'))
    s.append(sl(table(['Khái niệm', 'Ý nghĩa', 'Ví dụ gieo súc sắc'], [['Thực nghiệm', 'quá trình đo/quan sát ngẫu nhiên', 'gieo một con súc sắc'], ['Phép thử (trial)', 'một lần thực hiện', 'một lần gieo'], ['Kết cục (outcome)', 'kết quả của một phép thử', 'mặt 3 chấm'],
                                ['Không gian mẫu S', 'tập mọi kết cục có thể', 'S = {1,2,3,4,5,6}'], ['Biến cố (sự kiện)', 'tập con của S', 'A = {1,3,5} “số lẻ”'], ['Biến cố chắc chắn / không thể', 'S / ∅', 'S; “7 chấm” = ∅']])
                + '<p>S có thể <b>hữu hạn</b> (súc sắc), <b>vô hạn đếm được</b> (tung xu đến khi ngửa: {N, SN, SSN, …}) hay <b>liên tục</b> (điện áp ∈ [0, +∞)).</p>',
                'PHẦN 1 · Nền tảng', 'Thuật ngữ cơ bản',
                explain='Hãy nghĩ S là “cái túi chứa mọi kết cục có thể”. Một biến cố là một nhóm kết cục ta quan tâm; biến cố “xảy ra” khi kết cục thực tế nằm trong nhóm đó.'))
    s.append(sl(table(['Phép toán', 'Ký hiệu', 'Ý nghĩa'], [['Hợp (tổng)', 'A ∪ B hoặc A + B', 'ít nhất một trong hai xảy ra'], ['Giao (tích)', 'A ∩ B hoặc AB', 'cả hai cùng xảy ra'], ['Đối lập', 'Aᶜ hoặc Ā', 'A không xảy ra; A ∪ Aᶜ = S, A ∩ Aᶜ = ∅'], ['Xung khắc', 'A ∩ B = ∅', 'không thể cùng xảy ra']])
                + formula('Luật De Morgan', '(A\\cup B)^c=A^c\\cap B^c,\\qquad (A\\cap B)^c=A^c\\cup B^c')
                + '<p>Gieo súc sắc: A = “&gt; 3” = {4,5,6}, B = “&lt; 6” = {1,…,5}, C = “chẵn” = {2,4,6} ⇒ A ∩ B = {4,5}, B ∩ C = {2,4}, A ∩ B ∩ C = {4}, A ∪ B = S.</p>',
                'PHẦN 1 · Nền tảng', 'Phép toán trên biến cố',
                explain='Hợp = “hoặc”, giao = “và”, đối lập = “không”. Biểu đồ Venn giúp kiểm tra: vùng tô màu của (A ∪ B)ᶜ chính là phần bên ngoài cả hai hình tròn.'))
    parts.append(dict(title='Nền tảng', bullets=['Thuật ngữ', 'Phép toán trên biến cố'], slides=s))

    # ---------- PHẦN 2 ----------
    s = []
    s.append(sl(formula('Quy tắc cộng và quy tắc nhân', 'n_1+n_2+\\dots+n_k\\ (\\text{một trong }k\\text{ phương án}),\\qquad n_1\\,n_2\\cdots n_k\\ (k\\text{ giai đoạn liên tiếp})',
                        [('n_i', 'số cách ở phương án/giai đoạn i')]) + callout('info', 'Mẹo nhớ', '“HOẶC” ⇒ cộng (chọn một trong các phương án loại trừ nhau); “VÀ/TIẾP THEO” ⇒ nhân (các giai đoạn đều phải làm).')
                + '<p>Ví dụ: số có 5 chữ số khác nhau từ {0,1,2,3,4}: chữ số đầu ≠ 0 nên 4 · 4 · 3 · 2 · 1 = 96 (không phải 5! = 120).</p>',
                'PHẦN 2 · Phương pháp', 'Hai quy tắc nền tảng', explain='Gọi món: “1 món chính HOẶC 1 món cuối cùng” là cộng; “chọn món chính VÀ chọn đồ uống” là nhân.'))
    s.append(sl(formula('Hoán vị, chỉnh hợp, tổ hợp', 'P_n=n!,\\quad A_n^k=\\dfrac{n!}{(n-k)!},\\quad C_n^k=\\dbinom nk=\\dfrac{n!}{k!(n-k)!},\\quad \\tilde A_n^k=n^k,\\quad \\dfrac{n!}{n_1!\\,n_2!\\cdots n_c!}',
                        [('n!', 'hoán vị n phần tử khác nhau'), ('A_n^k', 'chọn k, có thứ tự, không lặp'), ('C_n^k', 'chọn k, không thứ tự, không lặp (A/k!)'), ('n^k', 'chọn k có thứ tự, có lặp'), ('\\frac{n!}{\\prod n_i!}', 'hoán vị có các nhóm giống nhau')])
                + '<p>Quy ước 0! = 1. Tổ hợp lặp: C(n + k − 1, k). Hoán vị vòng quanh bàn tròn: (n − 1)!.</p>',
                'PHẦN 2 · Phương pháp', 'Hoán vị, chỉnh hợp, tổ hợp',
                explain='Hai câu hỏi quyết định công thức: (1) có quan tâm thứ tự không? (2) có được lặp không? Có thứ tự, không lặp: A. Không thứ tự, không lặp: C. Có thứ tự, lặp: n^k.'))
    s.append(sl('<svg viewBox="0 0 640 250" style="max-width:100%;width:640px;font-size:13px" fill="currentColor"><g stroke="var(--text)" fill="var(--card)" stroke-width="2"><rect x="230" y="8" width="180" height="44" rx="8"/><rect x="40" y="95" width="200" height="50" rx="8"/><rect x="400" y="95" width="200" height="50" rx="8"/><rect x="30" y="190" width="150" height="44" rx="8"/><rect x="200" y="190" width="150" height="44" rx="8"/><rect x="400" y="190" width="200" height="44" rx="8"/></g>'
                '<g stroke="var(--accent2)" stroke-width="2"><line x1="320" y1="52" x2="140" y2="95"/><line x1="320" y1="52" x2="500" y2="95"/><line x1="140" y1="145" x2="105" y2="190"/><line x1="140" y1="145" x2="275" y2="190"/><line x1="500" y1="145" x2="500" y2="190"/></g>'
                '<g text-anchor="middle" fill="var(--text)"><text x="320" y="35" font-weight="bold">Chọn k từ n phần tử</text><text x="140" y="116">Thứ tự quan trọng?</text><text x="140" y="133">(Có)</text><text x="500" y="116">Không quan tâm thứ tự</text><text x="500" y="133">(không lặp)</text><text x="105" y="209">Không lặp</text><text x="105" y="225">A = n!/(n−k)!</text><text x="275" y="209">Có lặp</text><text x="275" y="225">n^k</text><text x="500" y="209">C = n!/(k!(n−k)!)</text><text x="500" y="225">(có lặp: C(n+k−1,k))</text></g></svg>'
                + '<p style="text-align:center;font-size:.85em;color:var(--muted)">Sơ đồ chọn công thức đếm.</p>',
                'PHẦN 2 · Phương pháp', 'Sơ đồ quyết định: dùng công thức nào?'))
    s.append(sl(sim('count'), 'PHẦN 2 · Phương pháp', 'Thực hành: máy tính đếm chính xác (BigInt)'))
    s.append(sl(sim('dice'), 'PHẦN 2 · Phương pháp', 'Thực hành: không gian mẫu hai súc sắc và biến cố'))
    parts.append(dict(title='Phương pháp', bullets=['Quy tắc cộng, nhân', 'Hoán vị, chỉnh hợp, tổ hợp', 'Sơ đồ chọn công thức', 'Hai widget tương tác'], slides=s))

    # ---------- PHẦN 3 ----------
    s = []
    s.append(sl(callout('info', 'Bài 1.8 (Lecture Notes) = Kreyszig PS 24.4/5', 'Chọn hội đồng 3 kỹ sư, 2 nhà sinh học, 2 nhà hóa học từ 10 kỹ sư, 5 nhà sinh học, 6 nhà hóa học.')
                + steps(['Ba nhóm chọn độc lập ⇒ quy tắc nhân.', m_('C_{10}^3=120,\\ C_5^2=10,\\ C_6^2=15'), m_('120\\cdot 10\\cdot 15=18\\,000')]), 'PHẦN 3 · Ví dụ', 'Ví dụ 1: hội đồng ba nhóm'))
    s.append(sl(callout('info', 'Đề giữa kỳ mẫu, câu 2', 'Lớp có 13 bạn nam và 17 bạn nữ. Chọn nhóm 2 nam và 3 nữ.')
                + steps([m_('C_{13}^2=78,\\quad C_{17}^3=680'), m_('78\\cdot 680=53\\,040\\text{ cách}')]) + callout('warn', 'Bẫy', 'Không dùng C(30,5) (đó là chọn 5 người bất kỳ) và không cộng 78 + 680 (hai việc đều phải làm ⇒ nhân).'),
                'PHẦN 3 · Ví dụ', 'Ví dụ 2: nhóm 2 nam 3 nữ (đề giữa kỳ)'))
    s.append(sl(callout('info', 'Kreyszig PS 24.4/7', 'Lô 10 vật có 2 vật hỏng. Đếm các mẫu 4 vật.')
                + table(['Loại mẫu', 'Số mẫu'], [['Tất cả', 'C(10,4) = 210'], ['Không có vật hỏng', 'C(8,4) = 70'], ['Đúng 1 hỏng', 'C(2,1)·C(8,3) = 112'], ['Cả 2 hỏng', 'C(2,2)·C(8,2) = 28']])
                + '<p>Kiểm tra: 70 + 112 + 28 = 210 ✓ (các trường hợp loại trừ nhau và phủ hết).</p>', 'PHẦN 3 · Ví dụ', 'Ví dụ 3: phân hoạch mẫu theo số vật hỏng'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)', bullets=['Hội đồng ba nhóm', 'Nhóm 2 nam 3 nữ', 'Phân hoạch mẫu theo số vật hỏng'], slides=s))

    # ---------- PHẦN 4 ----------
    s = []
    s.append(sl(ul(['<b>Cộng thay vì nhân</b> (hoặc ngược lại): “và” ⇒ nhân, “hoặc” ⇒ cộng.', '<b>Bỏ qua ràng buộc chữ số đầu ≠ 0</b> khi lập số.', '<b>Dùng chỉnh hợp thay tổ hợp</b>: chọn nhóm/hội đồng không có thứ tự ⇒ C.', '<b>Đếm trùng</b> khi dùng “ít nhất 1”: dùng biến cố bù (tổng trừ trường hợp 0).',
                    '<b>Hoán vị có lặp</b>: chia cho n_i! của từng nhóm giống nhau.', '<b>Bàn tròn</b>: (n − 1)!, không phải n!.']), 'PHẦN 4 · Bẫy và mở rộng', 'Sáu bẫy thường gặp'))
    s.append(sl(callout('warn', 'Lỗi in trong giáo trình (đã kiểm chứng)', 'Ví dụ 1.11: 7!/(2!·3!·2!) = 5040/24 = <b>210</b>, giáo trình in “201”. Ví dụ 1.7: B ∪ C = S (không phải {2,4,5,6}); Ví dụ 1.8: B ∩ C = {2,4} (không phải {4,6}).')
                + '<p>Kiểm chứng độc lập: liệt kê 5040 hoán vị của chuỗi 1122233 và đếm các hoán vị phân biệt: 210.</p>', 'PHẦN 4 · Bẫy và mở rộng', 'Sai sót đã phát hiện trong tài liệu'))
    parts.append(dict(title='Bẫy và mở rộng', bullets=['Sáu bẫy', 'Lỗi in đã sửa'], slides=s))

    # ---------- PHẦN 5 ----------
    s = []
    pb = 1 - 1.0
    import math
    pbd = 1 - math.prod((365 - i) / 365 for i in range(20))
    s.append(sl(f'<p><b>Bài toán ngày sinh</b> (Kreyszig PS 24.4/15): trong nhóm 20 người, xác suất có ít nhất hai người trùng ngày sinh là 1 − (365·364·…·346)/365²⁰ ≈ <b>{pbd:.4f}</b> — gần 41%, vượt xa trực giác. Với 23 người đã vượt 50%. Ứng dụng: va chạm băm (hash collision), thiết kế mật khẩu và mã định danh.</p>', 'PHẦN 5 · Ứng dụng và tổng kết', 'Case study: bài toán ngày sinh'))
    s.append(sl(ul(['Biến cố là tập con của S; dùng hợp/giao/đối lập.', 'Cộng cho “hoặc”, nhân cho “và”.', 'Thứ tự? ⇒ A(n,k); không thứ tự ⇒ C(n,k); có lặp ⇒ n^k hoặc C(n+k−1,k).', '“Ít nhất một” ⇒ biến cố bù.']) + callout('good', 'Tiếp theo', 'Module 3: định nghĩa xác suất, xác suất có điều kiện và độc lập — dùng chính các phép đếm này.'), 'PHẦN 5 · Ứng dụng và tổng kết', 'Tổng kết module'))
    parts.append(dict(title='Ứng dụng và tổng kết', bullets=['Ngày sinh', 'Tổng kết'], slides=s))

    # ---------- NỘI DUNG CHI TIẾT ----------
    notes = '<h2>1. Nội dung chi tiết</h2><p>Lecture Notes §1.2 định nghĩa thực nghiệm, phép thử, kết cục, không gian mẫu, biến cố và các phép toán (Ví dụ 1.2–1.8). §1.3 nhắc lại quy tắc cộng, quy tắc nhân, hoán vị (kể cả có lặp và công thức Stirling), chỉnh hợp (lặp/không lặp) và tổ hợp. Kreyszig §24.2 trình bày cùng nội dung (kèm biểu đồ Venn, De Morgan), §24.4 thêm tổ hợp có lặp, định lý nhị thức và bài toán ngày sinh.</p>'
    notes += '<h2>2. Năm ví dụ chi tiết có lời giải</h2>'
    notes += ex('1. Lecture Notes Bài 1.4–1.5: hai súc sắc', '<p>Gieo hai con súc sắc. Tìm không gian mẫu và các biến cố (a) hai mặt bằng nhau; (b) tổng &gt; 9; (c) tổng = 7.</p>' + steps(['|S| = 6·6 = 36: các cặp (a, b), a, b ∈ {1,…,6}.', '(a) {(1,1),(2,2),…,(6,6)}: 6 kết cục.', '(b) tổng 10: (4,6),(5,5),(6,4); tổng 11: (5,6),(6,5); tổng 12: (6,6) ⇒ 6 kết cục.', '(c) (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) ⇒ 6 kết cục.']))
    notes += ex('2. Lecture Notes Bài 1.7: số có 5 chữ số khác nhau từ {0,1,2,3,4}', '<p>Chữ số đầu khác 0 nên có 4 cách; các chữ số còn lại là hoán vị 4 chữ số còn lại: 4·4·3·2·1 = <b>96</b>. Kiểm chứng bằng liệt kê toàn bộ 5! = 120 hoán vị rồi loại 24 hoán vị bắt đầu bằng 0 ⇒ 96.</p>')
    notes += ex('3. Lecture Notes Bài 1.9: chọn 12 chuột có 2 đực', f'<p>Lồng 100 chuột có 2 đực. Chọn 12 con trong đó có (đủ) 2 con đực: C(2,2)·C(98,10) = <b>{G(comb(98,10))}</b>.</p>')
    notes += ex('4. Kreyszig PS 24.4/12: nhận dạng nghi phạm', '<p>3 nghi phạm + 6 người vô tội, nhân chứng chọn ngẫu nhiên 3 người.</p>' + steps(['|S| = C(9,3) = 84.', 'Chọn đúng 3 nghi phạm: C(3,3) = 1 ⇒ P = 1/84.', 'Chọn 3 người vô tội: C(6,3) = 20 ⇒ P = 20/84 = 5/21.']))
    notes += ex('5. Kreyszig PS 24.4/4: bình có 2 xanh, 3 vàng, 5 đỏ', '<p>Rút lần lượt không hoàn lại; xác suất ra thứ tự: 2 xanh trước, rồi 3 vàng, rồi các bi đỏ. Số chuỗi màu phân biệt = 10!/(2!3!5!) = 2520 và đều đồng khả năng ⇒ P = 1/2520.</p>')
    notes += '<h2>3. Thực hành tương tác</h2><p>Widget 1: máy tính đếm (hoán vị/chỉnh hợp/tổ hợp, số lớn chính xác). Widget 2: không gian mẫu 36 ô của hai súc sắc.</p>' + sim('count') + sim('dice')
    notes += '<h2>4. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Từ trò chơi đến lý thuyết', 'Giải tích tổ hợp và xác suất khởi đầu từ thư từ giữa Pascal và Fermat (1654) về bài toán chia tiền cược. Biểu đồ Venn do John Venn (1834–1923) giới thiệu; công thức Stirling n! ≈ √(2πn)(n/e)ⁿ có sai số tương đối ≈ 1/(12n) (khoảng 0.83% khi n = 10).')
    notes += '<h2>5. Case study</h2><p>Một hệ thống cấp mã vé gồm 2 chữ cái in hoa khác nhau và 3 chữ số tùy ý: 26·25·10³ = 650 000 mã (chữ khác nhau ⇒ chỉnh hợp, chữ số có lặp ⇒ 10³). Nếu cho phép chữ cái lặp, số mã tăng lên 676 000 — nhưng xác suất “trùng mã khi cấp ngẫu nhiên” cũng tăng; đây chính là bài toán ngày sinh với 650 000 “ngày”.</p>'
    notes += '<h2>6. Bẫy khi làm bài</h2>' + callout('warn', 'Chú ý', '• Luôn tự hỏi: có thứ tự không? có lặp không?<br>• “Ít nhất một” ⇒ lấy tổng trừ trường hợp không có.<br>• Kiểm tra bằng phân hoạch: các trường hợp phải loại trừ và cộng lại đúng tổng.')
    return dict(id='m02', slug='m02-phep-thu-su-kien-dem', title='Phép thử, kết cục, sự kiện và quy tắc đếm', subtitle='Không gian mẫu, biến cố, De Morgan, quy tắc cộng/nhân, hoán vị, chỉnh hợp, tổ hợp',
                source='Lecture Notes §1.2–1.3, Bài 1.4–1.10 · Kreyszig §24.2, §24.4 (PS 24.2, 24.4) · Đề giữa kỳ mẫu câu 2', exam='Đề giữa kỳ mẫu câu 2; nền tảng cho xác suất cổ điển ở Module 3', time='≈ 3 giờ',
                objectives=['Mô tả không gian mẫu và biến cố bằng ngôn ngữ tập hợp', 'Dùng đúng quy tắc cộng/nhân, hoán vị, chỉnh hợp, tổ hợp (có/không lặp)', 'Chia bài toán chọn nhóm thành các trường hợp loại trừ và kiểm tra bằng tổng', 'Nhận ra các lỗi in trong giáo trình bằng kiểm chứng độc lập'],
                parts=parts, notes=notes, sims=['count', 'dice'])
