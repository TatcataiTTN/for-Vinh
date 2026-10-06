# Cân bằng độ dài đáp án (không thêm chữ vô nghĩa: mỗi đáp án nhiễu là một hiểu sai có thật)
import re
p='q_m1.py'; s=open(p,encoding='utf-8').read()
R=[
 ("tập tất cả các tổ hợp lồi của các điểm thuộc C","tập tất cả các tổ hợp lồi của các điểm thuộc C",
  ["giao của tất cả các hình cầu chứa toàn bộ tập C","tập các điểm nằm trên biên của tập C cùng với tâm","tập lồi lớn nhất còn nằm hoàn toàn trong C"]),
 (r"\(B(x_c,r)=\{x\mid\|x-x_c\|\le r\}\)",r"\(B(x_c,r)=\{x\mid\|x-x_c\|\le r\}\)",
  [r"\(\{x\mid\|x-x_c\|=r\}\) (chỉ phần mặt cầu)",r"\(\{x\mid\|x\|\le r\}\) (luôn có tâm ở gốc)",r"\(\{x\mid\|x-x_c\|\ge r\}\) (phần ngoài cầu)"]),
 ("ma trận đối xứng và nửa xác định dương","ma trận đối xứng và nửa xác định dương",
  ["ma trận đường chéo với các phần tử bất kỳ","ma trận đơn vị (khi đó chỉ được hình cầu)","ma trận vuông bất kỳ có định thức bằng 1"]),
 ("tập nghiệm của một hệ hữu hạn đẳng thức và bất đẳng thức tuyến tính","tập nghiệm của hệ hữu hạn đẳng thức và bất đẳng thức tuyến tính",
  ["giao của một số hữu hạn các hình cầu đóng","bao lồi của một tập vô hạn các điểm bất kỳ","tập nghiệm của một bất đẳng thức bậc hai duy nhất"]),
 ("polytope (đa diện lồi bị chặn) — tam giác","polytope (đa diện lồi bị chặn): tam giác",
  ["polyhedron nhưng không bị chặn (nửa mặt phẳng)","tập không lồi vì có ba đỉnh nhọn","hình cầu đóng trong chuẩn \\(\\ell_1\\)"]),
 ("polyhedron nhưng KHÔNG phải polytope","polyhedron nhưng KHÔNG phải polytope",
  ["polytope, vì chỉ có hai ràng buộc","tập không lồi vì có góc vuông","một siêu phẳng vì có hai ràng buộc"]),
 (r"một điểm \((0.5,0.5)\) — vẫn là polyhedron",r"một điểm \((0.5,0.5)\), vẫn là polyhedron",
  ["tập rỗng vì hai đường thẳng song song",r"một đường thẳng nằm trong \(\mathbb R^2\)",r"toàn bộ mặt phẳng \(\mathbb R^2\) vì có hai ẩn"]),
 (r"\(\mathrm{dom}\,f\) lồi và \(f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)\)",r"\(\mathrm{dom}\,f\) lồi và \(f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)\)",
  [r"\(f(\theta x+(1-\theta)y)\ge\theta f(x)+(1-\theta)f(y)\) với mọi \(\theta\)",r"\(f\) liên tục và khả vi trên toàn miền xác định",r"\(f(x+y)=f(x)+f(y)\) với mọi \(x,y\)"]),
 (r"bất đẳng thức Jensen là bất đẳng thức chặt (<) với mọi \(x\ne y\), \(\theta\in(0,1)\)","Jensen là bất đẳng thức chặt (<) với mọi \\(x\\ne y\\)",
  ["f là hàm lồi, liên tục và có đạo hàm liên tục","f là hàm lồi và bị chặn dưới trên toàn miền","f có Hessian bằng ma trận không tại mọi điểm"]),
 ("dây cung nối hai điểm bất kỳ trên đồ thị luôn nằm phía trên (hoặc trùng) đồ thị","dây cung nối hai điểm trên đồ thị nằm phía trên đồ thị",
  ["tiếp tuyến tại mọi điểm luôn nằm phía trên đồ thị","đồ thị có đúng một điểm cực tiểu địa phương","đồ thị luôn đi qua gốc tọa độ và đối xứng"]),
 (r"\(f(y)\ge f(x)+\nabla f(x)^\top(y-x)\) với mọi \(x,y\in\mathrm{dom}\,f\)",r"\(f(y)\ge f(x)+\nabla f(x)^\top(y-x)\) với mọi \(x,y\in\mathrm{dom}\,f\)",
  [r"\(f(y)\le f(x)+\nabla f(x)^\top(y-x)\) với mọi \(x,y\in\mathrm{dom}\,f\)",r"\(\nabla f(x)^\top(y-x)\ge0\) với mọi \(x,y\in\mathrm{dom}\,f\)",r"\(\nabla f(x)=0\) tại mọi điểm \(x\in\mathrm{dom}\,f\)"]),
 (r"\(\mathrm{dom}\,f\) lồi và \(f^{\prime\prime}(x)\ge0\) với mọi x",r"\(\mathrm{dom}\,f\) lồi và \(f^{\prime\prime}(x)\ge0\ \forall x\)",
  [r"\(\mathrm{dom}\,f\) lồi và \(f^{\prime\prime}(x)\le0\ \forall x\)",r"\(\mathrm{dom}\,f\) lồi và \(f^{\prime}(x)\ge0\ \forall x\)",r"\(\mathrm{dom}\,f\) lồi và \(f(x)\ge0\ \forall x\)"]),
 (r"\(\mathrm{epi}\,f=\{(x,t)\mid x\in\mathrm{dom}\,f,\ f(x)\le t\}\subseteq\mathbb R^{n+1}\)",r"\(\mathrm{epi}\,f=\{(x,t)\mid f(x)\le t\}\subseteq\mathbb R^{n+1}\)",
  [r"\(\{(x,f(x))\mid x\in\mathrm{dom}\,f\}\subseteq\mathbb R^{n+1}\)",r"\(\{x\in\mathrm{dom}\,f\mid f(x)\le0\}\subseteq\mathbb R^{n}\)",r"\(\{(x,t)\mid f(x)\ge t\}\subseteq\mathbb R^{n+1}\)"]),
 (r"\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\succeq0\) với mọi \(x\in\mathrm{dom}\,f\)",r"\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\succeq0\ \forall x\in\mathrm{dom}\,f\)",
  [r"\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\preceq0\ \forall x\in\mathrm{dom}\,f\)",r"\(\mathrm{dom}\,f\) lồi và \(\nabla^2f(x)\) khả nghịch \(\forall x\in\mathrm{dom}\,f\)",r"\(\mathrm{dom}\,f\) lồi và \(\nabla f(x)\ne0\ \forall x\in\mathrm{dom}\,f\)"]),
 ("tất cả giá trị riêng dương (hoặc tất cả định thức con chính dẫn đầu dương)","mọi giá trị riêng dương (hoặc mọi minor dẫn đầu dương)",
  ["có ít nhất một giá trị riêng dương và đường chéo dương","định thức của A dương và các phần tử ngoài đường chéo bằng 0","vết (trace) của A dương và A đối xứng"]),
 ("0 và 0, nhưng ma trận KHÔNG nửa xác định dương","0 và 0, nhưng A KHÔNG nửa xác định dương",
  ["0 và 0, vậy A nửa xác định dương (mọi minor ≥ 0)","0 và -1, vậy A xác định âm (Δ₂ < 0)","-1 và 0, vậy A xác định dương (Δ₁ đổi dấu)"]),
 ("lồi chặt (Hessian xác định dương)","lồi chặt, vì Hessian xác định dương",
  ["lồi nhưng không chặt, vì Hessian chỉ nửa xác định dương","lõm, vì các phần tử đường chéo của Hessian dương","không lồi cũng không lõm, vì hai giá trị riêng bằng nhau"]),
 (r"\(\nabla^2f(x)=P\) (không phụ thuộc x)",r"\(\nabla^2f(x)=P\), hằng số theo x",
  [r"\(\nabla^2f(x)=Px+q\), phụ thuộc x tuyến tính",r"\(\nabla^2f(x)=\tfrac12P\), do có hệ số \(\tfrac12\) ở đầu",r"\(\nabla^2f(x)=q\), là vectơ hệ số bậc nhất"]),
 ("không lồi cũng không lõm (không xác định)","không lồi cũng không lõm (Hessian không xác định)",
  ["lồi chặt (Hessian xác định dương)","lõm chặt (Hessian xác định âm)","lồi nhưng không chặt (Hessian nửa xác định dương)"]),
 (r"Hessian \(\mathrm{diag}(8,2)\) xác định dương (các số hạng bậc nhất không ảnh hưởng)",r"Hessian \(\mathrm{diag}(8,2)\) xác định dương",
  ["f có điểm cực tiểu nên hàm lồi (suy luận sai)","f không có số hạng chéo \\(x_1x_2\\) nên chắc chắn lồi","Hessian bằng \\(\\mathrm{diag}(4,1)\\), dương (đạo hàm sai)"]),
 (r"\(\min\{f(x),g(x)\}\) của hai hàm lồi",r"\(\min\{f(x),g(x)\}\) của hai hàm lồi",
  [r"\(\alpha f(x)\) với hằng số \(\alpha>0\)",r"tổng \(f(x)+g(x)\) của hai hàm lồi",r"\(\max\{f(x),g(x)\}\) của hai hàm lồi"]),
 ("không lồi cũng không lõm","không lồi và cũng không lõm",
  ["lồi trên toàn miền, nhưng không chặt","lõm trên toàn miền, nhưng không chặt","vừa lồi vừa lõm trên toàn miền"]),
 (r"tính Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\) và chứng minh nó xác định dương",r"tính Hessian \(\begin{pmatrix}2&1\\1&2\end{pmatrix}\) và chứng minh \(\succ0\)",
  [r"chỉ ra \(\nabla f(0)=0\) rồi kết luận có cực tiểu",r"tính \(f(0,0)=0\) và thấy f không âm ở gốc",r"chỉ ra f không âm trên toàn \(\mathbb R^2\)"]),
 ("lồi nhưng không lồi chặt","lồi nhưng không lồi chặt",
  ["lồi chặt vì \\(P\\) có phần tử dương","lõm vì \\(P\\) có phần tử ngoài đường chéo","không lồi vì \\(\\det P=0\\)"]),
 (r"Hàm lồi khả vi luôn có điểm cực tiểu toàn cục",r"Hàm lồi khả vi luôn đạt cực tiểu toàn cục",
  ["Hàm tuyến tính \\(a^\\top x\\) là hàm lồi trên \\(\\mathbb R^n\\)","Tổng hai hàm lồi trên cùng miền là hàm lồi","Hàm \\(e^x\\) là hàm lồi trên toàn \\(\\mathbb R\\)"]),
]
# Áp dụng: thay đúng khối mc(...) theo chuỗi correct hiện tại
import ast
for old_c,new_c,new_w in R:
    # tìm dòng chứa old_c dạng r'...' hoặc '...'
    pat_candidates=["r'"+old_c+"'", "'"+old_c+"'"]
    idx=-1
    for pc in pat_candidates:
        idx=s.find(pc)
        if idx>=0: break
    if idx<0:
        print('KHÔNG TÌM THẤY',old_c[:50]); continue
    # đoạn từ idx tới dấu ']' đóng danh sách wrong: [ ... ],
    j=s.find('],',idx)  # kết thúc list wrong
    # phần list bắt đầu sau ", [" gần nhất sau idx
    k=s.find(', [',idx+len(pc))
    if k<0 or k>j: print('cấu trúc lạ',old_c[:50]); continue
    new_block="r'"+new_c.replace("'", "\\'")+"',\n   ["+", ".join("r'"+w.replace("'", "\\'")+"'" for w in new_w)+"]"
    s=s[:idx]+new_block+s[j+1:]
open(p,'w',encoding='utf-8').write(s)
