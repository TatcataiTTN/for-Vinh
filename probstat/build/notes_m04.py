"""Module 4 — phần “Nội dung chi tiết” cuối trang (công thức dựng bằng KaTeX, số đã kiểm tra)."""
from fractions import Fraction as Fr
from hx import *
def notes():
    assert Fr(1, 2) * Fr(65, 100) + Fr(1, 2) * Fr(534, 1000) == Fr(592, 1000)
    assert abs(0.05 / 0.0525 - 0.9524) < 5e-5 and Fr(1, 10) * Fr(1, 12) + Fr(9, 10) * Fr(1, 36) == Fr(1, 30)
    assert abs(0.747 / 0.883 - 0.8460) < 5e-5 and abs((6 / 7 * .85) / (6 / 7 * .85 + .15 / 8) - 0.9749) < 5e-5
    n = '<h2>1. Đọc kèm giáo trình và các công thức cần nhớ</h2><p>Lecture Notes §1.6: Định nghĩa 1.6 (hệ đầy đủ), Định lý 1.5 (xác suất toàn phần), Định lý 1.6 (Bayes), Nhận xét 1.3 (tiên nghiệm, hậu kiểm), Ví dụ 1.20–1.22 và Bài 1.19–1.23. Kreyszig Part G không có phần Bayes riêng; các bài ở đây đều lấy từ giáo trình và đề thi.</p>'
    n += table(['Tên', 'Công thức', 'Dùng khi'], [
        ['Hệ đầy đủ', m('A_i\\cap A_j=\\varnothing,\\ \\textstyle\\sum_iP(A_i)=1'), 'chia nguyên nhân thành các nhóm không chồng lấn'],
        ['Toàn phần', m('P(B)=\\textstyle\\sum_iP(A_i)P(B|A_i)'), 'hỏi xác suất của kết quả chung'],
        ['Bayes', m('P(A_i|B)=\\dfrac{P(A_i)P(B|A_i)}{P(B)}'), 'biết kết quả, hỏi nguyên nhân'],
        ['Dạng odds', m('\\text{odds hậu nghiệm}=\\text{odds tiên nghiệm}\\times\\mathrm{LR}'), 'nhiều bằng chứng độc lập, cập nhật liên tiếp'],
        ['Cây xác suất', m('P(\\text{đường đi})=\\prod P(\\text{nhánh})'), 'bài hai giai đoạn, kiểm tra nhanh']])
    n += '<h2>2. Các bài gốc của giáo trình, giải bằng công thức</h2>'
    n += ex('Bài 1.19 · Thừa cân ở Canada', '<p>65.0% đàn ông và 53.4% đàn bà thừa cân; số nam bằng số nữ. P(thừa cân)?</p>' + steps([m('P=0.5\\cdot0.650+0.5\\cdot0.534=0.592')]))
    n += ex('Bài 1.20 · Mù màu', '<p>5% đàn ông và 0.25% đàn bà mù màu. Chọn một người mù màu, xác suất là nam?</p>' + steps([m('P(\\text{nam}|\\text{mù})=\\tfrac{0.5\\cdot0.05}{0.5\\cdot0.05+0.5\\cdot0.0025}=\\tfrac{0.05}{0.0525}=0.9524'), 'Tiên nghiệm 0.5 tăng lên 0.9524 sau khi biết người đó mù màu.']))
    n += ex('Bài 1.21 · Hai hộp áo', '<p>Chuyển 1 áo từ hộp I (10 áo, 1 lỗi) sang hộp II (8 áo, 2 lỗi), rồi chọn 2 áo từ hộp II. P(cả hai lỗi)?</p>' + steps(['Áo chuyển lỗi (xác suất 1/10): hộp II có 9 áo, 3 lỗi: ' + m('\\tfrac39\\cdot\\tfrac28=\\tfrac1{12}'), 'Áo chuyển tốt (9/10): hộp II có 9 áo, 2 lỗi: ' + m('\\tfrac29\\cdot\\tfrac18=\\tfrac1{36}'), m('P=\\tfrac1{10}\\cdot\\tfrac1{12}+\\tfrac9{10}\\cdot\\tfrac1{36}=\\tfrac1{120}+\\tfrac1{40}=\\tfrac1{30}\\approx0.0333')]))
    n += ex('Bài 1.22 · Phòng khám', '<p>83% người đến khám có bệnh; chẩn đoán đúng 90% với người bệnh và 80% với người không bệnh.</p>' + steps([m('P(\\text{đúng})=0.83\\cdot0.9+0.17\\cdot0.8=0.747+0.136=0.883'), m('P(\\text{có bệnh}|\\text{đúng})=\\tfrac{0.747}{0.883}=0.8460')]))
    n += ex('Ví dụ 1.22 · Trạm phát tín hiệu', '<p>Phát I với 0.85, II với 0.15; 1/7 tín hiệu I và 1/8 tín hiệu II bị méo thành tín hiệu kia.</p>' + steps([m('P(\\text{thu I})=\\tfrac67\\cdot0.85+\\tfrac18\\cdot0.15=0.7473'), m('P(\\text{phát I}|\\text{thu I})=\\tfrac{0.7286}{0.7473}=0.9749')]))
    n += '<h2>3. Thực hành tương tác</h2>' + sim('bayes') + sim('freq')
    n += '<h2>4. Nội dung mở rộng trong slide</h2>' + ul(['<b>Phần 4</b>: Bayes dạng odds, cập nhật liên tiếp, xét nghiệm dương rồi âm, bốn nguyên nhân, bảng đếm.', '<b>Phần 5</b>: nghịch lý và bẫy (hộp Bertrand, Monty Hall, ngụy biện của công tố viên, bỏ qua tỉ lệ nền, Simpson).', '<b>Phần 6</b>: ứng dụng (lọc thư rác, đoán mò khi thi, chẩn đoán hỏng hóc) và bảng chọn công thức.'])
    n += '<h2>5. Bối cảnh lý thuyết và lịch sử</h2>' + callout('info', '📜 Thomas Bayes', 'Định lý do mục sư Thomas Bayes (1701–1761) tìm ra và được Richard Price công bố sau khi ông mất (1763); Laplace tổng quát hóa (1774). Ngày nay Bayes là nền của lọc thư rác, chẩn đoán y khoa, học máy xác suất và suy luận Bayes.')
    n += '<h2>6. Case study: bộ lọc thư rác</h2><p>40% thư là spam; từ “khuyến mãi” xuất hiện trong 80% spam và 10% thư thường (số minh họa). Với thư có từ này:</p>' + steps([m('P(\\text{spam}|\\text{từ})=\\tfrac{0.4\\cdot0.8}{0.4\\cdot0.8+0.6\\cdot0.1}=\\tfrac{0.32}{0.38}=0.8421'), 'Mỗi từ khóa mới nhân thêm một tỉ số hợp lý (Bayes ngây thơ, giả định độc lập có điều kiện).'])
    n += '<h2>7. Bẫy và danh sách tự kiểm tra</h2>' + callout('warn', 'Chú ý khi làm bài', ul(['Đọc kỹ “biết rằng” để xác định điều kiện; P(A|B) khác P(B|A).', 'Ghi rõ hệ đầy đủ và kiểm tra tổng tiên nghiệm bằng 1.', 'Tính P(B) bằng toàn phần trước, rồi mới chia để ra hậu nghiệm.', 'Hậu nghiệm cộng lại phải bằng 1; nếu không, mẫu số sai.', 'Bệnh hiếm: đừng bỏ qua tỉ lệ nền.']))
    n += callout('good', 'Tự kiểm tra', ul(['Tôi gọi tên được nguyên nhân Aᵢ và kết quả B.', 'Tôi lập được bảng P(Aᵢ), P(B|Aᵢ), tích và hậu nghiệm.', 'Tôi giải thích được vì sao dương tính có thể vẫn thường là khỏe.', 'Tôi chuyển được bài thành cây xác suất hoặc bảng đếm để kiểm tra.']))
    return n
