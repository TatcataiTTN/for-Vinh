"""Ngân hàng 'tra bảng': đáp án = giá trị ĐỌC TỪ BẢNG (đúng như in), kèm vị trí ô để tô sáng; câu nội suy dùng giá trị chính xác với sai số cho phép."""
import random, math
from scipy import stats as st
import tables as T

def f2(x, d=4): return f'{x:.{d}f}'.replace('-', '−')
def a7t(z):                      # Φ(z) theo bảng A7 (z có 2 chữ số thập phân)
    z = round(z, 2)
    if z == 0: return 0.5
    a = abs(z)
    v = 1.0 if a > 3.0 else float(T.a7_val(a))
    return round(v if z > 0 else 1 - v, 4)
def a8p(P):
    k = f'{P:g}'; return T.data()['A8'][k]
D = T.data()
def a9t(F, df): return float(D['A9']['v'][T.A9_F.index(F)][T.A9_DF.index(df)])
def a10t(F, df): return float(D['A10']['v'][T.A10_F.index(F)][T.A10_DF.index(df)])
DFS9 = [d for d in T.A9_DF if d is not None]

def build():
    rng = random.Random(20261111); Q = []
    def add(t, q, a, tol, hint, ex, loc): Q.append(dict(t=t, q=q, a=round(a, 6), tol=tol, hint=hint, ex=ex, loc=loc))
    # ---- A7
    for z in rng.sample([round(i / 100, 2) for i in range(1, 301)], 30):
        v = a7t(z); add('a7', f'Tra bảng A7: Φ({z:.2f}) bằng bao nhiêu?', v, 0.00006, f'Hàng z = {z:.2f}, cột Φ(z) ngay bên phải; đọc 4 chữ số rồi thêm “0.” phía trước.', f'Φ({z:.2f}) = {v:.4f} (bảng in {int(round(v*10000)):04d}, hiểu là 0.{int(round(v*10000)):04d}).', [['a7', f'{z:.2f}']])
    for z in rng.sample([round(i / 100, 2) for i in range(5, 300)], 20):
        p = a7t(z); v = round(1 - p, 4)
        add('a7', f'Tra bảng A7: Φ(−{z:.2f}) bằng bao nhiêu?', v, 0.00006, 'Bảng chỉ có z dương: dùng Φ(−z) = 1 − Φ(z).', f'Φ({z:.2f}) = {p:.4f} nên Φ(−{z:.2f}) = 1 − {p:.4f} = {v:.4f}.', [['a7', f'{z:.2f}']])
    for _ in range(20):
        a = round(rng.uniform(-2.5, 1.0), 2); b = round(a + rng.uniform(0.5, 2.5), 2); b = min(b, 3.0)
        v = round(a7t(b) - a7t(a), 4)
        add('a7', f'Cho Z ~ N(0, 1). Tính P({a:.2f} < Z < {b:.2f}) bằng bảng A7.'.replace('-', '−'), v, 0.00015, 'P(a < Z < b) = Φ(b) − Φ(a); a âm thì Φ(a) = 1 − Φ(|a|).', f'Φ({b:.2f}) = {a7t(b):.4f}; Φ({a:.2f}) = {a7t(a):.4f}; hiệu = {v:.4f}.'.replace('-', '−'), [['a7', f'{abs(a):.2f}'], ['a7', f'{b:.2f}']])
    for _ in range(20):
        mu = rng.choice([50, 100, 12, 8.5, 70]); sg = rng.choice([2, 5, 10, 15, 0.5]); lo = mu + rng.choice([-1.5, -1, -0.5, 0.3]) * sg; hi = lo + rng.choice([0.8, 1.2, 1.7, 2.1]) * sg
        lo, hi = round(lo, 2), round(hi, 2); z1 = round((lo - mu) / sg, 2); z2 = round((hi - mu) / sg, 2)
        v = round(a7t(z2) - a7t(z1), 4)
        add('a7', f'X ~ N({mu:g}; {sg:g}²). Tính P({lo:g} < X < {hi:g}) (chuẩn hóa, làm tròn z đến 2 chữ số thập phân rồi tra A7).', v, 0.0004, 'Đổi z = (x − μ)/σ cho hai đầu mút, làm tròn 2 chữ số, rồi lấy Φ(z₂) − Φ(z₁).',
            f'z₁ = ({lo:g} − {mu:g})/{sg:g} = {z1:.2f}; z₂ = ({hi:g} − {mu:g})/{sg:g} = {z2:.2f}; Φ(z₂) − Φ(z₁) = {a7t(z2):.4f} − {a7t(z1):.4f} = {v:.4f}.'.replace('-', '−'), [['a7', f'{abs(z1):.2f}'], ['a7', f'{abs(z2):.2f}']])
    # ---- A8
    for al in rng.sample(list(range(1, 50)), 25):
        P = 100 - al; z = float(a8p(P)[0]); add('a8', f'Tra bảng A8: giá trị tới hạn U_α với α = {al}% (Φ(U_α) = 1 − α).', z, 0.0006, f'Φ(U_α) = {P}% nên vào hàng {P}%, đọc cột z(Φ).', f'Hàng {P}%: z(Φ) = {z:.3f}. Vậy U_{{{al}%}} = {z:.3f}.', [['a8', f'{P}']])
    for P in rng.sample(list(range(1, 100)), 20):
        z = float(a8p(P)[0]); add('a8', f'Tìm z sao cho Φ(z) = {P}% (bảng A8, cột z(Φ)).', z, 0.0006, f'Vào hàng {P}%, cột z(Φ); chú ý P < 50% thì z âm.', f'Hàng {P}%: z(Φ) = {f2(z,3)}' + (' (âm vì xác suất nhỏ hơn 50%).' if P < 50 else '.'), [['a8', f'{P}']])
    for P in rng.sample([60, 68, 70, 75, 80, 85, 90, 95, 98, 99, 50, 40], 10):
        z = float(a8p(P)[1]); add('a8', f'Tìm z > 0 sao cho P(|Z| < z) = {P}% (cột z(D) của bảng A8).', z, 0.0006, f'P(|Z| < z) = D(z) = {P}% nên đọc cột z(D) ở hàng {P}%.', f'Hàng {P}%: z(D) = {z:.3f}.', [['a8', f'{P}']])
    # ---- A9
    for _ in range(30):
        df = rng.choice(DFS9); F = rng.choice(T.A9_F[1:]); v = a9t(F, df)
        add('a9', f'Tra bảng A9: giá trị z của phân phối Student {df} bậc tự do ứng với F(z) = {F:g}.', v, 0.006, f'Vào cột {df} bậc tự do, hàng F = {F:g}.', f'Cột {df}, hàng {F:g}: {v:g}.', [['a9', F, df]])
    for _ in range(20):
        g = rng.choice([0.9, 0.95, 0.99]); n = rng.choice([4, 6, 8, 10, 11, 12, 15, 16, 19, 21, 25, 31, 41]); df = n - 1
        if df not in DFS9: n = rng.choice([4, 6, 8, 10, 11, 15, 16, 21]); df = n - 1
        F = round((1 + g) / 2, 4); v = a9t(F, df)
        add('a9', f'Khoảng tin cậy {int(g*100)}% cho μ (σ chưa biết) từ mẫu cỡ n = {n}. Giá trị t_{{α/2}} cần tra bảng A9 là?', v, 0.006, f'Bậc tự do n − 1 = {df}; hai phía nên F = 1 − α/2 = (1 + γ)/2 = {F:g}.', f'α/2 = {(1-g)/2:g} ⇒ F = {F:g}; cột {df}, hàng {F:g}: {v:g}.', [['a9', F, df]])
    for _ in range(10):
        al = rng.choice([0.05, 0.025, 0.01, 0.005, 0.1]); df = rng.choice(DFS9); F = round(1 - al, 4); v = a9t(F, df)
        add('a9', f'Tìm giá trị tới hạn t_α với α = {al*100:g}% của phân bố Student {df} bậc tự do (một phía, F(t_α) = 1 − α).', v, 0.006, f'F = 1 − α = {F:g}; cột {df}.', f'F = {F:g}; cột {df}, hàng {F:g}: {v:g}.', [['a9', F, df]])
    cases = [(31, 0.95), (18, 0.93), (21, 0.95), (43, 0.95), (35, 0.975), (45, 0.99), (19, 0.93), (25, 0.975), (60, 0.95), (15, 0.92), (33, 0.9), (46, 0.76), (27, 0.975), (70, 0.995), (22, 0.89)]
    for df, F in cases:
        ex = float(st.t.ppf(F, df)); add('a9', f'Student {df} bậc tự do, F(z) = {F:g}. Bảng A9 không có đủ (cột hoặc hàng): ước lượng z bằng nội suy tuyến tính.', ex, 0.035, 'Tìm hai cột (hoặc hai hàng) kề hai bên rồi nội suy tuyến tính; đáp án chính xác được chấp nhận trong ±0.035.', f'Giá trị chính xác ≈ {ex:.3f}; nội suy từ bảng cho kết quả gần số này (sai lệch nhỏ).', [['a9', F, df]])
    # ---- A10
    for _ in range(20):
        df = rng.choice(T.A10_DF); F = rng.choice(T.A10_F); v = a10t(F, df)
        add('a10', f'Tra bảng A10 (χ²): với {df} bậc tự do, giá trị x ứng với F = {F:g} là?', v, 0.051 if df > 20 else 0.006, f'Cột {df} bậc tự do, hàng F = {F:g}.', f'Cột {df}, hàng {F:g}: {v:g}.', [['a10', F, df]])
    rng.shuffle(Q)
    for i, q in enumerate(Q): q['id'] = i + 1
    return Q

if __name__ == '__main__':
    Q = build(); import collections; print(len(Q), collections.Counter(q['t'] for q in Q)); [print(q['q'], q['a']) for q in Q[:6]]
