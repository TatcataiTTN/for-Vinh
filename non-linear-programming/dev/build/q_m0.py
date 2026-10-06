"""Ngân hàng câu hỏi Module 0 — Kiến thức tiên quyết. Module này không có slide chính khóa riêng:
câu hỏi dựa trên (T) Chương 1 BTDOC và các bài Studocu — chỉ tham khảo, đã kiểm bằng code; (G) các định nghĩa trong slide 2 nhắc lại;
(S) biên soạn thêm cho kiến thức nền chuẩn (đại số tuyến tính, giải tích) vì không có tài liệu gốc trong thư mục Slides."""
import numpy as np
from qlib import Bank
from helpers import R

bank = Bank('m0')
mc, tf, num, essay = bank.mc, bank.tf, bank.num, bank.essay
BT = 'BTDOC Ch.1 (tham khảo)'
SL = 'Studocu (tham khảo)'
inv = R['m0_btdoc_inv']; cram = R['m0_btdoc_cramer']; plan = R['m0_btdoc_plan']; four = R['m0_btdoc_4prod']

# =====================================================================  A. NGÔN NGỮ TỐI ƯU
A = 'A. Ngôn ngữ của bài toán tối ưu'
mc('T', BT, r'Trong bài toán tối ưu \(\max/\min f(x)\) với các ràng buộc, hàm \(f(x)\) được gọi là',
   'hàm mục tiêu', ['hàm ràng buộc', 'hàm phạt', 'hàm nhân tử'],
   r'BTDOC (mục I.3): “f(x) gọi là hàm mục tiêu; các hàm \(g_i(x)\) là hàm ràng buộc”.', A)
mc('T', BT, r'Tập hợp các điểm x thỏa mọi ràng buộc của bài toán tối ưu được gọi là',
   'miền ràng buộc (tập chấp nhận được)', ['miền giá trị của hàm mục tiêu', 'tập nghiệm tối ưu', 'tập điểm dừng'],
   r'Mỗi điểm thuộc miền ràng buộc gọi là một <b>phương án</b>; phương án làm f đạt max/min gọi là <b>phương án tối ưu</b>.', A)
mc('T', BT, r'Phương án \(x^*\) của bài toán min được gọi là phương án tối ưu nếu',
   r'\(f(x^*)\le f(x)\) với mọi phương án \(x\)', [r'\(f(x^*)\ge f(x)\) với mọi phương án x', r'\(\nabla f(x^*)=0\) và \(f(x^*)=0\)', r'\(x^*\) nằm trên biên miền ràng buộc'],
   r'Bài toán min: giá trị tại \(x^*\) nhỏ nhất trong mọi phương án. Chiều “≥” là bài toán max.', A)
mc('T', BT, r'“Quy hoạch phi tuyến” được BTDOC định nghĩa là bài toán mà',
   'hàm mục tiêu hoặc ít nhất một ràng buộc là phi tuyến', ['chỉ hàm mục tiêu là hàm bậc hai', 'mọi biến nhận giá trị nguyên', 'miền ràng buộc là tập rời rạc'],
   r'Nếu cả f và các \(g_i\) đều tuyến tính thì là quy hoạch tuyến tính; nếu biến nguyên thì là quy hoạch rời rạc/nguyên.', A)
mc('T', BT, r'Quy hoạch mà biến chỉ nhận giá trị 0 hoặc 1 được gọi là',
   'quy hoạch Boole (nhị phân)', ['quy hoạch tuyến tính liên tục', 'quy hoạch động', 'quy hoạch đa mục tiêu'],
   r'Trường hợp riêng của quy hoạch nguyên (BTDOC I.4).', A)
mc('T', BT, r'Quy hoạch đa mục tiêu là bài toán trong đó',
   'cùng một miền ràng buộc xét đồng thời nhiều hàm mục tiêu', ['có nhiều miền ràng buộc rời nhau', 'hàm mục tiêu có nhiều biến nguyên', 'các hệ số phụ thuộc tham số'],
   r'Ví dụ cân nhắc đồng thời lợi nhuận, việc làm và mức đầu tư (BTDOC).', A)
mc('T', BT, r'Quy hoạch tham số là bài toán mà',
   'các hệ số của hàm mục tiêu và ràng buộc phụ thuộc vào tham số', ['biến chỉ nhận giá trị nguyên', 'bài toán chia thành nhiều giai đoạn', 'chỉ có ràng buộc đẳng thức'],
   r'Phân loại theo BTDOC I.4.', A)
mc('T', BT, r'Quy hoạch động dùng khi đối tượng xét là',
   'quá trình nhiều giai đoạn hoặc phát triển theo thời gian', ['bài toán chỉ có một biến', 'hàm mục tiêu bậc hai', 'miền ràng buộc là đa diện lồi'],
   r'BTDOC I.4. Ví dụ ba lô 0–1 và bài toán tồn kho nhiều kỳ giải bằng quy hoạch động.', A)
mc('T', BT, r'Phương pháp tổng quát nhất nhưng chậm để giải một bài toán tối ưu có hữu hạn phương án là',
   'phương pháp duyệt toàn bộ (vét cạn)', ['phương pháp đơn hình', 'phương pháp gradient', 'phương pháp Newton'],
   r'BTDOC: tính f trên mọi phương án rồi so sánh. Chỉ khả thi khi số phương án nhỏ.', A)
mc('S', r'nền tảng', r'Cực tiểu địa phương \(x^*\) của f trên C là điểm mà',
   r'tồn tại \(\varepsilon>0\): \(f(x^*)\le f(x)\) với mọi \(x\in C\), \(\|x-x^*\|<\varepsilon\)', [r'\(f(x^*)\le f(x)\) với mọi \(x\in C\)', r'\(\nabla f(x^*)=0\) với mọi hướng d', r'\(f(x^*)=0\) và \(x^*\in C\)'],
   r'Địa phương chỉ so sánh với các điểm lân cận; toàn cục so sánh với mọi \(x\in C\).', A)
mc('S', 'nền tảng', r'Hàm \(f(x)=x^3-3x\) trên \(\mathbb R\) có',
   r'cực tiểu địa phương tại \(x=1\) nhưng không có cực tiểu toàn cục', [r'cực tiểu toàn cục tại \(x=1\)', r'cực tiểu toàn cục tại \(x=-1\)', r'không có cực trị địa phương nào'],
   r'\(f^{\prime}(x)=3x^2-3=0\Rightarrow x=\pm1\); \(f^{\prime\prime}(1)=6>0\) (cực tiểu địa phương, \(f=-2\)); nhưng \(f\to-\infty\) khi \(x\to-\infty\) nên không có cực tiểu toàn cục.', A)
tf('S', 'nền tảng', r'Mọi cực tiểu toàn cục đều là cực tiểu địa phương.', True, r'Nếu \(f(x^*)\le f(x)\) với mọi \(x\in C\) thì đúng với mọi x lân cận.', A)
tf('S', 'nền tảng', r'Mọi cực tiểu địa phương đều là cực tiểu toàn cục.', False, r'Chỉ đúng với bài toán lồi. Ví dụ \(x^3-3x\) có cực tiểu địa phương tại \(x=1\) nhưng không toàn cục.', A)
tf('S', 'nền tảng', r'Bài toán \(\max f(x)\) tương đương với bài toán \(\min(-f(x))\) trên cùng miền.', True, r'Tập nghiệm giống nhau; giá trị tối ưu đổi dấu.', A)
tf('G', 'slide 2 · tr.8', r'Dạng chuẩn của bài toán phi tuyến trong slide dùng ràng buộc bất đẳng thức \(g_i(x)\le0\) và đẳng thức \(h_j(x)=0\).', True, r'Slide 2, tr.8. Dạng \(g\ge0\) phải đổi thành \(-g\le0\).', A)
tf('S', 'nền tảng', r'Nếu miền chấp nhận được rỗng thì giá trị tối ưu của bài toán min được quy ước là \(+\infty\).', True, r'Infimum của tập rỗng là \(+\infty\) (slide 3, tr.23).', A)
tf('S', 'nền tảng', r'Tập chấp nhận được của bài toán tối ưu luôn khác rỗng.', False, r'Ví dụ \(x^2+y^2\le1\) và \(x+y\ge2\) không có điểm chung (bài toán vô nghiệm).', A)
tf('S', 'nền tảng', r'Quy hoạch tuyến tính là trường hợp riêng của quy hoạch toàn phương.', True, r'\(Q=0\) (Module 3).', A)
tf('S', 'nền tảng', r'Bài toán ba lô (knapsack) với biến nhị phân là bài toán tối ưu liên tục.', False, r'Biến nhị phân ⇒ miền rời rạc: quy hoạch nguyên/Boole (Studocu C13–C15 dùng quy hoạch động).', A)
mc('T', SL, r'Trong lĩnh vực tối ưu hóa, bài toán Knapsack được định nghĩa là',
   'bài toán chọn các món đồ vào túi có giới hạn trọng lượng để tối đa giá trị', ['bài toán tìm đường đi ngắn nhất giữa hai điểm trên đồ thị', 'bài toán tối ưu hóa hàm lồi có nhiều biến', 'bài toán phân loại đối tượng vào các lớp đã cho'],
   r'Knapsack 0–1: chọn tập vật có tổng khối lượng \(\le W\) sao cho tổng giá trị lớn nhất. (Đề Studocu, chỉ tham khảo.)', A)
mc('S', 'nền tảng', r'Lớp bài toán nào sau đây là lớp bao hàm hẹp nhất (nhỏ nhất) trong các lớp còn lại?',
   'quy hoạch tuyến tính', ['quy hoạch toàn phương lồi', 'tối ưu lồi', 'quy hoạch phi tuyến tổng quát'],
   r'LP ⊂ QP lồi ⊂ tối ưu lồi ⊂ phi tuyến (slide 2, tr.24, tr.67–68).', A)
num('S', 'nền tảng', r'Một bài toán có 4 biến, 3 ràng buộc bất đẳng thức và 2 ràng buộc đẳng thức. Số nhân tử Lagrange (tổng) là', 5, r'Mỗi ràng buộc một nhân tử: \(3+2=5\).', ans_text='5', grp=A)
essay('T', BT, r'Trình bày dạng tổng quát của bài toán tối ưu và phân biệt: hàm mục tiêu, ràng buộc, phương án, phương án tối ưu, giá trị tối ưu.',
      r'<p>Bài toán: \(f(x)\to\max(\min)\) với \(g_i(x)\ (\le,=,\ge)\ b_i\), \(x\in X\subseteq\mathbb R^n\). \(f\): hàm mục tiêu; \(g_i\): hàm ràng buộc; miền ràng buộc \(D=\{x\in X:g_i(x)\dots b_i\}\); mỗi \(x\in D\) là một phương án; \(x^*\in D\) với \(f(x^*)\ge f(x)\ \forall x\in D\) (max) hay \(\le\) (min) là phương án tối ưu; \(f(x^*)\) là giá trị tối ưu.</p>',
      ['Nêu đủ 5 khái niệm', 'Phân biệt max/min'], A)

# =====================================================================  B. ĐẠI SỐ TUYẾN TÍNH
B = 'B. Đại số tuyến tính'
mc('S', 'nền tảng', r'Tích vô hướng của \(u=(1,2,3)\) và \(v=(4,-5,6)\) bằng',
   '12', ['32', '-6', '4'], r'\(1\cdot4+2\cdot(-5)+3\cdot6=4-10+18=12\).', B)
num('S', 'nền tảng', r'Tính \(\|v\|\) với \(v=(2,3,6)\).', 7, r'\(\sqrt{4+9+36}=\sqrt{49}=7\).', ans_text='7', grp=B)
mc('S', 'nền tảng', r'Bất đẳng thức Cauchy–Schwarz nói',
   r'\(|u^\top v|\le\|u\|\,\|v\|\)', [r'\(|u^\top v|\ge\|u\|\,\|v\|\)', r'\(\|u+v\|=\|u\|+\|v\|\) với mọi u, v', r'\(u^\top v\le\|u\|+\|v\|\)'],
   r'Vì \(u^\top v=\|u\|\|v\|\cos\theta\) và \(|\cos\theta|\le1\). Dấu bằng khi u, v song song.', B)
num('S', 'nền tảng', r'Với \(u=(1,2,2)\), \(v=(2,3,6)\): tính \(\|u\|\|v\|-u^\top v\).', 1, r'\(\|u\|=3\), \(\|v\|=7\), \(u^\top v=20\): \(21-20=1\ge0\).', ans_text='1', grp=B)
mc('S', 'nền tảng', r'Khẳng định nào về tích ma trận là ĐÚNG?',
   r'\((AB)^\top=B^\top A^\top\)', [r'\((AB)^\top=A^\top B^\top\)', r'\(AB=BA\) với mọi A, B vuông cùng cỡ', r'\((AB)^{-1}=A^{-1}B^{-1}\) khi cả hai khả nghịch'],
   r'Chuyển vị (và nghịch đảo) của tích đảo thứ tự: \((AB)^\top=B^\top A^\top\), \((AB)^{-1}=B^{-1}A^{-1}\).', B)
mc('S', 'nền tảng', r'Với \(A=\begin{pmatrix}1&2\\3&4\end{pmatrix}\), \(B=\begin{pmatrix}0&1\\1&1\end{pmatrix}\), tích AB là',
   r'\(\begin{pmatrix}2&3\\4&7\end{pmatrix}\)', [r'\(\begin{pmatrix}3&4\\1&3\end{pmatrix}\)', r'\(\begin{pmatrix}0&2\\3&4\end{pmatrix}\)', r'\(\begin{pmatrix}2&4\\3&7\end{pmatrix}\)'],
   r'Dòng 1: \((1\cdot0+2\cdot1,\ 1\cdot1+2\cdot1)=(2,3)\); dòng 2: \((3\cdot0+4\cdot1,\ 3\cdot1+4\cdot1)=(4,7)\). Phương án cuối là \((AB)^\top\).', B)
tf('S', 'nền tảng', r'Với hai ma trận vuông cùng cỡ luôn có \(AB=BA\).', False, r'Phép nhân ma trận không giao hoán nói chung.', B)
tf('S', 'nền tảng', r'Ma trận A khả nghịch khi và chỉ khi \(\det A\ne0\).', True, r'Ma trận không suy biến; BTDOC 2.3: “Ma trận vuông A được gọi là không suy biến nếu nó có định thức khác 0”.', B)
mc('T', BT, r'Tính chất nào của định thức sau đây ĐÚNG?',
   'đổi chỗ hai hàng thì định thức đổi dấu', ['đổi chỗ hai hàng thì định thức không đổi', 'nhân một hàng với k thì định thức không đổi', 'cộng hai hàng vào nhau thì định thức nhân đôi'],
   r'BTDOC 2.2: đổi hai hàng ⇒ đổi dấu; cộng bội của một hàng vào hàng khác ⇒ không đổi; thừa số chung của một hàng đưa ra ngoài.', B)
mc('T', BT, r'Nếu các phần tử của một hàng tỷ lệ với các phần tử tương ứng của hàng khác thì định thức',
   'bằng 0', ['bằng 1', 'bằng tích các phần tử đường chéo', 'không xác định'],
   r'Hai hàng phụ thuộc tuyến tính ⇒ ma trận suy biến ⇒ \(\det=0\). (BTDOC 2.2)', B)
num('T', BT, r'Tính định thức của \(\begin{pmatrix}1&2\\3&4\end{pmatrix}\).', -2, r'\(1\cdot4-2\cdot3=-2\) (BTDOC dùng ví dụ này).', ans_text='-2', grp=B)
num('T', BT, r'Tính định thức của \(A=\begin{pmatrix}1&2&3\\2&5&3\\1&0&8\end{pmatrix}\) (BTDOC).', inv['det'],
    r'\(1(40-0)-2(16-3)+3(0-5)=40-26-15=-1\) (code: ' + str(inv['det']) + ').', ans_text='-1', grp=B)
mc('T', BT, r'Ma trận nghịch đảo của \(A=\begin{pmatrix}1&2&3\\2&5&3\\1&0&8\end{pmatrix}\) là',
   r'\(\begin{pmatrix}-40&16&9\\13&-5&-3\\5&-2&-1\end{pmatrix}\)', [r'\(\begin{pmatrix}40&-16&-9\\-13&5&3\\-5&2&1\end{pmatrix}\)', r'\(\begin{pmatrix}-40&13&5\\16&-5&-2\\9&-3&-1\end{pmatrix}\)', r'\(\begin{pmatrix}40&13&5\\16&5&2\\9&3&1\end{pmatrix}\)'],
   r'\(\det A=-1\), nên \(A^{-1}=-[A_{ji}]\). Phương án 2 quên dấu \(-1/\det\); phương án 3 quên chuyển vị ma trận phụ hợp. Code: \(A^{-1}A=I\).', B)
num('T', BT, r'Trong \(A^{-1}\) của ma trận ví dụ trên, phần tử dòng 2 cột 1 bằng', 13, r'\(A^{-1}=\begin{pmatrix}-40&16&9\\13&-5&-3\\5&-2&-1\end{pmatrix}\): \((A^{-1})_{21}=13\).', ans_text='13', grp=B)
mc('S', 'nền tảng', r'Nghịch đảo của \(A=\begin{pmatrix}2&5\\1&3\end{pmatrix}\) là',
   r'\(\begin{pmatrix}3&-5\\-1&2\end{pmatrix}\)', [r'\(\begin{pmatrix}3&5\\1&2\end{pmatrix}\)', r'\(\begin{pmatrix}2&-5\\-1&3\end{pmatrix}\)', r'\(\begin{pmatrix}-3&5\\1&-2\end{pmatrix}\)'],
   r'\(\det=6-5=1\); \(A^{-1}=\dfrac1{1}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}=\begin{pmatrix}3&-5\\-1&2\end{pmatrix}\).', B)
mc('T', BT, r'Hệ phương trình tuyến tính “xác định” theo BTDOC là hệ',
   'chỉ có một nghiệm duy nhất', ['không có nghiệm nào', 'có nhiều hơn một nghiệm', 'có tất cả hệ số vế phải bằng 0'],
   r'Không tương thích: vô nghiệm; bất định: quá một nghiệm; thuần nhất: mọi \(b_i=0\).', B)
mc('T', BT, r'Hệ \(Ax=b\) (A vuông khả nghịch) có nghiệm duy nhất được tính bằng',
   r'\(x=A^{-1}b\) (công thức Cramer cho từng thành phần)', [r'\(x=b^\top A^{-1}\)', r'\(x=Ab\)', r'\(x=A^\top b/\det A^\top\)'],
   r'Nhân hai vế với \(A^{-1}\): \(A^{-1}Ax=A^{-1}b\Rightarrow x=A^{-1}b\).', B)
mc('T', BT, r'Hệ \(x_1+2x_3=6,\ 3x_1+4x_2+6x_3=30,\ -x_1-2x_2+3x_3=8\) có nghiệm',
   r'\(x=(-2,3,4)\)', [r'\(x=(2,3,4)\)', r'\(x=(-2,4,3)\)', r'\(x=(6,5,0)\)'],
   r'\(\det A=20\); thay: \(-2+8=6\), \(-6+12+24=30\), \(2-6+12=8\) ✓ (code: ' + str(cram['x']) + ').', B)
num('T', BT, r'Trong hệ trên, giá trị \(x_3\) là', 4, r'\(x=(-2,3,4)\) (kiểm bằng phương trình 1: \(x_1+2x_3=6\Rightarrow-2+8=6\)).', ans_text='4', grp=B)
mc('S', 'nền tảng', r'Giá trị riêng của \(A=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\) là',
   '1 và 3', ['2 và 2', '0 và 4', '1 và 2'], r'\((2-\lambda)^2-1=0\Rightarrow\lambda=1,3\); vết 4, định thức 3.', B)
num('S', 'nền tảng', r'Tổng các giá trị riêng của \(\begin{pmatrix}4&1\\1&3\end{pmatrix}\) bằng', 7, r'Tổng giá trị riêng \(=\) vết \(=4+3=7\); (giá trị riêng \(2.382,4.618\)).', ans_text='7', grp=B)
num('S', 'nền tảng', r'Tích các giá trị riêng của \(\begin{pmatrix}4&1\\1&3\end{pmatrix}\) bằng', 11, r'Tích \(=\det=12-1=11\).', ans_text='11', grp=B)
mc('S', 'nền tảng', r'Ma trận đối xứng thực luôn có',
   'mọi giá trị riêng là số thực', ['ít nhất một giá trị riêng bằng 0', 'giá trị riêng phức không thực', 'các giá trị riêng đều dương'],
   r'Định lý phổ cho ma trận đối xứng thực: giá trị riêng thực và chéo hóa trực giao.', B)
tf('S', 'nền tảng', r'Định thức của ma trận bằng tích các giá trị riêng của nó.', True, r'\(\det A=\prod\lambda_i\), \(\mathrm{tr}A=\sum\lambda_i\).', B)
tf('S', 'nền tảng', r'Nếu \(\det A=0\) thì A có ít nhất một giá trị riêng bằng 0.', True, r'\(\prod\lambda_i=0\).', B)
mc('S', 'nền tảng', r'Ma trận đối xứng A gọi là xác định dương khi',
   r'\(x^\top Ax>0\) với mọi \(x\ne0\)', [r'\(\det A>0\)', r'các phần tử của A đều dương', r'A có ít nhất một giá trị riêng dương'],
   r'Tiêu chuẩn tương đương: mọi giá trị riêng dương. Định thức dương hoặc phần tử dương chưa đủ.', B)
tf('S', 'nền tảng', r'Ma trận đối xứng \(\begin{pmatrix}1&2\\2&1\end{pmatrix}\) là xác định dương.', False, r'Giá trị riêng \(3\) và \(-1\): không xác định dương.', B)
tf('S', 'nền tảng', r'Với ma trận vuông A, \(\det(A^\top)=\det A\).', True, r'Tính chất BTDOC: định thức không đổi khi thay hàng thành cột.', B)
tf('S', 'nền tảng', r'Nếu A khả nghịch thì \(\det(A^{-1})=1/\det A\).', True, r'Vì \(\det(AA^{-1})=\det I=1\).', B)
mc('S', 'nền tảng', r'Hạng (rank) của ma trận là',
   'số hàng (cột) độc lập tuyến tính tối đa', ['số phần tử khác 0', 'tổng các phần tử đường chéo', 'định thức của nó'],
   r'Hệ \(Ax=b\) tương thích ⇔ \(\mathrm{rank}A=\mathrm{rank}[A|b]\).', B)
essay('T', BT, r'Tính \(A^{-1}\) cho \(A=\begin{pmatrix}1&2&3\\2&5&3\\1&0&8\end{pmatrix}\) bằng ma trận phụ hợp và kiểm tra bằng \(AA^{-1}=I\).',
      r'<p>\(\det A=-1\). Cofactor: \(A_{11}=40,A_{12}=-13,A_{13}=-5,A_{21}=-16,A_{22}=5,A_{23}=2,A_{31}=-9,A_{32}=3,A_{33}=1\). \(A^{-1}=\dfrac1{\det A}\begin{pmatrix}A_{11}&A_{21}&A_{31}\\A_{12}&A_{22}&A_{32}\\A_{13}&A_{23}&A_{33}\end{pmatrix}=-\begin{pmatrix}40&-16&-9\\-13&5&3\\-5&2&1\end{pmatrix}=\begin{pmatrix}-40&16&9\\13&-5&-3\\5&-2&-1\end{pmatrix}\). Kiểm: dòng 1 của \(A\) nhân cột 1 của \(A^{-1}\): \(-40+26+15=1\) ✓.</p>',
      ['Tính định thức', 'Cofactor và chuyển vị', 'Kiểm tra lại bằng nhân'], B)
essay('S', 'nền tảng', r'Chứng minh \(x^\top Ax=\tfrac12x^\top(A+A^\top)x\) và suy ra vì sao Hessian và ma trận của dạng toàn phương có thể giả sử đối xứng.',
      r'<p>\(x^\top Ax\in\mathbb R\) nên \(x^\top Ax=(x^\top Ax)^\top=x^\top A^\top x\). Cộng: \(2x^\top Ax=x^\top(A+A^\top)x\). Do đó thay A bởi \(\tfrac12(A+A^\top)\) không đổi dạng toàn phương. Hessian đối xứng vì đạo hàm hỗn hợp bằng nhau (Schwarz).</p>',
      ['Dùng số thực bằng chuyển vị', 'Kết luận'], B)

# =====================================================================  C. GIẢI TÍCH NHIỀU BIẾN
C = 'C. Giải tích nhiều biến'
mc('S', 'nền tảng', r'Gradient của \(f(x,y)=x^2y+3xy^2-2x\) là',
   r'\((2xy+3y^2-2,\ x^2+6xy)\)', [r'\((2xy+3y^2,\ x^2+6xy-2)\)', r'\((x^2+3y^2-2,\ 2xy+6xy)\)', r'\((2xy+3y^2-2,\ x^2+3xy)\)'],
   r'\(f_x=2xy+3y^2-2\), \(f_y=x^2+6xy\). Code: ' + str(R['m0_grad_ex']['grad']) + '.', C)
num('S', 'nền tảng', r'Với \(f=x^2y+3xy^2-2x\), tính \(f_x(1,2)\).', 14, r'\(2\cdot1\cdot2+3\cdot4-2=4+12-2=14\).', ans_text='14', grp=C)
num('S', 'nền tảng', r'Với \(f=x^2y+3xy^2-2x\), tính \(f_y(1,2)\).', 13, r'\(1+6\cdot1\cdot2=13\).', ans_text='13', grp=C)
num('S', 'nền tảng', r'Với \(f=x^2y+3xy^2-2x\), tính \(f_{xy}(1,2)\) (đạo hàm hỗn hợp).', 14, r'\(f_{xy}=2x+6y=2+12=14\) (bằng \(f_{yx}\)).', ans_text='14', grp=C)
mc('S', 'nền tảng', r'Hướng giảm nhanh nhất của f tại x là',
   r'\(-\nabla f(x)\)', [r'\(\nabla f(x)\)', r'\(\nabla^2f(x)\,x\)', r'hướng vuông góc với \(-\nabla f(x)\)'],
   r'\(\nabla f\) là hướng tăng nhanh nhất nên \(-\nabla f\) là giảm nhanh nhất; hướng vuông góc gradient là hướng dọc đường mức (f không đổi bậc nhất).', C)
mc('S', 'nền tảng', r'Gradient \(\nabla f(x)\) so với đường mức của f qua x',
   'vuông góc với đường mức', ['song song với đường mức', 'tạo góc 45° với đường mức', 'không có quan hệ cố định'],
   r'Dọc đường mức f không đổi, nên đạo hàm theo hướng tiếp tuyến bằng \(\nabla f^\top d=0\).', C)
tf('S', 'nền tảng', r'Nếu \(f\) có đạo hàm riêng cấp hai liên tục thì Hessian của nó đối xứng.', True, r'Định lý Schwarz.', C)
mc('S', 'nền tảng', r'Khai triển Taylor bậc hai của f tại x là',
   r'\(f(x+d)\approx f(x)+\nabla f(x)^\top d+\tfrac12d^\top\nabla^2f(x)d\)', [r'\(f(x+d)\approx f(x)+\tfrac12\nabla f(x)^\top d\)', r'\(f(x+d)\approx f(x)+d^\top\nabla^2f(x)d\)', r'\(f(x+d)\approx\nabla f(x)+\nabla^2f(x)d\)'],
   r'Bậc hai gồm số hạng bậc nhất (gradient) và bậc hai (Hessian, có hệ số 1/2).', C)
num('S', 'nền tảng', r'Xấp xỉ Taylor bậc hai của \(e^x+y^2\) tại gốc, tại điểm \((0.1,0.2)\), cho giá trị (làm tròn 3 chữ số thập phân)', 1.145, r'\(1+0.1+\tfrac12(0.01)+0.04=1.145\) (giá trị thật \(1.14517\)).', tol=1e-3, ans_text='1.145', grp=C)
mc('S', 'nền tảng', r'Điều kiện cần cấp 1 để \(x^*\) là cực tiểu địa phương của f khả vi (không ràng buộc) là',
   r'\(\nabla f(x^*)=0\)', [r'\(\nabla f(x^*)>0\)', r'\(f(x^*)=0\)', r'\(\nabla^2f(x^*)=0\)'],
   r'Điều kiện Fermat. (Studocu Q4 hỏi về dạng “điều kiện cần bậc nhất” trong tối ưu không ràng buộc — chỉ tham khảo.)', C)
mc('S', 'nền tảng', r'Điều kiện đủ cấp 2 để \(x^*\) là cực tiểu địa phương chặt là',
   r'\(\nabla f(x^*)=0\) và \(\nabla^2f(x^*)\succ0\)', [r'\(\nabla f(x^*)=0\) và \(\nabla^2f(x^*)\preceq0\)', r'\(\nabla f(x^*)=0\) và \(\nabla^2f(x^*)\) khả nghịch', r'\(\nabla^2f(x^*)\succ0\) nhưng \(\nabla f(x^*)\ne0\)'],
   r'Hessian phải xác định dương tại điểm dừng. Khả nghịch chưa đủ: \(\mathrm{diag}(1,-1)\) khả nghịch nhưng yên ngựa.', C)
mc('T', SL, r'Trong tối ưu không ràng buộc, điều kiện cần bậc nhất và bậc hai để \(x^*\) là cực tiểu địa phương là',
   r'\(\nabla f(x^*)=0\) và \(\nabla^2f(x^*)\succeq0\)', [r'\(\nabla f(x^*)\ne0\) và \(\nabla^2f(x^*)\succeq0\)', r'\(\nabla f(x^*)=0\) và \(\nabla^2f(x^*)\prec0\)', r'\(\nabla^2f(x^*)=0\) chỉ'],
   r'Đề Studocu Q12 (chỉ tham khảo) hỏi đúng ý này. Điều kiện cần cấp 2 là \(\succeq0\); đủ cấp 2 là \(\succ0\).', C)
mc('S', 'nền tảng', r'Với \(f=x^2+xy+y^2-3x\), điểm dừng là',
   r'\((2,-1)\)', [r'\((3,0)\)', r'\((1,-1)\)', r'\((0,0)\)'],
   r'\(\nabla f=(2x+y-3,\ x+2y)=0\Rightarrow x=-2y\Rightarrow-4y+y-3=0\Rightarrow y=-1,x=2\). Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\succ0\) ⇒ cực tiểu.', C)
num('S', 'nền tảng', r'Giá trị của \(f=x^2+xy+y^2-3x\) tại điểm dừng \((2,-1)\) là', -3, r'\(4-2+1-6=-3\).', ans_text='-3', grp=C)
mc('S', 'nền tảng', r'Với \(f=x^3-3x+y^2\), điểm \((-1,0)\) là',
   'điểm yên ngựa (Hessian \\(\\mathrm{diag}(-6,2)\\))', ['cực tiểu địa phương', 'cực đại địa phương', 'cực tiểu toàn cục'],
   r'\(\nabla f=(3x^2-3,2y)=0\) tại \((\pm1,0)\); \(H=\mathrm{diag}(6x,2)\). Tại \((-1,0)\) giá trị riêng \(-6,2\) trái dấu ⇒ yên ngựa.', C)
num('S', 'nền tảng', r'Với \(f=x^3-3x+y^2\), giá trị tại cực tiểu địa phương \((1,0)\) là', -2, r'\(1-3+0=-2\).', ans_text='-2', grp=C)
mc('S', 'nền tảng', r'Gradient descent có công thức cập nhật',
   r'\(x^{k+1}=x^k-t\nabla f(x^k)\)', [r'\(x^{k+1}=x^k+t\nabla f(x^k)\)', r'\(x^{k+1}=x^k-t\nabla^2f(x^k)\)', r'\(x^{k+1}=x^k/\|\nabla f(x^k)\|\)'],
   r'Đi ngược chiều gradient một quãng t (bước). Dấu “+” là gradient ascent.', C)
num('S', 'nền tảng', r'Với \(f=x^2+3y^2\), \(x^0=(-1.8,1.4)\), \(t=0.1\): tọa độ thứ hai \(y\) của \(x^1\) là', 0.56, r'\(\nabla f=(2x,6y)=(-3.6,8.4)\); \(x^1=(-1.8+0.36,\ 1.4-0.84)=(-1.44,0.56)\).', ans_text='0.56', grp=C)
tf('S', 'nền tảng', r'Với hàm \(f=x^2+3y^2\), gradient descent với bước \(t=0.5\) hội tụ.', False, r'Hằng số Lipschitz \(L=6\); cần \(t<2/L=1/3\). Với \(t=0.5\): \(y\) nhân \((1-3)=-2\) mỗi bước (phân kỳ).', C)
mc('T', SL, r'Trong tối ưu không ràng buộc, tìm kiếm chính xác theo tia (exact line search) dùng để',
   'tìm độ dài bước làm cực tiểu hàm mục tiêu dọc một hướng cho trước', ['kiểm tra tính lồi của hàm mục tiêu', 'xác định ma trận Hessian của hàm số', 'tìm hướng giảm nhanh nhất của hàm mục tiêu'],
   r'Đề Studocu Q4 (tham khảo): line search chọn \(t\) tối thiểu \(f(x+td)\) khi hướng d đã biết.', C)
mc('S', 'nền tảng', r'Hessian của \(f(x)=\tfrac12x^\top Qx+c^\top x\) (Q đối xứng) là',
   r'\(Q\) (hằng số theo x)', [r'\(Qx+c\)', r'\(c\)', r'\(Q^\top Q\)'],
   r'\(\nabla f=Qx+c\), \(\nabla^2f=Q\).', C)
mc('S', 'nền tảng', r'Đạo hàm của f theo hướng d tại x là',
   r'\(\nabla f(x)^\top d\)', [r'\(d^\top\nabla^2f(x)d\)', r'\(\nabla f(x)\,d^\top\)', r'\(\|\nabla f(x)\|\)'],
   r'Nếu \(\|d\|=1\) giá trị lớn nhất bằng \(\|\nabla f(x)\|\) khi d cùng hướng gradient.', C)
essay('S', 'nền tảng', r'Tìm và phân loại các điểm dừng của \(f(x,y)=x^3-3x+y^2\).',
      r'<p>\(\nabla f=(3x^2-3,\ 2y)=0\Rightarrow(x,y)=(1,0),(-1,0)\). \(\nabla^2f=\mathrm{diag}(6x,2)\). Tại \((1,0)\): \(\mathrm{diag}(6,2)\succ0\) ⇒ cực tiểu địa phương, \(f=-2\). Tại \((-1,0)\): \(\mathrm{diag}(-6,2)\) không xác định ⇒ điểm yên ngựa, \(f=2\). Hàm không có cực tiểu toàn cục vì \(f\to-\infty\) khi \(x\to-\infty\).</p>',
      ['Giải \\(\\nabla f=0\\)', 'Tính Hessian tại từng điểm', 'Kết luận theo giá trị riêng'], C)
essay('S', 'nền tảng', r'Viết khai triển Taylor bậc hai của \(f(x,y)=e^x+y^2\) tại gốc và so sánh với giá trị thật tại \((0.1,0.2)\).',
      r'<p>\(f(0,0)=1\), \(\nabla f=(e^x,2y)=(1,0)\), \(\nabla^2f=\mathrm{diag}(e^x,2)=\mathrm{diag}(1,2)\). Taylor: \(1+x+\tfrac12x^2+y^2\). Tại \((0.1,0.2)\): \(1.145\); thật \(e^{0.1}+0.04=1.14517\), sai số \(1.7\cdot10^{-4}\).</p>',
      ['Đủ ba đại lượng f, gradient, Hessian', 'So sánh số'], C)

# =====================================================================  D. TÔPÔ VÀ TỒN TẠI NGHIỆM
D = 'D. Tập, tôpô và tồn tại nghiệm'
mc('S', 'nền tảng', r'\(\inf\{e^x:x\in\mathbb R\}\) bằng',
   '0, nhưng không đạt được', ['1, đạt tại \\(x=0\\)', '\\(-\\infty\\)', '0, đạt tại \\(x=-\\infty\\)'],
   r'\(e^x>0\) nhưng \(\to0\) khi \(x\to-\infty\); không có x nào cho giá trị 0 nên infimum không đạt (không có min).', D)
mc('S', 'nền tảng', r'Hàm \(f(x)=1/x\) trên \((0,\infty)\) có',
   r'\(\inf f=0\) nhưng không có giá trị nhỏ nhất', [r'giá trị nhỏ nhất bằng 0 tại \(x=\infty\)', r'giá trị nhỏ nhất bằng 1 tại \(x=1\)', r'\(\inf f=-\infty\)'],
   r'\(1/x\to0\) khi \(x\to\infty\), không đạt.', D)
mc('S', 'nền tảng', r'Tập compact trong \(\mathbb R^n\) là tập',
   'đóng và bị chặn', ['mở và bị chặn', 'đóng và không bị chặn', 'lồi và mở'],
   r'Định lý Heine–Borel trong \(\mathbb R^n\).', D)
mc('S', 'nền tảng', r'Tập nào sau đây là compact?',
   r'đĩa \(\{x^2+y^2\le2\}\)', [r'\((0,1]\)', r'\([0,\infty)\)', r'\(\{x^2+y^2<2\}\)'],
   r'Đĩa đóng và bị chặn. \((0,1]\) không đóng; \([0,\infty)\) không bị chặn; đĩa mở không đóng.', D)
mc('S', 'nền tảng', r'Định lý Weierstrass: hàm liên tục trên tập compact khác rỗng',
   'đạt giá trị nhỏ nhất và lớn nhất trên tập đó', ['luôn có duy nhất một cực tiểu', 'luôn khả vi', 'luôn lồi'],
   r'Không cần lồi hay khả vi.', D)
tf('S', 'nền tảng', r'Hàm liên tục trên tập đóng (không bị chặn) luôn đạt cực tiểu.', False, r'Ví dụ \(e^x\) trên \(\mathbb R\) (đóng) không đạt inf. Cần thêm coercive.', D)
mc('S', 'nền tảng', r'Hàm f được gọi là coercive nếu',
   r'\(f(x)\to+\infty\) khi \(\|x\|\to\infty\)', [r'\(f(x)\to0\) khi \(\|x\|\to\infty\)', r'\(f\) bị chặn dưới trên \(\mathbb R^n\)', r'\(\nabla f(x)\to0\) khi \(\|x\|\to\infty\)'],
   r'Khi đó f liên tục trên tập đóng khác rỗng đạt cực tiểu.', D)
tf('S', 'nền tảng', r'Hàm \(x_1^2+x_2^2\) là coercive.', True, r'\(f=\|x\|^2\to\infty\).', D)
tf('S', 'nền tảng', r'Hàm \(e^x\) là coercive trên \(\mathbb R\).', False, r'\(e^x\to0\) khi \(x\to-\infty\).', D)
mc('S', 'nền tảng', r'\(\min xy\) trên đĩa \(x^2+y^2\le2\) chắc chắn có nghiệm vì',
   r'đĩa compact và \(xy\) liên tục (Weierstrass)', [r'\(xy\) là hàm lồi', r'đĩa có điểm trong', r'\(\nabla(xy)\ne0\)'],
   r'Weierstrass không đòi lồi. (Ví dụ 3 của slide 2.)', D)
mc('S', 'nền tảng', r'\(\min x_1^2+x_2^2\) s.t. \(x_1+x_2\ge2\) có nghiệm vì',
   r'f coercive và miền đóng khác rỗng', [r'miền bị chặn', r'f tuyến tính', r'miền có điểm trong bị chặn'],
   r'Miền \(\{x_1+x_2\ge2\}\) không bị chặn nhưng f coercive nên vẫn có nghiệm \((1,1)\).', D)
tf('S', 'nền tảng', r'\(\inf S\) luôn thuộc S.', False, r'Ví dụ \(\inf(0,1)=0\notin(0,1)\).', D)
tf('S', 'nền tảng', r'Polyhedron \(\{x\mid Ax\le b\}\) luôn là tập đóng.', True, r'Giao của các nửa không gian đóng.', D)
num('S', 'nền tảng', r'Giá trị \(\inf\{x_1:\ x_1x_2\ge1,\ x_1,x_2\ge0\}\) là', 0, r'\(x=(t,1/t)\), \(t\to0^+\): \(f\to0\) nhưng không đạt (Module 3, Frank–Wolfe).', ans_text='0', grp=D)
essay('S', 'nền tảng', r'Giải thích vì sao \(\min e^x\) trên \(\mathbb R\) không có nghiệm, và cho một điều kiện đủ để hàm liên tục có cực tiểu.',
      r'<p>\(e^x>0\) với mọi x và \(e^x\to0\) khi \(x\to-\infty\) nên \(\inf=0\) nhưng không tồn tại x với \(e^x=0\). Điều kiện đủ: tập chấp nhận được compact (Weierstrass), hoặc f coercive và miền đóng khác rỗng.</p>',
      ['Chỉ ra inf không đạt', 'Nêu Weierstrass hoặc coercive'], D)

# =====================================================================  E. ÔN QUY HOẠCH TUYẾN TÍNH
E = 'E. Ôn quy hoạch tuyến tính'
mc('T', BT, r'Bài toán kế hoạch sản xuất: \(\max4x_1+5x_2\) s.t. \(2x_1+x_2\le8,\ x_1+2x_2\le7,\ x_2\le3,\ x\ge0\). Phương án tối ưu là',
   r'\(x^*=(3,2)\) với lợi nhuận 22', [r'\(x^*=(4,0)\) với lợi nhuận 16', r'\(x^*=(1,3)\) với lợi nhuận 19', r'\(x^*=(0,3)\) với lợi nhuận 15'],
   r'Đỉnh của miền: \((0,0)\to0\), \((4,0)\to16\), \((3,2)\to22\), \((1,3)\to19\), \((0,3)\to15\). Lớn nhất 22 tại \((3,2)\) (kiểm linprog: ' + str(plan) + ').', E)
num('T', BT, r'Lợi nhuận tối đa của bài toán kế hoạch sản xuất trên là', plan['f'], r'\(4\cdot3+5\cdot2=22\) triệu đồng.', ans_text='22', grp=E)
mc('T', BT, r'Trong bài toán trên, nguyên liệu \(N_3\) (\(x_2\le3\)) tại phương án tối ưu \((3,2)\)',
   'còn dư 1 đơn vị nên không chặt', ['dùng hết', 'bị vi phạm', 'có giá bóng dương'],
   r'\(x_2=2<3\): ràng buộc lỏng ⇒ biến đối ngẫu \(y_3=0\) (độ lệch bù).', E)
num('T', BT, r'Biến đối ngẫu \(y_1\) ứng với nguyên liệu \(N_1\) của bài toán kế hoạch sản xuất bằng', 1, r'Dual: \(\min8y_1+7y_2+3y_3\), \(2y_1+y_2\ge4\), \(y_1+2y_2+y_3\ge5\): nghiệm \(y=(1,2,0)\) (code: ' + str(R['m0_btdoc_plan_dual']['y']) + ').', ans_text='1', grp=E)
num('T', BT, r'Giá trị tối ưu của bài toán đối ngẫu của kế hoạch sản xuất trên là', 22, r'\(8\cdot1+7\cdot2+3\cdot0=22\), bằng giá trị bài gốc (đối ngẫu mạnh).', ans_text='22', grp=E)
mc('T', BT, r'Định lý đối ngẫu (BTDOC, Định lý 1) cho cặp P và D: nếu cả hai đều có phương án thì',
   r'cả hai đều có phương án tối ưu và \(Z_P^*=Z_D^*\)', [r'chỉ P có phương án tối ưu', r'\(Z_P^*<Z_D^*\) chặt', r'giá trị tối ưu không xác định'],
   r'Đối ngẫu mạnh. Ngoài ra chỉ xảy ra: cả hai vô nghiệm; hoặc một bài không bị chặn và bài kia vô nghiệm.', E)
mc('T', BT, r'Định lý độ lệch bù nói: phương án x của P và y của D đều tối ưu khi và chỉ khi',
   r'\(x_j(\sum_ia_{ij}y_i-c_j)=0\) và \(y_i(\sum_ja_{ij}x_j-b_i)=0\)', [r'\(x_j+y_i=0\) với mọi i, j', r'\(x_jy_i=c_jb_i\)', r'\(\sum x_j=\sum y_i\)'],
   r'Ràng buộc không chặt ⇒ biến đối ngẫu tương ứng bằng 0, và ngược lại. (BTDOC Định lý 2.)', E)
tf('T', BT, r'Trong QHTT, độ lệch bù là trường hợp riêng của điều kiện bù \(\lambda_ig_i=0\) trong KKT.', True, r'KKT của LP = khả thi gốc + khả thi đối ngẫu + độ lệch bù.', E)
mc('T', BT, r'Ví dụ 4 mặt hàng của BTDOC (max \(5x_1+8x_2+4x_3+6x_4\), vật tư 300/500/200) ghi kết quả \((0,15,0,0)\), \(f=120\). Kiểm bằng LP cho',
   r'nghiệm LP là \((0,15.385,0,0)\) với \(f=123.08\); 120 là nghiệm nguyên', [r'trùng hoàn toàn: LP tối ưu \((0,15,0,0)\), \(f=120\)', r'LP không có nghiệm', r'nghiệm LP là \((0,0,0,0)\)'],
   r'Ràng buộc III: \(13x_2\le200\Rightarrow x_2\le15.385\). LP: \(f=8\cdot15.385=123.08\). Nghiệm nguyên tối ưu \(f=120\) (vét cạn: \((0,15,0,0)\) hoặc \((0,14,2,0)\)). Kết quả của BTDOC là nghiệm nguyên.', E)
num('T', BT, r'Giá trị tối ưu LP (làm tròn 2 chữ số) của bài 4 mặt hàng BTDOC là', float(four['f']), r'\(8\cdot200/13=123.077\).', tol=1e-3, ans_text='123.08', grp=E)
mc('T', SL, r'Bài “thức ăn gia súc” (Studocu C11): min \(50x_1+35x_2+25x_3\) với \(2x_1+x_2+3x_3\ge60\), \(3x_1+2x_2+5x_3=50\), … Kiểm tra cho thấy',
   'bài toán vô nghiệm (miền rỗng)', ['nghiệm tối ưu là (10, 0, 0)', 'nghiệm tối ưu là (0, 25, 0)', 'bài toán có vô số nghiệm'],
   r'Từ \(3x_1+2x_2+5x_3=50\): \(2x_1+x_2+3x_3\le\tfrac23\cdot50<60\). Miền rỗng (linprog: infeasible). Đề nguồn ngoài có thể chép sai số liệu.', E)
tf('T', SL, r'Trong bài “thức ăn gia súc”, bài toán đối ngẫu không bị chặn (dual unbounded).', True, r'Primal vô nghiệm ⇒ dual hoặc vô nghiệm hoặc không bị chặn; linprog cho “unbounded”.', E)
mc('S', 'nền tảng', r'Nghiệm tối ưu của bài toán QHTT (nếu có) luôn đạt tại',
   'ít nhất một đỉnh (điểm cực biên) của miền khả thi', ['điểm trong của miền khả thi', 'gốc tọa độ', 'trung điểm của một cạnh'],
   r'Định lý cơ bản của QHTT; nếu miền không có đỉnh (chứa đường thẳng) thì cần xét riêng.', E)
mc('S', 'nền tảng', r'Khi đường mức của hàm mục tiêu QHTT song song với một cạnh của miền và cạnh đó là biên tối ưu thì',
   'có vô số nghiệm tối ưu (cả cạnh)', ['nghiệm duy nhất', 'bài toán vô nghiệm', 'bài toán không bị chặn'],
   r'Mọi điểm của cạnh cho cùng giá trị mục tiêu.', E)
mc('T', SL, r'Thuật toán đơn hình (Simplex) thường được sử dụng để giải loại bài toán nào?',
   'quy hoạch tuyến tính', ['quy hoạch toàn phương không lồi', 'quy hoạch phi tuyến không ràng buộc', 'quy hoạch nguyên hỗn hợp tổng quát'],
   r'Đề Studocu Q3 (tham khảo): đơn hình dùng cho LP (đi giữa các đỉnh của đa diện lồi).', E)
tf('T', SL, r'Với Q = 0, bài toán QP (min \(\tfrac12x^\top Qx+c^\top x\) s.t. \(Ax\ge b\)) là quy hoạch tuyến tính.', True, r'Không còn số hạng bậc hai.', E)
mc('T', SL, r'Knapsack (ba lô) 0–1 W=5, vật (khối lượng, giá trị): (2,3),(3,4),(4,5),(5,8). Giá trị tối ưu là',
   '8 (chọn riêng vật 4)', ['7 (chọn vật 1 và 2)', '9 (chọn vật 1, 2 và 3)', '12 (chọn cả bốn vật)'],
   r'Vật 1+2 nặng 5 giá trị 7; vật 4 nặng 5 giá trị 8; các tổ hợp khác vượt sức chứa 5. Bảng DP: \(8\) (Studocu C13, tham khảo).', E)
num('T', SL, r'Knapsack W=10, vật (5,10),(4,40),(6,30),(3,50) (Studocu C14): giá trị tối ưu', 90, r'Chọn vật 2 (4 kg, 40) và vật 4 (3 kg, 50): tổng 7 kg, giá trị 90. DP: bảng cuối \(90\). Vét cạn xác nhận.', ans_text='90', grp=E)
mc('T', SL, r'Với Knapsack C14, các vật được chọn trong phương án tối ưu là',
   'vật 2 và vật 4', ['vật 1 và vật 3', 'vật 1 và vật 4', 'vật 3 và vật 4'],
   r'Vật 2+4: \(4+3=7\le10\), giá trị \(40+50=90\). Vật 3+4: \(6+3=9\), giá trị 80; vật 1+4: \(5+3=8\), giá trị 60.', E)
tf('S', 'nền tảng', r'Quy hoạch động cho bài toán ba lô 0–1 có độ phức tạp thời gian đa thức theo cả n và W (giả đa thức).', True, r'Bảng \(n\times W\); độ phức tạp \(O(nW)\) (giả đa thức).', E)
mc('S', 'nền tảng', r'Điều nào sau đây là điểm chung giữa độ lệch bù của LP và điều kiện bù của KKT?',
   'ràng buộc lỏng thì nhân tử bằng 0', ['nhân tử luôn dương', 'ràng buộc luôn chặt', 'hàm mục tiêu phải tuyến tính'],
   r'Cả hai nói: \(\lambda_i g_i=0\) hoặc \(y_i(b_i-a_i^\top x)=0\).', E)
essay('T', BT, r'Giải bài toán kế hoạch sản xuất \(\max4x_1+5x_2\) (2x₁+x₂≤8, x₁+2x₂≤7, x₂≤3) bằng đồ thị và kiểm tra bằng đối ngẫu.',
      r'<p>Các đỉnh: \((0,0),(4,0),(3,2),(1,3),(0,3)\) với \(f=0,16,22,19,15\). Tối ưu \((3,2)\), \(f=22\). Đối ngẫu: \(\min8y_1+7y_2+3y_3\) s.t. \(2y_1+y_2\ge4\), \(y_1+2y_2+y_3\ge5\); nghiệm \(y=(1,2,0)\), giá trị \(22\) (bằng bài gốc). Độ lệch bù: \(N_3\) dư \(\Rightarrow y_3=0\).</p>',
      ['Liệt kê đỉnh và giá trị', 'Viết đúng đối ngẫu', 'Kiểm giá trị bằng nhau'], E)
essay('T', SL, r'Kiểm tra tính khả thi của bài “thức ăn gia súc” (Studocu C11) và giải thích vì sao đề vô nghiệm.',
      r'<p>Với \(x\ge0\) và \(3x_1+2x_2+5x_3=50\): \(D_1=2x_1+x_2+3x_3\), tỉ số \(D_1/D_3\) theo từng biến là \(2/3,1/2,3/5\le2/3\). Vậy \(D_1\le\tfrac23\cdot50\approx33.3<60\): mâu thuẫn với \(D_1\ge60\). Miền rỗng; bài toán vô nghiệm. (Có thể số liệu đề bị sai; cần đối chiếu.)</p>',
      ['Chỉ ra cận trên của \\(D_1\\)', 'Kết luận miền rỗng'], E)
essay('S', 'nền tảng', r'Nêu mối liên hệ giữa độ lệch bù trong QHTT và điều kiện bù trong KKT; cho ví dụ từ bài kế hoạch sản xuất.',
      r'<p>KKT cho LP (min \(c^\top x\) s.t. \(Ax\ge b\), \(x\ge0\)) gồm khả thi gốc, khả thi đối ngẫu và độ lệch bù \(y_i(a_i^\top x-b_i)=0\), \(x_j(c_j-a^{j\top}y)=0\) — chính là điều kiện bù \(\lambda_ig_i=0\) với \(\lambda=y\). Ví dụ: \(N_3\) dư (\(x_2=2<3\)) ⇒ \(y_3=0\).</p>',
      ['Nêu điều kiện bù', 'Ví dụ số'], E)

# =====================================================================  F. BỔ SUNG (mệnh đề dễ nhầm, tính toán nhanh)
F = 'F. Mệnh đề dễ nhầm và tính nhanh'
tf('S', 'nền tảng', r'Nếu \(\nabla f(x^*)=0\) thì \(x^*\) chắc chắn là cực tiểu địa phương của f.', False, r'Điểm dừng có thể là cực đại hoặc yên ngựa: \(f=x^3\) tại 0, \(f=x^2-y^2\) tại \((0,0)\).', F)
tf('S', 'nền tảng', r'Định thức của tổng hai ma trận bằng tổng hai định thức: \(\det(A+B)=\det A+\det B\).', False, r'Không đúng: \(A=B=I_2\): \(\det(2I)=4\ne2\). Định thức nhân tính chất cho tích: \(\det(AB)=\det A\det B\).', F)
tf('S', 'nền tảng', r'Bất đẳng thức tam giác: \(\|u+v\|\le\|u\|+\|v\|\).', True, r'Hệ quả của Cauchy–Schwarz.', F)
tf('S', 'nền tảng', r'Luôn có \(\|u+v\|=\|u\|+\|v\|\) với mọi u, v.', False, r'Chỉ khi u, v cùng hướng. Ví dụ \(u=(1,0),v=(-1,0)\): vế trái 0, vế phải 2.', F)
tf('S', 'nền tảng', r'Ma trận đối xứng xác định dương luôn có định thức dương.', True, r'\(\det A=\prod\lambda_i>0\).', F)
tf('S', 'nền tảng', r'Mọi ma trận đối xứng có định thức dương đều xác định dương.', False, r'\(-I_2\) có \(\det=1>0\) nhưng xác định âm.', F)
tf('S', 'nền tảng', r'Hessian của hàm bậc nhất \(f(x)=a^\top x+b\) bằng ma trận không.', True, r'\(\nabla f=a\) hằng số; \(\nabla^2f=0\).', F)
tf('S', 'nền tảng', r'Gradient descent hội tụ với mọi bước \(t>0\).', False, r'Cần \(t<2/L\) (L hằng số Lipschitz của gradient); bước quá lớn phân kỳ.', F)
tf('S', 'nền tảng', r'Hàm liên tục trên tập compact khác rỗng luôn đạt giá trị nhỏ nhất.', True, r'Weierstrass.', F)
tf('S', 'nền tảng', r'Một bài toán QHTT có thể có hàm mục tiêu không bị chặn trên miền khả thi.', True, r'Ví dụ \(\max x_1+x_2\) s.t. \(x_1-x_2\le1,\ x\ge0\).', F)
tf('S', 'nền tảng', r'Nếu bài toán QHTT có nghiệm tối ưu duy nhất thì nghiệm đó là điểm trong của miền khả thi.', False, r'Nghiệm duy nhất của LP nằm ở đỉnh (biên).', F)
tf('T', BT, r'Đối ngẫu của bài toán max với các ràng buộc “\(\le\)” và \(x\ge0\) là bài toán min với các ràng buộc “\(\ge\)” và \(y\ge0\).', True, r'Sơ đồ đối ngẫu chuẩn (BTDOC mục 2).', F)
tf('T', BT, r'Theo độ lệch bù: nếu \(y_i>0\) thì ràng buộc thứ i của bài gốc phải chặt.', True, r'\(y_i(b_i-a_i^\top x)=0\).', F)
tf('S', 'nền tảng', r'Hàm \(f=x^4\) có Hessian xác định dương tại \(x=0\).', False, r'\(f^{\prime\prime}(0)=0\): chỉ nửa xác định dương. (f vẫn lồi chặt và có cực tiểu tại 0.)', F)
tf('S', 'nền tảng', r'Ma trận đơn vị \(I\) là xác định dương.', True, r'\(x^\top Ix=\|x\|^2>0\) với \(x\ne0\).', F)
num('S', 'nền tảng', r'Tính định thức của \(\begin{pmatrix}3&1\\2&4\end{pmatrix}\).', 10, r'\(3\cdot4-1\cdot2=10\).', ans_text='10', grp=F)
num('S', 'nền tảng', r'Tính \(\|v\|\) với \(v=(1,-2,2)\).', 3, r'\(\sqrt{1+4+4}=3\).', ans_text='3', grp=F)
num('S', 'nền tảng', r'Gradient của \(f=x^2+y^2\) tại \((3,4)\) có độ dài (chuẩn) là', 10, r'\(\nabla f=(6,8)\); \(\|(6,8)\|=10\).', ans_text='10', grp=F)
num('S', 'nền tảng', r'Với \(f=x^3y\), tính \(f_{xx}(1,1)\).', 6, r'\(f_x=3x^2y\), \(f_{xx}=6xy=6\).', ans_text='6', grp=F)
num('S', 'nền tảng', r'Giá trị riêng lớn nhất của \(\mathrm{diag}(2,-1,5)\) là', 5, r'Ma trận chéo có giá trị riêng là các phần tử đường chéo.', ans_text='5', grp=F)
num('S', 'nền tảng', r'Giải hệ \(x+y=5,\ x-y=1\): giá trị \(x\).', 3, r'Cộng hai phương trình: \(2x=6\Rightarrow x=3\), \(y=2\).', ans_text='3', grp=F)
num('S', 'nền tảng', r'Với \(f(x)=x^2\) và \(t=0.25\), \(x^0=2\): giá trị \(x^1\) của gradient descent là', 1, r'\(f^{\prime}=2x=4\); \(x^1=2-0.25\cdot4=1\).', ans_text='1', grp=F)
num('S', 'nền tảng', r'Vết (trace) của \(\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}\) là', 6, r'\(2+2+2=6\) (tổng các giá trị riêng \(2-\sqrt2,2,2+\sqrt2\)).', ans_text='6', grp=F)
mc('S', 'nền tảng', r'Hessian của \(f(x,y)=x^2y\) là',
   r'\(\begin{pmatrix}2y&2x\\2x&0\end{pmatrix}\)', [r'\(\begin{pmatrix}2y&x^2\\x^2&0\end{pmatrix}\)', r'\(\begin{pmatrix}2&2x\\2x&1\end{pmatrix}\)', r'\(\begin{pmatrix}0&2x\\2x&2y\end{pmatrix}\)'],
   r'\(f_x=2xy\), \(f_y=x^2\); \(f_{xx}=2y\), \(f_{xy}=2x\), \(f_{yy}=0\).', F)
mc('S', 'nền tảng', r'Gradient của \(f(x)=\tfrac12x^\top Qx+c^\top x\) (Q đối xứng) là',
   r'\(Qx+c\)', [r'\(Q+c\)', r'\(x^\top Q+c\)', r'\(2Qx+c\)'],
   r'Đạo hàm của \(\tfrac12x^\top Qx\) là \(Qx\) (nhờ đối xứng và hệ số \(\tfrac12\)).', F)
mc('S', 'nền tảng', r'Tập nghiệm của \(2x+y\le4\) trong \(\mathbb R^2\) là',
   'một nửa mặt phẳng đóng (lồi)', ['một đường thẳng', 'một hình cầu', 'một điểm'],
   r'Nửa không gian đóng \(\{a^\top x\le b\}\) với \(a=(2,1)\), \(b=4\).', F)
mc('S', 'nền tảng', r'Đường mức của \(f(x,y)=x^2+y^2\) là',
   'các đường tròn đồng tâm', ['các đường thẳng song song', 'các hyperbol', 'các parabol'],
   r'\(x^2+y^2=c\) là đường tròn tâm gốc bán kính \(\sqrt c\).', F)
mc('S', 'nền tảng', r'Hàm nào sau đây là coercive trên \(\mathbb R^2\)?',
   r'\(f(x,y)=x^2+y^2+x\)', [r'\(f=e^{x}\)', r'\(f=x^2\)', r'\(f=\sin(x)+\sin(y)\)'],
   r'\(x^2+y^2+x\ge\|(x,y)\|^2-\|(x,y)\|\to\infty\). \(x^2\) không tăng theo y; \(e^x\to0\) khi \(x\to-\infty\); \(\sin\) bị chặn.', F)
mc('S', 'nền tảng', r'Nghiệm của hệ \(2x+y=5,\ x+3y=5\) là',
   r'\((2,1)\)', [r'\((1,2)\)', r'\((5/2,0)\)', r'\((1,1)\)'],
   r'Từ hệ: \(x=5-3y\Rightarrow10-6y+y=5\Rightarrow y=1,x=2\). Thử: \(4+1=5\), \(2+3=5\).', F)
mc('S', 'nền tảng', r'Khi nào bài toán \(\min c^\top x\) s.t. \(Ax\le b\) (LP) có thể không có nghiệm tối ưu dù miền khả thi khác rỗng?',
   'khi hàm mục tiêu không bị chặn dưới trên miền', ['khi miền khả thi là đa giác lồi', 'khi c = 0', 'khi \\(b\\ge0\\)'],
   r'Miền không bị chặn và c chỉ theo hướng giảm vô hạn ⇒ \(\inf=-\infty\), không có nghiệm (TH2 trong Module 3).', F)

# ---- cân bằng độ dài đáp án ----
F_ = bank.fix
F_(r'“Quy hoạch phi tuyến” được BTDOC', 'hàm mục tiêu hoặc ít nhất một ràng buộc phi tuyến', ['chỉ hàm mục tiêu là hàm bậc hai lồi', 'mọi biến đều nhận giá trị nguyên dương', 'miền ràng buộc là một tập rời rạc hữu hạn'])
F_(r'Quy hoạch đa mục tiêu là', 'cùng miền ràng buộc, xét nhiều hàm mục tiêu', ['có nhiều miền ràng buộc rời nhau', 'hàm mục tiêu có nhiều biến nguyên', 'các hệ số phụ thuộc vào một tham số'])
F_(r'Quy hoạch tham số là', 'hệ số của hàm mục tiêu và ràng buộc phụ thuộc tham số', ['biến chỉ nhận giá trị nguyên không âm', 'bài toán chia thành nhiều giai đoạn liên tiếp', 'bài toán chỉ chứa ràng buộc đẳng thức'])
F_(r'Quy hoạch động dùng khi', 'bài toán gồm nhiều giai đoạn hoặc thay đổi theo thời gian', ['bài toán chỉ có duy nhất một biến quyết định', 'hàm mục tiêu là hàm bậc hai của các biến', 'miền ràng buộc là một đa diện lồi bị chặn'])
F_(r'Hàm \(f(x)=x^3-3x\) trên \(\mathbb R\) có', r'cực tiểu địa phương tại \(x=1\), không toàn cục', [r'cực tiểu toàn cục tại \(x=1\) và \(x=-1\)', r'cực tiểu toàn cục duy nhất tại \(x=-1\)', r'không có điểm dừng nào trên \(\mathbb R\)'])
F_(r'Trong lĩnh vực tối ưu hóa, bài toán Knapsack', 'chọn đồ vào túi có giới hạn trọng lượng để tối đa giá trị', ['tìm đường đi ngắn nhất giữa hai điểm trên đồ thị', 'cực tiểu hóa một hàm lồi có nhiều biến số', 'phân loại các đối tượng vào những lớp cho trước'])
F_(r'Hạng (rank) của ma trận là', 'số hàng (cột) độc lập tuyến tính tối đa', ['số phần tử khác 0 của ma trận', 'tổng các phần tử nằm trên đường chéo', 'giá trị định thức của chính ma trận đó'])
F_(r'Khai triển Taylor bậc hai của f tại x là', r'\(f(x)+\nabla f^\top d+\tfrac12d^\top\nabla^2f\,d\)', [r'\(f(x)+\tfrac12\nabla f(x)^\top d\) (thiếu bậc hai)', r'\(f(x)+d^\top\nabla^2f(x)d\) (thiếu hệ số 1/2 và bậc một)', r'\(\nabla f(x)+\nabla^2f(x)d\) (thiếu \(f(x)\))'])
F_(r'Với \(f=x^3-3x+y^2\), điểm \((-1,0)\) là', r'điểm yên ngựa (Hessian \(\mathrm{diag}(-6,2)\))', ['cực tiểu địa phương (Hessian dương)', 'cực đại địa phương (Hessian âm)', 'cực tiểu toàn cục của f trên \\(\\mathbb R^2\\)'])
F_(r'Trong tối ưu không ràng buộc, tìm kiếm chính xác theo tia', 'tìm bước làm cực tiểu f dọc một hướng cho trước', ['kiểm tra tính lồi của hàm mục tiêu f', 'xác định ma trận Hessian của hàm số f', 'tìm hướng giảm nhanh nhất của hàm f'])
F_(r'\(\inf\{e^x:x\in\mathbb R\}\) bằng', '0, nhưng không đạt được', ['1, đạt tại \\(x=0\\) (giá trị nhỏ nhất)', '\\(-\\infty\\) vì hàm không bị chặn dưới', '0, đạt tại một điểm \\(x\\) hữu hạn'])
F_(r'Định lý Weierstrass: hàm liên tục trên tập compact', 'đạt cực tiểu và cực đại trên tập đó', ['luôn có duy nhất một điểm cực tiểu', 'luôn khả vi tại mọi điểm của tập', 'luôn là hàm lồi trên tập đó'])
F_(r'\(\min xy\) trên đĩa', r'đĩa compact và \(xy\) liên tục', [r'\(xy\) là hàm lồi trên đĩa', r'đĩa có ít nhất một điểm trong', r'gradient \(\nabla(xy)\) luôn khác 0'])
F_(r'Trong bài toán trên, nguyên liệu \(N_3\)', 'còn dư 1 đơn vị nên không chặt', ['được dùng hết nên chặt', 'bị vi phạm nên phương án không khả thi', 'có giá bóng dương lớn hơn \\(N_1\\)'])
F_(r'Định lý độ lệch bù nói', r'\(x_j(\sum a_{ij}y_i-c_j)=0\) và \(y_i(\sum a_{ij}x_j-b_i)=0\)', [r'\(x_j+y_i=0\) với mọi cặp chỉ số i, j', r'\(x_jy_i=c_jb_i\) với mọi i, j', r'\(\sum x_j=\sum y_i\) và \(x=y\)'])
F_(r'Nghiệm tối ưu của bài toán QHTT (nếu có)', 'một đỉnh của miền khả thi', ['một điểm nằm trong miền khả thi', 'gốc tọa độ (khi \\(x\\ge0\\))', 'trung điểm của một cạnh miền khả thi'])

tf('S', 'nền tảng', r'Tích vô hướng \(u^\top v\) luôn không âm.', False, r'Có thể âm: \(u=(1,0),v=(-1,0)\Rightarrow-1\). Dấu phụ thuộc góc giữa hai vectơ.', F)
tf('S', 'nền tảng', r'Nếu \(AB=I\) với A, B vuông thì \(B=A^{-1}\).', True, r'Với ma trận vuông, nghịch đảo phải cũng là nghịch đảo trái.', F)
tf('S', 'nền tảng', r'Mọi ma trận vuông đều có nghịch đảo.', False, r'Chỉ ma trận không suy biến (\(\det\ne0\)). Ví dụ \(\begin{pmatrix}1&1\\1&1\end{pmatrix}\) có \(\det=0\).', F)
tf('S', 'nền tảng', r'Giá trị riêng của ma trận đối xứng có thể là số phức không thực.', False, r'Ma trận đối xứng thực có mọi giá trị riêng thực.', F)
tf('S', 'nền tảng', r'Gradient \(\nabla f(x)\) chỉ hướng giảm nhanh nhất của f tại x.', False, r'\(\nabla f\) chỉ hướng <b>tăng</b> nhanh nhất; \(-\nabla f\) là hướng giảm nhanh nhất.', F)
tf('S', 'nền tảng', r'Hàm \(f=x^2-y^2\) có điểm dừng \((0,0)\) là cực tiểu.', False, r'Hessian \(\mathrm{diag}(2,-2)\) không xác định: điểm yên ngựa.', F)
tf('S', 'nền tảng', r'Hàm \(f=e^x\) trên \(\mathbb R\) có cực tiểu toàn cục.', False, r'\(\inf=0\) không đạt.', F)
tf('S', 'nền tảng', r'Đường mức của một hàm khả vi tại điểm x vuông góc với gradient \(\nabla f(x)\) (khi \(\nabla f(x)\ne0\)).', True, r'Đạo hàm theo hướng tiếp tuyến của đường mức bằng 0.', F)
