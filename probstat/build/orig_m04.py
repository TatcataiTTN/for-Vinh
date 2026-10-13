"""Module 4 — Xác suất toàn phần và Bayes. Gốc: Lecture Notes §1.6 (Ví dụ 1.20–1.22), Bài 1.19–1.23, đề giữa kỳ mẫu câu 5 và đáp án giữa kỳ HK2 2022–2023 câu 1."""
import random
from fractions import Fraction as Fr
from qb import f, fg, nd
from qh import pm
TOP = {'total': 'Xác suất toàn phần', 'bayes': 'Công thức Bayes (hậu nghiệm)', 'system': 'Hệ đầy đủ các biến cố', 'tree': 'Cây xác suất, hai giai đoạn', 'theory': 'Lý thuyết'}
def tot(prior, like): return sum(p * l for p, l in zip(prior, like))
def post(prior, like, i): return prior[i] * like[i] / tot(prior, like)
def build(B):
    rng = random.Random(404); P = pm
    S = 'Lecture Notes '
    # Ví dụ 1.20
    pr, lk = [0.35, 0.45, 0.20], [0.01, 0.005, 0.002]
    P(B, rng, 'Phân xưởng có 3 nhà máy I, II, III sản xuất 35%, 45%, 20% sản phẩm với tỉ lệ phế phẩm 1%, 0.5%, 0.2%. Chọn ngẫu nhiên một sản phẩm; xác suất đó là phế phẩm là', tot(pr, lk),
      'Công thức xác suất toàn phần: P(B) = 0.35·0.01 + 0.45·0.005 + 0.20·0.002 = 0.0035 + 0.00225 + 0.0004 = 0.00615.', 1, TOP['total'], S + 'Ví dụ 1.20', extra=[(0.01 + 0.005 + 0.002) / 3, 0.017, 0.0035], d=5)
    for i, nm in enumerate(['I', 'II', 'III']):
        P(B, rng, f'Cùng bài (ví dụ 1.20), biết sản phẩm chọn là phế phẩm, xác suất nó do nhà máy {nm} sản xuất (hậu nghiệm) là', post(pr, lk, i),
          f'P(A{i+1} | B) = P(B | A{i+1})P(A{i+1})/P(B) = {pr[i]}·{lk[i]}/0.00615 = {f(post(pr,lk,i),4)}. (Tiên nghiệm là {pr[i]}.)', 2, TOP['bayes'], S + 'Ví dụ 1.20 (mở rộng Bayes)', extra=[pr[i], lk[i], pr[i] * lk[i]], d=4)
    # Ví dụ 1.21
    pa, pb2 = 0.95, 0.98
    P(B, rng, 'Mạch gồm hai bộ phận nối tiếp, xác suất làm việc bình thường 0.95 và 0.98. Xác suất mạch ngừng làm việc là', 1 - pa * pb2, 'Mạch chạy ⇔ cả hai chạy: 0.95·0.98 = 0.931 ⇒ ngừng: 1 − 0.931 = 0.069.', 1, TOP['system'], S + 'Ví dụ 1.21', extra=[0.05 + 0.02 + 0.001, 0.931, 0.05], d=3)
    B.mcq('Cùng mạch đó, thấy mạch ngừng làm việc. Xác suất “chỉ đúng bộ phận thứ hai hỏng” (Ví dụ 1.21) là', '19/69', ['0.02', '49/69', '1/69'], 'Hệ đầy đủ A₁ (cả hai chạy) 0.931; A₂ (I chạy, II hỏng) 0.019; A₃ (I hỏng, II chạy) 0.049; A₄ (cả hai hỏng) 0.001. P(A₂ | ngừng) = 0.019/(0.019 + 0.049 + 0.001) = 19/69 ≈ 0.2754.', 2, TOP['bayes'], S + 'Ví dụ 1.21')
    B.mcq('Cùng mạch đó, thấy mạch ngừng làm việc. Xác suất chỉ bộ phận thứ nhất hỏng là', '49/69', ['0.05', '19/69', '1/69'], 'P(A₃ | ngừng) = 0.049/0.069 = 49/69 ≈ 0.7101.', 2, TOP['bayes'], S + 'Ví dụ 1.21 (mở rộng)')
    # Ví dụ 1.22
    pr2, lk2 = [0.85, 0.15], [6 / 7, 1 / 8]
    P(B, rng, 'Trạm phát tín hiệu I (xác suất 0.85) và II (0.15). Nhiễu làm 1/7 tín hiệu I thu như II, và 1/8 tín hiệu II thu như I. Xác suất thu được tín hiệu loại I là', tot(pr2, lk2), f'P(B) = (6/7)(0.85) + (1/8)(0.15) = {f(0.85*6/7,5)} + 0.01875 = {f(tot(pr2,lk2),4)}.', 2, TOP['total'], S + 'Ví dụ 1.22(i)', extra=[0.85, 6 / 7, 0.8], d=3)
    P(B, rng, 'Cùng trạm phát: đã thu được tín hiệu loại I. Xác suất tín hiệu được phát đúng là loại I là', post(pr2, lk2, 0), f'P(A₁ | B) = 0.85·(6/7)/{f(tot(pr2,lk2),4)} = {f(post(pr2,lk2,0),4)} ≈ 0.975.', 2, TOP['bayes'], S + 'Ví dụ 1.22(ii)', extra=[6 / 7, 0.85, 0.747], d=3)
    # Bài 1.19
    P(B, rng, 'Canada 2004: 65.0% đàn ông và 53.4% đàn bà thừa cân; số đàn ông bằng số đàn bà. Chọn ngẫu nhiên một người; xác suất người đó thừa cân là (Bài 1.19)', 0.5 * 0.65 + 0.5 * 0.534, 'Toàn phần với P(nam) = P(nữ) = 0.5: 0.5·0.65 + 0.5·0.534 = 0.325 + 0.267 = 0.592.', 1, TOP['total'], S + 'Bài 1.19', extra=[0.65 + 0.534, 0.65 * 0.534, 0.65], d=3)
    # Bài 1.20
    P(B, rng, '5% đàn ông và 0.25% đàn bà bị mù màu; số đàn ông bằng số đàn bà. Chọn một người bị mù màu; xác suất người đó là đàn ông là (Bài 1.20)', 0.05 / (0.05 + 0.0025), 'Bayes: P(nam | mù màu) = 0.5·0.05/(0.5·0.05 + 0.5·0.0025) = 0.05/0.0525 = 0.9524.', 2, TOP['bayes'], S + 'Bài 1.20', extra=[0.05, 0.5, 0.9], d=4)
    P(B, rng, 'Cùng bài mù màu (Bài 1.20): xác suất một người chọn ngẫu nhiên bị mù màu là', 0.5 * 0.05 + 0.5 * 0.0025, 'P = 0.5·0.05 + 0.5·0.0025 = 0.02625.', 1, TOP['total'], S + 'Bài 1.20 (bước toàn phần)', extra=[0.0525, 0.05 + 0.0025, 0.0025], d=5)
    # Bài 1.21 hai hộp áo
    # hộp I: 10 áo, 1 lỗi. hộp II: 8 áo, 2 lỗi. Chuyển 1 áo I -> II; rồi lấy 2 áo từ II (9 áo); cả hai lỗi
    p_def = 1 / 10
    pb21 = p_def * (3 * 2) / (9 * 8) + (1 - p_def) * (2 * 1) / (9 * 8)
    P(B, rng, 'Hộp I có 10 áo (1 lỗi), hộp II có 8 áo (2 lỗi). Lấy ngẫu nhiên 1 áo từ hộp I bỏ sang hộp II, rồi từ hộp II chọn ngẫu nhiên 2 áo. Xác suất cả hai áo đều lỗi là (Bài 1.21)', pb21,
      f'Nếu áo chuyển lỗi (xác suất 1/10): hộp II có 9 áo, 3 lỗi ⇒ (3/9)(2/8) = 1/12. Nếu áo chuyển tốt (9/10): 9 áo, 2 lỗi ⇒ (2/9)(1/8) = 1/36. P = (1/10)(1/12) + (9/10)(1/36) = {f(pb21,5)}.', 3, TOP['tree'], S + 'Bài 1.21', extra=[(2 / 8) * (1 / 7), 1 / 12, 1 / 36, 3 / 28], d=5)
    # Bài 1.22 phòng khám
    pr3, lk3 = [0.83, 0.17], [0.9, 0.8]
    pd = tot(pr3, lk3)
    P(B, rng, 'Phòng khám: 83% người đến khám có bệnh. Nếu chẩn đoán “có bệnh” thì đúng 90%, nếu chẩn đoán “không bệnh” thì đúng 80% — hiểu là P(chẩn đoán đúng | có bệnh) = 0.9, P(chẩn đoán đúng | không bệnh) = 0.8. Xác suất chẩn đoán đúng là (Bài 1.22a)', pd, f'P(đúng) = 0.83·0.9 + 0.17·0.8 = 0.747 + 0.136 = {f(pd,3)}.', 2, TOP['total'], S + 'Bài 1.22(a)', extra=[0.85, 0.9, 0.83], d=3)
    P(B, rng, 'Cùng bài phòng khám: biết một trường hợp chẩn đoán đúng, xác suất người đó có bệnh (Bài 1.22b) là', 0.83 * 0.9 / pd, f'P(có bệnh | đúng) = 0.747/{f(pd,3)} = {f(0.83*0.9/pd,4)}.', 3, TOP['bayes'], S + 'Bài 1.22(b)', extra=[0.83, 0.9, 0.747], d=4)
    # Bài 1.23 pít-tông
    pr4, lk4 = [0.40, 0.35, 0.25], [0.05, 0.08, 0.04]
    P(B, rng, 'Nhà máy A có 3 phân xưởng I, II, III sản xuất 40%, 35%, 25% pít-tông với tỉ lệ phế phẩm 5%, 8%, 4%. Xác suất một pít-tông chọn ngẫu nhiên là phế phẩm (Bài 1.23a) là', tot(pr4, lk4), '0.4·0.05 + 0.35·0.08 + 0.25·0.04 = 0.02 + 0.028 + 0.01 = 0.058.', 1, TOP['total'], S + 'Bài 1.23(a)', extra=[(0.05 + 0.08 + 0.04) / 3, 0.08, 0.17], d=3)
    for i, nm in enumerate(['I', 'II', 'III']):
        P(B, rng, f'Cùng bài pít-tông: biết sản phẩm là phế phẩm, xác suất nó do phân xưởng {nm} sản xuất là' + (' (Bài 1.23b)' if i == 1 else ''), post(pr4, lk4, i), f'P(A{i+1} | phế phẩm) = {pr4[i]}·{lk4[i]}/0.058 = {f(pr4[i]*lk4[i],4)}/0.058 = {f(post(pr4,lk4,i),4)}.', 2, TOP['bayes'], S + 'Bài 1.23' + ('(b)' if i == 1 else ' (mở rộng)'), extra=[pr4[i], lk4[i], pr4[i] * lk4[i]], d=4)
    # Đề giữa kỳ mẫu câu 5
    P(B, rng, 'Tỉ lệ mắc bệnh A ở nam là 0.07 và ở nữ là 0.07. Một vùng dân cư có 55% nam và 45% nữ. Chọn ngẫu nhiên một người; xác suất người đó mắc bệnh A là', 0.07, 'P = 0.55·0.07 + 0.45·0.07 = 0.07·(0.55 + 0.45) = 0.07. Tỉ lệ bằng nhau nên kết quả không phụ thuộc cơ cấu nam–nữ.', 1, TOP['total'], 'Đề giữa kỳ mẫu LTXSTK, câu 5', extra=[0.14, 0.0385, 0.55], d=3)
    # Đáp án giữa kỳ HK2 2022-2023 câu 1 (a=3,b=2,c=2): P(A)=0.45,0.25,0.3 ; P(B|A)=0.636,0.444,0.7
    pr5, lk5 = [0.45, 0.25, 0.30], [0.636, 0.444, 0.7]
    K = 'Đáp án giữa kỳ HK2 2022–2023, câu 1 (a=3, b=2, c=2)'
    P(B, rng, 'Sản phẩm thuộc phân xưởng 1, 2, 3 với xác suất P(A₁) = 0.45, P(A₂) = 0.25, P(A₃) = 0.3; xác suất là phế phẩm theo phân xưởng P(B | A₁) = 0.636, P(B | A₂) = 0.444, P(B | A₃) = 0.7. Xác suất sản phẩm là phế phẩm là', tot(pr5, lk5), f'{{A₁, A₂, A₃}} là hệ đầy đủ ⇒ P(B) = 0.45·0.636 + 0.25·0.444 + 0.3·0.7 = 0.2862 + 0.111 + 0.21 = {f(tot(pr5,lk5),4)} ≈ 0.607.', 2, TOP['total'], K, extra=[(0.636 + 0.444 + 0.7) / 3, 0.7, 0.636], d=3)
    for i in range(3):
        P(B, rng, f'Cùng đề (P(A) = 0.45, 0.25, 0.3; P(B | A) = 0.636, 0.444, 0.7): biết sản phẩm là phế phẩm, xác suất nó thuộc phân xưởng {i+1} là', post(pr5, lk5, i), f'P(A{i+1} | B) = {pr5[i]}·{lk5[i]}/{f(tot(pr5,lk5),4)} = {f(post(pr5,lk5,i),4)}.' + (' (Đáp án chính thức câu 1.2: 0.183.)' if i == 1 else ''), 2, TOP['bayes'], K + (' – câu (2)' if i == 1 else ' (mở rộng)'), extra=[pr5[i], lk5[i], pr5[i] * lk5[i]], d=3)
    # lý thuyết
    S2 = 'Lecture Notes §1.6'
    B.mcq('Các biến cố A₁, …, Aₙ tạo thành một HỆ ĐẦY ĐỦ khi:', 'Xung khắc từng đôi và hợp của chúng bằng S', ['Độc lập từng đôi', 'Có xác suất bằng nhau', 'Mỗi biến cố có xác suất 1/n'], 'Định nghĩa 1.6: (i) Aᵢ ∩ Aⱼ = ∅ với i ≠ j và (ii) A₁ ∪ … ∪ Aₙ = S. {A, Aᶜ} luôn là hệ đầy đủ.', 1, TOP['system'], S2 + ' (Định nghĩa 1.6)')
    B.mcq('Công thức xác suất toàn phần với hệ đầy đủ {A₁, …, Aₙ} là:', 'P(B) = Σ P(B | Aᵢ)·P(Aᵢ)', ['P(B) = Σ P(Aᵢ | B)', 'P(B) = Π P(B | Aᵢ)', 'P(B) = Σ P(Aᵢ)'], 'P(B) = Σ P(B ∩ Aᵢ) = Σ P(B | Aᵢ)P(Aᵢ) (Định lý 1.5).', 1, TOP['total'], S2 + ' (Định lý 1.5)')
    B.mcq('Công thức Bayes cho P(Aᵢ | B) là:', 'P(B | Aᵢ)P(Aᵢ) / Σⱼ P(B | Aⱼ)P(Aⱼ)', ['P(B | Aᵢ)/Σⱼ P(B | Aⱼ)', 'P(Aᵢ)·P(B)', 'P(B | Aᵢ) + P(Aᵢ)'], 'Tử số là P(B ∩ Aᵢ), mẫu số là P(B) theo công thức toàn phần (Định lý 1.6).', 1, TOP['bayes'], S2 + ' (Định lý 1.6)')
    B.mcq('Trong công thức Bayes, P(Aᵢ) được gọi là ... còn P(Aᵢ | B) được gọi là ...', 'Xác suất tiên nghiệm; xác suất hậu nghiệm (hậu kiểm)', ['Xác suất hậu nghiệm; xác suất tiên nghiệm', 'Xác suất biên; xác suất đồng thời', 'Xác suất toàn phần; xác suất nhân'], 'Nhận xét 1.3: trước khi quan sát B là tiên nghiệm; sau khi quan sát B là hậu kiểm.', 1, TOP['bayes'], S2 + ' (Nhận xét 1.3)')
    B.mcq('Tổng các xác suất hậu nghiệm Σᵢ P(Aᵢ | B) trên một hệ đầy đủ luôn bằng:', '1', ['Tùy thuộc B', 'Σ P(Aᵢ)·P(B)', '0'], 'Sau khi biết B xảy ra, B chắc chắn thuộc đúng một Aᵢ (hệ đầy đủ) nên xác suất hậu nghiệm cộng lại bằng 1.', 2, TOP['bayes'], S2 + ' (kiểm tra Bayes)')
    B.essay('Bài 1.23 (Lecture Notes): pít-tông ba phân xưởng (40%, 35%, 25%; phế phẩm 5%, 8%, 4%). (a) P(phế phẩm); (b) biết phế phẩm, P(do phân xưởng II).', f'(a) P(B) = 0.4·0.05 + 0.35·0.08 + 0.25·0.04 = 0.058. (b) P(A₂ | B) = 0.35·0.08/0.058 = {f(post(pr4,lk4,1),4)}. Các hậu nghiệm: I {f(post(pr4,lk4,0),4)}, II {f(post(pr4,lk4,1),4)}, III {f(post(pr4,lk4,2),4)} (tổng 1).', 2, TOP['bayes'], S + 'Bài 1.23')
    B.essay('Bài 1.22 (Lecture Notes): phòng khám 83% có bệnh; chẩn đoán đúng 90% nếu có bệnh, 80% nếu không bệnh. Tính P(đúng) và P(có bệnh | chẩn đoán đúng).', f'(a) 0.83·0.9 + 0.17·0.8 = {f(pd,3)}. (b) 0.747/{f(pd,3)} = {f(0.83*0.9/pd,4)}.', 2, TOP['bayes'], S + 'Bài 1.22')
    B.essay('Bài 1.21 (Lecture Notes): hai hộp áo, chuyển 1 áo từ hộp I sang hộp II rồi lấy 2 áo từ hộp II; xác suất cả hai áo đều lỗi.', f'Phân hoạch theo áo chuyển (lỗi/tốt): P = (1/10)(3/9)(2/8) + (9/10)(2/9)(1/8) = {f(pb21,5)}.', 3, TOP['tree'], S + 'Bài 1.21')
    B.essay('Ví dụ 1.21 (Lecture Notes): mạch hai bộ phận nối tiếp (0.95; 0.98) ngừng làm việc. Tìm xác suất chỉ bộ phận hai hỏng; xác suất bộ phận một hỏng.', 'P(A₂ | ngừng) = 0.019/0.069 = 19/69 ≈ 0.2754; P(A₃ | ngừng) = 0.049/0.069 = 49/69 ≈ 0.7101; P(cả hai hỏng | ngừng) = 1/69.', 2, TOP['bayes'], S + 'Ví dụ 1.21')
