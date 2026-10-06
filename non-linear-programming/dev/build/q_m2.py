"""Ngân hàng câu hỏi Module 2 — Tối ưu có ràng buộc & KKT. Nguồn chính: Slides/2_NonlinearProgram_KKT_250418.pdf
Nhãn: G = từ nội dung slide; B = bài tập/ví dụ của slide; T = tham khảo (Studocu); S = biên soạn thêm."""
import numpy as np
from qlib import Bank
from helpers import R
import c_m2

bank = Bank('m2')
mc, tf, num, essay = bank.mc, bank.tf, bank.num, bank.essay
def r(p): return f'slide 2 · tr.{p}'

# =====================================================================  A. BÀI TOÁN TỔNG QUÁT VÀ BÀI TOÁN LỒI
A = 'A. Bài toán tổng quát và bài toán lồi'
mc('G', r(8), r'Bài toán tối ưu phi tuyến dạng tổng quát trong slide có dạng',
   r'\(\min f(x)\) s.t. \(g_i(x)\le0,\ h_j(x)=0,\ x\in\mathbb R^n\)', [r'\(\max f(x)\) s.t. \(g_i(x)\ge0,\ h_j(x)\le0\)', r'\(\min f(x)\) s.t. \(g_i(x)=0,\ h_j(x)\le0\)', r'\(\min f(x)\) s.t. \(g_i(x)<0\) và \(h_j(x)\ne0\)'],
   r'Slide tr.8: \(g_i\) là ràng buộc bất đẳng thức dạng “≤ 0”, \(h_j\) là ràng buộc đẳng thức “= 0”. Đây là dạng chuẩn để áp dụng KKT.', A)
mc('G', r(8), r'Trong bài toán \(\min f(x)\) s.t. \(g_i(x)\le0,\ h_j(x)=0\), hàm \(g_i\) được gọi là',
   'hàm ràng buộc bất đẳng thức', ['hàm ràng buộc đẳng thức', 'hàm mục tiêu của bài toán phụ', 'hàm nhân tử Lagrange của bài toán'],
   r'Slide tr.8: “\(g_i:\mathbb R^n\to\mathbb R\) là các ràng buộc bất đẳng thức; \(h_j\) là các ràng buộc đẳng thức”.', A)
mc('G', r(8), r'Trong bài toán tổng quát của slide, biến \(x\) và hàm \(f\) lần lượt là',
   r'biến số \(x\in\mathbb R^n\) và hàm mục tiêu \(f:\mathbb R^n\to\mathbb R\)', [r'hằng số cần tìm và ràng buộc bất đẳng thức', r'nhân tử Lagrange và hàm Lagrange', r'tập chấp nhận và điểm cực tiểu'],
   r'Slide tr.8: “x: biến số; \(f:\mathbb R^n\to\mathbb R\) là hàm mục tiêu”.', A)
mc('G', r(37), r'Tập chấp nhận được (feasible set) của bài toán (P) được ký hiệu và định nghĩa là',
   r'\(C=\{x\in\mathbb R^n:\ g_i(x)\le0\ \forall i\in I,\ h_j(x)=0\ \forall j\in J\}\)', [r'\(C=\{x:\ f(x)\le0\}\)', r'\(C=\{x:\ \nabla f(x)=0\}\)', r'\(C=\{x:\ g_i(x)=0\ \forall i,\ h_j(x)\le0\ \forall j\}\)'],
   r'Slide tr.37: I, J là các tập chỉ số, và C là tập các điểm thỏa cả hai loại ràng buộc.', A)
mc('G', r(37), r'Trong slide, các tập \(I\) và \(J\) là',
   'các tập chỉ số của ràng buộc bất đẳng thức và đẳng thức', ['các tập nghiệm của hai bài toán đối ngẫu', 'hai tập lồi chứa điểm cực tiểu', 'các tập điểm KKT và tập điểm dừng'],
   r'\(I=\{1,\dots,n\}\), \(J=\{1,\dots,p\}\) (slide tr.37): chỉ số của các \(g_i\) và \(h_j\).', A)
mc('G', r(11), r'Bài toán tối ưu lồi \(\min_{x\in C}f(x)\) yêu cầu',
   'f lồi và tập chấp nhận được C lồi', ['f lõm và tập C lồi', 'f lồi và tập C chỉ cần đóng', 'f khả vi và C bị chặn'],
   r'Slide tr.11: “Hàm mục tiêu f: lồi; Tập chấp nhận được C: lồi”.', A)
tf('G', r(11), r'Trong bài toán tối ưu lồi, mọi cực tiểu địa phương đều là cực tiểu toàn cục.', True,
   r'Slide tr.11. Chứng minh: nếu có \(y\in C\) tốt hơn thì các điểm \((1-t)x+ty\) với t nhỏ vẫn khả thi và có f nhỏ hơn \(f(x)\), mâu thuẫn tính địa phương.', A)
tf('G', r(11), r'Bài toán tối ưu lồi luôn có ít nhất một nghiệm.', False,
   r'Lồi không bảo đảm tồn tại nghiệm: \(\min e^x\) trên \(\mathbb R\) có giá trị infimum 0 nhưng không đạt.', A)
mc('G', r(11), r'Điểm mạnh nhất của bài toán tối ưu lồi so với phi tuyến tổng quát là',
   'cực tiểu địa phương cũng là cực tiểu toàn cục', ['luôn có nghiệm duy nhất', 'luôn giải được bằng công thức đóng', 'hàm mục tiêu luôn tuyến tính'],
   r'Đó là tính chất nêu trong slide tr.11. Nghiệm không nhất thiết duy nhất (LP có thể có cả cạnh nghiệm) và không phải lúc nào cũng có công thức đóng.', A)
mc('G', r(16), r'Trong bài toán lồi dạng (P) ở slide tr.16, các hàm \(g_i\) và \(h_j\) phải là',
   r'\(g_i\) lồi và \(h_j\) affine', [r'\(g_i\) affine và \(h_j\) lồi', r'cả hai đều lồi', r'cả hai đều lõm'],
   r'Slide tr.16: “\(g_i\) là các hàm lồi; \(h_j\) là các hàm affine (Giải thích!!)”.', A)
mc('G', r(16), r'Vì sao ràng buộc đẳng thức \(h_j(x)=0\) của bài toán lồi phải dùng hàm affine?',
   r'vì \(h=0\Leftrightarrow h\le0\) và \(-h\le0\), cần cả \(h\) và \(-h\) lồi', [r'vì hàm affine có đạo hàm liên tục', r'vì hàm affine luôn có nghiệm của \(h=0\)', r'vì mọi hàm lồi đều có tập nghiệm \(h=0\) rỗng'],
   r'\(\{h=0\}=\{h\le0\}\cap\{-h\le0\}\). Để giao lồi ta cần cả hai hàm \(h\) và \(-h\) lồi, tức h vừa lồi vừa lõm, mà đó chính là hàm affine.', A)
tf('S', r(16), r'Tập nghiệm của phương trình \(x_1^2+x_2^2=1\) (đường tròn) là một tập lồi.', False,
   r'Đường tròn không lồi: trung điểm của hai điểm đối xứng là gốc tọa độ, không nằm trên đường tròn. Vì vậy ràng buộc đẳng thức phi tuyến làm bài toán mất tính lồi.', A)
tf('S', r(16), r'Ràng buộc \(2x_1+3x_2=5\) (đẳng thức affine) không làm mất tính lồi của miền chấp nhận được.', True,
   r'Tập nghiệm là một siêu phẳng (đường thẳng), lồi; giao với các tập lồi khác vẫn lồi.', A)
tf('G', r(16), r'Bài toán \(\min f\) s.t. \(g_i\le0,\ h_j=0\) với f, \(g_i\) lồi và \(h_j\) phi tuyến bất kỳ vẫn là bài toán lồi.', False,
   r'\(h_j\) phải affine. Ví dụ \(h=x^2+y^2-1\) tạo ra đường tròn (không lồi).', A)
mc('S', r(16), r'Ràng buộc nào sau đây có thể xuất hiện trong bài toán tối ưu LỒI dạng chuẩn?',
   r'\(x_1^2+x_2^2-4\le0\)', [r'\(x_1^2+x_2^2-4\ge0\)', r'\(x_1^2+x_2^2-4=0\)', r'\(1-x_1^2\le0\)'],
   r'Dạng chuẩn cần \(g_i\le0\) với \(g_i\) lồi: \(x_1^2+x_2^2-4\) lồi nên OK. \(\ge0\) đổi thành \(4-\|x\|^2\le0\) với \(g\) lõm (không lồi); \(=0\) không affine; \(1-x_1^2\) lõm.', A)
mc('S', r(8), r'Bài toán \(\max f(x)\) s.t. \(g(x)\ge0\) được đưa về dạng chuẩn (min, \(\le0\)) bằng cách',
   r'đổi thành \(\min(-f)\) s.t. \(-g\le0\)', [r'đổi thành \(\min f\) s.t. \(g\le0\)', r'đổi thành \(\min(-f)\) s.t. \(g\le0\)', r'đổi thành \(\min f\) s.t. \(-g\ge0\)'],
   r'Đổi max thành min bằng \(-f\) và đổi \(g\ge0\) thành \(-g\le0\). Cần làm cả hai việc.', A)
num('S', r(8), r'Bài toán \(\min f\) có 3 ràng buộc bất đẳng thức \(g_1,g_2,g_3\) và 2 đẳng thức \(h_1,h_2\). Có bao nhiêu nhân tử Lagrange (\(\lambda_i\) và \(\mu_j\)) trong hàm Lagrange?', 5,
    r'Mỗi ràng buộc có đúng một nhân tử: \(3+2=5\).', ans_text='5', grp=A)
num('S', r(37), r'Với \(m=3\) ràng buộc bất đẳng thức, tối đa bao nhiêu tập ràng buộc chặt (trường hợp) cần xét khi dùng điều kiện bù để chia trường hợp?', 8,
    r'Mỗi ràng buộc chặt hoặc lỏng: \(2^3=8\) trường hợp.', ans_text='8', grp=A)
essay('B', r(16), r'“Giải thích!!” (slide tr.16): vì sao trong bài toán tối ưu lồi các ràng buộc đẳng thức \(h_j(x)=0\) phải là hàm affine?',
      r'<p>\(\{h=0\}=\{h\le0\}\cap\{-h\le0\}\). Tập mức dưới \(\{h\le0\}\) lồi nếu h lồi; \(\{-h\le0\}\) lồi nếu \(-h\) lồi (tức h lõm). Để đảm bảo cả hai lồi với mọi trường hợp ta cần h vừa lồi vừa lõm, mà hàm khả vi hai lần vừa lồi vừa lõm có Hessian \(\succeq0\) và \(\preceq0\), tức \(\nabla^2h=0\): h là hàm affine \(h(x)=a^\top x+b\). Ví dụ đường tròn \(x^2+y^2=1\) không lồi.</p>',
      ['Viết \(h=0\) thành hai bất đẳng thức', 'Nêu điều kiện lồi cho từng tập', 'Kết luận affine bằng Hessian bằng 0 hoặc ví dụ đường tròn'], A)
essay('S', r(11), r'Chứng minh: trong bài toán tối ưu lồi, mọi cực tiểu địa phương là cực tiểu toàn cục.',
      r'<p>Giả sử \(x\) là cực tiểu địa phương: tồn tại \(\varepsilon>0\) sao cho \(f(x)\le f(z)\) với mọi \(z\in C\), \(\|z-x\|<\varepsilon\). Giả sử tồn tại \(y\in C\) với \(f(y)<f(x)\). Với \(t\in(0,1)\) đủ nhỏ, \(z_t=(1-t)x+ty\in C\) (C lồi) và \(\|z_t-x\|=t\|y-x\|<\varepsilon\). Vì f lồi: \(f(z_t)\le(1-t)f(x)+tf(y)<f(x)\), mâu thuẫn. Vậy \(f(x)\le f(y)\ \forall y\in C\).</p>',
      ['Giả sử phản chứng có điểm tốt hơn', 'Dùng tính lồi của C để giữ khả thi', 'Dùng Jensen để chứng tỏ f giảm'], A)

# =====================================================================  B. HỌ BÀI TOÁN LỒI VÀ ỨNG DỤNG
B = 'B. Các bài toán lồi và ứng dụng'
mc('G', r(24), r'Bài toán nào sau đây KHÔNG nằm trong danh sách “bài toán tối ưu lồi hoặc đưa được về lồi” của slide tr.24?',
   'quy hoạch nguyên hỗn hợp tổng quát (mixed-integer)', ['quy hoạch tuyến tính (linear programming)', 'bài toán bình phương tối thiểu (least squares)', 'quy hoạch nón bậc hai (second order cone programming)'],
   r'Slide liệt kê: Least squares, LP, QP lồi với ràng buộc tuyến tính, QCQP lồi, Conic, Geometric, SOCP, SDP. Quy hoạch nguyên tổng quát (miền rời rạc) không lồi.', B)
mc('G', r(24), r'Slide tr.24 liệt kê SOCP viết tắt cho',
   'Second order cone programming', ['Sequential optimality condition programming', 'Semi-orthogonal convex programming', 'Standard objective constraint problem'],
   r'SOCP = Second Order Cone Programming (quy hoạch nón bậc hai).', B)
mc('G', r(24), r'Slide tr.24 liệt kê SDP viết tắt cho',
   'Semidefinite programming', ['Sequential dual programming', 'Strict descent programming', 'Sparse differentiable problem'],
   r'SDP = Semidefinite Programming (quy hoạch nửa xác định dương): biến là ma trận, ràng buộc \(X\succeq0\).', B)
tf('G', r(24), r'Quy hoạch tuyến tính là một bài toán tối ưu lồi.', True, r'Hàm mục tiêu tuyến tính vừa lồi vừa lõm, ràng buộc tuyến tính cho polyhedron lồi (slide tr.24 và tr.67).', B)
tf('G', r(24), r'Bài toán bình phương tối thiểu \(\min\|Ax-b\|^2\) là bài toán lồi.', True, r'Hessian \(2A^\top A\succeq0\). Bình phương chuẩn của hàm affine là lồi (Module 1).', B)
tf('G', r(24), r'Cực tiểu hóa một hàm toàn phương lồi với ràng buộc toàn phương lồi (QCQP) là bài toán lồi.', True, r'Slide tr.24: “Quadratic minimization with convex quadratic constraints”. Các tập mức dưới của hàm lồi là lồi.', B)
mc('G', r(29), r'Ứng dụng nào sau đây được slide tr.29 nêu cho tối ưu lồi?',
   'tối ưu hóa danh mục đầu tư (portfolio optimization)', ['tối ưu quá trình phân rã hạt nhân', 'bài toán sắp xếp lịch bay tổ hợp không lồi', 'giải phương trình vi phân đạo hàm riêng'],
   r'Slide tr.29: Portfolio optimization, Worst-case risk analysis, Optimal advertising, hồi quy có điều chuẩn, Model fitting (phân loại nhiều lớp).', B)
mc('G', r(33), r'Trong các ứng dụng slide tr.33, “Localization using wireless signals” nghĩa là',
   'xác định vị trí thiết bị từ tín hiệu không dây', ['phân bổ phổ tần cho mọi thiết bị', 'mã hóa tín hiệu không dây', 'giảm nhiễu bằng bộ lọc số'],
   r'Bài toán định vị: cho khoảng cách/tín hiệu đo được từ các trạm, tìm vị trí thiết bị — thường mô hình thành bài toán lồi hoặc nới lồi.', B)
tf('G', r(33), r'Combinatorial optimization xuất hiện trong danh sách ứng dụng của tối ưu lồi ở slide tr.33 (dưới dạng các nới lồi).', True,
   r'Slide tr.33 nêu “Combinatorial optimization”: nhiều bài toán rời rạc được xấp xỉ bằng nới lồi (ví dụ LP relaxation, SDP relaxation).', B)
mc('G', r(67), r'Bài toán quy hoạch tuyến tính trong slide tr.67 có dạng',
   r'\(\min c^\top x+d\) s.t. \(Gx\le h,\ Ax=b\)', [r'\(\min\frac12x^\top Px+q^\top x\) s.t. \(Gx\le h\)', r'\(\min x^\top x\) s.t. \(Ax=b\)', r'\(\min\|x\|_1\) s.t. \(x\ge0\)'],
   r'Slide tr.67: hàm mục tiêu tuyến tính (affine) với ràng buộc \(Gx\le h\), \(Ax=b\).', B)
mc('G', r(68), r'Bài toán QP tuyến tính lồi trong slide tr.68 yêu cầu ma trận P',
   r'\(P\succeq0\) (nửa xác định dương)', [r'\(P\preceq0\)', r'\(P=0\)', r'\(P\) khả nghịch bất kỳ'],
   r'\(\min\tfrac12x^\top Px+q^\top x+r\) s.t. \(Gx\le h,\ Ax=b\) lồi khi và chỉ khi \(P\succeq0\) (Module 1).', B)
tf('G', r(68), r'Nếu \(P=0\), bài toán QP ở slide tr.68 suy biến thành một bài toán quy hoạch tuyến tính.', True,
   r'Khi \(P=0\), hàm mục tiêu là \(q^\top x+r\) tuyến tính: LP là trường hợp riêng của QP.', B)
mc('S', r(68), r'Trong LP ở slide tr.67, ma trận \(G\in\mathbb R^{m\times n}\) đóng vai trò',
   r'ma trận hệ số của các bất đẳng thức \(Gx\le h\)', [r'ma trận hệ số của các đẳng thức \(Ax=b\)', r'ma trận Hessian của hàm mục tiêu', r'ma trận nhân tử Lagrange'],
   r'Slide dùng \(G,h\) cho m bất đẳng thức và \(A,b\) cho p đẳng thức.', B)
mc('S', r(24), r'Thứ tự bao hàm đúng (từ hẹp đến rộng) của các lớp bài toán lồi trong slide tr.24 là',
   'LP ⊂ QP lồi ⊂ QCQP ⊂ SOCP ⊂ SDP', ['SDP ⊂ SOCP ⊂ QCQP ⊂ QP lồi ⊂ LP', 'LP ⊂ SDP ⊂ QP lồi ⊂ SOCP ⊂ QCQP', 'QP lồi ⊂ LP ⊂ SOCP ⊂ QCQP ⊂ SDP'],
   r'Đây là chuỗi bao hàm chuẩn (Boyd Ch.4): mỗi lớp là trường hợp riêng của lớp bên phải. Vì vậy phương pháp điểm trong giải SDP cũng giải được LP.', B)
tf('S', r(24), r'Mọi bài toán SDP đều là quy hoạch tuyến tính.', False, r'Chiều ngược mới đúng: LP là trường hợp riêng của SDP (ma trận đường chéo). SDP tổng quát có ràng buộc \(X\succeq0\) phi tuyến, không phải LP.', B)
tf('S', r(29), r'Bình phương tối thiểu có chuẩn hóa (ridge) \(\min\|Ax-b\|^2+\rho\|x\|^2\) vẫn là bài toán lồi.', True, r'Tổng của hai hàm lồi (\(\|Ax-b\|^2\) và \(\rho\|x\|^2\) với \(\rho\ge0\)) là lồi.', B)
num('S', r(67), r'Bài toán LP: \(\min x_1+2x_2\) s.t. \(x_1+x_2\ge1,\ x\ge0\). Giá trị tối ưu là bao nhiêu?', 1,
    r'Đưa về dạng \(G x\le h\): \(-x_1-x_2\le-1\), \(-x\le0\). Nghiệm \((1,0)\): \(f=1\) (đỉnh của miền; kiểm bằng linprog).', ans_text='1', grp=B)

# =====================================================================  C. LAGRANGE VÀ ĐIỀU KIỆN CẦN KKT
C = 'C. Hàm Lagrange và điều kiện cần KKT'
mc('G', r(38), r'Hàm Lagrange của bài toán (P) trong slide tr.38 là',
   r'\(L(x,\lambda,\mu)=f(x)+\sum_i\lambda_ig_i(x)+\sum_j\mu_jh_j(x)\)', [r'\(L=f(x)-\sum_i\lambda_ig_i(x)-\sum_j\mu_jh_j(x)\)', r'\(L=f(x)\cdot\prod_ig_i(x)\)', r'\(L=\sum_i\lambda_ig_i(x)+\sum_j\mu_jh_j(x)\)'],
   r'Slide tr.38. Dấu “+” cùng yêu cầu \(\lambda_i\ge0\) là quy ước khi dùng dạng \(g_i\le0\).', C)
mc('G', r(38), r'Nhân tử \(\lambda_i\) đi kèm ràng buộc bất đẳng thức \(g_i\le0\) phải thỏa',
   r'\(\lambda_i\ge0\)', [r'\(\lambda_i\le0\)', r'\(\lambda_i\in\mathbb R\) tùy ý', r'\(\lambda_i=1\)'],
   r'Slide tr.40: “\(\lambda_i\ge0\ \forall i\in I,\ \mu_j\in\mathbb R\ \forall j\in J\)”.', C)
mc('G', r(40), r'Nhân tử \(\mu_j\) đi kèm ràng buộc đẳng thức \(h_j=0\) có dấu',
   'tùy ý (thuộc \\(\\mathbb R\\))', ['luôn không âm', 'luôn không dương', 'luôn bằng 0'],
   r'Ràng buộc đẳng thức có thể “kéo” theo cả hai chiều nên \(\mu_j\) không bị ràng buộc dấu (slide tr.40).', C)
mc('G', r(40), r'Điều kiện “dừng” trong hệ KKT ở slide tr.40 là',
   r'\(\nabla_xL(x^*,\lambda,\mu)=0\)', [r'\(L(x^*,\lambda,\mu)=0\)', r'\(\nabla_\lambda L(x^*,\lambda,\mu)=0\)', r'\(\nabla f(x^*)=0\)'],
   r'Slide viết \(L^{\prime}_x(x^*,\lambda,\mu)=0\): đạo hàm của L theo x bằng không. Nói chung \(\nabla f(x^*)\ne0\); phải cộng thêm các thành phần ràng buộc.', C)
mc('G', r(40), r'Hệ KKT gồm mấy nhóm điều kiện chính (theo slide tr.40)?',
   'bốn nhóm: dừng, bù, khả thi gốc, dấu của nhân tử', ['hai nhóm: dừng và khả thi', 'ba nhóm: dừng, bù, hội tụ', 'năm nhóm: dừng, bù, khả thi, bậc hai, Slater'],
   r'Hệ (1): \(L_x=0\); \(\lambda_ig_i=0\); \(g_i\le0,h_j=0\); \(\lambda_i\ge0\).', C)
mc('G', r(43), r'Hai điều kiện \(g_i(x^*)\le0\) và \(h_j(x^*)=0\) trong hệ KKT có nghĩa là',
   r'\(x^*\) là điểm chấp nhận được của bài toán', [r'\(x^*\) là điểm dừng của L', r'\(x^*\) là cực tiểu địa phương', r'nhân tử là không âm'],
   r'Slide tr.43: hai điều kiện này chỉ ra \(x^*\) khả thi (thuộc C).', C)
mc('G', r(43), r'Điều kiện \(\lambda_ig_i(x^*)=0\) được gọi là',
   'điều kiện bù (complementary slackness)', ['điều kiện chính quy Slater', 'điều kiện dừng', 'điều kiện Jensen'],
   r'Tích \(\lambda_ig_i=0\): hoặc nhân tử bằng 0 hoặc ràng buộc chặt (slide tr.43).', C)
mc('G', r(43), r'Các số \(\lambda_i,\mu_j\) trong hệ KKT được gọi là',
   'các nhân tử Lagrange', ['các nghiệm cơ sở', 'các hệ số phạt', 'các ước lượng \\(\\Delta_j\\)'],
   r'Slide tr.43. (\(\Delta_j\) là ước lượng của đơn hình, còn nhân tử tương ứng với biến đối ngẫu trong LP.)', C)
mc('G', r(44), r'Điểm \(x^*\) thỏa hệ (1) được gọi là',
   r'điểm KKT (Karush–Kuhn–Tucker)', ['điểm Slater', 'điểm chính quy', 'điểm Lagrange–Euler'],
   r'Slide tr.44 (và tr.46: điểm KKT đôi khi còn gọi là điểm dừng KKT).', C)
tf('G', r(46), r'Slide tr.46 cho biết điều kiện Slater đảm bảo tính đối ngẫu mạnh.', True, r'Đối ngẫu mạnh: giá trị bài toán gốc bằng giá trị bài toán đối ngẫu (Boyd 5.2.3).', C)
tf('G', r(40), r'Tại điểm KKT, tích \(\lambda_ig_i(x^*)\) bằng 0 với mọi i.', True, r'Đó chính là điều kiện bù.', C)
tf('G', r(40), r'Tại điểm KKT của bài toán tối thiểu, ta phải có \(\nabla f(x^*)=0\).', False, r'Chỉ khi không có ràng buộc chặt. Nói chung \(\nabla f(x^*)=-\sum\lambda_i\nabla g_i-\sum\mu_j\nabla h_j\ne0\).', C)
tf('G', r(43), r'Nếu \(g_i(x^*)<0\) (ràng buộc lỏng) thì nhân tử \(\lambda_i\) tại điểm KKT bằng 0.', True, r'Điều kiện bù \(\lambda_ig_i=0\) với \(g_i\ne0\) buộc \(\lambda_i=0\).', C)
tf('G', r(43), r'Nếu \(\lambda_i>0\) thì ràng buộc \(g_i\) phải chặt (\(g_i(x^*)=0\)) tại điểm KKT.', True, r'Ngược lại: \(\lambda_i>0\) và \(\lambda_ig_i=0\Rightarrow g_i=0\).', C)
tf('G', r(43), r'Nếu ràng buộc \(g_i\) chặt tại \(x^*\) thì nhất thiết \(\lambda_i>0\).', False, r'Ví dụ 1 của slide: \(g_1=x+y-2\) chặt tại \((1/2,3/2)\) nhưng \(\lambda=0\). Điều kiện bù chỉ nói \(\lambda_i\ge0\).', C)
tf('G', r(38), r'Hàm Lagrange có thêm một số hạng cho mỗi ràng buộc, nhân với nhân tử tương ứng.', True, r'Mỗi \(g_i\) có \(\lambda_i\), mỗi \(h_j\) có \(\mu_j\).', C)
tf('G', r(40), r'Định lý điều kiện cần phát biểu: nếu \(x^*\) là nghiệm tối ưu thì tồn tại nhân tử thỏa hệ KKT (khi có điều kiện chính quy).', True, r'Slide tr.40 (phát biểu gọn; cần CQ như Slater hoặc LICQ).', C)
tf('S', r(40), r'Điều kiện cần KKT luôn đúng cho mọi bài toán tối ưu, kể cả khi không có điều kiện chính quy nào.', False,
   r'Phản ví dụ: \(\min x\) s.t. \(x^2\le0\): nghiệm \(x^*=0\) nhưng \(1+2\lambda\cdot0=1\ne0\). Cần CQ.', C)
mc('S', r(40), r'Bài toán \(\min x\) s.t. \(x^2\le0\) cho thấy',
   r'KKT có thể không là điều kiện cần khi thiếu điều kiện chính quy', [r'KKT luôn là điều kiện đủ', r'bài toán không có nghiệm', r'nhân tử Lagrange luôn bằng 1'],
   r'Nghiệm duy nhất \(x^*=0\) nhưng phương trình dừng \(1+2\lambda x=1\) vô nghiệm theo \(\lambda\); Slater thất bại.', C)
mc('S', r(40), r'Tại điểm \(x^*\) không có ràng buộc nào chặt và không có đẳng thức, điều kiện KKT rút gọn thành',
   r'\(\nabla f(x^*)=0\) (mọi \(\lambda_i=0\))', [r'\(\nabla f(x^*)=\mathbf1\)', r'\(f(x^*)=0\)', r'\(g_i(x^*)=0\) với mọi i'],
   r'Bù buộc \(\lambda_i=0\) cho mọi ràng buộc lỏng, nên dừng còn \(\nabla f(x^*)=0\): điều kiện Fermat cho tối ưu không ràng buộc.', C)
mc('S', r(40), r'Xét \(g_1\) chặt duy nhất tại \(x^*\), không có đẳng thức. Điều kiện dừng nói \(\nabla f(x^*)\) và \(\nabla g_1(x^*)\)',
   'ngược hướng nhau (\\(\\nabla f=-\\lambda_1\\nabla g_1\\), \\(\\lambda_1\\ge0\\))', ['cùng hướng với nhau (\\(\\nabla f=\\lambda_1\\nabla g_1\\), \\(\\lambda_1>0\\))', 'vuông góc với nhau', 'không có quan hệ nào'],
   r'\(\nabla f+\lambda_1\nabla g_1=0\) với \(\lambda_1\ge0\): \(-\nabla f\) chỉ ra ngoài miền khả thi theo hướng \(\nabla g_1\) (vượt biên); ta không thể giảm f mà vẫn khả thi.', C)
mc('S', r(38), r'Một ràng buộc có dạng \(x_1\ge2\). Để dùng KKT cần viết lại thành',
   r'\(g(x)=2-x_1\le0\)', [r'\(g(x)=x_1-2\le0\)', r'\(g(x)=x_1-2\ge0\)', r'\(g(x)=2-x_1\ge0\)'],
   r'Dạng chuẩn là \(g\le0\): \(x_1\ge2\Leftrightarrow2-x_1\le0\). Viết sai dấu làm nhân tử đổi dấu.', C)
mc('S', r(38), r'Với ràng buộc \(x_1\ge2\) viết lại thành \(g=2-x_1\le0\), gradient \(\nabla g\) là',
   r'\((-1,0)\)', [r'\((1,0)\)', r'\((2,0)\)', r'\((0,-1)\)'],
   r'\(\partial g/\partial x_1=-1\), \(\partial g/\partial x_2=0\).', C)
mc('S', r(43), r'Hệ quả của điều kiện bù với m ràng buộc bất đẳng thức: số trường hợp cần xét nhiều nhất là',
   r'\(2^m\) (mỗi ràng buộc chặt hoặc lỏng)', [r'\(m!\) (mọi hoán vị)', r'\(m^2\)', r'\(2m\)'],
   r'Mỗi \(g_i\) có hai khả năng (\(\lambda_i=0\) hoặc \(g_i=0\)), tổng \(2^m\) trường hợp, một số bị loại ngay khi vô nghiệm hoặc không khả thi.', C)
mc('S', r(40), r'Sau khi giải hệ dừng + bù, bước bắt buộc tiếp theo là',
   r'kiểm tra \(g_i\le0\) và \(\lambda_i\ge0\) cho từng nghiệm', [r'tính Hessian của f', r'chia nghiệm cho \(\lambda\)', r'đổi min thành max'],
   r'Nhiều nghiệm của hệ phương trình vi phạm khả thi hoặc có nhân tử âm (ví dụ \((1,1)\) có \(\lambda=-1/2\) trong Ví dụ 3), phải loại.', C)
tf('S', r(40), r'Nếu giải hệ dừng cho ra \(\lambda_i<0\) với một ràng buộc chặt thì điểm đó vẫn là điểm KKT.', False, r'KKT yêu cầu \(\lambda_i\ge0\). Nhân tử âm loại bỏ điểm đó (ví dụ \((1,1)\) trong Ví dụ 3).', C)
tf('S', r(38), r'Nhân tử Lagrange của ràng buộc đẳng thức có thể âm mà điểm vẫn là KKT.', True, r'\(\mu_j\in\mathbb R\) không bị hạn chế dấu.', C)
num('S', r(40), r'Bài toán \(\min x^2\) s.t. \(1-x\le0\) (tức \(x\ge1\)). Tại \(x^*=1\), tính nhân tử \(\lambda\).', 2,
    r'\(L=x^2+\lambda(1-x)\); dừng \(2x-\lambda=0\Rightarrow\lambda=2x=2\) tại \(x=1\). \(\lambda=2\ge0\) ✓.', ans_text='2', grp=C)
num('S', r(40), r'Bài toán \(\min(x-3)^2\) s.t. \(x\le1\). Tại \(x^*=1\), tính \(\lambda\) (với \(g=x-1\le0\)).', 4,
    r'\(L=(x-3)^2+\lambda(x-1)\); dừng \(2(x-3)+\lambda=0\Rightarrow\lambda=-2(1-3)=4\ge0\) ✓.', ans_text='4', grp=C)
essay('B', r(40), r'Phát biểu điều kiện cần cực trị KKT (slide tr.40) và giải thích ý nghĩa của điều kiện bù.',
      r'<p>Nếu \(x^*\) là nghiệm tối ưu của (P) (và có điều kiện chính quy) thì tồn tại \(\lambda_i\ge0\ (i\in I)\), \(\mu_j\in\mathbb R\ (j\in J)\) sao cho: (i) \(\nabla f(x^*)+\sum\lambda_i\nabla g_i(x^*)+\sum\mu_j\nabla h_j(x^*)=0\); (ii) \(\lambda_ig_i(x^*)=0\ \forall i\); (iii) \(g_i(x^*)\le0\), \(h_j(x^*)=0\).</p><p>Điều kiện bù: mỗi ràng buộc bất đẳng thức hoặc <i>chặt</i> (\(g_i=0\)) hoặc <i>không tác dụng</i> (\(\lambda_i=0\)). Ràng buộc lỏng không tham gia cân bằng lực nên nhân tử bằng 0.</p>',
      ['Nêu đủ các điều kiện dừng, bù, khả thi, dấu của nhân tử', 'Giải thích ràng buộc lỏng ⇒ nhân tử 0', 'Nhắc điều kiện chính quy'], C)
essay('S', r(43), r'Nêu quy trình chia trường hợp theo tập ràng buộc chặt để giải hệ KKT, và nói rõ các bước lọc nghiệm.',
      r'<ol><li>Chuẩn hóa \(g_i\le0\), viết L và hệ dừng.</li><li>Với mỗi tập \(A\subseteq I\) (ràng buộc chặt): đặt \(g_i=0\ (i\in A)\), \(\lambda_i=0\ (i\notin A)\), giải hệ phương trình còn lại.</li><li>Lọc: giữ nghiệm thỏa \(g_i\le0\ \forall i\) và \(\lambda_i\ge0\).</li><li>Với bài lồi + Slater: điểm còn lại là nghiệm tối ưu; với bài không lồi: so sánh giá trị f (và kiểm tồn tại nghiệm).</li></ol>',
      ['Đủ \(2^m\) trường hợp hoặc lập luận loại bớt', 'Lọc khả thi và dấu nhân tử', 'Phân biệt bài lồi/không lồi ở bước cuối'], C)

# =====================================================================  D. SLATER VÀ ĐIỀU KIỆN CẦN VÀ ĐỦ
D = 'D. Điều kiện Slater và điều kiện cần và đủ'
mc('G', r(47), r'Điều kiện chính quy Slater cho bài toán (P) yêu cầu',
   r'tồn tại \(z\in C\) sao cho \(g_i(z)<0\) với mọi i', [r'tồn tại \(z\in C\) sao cho \(g_i(z)=0\) với mọi i', r'tồn tại \(z\notin C\) sao cho \(g_i(z)<0\)', r'mọi \(z\in C\) đều có \(g_i(z)<0\)'],
   r'Slide tr.47: cần một điểm khả thi làm mọi bất đẳng thức <b>chặt</b>. Không đòi mọi điểm khả thi.', D)
tf('G', r(47), r'Điều kiện Slater đòi hỏi ĐÚNG MỘT điểm khả thi làm mọi bất đẳng thức chặt là đủ.', True, r'Chỉ cần tồn tại một điểm như vậy; không cần mọi điểm.', D)
mc('G', r(47), r'Điểm \(z\) trong điều kiện Slater còn được gọi (trong sách) là',
   'điểm khả thi chặt (strictly feasible point)', ['điểm dừng KKT', 'điểm cực trị toàn cục', 'điểm cực biên'],
   r'Boyd gọi z là “strictly feasible”: \(g_i(z)<0\), \(h_j(z)=0\).', D)
mc('G', r(46), r'Vai trò của điều kiện Slater trong bài toán lồi (slide tr.46) là bảo đảm',
   'tính đối ngẫu mạnh', ['tính lồi của hàm mục tiêu', 'tính khả vi của các ràng buộc', 'tính duy nhất của nghiệm'],
   r'Slater kéo theo đối ngẫu mạnh và (Boyd 5.5) KKT là điều kiện cần và đủ.', D)
mc('G', r(48), r'Hình (b) của slide tr.48 (“Not have interior point”) minh họa',
   'miền khả thi không có điểm trong nên Slater thất bại', ['miền khả thi rỗng', 'hàm mục tiêu không lồi', 'nhân tử Lagrange bằng 0'],
   r'Slide tr.48: “ĐK Slater không thỏa mãn” với hai trường hợp: không đủ hạng dòng (a) và không có điểm trong (b).', D)
mc('G', r(48), r'Hình (a) của slide tr.48 (“Not full row rank”) minh họa',
   'ràng buộc suy biến (gradient phụ thuộc tuyến tính), Slater/LICQ thất bại', ['miền khả thi quá lớn', 'hàm mục tiêu tuyến tính', 'điểm z nằm trong miền'],
   r'Khi các ràng buộc chặt có gradient phụ thuộc tuyến tính, nhân tử không duy nhất hoặc không tồn tại.', D)
mc('G', r(50), r'Định lý “cần và đủ” của slide tr.50 cần giả thiết',
   'bài toán lồi, điều kiện Slater và \\(x^*\\) khả thi', ['chỉ cần \\(x^*\\) khả thi', 'chỉ cần f khả vi', 'bài toán không lồi và nhân tử dương'],
   r'Slide tr.50: Slater thỏa; \(x^*\) chấp nhận được; khi đó \(x^*\) tối ưu ⇔ tồn tại \(\lambda,\mu\) thỏa hệ KKT.', D)
tf('G', r(50), r'Với bài toán lồi thỏa Slater, mọi điểm KKT đều là nghiệm tối ưu toàn cục.', True, r'Chiều đủ của định lý ở slide tr.50 (chứng minh bằng điều kiện cấp 1 cho \(L\) lồi theo x).', D)
tf('G', r(50), r'Với bài toán lồi thỏa Slater, nghiệm tối ưu nhất thiết là điểm KKT.', True, r'Chiều cần của định lý ở slide tr.50.', D)
tf('G', r(50), r'Với bài toán không lồi, mọi điểm KKT đều là điểm cực tiểu toàn cục.', False, r'Slide tr.56: “Đối với bài toán tối ưu không lồi, điểm KKT có thể không là điểm cực tiểu địa phương”. Ví dụ \((0,0)\) trong Ví dụ 3.', D)
mc('G', r(56), r'Slide tr.56 chú ý điều gì về bài toán không lồi?',
   'điểm KKT có thể không là cực tiểu địa phương', ['điểm KKT luôn là cực đại', 'không có điểm KKT nào', 'nhân tử luôn âm'],
   r'KKT chỉ là điều kiện cần trong trường hợp không lồi; cần xét thêm điều kiện bậc hai hoặc so sánh.', D)
mc('S', r(50), r'Bài toán \(\min x^2\) s.t. \(x\ge1\) là bài toán lồi, Slater thỏa vì',
   r'tồn tại \(z=2\) với \(g(2)=1-2<0\)', [r'\(g(1)=0\) chặt', r'f có Hessian bằng 2', r'\(x=0\) khả thi'],
   r'\(z=2\) khả thi và \(g(z)=-1<0\). Vì vậy KKT là cần và đủ: \(x^*=1\), \(\lambda=2\).', D)
mc('S', r(47), r'Miền \(\{(x,y)\mid x^2+y^2\le1,\ x+y\ge2\}\) có thỏa Slater không?',
   r'không, vì miền rỗng', [r'có, tại \((1,1)\)', r'có, tại \((0,0)\)', r'không, vì f không lồi'],
   r'\(x+y\ge2\) với \(x^2+y^2\le1\): \(x+y\le\sqrt2<2\). Miền rỗng nên không có điểm khả thi.', D)
mc('S', r(47), r'Miền \(\{x\mid x\le0,\ -x\le0\}=\{0\}\) không thỏa Slater vì',
   r'không có điểm nào làm cả \(x<0\) và \(-x<0\)', [r'miền không lồi', r'miền không bị chặn', r'hàm ràng buộc không khả vi'],
   r'Hai bất đẳng thức tạo thành một đẳng thức ngầm (\(x=0\)); không có điểm khả thi chặt.', D)
tf('S', r(47), r'Một miền chỉ gồm ràng buộc đẳng thức affine luôn thỏa Slater khi nó khác rỗng.', True, r'Slater chỉ đòi bất đẳng thức chặt; nếu không có bất đẳng thức thì điều kiện được thỏa khi miền khác rỗng.', D)
tf('S', r(50), r'Định lý cần và đủ vẫn đúng nếu ta bỏ giả thiết “bài toán lồi”.', False, r'Chiều đủ cần lồi (như ví dụ min xy trên đĩa: \((0,0)\) là KKT nhưng không tối ưu).', D)
tf('S', r(50), r'Nếu bài toán là LP thì KKT luôn là điều kiện cần và đủ khi có nghiệm (không cần kiểm Slater).', True,
   r'Với ràng buộc affine, Slater được thay bằng điều kiện yếu hơn (chỉ cần khả thi); LP thỏa CQ tuyến tính nên KKT cần và đủ.', D)
mc('S', r(50), r'Trong bài toán lồi thỏa Slater, sau khi tìm được điểm thỏa hệ KKT, ta kết luận',
   'đó là nghiệm tối ưu toàn cục', ['đó chỉ là cực tiểu địa phương', 'cần kiểm tra thêm Hessian', 'đó là cực đại'],
   r'Định lý cần và đủ: không cần thêm điều kiện bậc hai.', D)
mc('S', r(50), r'Trong bài toán không lồi, sau khi tìm các điểm KKT ta nên',
   'so sánh giá trị f tại các ứng viên (và kiểm tra tồn tại nghiệm)', ['chọn điểm có \\(\\lambda\\) lớn nhất', 'chọn điểm có \\(x\\) nhỏ nhất', 'kết luận mọi điểm KKT đều tối ưu'],
   r'Miền compact ⇒ tồn tại nghiệm (Weierstrass) và nghiệm là điểm KKT (nếu CQ), nên chọn ứng viên có f nhỏ nhất (Ví dụ 3).', D)
num('S', r(47), r'Miền \(x_1+x_2\le1\), \(x_1\ge0\), \(x_2\ge0\). Tính \(g_1(z)\) với \(g_1=x_1+x_2-1\) tại điểm Slater \(z=(0.25,0.25)\).', -0.5,
    r'\(0.25+0.25-1=-0.5<0\); các ràng buộc \(-x_i\le0\) cũng chặt (\(-0.25\)). Slater thỏa.', ans_text='-0.5', grp=D)
essay('B', r(48), r'Slide tr.66: cho ví dụ một miền ràng buộc của bài toán tối ưu lồi mà không thỏa điều kiện Slater, và cho biết hậu quả.',
      r'<p>Miền \(C=\{x\in\mathbb R\mid x^2\le0\}=\{0\}\) (\(g=x^2\) lồi). Mọi điểm khả thi có \(g=0\), không tồn tại z với \(g(z)<0\). Hậu quả: bài toán \(\min x\) s.t. \(x^2\le0\) có nghiệm \(x^*=0\) nhưng hệ KKT vô nghiệm (\(1+2\lambda\cdot0=1\ne0\)); KKT không còn là điều kiện cần. Ví dụ khác: hai bất đẳng thức \(x\le0\) và \(-x\le0\).</p>',
      ['Chỉ ra miền lồi nhưng không có điểm khả thi chặt', 'Nêu hậu quả cho KKT'], D)
essay('S', r(50), r'Chứng minh chiều “đủ” của định lý cần và đủ: nếu bài toán lồi và \(x^*\) khả thi thỏa hệ KKT thì \(x^*\) là nghiệm tối ưu.',
      r'<p>Với \(\lambda\ge0\), \(L(x,\lambda,\mu)=f(x)+\sum\lambda_ig_i+\sum\mu_jh_j\) là hàm lồi theo x (tổng các hàm lồi nhân hệ số không âm và các hàm affine). Vì \(\nabla_xL(x^*)=0\) nên \(x^*\) cực tiểu toàn cục của \(L(\cdot,\lambda,\mu)\). Với mọi x khả thi: \(f(x)\ge f(x)+\sum\lambda_ig_i(x)+\sum\mu_jh_j(x)=L(x)\ge L(x^*)=f(x^*)+\sum\lambda_ig_i(x^*)=f(x^*)\) (dùng \(g_i(x)\le0,\lambda_i\ge0\), \(h_j=0\) và điều kiện bù). Vậy \(f(x)\ge f(x^*)\).</p>',
      ['L lồi theo x nên dừng ⇒ cực tiểu', 'Dùng \\(\\lambda\\ge0\\), \\(g\\le0\\)', 'Dùng điều kiện bù để \\(L(x^*)=f(x^*)\\)'], D)

# =====================================================================  E. VÍ DỤ 1–4 VÀ THẢO LUẬN
E = 'E. Ví dụ 1–4 và câu hỏi thảo luận'
mc('B', r(55), r'Ví dụ 1 (slide tr.55): \(\min(x-1)^2+y-2\) s.t. \(x+y-2\le0\), \(x-y+1=0\). Bài toán này là',
   'bài toán lồi và Slater thỏa mãn', ['bài toán không lồi', 'bài toán lồi nhưng Slater không thỏa', 'bài toán không có điểm khả thi'],
   r'\(f\) lồi, \(g\) và \(h\) affine. Slater: \((0,1)\) có \(h=0\), \(g=-1<0\).', E)
mc('B', r(55), r'Nghiệm tối ưu của Ví dụ 1 theo slide là',
   r'\((x^*,y^*)=(1/2,3/2)\)', [r'\((x^*,y^*)=(1,0)\)', r'\((x^*,y^*)=(0,1)\)', r'\((x^*,y^*)=(3/2,1/2)\)'],
   r'Kiểm bằng sympy và SLSQP (kết quả ' + str(R['m2_ex1_num'][0]) + r'). \((1/2,3/2)\) thỏa \(h=1/2-3/2+1=0\) và \(g=0\).', E)
mc('B', r(55), r'Cặp nhân tử \((\lambda,\mu)\) ứng với nghiệm của Ví dụ 1 là',
   r'\((\lambda,\mu)=(0,1)\)', [r'\((\lambda,\mu)=(1,0)\)', r'\((\lambda,\mu)=(1,1)\)', r'\((\lambda,\mu)=(0,-1)\)'],
   r'Dừng: \(2(x-1)+\lambda+\mu=0\Rightarrow-1+0+\mu=0\Rightarrow\mu=1\); \(1+\lambda-\mu=0\Rightarrow\lambda=0\).', E)
num('B', r(55), r'Giá trị tối ưu \(f^*\) của Ví dụ 1 là bao nhiêu?', float(R['m2_ex1_num'][1]),
    r'\(f(1/2,3/2)=(1/2-1)^2+3/2-2=0.25-0.5=-0.25\).', ans_text='-0.25', grp=E)
tf('B', r(55), r'Trong Ví dụ 1 ràng buộc bất đẳng thức \(x+y-2\le0\) là chặt tại nghiệm nhưng nhân tử \(\lambda=0\).', True,
   r'\(1/2+3/2-2=0\): chặt. Nhưng dừng cho \(\lambda=0\). Đây là suy biến của điều kiện bù.', E)
mc('B', r(57), r'Ví dụ 2 (slide tr.57/59) yêu cầu \(\max f=x^2+y^2+4x-6y\) với \(x+y\le3\), \(-2x+y\le2\). Slide chuyển thành',
   r'bài toán cực tiểu \(-f\) (không lồi)', [r'bài toán cực tiểu f (lồi)', r'bài toán cực đại \(-f\)', r'bài toán không ràng buộc'],
   r'\(\max f=-\min(-f)\); \(-f=-x^2-y^2-4x+6y\) là hàm lõm nên bài toán min là không lồi.', E)
mc('B', r(57), r'Kiểm chứng bằng code cho thấy tại \((1/3,8/3)\) (Ví dụ 2), nhân tử \((\lambda_1,\lambda_2)\) bằng',
   r'\((10/9,\,-16/9)\): có nhân tử âm nên không phải điểm KKT', [r'\((1,1)\): hợp lệ', r'\((0,0)\): hợp lệ', r'\((2,4)\): hợp lệ'],
   r'Giải \(\lambda_1(1,1)+\lambda_2(-2,1)=(14/3,-2/3)\): \(\lambda_2=-16/9\). Vì có nhân tử âm nên điểm không là KKT của \(\min(-f)\) (xem trang “Kiểm chứng”).', E)
tf('B', r(57), r'Bài toán \(\max x^2+y^2+4x-6y\) trên miền của Ví dụ 2 bị chặn trên.', False,
   r'Miền \(\{x+y\le3,\ -2x+y\le2\}\) không bị chặn (nón mở về phía \(x\to-\infty\)); điểm \((-100,-198)\) khả thi cho \(f=49992\), f có thể lớn tùy ý.', E)
mc('B', r(57), r'Nếu Ví dụ 2 là bài toán CỰC TIỂU \(f=x^2+y^2+4x-6y\) trên cùng miền, điểm KKT là',
   r'\((0,2)\) với \(\lambda=(0,2)\)', [r'\((1/3,8/3)\) với \(\lambda=(10/9,0)\)', r'\((-2,3)\) với \(\lambda=(0,0)\)', r'\((0,0)\) với \(\lambda=(2,0)\)'],
   r'Cực tiểu không ràng buộc \((-2,3)\) vi phạm \(-2x+y\le2\); ràng buộc \(g_2\) chặt cho \((0,2)\), \(\lambda_2=2\ge0\). Kiểm SLSQP: \(f=-8\).', E)
mc('B', r(60), r'Ví dụ 3 (slide tr.60): \(\min xy\) s.t. \(x^2+y^2\le2\). Có mấy điểm KKT hợp lệ (\(\lambda\ge0\))?',
   'ba: (0,0), (1,−1), (−1,1)', ['hai: (1,1), (−1,−1)', 'bốn: (1,1), (−1,−1), (1,−1), (−1,1)', 'một: (0,0)'],
   r'Slide tr.60: ba điểm hợp lệ \((0,0)\) (\(\lambda=0\)), \((-1,1)\) và \((1,-1)\) (\(\lambda=1/2\)); loại \((1,1)\), \((-1,-1)\) vì \(\lambda=-1/2<0\).', E)
mc('B', r(60), r'Trong Ví dụ 3, vì sao \((1,1)\) bị loại?',
   r'vì nhân tử \(\lambda=-1/2<0\)', [r'vì \((1,1)\) không khả thi', r'vì f không xác định tại \((1,1)\)', r'vì \(g(1,1)<0\)'],
   r'\((1,1)\) khả thi (\(g=0\)) nhưng \(y+2\lambda x=0\Rightarrow1+2\lambda=0\Rightarrow\lambda=-1/2\). KKT đòi \(\lambda\ge0\).', E)
tf('B', r(60), r'Trong Ví dụ 3, điểm \((0,0)\) là điểm cực tiểu toàn cục của \(f=xy\) trên đĩa.', False,
   r'\(f(0,0)=0\) nhưng \(f(1,-1)=-1<0\). \((0,0)\) là yên ngựa (KKT nhưng không tối ưu).', E)
num('B', r(60), r'Giá trị cực tiểu của \(f=xy\) trên \(\{x^2+y^2\le2\}\) là bao nhiêu?', -1,
    r'Cực tiểu toàn cục tại \((1,-1),(-1,1)\): \(f=-1\) (Weierstrass: miền compact; so sánh với \(f(0,0)=0\)).', ans_text='-1', grp=E)
num('B', r(60), r'Nhân tử \(\lambda\) tại điểm cực tiểu \((1,-1)\) của Ví dụ 3 là bao nhiêu?', 0.5,
    r'\(y+2\lambda x=0\Rightarrow-1+2\lambda=0\Rightarrow\lambda=\tfrac12\).', ans_text='0.5', grp=E)
mc('B', r(60), r'Hessian của hàm Lagrange \(L=xy+\lambda(x^2+y^2-2)\) theo \((x,y)\) tại \(\lambda=0\) là',
   r'\(\begin{pmatrix}0&1\\1&0\end{pmatrix}\), không xác định (yên ngựa)', [r'\(\begin{pmatrix}1&0\\0&1\end{pmatrix}\), xác định dương', r'\(\begin{pmatrix}0&0\\0&0\end{pmatrix}\), suy biến', r'\(\begin{pmatrix}-1&0\\0&-1\end{pmatrix}\), xác định âm'],
   r'\(\nabla^2L=\begin{pmatrix}2\lambda&1\\1&2\lambda\end{pmatrix}\): tại \(\lambda=0\) có giá trị riêng \(\pm1\) (không xác định) ⇒ yên ngựa; tại \(\lambda=1/2\) là \(\begin{pmatrix}1&1\\1&1\end{pmatrix}\succeq0\).', E)
mc('B', r(61), r'Ví dụ 4 (slide tr.61): \(\min2x+y\) s.t. \(3x+y\le6,\ x+y\le4,\ x,y\ge0\). Nghiệm tối ưu là',
   r'\((0,0)\) với giá trị 0', [r'\((1,3)\) với giá trị 5', r'\((2,0)\) với giá trị 4', r'\((0,4)\) với giá trị 4'],
   r'Với hệ số dương, cực tiểu tại gốc: \(f=0\) (kiểm bằng linprog: ' + str(R['m2_ex4_min']) + r'). Nếu là bài max thì tối ưu tại \((1,3)\) với \(f=5\).', E)
num('B', r(61), r'Nếu Ví dụ 4 là bài toán cực ĐẠI \(2x+y\) trên cùng miền, giá trị tối ưu là', R['m2_ex4_max'][1],
    r'Đỉnh \((1,3)\) (giao \(3x+y=6\) và \(x+y=4\)): \(2+3=5\); các đỉnh khác cho \(0,4,4\).', ans_text='5', grp=E)
mc('B', r(61), r'Nhân tử của Ví dụ 4 tại nghiệm \((0,0)\) là \((\lambda_3,\lambda_4)\) (cho \(-x\le0\), \(-y\le0\)) bằng',
   r'\((2,1)\)', [r'\((1,2)\)', r'\((0,0)\)', r'\((-2,-1)\)'],
   r'\(\nabla f=(2,1)\); \(\nabla g_3=(-1,0)\), \(\nabla g_4=(0,-1)\); \((2,1)+\lambda_3(-1,0)+\lambda_4(0,-1)=0\Rightarrow\lambda_3=2,\lambda_4=1\).', E)
tf('B', r(61), r'Ví dụ 4 là quy hoạch tuyến tính nên KKT là điều kiện cần và đủ.', True, r'LP lồi với ràng buộc affine; KKT cần và đủ (và đối ngẫu mạnh).', E)
mc('B', r(66), r'Câu hỏi thảo luận 1 (slide tr.66): ví dụ một miền ràng buộc lồi không thỏa Slater là',
   r'\(\{x\in\mathbb R\mid x^2\le0\}\)', [r'\(\{x\mid x^2\le1\}\)', r'\(\{x\mid x\ge1\}\)', r'\(\{(x,y)\mid x^2+y^2\le1\}\)'],
   r'Miền là \(\{0\}\); không có \(z\) với \(z^2<0\). Các miền còn lại có điểm trong.', E)
mc('B', r(66), r'Câu hỏi thảo luận 2: cặp nhân tử \((\lambda,\mu)\) ứng với một điểm KKT có duy nhất không?',
   r'không nhất thiết; duy nhất khi các gradient ràng buộc chặt độc lập tuyến tính (LICQ)', [r'luôn duy nhất', r'không bao giờ duy nhất', r'duy nhất khi f lồi chặt'],
   r'Ví dụ ràng buộc \(x\le0\) viết hai lần: hai nhân tử \(\lambda_1+\lambda_2\) chia được tùy ý. LICQ đảm bảo duy nhất.', E)
mc('B', r(66), r'Câu hỏi thảo luận 3: một điều kiện đủ để bài toán tối ưu lồi có nghiệm DUY NHẤT là',
   'f lồi chặt trên tập chấp nhận được', ['f tuyến tính', 'C rỗng', 'C bị chặn'],
   r'Nếu \(x_1\ne x_2\) đều tối ưu thì trung điểm cho \(f<f^*\) (lồi chặt), mâu thuẫn.', E)
mc('B', r(66), r'Câu hỏi thảo luận 4: bài toán tối ưu lồi có thể có ĐÚNG hai nghiệm không?',
   'không: nếu có hai nghiệm phân biệt thì có vô số (cả đoạn nối)', ['có, luôn có đúng hai nghiệm', 'có, nếu f khả vi', 'không, luôn có nghiệm duy nhất'],
   r'Tập nghiệm là lồi: chứa cả đoạn nối hai nghiệm nên là một điểm hoặc vô hạn điểm.', E)
mc('B', r(66), r'Câu hỏi thảo luận 5: tập nghiệm của bài toán tối ưu lồi có tính chất gì?',
   'là tập lồi (và đóng)', ['là tập hữu hạn', 'là tập rời rạc', 'luôn chỉ có một điểm'],
   r'\(\{x\in C\mid f(x)=f^*\}\) là giao của C với tập mức dưới lồi \(\{f\le f^*\}\), do đó lồi (và đóng nếu f liên tục).', E)
tf('B', r(66), r'Tập nghiệm của bài toán tối ưu lồi có thể gồm đúng hai điểm rời nhau.', False, r'Vì tập nghiệm lồi: hai điểm phân biệt kéo theo cả đoạn nối.', E)
tf('B', r(66), r'Bài toán LP có thể có vô số nghiệm tối ưu (cả một cạnh).', True, r'Khi vector \(c\) vuông góc với một cạnh của polyhedron, cả cạnh đó là tập nghiệm (nghiệm không duy nhất).', E)
mc('S', r(60), r'Vì sao có thể chắc chắn Ví dụ 3 có nghiệm tối ưu (dù bài không lồi)?',
   r'vì \(f\) liên tục trên tập compact (định lý Weierstrass)', [r'vì f lồi', r'vì có điều kiện Slater', r'vì KKT có nghiệm'],
   r'Miền \(\{x^2+y^2\le2\}\) đóng và bị chặn; f liên tục ⇒ đạt min. Sau đó nghiệm phải là một trong các điểm KKT (khi có CQ).', E)
mc('S', r(60), r'Với \(f=xy\) và \((t,-t)\), tại \(t\ne0\) nhỏ, \(f(t,-t)\) bằng',
   r'\(-t^2<0=f(0,0)\)', [r'\(t^2>0\)', r'\(0\)', r'\(2t\)'],
   r'Do đó \((0,0)\) không là cực tiểu địa phương (có điểm lân cận với f nhỏ hơn): điểm yên ngựa.', E)
mc('S', r(55), r'Kiểm tra điều kiện Slater cho Ví dụ 1 bằng điểm \(z=(0,1)\): giá trị \(g(z)\) và \(h(z)\) là',
   r'\(g=-1<0\) và \(h=0\)', [r'\(g=0\) và \(h=0\)', r'\(g=1\) và \(h=-2\)', r'\(g=-1\) và \(h=1\)'],
   r'\(g(0,1)=0+1-2=-1\); \(h(0,1)=0-1+1=0\). ✓', E)
tf('S', r(59), r'Nếu đề Ví dụ 2 là bài toán cực đại, ta vẫn có thể kết luận nghiệm tối ưu bằng cách liệt kê điểm KKT mà không cần kiểm tra miền có bị chặn.', False,
   r'Nếu miền không bị chặn (như Ví dụ 2) thì cực đại có thể không tồn tại; KKT chỉ cho ứng viên khi nghiệm tồn tại. Phải kiểm tồn tại nghiệm.', E)
mc('T', 'Studocu C9', r'Bài tập tham khảo: \(\min3x_1^2+3x_2^2-4x_1x_2\) s.t. \(-x_1-x_2+2\le0\), \(x_1^2+x_2^2-4\le0\). Nghiệm tối ưu là',
   r'\(x^*=(1,1)\), \(f^*=2\)', [r'\(x^*=(0,0)\), \(f^*=0\)', r'\(x^*=(\sqrt2,\sqrt2)\), \(f^*=4\)', r'\(x^*=(2,0)\), \(f^*=12\)'],
   r'\(g_1\) chặt, \(g_2\) lỏng, \(\lambda_1=2\). Kiểm SLSQP: ' + str(R['m2_c9_num']) + r'. \((0,0)\) vi phạm \(g_1\); \((\sqrt2,\sqrt2)\) làm \(g_2=0\) nhưng không tối ưu.', E)
num('T', 'Studocu C9', r'Bài tập C9: giá trị nhân tử \(\lambda_1\) của ràng buộc \(-x_1-x_2+2\le0\) tại nghiệm \((1,1)\) là', 2,
    r'\(\nabla f=(6-4,6-4)=(2,2)\), \(\nabla g_1=(-1,-1)\): \((2,2)+\lambda_1(-1,-1)=0\Rightarrow\lambda_1=2\).', ans_text='2', grp=E)
mc('T', 'Studocu C10', r'Bài tập tham khảo: \(\min4x_1^2+x_2^2-x_1-2x_2\) s.t. \(2x_1+x_2\le1\), \(x_1^2-1\le0\). Nghiệm tối ưu là',
   r'\(x^*=(1/16,\,7/8)\), \(f^*=-33/32\)', [r'\(x^*=(1/8,\,1)\), \(f^*=-0.9375\)', r'\(x^*=(0,\,1)\), \(f^*=-1\)', r'\(x^*=(1/2,\,0)\), \(f^*=0\)'],
   r'Cực tiểu không ràng buộc \((1/8,1)\) vi phạm \(2x_1+x_2\le1\). Với \(g_1\) chặt: \(\lambda=1/4\). Kiểm SLSQP: ' + str(R['m2_c10_num']) + r'.', E)
num('T', 'Studocu C10', r'Bài tập C10: nhân tử \(\lambda_1\) của ràng buộc \(2x_1+x_2-1\le0\) tại nghiệm là', 0.25,
    r'\(\nabla f=(8x_1-1,2x_2-2)=(-0.5,-0.25)\), \(\nabla g_1=(2,1)\): \(-0.5+2\lambda=0\Rightarrow\lambda=0.25\) (và \(-0.25+\lambda=0\) ✓).', ans_text='0.25', grp=E)
num('T', 'Studocu C10', r'Bài tập C10: giá trị tối ưu \(f^*\) (lấy bốn chữ số thập phân)', -1.03125,
    r'\(f(1/16,7/8)=4/256+49/64-1/16-7/4=-33/32=-1.03125\).', tol=1e-4, ans_text='-1.03125', grp=E)
mc('T', 'Studocu C9-10', r'Trong bài tập C9 và C10, để áp dụng “KKT là cần và đủ” trước hết phải',
   'kiểm tra bài toán lồi và điều kiện Slater', ['tính Hessian của hàm Lagrange', 'chuyển sang bài toán đối ngẫu', 'đặt mọi nhân tử bằng 1'],
   r'Đề bài yêu cầu “Kiểm tra điều kiện Slater và giải”: có Slater + lồi ⇒ KKT là cần và đủ, nên chỉ cần tìm một điểm KKT.', E)

# =====================================================================  F. CASE STUDY, ESSAY TỔNG HỢP
F = 'F. Tổng hợp'
num('S', 'case study', r'Danh mục đầu tư (case study): tỉ trọng tài sản 1 tại nghiệm tối ưu \(w_1^*\) (làm tròn 4 chữ số) là', float(c_m2.w_star[0]),
    r'\(w^*=(6/7,0,1/7)\): \(6/7\approx0.8571\) (giải \(\Sigma_{\{1,3\}}^{-1}\mathbf1\), chuẩn hóa tổng bằng 1).', tol=1e-3, ans_text='0.8571', grp=F)
num('S', 'case study', r'Danh mục đầu tư: rủi ro (phương sai) \(w^{*\top}\Sigma w^*\) tại nghiệm tối ưu, nhân 1000 và làm tròn 3 chữ số', 1000 * float(c_m2.var_star),
    r'\(w^{*\top}\Sigma w^*=' + ('%.6f' % c_m2.var_star) + r'\); nhân 1000: ' + ('%.3f' % (1000 * c_m2.var_star)) + '.', tol=1e-3, ans_text=('%.3f' % (1000 * c_m2.var_star)), grp=F)
tf('S', 'case study', r'Trong case study, nhân tử của ràng buộc \(w_2\ge0\) dương (\(\lambda_2>0\)) nghĩa là việc ép \(w_2=0\) làm phương sai tối ưu tăng so với khi cho phép bán khống.', True,
   r'\(\lambda_2\) là độ nhạy: nới ràng buộc \(w_2\ge0\) một chút thì giá trị tối ưu giảm khoảng \(\lambda_2\) mỗi đơn vị nới.', F)
mc('S', r(50), r'Trong bài toán lồi thỏa Slater, điểm KKT \(x^*\) cho nhân tử \(\lambda_i>0\). Điều đó cho biết',
   r'ràng buộc \(g_i\) chặt tại \(x^*\) và “có giá” (nới lỏng sẽ giảm f)', [r'ràng buộc \(g_i\) lỏng tại \(x^*\)', r'f đạt cực đại', r'bài toán không có nghiệm'],
   r'Bù: \(\lambda_i>0\Rightarrow g_i=0\). Độ nhạy: \(\partial f^*/\partial u_i=-\lambda_i\) nếu ràng buộc là \(g_i\le u_i\) (Boyd 5.6).', F)
mc('S', r(50), r'Điều nào KHÔNG đúng khi giải bài toán lồi có ràng buộc bằng KKT?',
   'nhân tử \\(\\lambda_i\\) luôn dương tại mọi ràng buộc chặt', ['bài toán lồi thỏa Slater thì điểm KKT là nghiệm', 'nhân tử \\(\\mu_j\\) có thể mang dấu âm', 'ràng buộc lỏng có nhân tử bằng 0'],
   r'Ràng buộc chặt vẫn có thể có \(\lambda_i=0\) (suy biến bù), ví dụ Ví dụ 1.', F)
essay('B', r(60), r'Giải bài toán \(\min xy\) với \(x^2+y^2\le2\) (Ví dụ 3 slide tr.60): tìm mọi điểm KKT, loại điểm không hợp lệ, kết luận nghiệm.',
      r'<p>\(L=xy+\lambda(x^2+y^2-2)\). Dừng: \(y+2\lambda x=0\), \(x+2\lambda y=0\); bù \(\lambda(x^2+y^2-2)=0\).</p><p>Nếu \(\lambda=0\): \((x,y)=(0,0)\), khả thi, \(f=0\).</p><p>Nếu \(x^2+y^2=2\): từ dừng \(x^2=y^2\) ⇒ \(y=\pm x\), \(x=\pm1\). \(y=x\): \(\lambda=-1/2<0\) loại (\((1,1),(-1,-1)\)). \(y=-x\): \(\lambda=1/2\ge0\) ✓ (\((1,-1),(-1,1)\), \(f=-1\)).</p><p>Miền compact ⇒ có nghiệm; so sánh: \(f_{\min}=-1\) tại \((1,-1),(-1,1)\); \((0,0)\) là yên ngựa.</p>',
      ['Đủ các trường hợp \\(\\lambda=0\\) và \\(g=0\\)', 'Loại nghiệm có \\(\\lambda<0\\)', 'Kết luận bằng so sánh giá trị'], F)
essay('B', r(55), r'Giải Ví dụ 1 (slide tr.55) đầy đủ: chứng minh bài toán lồi, kiểm tra Slater, giải KKT và kết luận.',
      r'<p>\(f\) lồi (\((x-1)^2\) lồi, \(y-2\) affine); \(g=x+y-2\) và \(h=x-y+1\) affine ⇒ bài toán lồi. Slater: \(z=(0,1)\): \(h=0\), \(g=-1<0\).</p><p>\(L=(x-1)^2+y-2+\lambda(x+y-2)+\mu(x-y+1)\); dừng: \(2(x-1)+\lambda+\mu=0\), \(1+\lambda-\mu=0\). Với \(\lambda=0\): \(\mu=1\), \(x=1/2\), \(y=3/2\) (từ \(h=0\)), \(g=0\) khả thi. Vì bài lồi + Slater nên \((1/2,3/2)\) là nghiệm, \((\lambda,\mu)=(0,1)\), \(f^*=-1/4\).</p>',
      ['Chứng minh lồi', 'Kiểm Slater bằng điểm cụ thể', 'Giải hệ và kiểm dấu nhân tử'], F)
essay('S', 'case study', r'Giải bài toán danh mục 2 tài sản: \(\min w^\top\Sigma w\) s.t. \(w_1+w_2=1,\ w\ge0\) với \(\Sigma=\begin{pmatrix}0.04&0.01\\0.01&0.09\end{pmatrix}\).',
      r'<p>Bỏ ràng buộc \(w\ge0\): \(w\propto\Sigma^{-1}\mathbf1\). \(\Sigma^{-1}\mathbf1\propto(0.09-0.01,\ 0.04-0.01)=(0.08,0.03)\) ⇒ \(w=(8/11,3/11)\approx(0.727,0.273)\ge0\) nên thỏa cả \(w\ge0\): \(\lambda=0\). Phương sai \(=\dfrac{\det\Sigma}{0.09+0.04-2(0.01)}=\dfrac{0.0035}{0.11}\approx0.0318\).</p>',
      ['Nhận ra nghiệm không ràng buộc đã khả thi', 'Nêu \\(\\lambda=0\\)', 'Tính giá trị tối ưu'], F)

# ---- cân bằng độ dài đáp án (mỗi đáp án nhiễu là một hiểu sai có thật) ----
F_ = bank.fix
F_(r'Trong slide, các tập \(I\) và \(J\) là', 'các tập chỉ số của ràng buộc bất đẳng thức và đẳng thức',
   ['hai tập nghiệm của cặp bài toán gốc và đối ngẫu', 'hai tập lồi chứa các điểm cực tiểu địa phương', 'các tập điểm KKT và tập điểm dừng của L'])
F_(r'Điểm mạnh nhất của bài toán tối ưu lồi', 'cực tiểu địa phương cũng là cực tiểu toàn cục',
   ['luôn có nghiệm duy nhất trên tập chấp nhận được', 'luôn giải được bằng một công thức đóng', 'hàm mục tiêu luôn là hàm tuyến tính'])
F_(r'Trong các ứng dụng slide tr.33, “Localization', 'xác định vị trí thiết bị từ tín hiệu',
   ['phân bổ phổ tần cho mọi thiết bị', 'mã hóa tín hiệu không dây', 'giảm nhiễu bằng bộ lọc số'])
F_(r'Hai điều kiện \(g_i(x^*)\le0\) và', r'\(x^*\) là điểm chấp nhận được của bài toán',
   [r'\(x^*\) là điểm dừng của hàm Lagrange L', r'\(x^*\) là cực tiểu địa phương của f trên C', r'các nhân tử Lagrange đều không âm'])
F_(r'Bài toán \(\min x\) s.t. \(x^2\le0\) cho thấy', r'KKT không là điều kiện cần khi thiếu điều kiện chính quy',
   [r'KKT luôn là điều kiện đủ cho mọi bài toán', r'bài toán này không có nghiệm tối ưu nào', r'nhân tử Lagrange luôn phải bằng 1'])
F_(r'Sau khi giải hệ dừng + bù, bước bắt buộc', r'kiểm tra \(g_i\le0\) và \(\lambda_i\ge0\)',
   [r'tính Hessian của f tại nghiệm tìm được', r'chia nghiệm cho các nhân tử \(\lambda\)', r'đổi bài toán min thành bài toán max'])
F_(r'Hình (b) của slide tr.48', 'miền không có điểm trong nên Slater thất bại',
   ['miền khả thi rỗng nên bài toán vô nghiệm', 'hàm mục tiêu không lồi nên KKT mất hiệu lực', 'nhân tử Lagrange bằng 0 tại mọi điểm'])
F_(r'Hình (a) của slide tr.48', 'ràng buộc suy biến (gradient phụ thuộc tuyến tính)',
   ['miền khả thi quá lớn để bài toán có nghiệm', 'hàm mục tiêu tuyến tính nên nhân tử vô nghiệm', 'điểm z nằm trong miền nên Slater thỏa'])
F_(r'Định lý “cần và đủ” của slide tr.50', r'bài toán lồi, Slater và \(x^*\) khả thi',
   [r'chỉ cần \(x^*\) khả thi, không cần lồi', r'chỉ cần f khả vi tại điểm \(x^*\)', r'bài toán không lồi và các nhân tử dương'])
F_(r'Slide tr.56 chú ý điều gì', 'điểm KKT có thể không là cực tiểu địa phương',
   ['điểm KKT luôn luôn là điểm cực đại', 'bài toán không lồi không có điểm KKT nào', 'mọi nhân tử đều phải âm ở bài toán không lồi'])
F_(r'Câu hỏi thảo luận 3', r'f lồi chặt trên tập chấp nhận được',
   [r'f là hàm tuyến tính trên tập chấp nhận được', r'tập chấp nhận được C là tập rỗng', r'tập chấp nhận được C bị chặn và đóng'])
F_(r'Câu hỏi thảo luận 4', 'không: hai nghiệm phân biệt kéo theo vô số nghiệm',
   ['có, luôn có đúng hai nghiệm khi f khả vi', 'có, nếu miền chấp nhận được không lồi', 'không, bài lồi luôn có nghiệm duy nhất'])
F_(r'Vì sao có thể chắc chắn Ví dụ 3', r'f liên tục trên tập compact (Weierstrass)',
   [r'vì f là hàm lồi trên miền chấp nhận được', r'vì điều kiện Slater được thỏa mãn', r'vì hệ KKT có nghiệm hữu hạn'])
F_(r'Với \(f=xy\) và \((t,-t)\)', r'\(-t^2<0=f(0,0)\)', [r'\(t^2>0=f(0,0)\)', r'\(0=f(0,0)\) với mọi \(t\)', r'\(2t>0\) khi \(t>0\)'])
F_(r'Trong bài tập C9 và C10', 'kiểm tra bài toán lồi và điều kiện Slater',
   ['tính Hessian của hàm Lagrange tại nghiệm', 'chuyển sang bài toán đối ngẫu Lagrange', 'đặt mọi nhân tử bằng một hằng số'])
F_(r'Trong bài toán lồi thỏa Slater, điểm KKT', r'\(g_i\) chặt và “có giá” (nới lỏng sẽ giảm f)',
   [r'\(g_i\) lỏng hoàn toàn tại điểm \(x^*\)', r'f đạt giá trị cực đại tại \(x^*\)', r'bài toán không có nghiệm tối ưu'])

# =====================================================================  G. MỆNH ĐỀ SAI THƯỜNG GẶP + BỔ SUNG
G = 'G. Mệnh đề dễ nhầm'
tf('G', r(47), r'Điều kiện Slater chỉ đòi hỏi tồn tại điểm khả thi z với \(g_i(z)\le0\) (bất đẳng thức không chặt).', False, r'Slater đòi <b>bất đẳng thức chặt</b> \(g_i(z)<0\) (slide tr.47). Với \(\le0\) thì mọi điểm khả thi đều thỏa, điều kiện trở nên vô nghĩa.', G)
tf('G', r(50), r'Với bài toán lồi thỏa Slater, KKT chỉ là điều kiện cần chứ không đủ để kết luận tối ưu.', False, r'Slide tr.50: điều kiện <b>cần và đủ</b>.', G)
tf('G', r(50), r'Với bài toán không lồi, điều kiện Slater vẫn bảo đảm mọi điểm KKT là cực tiểu toàn cục.', False, r'Slater chỉ hữu ích cho bài toán lồi. Ví dụ 3 (\(\min xy\) trên đĩa) có Slater thỏa (điểm \((0,0)\)) nhưng \((0,0)\) là KKT không tối ưu.', G)
tf('G', r(40), r'Nhân tử \(\lambda_i\) của ràng buộc bất đẳng thức \(g_i\le0\) có thể âm tại một điểm KKT.', False, r'Slide tr.40: \(\lambda_i\ge0\ \forall i\in I\). Chỉ \(\mu_j\) mới tùy ý dấu.', G)
tf('G', r(43), r'Nếu \(\lambda_i=0\) thì ràng buộc \(g_i\) chắc chắn lỏng (\(g_i(x^*)<0\)).', False, r'Điều kiện bù \(\lambda_ig_i=0\) cho phép \(\lambda_i=0\) khi \(g_i\) chặt (Ví dụ 1).', G)
tf('G', r(60), r'Trong Ví dụ 3, điểm \((1,1)\) là điểm KKT hợp lệ với \(\lambda=1/2\).', False, r'Tại \((1,1)\): \(\lambda=-1/2<0\), loại (slide tr.60).', G)
tf('G', r(55), r'Trong Ví dụ 1, nhân tử ứng với nghiệm là \((\lambda,\mu)=(1,0)\).', False, r'Slide tr.55: \((\lambda,\mu)=(0,1)\). Kiểm: \(2(x-1)+\lambda+\mu=-1+0+1=0\).', G)
tf('G', r(61), r'Trong Ví dụ 4, các nhân tử của ràng buộc \(x\ge0\), \(y\ge0\) tại nghiệm là âm.', False, r'\(\lambda_3=2\), \(\lambda_4=1\) đều dương.', G)
tf('G', r(37), r'Tập chấp nhận được C của bài toán (P) luôn khác rỗng.', False, r'C có thể rỗng (ví dụ \(x^2+y^2\le1\) và \(x+y\ge2\)); khi đó bài toán vô nghiệm.', G)
tf('G', r(66), r'Bài toán tối ưu lồi luôn có nghiệm duy nhất.', False, r'LP có thể có cả một cạnh nghiệm; nghiệm duy nhất cần thêm giả thiết (ví dụ f lồi chặt).', G)
tf('G', r(24), r'Bình phương tối thiểu \(\min\|Ax-b\|^2\) không phải bài toán lồi.', False, r'Hessian \(2A^\top A\succeq0\) ⇒ lồi (slide tr.24).', G)
tf('G', r(43), r'Tại mọi điểm KKT, các ràng buộc bất đẳng thức đều chặt.', False, r'Các ràng buộc lỏng có \(\lambda=0\). Có điểm KKT nằm hoàn toàn trong miền (ví dụ \((0,0)\) trong Ví dụ 3).', G)
tf('G', r(16), r'Ràng buộc đẳng thức phi tuyến, ví dụ \(x^2+y^2=1\), có thể xuất hiện trong bài toán tối ưu lồi dạng chuẩn.', False, r'\(h\) phải affine; đường tròn không lồi.', G)
tf('G', r(38), r'Nếu ràng buộc đổi từ \(g\le0\) sang \(-g\ge0\) thì cùng một nhân tử \(\lambda\ge0\) vẫn dùng được trong \(L=f+\lambda g\).', False, r'Sau khi đổi dấu, ta phải viết lại thành \(g\le0\) hoặc đổi dấu nhân tử, nếu không hệ KKT sai dấu.', G)

# bổ sung MCQ/num thiết thực (biên soạn thêm khi cần)
mc('S', r(40), r'Bài toán \(\min x_1^2+x_2^2\) s.t. \(x_1+x_2\ge2\). Chuẩn hóa \(g\le0\) và nhân tử tại nghiệm \((1,1)\) là',
   r'\(g=2-x_1-x_2\le0\), \(\lambda=2\)', [r'\(g=x_1+x_2-2\le0\), \(\lambda=2\)', r'\(g=2-x_1-x_2\le0\), \(\lambda=-2\)', r'\(g=x_1+x_2-2\le0\), \(\lambda=-2\)'],
   r'\(\nabla f=(2,2)\), \(\nabla g=(-1,-1)\): \((2,2)+\lambda(-1,-1)=0\Rightarrow\lambda=2\ge0\).', F)
mc('S', r(40), r'Cho \(\min x^2\) s.t. \(x\ge1\). Tại \(x^*=1\), điều kiện bù \(\lambda g(x^*)=0\) được thỏa vì',
   r'\(g(1)=1-1=0\) (ràng buộc chặt)', [r'\(\lambda=0\)', r'\(f(1)=1\)', r'\(\nabla f(1)=0\)'],
   r'Tại \(x^*=1\) ràng buộc chặt nên tích \(\lambda g=0\) tự động dù \(\lambda=2>0\). Nếu \(\lambda=0\) thì dừng \(2x=0\) sai.', F)
mc('S', r(50), r'Cho bài toán lồi thỏa Slater và điểm \(x^*\) thỏa hệ KKT với \(\lambda_1>0\). Nếu ta thay ràng buộc 1 bởi \(g_1\le-0.01\) (chặt hơn), giá trị tối ưu',
   r'không giảm (thường tăng vì miền hẹp hơn)', [r'chắc chắn giảm đi \(0.01\lambda_1\)', r'không đổi vì nhân tử không đo được độ nhạy', r'luôn bằng 0'],
   r'Thu hẹp miền chỉ có thể làm giá trị tối ưu tăng hoặc giữ nguyên: xấp xỉ \(f^*+0.01\lambda_1\) (nhân tử = độ nhạy, Boyd 5.6).', F)
mc('S', r(38), r'Ràng buộc đẳng thức \(x_1+x_2=1\) trong hàm Lagrange được viết thành',
   r'\(\mu(x_1+x_2-1)\) với \(\mu\in\mathbb R\)', [r'\(\lambda(x_1+x_2-1)\) với \(\lambda\ge0\)', r'\(\mu(x_1+x_2)\) không có hằng số', r'\(\mu\cdot1\) chỉ khi \(x_1=x_2\)'],
   r'Ràng buộc đẳng thức \(h=0\) với \(h=x_1+x_2-1\) đi kèm \(\mu h\) và \(\mu\) tùy ý dấu.', F)
mc('S', r(56), r'Bài toán không lồi có điểm KKT \(x^*\). Để kết luận x* là cực tiểu địa phương ta thường cần thêm',
   'điều kiện bậc hai (Hessian của L dương trên không gian tiếp tuyến)', ['điều kiện Slater', 'điều kiện \\(\\lambda=0\\)', 'điều kiện f tuyến tính'],
   r'Điều kiện đủ bậc hai (SOSC) là công cụ cho bài không lồi; Module 3 dùng \(Z^\top QZ\succ0\) (Hessian rút gọn) cho QP.', F)
num('S', r(57), r'Ví dụ 2 dạng cực tiểu \(f=x^2+y^2+4x-6y\) trên miền của slide: giá trị tối ưu \(f^*\) là', -8,
    r'Điểm KKT \((0,2)\): \(0+4+0-12=-8\) (kiểm bằng SLSQP: ' + str(R['m2_ex2_min_variant_num'][1]) + ').', ans_text='-8', grp=F)
num('S', r(57), r'Ví dụ 2 dạng cực tiểu: nhân tử \(\lambda_2\) của ràng buộc \(-2x+y\le2\) tại \((0,2)\) là', 2,
    r'\(\nabla f=(2x+4,2y-6)=(4,-2)\), \(\nabla g_2=(-2,1)\): \((4,-2)+\lambda_2(-2,1)=0\Rightarrow\lambda_2=2\).', ans_text='2', grp=F)
num('S', 'case study', r'Danh mục đầu tư: nếu bỏ ràng buộc \(w\ge0\), tỉ trọng tài sản 2 tính từ \(w\propto\Sigma^{-1}\mathbf1\) là (làm tròn 4 chữ số)', float(c_m2.w_un[1]),
    r'\(w_2=' + ('%.4f' % c_m2.w_un[1]) + r'\) — quá lớn và hai tỉ trọng kia âm, cho thấy cần ràng buộc \(w\ge0\).', tol=1e-3, ans_text=('%.4f' % c_m2.w_un[1]), grp=F)
essay('S', r(43), r'Giải \(\min x^2+y^2\) s.t. \(x+y\ge2\): chuẩn hóa, kiểm Slater, viết KKT và giải.',
      r'<p>Chuẩn hóa: \(g=2-x-y\le0\) (affine); f lồi ⇒ bài toán lồi; Slater: \((2,2)\) có \(g=-2<0\).</p><p>\(L=x^2+y^2+\lambda(2-x-y)\); dừng \(2x-\lambda=0\), \(2y-\lambda=0\) ⇒ \(x=y=\lambda/2\). Nếu \(\lambda=0\): \((0,0)\), vi phạm \(g\le0\). Vậy \(g=0\): \(x+y=2\Rightarrow x=y=1\), \(\lambda=2\ge0\) ✓. Nghiệm \((1,1)\), \(f^*=2\).</p>',
      ['Chuẩn hóa \\(g\\le0\\)', 'Kiểm Slater', 'Chia hai trường hợp \\(\\lambda=0\\) và \\(g=0\\)'], F)
