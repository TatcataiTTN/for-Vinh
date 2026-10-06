"""Ngân hàng câu hỏi Module 1 — Tập lồi & hàm lồi. Nguồn chính: Slides/1_Kien thuc ve ham loi va tap loi_250418.pdf
Nhãn nguồn: G = lấy trực tiếp từ nội dung slide; B = bài tập/ví dụ gốc của slide; T = tham khảo Studocu; S = biên soạn thêm."""
import json, os, numpy as np
from qlib import Bank
from helpers import R

bank = Bank('m1')
mc, tf, num, essay = bank.mc, bank.tf, bank.num, bank.essay
S1 = 'slide 1'

def r(p): return f'{S1} · tr.{p}'

# =====================================================================  A. TẬP LỒI (tr.3–9)
A = 'A. Tập lồi'
mc('G', r(3), r'Cho hai điểm \(x,y\in\mathbb R^n\). Tập các điểm \(z=\theta x+(1-\theta)y\) với \(\theta\in\mathbb R\) là:',
   'đường thẳng đi qua x và y',
   ['đoạn thẳng nối x và y', 'nửa đường thẳng xuất phát từ x', 'mặt phẳng chứa x và y'],
   r'Khi \(\theta\) chạy trên <b>toàn bộ</b> \(\mathbb R\), tập \(\{\theta x+(1-\theta)y\}\) là cả đường thẳng qua x, y. Chỉ khi hạn chế \(\theta\in[0,1]\) mới được đoạn thẳng (slide tr.3).', A)
mc('G', r(3), r'Khi hạn chế \(\theta\in[0,1]\), tập \(\{\theta x+(1-\theta)y\}\) là:',
   'đoạn thẳng nối x và y',
   ['đường thẳng đi qua x và y', 'chỉ hai điểm x và y', 'nửa đường thẳng từ x qua y'],
   r'\(\theta=1\) cho \(z=x\), \(\theta=0\) cho \(z=y\), các giá trị giữa cho các điểm nằm giữa: đó là đoạn thẳng \([x,y]\).', A)
mc('G', r(7), r'Định nghĩa tập lồi: một tập khác rỗng \(C\subset\mathbb R^n\) là lồi nếu',
   'đoạn thẳng nối hai điểm bất kỳ của C nằm trọn trong C',
   ['đường thẳng nối hai điểm bất kỳ của C nằm trong C', 'C có ít nhất một điểm trong', 'C là tập đóng và bị chặn'],
   r'Điều kiện: \(x,y\in C\Rightarrow\theta x+(1-\theta)y\in C\ \forall\theta\in[0,1]\). Đóng/bị chặn/có điểm trong là các tính chất khác, không liên quan định nghĩa (slide tr.7).', A)
mc('G', r(7), r'Điều kiện nào sau đây là cách viết đại số của tính lồi của C?',
   r'\(x,y\in C,\ \theta\in[0,1]\Rightarrow\theta x+(1-\theta)y\in C\)',
   [r'\(x,y\in C,\ \theta\in\mathbb R\Rightarrow\theta x+(1-\theta)y\in C\)', r'\(x,y\in C\Rightarrow x+y\in C\)', r'\(x\in C,\ t\ge0\Rightarrow tx\in C\)'],
   r'Đáp án A. Đáp án B đòi hỏi C chứa cả đường thẳng qua hai điểm (tập affine, mạnh hơn lồi). Hai phương án còn lại là tính đóng với phép cộng / phép nhân vô hướng (nón), cũng không phải tính lồi.', A)
tf('G', r(7), r'Theo quy ước trong slide, tập rỗng được coi là tập lồi.', True,
   r'Slide tr.7: “Người ta quy ước tập rỗng là tập lồi” (vì điều kiện “với mọi x, y ∈ C” đúng rỗng).', A)
tf('G', r(7), r'Một tập chỉ gồm đúng một điểm là tập lồi.', True,
   r'Với \(x=y\) thì \(\theta x+(1-\theta)y=x\in C\). Slide tr.7 liệt kê “tập chỉ gồm một phần tử” trong các ví dụ về tập lồi.', A)
tf('G', r(7), r'Toàn bộ không gian \(\mathbb R^n\) là một tập lồi.', True, r'Mọi tổ hợp lồi của hai điểm của \(\mathbb R^n\) vẫn thuộc \(\mathbb R^n\).', A)
tf('G', r(7), r'Một đoạn thẳng bất kỳ trong \(\mathbb R^n\) là tập lồi.', True, r'Tổ hợp lồi của hai điểm trên đoạn vẫn nằm trên đoạn đó.', A)
tf('G', r(9), r'Giao của hai tập lồi \(S_1\cap S_2\) là tập lồi.', True,
   r'Lấy \(x,y\in S_1\cap S_2\). Cả hai tập đều lồi nên \(\theta x+(1-\theta)y\) thuộc \(S_1\) và thuộc \(S_2\), tức thuộc giao (slide tr.9).', A)
tf('G', r(9), r'Tổng \(S_1+S_2=\{x_1+x_2\mid x_1\in S_1,x_2\in S_2\}\) của hai tập lồi là tập lồi.', True,
   r'Với \(x=x_1+x_2,\ y=y_1+y_2\): \(\theta x+(1-\theta)y=(\theta x_1+(1-\theta)y_1)+(\theta x_2+(1-\theta)y_2)\in S_1+S_2\).', A)
tf('G', r(9), r'Hợp của hai tập lồi luôn là một tập lồi (câu hỏi đặt ra ở slide tr.9).', False,
   r'Phản ví dụ: hai đoạn \([0,1]\) và \([2,3]\) trên trục số đều lồi, nhưng hợp của chúng không chứa điểm \(1.5\) nằm giữa \(1\) và \(2\).', A)
mc('G', r(9), r'Trong \(\mathbb R\), hai tập lồi nào dưới đây có hợp KHÔNG lồi?',
   r'\([0,1]\) và \([2,3]\)', [r'\([0,2]\) và \([1,3]\)', r'\([0,1]\) và \([1,2]\)', r'\([0,1]\) và \([0.2,0.5]\)'],
   r'\([0,1]\cup[2,3]\) không chứa điểm 1,5. Các cặp còn lại có hợp là \([0,3]\), \([0,2]\), \([0,1]\) — đều là đoạn (lồi).', A)
mc('S', r(9), r'Tập nào sau đây KHÔNG phải là tập lồi trong \(\mathbb R^2\)?',
   r'Vành khuyên \(\{1\le\|x\|\le2\}\)', [r'Hình tròn đóng \(\{\|x\|\le2\}\)', r'Nửa mặt phẳng \(\{x_1+x_2\le1\}\)', r'Đoạn thẳng nối \((0,0)\) và \((1,1)\)'],
   r'Lấy \((1.5,0)\) và \((-1.5,0)\): trung điểm \((0,0)\) có chuẩn 0 < 1 nên nằm ngoài vành khuyên.', A)
mc('S', r(9), r'Nếu \(S_1\) lồi và \(S_2\) lồi thì tập nào sau đây chắc chắn lồi?',
   r'\(S_1\cap S_2\)', [r'\(S_1\cup S_2\)', r'\(S_1\setminus S_2\)', r'phần bù \(\mathbb R^n\setminus S_1\)'],
   r'Chỉ giao (và tổng Minkowski) được bảo toàn. Hợp, hiệu tập hợp và phần bù nói chung làm mất tính lồi (ví dụ phần bù của hình tròn).', A)
mc('S', r(3), r'Điểm \(z=0.3x+0.7y\) nằm ở đâu trên đường thẳng qua x và y?',
   r'Trong đoạn \([x,y]\), gần y hơn', [r'Trong đoạn \([x,y]\), gần x hơn', r'Ngoài đoạn, phía x', r'Ngoài đoạn, phía y'],
   r'\(\theta=0.3\in[0,1]\) nên z thuộc đoạn. Vì hệ số của y (0,7) lớn hơn nên z gần y hơn: \(\|z-y\|=0.3\|x-y\|\) còn \(\|z-x\|=0.7\|x-y\|\).', A)
num('S', r(3), r'Cho \(x=(0,0)\), \(y=(4,2)\). Tính tổng hai tọa độ của điểm \(z=\tfrac14x+\tfrac34y\).', 4.5,
    r'\(z=\tfrac34(4,2)=(3,1.5)\), tổng tọa độ \(=4.5\).', ans_text='4.5', grp=A)
essay('B', r(9), r'Chứng minh giao của hai tập lồi là tập lồi, và cho ví dụ chứng tỏ hợp của hai tập lồi có thể không lồi (bài tập Studocu C6 cùng dạng).',
      r'<p>Giả sử \(S_1,S_2\) lồi và \(x,y\in S_1\cap S_2\), \(\theta\in[0,1]\). Vì \(x,y\in S_1\) và \(S_1\) lồi nên \(z=\theta x+(1-\theta)y\in S_1\). Tương tự \(z\in S_2\). Vậy \(z\in S_1\cap S_2\): giao lồi.</p><p>Hợp: \(S_1=[0,1]\), \(S_2=[2,3]\subset\mathbb R\) đều lồi; \(1\in S_1\), \(2\in S_2\) nhưng \(\tfrac12\cdot1+\tfrac12\cdot2=1.5\notin S_1\cup S_2\). Vậy hợp không lồi.</p>',
      [r'Nêu đúng định nghĩa lồi (\(\theta\in[0,1]\))', 'Dùng tính lồi của TỪNG tập để suy ra z thuộc từng tập', 'Phản ví dụ cụ thể, chỉ ra điểm bị thiếu'], A)

# =====================================================================  B. BAO LỒI, TÍCH VÔ HƯỚNG, SIÊU PHẲNG, CHUẨN, CẦU, POLYHEDRON (tr.11–22)
B = 'B. Bao lồi, siêu phẳng, cầu, polyhedron'
mc('G', r(11), r'Tổ hợp lồi của các điểm \(x_1,\dots,x_k\) là điểm \(\theta_1x_1+\dots+\theta_kx_k\) với điều kiện',
   r'\(\theta_i\ge0\) và \(\theta_1+\dots+\theta_k=1\)', [r'\(\theta_i\in\mathbb R\) và \(\sum\theta_i=1\)', r'\(\theta_i\ge0\) và \(\sum\theta_i\le1\)', r'\(\theta_i>1\) với mọi i'],
   r'Tổ hợp lồi cần hệ số không âm và tổng bằng 1. Bỏ điều kiện không âm ta được tổ hợp affine; bỏ điều kiện tổng bằng 1 mà giữ không âm ta được tổ hợp nón (slide tr.11).', B)
mc('G', r(11), r'Bao lồi \(\mathrm{conv}\,C\) của tập C là',
   r'tập tất cả các tổ hợp lồi của các điểm thuộc C',
   [r'giao của tất cả các hình cầu chứa toàn bộ tập C', r'tập các điểm nằm trên biên của tập C cùng với tâm', r'tập lồi lớn nhất còn nằm hoàn toàn trong C'],
   r'\(\mathrm{conv}\,C=\{\theta_1x_1+\dots+\theta_kx_k\mid x_i\in C,\theta_i\ge0,\sum\theta_i=1\}\). Nó là tập lồi <b>nhỏ nhất</b> chứa C (không phải lớn nhất nằm trong C).', B)
tf('G', r(11), r'Bao lồi của tập C luôn chứa C.', True, r'Lấy \(k=1,\theta_1=1\): mỗi điểm \(x\in C\) là một tổ hợp lồi của chính nó.', B)
tf('S', r(11), r'Nếu C đã là tập lồi thì \(\mathrm{conv}\,C=C\).', True, r'Tập lồi đóng với mọi tổ hợp lồi (bằng quy nạp theo k), nên \(\mathrm{conv}\,C\subseteq C\); kết hợp \(C\subseteq\mathrm{conv}\,C\) được đẳng thức.', B)
mc('S', r(11), r'Bao lồi của ba điểm không thẳng hàng \((0,0),(2,0),(0,2)\) trong \(\mathbb R^2\) là',
   'tam giác đóng với ba đỉnh đó', ['chỉ ba điểm đó', 'đường tròn đi qua ba điểm đó', 'toàn bộ mặt phẳng'],
   r'Tổ hợp lồi của ba điểm phủ kín tam giác (kể cả biên và phần trong).', B)
mc('G', r(13), r'Tích vô hướng của \(u,v\in\mathbb R^n\) được định nghĩa bởi',
   r'\(\langle u,v\rangle=u_1v_1+\dots+u_nv_n\)', [r'\(\langle u,v\rangle=\sqrt{u_1^2v_1^2+\dots+u_n^2v_n^2}\)', r'\(\langle u,v\rangle=(u_1+v_1)\cdots(u_n+v_n)\)', r'\(\langle u,v\rangle=\max_i u_iv_i\)'],
   r'Tích vô hướng Euclid là tổng các tích tọa độ tương ứng; có thể viết \(u^\top v\) hoặc \(v^\top u\) (slide tr.13).', B)
num('G', r(13), r'Tính tích vô hướng \(\langle u,v\rangle\) với \(u=(1,2,3)\), \(v=(4,-5,6)\).', 12,
    r'\(1\cdot4+2\cdot(-5)+3\cdot6=4-10+18=12\).', ans_text='12', grp=B)
mc('G', r(17), r'Chuẩn Euclid của \(v=(v_1,\dots,v_n)\) là',
   r'\(\|v\|=\sqrt{v_1^2+\dots+v_n^2}\)', [r'\(\|v\|=|v_1|+\dots+|v_n|\)', r'\(\|v\|=v_1^2+\dots+v_n^2\)', r'\(\|v\|=\max_i|v_i|\)'],
   r'Các phương án còn lại là chuẩn \(\ell_1\), bình phương chuẩn và chuẩn \(\ell_\infty\). Chuẩn trong slide tr.17 là chuẩn Euclid (\(\ell_2\)) và \(\|v\|^2=v^\top v\).', B)
num('G', r(17), r'Tính chuẩn Euclid của \(v=(3,4)\).', 5, r'\(\sqrt{3^2+4^2}=\sqrt{25}=5\).', ans_text='5', grp=B)
mc('G', r(14), r'Siêu phẳng trong \(\mathbb R^n\) là tập có dạng',
   r'\(\{x\mid a^\top x=b\}\) với \(a\ne0\)', [r'\(\{x\mid a^\top x\le b\}\) với \(a\ne0\)', r'\(\{x\mid \|x-a\|=b\}\)', r'\(\{x\mid Ax=b\}\) với A bất kỳ'],
   r'Siêu phẳng \(\{a^\top x=b\}\) (\(a\ne0\)) là một đường thẳng trong \(\mathbb R^2\), một mặt phẳng trong \(\mathbb R^3\). Dạng \(a^\top x\le b\) là nửa không gian (slide tr.14).', B)
mc('G', r(14), r'Nửa không gian đóng là tập có dạng',
   r'\(\{x\mid a^\top x\le b\}\) với \(a\ne0\)', [r'\(\{x\mid a^\top x=b\}\)', r'\(\{x\mid a^\top x<0,\ b>0\}\)', r'\(\{x\mid \|x\|\le b\}\)'],
   r'Siêu phẳng chia \(\mathbb R^n\) thành hai nửa không gian; nửa không gian đóng chứa cả siêu phẳng biên (slide tr.14).', B)
tf('G', r(14), r'Một siêu phẳng chia \(\mathbb R^n\) thành hai nửa không gian.', True, r'Hai nửa không gian \(\{a^\top x\le b\}\) và \(\{a^\top x\ge b\}\) cùng nhận siêu phẳng làm biên.', B)
mc('S', r(14), r'Vectơ \(a\) trong siêu phẳng \(\{a^\top x=b\}\) có vai trò gì?',
   'vectơ pháp tuyến, vuông góc với siêu phẳng', ['vectơ chỉ phương nằm trong siêu phẳng', 'một điểm nằm trên siêu phẳng', 'khoảng cách từ gốc đến siêu phẳng'],
   r'Với hai điểm x, y thuộc siêu phẳng, \(a^\top(x-y)=b-b=0\): a vuông góc với mọi vectơ nằm trong siêu phẳng.', B)
tf('S', r(14), r'Mọi siêu phẳng và mọi nửa không gian đóng đều là tập lồi.', True, r'Nếu \(a^\top x\le b\) và \(a^\top y\le b\) thì \(a^\top(\theta x+(1-\theta)y)\le\theta b+(1-\theta)b=b\). Với dấu “=” chứng minh tương tự.', B)
mc('G', r(18), r'Hình cầu tâm \(x_c\) bán kính \(r>0\) trong \(\mathbb R^n\) là',
   r'\(B(x_c,r)=\{x\mid\|x-x_c\|\le r\}\)',
   [r'\(\{x\mid\|x-x_c\|=r\}\) (chỉ phần mặt cầu)', r'\(\{x\mid\|x\|\le r\}\) (luôn có tâm ở gốc)', r'\(\{x\mid\|x-x_c\|\ge r\}\) (phần ngoài cầu)'],
   r'Slide tr.18: hình cầu (đóng) là \(\{x\mid(x-x_c)^\top(x-x_c)\le r^2\}\). Bỏ dấu “≤” thành “=” sẽ chỉ còn mặt cầu.', B)
mc('G', r(18), r'Một ellipsoid có dạng \(E=\{x\mid(x-x_c)^\top P(x-x_c)\le1\}\). Theo slide, ma trận P phải là',
   r'ma trận đối xứng và nửa xác định dương',
   [r'ma trận đường chéo với các phần tử bất kỳ', r'ma trận đơn vị (khi đó chỉ được hình cầu)', r'ma trận vuông bất kỳ có định thức bằng 1'],
   r'Slide tr.18: “P là ma trận đối xứng và nửa xác định dương cỡ n”. Lưu ý thêm: nếu P chỉ nửa xác định dương thì tập vẫn lồi nhưng có thể không bị chặn; để E là ellipsoid thật sự (bị chặn) cần \(P\succ0\) (Boyd dùng \(P\in\mathbb S^n_{++}\)). \(P=r^{-2}I\) cho hình cầu bán kính r.', B)
tf('G', r(18), r'Hình cầu đóng và ellipsoid (với \(P\succeq0\)) đều là tập lồi.', True,
   r'Cả hai đều là tập mức dưới \(\{f(x)\le c\}\) của hàm lồi (\(\|x-x_c\|^2\) hoặc \((x-x_c)^\top P(x-x_c)\) với \(P\succeq0\)); tập mức dưới của hàm lồi là lồi.', B)
mc('G', r(22), r'Polyhedron (tập lồi đa diện) là',
   r'tập nghiệm của hệ hữu hạn đẳng thức và bất đẳng thức tuyến tính',
   [r'giao của một số hữu hạn các hình cầu đóng', r'bao lồi của một tập vô hạn các điểm bất kỳ', r'tập nghiệm của một bất đẳng thức bậc hai duy nhất'],
   r'\(P=\{x\mid a_j^\top x\le b_j,\ c_j^\top x=d_j\}\); tương đương là giao hữu hạn các nửa không gian đóng (slide tr.22).', B)
mc('G', r(22), r'Polytope là',
   'polyhedron bị chặn', ['polyhedron không bị chặn', 'ellipsoid bị chặn', 'bao lồi của một đường tròn'],
   r'Slide tr.22: “Một tập lồi đa diện bị chặn đôi khi được gọi là một polytope”.', B)
tf('G', r(22), r'Miền chấp nhận của một bài toán quy hoạch tuyến tính là một polyhedron.', True,
   r'Hệ ràng buộc \(Ax\le b,\ Cx=d\) chính là dạng định nghĩa polyhedron. Đây là chỗ nối giữa QHTT (môn cũ) và giải tích lồi.', B)
mc('S', r(22), r'Tập \(\{(x_1,x_2)\mid x_1\ge0,\ x_2\ge0,\ x_1+x_2\le1\}\) là',
   r'polytope (đa diện lồi bị chặn): tam giác',
   [r'polyhedron nhưng không bị chặn (nửa mặt phẳng)', r'tập không lồi vì có ba đỉnh nhọn', r'hình cầu đóng trong chuẩn \(\ell_1\)'],
   r'Đây là giao ba nửa mặt phẳng, bị chặn (\(0\le x_i\le1\)), chính là tam giác với đỉnh \((0,0),(1,0),(0,1)\).', B)
mc('S', r(22), r'Tập \(\{x\in\mathbb R^2\mid x_1\ge0,\ x_2\ge0\}\) (góc phần tư thứ nhất) là',
   r'polyhedron nhưng KHÔNG phải polytope',
   [r'polytope, vì chỉ có hai ràng buộc', r'tập không lồi vì có góc vuông', r'một siêu phẳng vì có hai ràng buộc'],
   r'Nó là giao hai nửa mặt phẳng (polyhedron) nhưng không bị chặn nên không phải polytope.', B)
tf('S', r(22), r'Mọi polytope đều là bao lồi của hữu hạn điểm (các đỉnh của nó).', True,
   r'Đây là định lý biểu diễn Minkowski–Weyl cho polytope: polytope = bao lồi hữu hạn các đỉnh. Nó giải thích vì sao tối ưu tuyến tính đạt tại đỉnh.', B)
mc('S', r(14), r'Tập nghiệm của hệ \(\{x_1+x_2=1,\ x_1-x_2=0\}\) trong \(\mathbb R^2\) là',
   r'một điểm \((0.5,0.5)\), vẫn là polyhedron',
   [r'tập rỗng vì hai đường thẳng song song', r'một đường thẳng nằm trong \(\mathbb R^2\)', r'toàn bộ mặt phẳng \(\mathbb R^2\) vì có hai ẩn'],
   r'Giao hai đường thẳng không song song là một điểm; hệ đẳng thức tuyến tính luôn cho polyhedron (có thể suy biến thành một điểm).', B)
essay('S', r(22), r'Chứng minh rằng polyhedron \(P=\{x\mid Ax\le b\}\) là tập lồi.',
      r'<p>Lấy \(x,y\in P\), \(\theta\in[0,1]\). Khi đó \(A(\theta x+(1-\theta)y)=\theta Ax+(1-\theta)Ay\le\theta b+(1-\theta)b=b\) (vì \(\theta\ge0\), \(1-\theta\ge0\) và \(Ax\le b\), \(Ay\le b\)). Vậy \(\theta x+(1-\theta)y\in P\).</p>',
      ['Nhân bất đẳng thức với hệ số không âm rồi cộng', 'Kết luận theo định nghĩa lồi'], B)

# =====================================================================  C. HÀM LỒI (tr.25–27, 45, 52)
C = 'C. Hàm lồi'
mc('G', r(25), r'Hàm \(f:\mathbb R^n\to\mathbb R\) là lồi khi và chỉ khi',
   r'\(\mathrm{dom}\,f\) lồi và \(f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)\)',
   [r'\(f(\theta x+(1-\theta)y)\ge\theta f(x)+(1-\theta)f(y)\) với mọi \(\theta\)', r'\(f\) liên tục và khả vi trên toàn miền xác định', r'\(f(x+y)=f(x)+f(y)\) với mọi \(x,y\)'],
   r'Đó là bất đẳng thức Jensen kèm điều kiện miền hữu hiệu lồi (slide tr.25). Chiều “≥” là định nghĩa hàm lõm.', C)
mc('G', r(25), r'Miền hữu hiệu (effective domain) của f được định nghĩa là',
   r'\(\mathrm{dom}\,f=\{x\in\mathbb R^n\mid f(x)<+\infty\}\)', [r'\(\{x\mid f(x)\ge0\}\)', r'\(\{x\mid\nabla f(x)=0\}\)', r'\(\{x\mid f(x)\le f(0)\}\)'],
   r'Slide tr.25 dùng \(\mathrm{dom}\,f:=\{x\mid f(x)<+\infty\}\): tập các điểm mà f nhận giá trị hữu hạn.', C)
mc('G', r(25), r'Hàm f được gọi là lồi chặt nếu',
   r'Jensen là bất đẳng thức chặt (<) với mọi \(x\ne y\)',
   [r'f là hàm lồi, liên tục và có đạo hàm liên tục', r'f là hàm lồi và bị chặn dưới trên toàn miền', r'f có Hessian bằng ma trận không tại mọi điểm'],
   r'Lồi chặt: \(f(\theta x+(1-\theta)y)<\theta f(x)+(1-\theta)f(y)\). Hàm tuyến tính lồi nhưng không lồi chặt (luôn xảy ra dấu bằng).', C)
mc('G', r(25), r'Hàm f được gọi là lõm nếu',
   r'\(-f\) là hàm lồi', [r'\(f\) là hàm lồi âm', r'\(1/f\) là hàm lồi', r'\(f\) đạt cực đại'],
   r'Định nghĩa của slide tr.25: “lõm nếu −f là lồi”; lõm chặt nếu −f lồi chặt.', C)
tf('G', r(25), r'Hàm tuyến tính \(f(x)=a_1x_1+\dots+a_nx_n\) vừa lồi vừa lõm.', True,
   r'Với hàm tuyến tính Jensen luôn có dấu “=”, thỏa cả hai chiều (slide tr.50).', C)
mc('G', r(26), r'Về hình học, hàm số một biến là lồi khi và chỉ khi',
   r'dây cung nối hai điểm trên đồ thị nằm phía trên đồ thị',
   [r'tiếp tuyến tại mọi điểm luôn nằm phía trên đồ thị', r'đồ thị có đúng một điểm cực tiểu địa phương', r'đồ thị luôn đi qua gốc tọa độ và đối xứng'],
   r'Hình slide tr.26: hàm lồi có dây cung trên đồ thị; hàm lõm có dây cung dưới đồ thị. Với hàm lồi khả vi thì <i>tiếp tuyến</i> nằm dưới đồ thị.', C)
mc('G', r(27), r'Điều kiện cấp 1 cho hàm lồi khả vi: f lồi khi và chỉ khi \(\mathrm{dom}\,f\) lồi và',
   r'\(f(y)\ge f(x)+\nabla f(x)^\top(y-x)\) với mọi \(x,y\in\mathrm{dom}\,f\)',
   [r'\(f(y)\le f(x)+\nabla f(x)^\top(y-x)\) với mọi \(x,y\in\mathrm{dom}\,f\)', r'\(\nabla f(x)^\top(y-x)\ge0\) với mọi \(x,y\in\mathrm{dom}\,f\)', r'\(\nabla f(x)=0\) tại mọi điểm \(x\in\mathrm{dom}\,f\)'],
   r'Đồ thị của hàm lồi nằm phía trên mọi “siêu phẳng tiếp xúc” (xấp xỉ tuyến tính bậc nhất). Chiều “≤” ứng với hàm lõm.', C)
mc('S', r(27), r'Từ điều kiện cấp 1 suy ra: nếu \(\nabla f(x^*)=0\) và f lồi thì',
   r'\(x^*\) là điểm cực tiểu toàn cục của f', [r'\(x^*\) là điểm cực đại của f', r'\(x^*\) chỉ là cực tiểu địa phương', r'f không có cực tiểu'],
   r'\(f(y)\ge f(x^*)+\nabla f(x^*)^\top(y-x^*)=f(x^*)\) với mọi y. Đây là lý do hàm lồi được ưa chuộng: điểm dừng là cực tiểu toàn cục.', C)
tf('G', r(45), r'Hàm \(e^{ax}\) là lồi trên \(\mathbb R\) với mọi \(a\in\mathbb R\).', True, r'\((e^{ax})^{\prime\prime}=a^2e^{ax}\ge0\) với mọi \(x\).', C)
mc('G', r(45), r'Hàm \(x^a\) là lồi trên \(\mathbb R_{++}\) khi',
   r'\(a\ge1\) hoặc \(a\le0\)', [r'\(0\le a\le1\)', r'\(a>0\) bất kỳ', r'chỉ khi \(a=2\)'],
   r'\((x^a)^{\prime\prime}=a(a-1)x^{a-2}\ge0\) trên \(x>0\) khi \(a(a-1)\ge0\), tức \(a\ge1\) hoặc \(a\le0\). Với \(0\le a\le1\) hàm lõm (slide tr.45).', C)
mc('G', r(45), r'Hàm \(\log x\) trên \(\mathbb R_{++}\) là',
   'lõm', ['lồi', 'vừa lồi vừa lõm', 'không lồi cũng không lõm'],
   r'\((\log x)^{\prime\prime}=-1/x^2<0\): lõm. Do đó \(-\log x\) là lồi — hàm chắn (barrier) nổi tiếng trong phương pháp điểm trong.', C)
mc('G', r(33), r'Trường hợp một chiều, f khả vi hai lần là lồi khi và chỉ khi',
   r'\(\mathrm{dom}\,f\) lồi và \(f^{\prime\prime}(x)\ge0\ \forall x\)',
   [r'\(\mathrm{dom}\,f\) lồi và \(f^{\prime\prime}(x)\le0\ \forall x\)', r'\(\mathrm{dom}\,f\) lồi và \(f^{\prime}(x)\ge0\ \forall x\)', r'\(\mathrm{dom}\,f\) lồi và \(f(x)\ge0\ \forall x\)'],
   r'Slide tr.33: điều kiện cấp 2 trong \(\mathbb R\): \(f^{\prime\prime}\ge0\). \(f^{\prime}\ge0\) nói f đơn điệu tăng chứ không nói f lồi.', C)
mc('G', r(52), r'Trên đồ thị (epigraph) của \(f:\mathbb R^n\to\mathbb R\) là tập',
   r'\(\mathrm{epi}\,f=\{(x,t)\mid f(x)\le t\}\subseteq\mathbb R^{n+1}\)',
   [r'\(\{(x,f(x))\mid x\in\mathrm{dom}\,f\}\subseteq\mathbb R^{n+1}\)', r'\(\{x\in\mathrm{dom}\,f\mid f(x)\le0\}\subseteq\mathbb R^{n}\)', r'\(\{(x,t)\mid f(x)\ge t\}\subseteq\mathbb R^{n+1}\)'],
   r'Đồ thị (graph) là \(\{(x,f(x))\}\); epigraph là phần nằm <b>trên</b> hoặc trên đồ thị (slide tr.52). Chúng nằm trong \(\mathbb R^{n+1}\).', C)
mc('G', r(52), r'Đồ thị (graph) \(\{(x,f(x))\mid x\in\mathrm{dom}\,f\}\) nằm trong không gian',
   r'\(\mathbb R^{n+1}\)', [r'\(\mathbb R^n\)', r'\(\mathbb R^{2n}\)', r'\(\mathbb R\)'],
   r'Mỗi điểm gồm n tọa độ của x và 1 tọa độ giá trị f(x): tổng cộng \(n+1\) (slide tr.52).', C)
tf('S', r(52), r'Hàm f là lồi khi và chỉ khi epigraph của nó là một tập lồi.', True,
   r'Đây là cách nối giữa “tập lồi” và “hàm lồi” (Boyd 3.1.7): dây cung nằm trên đồ thị ⇔ epigraph lồi. Ta nên nhớ vì mọi tính chất tập lồi có thể áp dụng cho hàm.', C)
tf('S', r(25), r'Nếu f lồi thì mọi tập mức dưới \(\{x\mid f(x)\le c\}\) là tập lồi.', True,
   r'Lấy x, y với \(f(x),f(y)\le c\): \(f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)\le c\). Chiều ngược lại không đúng (hàm tựa lồi có tập mức lồi nhưng chưa chắc lồi).', C)
tf('S', r(25), r'Nếu mọi tập mức dưới \(\{x\mid f(x)\le c\}\) của f đều lồi thì f chắc chắn là hàm lồi.', False,
   r'Phản ví dụ: \(f(x)=\sqrt{|x|}\) hoặc \(f(x)=x^3\) trên \(\mathbb R\) có tập mức dưới là các khoảng (lồi) nhưng f không lồi.', C)
mc('S', r(25), r'Với \(f(x)=x^2\), \(x=-1\), \(y=3\), \(\theta=0.5\): giá trị \(f(\theta x+(1-\theta)y)\) và \(\theta f(x)+(1-\theta)f(y)\) lần lượt là',
   '1 và 5 (thỏa Jensen)', ['5 và 1 (vi phạm Jensen)', '1 và 1', '4 và 5'],
   r'\(\theta x+(1-\theta)y=1\), \(f(1)=1\); \(0.5\cdot1+0.5\cdot9=5\). Ta có \(1\le5\): đồ thị nằm dưới dây cung.', C)
num('S', r(25), r'Với \(f(x)=x^2\), \(x=-1\), \(y=3\), \(\theta=0.5\): tính hiệu \(\theta f(x)+(1-\theta)f(y)-f(\theta x+(1-\theta)y)\).', 4,
    r'\(5-1=4\ge0\): khoảng cách giữa dây cung và đồ thị tại điểm giữa.', ans_text='4', grp=C)
mc('S', r(25), r'Hàm \(f(x)=x^3\) trên \(\mathbb R\) không lồi vì',
   r'\(f^{\prime\prime}(x)=6x\) âm khi \(x<0\)', [r'\(f^{\prime\prime}(x)=6x\) luôn dương', r'f không liên tục', r'f không có cực tiểu nên không lồi'],
   r'\(f^{\prime\prime}(x)=6x<0\) với \(x<0\) nên điều kiện cấp 2 vi phạm. (Không có cực tiểu không phải là lý do: hàm \(e^x\) lồi nhưng không đạt cực tiểu.)', C)
mc('S', r(45), r'Hàm nào sau đây là lồi trên \(\mathbb R\)?',
   r'\(e^x-1\)', [r'\(-e^x\)', r'\(\sin x\)', r'\(x^3\)'],
   r'\((e^x-1)^{\prime\prime}=e^x>0\). \(-e^x\) lõm; \(\sin x\) đổi dấu đạo hàm cấp hai; \(x^3\) có \(f^{\prime\prime}=6x\) đổi dấu (bài tập slide tr.54, câu a).', C)

# =====================================================================  D. HESSIAN, XÁC ĐỊNH DƯƠNG (tr.28–51)
D = 'D. Hessian & ma trận xác định dương'
mc('G', r(28), r'Ma trận Hessian \(H(x)\) của \(f:\mathbb R^n\to\mathbb R\) có phần tử ở dòng i, cột j là',
   r'\(\dfrac{\partial^2f}{\partial x_i\partial x_j}\)', [r'\(\dfrac{\partial f}{\partial x_i}\dfrac{\partial f}{\partial x_j}\)', r'\(\dfrac{\partial f}{\partial x_i\partial x_j}\)', r'\(\dfrac{\partial^2f}{\partial x_i^2}\) trên mọi vị trí'],
   r'Hessian là ma trận các đạo hàm riêng cấp hai; đường chéo là \(\partial^2f/\partial x_i^2\) (slide tr.28).', D)
tf('S', r(28), r'Nếu f có các đạo hàm riêng cấp hai liên tục thì Hessian là ma trận đối xứng.', True,
   r'Định lý Schwarz/Clairaut: \(\partial^2f/\partial x_i\partial x_j=\partial^2f/\partial x_j\partial x_i\) khi các đạo hàm này liên tục.', D)
mc('G', r(31), r'Điều kiện cấp 2 cho hàm lồi: f khả vi hai lần là lồi khi và chỉ khi',
   r'\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\succeq0\ \forall x\in\mathrm{dom}\,f\)',
   [r'\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\preceq0\ \forall x\in\mathrm{dom}\,f\)', r'\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\) khả nghịch \(\forall x\in\mathrm{dom}\,f\)', r'\(\mathrm{dom}\,f\) lồi và \(\nabla f(x)\ne0\ \forall x\in\mathrm{dom}\,f\)'],
   r'Hessian phải <b>nửa xác định dương tại mọi điểm</b> của miền (slide tr.31). Nếu chỉ kiểm tại một điểm thì chưa đủ.', D)
tf('G', r(33), r'Nếu Hessian xác định dương tại mọi điểm của miền lồi thì f lồi chặt.', True,
   r'Slide tr.33: “Trong trường hợp ma trận Hessian là xác định dương, hàm số lồi chặt”.', D)
tf('S', r(33), r'Nếu f lồi chặt thì Hessian của f xác định dương tại mọi điểm.', False,
   r'Chiều ngược lại sai: \(f(x)=x^4\) lồi chặt nhưng \(f^{\prime\prime}(0)=0\) (Hessian nửa xác định dương chứ không xác định dương tại 0).', D)
mc('G', r(36), r'Ma trận đối xứng A là xác định dương (\(A\succ0\)) nếu',
   r'\(x^\top Ax>0\) với mọi vectơ \(x\ne0\)', [r'\(x^\top Ax\ge0\) với mọi x', r'\(\det A>0\)', r'mọi phần tử của A dương'],
   r'Đây là định nghĩa (slide tr.36). \(x^\top Ax\ge0\) là nửa xác định dương. \(\det A>0\) hay phần tử dương chưa đủ: \(\begin{pmatrix}1&2\\2&1\end{pmatrix}\) có phần tử dương nhưng \(\det=-3<0\).', D)
mc('G', r(36), r'Ma trận đối xứng A là nửa xác định dương (\(A\succeq0\)) nếu',
   r'\(x^\top Ax\ge0\) với mọi \(x\in\mathbb R^n\)', [r'\(x^\top Ax>0\) với mọi \(x\ne0\)', r'\(x^\top Ax\le0\) với mọi x', r'A có ít nhất một giá trị riêng dương'],
   r'Slide tr.36. Nhớ: xác định dương ⇒ nửa xác định dương (nhưng không ngược lại).', D)
tf('G', r(36), r'Mọi ma trận xác định dương đều là nửa xác định dương.', True, r'\(x^\top Ax>0\ \forall x\ne0\) kéo theo \(x^\top Ax\ge0\ \forall x\) (tại \(x=0\) bằng 0).', D)
mc('G', r(37), r'Ma trận \(A=I_2\) là xác định dương vì',
   r'\(x^\top Ax=x_1^2+x_2^2>0\) với mọi \(x\ne0\)', [r'\(\det A=1\) nên chắc chắn dương', r'các phần tử của A đều không âm', r'A là ma trận vuông'],
   r'Slide tr.37 tính trực tiếp dạng toàn phương. Hàm tương ứng \(f=x_1^2+x_2^2\) lồi.', D)
mc('G', r(38), r'Ma trận đối xứng A cỡ \(n\times n\) là xác định dương khi và chỉ khi (chọn tiêu chuẩn đúng)',
   r'mọi giá trị riêng dương (hoặc mọi minor dẫn đầu dương)',
   [r'có ít nhất một giá trị riêng dương và đường chéo dương', r'định thức của A dương và các phần tử ngoài đường chéo bằng 0', r'vết (trace) của A dương và A đối xứng'],
   r'Slide tr.38 nêu hai tiêu chuẩn: mọi giá trị riêng dương hoặc mọi định thức con chính (dẫn đầu) dương (tiêu chuẩn Sylvester). Tồn tại một giá trị riêng dương / det dương / trace dương đều chưa đủ.', D)
mc('G', r(41), r'Ma trận đối xứng A là nửa xác định dương khi và chỉ khi',
   'tất cả giá trị riêng không âm', ['tất cả định thức con chính dẫn đầu không âm', 'det A = 0', 'trace A ≥ 0'],
   r'Slide tr.41 nhấn mạnh: <b>không</b> thể dùng dấu các định thức con chính dẫn đầu để kiểm tra nửa xác định dương. Ví dụ \(\begin{pmatrix}0&0\\0&-1\end{pmatrix}\) có \(\Delta_1=0,\Delta_2=0\) (đều ≥ 0) nhưng có giá trị riêng \(-1\).', D)
tf('G', r(41), r'Để kiểm tra A nửa xác định dương, chỉ cần kiểm các định thức con chính dẫn đầu \(\Delta_1,\Delta_2,\dots\) đều \(\ge0\).', False,
   r'Sai (slide tr.41). Cần <b>mọi</b> minor chính (không chỉ dẫn đầu) \(\ge0\), hoặc dùng giá trị riêng. Phản ví dụ: \(\mathrm{diag}(0,-1)\).', D)
mc('S', r(41), r'Ma trận \(\begin{pmatrix}0&0\\0&-1\end{pmatrix}\): các minor dẫn đầu \(\Delta_1,\Delta_2\) lần lượt là',
   r'0 và 0, nhưng A KHÔNG nửa xác định dương',
   [r'0 và 0, vậy A nửa xác định dương (mọi minor ≥ 0)', r'0 và -1, vậy A xác định âm (Δ₂ < 0)', r'-1 và 0, vậy A xác định dương (Δ₁ đổi dấu)'],
   r'\(\Delta_1=0\), \(\Delta_2=\det=0\cdot(-1)-0=0\). Tuy vậy \(x^\top Ax=-x_2^2<0\) với \(x=(0,1)\); minor chính \(a_{22}=-1<0\) phát hiện ra điều đó.', D)
tf('S', r(41), r'Nếu A nửa xác định dương nhưng không xác định dương thì \(\det A=0\).', True,
   r'Nửa xác định dương ⇒ mọi giá trị riêng \(\ge0\); nếu không xác định dương thì có giá trị riêng bằng 0, do đó tích các giá trị riêng \(\det A=0\).', D)
mc('G', r(42), r'Hàm \(f(x_1,x_2)=x_1^2+x_2^2\) có Hessian \(H=\begin{pmatrix}2&0\\0&2\end{pmatrix}\), suy ra f là',
   r'lồi chặt, vì Hessian xác định dương',
   [r'lồi nhưng không chặt, vì Hessian chỉ nửa xác định dương', r'lõm, vì các phần tử đường chéo của Hessian dương', r'không lồi cũng không lõm, vì hai giá trị riêng bằng nhau'],
   r'Giá trị riêng của H đều bằng 2 > 0 nên \(H\succ0\) (slide tr.42).', D)
mc('G', r(46), r'Với \(f(x,y)=x^2+xy+y^2\), Hessian là',
   r'\(\begin{pmatrix}2&1\\1&2\end{pmatrix}\)', [r'\(\begin{pmatrix}2&2\\2&2\end{pmatrix}\)', r'\(\begin{pmatrix}1&1\\1&1\end{pmatrix}\)', r'\(\begin{pmatrix}2&0\\0&2\end{pmatrix}\)'],
   r'\(f_{xx}=2,\ f_{yy}=2,\ f_{xy}=1\). Giá trị riêng \(1\) và \(3\) (kiểm bằng code: ' + str(R['m1_mat']['P1']['eig']) + r'), nên \(H\succ0\) và f lồi chặt (slide tr.46, 49).', D)
num('G', r(46), r'Tính giá trị riêng lớn nhất của Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\) của \(f=x^2+xy+y^2\).', 3,
    r'Đa thức đặc trưng \((2-\lambda)^2-1=0\Rightarrow\lambda=1,3\). Giá trị lớn nhất là 3.', ans_text='3', grp=D)
tf('G', r(46), r'\(x^\top\!\begin{pmatrix}2&1\\1&2\end{pmatrix}x=2(x^2+xy+y^2)\ge0\), do đó \(f=x^2+xy+y^2\) là hàm lồi trên \(\mathbb R^2\).', True,
   r'Slide tr.46 chứng minh bằng chính đẳng thức này: \(x^2+xy+y^2=\tfrac12[(x+y)^2+x^2+y^2]\ge0\), và bằng 0 chỉ tại \((0,0)\).', D)
mc('G', r(48), r'Hàm toàn phương \(f(x)=\tfrac12x^\top Px+q^\top x+r\) (P đối xứng) có Hessian bằng',
   r'\(\nabla^2f(x)=P\), hằng số theo x',
   [r'\(\nabla^2f(x)=Px+q\), phụ thuộc x tuyến tính', r'\(\nabla^2f(x)=\tfrac12P\), do có hệ số \(\tfrac12\) ở đầu', r'\(\nabla^2f(x)=q\), là vectơ hệ số bậc nhất'],
   r'\(\nabla f=Px+q\), \(\nabla^2f=P\). Vì vậy f lồi khi và chỉ khi \(P\succeq0\) (slide tr.48).', D)
mc('G', r(48), r'Hàm toàn phương \(f(x)=\tfrac12x^\top Px+q^\top x+r\) là lồi khi và chỉ khi',
   r'\(P\succeq0\)', [r'\(q=0\)', r'\(r\ge0\)', r'\(\det P>0\)'],
   r'Chỉ ma trận P (phần bậc hai) quyết định tính lồi; vectơ q và hằng số r chỉ tịnh tiến/nâng đồ thị.', D)
tf('G', r(50), r'Hàm tuyến tính \(f(x)=a^\top x\) vừa lồi vừa lõm.', True, r'Hessian bằng ma trận không, vừa \(\succeq0\) vừa \(\preceq0\).', D)
tf('G', r(51), r'Hàm \(f(x,y)=\sqrt{x^2+y^2}\) (chuẩn Euclid) là hàm lồi trên \(\mathbb R^2\).', True,
   r'Slide tr.51. Chuẩn nào cũng lồi vì bất đẳng thức tam giác và tính thuần nhất: \(\|\theta x+(1-\theta)y\|\le\theta\|x\|+(1-\theta)\|y\|\).', D)
tf('G', r(51), r'Hàm \(f(x,y)=x^2/y\) là lồi trên \(\mathrm{dom}\,f=\{(x,y)\mid y>0\}\).', True,
   r'Hessian \(\dfrac{2}{y^3}\begin{pmatrix}y^2&-xy\\-xy&x^2\end{pmatrix}\) nửa xác định dương khi \(y>0\) (\(\det=0\), vết \(>0\)). Kiểm bằng code tại các điểm mẫu: giá trị riêng \(\ge0\).', D)
mc('S', r(48), r'Hàm \(f(x,y)=x^2-y^2\) có Hessian \(\mathrm{diag}(2,-2)\). Nhận xét nào đúng?',
   r'không lồi cũng không lõm (Hessian không xác định)',
   [r'lồi chặt (Hessian xác định dương)', r'lõm chặt (Hessian xác định âm)', r'lồi nhưng không chặt (Hessian nửa xác định dương)'],
   r'Giá trị riêng \(2\) và \(-2\) trái dấu: điểm yên ngựa; \(f\) tăng theo x, giảm theo y.', D)
mc('S', r(38), r'Ma trận \(\begin{pmatrix}6&-4\\-4&6\end{pmatrix}\) (Hessian của \(3x_1^2+3x_2^2-4x_1x_2\)) là',
   'xác định dương (giá trị riêng 2 và 10)', ['nửa xác định dương nhưng không xác định dương', 'không xác định', 'xác định âm'],
   r'\(\Delta_1=6>0\), \(\Delta_2=36-16=20>0\); giá trị riêng \(2,10>0\). Hàm lồi chặt (bài tập tham khảo Studocu C8).', D)
num('T', 'Studocu C8', r'Tính định thức của Hessian của \(f(x_1,x_2)=3x_1^2+3x_2^2-4x_1x_2\).', 20,
    r'Hessian \(\begin{pmatrix}6&-4\\-4&6\end{pmatrix}\): \(\det=36-16=20>0\) và \(\Delta_1=6>0\) ⇒ xác định dương ⇒ f lồi.', ans_text='20', grp=D)
mc('T', 'Studocu C8', r'Hàm \(f(x_1,x_2)=4x_1^2+x_2^2-x_1-2x_2\) là lồi vì',
   r'Hessian \(\mathrm{diag}(8,2)\) xác định dương',
   [r'f có điểm cực tiểu nên hàm lồi (suy luận sai)', r'f không có số hạng chéo \(x_1x_2\) nên chắc chắn lồi', r'Hessian bằng \(\mathrm{diag}(4,1)\), dương (đạo hàm sai)'],
   r'\(f_{11}=8\), \(f_{22}=2\), \(f_{12}=0\). Hessian đường chéo dương ⇒ xác định dương. Nhớ đạo hàm cấp hai của \(4x_1^2\) là 8, không phải 4.', D)
mc('S', r(30), r'Với ma trận \(A\) cỡ 3×3, \(\Delta_2\) (định thức con chính cấp 2 dẫn đầu) là',
   'định thức của ma trận con góc trên bên trái cỡ 2×2', ['định thức của ma trận con góc dưới bên phải cỡ 2×2', 'tổng hai phần tử đầu đường chéo', r'bình phương của \(a_{22}\)'],
   r'Slide tr.30: \(H_k\) là ma trận con phía trên bên trái cỡ \(k\times k\) và \(\Delta_k=\det H_k\).', D)
tf('S', r(38), r'Ma trận đối xứng có mọi giá trị riêng dương thì mọi phần tử trên đường chéo của nó dương.', True,
   r'\(a_{ii}=e_i^\top Ae_i>0\) vì \(A\succ0\). (Chiều ngược lại không đúng.)', D)
tf('S', r(38), r'Ma trận đối xứng có mọi phần tử dương thì chắc chắn xác định dương.', False,
   r'Phản ví dụ \(\begin{pmatrix}1&2\\2&1\end{pmatrix}\): giá trị riêng \(3\) và \(-1\).', D)

# =====================================================================  E. PHÉP BẢO TOÀN, BÀI TẬP (tr.53–54)
E = 'E. Phép toán bảo toàn & bài tập'
mc('G', r(53), r'Phép toán nào sau đây KHÔNG được slide liệt kê là bảo toàn tính lồi?',
   r'\(\min\{f(x),g(x)\}\) của hai hàm lồi',
   [r'\(\alpha f(x)\) với hằng số \(\alpha>0\)', r'tổng \(f(x)+g(x)\) của hai hàm lồi', r'\(\max\{f(x),g(x)\}\) của hai hàm lồi'],
   r'Slide tr.53: nhân dương, cộng, lấy max giữ nguyên tính lồi. Lấy <b>min</b> của hai hàm lồi nói chung không lồi (ví dụ \(\min\{x^2,(x-2)^2\}\)).', E)
tf('G', r(53), r'Nếu \(f\) và \(g\) lồi thì \(h(x)=\max\{f(x),g(x)\}\) lồi.', True,
   r'Với mỗi \(\theta\): \(h(\theta x+(1-\theta)y)=\max\{f(\cdot),g(\cdot)\}\le\max\{\theta f(x)+(1-\theta)f(y),\ \theta g(x)+(1-\theta)g(y)\}\le\theta h(x)+(1-\theta)h(y)\). (Studocu C1 mở rộng ra max của n hàm.)', E)
tf('G', r(53), r'Nếu \(f\) lồi và \(\alpha>0\) thì \(\alpha f\) lồi; nếu \(\alpha<0\) thì \(\alpha f\) lõm.', True,
   r'Nhân hệ số dương giữ chiều bất đẳng thức Jensen; hệ số âm đảo chiều (được hàm lõm).', E)
tf('S', r(53), r'Hiệu \(f-g\) của hai hàm lồi luôn là hàm lồi.', False,
   r'Ví dụ \(f=x^2\), \(g=2x^2\): \(f-g=-x^2\) lõm. Phép trừ không bảo toàn tính lồi.', E)
tf('S', r(53), r'Nếu \(f\) lồi và \(g(x)=f(Ax+b)\) (A, b cố định) thì g lồi.', True,
   r'Hợp thành với ánh xạ affine bảo toàn tính lồi (Boyd 3.2.2). Ví dụ: \(\|Ax-b\|_2^2\) lồi vì hợp của bình phương chuẩn (lồi) với ánh xạ affine.', E)
tf('S', r(53), r'Hàm khoảng cách \(d(x;\Omega)=\inf_{y\in\Omega}\|x-y\|\) tới một tập lồi \(\Omega\) khác rỗng là hàm lồi (Studocu C2).', True,
   r'Với \(x_1,x_2\) và \(\varepsilon>0\) chọn \(y_i\in\Omega\) với \(\|x_i-y_i\|\le d(x_i)+\varepsilon\). Khi đó \(z=\theta y_1+(1-\theta)y_2\in\Omega\) và \(d(\theta x_1+(1-\theta)x_2)\le\|\theta(x_1-y_1)+(1-\theta)(x_2-y_2)\|\le\theta d(x_1)+(1-\theta)d(x_2)+\varepsilon\). Cho \(\varepsilon\to0\).', E)
mc('B', r(54), r'Bài tập slide tr.54(a): \(f(x)=e^x-1\) trên \(\mathbb R\) là',
   'lồi', ['lõm', 'vừa lồi vừa lõm', 'không lồi cũng không lõm'],
   r'\(f^{\prime\prime}(x)=e^x>0\) với mọi x ⇒ lồi (thậm chí lồi chặt).', E)
mc('B', r(54), r'Bài tập slide tr.54(b): \(f(x,y)=xy\) trên \(\mathbb R^2_{++}\) là',
   'không lồi cũng không lõm', ['lồi', 'lõm', 'lồi chặt'],
   r'Hessian \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\) có giá trị riêng \(-1\) và \(1\) (kiểm bằng code) tại mọi điểm ⇒ Hessian không xác định ⇒ f không lồi (có giá trị riêng âm) và không lõm (có giá trị riêng dương).', E)
mc('B', r(54), r'Bài tập slide tr.54(c): \(f(x,y)=1/(xy)\) trên \(\mathbb R^2_{++}\) là',
   'lồi', ['lõm', 'không lồi cũng không lõm', 'vừa lồi vừa lõm'],
   r'\(\nabla^2f=\begin{pmatrix}2/(x^3y)&1/(x^2y^2)\\1/(x^2y^2)&2/(xy^3)\end{pmatrix}\); \(\det=3/(x^4y^4)>0\) và \(f_{xx}>0\) ⇒ xác định dương. (Kiểm số bằng code tại 4 điểm: mọi giá trị riêng > 0.)', E)
mc('B', r(54), r'Bài tập slide tr.54(d): \(f(x,y)=x/y\) trên \(\mathbb R^2_{++}\) là',
   'không lồi cũng không lõm', ['lồi', 'lõm', 'lồi chặt'],
   r'\(\nabla^2f=\begin{pmatrix}0&-1/y^2\\-1/y^2&2x/y^3\end{pmatrix}\), \(\det=-1/y^4<0\) ⇒ giá trị riêng trái dấu ⇒ không lồi, không lõm.', E)
num('B', r(54), r'Với \(f(x,y)=1/(xy)\) tại điểm \((1,1)\), tính giá trị riêng nhỏ nhất của Hessian.', 1,
    r'Tại \((1,1)\): \(\nabla^2f=\begin{pmatrix}2&1\\1&2\end{pmatrix}\) ⇒ giá trị riêng 1 và 3; nhỏ nhất là 1 (> 0 nên tại điểm này Hessian xác định dương).', ans_text='1', grp=E)
num('B', r(54), r'Với \(f(x,y)=x/y\) tại \((1,1)\), tính định thức của Hessian.', -1,
    r'Hessian \(\begin{pmatrix}0&-1\\-1&2\end{pmatrix}\): \(\det=0\cdot2-(-1)(-1)=-1<0\) ⇒ không nửa xác định dương.', ans_text='-1', grp=E)
essay('B', r(54), r'Bài tập slide tr.54: xác định các hàm sau lồi hay lõm: \(e^x-1\) trên \(\mathbb R\); \(xy\), \(1/(xy)\), \(x/y\) trên \(\mathbb R^2_{++}\). Trình bày lời giải bằng Hessian.',
      r'<p>(a) \(f^{\prime\prime}=e^x>0\): lồi (chặt).</p><p>(b) \(f=xy\): \(H=\begin{pmatrix}0&1\\1&0\end{pmatrix}\), \(\det=-1<0\) ⇒ giá trị riêng trái dấu ⇒ không lồi, không lõm.</p><p>(c) \(f=1/(xy)\): \(f_{xx}=\tfrac{2}{x^3y}\), \(f_{yy}=\tfrac{2}{xy^3}\), \(f_{xy}=\tfrac1{x^2y^2}\). \(\Delta_1=f_{xx}>0\), \(\Delta_2=\tfrac{4}{x^4y^4}-\tfrac{1}{x^4y^4}=\tfrac{3}{x^4y^4}>0\) ⇒ \(H\succ0\): lồi chặt.</p><p>(d) \(f=x/y\): \(f_{xx}=0\), \(f_{xy}=-\tfrac1{y^2}\), \(f_{yy}=\tfrac{2x}{y^3}\). \(\Delta_2=-\tfrac1{y^4}<0\) ⇒ Hessian không xác định ⇒ không lồi, không lõm.</p>',
      ['Tính đủ 4 đạo hàm riêng cấp hai', 'Dùng Δ₂ = det để kết luận dấu giá trị riêng', r'Nêu rõ miền \(\mathbb R^2_{++}\)'], E)
essay('T', 'Studocu C1', r'Cho \(f_1,\dots,f_n:\mathbb R^n\to\mathbb R\) lồi. Chứng minh \(g(x)=\max_i f_i(x)\) là hàm lồi.',
      r'<p>Với mỗi \(i\): \(f_i(\theta x+(1-\theta)y)\le\theta f_i(x)+(1-\theta)f_i(y)\le\theta g(x)+(1-\theta)g(y)\) vì \(f_i\le g\). Lấy max theo i vế trái: \(g(\theta x+(1-\theta)y)\le\theta g(x)+(1-\theta)g(y)\). Vậy g lồi.</p>',
      [r'Đánh giá từng \(f_i\) bằng g', 'Lấy max theo i ở vế trái'], E)
essay('T', 'Studocu C3', r'Cho \(\Omega_1,\Omega_2\) lồi. Chứng minh \(\Omega=\Omega_1+\Omega_2\) lồi. Minh họa trong \(\mathbb R\).',
      r'<p>Lấy \(x=x_1+x_2\), \(y=y_1+y_2\) (\(x_i,y_i\in\Omega_i\)). Khi đó \(\theta x+(1-\theta)y=[\theta x_1+(1-\theta)y_1]+[\theta x_2+(1-\theta)y_2]\in\Omega_1+\Omega_2\). Ví dụ \(\Omega_1=[0,1]\), \(\Omega_2=[2,4]\) ⇒ \(\Omega=[2,5]\).</p>',
      ['Tách thành hai thành phần', 'Ví dụ số cụ thể'], E)
essay('T', 'Studocu C5', r'Cho \(\Omega\) lồi. Chứng minh \(k\Omega=\{kx\mid x\in\Omega\}\) (với \(k\ge0\)) là lồi.',
      r'<p>Lấy \(u=kx\), \(v=ky\) với \(x,y\in\Omega\). \(\theta u+(1-\theta)v=k(\theta x+(1-\theta)y)\in k\Omega\) vì \(\theta x+(1-\theta)y\in\Omega\).</p>',
      ['Đặt thừa số k ra ngoài', 'Dùng tính lồi của Ω'], E)
essay('T', 'Studocu C7', r'Nêu định nghĩa hàm lồi và cho một ví dụ hàm lồi, một ví dụ hàm không lồi.',
      r'<p>f lồi nếu \(\mathrm{dom}\,f\) lồi và \(f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)\) với mọi \(x,y\in\mathrm{dom}\,f\), \(\theta\in[0,1]\). Ví dụ lồi: \(x^2\), \(e^x\), \(|x|\). Ví dụ không lồi: \(x^3\): với \(x=-1,\ y=0,\ \theta=\tfrac12\) ta có \(f(-\tfrac12)=-0.125\) nhưng \(\theta f(x)+(1-\theta)f(y)=-0.5\); vì \(-0.125>-0.5\) nên Jensen bị vi phạm.</p>',
      ['Đủ hai điều kiện: miền lồi và Jensen', 'Ví dụ phản chứng có số cụ thể'], E)
essay('S', r(48), r'Chứng minh hàm toàn phương \(f(x)=\tfrac12x^\top Px+q^\top x+r\) lồi khi và chỉ khi \(P\succeq0\).',
      r'<p>\(\nabla f(x)=Px+q\) (P đối xứng), \(\nabla^2f(x)=P\) với mọi x. Theo điều kiện cấp 2, f lồi ⇔ \(\nabla^2f(x)\succeq0\ \forall x\) ⇔ \(P\succeq0\).</p>',
      ['Tính Hessian', 'Áp dụng điều kiện cấp 2'], D)

# =====================================================================  F. NĂNG LỰC KẾT HỢP (biên soạn ít, khi thật cần)
F = 'F. Vận dụng'
mc('S', r(31), r'Để chứng minh \(f(x)=x_1^2+x_1x_2+x_2^2+3x_1\) lồi trên \(\mathbb R^2\), bước quyết định là',
   r'tính Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\) và chứng minh \(\succ0\)',
   [r'chỉ ra \(\nabla f(0)=0\) rồi kết luận có cực tiểu', r'tính \(f(0,0)=0\) và thấy f không âm ở gốc', r'chỉ ra f không âm trên toàn \(\mathbb R^2\)'],
   r'Số hạng \(3x_1\) tuyến tính nên không ảnh hưởng Hessian. Hessian trùng với hàm ở slide tr.46 ⇒ xác định dương ⇒ lồi.', F)
mc('S', r(48), r'Hàm \(f(x)=\tfrac12x^\top Px\) với \(P=\begin{pmatrix}1&1\\1&1\end{pmatrix}\) là',
   r'lồi nhưng không lồi chặt',
   [r'lồi chặt vì \(P\) có phần tử dương', r'lõm vì \(P\) có phần tử ngoài đường chéo', r'không lồi vì \(\det P=0\)'],
   r'\(P\) có giá trị riêng \(0\) và \(2\) ⇒ \(P\succeq0\) nhưng không \(\succ0\). \(f=\tfrac12(x_1+x_2)^2\) không đổi dọc hướng \((1,-1)\), nên không lồi chặt.', F)
mc('S', r(48), r'Hàm \(f(x)=-x_1^2-x_2^2\) là',
   'lõm chặt', ['lồi chặt', 'lồi nhưng không chặt', 'không lồi cũng không lõm'],
   r'\(-f=x_1^2+x_2^2\) lồi chặt ⇒ f lõm chặt (slide tr.25).', F)
num('S', r(46), r'Cho \(f(x,y)=x^2+xy+y^2\). Tính \(f(1,-1)\) và cho biết giá trị (dương). Đây là giá trị của \(\tfrac12x^\top Hx\) tại \((1,-1)\).', 1,
    r'\(f(1,-1)=1-1+1=1\). Đối chiếu: \(\tfrac12(1,-1)\begin{pmatrix}2&1\\1&2\end{pmatrix}(1,-1)^\top=\tfrac12\cdot2=1\).', ans_text='1', grp=F)
mc('S', r(45), r'Tập mức dưới \(\{x\in\mathbb R\mid x^2\le4\}\) của hàm lồi \(x^2\) là',
   r'đoạn \([-2,2]\) (lồi)', [r'hai điểm \(\{-2,2\}\)', r'tập \((-\infty,-2]\cup[2,\infty)\)', r'tập rỗng'],
   r'\(x^2\le4\Leftrightarrow|x|\le2\): đoạn lồi. Đây là ví dụ tập mức dưới của hàm lồi.', F)
mc('S', r(25), r'Trong các mệnh đề sau, mệnh đề nào SAI?',
   r'Hàm lồi khả vi luôn đạt cực tiểu toàn cục',
   [r'Hàm tuyến tính \(a^\top x\) là hàm lồi trên \(\mathbb R^n\)', r'Tổng hai hàm lồi trên cùng miền là hàm lồi', r'Hàm \(e^x\) là hàm lồi trên toàn \(\mathbb R\)'],
   r'\(e^x\) lồi khả vi nhưng không đạt cực tiểu (giá trị nhỏ nhất \(0\) chỉ là infimum, không đạt). Tính lồi không bảo đảm sự tồn tại nghiệm.', F)
mc('S', r(27), r'Nếu \(f\) lồi khả vi và tồn tại x sao cho \(\nabla f(x)^\top(y-x)\ge0\) với mọi y thuộc tập lồi C, thì',
   r'x là điểm cực tiểu của f trên C', [r'x là điểm cực đại của f trên C', r'f hằng trên C', r'x nằm trên biên của C'],
   r'Từ \(f(y)\ge f(x)+\nabla f(x)^\top(y-x)\ge f(x)\). Đây là điều kiện tối ưu cho bài toán lồi có ràng buộc tập (Boyd 4.2.3), tổng quát hóa của \(\nabla f=0\).', F)

# =====================================================================  G. MỆNH ĐỀ SAI THƯỜNG GẶP (đối trọng với các câu đúng phía trên; biến thể của mệnh đề trong slide)
G = 'G. Mệnh đề dễ nhầm'
tf('G', r(3), r'Tập \(\{\theta x+(1-\theta)y\mid\theta\in[0,1]\}\) là đường thẳng đi qua x và y.', False,
   r'Với \(\theta\in[0,1]\) ta chỉ được <b>đoạn thẳng</b> nối x và y; đường thẳng cần \(\theta\in\mathbb R\) (slide tr.3).', G)
tf('G', r(7), r'Tập \(C\) là lồi nếu với mọi \(x,y\in C\) và mọi \(\theta\in\mathbb R\) thì \(\theta x+(1-\theta)y\in C\).', False,
   r'Điều kiện đó (mọi \(\theta\in\mathbb R\)) đòi hỏi C chứa cả đường thẳng qua hai điểm: đó là tập <b>affine</b>, mạnh hơn lồi. Tập lồi chỉ cần \(\theta\in[0,1]\).', G)
tf('G', r(7), r'Tập rỗng không phải là tập lồi vì không có điểm nào để kiểm tra.', False,
   r'Slide tr.7 quy ước tập rỗng là lồi: điều kiện “với mọi x, y thuộc C” đúng theo nghĩa rỗng.', G)
tf('G', r(9), r'Nếu \(S_1\), \(S_2\) lồi thì \(S_1\cup S_2\) lồi.', False, r'Sai: \([0,1]\cup[2,3]\) không chứa \(1.5\) (slide tr.9).', G)
tf('G', r(11), r'Bao lồi của C là tập lồi lớn nhất nằm trong C.', False, r'Bao lồi là tập lồi <b>nhỏ nhất chứa</b> C, không phải lớn nhất nằm trong C.', G)
tf('G', r(11), r'Điểm \(\theta_1x_1+\dots+\theta_kx_k\) với \(\sum\theta_i=1\) (hệ số có thể âm) là tổ hợp lồi của \(x_1,\dots,x_k\).', False,
   r'Tổ hợp lồi cần thêm \(\theta_i\ge0\). Nếu cho phép hệ số âm ta được tổ hợp <i>affine</i>.', G)
tf('G', r(14), r'Nửa không gian đóng \(\{x\mid a^\top x\le b\}\) không phải là tập lồi.', False, r'Nếu \(a^\top x\le b\), \(a^\top y\le b\) thì \(a^\top(\theta x+(1-\theta)y)\le b\): nửa không gian là lồi.', G)
tf('G', r(14), r'Siêu phẳng \(\{x\mid a^\top x=b\}\) có thể được xác định với \(a=0\).', False, r'Slide tr.14 yêu cầu \(a\ne0\). Với \(a=0\) tập là rỗng (nếu \(b\ne0\)) hoặc toàn không gian (nếu \(b=0\)), không phải siêu phẳng.', G)
tf('G', r(17), r'Chuẩn Euclid của \(v\) được tính bằng \(v_1^2+v_2^2+\dots+v_n^2\) (không có căn bậc hai).', False, r'Đó là bình phương chuẩn. Chuẩn là \(\sqrt{v_1^2+\dots+v_n^2}\) (slide tr.17).', G)
tf('G', r(18), r'Hình cầu \(B(x_c,r)=\{x\mid\|x-x_c\|\le r\}\) không phải là tập lồi.', False, r'Bất đẳng thức tam giác cho \(\|\theta x+(1-\theta)y-x_c\|\le\theta\|x-x_c\|+(1-\theta)\|y-x_c\|\le r\): hình cầu lồi.', G)
tf('G', r(22), r'Miền chấp nhận của một bài toán QHTT không phải polyhedron.', False, r'Hệ \(Ax\le b,\ Cx=d\) chính là định nghĩa polyhedron (slide tr.22).', G)
tf('G', r(22), r'Mọi polyhedron đều là polytope.', False, r'Polytope là polyhedron <b>bị chặn</b>. Góc phần tư \(\{x\ge0\}\) là polyhedron không bị chặn.', G)
tf('G', r(25), r'Hàm f là lồi nếu \(f(\theta x+(1-\theta)y)\ge\theta f(x)+(1-\theta)f(y)\).', False, r'Chiều “≥” là hàm <b>lõm</b>. Hàm lồi có “≤” (Jensen, slide tr.25).', G)
tf('G', r(25), r'Hàm tuyến tính \(a^\top x\) là lồi chặt.', False, r'Với hàm tuyến tính Jensen luôn xảy ra dấu “=”, không chặt: nó lồi và lõm nhưng không lồi chặt hay lõm chặt.', G)
tf('G', r(25), r'Nếu \(f\) lồi thì \(-f\) cũng lồi.', False, r'Nếu f lồi thì \(-f\) lõm (định nghĩa slide tr.25). \(-f\) chỉ lồi khi f vừa lồi vừa lõm (hàm affine).', G)
tf('G', r(26), r'Với hàm lồi một biến, dây cung nối hai điểm trên đồ thị nằm phía dưới đồ thị.', False, r'Dây cung nằm <b>trên</b> đồ thị (hoặc trùng). Nằm dưới là trường hợp hàm lõm (slide tr.26).', G)
tf('G', r(27), r'Điều kiện cấp 1 nói \(f(y)\le f(x)+\nabla f(x)^\top(y-x)\) với mọi x, y đối với hàm lồi khả vi.', False, r'Chiều đúng là “≥”: đồ thị nằm trên tiếp tuyến/mặt phẳng tiếp xúc (slide tr.27).', G)
tf('G', r(33), r'Trong \(\mathbb R\), f khả vi hai lần là lồi khi và chỉ khi \(f^{\prime\prime}(x)\le0\) với mọi x.', False, r'Điều kiện là \(f^{\prime\prime}(x)\ge0\). \(f^{\prime\prime}\le0\) ứng với hàm lõm.', G)
tf('G', r(36), r'Ma trận đối xứng A có \(\det A>0\) thì A xác định dương.', False, r'Phản ví dụ: \(A=-I_2\) có \(\det=1>0\) nhưng xác định âm. Cần mọi minor dẫn đầu dương, không chỉ \(\det\).', G)
tf('G', r(36), r'Ma trận xác định dương không phải là nửa xác định dương.', False, r'Xác định dương ⇒ nửa xác định dương (\(x^\top Ax>0\ \forall x\ne0\) kéo theo \(\ge0\)).', G)
tf('G', r(38), r'A đối xứng là xác định dương khi và chỉ khi có ít nhất một giá trị riêng dương.', False, r'Phải là <b>tất cả</b> giá trị riêng dương. \(\mathrm{diag}(1,-1)\) có giá trị riêng dương nhưng không xác định dương.', G)
tf('G', r(42), r'Hessian \(\mathrm{diag}(2,2)\) cho biết \(x_1^2+x_2^2\) chỉ lồi, không lồi chặt.', False, r'\(\mathrm{diag}(2,2)\succ0\) nên hàm lồi <b>chặt</b> (slide tr.42).', G)
tf('G', r(46), r'Hàm \(x^2+xy+y^2\) không lồi vì có số hạng chéo \(xy\).', False, r'Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\) có giá trị riêng 1 và 3, xác định dương ⇒ lồi chặt. Số hạng chéo không tự làm mất tính lồi.', G)
tf('G', r(48), r'Tính lồi của hàm toàn phương \(\tfrac12x^\top Px+q^\top x+r\) phụ thuộc vào vectơ q.', False, r'Hessian bằng P, không phụ thuộc q hay r; tính lồi ⇔ \(P\succeq0\) (slide tr.48).', G)
tf('G', r(53), r'Nếu f, g lồi thì \(\min\{f,g\}\) lồi.', False, r'Chỉ \(\max\{f,g\}\) được bảo toàn. Ví dụ \(\min\{x^2,(x-2)^2\}\) có hai đáy nên không lồi.', G)
tf('G', r(53), r'Nếu \(f\) và \(g\) lồi thì \(f-g\) lồi.', False, r'Phản ví dụ \(f=x^2,g=2x^2\Rightarrow f-g=-x^2\) lõm.', G)
tf('G', r(45), r'Hàm \(\log x\) là lồi trên \(\mathbb R_{++}\).', False, r'\((\log x)^{\prime\prime}=-1/x^2<0\): \(\log x\) lõm (slide tr.45).', G)
tf('G', r(54), r'Hàm \(f(x,y)=xy\) là lồi trên \(\mathbb R^2_{++}\) vì các đạo hàm riêng cấp hai \(f_{xx}=f_{yy}=0\) không âm.', False, r'Phải xét cả đạo hàm chéo: \(H=\begin{pmatrix}0&1\\1&0\end{pmatrix}\) có giá trị riêng \(-1\) ⇒ không nửa xác định dương ⇒ không lồi.', G)
tf('G', r(54), r'Hàm \(f(x,y)=x/y\) trên \(\mathbb R^2_{++}\) là hàm lồi.', False, r'\(\det H=-1/y^4<0\) ⇒ giá trị riêng trái dấu ⇒ không lồi, không lõm.', G)
tf('G', r(52), r'Epigraph của f là tập các điểm nằm <b>dưới</b> đồ thị của f.', False, r'Epi = “ở trên”: \(\{(x,t)\mid f(x)\le t\}\), tức các điểm nằm trên hoặc trên đồ thị.', G)
tf('G', r(41), r'Nếu A nửa xác định dương và \(\det A>0\) thì A vẫn có thể có giá trị riêng bằng 0.', False, r'\(\det A=\prod\lambda_i>0\) loại trừ giá trị riêng 0; khi đó mọi \(\lambda_i>0\) và A xác định dương.', G)
