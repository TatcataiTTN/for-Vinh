"""Module 4 — phần chuyên sâu: mọi số được tính bằng phân số chính xác khi dựng trang."""
from fractions import Fraction as Fr
from hx import *
from orig_m04 import tot, post
K = 'MODULE 4 · '
def pc(x, d=2): return f'{float(x)*100:.{d}f}%'
def parts():
    P = []
    # ───────── A. Toàn phần ─────────
    s = []
    pri = [Fr(1, 2), Fr(3, 10), Fr(1, 5)]; lk = [Fr(2, 100), Fr(3, 100), Fr(5, 100)]
    T = tot(pri, lk); assert abs(float(T) - 0.029) < 1e-12
    s.append(sl(callout('info', 'Ví dụ A1 · Ba dây chuyền', 'Ba dây chuyền sản xuất 50%, 30%, 20% sản lượng; tỉ lệ phế phẩm 2%, 3%, 5%. Chọn ngẫu nhiên một sản phẩm. P(phế phẩm)?')
                + table(['Dây chuyền', 'P(Aᵢ)', 'P(B | Aᵢ)', 'Tích'], [[f'{i+1}', f'{float(p):.2f}', f'{float(l):.2f}', f'{float(p*l):.3f}'] for i, (p, l) in enumerate(zip(pri, lk))] + [['Tổng', '1', '', f'{float(T):.3f}']])
                + steps([m('P(B)=\\sum_iP(A_i)P(B|A_i)=0.5\\cdot0.02+0.3\\cdot0.03+0.2\\cdot0.05'), m('=0.010+0.009+0.010=0.029')]) + '<p>Nhìn như trung bình có trọng số của các tỉ lệ phế phẩm.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Công thức toàn phần từng bước', explain='Chia “thế giới” thành các trường hợp không chồng lấn, tính xác suất của B trong từng trường hợp rồi cộng theo tỉ trọng.'))
    s.append(sl(callout('info', 'Ví dụ A2 · Hai hộp', 'Hộp I: 3 bi trắng, 2 đen. Hộp II: 2 trắng, 4 đen. Chọn một hộp ngẫu nhiên, rút một bi. P(trắng)?')
                + steps([m('P(T)=\\tfrac12\\cdot\\tfrac35+\\tfrac12\\cdot\\tfrac26=0.3+0.1667=0.4667')]) + '<p>Nếu chọn hộp theo xác suất 0.7 và 0.3 thì P(T) = 0.7·0.6 + 0.3·0.3333 = 0.52: đáp số thay đổi theo xác suất chọn hộp.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Chọn hộp rồi rút bi'))
    P.append(dict(title='Chuyên sâu: xác suất toàn phần', bullets=['Ba dây chuyền', 'Hai hộp'], slides=s))
    # ───────── B. Bayes ─────────
    s = []
    ps = [post(pri, lk, i) for i in range(3)]; assert abs(sum(ps) - 1) < 1e-12
    s.append(sl(callout('info', 'Ví dụ B1 · Sản phẩm phế phẩm đến từ đâu?', 'Tiếp Ví dụ A1: sản phẩm chọn ra là phế phẩm. Xác suất nó do từng dây chuyền?')
                + table(['Dây chuyền', 'Tiên nghiệm P(Aᵢ)', 'P(Aᵢ)P(B|Aᵢ)', 'Hậu nghiệm P(Aᵢ|B)'], [[f'{i+1}', f'{float(p):.2f}', f'{float(p*l):.3f}', f'{float(post(pri,lk,i)):.4f}'] for i, (p, l) in enumerate(zip(pri, lk))])
                + steps([m('P(A_1|B)=\\tfrac{0.010}{0.029}=0.3448'), m('P(A_2|B)=\\tfrac{0.009}{0.029}=0.3103'), m('P(A_3|B)=\\tfrac{0.010}{0.029}=0.3448')]) + '<p>Dây chuyền 3 chỉ sản xuất 20% nhưng chịu trách nhiệm 34.5% phế phẩm vì tỉ lệ lỗi cao nhất. Tổng hậu nghiệm = 1.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Bayes: cập nhật niềm tin sau khi quan sát', explain='Bayes đảo chiều điều kiện: từ “biết nguyên nhân, xác suất kết quả” sang “thấy kết quả, xác suất nguyên nhân”.'))
    sens, spec, prev = Fr(95, 100), Fr(90, 100), Fr(1, 100)
    ppv = sens * prev / (sens * prev + (1 - spec) * (1 - prev)); npv = spec * (1 - prev) / (spec * (1 - prev) + (1 - sens) * prev)
    s.append(sl(callout('info', 'Ví dụ B2 · Xét nghiệm sàng lọc', 'Bệnh có tỉ lệ mắc 1%. Xét nghiệm có độ nhạy 95% (P(+|bệnh)) và độ đặc hiệu 90% (P(−|khỏe)). Người có kết quả dương tính thực sự bệnh với xác suất bao nhiêu?')
                + steps([m('P(+)=0.95\\cdot0.01+0.10\\cdot0.99=0.0095+0.099=0.1085'), m(f'P(\\text{{bệnh}}|+)=\\tfrac{{0.0095}}{{0.1085}}={float(ppv):.4f}'), m(f'P(\\text{{khỏe}}|-)=\\tfrac{{0.891}}{{0.8915}}={float(npv):.4f}')])
                + callout('warn', 'Nghịch lý', f'Dù xét nghiệm “chính xác 90–95%”, dương tính chỉ có {pc(ppv,1)} khả năng bệnh thật vì bệnh hiếm (tiên nghiệm 1%).'), K + 'PHẦN 2 · Chuyên sâu', 'Giá trị tiên đoán dương'))
    s.append(sl(callout('info', 'Ví dụ B3 · Tần suất tự nhiên (10 000 người)', 'Cùng số liệu Ví dụ B2, đếm người thay vì xác suất.')
                + table(['', 'Bệnh (100)', 'Khỏe (9 900)', 'Tổng'], [['Dương tính', '95', '990', '1 085'], ['Âm tính', '5', '8 910', '8 915']])
                + '<p>Trong 1 085 người dương tính, chỉ 95 người thật sự bệnh: 95/1085 = 8.76%. Cách đếm này giúp hiểu trực giác, kết quả trùng công thức Bayes.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Cùng bài toán bằng bảng đếm'))
    p2 = sens * ppv / (sens * ppv + (1 - spec) * (1 - ppv))
    s.append(sl(callout('info', 'Ví dụ B4 · Xét nghiệm lặp lại', 'Người dương tính lần một làm lại xét nghiệm độc lập, lại dương tính. Xác suất bệnh?')
                + steps([m(f'\\text{{Tiên nghiệm mới}}=P(\\text{{bệnh}}|+)={float(ppv):.4f}'), m(f'P(\\text{{bệnh}}|++)=\\tfrac{{0.95\\cdot{float(ppv):.4f}}}{{0.95\\cdot{float(ppv):.4f}+0.10\\cdot{float(1-ppv):.4f}}}={float(p2):.4f}')]) + '<p>Hậu nghiệm của lần trước thành tiên nghiệm của lần sau: hai dương tính đưa xác suất lên ~48%.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Cập nhật liên tiếp'))
    s.append(sl(callout('info', 'Ví dụ B5 · Kênh truyền nhiễu', 'Nguồn gửi bit 1 với xác suất 0.6, bit 0 với 0.4. Kênh lật bit với xác suất 0.1. Nhận được bit 1. Xác suất đã gửi 1?')
                + steps([m('P(\\text{nhận }1)=0.6\\cdot0.9+0.4\\cdot0.1=0.58'), m('P(\\text{gửi }1|\\text{nhận }1)=\\tfrac{0.54}{0.58}=0.9310')]), K + 'PHẦN 2 · Chuyên sâu', 'Bayes trong truyền thông'))
    P.append(dict(title='Chuyên sâu: công thức Bayes', bullets=['Hậu nghiệm từng bước', 'Xét nghiệm sàng lọc', 'Tần suất tự nhiên', 'Xét nghiệm lặp lại', 'Kênh nhiễu'], slides=s))
    # ───────── C. Quy trình ─────────
    s = []
    s.append(sl(ul(['<b>Bước 1</b>: gọi tên các nguyên nhân A₁, …, Aₙ (hệ đầy đủ: xung khắc, tổng xác suất 1) và kết quả B.', '<b>Bước 2</b>: lập bảng P(Aᵢ) và P(B|Aᵢ).', '<b>Bước 3</b>: toàn phần P(B) = ΣP(Aᵢ)P(B|Aᵢ).', '<b>Bước 4</b>: Bayes P(Aᵢ|B) = P(Aᵢ)P(B|Aᵢ)/P(B).', '<b>Bước 5</b>: kiểm tra Σ P(Aᵢ|B) = 1.'])
                + callout('warn', 'Dấu hiệu nhận biết', 'Đề hỏi “biết kết quả B, xác suất do nguyên nhân Aᵢ” ⇒ Bayes. Đề hỏi “xác suất kết quả B chung” ⇒ toàn phần.'), K + 'PHẦN 3 · Chuyên sâu', 'Quy trình năm bước'))
    s.append(sl(callout('info', 'Ví dụ C1 · Cây xác suất hai giai đoạn', 'Giai đoạn 1: máy A (60%) hoặc B (40%). Giai đoạn 2: sản phẩm đạt (A: 97%, B: 92%).')
                + table(['Đường đi', 'Xác suất'], [['A → đạt', '0.6·0.97 = 0.582'], ['A → lỗi', '0.6·0.03 = 0.018'], ['B → đạt', '0.4·0.92 = 0.368'], ['B → lỗi', '0.4·0.08 = 0.032']])
                + '<p>Nhân dọc theo nhánh, cộng các nhánh cùng kết quả: P(đạt) = 0.950; P(A | lỗi) = 0.018/0.05 = 0.36.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Cây xác suất'))
    P.append(dict(title='Chuyên sâu: quy trình và cây', bullets=['Năm bước', 'Cây hai giai đoạn'], slides=s))
    from more_m04b import parts as _pb
    P += _pb()
    return P
