"""Module 1 — mở rộng: khái niệm + họ bài tính (đáp án tự tính, nhãn bo_sung)."""
import math, random
from pskit import *
from qb import f, fg, nd
from orig_m01 import TOPIC, nums_text
SRC = 'Bổ sung: dạng bài §1.1 / Kreyszig PS 24.1 (đáp án tự tính, đối chiếu numpy)'
def build(B):
    rng = random.Random(2501)
    def C(stem, ok, bad, expl, lvl=1, topic='theory'):
        B.mcq(stem, ok, bad, expl, lvl, TOPIC[topic], SRC, 'bo_sung')
    C('Dữ liệu nào là định tính theo thang thứ bậc?', 'Xếp loại học lực: giỏi, khá, trung bình', ['Chiều cao (cm)', 'Số lỗi in trên trang', 'Nhóm máu'], 'Có thứ tự nhưng khoảng cách giữa các bậc không đo được.', 1, 'theory')
    C('Đại lượng nào KHÔNG nên tính trung bình số học?', 'Nhóm máu mã hóa 1, 2, 3, 4', ['Điểm kiểm tra', 'Thời gian chạy chương trình', 'Số lỗi mỗi trang'], 'Dữ liệu danh nghĩa: các số chỉ là nhãn.', 1, 'theory')
    C('Tổng các độ lệch Σ(xᵢ − x̄) luôn bằng', '0', ['n', 's²', '1'], 'Tính chất của trung bình: tâm cân bằng của dữ liệu.', 1, 'mean')
    C('Phương sai mẫu s² chia cho n − 1 vì', 'đã dùng dữ liệu để ước lượng x̄ (mất một bậc tự do), cho ước lượng không chệch', ['để s² luôn lớn hơn σ²', 'để s² luôn nguyên', 'vì n − 1 dễ tính hơn'], 'Chia n − 1 làm E(s²) = σ².', 2, 'spread')
    C('Nếu cộng 10 vào mọi giá trị của mẫu thì', 'x̄ tăng 10, s không đổi', ['x̄ không đổi, s tăng 10', 'cả x̄ và s tăng 10', 'x̄ tăng 10, s tăng 100'], 'Dịch chuyển không đổi độ phân tán.', 1, 'spread')
    C('Nếu nhân mọi giá trị của mẫu với 3 thì phương sai', 'nhân với 9', ['nhân với 3', 'không đổi', 'cộng thêm 3'], 's² nhân a² còn s nhân |a|.', 1, 'spread')
    C('Dữ liệu lệch phải mạnh, nên dùng đại lượng nào để đo vị trí trung tâm?', 'Trung vị', ['Trung bình', 'Khoảng biến thiên', 'Tổng các giá trị'], 'Trung vị không bị đuôi dài kéo lệch.', 2, 'mean')
    C('Nếu trung bình lớn hơn trung vị rõ rệt, phân phối thường', 'lệch phải', ['lệch trái', 'đối xứng', 'đều'], 'Đuôi phải kéo trung bình lên.', 2, 'mean')
    C('Boxplot cho thấy trực tiếp', 'min, qL, trung vị, qU, max và ngoại lai', ['trung bình và độ lệch chuẩn', 'tần số từng giá trị', 'phương sai'], 'Năm số tóm tắt + ngoại lai.', 1, 'quart')
    C('Giá trị x bị coi là ngoại lai (tiêu chuẩn giáo trình) nếu', 'x < qL − 1.5·IQR hoặc x > qU + 1.5·IQR', ['x > x̄ + s', 'x > qU', 'x < x̄ − 3'], 'Hàng rào Tukey 1.5·IQR.', 1, 'quart')
    C('IQR bằng', 'qU − qL', ['max − min', 'qM − qL', 'qU + qL'], 'Khoảng tứ phân vị: độ rộng của 50% dữ liệu giữa.', 1, 'quart')
    C('Hệ số biến thiên CV dùng để', 'so sánh độ phân tán tương đối giữa các đại lượng khác đơn vị', ['tính trung bình', 'tìm ngoại lai', 'xác định mốt'], 'CV = s/x̄ không có đơn vị.', 2, 'spread')
    C('Điểm chuẩn hóa z = (x − x̄)/s cho biết', 'x cách x̄ bao nhiêu độ lệch chuẩn', ['x lớn hơn x̄ bao nhiêu đơn vị', 'tỉ lệ phần trăm của x', 'phương sai của x'], 'z là số độ lệch chuẩn so với trung bình.', 1, 'spread')
    C('Quy tắc 68–95–99.7 áp dụng cho', 'dữ liệu có phân phối hình chuông', ['mọi dữ liệu', 'chỉ dữ liệu rời rạc', 'chỉ dữ liệu lệch'], 'Với dữ liệu bất kỳ chỉ có Chebyshev.', 1, 'theory')
    C('Histogram có độ rộng lớp bằng nhau thì chiều cao cột tỉ lệ với', 'tần số của lớp', ['tần số tích lũy', 'trung điểm lớp', 'số lớp'], 'Cùng độ rộng nên diện tích tỉ lệ với chiều cao.', 1, 'repr')
    C('Biểu đồ thân–lá khác histogram ở chỗ', 'giữ lại giá trị từng quan sát', ['chỉ hiển thị trung bình', 'không dùng được cho dữ liệu số', 'luôn có 5 lớp'], 'Lá là chữ số cuối của từng quan sát.', 1, 'repr')
    C('Số lớp gợi ý theo Sturges cho n = 100 là khoảng', '8', ['3', '20', '100'], '1 + 3.3·log₁₀100 = 7.6 ≈ 8.', 2, 'repr')
    C('Tần suất tương đối của lớp có 12 quan sát trong mẫu 40 là', '0.30', ['0.12', '3.33', '0.40'], '12/40 = 0.30.', 1, 'repr')
    C('Nếu thêm một giá trị đúng bằng x̄ vào mẫu thì x̄', 'không đổi', ['tăng', 'giảm', 'bằng 0'], 'Thêm đúng giá trị trung bình không làm đổi trung bình.', 2, 'mean')
    # z-score
    for k in range(8):
        mu = rng.choice([50, 70, 100, 12, 170]); s = rng.choice([4, 5, 8, 10, 15]); x = mu + rng.choice([-2, -1.5, 1, 1.5, 2, 2.5]) * s
        z = (x - mu) / s
        B.mcq(f'Mẫu có x̄ = {mu}, s = {s}. Điểm chuẩn hóa z của giá trị x = {fg(x,3)} là', fg(z, 3), [fg(-z, 3), fg(x - mu, 3), fg((x - mu) / s ** 2, 3), fg(z + 1, 3)],
              f'z = (x − x̄)/s = ({fg(x,3)} − {mu})/{s} = {fg(z,3)}.', 1, TOPIC['spread'], SRC, 'bo_sung')
    # CV
    for k in range(6):
        xb = rng.choice([20, 40, 50, 80, 120]); s = rng.choice([2, 3, 4, 6, 10]); cv = s / xb * 100
        B.mcq(f'Mẫu có x̄ = {xb}, s = {s}. Hệ số biến thiên CV (%) bằng', f(cv, 1), [f(xb / s, 1), f(s / xb, 3), f(cv * 2, 1), f(s, 1)],
              f'CV = s/x̄·100% = {s}/{xb}·100% = {f(cv,1)}%.', 2, TOPIC['spread'], SRC, 'bo_sung')
    # trung bình chung của hai nhóm
    for k in range(8):
        n1, n2 = rng.choice([10, 15, 20, 30]), rng.choice([10, 20, 25, 40]); m1, m2 = rng.randint(50, 80), rng.randint(50, 80)
        if m1 == m2: m2 += 3
        mt = (n1 * m1 + n2 * m2) / (n1 + n2)
        B.mcq(f'Nhóm A có {n1} người, điểm trung bình {m1}; nhóm B có {n2} người, điểm trung bình {m2}. Trung bình chung của cả hai nhóm là', f(mt, 3), nd(mt, rng, 3, extra=[(m1 + m2) / 2, (n1 * m1 + n2 * m2) / (n1 + n2 + 1)]),
              f'Trung bình có trọng số: ({n1}·{m1} + {n2}·{m2})/({n1}+{n2}) = {f(mt,3)} (không phải trung bình cộng đơn giản {f((m1+m2)/2,3)}).', 2, TOPIC['mean'], SRC, 'bo_sung')
    # thêm giá trị mới
    for k in range(8):
        n = rng.randint(6, 12); x = [rng.randint(10, 40) for _ in range(n)]; new = rng.choice([5, 60, 80, 100])
        m0 = mean(x); m1 = (sum(x) + new) / (n + 1)
        B.mcq(f'Mẫu {nums_text(x)} (n = {n}). Thêm giá trị {new}. Trung bình mới bằng', f(m1, 3), nd(m1, rng, 3, extra=[m0, (m0 + new) / 2, sum(x) / (n + 1)]),
              f'Tổng mới = {sum(x)} + {new} = {sum(x)+new}; chia cho {n+1}: {f(m1,3)} (trung bình cũ {f(m0,3)}).', 2, TOPIC['mean'], SRC, 'bo_sung')
    # công thức nhanh của s²
    for k in range(6):
        n = rng.randint(5, 9); x = [rng.randint(2, 15) for _ in range(n)]; sx = sum(x); sx2 = sum(v * v for v in x)
        v = (sx2 - sx * sx / n) / (n - 1)
        B.mcq(f'Một mẫu có n = {n}, Σxᵢ = {sx}, Σxᵢ² = {sx2}. Phương sai mẫu s² bằng', f(v, 3), nd(v, rng, 3, extra=[(sx2 - sx * sx / n) / n, sx2 / (n - 1), sx2 / n - (sx / n) ** 2 + 1]),
              f's² = (Σx² − (Σx)²/n)/(n − 1) = ({sx2} − {f(sx*sx/n,3)})/{n-1} = {f(v,3)}.', 2, TOPIC['spread'], SRC, 'bo_sung')
    # tần suất tương đối
    for k in range(6):
        cnt = [rng.randint(2, 15) for _ in range(5)]; N = sum(cnt); i = rng.randrange(5)
        B.mcq(f'Một mẫu {N} quan sát chia 5 lớp có tần số {", ".join(map(str,cnt))}. Tần suất tương đối của lớp thứ {i+1} là', f(cnt[i] / N, 3), nd(cnt[i] / N, rng, 3, extra=[cnt[i], cnt[i] / (N - cnt[i]), 1 / 5], lo=0.0),
              f'{cnt[i]}/{N} = {f(cnt[i]/N,3)}.', 1, TOPIC['repr'], SRC, 'bo_sung')
    B.essay('Dữ liệu (giây): 12, 15, 14, 10, 18, 20, 16, 13, 17. Tính x̄, s, qL, qM, qU, IQR và xác định ngoại lai.', 'x̄ = 15; Σ(x − x̄)² = 78 ⇒ s² = 9.75, s = 3.122; sắp xếp 10 12 13 14 15 16 17 18 20; qM = 15, qL = (12+13)/2 = 12.5, qU = (17+18)/2 = 17.5, IQR = 5; ngưỡng [5, 25] ⇒ không có ngoại lai.', 2, TOPIC['quart'], SRC, 'bo_sung')
    B.essay('Lớp 1 có x̄ = 72, s = 8; lớp 2 có x̄ = 60, s = 5. Bạn A (lớp 1) 80 điểm, bạn B (lớp 2) 70 điểm. Ai học tốt hơn so với lớp mình? So sánh CV của hai lớp.', 'z_A = (80 − 72)/8 = 1.0; z_B = (70 − 60)/5 = 2.0 ⇒ B tốt hơn so với lớp mình. CV₁ = 11.1%, CV₂ = 8.3% ⇒ lớp 1 phân tán tương đối hơn.', 2, TOPIC['spread'], SRC, 'bo_sung')
    B.essay('Mẫu gồm các giá trị 4, 5, 5, 6, 6, 7, 7, 8, 38. (a) Tính x̄ và trung vị. (b) Bỏ giá trị 38, tính lại. (c) Nhận xét.', '(a) x̄ = 86/9 = 9.556; trung vị = 6. (b) x̄ = 6.0; trung vị = 6. (c) Một ngoại lai kéo x̄ lên thêm 3.56 đơn vị còn trung vị không đổi: dữ liệu lệch nên dùng trung vị.', 2, TOPIC['mean'], SRC, 'bo_sung')
