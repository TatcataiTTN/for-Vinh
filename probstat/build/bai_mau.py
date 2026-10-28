"""Trang 'Ba bài mẫu tự luận khó' (deck): chép vào vở, tự làm, đối chiếu từng bước, tập chữa.
Mọi con số tính bằng Fraction / sympy và kiểm bằng assert."""
import math
from fractions import Fraction as Fr
import sympy as sp
from hx import *
from sitelib import page, write

def fk(x, d=4): return f'{float(x):.{d}f}'.replace('.', '{,}')
def fl(x, d=4): return f'{float(x):.{d}f}'.replace('.', ',')
K1, K2, K3 = 'BÀI MẪU 1 · Thống kê mô tả + đếm', 'BÀI MẪU 2 · Bayes (mục 1.6)', 'BÀI MẪU 3 · Biến ngẫu nhiên (1.7–1.9)'

def mistakes(items): return callout('warn', 'Lỗi hay gặp (rút từ bài làm lần 1)', ul(items))
def selfcheck(items): return callout('good', 'Tập chữa: tự chấm bằng bút khác màu', ul(items))
def blank(txt='Tự làm trước, 10–15 phút, che phần lời giải rồi mới lật sang slide sau.'):
    return f'<p class="lead">✍️ {txt}</p>'

def grouped(cls, f):
    mids = [Fr(a + b, 2) for a, b in cls]; n = sum(f)
    xb = sum(mm * k for mm, k in zip(mids, f)) / n
    sxx = sum(k * mm * mm for mm, k in zip(mids, f)) - n * xb * xb
    return mids, n, xb, sxx / (n - 1)

def slides():
    S = []   # (html, is_divider)
    # ───────────── Mở đầu
    S.append((sl(callout('info', 'Cách học với bộ bài mẫu này', ul([
        '<b>Chép đề</b> vào vở (viết tay, có đủ số liệu).',
        '<b>Che lời giải</b>, tự làm 10–15 phút. Làm không ra thì viết công thức bạn biết để lấy điểm từng phần.',
        '<b>Lật từng bước</b> để đối chiếu; sửa bằng bút khác màu, không tẩy.',
        '<b>Làm lại bản sạch</b> sau 1 ngày, rồi làm “bài tương tự” cuối mỗi bài.'], True))
        + callout('good', 'Khung trình bày mọi câu', ul([
            'Đặt tên biến cố/biến: <i>A: …, X: …</i>',
            'Viết công thức tổng quát',
            'Thay số (dấu × viết rõ, khác dấu +)',
            'Kết quả: giữ 4 chữ số thập phân, chỉ làm tròn ở cuối',
            'Dòng <b>Đáp số</b> hoặc kết luận bằng lời'], True)),
        'BỘ BÀI MẪU TỰ LUẬN', 'Ba bài khó, học từng bước'), False))
    S.append((sl(table(['Bài', 'Nội dung', 'Vì sao khó', 'Mục'], [
        ['1', 'Số liệu ghép lớp: x̄, s², trung vị, xác suất chọn mẫu', 'Nhiều phép tính, dễ sai số học và quên s²', '1.1–1.4'],
        ['2', 'Hai bộ lọc thư rác: toàn phần, Bayes, cập nhật liên tiếp, độc lập', 'Phải chọn đúng hệ đầy đủ và điều kiện', '1.5–1.6'],
        ['3', 'Mật độ từng khúc: c, F(x), P, E, Var, Y = 2X + 3', 'Tích phân hai đoạn, phân biệt E(X²) với [E(X)]²', '1.7–1.9']]),
        'BỘ BÀI MẪU TỰ LUẬN', 'Ba bài này nhắm vào các lỗi của bài làm lần 1'), False))

    # ───────────── BÀI 1
    cls = [(0, 4), (4, 8), (8, 12), (12, 16), (16, 20)]; f = [6, 14, 18, 9, 3]
    mids, n, xb, s2 = grouped(cls, f); s = math.sqrt(s2)
    sxf = sum(mm * k for mm, k in zip(mids, f)); sxf2 = sum(k * mm * mm for mm, k in zip(mids, f))
    assert (n, xb, sxf, sxf2) == (50, Fr(456, 50), 456, 5064)
    cum = [sum(f[:i + 1]) for i in range(5)]; assert cum == [6, 20, 38, 47, 50]
    med = 8 + Fr(25 - 20, 18) * 4
    over12 = 9 + 3; p2 = Fr(math.comb(over12, 2), math.comb(50, 2)); p1 = Fr(over12 * (50 - over12), math.comb(50, 2))
    assert p2 == Fr(66, 1225) and p1 == Fr(456, 1225)
    S.append((divider(1, 3, 'Bài mẫu 1: số liệu ghép lớp và xác suất chọn mẫu', ['Chép đề', 'x̄, s², s', 'Tần suất, tích lũy, trung vị', 'Chọn 2 đơn không hoàn lại', 'Tập chữa']), True))
    de1 = '''Thời gian xử lý (giờ) của 50 đơn hàng: 0–4: 6; 4–8: 14; 8–12: 18; 12–16: 9; 16–20: 3.
(a) (2đ) Tính trung bình mẫu x̄, phương sai mẫu s², độ lệch chuẩn s.
(b) (2đ) Lập bảng tần suất và tần suất tích lũy; tính trung vị ghép lớp.
(c) (2đ) Chọn ngẫu nhiên đồng thời 2 đơn. Tính xác suất cả hai đơn xử lý quá 12 giờ, và xác suất có đúng 1 đơn quá 12 giờ.'''
    S.append((sl('<pre>' + de1 + '</pre>' + blank(), K1, 'Chép đề vào vở'), False))
    S.append((sl(table(['Từ khóa trong đề', 'Nghĩa là', 'Công thức cần'], [
        ['“ghép lớp”, “trung bình mẫu”', 'Dùng trung điểm lớp thay cho giá trị', m('\\bar x=\\tfrac1n\\sum f_i m_i')],
        ['“phương sai mẫu”', 'Chia cho n−1 (không phải n)', m('s^2=\\tfrac{\\sum f_i m_i^2-n\\bar x^2}{n-1}')],
        ['“trung vị ghép lớp”', 'Tìm lớp chứa phần tử thứ n/2', m('L+\\tfrac{n/2-F}{f}\\,h')],
        ['“đồng thời 2 đơn”', 'Tổ hợp, không có thứ tự', m('\\tfrac{C_{12}^2}{C_{50}^2}')]]),
        K1, 'Đọc đề: từ khóa → công thức'), False))
    rows = [[f'{a}–{b}', str(k), fl(mm, 0), fl(k * mm, 0), fl(k * mm * mm, 0)] for (a, b), k, mm in zip(cls, f, mids)]
    rows.append(['Tổng', str(n), '', str(sxf), str(sxf2)])
    S.append((sl(table(['Lớp', 'Tần số f', 'Trung điểm m', 'f·m', 'f·m²'], rows)
                 + steps([m(f'\\bar x=\\tfrac{{{sxf}}}{{50}}={fl(xb,2)}'),
                          m(f's^2=\\tfrac{{{sxf2}-50\\cdot{fk(xb,2)}^2}}{{49}}=\\tfrac{{{sxf2}-{fk(n*xb*xb,2)}}}{{49}}={fk(s2,4)}'),
                          m(f's=\\sqrt{{{fk(s2,4)}}}={fk(s,4)}'),
                          '<b>Đáp số (a):</b> x̄ = ' + fl(xb, 2) + '; s² ≈ ' + fl(s2, 3) + '; s ≈ ' + fl(s, 3) + ' (giờ).']),
                 K1, 'Câu (a): lập bảng rồi tính'), False))
    S.append((sl(table(['Lớp', 'f', 'Tần suất f/n', 'Tích lũy F', 'Tần suất tích lũy'],
                       [[f'{a}–{b}', str(k), fl(Fr(k, 50), 2), str(c), fl(Fr(c, 50), 2)] for (a, b), k, c in zip(cls, f, cum)])
                 + steps(['n/2 = 25. Tích lũy lên tới 20 ở lớp 4–8 và 38 ở lớp 8–12 ⇒ <b>lớp chứa trung vị là 8–12</b> (F trước đó = 20, f = 18, h = 4).',
                          m(f'\\mathrm{{Me}}=8+\\tfrac{{25-20}}{{18}}\\cdot4={fl(med,3)}'),
                          '<b>Đáp số (b):</b> Me ≈ ' + fl(med, 3) + ' giờ; trung vị nhỏ hơn trung bình ' + fl(xb, 2) + ' ⇒ phân bố lệch phải (đuôi dài về phía đơn xử lý lâu).']),
                 K1, 'Câu (b): tần suất, tích lũy, trung vị'), False))
    S.append((sl(steps(['Số đơn quá 12 giờ: 9 + 3 = 12; không quá 12 giờ: 38.',
                        'Không gian mẫu: ' + m('C_{50}^2=1225') + '. Hai đơn đều quá 12 giờ: ' + m('C_{12}^2=66') + '.',
                        m(f'P(\\text{{cả hai}})=\\tfrac{{66}}{{1225}}={fl(p2,4)}'),
                        'Đúng 1 đơn: chọn 1 trong 12 và 1 trong 38: ' + m('12\\cdot38=456') + '.',
                        m(f'P(\\text{{đúng 1}})=\\tfrac{{456}}{{1225}}={fl(p1,4)}'),
                        '<b>Đáp số (c):</b> ' + fl(p2, 4) + ' và ' + fl(p1, 4) + '.'])
                 + callout('warn', 'Kiểm tra nhanh', '<p>Ba trường hợp 0, 1, 2 đơn quá 12 giờ phải có tổng bằng 1: ' + m(f'\\tfrac{{703+456+66}}{{1225}}=1') + ' (703 = C(38,2)).</p>'),
                 K1, 'Câu (c): xác suất chọn đồng thời'), False))
    assert math.comb(38, 2) == 703 and 703 + 456 + 66 == 1225
    # tương tự 1
    cls2 = [(0, 10), (10, 20), (20, 30), (30, 40)]; f2 = [4, 12, 16, 8]
    _, n2, xb2, s22 = grouped(cls2, f2); c2 = [4, 16, 32, 40]
    med2 = 20 + Fr(20 - 16, 16) * 10; q2 = Fr(math.comb(8, 2), math.comb(40, 2))
    S.append((sl(mistakes(['Chia cho n thay vì n−1 khi tính s².', 'Quên tính s² (chỉ làm x̄), bỏ ý (b), (c).', 'Làm tròn x̄ rồi mới bình phương làm s² lệch.', 'Viết 12 × 38 thành 12 + 38.'])
                 + selfcheck(['Có bảng f, m, f·m, f·m² không?', 'Có ghi lớp chứa trung vị và lý do (F trước, f, h) không?', 'Cuối mỗi câu có dòng Đáp số không?'])
                 + '<details><summary><b>Bài tương tự để tự làm</b> (bấm xem đáp số sau khi làm)</summary><p>Thời gian chờ (phút) của 40 người: 0–10: 4; 10–20: 12; 20–30: 16; 30–40: 8. Tính x̄, s², trung vị ghép lớp; chọn đồng thời 2 người, xác suất cả hai chờ từ 30 phút trở lên.</p>'
                 + f'<p><b>Đáp số:</b> x̄ = {fl(xb2,2)}; s² = {fl(s22,3)}; Me = {fl(med2,2)}; P = C(8,2)/C(40,2) = 28/780 = {fl(q2,4)}.</p></details>', K1, 'Tập chữa và bài tương tự'), False))

    # ───────────── BÀI 2
    pS, a1, b1, a2, b2 = Fr(3, 10), Fr(9, 10), Fr(5, 100), Fr(8, 10), Fr(1, 10)
    PF1 = pS * a1 + (1 - pS) * b1; PS_F1 = pS * a1 / PF1
    PBoth = pS * a1 * a2 + (1 - pS) * b1 * b2; PS_both = pS * a1 * a2 / PBoth
    PF2 = pS * a2 + (1 - pS) * b2
    PNo = pS * a1 * (1 - a2) + (1 - pS) * b1 * (1 - b2); PS_no = pS * a1 * (1 - a2) / PNo
    assert (PF1, PBoth, PF2) == (Fr(305, 1000), Fr(2195, 10000), Fr(31, 100)) and PBoth != PF1 * PF2
    odds = pS / (1 - pS) * (a1 / b1) * (a2 / b2); assert odds / (1 + odds) == PS_both
    S.append((divider(2, 3, 'Bài mẫu 2: hai bộ lọc thư rác', ['Chép đề', 'Sơ đồ cây, hệ đầy đủ', 'Xác suất toàn phần', 'Bayes một và hai bộ lọc', 'Độc lập hay không', 'Tập chữa']), True))
    de2 = '''Trong hộp thư, 30% email là thư rác (S). Bộ lọc 1 gắn cờ “rác” cho 90% thư rác và nhầm cho 5% thư thường. Bộ lọc 2 gắn cờ cho 80% thư rác và nhầm cho 10% thư thường. Biết loại thư, hai bộ lọc hoạt động độc lập với nhau.
(a) (0,5đ) Đặt tên biến cố và vẽ sơ đồ cây.
(b) (0,5đ) Tính xác suất bộ lọc 1 gắn cờ một email ngẫu nhiên.
(c) (0,5đ) Biết bộ lọc 1 gắn cờ, tính xác suất email là thư rác.
(d) (0,75đ) Biết cả hai bộ lọc đều gắn cờ, tính xác suất thư rác.
(e) (0,25đ) Biết bộ lọc 1 gắn cờ nhưng bộ lọc 2 không gắn cờ, tính xác suất thư rác.
(f) (0,5đ) Hai biến cố “bộ lọc 1 gắn cờ” và “bộ lọc 2 gắn cờ” có độc lập không? Giải thích.'''
    S.append((sl('<pre>' + de2 + '</pre>' + blank(), K2, 'Chép đề vào vở'), False))
    S.append((sl(table(['Biến cố', 'Ý nghĩa', 'Xác suất'], [
        [m('S'), 'email là thư rác', '0,3'], [m('\\bar S'), 'thư thường', '0,7'],
        [m('F_1|S'), 'lọc 1 gắn cờ khi là thư rác', '0,9'], [m('F_1|\\bar S'), 'lọc 1 gắn cờ nhầm', '0,05'],
        [m('F_2|S'), 'lọc 2 gắn cờ khi là thư rác', '0,8'], [m('F_2|\\bar S'), 'lọc 2 gắn cờ nhầm', '0,1']])
        + callout('info', 'Hệ đầy đủ', '<p>' + m('\\{S,\\bar S\\}') + ' là hệ đầy đủ (hai biến cố xung khắc, hợp là toàn bộ). Mọi xác suất toàn phần đều chia theo hệ này. “Độc lập biết loại thư” nghĩa là ' + m('P(F_1F_2|S)=P(F_1|S)P(F_2|S)') + ' và tương tự với ' + m('\\bar S') + '.</p>'),
        K2, 'Câu (a): đặt tên và sơ đồ cây'), False))
    S.append((sl(steps([m('P(F_1)=P(S)P(F_1|S)+P(\\bar S)P(F_1|\\bar S)'), m(f'=0{{,}}3\\times0{{,}}9+0{{,}}7\\times0{{,}}05=0{{,}}27+0{{,}}035={fl(PF1,3)}'),
                        '<b>Đáp số (b):</b> ' + fl(PF1, 3) + '.', '',
                        m('P(S|F_1)=\\tfrac{P(S)P(F_1|S)}{P(F_1)}=\\tfrac{0{,}27}{0{,}305}=' + fl(PS_F1, 4)),
                        '<b>Đáp số (c):</b> ' + fl(PS_F1, 4) + ' (≈ ' + fl(PS_F1 * 100, 2) + '%).']).replace('<li></li>', ''),
                 K2, 'Câu (b), (c): toàn phần rồi Bayes'), False))
    S.append((sl(steps(['Vì hai bộ lọc độc lập khi biết loại thư: ' + m('P(F_1F_2|S)=0{,}9\\times0{,}8=0{,}72'), m('P(F_1F_2|\\bar S)=0{,}05\\times0{,}1=0{,}005'),
                        m(f'P(F_1F_2)=0{{,}}3\\times0{{,}}72+0{{,}}7\\times0{{,}}005=0{{,}}216+0{{,}}0035={fl(PBoth,4)}'),
                        m(f'P(S|F_1F_2)=\\tfrac{{0{{,}}216}}{{{fl(PBoth,4)}}}={fl(PS_both,4)}'),
                        '<b>Đáp số (d):</b> ' + fl(PS_both, 4) + '.',
                        'Câu (e): lọc 2 KHÔNG gắn cờ nên dùng phần bù: ' + m('P(F_1\\bar F_2|S)=0{,}9\\times0{,}2=0{,}18') + '; ' + m('P(F_1\\bar F_2|\\bar S)=0{,}05\\times0{,}9=0{,}045'),
                        m(f'P(S|F_1\\bar F_2)=\\tfrac{{0{{,}}3\\times0{{,}}18}}{{0{{,}}3\\times0{{,}}18+0{{,}}7\\times0{{,}}045}}=\\tfrac{{0{{,}}054}}{{{fl(PNo,4)}}}={fl(PS_no,4)}'),
                        '<b>Đáp số (e):</b> ' + fl(PS_no, 4) + '.'])
                 + callout('good', 'Kiểm tra bằng dạng odds', '<p>Odds tiên nghiệm ' + m('\\tfrac{3}{7}') + ' nhân LR₁ = 0,9/0,05 = 18 và LR₂ = 0,8/0,1 = 8 cho ' + m(f'\\tfrac37\\cdot144={fl(odds,3)}') + '; xác suất ' + m(f'\\tfrac{{{fl(odds,3)}}}{{1+{fl(odds,3)}}}={fl(PS_both,4)}') + '. Trùng kết quả (d).</p>'),
                 K2, 'Câu (d), (e): hai bộ lọc'), False))
    S.append((sl(steps([m(f'P(F_2)=0{{,}}3\\times0{{,}}8+0{{,}}7\\times0{{,}}1={fl(PF2,2)}'), m(f'P(F_1)P(F_2)={fl(PF1,3)}\\times{fl(PF2,2)}={fl(PF1*PF2,5)}'),
                        m(f'P(F_1F_2)={fl(PBoth,4)}\\neq{fl(PF1*PF2,5)}'),
                        '<b>Kết luận (f):</b> <b>không độc lập</b>. Hai bộ lọc chỉ độc lập khi đã biết loại thư; không biết loại thì cả hai cùng “nghiêng” theo việc thư có phải rác hay không, nên có tương quan.'])
                 + callout('warn', 'Bẫy', '<p>Không được nhân thẳng P(F₁)·P(F₂) để ra P(F₁F₂). Phải điều kiện hóa theo hệ đầy đủ rồi mới cộng.</p>'),
                 K2, 'Câu (f): độc lập có điều kiện khác độc lập'), False))
    t = dict(pS=Fr(2, 10), a1=Fr(85, 100), b1=Fr(4, 100), a2=Fr(7, 10), b2=Fr(8, 100))
    pb = t['pS'] * t['a1'] * t['a2'] + (1 - t['pS']) * t['b1'] * t['b2']; pst = t['pS'] * t['a1'] * t['a2'] / pb
    S.append((sl(mistakes(['Chia cho P(S) thay vì cho P(F₁): nhầm P(F₁|S) với P(S|F₁).', 'Dùng P(F₁)·P(F₂) làm mẫu số khi cả hai cùng gắn cờ.', 'Quên phần bù khi lọc 2 không gắn cờ (dùng 0,8 thay vì 0,2).', 'Không kiểm tra tổng các xác suất hậu nghiệm bằng 1.'])
                 + selfcheck(['Có hệ đầy đủ và sơ đồ cây không?', 'Mẫu số là xác suất toàn phần, có viết đủ hai nhánh không?', 'Có kết luận bằng lời cho câu (f) không?'])
                 + '<details><summary><b>Bài tương tự để tự làm</b></summary><p>20% email là thư rác. Lọc 1 gắn cờ 85% thư rác, nhầm 4% thư thường; lọc 2 gắn cờ 70% thư rác, nhầm 8% thư thường; độc lập khi biết loại thư. Tính xác suất thư rác biết cả hai lọc cùng gắn cờ.</p>'
                 + f'<p><b>Đáp số:</b> tử = 0,2·0,85·0,7 = {fl(t["pS"]*t["a1"]*t["a2"],4)}; mẫu = {fl(pb,5)}; P = {fl(pst,4)}.</p></details>', K2, 'Tập chữa và bài tương tự'), False))

    # ───────────── BÀI 3
    x, c = sp.symbols('x c')
    fx1, fx2 = x, 2 - x
    area = sp.integrate(c * fx1, (x, 0, 1)) + sp.integrate(c * fx2, (x, 1, 2)); cv = sp.solve(area - 1, c)[0]; assert cv == 1
    F1 = sp.integrate(x, (x, 0, x)); F2 = 1 - sp.integrate(2 - x, (x, x, 2)); assert sp.simplify(F1.subs(x, 1) - F2.subs(x, 1)) == 0
    Fp = lambda v: F1.subs(x, v) if v <= 1 else F2.subs(x, v)
    pab = Fp(sp.Rational(3, 2)) - Fp(sp.Rational(1, 2)); assert pab == sp.Rational(3, 4)
    EX = sp.integrate(x * x, (x, 0, 1)) + sp.integrate(x * (2 - x), (x, 1, 2)); EX2 = sp.integrate(x**3, (x, 0, 1)) + sp.integrate(x**2 * (2 - x), (x, 1, 2))
    VX = EX2 - EX**2; assert (EX, EX2, VX) == (1, sp.Rational(7, 6), sp.Rational(1, 6))
    S.append((divider(3, 3, 'Bài mẫu 3: hàm mật độ từng khúc', ['Chép đề', 'Tìm c bằng diện tích', 'Hàm phân phối từng khúc', 'P, E, Var', 'Biến đổi Y = 2X + 3', 'Tập chữa']), True))
    de3 = '''Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = c·x với 0 ≤ x ≤ 1; f(x) = c·(2 − x) với 1 < x ≤ 2; f(x) = 0 nếu x ngoài [0; 2].
(a) (0,5đ) Tìm c.
(b) (0,75đ) Tìm hàm phân phối F(x) trên từng khoảng.
(c) (0,5đ) Tính P(0,5 < X < 1,5).
(d) (0,75đ) Tính E(X) và Var(X).
(e) (0,5đ) Đặt Y = 2X + 3. Tính E(Y), Var(Y) và P(Y > 4).'''
    S.append((sl('<pre>' + de3 + '</pre>' + blank(), K3, 'Chép đề vào vở'), False))
    S.append((sl(callout('info', 'Ý tưởng', '<p>Đồ thị f(x) là một <b>tam giác</b> đáy [0; 2], đỉnh tại (1; c). Tổng diện tích phải bằng 1 ⇒ tìm c. Với hàm từng khúc luôn <b>tách tích phân theo từng khoảng</b>.</p>')
                 + steps([m('\\int_0^2 f=\\int_0^1 cx\\,dx+\\int_1^2 c(2-x)\\,dx=\\tfrac c2+\\tfrac c2=c'), m('c=1'),
                          'Kiểm tra bằng hình học: tam giác đáy 2, cao 1 có diện tích ' + m('\\tfrac12\\cdot2\\cdot1=1') + '.', '<b>Đáp số (a):</b> c = 1.']),
                 K3, 'Câu (a): tìm c'), False))
    S.append((sl(steps([m('0\\le x\\le1:\\ F(x)=\\int_0^x t\\,dt=\\tfrac{x^2}{2}'), m('F(1)=\\tfrac12'),
                        m('1<x\\le2:\\ F(x)=\\tfrac12+\\int_1^x(2-t)\\,dt=1-\\tfrac{(2-x)^2}{2}'),
                        'Kiểm tra: F(2) = 1 và hai công thức khớp nhau tại x = 1 (cùng bằng 1/2).',
                        '<b>Đáp số (b):</b> F(x) = 0 (x<0); x²/2 (0≤x≤1); 1 − (2−x)²/2 (1<x≤2); 1 (x>2).'])
                 + callout('warn', 'Bẫy', '<p>Ở khoảng thứ hai không được tích phân từ 0 mà quên cộng phần diện tích đã có ở đoạn đầu (1/2).</p>'),
                 K3, 'Câu (b): hàm phân phối từng khúc'), False))
    S.append((sl(steps([m('P(0{,}5<X<1{,}5)=F(1{,}5)-F(0{,}5)'), m('F(1{,}5)=1-\\tfrac{0{,}5^2}{2}=0{,}875,\\quad F(0{,}5)=\\tfrac{0{,}25}{2}=0{,}125'), '<b>Đáp số (c):</b> 0,875 − 0,125 = 0,75.', '',
                        m('E(X)=\\int_0^1x\\cdot x\\,dx+\\int_1^2x(2-x)\\,dx=\\tfrac13+\\tfrac23=1'),
                        m('E(X^2)=\\int_0^1x^3\\,dx+\\int_1^2x^2(2-x)\\,dx=\\tfrac14+\\tfrac{11}{12}=\\tfrac76'),
                        m('\\mathrm{Var}(X)=E(X^2)-[E(X)]^2=\\tfrac76-1=\\tfrac16\\approx0{,}1667'), '<b>Đáp số (d):</b> E(X) = 1; Var(X) = 1/6.']).replace('<li></li>', ''),
                 K3, 'Câu (c), (d): xác suất, kỳ vọng, phương sai'), False))
    assert sp.integrate(x**2 * (2 - x), (x, 1, 2)) == sp.Rational(11, 12)
    S.append((sl(steps(['Công thức biến đổi tuyến tính: ' + m('E(aX+b)=aE(X)+b,\\quad \\mathrm{Var}(aX+b)=a^2\\mathrm{Var}(X)'),
                        m('E(Y)=2\\cdot1+3=5'), m('\\mathrm{Var}(Y)=2^2\\cdot\\tfrac16=\\tfrac23\\approx0{,}6667'),
                        m('P(Y>4)=P(2X+3>4)=P(X>0{,}5)=1-F(0{,}5)=1-0{,}125=0{,}875'),
                        '<b>Đáp số (e):</b> E(Y) = 5; Var(Y) = 2/3; P(Y>4) = 0,875.'])
                 + callout('warn', 'Bẫy', '<p>Var(2X+3) = 4·Var(X), không phải 2·Var(X) và không cộng 3. Hằng số cộng không làm đổi độ phân tán.</p>'),
                 K3, 'Câu (e): biến đổi Y = 2X + 3'), False))
    k = sp.Rational(3, 16); fx3 = k * (4 - x**2)
    assert sp.integrate(fx3, (x, 0, 2)) == 1
    e3 = sp.integrate(x * fx3, (x, 0, 2)); p3 = sp.integrate(fx3, (x, 0, 1))
    e32 = sp.integrate(x**2 * fx3, (x, 0, 2)); v3 = e32 - e3**2
    S.append((sl(mistakes(['Chỉ tích phân một khoảng, quên khoảng còn lại.', 'Viết Var(X) = E(X²) mà quên trừ [E(X)]².', 'F(x) ở khoảng sau thiếu phần cộng dồn.', 'Var(aX+b) = a·Var(X) hoặc cộng b vào phương sai.'])
                 + selfcheck(['Có kiểm tra F(2) = 1 và F liên tục tại điểm nối không?', 'E(X²) và [E(X)]² có viết riêng không?', 'Mỗi ý (a)–(e) có Đáp số không?'])
                 + '<details><summary><b>Bài tương tự để tự làm</b></summary><p>X có mật độ f(x) = c(4 − x²) với 0 ≤ x ≤ 2. Tìm c, P(X &lt; 1), E(X), Var(X).</p>'
                 + f'<p><b>Đáp số:</b> c = 3/16; P(X<1) = {sp.nsimplify(p3)} = {fl(p3,4)}; E(X) = {e3} = {fl(e3,4)}; E(X²) = {e32}; Var(X) = {v3} ≈ {fl(v3,4)}.</p></details>', K3, 'Tập chữa và bài tương tự'), False))
    S.append((sl(callout('good', 'Chuẩn bị cho kỳ thi', ul([
        'Làm lại cả ba bài vào một tờ giấy sạch, bấm giờ 20 phút mỗi bài.',
        'Chụp bài thẳng, đủ sáng, rồi tự chấm theo danh sách “Tập chữa”.',
        'Làm trước phần tự luận của <a href="../de-giua-ky-2/index.html">đề giữa kỳ lần 2</a> (đáp án khóa bằng mật khẩu).',
        'Ôn lý thuyết ở <a href="../m04-toan-phan-bayes/index.html">M4</a> và <a href="../m05-bien-ngau-nhien/index.html">M5</a>.'])), 'KẾT THÚC', 'Việc tiếp theo'), False))
    return S

def build():
    body = ('<div class="crumbs"><a href="../index.html">Trang chủ</a> › Bài mẫu tự luận</div><h1>Ba bài mẫu tự luận khó, học từng bước</h1>'
            '<p class="lead">Bộ slide để chép vào vở, tự làm, đối chiếu từng bước và tập chữa. Ba bài nhắm vào các điểm yếu của bài làm lần 1: số liệu ghép lớp, xác suất toàn phần – Bayes, biến ngẫu nhiên.</p>'
            + deck([(autotex(h), d) for h, d in slides()], 'd-baimau'))
    write('vi/bai-mau-tu-luan/index.html', page('Ba bài mẫu tự luận khó', body, 2, 'Ba bài tự luận mẫu có lời giải từng bước, bài tương tự và danh sách tự chấm', scripts=['deck.js']))
    print('bai mau ok', len(slides()), 'slide')
