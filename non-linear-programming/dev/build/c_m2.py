"""Nội dung Module 2 — Tối ưu có ràng buộc & KKT (bám Slides/2_NonlinearProgram_KKT_250418.pdf)."""
import numpy as np
from helpers import *

M = 'MODULE 2'
LEAD = 'Từ bài toán tối ưu phi tuyến có ràng buộc tổng quát tới điều kiện Karush–Kuhn–Tucker: hàm Lagrange, nhân tử, điều kiện bù, điều kiện chính quy Slater, và khi nào KKT là điều kiện cần và đủ.'
META = ['Nguồn: Slide 2, ORLab Phenikaa (68 trang)', 'Boyd & Vandenberghe: Ch.4–5', 'Thời lượng gợi ý: 5–6 giờ']
OBJECTIVES = [
    'Viết bài toán phi tuyến ở dạng chuẩn (\\(g_i\\le0\\), \\(h_j=0\\)), xác định bài toán lồi và giải thích vì sao \\(h_j\\) phải affine.',
    'Lập hàm Lagrange, viết đúng hệ KKT (dừng, khả thi, bù, dấu nhân tử) và giải bằng cách chia trường hợp theo tập ràng buộc chặt.',
    'Kiểm tra điều kiện Slater và dùng định lý “cần và đủ” cho bài toán lồi.',
    'Phân biệt điểm KKT với cực tiểu thật sự trong bài toán không lồi (min xy trên đĩa).',
    'Nhận ra khi nào bài toán có nhân tử không duy nhất, nghiệm không duy nhất, và phát hiện chỗ chưa khớp trong ví dụ của slide.',
]

# ---- số liệu tính lúc build ----
sig = np.array([0.10, 0.15, 0.20]); C = np.array([[1, .8, .2], [.8, 1, .9], [.2, .9, 1]])
Sg = np.outer(sig, sig) * C
w_un = np.linalg.solve(Sg, np.ones(3)); w_un /= w_un.sum()
idx = [0, 2]
S2 = Sg[np.ix_(idx, idx)]; w2 = np.linalg.solve(S2, np.ones(2)); w2 /= w2.sum()
w_star = np.array([w2[0], 0.0, w2[1]])
mu_sum = 2 * float(w_star @ Sg @ w_star)          # từ 2(Σw)_i = μ với i có w_i>0
lam2 = 2 * float((Sg @ w_star)[1]) - mu_sum          # 2(Σw)_2 - μ = λ_2 ≥ 0 (ràng buộc w_2≥0 dạng -w_2≤0)
var_star = float(w_star @ Sg @ w_star)
def f4(x): return ('%.4f' % x).rstrip('0').rstrip('.')
def f6(x): return ('%.6f' % x).rstrip('0').rstrip('.')

DECK = []
add = DECK.append

add(sl('Từ bài toán có ràng buộc tới điều kiện KKT',
       '<p>Module này bám <b>Slide 2</b> (68 trang, ORLab, 2024): bài toán tối ưu có ràng buộc, điều kiện cần cực trị và điều kiện cần và đủ.</p>'
       '<ol><li>Bài toán phi tuyến tổng quát và bài toán lồi</li><li>Các bài toán lồi và ứng dụng</li><li>Hàm Lagrange và điều kiện cần KKT</li><li>Điều kiện Slater và điều kiện cần và đủ</li><li>Bốn ví dụ và câu hỏi thảo luận</li></ol>'
       + callout('info', 'Ý tưởng một câu', '<p>Tại nghiệm tối ưu, hướng giảm nhanh nhất của f không thể “đẩy” điểm vào miền khả thi được nữa: \\(-\\nabla f\\) bị các gradient ràng buộc chặt “chặn lại”. Nhân tử Lagrange đo mức độ chặn đó.</p>'),
       kicker=M + ' · MỞ ĐẦU', img='m2:1',
       explain='<p>Ở Module 1 ta học cách nhận ra hàm/tập lồi. Bây giờ ta dùng chúng để giải bài toán có ràng buộc \\(g_i(x)\\le0\\), \\(h_j(x)=0\\).</p>'))

# ---------------- PHẦN 1
add(part(1, 5, 'Bài toán tối ưu phi tuyến và bài toán lồi', ['Dạng tổng quát, tập chỉ số, tập chấp nhận', 'Bài toán lồi: cực tiểu địa phương = toàn cục', 'Vì sao ràng buộc đẳng thức phải affine'], M))
add(sl('Bài toán tối ưu phi tuyến tổng quát',
       formula('Bài toán (P)', r'\min\ f(x)\quad\text{s.t.}\quad g_i(x)\le0\ (i\in I),\quad h_j(x)=0\ (j\in J),\quad x\in\mathbb R^n')
       + '<ul><li>\\(x\\): biến số; \\(f:\\mathbb R^n\\to\\mathbb R\\): hàm mục tiêu</li><li>\\(g_i\\): ràng buộc bất đẳng thức; \\(h_j\\): ràng buộc đẳng thức</li><li>\\(I=\\{1,\\dots,n\\}\\), \\(J=\\{1,\\dots,p\\}\\): tập chỉ số</li></ul>'
       + formula('Tập chấp nhận được', r'C=\{x\in\mathbb R^n\mid g_i(x)\le0\ \forall i\in I,\ h_j(x)=0\ \forall j\in J\}'),
       kicker=M + ' · PHẦN 1', img='m2:37',
       explain='<p>Mọi bài toán tối ưu “có điều kiện” đều đưa được về dạng này: mục tiêu là làm nhỏ f, điều kiện là “nằm trong C”. Ràng buộc \\(g\\ge0\\) đổi thành \\(-g\\le0\\); bài toán max đổi thành min của \\(-f\\).</p><p>Chú ý ký hiệu: slide dùng \\(n\\) cho số ràng buộc bất đẳng thức ở tr.4 và \\(m\\) ở tr.17; khi đọc hãy hiểu đó là số phần tử của \\(I\\).</p>'))
add(sl('Bài toán tối ưu lồi',
       formula('Dạng tập', r'\min_{x\in C} f(x)') + '<ul><li>Hàm mục tiêu f: <b>lồi</b></li><li>Tập chấp nhận được C: <b>lồi</b></li><li>Cực tiểu (nghiệm) <b>địa phương</b> cũng là cực tiểu (nghiệm) <b>toàn cục</b></li></ul>',
       kicker=M + ' · PHẦN 1', img='m2:11',
       explain='<p>Đây là “phần thưởng” của tính lồi: không cần lo mắc kẹt ở cực tiểu địa phương. Bằng chứng ngắn: nếu \\(x\\) là cực tiểu địa phương nhưng có \\(y\\in C\\) với \\(f(y)<f(x)\\), thì các điểm \\(z_t=(1-t)x+ty\\in C\\) khi \\(t\\to0\\) có \\(f(z_t)\\le(1-t)f(x)+tf(y)<f(x)\\), mâu thuẫn với tính cực tiểu địa phương.</p>'))
add(sl('Dạng chuẩn của bài toán lồi',
       formula('Bài toán lồi (P)', r'\min f(x)\ \ \text{s.t.}\ \ g_i(x)\le0,\ \ h_j(x)=0,\qquad f,g_i\ \text{lồi},\ \ h_j\ \text{affine}')
       + callout('good', 'Giải thích “\\(h_j\\) affine”', '<p>\\(h_j(x)=0\\) tương đương \\(h_j\\le0\\) và \\(-h_j\\le0\\). Tập \\(\\{h\\le0\\}\\) lồi khi h lồi; \\(\\{-h\\le0\\}\\) lồi khi \\(-h\\) lồi. Muốn dùng được cả hai, h phải vừa lồi vừa lõm, tức h là hàm <b>affine</b>: \\(h(x)=a^\\top x+b\\).</p>'),
       kicker=M + ' · PHẦN 1', img='m2:16',
       explain='<p>Slide đặt câu hỏi “(Giải thích!!)” ngay chỗ này. Ví dụ \\(h(x)=x_1^2+x_2^2-1=0\\) (đường tròn) không affine, và tập đường tròn không lồi: nối hai điểm đối xứng trên đường tròn được đoạn đi qua tâm, nằm ngoài đường tròn.</p>'))

# ---------------- PHẦN 2
add(part(2, 5, 'Các bài toán lồi và ứng dụng', ['Danh sách các lớp bài toán lồi', 'Ứng dụng trong thực tế', 'LP và QP lồi'], M))
add(sl('Các bài toán lồi hoặc đưa được về lồi',
       '<ul><li>Least squares (bình phương tối thiểu)</li><li>Linear programming (quy hoạch tuyến tính)</li><li>Convex quadratic minimization with linear constraints</li><li>Quadratic minimization with convex quadratic constraints</li><li>Conic optimization</li><li>Geometric programming</li><li>Second order cone programming (SOCP)</li><li>Semidefinite programming (SDP)</li></ul>',
       kicker=M + ' · PHẦN 2', img='m2:24',
       explain='<p>Đây là “bản đồ” các bài toán lồi từ đơn giản (LP) đến tổng quát (SDP). Mỗi lớp là trường hợp riêng của lớp sau: LP ⊂ QP lồi ⊂ QCQP ⊂ SOCP ⊂ SDP. Bạn đã gặp LP trong môn Quy hoạch tuyến tính; Module 3 nghiên cứu QP.</p>'))
add(sl('Những bài toán lồi có nhiều ứng dụng',
       '<div style="display:flex;gap:2em;flex-wrap:wrap"><ul><li>Portfolio optimization</li><li>Worst-case risk analysis</li><li>Optimal advertising</li><li>Statistical regression (regularization, quantile regression)</li><li>Model fitting (multiclass classification)</li></ul>'
       '<ul><li>Electricity generation optimization</li><li>Combinatorial optimization (nới lồi)</li><li>Non-probabilistic modelling of uncertainty</li><li>Localization using wireless signals</li></ul></div>',
       kicker=M + ' · PHẦN 2', img='m2:29',
       explain='<p>Mỗi ứng dụng đều quy về “tối thiểu hóa một hàm lồi trong một tập lồi”. Case study bên dưới giải một bài toán danh mục đầu tư (portfolio) cụ thể bằng KKT.</p>'))
add(sl('LP và QP lồi là hai bài toán lồi tiêu biểu',
       formula('Quy hoạch tuyến tính', r'\min\ c^\top x+d\quad\text{s.t.}\ Gx\le h,\ Ax=b')
       + formula('Quy hoạch toàn phương lồi', r'\min\ \tfrac12x^\top Px+q^\top x+r\quad\text{s.t.}\ Gx\le h,\ Ax=b,\qquad P\succeq0'),
       kicker=M + ' · PHẦN 2', img='m2:68',
       explain='<p>Hai bài toán này chỉ khác nhau ở hàm mục tiêu: tuyến tính hay toàn phương lồi (\\(P\\succeq0\\)). Trong QP lồi, miền chấp nhận vẫn là polyhedron. Module 3 giải QP bằng null space và active set.</p>'))

# ---------------- PHẦN 3
add(part(3, 5, 'Hàm Lagrange và điều kiện cần KKT', ['Hàm Lagrange \\(L(x,\\lambda,\\mu)\\)', 'Định lý điều kiện cần cực trị', 'Điều kiện bù và điểm KKT'], M))
add(sl('Hàm Lagrange',
       formula('Hàm Lagrange', r'L(x,\lambda,\mu)=f(x)+\sum_{i\in I}\lambda_ig_i(x)+\sum_{j\in J}\mu_jh_j(x)',
               [(r'\lambda_i', 'nhân tử của ràng buộc bất đẳng thức, cần \\(\\ge0\\)'), (r'\mu_j', 'nhân tử của ràng buộc đẳng thức, dấu tùy ý')]),
       kicker=M + ' · PHẦN 3', img='m2:38',
       explain='<p>Ý tưởng “phạt”: cộng vào f một khoản phạt \\(\\lambda_ig_i\\) khi vi phạm ràng buộc. Nhân tử \\(\\lambda_i\\ge0\\) sao cho khoản phạt đẩy nghiệm về phía khả thi (khi \\(g_i>0\\) thì \\(\\lambda_ig_i>0\\) làm L tăng).</p>'))
add(sl('Định lý: điều kiện cần cực trị',
       '<p>Nếu \\(x^*\\) là nghiệm tối ưu của (P) thì tồn tại \\(\\lambda_i\\ (i\\in I)\\), \\(\\mu_j\\ (j\\in J)\\) sao cho:</p>'
       + formula('Hệ KKT', r'\begin{cases}\nabla_xL(x^*,\lambda,\mu)=0&\text{(dừng)}\\ \lambda_ig_i(x^*)=0\ \ \forall i&\text{(bù)}\\ g_i(x^*)\le0,\ h_j(x^*)=0&\text{(khả thi gốc)}\\ \lambda_i\ge0,\ \mu_j\in\mathbb R&\text{(khả thi đối ngẫu)}\end{cases}')
       + callout('warn', 'Lưu ý về điều kiện chính quy', '<p>Slide phát biểu gọn; định lý “cần” đúng khi có <b>điều kiện chính quy</b> (Slater cho bài lồi, hoặc LICQ/MFCQ nói chung). Ví dụ \\(\\min x\\) s.t. \\(x^2\\le0\\): nghiệm \\(x^*=0\\) nhưng không tồn tại \\(\\lambda\\).</p>'),
       kicker=M + ' · PHẦN 3', img='m2:40',
       explain='<p>Bốn dòng của hệ: (1) đạo hàm của L theo x bằng 0; (2) điều kiện bù: mỗi tích \\(\\lambda_ig_i\\) bằng 0 (hoặc ràng buộc chặt, hoặc nhân tử bằng 0); (3) điểm phải khả thi; (4) \\(\\lambda_i\\ge0\\).</p>'))
add(sl('Ý nghĩa từng thành phần',
       '<ul><li>\\(g_i(x^*)\\le0,\\ h_j(x^*)=0\\): \\(x^*\\) là điểm chấp nhận được.</li><li>\\(\\lambda_ig_i(x^*)=0\\): <b>điều kiện bù</b> (complementary slackness).</li><li>\\(\\lambda_i,\\mu_j\\): các <b>nhân tử Lagrange</b>.</li>'
       '<li>Điểm \\(x^*\\) thỏa hệ (1) gọi là <b>điểm KKT</b> (điểm dừng KKT).</li></ul>'
       + table(['Trường hợp với \\(g_i\\)', 'Hệ quả cho \\(\\lambda_i\\)'], [['\\(g_i(x^*)<0\\) (không chặt)', '\\(\\lambda_i=0\\): ràng buộc “không ảnh hưởng”'], ['\\(g_i(x^*)=0\\) (chặt)', '\\(\\lambda_i\\ge0\\): có thể dương']]),
       kicker=M + ' · PHẦN 3', img='m2:43',
       explain='<p>Điều kiện bù chia bài toán thành các “trường hợp”: mỗi ràng buộc \\(g_i\\) hoặc chặt (nằm sát biên) hoặc lỏng (nhân tử bằng 0). Với m ràng buộc bất đẳng thức có tối đa \\(2^m\\) trường hợp cần xét.</p>'))
add(sl('Ý nghĩa hình học của KKT',
       formula('Dừng', r'\nabla f(x^*)=-\sum_i\lambda_i\nabla g_i(x^*)-\sum_j\mu_j\nabla h_j(x^*)')
       + '<p>Với \\(\\lambda_i\\ge0\\): vectơ \\(-\\nabla f(x^*)\\) nằm trong nón sinh bởi các gradient \\(\\nabla g_i\\) của các ràng buộc <b>chặt</b>. Không thể giảm f mà vẫn khả thi.</p>'
       '<p>Thử ngay ở “Phòng thí nghiệm KKT” bên dưới: mũi tên đỏ (∇f) phải ngược hướng với các mũi tên xanh (∇g) tại điểm KKT.</p>',
       kicker=M + ' · PHẦN 3',
       explain='<p>Ví dụ trực giác: bóng lăn xuống dốc (hướng \\(-\\nabla f\\)) trong một cái sân bị tường bao quanh. Nó dừng ở chân tường khi lực đẩy của tường (\\(\\lambda\\nabla g\\)) cân bằng với lực kéo xuống dốc. Tường càng phải “đỡ” mạnh thì nhân tử \\(\\lambda\\) càng lớn.</p>'))

# ---------------- PHẦN 4
add(part(4, 5, 'Điều kiện Slater và điều kiện cần và đủ', ['Điều kiện chính quy Slater', 'Khi Slater không thỏa mãn', 'Định lý cần và đủ cho bài toán lồi'], M))
add(sl('Điều kiện chính quy Slater',
       '<div class="callout good"><span class="ct"><b>Slater (CQ)</b></span>Bài toán (P) thỏa Slater nếu tồn tại \\(z\\in C\\) với \\(g_i(z)<0\\ \\ \\forall i=1,\\dots,m\\).</div>'
       '<p>Nghĩa là tồn tại điểm khả thi <b>thỏa chặt</b> mọi ràng buộc bất đẳng thức (điểm “trong” của miền). Với ràng buộc đẳng thức affine chỉ cần điểm đó thuộc miền.</p>'
       '<p>Slater bảo đảm <b>đối ngẫu mạnh</b> cho bài toán lồi (Boyd).</p>',
       kicker=M + ' · PHẦN 4', img='m2:47',
       explain='<p>Kiểm tra Slater rất đơn giản: tìm <i>một</i> điểm khả thi làm cho mọi bất đẳng thức là bất đẳng thức chặt. Ví dụ miền \\(x^2+y^2\\le4\\), \\(x+y\\ge2\\) có điểm \\((1.2,1.2)\\) làm cả hai chặt, nên thỏa Slater.</p>'))
add(sl('Khi Slater không thỏa mãn',
       '<p>Slide tr.48 minh họa hai tình huống miền không có điểm trong: (a) không đủ hạng dòng (ràng buộc suy biến), (b) miền không có điểm trong (chỉ có biên).</p>'
       '<ul><li>Ví dụ (b): \\(\\{x\\mid x^2\\le0\\}=\\{0\\}\\) — mọi điểm khả thi làm \\(g=0\\), không có điểm nào \\(g<0\\).</li><li>Hệ quả: KKT có thể <b>không</b> là điều kiện cần (\\(\\min x\\) s.t. \\(x^2\\le0\\)).</li></ul>',
       kicker=M + ' · PHẦN 4', img='m2:48',
       explain='<p>Hai hình trong slide: bên trái là hai vùng tròn chạm nhau tại điểm hoặc cạnh; bên phải là miền hình parabol, điểm z nằm ngoài. Hình dung “Slater fail” là khi miền khả thi <i>quá mỏng</i> (không có “ruột”).</p>'))
add(sl('Định lý điều kiện cần và đủ',
       '<p>Giả sử bài toán (P) <b>lồi</b>, Slater thỏa mãn, \\(x^*\\) khả thi. Khi đó:</p>'
       + formula('Cần và đủ', r'x^*\ \text{tối ưu}\iff\exists\lambda\ge0,\mu:\ \nabla f(x^*)+\sum_i\lambda_i\nabla g_i(x^*)+\sum_j\mu_j\nabla h_j(x^*)=0,\ \lambda_ig_i(x^*)=0')
       + '<p>Tức là điểm KKT của bài toán lồi thỏa Slater <b>chính là</b> nghiệm tối ưu toàn cục.</p>',
       kicker=M + ' · PHẦN 4', img='m2:52',
       explain='<p>Chiều “⇐” (đủ) là chiều quan trọng khi giải bài: tìm ra một điểm KKT là đã tìm ra nghiệm tối ưu. Chiều “⇒” (cần) cho phép ta chắc chắn khi có nghiệm thì nó nằm trong tập điểm KKT nên liệt kê hết các điểm KKT sẽ không bỏ sót.</p>'))
add(sl('Quy trình giải bằng KKT',
       '<figure class="slide-fig"><img src="../../assets/diagrams/d3-quy-trinh-kkt.svg" alt="Quy trình KKT" style="max-height:20em;background:#fff"/></figure><p>Bài không lồi: KKT chỉ cho <b>ứng viên</b>; phải so sánh giá trị f hoặc xét điều kiện bậc hai.</p>',
       kicker=M + ' · TỔNG KẾT',
       explain='<p>Sơ đồ tóm tắt 7 bước. Bước 5 (chia trường hợp theo ràng buộc chặt) là bước tốn công nhất; bước 7 (thay lại kiểm tra) giúp tránh sai sót số học.</p>'))

# ---------------- PHẦN 5
add(part(5, 5, 'Bốn ví dụ và câu hỏi thảo luận', ['Ví dụ 1: bài toán lồi có ràng buộc đẳng thức', 'Ví dụ 2: max hàm lồi (bài không lồi)', 'Ví dụ 3: \\(\\min xy\\) trên đĩa', 'Ví dụ 4: LP'], M))
add(sl('Ví dụ 1: bài toán lồi, nhân tử (0, 1)',
       '<p>Cực tiểu \\(f(x,y)=(x-1)^2+y-2\\) với \\(x+y-2\\le0\\), \\(x-y+1=0\\).</p>'
       '<ul><li>Bài toán tối ưu là lồi (f lồi, \\(g\\) affine, \\(h\\) affine).</li><li>Điều kiện Slater thỏa (điểm \\((0,1)\\): \\(g=-1<0\\), \\(h=0\\)).</li><li>Điểm dừng \\((x^*,y^*)=(1/2,3/2)\\) là nghiệm ứng với \\((\\lambda,\\mu)=(0,1)\\).</li></ul>',
       kicker=M + ' · PHẦN 5', img='m2:55',
       explain='<p>Ràng buộc \\(g_1=x+y-2\\le0\\) <i>chặt</i> tại nghiệm nhưng \\(\\lambda=0\\) (suy biến bù). Chỉ ràng buộc đẳng thức thật sự “đỡ” nghiệm: \\(\\nabla f=(-1,1)\\) song song với \\(\\nabla h=(1,-1)\\).</p>'))
add(sl('Chú ý: bài không lồi',
       '<p>Với bài toán tối ưu <b>không lồi</b>, điểm KKT có thể không là điểm cực tiểu địa phương.</p><p>Điều kiện đủ của KKT (Module 3 và 2) đòi hỏi tính lồi; nếu không lồi, KKT chỉ là điều kiện cần (khi có CQ).</p>',
       kicker=M + ' · PHẦN 5', img='m2:56',
       explain='<p>Ví dụ 3 (min xy trên đĩa) cho thấy điều này: điểm \\((0,0)\\) là điểm KKT nhưng là điểm yên ngựa, không phải cực tiểu.</p>'))
add(sl('Ví dụ 2: max hàm lồi trên tập ràng buộc',
       '<p>Bài toán: \\(\\max\\ f=x^2+y^2+4x-6y\\) với \\(x+y\\le3\\), \\(-2x+y\\le2\\); chuyển sang cực tiểu \\(-f\\) (không lồi). Slide nêu điểm KKT \\((1/3,8/3)\\).</p>'
       + callout('warn', 'Kiểm chứng bằng code', '<p>Tại \\((1/3,8/3)\\), hai ràng buộc cùng chặt và giải \\(\\nabla(-f)+\\lambda_1\\nabla g_1+\\lambda_2\\nabla g_2=0\\) cho \\(\\lambda=(10/9,\\,-16/9)\\): có nhân tử <b>âm</b> nên <b>không</b> phải điểm KKT. Xem trang “Kiểm chứng” và ví dụ chi tiết bên dưới.</p>'),
       kicker=M + ' · PHẦN 5', img='m2:59',
       explain='<p>Đây là chỗ nên hỏi lại giảng viên: có thể đề đúng là cực tiểu \\(f\\) (khi đó điểm KKT là \\((0,2)\\), \\(\\lambda=(0,2)\\)), hoặc ràng buộc khác. Phương pháp giải (liệt kê các trường hợp chặt và kiểm dấu nhân tử) thì luôn đúng.</p>'))
add(sl('Ví dụ 3: \\(\\min xy\\) trên đĩa \\(x^2+y^2\\le2\\)',
       '<p>Ba điểm KKT hợp lệ: \\((0,0)\\) với \\(\\lambda=0\\); \\((1,-1)\\) và \\((-1,1)\\) với \\(\\lambda=\\tfrac12\\).</p><p>Loại: \\((1,1)\\) và \\((-1,-1)\\) vì \\(\\lambda=-\\tfrac12<0\\).</p>'
       '<ul><li>\\(f(0,0)=0\\); \\(f(1,-1)=f(-1,1)=-1\\) ⇒ hai điểm sau là cực tiểu toàn cục (miền compact nên tồn tại nghiệm).</li><li>\\((0,0)\\) là <b>điểm yên ngựa</b>: dọc \\((t,-t)\\), \\(f=-t^2<0\\).</li></ul>',
       kicker=M + ' · PHẦN 5', img='m2:60',
       explain='<p>Hàm \\(xy\\) không lồi (Hessian \\(\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\) không xác định), nên KKT chỉ cho ứng viên. Miền là hình tròn đóng (bị chặn), nên nghiệm tồn tại (định lý Weierstrass) và ta chọn ứng viên có f nhỏ nhất.</p>'))
add(sl('Ví dụ 4: quy hoạch tuyến tính',
       '<p>\\(\\min f=2x+y\\) với \\(3x+y\\le6\\), \\(x+y\\le4\\), \\(x\\ge0\\), \\(y\\ge0\\).</p><p>Đây là LP (bài toán lồi, Slater thỏa: \\((0.5,0.5)\\) làm cả 4 bất đẳng thức chặt). Nghiệm \\((0,0)\\); KKT: \\(\\nabla f=(2,1)\\), \\(\\lambda_3=2\\), \\(\\lambda_4=1\\) (ràng buộc \\(-x\\le0\\), \\(-y\\le0\\)).</p>'
       '<p>Nếu đề là <b>max</b> \\(2x+y\\): tối ưu tại \\((1,3)\\) với giá trị 5.</p>',
       kicker=M + ' · PHẦN 5', img='m2:61',
       explain='<p>KKT của LP chính là điều kiện tối ưu của thuật toán đơn hình dưới dạng đối ngẫu: \\(\\lambda\\) là biến đối ngẫu (giá bóng). Đây là chỗ nối trực tiếp với môn Quy hoạch tuyến tính.</p>'))
add(sl('Câu hỏi và thảo luận (slide tr.66) — trả lời gợi ý',
       '<ol><li><b>Miền lồi không thỏa Slater:</b> \\(\\{x\\mid x^2\\le0\\}=\\{0\\}\\).</li><li><b>Cặp nhân tử \\((\\lambda,\\mu)\\) có duy nhất?</b> Không nhất thiết (ví dụ ràng buộc trùng lặp hoặc gradient phụ thuộc tuyến tính); duy nhất khi các \\(\\nabla g_i,\\nabla h_j\\) của ràng buộc chặt độc lập tuyến tính (LICQ).</li>'
       '<li><b>Khi nào có duy nhất nghiệm?</b> Ví dụ f lồi chặt.</li><li><b>Có thể có hai nghiệm?</b> Không đúng hai: nếu \\(x_1\\ne x_2\\) đều tối ưu thì cả đoạn nối cũng tối ưu (vô số).</li><li><b>Tập nghiệm:</b> là tập lồi (và đóng).</li></ol>',
       kicker=M + ' · PHẦN 5', img='m2:66',
       explain='<p>Năm câu này ôn lại các hệ quả của tính lồi. Chứng minh câu 4: nếu \\(f(x_1)=f(x_2)=f^*\\) thì \\(f((x_1+x_2)/2)\\le f^*\\) và cũng \\(\\ge f^*\\) vì \\(f^*\\) là cực tiểu ⇒ điểm giữa cũng tối ưu; tương tự mọi điểm trên đoạn.</p>'))

# =====================================================================  SECTIONS
SECTIONS = []
SECTIONS.append(('cong-thuc', 'Công thức cốt lõi',
    formula('Bài toán (P)', r'\min f(x)\ \ \text{s.t.}\ g_i(x)\le0\ (i\in I),\ h_j(x)=0\ (j\in J)')
    + formula('Hàm Lagrange', r'L(x,\lambda,\mu)=f(x)+\sum_i\lambda_ig_i(x)+\sum_j\mu_jh_j(x)')
    + formula('Hệ KKT', r'\nabla f(x^*)+\sum_i\lambda_i\nabla g_i(x^*)+\sum_j\mu_j\nabla h_j(x^*)=0;\ \ \lambda_ig_i(x^*)=0;\ \ g_i\le0,\ h_j=0;\ \ \lambda_i\ge0',
              [('\\lambda_ig_i=0', 'điều kiện bù'), ('\\lambda_i\\ge0', 'khả thi đối ngẫu'), ('\\mu_j', 'nhân tử của ràng buộc đẳng thức (dấu tùy ý)')])
    + formula('Slater', r'\exists z:\ g_i(z)<0\ (\forall i),\ h_j(z)=0\ (\forall j)')
    + table(['Tình huống', 'Vai trò của KKT'],
            [['Bài lồi + Slater', 'điều kiện <b>cần và đủ</b>'], ['Bài lồi, không Slater', 'có thể không cần (phản ví dụ \\(x^2\\le0\\))'], ['Bài không lồi + CQ', 'điều kiện <b>cần</b>: chỉ cho ứng viên'], ['Bài không lồi, không CQ', 'không bảo đảm gì']])))

SECTIONS.append(('lich-su', 'Bối cảnh lý thuyết và lịch sử', callout('hist', '📜 Bối cảnh lý thuyết & lịch sử',
    '<p>Phương pháp nhân tử cho ràng buộc đẳng thức thuộc về <b>Joseph-Louis Lagrange</b> (khuôn khổ cơ học giải tích, <i>Mécanique analytique</i>, 1788). Mở rộng cho ràng buộc bất đẳng thức là điều kiện <b>Karush–Kuhn–Tucker</b>: William Karush trình bày trong luận văn thạc sĩ năm 1939; Harold Kuhn và Albert Tucker công bố độc lập năm 1951 và làm cho kết quả nổi tiếng trong quy hoạch phi tuyến.</p>'
    '<p>Điều kiện chính quy <b>Slater</b> mang tên Morton Slater (1950). Trong lý thuyết đối ngẫu lồi, Slater bảo đảm không có khoảng cách đối ngẫu, nên hệ KKT là cần và đủ (Boyd &amp; Vandenberghe, mục 5.5).</p>')))

# --- case study danh mục đầu tư
S_case = ('<p>Bài toán <b>danh mục đầu tư phương sai nhỏ nhất, không bán khống</b> (Markowitz đơn giản hóa): chọn tỉ trọng \\(w\\in\\mathbb R^3\\) của ba tài sản để cực tiểu rủi ro (phương sai) \\(f(w)=w^\\top\\Sigma w\\) với \\(\\mathbf 1^\\top w=1\\), \\(w\\ge0\\).</p>'
          '<p>Độ lệch chuẩn \\(\\sigma=(10\\%,15\\%,20\\%)\\), tương quan \\(\\rho_{12}=0.8,\\ \\rho_{13}=0.2,\\ \\rho_{23}=0.9\\). Ma trận hiệp phương sai \\(\\Sigma=\\mathrm{diag}(\\sigma)\\,\\mathrm{corr}\\,\\mathrm{diag}(\\sigma)\\):</p>'
          '<p style="text-align:center">\\[\\Sigma=\\begin{pmatrix}' + f4(Sg[0, 0]) + '&' + f4(Sg[0, 1]) + '&' + f4(Sg[0, 2]) + r'\\' + f4(Sg[1, 0]) + '&' + f4(Sg[1, 1]) + '&' + f4(Sg[1, 2]) + r'\\' + f4(Sg[2, 0]) + '&' + f4(Sg[2, 1]) + '&' + f4(Sg[2, 2]) + r'\end{pmatrix}\]</p>'
          + steps([
              'f là hàm toàn phương với Hessian \\(2\\Sigma\\succ0\\) ⇒ <b>lồi chặt</b>; ràng buộc \\(\\mathbf1^\\top w=1\\) affine, \\(-w_i\\le0\\) affine ⇒ bài toán lồi; Slater thỏa (ví dụ \\(w=(\\tfrac13,\\tfrac13,\\tfrac13)\\) làm mọi \\(-w_i<0\\)).',
              'Lagrange: \\(L=w^\\top\\Sigma w+\\mu(\\mathbf1^\\top w-1)-\\sum_i\\lambda_iw_i\\). Dừng: \\(2\\Sigma w+\\mu\\mathbf1-\\lambda=0\\); bù \\(\\lambda_iw_i=0\\); \\(\\lambda\\ge0\\).',
              'Nếu bỏ ràng buộc \\(w\\ge0\\) (chỉ giữ tổng bằng 1): \\(w\\propto\\Sigma^{-1}\\mathbf1\\) cho \\(w=(' + ', '.join(f4(v) for v in w_un) + ')\\) — có tỉ trọng <b>âm</b> nên vi phạm \\(w\\ge0\\).',
              'Thử tập chặt \\(\\{w_2=0\\}\\): giải trên tài sản 1, 3: \\(w_{1,3}\\propto\\Sigma_{\\{1,3\\}}^{-1}\\mathbf1\\) ⇒ \\(w^*=(' + ', '.join(f4(v) for v in w_star) + ')\\) (tức \\(6/7,\\ 0,\\ 1/7\\)), rủi ro \\(w^{*\\top}\\Sigma w^*=' + f6(var_star) + '\\) (độ lệch chuẩn \\(' + f4(100 * np.sqrt(var_star)) + '\\%\\)).',
              'Nhân tử: \\(\\mu=2w^{*\\top}\\Sigma w^*=' + f6(mu_sum) + '\\) và \\(\\lambda_2=2(\\Sigma w^*)_2-\\mu=' + f6(lam2) + '\\ge0\\) ✓. Các nhân tử \\(\\lambda_1=\\lambda_3=0\\) vì \\(w_1,w_3>0\\). Mọi điều kiện KKT thỏa ⇒ do bài lồi + Slater, \\(w^*\\) là <b>nghiệm tối ưu toàn cục</b>.'])
          + callout('good', 'Điều học được', '<p>Tài sản 2 (rủi ro trung bình, tương quan cao với tài sản 3) bị loại khỏi danh mục: nhân tử \\(\\lambda_2>0\\) đo “giá” của việc bị ép bằng 0 (rủi ro sẽ giảm thêm một chút nếu được phép bán khống).</p>'))
SECTIONS.append(('case-study', '🔎 Case study: danh mục đầu tư phương sai nhỏ nhất', S_case))

# --- ví dụ chi tiết
def ex(t, b): return solution(t, b)
EXS = ''
EXS += ex('Ví dụ 1 (slide tr.55) — giải đầy đủ',
    steps(['Đặt \\(g(x,y)=x+y-2\\le0\\), \\(h(x,y)=x-y+1=0\\). \\(f\\) lồi (tổng của bình phương lồi và hàm tuyến tính), \\(g,h\\) affine ⇒ bài toán lồi.',
           'Slater: \\((0,1)\\) có \\(h=0\\), \\(g=-1<0\\) ✓ ⇒ KKT là cần và đủ.',
           'Lagrange \\(L=(x-1)^2+y-2+\\lambda(x+y-2)+\\mu(x-y+1)\\). Dừng: \\(2(x-1)+\\lambda+\\mu=0\\); \\(1+\\lambda-\\mu=0\\).',
           'Trường hợp \\(g\\) không chặt (\\(\\lambda=0\\)): \\(\\mu=1\\), \\(x=1/2\\); từ \\(h=0\\): \\(y=3/2\\). Kiểm \\(g=1/2+3/2-2=0\\) — thực ra <b>chặt</b>, nhưng \\(\\lambda=0\\) vẫn thỏa bù. Khả thi ✓, \\(\\lambda=0\\ge0\\) ✓.',
           'Kết luận (sympy + SLSQP): \\((x^*,y^*)=(1/2,3/2)\\), \\((\\lambda,\\mu)=(0,1)\\), \\(f^*=-0.25\\).']))
EXS += ex('Ví dụ 3 (slide tr.60) — \\(\\min xy\\) trên đĩa: chia trường hợp',
    steps(['\\(g=x^2+y^2-2\\le0\\); \\(L=xy+\\lambda(x^2+y^2-2)\\). Dừng: \\(y+2\\lambda x=0\\), \\(x+2\\lambda y=0\\); bù \\(\\lambda g=0\\).',
           '<b>Trường hợp \\(\\lambda=0\\):</b> \\(y=0\\), \\(x=0\\) ⇒ \\((0,0)\\), \\(g=-2<0\\) khả thi ✓ KKT, \\(f=0\\).',
           '<b>Trường hợp \\(g=0\\), \\(\\lambda>0\\) hoặc bất kỳ:</b> từ hai phương trình dừng suy \\(x^2=y^2\\) nên \\(y=\\pm x\\); với \\(x^2+y^2=2\\) ⇒ \\(x=\\pm1\\).',
           '\\(y=x\\): \\(y+2\\lambda x=0\\Rightarrow\\lambda=-\\tfrac12<0\\) ⇒ <b>loại</b> \\((1,1),(-1,-1)\\). \\(y=-x\\): \\(\\lambda=\\tfrac12>0\\) ✓ ⇒ \\((1,-1),(-1,1)\\), \\(f=-1\\).',
           'Hessian của L tại \\(\\lambda=1/2\\): \\(\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}\\succeq0\\); tại \\(\\lambda=0\\): \\(\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\) không xác định ⇒ \\((0,0)\\) là yên ngựa.',
           'Miền compact ⇒ nghiệm tồn tại; so sánh giá trị: \\(f=-1<0\\). Kết luận: cực tiểu toàn cục tại \\((1,-1)\\) và \\((-1,1)\\), \\(f^*=-1\\).']))
EXS += ex('Ví dụ 4 (slide tr.61) — LP',
    steps(['\\(f=2x+y\\), ràng buộc \\(g_1=3x+y-6\\le0\\), \\(g_2=x+y-4\\le0\\), \\(g_3=-x\\le0\\), \\(g_4=-y\\le0\\).',
           'Tại \\((0,0)\\): chặt \\(g_3,g_4\\). Dừng \\((2,1)+\\lambda_3(-1,0)+\\lambda_4(0,-1)=0\\) ⇒ \\(\\lambda_3=2\\), \\(\\lambda_4=1\\ge0\\) ✓, \\(\\lambda_1=\\lambda_2=0\\).',
           'LP lồi, Slater ✓ ⇒ \\((0,0)\\) là nghiệm; \\(f^*=0\\). Kiểm bằng <code>linprog</code>.',
           f'Biến thể max: nghiệm \\((1,3)\\), giá trị {R["m2_ex4_max"][1]:.0f} (giao của \\(3x+y=6\\) và \\(x+y=4\\)).']))
ex2 = R['m2_ex2_all_active_sets']
EXS += ex('Ví dụ 2 (slide tr.57/59) — kiểm chứng: không có điểm KKT nào',
    '<p>Bài toán \\(\\min F=-(x^2+y^2+4x-6y)\\) với \\(g_1=x+y-3\\le0\\), \\(g_2=-2x+y-2\\le0\\). Liệt kê 4 tập chặt:</p>'
    + table(['Tập chặt', 'Nghiệm', 'Khả thi', 'λ ≥ 0'], [[str(e['active']), ', '.join(f'{k}={v}' for k, v in e['sol'].items()), 'có' if e['feasible'] else 'không', 'có' if e['KKT(lam>=0)'] else 'không'] for e in ex2])
    + '<p>Không tập nào cho điểm KKT (điểm \\((1/3,8/3)\\) có \\(\\lambda_2=-16/9<0\\)). Điều này khớp với việc \\(\\max f\\) <b>không bị chặn</b> trên miền (miền không bị chặn, f→∞). Nếu bài là cực tiểu \\(f\\) (lồi) thì điểm KKT là \\((0,2)\\), \\(\\lambda=(0,2)\\), \\(f^*=-8\\).</p>')
EXS += ex('Phản ví dụ — KKT không là điều kiện cần khi thiếu Slater',
    '<p>\\(\\min x\\) s.t. \\(x^2\\le0\\). Miền khả thi \\(\\{0\\}\\) nên \\(x^*=0\\) là nghiệm. Dừng: \\(1+2\\lambda x^*=1+0=1\\ne0\\) với mọi \\(\\lambda\\) ⇒ không có nhân tử. Slater vi phạm (không có z với \\(z^2<0\\)); \\(\\nabla g(x^*)=0\\) cũng vi phạm LICQ.</p>')
EXS += ex('Bài tập tham khảo C9 — Slater rồi KKT',
    steps(['\\(f=3x_1^2+3x_2^2-4x_1x_2\\), Hessian \\(\\begin{pmatrix}6&-4\\\\-4&6\\end{pmatrix}\\succ0\\) ⇒ lồi chặt. \\(g_1=-x_1-x_2+2\\) affine, \\(g_2=x_1^2+x_2^2-4\\) lồi ⇒ bài toán lồi.',
           'Slater: \\((1.2,1.2)\\): \\(g_1=-0.4<0\\), \\(g_2=-1.12<0\\) ✓.',
           'Thử \\(g_1\\) chặt, \\(g_2\\) lỏng: \\(x_1+x_2=2\\) và \\(6x_1-4x_2-\\lambda=0\\), \\(6x_2-4x_1-\\lambda=0\\) ⇒ \\(x_1=x_2=1\\), \\(\\lambda_1=2\\ge0\\). \\(g_2(1,1)=-2<0\\) ✓ lỏng.',
           'Kết luận: \\(x^*=(1,1)\\), \\(f^*=2\\) (khớp SLSQP). Đề tham khảo cũ, nhưng lời giải đã kiểm bằng code.']))
EXS += ex('Bài tập tham khảo C10 — Slater rồi KKT',
    steps(['\\(f=4x_1^2+x_2^2-x_1-2x_2\\) (Hessian \\(\\mathrm{diag}(8,2)\\succ0\\)); \\(g_1=2x_1+x_2-1\\), \\(g_2=x_1^2-1\\) lồi ⇒ bài toán lồi.',
           'Slater: \\((0,0)\\): \\(g_1=-1<0\\), \\(g_2=-1<0\\) ✓.',
           'Cực tiểu không ràng buộc \\((1/8,1)\\) có \\(2x_1+x_2=1.25>1\\) vi phạm \\(g_1\\) ⇒ \\(g_1\\) chặt.',
           'Dừng với \\(g_1\\) chặt: \\(8x_1-1+2\\lambda=0\\), \\(2x_2-2+\\lambda=0\\), \\(2x_1+x_2=1\\) ⇒ \\(x^*=(1/16,\\ 7/8)\\), \\(\\lambda=1/4\\ge0\\); \\(g_2=1/256-1<0\\) lỏng ✓.',
           'Kết luận: \\(x^*=(1/16,7/8)\\), \\(f^*=-33/32=-1.03125\\).']))
SECTIONS.append(('vi-du', 'Ví dụ chi tiết (có lời giải từng bước)', '<p>Bấm từng ví dụ để mở lời giải. Mọi số liệu được kiểm bằng sympy/scipy.</p>' + EXS))
SECTIONS.append(('so-do', 'Sơ đồ tổng hợp', fig('d3-quy-trinh-kkt', 'Quy trình giải bài toán có ràng buộc bằng KKT (drawio)') + fig('d1-phan-loai-toi-uu', 'Các lớp bài toán tối ưu')))
SECTIONS.append(('tuong-tac', 'Thực hành tương tác', widget('kkt-lab') + widget('grad-lab')))
SECTIONS.append(('bay', 'Cảnh báo bẫy diễn giải sai',
    callout('warn', 'Bẫy 1 — Dấu của nhân tử', '<p>Với dạng \\(g_i\\le0\\) và \\(L=f+\\sum\\lambda_ig_i\\), yêu cầu là \\(\\lambda_i\\ge0\\). Nếu viết ràng buộc dạng \\(g\\ge0\\) hoặc dùng \\(L=f-\\sum\\lambda g\\) thì dấu thay đổi; luôn chuẩn hóa về \\(g\\le0\\) trước.</p>')
    + callout('warn', 'Bẫy 2 — KKT không lồi chưa phải nghiệm', '<p>\\(\\min xy\\) trên đĩa có điểm KKT \\((0,0)\\) là yên ngựa. Bài không lồi: so sánh các ứng viên và kiểm tồn tại nghiệm.</p>')
    + callout('warn', 'Bẫy 3 — Ràng buộc chặt mà \\(\\lambda=0\\)', '<p>Ví dụ 1: \\(g\\) chặt nhưng \\(\\lambda=0\\). Điều kiện bù cho phép điều này (suy biến bù), không mâu thuẫn.</p>')
    + callout('warn', 'Bẫy 4 — Quên kiểm khả thi và dấu', '<p>Sau khi giải hệ dừng + bù, phải kiểm tra <b>khả thi gốc</b> (\\(g\\le0\\)) và \\(\\lambda\\ge0\\); nhiều nghiệm của hệ phương trình bị loại ở bước này (ví dụ \\((1,1)\\) trong ví dụ 3).</p>')
    + callout('warn', 'Bẫy 5 — Slater ≠ “miền có điểm trong” nói chung', '<p>Slater cần điểm khả thi làm mọi bất đẳng thức chặt và thỏa đẳng thức affine; miền chỉ gồm biên (\\(x^2\\le0\\)) không thỏa.</p>')))
READING = ('<ul><li>Boyd &amp; Vandenberghe: Ch.4 “Convex optimization problems” (tr.127) và Ch.5 “Duality” (tr.215), đặc biệt 5.5 “Optimality conditions” (tr.241) — file <code>bv_cvxbook.pdf</code>.</li>'
           '<li>Tham khảo: Nocedal &amp; Wright, <i>Numerical Optimization</i>, chương 12 (điều kiện tối ưu cho bài có ràng buộc, LICQ/MFCQ).</li>'
           '<li>Tiếp theo: Module 3 áp dụng KKT cho quy hoạch toàn phương (null space và active set).</li></ul>')
