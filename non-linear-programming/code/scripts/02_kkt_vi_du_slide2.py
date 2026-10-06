"""02 — Các ví dụ KKT của Slide 2 (tr.55-61) giải bằng code, thay cho việc làm tay nhiều bảng.

Hai công cụ:
  (a) cvxpy      : bài toán LỒI -> cho nghiệm và nhân tử (dual_value) trực tiếp.
  (b) sympy      : liệt kê MỌI trường hợp 'ràng buộc chặt / lỏng' của hệ KKT (dùng cho bài không lồi).
Chạy: python3 02_kkt_vi_du_slide2.py        Cần: pip install cvxpy sympy numpy scipy
"""
import itertools
import cvxpy as cp
import sympy as sp

print("=" * 70)
print("VÍ DỤ 1 (slide tr.55): min (x-1)^2 + y - 2  s.t. x+y-2<=0, x-y+1=0   (bài toán lồi)")
x, y = cp.Variable(), cp.Variable()
g = x + y - 2 <= 0
h = x - y + 1 == 0
p = cp.Problem(cp.Minimize((x - 1) ** 2 + y - 2), [g, h])
p.solve()
print(f"  nghiệm (x*, y*) = ({x.value:.4f}, {y.value:.4f}),  f* = {p.value:.4f}")
print(f"  nhân tử (lambda, mu) = ({g.dual_value:.4f}, {h.dual_value:.4f})   <- khớp slide (0, 1)")


def kkt_enumerate(f, ineq, eq, vars_):
    """Liệt kê điểm KKT của  min f  s.t.  ineq_i <= 0,  eq_j = 0  bằng cách chia trường hợp theo ràng buộc chặt.
    Trả về danh sách (điểm, nhân tử, hợp lệ?).  hợp lệ = khả thi và lambda >= 0."""
    lam = sp.symbols(f"l1:{len(ineq) + 1}", real=True)
    mu = sp.symbols(f"m1:{len(eq) + 1}", real=True)
    L = f + sum(l * g_ for l, g_ in zip(lam, ineq)) + sum(m * h_ for m, h_ in zip(mu, eq))
    out = []
    for active in itertools.product([False, True], repeat=len(ineq)):
        eqs = [sp.diff(L, v) for v in vars_] + list(eq)
        for a, l, g_ in zip(active, lam, ineq):
            eqs.append(g_ if a else l)               # chặt: g_i = 0;  lỏng: lambda_i = 0 (điều kiện bù)
        for sol in sp.solve(eqs, list(vars_) + list(lam) + list(mu), dict=True):
            if not all(v.is_real for v in sol.values()):
                continue
            pt = {v: sol[v] for v in vars_}
            feasible = all(g_.subs(sol) <= 1e-9 for g_ in ineq)
            sign_ok = all(sol[l] >= -1e-9 for l in lam)
            out.append((pt, {str(l): sol[l] for l in lam}, feasible and sign_ok))
    return out


print("=" * 70)
print("VÍ DỤ 3 (slide tr.60): min x*y  s.t.  x^2 + y^2 <= 2   (KHÔNG lồi -> dùng liệt kê KKT)")
X, Y = sp.symbols("x y", real=True)
for pt, lam, ok in kkt_enumerate(X * Y, [X ** 2 + Y ** 2 - 2], [], (X, Y)):
    print(f"  điểm {pt}, nhân tử {lam}, f = {pt[X] * pt[Y]}, "
          f"{'HỢP LỆ (KKT)' if ok else 'loại (lambda<0 hoặc không khả thi)'}")
print("  => so sánh f: (1,-1) và (-1,1) cho f = -1 (cực tiểu); (0,0) có f = 0 là điểm yên ngựa.")

print("=" * 70)
print("VÍ DỤ 2 (slide tr.57): min -(x^2+y^2+4x-6y)  s.t.  x+y-3<=0, -2x+y-2<=0")
F = -(X ** 2 + Y ** 2 + 4 * X - 6 * Y)
res = kkt_enumerate(F, [X + Y - 3, -2 * X + Y - 2], [], (X, Y))
for pt, lam, ok in res:
    print(f"  điểm {pt}, nhân tử {lam}, {'HỢP LỆ' if ok else 'loại'}")
print(f"  => số điểm KKT hợp lệ: {sum(1 for r in res if r[2])}  (điểm (1/3, 8/3) của slide có lambda_2 < 0)")

print("=" * 70)
print("VÍ DỤ 4 (slide tr.61): min 2x+y  s.t. 3x+y<=6, x+y<=4, x>=0, y>=0   (LP)")
x, y = cp.Variable(), cp.Variable()
cons = [3 * x + y <= 6, x + y <= 4, x >= 0, y >= 0]
p = cp.Problem(cp.Minimize(2 * x + y), cons)
p.solve()
print(f"  min: ({x.value:.4f}, {y.value:.4f}), f* = {p.value:.4f}, nhân tử = {[round(abs(float(c.dual_value)), 4) for c in cons]}")
p = cp.Problem(cp.Maximize(2 * x + y), cons)
p.solve()
print(f"  max: ({x.value:.4f}, {y.value:.4f}), f* = {p.value:.4f}")
