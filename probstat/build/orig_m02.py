"""Module 2 — Phép thử, sự kiện, quy tắc đếm. Câu GỐC: Lecture Notes §1.2–1.3 + Bài 1.4–1.10, Kreyszig PS 24.2 & 24.4,
đề giữa kỳ mẫu câu 2. Đáp án tự tính (math.comb/perm) và kiểm bằng vét cạn itertools khi có thể."""
import math, itertools, random
from math import comb, perm, factorial as fac
from qb import f, fg, nd, ni

TOP = {'space': 'Không gian mẫu và biến cố', 'ops': 'Phép toán trên biến cố', 'rule': 'Quy tắc cộng, nhân', 'perm': 'Hoán vị, chỉnh hợp',
       'comb': 'Tổ hợp', 'mix': 'Đếm kết hợp / chọn nhóm', 'prob': 'Xác suất cổ điển bằng phép đếm', 'theory': 'Lý thuyết'}

def G(n):
    """Định dạng số nguyên lớn: nhóm 3 chữ số bằng khoảng trắng hẹp."""
    return f'{n:,}'.replace(',', ' ')

def build(B):
    rng = random.Random(202)
    def cnt(stem, ans, wrong, expl, lvl, topic, src):
        wl = [w for w in wrong if w != ans]
        if isinstance(ans, int):
            for w in (ans * 2, max(1, ans // 2), ans + max(1, ans // 9), max(1, ans - max(1, ans // 7)), ans * 3):
                if w != ans and w not in wl and len(set(wl)) < 4: wl.append(w)
        ws = [G(w) if isinstance(w, int) else str(w) for w in wl]
        B.mcq(stem, G(ans) if isinstance(ans, int) else str(ans), ws, expl, lvl, topic, src)
    def near(a, extra=()):
        return list(extra) + [a + 1, a - 1, a * 2, max(1, a // 2), a + 10, a * 3]

    # ================= A. Không gian mẫu, biến cố =================
    S = 'Lecture Notes §1.2 / Bài 1.4–1.5'
    pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    assert len(pairs) == 36
    cnt('Gieo hai con súc sắc cân đối (phân biệt được). Không gian mẫu S (các cặp (a, b)) có bao nhiêu kết cục?', 36, near(36, [12, 6, 21]),
        'Mỗi con có 6 mặt, theo quy tắc nhân |S| = 6 × 6 = 36 (Bài 1.4).', 1, TOP['space'], 'Lecture Notes Bài 1.4')
    ev_a = [p for p in pairs if p[0] == p[1]]; ev_b = [p for p in pairs if sum(p) > 9]; ev_c = [p for p in pairs if sum(p) == 7]
    cnt('Gieo hai con súc sắc. Sự kiện “hai mặt bằng nhau” (Bài 1.5a) gồm bao nhiêu kết cục?', len(ev_a), [12, 36, 5, 3],
        'Các cặp (k, k), k = 1..6 ⇒ 6 kết cục.', 1, TOP['space'], 'Lecture Notes Bài 1.5(a)')
    cnt('Gieo hai con súc sắc. Sự kiện “tổng số chấm lớn hơn 9” (Bài 1.5b) gồm bao nhiêu kết cục?', len(ev_b), [3, 4, 10, 36],
        f'Tổng 10: (4,6), (5,5), (6,4); tổng 11: (5,6), (6,5); tổng 12: (6,6) ⇒ {len(ev_b)} kết cục.', 2, TOP['space'], 'Lecture Notes Bài 1.5(b)')
    cnt('Gieo hai con súc sắc. Sự kiện “tổng số chấm bằng 7” (Bài 1.5c) gồm bao nhiêu kết cục?', len(ev_c), [7, 5, 12, 36],
        '(1,6), (2,5), (3,4), (4,3), (5,2), (6,1) ⇒ 6 kết cục. Đây là tổng có nhiều cách nhất khi gieo hai súc sắc.', 1, TOP['space'], 'Lecture Notes Bài 1.5(c)')
    B.mcq('Thực nghiệm “tung một đồng xu cho đến khi xuất hiện mặt ngửa lần đầu” (Bài 1.6): không gian mẫu là gì?', 'S = {N, SN, SSN, SSSN, …}: vô hạn đếm được',
          ['S = {sấp, ngửa}: hữu hạn, 2 phần tử', 'S = [0, +∞): một khoảng liên tục', 'S = {1, 2, 3}: 3 phần tử'],
          'Kết cục là chuỗi các mặt sấp rồi một mặt ngửa; số lần tung có thể là 1, 2, 3, … không có cận trên ⇒ vô hạn nhưng đếm được (tương ứng các số nguyên dương).', 2, TOP['space'], 'Lecture Notes Bài 1.6 / Kreyszig PS 24.2 Prob. 5')
    B.mcq('Tung một đồng xu hai lần và ghi kết quả từng lần. Không gian mẫu có bao nhiêu điểm mẫu?', '4', ['2', '3', '6'], 'Các kết cục: SS, SN, NS, NN ⇒ 4 (quy tắc nhân 2 × 2).', 1, TOP['space'], 'Kreyszig PS 24.2, Prob. 2')
    B.mcq('Rút lần lượt 3 con ốc vít từ một lô gồm ốc xoắn phải (R) và ốc xoắn trái (L), ghi loại từng con. Số điểm mẫu của không gian mẫu là:', '8', ['3', '6', '9'],
          '2 × 2 × 2 = 8: RRR, RRL, RLR, RLL, LRR, LRL, LLR, LLL.', 1, TOP['space'], 'Kreyszig PS 24.2, Prob. 1')
    B.mcq('Gieo ba con súc sắc. Không gian mẫu (các bộ (a, b, c)) có bao nhiêu điểm?', '216', ['18', '36', '120'], 'Mỗi súc sắc có 6 mặt và ba súc sắc độc lập nên theo quy tắc nhân |S| = 6·6·6 = 6³ = 216.', 1, TOP['space'], 'Kreyszig PS 24.2 (mở rộng Prob. 3)')
    B.mcq('Chọn một ủy ban 2 người từ nhóm 5 người (Kreyszig PS 24.2, Prob. 8). Số điểm mẫu là:', '10', ['20', '25', '5'], 'Không phân biệt thứ tự: C(5,2) = 10.', 1, TOP['space'], 'Kreyszig PS 24.2, Prob. 8')
    B.mcq('Lấy lần lượt (không hoàn lại) từng chiếc đệm cho đến khi gặp chiếc hỏng duy nhất trong lô 10 chiếc. Số điểm mẫu (vị trí của chiếc hỏng) là:', '10', ['9', '11', '10!'],
          'Chiếc hỏng có thể xuất hiện ở lần rút thứ 1, 2, …, 10 ⇒ 10 kết cục.', 2, TOP['space'], 'Kreyszig PS 24.2, Prob. 9')
    B.mcq('Đo điện áp hai đầu một mạch điện (kết quả thực không âm). Không gian mẫu là:', 'Khoảng [0, +∞) (liên tục)', ['Tập hữu hạn {0, 1, 2}', 'Tập {sấp, ngửa}', 'Tập rỗng'],
          'Biến đo liên tục nên S là một khoảng số (giáo trình ví dụ 1.5).', 1, TOP['space'], 'Lecture Notes Ví dụ 1.5')
    B.mcq('Đếm số tai nạn giao thông trong một ngày ở Hà Nội. Không gian mẫu là:', 'Tập các số nguyên không âm {0, 1, 2, …}', ['Khoảng thực (0, 1)', '{Có, Không}', 'Chỉ {0, 1}'],
          'Kết quả đếm là số nguyên không âm (Kreyszig Example 5).', 1, TOP['space'], 'Kreyszig §24.2, Example 5')
    B.mcq('Hỏi ý kiến về một mẫu ô tô mới: {Thích, Không thích, Chưa quyết định}. Đó là không gian mẫu gồm bao nhiêu điểm?', '3', ['2', '4', 'Vô hạn'], 'Ba kết cục liệt kê trực tiếp (Kreyszig Example 6).', 1, TOP['space'], 'Kreyszig §24.2, Example 6')
    B.mcq('Khi gieo súc sắc, “xuất hiện mặt 7 chấm hoặc 0 chấm” là loại biến cố nào?', 'Biến cố không thể (∅)', ['Biến cố chắc chắn (S)', 'Biến cố cơ sở', 'Biến cố đối của S'],
          'Không kết cục nào thỏa ⇒ tập rỗng; biến cố chắc chắn trùng S (Ví dụ 1.6).', 1, TOP['space'], 'Lecture Notes Ví dụ 1.6')
    B.mcq('Khi gieo súc sắc, A = {1, 3, 5}, B = {2, 4, 6}. Biến cố A ∪ B là:', 'S = {1, 2, 3, 4, 5, 6} (biến cố chắc chắn)', ['∅', '{1, 2}', '{3, 4}'], 'Hợp chứa mọi điểm thuộc A hoặc B; A, B là đối lập của nhau nên A ∪ B = S, A ∩ B = ∅.', 1, TOP['ops'], 'Lecture Notes Ví dụ 1.6 / Kreyszig Ex. 7')
    # ví dụ 1.7/1.8: A>3, B<6, C chẵn
    A_ = {4, 5, 6}; B_ = {1, 2, 3, 4, 5}; C_ = {2, 4, 6}; Sx = set(range(1, 7))
    q = 'Gieo một con súc sắc với A = “số điểm > 3”, B = “số điểm < 6”, C = “số chẵn”. '
    cnt(q + 'Số phần tử của A ∪ B là', len(A_ | B_), [5, 3, 4], 'A = {4,5,6}, B = {1,2,3,4,5} ⇒ A ∪ B = S (6 phần tử).', 1, TOP['ops'], 'Lecture Notes Ví dụ 1.7')
    cnt(q + 'Số phần tử của B ∪ C là', len(B_ | C_), [4, 5, 3], 'B = {1,2,3,4,5}, C = {2,4,6} ⇒ B ∪ C = {1,2,3,4,5,6} = S (6 phần tử). Giáo trình in nhầm “B ∪ C = {2,4,5,6}”.', 2, TOP['ops'], 'Lecture Notes Ví dụ 1.7 (đã sửa lỗi in)')
    cnt(q + 'Số phần tử của A ∩ B là', len(A_ & B_), [1, 3, 5], 'A ∩ B = {4, 5}.', 1, TOP['ops'], 'Lecture Notes Ví dụ 1.8')
    cnt(q + 'Số phần tử của B ∩ C là', len(B_ & C_), [1, 3, 5], 'B ∩ C = {2, 4} (Kreyszig Example 8). Giáo trình in nhầm “{4, 6}” — đó là C ∩ A.', 1, TOP['ops'], 'Lecture Notes Ví dụ 1.8 (đã sửa lỗi in) / Kreyszig Ex. 8')
    cnt(q + 'Số phần tử của A ∩ B ∩ C là', len(A_ & B_ & C_), [0, 2, 3], 'A ∩ B ∩ C = {4}.', 2, TOP['ops'], 'Lecture Notes Ví dụ 1.8')
    # Kreyszig 13
    eq = {p for p in pairs if p[0] == p[1]}; lt5 = {p for p in pairs if sum(p) < 5}
    cnt('Gieo hai súc sắc: A = “hai mặt bằng nhau”, B = “tổng các mặt nhỏ hơn 5”. |B| = ?', len(lt5), [4, 5, 10, 3], 'Tổng 2: 1 cách; tổng 3: 2 cách; tổng 4: 3 cách ⇒ 6.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 13')
    cnt('Với A, B ở bài trên: |A ∩ B| = ?', len(eq & lt5), [1, 3, 4, 6], '(1,1) có tổng 2 và (2,2) có tổng 4 (< 5); (3,3) có tổng 6 không thỏa ⇒ 2.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 13')
    cnt('Với A, B ở bài trên: |A ∪ B| = ?', len(eq | lt5), [12, 8, 9, 11], '|A ∪ B| = |A| + |B| − |A ∩ B| = 6 + 6 − 2 = 10.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 13')
    cnt('Với A ở bài trên, số phần tử của biến cố đối Aᶜ là', 36 - len(eq), [6, 18, 35, 25], '|Aᶜ| = 36 − 6 = 30.', 1, TOP['ops'], 'Kreyszig PS 24.2, Prob. 13')
    d3 = list(itertools.product(range(1, 7), repeat=3)); a3 = [t for t in d3 if sum(t) % 3 == 0]; b3 = [t for t in d3 if sum(t) % 5 == 0]
    both3 = [t for t in d3 if sum(t) % 15 == 0]
    B.mcq('Gieo ba súc sắc, A = “tổng chia hết cho 3”, B = “tổng chia hết cho 5”. A và B có xung khắc không?', 'Không xung khắc (có tổng bằng 15 chia hết cho cả 3 và 5)', ['Xung khắc vì 3 và 5 nguyên tố cùng nhau', 'Xung khắc vì A ∩ B = S', 'Không thể kết luận'],
          f'Tổng ba súc sắc từ 3 đến 18 nên có thể bằng 15 = 3·5; có {len(both3)} bộ như vậy (ví dụ (4,5,6)) ⇒ A ∩ B ≠ ∅.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 10')
    B.mcq('Gieo hai súc sắc, A = “tổng chia hết cho 3”, B = “tổng chia hết cho 5”. A và B có xung khắc không?', 'Có, xung khắc (không có tổng nào chia hết cho cả 3 và 5 trong khoảng 2…12)', ['Không xung khắc vì có tổng 15', 'Không xung khắc vì có tổng 6', 'Không thể kết luận'],
          'Tổng hai súc sắc ∈ {2, …, 12}; chia hết cho 15 là không thể (15 > 12) ⇒ A ∩ B = ∅.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 11')
    B.mcq('Rút 2 con ốc vít (phải/trái). A: “ít nhất 1 phải”, B: “ít nhất 1 trái”. A và B có xung khắc không?', 'Không xung khắc (cặp một phải một trái thuộc cả hai)', ['Xung khắc', 'Chỉ xung khắc nếu hoàn lại', 'Luôn A = B'],
          'Kết cục RL (một phải, một trái) thuộc A ∩ B ⇒ không xung khắc.', 2, TOP['ops'], 'Kreyszig PS 24.2, Prob. 14')
    B.mcq('Rút 2 con ốc vít. C: “cả 2 phải”, D: “cả 2 trái”. C và D có xung khắc không?', 'Có, xung khắc (không thể đồng thời)', ['Không xung khắc', 'Chỉ xung khắc nếu rút có hoàn lại', 'Không thể kết luận'],
          'C ∩ D = ∅: hai ốc không thể đều là phải và đều là trái.', 1, TOP['ops'], 'Kreyszig PS 24.2, Prob. 14')
    cnt('Liệt kê tất cả tập con của S = {a, b, c} (kể cả ∅ và S). Có bao nhiêu tập con?', 8, [6, 7, 9, 3], 'Mỗi phần tử có 2 lựa chọn (thuộc/không thuộc): 2³ = 8.', 1, TOP['space'], 'Kreyszig PS 24.2, Prob. 12')
    # De Morgan & luật
    for stem, tr, ex in [
        ('Luật De Morgan: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ.', True, 'Phần bù của hợp bằng giao các phần bù; đúng.'),
        ('Luật De Morgan: (A ∩ B)ᶜ = Aᶜ ∩ Bᶜ.', False, 'Sai: (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ.'),
        ('Với mọi biến cố A: (Aᶜ)ᶜ = A.', True, 'Phần bù của phần bù là chính nó.'),
        ('Với mọi A: A ∪ Aᶜ = S và A ∩ Aᶜ = ∅.', True, 'Định nghĩa biến cố đối lập.'),
        ('A ⊂ B khi và chỉ khi A ∪ B = B.', True, 'Nếu A ⊂ B thì hợp chính là B và ngược lại.'),
        ('A ⊂ B khi và chỉ khi A ∩ B = A.', True, 'Nếu A ⊂ B thì giao chính là A và ngược lại.'),
        ('Hai biến cố đối lập luôn xung khắc, nhưng hai biến cố xung khắc không nhất thiết đối lập.', True, 'Ví dụ: {1} và {2} khi gieo súc sắc xung khắc nhưng không đối lập.'),
        ('Luật phân phối: A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C).', True, 'Phân phối của giao đối với hợp (kiểm bằng biểu đồ Venn).'),
        ('Luật phân phối: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C).', True, 'Phân phối của hợp đối với giao.'),
        ('Sự kiện chắc chắn trùng với không gian mẫu S.', True, 'Biến cố chắc chắn luôn xảy ra ⇒ chính là S.')]:
        B.tf(stem, tr, ex, 1, TOP['ops'], 'Kreyszig PS 24.2, Prob. 16–20 / Lecture Notes §1.2.2')

    # ================= B. Quy tắc cộng, nhân; hoán vị, chỉnh hợp, tổ hợp =================
    cnt('Một công việc có thể làm bằng 1 trong 3 phương án với 4, 5 và 6 cách. Có bao nhiêu cách hoàn thành công việc?', 15, [120, 14, 16, 60], 'Quy tắc cộng: 4 + 5 + 6 = 15.', 1, TOP['rule'], 'Lecture Notes §1.3.1')
    cnt('Một công việc gồm 3 giai đoạn có 4, 5 và 6 cách. Có bao nhiêu cách hoàn thành?', 120, [15, 14, 30, 60], 'Quy tắc nhân: 4 × 5 × 6 = 120.', 1, TOP['rule'], 'Lecture Notes §1.3.2')
    B.mcq('Khi nào dùng quy tắc nhân thay vì quy tắc cộng?', 'Khi công việc chia thành các giai đoạn nối tiếp, mỗi giai đoạn đều phải thực hiện',
          ['Khi công việc có thể làm bằng một trong nhiều phương án loại trừ nhau', 'Khi mọi phương án có cùng số cách', 'Khi không quan tâm thứ tự'],
          'Quy tắc nhân ↔ “và” (các giai đoạn liên tiếp); quy tắc cộng ↔ “hoặc” (chọn một trong các phương án).', 1, TOP['rule'], 'Lecture Notes §1.3')
    cnt('Sắp xếp 5 người vào một băng ghế (Ví dụ 1.10). Số cách là', fac(5), [25, 24, 60, 720], 'Hoán vị của 5 phần tử: 5! = 120.', 1, TOP['perm'], 'Lecture Notes Ví dụ 1.10')
    n11 = fac(7) // (fac(2) * fac(3) * fac(2))
    assert n11 == len({p for p in itertools.permutations('1122233')})
    cnt('Từ các chữ số 1, 2, 3 lập số có 7 chữ số trong đó 1 xuất hiện hai lần, 2 xuất hiện ba lần, 3 xuất hiện hai lần (Ví dụ 1.11). Có bao nhiêu số?', n11, [201, 5040, 420, 105],
        f'7!/(2!·3!·2!) = 5040/24 = {n11}. (Giáo trình in “= 201” do lỗi đánh máy; đúng là {n11}.)', 2, TOP['perm'], 'Lecture Notes Ví dụ 1.11 (đã sửa lỗi in)')
    cnt('Tập {a, b, c}. Số “ký tự” gồm 2 phần tử, có thứ tự, mỗi phần tử chọn tối đa một lần (Ví dụ 1.12i) là', 6, [3, 9, 8, 12], 'A(3,2) = 3·2 = 6: ab, ba, ac, ca, bc, cb.', 1, TOP['perm'], 'Lecture Notes Ví dụ 1.12(i)')
    cnt('Tập {a, b, c}. Số “ký tự” gồm 2 phần tử, có thứ tự, mỗi phần tử có thể lặp lại (Ví dụ 1.12ii) là', 9, [6, 3, 8, 12], 'Chỉnh hợp lặp: 3² = 9.', 1, TOP['perm'], 'Lecture Notes Ví dụ 1.12(ii)')
    cnt('Lập một hội đồng 3 thành viên chọn từ 8 người (Ví dụ 1.13). Số cách là', comb(8, 3), [24, 336, 512, 28], 'Không phân biệt thứ tự: C(8,3) = 8!/(3!5!) = 56.', 1, TOP['comb'], 'Lecture Notes Ví dụ 1.13')
    five = [n for n in itertools.product(range(5), repeat=5) if n[0] != 0 and len(set(n)) == 5]
    cnt('Từ các chữ số 0, 1, 2, 3, 4 lập được bao nhiêu số có năm chữ số khác nhau? (Bài 1.7)', len(five), [120, 24, 625, 100],
        'Chữ số đầu ≠ 0: 4 cách; các vị trí còn lại: 4 · 3 · 2 · 1 ⇒ 4·4·3·2·1 = 96. (120 là số hoán vị 5! kể cả số bắt đầu bằng 0.)', 2, TOP['perm'], 'Lecture Notes Bài 1.7')
    cnt('Chọn hội đồng 3 kỹ sư, 2 nhà sinh học, 2 nhà hóa học từ 10 kỹ sư, 5 nhà sinh học, 6 nhà hóa học (Bài 1.8). Số cách là', comb(10, 3) * comb(5, 2) * comb(6, 2), [comb(21, 7), comb(10, 3) + comb(5, 2) + comb(6, 2), perm(10, 3) * perm(5, 2) * perm(6, 2), comb(10, 3) * comb(5, 2)],
        'Quy tắc nhân trên ba nhóm: C(10,3)·C(5,2)·C(6,2) = 120·10·15 = 18 000.', 2, TOP['mix'], 'Lecture Notes Bài 1.8 / Kreyszig PS 24.4, Prob. 5')
    cnt('Chuồng có 100 con chuột, 2 con đực. Có bao nhiêu cách chọn 12 con sao cho có đúng 2 con đực? (Bài 1.9)', comb(2, 2) * comb(98, 10), [comb(100, 12), comb(98, 12), comb(2, 2) * comb(98, 12)],
        'Chọn cả 2 con đực: C(2,2) = 1; chọn 10 con trong 98 con cái: C(98,10) ⇒ C(98,10) = ' + G(comb(98, 10)) + '.', 3, TOP['mix'], 'Lecture Notes Bài 1.9')
    cnt('Lô 50 sản phẩm có 5 phế phẩm. Có bao nhiêu cách chọn 10 sản phẩm trong đó có đúng 3 phế phẩm? (Bài 1.10)', comb(5, 3) * comb(45, 7), [comb(50, 10), comb(5, 3) * comb(45, 10), comb(5, 3) + comb(45, 7)],
        'C(5,3)·C(45,7) = 10 · ' + G(comb(45, 7)) + ' = ' + G(comb(5, 3) * comb(45, 7)) + '.', 3, TOP['mix'], 'Lecture Notes Bài 1.10')
    cnt('Lớp có 13 bạn nam và 17 bạn nữ. Có bao nhiêu cách chọn một nhóm gồm 2 bạn nam và 3 bạn nữ?', comb(13, 2) * comb(17, 3), [comb(30, 5), comb(13, 2) + comb(17, 3), perm(13, 2) * perm(17, 3), comb(13, 3) * comb(17, 2)],
        'C(13,2)·C(17,3) = 78 · 680 = 53 040.', 2, TOP['mix'], 'Đề giữa kỳ mẫu LTXSTK, câu 2')
    # Kreyszig PS 24.4
    cnt('Công ty phân công 10 tài xế cho 10 xe buýt, mỗi tài xế một xe và ngược lại. Số cách là', fac(10), [10 ** 10, comb(10, 5), 100, fac(9)], '10! = 3 628 800 (Prob. 1).', 1, TOP['perm'], 'Kreyszig PS 24.4, Prob. 1')
    L = 'aeiou'
    cnt('Với 5 chữ cái a, e, i, o, u lấy 2 chữ cái: số hoán vị (chỉnh hợp không lặp) là', perm(5, 2), [10, 15, 25, 5], 'A(5,2) = 5·4 = 20 (Prob. 2a).', 1, TOP['perm'], 'Kreyszig PS 24.4, Prob. 2(a)')
    cnt('Với 5 chữ cái a, e, i, o, u lấy 2 chữ cái: số tổ hợp không lặp là', comb(5, 2), [20, 15, 25, 5], 'C(5,2) = 10 (Prob. 2b).', 1, TOP['comb'], 'Kreyszig PS 24.4, Prob. 2(b)')
    cnt('Với 5 chữ cái a, e, i, o, u lấy 2 chữ cái: số tổ hợp CÓ lặp là', comb(5 + 2 - 1, 2), [10, 20, 25, 6], 'Tổ hợp lặp chập k của n: C(n + k − 1, k) = C(6,2) = 15 (Prob. 2c).', 2, TOP['comb'], 'Kreyszig PS 24.4, Prob. 2(c)')
    gas = 'Hộp có 4 gioăng cao su và 2 gioăng nhựa. Rút lần lượt không hoàn lại. '
    B.mcq(gas + 'Xác suất rút 2 gioăng nhựa trước rồi 4 gioăng cao su (Prob. 3a) là', '1/15', ['1/6', '1/2', '1/720'], 'P = (2/6)(1/5)(4/4)(3/3)(2/2)(1/1) = 2!4!/6! = 48/720 = 1/15.', 2, TOP['prob'], 'Kreyszig PS 24.4, Prob. 3(a)')
    B.mcq(gas + 'Xác suất rút 4 gioăng cao su trước rồi 2 gioăng nhựa (Prob. 3b) là', '1/15', ['1/6', '4/15', '1/30'], 'Cùng một thứ tự khối nên cũng bằng 4!2!/6! = 1/15.', 2, TOP['prob'], 'Kreyszig PS 24.4, Prob. 3(b)')
    B.mcq('Bình có 2 bi xanh lá, 3 bi vàng, 5 bi đỏ. Rút lần lượt không hoàn lại. Xác suất rút trước hết 2 bi xanh, rồi 3 bi vàng, cuối cùng các bi đỏ (Prob. 4) là', '1/2520', ['1/252', '1/10!', '1/120'],
          'Số hoán vị phân biệt của chuỗi màu: 10!/(2!3!5!) = 2520; chỉ một chuỗi ⇒ 1/2520.', 3, TOP['prob'], 'Kreyszig PS 24.4, Prob. 4')
    cnt('Có bao nhiêu mẫu khác nhau gồm 4 vật lấy từ lô 50 vật? (Prob. 6)', comb(50, 4), [perm(50, 4), 50 ** 4, comb(50, 3), fac(50) // fac(4)], 'C(50,4) = ' + G(comb(50, 4)) + '.', 1, TOP['comb'], 'Kreyszig PS 24.4, Prob. 6')
    cnt('Lô 10 vật có 2 vật hỏng. Số mẫu 4 vật khác nhau là', comb(10, 4), [perm(10, 4), 10 ** 4, 70, 120], 'C(10,4) = 210 (Prob. 7a).', 1, TOP['comb'], 'Kreyszig PS 24.4, Prob. 7(a)')
    cnt('Lô 10 vật có 2 vật hỏng. Số mẫu 4 vật không chứa vật hỏng là', comb(8, 4), [comb(10, 4), 56, 112, 28], 'C(8,4) = 70 (Prob. 7b).', 2, TOP['mix'], 'Kreyszig PS 24.4, Prob. 7(b)')
    cnt('Lô 10 vật có 2 vật hỏng. Số mẫu 4 vật chứa đúng 1 vật hỏng là', comb(2, 1) * comb(8, 3), [70, 28, 210, 56], 'C(2,1)·C(8,3) = 2·56 = 112 (Prob. 7c).', 2, TOP['mix'], 'Kreyszig PS 24.4, Prob. 7(c)')
    cnt('Lô 10 vật có 2 vật hỏng. Số mẫu 4 vật chứa cả 2 vật hỏng là', comb(2, 2) * comb(8, 2), [56, 112, 70, 14], 'C(2,2)·C(8,2) = 28 (Prob. 7d). Kiểm tra: 70 + 112 + 28 = 210 = C(10,4).', 2, TOP['mix'], 'Kreyszig PS 24.4, Prob. 7(d)')
    cnt('Số tay bài bridge khác nhau (13 lá chọn từ bộ 52 lá) là', comb(52, 13), [perm(52, 13), 52 ** 13 // 10 ** 6, comb(52, 4), fac(13)], 'C(52,13) = ' + G(comb(52, 13)) + ' (Prob. 8).', 2, TOP['comb'], 'Kreyszig PS 24.4, Prob. 8')
    cnt('Có bao nhiêu cách xếp 6 người ngồi quanh một bàn tròn? (Prob. 9)', fac(5), [720, 24, 360, 6], 'Hoán vị vòng: (n−1)! = 5! = 120 (cố định một người, hoán vị 5 người còn lại).', 2, TOP['perm'], 'Kreyszig PS 24.4, Prob. 9')
    p10 = comb(97, 7) / comb(100, 10)
    B.mcq('Chuồng 100 chuột có 3 con đực; chọn ngẫu nhiên 10 con. Xác suất cả 3 con đực nằm trong 10 con được chọn là (Prob. 10)', f(p10, 4), nd(p10, rng, 4, extra=[10 / 100 * 3, 0.1 ** 3, 3 / 100]),
          f'P = C(97,7)/C(100,10) = {f(p10,4)} (= (10·9·8)/(100·99·98)).', 3, TOP['prob'], 'Kreyszig PS 24.4, Prob. 10')
    cnt('Biển số “KDP7” rồi hai chữ số cuối quên, nhưng chắc cả ba chữ số đều khác nhau. Có bao nhiêu biển số cần kiểm tra? (Prob. 11)', 9 * 8, [90, 100, 81, 72 + 1], 'Chữ số 7 đã biết; hai chữ số còn lại khác 7 và khác nhau: 9 × 8 = 72.', 2, TOP['perm'], 'Kreyszig PS 24.4, Prob. 11')
    B.mcq('3 nghi phạm và 6 người vô tội đứng thành hàng; nhân chứng chọn ngẫu nhiên 3 người. Xác suất chọn đúng 3 nghi phạm là (Prob. 12)', '1/84', ['1/9', '1/27', '1/20'], 'C(3,3)/C(9,3) = 1/84.', 2, TOP['prob'], 'Kreyszig PS 24.4, Prob. 12')
    B.mcq('Với nhóm trên, xác suất nhân chứng chọn 3 người đều vô tội là', '5/21', ['2/3', '1/84', '20/9'], 'C(6,3)/C(9,3) = 20/84 = 5/21.', 2, TOP['prob'], 'Kreyszig PS 24.4, Prob. 12')
    pb = 1 - math.prod((365 - i) / 365 for i in range(20))
    B.mcq('Nhóm 20 người (không có sinh đôi): xác suất có ít nhất hai người cùng ngày sinh (bài toán ngày sinh, Prob. 15) xấp xỉ', f(pb, 4), nd(pb, rng, 4, extra=[20 / 365, 1 - 1 / 365, 0.5]),
          f'Dùng biến cố bù: P = 1 − (365·364·…·346)/365²⁰ = {f(pb,4)} ≈ 41%. Kết quả gây ngạc nhiên vì lớn hơn nhiều so với trực giác.', 3, TOP['prob'], 'Kreyszig PS 24.4, Prob. 15')
    stir = lambda n: math.sqrt(2 * math.pi * n) * (n / math.e) ** n
    err10 = abs(stir(10) - fac(10)) / fac(10)
    B.mcq('Công thức Stirling: n! ≈ √(2πn)(n/e)ⁿ. Với n = 10, sai số tương đối so với 10! = 3 628 800 xấp xỉ', f(err10 * 100, 2) + '%', [f(err10 * 100 * 10, 2) + '%', f(err10 * 100 / 10, 2) + '%', '8.3%'],
          f'√(20π)(10/e)¹⁰ ≈ {stir(10):,.0f}; |sai số|/10! ≈ {err10*100:.2f}% (sai số giảm khi n tăng, ≈ 1/(12n)).', 3, TOP['theory'], 'Kreyszig PS 24.4, Prob. 13 / Lecture Notes Nhận xét 1.2(iii)')
    # Lý thuyết
    B.mcq('Theo quy ước, 0! bằng bao nhiêu?', '1', ['0', 'Không xác định', '−1'], 'Quy ước 0! = 1 (Nhận xét 1.2(i)), cho phép C(n,0) = C(n,n) = 1.', 1, TOP['theory'], 'Lecture Notes Nhận xét 1.2(i)')
    B.mcq('Công thức nào biểu thị số chỉnh hợp (không lặp) chập k của n phần tử?', 'A(n,k) = n!/(n − k)!', ['C(n,k) = n!/(k!(n − k)!)', 'nᵏ', 'n!/k!'], 'Chỉnh hợp có thứ tự: n(n−1)…(n−k+1) = n!/(n−k)!. C là tổ hợp (không thứ tự); nᵏ là chỉnh hợp lặp.', 1, TOP['theory'], 'Lecture Notes §1.3.4')
    B.mcq('Quan hệ giữa tổ hợp và chỉnh hợp là:', 'C(n,k) = A(n,k)/k!', ['C(n,k) = A(n,k)·k!', 'C(n,k) = A(n,k)', 'C(n,k) = A(n,k)/n!'], 'Mỗi tổ hợp k phần tử có k! cách sắp thứ tự (thành k! chỉnh hợp) ⇒ A = k!·C.', 1, TOP['theory'], 'Lecture Notes (1.9)')
    B.mcq('Hoán vị của n phần tử chia thành c lớp giống nhau (n₁ + … + n_c = n) có số cách là:', 'n!/(n₁!·n₂!·…·n_c!)', ['n!·n₁!·…·n_c!', 'n!/(n₁ + … + n_c)', 'C(n, c)'], 'Chia cho các hoán vị trong từng lớp giống nhau (Kreyszig Thm 1b).', 2, TOP['theory'], 'Lecture Notes §1.3.3 / Kreyszig Thm 1(b)')
    B.mcq('Số tổ hợp chập k có lặp từ n loại đối tượng là:', 'C(n + k − 1, k)', ['C(n, k)', 'nᵏ', 'n!/(n − k)!'], 'Tổ hợp có lặp (Kreyszig Thm 2): C(n + k − 1, k).', 2, TOP['theory'], 'Kreyszig §24.4, Theorem 2')
    B.mcq('Đẳng thức nào đúng với mọi 0 ≤ k ≤ n?', 'C(n,k) = C(n, n − k)', ['C(n,k) = C(n, k + 1)', 'C(n,k) = n·C(n − 1, k)', 'C(n,k) = k!·C(n, n − k)'], 'Chọn k phần tử để lấy tương ứng chọn n−k phần tử để bỏ.', 1, TOP['theory'], 'Kreyszig §24.4 (11)–(14)')
    B.mcq('Đẳng thức Pascal: C(n + 1, k) bằng', 'C(n, k) + C(n, k − 1)', ['C(n, k)·C(n, k − 1)', '2·C(n, k)', 'C(n, k) − C(n, k − 1)'], 'Chia các tổ hợp của n+1 phần tử theo việc có chọn phần tử cuối hay không.', 2, TOP['theory'], 'Kreyszig PS 24.4, Prob. 14 (liên hệ định lý nhị thức)')
    B.mcq('Theo định lý nhị thức, hệ số của aᵏbⁿ⁻ᵏ trong khai triển (a + b)ⁿ là:', 'C(n,k)', ['A(n,k)', 'n!/k!', 'nᵏ'], 'Chọn k trong n thừa số để lấy a ⇒ C(n,k) (Prob. 14d).', 2, TOP['theory'], 'Kreyszig PS 24.4, Prob. 14(d)')
    B.essay('Liệt kê không gian mẫu và các biến cố: gieo hai con súc sắc (Bài 1.4–1.5): (a) hai mặt bằng nhau; (b) tổng > 9; (c) tổng = 7.',
            f'|S| = 36. (a) {sorted(ev_a)}; (b) {sorted(ev_b)}; (c) {sorted(ev_c)}.', 1, TOP['space'], 'Lecture Notes Bài 1.4–1.5')
    B.essay('Bài 1.6: xác định không gian mẫu khi tung một đồng xu cho đến khi xuất hiện mặt ngửa.', 'S = {N, SN, SSN, SSSN, …}; hoặc S = {1, 2, 3, …} với k là số lần tung. S vô hạn đếm được.', 1, TOP['space'], 'Lecture Notes Bài 1.6')
    B.essay('Bài 1.7–1.10 (tổng hợp): (i) số có 5 chữ số khác nhau từ {0,1,2,3,4}; (ii) hội đồng 3 kỹ sư, 2 sinh học, 2 hóa học; (iii) 12 chuột có 2 đực; (iv) 10 sản phẩm có 3 phế phẩm.',
            f'(i) 4·4·3·2·1 = 96. (ii) C(10,3)C(5,2)C(6,2) = 18 000. (iii) C(98,10) = {G(comb(98,10))}. (iv) C(5,3)C(45,7) = {G(comb(5,3)*comb(45,7))}.', 2, TOP['mix'], 'Lecture Notes Bài 1.7–1.10')
    B.essay('Kreyszig PS 24.4, Prob. 7: lô 10 vật, 2 hỏng. Đếm số mẫu 4 vật: tổng, 0 hỏng, 1 hỏng, 2 hỏng; kiểm tra tổng.', 'C(10,4) = 210; C(8,4) = 70; C(2,1)C(8,3) = 112; C(2,2)C(8,2) = 28; 70 + 112 + 28 = 210 ✓.', 2, TOP['mix'], 'Kreyszig PS 24.4, Prob. 7')
    B.essay('Bài toán ngày sinh (Kreyszig PS 24.4, Prob. 15): xác suất trong 20 người có ít nhất hai người trùng ngày sinh.', f'Biến cố bù: mọi người khác ngày sinh: 365·364·…·346/365²⁰ ≈ {1-pb:.4f} ⇒ P ≈ {pb:.4f}.', 3, TOP['prob'], 'Kreyszig PS 24.4, Prob. 15')
    # ---- Tự luận Kreyszig PS 24.2 (vẽ/liệt kê không gian mẫu) ----
    SP = 'Kreyszig PS 24.2'
    B.essay('Liệt kê không gian mẫu: rút 3 ốc vít từ lô ốc xoắn phải (R) và trái (L); sau đó tìm số điểm mẫu và biến cố “có ít nhất 1 ốc xoắn phải”.',
            'S = {RRR, RRL, RLR, RLL, LRR, LRL, LLR, LLL}, |S| = 8. “Ít nhất 1 phải” = S \\ {LLL} ⇒ 7 điểm mẫu.', 1, TOP['space'], SP + ', Prob. 1')
    B.essay('Tung 2 đồng xu: liệt kê không gian mẫu và biến cố “hai mặt giống nhau”.', 'S = {SS, SN, NS, NN}; “giống nhau” = {SS, NN}.', 1, TOP['space'], SP + ', Prob. 2')
    B.essay('Chọn ủy ban 2 người từ nhóm 5 người {1,2,3,4,5}: liệt kê không gian mẫu.', 'S = {12, 13, 14, 15, 23, 24, 25, 34, 35, 45}, |S| = C(5,2) = 10.', 1, TOP['space'], SP + ', Prob. 8')
    B.essay('Gieo 3 súc sắc: tìm số kết cục có tổng chia hết cho 3 và số kết cục có tổng chia hết cho 5; chứng tỏ hai biến cố không xung khắc.',
            f'|S| = 216; tổng chia hết cho 3: {len(a3)} kết cục; chia hết cho 5: {len(b3)} kết cục; chia hết cho 15 (tổng = 15): {len(both3)} kết cục ⇒ giao khác rỗng nên không xung khắc.', 2, TOP['ops'], SP + ', Prob. 10')
    B.essay('Hai súc sắc: liệt kê A = “hai mặt bằng nhau”, B = “tổng < 5”, rồi tìm A ∩ B, A ∪ B, Aᶜ, Bᶜ.',
            f'A = {sorted(eq)}; B = {sorted(lt5)}; A ∩ B = {sorted(eq & lt5)}; |A ∪ B| = {len(eq | lt5)}; |Aᶜ| = 30; |Bᶜ| = 30.', 2, TOP['ops'], SP + ', Prob. 13')
    B.essay('Chứng minh luật De Morgan (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ.', 'x ∈ (A ∪ B)ᶜ ⇔ x ∉ A và x ∉ B ⇔ x ∈ Aᶜ ∩ Bᶜ. (Vẽ Venn: vùng ngoài cả hai hình tròn.)', 2, TOP['ops'], SP + ', Prob. 19')
    B.essay('Chứng minh nếu A ⊂ B thì A ∪ B = B (Kreyszig Prob. 17).', 'Nếu A ⊂ B: mọi điểm của A đều thuộc B nên A ∪ B ⊂ B; ngược lại B ⊂ A ∪ B ⇒ A ∪ B = B. Chiều đảo: nếu A ∪ B = B thì A ⊂ A ∪ B = B.', 2, TOP['ops'], SP + ', Prob. 17')
    B.essay('Tìm số cách xếp 6 người quanh một bàn tròn và giải thích vì sao không phải 6!.', '(6−1)! = 120. Mỗi cách xếp quanh bàn tròn tương ứng 6 phép xoay như nhau nên 6!/6 = 120.', 2, TOP['perm'], 'Kreyszig PS 24.4, Prob. 9')
