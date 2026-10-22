"""Module 7 — phần chuyên sâu (số liệu tính bằng code khi dựng trang)."""
import math
from hx import *
from pskit import mean, var_s, var_p, sd_s
from qb import fg, f
K = 'MODULE 7 · '
def L(x): return ', '.join(fg(v, 3) for v in x)
def parts():
    P = []
    # ───────── A. Phân phối mẫu ─────────
    s = []
    s.append(sl(formula('Phân phối của trung bình mẫu', 'E(\\bar X)=\\mu,\\qquad \\operatorname{Var}(\\bar X)=\\dfrac{\\sigma^2}{n},\\qquad \\sigma_{\\bar X}=\\dfrac{\\sigma}{\\sqrt n}\\ \\text{(sai số chuẩn)}')
                + ul(['Mẫu từ tổng thể chuẩn: X̄ ~ N(μ, σ²/n) chính xác.', 'Mẫu lớn (n ≥ 30) từ tổng thể bất kỳ: X̄ ≈ N(μ, σ²/n) (định lý giới hạn trung tâm).', 'Nhân bốn cỡ mẫu ⇒ sai số chuẩn giảm một nửa.']),
                K + 'PHẦN 1 · Chuyên sâu', 'Trung bình mẫu có phân phối chuẩn', explain='Mỗi lần lấy mẫu cho một x̄ khác nhau; x̄ dao động quanh μ với độ rộng σ/√n — mẫu càng lớn càng chính xác.'))
    s.append(sl(callout('info', 'Ví dụ A1 · Sai số chuẩn', 'Thời gian chạy một tác vụ có σ = 12 giây. Lấy mẫu n = 36. P(x̄ lệch khỏi μ không quá 3 giây)?')
                + steps([m('\\sigma_{\\bar X}=12/\\sqrt{36}=2'), m('P(|\\bar X-\\mu|<3)=P(|Z|<1.5)=2\\Phi(1.5)-1=0.8664')]) + '<p>Cỡ mẫu n = 144 cho sai số chuẩn 1 và xác suất 0.9973.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Xác suất lệch của x̄'))
    s.append(sl(callout('info', 'Ví dụ A2 · Chọn cỡ mẫu', 'σ = 10. Cần P(|x̄ − μ| < 2) ≥ 0.95. Tìm n nhỏ nhất.')
                + steps([m('2=1.96\\cdot10/\\sqrt n\\Rightarrow\\sqrt n=9.8\\Rightarrow n=96.04'), m('n_{\\min}=97')]) + '<p>Luôn làm tròn LÊN để đảm bảo độ chính xác.</p>', K + 'PHẦN 1 · Chuyên sâu', 'Cỡ mẫu cần thiết'))
    P.append(dict(title='Chuyên sâu: phân phối mẫu', bullets=['Sai số chuẩn', 'Giới hạn trung tâm', 'Chọn cỡ mẫu'], slides=s))
    # ───────── B. Ước lượng điểm ─────────
    s = []
    x = [4.2, 5.1, 3.8, 4.9, 5.4, 4.4, 4.7, 5.0]
    n = len(x)
    s.append(sl(callout('info', 'Ví dụ B1 · Hai ước lượng của σ²', 'Mẫu n = 8: ' + L(x) + '.')
                + steps(['x̄ = ' + f(mean(x), 4), 'Σ(xᵢ − x̄)² = ' + f(var_s(x) * (n - 1), 4), 's² = Σ/(n − 1) = ' + f(var_s(x), 4) + ' (không chệch)', 'σ̂² = Σ/n = ' + f(var_p(x), 4) + ' (MLE của chuẩn, chệch thấp: E = (n−1)σ²/n)'])
                + '<p>Với n nhỏ hai giá trị khác biệt rõ; n lớn thì gần nhau.</p>', K + 'PHẦN 2 · Chuyên sâu', 'Chia n hay n − 1?'))
    s.append(sl(table(['Tính chất', 'Ý nghĩa', 'Ví dụ'], [['Không chệch', 'E(θ̂) = θ', 'X̄ cho μ; S² cho σ²'], ['Chệch', 'E(θ̂) ≠ θ', 'σ̂² = Σ(Xᵢ − X̄)²/n: E = (n−1)σ²/n'], ['Vững', 'θ̂ → θ khi n → ∞', 'X̄, S², p̂'], ['Hiệu quả', 'phương sai nhỏ nhất trong các ước lượng không chệch', 'X̄ với mẫu chuẩn']])
                + callout('good', 'Sai số bình phương trung bình', 'MSE(θ̂) = Var(θ̂) + [Bias(θ̂)]². Ước lượng chệch nhẹ nhưng phương sai nhỏ có thể có MSE nhỏ hơn.'), K + 'PHẦN 2 · Chuyên sâu', 'Bốn tiêu chuẩn của ước lượng điểm'))
    s.append(sl(callout('info', 'Ví dụ B2 · Chứng minh X̄ không chệch', 'Chứng minh E(X̄) = μ và Var(X̄) = σ²/n.')
                + steps([m('E(\\bar X)=\\tfrac1n\\sum E(X_i)=\\tfrac1n\\cdot n\\mu=\\mu'), m('\\operatorname{Var}(\\bar X)=\\tfrac1{n^2}\\sum\\operatorname{Var}(X_i)=\\tfrac{n\\sigma^2}{n^2}=\\tfrac{\\sigma^2}n\\ (\\text{độc lập})')]), K + 'PHẦN 2 · Chuyên sâu', 'Chứng minh tính không chệch'))
    P.append(dict(title='Chuyên sâu: ước lượng điểm', bullets=['n hay n − 1', 'Bốn tiêu chuẩn', 'Chứng minh'], slides=s))
    # ───────── C. MLE ─────────
    s = []
    s.append(sl(callout('info', 'Quy trình MLE', '1) Viết hàm hợp lý L(θ) = Πf(xᵢ; θ). 2) Lấy logarit: ℓ = ln L. 3) Giải dℓ/dθ = 0. 4) Kiểm tra cực đại (đạo hàm bậc hai âm).')
                + callout('good', 'Mẹo', 'Logarit biến tích thành tổng nên dễ đạo hàm; cực đại của L và ℓ cùng điểm vì ln đơn điệu tăng.'), K + 'PHẦN 3 · Chuyên sâu', 'Bốn bước tìm MLE'))
    s.append(sl(callout('info', 'Ví dụ C1 · MLE của p (Bernoulli/nhị thức)', 'Tung đồng xu n lần được k sấp. Tìm p̂.')
                + steps([m('L(p)=p^k(1-p)^{n-k}\\Rightarrow\\ell=k\\ln p+(n-k)\\ln(1-p)'), m('\\ell\'=\\tfrac kp-\\tfrac{n-k}{1-p}=0\\Rightarrow\\hat p=\\tfrac kn')]) + '<p>Ví dụ: 100 lần, 58 sấp: p̂ = 0.58.</p>', K + 'PHẦN 3 · Chuyên sâu', 'MLE của tỷ lệ'))
    xs = [2, 0, 3, 1, 4, 2, 1, 3]
    s.append(sl(callout('info', 'Ví dụ C2 · MLE của λ (Poisson)', 'Số cuộc gọi mỗi phút trong 8 phút: ' + L(xs) + '.')
                + steps([m('\\ell=\\sum(x_i\\ln\\lambda-\\lambda-\\ln x_i!)\\Rightarrow\\ell\'=\\tfrac{\\sum x_i}\\lambda-n=0\\Rightarrow\\hat\\lambda=\\bar x'), m(f'\\hat\\lambda=\\tfrac{{{sum(xs)}}}{{{len(xs)}}}={sum(xs)/len(xs):.3f}')]), K + 'PHẦN 3 · Chuyên sâu', 'MLE của Poisson'))
    te = [12.5, 8.1, 20.3, 15.0, 6.9, 9.2]
    s.append(sl(callout('info', 'Ví dụ C3 · MLE của λ (mũ)', 'Tuổi thọ (giờ) của 6 linh kiện: ' + L(te) + '. Mật độ f(t) = λe^(−λt).')
                + steps([m('\\ell=n\\ln\\lambda-\\lambda\\sum t_i\\Rightarrow\\ell\'=\\tfrac n\\lambda-\\sum t_i=0\\Rightarrow\\hat\\lambda=\\tfrac1{\\bar t}'), m(f'\\bar t={mean(te):.4f},\\ \\hat\\lambda={1/mean(te):.5f}\\ \\text{{(1/giờ)}}'), m(f'\\text{{Tuổi thọ kỳ vọng ước lượng }}=\\bar t={mean(te):.3f}\\text{{ giờ}}')]), K + 'PHẦN 3 · Chuyên sâu', 'MLE của phân phối mũ'))
    s.append(sl(callout('info', 'Ví dụ C4 · MLE của μ, σ² (chuẩn)', 'Mẫu n quan sát chuẩn.')
                + steps([m('\\hat\\mu=\\bar x'), m('\\hat\\sigma^2=\\tfrac1n\\sum(x_i-\\bar x)^2\\ (\\text{chia }n,\\ \\text{chệch})'), m('\\text{Dùng }s^2=\\tfrac1{n-1}\\sum(x_i-\\bar x)^2\\text{ nếu cần không chệch}')]), K + 'PHẦN 3 · Chuyên sâu', 'MLE của chuẩn'))
    s.append(sl(callout('info', 'Ví dụ C5 · MLE không đạo hàm: phân phối đều U[0, θ]', 'Mẫu 3.1, 7.4, 5.0, 6.2. Tìm θ̂.')
                + steps([m('L(\\theta)=\\theta^{-n}\\ \\text{khi }\\theta\\ge\\max x_i,\\ 0\\text{ ngược lại}'), m('L\\text{ giảm theo }\\theta\\Rightarrow\\text{cực đại tại }\\hat\\theta=\\max x_i=7.4')]) + '<p>Ước lượng này chệch thấp (E = nθ/(n+1)) nên người ta dùng (n+1)/n·max.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Khi đạo hàm không giải được'))
    s.append(sl(callout('info', 'Ví dụ C6 · Tính bất biến của MLE', 'Mũ có λ̂ = 0.0833. Ước lượng xác suất linh kiện sống quá 20 giờ?')
                + steps([m('P(T>20)=e^{-20\\lambda}\\Rightarrow\\widehat{P}=e^{-20\\cdot0.0833}=0.1890')]) + '<p>MLE của hàm g(θ) là g(θ̂): thay trực tiếp MLE vào công thức.</p>', K + 'PHẦN 3 · Chuyên sâu', 'Bất biến hàm'))
    P.append(dict(title='Chuyên sâu: hợp lý cực đại', bullets=['Quy trình', 'Bernoulli, Poisson, mũ', 'Chuẩn, đều', 'Bất biến'], slides=s))
    return P
