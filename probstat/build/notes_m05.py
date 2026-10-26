"""Module 5 — phần “Nội dung chi tiết” cuối trang (công thức dựng bằng KaTeX)."""
from hx import *
def notes():
    n = '<h2>1. Đọc kèm giáo trình</h2><p>Lecture Notes §1.7 (khái niệm BNN, Định nghĩa 1.7), §1.8 (bảng phân phối, hàm phân phối, hàm mật độ), §1.9 (kỳ vọng, phương sai, độ lệch chuẩn). Kreyszig §24.5 (hàm xác suất, mật độ và F; Problem Set 24.5 gồm 15 bài) và §24.6 (kỳ vọng, phương sai, mô-men; Problem Set 24.6 gồm 20 bài). Bài 1.24–1.31 của giáo trình và các câu 1, 5 của đề cuối kỳ được dùng làm câu gốc.</p>'
    n += '<h2>2. Công thức cần nhớ</h2>' + table(['Đại lượng', 'Rời rạc', 'Liên tục'], [
        ['Điều kiện hợp lệ', m('p_i\\ge0,\\ \\sum p_i=1'), m('f\\ge0,\\ \\int f=1')],
        ['Hàm phân phối', m('F(x)=\\sum_{x_i\\le x}p_i'), m('F(x)=\\int_{-\\infty}^xf(t)dt')],
        ['Xác suất khoảng', m('P(a<X\\le b)=F(b)-F(a)'), m('P(a<X\\le b)=\\int_a^bf')],
        ['Kỳ vọng', m('\\sum x_ip_i'), m('\\int xf(x)dx')],
        ['Phương sai', m('E(X^2)-[E(X)]^2'), m('E(X^2)-[E(X)]^2')],
        ['Hàm của X', m('E(g(X))=\\sum g(x_i)p_i'), m('E(g(X))=\\int g\\,f')]])
    n += table(['Quy tắc', 'Công thức', 'Điều kiện'], [
        ['Biến đổi tuyến tính', m('E(aX+b)=aE(X)+b,\\ \\mathrm{Var}(aX+b)=a^2\\mathrm{Var}(X)'), 'luôn đúng'],
        ['Tổng', m('E(X+Y)=E(X)+E(Y)'), 'luôn đúng'],
        ['Phương sai của tổng', m('\\mathrm{Var}(X+Y)=\\mathrm{Var}X+\\mathrm{Var}Y+2\\mathrm{Cov}(X,Y)'), 'Cov = 0 khi độc lập'],
        ['Chebyshev', m('P(|X-\\mu|\\ge k\\sigma)\\le1/k^2'), 'chỉ cần biết μ, σ']])
    n += '<h2>3. Năm dạng bài thường gặp và cách làm</h2>' + ul([
        '<b>Tìm hằng số k hoặc tham số</b>: dùng Σp = 1 (hoặc ∫f = 1) và điều kiện cho thêm như E(X) cho trước.',
        '<b>Tính F(x) và xác suất khoảng</b>: rời rạc cộng dồn (bậc thang), liên tục tích phân; với mật độ phân đoạn, cộng dồn các đoạn trước.',
        '<b>Tính E, Var, σ</b>: tính E(X) và E(X²) trước, giữ nhiều chữ số khi trừ μ².',
        '<b>Phân vị, trung vị</b>: giải F(x) = p; với mật độ đối xứng, trung vị bằng tâm.',
        '<b>Hàm của biến ngẫu nhiên</b>: rời rạc gộp các giá trị trùng; liên tục viết F_Y theo F_X rồi đạo hàm.'], ordered=True)
    n += '<h2>4. Thực hành tương tác</h2>' + sim('rv') + sim('pdf')
    n += '<h2>5. Nội dung mở rộng trong slide</h2>' + ul(['<b>Phần 4</b>: tìm tham số, phân phối của Y = g(X), bảng đồng thời, hiệp phương sai, tổng hai biến.', '<b>Phần 5</b>: mật độ phân đoạn, Y = X², Y = 2X + 3, phân phối mũ và tính chất không nhớ, mốt, trung vị, trung bình.', '<b>Phần 6</b>: phương sai tổ hợp tuyến tính, tổng và trung bình của n biến, Markov, Chebyshev, quyết định bảo hiểm, độ lệch.'])
    n += '<h2>6. Bẫy và danh sách tự kiểm tra</h2>' + callout('warn', 'Chú ý khi làm bài', ul(['Viết rõ công thức rồi thay số; làm tròn ít nhất 3 chữ số thập phân.', 'E(g(X)) khác g(E(X)).', 'Var(X + Y) = Var X + Var Y chỉ khi độc lập hoặc Cov = 0.', 'Với BNN liên tục, P(X = a) = 0 nhưng f(a) có thể lớn hơn 1.', 'Mật độ đối xứng: kỳ vọng = trung vị = tâm đối xứng (kiểm tra nhanh).']))
    n += callout('good', 'Tự kiểm tra', ul(['Tôi kiểm tra được một bảng hoặc hàm có phải phân phối hợp lệ.', 'Tôi vẽ được F(x) bậc thang và đọc xác suất khoảng từ F.', 'Tôi tính được E, Var cho cả bảng lẫn mật độ.', 'Tôi biết khi nào dùng Chebyshev và khi nào dùng phân phối đã biết.']))
    return n
