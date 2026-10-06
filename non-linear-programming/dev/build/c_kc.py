"""Trang kiểm chứng và ghi chú về slide."""
from helpers import *

def body(R):
    b = '<p class="tag">KIỂM CHỨNG</p><h1>Kiểm chứng số liệu và ghi chú về slide</h1>'
    b += '<p class="lead">Mọi ví dụ trong slide được tính lại bằng code (numpy, scipy, sympy). Các chỗ khớp thì dùng nguyên; các chỗ chưa khớp được ghi rõ dưới đây. Đây là ghi chú để <b>hỏi lại giảng viên</b>, không phải kết luận chê bai: có thể là lỗi chép khi chuyển slide.</p>'
    b += callout('info', 'Cách kiểm chứng', '<p>Script: <code>NLP-work/verify/verify_all.py</code> (trong thư mục dự án). Kết quả dạng số lưu ở <code>results.json</code>. Các tài liệu Studocu chỉ tham khảo, không dùng để suy ra cấu trúc đề.</p>')
    ex2 = R['m2_ex2_all_active_sets']
    b += '<h2>1. Slide 2, Ví dụ 2 (tr.57/59): điểm KKT \\((1/3,8/3)\\) không khớp</h2>'
    b += ('<p>Bài toán: \\(\\max f=x^2+y^2+4x-6y\\) với \\(x+y\\le3,\\ -2x+y\\le2\\); đổi thành \\(\\min(-f)\\). Slide nêu điểm KKT \\((1/3,8/3)\\) (giao của hai ràng buộc).</p>'
          + table(['Tập ràng buộc chặt', 'Nghiệm hệ KKT', 'Khả thi?', 'Nhân tử \\(\\ge0\\)?'],
                  [[str(e['active']), ', '.join(f'{k}={v}' for k, v in e['sol'].items()), 'có' if e['feasible'] else 'không', 'có' if e['KKT(lam>=0)'] else 'không'] for e in ex2])
          + '<p>Tại \\((1/3,8/3)\\): \\((\\lambda_1,\\lambda_2)=(10/9,\\,-16/9)\\) có một nhân tử <b>âm</b> nên nó <b>không</b> phải điểm KKT của \\(\\min(-f)\\). Ngoài ra \\(\\max f\\) không bị chặn trên (chẳng hạn điểm \\((-100,-198)\\) khả thi cho \\(f=49992\\)). '
            'Nếu đề thực ra là <b>cực tiểu</b> \\(f\\) thì điểm KKT là \\((0,2)\\) với \\(\\lambda=(0,2)\\), giá trị \\(-8\\) (đã kiểm bằng SLSQP).</p>')
    b += '<h2>2. Slide 3, ví dụ null-space (tr.56–58): hai quy ước mâu thuẫn</h2>'
    e = R['errata_null_space']
    b += (f'<p>Hàm ghi trên slide: \\(2x_1^2-4x_1x_2-2x_1x_3+2x_2^2+2x_2x_3+5x_3^2+10x_1-26x_2-2x_3\\) có Hessian \\(=2Q_{{slide}}\\) (không bằng \\(Q\\) ghi trên slide). '
          f'Lời giải trên slide (\\(x^*=(3.0588,0.9412,6.9412)\\), \\(\\mu=(23.2941,-30.5882)\\)) là nghiệm của \\(\\min\\tfrac12x^\\top Qx+c^\\top x\\) với \\(Q,c\\) như slide; giá trị đúng của hàm đó là <b>{e["half_form_at_slide_x"]}</b>. '
          f'Số <b>{e["poly_at_slide_x"]}</b> ghi trên slide là giá trị của <i>đa thức</i> tại điểm đó, không phải giá trị cực tiểu. '
          f'Nếu cực tiểu đa thức như đã viết thì nghiệm là \\(x^*=({e["true_opt_of_polynomial"]["x"][0]},{e["true_opt_of_polynomial"]["x"][1]},{e["true_opt_of_polynomial"]["x"][2]})\\), giá trị \\({e["true_opt_of_polynomial"]["f"]}\\).</p>')
    b += '<h2>3. Slide 3, Bài tập 1 (tr.59): ràng buộc và đáp số không khớp</h2>'
    b += ('<p>Đề: ràng buộc \\(x_1+x_3=0,\\ x_2+x_3=0\\), đáp số \\((2,-1,1)^\\top\\). Nhưng \\((2,-1,1)\\) không thỏa \\(x_1+x_3=0\\) (bằng 3). Nghiệm đúng của bài với \\(b=(0,0)\\) là \\((0.6154,0.6154,-0.6154)\\). '
          'Đáp số \\((2,-1,1)\\) khớp chính xác khi ràng buộc thứ nhất là \\(x_1+x_3=3\\) (tức \\(b=(3,0)\\), \\(\\mu=(-3,2)\\), \\(f=-3.5\\)). Có thể slide chép thiếu số 3.</p>')
    b += '<h2>4. Slide 3, ví dụ active set (tr.55): vectơ c</h2>'
    b += '<p>Slide ghi \\(c=[-2,1]^\\top\\) ở tr.55 nhưng các bước sau dùng \\(g=Qx+c=(-2,-1)\\), tức \\(c=[-2,-1]^\\top\\) (đúng với \\((x_1-1)^2+(x_2-0.5)^2\\)). Kết quả cuối \\(x^*=(0.4,0.3)\\), \\(f=0.4\\) khớp scipy.</p>'
    b += '<h2>5. Slide 3, bài tập active set (tr.81)</h2>'
    log = R['m3_active_bt']
    b += f'<p>Đáp số gợi ý \\((3.25,1.75)\\) khớp. Gợi ý “4 bước lặp” phụ thuộc cách đếm: với \\(W_0=I(x_0)=\\{{4,5\\}}\\), mô phỏng của chúng tôi cần {log["iters"]} vòng (3 lần di chuyển, 3 lần loại ràng buộc, 1 lần dừng); có thể slide chỉ đếm các bước di chuyển hoặc chọn \\(W_0\\) khác.</p>'
    b += '<h2>6. Slide 3, Hệ quả 4 (tr.30)</h2>'
    b += '<p>Hệ quả 2 và Hệ quả 4 đều ghi “nửa xác định âm”. Hệ quả 4 (“có nghiệm khi và chỉ khi \\(\\Delta\\) khác rỗng và compact”) cần <b>xác định âm</b>: với \\(Q=0\\) (vừa nửa xác định dương vừa âm) bài toán LP \\(\\min x\\) s.t. \\(x\\ge0\\) có nghiệm trong khi \\(\\Delta\\) không compact.</p>'
    b += '<h2>7. Slide 2, Ví dụ 4 (tr.61)</h2>'
    b += f'<p>Slide ghi \\(\\min 2x+y\\). Với miền \\(3x+y\\le6,\\ x+y\\le4,\\ x,y\\ge0\\): cực tiểu tại \\((0,0)\\), giá trị 0 (bài trivial: \\(\\lambda_3=2,\\lambda_4=1\\)); nếu là <b>cực đại</b> thì tối ưu tại \\((1,3)\\) với giá trị {R["m2_ex4_max"][1]:.0f}. Có thể slide muốn dùng max; cả hai đã kiểm bằng code.</p>'
    b += '<h2>8. Slide 1, ellipsoid (tr.18)</h2><p>Slide viết \\(P\\) đối xứng nửa xác định dương; để tập bị chặn (ellipsoid thật sự) cần \\(P\\) xác định dương, như Boyd.</p>'
    b += '<h2>10. Slide 3, công thức (4.7) và nhân tử ở k=0 (tr.55, tr.71)</h2>'
    b += '<p>(a) Slide (4.7) viết \\((AY)^\\top\\mu^*=-Y^\\top\\bar g+Gd\\); suy dẫn từ \\(Qd+\\bar g+A^\\top\\mu=0\\) cho \\((AY)^\\top\\mu=-Y^\\top(\\bar g+Qd)\\). Các số ví dụ của slide (\\(\\mu=(23.2941,-30.5882)\\)) khớp công thức đúng.</p>'
    b += '<p>(b) Ở vòng k=0 của ví dụ active set, từ \\((-2,-1)+\\hat\\mu_3(-1,0)+\\hat\\mu_4(0,-1)=0\\) ta được \\(\\hat\\mu_3=-2\\) và \\(\\hat\\mu_4=-1\\); slide ghi \\(\\hat\\mu_4=1\\). Quyết định loại ràng buộc 3 (âm nhất) không đổi.</p>'
    b += '<h2>9. Tài liệu tham khảo ngoài lề</h2>'
    b += table(['Tài liệu', 'Độ tin cậy', 'Cách dùng'],
               [['3 slide ORLab (thư mục Slides)', 'Nguồn chính', 'Nội dung bài giảng, câu hỏi gốc'],
                ['Đề cương CSE703057', 'Chính thức', 'Lộ trình 9 buổi, giáo trình Boyd'],
                ['bv_cvxbook.pdf (Boyd &amp; Vandenberghe)', 'Giáo trình chính', 'Đọc thêm, số chương/trang'],
                ['Studocu: đề giữa kỳ (AI sinh), bài tập giữa kỳ, Chương 1 BTDOC', 'Rất cũ, khác ngành — chỉ tham khảo', 'Một số bài luyện, gắn nhãn “tham khảo”; không suy ra cấu trúc đề thi'],
                ['Bài “nông trại thức ăn” (Studocu C11)', 'Kiểm tra cho thấy đề <b>vô nghiệm</b>', 'Dùng làm ví dụ “kiểm tra khả thi trước khi giải” (Module 0)']])
    return b
