"""Nội dung Module 0 — Kiến thức tiên quyết (đại số tuyến tính, giải tích nhiều biến, ngôn ngữ tối ưu, ôn QHTT).
Nguồn: kiến thức nền chuẩn + đối chiếu Chương 1 BTDOC (tham khảo, độ tin cậy thấp) + môn QHTT/VTH đã học."""
import numpy as np
from helpers import *

M = 'MODULE 0'
LEAD = 'Những công cụ toán cần có trước khi vào tối ưu lồi: ngôn ngữ của bài toán tối ưu, đại số tuyến tính (vectơ, ma trận, giá trị riêng), giải tích nhiều biến (gradient, Hessian, Taylor), tập và sự tồn tại nghiệm, cùng phần ôn nhanh quy hoạch tuyến tính từ môn đã học.'
META = ['Nguồn: kiến thức nền + đối chiếu BTDOC Ch.1 (chỉ tham khảo)', 'Boyd & Vandenberghe: Ch.1 và phụ lục A', 'Thời lượng gợi ý: 4–6 giờ']
OBJECTIVES = [
    'Phát biểu bài toán tối ưu tổng quát và phân biệt cực tiểu địa phương/toàn cục, tập chấp nhận được, giá trị tối ưu (infimum).',
    'Tính thành thạo tích vô hướng, chuẩn, nhân/chuyển vị ma trận, định thức, nghịch đảo 2×2 và 3×3, giá trị riêng của ma trận 2×2.',
    'Tính gradient, Hessian, khai triển Taylor bậc hai và dùng điều kiện cấp 1–2 cho tối ưu không ràng buộc.',
    'Nhận biết khi nào cực tiểu tồn tại (Weierstrass, coercive) và khi nào không (\\(e^x\\), \\(1/x\\)).',
    'Ôn lại QHTT: dạng chuẩn, nghiệm ở đỉnh, đối ngẫu và độ lệch bù — và thấy chúng là trường hợp riêng của KKT.',
]
R_ = R
def f4(x): return ('%.4f' % x).rstrip('0').rstrip('.')
plan = R['m0_btdoc_plan']; plan_dual = R['m0_btdoc_plan_dual']; four = R['m0_btdoc_4prod']
inv = R['m0_btdoc_inv']; cram = R['m0_btdoc_cramer']; cs = R['m0_cs']; abt = R['m0_ABT']
st1 = R['m0_stat1']; st2 = R['m0_stat2']; gd = R['m0_gd']; gdf = R['m0_gd_f']

DECK = []
add = DECK.append

add(sl('Trước khi học tối ưu: cần trang bị gì?',
       '<p>Module 0 gồm 5 phần:</p><ol><li>Ngôn ngữ của bài toán tối ưu</li><li>Đại số tuyến tính cần nhớ</li><li>Giải tích nhiều biến: gradient, Hessian, Taylor</li><li>Tập, tôpô và sự tồn tại nghiệm</li><li>Ôn quy hoạch tuyến tính và cầu nối sang KKT</li></ol>'
       + callout('info', 'Cách dùng', '<p>Nếu đã quen phần nào thì lướt nhanh và làm bài kiểm tra ở cuối; nếu còn lúng túng thì mở khung “📖 Giải thích cho người mới” và làm lại từng ví dụ bằng tay trước khi xem lời giải.</p>'),
       kicker=M + ' · MỞ ĐẦU',
       explain='<p>Tối ưu hóa dùng ba mảng toán nền: đại số tuyến tính (mô tả bài toán bằng ma trận), giải tích (gradient và Hessian cho biết hàm tăng giảm thế nào) và tôpô cơ bản (nghiệm có tồn tại không). Ta chỉ ôn đúng phần cần thiết.</p>'))

# ---------------- PHẦN 1
add(part(1, 5, 'Ngôn ngữ của bài toán tối ưu', ['Hàm mục tiêu, ràng buộc, tập chấp nhận được', 'Cực tiểu địa phương và toàn cục', 'Phân loại các bài toán tối ưu'], M))
add(sl('Bài toán tối ưu tổng quát',
       formula('Bài toán', r'\min_{x\in\mathbb R^n}\ f(x)\quad\text{s.t.}\quad g_i(x)\le0\ (i=1..m),\ \ h_j(x)=0\ (j=1..p)',
               [('f', 'hàm mục tiêu'), ('g_i,\\ h_j', 'các hàm ràng buộc'), ('C', 'tập chấp nhận được: các x thỏa mọi ràng buộc')])
       + '<ul><li><b>Phương án</b> (điểm chấp nhận được): \\(x\\in C\\).</li><li><b>Phương án tối ưu</b> \\(x^*\\in C\\): \\(f(x^*)\\le f(x)\\ \\forall x\\in C\\) (bài toán min); \\(f(x^*)\\) là <b>giá trị tối ưu</b>.</li><li>Bài toán max đổi thành min của \\(-f\\).</li></ul>',
       kicker=M + ' · PHẦN 1',
       explain='<p>Mọi bài toán tối ưu gồm ba thành phần: <i>cái muốn làm nhỏ</i> (f), <i>các điều kiện phải giữ</i> (ràng buộc), và <i>biến quyết định</i> (x). Bài toán sản xuất trong môn QHTT (tối đa lợi nhuận với giới hạn nguyên liệu) là ví dụ: \\(f=-\\)lợi nhuận, ràng buộc là nguyên liệu.</p>'))
add(sl('Cực tiểu địa phương và toàn cục',
       '<ul><li><b>Toàn cục</b>: \\(f(x^*)\\le f(x)\\) với mọi \\(x\\in C\\).</li><li><b>Địa phương</b>: tồn tại \\(\\varepsilon>0\\) sao cho \\(f(x^*)\\le f(x)\\) với mọi \\(x\\in C\\), \\(\\|x-x^*\\|<\\varepsilon\\).</li></ul>'
       + '<p>Toàn cục ⇒ địa phương; ngược lại chỉ đúng với bài toán <b>lồi</b> (Module 1–2). Ví dụ \\(f=x^3-3x\\) có cực tiểu địa phương tại \\(x=1\\) nhưng không có cực tiểu toàn cục trên \\(\\mathbb R\\).</p>',
       kicker=M + ' · PHẦN 1',
       explain='<p>Hình dung địa hình núi: cực tiểu địa phương là đáy một thung lũng; cực tiểu toàn cục là điểm thấp nhất của cả bản đồ. Thuật toán chỉ nhìn cục bộ nên có thể kẹt ở thung lũng cao. Tính lồi loại trừ tình huống này.</p>'))
add(sl('Phân loại bài toán tối ưu',
       table(['Loại', 'Đặc điểm', 'Ví dụ'],
             [['Tuyến tính (LP)', 'f và ràng buộc tuyến tính', 'kế hoạch sản xuất'], ['Toàn phương (QP)', 'f bậc hai, ràng buộc tuyến tính', 'chiếu điểm lên đa diện'],
              ['Lồi', 'f, \\(g_i\\) lồi, \\(h_j\\) affine', 'bình phương tối thiểu, danh mục đầu tư'], ['Phi tuyến (NLP)', 'f hoặc ràng buộc phi tuyến', '\\(\\min xy\\) trên đĩa'],
              ['Rời rạc/nguyên', 'biến nguyên hoặc 0–1', 'ba lô (knapsack)'], ['Động, tham số, đa mục tiêu', 'nhiều giai đoạn / hệ số phụ thuộc tham số / nhiều mục tiêu', '—']])
       + '<p style="font-size:.85em">Phân loại theo giáo trình BTDOC Chương 1 (tham khảo) và slide 2 (tr.24).</p>',
       kicker=M + ' · PHẦN 1',
       explain='<p>Phân loại cho biết “cây gậy” nào dùng được: LP có đơn hình, QP có null space/active set, bài toán lồi có điều kiện KKT cần và đủ, bài toán nguyên thì khó (NP-khó). Môn này tập trung phần lồi và phi tuyến liên tục.</p>'))
add(sl('Bản đồ các lớp bài toán',
       '<figure class="slide-fig"><img src="../../assets/diagrams/d1-phan-loai-toi-uu.svg" alt="Phân loại" style="max-height:20em;background:#fff"/></figure>',
       kicker=M + ' · PHẦN 1',
       explain='<p>LP ⊂ QP lồi ⊂ tối ưu lồi ⊂ phi tuyến tổng quát. Bài toán nguyên nằm ngoài sơ đồ vì miền rời rạc không lồi.</p>'))

# ---------------- PHẦN 2
add(part(2, 5, 'Đại số tuyến tính cần nhớ', ['Vectơ, tích vô hướng, chuẩn', 'Ma trận: nhân, chuyển vị, định thức, nghịch đảo', 'Giá trị riêng và ma trận đối xứng', 'Dạng toàn phương'], M))
add(sl('Vectơ, tích vô hướng, chuẩn',
       formula('Tích vô hướng và chuẩn', r'\langle u,v\rangle=u^\top v=\sum_iu_iv_i,\qquad\|u\|=\sqrt{u^\top u}')
       + formula('Bất đẳng thức Cauchy–Schwarz', r'|u^\top v|\le\|u\|\,\|v\|')
       + '<p>Ví dụ: \\(u=(1,2,2)\\), \\(v=(2,3,6)\\): \\(u^\\top v=' + f4(cs['dot']) + '\\), \\(\\|u\\|=' + f4(cs['nu']) + '\\), \\(\\|v\\|=' + f4(cs['nv']) + '\\), \\(\\|u\\|\\|v\\|=' + f4(cs['prod']) + '\\ge20\\).</p>',
       kicker=M + ' · PHẦN 2',
       explain='<p>\\(u^\\top v=\\|u\\|\\|v\\|\\cos\\theta\\): tích vô hướng đo mức cùng hướng. Bất đẳng thức Cauchy–Schwarz nói \\(|\\cos\\theta|\\le1\\); dấu bằng khi hai vectơ song song.</p>'))
add(sl('Ma trận: nhân, chuyển vị, đối xứng',
       '<ul><li>\\((AB)_{ij}=\\sum_kA_{ik}B_{kj}\\): cần \\(A\\) cỡ \\(m\\times n\\), \\(B\\) cỡ \\(n\\times l\\); kết quả \\(m\\times l\\); nói chung \\(AB\\ne BA\\).</li><li>\\((AB)^\\top=B^\\top A^\\top\\); \\((A^\\top)^\\top=A\\).</li><li>A đối xứng: \\(A=A^\\top\\).</li></ul>'
       + '<p>Ví dụ: \\(A=\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\), \\(B=\\begin{pmatrix}0&1\\\\1&1\\end{pmatrix}\\): \\(AB=\\begin{pmatrix}' + '&'.join(str(int(v)) for v in abt['AB'][0]) + '\\\\' + '&'.join(str(int(v)) for v in abt['AB'][1]) + '\\end{pmatrix}\\), \\((AB)^\\top=B^\\top A^\\top=\\begin{pmatrix}' + '&'.join(str(int(v)) for v in abt['ABt'][0]) + '\\\\' + '&'.join(str(int(v)) for v in abt['ABt'][1]) + '\\end{pmatrix}\\).</p>',
       kicker=M + ' · PHẦN 2',
       explain='<p>Điều quan trọng cho tối ưu: Hessian luôn đối xứng; \\(x^\\top Ax\\) là số thực nên bằng chuyển vị của nó. Nhớ đảo thứ tự khi chuyển vị một tích.</p>'))
add(sl('Định thức và nghịch đảo',
       formula('Định thức 2×2 và nghịch đảo 2×2', r'\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc,\qquad A^{-1}=\frac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}')
       + '<ul><li>A khả nghịch ⇔ \\(\\det A\\ne0\\).</li><li>Tính chất: đổi hai hàng thì đổi dấu; cộng bội của một hàng vào hàng khác không đổi; \\(\\det A=\\det A^\\top\\); \\(\\det(AB)=\\det A\\det B\\).</li></ul>'
       + '<p>Ví dụ (BTDOC): \\(A=\\begin{pmatrix}1&2&3\\\\2&5&3\\\\1&0&8\\end{pmatrix}\\): \\(\\det A=' + f4(inv['det']) + '\\), \\(A^{-1}=\\begin{pmatrix}' + '\\\\'.join('&'.join(f4(v) for v in row) for row in inv['inv']) + '\\end{pmatrix}\\).</p>',
       kicker=M + ' · PHẦN 2',
       explain='<p>Định thức bằng 0 nghĩa là các hàng phụ thuộc tuyến tính (ma trận “suy biến”) và không đảo được. Với ma trận 3×3 dùng khai triển theo hàng hoặc ma trận phụ hợp: \\(A^{-1}=\\dfrac1{\\det A}\\,[A_{ji}]\\). Kiểm lại luôn bằng \\(AA^{-1}=I\\).</p>'))
add(sl('Hệ phương trình tuyến tính',
       '<p>\\(Ax=b\\) với A vuông khả nghịch có nghiệm duy nhất \\(x=A^{-1}b\\); công thức Cramer \\(x_i=\\det A_i/\\det A\\) (\\(A_i\\): thay cột i bằng b).</p>'
       '<p>Ví dụ (BTDOC): \\(x_1+2x_3=6\\), \\(3x_1+4x_2+6x_3=30\\), \\(-x_1-2x_2+3x_3=8\\): \\(\\det A=' + f4(cram['det']) + '\\), nghiệm \\(x=(' + ', '.join(f4(v) for v in cram['x']) + ')\\).</p>'
       '<ul><li>Hạng \\(\\mathrm{rank}A\\) = số hàng độc lập tuyến tính.</li><li>Tương thích ⇔ \\(\\mathrm{rank}A=\\mathrm{rank}[A\\,|\\,b]\\); xác định nếu nghiệm duy nhất, bất định nếu có vô số nghiệm.</li></ul>',
       kicker=M + ' · PHẦN 2',
       explain='<p>Hệ KKT của Module 3 là một hệ tuyến tính lớn: bạn sẽ giải nó bằng chính các kỹ thuật này. Điều kiện \\(\\mathrm{rank}A=m\\) trong null space chính là “các ràng buộc độc lập”.</p>'))
add(sl('Giá trị riêng và ma trận đối xứng',
       formula('Giá trị riêng', r'Av=\lambda v,\ v\ne0\iff\det(A-\lambda I)=0')
       + '<ul><li>Vết \\(=\\sum\\lambda_i\\); định thức \\(=\\prod\\lambda_i\\).</li><li>Ma trận <b>đối xứng</b> thực có mọi giá trị riêng thực và chéo hóa được bằng ma trận trực giao.</li></ul>'
       + '<p>Ví dụ: \\(A=\\begin{pmatrix}2&-1\\\\-1&2\\end{pmatrix}\\): \\((2-\\lambda)^2-1=0\\Rightarrow\\lambda=1,3\\) (vết 4, định thức 3). Ví dụ \\(\\begin{pmatrix}4&1\\\\1&3\\end{pmatrix}\\): \\(\\lambda=' + ', '.join(f4(v) for v in R['m0_eig_2x2b']['eig']) + '\\).</p>',
       kicker=M + ' · PHẦN 2',
       explain='<p>Giá trị riêng cho biết ma trận “kéo giãn” theo từng hướng chính bao nhiêu lần. Với Hessian, giá trị riêng chính là độ cong theo các hướng chính: tất cả dương ⇒ đáy bát (cực tiểu).</p>'))
add(sl('Dạng toàn phương và dấu',
       formula('Dạng toàn phương', r'q(x)=x^\top Ax\quad(A=A^\top)')
       + table(['Dấu của A', 'Điều kiện', 'Giá trị riêng'], [['xác định dương', '\\(x^\\top Ax>0\\ \\forall x\\ne0\\)', 'tất cả \\(>0\\)'], ['nửa xác định dương', '\\(x^\\top Ax\\ge0\\ \\forall x\\)', 'tất cả \\(\\ge0\\)'], ['xác định âm', '\\(x^\\top Ax<0\\ \\forall x\\ne0\\)', 'tất cả \\(<0\\)'], ['không xác định', 'đổi dấu', 'có cả dương và âm']])
       + '<p>Chi tiết và công cụ tương tác ở Module 1.</p>',
       kicker=M + ' · PHẦN 2',
       explain='<p>Đây là “cầu nối” sang Module 1: tính lồi của hàm được kiểm bằng dấu của dạng toàn phương của Hessian.</p>'))

# ---------------- PHẦN 3
add(part(3, 5, 'Giải tích nhiều biến', ['Gradient và Hessian', 'Khai triển Taylor', 'Điều kiện tối ưu cấp 1 và cấp 2 (không ràng buộc)', 'Gradient descent'], M))
add(sl('Gradient',
       formula('Gradient', r'\nabla f(x)=\Big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\Big)^\top')
       + '<ul><li>\\(\\nabla f(x)\\) là hướng <b>tăng nhanh nhất</b> của f; \\(-\\nabla f\\) là hướng giảm nhanh nhất.</li><li>\\(\\nabla f(x)\\perp\\) đường mức của f qua x.</li></ul>'
       + '<p>Ví dụ: \\(f=x^2y+3xy^2-2x\\): \\(\\nabla f=(2xy+3y^2-2,\\ x^2+6xy)\\); tại \\((1,2)\\): \\(\\nabla f=(' + ', '.join(f4(v) for v in R['m0_grad_ex']['grad_at_1_2']) + ')\\).</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Hình dung f là độ cao của một ngọn đồi: gradient trỏ lên dốc nhất; đi ngược lại thì xuống dốc nhanh nhất. Đường mức (đường đồng độ cao) luôn vuông góc gradient. Thử ở công cụ “Gradient, đường mức” bên dưới.</p>'))
add(sl('Hessian và đạo hàm theo hướng',
       formula('Hessian', r'\nabla^2f(x)=\Big[\frac{\partial^2f}{\partial x_i\partial x_j}\Big]')
       + formula('Đạo hàm theo hướng d', r'f^{\prime}(x;d)=\nabla f(x)^\top d,\qquad \frac{d^2}{dt^2}f(x+td)\Big|_{t=0}=d^\top\nabla^2f(x)d')
       + '<p>Ví dụ (code): tại \\((1,2)\\), \\(H=\\begin{pmatrix}' + '\\\\'.join('&'.join(f4(v) for v in row) for row in R['m0_grad_ex']['H_at_1_2']) + '\\end{pmatrix}\\).</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Đạo hàm cấp một cho độ dốc theo hướng d; đạo hàm cấp hai \\(d^\\top Hd\\) cho độ cong theo hướng d. Hessian dương ⇒ đồ thị cong lên theo mọi hướng.</p>'))
add(sl('Khai triển Taylor',
       formula('Taylor bậc hai', r'f(x+d)\approx f(x)+\nabla f(x)^\top d+\tfrac12d^\top\nabla^2f(x)d')
       + '<p>Ví dụ \\(f(x,y)=e^x+y^2\\) tại \\((0,0)\\): \\(f\\approx1+x+\\tfrac12x^2+y^2\\). Tại \\((0.1,0.2)\\): giá trị thật \\(' + f4(R['m0_taylor']['f(0.1,0.2)']) + '\\), xấp xỉ bậc hai \\(' + f4(R['m0_taylor']['T2(0.1,0.2)']) + '\\).</p>'
       '<p>Bậc một: \\(f(x+d)\\approx f(x)+\\nabla f(x)^\\top d\\) (“tiếp tuyến”). Sai số bậc hai \\(O(\\|d\\|^3)\\).</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Taylor là ý tưởng nền của mọi thuật toán tối ưu: thay hàm phức tạp bằng xấp xỉ đơn giản (tuyến tính ⇒ gradient descent; toàn phương ⇒ Newton, SQP) rồi giải xấp xỉ.</p>'))
add(sl('Điều kiện tối ưu không ràng buộc',
       '<div class="callout good"><span class="ct"><b>Điều kiện cần cấp 1 (Fermat)</b></span>Nếu \\(x^*\\) là cực tiểu địa phương của f khả vi thì \\(\\nabla f(x^*)=0\\).</div>'
       '<div class="callout good"><span class="ct"><b>Điều kiện cần cấp 2</b></span>Cực tiểu địa phương ⇒ \\(\\nabla f(x^*)=0\\) và \\(\\nabla^2f(x^*)\\succeq0\\).</div>'
       '<div class="callout good"><span class="ct"><b>Điều kiện đủ cấp 2</b></span>\\(\\nabla f(x^*)=0\\) và \\(\\nabla^2f(x^*)\\succ0\\) ⇒ cực tiểu địa phương chặt.</div>'
       '<p>Nếu f lồi: \\(\\nabla f(x^*)=0\\) ⇔ cực tiểu <b>toàn cục</b> (Module 1).</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Đây là dạng đơn giản nhất của KKT (không có ràng buộc). Điểm dừng \\(\\nabla f=0\\) có thể là cực tiểu, cực đại hoặc điểm yên ngựa; Hessian phân biệt chúng.</p>'))
add(sl('Ví dụ phân loại điểm dừng',
       '<p>(a) \\(f=x^2+xy+y^2-3x\\): \\(\\nabla f=(2x+y-3,\\ x+2y)=0\\Rightarrow(x,y)=(2,-1)\\); \\(H=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}\\succ0\\) ⇒ cực tiểu (toàn cục vì f lồi), \\(f=' + f4(st1['fval']) + '\\).</p>'
       '<p>(b) \\(f=x^3-3x+y^2\\): \\(\\nabla f=(3x^2-3,\\ 2y)=0\\Rightarrow(1,0),(-1,0)\\). \\(H=\\mathrm{diag}(6x,2)\\): tại \\((1,0)\\) giá trị riêng \\(6,2>0\\) ⇒ cực tiểu địa phương (\\(f=-2\\)); tại \\((-1,0)\\) giá trị riêng \\(-6,2\\) ⇒ <b>điểm yên ngựa</b> (\\(f=2\\)). Hàm không có cực tiểu toàn cục (\\(x\\to-\\infty\\)).</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Quy trình: giải \\(\\nabla f=0\\) ⇒ tính Hessian tại từng nghiệm ⇒ phân loại theo giá trị riêng. (Kết quả được kiểm bằng sympy.)</p>'))
add(sl('Gradient descent',
       formula('Gradient descent', r'x^{k+1}=x^k-t\,\nabla f(x^k)')
       + '<p>Ví dụ \\(f=x^2+3y^2\\), \\(x^0=(-1.8,1.4)\\), \\(t=0.1\\): \\(x^1=(' + ', '.join(f4(v) for v in gd[1]) + ')\\), \\(x^2=(' + ', '.join(f4(v) for v in gd[2]) + ')\\); \\(f\\) giảm \\(' + ' → '.join(f4(v) for v in gdf[:4]) + '\\).</p>'
       '<p>Bước quá lớn (\\(t>2/L\\), L là hằng số Lipschitz của gradient, ở đây \\(L=6\\)) làm dãy dao động hoặc phân kỳ.</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Mỗi bước đi một quãng t theo hướng dốc xuống nhất. Bước nhỏ thì an toàn nhưng chậm; bước lớn nhanh nhưng có thể vượt qua đáy. Đây là nội dung “tối ưu không ràng buộc” của buổi 4 trong đề cương; thử ở công cụ bên dưới.</p>'))

# ---------------- PHẦN 4
add(part(4, 5, 'Tập, tôpô và sự tồn tại nghiệm', ['Infimum, supremum', 'Tập đóng, bị chặn, compact', 'Định lý Weierstrass và hàm coercive'], M))
add(sl('Infimum và supremum',
       '<ul><li>\\(\\inf S\\): cận dưới lớn nhất của S; \\(\\sup S\\): cận trên nhỏ nhất.</li><li>\\(\\min S\\) tồn tại ⇔ \\(\\inf S\\in S\\).</li></ul>'
       + '<p>Ví dụ: \\(\\inf\\{e^x\\}=0\\) nhưng không đạt (không có min); \\(\\inf\\{1/x:x>0\\}=0\\), không đạt; \\(\\inf\\{x_1:x_1x_2\\ge1,x\\ge0\\}=0\\), không đạt (Module 3).</p>',
       kicker=M + ' · PHẦN 4',
       explain='<p>Trong tối ưu ta phải phân biệt “giá trị nhỏ nhất” (min, phải đạt được) với “cận dưới lớn nhất” (inf, có thể chỉ tiệm cận). Đó là lý do phải kiểm sự tồn tại nghiệm trước khi giải.</p>'))
add(sl('Tập đóng, bị chặn, compact',
       '<ul><li><b>Bị chặn</b>: nằm trong một hình cầu.</li><li><b>Đóng</b>: chứa mọi điểm giới hạn của mình (chứa biên).</li><li><b>Compact</b> (trong \\(\\mathbb R^n\\)): đóng và bị chặn.</li></ul>'
       + '<p>Ví dụ: \\([0,1]\\) compact; \\((0,1]\\) không đóng; \\([0,\\infty)\\) không bị chặn; đĩa \\(\\{x^2+y^2\\le2\\}\\) compact; polyhedron \\(\\{Ax\\le b\\}\\) luôn đóng.</p>',
       kicker=M + ' · PHẦN 4',
       explain='<p>Compact là “đủ nhỏ và đủ kín”: dãy điểm bất kỳ trong tập đều có dãy con hội tụ về một điểm trong tập. Tính chất này giúp chứng minh cực tiểu tồn tại.</p>'))
add(sl('Định lý Weierstrass và hàm coercive',
       '<div class="callout good"><span class="ct"><b>Weierstrass</b></span>Hàm f liên tục trên tập <b>compact</b> \\(C\\ne\\emptyset\\) đạt giá trị nhỏ nhất và lớn nhất trên C.</div>'
       '<div class="callout good"><span class="ct"><b>Coercive</b></span>f coercive nếu \\(f(x)\\to+\\infty\\) khi \\(\\|x\\|\\to\\infty\\). Khi đó f liên tục trên tập đóng \\(C\\ne\\emptyset\\) đạt cực tiểu (kể cả C không bị chặn).</div>'
       '<p>Ví dụ: \\(x_1^2+x_2^2\\) coercive: \\(\\min\\) trên \\(x_1+x_2\\ge2\\) tồn tại (\\((1,1)\\)). \\(e^x\\) không coercive: không có min trên \\(\\mathbb R\\).</p>',
       kicker=M + ' · PHẦN 4',
       explain='<p>Ví dụ: \\(\\min xy\\) trên đĩa (Module 2, Ví dụ 3) có nghiệm vì đĩa compact và \\(xy\\) liên tục — ta chắc chắn có nghiệm trước khi tìm.</p>'))

# ---------------- PHẦN 5
add(part(5, 5, 'Ôn quy hoạch tuyến tính và cầu nối sang KKT', ['Dạng chuẩn, nghiệm ở đỉnh, đồ thị', 'Đơn hình (nhắc lại)', 'Đối ngẫu và độ lệch bù', 'Kiểm tra khả thi trước khi giải'], M))
add(sl('QHTT: mô hình và đồ thị',
       '<p>Ví dụ kế hoạch sản xuất (BTDOC, tham khảo): \\(\\max4x_1+5x_2\\) s.t. \\(2x_1+x_2\\le8\\), \\(x_1+2x_2\\le7\\), \\(x_2\\le3\\), \\(x\\ge0\\).</p>'
       + table(['Đỉnh', '(0,0)', '(4,0)', '(3,2)', '(1,3)', '(0,3)'], [['\\(4x_1+5x_2\\)', '0', '16', '<b>22</b>', '19', '15']])
       + '<p>Nghiệm tối ưu \\((3,2)\\), giá trị \\(' + f4(plan['f']) + '\\) (kiểm bằng linprog). LP luôn đạt tối ưu ở đỉnh (định lý Module 1).</p>',
       kicker=M + ' · PHẦN 5',
       explain='<p>Phương pháp đồ thị: vẽ miền khả thi (đa giác), tính f tại các đỉnh, chọn đỉnh tốt nhất. Thử với công cụ LP bên dưới, đổi hệ số hàm mục tiêu và quan sát đỉnh tối ưu di chuyển.</p>'))
add(sl('Đơn hình và đối ngẫu (nhắc lại)',
       '<ul><li><b>Đơn hình</b>: đi từ đỉnh này sang đỉnh kề tốt hơn đến khi mọi ước lượng \\(\\Delta_j\\le0\\) (bài min).</li><li><b>Đối ngẫu</b>: mỗi ràng buộc gốc ↔ một biến đối ngẫu; hệ số hàm mục tiêu ↔ vế phải.</li></ul>'
       + '<p>Dual của ví dụ trên: \\(\\min8y_1+7y_2+3y_3\\) s.t. \\(2y_1+y_2\\ge4\\), \\(y_1+2y_2+y_3\\ge5\\), \\(y\\ge0\\); nghiệm \\(y=(' + ', '.join(f4(v) for v in plan_dual['y']) + ')\\), giá trị \\(' + f4(plan_dual['g']) + '\\) — <b>bằng</b> giá trị bài gốc (đối ngẫu mạnh).</p>',
       kicker=M + ' · PHẦN 5',
       explain='<p>Biến đối ngẫu \\(y_i\\) là “giá bóng” của nguyên liệu i: tăng 1 đơn vị nguyên liệu 1 thì lợi nhuận tăng \\(y_1=1\\). Nguyên liệu 3 dư (ràng buộc \\(x_2\\le3\\) không chặt: \\(2<3\\)) nên \\(y_3=0\\).</p>'))
add(sl('Độ lệch bù: tiền thân của điều kiện bù trong KKT',
       formula('Độ lệch bù (LP)', r'y_i\,(b_i-a_i^\top x)=0,\qquad x_j\,(a^{j\top}y-c_j)=0')
       + '<p>Ràng buộc gốc không chặt ⇒ biến đối ngẫu tương ứng bằng 0 (ví dụ \\(y_3=0\\) vì \\(x_2=2<3\\)). Đây chính là điều kiện bù \\(\\lambda_ig_i=0\\) của <b>KKT</b> (Module 2) áp dụng cho LP.</p>'
       + callout('good', 'Cầu nối', '<p>KKT của LP = khả thi gốc + khả thi đối ngẫu + độ lệch bù. Module 2 tổng quát hóa cho hàm mục tiêu và ràng buộc phi tuyến; Module 3 cho hàm mục tiêu bậc hai.</p>'),
       kicker=M + ' · PHẦN 5',
       explain='<p>Mỗi đỉnh tối ưu của LP là điểm KKT với nhân tử = biến đối ngẫu. Nếu bạn nhớ độ lệch bù, bạn đã hiểu 60% điều kiện KKT.</p>'))
add(sl('Kiểm tra khả thi trước khi giải',
       '<p>Bài “thức ăn gia súc” (Studocu C11, tham khảo): \\(\\min50x_1+35x_2+25x_3\\) với \\(2x_1+x_2+3x_3\\ge60\\), \\(20\\le5x_1+4x_2+2x_3\\le40\\), \\(3x_1+2x_2+5x_3=50\\).</p>'
       '<p>Từ ràng buộc đẳng thức \\(3x_1+2x_2+5x_3=50\\): tỉ số \\(D_1/D_3\\) lớn nhất là \\(2/3\\) (tại \\(T_1\\)) nên \\(D_1\\le\\tfrac23\\cdot50\\approx33.3<60\\): <b>bài toán vô nghiệm</b> (miền rỗng); bài đối ngẫu không bị chặn (linprog xác nhận: primal infeasible, dual unbounded).</p>'
       + callout('warn', 'Bài học', '<p>Trước khi giải một bài toán từ đề, hãy kiểm tra miền khả thi khác rỗng bằng một lập luận nhanh (cận trên/dưới). Đề nguồn cũ hoặc chép sai số rất hay gây ra bài vô nghiệm.</p>'),
       kicker=M + ' · PHẦN 5',
       explain='<p>Chỉ một phép nhân đơn giản (\\(2/3\\times50\\)) đã chỉ ra bài toán không có phương án. Hãy tập thói quen tìm cận trước khi tính toán dài.</p>'))
add(sl('Tổng kết Module 0',
       '<ul><li>Bài toán tối ưu = (f, ràng buộc, biến); địa phương ≠ toàn cục.</li><li>\\(\\nabla f\\perp\\) đường mức; \\(-\\nabla f\\) giảm nhanh nhất; Hessian đo độ cong.</li><li>Điểm dừng \\(\\nabla f=0\\); phân loại bằng Hessian.</li><li>Cực tiểu tồn tại khi compact (Weierstrass) hoặc coercive.</li><li>LP: nghiệm ở đỉnh; đối ngẫu mạnh; độ lệch bù ⇒ KKT.</li></ul>'
       '<p>Tiếp theo: <b>Module 1</b> — tập lồi và hàm lồi.</p>',
       kicker=M + ' · TỔNG KẾT',
       explain='<p>Nếu bạn làm ngân hàng câu hỏi Module 0 đạt trên 80%, bạn đã sẵn sàng cho Module 1. Nếu chưa, hãy làm lại các câu sai (nút “chỉ câu làm sai”).</p>'))

# =====================================================================  SECTIONS
SECTIONS = []
SECTIONS.append(('cong-thuc', 'Công thức cốt lõi',
    formula('Bài toán tối ưu', r'\min f(x)\ \ \text{s.t.}\ g_i(x)\le0,\ h_j(x)=0')
    + formula('Gradient và Hessian', r'\nabla f=\Big(\tfrac{\partial f}{\partial x_i}\Big),\qquad\nabla^2f=\Big(\tfrac{\partial^2f}{\partial x_i\partial x_j}\Big)')
    + formula('Taylor bậc hai', r'f(x+d)\approx f(x)+\nabla f(x)^\top d+\tfrac12d^\top\nabla^2f(x)d')
    + formula('Điều kiện cấp 1 và 2', r'\nabla f(x^*)=0,\quad\nabla^2f(x^*)\succeq0\ (\text{cần});\quad\nabla^2f(x^*)\succ0\ (\text{đủ})')
    + formula('Giá trị riêng', r'\det(A-\lambda I)=0,\quad\mathrm{tr}A=\sum\lambda_i,\quad\det A=\prod\lambda_i')
    + formula('Cauchy–Schwarz', r'|u^\top v|\le\|u\|\|v\|')))
SECTIONS.append(('lich-su', 'Bối cảnh lý thuyết và lịch sử', callout('hist', '📜 Bối cảnh lý thuyết & lịch sử',
    '<p>Điều kiện “đạo hàm bằng 0 tại cực trị” gắn với Pierre de Fermat (thế kỷ XVII). Định lý giá trị cực trị cho hàm liên tục trên tập compact mang tên Karl Weierstrass (thế kỷ XIX). Phương pháp gradient (đi theo hướng dốc nhất) được Augustin-Louis Cauchy đề xuất năm 1847 để giải hệ phương trình.</p>'
    '<p>Đối ngẫu trong quy hoạch tuyến tính được hình thành khoảng 1947 (Dantzig, von Neumann); thuật toán đơn hình do George Dantzig đề xuất năm 1947 — nền cho môn Quy hoạch tuyến tính bạn đã học trước đó.</p>')))
S_case = ('<p>Bài toán <b>kế hoạch sản xuất</b> (BTDOC Ch.2, tham khảo): xí nghiệp làm hai sản phẩm \\(S_1,S_2\\) từ ba nguyên liệu; lợi nhuận 4 và 5 triệu đồng/đơn vị; dự trữ \\(N_1=8\\), \\(N_2=7\\), \\(N_3=3\\).</p>'
          + table(['', 'S₁', 'S₂', 'Dự trữ'], [['N₁', '2', '1', '8'], ['N₂', '1', '2', '7'], ['N₃', '0', '1', '3'], ['Lãi', '4', '5', '']])
          + steps(['Biến: \\(x_1,x_2\\) số sản phẩm; mô hình \\(\\max4x_1+5x_2\\), \\(2x_1+x_2\\le8\\), \\(x_1+2x_2\\le7\\), \\(x_2\\le3\\), \\(x\\ge0\\).',
                   'Các đỉnh của miền (code): ' + '; '.join('(' + ', '.join(f4(t) for t in v['v']) + ') → ' + f4(v['f']) for v in R['m0_btdoc_plan_vertices']) + '.',
                   'Nghiệm tối ưu \\((3,2)\\), lãi \\(22\\) triệu; hai nguyên liệu \\(N_1,N_2\\) dùng hết, \\(N_3\\) dư 1 đơn vị.',
                   'Đối ngẫu: \\(y=(1,2,0)\\), giá trị \\(22\\); nguyên liệu \\(N_1\\) đáng giá 1 triệu/đơn vị, \\(N_2\\) đáng giá 2 triệu, \\(N_3\\) không có giá trị biên (dư).',
                   'Kiểm KKT/độ lệch bù: \\(y_3(3-x_2)=0\\cdot1=0\\); \\(x_1(2y_1+y_2-4)=3\\cdot0=0\\); \\(x_2(y_1+2y_2+y_3-5)=2\\cdot0=0\\) ✓.'])
          + callout('good', 'Điều học được', '<p>Ràng buộc chặt ↔ biến đối ngẫu dương. Đó là ngôn ngữ chung của LP và KKT.</p>')
          + callout('warn', 'Ghi chú về nguồn BTDOC', '<p>Tài liệu BTDOC ghi ví dụ 4 mặt hàng có kết quả \\((0,15,0,0)\\), \\(f=120\\). Kiểm bằng code: LP tối ưu là \\((0,15.385,0,0)\\), \\(f=' + f4(four['f']) + '\\); giá trị 120 là nghiệm <b>nguyên</b> (ví dụ \\((0,15,0,0)\\) hoặc \\((0,14,2,0)\\)). Đây là lý do các tài liệu ngoài cần đối chiếu.</p>'))
SECTIONS.append(('case-study', '🔎 Case study: kế hoạch sản xuất và biến đối ngẫu', S_case))

def ex(t, b): return solution(t, b)
EXS = ''
EXS += ex('Ví dụ 1 — gradient và Hessian của \\(f=x^2y+3xy^2-2x\\)',
    steps(['\\(f_x=2xy+3y^2-2\\), \\(f_y=x^2+6xy\\) ⇒ \\(\\nabla f(1,2)=(4+12-2,\\ 1+12)=(14,13)\\).',
           '\\(f_{xx}=2y\\), \\(f_{xy}=2x+6y\\), \\(f_{yy}=6x\\) ⇒ \\(H(1,2)=\\begin{pmatrix}4&14\\\\14&6\\end{pmatrix}\\) (code khớp: ' + str(R['m0_grad_ex']['H_at_1_2']) + ').',
           'Hướng giảm nhanh nhất tại \\((1,2)\\): \\(-\\nabla f=(-14,-13)\\).']))
EXS += ex('Ví dụ 2 — giá trị riêng của \\(\\begin{pmatrix}2&-1\\\\-1&2\\end{pmatrix}\\)',
    steps(['\\(\\det(A-\\lambda I)=(2-\\lambda)^2-1=\\lambda^2-4\\lambda+3=0\\).', '\\(\\lambda=1,3\\); vết \\(=4\\), định thức \\(=3\\) ✓.', 'Cả hai dương ⇒ xác định dương.']))
EXS += ex('Ví dụ 3 — nghịch đảo ma trận 3×3 (BTDOC)',
    steps(['\\(A=\\begin{pmatrix}1&2&3\\\\2&5&3\\\\1&0&8\\end{pmatrix}\\), \\(\\det A=1\\cdot(40-0)-2\\cdot(16-3)+3\\cdot(0-5)=40-26-15=-1\\) ✓.',
           'Các phần bù đại số (cofactor): \\(A_{11}=40,A_{12}=-13,A_{13}=-5,A_{21}=-16,A_{22}=5,A_{23}=2,A_{31}=-9,A_{32}=3,A_{33}=1\\).',
           '\\(A^{-1}=\\dfrac1{\\det A}[A_{ji}]=-\\begin{pmatrix}40&-16&-9\\\\-13&5&3\\\\-5&2&1\\end{pmatrix}=\\begin{pmatrix}-40&16&9\\\\13&-5&-3\\\\5&-2&-1\\end{pmatrix}\\).',
           'Kiểm bằng code: \\(A^{-1}A=I\\) (' + str(inv['check_AinvA']) + ').']))
EXS += ex('Ví dụ 4 — Cramer (BTDOC)',
    steps(['\\(A=\\begin{pmatrix}1&0&2\\\\3&4&6\\\\-1&-2&3\\end{pmatrix}\\), \\(\\det A=20\\) (code); tính \\(\\det A_1,\\det A_2,\\det A_3\\) bằng cách thay cột.', 'Nghiệm \\(x=(-2,\\ 3,\\ 4)\\) (code).', 'Kiểm: \\(x_1+2x_3=-2+8=6\\) ✓; \\(3x_1+4x_2+6x_3=-6+12+24=30\\) ✓; \\(-x_1-2x_2+3x_3=2-6+12=8\\) ✓.']))
EXS += ex('Ví dụ 5 — Taylor bậc hai của \\(e^x+y^2\\)',
    steps(['Tại gốc: \\(f=1\\), \\(\\nabla f=(1,0)\\), \\(\\nabla^2f=\\mathrm{diag}(1,2)\\).', 'Taylor: \\(1+x+\\tfrac12(x^2+2y^2)=1+x+\\tfrac12x^2+y^2\\).', 'Tại \\((0.1,0.2)\\): \\(1+0.1+0.005+0.04=1.145\\); giá trị thật \\(e^{0.1}+0.04=1.14517\\) (sai số \\(\\approx1.7\\times10^{-4}\\), bậc 3).']))
EXS += ex('Ví dụ 6 — phân loại điểm dừng',
    '<p>(a) \\(f=x^2+xy+y^2-3x\\): \\(\\nabla f=0\\Rightarrow(2,-1)\\); \\(H=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}\\), giá trị riêng \\(1,3\\) ⇒ cực tiểu; \\(f=-3\\).</p><p>(b) \\(f=x^3-3x+y^2\\): \\((1,0)\\): \\(H=\\mathrm{diag}(6,2)\\) ⇒ cực tiểu địa phương, \\(f=-2\\); \\((-1,0)\\): \\(H=\\mathrm{diag}(-6,2)\\) ⇒ yên ngựa, \\(f=2\\).</p>')
EXS += ex('Ví dụ 7 — kế hoạch sản xuất bằng đồ thị và đối ngẫu',
    '<p>Các đỉnh khả thi và giá trị: ' + '; '.join('(' + ', '.join(f4(t) for t in v['v']) + ') → ' + f4(v['f']) for v in R['m0_btdoc_plan_vertices']) + '. Lớn nhất 22 tại \\((3,2)\\). Dual: \\(y=(1,2,0)\\), \\(8+14+0=22\\).</p>')
EXS += ex('Ví dụ 8 — bài toán thức ăn gia súc: phát hiện vô nghiệm',
    '<p>Ràng buộc đẳng thức \\(D_3=3x_1+2x_2+5x_3=50\\). Với \\(x\\ge0\\), tỉ số \\(D_1/D_3\\) của từng loại thức ăn là \\(\\tfrac23,\\tfrac12,\\tfrac35\\), đều \\(\\le\\tfrac23\\). Do đó \\(D_1=2x_1+x_2+3x_3\\le\\tfrac23D_3=\\tfrac{100}3\\approx33.3\\). Yêu cầu \\(D_1\\ge60\\) mâu thuẫn ⇒ miền rỗng. Code (linprog): primal “infeasible”, dual “unbounded”.</p>')
EXS += ex('Ví dụ 9 — ba lô 0-1 bằng quy hoạch động (Studocu C13, tham khảo)',
    '<p>Sức chứa \\(W=5\\); vật (khối lượng, giá trị): \\((2,3),(3,4),(4,5),(5,8)\\). Bảng DP (dòng i, cột \\(c=0..5\\)):</p>'
    + table(['i', 'c=0', '1', '2', '3', '4', '5'], [[str(i)] + [str(v) for v in row] for i, row in enumerate(R['m0_knap13_table'])])
    + '<p>Giá trị tối ưu \\(8\\) (chọn vật 4 một mình, 5 kg → 8; hai vật \\((2,3)+(3,4)\\) cho 7). Vét cạn xác nhận. Đây là bài toán rời rạc (không lồi), ngoài trọng tâm môn.</p>')
SECTIONS.append(('vi-du', 'Ví dụ chi tiết (có lời giải từng bước)', '<p>Mọi con số do script kiểm chứng. Bài toán từ BTDOC/Studocu chỉ để tham khảo.</p>' + EXS))
SECTIONS.append(('so-do', 'Sơ đồ tổng hợp', fig('d1-phan-loai-toi-uu', 'Các lớp bài toán tối ưu') + fig('d5-lo-trinh', 'Lộ trình bốn module')))
SECTIONS.append(('tuong-tac', 'Thực hành tương tác', widget('grad-lab') + widget('lp-lab') + widget('hessian-lab')))
SECTIONS.append(('bay', 'Cảnh báo bẫy diễn giải sai',
    callout('warn', 'Bẫy 1 — Nhầm inf với min', '<p>\\(\\inf\\) có thể không đạt (ví dụ \\(e^x\\)). Chỉ khi đạt mới là min.</p>')
    + callout('warn', 'Bẫy 2 — \\(\\nabla f=0\\) ⇒ cực tiểu', '<p>Không đúng: có thể là cực đại hoặc điểm yên ngựa; \\(x^3\\) có \\(f^{\\prime}(0)=0\\) nhưng không cực trị.</p>')
    + callout('warn', 'Bẫy 3 — Thứ tự nhân ma trận', '<p>\\(AB\\ne BA\\); \\((AB)^\\top=B^\\top A^\\top\\).</p>')
    + callout('warn', 'Bẫy 4 — Hessian tại một điểm', '<p>Cực tiểu địa phương cần Hessian \\(\\succeq0\\) tại điểm dừng; nhưng để khẳng định toàn cục cần tính lồi trên toàn miền.</p>')
    + callout('warn', 'Bẫy 5 — Tin đề nguồn cũ', '<p>Bài “thức ăn gia súc” vô nghiệm; ví dụ 4 mặt hàng của BTDOC ghi nghiệm nguyên thay vì nghiệm LP. Hãy tự kiểm bằng code.</p>')))
READING = ('<ul><li>Boyd &amp; Vandenberghe: Ch.1 “Introduction” (tr.1) và Phụ lục A “Mathematical background” (ký hiệu, chuẩn, hàm, đạo hàm) — file <code>bv_cvxbook.pdf</code>.</li>'
           '<li>Tài liệu ôn LP: các file <code>QHTT/</code> của môn cũ (đơn hình, đối ngẫu, vận tải); xem thư mục <code>00_Kien_thuc_mon_cu_QHTT_VTH</code>.</li>'
           '<li>Chương 1 BTDOC (Studocu): chỉ tham khảo, rất cũ và khác ngành; đã đối chiếu các ví dụ số bằng code.</li>'
           '<li>Tiếp theo: Module 1 — tập lồi và hàm lồi.</li></ul>')
