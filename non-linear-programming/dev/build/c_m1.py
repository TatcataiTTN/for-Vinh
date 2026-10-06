"""Nội dung Module 1 — Tập lồi & hàm lồi (bám Slides/1_Kien thuc ve ham loi va tap loi_250418.pdf)."""
import numpy as np
from helpers import *

M = 'MODULE 1'
LEAD = 'Nền tảng của toàn bộ môn tối ưu lồi: tập lồi, bao lồi, siêu phẳng, polyhedron, hàm lồi và tiêu chuẩn Hessian. Đây cũng là chương nối trực tiếp từ giải tích lồi trong môn Quy hoạch tuyến tính (Chương II) sang tối ưu lồi.'
META = ['Nguồn: Slide 1, ORLab Phenikaa (54 trang)', 'Boyd & Vandenberghe: Ch.2–3', 'Thời lượng gợi ý: 4–5 giờ']
OBJECTIVES = [
    'Nêu định nghĩa và kiểm tra tính lồi của một tập bằng định nghĩa, bằng phép giao/tổng, hoặc nhận ra polyhedron, hình cầu, ellipsoid.',
    'Phát biểu và dùng bất đẳng thức Jensen, điều kiện cấp 1 và cấp 2 của hàm lồi.',
    'Tính Hessian và kết luận lồi/lõm/không xác định bằng giá trị riêng hoặc minor chính, tránh bẫy “minor dẫn đầu chưa đủ cho nửa xác định dương”.',
    'Nhận biết các phép toán bảo toàn tính lồi và chứng minh được các bài tập điển hình (max của hàm lồi, tổng Minkowski, khoảng cách tới tập lồi).',
]

# ---- số liệu tính lúc build (không gõ tay) ----
mat = R['m1_mat']
ex_slide = R['m1_ex_slide']
xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0]); ys = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
Amat = np.column_stack([np.ones_like(xs), xs])
theta = np.linalg.solve(Amat.T @ Amat, Amat.T @ ys)
Hls = 2 * Amat.T @ Amat
eig_ls = np.linalg.eigvalsh(Hls)
res = float(np.sum((Amat @ theta - ys) ** 2))

def f4(x): return ('%.4f' % x).rstrip('0').rstrip('.')

DECK = []
add = DECK.append

# ====================================================== slide 0: mở đầu
add(sl('Tối ưu lồi bắt đầu từ hai khái niệm: tập lồi và hàm lồi',
       '<p>Module này bám sát <b>Slide 1</b> của ORLab (Phenikaa), 54 trang, gồm 5 phần:</p>'
       '<ol><li>Tập lồi: định nghĩa, ví dụ, phép giao/tổng, phản ví dụ hợp</li><li>Bao lồi, siêu phẳng, hình cầu, ellipsoid, polyhedron</li>'
       '<li>Hàm lồi: Jensen, lồi chặt/lõm, điều kiện cấp 1, epigraph</li><li>Điều kiện cấp 2: Hessian, xác định dương</li><li>Phép toán bảo toàn tính lồi và bài tập</li></ol>'
       + callout('info', 'Vì sao quan trọng?', '<p>Với bài toán tối ưu lồi, <b>mọi cực tiểu địa phương đều là cực tiểu toàn cục</b> và điều kiện KKT (Module 2) trở thành điều kiện cần và đủ. Toàn bộ sức mạnh đó xuất phát từ hai định nghĩa trong module này.</p>'),
       kicker=M + ' · MỞ ĐẦU', img='m1:1',
       explain='<p>Đây là trang bìa của slide. “Tối ưu lồi” là lớp bài toán tối ưu dễ giải nhất: một khi bạn xác nhận được hàm mục tiêu và miền ràng buộc đều lồi, bạn có thể tin tưởng mọi điểm dừng là nghiệm tối ưu thật sự.</p>'))

# ====================================================== PHẦN 1
add(part(1, 5, 'Tập lồi', ['Đường thẳng, đoạn thẳng, tổ hợp \\(\\theta x+(1-\\theta)y\\)', 'Định nghĩa và ví dụ', 'Giao, tổng: lồi; hợp: không nhất thiết lồi'], M))
add(sl('Đường thẳng và đoạn thẳng',
       '<p>Với hai điểm \\(x,y\\in\\mathbb R^n\\), xét điểm \\(z=\\theta x+(1-\\theta)y\\).</p><ul><li>\\(\\theta\\in\\mathbb R\\): \\(z\\) chạy trên <b>đường thẳng</b> qua \\(x\\) và \\(y\\).</li><li>\\(\\theta\\in[0,1]\\): \\(z\\) chạy trên <b>đoạn thẳng</b> nối \\(x\\) và \\(y\\).</li></ul>'
       + formula('Tổ hợp lồi của hai điểm', r'z=\theta x+(1-\theta)y,\qquad \theta\in[0,1]',
                 [(r'\theta=1', 'z trùng x'), (r'\theta=0', 'z trùng y'), (r'\theta=\tfrac12', 'z là trung điểm')]),
       kicker=M + ' · PHẦN 1', img='m1:3',
       explain='<p>Hãy hình dung \\(\\theta\\) như “tỉ lệ pha trộn”: \\(\\theta=0.3\\) nghĩa là lấy 30% từ x và 70% từ y. Trộn theo tỉ lệ không âm cho ra các điểm nằm <i>giữa</i> hai điểm; cho phép tỉ lệ âm hoặc lớn hơn 1 thì điểm chạy ra ngoài, trên phần kéo dài của đường thẳng.</p>'))
add(sl('Tập lồi: định nghĩa và ví dụ',
       '<div class="callout good"><span class="ct"><b>Định nghĩa</b></span>Tập \\(C\\ne\\emptyset\\) là lồi nếu \\(x,y\\in C\\Rightarrow \\theta x+(1-\\theta)y\\in C\\ \\ \\forall\\theta\\in[0,1]\\).</div>'
       '<p>Ví dụ tập lồi (slide tr.7): tập rỗng (quy ước), một điểm, toàn bộ \\(\\mathbb R^n\\), một đoạn thẳng bất kỳ.</p>'
       '<p>Không lồi: vành khuyên, chữ L, hợp hai hình tròn rời nhau (thử ở công cụ tương tác bên dưới).</p>',
       kicker=M + ' · PHẦN 1', img='m1:7',
       explain='<p>Cách kiểm tra bằng hình: chọn hai điểm bất kỳ trong tập, nối bằng một sợi dây. Nếu sợi dây luôn nằm trọn trong tập thì tập lồi. Chỉ cần <i>một cặp</i> điểm có dây chui ra ngoài là tập không lồi.</p>'))
add(sl('Giao và tổng của tập lồi là lồi; hợp thì không',
       '<ul><li>\\(S_1\\cap S_2\\) lồi.</li><li>\\(S_1+S_2=\\{x_1+x_2\\mid x_1\\in S_1,x_2\\in S_2\\}\\) lồi.</li><li>Hợp \\(S_1\\cup S_2\\) <b>không</b> nhất thiết lồi: \\([0,1]\\cup[2,3]\\) không chứa \\(1.5\\).</li></ul>'
       + callout('warn', 'Câu hỏi của slide tr.9', '<p>“Hợp của hai tập lồi có phải là tập lồi?” — Không. Ví dụ ở trên là phản ví dụ.</p>'),
       kicker=M + ' · PHẦN 1', img='m1:9',
       explain='<p>Giao giữ được tính lồi vì điểm z phải thuộc <i>cả hai</i> tập, mà từng tập đều “đóng kín” với phép pha trộn. Hợp thì không vì hai tập có thể nằm rời nhau, sợi dây nối hai điểm ở hai tập khác nhau đi qua khoảng trống.</p>'))

# ====================================================== PHẦN 2
add(part(2, 5, 'Bao lồi, siêu phẳng, hình cầu, polyhedron', ['Bao lồi và tổ hợp lồi', 'Tích vô hướng, chuẩn, siêu phẳng, nửa không gian', 'Hình cầu, ellipsoid, polyhedron, polytope'], M))
add(sl('Bao lồi',
       '<p>Điểm \\(\\theta_1x_1+\\dots+\\theta_kx_k\\) với \\(\\theta_i\\ge0\\), \\(\\sum\\theta_i=1\\) là <b>tổ hợp lồi</b> của \\(x_1,\\dots,x_k\\).</p>'
       + formula('Bao lồi', r'\mathrm{conv}\,C=\Big\{\sum_{i=1}^k\theta_ix_i\ \Big|\ x_i\in C,\ \theta_i\ge0,\ \sum_{i=1}^k\theta_i=1\Big\}')
       + '<p>Bao lồi là tập lồi <b>nhỏ nhất</b> chứa C. Bao lồi của 3 điểm không thẳng hàng là một tam giác đặc.</p>',
       kicker=M + ' · PHẦN 2', img='m1:11',
       explain='<p>Hình dung C là các chiếc đinh đóng trên tấm ván; bao lồi là hình dạng của sợi dây thun căng quanh các chiếc đinh đó và phần bên trong nó.</p>'))
add(sl('Tích vô hướng và chuẩn Euclid',
       formula('Tích vô hướng', r'\langle u,v\rangle=u_1v_1+\dots+u_nv_n=u^\top v') + formula('Chuẩn Euclid', r'\|v\|=\sqrt{v_1^2+\dots+v_n^2}=\sqrt{v^\top v}')
       + '<p>Ví dụ: \\(u=(1,2,3),v=(4,-5,6)\\Rightarrow\\langle u,v\\rangle=12\\); \\(\\|(3,4)\\|=5\\).</p>',
       kicker=M + ' · PHẦN 2', img='m1:13',
       explain='<p>Tích vô hướng đo mức “cùng hướng” của hai vectơ; chuẩn đo độ dài. Hai công cụ này dùng để định nghĩa siêu phẳng, hình cầu và (ở module sau) gradient.</p>'))
add(sl('Siêu phẳng và nửa không gian',
       formula('Siêu phẳng', r'\{x\in\mathbb R^n\mid a^\top x=b\},\quad a\ne0') + formula('Nửa không gian đóng', r'\{x\in\mathbb R^n\mid a^\top x\le b\},\quad a\ne0')
       + '<ul><li>a là <b>vectơ pháp tuyến</b> của siêu phẳng.</li><li>Một siêu phẳng chia \\(\\mathbb R^n\\) thành hai nửa không gian.</li><li>Cả hai đều là tập lồi.</li></ul>',
       kicker=M + ' · PHẦN 2', img='m1:14',
       explain='<p>Trong mặt phẳng \\(\\mathbb R^2\\), siêu phẳng là một đường thẳng và nửa không gian là một nửa mặt phẳng — chính là “một ràng buộc \\(\\le\\)” trong bài toán quy hoạch tuyến tính bạn đã học.</p>'))
add(sl('Hình cầu và ellipsoid',
       formula('Hình cầu', r'B(x_c,r)=\{x\mid\|x-x_c\|\le r\}=\{x\mid(x-x_c)^\top(x-x_c)\le r^2\}')
       + formula('Ellipsoid', r'E=\{x\mid(x-x_c)^\top P(x-x_c)\le1\},\quad P=P^\top\succeq0')
       + '<p>Cả hai là tập lồi. Khi \\(P\\succ0\\) ellipsoid bị chặn; \\(P=r^{-2}I\\) cho hình cầu.</p>',
       kicker=M + ' · PHẦN 2', img='m1:18',
       explain='<p>Ellipsoid là “hình cầu bị kéo giãn”. Ma trận P quyết định độ dài các trục: giá trị riêng lớn của P ứng với trục ngắn.</p>'))
add(sl('Polyhedron và polytope',
       formula('Polyhedron', r'P=\{x\mid a_j^\top x\le b_j\ (j=1..m),\ c_j^\top x=d_j\ (j=1..p)\}')
       + '<ul><li>Polyhedron = giao hữu hạn các nửa không gian đóng (và siêu phẳng).</li><li><b>Polytope</b> = polyhedron bị chặn.</li><li>Miền chấp nhận của một bài toán QHTT chính là một polyhedron.</li></ul>',
       kicker=M + ' · PHẦN 2', img='m1:22',
       explain='<p>Mỗi ràng buộc tuyến tính cắt ra một nửa không gian; đặt nhiều ràng buộc cùng lúc là lấy giao. Kết quả là một “khối nhiều mặt phẳng” (đa diện lồi). Chính vì thế nghiệm tối ưu của QHTT nằm ở đỉnh.</p>'))
add(sl('Cách chứng minh một tập là lồi',
       '<ol><li><b>Dùng định nghĩa:</b> lấy \\(x,y\\in C\\), \\(\\theta\\in[0,1]\\), chứng minh \\(\\theta x+(1-\\theta)y\\in C\\).</li>'
       '<li><b>Nhận dạng:</b> siêu phẳng, nửa không gian, hình cầu, ellipsoid, polyhedron.</li><li><b>Phép toán:</b> giao, tổng, ảnh/tiền ảnh qua ánh xạ affine, nhân vô hướng \\(k\\Omega\\).</li>'
       '<li><b>Tập mức dưới:</b> \\(\\{x\\mid f(x)\\le c\\}\\) với f lồi.</li></ol>'
       + callout('warn', 'Bẫy', '<p>Đừng kết luận “lồi” chỉ vì thử được vài cặp điểm; ngược lại chỉ cần một cặp vi phạm là đủ kết luận “không lồi”.</p>'),
       kicker=M + ' · PHẦN 2',
       explain='<p>Bốn cách trên xếp theo độ nhanh: nếu nhận dạng được tập là giao các nửa không gian thì xong ngay; chỉ khi không nhận dạng được mới quay về định nghĩa.</p>'))

# ====================================================== PHẦN 3
add(part(3, 5, 'Hàm lồi', ['Miền hữu hiệu và bất đẳng thức Jensen', 'Lồi chặt, lõm, đồ thị và epigraph', 'Điều kiện cấp 1'], M))
add(sl('Hàm lồi và bất đẳng thức Jensen',
       '<p>\\(f:\\mathbb R^n\\to\\mathbb R\\) là <b>lồi</b> nếu \\(\\mathrm{dom}\\,f:=\\{x\\mid f(x)<+\\infty\\}\\) là tập lồi và:</p>'
       + formula('Jensen', r'f(\theta x+(1-\theta)y)\ \le\ \theta f(x)+(1-\theta)f(y),\quad \forall x,y\in\mathrm{dom}\,f,\ \theta\in(0,1)')
       + '<ul><li><b>lồi chặt</b>: bất đẳng thức chặt (\\(<\\)) khi \\(x\\ne y\\)</li><li><b>lõm</b>: \\(-f\\) lồi; <b>lõm chặt</b>: \\(-f\\) lồi chặt</li></ul>',
       kicker=M + ' · PHẦN 3', img='m1:25',
       explain='<p>Vế trái là giá trị của hàm ở điểm “pha trộn”; vế phải là giá trị pha trộn của hai giá trị hàm (nằm trên dây cung). Hàm lồi có dạng “cái bát”: giá trị ở giữa luôn thấp hơn hoặc bằng trung bình giá trị hai đầu.</p>'))
add(sl('Ý nghĩa hình học: dây cung nằm trên đồ thị',
       '<p>Hàm một biến lồi ⇔ mọi dây cung nối hai điểm trên đồ thị nằm <b>phía trên</b> đồ thị. Hàm lõm ngược lại.</p>'
       '<p>Thử ngay ở công cụ “Kiểm tra bất đẳng thức Jensen” bên dưới: kéo x, y, θ và quan sát khoảng cách giữa dây cung và đồ thị.</p>',
       kicker=M + ' · PHẦN 3', img='m1:26',
       explain='<p>Hình bên trái (convex function): dây cung nối \\((x,f(x))\\) và \\((y,f(y))\\) nằm trên đồ thị. Hình bên phải (concave function): dây cung nằm dưới đồ thị.</p>'))
add(sl('Điều kiện cấp 1',
       '<p>Giả sử f khả vi. Khi đó f lồi ⇔ \\(\\mathrm{dom}\\,f\\) lồi và</p>'
       + formula('Điều kiện cấp 1', r'f(y)\ \ge\ f(x)+\nabla f(x)^\top(y-x),\quad\forall x,y\in\mathrm{dom}\,f')
       + '<p>Đồ thị của hàm lồi nằm phía trên mọi “mặt phẳng tiếp xúc”. Hệ quả: nếu \\(\\nabla f(x^*)=0\\) thì \\(x^*\\) là cực tiểu <b>toàn cục</b>.</p>',
       kicker=M + ' · PHẦN 3', img='m1:27',
       explain='<p>Vế phải là xấp xỉ tuyến tính (tiếp tuyến) của f tại x. Hàm lồi luôn “nằm trên” tiếp tuyến của nó. Nếu tiếp tuyến nằm ngang (\\(\\nabla f=0\\)) thì f không thể thấp hơn giá trị đó ở bất kỳ nơi nào.</p>'))
add(sl('Đồ thị và epigraph',
       formula('Graph và Epigraph', r'\mathrm{graph}=\{(x,f(x))\},\qquad \mathrm{epi}\,f=\{(x,t)\mid x\in\mathrm{dom}\,f,\ f(x)\le t\}\subseteq\mathbb R^{n+1}')
       + '<p><b>f lồi ⇔ epi f là tập lồi</b>: chiếc cầu nối giữa “hàm lồi” và “tập lồi”.</p>',
       kicker=M + ' · PHẦN 3', img='m1:52',
       explain='<p>Epigraph là “phần đất nằm trên đồ thị” (epi = ở trên). Một hàm là lồi nếu và chỉ nếu vùng đất ở trên đồ thị của nó là một tập lồi.</p>'))
add(sl('Ví dụ trong \\(\\mathbb R\\)',
       '<ul><li>\\(e^{ax}\\) lồi trên \\(\\mathbb R\\), mọi \\(a\\)</li><li>\\(x^a\\) lồi trên \\(\\mathbb R_{++}\\) nếu \\(a\\ge1\\) hoặc \\(a\\le0\\); lõm nếu \\(a\\in[0,1]\\)</li><li>\\(\\log x\\) lõm trên \\(\\mathbb R_{++}\\)</li></ul>'
       '<p>Kiểm bằng \\(f^{\\prime\\prime}\\): \\((e^{ax})^{\\prime\\prime}=a^2e^{ax}\\ge0\\); \\((x^a)^{\\prime\\prime}=a(a-1)x^{a-2}\\); \\((\\log x)^{\\prime\\prime}=-1/x^2<0\\).</p>',
       kicker=M + ' · PHẦN 3', img='m1:45',
       explain='<p>Trong một chiều, kiểm tra tính lồi rất nhanh: chỉ cần đạo hàm cấp hai không âm trên miền xác định. Ví dụ \\(x^2\\) có \\(f^{\\prime\\prime}=2>0\\) nên lồi.</p>'))

# ====================================================== PHẦN 4
add(part(4, 5, 'Điều kiện cấp 2: Hessian', ['Ma trận Hessian và định thức con chính', 'Xác định dương, nửa xác định dương', 'Ví dụ: hàm toàn phương'], M))
add(sl('Ma trận Hessian',
       formula('Hessian', r'H(x)=\nabla^2f(x)=\Big[\frac{\partial^2f}{\partial x_i\partial x_j}\Big]_{i,j=1}^n')
       + '<p>Nếu các đạo hàm riêng cấp hai liên tục thì H đối xứng. Định thức con chính (dẫn đầu): \\(\\Delta_k=\\det H_k\\), \\(H_k\\) là ma trận con góc trên bên trái cỡ \\(k\\times k\\).</p>',
       kicker=M + ' · PHẦN 4', img='m1:28',
       explain='<p>Hessian là “đạo hàm cấp hai dạng ma trận”; nó mô tả độ cong của đồ thị theo mọi hướng. Đường chéo cho độ cong theo từng trục, các phần tử ngoài đường chéo cho độ cong “xoắn” giữa hai biến.</p>'))
add(sl('Điều kiện cấp 2',
       '<p>Nếu f khả vi hai lần thì:</p>' + formula('Điều kiện cấp 2', r'f\ \text{lồi}\iff \mathrm{dom}\,f\ \text{lồi và}\ \nabla^2f(x)\succeq0\ \ \forall x\in\mathrm{dom}\,f')
       + '<ul><li>\\(\\nabla^2f(x)\\succ0\\ \\forall x\\Rightarrow f\\) <b>lồi chặt</b> (chiều ngược lại sai: \\(x^4\\)).</li><li>Trong \\(\\mathbb R\\): \\(f^{\\prime\\prime}(x)\\ge0\\).</li></ul>',
       kicker=M + ' · PHẦN 4', img='m1:31',
       explain='<p>Điều kiện này chỉ ra Hessian phải “không âm” <b>ở mọi điểm</b>. Nếu chỉ kiểm được ở vài điểm thì không đủ để kết luận f lồi; cần chứng minh cho cả miền.</p>'))
add(sl('Ma trận xác định dương và nửa xác định dương',
       '<ul><li>\\(A\\succ0\\) (xác định dương): \\(x^\\top Ax>0\\ \\forall x\\ne0\\).</li><li>\\(A\\succeq0\\) (nửa xác định dương): \\(x^\\top Ax\\ge0\\ \\forall x\\).</li><li>\\(A\\succ0\\Rightarrow A\\succeq0\\).</li></ul>'
       '<p>Ví dụ: \\(A=I\\) xác định dương vì \\(x^\\top Ax=x_1^2+x_2^2>0\\) với \\(x\\ne0\\); hàm \\(f=x_1^2+x_2^2\\) lồi.</p>',
       kicker=M + ' · PHẦN 4', img='m1:36',
       explain='<p>\\(x^\\top Ax\\) là “dạng toàn phương”: nó biến mỗi vectơ x thành một số. Xác định dương nghĩa là con số đó luôn dương với mọi x khác không: đồ thị dạng toàn phương là một cái bát mở lên trên.</p>'))
add(sl('Hai tiêu chuẩn kiểm tra: giá trị riêng và minor',
       table(['', 'Xác định dương (\\(\\succ0\\))', 'Nửa xác định dương (\\(\\succeq0\\))'],
             [['Giá trị riêng', 'tất cả \\(>0\\)', 'tất cả \\(\\ge0\\)'], ['Minor chính', 'mọi minor <b>dẫn đầu</b> \\(\\Delta_k>0\\) (Sylvester)', 'phải xét <b>MỌI</b> minor chính \\(\\ge0\\), không chỉ dẫn đầu']])
       + callout('warn', 'Cảnh báo của slide tr.41', '<p>Không dùng dấu các định thức con chính dẫn đầu để kiểm tra nửa xác định dương. Ví dụ \\(\\mathrm{diag}(0,-1)\\): \\(\\Delta_1=0,\\Delta_2=0\\) nhưng có giá trị riêng \\(-1\\).</p>'),
       kicker=M + ' · PHẦN 4', img='m1:41',
       explain='<p>Với ma trận 2×2 \\(\\begin{pmatrix}a&b\\\\b&c\\end{pmatrix}\\): xác định dương ⇔ \\(a>0\\) và \\(ac-b^2>0\\). Nửa xác định dương ⇔ \\(a\\ge0,\\ c\\ge0,\\ ac-b^2\\ge0\\) (cần cả c). Nếu nửa xác định dương mà không xác định dương thì \\(\\det=0\\).</p>'))
add(sl('Ví dụ: \\(x^2+xy+y^2\\) và \\(x_1^2+x_2^2\\)',
       '<p>\\(f=x_1^2+x_2^2\\): \\(H=\\begin{pmatrix}2&0\\\\0&2\\end{pmatrix}\\succ0\\) ⇒ lồi chặt.</p>'
       '<p>\\(f=x^2+xy+y^2\\): \\(H=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}\\), giá trị riêng \\(1\\) và \\(3\\) ⇒ \\(H\\succ0\\) ⇒ lồi chặt. Cách khác: \\(x^\\top Hx=2(x^2+xy+y^2)\\ge0\\).</p>',
       kicker=M + ' · PHẦN 4', img='m1:46',
       explain='<p>Hai ví dụ chuẩn cần thuộc: ma trận chéo dương là xác định dương; ma trận có phần tử ngoài đường chéo vẫn xác định dương nếu các giá trị riêng đều dương. Dùng công cụ Hessian ở dưới để tự thử.</p>'))
add(sl('Hàm toàn phương và hàm tuyến tính',
       formula('Hàm toàn phương', r'f(x)=\tfrac12x^\top Px+q^\top x+r,\quad P=P^\top,\ \nabla^2f=P')
       + '<p>f lồi ⇔ \\(P\\succeq0\\). Ví dụ \\(x^2+xy+y^2=\\tfrac12\\begin{pmatrix}x&y\\end{pmatrix}\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}\\begin{pmatrix}x\\\\y\\end{pmatrix}\\).</p><p>Hàm tuyến tính \\(a^\\top x\\) vừa lồi vừa lõm.</p>',
       kicker=M + ' · PHẦN 4', img='m1:48',
       explain='<p>Chỉ phần bậc hai (ma trận P) quyết định tính lồi. Vectơ q và hằng số r chỉ làm đồ thị “nghiêng” và “dịch lên xuống”, không đổi độ cong. Module 3 nghiên cứu sâu lớp hàm này.</p>'))
add(sl('Thêm hai ví dụ trong \\(\\mathbb R^2\\)',
       '<ul><li>\\(f(x,y)=\\sqrt{x^2+y^2}\\) lồi trên \\(\\mathbb R^2\\) (mọi chuẩn đều lồi).</li><li>\\(f(x,y)=x^2/y\\) lồi trên \\(\\{y>0\\}\\).</li></ul>'
       '<p>Hessian của \\(x^2/y\\) là \\(\\dfrac{2}{y^3}\\begin{pmatrix}y^2&-xy\\\\-xy&x^2\\end{pmatrix}\\), có \\(\\det=0\\) và vết \\(>0\\) ⇒ nửa xác định dương (kiểm bằng code: giá trị riêng \\(\\ge0\\)).</p>',
       kicker=M + ' · PHẦN 4', img='m1:51',
       explain='<p>Hàm \\(x^2/y\\) (“bình phương chia biến”) xuất hiện rất nhiều trong tối ưu (ví dụ hàm perspective, chuẩn hóa). Chuẩn Euclid lồi vì nó thỏa bất đẳng thức tam giác.</p>'))

# ====================================================== PHẦN 5
add(part(5, 5, 'Phép toán bảo toàn tính lồi và bài tập', ['Nhân dương, cộng, lấy max', 'Bài tập slide: \\(e^x-1\\), \\(xy\\), \\(1/(xy)\\), \\(x/y\\)', 'Quy trình kiểm tra hàm lồi'], M))
add(sl('Các phép toán bảo toàn tính lồi',
       '<ul><li>f lồi, \\(\\alpha>0\\) ⇒ \\(\\alpha f\\) lồi.</li><li>f, g lồi ⇒ \\(f+g\\) lồi.</li><li>f, g lồi ⇒ \\(h=\\max\\{f,g\\}\\) lồi.</li></ul>'
       + callout('warn', 'Không bảo toàn', '<p>\\(f-g\\) và \\(\\min\\{f,g\\}\\) nói chung <b>không</b> lồi. Ví dụ \\(x^2-2x^2=-x^2\\) lõm; \\(\\min\\{x^2,(x-2)^2\\}\\) có hai “đáy”.</p>')
       + '<p>Thêm (Boyd 3.2): hợp thành với ánh xạ affine \\(f(Ax+b)\\) lồi; ví dụ \\(\\|Ax-b\\|^2\\) lồi.</p>',
       kicker=M + ' · PHẦN 5', img='m1:53',
       explain='<p>Đây là “bộ quy tắc xây dựng”: từ các hàm lồi đã biết (bình phương, mũ, chuẩn) ta ghép lại theo các phép trên mà vẫn giữ được tính lồi, không cần tính Hessian.</p>'))
add(sl('Bài tập slide: bốn hàm cần phân loại',
       table(['Hàm', 'Miền', 'Kết luận', 'Lý do (Hessian)'],
             [['\\(e^x-1\\)', '\\(\\mathbb R\\)', '<b>lồi</b>', '\\(f^{\\prime\\prime}=e^x>0\\)'],
              ['\\(xy\\)', '\\(\\mathbb R^2_{++}\\)', '<b>không lồi, không lõm</b>', '\\(H=\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\), giá trị riêng \\(\\pm1\\)'],
              ['\\(1/(xy)\\)', '\\(\\mathbb R^2_{++}\\)', '<b>lồi</b>', '\\(f_{xx}>0\\), \\(\\det H=3/(xy)^4>0\\)'],
              ['\\(x/y\\)', '\\(\\mathbb R^2_{++}\\)', '<b>không lồi, không lõm</b>', '\\(\\det H=-1/y^4<0\\)']]),
       kicker=M + ' · PHẦN 5', img='m1:54',
       explain='<p>Đây là bài tập cuối slide. Lời giải chi tiết (kèm kiểm số bằng code) nằm ở phần “Ví dụ chi tiết” bên dưới. Nhớ: khi \\(\\det H<0\\) thì hai giá trị riêng trái dấu, Hessian không xác định.</p>'))
add(sl('Quy trình kiểm tra hàm lồi (sơ đồ)',
       f'<figure class="slide-fig"><img src="../../assets/diagrams/d2-kiem-tra-ham-loi.svg" alt="Quy trình kiểm tra hàm lồi" style="max-height:20em;background:#fff"/></figure>'
       '<p>Ưu tiên: nhận dạng bằng phép toán bảo toàn → Hessian → định nghĩa Jensen.</p>',
       kicker=M + ' · TỔNG KẾT',
       explain='<p>Sơ đồ tóm tắt cách làm bài “kiểm tra f có lồi không”. Lưu ý bước cuối: muốn kết luận <i>không lồi</i> chỉ cần chỉ ra một điểm mà Hessian có giá trị riêng âm.</p>'))

# =====================================================================  CÁC PHẦN BÊN DƯỚI DECK
SECTIONS = []

# ---- công thức cốt lõi
S_form = formula('Tập lồi', r'x,y\in C,\ \theta\in[0,1]\ \Rightarrow\ \theta x+(1-\theta)y\in C') + \
    formula('Bao lồi', r'\mathrm{conv}\,C=\{\textstyle\sum_i\theta_ix_i\mid x_i\in C,\ \theta_i\ge0,\ \sum_i\theta_i=1\}') + \
    formula('Bất đẳng thức Jensen', r'f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)') + \
    formula('Điều kiện cấp 1', r'f(y)\ge f(x)+\nabla f(x)^\top(y-x)') + \
    formula('Điều kiện cấp 2', r'\nabla^2f(x)\succeq0\ \ \forall x\in\mathrm{dom}\,f') + \
    formula('Hàm toàn phương', r'f(x)=\tfrac12x^\top Px+q^\top x+r,\qquad\nabla f=Px+q,\quad\nabla^2f=P',
            [('P', 'ma trận đối xứng (phần bậc hai)'), ('q', 'vectơ hệ số bậc nhất'), ('r', 'hằng số')]) + \
    table(['Khái niệm', 'Xác định dương', 'Nửa xác định dương'],
          [['Định nghĩa', '\\(x^\\top Ax>0\\ \\forall x\\ne0\\)', '\\(x^\\top Ax\\ge0\\ \\forall x\\)'], ['Giá trị riêng', 'mọi \\(\\lambda_i>0\\)', 'mọi \\(\\lambda_i\\ge0\\)'],
           ['Minor', 'mọi minor dẫn đầu \\(>0\\)', 'mọi minor chính (không chỉ dẫn đầu) \\(\\ge0\\)'], ['Hàm', 'lồi chặt (nếu mọi x)', 'lồi']])
SECTIONS.append(('cong-thuc', 'Công thức cốt lõi', S_form))

# ---- lịch sử
S_hist = callout('hist', '📜 Bối cảnh lý thuyết & lịch sử',
    '<p>Bất đẳng thức <b>Jensen</b> mang tên nhà toán học Đan Mạch Johan Jensen, người công bố dạng tổng quát cho hàm lồi năm 1906. Khái niệm tập lồi gắn với công trình hình học các vật thể lồi của <b>Hermann Minkowski</b> đầu thế kỷ XX; định lý biểu diễn “polytope = bao lồi hữu hạn điểm” mang tên Minkowski–Weyl.</p>'
    '<p>Giải tích lồi được hệ thống hóa thành một ngành độc lập trong cuốn <i>Convex Analysis</i> của R. T. Rockafellar (1970). Tối ưu lồi hiện đại, gồm phương pháp điểm trong, được trình bày trong giáo trình Boyd &amp; Vandenberghe <i>Convex Optimization</i> (2004) — giáo trình chính của học phần này.</p>')
SECTIONS.append(('lich-su', 'Bối cảnh lý thuyết và lịch sử', S_hist))

# ---- case study
S_case = ('<p>Bài toán <b>bình phương tối thiểu</b> (đường hồi quy): cho 5 điểm đo \\((x_i,y_i)\\) như bảng dưới, tìm đường thẳng \\(y=\\theta_0+\\theta_1x\\) làm cực tiểu \\(f(\\theta)=\\|A\\theta-y\\|^2\\).</p>'
          + table(['x', '1', '2', '3', '4', '5'], [['y', '2.1', '3.9', '6.2', '7.8', '10.1']])
          + steps([
              'Ma trận thiết kế \\(A=[1,\\ x]\\) cỡ \\(5\\times2\\). Hàm \\(f(\\theta)=\\theta^\\top A^\\top A\\theta-2y^\\top A\\theta+y^\\top y\\) là hàm toàn phương.',
              f'Hessian \\(\\nabla^2f=2A^\\top A=\\begin{{pmatrix}}{f4(Hls[0,0])}&{f4(Hls[0,1])}\\\\{f4(Hls[1,0])}&{f4(Hls[1,1])}\\end{{pmatrix}}\\), giá trị riêng \\({f4(eig_ls[0])}\\) và \\({f4(eig_ls[1])}\\) đều dương ⇒ \\(\\nabla^2f\\succ0\\) ⇒ f <b>lồi chặt</b>.',
              'Vì f lồi chặt khả vi nên điểm dừng \\(\\nabla f=0\\) là cực tiểu toàn cục <b>duy nhất</b>: giải phương trình chuẩn \\(A^\\top A\\theta=A^\\top y\\).',
              f'Kết quả (giải bằng code): \\(\\theta_0={f4(theta[0])}\\), \\(\\theta_1={f4(theta[1])}\\); tổng bình phương sai số \\(f(\\theta^*)={f4(res)}\\).'])
          + callout('good', 'Điều học được', '<p>Chỉ cần kiểm tra Hessian \\(2A^\\top A\\succ0\\) (khi các cột của A độc lập tuyến tính), ta biết ngay mô hình hồi quy có nghiệm duy nhất và không cần lo mắc kẹt cực tiểu địa phương.</p>'))
SECTIONS.append(('case-study', '🔎 Case study: hồi quy bình phương tối thiểu', S_case))

# ---- ví dụ chi tiết
def ex(title, body): return solution(title, body)
EXS = ''
EXS += ex('Ví dụ 1 — Hessian của \\(f=x^2+xy+y^2\\) (slide tr.46)',
    steps(['Đạo hàm riêng: \\(f_x=2x+y\\), \\(f_y=x+2y\\).', 'Đạo hàm cấp hai: \\(f_{xx}=2\\), \\(f_{yy}=2\\), \\(f_{xy}=f_{yx}=1\\).',
           f'Hessian \\(H=\\begin{{pmatrix}}2&1\\\\1&2\\end{{pmatrix}}\\): \\(\\Delta_1=2>0\\), \\(\\Delta_2=4-1=3>0\\) ⇒ xác định dương. Giá trị riêng (code): \\({mat["P1"]["eig"][0]}\\) và \\({mat["P1"]["eig"][1]}\\).',
           'Kết luận: f lồi chặt trên \\(\\mathbb R^2\\).']))
EXS += ex('Ví dụ 2 — Hàm \\(3x_1^2+3x_2^2-4x_1x_2\\) (bài tập tham khảo C8)',
    steps(['\\(H=\\begin{pmatrix}6&-4\\\\-4&6\\end{pmatrix}\\).', f'\\(\\Delta_1=6>0\\), \\(\\Delta_2=36-16={mat["P2"]["minors"][1]:.0f}>0\\) ⇒ xác định dương; giá trị riêng \\({mat["P2"]["eig"][0]}\\) và \\({mat["P2"]["eig"][1]}\\).', 'Kết luận: lồi chặt. Hàm thứ hai \\(4x_1^2+x_2^2-x_1-2x_2\\) có \\(H=\\mathrm{diag}(8,2)\\succ0\\) ⇒ lồi chặt (số hạng bậc nhất không đổi Hessian).']))
EXS += ex('Ví dụ 3 — Bốn hàm ở bài tập slide tr.54',
    '<p><b>(a)</b> \\(f=e^x-1\\): \\(f^{\\prime\\prime}=e^x>0\\) ⇒ lồi.</p>'
    '<p><b>(b)</b> \\(f=xy\\): \\(H=\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\), giá trị riêng \\(-1,1\\) (mọi điểm) ⇒ không lồi, không lõm.</p>'
    '<p><b>(c)</b> \\(f=1/(xy)\\): \\(H=\\begin{pmatrix}\\frac{2}{x^3y}&\\frac1{x^2y^2}\\\\\\frac1{x^2y^2}&\\frac2{xy^3}\\end{pmatrix}\\); \\(\\Delta_1>0\\), \\(\\Delta_2=\\frac{4-1}{x^4y^4}>0\\) ⇒ lồi chặt. Kiểm số (code) giá trị riêng nhỏ nhất tại \\((1,1),(2,1),(1,3),(0.5,0.5)\\): '
    + ', '.join(f4(min(p['eig'])) for p in ex_slide['1/(xy)']) + ' — đều dương.</p>'
    '<p><b>(d)</b> \\(f=x/y\\): \\(H=\\begin{pmatrix}0&-1/y^2\\\\-1/y^2&2x/y^3\\end{pmatrix}\\), \\(\\det H=-1/y^4<0\\) ⇒ không lồi, không lõm. Giá trị riêng nhỏ nhất (code) tại các điểm mẫu: '
    + ', '.join(f4(min(p['eig'])) for p in ex_slide['x/y']) + ' — đều âm.</p>')
EXS += ex('Ví dụ 4 — Chứng minh “max của các hàm lồi là hàm lồi”',
    '<p>Với \\(g=\\max_if_i\\): \\(f_i(\\theta x+(1-\\theta)y)\\le\\theta f_i(x)+(1-\\theta)f_i(y)\\le\\theta g(x)+(1-\\theta)g(y)\\). Lấy max theo i ở vế trái ⇒ \\(g(\\theta x+(1-\\theta)y)\\le\\theta g(x)+(1-\\theta)g(y)\\). Kiểm số: lấy ngẫu nhiên 20 000 bộ \\((x,y,\\theta)\\) cho \\(\\max\\{x^2,(x-2)^2\\}\\): số vi phạm = '
    + str(R['m1_jensen']['max(x^2, (x-2)^2)']) + '; hàm \\(x^3\\) (không lồi) vi phạm ' + str(R['m1_jensen']['x^3 (should violate)']) + ' lần.</p>')
EXS += ex('Ví dụ 5 — Bẫy “minor dẫn đầu” cho nửa xác định dương',
    '<p>Ma trận \\(A=\\begin{pmatrix}0&0\\\\0&-1\\end{pmatrix}\\): \\(\\Delta_1=0\\), \\(\\Delta_2=0\\), cả hai \\(\\ge0\\); nếu chỉ nhìn dẫn đầu ta tưởng \\(A\\succeq0\\). Nhưng \\(x=(0,1)\\) cho \\(x^\\top Ax=-1<0\\), và minor chính \\(a_{22}=-1<0\\) (giá trị riêng \\(0,-1\\)) đã phát hiện ra điều đó.</p>'
    '<p>Ngược lại \\(\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}\\) có giá trị riêng \\(0,2\\) ⇒ nửa xác định dương, không xác định dương, \\(\\det=0\\).</p>')
EXS += ex('Ví dụ 6 — Hợp hai tập lồi không lồi; tổng Minkowski',
    '<p>\\([0,1]\\cup[2,3]\\) không chứa \\(1.5\\). Ngược lại \\([0,1]+[2,3]=[2,4]\\) là đoạn (lồi). Tổng hai hình tròn bán kính 1 và 2 cùng tâm gốc là hình tròn bán kính 3.</p>')
SECTIONS.append(('vi-du', 'Ví dụ chi tiết (có lời giải từng bước)', '<p>Bấm từng ví dụ để mở lời giải. Các con số Hessian/giá trị riêng lấy từ script kiểm chứng.</p>' + EXS))

# ---- sơ đồ
SECTIONS.append(('so-do', 'Sơ đồ tổng hợp', fig('d2-kiem-tra-ham-loi', 'Quy trình kiểm tra hàm lồi (drawio)') + fig('d1-phan-loai-toi-uu', 'Vị trí của tối ưu lồi trong các lớp bài toán tối ưu')))

# ---- tương tác
SECTIONS.append(('tuong-tac', 'Thực hành tương tác',
    widget('convex-set-lab') + widget('jensen-lab') + widget('hessian-lab')))

# ---- bẫy
S_warn = ''.join([
    callout('warn', 'Bẫy 1 — “Hợp hai tập lồi cũng lồi”', '<p>Sai. Chỉ giao và tổng Minkowski bảo toàn tính lồi.</p>'),
    callout('warn', 'Bẫy 2 — Minor dẫn đầu cho nửa xác định dương', '<p>Xác định dương: chỉ cần minor dẫn đầu \\(>0\\). Nửa xác định dương: phải xét mọi minor chính hoặc giá trị riêng.</p>'),
    callout('warn', 'Bẫy 3 — “Lồi chặt ⇒ Hessian xác định dương”', '<p>Chiều thuận đúng (Hessian \\(\\succ0\\) ⇒ lồi chặt), chiều nghịch sai: \\(x^4\\) lồi chặt nhưng \\(f^{\\prime\\prime}(0)=0\\).</p>'),
    callout('warn', 'Bẫy 4 — Kiểm Hessian tại một điểm', '<p>Điều kiện cấp 2 đòi hỏi \\(\\nabla^2f(x)\\succeq0\\) trên <b>toàn miền</b>. \\(f=xy\\) có Hessian cố định nhưng không xác định; \\(f=x^3\\) có \\(f^{\\prime\\prime}>0\\) ở \\(x>0\\) mà vẫn không lồi trên \\(\\mathbb R\\).</p>'),
    callout('warn', 'Bẫy 5 — Tính lồi không bảo đảm tồn tại cực tiểu', '<p>\\(e^x\\) lồi nhưng không đạt giá trị nhỏ nhất. Sự tồn tại nghiệm cần thêm điều kiện (bị chặn, đóng, coercive — Module 0 và 3).</p>'),
    callout('warn', 'Bẫy 6 — Ellipsoid', '<p>Slide viết \\(P\\succeq0\\); để ellipsoid bị chặn cần \\(P\\succ0\\). Xem trang “Kiểm chứng”.</p>')])
SECTIONS.append(('bay', 'Cảnh báo bẫy diễn giải sai', S_warn))

READING = ('<ul><li>Boyd &amp; Vandenberghe, <i>Convex Optimization</i>: Ch.2 (Convex sets, tr.21) và Ch.3 (Convex functions, tr.67) — file <code>bv_cvxbook.pdf</code>.</li>'
           '<li>Bài tập tham khảo (Studocu, rất cũ và khác ngành, chỉ để luyện thêm): C1–C8 về chứng minh tính lồi; đã đưa vào ngân hàng câu hỏi với nhãn “tham khảo”.</li>'
           '<li>Tiếp theo: Module 2 dùng trực tiếp khái niệm “bài toán lồi” (f lồi, \\(g_i\\) lồi, \\(h_j\\) affine).</li></ul>')
