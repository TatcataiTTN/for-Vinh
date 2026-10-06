"""Ngân hàng câu hỏi Module 3 — Quy hoạch toàn phương. Nguồn chính: Slides/3_QuadraticPrograming_250419a.pdf
Nhãn: G = từ nội dung slide; B = bài tập/ví dụ của slide; T = tham khảo; S = biên soạn thêm."""
import numpy as np
from qlib import Bank
from helpers import R

bank = Bank('m3')
mc, tf, num, essay = bank.mc, bank.tf, bank.num, bank.essay
def r(p): return f'slide 3 · tr.{p}'
AE = R['m3_active_ex']; AB = R['m3_active_bt']; NE = R['m3_null_ex']; ER = R['errata_null_space']; BT1 = R['m3_bt1']; EB = R['errata_bt1']['constraint_b=(3,0)']

# =====================================================================  A. HÀM TOÀN PHƯƠNG VÀ BÀI TOÁN QP
A = 'A. Hàm toàn phương và bài toán QP'
mc('G', r(3), r'Hàm toàn phương–tuyến tính (linear-quadratic) trong slide có dạng',
   r'\(f(x)=\tfrac12x^\top Qx+c^\top x+\alpha\)', [r'\(f(x)=x^\top Qx\cdot c^\top x+\alpha\)', r'\(f(x)=\tfrac12\|Qx\|+c^\top x\)', r'\(f(x)=Q+cx+\alpha x^2\)'],
   r'Định nghĩa 1.1 (slide tr.3): tồn tại \(Q\in\mathbb R^{n\times n}\), \(c\in\mathbb R^n\), \(\alpha\in\mathbb R\) sao cho \(f(x)=\tfrac12x^\top Qx+c^\top x+\alpha=\tfrac12\langle x,Qx\rangle+\langle c,x\rangle+\alpha\).', A)
mc('G', r(4), r'Dạng khai triển của hàm toàn phương–tuyến tính (tr.4) là',
   r'\(\tfrac12\sum_{i,j}q_{ij}x_ix_j+\sum_ic_ix_i+\alpha\)', [r'\(\sum_iq_{ii}x_i^2+\sum_ic_ix_i\)', r'\(\tfrac12\sum_iq_ix_i+\sum_ic_ix_i^2+\alpha\)', r'\(\prod_{i,j}q_{ij}x_ix_j+\alpha\)'],
   r'Thay \(x^\top Qx=\sum_{i,j}q_{ij}x_ix_j\) và \(c^\top x=\sum c_ix_i\).', A)
mc('G', r(7), r'Vì sao có thể giả sử ma trận Q đối xứng?',
   r'vì \(x^\top Qx=\tfrac12x^\top(Q+Q^\top)x\) nên có thể thay Q bằng phần đối xứng', [r'vì mọi ma trận vuông đều đối xứng', r'vì Q luôn xác định dương', r'vì \(x^\top Qx=x^\top Q^\top Qx\)'],
   r'Slide tr.7: “ta chỉ cần thay Q trong (1.1) bởi ma trận đối xứng \(\tfrac12(Q+Q^\top)\)”. Phần phản đối xứng \(Q-Q^\top\) không đóng góp vào dạng toàn phương.', A)
num('G', r(7), r'Cho \(Q=\begin{pmatrix}1&4\\0&3\end{pmatrix}\), \(x=(2,-1)\). Tính \(x^\top Qx\).', -1,
    r'\(x^\top Qx=1\cdot4+4\cdot2(-1)+0\cdot(-1)(2)+3\cdot1=4-8+3=-1\). Ma trận đối xứng hóa \(\begin{pmatrix}1&2\\2&3\end{pmatrix}\) cho cùng giá trị.', ans_text='-1', grp=A)
mc('G', r(9), r'Với \(f(x)=x_1^2+x_2^2\), viết dưới dạng (1.1) ta có',
   r'\(Q=\begin{pmatrix}2&0\\0&2\end{pmatrix}\), \(c=0\), \(\alpha=0\)', [r'\(Q=\begin{pmatrix}1&0\\0&1\end{pmatrix}\), \(c=0\), \(\alpha=0\)', r'\(Q=\begin{pmatrix}2&2\\2&2\end{pmatrix}\), \(c=0\), \(\alpha=0\)', r'\(Q=\begin{pmatrix}1&1\\1&1\end{pmatrix}\), \(c=(1,1)\), \(\alpha=0\)'],
   r'\(\tfrac12x^\top\mathrm{diag}(2,2)x=x_1^2+x_2^2\). Nhớ hệ số \(\tfrac12\): Q gấp đôi hệ số của \(x_i^2\) (slide tr.9).', A)
mc('G', r(10), r'Bài toán (P) \(\min f(x)\) s.t. \(x\in\Delta\) là quy hoạch toàn phương–tuyến tính nếu',
   'f toàn phương–tuyến tính và Δ là tập lồi đa diện', ['f toàn phương và Δ là hình cầu', 'f tuyến tính và Δ là tập lồi bất kỳ', 'f bậc ba và Δ là polyhedron'],
   r'Định nghĩa 1.2 (slide tr.10): f toàn phương–tuyến tính, \(\Delta\) polyhedron.', A)
tf('G', r(12), r'Nếu \(Q=0\) và \(\alpha=0\) thì hàm f trong QP là hàm tuyến tính, nên lớp bài toán QHTT là lớp con của lớp bài toán QP.', True, r'Slide tr.12.', A)
mc('G', r(12), r'QP được gọi là lồi khi',
   r'\(Q\succeq0\) (nửa xác định dương)', [r'\(Q\preceq0\)', r'\(Q=0\) và \(\alpha=0\)', r'\(\det Q>0\)'],
   r'Slide tr.12: “Nếu \(Q\succeq0\) thì ta có bài toán QHTP lồi”. \(Q=0\) là trường hợp riêng (QHTT).', A)
mc('G', r(14), r'Bỏ hằng số \(\alpha\) khỏi hàm mục tiêu của QP thì',
   'tập nghiệm không đổi (giá trị tối ưu thay đổi)', ['tập nghiệm thay đổi', 'bài toán trở nên không lồi', 'bài toán vô nghiệm'],
   r'Hằng số cộng vào f không đổi vị trí cực tiểu, chỉ đổi giá trị tối ưu (slide tr.14).', A)
mc('G', r(14), r'Thay \(Q\) bởi \(\tfrac12Q\) trong \(\min\tfrac12x^\top Qx+c^\top x\) thì bài toán tương đương với',
   r'\(\min x^\top Qx+c^\top x\) (chỉ khác quy ước hệ số \(\tfrac12\))', [r'\(\min\tfrac12x^\top Qx+2c^\top x\)', r'\(\min x^\top Qx+\tfrac12c^\top x\)', r'\(\min x^\top Q^{-1}x+c^\top x\)'],
   r'Slide tr.14: \(\tfrac12x^\top(\tfrac12Q)x\) biến thành ... tùy quy ước; khi bỏ hệ số \(\tfrac12\) ở đầu ta được \(\min x^\top Qx+c^\top x\) với Q mới. Điều cần nhớ: hằng số nhân trước phần bậc hai đổi Q chứ không đổi tính chất.', A)
mc('B', r(16), r'Ví dụ slide tr.16: \(\min x_1^2-x_2^2\) với \(1\le x_1,x_2\le3\). Bài toán này là',
   'quy hoạch toàn phương không lồi', ['quy hoạch toàn phương lồi', 'quy hoạch tuyến tính', 'quy hoạch phi tuyến bậc ba'],
   r'\(Q=\mathrm{diag}(2,-2)\) không nửa xác định dương ⇒ QP không lồi (slide tr.16: “Bài toán (1) là một QHTP không lồi!”).', A)
num('B', r(16), r'Giá trị nhỏ nhất của \(x_1^2-x_2^2\) trên \([1,3]^2\) là', -8,
    r'Bốn đỉnh cho \(0,-8,8,0\); f lõm theo \(x_2\), tăng theo \(x_1\): cực tiểu \(-8\) tại \((1,3)\) (kiểm SLSQP: ' + str(R['m3_nonconvex_box_num']) + ').', ans_text='-8', grp=A)
mc('G', r(17), r'Dạng tổng quát nhất của QP dùng trong slide tr.17 và tr.21 là',
   r'\(\min\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax\ge b\)', [r'\(\min\tfrac12x^\top Qx\) s.t. \(Ax=b\) và \(x\ge0\) chỉ', r'\(\max\tfrac12x^\top Qx+c^\top x\) s.t. \(x=0\)', r'\(\min\|Qx-c\|\) s.t. \(x^\top x=1\)'],
   r'Các dạng còn lại (\(x\ge0\), đẳng thức, \(\le\)) đều đổi được về \(Ax\ge b\) (slide tr.17, tr.20).', A)
tf('G', r(20), r'Dạng QP với ràng buộc \(Ax\le b,\ x\ge0\) cũng nằm trong họ các dạng QP được slide liệt kê.', True, r'Slide tr.20 liệt kê bốn dạng: \(Ax\ge b\); \(Ax\ge b,x\ge0\); \(Ax\ge b,Cx=d\); \(Ax\le b,x\ge0\).', A)
tf('S', r(3), r'Hessian của hàm toàn phương \(\tfrac12x^\top Qx+c^\top x+\alpha\) (Q đối xứng) bằng Q tại mọi điểm.', True, r'\(\nabla f=Qx+c\), \(\nabla^2f=Q\).', A)
tf('S', r(9), r'Hàm \(x_1^2+x_2^2\) tương ứng với \(Q=\mathrm{diag}(1,1)\) trong dạng \(\tfrac12x^\top Qx\).', False, r'\(\tfrac12x^\top\mathrm{diag}(1,1)x=\tfrac12(x_1^2+x_2^2)\); phải dùng \(Q=\mathrm{diag}(2,2)\).', A)
tf('S', r(12), r'Mọi bài toán QP đều là bài toán tối ưu lồi.', False, r'QP lồi chỉ khi \(Q\succeq0\) (ví dụ \(x_1^2-x_2^2\) trên hình hộp không lồi).', A)
tf('S', r(12), r'Một quy hoạch tuyến tính là một quy hoạch toàn phương (với \(Q=0\)).', True, r'Slide tr.12.', A)
tf('S', r(10), r'Trong định nghĩa QP, miền \(\Delta\) chỉ cần là tập đóng bất kỳ.', False, r'Δ phải là <b>polyhedron</b> (tập lồi đa diện). Nhiều định lý (Frank–Wolfe) sai nếu bỏ giả thiết này.', A)
num('S', r(9), r'Cho \(f(x)=3x_1^2+2x_1x_2+x_2^2\). Phần tử \(Q_{11}\) của \(Q=\nabla^2f\) (để \(f=\tfrac12x^\top Qx\)) bằng', 6,
    r'\(\partial^2f/\partial x_1^2=6\). (Hessian \(\begin{pmatrix}6&2\\2&2\end{pmatrix}\).)', ans_text='6', grp=A)
essay('S', r(7), r'Chứng minh \(x^\top Qx=\tfrac12x^\top(Q+Q^\top)x\) với mọi \(x\), và giải thích vì sao có thể giả sử Q đối xứng.',
      r'<p>\(x^\top Qx\) là một số thực nên bằng chuyển vị của nó: \(x^\top Qx=(x^\top Qx)^\top=x^\top Q^\top x\). Cộng hai vế: \(2x^\top Qx=x^\top(Q+Q^\top)x\) ⇒ \(x^\top Qx=\tfrac12x^\top(Q+Q^\top)x\). Do đó thay Q bởi \(\tfrac12(Q+Q^\top)\) (đối xứng) không đổi hàm f.</p>',
      ['Dùng số thực bằng chuyển vị của nó', 'Kết luận đối xứng hóa'], A)
essay('B', r(16), r'Giải bài toán slide tr.16: \(\min x_1^2-x_2^2\) với \(1\le x_1,x_2\le3\). Xác định Q, phân loại bài toán và tìm nghiệm.',
      r'<p>\(f=\tfrac12x^\top\mathrm{diag}(2,-2)x\), \(Q\) có giá trị riêng \(2,-2\): không nửa xác định dương ⇒ QP không lồi. Miền là hình vuông (polytope) compact ⇒ có nghiệm. \(f\) tăng theo \(x_1\) và giảm theo \(x_2\) trên miền ⇒ nghiệm ở \(x_1=1\), \(x_2=3\): \(f=1-9=-8\). Bốn đỉnh: \(0,-8,8,0\). Nghiệm \((1,3)\), \(f^*=-8\).</p>',
      ['Nêu \\(Q\\) và dấu của giá trị riêng', 'Lập luận nghiệm ở đỉnh', 'So sánh bốn đỉnh'], A)

# =====================================================================  B. TỒN TẠI NGHIỆM
B = 'B. Điều kiện tồn tại nghiệm'
mc('G', r(21), r'Bài toán (2) trong slide tr.21 là',
   r'\(\min f(x)=\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax\ge b\)', [r'\(\min f(x)=\tfrac12x^\top Qx\) s.t. \(Ax=b\)', r'\(\max f(x)=\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax\le b\)', r'\(\min f(x)=c^\top x\) s.t. \(x^\top Qx\le1\)'],
   r'Slide tr.21: dạng tổng quát nhất; \(A\in\mathbb R^{m\times n}\), \(c\in\mathbb R^n\), \(b\in\mathbb R^m\).', B)
mc('G', r(23), r'Ký hiệu \(\Delta(A,b)\) và \(\bar\theta\) trong slide tr.23 là',
   r'\(\Delta(A,b)=\{x:Ax\ge b\}\) và \(\bar\theta=\inf\{f(x):x\in\Delta(A,b)\}\)', [r'\(\Delta(A,b)=\{x:Ax=b\}\) và \(\bar\theta=\sup f\)', r'\(\Delta(A,b)=\{x:f(x)\le b\}\) và \(\bar\theta=\min f\)', r'\(\Delta(A,b)=\{Ax\}\) và \(\bar\theta=\|c\|\)'],
   r'Slide tr.23. Nếu \(\Delta=\emptyset\) thì quy ước \(\bar\theta=+\infty\).', B)
mc('G', r(23), r'Nếu \(\Delta(A,b)=\emptyset\) thì slide quy ước \(\bar\theta\) bằng',
   r'\(+\infty\)', [r'\(-\infty\)', r'0', r'\(f(0)\)'],
   r'Infimum của tập rỗng là \(+\infty\) (quy ước, slide tr.23).', B)
mc('G', r(23), r'Khi \(\Delta(A,b)\ne\emptyset\), trường hợp \(\bar\theta=-\infty\) nghĩa là',
   'f giảm vô hạn trên miền nên bài toán không có nghiệm', ['bài toán có nghiệm duy nhất', 'bài toán có vô số nghiệm', 'miền chấp nhận được rỗng'],
   r'Slide tr.23: “TH2: \(\bar\theta=-\infty\) (bài toán không có nghiệm)”.', B)
mc('G', r(24), r'Định lý Frank–Wolfe (slide tr.24) nói',
   r'nếu \(\bar\theta\) là số thực hữu hạn thì bài toán (2) có nghiệm', [r'nếu Δ bị chặn thì nghiệm duy nhất', r'nếu \(Q\succ0\) thì \(\bar\theta=-\infty\)', r'nếu \(\bar\theta=-\infty\) thì có nghiệm ở vô cực'],
   r'Giả thiết chính: \(\bar\theta\) hữu hạn (f bị chặn dưới trên miền); kết luận: infimum được đạt.', B)
tf('G', r(24), r'Định lý Frank–Wolfe không yêu cầu miền \(\Delta\) bị chặn.', True, r'Chỉ cần \(\bar\theta\) hữu hạn. Điều này khác với Weierstrass (cần compact).', B)
mc('B', r(25), r'Ví dụ slide tr.25: \(\min x_1\) trên \(\Delta=\{x_1x_2\ge1,x_1\ge0,x_2\ge0\}\). Kết luận đúng là',
   r'\(\bar\theta=0\) nhưng bài toán không có nghiệm', [r'\(\bar\theta=1\) và nghiệm \((1,1)\)', r'\(\bar\theta=-\infty\)', r'\(\bar\theta=0\) và nghiệm \((0,0)\)'],
   r'\(x_1x_2\ge1\) ⇒ \(x_1>0\), nhưng có thể nhỏ tùy ý (\(x_2=1/x_1\)); infimum 0 không đạt. Δ không phải polyhedron nên Frank–Wolfe không áp dụng.', B)
tf('B', r(25), r'Trong ví dụ slide tr.25, tập \(\Delta\) là một tập lồi đa diện.', False, r'Slide nêu rõ Δ “không phải là tập lồi đa diện” (biên là hyperbol \(x_1x_2=1\)); vì vậy Frank–Wolfe không dùng được.', B)
mc('G', r(26), r'Định lý Eaves cho biết bài toán (2) có nghiệm khi và chỉ khi',
   'Δ khác rỗng và hai điều kiện về hướng \\(v\\) (\\(Av\\ge0\\)) thỏa mãn', ['Q xác định dương', 'Δ bị chặn', 'c = 0 và b = 0'],
   r'Ba điều kiện: (1) \(\Delta\ne\emptyset\); (2) \(Av\ge0\Rightarrow v^\top Qv\ge0\); (3) \(Av\ge0,\ v^\top Qv=0,\ Ax\ge b\Rightarrow(Qx+c)^\top v\ge0\) (slide tr.26).', B)
mc('G', r(26), r'Điều kiện (2) của Eaves: “\(v\in\mathbb R^n,\ Av\ge0\Rightarrow v^\top Qv\ge0\)” có nghĩa là',
   'dạng bậc hai không âm theo mọi hướng lùi của miền', ['Q xác định dương trên toàn không gian', 'miền Δ bị chặn', 'nghiệm là điểm cực biên'],
   r'\(\{v:Av\ge0\}\) là nón lùi của Δ (các hướng đi mãi trong miền). Nếu \(v^\top Qv<0\) thì f giảm về \(-\infty\) dọc hướng đó.', B)
mc('G', r(26), r'Điều kiện (3) của Eaves quan tâm trường hợp',
   r'\(v^\top Qv=0\) (bậc hai triệt tiêu) và yêu cầu phần tuyến tính \((Qx+c)^\top v\ge0\)', [r'\(v^\top Qv>0\) và yêu cầu \(c=0\)', r'\(Av<0\) và yêu cầu \(x=0\)', r'\(v=0\) và yêu cầu \(Ax=b\)'],
   r'Dọc \(x+tv\): \(f(x+tv)=f(x)+t(Qx+c)^\top v+\tfrac{t^2}2v^\top Qv\). Khi hệ số \(t^2\) bằng 0 thì hệ số \(t\) phải không âm.', B)
mc('G', r(27), r'Hệ quả 1 (slide tr.27): nếu \(Q\succeq0\) thì (2) có nghiệm khi và chỉ khi',
   r'\(\Delta\ne\emptyset\) và \((Av\ge0,\ v^\top Qv=0,\ Ax\ge b)\Rightarrow(Qx+c)^\top v\ge0\)', [r'\(\Delta\) compact', r'\(c=0\)', r'\(\Delta=\emptyset\)'],
   r'Điều kiện (2) của Eaves tự động thỏa khi \(Q\succeq0\); chỉ còn (1) và (3).', B)
mc('G', r(29), r'Hệ quả 3 (slide tr.29): nếu \(Q\succ0\) thì (2) có nghiệm khi và chỉ khi',
   r'\(\Delta(A,b)\ne\emptyset\)', [r'\(\Delta(A,b)\) compact', r'\(c=0\)', r'\(A\) khả nghịch'],
   r'\(Q\succ0\Rightarrow f\) coercive: chỉ cần miền khác rỗng là có nghiệm (và duy nhất).', B)
tf('G', r(29), r'Nếu \(Q\succ0\) và miền \(\Delta\) khác rỗng nhưng không bị chặn thì bài toán (2) vẫn có nghiệm.', True, r'Hệ quả 3: chỉ cần \(\Delta\ne\emptyset\). Ví dụ \(\min x^2\) trên \(x\ge1\) (miền không bị chặn) có nghiệm \(x=1\).', B)
mc('G', r(28), r'Hệ quả 2 (slide tr.28) áp dụng cho',
   r'\(Q\) nửa xác định âm', [r'\(Q\) xác định dương', r'\(Q=0\) duy nhất', r'\(Q\) không xác định'],
   r'Điều kiện: \(\Delta\ne\emptyset\), \((Av\ge0\Rightarrow v^\top Qv=0)\) và \((Av\ge0,Ax\ge b\Rightarrow(Qx+c)^\top v=0)\).', B)
mc('G', r(30), r'Hệ quả 4 (slide tr.30) nói nghiệm tồn tại khi và chỉ khi',
   r'\(\Delta\) khác rỗng và compact (áp dụng khi Q xác định âm)', [r'\(\Delta\) khác rỗng và không bị chặn', r'\(\Delta\) rỗng', r'\(Q=0\)'],
   r'Với Q xác định âm, f giảm vô hạn dọc mọi hướng lùi khác 0 nên miền phải compact (không có hướng lùi). Slide ghi “nửa xác định âm”, cần “xác định âm”.', B)
tf('S', r(30), r'Hệ quả 4 đúng cả khi Q = 0 (vừa nửa xác định dương vừa nửa xác định âm).', False,
   r'Với \(Q=0\) bài toán là LP: \(\min x\) s.t. \(x\ge0\) có nghiệm nhưng \(\Delta=[0,\infty)\) không compact. Cần Q <b>xác định âm</b>.', B)
tf('S', r(24), r'Với QP, nếu \(f\) bị chặn dưới trên polyhedron Δ thì f đạt cực tiểu trên Δ.', True, r'Đây chính là định lý Frank–Wolfe.', B)
tf('S', r(24), r'Định lý Frank–Wolfe vẫn đúng nếu Δ là miền không phải polyhedron.', False, r'Ví dụ \(\min x_1\) trên \(x_1x_2\ge1\) (slide tr.25) phản bác.', B)
mc('S', r(29), r'Bài toán \(\min x_1^2+x_2^2\) s.t. \(x_1+x_2\ge1\): theo Hệ quả 3 nghiệm tồn tại vì',
   r'\(Q=2I\succ0\) và \(\Delta\ne\emptyset\)', [r'Δ compact', r'\(c=0\)', r'Δ có điểm trong nên nghiệm tồn tại'],
   r'Chỉ cần \(Q\succ0\) và Δ khác rỗng. Nghiệm \((0.5,0.5)\).', B)
mc('S', r(27), r'Bài toán LP \(\min x\) s.t. \(x\ge0\) (Q = 0). Điều kiện (3) của Eaves kiểm với \(v=1\): \(Av=1\ge0\), \(v^\top Qv=0\), \((Qx+c)^\top v=c\cdot v=1\)',
   r'\(\ge0\): đủ điều kiện, bài toán có nghiệm \(x=0\)', [r'\(<0\): bài toán không có nghiệm', r'bằng 0: mọi x đều là nghiệm', r'không xác định'],
   r'Với \(c=1\) thì \(c v=1\ge0\) nên thỏa: nghiệm \(x=0\). Nếu \(c=-1\) thì \(-1<0\) vi phạm (LP không bị chặn dưới).', B)
mc('S', r(26), r'Bài toán \(\min-x^2\) s.t. \(x\ge0\) không có nghiệm vì',
   r'\(Q=-2<0\), \(A=1\): \(v=1\), \(Av\ge0\) nhưng \(v^\top Qv=-2<0\) vi phạm điều kiện (2)', [r'\(\Delta\) rỗng', r'\(Q\succ0\)', r'\(c\ne0\)'],
   r'\(f(x)=-x^2\to-\infty\) khi \(x\to\infty\) trên \([0,\infty)\); Eaves (2) vi phạm.', B)
num('S', r(23), r'\(\min-x^2\) trên \(x\ge0\): giá trị \(f(10)\) là', -100, r'\(-(10)^2=-100\) và tiếp tục giảm khi x tăng ⇒ \(\bar\theta=-\infty\).', ans_text='-100', grp=B)
essay('B', r(24), r'Phát biểu định lý Frank–Wolfe và cho một phản ví dụ khi Δ không phải polyhedron (slide tr.24–25).',
      r'<p><b>Frank–Wolfe:</b> nếu \(\bar\theta=\inf\{f(x):x\in\Delta(A,b)\}\) là số thực hữu hạn thì bài toán \(\min\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax\ge b\) có nghiệm.</p><p><b>Phản ví dụ:</b> \(\min x_1\) trên \(\Delta=\{x_1x_2\ge1,x_1,x_2\ge0\}\) (không phải polyhedron): \(f=x_1\) toàn phương-tuyến tính, \(\bar\theta=0\) hữu hạn (lấy \(x=(t,1/t)\), \(t\to0^+\)) nhưng \(x_1>0\) trên Δ nên không đạt.</p>',
      ['Phát biểu đúng giả thiết (Δ polyhedron, \\(\\bar\\theta\\) hữu hạn)', 'Phản ví dụ có infimum không đạt'], B)
essay('S', r(26), r'Nêu ý nghĩa của ba điều kiện trong định lý Eaves bằng cách xét \(f(x+tv)\) với \(Av\ge0\).',
      r'<p>Nếu \(x\in\Delta\) và \(Av\ge0\) thì \(x+tv\in\Delta\ \forall t\ge0\). \(f(x+tv)=f(x)+t(Qx+c)^\top v+\tfrac{t^2}2v^\top Qv\). Để f không giảm về \(-\infty\): hệ số \(t^2\) phải \(\ge0\) (điều kiện 2: \(v^\top Qv\ge0\)); nếu bằng 0 thì hệ số \(t\) phải \(\ge0\) (điều kiện 3). Điều kiện (1) là miền khác rỗng. Đó cũng là điều kiện đủ.</p>',
      ['Viết khai triển \\(f(x+tv)\\)', 'Diễn giải hệ số \\(t^2\\) và \\(t\\)'], B)

# =====================================================================  C. TÍNH CHẤT TẬP NGHIỆM
C = 'C. Tính chất của tập nghiệm'
mc('G', r(33), r'Ký hiệu \(\mathrm{Sol}(P)\) trong phần 3 của slide là',
   'tập các nghiệm (cực tiểu toàn cục) của bài toán QP (P)', ['tập các ràng buộc chặt', 'tập các nhân tử Lagrange', 'tập các điểm cực biên'],
   r'Slide tr.33: “Ký hiệu: Sol(P) là tập các nghiệm của bài toán QHTP (P)”.', C)
mc('G', r(34), r'Bài toán thuần nhất \((P_0)\) liên kết với (P) là',
   r'\(\min\tfrac12v^\top Qv\) s.t. \(Av\ge0,\ Cv=0\)', [r'\(\min c^\top v\) s.t. \(Av\ge b\)', r'\(\min\tfrac12v^\top Qv+c^\top v\) s.t. \(Av\ge b\)', r'\(\min v^\top v\) s.t. \(Cv=d\)'],
   r'Slide tr.34: bỏ phần tuyến tính và thay vế phải bằng 0 (chỉ giữ “phần hướng”).', C)
mc('G', r(36), r'Nghiệm tia của bài toán (P) là',
   r'nửa đường thẳng \(\{\bar x+t\bar v:t\ge0\}\), \(\bar v\ne0\), nằm trong \(\mathrm{Sol}(P)\)', [r'một điểm cực biên của Δ', r'một đoạn thẳng bị chặn nằm trong Δ', r'đường thẳng vuông góc với Δ'],
   r'Slide tr.36 (định nghĩa). Nếu tồn tại nghiệm tia thì tập nghiệm không bị chặn.', C)
mc('G', r(36), r'Định lý 3.1: \(\mathrm{Sol}(P)\) không bị chặn khi và chỉ khi',
   'P có nghiệm tia', ['Q xác định dương', 'Δ compact', 'có ít nhất hai nghiệm'],
   r'Slide tr.36: “Tập nghiệm Sol(P) không bị chặn nếu và chỉ nếu (P) có nghiệm tia”, kèm điều kiện \((Q\bar x+c)^\top\bar v=0\).', C)
tf('G', r(36), r'Theo Định lý 3.1, điều kiện cần và đủ để \(\mathrm{Sol}(P)\) không bị chặn là tồn tại \(\bar x\in\mathrm{Sol}(P)\), \(\bar v\in\mathrm{Sol}(P_0)\setminus\{0\}\) sao cho \((Q\bar x+c)^\top\bar v=0\).', True, r'Đúng theo slide tr.36.', C)
mc('G', r(38), r'Định lý 3.2 nói',
   r'\(\mathrm{Sol}(P)\) của bài toán QP là tập đóng', [r'\(\mathrm{Sol}(P)\) luôn bị chặn', r'\(\mathrm{Sol}(P)\) luôn lồi', r'\(\mathrm{Sol}(P)\) luôn hữu hạn'],
   r'Slide tr.38. Chú ý: tập cực tiểu địa phương \(\mathrm{loc}(P)\) có thể KHÔNG đóng (slide tr.39).', C)
mc('B', r(38), r'Ví dụ (P1) slide tr.38: \(\min-x_2^2+x_1x_2\) với \(x_1,x_2\ge0\). Kết luận đúng là',
   r'\(\mathrm{Sol}(P_1)=\emptyset\), \(\mathrm{loc}(P_1)=\{x_1>0,x_2=0\}\) không đóng', [r'\(\mathrm{Sol}(P_1)=\{(0,0)\}\)', r'\(\mathrm{Sol}(P_1)=\mathrm{loc}(P_1)=\{x_2=0\}\)', r'\(\mathrm{Sol}(P_1)\) là tập lồi bị chặn'],
   r'\(f(0,t)=-t^2\to-\infty\) nên không có nghiệm; tại \((a,0)\), \(a>0\): \(f=x_2(a-x_2)\ge0=f(a,0)\) nên là cực tiểu địa phương; \((0,0)\) thì không.', C)
tf('B', r(38), r'Trong ví dụ (P1), điểm \((0,0)\) là cực tiểu địa phương.', False, r'\(f(0,t)=-t^2<0=f(0,0)\) với \(t>0\) nhỏ, nên không.', C)
tf('B', r(39), r'Tập nghiệm cực tiểu địa phương \(\mathrm{loc}(P)\) của bài toán QP luôn là tập đóng.', False, r'Slide tr.39 “Lưu ý”: loc(P) có thể không đóng; ví dụ (P1).', C)
mc('G', r(40), r'Định lý 3.3 (a): nếu Q xác định dương và Δ khác rỗng thì',
   'bài toán (P) có nghiệm duy nhất, \\(\\mathrm{Sol}(P)=\\mathrm{loc}(P)\\)', ['bài toán có vô số nghiệm', 'nghiệm là điểm cực biên của Δ', 'bài toán không có nghiệm'],
   r'Slide tr.40: f lồi chặt (Q ≻ 0) ⇒ nghiệm duy nhất và mọi cực tiểu địa phương là toàn cục.', C)
mc('G', r(40), r'Định lý 3.3 (b): nếu Q xác định âm thì mỗi cực tiểu địa phương (nếu có) là',
   'một điểm cực biên của Δ', ['một điểm trong của Δ', 'một điểm biên không phải đỉnh', 'điểm tối ưu không duy nhất'],
   r'Slide tr.40: \(\mathrm{Sol}(P)\subset\mathrm{loc}(P)\subset\mathrm{extr}\,\Delta\), số nghiệm nhỏ hơn số điểm cực biên. Lý do: f lõm chặt nên không thể cực tiểu ở điểm không cực biên.', C)
mc('G', r(40), r'Định lý 3.3 (c): nếu Q nửa xác định dương thì \(\mathrm{Sol}(P)\)',
   'là tập lồi đóng', ['luôn có đúng một phần tử', 'là tập rời rạc hữu hạn', 'không lồi'],
   r'Slide tr.40. Hơn nữa, nếu Sol(P) hữu hạn thì rỗng hoặc chỉ có một phần tử.', C)
tf('G', r(40), r'Với Q nửa xác định dương, nếu \(\mathrm{Sol}(P)\) hữu hạn thì nó rỗng hoặc chỉ có một phần tử.', True, r'Tập lồi hữu hạn phải rỗng hoặc một điểm (hai điểm phân biệt kéo theo cả đoạn).', C)
mc('B', r(41), r'Ví dụ slide tr.41: \(\min-x_1^2-x_2^2+1\) trên \([-1,1]^2\). Q là',
   r'\(\begin{pmatrix}-2&0\\0&-2\end{pmatrix}\) xác định âm', [r'\(\begin{pmatrix}2&0\\0&2\end{pmatrix}\) xác định dương', r'\(\begin{pmatrix}-2&0\\0&2\end{pmatrix}\) không xác định', r'\(\begin{pmatrix}0&0\\0&0\end{pmatrix}\)'],
   r'\(f=\tfrac12x^\top\mathrm{diag}(-2,-2)x+1\). Q xác định âm ⇒ nghiệm nằm ở đỉnh.', C)
mc('B', r(41), r'Trong ví dụ slide tr.41, tập nghiệm \(\mathrm{Sol}(P)\) gồm',
   'bốn đỉnh \\((\\pm1,\\pm1)\\) của hình vuông', ['chỉ điểm \\((0,0)\\)', 'toàn bộ biên của hình vuông', 'đúng một đỉnh'],
   r'\(f=1-x_1^2-x_2^2\) nhỏ nhất khi \(x_1^2+x_2^2\) lớn nhất: tại \((\pm1,\pm1)\), \(f=-1\). \(\mathrm{Sol}=\mathrm{loc}=\mathrm{extr}(\Delta)\).', C)
num('B', r(41), r'Giá trị tối ưu của \(\min-x_1^2-x_2^2+1\) trên \([-1,1]^2\) là', -1, r'Tại đỉnh \((1,1)\): \(-1-1+1=-1\).', ans_text='-1', grp=C)
tf('B', r(42), r'Tập nghiệm của ví dụ \(\min-x_1^2-x_2^2+1\) trên \([-1,1]^2\) là tập lồi.', False, r'Bốn điểm rời nhau; trung điểm của \((1,1)\) và \((-1,-1)\) là gốc, không phải nghiệm. Slide tr.42: “Sol(P) không phải là tập lồi”.', C)
tf('G', r(43), r'Nghiệm của bài toán QP có thể là điểm trong của tập ràng buộc Δ.', True, r'Slide tr.43: \(\mathrm{Sol}(P)\cap\mathrm{int}\,\Delta\) có thể khác rỗng (khác với LP).', C)
mc('B', r(44), r'Ví dụ 1 slide tr.44: \(\min x^2\) với \(-1\le x\le1\). Nghiệm là',
   r'\(x=0\), nằm trong khoảng \((-1,1)\)', [r'\(x=1\)', r'\(x=-1\)', r'không có nghiệm'],
   r'\(Q=1\succ0\): QP lồi; nghiệm \(x=0\) là điểm trong. Vậy \(\mathrm{Sol}(P)\cap\mathrm{int}\,\Delta\ne\emptyset\).', C)
mc('B', r(45), r'Ví dụ 2 slide tr.45: \(\min x_1^2+x_2^2\) trên \([-1,1]^2\). Nghiệm và Q là',
   r'\(x^*=(0,0)\) và \(Q=\mathrm{diag}(2,2)\succ0\)', [r'\(x^*=(1,1)\) và \(Q=\mathrm{diag}(2,2)\)', r'\(x^*=(0,0)\) và \(Q=\mathrm{diag}(1,1)\)', r'\(x^*=(1,-1)\) và \(Q\prec0\)'],
   r'Nghiệm duy nhất \((0,0)\) là điểm trong của hình vuông (slide tr.45).', C)
tf('S', r(43), r'Nếu nghiệm của QP lồi là điểm trong của Δ thì mọi nhân tử \(\lambda_i\) bằng 0 và KKT rút gọn thành \(Qx^*+c=0\).', True, r'Không có ràng buộc chặt ⇒ bù cho \(\lambda_i=0\).', C)
mc('S', r(40), r'Trong QP với \(Q\prec0\) và Δ là polytope, để tìm nghiệm ta chỉ cần xét',
   'các đỉnh (điểm cực biên) của Δ', ['các điểm trong của Δ', 'các điểm có \\(\\lambda=0\\)', 'điểm có f = 0'],
   r'Định lý 3.3(b): \(\mathrm{Sol}\subset\mathrm{extr}\,\Delta\); polytope có hữu hạn đỉnh nên chỉ cần so sánh f tại các đỉnh.', C)
mc('S', r(40), r'\(\min x_1^2+x_2^2\) trên \(\{x_1+x_2\ge2\}\) (Q ≻ 0). Số nghiệm là',
   'đúng một: \\((1,1)\\)', ['vô số nghiệm trên đường \\(x_1+x_2=2\\)', 'hai nghiệm', 'không có nghiệm'],
   r'Q ≻ 0 ⇒ duy nhất. \((1,1)\) là điểm gần gốc nhất trên miền.', C)
mc('S', r(40), r'\(\min(x_1+x_2)^2\) (Q nửa xác định dương) trên \(x\in\mathbb R^2\). Tập nghiệm là',
   r'đường thẳng \(x_1+x_2=0\) (lồi, không bị chặn)', [r'một điểm \((0,0)\)', r'hai điểm \((\pm1,\mp1)\)', r'tập rỗng'],
   r'\(f=0\) trên cả đường thẳng; \(Q=\begin{pmatrix}2&2\\2&2\end{pmatrix}\succeq0\) không xác định dương ⇒ nghiệm không duy nhất. Có nghiệm tia (Định lý 3.1).', C)
tf('S', r(36), r'Bài toán \(\min(x_1+x_2)^2\) trên \(\mathbb R^2\) có nghiệm tia (do Sol không bị chặn).', True, r'Sol là đường thẳng \(x_1+x_2=0\); nửa đường thẳng nào của nó cũng nằm trong Sol.', C)
tf('S', r(40), r'Nếu Q ≻ 0 thì tập nghiệm của QP (Δ ≠ ∅) có thể chứa hơn một điểm.', False, r'Q ≻ 0 ⇒ f lồi chặt ⇒ nghiệm duy nhất.', C)
tf('S', r(40), r'Nếu Q ≺ 0 và Δ là polytope thì nghiệm của QP có thể nằm ở điểm trong của Δ.', False, r'Định lý 3.3(b): cực tiểu địa phương là điểm cực biên (đỉnh), không phải điểm trong.', C)
tf('S', r(38), r'Tập nghiệm Sol(P) của QP không thể rỗng nếu \(\Delta\ne\emptyset\).', False, r'Ví dụ (P1) có Δ ≠ ∅ nhưng Sol = ∅; hoặc \(\min x_1\) trên \(x_1\ge0,x_2\ge0\) không cần… QP không lồi có thể vô nghiệm.', C)
essay('B', r(38), r'Xét \(\min-x_2^2+x_1x_2\) với \(x_1,x_2\ge0\) (slide tr.38). Chứng minh \(\mathrm{Sol}(P)=\emptyset\) và xác định \(\mathrm{loc}(P)\).',
      r'<p>Với \(x=(0,t)\): \(f=-t^2\to-\infty\) khi \(t\to\infty\) ⇒ \(\inf f=-\infty\), không đạt: \(\mathrm{Sol}=\emptyset\).</p><p>\(f(x_1,x_2)=x_2(x_1-x_2)\). Nếu \(x_1>0\): với \(x_2\in[0,x_1]\) có \(f\ge0=f(x_1,0)\) ⇒ \((x_1,0)\) là cực tiểu địa phương. Nếu \(x_1=0\): \(f(0,x_2)=-x_2^2<0\) ⇒ không có cực tiểu địa phương (kể cả \((0,0)\), vì \(f(0,t)<f(0,0)\)). Nếu \(x_2>0\), \(x_1\ge0\): dọc \((x_1,x_2+s)\) f giảm (thử) ⇒ không cực tiểu. Vậy \(\mathrm{loc}=\{x_1>0,x_2=0\}\), không đóng (thiếu \((0,0)\)).</p>',
      ['Chỉ ra \\(f\\to-\\infty\\)', 'Xác định loc và điểm biên bị thiếu'], C)
essay('S', r(40), r'So sánh tính chất tập nghiệm của QP trong ba trường hợp Q ≻ 0, Q ≺ 0, Q ⪰ 0 (Định lý 3.3). Cho ví dụ cho mỗi trường hợp.',
      r'<p>Q ≻ 0: nghiệm duy nhất (ví dụ \(\min x_1^2+x_2^2\) trên \(x_1+x_2\ge2\): \((1,1)\)). Q ≺ 0: cực tiểu địa phương là điểm cực biên; Sol có thể không lồi (ví dụ \(\min-x_1^2-x_2^2+1\) trên \([-1,1]^2\): bốn đỉnh). Q ⪰ 0: Sol lồi đóng, có thể vô số nghiệm (ví dụ \(\min(x_1+x_2)^2\): cả đường thẳng \(x_1+x_2=0\)).</p>',
      ['Đủ ba trường hợp', 'Ví dụ cụ thể cho từng trường hợp'], C)

# =====================================================================  D. NULL SPACE
D = 'D. Phương pháp không gian hạt nhân'
mc('G', r(46), r'Phương pháp không gian hạt nhân (null space) trong slide dùng để giải',
   'bài toán QP có ràng buộc đẳng thức', ['bài toán QP có ràng buộc bất đẳng thức', 'bài toán QHTT', 'bài toán không ràng buộc bất kỳ'],
   r'Slide tr.46: null space cho ràng buộc đẳng thức; active set cho bất đẳng thức.', D)
mc('G', r(46), r'Phương pháp tập hoạt động (active set) trong slide dùng để giải',
   'bài toán QP có ràng buộc bất đẳng thức', ['bài toán QP có ràng buộc đẳng thức', 'bài toán không ràng buộc', 'bài toán vận tải'],
   r'Slide tr.46; mỗi vòng của active set dùng null space cho bài toán con.', D)
mc('G', r(47), r'Bài toán QP đẳng thức của slide tr.47 giả thiết',
   r'Q đối xứng nửa xác định dương, \(A\in\mathbb R^{m\times n}\) (m ≤ n), \(\mathrm{rank}A=m\)', [r'Q khả nghịch bất kỳ, A vuông', r'Q xác định âm, \(\mathrm{rank}A<m\)', r'Q = 0 và A không có hàng nào'],
   r'\(\mathrm{rank}A=m\) nghĩa là các ràng buộc độc lập tuyến tính.', D)
mc('G', r(48), r'Hàm Lagrange của QP đẳng thức là',
   r'\(L=\tfrac12x^\top Qx+c^\top x+\mu^\top(Ax-b)\)', [r'\(L=\tfrac12x^\top Qx+c^\top x+\mu^\top(Ax-b)^2\)', r'\(L=\tfrac12x^\top Qx-\mu^\top A\)', r'\(L=c^\top x+\mu^\top(Ax-b)\)'],
   r'Slide tr.48 (nhân tử \(\mu\) không bị ràng buộc dấu vì đẳng thức).', D)
mc('G', r(48), r'Điều kiện KKT (4.1) của QP đẳng thức là',
   r'\(Qx^*+c+A^\top\mu^*=0\) và \(Ax^*=b\)', [r'\(Qx^*+c=0\) và \(Ax^*=b\)', r'\(Qx^*+c+A\mu^*=0\) và \(A^\top x^*=b\)', r'\(Q+c+A^\top\mu=0\) và \(x=b\)'],
   r'\(\nabla_xL=Qx+c+A^\top\mu\); \(\nabla_\mu L=Ax-b\). (Kích thước: \(A^\top\mu\in\mathbb R^n\).)', D)
tf('G', r(48), r'Vì hàm mục tiêu lồi và ràng buộc affine nên \(x^*\) là nghiệm khi và chỉ khi \(x^*\) là điểm KKT.', True, r'Slide tr.48: KKT cần và đủ cho QP lồi ràng buộc affine (không cần Slater).', D)
mc('G', r(49), r'Vì sao slide đổi biến \(d=x-\bar x\)?',
   'để đưa về hệ KKT có ma trận hệ số đối xứng', ['để biến bài toán thành không lồi', 'để loại bỏ ràng buộc đẳng thức', 'để tránh dùng nhân tử'],
   r'Slide tr.49: hệ (4.1) có ma trận hệ số không đối xứng khi viết theo \((x,\mu)\); sau đổi biến ta được hệ (4.2).', D)
mc('G', r(50), r'Hệ KKT đối xứng (4.2) là',
   r'\(\begin{pmatrix}Q&A^\top\\A&0\end{pmatrix}\begin{pmatrix}d^*\\\mu^*\end{pmatrix}=\begin{pmatrix}-\bar g\\\bar b\end{pmatrix}\)', [r'\(\begin{pmatrix}Q&A\\A^\top&0\end{pmatrix}\begin{pmatrix}d\\\mu\end{pmatrix}=\begin{pmatrix}\bar g\\\bar b\end{pmatrix}\)', r'\(\begin{pmatrix}Q&0\\0&A^\top\end{pmatrix}\begin{pmatrix}d\\\mu\end{pmatrix}=\begin{pmatrix}-\bar g\\0\end{pmatrix}\)', r'\(\begin{pmatrix}A&Q\\0&A^\top\end{pmatrix}\begin{pmatrix}d\\\mu\end{pmatrix}=\begin{pmatrix}\bar b\\-\bar g\end{pmatrix}\)'],
   r'Từ \(Qd+A^\top\mu=-\bar g\) và \(Ad=\bar b\) với \(\bar g=Q\bar x+c\), \(\bar b=b-A\bar x\) (slide tr.50).', D)
mc('G', r(49), r'Trong (PD), \(\bar g\) và \(\bar b\) được định nghĩa bởi',
   r'\(\bar g=Q\bar x+c\), \(\bar b=b-A\bar x\)', [r'\(\bar g=c\), \(\bar b=b\)', r'\(\bar g=Q\bar x\), \(\bar b=A\bar x\)', r'\(\bar g=c-Q\bar x\), \(\bar b=A\bar x-b\)'],
   r'Slide tr.49. Khi \(\bar x=0\) thì \(\bar g=c\), \(\bar b=b\).', D)
mc('G', r(51), r'Ma trận Z trong phương pháp null space là',
   r'ma trận cỡ \(n\times(n-m)\) có các cột sinh \(\ker A\), thỏa \(AZ=0\)', [r'ma trận cỡ \(m\times m\) nghịch đảo của A', r'ma trận cỡ \(n\times m\) thỏa \(AZ=I\)', r'ma trận đường chéo của các nhân tử'],
   r'Slide tr.51: Z là ma trận cơ sở của không gian hạt nhân \(\ker A\).', D)
mc('G', r(51), r'Ma trận Hessian rút gọn (reduced Hessian) là',
   r'\(Z^\top QZ\)', [r'\(Q^\top Z\)', r'\(A^\top Z\)', r'\(ZQ^{-1}Z^\top\)'],
   r'Dạng toàn phương hạn chế lên \(\ker A\) (slide tr.51).', D)
mc('G', r(51), r'Mệnh đề slide tr.51: nếu \(\mathrm{rank}A=m\) và \(Z^\top QZ\succ0\) thì',
   'hệ (4.2) không suy biến, có duy nhất \\((d^*,\\mu^*)\\) và (P) có nghiệm duy nhất', ['bài toán không có nghiệm', 'Q phải xác định dương', 'nghiệm không tồn tại nhân tử'],
   r'Đó là điều kiện đủ để dùng null space. Lưu ý chỉ cần \(Z^\top QZ\succ0\), không cần Q ≻ 0.', D)
mc('G', r(52), r'Ma trận Y trong phương pháp null space thỏa',
   r'\([Y\ Z]\) là ma trận vuông không suy biến (có thể chọn \(AY=I\))', [r'\(YZ=0\) và \(Y^\top Y=I\)', r'\(Y=Z^\top\)', r'\(Y=A^{-1}\)'],
   r'Slide tr.52: Y cỡ \(n\times m\) bổ sung cho Z để \([Y\ Z]\) khả nghịch; chọn \(AY=I\) để đơn giản.', D)
mc('G', r(52), r'Phân tích \(d=Yd_Y+Zd_Z\) có \(d_Y,d_Z\) lần lượt thuộc',
   r'\(\mathbb R^m\) và \(\mathbb R^{n-m}\)', [r'\(\mathbb R^n\) và \(\mathbb R^m\)', r'\(\mathbb R^{n-m}\) và \(\mathbb R^m\)', r'\(\mathbb R^n\) và \(\mathbb R^n\)'],
   r'Y có m cột, Z có \(n-m\) cột.', D)
mc('G', r(54), r'Vì \(AZ=0\), từ (4.5) suy ra \(d_Y\) được tính bởi',
   r'\(AYd_Y=\bar b\)', [r'\(Z^\top QZd_Y=\bar b\)', r'\((AY)^\top d_Y=\bar g\)', r'\(d_Y=Z^\top\bar g\)'],
   r'\(Ad=AYd_Y+AZd_Z=AYd_Y=\bar b\). Vì \(AY\) khả nghịch (\(m\times m\)) nên \(d_Y=(AY)^{-1}\bar b\).', D)
mc('G', r(54), r'Nhân phương trình dừng với \(Z^\top\) cho phương trình tính \(d_Z\):',
   r'\(Z^\top QZd_Z=-(Z^\top QYd_Y+Z^\top\bar g)\)', [r'\(Z^\top QZd_Z=Z^\top QYd_Y+Z^\top\bar g\)', r'\(Z^\top Ad_Z=\bar b\)', r'\(Qd_Z=-\bar g\)'],
   r'\(Z^\top A^\top\mu=(AZ)^\top\mu=0\), nên số hạng nhân tử biến mất (slide tr.54, phương trình (4.6)).', D)
mc('G', r(55), r'Để tính \(\mu^*\) ta nhân phương trình dừng với \(Y^\top\) và giải',
   r'\((AY)^\top\mu^*=-Y^\top(\bar g+Qd)\)', [r'\((AZ)^\top\mu^*=-Z^\top\bar g\)', r'\(\mu^*=Y^\top\bar b\)', r'\(\mu^*=-A\bar g\)'],
   r'Slide tr.55 viết “\(-Y^\top\bar g+Gd\)”; suy dẫn đúng là \(-Y^\top(\bar g+Qd)\). AY khả nghịch nên giải được \(\mu\).', D)
mc('B', r(56), r'Ví dụ slide tr.56–58 (3 biến, 2 ràng buộc). Số chiều của \(d_Y\) và \(d_Z\) là',
   'hai và một', ['một và hai', 'ba và một', 'hai và hai'],
   r'\(n=3\), \(m=2\): \(d_Y\in\mathbb R^2\), \(d_Z\in\mathbb R^{n-m}=\mathbb R\).', D)
mc('B', r(57), r'Trong ví dụ slide tr.57, \(Z=(-1,1,1)^\top\). Kiểm \(AZ\) với \(A=\begin{pmatrix}1&1&0\\1&0&1\end{pmatrix}\) ta được',
   r'\(AZ=(0,0)^\top\)', [r'\(AZ=(1,1)^\top\)', r'\(AZ=(-1,-1)^\top\)', r'\(AZ=(2,0)^\top\)'],
   r'\(1\cdot(-1)+1\cdot1+0=0\); \(1\cdot(-1)+0+1\cdot1=0\). Vậy Z nằm trong \(\ker A\).', D)
mc('B', r(58), r'Ví dụ slide tr.58 cho \(d_Y=(4,10)^\top\). Điều đó đến từ',
   r'\(AY=I\) và \(\bar b=b=(4,10)^\top\) (vì \(\bar x=0\))', [r'\(AZ=I\) và \(\bar g=c\)', r'\(Y=A^\top\) và \(\bar g=(4,10)\)', r'\(Z^\top QZ=(4,10)\)'],
   r'\(d_Y=(AY)^{-1}\bar b=I\cdot(4,10)^\top\).', D)
num('B', r(58), r'Trong ví dụ slide tr.57, tính \(Z^\top QZ\) (số vô hướng) với \(Q=\begin{pmatrix}2&-2&-1\\-2&2&1\\-1&1&5\end{pmatrix}\), \(Z=(-1,1,1)^\top\).', R['m3_null_steps']['ZtQZ'][0][0],
    r'\(QZ=(-2-2-1,\ 2+2+1,\ 1+1+5)=(-5,5,7)\); \(Z^\top QZ=5+5+7=17\).', ans_text='17', grp=D)
num('B', r(58), r'Giá trị \(d_Z\) trong ví dụ (làm tròn 4 chữ số thập phân) bằng', R['m3_null_steps']['dZ'][0],
    r'\(d_Z=-(Z^\top QYd_Y+Z^\top\bar g)/17=27.333.../17\approx1.6078\) (khớp slide 1.6078).', tol=1e-3, ans_text='1.6078', grp=D)
mc('B', r(58), r'Nghiệm của ví dụ null space theo slide (và theo code với Q, c như slide) là',
   r'\(x^*=(3.0588,\ 0.9412,\ 6.9412)^\top\)', [r'\(x^*=(4.1765,\ -0.1765,\ 5.8235)^\top\)', r'\(x^*=(4,\ 0,\ 6)^\top\)', r'\(x^*=(3,\ 1,\ 7)^\top\)'],
   r'Đối chiếu SLSQP: ' + str(R['m3_null_ex_num'][0]) + r'. Điểm \((4.1765,-0.1765,5.8235)\) là nghiệm nếu cực tiểu đa thức ghi trên slide (Hessian \(2Q\)).', D)
mc('B', r(58), r'Giá trị \(\tfrac12x^{*\top}Qx^*+c^\top x^*\) của ví dụ (Q, c như slide) là',
   r'\(' + f"{NE['f']}" + r'\)', [r'\(212.7059\)', r'\(191.4706\)', r'\(0\)'],
   r'Slide ghi \(212.7059\): đó là giá trị của <i>đa thức</i> \(2x_1^2-4x_1x_2-\dots\) tại \(x^*\) (Hessian \(2Q\)), không phải giá trị của dạng \(\tfrac12x^\top Qx+c^\top x\). Xem trang “Kiểm chứng”.', D)
num('B', r(58), r'Giá trị \(\tfrac12x^{*\top}Qx^*+c^\top x^*\) (Q, c như slide) làm tròn 2 chữ số thập phân', float(NE['f']),
    r'Code: ' + str(NE['f']) + r'; slide ghi 212.7059 là giá trị của đa thức tại x*.', tol=1e-4, ans_text=str(NE['f']), grp=D)
mc('B', r(58), r'Nhân tử \(\mu^*\) của ví dụ theo slide là',
   r'\((23.2941,\ -30.5882)^\top\)', [r'\((30.5882,\ -23.2941)^\top\)', r'\((23.2941,\ 30.5882)^\top\)', r'\((-23.2941,\ -30.5882)^\top\)'],
   r'Khớp với \(\mu=(AY)^{-\top}(-Y^\top(\bar g+Qd))\) (code). Nhân tử của ràng buộc đẳng thức được phép âm.', D)
mc('B', r(59), r'Bài tập 1 slide tr.59 ghi ĐS \((2,-1,1)^\top\). Với ràng buộc ghi trên slide (\(x_1+x_3=0\)), điểm \((2,-1,1)\)',
   r'không thỏa ràng buộc thứ nhất (\(2+1=3\ne0\))', [r'thỏa cả hai ràng buộc', r'là nghiệm với \(\mu=(0,0)\)', r'thỏa vì \(x_2+x_3=0\) nên đủ'],
   r'\(x_1+x_3=2+1=3\). Đáp số khớp nếu ràng buộc là \(x_1+x_3=3\) (code: \(x^*=(2,-1,1)\), \(\mu=(-3,2)\), \(f=-3.5\)).', D)
num('B', r(59), r'Bài tập 1 với ràng buộc \(x_1+x_3=3,\ x_2+x_3=0\): giá trị hàm mục tiêu tại nghiệm \((2,-1,1)\) là', float(EB['f']),
    r'\(f=3\cdot4+2(2)(-1)+2\cdot1+2.5\cdot1+2(-1)(1)+2\cdot1-16+3-3=12-4+2+2.5-2+2-16+3-3=-3.5\).', ans_text='-3.5', grp=D)
num('B', r(59), r'Bài tập 1 với \(b=(0,0)\) (đúng như slide viết): thành phần \(x_1^*\) của nghiệm, làm tròn 4 chữ số', float(BT1['x*'][0]),
    r'\(x^*=(0.6154,0.6154,-0.6154)\) (\(=8/13\)). Kiểm SLSQP.', tol=1e-3, ans_text='0.6154', grp=D)
tf('S', r(51), r'Để dùng null space cần \(Q\succ0\) trên toàn \(\mathbb R^n\).', False, r'Chỉ cần \(Z^\top QZ\succ0\) (Hessian rút gọn) cùng \(\mathrm{rank}A=m\).', D)
tf('S', r(51), r'Nếu \(Z^\top QZ\succ0\) và \(\mathrm{rank}A=m\) thì QP đẳng thức có nghiệm duy nhất.', True, r'Mệnh đề slide tr.51.', D)
tf('S', r(54), r'Trong null space, \(d_Y\) phụ thuộc vào Q còn \(d_Z\) chỉ phụ thuộc vào A.', False, r'Ngược lại: \(d_Y=(AY)^{-1}\bar b\) chỉ phụ thuộc A, b; \(d_Z\) phụ thuộc \(Z^\top QZ\).', D)
tf('S', r(55), r'Nhân tử \(\mu^*\) của ràng buộc đẳng thức luôn không âm.', False, r'Nhân tử đẳng thức tùy dấu (ví dụ \(\mu_2=-30.5882\) trong slide).', D)
tf('S', r(50), r'Hệ KKT (4.2) có ma trận hệ số đối xứng.', True, r'\(\begin{pmatrix}Q&A^\top\\A&0\end{pmatrix}\) đối xứng vì Q đối xứng.', D)
mc('S', r(50), r'Kích thước của ma trận hệ số trong (4.2) khi có n biến và m ràng buộc đẳng thức là',
   r'\((n+m)\times(n+m)\)', [r'\(n\times n\)', r'\(m\times m\)', r'\(2n\times2m\)'],
   r'Khối \(Q\) cỡ \(n\times n\), \(A^\top\) cỡ \(n\times m\), \(A\) cỡ \(m\times n\), và khối 0 cỡ \(m\times m\).', D)
mc('S', r(48), r'Khi QP đẳng thức có nghiệm duy nhất, kết quả \(x^*\) có phụ thuộc điểm xuất phát \(\bar x\) không?',
   r'không: \(x^*=\bar x+d^*\) không đổi khi đổi \(\bar x\) (chỉ \(d^*\) đổi bù)', [r'có, mỗi \(\bar x\) cho một nghiệm khác', r'chỉ phụ thuộc khi Q đối xứng', r'chỉ phụ thuộc khi \(\mathrm{rank}A<m\)'],
   r'\(\bar x\) chỉ là điểm “dịch gốc”; nghiệm duy nhất của bài toán gốc không phụ thuộc vào nó.', D)
essay('B', r(54), r'Trình bày các bước của phương pháp không gian hạt nhân (công thức \(d_Y\), \(d_Z\), \(d\), \(\mu\)) và điều kiện để áp dụng.',
      r'<p>Điều kiện: Q đối xứng, \(\mathrm{rank}A=m\), \(Z^\top QZ\succ0\).</p><ol><li>Chọn \(\bar x\) (thường 0), \(\bar g=Q\bar x+c\), \(\bar b=b-A\bar x\); chọn Z (cơ sở \(\ker A\)) và Y (sao cho \([Y\ Z]\) khả nghịch, ưu tiên \(AY=I\)).</li><li>\(d_Y=(AY)^{-1}\bar b\).</li><li>Giải \((Z^\top QZ)d_Z=-Z^\top(QYd_Y+\bar g)\).</li><li>\(d=Yd_Y+Zd_Z\), \(x^*=\bar x+d\).</li><li>\((AY)^\top\mu^*=-Y^\top(\bar g+Qd)\) ⇒ \(\mu^*\).</li></ol>',
      ['Nêu đủ điều kiện áp dụng', 'Viết đúng 4–5 công thức', 'Giải thích vì sao \\(AZ=0\\) khử được số hạng nhân tử'], D)
essay('B', r(59), r'Giải Bài tập 1 (slide tr.59) hoàn toàn. Nếu đáp số \((2,-1,1)\) của slide không khớp với ràng buộc ghi trên slide, hãy chỉ ra và tìm phiên bản ràng buộc làm đáp số đúng.',
      r'<p>\(Q=\begin{pmatrix}6&2&1\\2&5&2\\1&2&4\end{pmatrix}\succ0\), \(c=(-8,-3,-3)\), \(A=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}\). Giải hệ KKT \(\begin{pmatrix}Q&A^\top\\A&0\end{pmatrix}\begin{pmatrix}x\\\mu\end{pmatrix}=\begin{pmatrix}-c\\b\end{pmatrix}\).</p><p>Với \(b=(0,0)\): \(x^*=(8/13,8/13,-8/13)\approx(0.6154,0.6154,-0.6154)\), \(\mu=(3.6923,-0.0769)\).</p><p>ĐS \((2,-1,1)\) không thỏa \(x_1+x_3=0\); nó là nghiệm khi \(b=(3,0)\) (\(\mu=(-3,2)\), \(f=-3.5\)).</p>',
      ['Giải được hệ KKT', 'Nhận ra ĐS không khớp b=(0,0)', 'Tìm b làm ĐS đúng'], D)

# =====================================================================  E. ACTIVE SET
E = 'E. Phương pháp tập hoạt động'
mc('G', r(60), r'Trong bài toán của slide tr.60, \(I(x^*)\) là',
   r'\(I(x^*)=\{i\mid a_i^\top x^*=b_i\}\), tập chỉ số ràng buộc hoạt động', [r'\(I(x^*)=\{i\mid a_i^\top x^*<b_i\}\)', r'tập các nhân tử dương', r'tập các điểm khả thi'],
   r'Ràng buộc “active” là ràng buộc chặt (dấu bằng) tại điểm đang xét.', E)
mc('G', r(60), r'Bài toán QP của phương pháp tập hoạt động trong slide có Q',
   'đối xứng và xác định dương', ['đối xứng và xác định âm', 'đường chéo bất kỳ', 'bằng không'],
   r'Slide tr.60: “Q là ma trận đối xứng, xác định dương”; nhờ đó bài toán con luôn có nghiệm duy nhất.', E)
mc('G', r(61), r'Ý tưởng của active set: nếu biết \(I(x^*)\) thì \(x^*\) là nghiệm của bài toán',
   r'\(\min\tfrac12x^\top Qx+c^\top x\) s.t. \(a_i^\top x=b_i,\ i\in I(x^*)\)', [r'\(\min\tfrac12x^\top Qx\) không ràng buộc', r'\(\max\) cùng hàm với ràng buộc \(\le\)', r'bài toán đối ngẫu Lagrange không ràng buộc'],
   r'Giả các ràng buộc hoạt động thành đẳng thức và bỏ các ràng buộc lỏng (slide tr.61).', E)
mc('G', r(61), r'Vì \(I(x^*)\) chưa biết trước, thuật toán',
   'cập nhật dần một tập chỉ số làm việc (working set) \\(W_k\\)', ['giải mọi tổ hợp ràng buộc cùng lúc', 'bỏ qua ràng buộc bất đẳng thức', 'đổi bài toán sang QHTT'],
   r'Slide tr.61 và tr.63: “phương pháp sẽ cập nhật một tập chỉ số làm việc cho đến khi xác định được \(I(x^*)\)”.', E)
mc('G', r(62), r'Điều kiện KKT (4.9) của bài toán active set là',
   r'\(Qx^*+c+\sum_{i\in I(x^*)}\mu_i^*a_i=0\), \(a_i^\top x^*=b_i\), \(\mu_i^*\ge0\)', [r'\(Qx^*+c=0\), \(a_i^\top x^*<b_i\), \(\mu_i^*\le0\)', r'\(Qx^*+c-\sum\mu_i^*a_i=0\), \(\mu_i^*\le0\)', r'\(x^*=0\), \(\mu^*=0\)'],
   r'Slide tr.62–63 với dạng \(a_i^\top x\le b_i\) và \(L=\tfrac12x^\top Qx+c^\top x+\sum\mu_i(a_i^\top x-b_i)\).', E)
mc('G', r(63), r'Mệnh đề nền tảng (slide tr.63): nếu \(x^*\) thỏa (4.9) và Q nửa xác định dương thì',
   r'\(x^*\) là nghiệm toàn cục của (P)', [r'\(x^*\) là cực đại của (P)', r'\(x^*\) chỉ là cực tiểu địa phương', r'(P) vô nghiệm'],
   r'QP lồi với ràng buộc affine: KKT cần và đủ.', E)
mc('G', r(64), r'Ở mỗi vòng k, thuật toán giả sử \(x^k\) khả thi và \(W_k\)',
   r'là tập con của \(I(x^k)\)', [r'là tập chứa mọi ràng buộc', r'rỗng', r'chứa toàn bộ ràng buộc lỏng'],
   r'Slide tr.64: “\(W_k\) là tập con của \(I(x^k)\)”.', E)
mc('G', r(64), r'Bước 1 của active set kiểm tra \(x^k\) có phải nghiệm của \((P_k)\) bằng cách giải bài toán con',
   r'\(\min\tfrac12d^\top Qd+(g^k)^\top d\) s.t. \(a_i^\top d=0,\ i\in W_k\), với \(g^k=Qx^k+c\)', [r'\(\min\tfrac12d^\top Qd\) s.t. \(Ad=b\)', r'\(\min(g^k)^\top d\) s.t. \(a_i^\top d\le0\)', r'\(\max\tfrac12d^\top Qd+g^\top d\) s.t. \(d=0\)'],
   r'Slide tr.64 (bằng null space): ràng buộc \(a_i^\top d=0\) giữ nguyên các ràng buộc trong \(W_k\).', E)
tf('G', r(65), r'Vì \(d=0\) là điểm khả thi của \((PD_k)\) nên giá trị tối ưu của \((PD_k)\) là không dương.', True, r'Slide tr.65: bài toán tìm min, nên giá trị tối ưu \(\le f(0)=0\).', E)
mc('G', r(65), r'Nếu \(d^k=0\) thì (Bước 1)',
   r'\(x^k\) là nghiệm của \((P_k)\); chuyển sang Bước 3', [r'\(x^k\) là nghiệm của (P), dừng ngay', r'\(x^k\) không khả thi', r'phải đổi hướng \(d^k\) thành \(-d^k\)'],
   r'\(d^k=0\) chỉ nói x^k tối ưu khi giữ nguyên \(W_k\); còn phải kiểm dấu nhân tử (Bước 3).', E)
mc('G', r(66), r'Bước 2: độ dài bước \(\alpha_k\) lớn nhất trong \([0,1]\) sao cho \(x^k+\alpha_kd^k\) khả thi được tính bởi',
   r'\(\alpha_k=\min\{1,\ \min_{i\notin W_k,\ a_i^\top d^k>0}(b_i-a_i^\top x^k)/(a_i^\top d^k)\}\)', [r'\(\alpha_k=\max\{1,\ \max_i(b_i-a_i^\top x^k)\}\)', r'\(\alpha_k=\min_{i\in W_k}(b_i-a_i^\top x^k)\)', r'\(\alpha_k=\|d^k\|^{-1}\)'],
   r'Chỉ xét các ràng buộc ngoài \(W_k\) có \(a_i^\top d^k>0\) (tiến tới tường).', E)
mc('G', r(66), r'“Ràng buộc cản” (blocking constraint) là',
   r'ràng buộc cho \(\alpha_k\) nhỏ nhất, làm x^k + αd^k chạm biên', [r'ràng buộc có nhân tử âm nhất', r'ràng buộc mọi điểm khả thi đều thỏa', r'ràng buộc đẳng thức duy nhất'],
   r'Slide tr.66. Sau khi đi, ràng buộc cản trở thành chặt và được thêm vào \(W_k\).', E)
mc('G', r(67), r'Sau Bước 2, nếu có ràng buộc cản thì',
   r'thêm một chỉ số cản vào \(W_k\) và quay lại Bước 1', [r'xóa mọi ràng buộc khỏi \(W_k\)', r'dừng thuật toán', r'đổi hàm mục tiêu'],
   r'Slide tr.67: “bổ sung vào \(W_k\) một trong số các chỉ số của ràng buộc cản (nếu có)”.', E)
mc('G', r(67), r'Bước 3: khi \(d^k=0\), nhân tử \(\hat\mu_i\) được tính từ',
   r'\(Qx^k+c+\sum_{i\in W_k}\hat\mu_ia_i=0\)', [r'\(x^k+\sum\hat\mu_i=0\)', r'\(a_i^\top d^k=\hat\mu_i\)', r'\(\hat\mu_i=b_i-a_i^\top x^k\)'],
   r'Slide tr.67. Đây là điều kiện dừng của bài toán \((P_k)\) (đẳng thức).', E)
mc('G', r(67), r'Nếu mọi \(\hat\mu_i\ge0\) với \(i\in W_k\) (và \(d^k=0\)) thì',
   r'\(x^k\) là nghiệm của bài toán (P): dừng', [r'phải loại mọi ràng buộc', r'phải giảm bước \(\alpha_k\)', r'x^k là cực đại'],
   r'\(x^k\) khả thi và thỏa KKT (4.9) ⇒ nghiệm toàn cục (Q ⪰ 0).', E)
mc('G', r(67), r'Nếu \(d^k=0\) và có \(\hat\mu_j<0\) thì',
   r'loại chỉ số j (thường chọn \(\hat\mu_j\) âm nhất) khỏi \(W_k\): \(W_{k+1}=W_k\setminus\{j\}\)', [r'thêm chỉ số j vào \(W_k\)', r'dừng và báo vô nghiệm', r'đổi dấu \(\hat\mu_j\)'],
   r'Nhân tử âm chỉ ra ràng buộc j đang cản đường giảm f; buông nó ra: \(x^{k+1}=x^k\), \(W_{k+1}=W_k\setminus\{j\}\).', E)
mc('G', r(68), r'Trong thuật toán active set (slide tr.68), nếu \(d^k\ne0\) thì',
   r'tính \(\alpha_k\), đặt \(x^{k+1}=x^k+\alpha_kd^k\)', [r'tính nhân tử \(\hat\mu\)', r'đặt \(W_{k+1}=\emptyset\)', r'kết luận nghiệm là \(x^k\)'],
   r'Nhánh else của thuật toán: di chuyển theo hướng \(d^k\) và cập nhật \(W\) nếu có ràng buộc cản.', E)
tf('G', r(68), r'Ở mỗi vòng của active set, chỉ một ràng buộc được thêm hoặc bị loại khỏi tập làm việc.', True, r'Thuật toán thêm một chỉ số cản, hoặc loại một chỉ số có nhân tử âm nhất (slide tr.67–68).', E)
mc('B', r(69), r'Ví dụ slide tr.69: \(\min(x_1-1)^2+(x_2-0.5)^2\) s.t. \(x_1+x_2\le1\), \(3x_1+x_2\le1.5\), \(x_1,x_2\ge0\). Q và c là',
   r'\(Q=2I\), \(c=(-2,-1)\)', [r'\(Q=I\), \(c=(-1,-0.5)\)', r'\(Q=2I\), \(c=(2,1)\)', r'\(Q=2I\), \(c=(-2,1)\)'],
   r'\((x_1-1)^2+(x_2-0.5)^2=x_1^2+x_2^2-2x_1-x_2+1.25\) ⇒ \(Q=2I\), \(c=(-2,-1)\) (constant bị bỏ). Slide tr.55 ghi nhầm \(c=[-2,1]\) nhưng các bước dùng \((-2,-1)\).', E)
mc('B', r(70), r'Trong ví dụ, tại \(x^0=(0,0)\) các ràng buộc chặt là',
   'ràng buộc 3 và 4 (\\(x_1\\ge0,\\ x_2\\ge0\\)) nên \\(W_0=\\{3,4\\}\\)', ['ràng buộc 1 và 2', 'chỉ ràng buộc 1', 'không có ràng buộc nào chặt'],
   r'\(a_3^\top x^0=0=b_3\), \(a_4^\top x^0=0=b_4\); các ràng buộc 1, 2 có \(0<1\) và \(0<1.5\) (lỏng).', E)
mc('B', r(70), r'Tại \(k=0\) (\(x^0=(0,0)\), \(W_0=\{3,4\}\)), \(g^0=Qx^0+c=\)',
   r'\((-2,-1)\)', [r'\((2,1)\)', r'\((0,0)\)', r'\((-1,-0.5)\)'],
   r'\(Q\cdot0+c=c=(-2,-1)\).', E)

mc('B', r(71), r'Tại \(k=0\), nhân tử \(\hat\mu_3,\hat\mu_4\) tính từ \(g^0+\hat\mu_3(-1,0)^\top+\hat\mu_4(0,-1)^\top=0\) với \(g^0=(-2,-1)\) là',
   r'\(\hat\mu_3=-2\) và \(\hat\mu_4=-1\) (cả hai âm)', [r'\(\hat\mu_3=-2\) và \(\hat\mu_4=1\)', r'\(\hat\mu_3=2\) và \(\hat\mu_4=1\)', r'\(\hat\mu_3=1\) và \(\hat\mu_4=-2\)'],
   r'\(-2-\hat\mu_3=0\Rightarrow\hat\mu_3=-2\); \(-1-\hat\mu_4=0\Rightarrow\hat\mu_4=-1\). Slide tr.71 ghi \(\hat\mu_4=1\) (mâu thuẫn với chính phương trình của nó); kết luận “loại ràng buộc 3 vì âm nhất” không đổi. Xem trang “Kiểm chứng”.', E)
mc('B', r(71), r'Tại \(k=0\) của ví dụ, ràng buộc bị loại khỏi \(W_0\) là',
   'ràng buộc 3: \\(x_1\\ge0\\)', ['ràng buộc 4: \\(x_2\\ge0\\)', 'ràng buộc 2', 'không có ràng buộc bị loại'],
   r'Nhân tử \(\hat\mu_3=-2\) là âm nhất (\(\hat\mu_4=-1\)); loại ràng buộc 3, \(W_1=\{4\}\).', E)
mc('B', r(72), r'Tại \(k=1\), \(W_1=\{4\}\), \(g^1=(-2,-1)\). Nghiệm bài toán con \(d^1\) là',
   r'\(d^1=(1,0)\)', [r'\(d^1=(0,1)\)', r'\(d^1=(-1,0)\)', r'\(d^1=(0,0)\)'],
   r'Ràng buộc \(-d_2=0\Rightarrow d_2=0\); \(\min d_1^2-2d_1\Rightarrow d_1=1\).', E)
mc('B', r(73), r'Tại \(k=1\), \(\alpha_1=\min\{1,\ \min\}\) với các ràng buộc 1 và 2 cho tỉ số \(1\) và \(0.5\). Vậy',
   r'\(\alpha_1=0.5\), ràng buộc cản là ràng buộc 2', [r'\(\alpha_1=1\), ràng buộc cản là ràng buộc 1', r'\(\alpha_1=0.5\), ràng buộc cản là ràng buộc 1', r'\(\alpha_1=0\)'],
   r'Ràng buộc 1: \((1-0)/1=1\); ràng buộc 2: \((1.5-0)/3=0.5\). Nhỏ nhất là 0.5 (ràng buộc 2), nên \(x^2=(0.5,0)\) và \(W_2=\{2,4\}\).', E)
num('B', r(73), r'Tính \(\alpha_1\) của ví dụ (\(k=1\)).', 0.5, r'\(\alpha_1=\min\{1,1,0.5\}=0.5\).', ans_text='0.5', grp=E)
mc('B', r(73), r'Sau vòng \(k=1\), điểm \(x^2\) và tập làm việc \(W_2\) là',
   r'\(x^2=(0.5,0)\), \(W_2=\{2,4\}\)', [r'\(x^2=(1,0)\), \(W_2=\{1,4\}\)', r'\(x^2=(0.5,0)\), \(W_2=\{4\}\)', r'\(x^2=(0,0.5)\), \(W_2=\{2,3\}\)'],
   r'\(x^2=x^1+0.5(1,0)=(0.5,0)\); thêm ràng buộc cản 2 vào \(W_1=\{4\}\).', E)
mc('B', r(74), r'Tại \(k=2\): \(x^2=(0.5,0)\), \(W_2=\{2,4\}\), \(d^2=0\), nhân tử \(\hat\mu_2,\hat\mu_4\) là',
   r'\(\hat\mu_2=1/3\), \(\hat\mu_4=-2/3\)', [r'\(\hat\mu_2=-1/3\), \(\hat\mu_4=2/3\)', r'\(\hat\mu_2=1\), \(\hat\mu_4=1\)', r'\(\hat\mu_2=0\), \(\hat\mu_4=0\)'],
   r'\(g^2=(-1,-1)\); \((-1,-1)+\hat\mu_2(3,1)+\hat\mu_4(0,-1)=0\Rightarrow\hat\mu_2=1/3\), \(-1+1/3-\hat\mu_4=0\Rightarrow\hat\mu_4=-2/3\).', E)
num('B', r(75), r'Tại \(k=2\), tính \(\hat\mu_2\) (số thập phân 4 chữ số).', 1 / 3,
    r'\(3\hat\mu_2=1\Rightarrow\hat\mu_2=1/3\approx0.3333\).', tol=1e-3, ans_text='0.3333', grp=E)
mc('B', r(75), r'Tại \(k=2\), ràng buộc bị loại là',
   'ràng buộc 4 (nhân tử âm nhất \\(-2/3\\))', ['ràng buộc 2', 'ràng buộc 1', 'không loại ràng buộc nào'],
   r'\(W_3=W_2\setminus\{4\}=\{2\}\), \(x^3=x^2\).', E)
mc('B', r(76), r'Tại \(k=3\), \(W_3=\{2\}\), \(g^3=(-1,-1)\). Bài toán con \(\min d_1^2+d_2^2-d_1-d_2\) s.t. \(3d_1+d_2=0\) cho',
   r'\(d^3=(-0.1,\ 0.3)\)', [r'\(d^3=(0.1,\ -0.3)\)', r'\(d^3=(0.3,\ -0.1)\)', r'\(d^3=(-0.3,\ 0.1)\)'],
   r'\(d_2=-3d_1\): \(10d_1^2+2d_1\) tối thiểu tại \(d_1=-0.1\), \(d_2=0.3\).', E)
num('B', r(76), r'Tại \(k=3\) (\(d^3=(-0.1,0.3)\)), tính \(3d_1+d_2\).', 0, r'\(3(-0.1)+0.3=0\): hướng d nằm trong \(\ker a_2\).', ans_text='0', grp=E)
mc('B', r(77), r'Tại \(k=3\), độ dài bước là',
   r'\(\alpha_3=1\) (không có ràng buộc cản)', [r'\(\alpha_3=0.5\) (cản bởi ràng buộc 1)', r'\(\alpha_3=0\)', r'\(\alpha_3=3.75\)'],
   r'\(\alpha_3=\min\{1,7.5,3.75\}=1\). Do đó \(x^4=(0.5,0)+(-0.1,0.3)=(0.4,0.3)\), \(W_4=W_3=\{2\}\).', E)
mc('B', r(78), r'Tại \(k=4\), \(x^4=(0.4,0.3)\), \(g^4=(-1.2,-0.4)\). Bài toán con cho \(d^4\) là',
   r'\(d^4=0\)', [r'\(d^4=(-0.1,0.3)\)', r'\(d^4=(1,0)\)', r'\(d^4=(0.4,0.3)\)'],
   r'\(d_2=-3d_1\) và mục tiêu \(10d_1^2\) tối thiểu tại \(d_1=0\).', E)
mc('B', r(79), r'Tại \(k=4\), nhân tử \(\hat\mu_2\) và kết luận là',
   r'\(\hat\mu_2=0.4>0\): dừng, \(x^*=(0.4,0.3)\)', [r'\(\hat\mu_2=-0.4<0\): loại ràng buộc 2', r'\(\hat\mu_2=0\): phải đi tiếp', r'\(\hat\mu_2=0.4\): loại ràng buộc 2'],
   r'\((-1.2,-0.4)+\hat\mu_2(3,1)=0\Rightarrow\hat\mu_2=0.4\ge0\) ⇒ dừng. \(f=(0.4-1)^2+(0.3-0.5)^2=0.4\).', E)
num('B', r(79), r'Giá trị tối ưu \((x_1-1)^2+(x_2-0.5)^2\) tại \(x^*=(0.4,0.3)\) là', 0.4, r'\((0.4-1)^2+(0.3-0.5)^2=0.36+0.04=0.4\).', ans_text='0.4', grp=E)
num('B', r(79), r'Tổng số vòng lặp (k = 0, 1, …, dừng) của ví dụ theo mô phỏng là', len(AE['log']),
    r'k=0..4: 5 vòng (2 lần loại ràng buộc 3 và 4, 1 lần di chuyển có cản, 1 lần di chuyển không cản, 1 lần dừng).', ans_text=str(len(AE['log'])), grp=E)
mc('B', r(81), r'Bài tập slide tr.81: \(\min(x_1-4.5)^2+(x_2-3)^2\) với năm ràng buộc, \(x^0=(0,0)\). Đáp số slide là',
   r'\(x^*=(3.25,\ 1.75)^\top\)', [r'\(x^*=(4.5,\ 3)^\top\)', r'\(x^*=(3,\ 2)^\top\)', r'\(x^*=(4.2,\ 0.8)^\top\)'],
   r'Điểm \((4.5,3)\) vi phạm \(x_1+x_2\le5\). Code: ' + str(R['m3_active_bt_num']) + r'. \((4.2,0.8)\) là điểm trung gian ở vòng 4.', E)
num('B', r(81), r'Bài tập tr.81: giá trị \((x_1-4.5)^2+(x_2-3)^2\) tại \(x^*=(3.25,1.75)\) là', 3.125,
    r'\((3.25-4.5)^2+(1.75-3)^2=1.5625+1.5625=3.125\).', ans_text='3.125', grp=E)
mc('B', r(81), r'Trong bài tập tr.81, tại \(x^0=(0,0)\) tập chặt ban đầu là',
   'ràng buộc 4 và 5 (\\(-x_1\\le0\\), \\(-x_2\\le0\\))', ['ràng buộc 1 và 2', 'ràng buộc 3 và 4', 'không có ràng buộc chặt'],
   r'\(a_1^\top0=0<6\), \(a_2^\top0=0<5\), \(a_3^\top0=0<15\): lỏng; \(-0=0\) chặt cho hai ràng buộc cuối. \(W_0=\{4,5\}\).', E)
mc('B', r(81), r'Trong bài tập tr.81 (mô phỏng), vòng 1 di chuyển từ \((0,0)\) tới',
   r'\((3,0)\), cản bởi ràng buộc 1 (\(2x_1-3x_2\le6\))', [r'\((4.5,0)\), cản bởi ràng buộc 2', r'\((0,3)\), cản bởi ràng buộc 3', r'\((4.5,3)\), không cản'],
   r'\(d^1=(4.5,0)\), \(\alpha_1=6/(2\cdot4.5)=2/3\Rightarrow x^2=(3,0)\). Tỉ số ràng buộc 2: \(5/4.5>2/3\).', E)
tf('B', r(81), r'Trong bài tập tr.81, nghiệm tối ưu chỉ có ràng buộc \(x_1+x_2\le5\) chặt.', True, r'Tại \((3.25,1.75)\): \(x_1+x_2=5\) chặt; các ràng buộc khác lỏng (\(2x_1-3x_2=1.25<6\), …). \(\hat\mu=2.5>0\).', E)
tf('S', r(66), r'Trong active set, ràng buộc trong \(W_k\) không bao giờ vi phạm vì bước d thỏa \(a_i^\top d=0\).', True, r'\(a_i^\top(x+\alpha d)=a_i^\top x=b_i\ \forall i\in W_k\): các ràng buộc trong W được giữ chặt.', E)
tf('S', r(66), r'Trong công thức \(\alpha_k\), cần xét cả các ràng buộc \(i\in W_k\).', False, r'Chỉ xét \(i\notin W_k\), \(a_i^\top d^k>0\). Các ràng buộc trong W luôn thỏa chặt.', E)
tf('S', r(67), r'Nếu \(d^k=0\) và \(W_k=\emptyset\) thì \(x^k\) là nghiệm không ràng buộc và thuật toán dừng.', True, r'Không có ràng buộc nào trong W nên không có nhân tử; điều kiện dừng \(Qx^k+c=0\) đã thỏa. (Dừng vì “mọi \(\hat\mu\ge0\)” đúng rỗng.)', E)
tf('S', r(67), r'Khi loại ràng buộc j khỏi \(W_k\), điểm x thay đổi ngay trong cùng vòng.', False, r'\(x^{k+1}=x^k\); chỉ tập W đổi, vòng sau mới di chuyển.', E)
tf('S', r(68), r'Thuật toán active set luôn giữ các điểm \(x^k\) khả thi.', True, r'\(\alpha_k\) được chọn để \(x^k+\alpha_kd^k\) khả thi; \(x^0\) khả thi.', E)
tf('S', r(68), r'Ở mỗi vòng active set, giá trị hàm mục tiêu không tăng.', True, r'Khi đi theo d là hướng giảm; khi loại ràng buộc thì x giữ nguyên.', E)
tf('S', r(63), r'Nếu Q chỉ nửa xác định dương, ta vẫn kết luận nghiệm toàn cục khi (4.9) thỏa (Mệnh đề slide tr.63).', True, r'Mệnh đề slide tr.63: “Q là ma trận nửa xác định dương”. (Bài toán con có thể cần \(Z^\top QZ\succ0\) để giải được.)', E)
mc('S', r(67), r'Nhân tử \(\hat\mu_i<0\) tại một ràng buộc trong \(W_k\) cho biết',
   'buông ràng buộc đó ra thì f có thể giảm tiếp', ['ràng buộc đó bị vi phạm', 'bài toán vô nghiệm', 'x^k đã là nghiệm'],
   r'Nhân tử là “giá” của ràng buộc; âm nghĩa là ràng buộc đang bị dùng ngược chiều (kéo vào trong), nên loại nó đi.', E)
mc('S', r(66), r'Khi \(\alpha_k<1\), điều đó có nghĩa là',
   'bước Newton đầy đủ sẽ vi phạm một ràng buộc ngoài W, nên dừng ở biên', ['bài toán con vô nghiệm', 'nhân tử âm', 'Q không xác định dương'],
   r'\(\alpha_k<1\) chỉ xảy ra khi có ràng buộc cản; ràng buộc đó được thêm vào W.', E)
mc('S', r(60), r'Ưu điểm của active set so với đơn hình trong QP là',
   'nghiệm có thể nằm trong miền (không chỉ ở đỉnh), nên cần giải bài toán con toàn phương', ['luôn nhanh hơn điểm trong', 'không cần Q đối xứng', 'không cần điểm xuất phát khả thi'],
   r'LP có nghiệm ở đỉnh nên đơn hình chỉ đi giữa các đỉnh; QP lồi có thể có nghiệm ở điểm trong hoặc trên mặt, nên active set giải bài toán con đẳng thức.', E)
essay('B', r(69), r'Giải bằng thuật toán tập hoạt động: \(\min(x_1-1)^2+(x_2-0.5)^2\) s.t. \(x_1+x_2\le1,\ 3x_1+x_2\le1.5,\ x_1\ge0,\ x_2\ge0\) từ \(x^0=(0,0)\). Trình bày từng vòng (\(W_k\), \(d^k\), \(\alpha_k\), nhân tử).',
      r'<p>\(Q=2I\), \(c=(-2,-1)\), \(a_1=(1,1),a_2=(3,1),a_3=(-1,0),a_4=(0,-1)\), \(b=(1,1.5,0,0)\).</p><ol><li>k=0: \(x=(0,0)\), \(W=\{3,4\}\), \(g=(-2,-1)\), \(d=0\). Nhân tử \(\hat\mu_3=-2\) (âm) ⇒ loại 3, \(W=\{4\}\).</li><li>k=1: \(d=(1,0)\); \(\alpha=\min\{1,1,0.5\}=0.5\) (cản bởi 2) ⇒ \(x=(0.5,0)\), \(W=\{2,4\}\).</li><li>k=2: \(g=(-1,-1)\), \(d=0\); \(\hat\mu_2=1/3\), \(\hat\mu_4=-2/3\) ⇒ loại 4, \(W=\{2\}\).</li><li>k=3: \(d=(-0.1,0.3)\), \(\alpha=1\) ⇒ \(x=(0.4,0.3)\).</li><li>k=4: \(g=(-1.2,-0.4)\), \(d=0\), \(\hat\mu_2=0.4>0\) ⇒ dừng.</li></ol><p>Nghiệm \((0.4,0.3)\), \(f=0.4\).</p>',
      ['Đủ các vòng, ghi \\(W_k\\)', 'Tính đúng \\(\\alpha_k\\) và ràng buộc cản', 'Kết luận bằng nhân tử không âm'], E)
essay('B', r(81), r'Bài tập slide tr.81: giải \(\min(x_1-4.5)^2+(x_2-3)^2\) với năm ràng buộc bằng active set từ \((0,0)\); tổng hợp bảng \(x^k,W_k,d^k,\alpha_k,\hat\mu\).',
      r'<p>Ràng buộc: \(a_1=(2,-3),b_1=6\); \(a_2=(1,1),b_2=5\); \(a_3=(-3,5),b_3=15\); \(a_4=(-1,0),b_4=0\); \(a_5=(0,-1),b_5=0\). \(Q=2I\), \(c=(-9,-6)\).</p><p>Kết quả mô phỏng (đã kiểm): (0,0) W={4,5} d=0, μ̂=(−9,−6): loại 4 → (0,0) W={5} d=(4.5,0), α=2/3, cản bởi 1 → (3,0) W={5,1} d=0, μ̂₅=−10.5, μ̂₁=1.5: loại 5 → W={1} d=(2.4231,1.6154), α≈0.4952, cản bởi 2 → (4.2,0.8) W={1,2} d=0, μ̂₁=−0.76, μ̂₂=2.12: loại 1 → W={2}, d=(−0.95,0.95), α=1 → (3.25,1.75) W={2}, d=0, μ̂₂=2.5>0: dừng. \(x^*=(3.25,1.75)\), \(f=3.125\).</p>',
      ['Bảng đầy đủ', 'Kết luận \\((3.25,1.75)\\)'], E)
essay('S', r(60), r'So sánh phương pháp null space và phương pháp tập hoạt động: dùng cho bài toán nào, mối liên hệ giữa hai phương pháp.',
      r'<p>Null space giải QP <i>đẳng thức</i> \(\min\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax=b\) bằng cách khử ràng buộc qua \(\ker A\) và giải hệ KKT tuyến tính. Active set giải QP <i>bất đẳng thức</i> bằng cách đoán tập ràng buộc chặt \(W_k\): mỗi vòng biến các ràng buộc trong \(W_k\) thành đẳng thức (bài toán con giải bằng null space), rồi thêm ràng buộc cản hoặc loại ràng buộc có nhân tử âm. Như vậy null space là “động cơ” của mỗi vòng active set.</p>',
      ['Phân biệt đẳng thức/bất đẳng thức', 'Nêu null space là bài toán con của active set'], E)

# =====================================================================  F. MỆNH ĐỀ SAI THƯỜNG GẶP (đối trọng)
G = 'F. Mệnh đề dễ nhầm'
tf('G', r(40), r'Nếu Q xác định âm thì nghiệm QP luôn nằm ở điểm trong của Δ.', False, r'Ngược lại: nằm ở điểm cực biên (Định lý 3.3b).', G)
tf('G', r(43), r'Nghiệm của bài toán QP không bao giờ là điểm trong của miền chấp nhận được.', False, r'Slide tr.43–45: có thể là điểm trong (ví dụ \(\min x^2\) trên \([-1,1]\)).', G)
tf('G', r(38), r'Tập cực tiểu địa phương \(\mathrm{loc}(P)\) của QP luôn đóng.', False, r'Slide tr.39: có thể không đóng (ví dụ (P1)).', G)
tf('G', r(24), r'Định lý Frank–Wolfe cần miền Δ bị chặn.', False, r'Không cần: chỉ cần \(\bar\theta\) hữu hạn và Δ polyhedron.', G)
tf('G', r(29), r'Nếu Q ≻ 0 thì bài toán (2) có thể vô nghiệm dù \(\Delta\ne\emptyset\).', False, r'Hệ quả 3: \(Q\succ0\) và \(\Delta\ne\emptyset\) ⇒ có nghiệm.', G)
tf('G', r(48), r'KKT của QP đẳng thức chỉ là điều kiện cần, không đủ để kết luận nghiệm.', False, r'QP lồi + ràng buộc affine: KKT cần và đủ (slide tr.48).', G)
tf('G', r(51), r'Ma trận Z trong null space thỏa \(Z^\top A=0\).', False, r'Z thỏa \(AZ=0\) (các cột của Z nằm trong \(\ker A\)).', G)
tf('G', r(52), r'\(d_Y\) và \(d_Z\) đều là vectơ thuộc \(\mathbb R^{n-m}\).', False, r'\(d_Y\in\mathbb R^m\), \(d_Z\in\mathbb R^{n-m}\).', G)
tf('G', r(62), r'Trong active set, nhân tử \(\hat\mu_i\) của ràng buộc bất đẳng thức trong \(W_k\) có thể âm tại nghiệm tối ưu của (P).', False, r'Tại nghiệm tối ưu mọi \(\hat\mu_i\ge0\) (KKT); nhân tử âm ở vòng giữa chỉ đường loại ràng buộc.', G)
tf('G', r(67), r'Nếu \(d^k\ne0\) thì ta tính nhân tử \(\hat\mu\) ngay.', False, r'Chỉ khi \(d^k=0\) mới tính nhân tử (Bước 3); nếu \(d^k\ne0\) thì di chuyển (Bước 2).', G)
tf('G', r(66), r'\(\alpha_k\) có thể lớn hơn 1 trong thuật toán active set của slide.', False, r'\(\alpha_k=\min\{1,\dots\}\le1\): bước tối đa là bước Newton đầy đủ.', G)
tf('G', r(60), r'Active set yêu cầu điểm xuất phát \(x^0\) khả thi.', True, r'Slide tr.68: “Chọn \(x^0\) là điểm chấp nhận được”.', G)
tf('G', r(12), r'Nếu \(Q\prec0\) thì QP là bài toán lồi.', False, r'Lồi khi \(Q\succeq0\). \(Q\prec0\) ⇒ f lõm chặt: không lồi.', G)
tf('G', r(58), r'Trong ví dụ null space của slide, giá trị 212.7059 chính là giá trị tối ưu của \(\tfrac12x^\top Qx+c^\top x\) với Q, c như slide.', False, r'Giá trị của dạng đó là ' + str(NE['f']) + r'. 212.7059 là giá trị của đa thức ghi trên slide (Hessian \(2Q\)) tại \(x^*\).', G)
tf('G', r(59), r'Đáp số \((2,-1,1)\) của Bài tập 1 thỏa cả hai ràng buộc ghi trên slide (\(x_1+x_3=0\), \(x_2+x_3=0\)).', False, r'\(x_1+x_3=3\ne0\): không thỏa. Đáp số khớp khi \(x_1+x_3=3\).', G)

# ---- cân bằng độ dài đáp án (mỗi đáp án nhiễu là một hiểu sai có thật) ----
F_ = bank.fix
F_(r'Vì sao có thể giả sử ma trận Q đối xứng?', None, ['vì mọi ma trận vuông thực đều tự đối xứng', 'vì Q luôn xác định dương nên đối xứng', r'vì \(x^\top Qx=x^\top Q^\top Qx\) nên chỉ cần Q đối xứng'])
F_(r'Bài toán (P) \(\min f(x)\) s.t. \(x\in\Delta\) là', None, ['f toàn phương và Δ là một hình cầu đóng', 'f tuyến tính và Δ là một tập lồi bất kỳ', 'f là đa thức bậc ba và Δ là polyhedron'])
F_(r'Thay \(Q\) bởi \(\tfrac12Q\) trong', None, [r'\(\min\tfrac12x^\top Qx+2c^\top x\) (nhân đôi phần tuyến tính)', r'\(\min x^\top Qx+\tfrac12c^\top x\) (chỉ giảm phần tuyến tính)', r'\(\min x^\top Q^{-1}x+c^\top x\) (đảo ma trận Q)'])
F_(r'Ký hiệu \(\Delta(A,b)\) và \(\bar\theta\) trong slide tr.23', r'\(\{x:Ax\ge b\}\) và \(\bar\theta=\inf\{f(x)\}\) trên đó', [r'\(\{x:Ax=b\}\) và \(\bar\theta=\sup f\) trên đó', r'\(\{x:f(x)\le b\}\) và \(\bar\theta=\min f\) trên đó', r'\(\{Ax\}\) (ảnh của A) và \(\bar\theta=\|c\|\)'])
F_(r'Khi \(\Delta(A,b)\ne\emptyset\), trường hợp', 'f giảm vô hạn trên miền nên không có nghiệm', ['bài toán có nghiệm duy nhất trên miền', 'bài toán có vô số nghiệm trên miền', 'miền chấp nhận được là tập rỗng'])
F_(r'Định lý Frank–Wolfe (slide tr.24) nói', r'\(\bar\theta\) hữu hạn thì bài toán (2) có nghiệm', [r'nếu Δ bị chặn thì nghiệm luôn duy nhất', r'nếu \(Q\succ0\) thì luôn có \(\bar\theta=-\infty\)', r'nếu \(\bar\theta=-\infty\) thì có nghiệm ở vô cực'])
F_(r'Ví dụ slide tr.25: \(\min x_1\)', r'\(\bar\theta=0\) nhưng không đạt được', [r'\(\bar\theta=1\) và nghiệm là \((1,1)\)', r'\(\bar\theta=-\infty\), bài toán vô nghiệm', r'\(\bar\theta=0\) và nghiệm là \((0,0)\)'])
F_(r'Định lý Eaves cho biết bài toán (2) có nghiệm', r'Δ khác rỗng và hai điều kiện về hướng \(v\) thỏa', ['Q xác định dương trên toàn không gian', 'Δ là tập bị chặn và đóng', 'c = 0 và b = 0 đồng thời'])
F_(r'Điều kiện (2) của Eaves:', 'bậc hai không âm theo mọi hướng lùi của miền', ['Q xác định dương trên toàn không gian', 'miền Δ bị chặn theo mọi hướng', 'nghiệm phải là điểm cực biên của Δ'])
F_(r'Điều kiện (3) của Eaves quan tâm trường hợp', r'\(v^\top Qv=0\) và đòi \((Qx+c)^\top v\ge0\)', [r'\(v^\top Qv>0\) và đòi \(c=0\) tuyệt đối', r'\(Av<0\) và đòi \(x=0\) tại mọi điểm', r'\(v=0\) và đòi \(Ax=b\) với mọi x'])
F_(r'Hệ quả 1 (slide tr.27)', r'\(\Delta\ne\emptyset\) và điều kiện (3) của Eaves thỏa', [r'\(\Delta\) khác rỗng và compact', r'\(c=0\) và \(\Delta\ne\emptyset\)', r'\(\Delta=\emptyset\) hoặc \(Q=0\)'])
F_(r'Ký hiệu \(\mathrm{Sol}(P)\) trong phần 3', 'tập các nghiệm tối ưu toàn cục của (P)', ['tập các ràng buộc chặt tại nghiệm', 'tập các nhân tử Lagrange của bài toán', 'tập các điểm cực biên của miền Δ'])
F_(r'Nghiệm tia của bài toán (P) là', r'nửa đường thẳng \(\bar x+t\bar v\ (t\ge0)\) nằm trong Sol(P)', ['một điểm cực biên của miền Δ', 'một đoạn thẳng bị chặn nằm trong Δ', 'một đường thẳng vuông góc với Δ'])
F_(r'Định lý 3.2 nói', r'\(\mathrm{Sol}(P)\) là tập đóng', [r'\(\mathrm{Sol}(P)\) luôn là tập bị chặn', r'\(\mathrm{Sol}(P)\) luôn là tập lồi', r'\(\mathrm{Sol}(P)\) luôn là tập hữu hạn'])
F_(r'Ví dụ (P1) slide tr.38', r'\(\mathrm{Sol}=\emptyset\), \(\mathrm{loc}=\{x_1>0,x_2=0\}\) không đóng', [r'\(\mathrm{Sol}(P_1)=\{(0,0)\}\), một nghiệm duy nhất', r'\(\mathrm{Sol}(P_1)=\mathrm{loc}(P_1)=\{x_2=0\}\), đóng', r'\(\mathrm{Sol}(P_1)\) là tập lồi bị chặn khác rỗng'])
F_(r'Định lý 3.3 (a): nếu Q xác định dương', 'nghiệm duy nhất, Sol(P) = loc(P)', ['có vô số nghiệm nằm trên một cạnh', 'nghiệm là điểm cực biên của Δ', 'bài toán không có nghiệm nào'])
F_(r'Ví dụ 1 slide tr.44', r'\(x=0\), nằm trong \((-1,1)\)', [r'\(x=1\), ở biên phải của miền', r'\(x=-1\), ở biên trái của miền', 'bài toán không có nghiệm nào'])
F_(r'Trong QP với \(Q\prec0\) và Δ là polytope', 'các đỉnh của Δ', ['các điểm nằm trong Δ', r'các điểm có mọi nhân tử \(\lambda=0\)', 'các điểm mà f bằng 0'])
F_(r'Bài toán QP đẳng thức của slide tr.47 giả thiết', r'Q đối xứng, \(Q\succeq0\), \(\mathrm{rank}A=m\)', ['Q khả nghịch bất kỳ và A là ma trận vuông', r'Q xác định âm và \(\mathrm{rank}A<m\)', 'Q = 0 và A không có hàng nào'])
F_(r'Vì sao slide đổi biến \(d=x-\bar x\)?', 'để được hệ KKT có ma trận đối xứng', ['để biến bài toán thành không lồi', 'để loại bỏ hoàn toàn ràng buộc đẳng thức', 'để tránh phải dùng nhân tử Lagrange'])
F_(r'Ma trận Z trong phương pháp null space là', r'ma trận \(n\times(n-m)\) có \(AZ=0\)', [r'ma trận \(m\times m\) là nghịch đảo của A', r'ma trận \(n\times m\) thỏa \(AZ=I\)', 'ma trận đường chéo của các nhân tử'])
F_(r'Mệnh đề slide tr.51', r'hệ (4.2) không suy biến và (P) có nghiệm duy nhất', ['bài toán không có nghiệm hữu hạn nào', r'Q bắt buộc phải xác định dương trên \(\mathbb R^n\)', 'nghiệm tồn tại nhưng nhân tử không tồn tại'])
F_(r'Ma trận Y trong phương pháp null space thỏa', r'\([Y\ Z]\) khả nghịch (chọn được \(AY=I\))', [r'\(YZ=0\) và \(Y^\top Y=I\) đồng thời', r'\(Y=Z^\top\) (chuyển vị của Z)', r'\(Y=A^{-1}\) (A khả nghịch)'])
F_(r'Ví dụ slide tr.58 cho \(d_Y=(4,10)^\top\)', r'\(AY=I\) và \(\bar b=b=(4,10)^\top\)', [r'\(AZ=I\) và \(\bar g=c\) đồng thời', r'\(Y=A^\top\) và \(\bar g=(4,10)\)', r'\(Z^\top QZ=(4,10)^\top\) trực tiếp'])
F_(r'Bài tập 1 slide tr.59 ghi ĐS', r'không thỏa ràng buộc \(x_1+x_3=0\) (vì bằng 3)', ['thỏa cả hai ràng buộc ghi trên slide', r'là nghiệm với nhân tử \(\mu=(0,0)\)', r'thỏa vì \(x_2+x_3=0\) đã là đủ'])
F_(r'Khi QP đẳng thức có nghiệm duy nhất', r'không: \(x^*=\bar x+d^*\) không đổi', [r'có: mỗi \(\bar x\) cho một nghiệm khác nhau', r'chỉ phụ thuộc \(\bar x\) khi Q đối xứng', r'chỉ phụ thuộc \(\bar x\) khi \(\mathrm{rank}A<m\)'])
F_(r'Trong bài toán của slide tr.60, \(I(x^*)\) là', r'tập chỉ số ràng buộc hoạt động (chặt)', [r'\(\{i\mid a_i^\top x^*<b_i\}\): các ràng buộc lỏng', 'tập các nhân tử Lagrange dương', 'tập các điểm khả thi của bài toán'])
F_(r'Vì \(I(x^*)\) chưa biết trước', r'cập nhật dần tập làm việc \(W_k\)', ['giải mọi tổ hợp ràng buộc cùng một lúc', 'bỏ qua hoàn toàn các bất đẳng thức', 'đổi bài toán thành quy hoạch tuyến tính'])
F_(r'Điều kiện KKT (4.9) của bài toán active set', r'\(Qx^*+c+\sum_{I(x^*)}\mu_i^*a_i=0\), \(a_i^\top x^*=b_i\), \(\mu_i^*\ge0\)', [r'\(Qx^*+c=0\), \(a_i^\top x^*<b_i\), \(\mu_i^*\le0\) với mọi i', r'\(Qx^*+c-\sum\mu_i^*a_i=0\) và \(\mu_i^*\le0\) với mọi i', r'\(x^*=0\) và \(\mu^*=0\) với mọi bài toán'])
F_(r'Bước 1 của active set kiểm tra', r'\(\min\tfrac12d^\top Qd+g^\top d\) s.t. \(a_i^\top d=0\ (i\in W_k)\)', [r'\(\min\tfrac12d^\top Qd\) s.t. \(Ad=b\) với mọi ràng buộc', r'\(\min g^\top d\) s.t. \(a_i^\top d\le0\ (i\in W_k)\)', r'\(\max\tfrac12d^\top Qd+g^\top d\) s.t. \(d=0\) và \(x\ge0\)'])
F_(r'Bước 2: độ dài bước', r'\(\alpha_k=\min\{1,\min_{i\notin W_k,a_i^\top d^k>0}\frac{b_i-a_i^\top x^k}{a_i^\top d^k}\}\)', [r'\(\alpha_k=\max\{1,\max_i(b_i-a_i^\top x^k)\}\) lấy trên mọi i', r'\(\alpha_k=\min_{i\in W_k}(b_i-a_i^\top x^k)\) lấy trên tập W', r'\(\alpha_k=\|d^k\|^{-1}\) (nghịch đảo độ dài hướng)'])
F_(r'“Ràng buộc cản” (blocking constraint) là', r'ràng buộc cho \(\alpha_k\) nhỏ nhất (chạm biên)', ['ràng buộc có nhân tử Lagrange âm nhất', 'ràng buộc mà mọi điểm khả thi đều thỏa', 'ràng buộc đẳng thức duy nhất của bài toán'])
F_(r'Sau Bước 2, nếu có ràng buộc cản thì', r'thêm chỉ số cản vào \(W_k\), quay lại Bước 1', ['xóa toàn bộ ràng buộc khỏi tập \\(W_k\\)', 'dừng thuật toán và báo vô nghiệm', 'đổi hàm mục tiêu sang hàm tuyến tính'])
F_(r'Nếu \(d^k=0\) và có \(\hat\mu_j<0\) thì', r'loại chỉ số j (\(\hat\mu_j\) âm nhất): \(W_{k+1}=W_k\setminus\{j\}\)', [r'thêm chỉ số j vào \(W_k\) và giữ nguyên các chỉ số khác', 'dừng thuật toán và báo bài toán vô nghiệm', r'đổi dấu \(\hat\mu_j\) rồi tiếp tục với cùng \(W_k\)'])
F_(r'Tại \(k=2\), ràng buộc bị loại là', r'ràng buộc 4 (\(\hat\mu_4=-2/3\))', ['ràng buộc 2, vì nhân tử \\(\\hat\\mu_2\\) dương', 'ràng buộc 1, vì nó là ràng buộc đầu tiên', 'không loại ràng buộc nào ở vòng này'])
F_(r'Trong bài tập tr.81 (mô phỏng), vòng 1', r'\((3,0)\), cản bởi ràng buộc 1', [r'\((4.5,0)\), cản bởi ràng buộc 2 (\(x_1+x_2\le5\))', r'\((0,3)\), cản bởi ràng buộc 3 (\(-3x_1+5x_2\le15\))', r'\((4.5,3)\), đi trọn bước không bị cản'])
F_(r'Nhân tử \(\hat\mu_i<0\) tại một ràng buộc', 'buông ràng buộc đó thì f giảm tiếp', ['ràng buộc đó đã bị vi phạm', 'bài toán không có nghiệm hữu hạn', r'\(x^k\) đã là nghiệm tối ưu của (P)'])
F_(r'Khi \(\alpha_k<1\), điều đó có nghĩa là', 'bước đầy đủ sẽ vi phạm một ràng buộc ngoài W', ['bài toán con không có nghiệm', 'một nhân tử Lagrange đang âm', r'ma trận Q không xác định dương'])
F_(r'Ưu điểm của active set so với đơn hình', 'xử lý được nghiệm nằm trong miền, không chỉ ở đỉnh', ['luôn nhanh hơn phương pháp điểm trong', 'không cần Q đối xứng để chạy được', 'không cần điểm xuất phát khả thi'])
