"""Module 5 — chuyên sâu: bảng hai BNN, hàm của BNN, mật độ phân đoạn, quyết định theo kỳ vọng. Số tính bằng phân số/tích phân số."""
import math
from fractions import Fraction as Fr
from scipy import integrate
from hx import *
K = 'MODULE 5 · '
def fl(x, d=4): return f'{float(x):.{d}f}'
def ev(xs, ps): return sum(Fr(x) * Fr(p) for x, p in zip(xs, ps))
def var(xs, ps): mu = ev(xs, ps); return sum(Fr(p) * (Fr(x) - mu) ** 2 for x, p in zip(xs, ps))
def parts():
    P = []
    # ───────── A. Rời rạc nâng cao ─────────
    s = []
    # tìm tham số
    a, b = Fr(2, 5), Fr(1, 5)
    xs = [1, 2, 3, 4]; ps = [Fr(1, 10), a, b, Fr(3, 10)]
    assert sum(ps) == 1 and ev(xs, ps) == Fr(27, 10)
    s.append(sl(callout('info', 'Ví dụ A1 · Tìm hai tham số từ E(X)', 'X nhận 1, 2, 3, 4 với P = 0.1; a; b; 0.3 và E(X) = 2.7. Tìm a, b.')
                + steps([m('0.1+a+b+0.3=1\\Rightarrow a+b=0.6'), m('0.1\\cdot1+2a+3b+0.3\\cdot4=2.7\\Rightarrow2a+3b=1.4'), m('b=1.4-2(0.6)=0.2,\\quad a=0.4'), m(f'\\text{{Kiểm tra: }}E(X)=0.1+0.8+0.6+1.2={fl(ev(xs,ps),2)}')])
                + '<p>Hai ẩn cần hai phương trình: một từ tổng xác suất bằng 1, một từ giá trị kỳ vọng cho trước.</p>', K + 'PHẦN 4 · Chuyên sâu', 'Tìm tham số của bảng phân phối'))
    X2 = [-1, 0, 1, 2, 3]; Pp = [Fr(10, 100), Fr(20, 100), Fr(30, 100), Fr(25, 100), Fr(15, 100)]
    dist = {}
    for x, p in zip(X2, Pp): dist[(x - 2) ** 2] = dist.get((x - 2) ** 2, 0) + p
    EY1 = sum(k * v for k, v in dist.items()); EY2 = sum(p * (x - 2) ** 2 for x, p in zip(X2, Pp)); assert EY1 == EY2
    s.append(sl(callout('info', 'Ví dụ A2 · Phân phối của Y = (X − 2)²', 'X nhận −1, 0, 1, 2, 3 với P = 0.10; 0.20; 0.30; 0.25; 0.15. Lập bảng phân phối của Y và tính E(Y).')
                + table(['x', '−1', '0', '1', '2', '3'], [['P', '0.10', '0.20', '0.30', '0.25', '0.15'], ['y = (x−2)²', '9', '4', '1', '0', '1']])
                + table(['y', '0', '1', '4', '9'], [['P(Y=y)'] + [fl(dist[k], 2) for k in (0, 1, 4, 9)]])
                + steps(['Các x cho cùng y thì cộng xác suất: y = 1 ứng với x = 1 và x = 3 nên 0.30 + 0.15 = 0.45.', m(f'E(Y)=0\\cdot0.25+1\\cdot0.45+4\\cdot0.20+9\\cdot0.10={fl(EY1,2)}'), m(f'\\text{{Cũng bằng }}\\sum(x-2)^2p={fl(EY2,2)}')]), K + 'PHẦN 4 · Chuyên sâu', 'Hàm của một BNN rời rạc: gộp các giá trị trùng'))
    # hai BNN
    J = {(0, 1): Fr(10, 100), (0, 2): Fr(20, 100), (0, 3): Fr(10, 100), (1, 1): Fr(20, 100), (1, 2): Fr(10, 100), (1, 3): Fr(30, 100)}
    assert sum(J.values()) == 1
    px = {x: sum(v for (a_, b_), v in J.items() if a_ == x) for x in (0, 1)}; py = {y: sum(v for (a_, b_), v in J.items() if b_ == y) for y in (1, 2, 3)}
    exy = sum(a_ * b_ * v for (a_, b_), v in J.items()); ex = sum(k * v for k, v in px.items()); ey = sum(k * v for k, v in py.items()); cov = exy - ex * ey
    ind = all(J[(x, y)] == px[x] * py[y] for x in px for y in py); assert not ind
    s.append(sl(callout('info', 'Ví dụ A3 · Phân phối đồng thời của (X, Y)', 'Bảng xác suất đồng thời P(X = x, Y = y):')
                + table(['', 'Y=1', 'Y=2', 'Y=3', 'P(X=x)'], [['X=0', '0.10', '0.20', '0.10', fl(px[0], 2)], ['X=1', '0.20', '0.10', '0.30', fl(px[1], 2)], ['P(Y=y)', fl(py[1], 2), fl(py[2], 2), fl(py[3], 2), '1']])
                + steps(['Phân phối biên: cộng theo hàng hoặc cột (hàng và cột cuối của bảng).', m(f'E(X)={fl(ex,2)},\\ E(Y)={fl(ey,2)},\\ E(XY)=\\sum xyP={fl(exy,2)}'), m(f'\\mathrm{{Cov}}(X,Y)=E(XY)-E(X)E(Y)={fl(exy,2)}-{fl(ex,2)}\\cdot{fl(ey,2)}={fl(cov,3)}'), m(f'\\text{{Độc lập? }}P(X{{=}}0,Y{{=}}1)=0.10\\ne0.4\\cdot0.3={fl(px[0]*py[1],2)}\\Rightarrow\\text{{không độc lập}}')]), K + 'PHẦN 4 · Chuyên sâu', 'Bảng đồng thời, phân phối biên, hiệp phương sai'))
    PX = [Fr(5, 10), Fr(3, 10), Fr(2, 10)]; PY = [Fr(6, 10), Fr(4, 10)]
    S = {}
    for i, p in enumerate(PX):
        for j, q in enumerate(PY): S[i + j] = S.get(i + j, 0) + p * q
    ES = sum(k * v for k, v in S.items()); VS = sum(v * (k - ES) ** 2 for k, v in S.items())
    assert ES == ev([0, 1, 2], PX) + ev([0, 1], PY) and VS == var([0, 1, 2], PX) + var([0, 1], PY)
    s.append(sl(callout('info', 'Ví dụ A4 · Tổng hai BNN độc lập', 'X ∈ {0,1,2} với P = 0.5; 0.3; 0.2. Y ∈ {0,1} với P = 0.6; 0.4. X, Y độc lập. S = X + Y.')
                + table(['s', '0', '1', '2', '3'], [['P(S=s)'] + [fl(S[k], 2) for k in range(4)]])
                + steps([m('P(S=1)=P(0,1)+P(1,0)=0.5\\cdot0.4+0.3\\cdot0.6=0.38'), m(f'E(S)={fl(ES,2)}=E(X)+E(Y)=0.7+0.4'), m(f'\\mathrm{{Var}}(S)={fl(VS,2)}=\\mathrm{{Var}}(X)+\\mathrm{{Var}}(Y)=0.61+0.24\\ \\text{{(vì độc lập)}}')]), K + 'PHẦN 4 · Chuyên sâu', 'Tổng hai BNN rời rạc: tích chập và cộng phương sai'))
    P.append(dict(title='Chuyên sâu: tham số, hàm của BNN, bảng đồng thời', bullets=['Tìm tham số', 'Phân phối của Y = g(X)', 'Bảng đồng thời và hiệp phương sai', 'Tổng hai BNN'], slides=s))
    # ───────── B. Liên tục nâng cao ─────────
    s = []
    f1 = lambda x: x if x <= 1 else 2 - x
    I = integrate.quad(f1, 0, 2, points=[1])[0]; assert abs(I - 1) < 1e-9
    P2 = integrate.quad(f1, 0.5, 1.5, points=[1])[0]; assert abs(P2 - 0.75) < 1e-9
    EXt = integrate.quad(lambda x: x * f1(x), 0, 2, points=[1])[0]; VXt = integrate.quad(lambda x: (x - 1) ** 2 * f1(x), 0, 2, points=[1])[0]
    assert abs(EXt - 1) < 1e-9 and abs(VXt - 1 / 6) < 1e-9
    s.append(sl(callout('info', 'Ví dụ B1 · Mật độ tam giác (phân đoạn)', 'f(x) = x trên [0, 1], f(x) = 2 − x trên (1, 2], 0 ở ngoài. Kiểm tra chuẩn hóa, tìm F(x), P(0.5 < X < 1.5), E(X), Var(X).')
                + steps([m('\\text{Diện tích tam giác đáy 2, cao 1: }\\tfrac12\\cdot2\\cdot1=1\\ \\checkmark'), m('F(x)=\\tfrac{x^2}2\\ (0\\le x\\le1);\\quad F(x)=1-\\tfrac{(2-x)^2}2\\ (1<x\\le2)'), m(f'P(0.5<X<1.5)=F(1.5)-F(0.5)=0.875-0.125={fl(P2,2)}'), m(f'E(X)=1\\ \\text{{(đối xứng quanh }}x=1\\text{{)}};\\quad\\mathrm{{Var}}(X)=\\tfrac16={fl(VXt,4)}')])
                + '<p>Với mật độ phân đoạn, F cũng phân đoạn: phải cộng dồn diện tích các đoạn trước (F(1) = 0.5).</p>', K + 'PHẦN 5 · Chuyên sâu', 'Mật độ phân đoạn và hàm phân phối'))
    Ey = integrate.quad(lambda x: x ** 2, 0, 1)[0]; Vy = integrate.quad(lambda x: x ** 4, 0, 1)[0] - Ey ** 2; assert abs(Ey - 1 / 3) < 1e-9 and abs(Vy - 4 / 45) < 1e-9
    s.append(sl(callout('info', 'Ví dụ B2 · Mật độ của Y = X²', 'X ~ đều trên [0, 1]. Tìm F_Y, f_Y, E(Y), Var(Y).')
                + steps([m('F_Y(y)=P(X^2\\le y)=P(X\\le\\sqrt y)=\\sqrt y,\\ 0\\le y\\le1'), m('f_Y(y)=F_Y\'(y)=\\tfrac1{2\\sqrt y},\\ 0<y<1'), m(f'E(Y)=\\int_0^1x^2dx=\\tfrac13={fl(Ey)},\\ \\ E(Y^2)=\\int_0^1x^4dx=\\tfrac15'), m(f'\\mathrm{{Var}}(Y)=\\tfrac15-\\tfrac19=\\tfrac4{{45}}={fl(Vy)}')])
                + '<p>Cách làm tổng quát: viết F của biến mới theo F của biến cũ, rồi đạo hàm. Mật độ f_Y không bằng f_X(√y); phải nhân hệ số 1/(2√y).</p>', K + 'PHẦN 5 · Chuyên sâu', 'Phân phối của hàm của BNN liên tục'))
    EX = integrate.quad(lambda x: x * 2 * x, 0, 1)[0]; assert abs(EX - 2 / 3) < 1e-9
    s.append(sl(callout('info', 'Ví dụ B3 · Biến đổi tuyến tính Y = 2X + 3', 'X có mật độ f(x) = 2x trên [0, 1]. Tìm f_Y, E(Y), Var(Y).')
                + steps([m('F_Y(y)=P(X\\le\\tfrac{y-3}2)=\\left(\\tfrac{y-3}2\\right)^2,\\ 3\\le y\\le5'), m('f_Y(y)=\\tfrac{y-3}2,\\ 3\\le y\\le5'), m(f'E(Y)=2E(X)+3=2\\cdot\\tfrac23+3=\\tfrac{{13}}3={fl(13/3)}'), m('\\mathrm{Var}(X)=\\tfrac12-\\tfrac49=\\tfrac1{18},\\ \\mathrm{Var}(Y)=4\\cdot\\tfrac1{18}=\\tfrac29')]), K + 'PHẦN 5 · Chuyên sâu', 'Biến đổi tuyến tính: dịch và co giãn'))
    lam = 0.5
    s3 = math.exp(-lam * 3); cond = math.exp(-lam * 5) / math.exp(-lam * 2); assert abs(s3 - cond) < 1e-12
    s.append(sl(callout('info', 'Ví dụ B4 · Thời gian sống mũ λ = 0.5', 'X ~ Exp(0.5) (đơn vị năm). Tính P(X > 3), P(X > 5 | X > 2), trung vị, E(X), σ.')
                + steps([m(f'P(X>3)=e^{{-1.5}}={fl(s3)}'), m(f'P(X>5|X>2)=\\tfrac{{e^{{-2.5}}}}{{e^{{-1}}}}=e^{{-1.5}}={fl(cond)}'), m(f'\\text{{Trung vị}}=\\tfrac{{\\ln2}}{{\\lambda}}={fl(math.log(2)/lam)},\\ E(X)=2,\\ \\sigma=2')])
                + '<p>Tính chất không nhớ: đã sống 2 năm không làm thay đổi xác suất sống thêm 3 năm. Trung vị (1.386) nhỏ hơn kỳ vọng (2): phân phối lệch phải.</p>', K + 'PHẦN 5 · Chuyên sâu', 'Phân phối mũ và tính chất không nhớ'))
    med = 2 * 0.5 ** (1 / 3); EX3 = integrate.quad(lambda x: x * 3 / 8 * x * x, 0, 2)[0]; assert abs(EX3 - 1.5) < 1e-9
    s.append(sl(callout('info', 'Ví dụ B5 · Mốt, trung vị, trung bình', 'f(x) = (3/8)x² trên [0, 2]. So sánh ba đặc trưng vị trí.')
                + table(['Đặc trưng', 'Cách tìm', 'Giá trị'], [['Mốt', 'f lớn nhất (f tăng) tại x = 2', '2'], ['Trung vị', 'F(x) = x³/8 = 1/2 ⇒ x = 2·(1/2)^{1/3}', fl(med)], ['Kỳ vọng', '∫ x·(3/8)x² dx = 3/2', '1.5']])
                + '<p>Mốt 2 &gt; trung vị 1.587 &gt; kỳ vọng 1.5: phân phối lệch trái (đuôi dài về phía nhỏ). Dùng kỳ vọng làm “giá trị điển hình” sẽ thấp hơn mốt.</p>', K + 'PHẦN 5 · Chuyên sâu', 'Ba đặc trưng vị trí cho phân phối lệch'))
    P.append(dict(title='Chuyên sâu: mật độ phân đoạn, hàm của BNN, phân phối mũ', bullets=['Mật độ tam giác', 'Y = X²', 'Y = 2X + 3', 'Phân phối mũ', 'Mốt, trung vị, trung bình'], slides=s))
    # ───────── C. Đặc trưng và quyết định ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ C1 · Phương sai của tổ hợp tuyến tính', 'Var(X) = 4, Var(Y) = 9, Cov(X, Y) = 3. Tính Var(2X − Y) và Var(X + Y), hệ số tương quan.')
                + steps([m('\\mathrm{Var}(aX+bY)=a^2\\mathrm{Var}(X)+b^2\\mathrm{Var}(Y)+2ab\\,\\mathrm{Cov}(X,Y)'), m('\\mathrm{Var}(2X-Y)=4\\cdot4+9+2\\cdot2\\cdot(-1)\\cdot3=13'), m('\\mathrm{Var}(X+Y)=4+9+2\\cdot3=19'), m(f'\\rho=\\tfrac{{3}}{{\\sqrt{{4\\cdot9}}}}={fl(3/6,2)}')])
                + '<p>Nếu X, Y độc lập (Cov = 0) thì Var(2X − Y) = 25 và Var(X + Y) = 13. Tương quan dương làm Var(X + Y) tăng lên 19 và Var(2X − Y) giảm xuống 13.</p>', K + 'PHẦN 6 · Chuyên sâu', 'Phương sai khi hai BNN phụ thuộc'))
    mu, sg, n = 10, 3, 36
    s.append(sl(callout('info', 'Ví dụ C2 · Tổng và trung bình của n BNN độc lập cùng phân phối', 'Mỗi X_i có μ = 10, σ = 3; n = 36.')
                + steps([m('S=X_1+\\dots+X_n:\\ E(S)=n\\mu=360,\\ \\sigma_S=\\sigma\\sqrt n=18'), m(f'\\bar X=S/n:\\ E(\\bar X)=\\mu=10,\\ \\sigma_{{\\bar X}}=\\tfrac{{\\sigma}}{{\\sqrt n}}={fl(sg/math.sqrt(n),2)}')])
                + '<p>Độ lệch chuẩn của tổng tăng theo √n, của trung bình giảm theo 1/√n. Đây là nền tảng của ước lượng ở các module sau.</p>', K + 'PHẦN 6 · Chuyên sâu', 'Tổng và trung bình: độ lệch theo √n'))
    # Chebyshev / Markov
    s.append(sl(callout('info', 'Ví dụ C3 · Markov và Chebyshev', 'Số lượt truy cập mỗi ngày X ≥ 0 có E(X) = 50 và σ = 5.')
                + steps([m('\\text{Markov: }P(X\\ge80)\\le\\tfrac{E(X)}{80}=0.625'), m('\\text{Chebyshev: }P(|X-50|\\ge10)\\le\\tfrac{\\sigma^2}{10^2}=0.25'), m('\\Rightarrow P(40<X<60)\\ge1-0.25=0.75')])
                + '<p>Cả hai cho <b>cận trên</b> không phụ thuộc dạng phân phối, nên thường khá lỏng. Chebyshev dùng cả μ và σ nên chặt hơn Markov.</p>', K + 'PHẦN 6 · Chuyên sâu', 'Hai bất đẳng thức không cần biết phân phối'))
    # quyết định
    LA = [0, 100, 500]; pA = [Fr(90, 100), Fr(8, 100), Fr(2, 100)]
    prem = Fr(30)
    EL = ev(LA, pA); VL = var(LA, pA)
    s.append(sl(callout('info', 'Ví dụ C4 · Có nên mua bảo hiểm?', 'Thiệt hại hàng năm (triệu đồng): 0 với xác suất 0.90; 100 với 0.08; 500 với 0.02. Phí bảo hiểm trọn gói 30 triệu/năm.')
                + steps([m(f'E(L)=0\\cdot0.9+100\\cdot0.08+500\\cdot0.02={fl(EL,1)}\\ \\text{{triệu}}'), m(f'\\mathrm{{Var}}(L)=E(L^2)-E(L)^2={fl(sum(p*l*l for l,p in zip(LA,pA)),0)}-{fl(EL*EL,0)}={fl(VL,0)},\\ \\sigma={fl(math.sqrt(VL),1)}'), 'Chi phí kỳ vọng nếu không mua = 18; nếu mua = 30. Kỳ vọng nói “không mua”, nhưng bảo hiểm giảm rủi ro (σ từ %s xuống 0).' % fl(math.sqrt(VL), 1)])
                + '<p>Chênh lệch 12 triệu là “giá của sự an tâm”. Quyết định thực tế cân nhắc cả kỳ vọng và mức chịu rủi ro, không chỉ E(X).</p>', K + 'PHẦN 6 · Chuyên sâu', 'Quyết định theo kỳ vọng và rủi ro'))
    pm = [Fr(5, 10), Fr(3, 10), Fr(2, 10)]; ex_ = ev([0, 1, 2], pm); v_ = var([0, 1, 2], pm)
    sk = sum(p * (Fr(x) - ex_) ** 3 for x, p in zip([0, 1, 2], pm)) / v_ ** Fr(3, 2) if False else sum(float(p) * (x - float(ex_)) ** 3 for x, p in zip([0, 1, 2], pm)) / float(v_) ** 1.5
    s.append(sl(callout('info', 'Ví dụ C5 · Hệ số bất đối xứng', 'X ∈ {0, 1, 2} với P = 0.5; 0.3; 0.2. Tính E(X), σ và hệ số bất đối xứng γ = E[(X−μ)³]/σ³.')
                + steps([m(f'E(X)={fl(ex_,2)},\\ \\mathrm{{Var}}(X)={fl(v_,2)},\\ \\sigma={fl(float(v_)**.5,4)}'), m(f'\\gamma={fl(sk,4)}>0\\ \\Rightarrow\\ \\text{{lệch phải (đuôi dài về giá trị lớn)}}')])
                + '<p>γ = 0 với phân phối đối xứng; γ &gt; 0 lệch phải; γ &lt; 0 lệch trái. Với lệch phải thường có trung bình &gt; trung vị.</p>', K + 'PHẦN 6 · Chuyên sâu', 'Hình dạng phân phối: độ lệch'))
    s.append(sl(table(['', 'Rời rạc', 'Liên tục'], [['Mô tả', 'bảng pᵢ = P(X = xᵢ)', 'hàm mật độ f(x) ≥ 0'], ['Chuẩn hóa', 'Σ pᵢ = 1', '∫ f = 1'], ['P(a < X ≤ b)', 'Σ pᵢ (a < xᵢ ≤ b)', '∫ₐᵇ f = F(b) − F(a)'], ['E(X)', 'Σ xᵢ pᵢ', '∫ x f(x) dx'], ['E(g(X))', 'Σ g(xᵢ) pᵢ', '∫ g(x) f(x) dx'], ['Var(X)', 'E(X²) − [E(X)]²', 'E(X²) − [E(X)]²'], ['Hàm của X', 'gộp giá trị trùng', 'qua F rồi đạo hàm']])
                + callout('warn', 'Ba cái bẫy', '1) E(g(X)) ≠ g(E(X)). 2) Var(X+Y) = Var X + Var Y chỉ khi độc lập (hoặc Cov = 0). 3) P(X = a) = 0 với BNN liên tục nhưng f(a) có thể lớn hơn 1.'), K + 'PHẦN 6 · Chuyên sâu', 'Bảng tổng hợp rời rạc và liên tục'))
    P.append(dict(title='Chuyên sâu: phương sai tổ hợp, bất đẳng thức, quyết định', bullets=['Var của tổ hợp tuyến tính', 'Tổng và trung bình n BNN', 'Markov, Chebyshev', 'Bảo hiểm', 'Độ lệch', 'Bảng tổng hợp'], slides=s))
    return P
