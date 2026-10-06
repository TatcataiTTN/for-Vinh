"""Nội dung Module 3 — Quy hoạch toàn phương (bám Slides/3_QuadraticPrograming_250419a.pdf)."""
import json
import numpy as np
from helpers import *

M = 'MODULE 3'
LEAD = 'Quy hoạch toàn phương (QP): hàm mục tiêu toàn phương, ràng buộc tuyến tính. Module này nghiên cứu điều kiện tồn tại nghiệm, cấu trúc tập nghiệm, rồi hai thuật toán: phương pháp không gian hạt nhân (ràng buộc đẳng thức) và phương pháp tập hoạt động (ràng buộc bất đẳng thức).'
META = ['Nguồn: Slide 3, Khoa KHMT Phenikaa (81 trang)', 'Boyd & Vandenberghe: 4.4, 10.1; Lee–Tam–Yen 2005', 'Thời lượng gợi ý: 6–8 giờ']
OBJECTIVES = [
    'Đối xứng hóa ma trận Q, phân loại QP (lồi, lõm, không xác định) và nhận ra LP là trường hợp riêng.',
    'Phát biểu điều kiện tồn tại nghiệm (Frank–Wolfe, Eaves và các hệ quả) và các tính chất của tập nghiệm (đóng, không bị chặn, hữu hạn).',
    'Giải QP ràng buộc đẳng thức bằng phương pháp không gian hạt nhân (Z, Y, \\(d_Y\\), \\(d_Z\\), \\(\\mu\\)).',
    'Thực hiện thuật toán tập hoạt động: giải bài toán con, tính bước \\(\\alpha_k\\), thêm ràng buộc cản, loại ràng buộc có nhân tử âm.',
    'Đối chiếu kết quả với phần mềm và nhận ra chỗ chưa khớp trong slide (ví dụ null-space, Bài tập 1).',
]

def f4(x): return ('%.4f' % x).rstrip('0').rstrip('.')
ne = R['m3_null_ex']; nsteps = R['m3_null_steps']; AE = R['m3_active_ex']; AB = R['m3_active_bt']
ER = R['errata_null_space']; BT1 = R['m3_bt1']; EB = R['errata_bt1']['constraint_b=(3,0)']

# ---------- dữ liệu widget active set ----------
def poly_levels(v): return v
WDATA = {
    'Ví dụ slide tr.69: min (x₁−1)²+(x₂−0.5)² (x⁰=(0,0), W₀={3,4})': dict(
        xr=[-0.4, 1.6], yr=[-0.4, 1.4], Q=[[2, 0], [0, 2]], c=[-2, -1], A=[[1, 1], [3, 1], [-1, 0], [0, -1]], b=[1, 1.5, 0, 0],
        levels=[-1.2, -1.0, -0.85, -0.6, -0.3, 0.0, 0.4], opt=AE['x*'], log=AE['log']),
    'Bài tập tr.81: min (x₁−4.5)²+(x₂−3)² (x⁰=(0,0), W₀={4,5})': dict(
        xr=[-0.5, 6], yr=[-0.5, 5], Q=[[2, 0], [0, 2]], c=[-9, -6], A=[[2, -3], [1, 1], [-3, 5], [-1, 0], [0, -1]], b=[6, 5, 15, 0, 0],
        levels=[-26, -24, -20, -14, -8, -2, 4], opt=AB['x*'], log=AB['log']),
}
WIDGET = '<div class="widget" data-widget="active-set-stepper"><script type="application/json">' + json.dumps(WDATA, ensure_ascii=False) + '</script></div>'

DECK = []
add = DECK.append

add(sl('Quy hoạch toàn phương: hàm bậc hai, ràng buộc tuyến tính',
       '<p>Module này bám <b>Slide 3</b> (81 trang), gồm 5 phần:</p><ol><li>Hàm toàn phương và bài toán QP</li><li>Điều kiện tồn tại nghiệm</li><li>Tính chất của tập nghiệm</li><li>Phương pháp không gian hạt nhân (null space)</li><li>Phương pháp tập hoạt động (active set)</li></ol>'
       + callout('info', 'Vì sao học QP?', '<p>QP là “bậc thang” đầu tiên sau LP: hàm mục tiêu cong nhưng ràng buộc vẫn tuyến tính. Nó xuất hiện khi hồi quy có ràng buộc, chiếu điểm lên đa diện, danh mục đầu tư, SVM, và là bài toán con của phương pháp SQP.</p>'),
       kicker=M + ' · MỞ ĐẦU', img='m3:1',
       explain='<p>Ở Module 2 ta có điều kiện KKT tổng quát. Ở đây ta áp dụng chúng cho trường hợp đặc biệt “dễ” nhất của tối ưu phi tuyến: hàm mục tiêu toàn phương, ràng buộc tuyến tính. Nhờ đó KKT trở thành hệ phương trình tuyến tính.</p>'))

# ---------------- PHẦN 1
add(part(1, 5, 'Hàm toàn phương và bài toán QP', ['Hàm toàn phương–tuyến tính, đối xứng hóa Q', 'Bài toán QP, QP lồi, LP là trường hợp riêng', 'Các dạng QP thường gặp'], M))
add(sl('Hàm toàn phương–tuyến tính',
       formula('Định nghĩa 1.1', r'f(x)=\tfrac12x^\top Qx+c^\top x+\alpha=\tfrac12\langle x,Qx\rangle+\langle c,x\rangle+\alpha,\quad x\in\mathbb R^n',
               [('Q', 'ma trận \\(n\\times n\\)'), ('c', 'vectơ hệ số bậc nhất'), ('\\alpha', 'hằng số')])
       + '<p>Dạng khai triển: \\(f(x)=\\tfrac12\\sum_{i,j}q_{ij}x_ix_j+\\sum_ic_ix_i+\\alpha\\).</p>',
       kicker=M + ' · PHẦN 1', img='m3:3',
       explain='<p>“Toàn phương–tuyến tính” nghĩa là có cả phần bậc hai (\\(\\tfrac12x^\\top Qx\\)) và phần bậc nhất (\\(c^\\top x\\)). Ví dụ \\(f=x_1^2+x_2^2\\) là \\(\\tfrac12x^\\top\\mathrm{diag}(2,2)x\\).</p>'))
add(sl('Có thể giả sử Q đối xứng',
       formula('Đối xứng hóa', r'x^\top Qx=\tfrac12x^\top(Q+Q^\top)x\quad\forall x')
       + '<p>Thay Q bởi \\(\\tfrac12(Q+Q^\\top)\\) không đổi hàm f, nên ta luôn giả sử \\(Q\\in\\mathbb S^n\\) (đối xứng).</p>'
       + '<p>Ví dụ: \\(Q=\\begin{pmatrix}1&4\\\\0&3\\end{pmatrix}\\Rightarrow\\tfrac12(Q+Q^\\top)=\\begin{pmatrix}1&2\\\\2&3\\end{pmatrix}\\); với \\(x=(2,-1)\\) cả hai cho \\(x^\\top Qx=-1\\).</p>',
       kicker=M + ' · PHẦN 1', img='m3:7',
       explain='<p>Phần “lệch” của Q (\\(Q-Q^\\top\\)) triệt tiêu trong dạng toàn phương: \\(x^\\top(Q-Q^\\top)x=0\\). Vì vậy chỉ phần đối xứng có ý nghĩa; Hessian của f luôn đối xứng.</p>'))
add(sl('Ví dụ: \\(f=x_1^2+x_2^2\\)',
       '<p>\\(f(x)=x_1^2+x_2^2=\\tfrac12(x_1,x_2)\\begin{pmatrix}2&0\\\\0&2\\end{pmatrix}\\begin{pmatrix}x_1\\\\x_2\\end{pmatrix}\\), tức \\(Q=2I\\), \\(c=0\\), \\(\\alpha=0\\): f là hàm toàn phương dạng (1.1).</p>',
       kicker=M + ' · PHẦN 1', img='m3:9',
       explain='<p>Nhân đôi hệ số vì có \\(\\tfrac12\\) ở đầu công thức. Đây là nguyên nhân nhiều sai sót số học: luôn kiểm bằng cách tính Hessian của f, phải bằng Q.</p>'))
add(sl('Bài toán quy hoạch toàn phương',
       formula('Bài toán (P)', r'\min f(x)\quad\text{s.t.}\quad x\in\Delta')
       + '<div class="callout good"><span class="ct"><b>Định nghĩa 1.2</b></span>(P) là QP (quy hoạch toàn phương–tuyến tính) nếu f là hàm toàn phương–tuyến tính và \\(\\Delta\\) là <b>tập lồi đa diện</b>.</div>'
       '<ul><li>\\(Q=0\\), \\(\\alpha=0\\): f tuyến tính ⇒ <b>QHTT ⊂ QP</b>.</li><li>\\(Q\\succeq0\\): QP <b>lồi</b>.</li></ul>',
       kicker=M + ' · PHẦN 1', img='m3:12',
       explain='<p>Điều kiện “\\(\\Delta\\) là polyhedron” (Module 1) là quan trọng: nó cho phép dùng ràng buộc tuyến tính, đảm bảo tính chất tốt như định lý Frank–Wolfe ở phần 2.</p>'))
add(sl('Hai lưu ý về hằng số và hệ số 1/2',
       '<ul><li>Bỏ hằng số \\(\\alpha\\) không đổi <b>tập nghiệm</b> (chỉ đổi giá trị tối ưu). Có thể xét \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\).</li><li>Thay \\(Q\\) bởi \\(\\tfrac12Q\\): \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) trở thành \\(\\min x^\\top Qx+c^\\top x\\) (bỏ hệ số \\(\\tfrac12\\)) — hai dạng chỉ khác quy ước.</li></ul>'
       + callout('warn', 'Bẫy quy ước', '<p>Khi đề cho đa thức \\(f\\), hãy tính Hessian rồi mới đặt \\(Q=\\nabla^2f\\). Ví dụ null-space ở tr.56: Q ghi trên slide bằng <b>một nửa</b> Hessian của đa thức (xem trang “Kiểm chứng”).</p>'),
       kicker=M + ' · PHẦN 1', img='m3:14',
       explain='<p>Đây là bẫy hay gặp: nếu bạn viết đa thức, rồi lấy Q là ma trận các hệ số (không nhân đôi phần chéo) thì thiếu một hệ số 2 so với chuẩn \\(\\tfrac12x^\\top Qx\\).</p>'))
add(sl('QP không lồi: \\(\\min x_1^2-x_2^2\\) trên \\([1,3]^2\\)',
       '<p>\\(f=\\tfrac12x^\\top\\mathrm{diag}(2,-2)x\\), \\(\\Delta=\\{1\\le x_1,x_2\\le3\\}\\). Đây là QP <b>không lồi</b>.</p>'
       + table(['Đỉnh', '(1,1)', '(1,3)', '(3,1)', '(3,3)'], [['f', '0', '<b>−8</b>', '8', '0']])
       + '<p>Cực tiểu tại đỉnh \\((1,3)\\) với \\(f=-8\\) (kiểm bằng code).</p>',
       kicker=M + ' · PHẦN 1', img='m3:16',
       explain='<p>Vì f lõm theo \\(x_2\\) nên giá trị nhỏ nhất theo \\(x_2\\) đạt ở biên (\\(x_2=3\\)); lồi theo \\(x_1\\) với đạo hàm dương nên nhỏ nhất ở \\(x_1=1\\). Bài toán không lồi có thể có nghiệm ở đỉnh.</p>'))
add(sl('Các dạng QP thường gặp',
       '<ul><li>\\(\\min\\tfrac12x^\\top Qx+c^\\top x:\\ x\\in\\mathbb R^n,\\ Ax\\ge b\\)</li><li>\\(\\ \\ \\ \\ \\ \\ \\ \\ \\ldots,\\ Ax\\ge b,\\ x\\ge0\\)</li><li>\\(\\ \\ \\ \\ \\ \\ \\ \\ \\ldots,\\ Ax\\ge b,\\ Cx=d\\)</li><li>\\(\\ \\ \\ \\ \\ \\ \\ \\ \\ldots,\\ Ax\\le b,\\ x\\ge0\\)</li></ul><p>Mọi dạng đều quy về dạng tổng quát \\(Ax\\ge b\\) (thêm ràng buộc \\(x\\ge0\\) và đổi dấu).</p>',
       kicker=M + ' · PHẦN 1', img='m3:20',
       explain='<p>Bốn dạng chỉ khác cách viết ràng buộc: có/không có \\(x\\ge0\\), có/không có đẳng thức. Trong phần “tập hoạt động” ta dùng dạng \\(a_i^\\top x\\le b_i\\); để chuyển sang dạng này chỉ cần nhân \\(-1\\).</p>'))

# ---------------- PHẦN 2
add(part(2, 5, 'Điều kiện tồn tại nghiệm', ['Giá trị tối ưu \\(\\bar\\theta\\) và ba trường hợp', 'Định lý Frank–Wolfe và định lý Eaves', 'Bốn hệ quả theo dấu của Q'], M))
add(sl('Ba tình huống của bài toán (2)',
       formula('Bài toán (2)', r'\min f(x)=\tfrac12x^\top Qx+c^\top x\quad\text{s.t.}\quad Ax\ge b')
       + '<p>Đặt \\(\\Delta(A,b)=\\{x\\mid Ax\\ge b\\}\\), \\(\\bar\\theta=\\inf\\{f(x):x\\in\\Delta(A,b)\\}\\).</p><ul><li>\\(\\Delta=\\emptyset\\): \\(\\bar\\theta=+\\infty\\) (quy ước).</li><li>\\(\\Delta\\ne\\emptyset\\), TH1: \\(\\bar\\theta\\in\\mathbb R\\).</li><li>TH2: \\(\\bar\\theta=-\\infty\\) (bài toán không có nghiệm).</li></ul>',
       kicker=M + ' · PHẦN 2', img='m3:23',
       explain='<p>Bài toán chưa chắc có nghiệm: có thể miền rỗng, hoặc f giảm vô hạn, hoặc infimum hữu hạn nhưng không đạt được (như \\(\\min x_1\\) với \\(x_1x_2\\ge1\\)). Định lý Frank–Wolfe cho biết khi nào TH1 kéo theo có nghiệm.</p>'))
add(sl('Định lý Frank–Wolfe',
       '<div class="callout good"><span class="ct"><b>Frank–Wolfe</b></span>Nếu \\(\\bar\\theta=\\inf\\{f(x):x\\in\\Delta(A,b)\\}\\) là một số thực hữu hạn thì bài toán (2) <b>có nghiệm</b>.</div>'
       '<p>Giả thiết quan trọng: \\(\\Delta\\) là <b>polyhedron</b> và f là toàn phương. Nếu bỏ giả thiết polyhedron thì định lý sai:</p>'
       '<p>Ví dụ (slide tr.25): \\(\\min x_1\\) với \\(\\Delta=\\{x_1x_2\\ge1,\\ x_1,x_2\\ge0\\}\\) (không phải polyhedron): \\(\\bar\\theta=0\\) nhưng không đạt (chỉ tiến tới 0 khi \\(x_2=1/x_1\\to\\infty\\)).</p>',
       kicker=M + ' · PHẦN 2', img='m3:24',
       explain='<p>Điểm đặc biệt của QP: chỉ cần infimum hữu hạn là chắc chắn đạt được nghiệm (không cần miền bị chặn!). Điều này không đúng cho hàm bậc hai phi tuyến trên miền phi tuyến, như ví dụ \\(x_1x_2\\ge1\\).</p>'))
add(sl('Định lý Eaves',
       '<div class="callout good"><span class="ct"><b>Eaves</b></span>Bài toán (2) có nghiệm ⇔ ba điều kiện:<ol><li>\\(\\Delta(A,b)\\ne\\emptyset\\);</li><li>\\(v\\in\\mathbb R^n,\\ Av\\ge0\\Rightarrow v^\\top Qv\\ge0\\);</li><li>\\(Av\\ge0,\\ v^\\top Qv=0,\\ Ax\\ge b\\Rightarrow(Qx+c)^\\top v\\ge0\\).</li></ol></div>'
       '<p>Ý nghĩa: đi theo mọi <b>hướng lùi</b> \\(v\\) (\\(Av\\ge0\\), giữ khả thi) thì f không được giảm vô hạn: dạng bậc hai không âm (2), và nếu bậc hai bằng 0 thì phần tuyến tính không âm (3).</p>',
       kicker=M + ' · PHẦN 2', img='m3:26',
       explain='<p>\\(\\{v:Av\\ge0\\}\\) là “nón lùi” của miền: các hướng ta có thể đi mãi mà vẫn khả thi. Dọc hướng đó f có dạng \\(f(x+tv)=f(x)+t(Qx+c)^\\top v+\\tfrac{t^2}2v^\\top Qv\\); để f không rơi xuống \\(-\\infty\\) thì hệ số \\(t^2\\) phải \\(\\ge0\\), và nếu bằng 0 thì hệ số \\(t\\) phải \\(\\ge0\\).</p>'))
add(sl('Bốn hệ quả theo dấu của Q',
       table(['Hệ quả', 'Q', 'Bài toán (2) có nghiệm ⇔'],
             [['1', '\\(Q\\succeq0\\)', '\\(\\Delta\\ne\\emptyset\\) và (\\(Av\\ge0,\\ v^\\top Qv=0,\\ Ax\\ge b\\Rightarrow(Qx+c)^\\top v\\ge0\\))'],
              ['2', '\\(Q\\preceq0\\)', '\\(\\Delta\\ne\\emptyset\\) và (\\(Av\\ge0\\Rightarrow v^\\top Qv=0\\)) và (\\(Av\\ge0,Ax\\ge b\\Rightarrow(Qx+c)^\\top v=0\\))'],
              ['3', '\\(Q\\succ0\\)', '\\(\\Delta\\ne\\emptyset\\) (chỉ cần khả thi!)'],
              ['4', 'xác định âm (slide ghi “nửa xác định âm”)', '\\(\\Delta\\ne\\emptyset\\) và <b>compact</b>']])
       + callout('warn', 'Ghi chú kiểm chứng', '<p>Slide tr.30 ghi Hệ quả 4 với “nửa xác định âm” như Hệ quả 2. Với \\(Q=0\\) (LP) điều đó sai (LP \\(\\min x\\), \\(x\\ge0\\) có nghiệm nhưng \\(\\Delta\\) không compact); cần <b>xác định âm</b>. Xem trang “Kiểm chứng”.</p>'),
       kicker=M + ' · PHẦN 2', img='m3:27',
       explain='<p>Hệ quả 3 là dễ nhớ nhất: Q xác định dương ⇒ f “coercive” (→∞ khi \\(\\|x\\|\\to\\infty\\)) nên chỉ cần miền khác rỗng là có nghiệm (và duy nhất). Hệ quả 4: hàm lõm chặt chỉ đạt cực tiểu ở “đỉnh xa”, nên cần miền compact để tránh giảm vô hạn.</p>'))

# ---------------- PHẦN 3
add(part(3, 5, 'Tính chất của tập nghiệm', ['Sol(P) đóng; nghiệm tia và tính không bị chặn', 'Cực tiểu địa phương loc(P) có thể không đóng', 'Q xác định dương / xác định âm / nửa xác định dương', 'Nghiệm có thể là điểm trong'], M))
add(sl('Ký hiệu và bài toán thuần nhất liên kết',
       '<p>(P): \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) s.t. \\(Ax\\ge b,\\ Cx=d\\), \\(\\Delta=\\{Ax\\ge b,Cx=d\\}\\). Ký hiệu \\(\\mathrm{Sol}(P)\\) là tập nghiệm.</p>'
       '<p>Bài toán <b>thuần nhất</b> liên kết: \\((P_0)\\ \\min\\tfrac12v^\\top Qv\\) s.t. \\(Av\\ge0,\\ Cv=0\\).</p>'
       '<p><b>Nghiệm tia</b>: nửa đường thẳng \\(\\{\\bar x+t\\bar v:t\\ge0\\}\\subset\\mathrm{Sol}(P)\\), \\(\\bar v\\ne0\\).</p>',
       kicker=M + ' · PHẦN 3', img='m3:34',
       explain='<p>\\(P_0\\) chỉ giữ lại “phần hướng” của bài toán (bỏ hằng số b, d, c). Nghiệm tia là hướng mà ta đi mãi vẫn tối ưu; nếu có thì tập nghiệm không bị chặn.</p>'))
add(sl('Định lý 3.1 và 3.2',
       '<div class="callout good"><span class="ct"><b>Định lý 3.1</b></span>\\(\\mathrm{Sol}(P)\\) không bị chặn ⇔ (P) có nghiệm tia. Điều kiện cần và đủ: tồn tại \\(\\bar x\\in\\mathrm{Sol}(P)\\), \\(\\bar v\\in\\mathrm{Sol}(P_0)\\setminus\\{0\\}\\) với \\((Q\\bar x+c)^\\top\\bar v=0\\).</div>'
       '<div class="callout good"><span class="ct"><b>Định lý 3.2</b></span>\\(\\mathrm{Sol}(P)\\) là tập <b>đóng</b>.</div>'
       '<p>Nhưng tập cực tiểu địa phương \\(\\mathrm{loc}(P)\\) có thể không đóng: xét \\(\\min-x_2^2+x_1x_2\\) trên \\(x\\ge0\\): \\(\\mathrm{Sol}=\\emptyset\\), \\(\\mathrm{loc}=\\{x_1>0,\\ x_2=0\\}\\) (không đóng).</p>',
       kicker=M + ' · PHẦN 3', img='m3:38',
       explain='<p>Kiểm ví dụ: tại \\((a,0)\\) với \\(a>0\\), \\(f(a,x_2)=-x_2^2+ax_2\\ge0\\) với \\(x_2\\) nhỏ nên là cực tiểu địa phương; tại \\((0,0)\\), dọc \\((0,t)\\) có \\(f=-t^2<0\\), nên không. Tập \\(\\{x_1>0,x_2=0\\}\\) không chứa điểm biên \\((0,0)\\): không đóng. \\(\\mathrm{Sol}\\) rỗng vì \\(f(0,t)=-t^2\\to-\\infty\\).</p>'))
add(sl('Định lý 3.3: tập nghiệm theo dấu của Q',
       table(['Q', 'Kết luận (với \\(\\Delta\\ne\\emptyset\\))'],
             [['\\(Q\\succ0\\)', '(P) có nghiệm <b>duy nhất</b>; \\(\\mathrm{Sol}(P)=\\mathrm{loc}(P)\\)'],
              ['\\(Q\\prec0\\)', 'mỗi cực tiểu địa phương là <b>điểm cực biên</b> của Δ: \\(\\mathrm{Sol}\\subset\\mathrm{loc}\\subset\\mathrm{extr}\\,\\Delta\\); số nghiệm nhỏ hơn số điểm cực biên'],
              ['\\(Q\\succeq0\\)', '\\(\\mathrm{Sol}(P)\\) là tập <b>lồi đóng</b>; nếu hữu hạn thì rỗng hoặc đúng một phần tử']])
       + '<p style="font-size:.85em">Sơ đồ tóm tắt ở phần “Sơ đồ tổng hợp” bên dưới.</p>',
       kicker=M + ' · PHẦN 3', img='m3:40',
       explain='<p>Q xác định dương: bài toán lồi chặt nên nghiệm duy nhất. Q xác định âm: f lõm chặt nên cực tiểu ở “góc” của miền (điểm cực biên). Q nửa xác định dương: bài toán lồi nhưng có thể có cả cạnh nghiệm.</p>'))
add(sl('Ví dụ: \\(-x_1^2-x_2^2+1\\) trên \\([-1,1]^2\\)',
       '<p>\\(Q=\\begin{pmatrix}-2&0\\\\0&-2\\end{pmatrix}\\prec0\\). \\(\\mathrm{Sol}(P)=\\mathrm{loc}(P)=\\{(1,1),(1,-1),(-1,1),(-1,-1)\\}=\\mathrm{extr}(\\Delta)\\).</p>'
       '<p>Tại bốn đỉnh \\(f=-1\\) (kiểm code). Tập nghiệm <b>không lồi</b> (bốn điểm rời nhau).</p>',
       kicker=M + ' · PHẦN 3', img='m3:41',
       explain='<p>Đây là QP không lồi: nghiệm là bốn góc của hình vuông, tập nghiệm không lồi. Ngược lại QP lồi luôn có tập nghiệm lồi.</p>'))
add(sl('Nghiệm của QP có thể là điểm TRONG của miền',
       '<ul><li>Ví dụ 1: \\(\\min x^2\\), \\(-1\\le x\\le1\\): \\(x=0\\) là nghiệm, nằm trong khoảng.</li><li>Ví dụ 2: \\(\\min x_1^2+x_2^2\\) trên \\([-1,1]^2\\): \\(x^*=(0,0)\\in\\mathrm{int}\\,\\Delta\\).</li></ul>'
       '<p>Khác với LP (nghiệm luôn ở biên/đỉnh), QP lồi có thể có nghiệm nội điểm: khi đó tất cả \\(\\lambda_i=0\\) và KKT rút gọn thành \\(Qx+c=0\\).</p>',
       kicker=M + ' · PHẦN 3', img='m3:45',
       explain='<p>Khi hàm mục tiêu có “đáy” nằm trong miền (như \\(x^2\\) có đáy tại 0), nghiệm là đáy đó; các ràng buộc “lỏng” không tham gia. Đó là điểm khác biệt cơ bản của QP so với LP.</p>'))

# ---------------- PHẦN 4
add(part(4, 5, 'Phương pháp không gian hạt nhân (Null space)', ['QP chỉ có ràng buộc đẳng thức và hệ KKT tuyến tính', 'Ma trận Z (nhân của A) và Y', 'Công thức \\(d_Y\\), \\(d_Z\\), \\(d\\), \\(\\mu\\)', 'Ví dụ 3 biến và bài tập'], M))
add(sl('Hai phương pháp số và bài toán ràng buộc đẳng thức',
       '<ul><li><b>Null space</b>: giải bài toán có ràng buộc <b>đẳng thức</b>.</li><li><b>Active set</b>: giải bài toán có ràng buộc <b>bất đẳng thức</b> (dùng null space cho bài toán con).</li></ul>'
       + formula('Bài toán (P) đẳng thức', r'\min\tfrac12x^\top Qx+c^\top x\quad\text{s.t.}\ Ax=b,\qquad Q=Q^\top\succeq0,\ A\in\mathbb R^{m\times n},\ \mathrm{rank}\,A=m'),
       kicker=M + ' · PHẦN 4', img='m3:47',
       explain='<p>Điều kiện \\(\\mathrm{rank}A=m\\) nghĩa là các ràng buộc độc lập tuyến tính (không thừa, không mâu thuẫn). Khi ràng buộc đẳng thức, KKT trở thành hệ phương trình tuyến tính nên giải được trực tiếp.</p>'))
add(sl('KKT của QP đẳng thức',
       '<p>Hàm Lagrange \\(L=\\tfrac12x^\\top Qx+c^\\top x+\\mu^\\top(Ax-b)\\). Vì mục tiêu lồi và ràng buộc affine, \\(x^*\\) là nghiệm ⇔ \\(x^*\\) là điểm KKT:</p>'
       + formula('Hệ KKT (4.1)', r'\begin{cases}Qx^*+c+A^\top\mu^*=0\\ Ax^*=b\end{cases}')
       + '<p>Hệ có ma trận hệ số <b>không đối xứng</b> khi viết theo \\((x,\\mu)\\); ta đổi biến để được ma trận đối xứng.</p>',
       kicker=M + ' · PHẦN 4', img='m3:48',
       explain='<p>Từ Module 2: bài lồi có ràng buộc affine (không cần Slater, vì affine) ⇒ KKT cần và đủ. Hệ gồm n phương trình dừng và m phương trình ràng buộc: \\(n+m\\) phương trình cho \\(n+m\\) ẩn \\((x,\\mu)\\).</p>'))
add(sl('Đổi biến \\(d=x-\\bar x\\) và hệ (4.2)',
       '<p>Với \\(\\bar x\\) gần nghiệm, đặt \\(d=x-\\bar x\\), \\(\\bar g=Q\\bar x+c\\), \\(\\bar b=b-A\\bar x\\). Bài toán (PD): \\(\\min\\tfrac12d^\\top Qd+\\bar g^\\top d\\) s.t. \\(Ad=\\bar b\\).</p>'
       + formula('Hệ KKT đối xứng (4.2)', r'\begin{pmatrix}Q&A^\top\\A&0\end{pmatrix}\begin{pmatrix}d^*\\\mu^*\end{pmatrix}=\begin{pmatrix}-\bar g\\\bar b\end{pmatrix},\qquad x^*=\bar x+d^*')
       + '<p>Ma trận khối này đối xứng (vì Q đối xứng). \\(\\mu^*\\) là nhân tử của bài toán gốc.</p>',
       kicker=M + ' · PHẦN 4', img='m3:50',
       explain='<p>Ý tưởng “dịch gốc”: thay vì tìm x, ta tìm bước d từ điểm xuất phát \\(\\bar x\\) (không cần khả thi). Kết quả x* không phụ thuộc \\(\\bar x\\) khi nghiệm duy nhất. Slide dùng \\(G\\) (Hessian) trong vài công thức; với hàm toàn phương \\(G=Q\\).</p>'))
add(sl('Ma trận Z và Y; điều kiện ZᵀQZ ≻ 0',
       '<ul><li>Z: cơ sở của \\(\\ker A\\), cỡ \\(n\\times(n-m)\\), \\(AZ=0\\).</li><li>Y: cỡ \\(n\\times m\\) sao cho \\([Y\\ Z]\\) khả nghịch (có thể chọn \\(AY=I\\)).</li><li>\\(d=Yd_Y+Zd_Z\\), \\(d_Y\\in\\mathbb R^m\\), \\(d_Z\\in\\mathbb R^{n-m}\\).</li></ul>'
       '<div class="callout good"><span class="ct"><b>Mệnh đề</b></span>Nếu \\(\\mathrm{rank}A=m\\) và <b>Hessian rút gọn</b> \\(Z^\\top QZ\\succ0\\) thì ma trận của hệ (4.2) không suy biến, tồn tại duy nhất \\((d^*,\\mu^*)\\), và (P) có nghiệm duy nhất.</div>',
       kicker=M + ' · PHẦN 4', img='m3:52',
       explain='<p>Không gian hạt nhân \\(\\ker A=\\{d:Ad=0\\}\\) là tập các hướng đi mà ràng buộc đẳng thức được giữ nguyên. \\(Z^\\top QZ\\) là dạng toàn phương của f <i>hạn chế</i> trên các hướng đó; nó xác định dương thì f “cong lên” dọc mọi hướng khả thi ⇒ có đúng một nghiệm.</p>'))
add(sl('Các bước tính (4.5)–(4.7)',
       steps(['Giải \\(AYd_Y=\\bar b\\) (vì \\(AZ=0\\)) ⇒ \\(d_Y\\).',
              'Giải \\((Z^\\top QZ)d_Z=-Z^\\top QYd_Y-Z^\\top\\bar g\\) (4.6) ⇒ \\(d_Z\\) (Cholesky).',
              'Tính \\(d=Yd_Y+Zd_Z\\), \\(x^*=\\bar x+d\\).',
              'Giải \\((AY)^\\top\\mu^*=-Y^\\top(\\bar g+Qd)\\) (từ nhân \\(Y^\\top\\) vào phương trình dừng) ⇒ \\(\\mu^*\\).'])
       + callout('warn', 'Ghi chú', '<p>Slide (4.7) viết “\\(-Y^\\top\\bar g+Gd\\)”; theo suy dẫn đúng là \\(-Y^\\top(\\bar g+Qd)\\). Các số ví dụ của slide trùng với công thức đúng (xem “Kiểm chứng”).</p>'),
       kicker=M + ' · PHẦN 4', img='m3:55',
       explain='<p>Cách nhớ: nhân phương trình dừng \\(Qd+\\bar g+A^\\top\\mu=0\\) với \\(Z^\\top\\): số hạng \\(A^\\top\\mu\\) biến mất (vì \\(AZ=0\\)) nên tìm được \\(d_Z\\). Nhân với \\(Y^\\top\\): còn lại \\((AY)^\\top\\mu\\) nên tìm được \\(\\mu\\).</p>'))
add(sl('Ví dụ 3 biến (slide tr.56–58)',
       '<p>\\(Q=\\begin{pmatrix}2&-2&-1\\\\-2&2&1\\\\-1&1&5\\end{pmatrix}\\), \\(c=(10,-26,-2)^\\top\\), \\(A=\\begin{pmatrix}1&1&0\\\\1&0&1\\end{pmatrix}\\), \\(b=(4,10)^\\top\\); \\(\\bar x=0\\).</p>'
       '<p>\\(Z=(-1,1,1)^\\top\\), \\(Y=\\begin{pmatrix}1/3&1/3\\\\2/3&-1/3\\\\-1/3&2/3\\end{pmatrix}\\) (có \\(AY=I\\)); \\(d_Y=(4,10)^\\top\\); \\(Z^\\top QZ=' + f4(nsteps['ZtQZ'][0][0]) + '\\) ⇒ \\(d_Z=' + f4(nsteps['dZ'][0]) + '\\).</p>'
       '<p>\\(x^*=(' + ', '.join(f4(v) for v in ne['x*']) + ')^\\top\\), \\(\\mu^*=(' + ', '.join(f4(v) for v in ne['mu']) + ')^\\top\\) (khớp slide).</p>'
       + callout('warn', 'Giá trị hàm mục tiêu', '<p>Slide ghi \\(f_{\\min}=212.7059\\); đó là giá trị của <i>đa thức</i> tại \\(x^*\\). Giá trị của \\(\\tfrac12x^\\top Qx+c^\\top x\\) với Q, c như trên là <b>' + f4(ne['f']) + '</b>. Hai quy ước khác nhau (Hessian của đa thức là \\(2Q\\)); xem trang “Kiểm chứng”.</p>'),
       kicker=M + ' · PHẦN 4', img='m3:58',
       explain='<p>Ví dụ này cho thấy cả quy trình: chọn Z, Y, tính \\(d_Y\\) (giải hệ 2×2), \\(d_Z\\) (chỉ 1 ẩn, vì \\(n-m=1\\)), rồi ghép. Bạn có thể kiểm bằng công cụ “Giải QP đẳng thức” bên dưới.</p>'))
add(sl('Bài tập 1 (slide tr.59)',
       '<p>Giải bằng null space với \\(\\bar x=0\\): \\(\\min f=3x_1^2+2x_1x_2+x_1x_3+2.5x_2^2+2x_2x_3+2x_3^2-8x_1-3x_2-3x_3\\) s.t. \\(x_1+x_3=0\\), \\(x_2+x_3=0\\). Slide ghi ĐS \\((2,-1,1)^\\top\\).</p>'
       + callout('warn', 'Kiểm chứng', '<p>\\((2,-1,1)\\) không thỏa \\(x_1+x_3=0\\). Nghiệm đúng của bài với \\(b=(0,0)\\) là \\((' + ', '.join(f4(v) for v in BT1['x*']) + ')\\). ĐS \\((2,-1,1)\\) khớp khi ràng buộc thứ nhất là \\(x_1+x_3=3\\) (\\(b=(3,0)\\), \\(\\mu=(' + ', '.join(f4(v) for v in EB['mu']) + ')\\), \\(f=' + f4(EB['f']) + '\\)).</p>'),
       kicker=M + ' · PHẦN 4', img='m3:59',
       explain='<p>Hessian của f là \\(\\begin{pmatrix}6&2&1\\\\2&5&2\\\\1&2&4\\end{pmatrix}\\succ0\\) (giá trị riêng ' + ', '.join(f4(v) for v in BT1['eig']) + ') nên nghiệm duy nhất. Hãy thử cả hai phiên bản trong công cụ “Giải QP đẳng thức”: nút “Bài tập” dùng \\(b=(3,0)\\).</p>'))

# ---------------- PHẦN 5
add(part(5, 5, 'Phương pháp tập hoạt động (Active set)', ['Ràng buộc chặt \\(I(x^*)\\) và tập làm việc \\(W_k\\)', 'Ba bước: bài toán con, bước \\(\\alpha_k\\), nhân tử', 'Ví dụ 2 biến giải đầy đủ và bài tập'], M))
add(sl('Bài toán và ý tưởng',
       formula('Bài toán (P)', r'\min\tfrac12x^\top Qx+c^\top x\quad\text{s.t.}\ a_i^\top x\le b_i\ (i=1..m),\qquad Q=Q^\top\succ0')
       + '<p>\\(I(x^*)=\\{i\\mid a_i^\\top x^*=b_i\\}\\): tập chỉ số các ràng buộc <b>hoạt động</b> (chặt) tại \\(x^*\\).</p><p>Nếu biết \\(I(x^*)\\), \\(x^*\\) là nghiệm của bài toán <b>đẳng thức</b> \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) s.t. \\(a_i^\\top x=b_i\\ (i\\in I(x^*))\\). Vì chưa biết trước, thuật toán cập nhật một <b>tập làm việc</b> \\(W_k\\subseteq I(x^k)\\).</p>',
       kicker=M + ' · PHẦN 5', img='m3:61',
       explain='<p>Hình dung: mỗi ràng buộc là một bức tường; nghiệm dựa vào một số bức tường (các ràng buộc hoạt động) và không chạm các bức tường khác. Thuật toán “đoán” dần tập tường đó: thêm tường khi đi chạm, bỏ tường khi thấy đẩy ngược chiều.</p>'))
add(sl('KKT và mệnh đề nền tảng',
       formula('(4.9)', r'Qx^*+c+\sum_{i\in I(x^*)}\mu_i^*a_i=0,\qquad a_i^\top x^*=b_i\ \ (i\in I(x^*)),\qquad \mu_i^*\ge0')
       + '<div class="callout good"><span class="ct"><b>Mệnh đề</b></span>Nếu \\(x^*\\) thỏa (4.9) và \\(Q\\succeq0\\) thì \\(x^*\\) là nghiệm <b>toàn cục</b> của (P).</div>',
       kicker=M + ' · PHẦN 5', img='m3:63',
       explain='<p>Đây là KKT của Module 2 áp dụng cho QP lồi: (4.9) chính là hệ dừng + bù (chỉ giữ các ràng buộc hoạt động) + \\(\\mu\\ge0\\). Vì QP lồi có ràng buộc affine, KKT cần và đủ.</p>'))
add(sl('Thuật toán: Bước 1 — bài toán con',
       '<p>Giả sử \\(x^k\\) khả thi, \\(W_k\\subseteq I(x^k)\\). Kiểm tra \\(x^k\\) có là nghiệm của \\((P_k)\\): \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) s.t. \\(a_i^\\top x=b_i\\ (i\\in W_k)\\) bằng cách giải, với \\(d=x-x^k\\), \\(g^k=Qx^k+c\\):</p>'
       + formula('(PD_k)', r'\min\tfrac12d^\top Qd+(g^k)^\top d\quad\text{s.t.}\ a_i^\top d=0,\ i\in W_k')
       + '<p>(bằng phương pháp null space). \\(d^k=0\\) ⇔ \\(x^k\\) là nghiệm \\((P_k)\\). Vì \\(d=0\\) khả thi nên giá trị tối ưu của \\((PD_k)\\) là <b>không dương</b>.</p><p>Nếu \\(d^k\\ne0\\): sang Bước 2; nếu \\(d^k=0\\): sang Bước 3.</p>',
       kicker=M + ' · PHẦN 5', img='m3:64',
       explain='<p>Bước 1 hỏi: “giữ nguyên các bức tường đang dựa vào \\(W_k\\) thì có còn đi xuống được không?”. Nếu có (\\(d^k\\ne0\\)) ta đi; nếu không (\\(d^k=0\\)) ta đứng lại và hỏi các bức tường có đang “đỡ” đúng chiều hay không (nhân tử).</p>'))
add(sl('Bước 2 — độ dài bước và ràng buộc cản',
       formula('Độ dài bước', r'\alpha_k=\min\Big\{1,\ \min_{i\notin W_k,\ a_i^\top d^k>0}\frac{b_i-a_i^\top x^k}{a_i^\top d^k}\Big\}')
       + '<ul><li>\\(d^k\\) là hướng giảm tại \\(x^k\\). Chọn \\(\\alpha_k\\in[0,1]\\) lớn nhất để \\(x^k+\\alpha_kd^k\\) vẫn khả thi.</li><li>Ràng buộc đạt min trong công thức là <b>ràng buộc cản</b> (blocking).</li><li>\\(x^{k+1}=x^k+\\alpha_kd^k\\); nếu có ràng buộc cản, <b>thêm</b> một chỉ số cản vào \\(W_k\\). Quay lại Bước 1.</li></ul>',
       kicker=M + ' · PHẦN 5', img='m3:66',
       explain='<p>Chỉ các ràng buộc có \\(a_i^\\top d>0\\) (đang tiến sát tường) mới hạn chế bước. Tỉ số \\((b_i-a_i^\\top x)/(a_i^\\top d)\\) là “khoảng cách còn lại” chia “tốc độ tiến tới tường”. \\(\\alpha=1\\) nghĩa là đi trọn bước Newton mà không chạm tường nào.</p>'))
add(sl('Bước 3 — nhân tử Lagrange',
       '<p>Khi \\(d^k=0\\): giải \\(Qx^k+c+\\sum_{i\\in W_k}\\hat\\mu_ia_i=0\\) tìm \\(\\hat\\mu_i\\).</p><ul><li>\\(\\hat\\mu_i\\ge0\\ \\forall i\\in W_k\\) ⇒ \\(x^k\\) là <b>nghiệm</b> của (P) (dừng).</li><li>Có \\(\\hat\\mu_j<0\\) ⇒ <b>loại</b> chỉ số \\(j\\) (thường chọn \\(\\hat\\mu_j\\) âm nhất) khỏi \\(W_k\\): \\(x^{k+1}=x^k\\), \\(W_{k+1}=W_k\\setminus\\{j\\}\\); về Bước 1.</li></ul>',
       kicker=M + ' · PHẦN 5', img='m3:67',
       explain='<p>Nhân tử âm nghĩa là bức tường j đang “kéo” điểm về phía trong miền thay vì đỡ: nếu buông tường đó, ta có thể đi xuống tiếp. Vì vậy ta loại nó khỏi tập làm việc (giải phóng ràng buộc).</p>'))
add(sl('Thuật toán tập hoạt động (tổng hợp)',
       '<figure class="slide-fig"><img src="../../assets/diagrams/d4-active-set.svg" alt="Lưu đồ active set" style="max-height:20em;background:#fff"/></figure>',
       kicker=M + ' · PHẦN 5', img='m3:68',
       explain='<p>Thuật toán trong slide: khởi tạo \\(x^0\\) khả thi, \\(W_0=I(x^0)\\). Với mỗi k giải \\(d^k\\); nếu \\(d^k=0\\) tính nhân tử (dừng hoặc loại một ràng buộc); nếu không thì tính \\(\\alpha_k\\), cập nhật x và thêm ràng buộc cản.</p>'))
add(sl('Ví dụ: đề bài và khởi tạo',
       '<p>\\(\\min(x_1-1)^2+(x_2-0.5)^2\\) s.t. \\(x_1+x_2\\le1,\\ 3x_1+x_2\\le1.5,\\ x_1\\ge0,\\ x_2\\ge0\\).</p><p>\\(Q=2I\\), \\(c=(-2,-1)^\\top\\) (slide tr.55 ghi nhầm \\(c=[-2,1]\\)), \\(A=\\begin{pmatrix}1&1\\\\3&1\\\\-1&0\\\\0&-1\\end{pmatrix}\\), \\(b=(1,1.5,0,0)^\\top\\).</p>'
       '<p>Khởi tạo \\(x^0=(0,0)\\); ràng buộc 3, 4 chặt ⇒ \\(W_0=I(x^0)=\\{3,4\\}\\).</p>',
       kicker=M + ' · PHẦN 5', img='m3:69',
       explain='<p>Đây là bài toán “chiếu điểm \\((1,0.5)\\) lên miền khả thi”: tìm điểm khả thi gần điểm đó nhất. Hai ràng buộc đầu là tường trên/phải, hai ràng buộc sau là hai trục tọa độ.</p>'))
add(sl('Vòng 0 và 1',
       f'<ul><li><b>k=0:</b> \\(x^0=(0,0)\\), \\(W=\\{{3,4\\}}\\), \\(g^0=(-2,-1)\\), \\(d^0=0\\). Nhân tử: \\(\\hat\\mu_3=-2\\), \\(\\hat\\mu_4=-1\\) (slide ghi \\(\\hat\\mu_4=1\\), nhầm dấu). Loại ràng buộc 3 (âm nhất) ⇒ \\(W_1=\\{{4\\}}\\).</li>'
       f'<li><b>k=1:</b> \\(W=\\{{4\\}}\\), \\(d^1=(1,0)\\ne0\\). \\(\\alpha_1=\\min\\{{1,\\ 1,\\ 0.5\\}}=0.5\\) (ràng buộc cản 2: \\(3x_1+x_2\\le1.5\\)). \\(x^2=(0.5,0)\\), \\(W_2=\\{{2,4\\}}\\).</li></ul>',
       kicker=M + ' · PHẦN 5', img='m3:72',
       explain='<p>Ở vòng 0 điểm \\((0,0)\\) đang “bị ép” bởi hai trục nhưng nhân tử \\(\\hat\\mu_3<0\\) cho biết trục \\(x_1=0\\) đang cản đường đi xuống. Bỏ nó đi, ta di chuyển dọc trục \\(x_1\\) tới khi chạm tường \\(3x_1+x_2=1.5\\) tại \\(x_1=0.5\\).</p>'))
add(sl('Vòng 2, 3, 4 và kết luận',
       f'<ul><li><b>k=2:</b> \\(x^2=(0.5,0)\\), \\(W=\\{{2,4\\}}\\), \\(d^2=0\\). \\(\\hat\\mu_2=1/3\\), \\(\\hat\\mu_4=-2/3\\) ⇒ loại 4, \\(W_3=\\{{2\\}}\\).</li>'
       f'<li><b>k=3:</b> \\(d^3=(-0.1,0.3)\\), \\(\\alpha_3=1\\) (không bị cản) ⇒ \\(x^4=(0.4,0.3)\\).</li>'
       f'<li><b>k=4:</b> \\(d^4=0\\), \\(\\hat\\mu_2=0.4>0\\) ⇒ <b>dừng</b>.</li></ul>'
       f'<p>Nghiệm \\(x^*=(0.4,0.3)\\), \\(f(x^*)=(0.4-1)^2+(0.3-0.5)^2=0.4\\) (khớp scipy).</p>',
       kicker=M + ' · PHẦN 5', img='m3:79',
       explain='<p>Từ \\((0.5,0)\\) thuật toán bỏ trục \\(x_2=0\\), chỉ dựa vào tường \\(3x_1+x_2=1.5\\) rồi trượt dọc tường tới điểm gần \\((1,0.5)\\) nhất (\\(d^3\\perp\\) tường thì hướng \\(d^3\\propto(-1,3)\\) đúng dọc tường). Dùng công cụ “Duyệt từng bước” bên dưới để xem trực quan.</p>'))
add(sl('Bài tập (slide tr.81) và kết quả',
       '<p>\\(\\min(x_1-4.5)^2+(x_2-3)^2\\) s.t. \\(2x_1-3x_2\\le6,\\ x_1+x_2\\le5,\\ -3x_1+5x_2\\le15,\\ -x_1\\le0,\\ -x_2\\le0\\); \\(x^0=(0,0)\\).</p>'
       f'<p>Slide gợi ý “4 bước lặp”, \\(x^*=(3.25,1.75)^\\top\\). Mô phỏng (đã kiểm bằng scipy): \\(x^*=({AB["x*"][0]},{AB["x*"][1]})\\), \\(f={f4(AB["f"])}\\). Với \\(W_0=\\{{4,5\\}}\\) thuật toán cần {AB["iters"]} vòng (3 lần di chuyển, 3 lần loại ràng buộc, 1 lần dừng).</p>',
       kicker=M + ' · PHẦN 5', img='m3:81',
       explain='<p>Con số “4 bước” trong gợi ý có thể đếm theo cách khác (ví dụ chỉ đếm vòng có \\(d^k\\ne0\\) hoặc chọn \\(W_0\\) khác). Điều quan trọng là kết quả cuối \\((3.25,1.75)\\) khớp. Bạn nên tự lần lại từng vòng, rồi so với công cụ bên dưới.</p>'))
add(sl('Tổng kết Module 3',
       '<ul><li>QP: mục tiêu bậc hai, miền polyhedron; LP ⊂ QP; Q ⪰ 0 ⇒ QP lồi.</li><li>Tồn tại nghiệm: Frank–Wolfe, Eaves; Q ≻ 0 chỉ cần Δ ≠ ∅.</li><li>Tập nghiệm: đóng; Q≻0 duy nhất; Q≺0 tại đỉnh; Q⪰0 lồi.</li><li>Null space: KKT tuyến tính; Z, Y; \\(Z^\\top QZ\\succ0\\).</li><li>Active set: bài toán con + \\(\\alpha_k\\) + nhân tử; loại ràng buộc có \\(\\hat\\mu<0\\).</li></ul>'
       '<p>Tiếp theo trong đề cương (buổi 7–8): QP tổng quát, SQP và phương pháp điểm trong; đối chiếu bằng phần mềm (scipy, cvxpy).</p>',
       kicker=M + ' · TỔNG KẾT',
       explain='<p>Bạn đã có đủ nền tảng: tính lồi (Module 1), điều kiện KKT (Module 2), và hai thuật toán giải QP (Module 3). Bước tiếp theo trong học phần là tối ưu không ràng buộc (gradient, Newton) và các phương pháp cho bài toán phi tuyến tổng quát.</p>'))

# =====================================================================  SECTIONS
SECTIONS = []
SECTIONS.append(('cong-thuc', 'Công thức cốt lõi',
    formula('QP', r'\min\ \tfrac12x^\top Qx+c^\top x+\alpha\quad\text{s.t.}\ x\in\Delta=\{Ax\ge b,\ Cx=d\},\qquad Q=Q^\top')
    + formula('KKT của QP đẳng thức (hệ 4.2)', r'\begin{pmatrix}Q&A^\top\\A&0\end{pmatrix}\begin{pmatrix}d\\\mu\end{pmatrix}=\begin{pmatrix}-g\\b-Ax\end{pmatrix},\quad g=Q\bar x+c')
    + formula('Null space', r'd=Yd_Y+Zd_Z:\ \ AYd_Y=\bar b,\ \ (Z^\top QZ)d_Z=-Z^\top(QYd_Y+\bar g),\ \ (AY)^\top\mu=-Y^\top(\bar g+Qd)')
    + formula('Active set: độ dài bước', r'\alpha_k=\min\Big\{1,\ \min_{i\notin W_k,\ a_i^\top d^k>0}\frac{b_i-a_i^\top x^k}{a_i^\top d^k}\Big\}')
    + table(['Bước', 'Dấu hiệu', 'Hành động'],
            [['\\(d^k\\ne0\\)', 'còn hướng giảm với \\(W_k\\) hiện tại', 'đi \\(x^{k+1}=x^k+\\alpha_kd^k\\); thêm ràng buộc cản'], ['\\(d^k=0\\), mọi \\(\\hat\\mu\\ge0\\)', 'KKT thỏa', 'DỪNG: nghiệm toàn cục (Q ⪰ 0)'], ['\\(d^k=0\\), có \\(\\hat\\mu<0\\)', 'ràng buộc đang cản đường', 'loại chỉ số có \\(\\hat\\mu\\) âm nhất']])))
SECTIONS.append(('lich-su', 'Bối cảnh lý thuyết và lịch sử', callout('hist', '📜 Bối cảnh lý thuyết & lịch sử',
    '<p>Định lý <b>Frank–Wolfe</b> (Marguerite Frank và Philip Wolfe, 1956) xuất hiện trong bài báo về thuật toán cho quy hoạch toàn phương; nó khẳng định hàm toàn phương bị chặn dưới trên polyhedron thì đạt cực tiểu. Điều kiện Eaves cho sự tồn tại nghiệm của QP tổng quát (không lồi) mang tên B. C. Eaves (1971). Slide tham chiếu chuyên khảo của Lee, Tam và Yen (2005) về QP và bất đẳng thức biến phân affine.</p>'
    '<p>QP nổi tiếng trong tài chính nhờ Harry Markowitz (1952, lý thuyết danh mục đầu tư). Các phương pháp tập hoạt động cho QP được phát triển từ cuối thập niên 1950 (Beale, Wolfe) và vẫn là nền của các bộ giải hiện đại, bên cạnh phương pháp điểm trong.</p>')))
S_case = ('<p><b>Bài toán “hiệu chỉnh kế hoạch gần nhất”</b> (chính là ví dụ của slide tr.69): kế hoạch mong muốn là \\((1,\\ 0.5)\\) (đơn vị: tấn) nhưng hai nguồn lực giới hạn \\(x_1+x_2\\le1\\), \\(3x_1+x_2\\le1.5\\) và không sản xuất âm. Tìm kế hoạch khả thi <b>gần kế hoạch mong muốn nhất</b> theo khoảng cách Euclid.</p>'
          + steps(['Mô hình: \\(\\min(x_1-1)^2+(x_2-0.5)^2\\) — QP với \\(Q=2I\\succ0\\), \\(c=(-2,-1)\\). Vì \\(Q\\succ0\\) và \\(\\Delta\\ne\\emptyset\\), có <b>nghiệm duy nhất</b> (Hệ quả 3, Định lý 3.3).',
                   f'Active set từ \\(x^0=(0,0)\\): {len(AE["log"])} vòng, kết quả \\(x^*=({AE["x*"][0]},{AE["x*"][1]})\\).',
                   'Kiểm KKT: tại \\(x^*\\) chỉ ràng buộc 2 chặt: \\(3(0.4)+0.3=1.5\\) ✓; \\(Qx^*+c=(-1.2,-0.4)\\); \\(\\hat\\mu_2=0.4\\) từ \\((-1.2,-0.4)+\\hat\\mu_2(3,1)=0\\) ✓ (cả hai thành phần cùng cho \\(0.4\\)).',
                   f'Khoảng cách bình phương tối thiểu \\(f(x^*)={f4(AE["f"])}\\), tức hiệu chỉnh \\(\\sqrt{{0.4}}\\approx0.632\\) tấn.'])
          + callout('good', 'Điều học được', '<p>Nhân tử \\(\\hat\\mu_2=0.4\\) là “giá” của nguồn lực thứ hai: nới \\(3x_1+x_2\\le1.5\\) thêm một chút \\(\\delta\\) làm khoảng cách giảm khoảng \\(0.4\\delta\\).</p>'))
SECTIONS.append(('case-study', '🔎 Case study: hiệu chỉnh kế hoạch gần nhất', S_case))

def ex(t, b): return solution(t, b)
EXS = ''
EXS += ex('Ví dụ 1 — đối xứng hóa Q',
    '<p>\\(Q=\\begin{pmatrix}1&4\\\\0&3\\end{pmatrix}\\Rightarrow Q_s=\\tfrac12(Q+Q^\\top)=\\begin{pmatrix}1&2\\\\2&3\\end{pmatrix}\\). Với \\(x=(2,-1)\\): \\(x^\\top Qx=1\\cdot4+4\\cdot(2)(-1)+3\\cdot1=4-8+3=-1\\); \\(x^\\top Q_sx=4+2\\cdot2\\cdot(2)(-1)+3=4-8+3=-1\\) ✓ (code: ' + str(R['m3_sym']['xQx']) + ' và ' + str(R['m3_sym']['xQsx']) + ').</p>')
EXS += ex('Ví dụ 2 — QP không lồi trên hình hộp (slide tr.16)',
    '<p>\\(\\min x_1^2-x_2^2\\) trên \\([1,3]^2\\): giá trị tại bốn đỉnh \\((1,1),(1,3),(3,1),(3,3)\\) lần lượt \\(0,-8,8,0\\) ⇒ cực tiểu \\(-8\\) tại \\((1,3)\\) (SLSQP: ' + str(R['m3_nonconvex_box_num']) + '). Hàm lõm theo \\(x_2\\) nên cực tiểu ở biên \\(x_2=3\\).</p>')
EXS += ex('Ví dụ 3 — tồn tại nghiệm: \\(\\min x_1\\) trên \\(x_1x_2\\ge1\\)',
    '<p>\\(\\Delta=\\{x_1x_2\\ge1,x_1,x_2\\ge0\\}\\) không phải polyhedron. \\(x_1=t\\), \\(x_2=1/t\\): \\(f=t\\to0\\) khi \\(t\\to0^+\\) nên \\(\\bar\\theta=0\\); nhưng \\(x_1>0\\) trên \\(\\Delta\\) nên không đạt: <b>không có nghiệm</b>. Đây là phản ví dụ khi bỏ giả thiết polyhedron của Frank–Wolfe.</p>')
EXS += ex('Ví dụ 4 — \\(\\mathrm{loc}(P)\\) không đóng (slide tr.38)',
    '<p>\\(\\min-x_2^2+x_1x_2\\) trên \\(x\\ge0\\). Với \\(x_1>0\\): \\(f(x_1,x_2)=x_2(x_1-x_2)\\ge0=f(x_1,0)\\) khi \\(x_2\\in[0,x_1]\\) ⇒ \\((x_1,0)\\) là cực tiểu địa phương. Tại \\((0,0)\\): \\(f(0,t)=-t^2<0\\) ⇒ không. \\(f(0,t)\\to-\\infty\\) ⇒ \\(\\mathrm{Sol}=\\emptyset\\). \\(\\mathrm{loc}=\\{x_1>0,x_2=0\\}\\) không đóng.</p>')
EXS += ex('Ví dụ 5 — null space (slide tr.56–58) từng bước',
    steps(['\\(Q,c,A,b\\) như slide; \\(\\bar x=0\\Rightarrow\\bar g=c=(10,-26,-2)\\), \\(\\bar b=b=(4,10)\\).',
           '\\(Z=(-1,1,1)^\\top\\) (kiểm \\(AZ=(-1+1,\\ -1+1)=0\\)); \\(Y\\) như trên có \\(AY=I\\) (code: ' + str(R['m3_null_YZ']['AY']) + ').',
           '\\(d_Y=(AY)^{-1}\\bar b=(4,10)\\). \\(Z^\\top QZ=' + f4(nsteps['ZtQZ'][0][0]) + '\\).',
           '\\(d_Z=-(Z^\\top QYd_Y+Z^\\top\\bar g)/(Z^\\top QZ)=' + f4(nsteps['dZ'][0]) + '\\). \\(d=Yd_Y+Zd_Z=(' + ', '.join(f4(v) for v in nsteps['d']) + ')\\).',
           '\\(\\mu\\): \\((AY)^\\top\\mu=-Y^\\top(\\bar g+Qd)\\Rightarrow\\mu=(' + ', '.join(f4(v) for v in nsteps['mu']) + ')\\).',
           'Kết luận: \\(x^*=(' + ', '.join(f4(v) for v in ne['x*']) + ')\\); giá trị \\(\\tfrac12x^{*\\top}Qx^*+c^\\top x^*=' + f4(ne['f']) + '\\). Đối chiếu SLSQP: ' + str(R['m3_null_ex_num']) + '. Nếu cực tiểu đúng <i>đa thức ghi trên slide</i> thì nghiệm là \\((' + ', '.join(f4(v) for v in ER['true_opt_of_polynomial']['x']) + ')\\), \\(f=' + f4(ER['true_opt_of_polynomial']['f']) + '\\).']))
EXS += ex('Ví dụ 6 — Bài tập 1 (tr.59) với hai phiên bản ràng buộc',
    '<p>Hessian \\(\\begin{pmatrix}6&2&1\\\\2&5&2\\\\1&2&4\\end{pmatrix}\\succ0\\), \\(c=(-8,-3,-3)\\), \\(A=\\begin{pmatrix}1&0&1\\\\0&1&1\\end{pmatrix}\\).</p>'
    '<p>(a) \\(b=(0,0)\\): giải hệ KKT \\(6\\times6\\)… → \\(x^*=(' + ', '.join(f4(v) for v in BT1['x*']) + ')\\), \\(\\mu=(' + ', '.join(f4(v) for v in BT1['mu']) + ')\\), \\(f=' + f4(BT1['f']) + '\\).</p>'
    '<p>(b) \\(b=(3,0)\\): \\(x^*=(2,-1,1)\\) (khớp ĐS slide), \\(\\mu=(' + ', '.join(f4(v) for v in EB['mu']) + ')\\), \\(f=' + f4(EB['f']) + '\\).</p>')
lg = AE['log']
def logrows(log):
    out = []
    for s in log:
        mu = ', '.join(f'\\(\\hat\\mu_{k}={f4(v)}\\)' for k, v in s.get('mu', {}).items()) if 'mu' in s else '—'
        out.append([str(s['k']), '\\((' + ', '.join(f4(v) for v in s['x']) + ')\\)', '\\(\\{' + ','.join(map(str, s['W'])) + '\\}\\)', '\\((' + ', '.join(f4(v) for v in s['d']) + ')\\)', f4(s['alpha']) if 'alpha' in s else '—', mu, s['action']])
    return out
EXS += ex('Ví dụ 7 — active set: bảng vết đầy đủ (slide tr.69–79)',
    '<p>Số liệu do script mô phỏng thuật toán (không gõ tay):</p>' + table(['k', '\\(x^k\\)', '\\(W_k\\)', '\\(d^k\\)', '\\(\\alpha_k\\)', 'Nhân tử', 'Hành động'], logrows(lg)))
EXS += ex('Ví dụ 8 — active set: bài tập tr.81',
    '<p>\\(W_0=\\{4,5\\}\\) (ràng buộc \\(-x_1\\le0\\), \\(-x_2\\le0\\)). Bảng vết:</p>' + table(['k', '\\(x^k\\)', '\\(W_k\\)', '\\(d^k\\)', '\\(\\alpha_k\\)', 'Nhân tử', 'Hành động'], logrows(AB['log'])) + f'<p>Kết quả \\(x^*=(3.25,1.75)\\), \\(f={f4(AB["f"])}\\) (khớp ĐS).</p>')
SECTIONS.append(('vi-du', 'Ví dụ chi tiết (có lời giải từng bước)', '<p>Bấm từng ví dụ để mở lời giải. Bảng vết active set do script sinh.</p>' + EXS))
SECTIONS.append(('so-do', 'Sơ đồ tổng hợp', fig('d4-active-set', 'Lưu đồ thuật toán tập hoạt động (drawio)') + fig('d6-qp-theo-Q', 'Tính chất nghiệm của QP theo dạng của Q')))
SECTIONS.append(('tuong-tac', 'Thực hành tương tác', WIDGET + widget('qp-eq-solver')))
SECTIONS.append(('bay', 'Cảnh báo bẫy diễn giải sai',
    callout('warn', 'Bẫy 1 — Hệ số 1/2', '<p>\\(f=\\tfrac12x^\\top Qx+\\dots\\) có Hessian \\(=Q\\). Từ đa thức phải nhân đôi hệ số các số hạng \\(x_i^2\\) để có \\(Q_{ii}\\).</p>')
    + callout('warn', 'Bẫy 2 — QP lồi cần Q ⪰ 0, nhưng Hessian rút gọn mới quyết định null space', '<p>Với QP đẳng thức chỉ cần \\(Z^\\top QZ\\succ0\\); Q có thể không xác định dương trên toàn không gian.</p>')
    + callout('warn', 'Bẫy 3 — Dấu nhân tử trong active set', '<p>Dạng \\(a_i^\\top x\\le b_i\\) và \\(Qx+c+\\sum\\hat\\mu_ia_i=0\\) đòi \\(\\hat\\mu_i\\ge0\\). Nếu viết ràng buộc dạng \\(\\ge\\), dấu ngược lại.</p>')
    + callout('warn', 'Bẫy 4 — Bước \\(\\alpha_k\\)', '<p>Chỉ tính tỉ số cho \\(i\\notin W_k\\) với \\(a_i^\\top d^k>0\\); các ràng buộc có \\(a_i^\\top d\\le0\\) không cản.</p>')
    + callout('warn', 'Bẫy 5 — Loại nhiều ràng buộc một lúc', '<p>Mỗi lần chỉ loại <b>một</b> ràng buộc (nhân tử âm nhất), rồi giải lại bài toán con.</p>')
    + callout('warn', 'Bẫy 6 — Chỗ chưa khớp trong slide', '<p>Ví dụ null space (giá trị hàm mục tiêu), Bài tập 1 (ràng buộc), Hệ quả 4, vectơ c ở tr.55: xem trang “Kiểm chứng”.</p>')))
READING = ('<ul><li>Boyd &amp; Vandenberghe: 4.4 “Quadratic optimization problems” (tr.152), 10.1–10.2 “Equality constrained minimization” (tr.521–525) — file <code>bv_cvxbook.pdf</code>.</li>'
           '<li>Lee, G.M., Tam, N.N., Yen, N.D.: <i>Quadratic Programming and Affine Variational Inequalities</i>, Springer 2005 (tài liệu tham khảo của slide cho các dạng QP còn lại).</li>'
           '<li>Nocedal &amp; Wright, <i>Numerical Optimization</i>, ch.16 (Quadratic programming): phương pháp active set.</li>'
           '<li>Tiếp theo theo đề cương: tối ưu không ràng buộc, SQP, phương pháp điểm trong.</li></ul>')
