"""Module 3 — phần chuyên sâu: số liệu tính bằng phân số chính xác / liệt kê khi dựng trang."""
import itertools
from fractions import Fraction as Fr
from hx import *
K = 'MODULE 3 · '
def parts():
    P = []
    # kiểm chứng
    assert Fr(5, 8) * Fr(4, 7) == Fr(5, 14)
    kids = list(itertools.product('TG', repeat=2))   # T=trai, G=gái; (anh/chị, em)
    a = [k for k in kids if 'T' in k]; assert Fr(sum(1 for k in a if k == ('T', 'T')), len(a)) == Fr(1, 3)
    b = [k for k in kids if k[0] == 'T']; assert Fr(sum(1 for k in b if k == ('T', 'T')), len(b)) == Fr(1, 2)
    # ───────── A. Cộng và bù ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ A1 · Quy tắc cộng cho hai biến cố', 'Rút một lá từ bộ 52 lá. A = “lá cơ”, B = “J, Q hoặc K”. Tính P(A ∪ B).')
                + steps([m('P(A)=\\tfrac{13}{52},\\ P(B)=\\tfrac{12}{52},\\ P(A\\cap B)=\\tfrac3{52}'), m('P(A\\cup B)=\\tfrac{13+12-3}{52}=\\tfrac{22}{52}=\\tfrac{11}{26}\\approx0.4231')]) + '<p>Nếu quên trừ P(A ∩ B) sẽ đếm hai lần ba lá J♥, Q♥, K♥.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Cộng xác suất và phần giao'))
    s.append(sl(callout('info', 'Ví dụ A2 · Bù trừ ba biến cố', 'Khảo sát sinh viên: P(A) = 0.5 (học tiếng Anh), P(B) = 0.4 (Pháp), P(C) = 0.3 (Nhật), P(AB) = 0.2, P(AC) = 0.1, P(BC) = 0.15, P(ABC) = 0.05. Tìm xác suất học ít nhất một ngoại ngữ và không học ngoại ngữ nào.')
                + steps([m('P(A\\cup B\\cup C)=0.5+0.4+0.3-0.2-0.1-0.15+0.05=0.8'), m('P(\\text{không học})=1-0.8=0.2')]), K + 'PHẦN 1 · Chuyên sâu', 'Công thức cộng cho ba biến cố'))
    s.append(sl(callout('info', 'Ví dụ A3 · “Ít nhất một” bằng phần bù', 'Năm người độc lập thử cùng một việc, mỗi người thành công với xác suất 0.1. P(có ít nhất một người thành công)?')
                + steps([m('P(\\text{không ai})=0.9^5=0.5905'), m('P(\\ge1)=1-0.5905=0.4095')]) + '<p>Tính trực tiếp phải cộng 5 trường hợp; phần bù chỉ một phép tính.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Ít nhất một: dùng phần bù'))
    P.append(dict(title='Chuyên sâu: quy tắc cộng và phần bù', bullets=['Cộng hai biến cố', 'Bù trừ ba biến cố', 'Ít nhất một'], slides=s))
    # ───────── B. Có điều kiện ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ B1 · Bảng hai chiều', 'Khảo sát 200 sinh viên: học thêm (A) và đậu (B). Có học thêm & đậu: 90; học thêm & trượt: 10; không học thêm & đậu: 60; không học thêm & trượt: 40.')
                + table(['', 'Đậu', 'Trượt', 'Tổng'], [['Học thêm', '90', '10', '100'], ['Không học thêm', '60', '40', '100'], ['Tổng', '150', '50', '200']])
                + steps([m('P(B)=\\tfrac{150}{200}=0.75;\\ P(A)=0.5;\\ P(A\\cap B)=\\tfrac{90}{200}=0.45'), m('P(B|A)=\\tfrac{90}{100}=0.9;\\ P(B|A^c)=\\tfrac{60}{100}=0.6'), m('P(A|B)=\\tfrac{90}{150}=0.6\\ne P(B|A)'), m('P(A)P(B)=0.375\\ne0.45\\Rightarrow\\text{không độc lập}')]), K + 'PHẦN 2 · Chuyên sâu', 'Đọc xác suất có điều kiện từ bảng'))
    s.append(sl(callout('info', 'Ví dụ B2 · Rút không hoàn lại', 'Hộp 5 bi đỏ, 3 bi xanh. Rút lần lượt 2 bi không hoàn lại. P(cả hai đỏ)? P(khác màu)?')
                + steps([m('P(Đ_1)=\\tfrac58,\\ P(Đ_2|Đ_1)=\\tfrac47\\Rightarrow P(ĐĐ)=\\tfrac58\\cdot\\tfrac47=\\tfrac5{14}\\approx0.3571'), m('P(\\text{khác màu})=\\tfrac58\\cdot\\tfrac37+\\tfrac38\\cdot\\tfrac57=\\tfrac{30}{56}=\\tfrac{15}{28}\\approx0.5357')])
                + '<p>Có hoàn lại: P(ĐĐ) = (5/8)² = 0.3906 — khác vì xác suất lần hai không đổi.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Công thức nhân P(AB) = P(A)P(B|A)'))
    s.append(sl(callout('info', 'Ví dụ B3 · Chuỗi ba lá bài', 'Rút 3 lá liên tiếp không hoàn lại. P(cả ba đều là át)?')
                + steps([m('P=\\tfrac4{52}\\cdot\\tfrac3{51}\\cdot\\tfrac2{50}=\\tfrac{24}{132600}=\\tfrac1{5525}\\approx0.000181')]) + '<p>Tổng quát: P(A₁A₂A₃) = P(A₁)·P(A₂|A₁)·P(A₃|A₁A₂).</p>', K + 'PHẦN 2 · Chuyên sâu', 'Công thức nhân mở rộng'))
    s.append(sl(callout('info', 'Ví dụ B4 · Hai đứa trẻ', 'Gia đình có hai con. (a) Biết có ít nhất một con trai, P(cả hai là trai)? (b) Biết con đầu là trai, P(cả hai là trai)?')
                + steps(['Không gian mẫu (đầu, sau): TT, TG, GT, GG đồng khả năng.', m('\\text{(a) Thu hẹp còn {TT, TG, GT}: }P=\\tfrac13'), m('\\text{(b) Thu hẹp còn {TT, TG}: }P=\\tfrac12')]) + '<p>Thông tin “ít nhất một” và “con đầu” cho hai không gian thu hẹp khác nhau nên đáp án khác nhau (đã kiểm chứng bằng liệt kê).</p>', K + 'PHẦN 2 · Chuyên sâu', 'Thu hẹp không gian mẫu: bẫy kinh điển'))
    s.append(sl(callout('info', 'Ví dụ B5 · Bài toán Monty Hall', 'Ba cửa, một có xe. Bạn chọn cửa 1; người dẫn (biết sau cửa nào) mở một cửa dê. Đổi hay giữ?')
                + steps(['Giữ: thắng khi lúc đầu chọn đúng: 1/3.', 'Đổi: thắng khi lúc đầu chọn sai (2/3) vì người dẫn đã loại cửa dê còn lại, cửa còn lại chắc chắn có xe.', m('P(\\text{thắng nếu đổi})=\\tfrac23>\\tfrac13')]) + '<p>Điểm mấu chốt: người dẫn không mở ngẫu nhiên nên thông tin thay đổi xác suất có điều kiện.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Monty Hall'))
    P.append(dict(title='Chuyên sâu: xác suất có điều kiện', bullets=['Bảng hai chiều', 'Rút không hoàn lại', 'Hai đứa trẻ, Monty Hall'], slides=s))
    # ───────── C. Độc lập và độ tin cậy ─────────
    s = []
    s.append(sl(callout('info', 'Ví dụ C1 · Kiểm tra độc lập', 'P(A) = 0.4, P(B) = 0.5. (a) P(A ∩ B) = 0.2. (b) P(A ∩ B) = 0.25. Hai biến cố có độc lập không?')
                + steps([m('\\text{Độc lập }\\iff P(A\\cap B)=P(A)P(B)=0.2'), m('\\text{(a) }0.2=0.2\\Rightarrow\\text{độc lập}'), m('\\text{(b) }0.25\\ne0.2\\Rightarrow\\text{không độc lập; }P(A|B)=0.5\\ne P(A)')]), K + 'PHẦN 3 · Chuyên sâu', 'Định nghĩa độc lập'))
    s.append(sl(callout('info', 'Ví dụ C2 · Độ tin cậy hệ thống', 'Ba linh kiện độc lập, độ tin cậy 0.9; 0.95; 0.98.')
                + steps([m('\\text{Nối tiếp: }R=0.9\\cdot0.95\\cdot0.98=0.8379'), m('\\text{Song song: }R=1-0.1\\cdot0.05\\cdot0.02=0.9999'), m('\\text{Hỗn hợp: linh kiện 1 nối tiếp với (2 song song 3): }R=0.9\\,[1-0.05\\cdot0.02]=0.8991')])
                + '<p>Nối tiếp làm tin cậy giảm (mắt xích yếu nhất); song song tăng nhờ dự phòng.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Nối tiếp, song song, hỗn hợp'))
    s.append(sl(callout('info', 'Ví dụ C3 · Bắn đến khi trúng', 'Xạ thủ trúng mỗi phát với xác suất 0.7, độc lập. P(trúng ở phát thứ k)? P(cần không quá 3 phát)?')
                + steps([m('P(K=k)=0.3^{k-1}\\cdot0.7'), m('P(K\\le3)=1-0.3^3=0.973'), m('E(K)=1/0.7\\approx1.43\\text{ phát}')]), K + 'PHẦN 3 · Chuyên sâu', 'Phân phối hình học (xem trước)'))
    s.append(sl(table(['Câu hỏi', 'Công thức', 'Điều kiện'], [['P(A hoặc B)', 'P(A) + P(B) − P(AB)', 'luôn đúng'], ['P(A và B)', 'P(A)P(B|A)', 'luôn đúng'], ['P(A và B)', 'P(A)P(B)', 'chỉ khi độc lập'], ['P(ít nhất một)', '1 − P(không có)', 'dùng phần bù'], ['P(A hoặc B)', 'P(A) + P(B)', 'chỉ khi xung khắc']])
                + callout('warn', 'Xung khắc ≠ độc lập', 'Nếu P(A), P(B) > 0 và A, B xung khắc thì P(AB) = 0 ≠ P(A)P(B): hai biến cố KHÔNG độc lập.'), K + 'PHẦN 3 · Chuyên sâu', 'Bảng tổng hợp công thức'))
    P.append(dict(title='Chuyên sâu: độc lập và độ tin cậy', bullets=['Kiểm tra độc lập', 'Nối tiếp, song song', 'Bắn đến khi trúng', 'Bảng công thức'], slides=s))
    return P
