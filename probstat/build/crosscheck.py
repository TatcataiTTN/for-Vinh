"""Đối chiếu kết quả tự tính với ĐÁP ÁN CHÍNH THỨC có trong tài liệu (đáp án HK2 2022–2023, 2021–2022, giữa kỳ HK2). Trả về danh sách dòng và kiểm tra dung sai."""
import math
from scipy import stats as st
from orig_m08 import gstats
from orig_m13 import mine
Phi = st.norm.cdf; PhiI = st.norm.ppf
def rows():
    R = []
    def add(src, item, off, mine_, tol):
        R.append((src, item, off, mine_, abs(off - mine_) <= tol))
    S1 = 'HK2 2022–2023, đề số 1'
    add(S1, 'Câu 1a: Φ((13.7135 − 12.5)/0.809)', 0.9332, round(Phi((13.7135 - 12.5) / 0.809), 4), 6e-4)
    add(S1, 'Câu 1b: c = 12.5 + z₀.₉₉·0.809', 14.382, 12.5 + PhiI(0.99) * 0.809, 2e-3)
    N, m, v = gstats(70, 15, [2, 4, 7, 8, 4, 2]); k = 1.96 * 16 / math.sqrt(N)
    add(S1, 'Câu 2: cận dưới khoảng tin cậy', 109.243, m - k, 2e-3); add(S1, 'Câu 2: cận trên khoảng tin cậy', 121.313, m + k, 2e-3)
    N, m, v = gstats(5.0, 0.4, [2, 4, 7, 8, 4, 2]); tq = (m - 5.75) / (math.sqrt(v) / math.sqrt(N))
    add(S1, 'Câu 3: trung bình mẫu z̄', 6.207, m, 1e-3); add(S1, 'Câu 3: phương sai mẫu s² (đáp án chính thức làm tròn x̄ trước khi bình phương: chênh ≈ 2%)', 0.293, v, 8e-3); add(S1, 'Câu 3: giá trị quan sát T_qs (cùng lý do làm tròn trung gian; kết luận không đổi)', 4.389, tq, 0.06)
    k1, k0, r = mine([1.55, 6.55, 11.55, 16.55, 21.55], [13.03, 17.08, 21.03, 25.10, 29.08]); add(S1, 'Câu 4: hệ số k₁', 0.802, k1, 1e-3)
    S2 = 'Đề 22/12/2021 (3TC), đề số 1 (a = 9, b = 2)'
    add(S2, 'Câu 1a: m = Φ(3.0)', 0.9987, round(Phi(3.0), 4), 1e-4); add(S2, 'Câu 1b: k = z₀.₈₄·σ − b', -1.702, PhiI(0.84) * 0.3 - 2, 3e-3)
    N, m, v = gstats(170, 2, [3, 5, 17, 7, 2]); k = st.t.ppf(0.975, N - 1) * math.sqrt(v) / math.sqrt(N)
    add(S2, 'Câu 2: cận dưới khoảng tin cậy (t làm tròn 2.03)', 174.315, m - 2.03 * math.sqrt(v) / math.sqrt(N), 2e-3); add(S2, 'Câu 2: cận trên khoảng tin cậy', 175.685, m + 2.03 * math.sqrt(v) / math.sqrt(N), 2e-3)
    xs = [3080, 3100, 3159, 3182, 3200]; add(S2, 'Câu 3: T_qs', -1.29692, (sum(xs) / 5 - 3150) / (10 / math.sqrt(5)), 1e-4)
    k1, k0, r = mine([1.5, 2.5, 3.5, 4.5, 14], [8.31, 12.29, 16.32, 20.28, 58.3]); add(S2, 'Câu 4: k₁', 4.0, k1, 1e-3); add(S2, 'Câu 4: y(3)', 14.3, k0 + 3 * k1, 2e-3)
    xs5 = [1.5, 11.5, 5.5, 4, 5, 6]; add(S2, 'Câu 5: θ̂ = 1/(2(x̄ − 1))', 0.109, 1 / (2 * (sum(xs5) / 6 - 1)), 1e-3)
    S3 = 'Giữa kỳ HK2 2022–2023 (a=3, b=2, c=2)'
    pr, lk = [0.45, 0.25, 0.30], [0.636, 0.444, 0.7]; PB = sum(a * b for a, b in zip(pr, lk))
    add(S3, 'Câu 1: P(B)', 0.607, PB, 1e-3); add(S3, 'Câu 1: P(A₂|B)', 0.183, pr[1] * lk[1] / PB, 1e-3)
    pT = [0.28, 0.1332, 0.3648, 0.222]; mu = sum(i * p for i, p in enumerate(pT)); var = sum((i - mu) ** 2 * p for i, p in enumerate(pT))
    add(S3, 'Câu 2: E(T)', 1.5288, mu, 1e-4); add(S3, 'Câu 2: σ²', 1.25317, var, 1e-4)
    p = Phi(1) - Phi(0); add(S3, 'Câu 3: Φ(1) − Φ(0)', 0.3413, p, 1e-4); add(S3, 'Câu 3: P(đúng 2 trong 6)', 0.328938, 15 * 0.3413 ** 2 * (1 - 0.3413) ** 4, 5e-4)
    return R
if __name__ == '__main__':
    for r in rows(): print(r)
    assert all(r[4] for r in rows())
