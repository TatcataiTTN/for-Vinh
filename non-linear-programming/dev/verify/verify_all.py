#!/usr/bin/env python3
"""Kiểm chứng MỌI con số dùng trong site non-linear-programming.
Chạy: python3 NLP-work/verify/verify_all.py  -> in kết quả + ghi NLP-work/verify/results.json
Không gõ tay đáp án: mọi số hiển thị trên site lấy từ results.json."""
import json, itertools
import numpy as np
import sympy as sp
from scipy.optimize import minimize, linprog

R = {}

# ---------- Module 1: hàm lồi / Hessian ----------
def classify(H):
    H = np.array(H, float)
    ev = np.linalg.eigvalsh(H)
    if np.all(ev > 1e-9): k = "xác định dương (lồi chặt)"
    elif np.all(ev >= -1e-9): k = "nửa xác định dương (lồi)"
    elif np.all(ev < -1e-9): k = "xác định âm (lõm chặt)"
    elif np.all(ev <= 1e-9): k = "nửa xác định âm (lõm)"
    else: k = "không xác định (không lồi, không lõm)"
    return ev.round(6).tolist(), k

x, y = sp.symbols('x y', real=True)
def hess(f, vars_=(x, y)):
    return sp.hessian(f, vars_)

R["m1_hess"] = {}
for name, f in {
    "x^2+y^2": x**2 + y**2,
    "x^2+xy+y^2": x**2 + x*y + y**2,
    "3x^2+3y^2-4xy": 3*x**2 + 3*y**2 - 4*x*y,
    "4x^2+y^2-x-2y": 4*x**2 + y**2 - x - 2*y,
    "xy": x*y,
    "x^2-y^2": x**2 - y**2,
    "x^2/y": x**2 / y,
    "x/y": x / y,
    "1/(xy)": 1/(x*y),
    "sqrt(x^2+y^2)": sp.sqrt(x**2 + y**2),
}.items():
    H = hess(f)
    R["m1_hess"][name] = {"H": str(H), "H_latex": sp.latex(H)}
# các ma trận số
R["m1_mat"] = {}
for name, H in {
    "I": [[2, 0], [0, 2]], "P1": [[2, 1], [1, 2]], "P2": [[6, -4], [-4, 6]],
    "P3": [[8, 0], [0, 2]], "S": [[0, 1], [1, 0]], "D": [[2, 0], [0, -2]],
    "semi": [[1, 1], [1, 1]], "semi2": [[1, 0], [0, 0]],
}.items():
    ev, k = classify(H)
    R["m1_mat"][name] = {"H": H, "eig": ev, "class": k,
                          "minors": [float(np.linalg.det(np.array(H, float)[:i, :i])) for i in (1, 2)]}

# 1D/2D slide exercises - numeric spot checks of convexity via Hessian symbolic
t = sp.symbols('t', real=True)
R["m1_1d"] = {
    "e^x-1": sp.simplify(sp.diff(sp.exp(t) - 1, t, 2)).__str__(),
    "log x": sp.simplify(sp.diff(sp.log(t), t, 2)).__str__(),
    "x^a (a=3)": sp.simplify(sp.diff(t**3, t, 2)).__str__(),
}
# xy on R^2_{++}: H=[[0,1],[1,0]] indefinite -> neither; 1/(xy): PSD on positive orthant; x/y: indefinite
xp, yp = sp.symbols('x y', positive=True)
def eig_at(f, pts):
    Hs = hess(f, (xp, yp))
    out = []
    for (a, b) in pts:
        M = np.array(Hs.subs({xp: a, yp: b}).tolist(), float)
        out.append({"pt": [a, b], "eig": np.linalg.eigvalsh(M).round(5).tolist()})
    return out
pts = [(1, 1), (2, 1), (1, 3), (0.5, 0.5)]
R["m1_ex_slide"] = {
    "xy": eig_at(xp*yp, pts),
    "1/(xy)": eig_at(1/(xp*yp), pts),
    "x/y": eig_at(xp/yp, pts),
}
# max of convex is convex (midpoint sample check), distance to convex set
rng = np.random.default_rng(2026)
def jensen_violations(f, dim, n=20000, lo=-3, hi=3):
    v = 0
    for _ in range(n):
        a = rng.uniform(lo, hi, dim); b = rng.uniform(lo, hi, dim); th = rng.uniform()
        if f(th*a + (1-th)*b) > th*f(a) + (1-th)*f(b) + 1e-9: v += 1
    return v
R["m1_jensen"] = {
    "max(x^2, (x-2)^2)": jensen_violations(lambda z: max(z[0]**2, (z[0]-2)**2), 1),
    "dist to unit disk": jensen_violations(lambda z: max(0, np.linalg.norm(z) - 1), 2),
    "x^3 (should violate)": jensen_violations(lambda z: z[0]**3, 1),
}

# ---------- Module 2: KKT ----------
# Ví dụ 1 (slide tr.55)
def ex1():
    f = lambda v: (v[0]-1)**2 + v[1] - 2
    cons = [{'type': 'ineq', 'fun': lambda v: -(v[0] + v[1] - 2)},
            {'type': 'eq', 'fun': lambda v: v[0] - v[1] + 1}]
    r = minimize(f, [0, 1], constraints=cons, method='SLSQP', options={'ftol': 1e-14})
    return r.x.round(5).tolist(), round(float(r.fun), 6)
R["m2_ex1_num"] = ex1()
# nhân tử (lam, mu) tại (1/2, 3/2)
xs, ys, lam, mu = sp.symbols('x y lam mu', real=True)
L1 = (xs-1)**2 + ys - 2 + lam*(xs+ys-2) + mu*(xs-ys+1)
sol = sp.solve([sp.diff(L1, xs), sp.diff(L1, ys), xs+ys-2, xs-ys+1], [xs, ys, lam, mu], dict=True)
R["m2_ex1_kkt"] = [{k: str(v) for k, v in s.items()} for s in sol]
# case g inactive: lam=0
sol0 = sp.solve([sp.diff(L1.subs(lam, 0), xs), sp.diff(L1.subs(lam, 0), ys), xs-ys+1], [xs, ys, mu], dict=True)
R["m2_ex1_lam0"] = [{k: str(v) for k, v in s.items()} for s in sol0]

# Ví dụ 2 (slide tr.57/59): max x^2+y^2+4x-6y, x+y<=3, -2x+y<=2   -> min F=-f
F2 = lambda xx, yy: -(xx**2 + yy**2 + 4*xx - 6*yy)
l1, l2 = sp.symbols('l1 l2', real=True)
Fs = -(xs**2 + ys**2 + 4*xs - 6*ys)
g1 = xs + ys - 3
g2 = -2*xs + ys - 2
L2 = Fs + l1*g1 + l2*g2
ex2 = []
for act in [(), (1,), (2,), (1, 2)]:
    eqs = [sp.diff(L2, xs), sp.diff(L2, ys)]
    unk = [xs, ys, l1, l2]
    if 1 in act: eqs.append(g1)
    else: eqs.append(l1)
    if 2 in act: eqs.append(g2)
    else: eqs.append(l2)
    s = sp.solve(eqs, unk, dict=True)
    for sol_ in s:
        pt = {k: sp.nsimplify(v) for k, v in sol_.items()}
        feas = all(float(c.subs(sol_)) <= 1e-9 for c in (g1, g2))
        ok = feas and float(sol_[l1]) >= -1e-9 and float(sol_[l2]) >= -1e-9
        ex2.append({"active": list(act), "sol": {str(k): str(v) for k, v in pt.items()}, "feasible": feas, "KKT(lam>=0)": ok})
R["m2_ex2_all_active_sets"] = ex2
# f trên miền: không bị chặn trên
R["m2_ex2_unbounded_pt"] = {"pt": [-100, -198], "g1": -100-198-3, "g2": 200-198-2,
                            "f": (-100)**2 + (-198)**2 + 4*(-100) - 6*(-198)}
# biến thể: cực tiểu f (lồi) -> KKT (0,2), lam=2
Lmin = xs**2 + ys**2 + 4*xs - 6*ys + l1*g1 + l2*g2
sm = sp.solve([sp.diff(Lmin, xs), sp.diff(Lmin, ys), g2, l1], [xs, ys, l1, l2], dict=True)
R["m2_ex2_min_variant"] = [{str(k): str(v) for k, v in s.items()} for s in sm]
rr = minimize(lambda v: v[0]**2+v[1]**2+4*v[0]-6*v[1], [0, 0], method='SLSQP',
              constraints=[{'type': 'ineq', 'fun': lambda v: 3 - v[0] - v[1]}, {'type': 'ineq', 'fun': lambda v: 2 + 2*v[0] - v[1]}])
R["m2_ex2_min_variant_num"] = [rr.x.round(5).tolist(), round(float(rr.fun), 5)]

# Ví dụ 3: min xy, x^2+y^2<=2
L3 = xs*ys + lam*(xs**2 + ys**2 - 2)
s3 = sp.solve([sp.diff(L3, xs), sp.diff(L3, ys), lam*(xs**2+ys**2-2)], [xs, ys, lam], dict=True)
R["m2_ex3"] = [{"x": str(s[xs]), "y": str(s[ys]), "lam": str(s[lam]), "f": str(s[xs]*s[ys]),
                "KKT": bool(float(s[lam]) >= 0)} for s in s3]
H3 = np.array([[2*0.5*2, 1], [1, 2*0.5*2]])  # Hessian L tại lam=1/2: [[2lam,1],[1,2lam]]
R["m2_ex3_hessL"] = {"lam=1/2": np.linalg.eigvalsh(np.array([[1, 1], [1, 1]])).tolist(),
                     "lam=0": np.linalg.eigvalsh(np.array([[0, 1], [1, 0]])).tolist(),
                     "lam=-1/2": np.linalg.eigvalsh(np.array([[-1, 1], [1, -1]])).tolist()}

# Ví dụ 4: LP min 2x+y
r4 = linprog([2, 1], A_ub=[[3, 1], [1, 1]], b_ub=[6, 4], bounds=[(0, None), (0, None)], method='highs')
R["m2_ex4_min"] = [r4.x.tolist(), r4.fun]
r4m = linprog([-2, -1], A_ub=[[3, 1], [1, 1]], b_ub=[6, 4], bounds=[(0, None), (0, None)], method='highs')
R["m2_ex4_max"] = [r4m.x.tolist(), -r4m.fun]

# Câu 9 (bài tập tham khảo): min 3x1^2+3x2^2-4x1x2, -x1-x2+2<=0, x1^2+x2^2-4<=0
a1, a2, m1_, m2_ = sp.symbols('a1 a2 m1 m2', real=True)
f9 = 3*a1**2 + 3*a2**2 - 4*a1*a2
c1 = -a1 - a2 + 2
c2 = a1**2 + a2**2 - 4
r9 = minimize(lambda v: 3*v[0]**2+3*v[1]**2-4*v[0]*v[1], [1.5, 1.0],
              constraints=[{'type': 'ineq', 'fun': lambda v: -( -v[0]-v[1]+2)},
                           {'type': 'ineq', 'fun': lambda v: -(v[0]**2+v[1]**2-4)}], method='SLSQP', options={'ftol': 1e-14})
R["m2_c9_num"] = [r9.x.round(5).tolist(), round(float(r9.fun), 6)]
R["m2_c9_slater_pt"] = {"pt": [1.2, 1.2], "c1": -1.2-1.2+2, "c2": 1.44+1.44-4}
# KKT thủ công: c1 active, c2 inactive -> x1=x2=1 ; nhân tử
L9 = f9 + m1_*c1
s9 = sp.solve([sp.diff(L9, a1), sp.diff(L9, a2), c1], [a1, a2, m1_], dict=True)
R["m2_c9_kkt"] = [{str(k): str(v) for k, v in s.items()} for s in s9]
R["m2_c9_c2_at_sol"] = float(c2.subs(s9[0]))

# Câu 10: min 4x1^2+x2^2-x1-2x2, 2x1+x2<=1, x1^2-1<=0
f10 = 4*a1**2 + a2**2 - a1 - 2*a2
d1 = 2*a1 + a2 - 1
d2 = a1**2 - 1
r10 = minimize(lambda v: 4*v[0]**2+v[1]**2-v[0]-2*v[1], [0, 0],
               constraints=[{'type': 'ineq', 'fun': lambda v: 1-2*v[0]-v[1]}, {'type': 'ineq', 'fun': lambda v: 1-v[0]**2}],
               method='SLSQP', options={'ftol': 1e-14})
R["m2_c10_num"] = [r10.x.round(5).tolist(), round(float(r10.fun), 6)]
L10 = f10 + m1_*d1
s10 = sp.solve([sp.diff(L10, a1), sp.diff(L10, a2), d1], [a1, a2, m1_], dict=True)
R["m2_c10_kkt"] = [{str(k): str(v) for k, v in s.items()} for s in s10]
R["m2_c10_unconstrained"] = {"pt": [1/8, 1], "g1": 2/8 + 1 - 1, "note": "vi phạm 2x1+x2<=1 vì =1.25"}
R["m2_c10_slater"] = {"pt": [0, 0], "d1": -1, "d2": -1}

# ---------- Module 0: đại số, LP ôn tập ----------
A = np.array([[4, 1], [3, 0], [2, 7]], float)
R["m0_transpose"] = A.T.tolist()
B = np.array([[3, 1], [2, 4]], float)
R["m0_inverse_ex"] = {"A": [[2, 5, 3], [1, 4, 3], [1, 3, 2]]}
Ainv = np.linalg.inv(np.array([[2, 5], [1, 3]], float))
R["m0_inv_2x2"] = {"A": [[2, 5], [1, 3]], "det": round(float(np.linalg.det(np.array([[2, 5], [1, 3]]))), 6), "inv": Ainv.round(6).tolist()}
Hh = np.array([[2, -1], [-1, 2]], float)
R["m0_eig_2x2"] = {"A": Hh.tolist(), "eig": np.linalg.eigvalsh(Hh).tolist(), "det": float(np.linalg.det(Hh)), "trace": float(np.trace(Hh))}
# gradient/Hessian mẫu: f=x^2 y + 3xy^2 - 2x at (1,2)
fx = xs**2*ys + 3*xs*ys**2 - 2*xs
g = [sp.diff(fx, v) for v in (xs, ys)]
Hf = sp.hessian(fx, (xs, ys))
R["m0_grad_ex"] = {"f": str(fx), "grad": [str(t_) for t_ in g], "grad_at_1_2": [float(t_.subs({xs: 1, ys: 2})) for t_ in g],
                   "H": str(Hf), "H_at_1_2": np.array(Hf.subs({xs: 1, ys: 2}).tolist(), float).tolist()}
# Taylor bậc 2 của f=e^x+y^2 tại (0,0), đánh giá tại (0.1,0.2)
ft = sp.exp(xs) + ys**2
q = ft.subs({xs: 0, ys: 0}) + sum(sp.diff(ft, v).subs({xs: 0, ys: 0})*v for v in (xs, ys)) \
    + sp.Rational(1, 2)*(sp.diff(ft, xs, 2).subs({xs: 0, ys: 0})*xs**2 + 2*sp.diff(ft, xs, ys).subs({xs: 0, ys: 0})*xs*ys + sp.diff(ft, ys, 2).subs({xs: 0, ys: 0})*ys**2)
R["m0_taylor"] = {"f": str(ft), "taylor2": str(sp.expand(q)),
                  "f(0.1,0.2)": float(ft.subs({xs: 0.1, ys: 0.2})), "T2(0.1,0.2)": float(q.subs({xs: 0.1, ys: 0.2}))}
# Câu hỏi hướng giảm nhanh nhất: -grad
# Nông trại (bài 11 tham khảo): min 50x1+35x2+25x3 ; 2x1+x2+3x3>=60 ; 5x1+4x2+2x3 in [20,40]; 3x1+2x2+5x3=50
c = [50, 35, 25]
Aub = [[-2, -1, -3], [-5, -4, -2], [5, 4, 2]]
bub = [-60, -20, 40]
Aeq = [[3, 2, 5]]; beq = [50]
r11 = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs')
R["m0_farm_primal"] = {"status": int(r11.status), "msg": r11.message, "max_D1_given_D3_50": 50*2/3}
# đối ngẫu: max 60 y1 + 20 y2 - 40 y3 + 50 y4 ; y1,y2,y3>=0; y4 tự do; A^T y <= c
# biến: y1 (>=60), y2 (>=20), y3 (<=40 -> dùng y3>=0 hệ số -40), y4 free
cd = [-60, -20, 40, -50]
Aud = [[2, 5, -5, 3], [1, 4, -4, 2], [3, 2, -2, 5]]
bud = [50, 35, 25]
rd = linprog(cd, A_ub=Aud, b_ub=bud, bounds=[(0, None)]*3 + [(None, None)], method='highs')
R["m0_farm_dual"] = {"status": int(rd.status), "msg": rd.message}

# Knapsack DP (câu 13,14 tham khảo)
def knap(W, items):
    dp = [0]*(W+1); pick = [[False]*(W+1) for _ in items]
    for i, (w, v) in enumerate(items):
        for c_ in range(W, w-1, -1):
            if dp[c_-w] + v > dp[c_]:
                dp[c_] = dp[c_-w] + v; pick[i][c_] = True
    # backtrack
    c_ = W; chosen = []
    for i in range(len(items)-1, -1, -1):
        if pick[i][c_]:
            chosen.append(i+1); c_ -= items[i][0]
    return dp[W], sorted(chosen), dp
R["m0_knap_13"] = knap(5, [(2, 3), (3, 4), (4, 5), (5, 8)])[:2]
R["m0_knap_14"] = knap(10, [(5, 10), (4, 40), (6, 30), (3, 50)])[:2]
# vét cạn
def brute(W, items):
    best = (0, ())
    for mask in itertools.product([0, 1], repeat=len(items)):
        if sum(m*w for m, (w, v) in zip(mask, items)) <= W:
            val = sum(m*v for m, (w, v) in zip(mask, items))
            if val > best[0]: best = (val, mask)
    return best
R["m0_knap_13_brute"] = brute(5, [(2, 3), (3, 4), (4, 5), (5, 8)])
R["m0_knap_14_brute"] = brute(10, [(5, 10), (4, 40), (6, 30), (3, 50)])

# LP mẫu Module 0: max 3x1+2x2, x1+x2<=4, x1+3x2<=6, x1<=3
rlp = linprog([-3, -2], A_ub=[[1, 1], [1, 3], [1, 0]], b_ub=[4, 6, 3], bounds=(0, None), method='highs')
R["m0_lp_demo"] = [rlp.x.tolist(), -rlp.fun]

# ---------- Module 3: QP ----------
# 3.1 đối xứng hóa
Qn = np.array([[1, 4], [0, 3]], float)
Qs = (Qn + Qn.T)/2
R["m3_sym"] = {"Q": Qn.tolist(), "Qs": Qs.tolist(),
               "check_x": [2, -1], "xQx": float(np.array([2, -1]) @ Qn @ np.array([2, -1])),
               "xQsx": float(np.array([2, -1]) @ Qs @ np.array([2, -1]))}
# QP không lồi slide: min x1^2 - x2^2 trên [1,3]^2
best = None
for v in itertools.product([1, 3], repeat=2):
    val = v[0]**2 - v[1]**2
    best = min(best or (1e9, None), (val, v))
R["m3_nonconvex_box"] = {"min_at_vertices": best, "all": {str(v): v[0]**2 - v[1]**2 for v in itertools.product([1, 3], repeat=2)}}
rb = minimize(lambda v: v[0]**2 - v[1]**2, [2, 2], bounds=[(1, 3), (1, 3)], method='SLSQP')
R["m3_nonconvex_box_num"] = [rb.x.round(5).tolist(), round(float(rb.fun), 6)]
# QP -x1^2-x2^2+1 trên [-1,1]^2 : 4 đỉnh
R["m3_concave_box"] = {str(v): -v[0]**2 - v[1]**2 + 1 for v in itertools.product([-1, 1], repeat=2)}
# Null space method ví dụ tr.56-58
Q = np.array([[2, -2, -1], [-2, 2, 1], [-1, 1, 5]], float)
cvec = np.array([10, -26, -2], float)
Aeq3 = np.array([[1, 1, 0], [1, 0, 1]], float)
beq3 = np.array([4, 10], float)
# đối chiếu hàm mục tiêu slide: 2x1^2 -4x1x2 -2x1x3 +2x2^2 +2x2x3 +5x3^2 +10x1 -26x2 -2x3
xs3 = sp.symbols('x1 x2 x3', real=True)
fq = 2*xs3[0]**2 - 4*xs3[0]*xs3[1] - 2*xs3[0]*xs3[2] + 2*xs3[1]**2 + 2*xs3[1]*xs3[2] + 5*xs3[2]**2 + 10*xs3[0] - 26*xs3[1] - 2*xs3[2]
Hq = np.array(sp.hessian(fq, xs3).tolist(), float)
R["m3_null_Q_check"] = {"Hessian_from_f": Hq.tolist(), "Q_slide": Q.tolist(), "equal": bool(np.allclose(Hq, Q)),
                        "eig": np.linalg.eigvalsh(Q).round(6).tolist()}
def null_space_qp(Q, c, A, b, xbar):
    m, n = A.shape
    gbar = Q @ xbar + c; bbar = b - A @ xbar
    # KKT trực tiếp
    K = np.block([[Q, A.T], [A, np.zeros((m, m))]])
    rhs = np.concatenate([-gbar, bbar])
    sol = np.linalg.solve(K, rhs)
    d = sol[:n]; mu = sol[n:]
    return xbar + d, mu, d
xk, mu, d = null_space_qp(Q, cvec, Aeq3, beq3, np.zeros(3))
fval = float(0.5*xk@Q@xk + cvec@xk)
R["m3_null_ex"] = {"x*": xk.round(4).tolist(), "mu": mu.round(4).tolist(), "f": round(fval, 4),
                   "slide_claim": {"x*": [3.0588, 0.9412, 6.9412], "mu": [23.2941, -30.5882], "f": 212.7059}}
# đối chiếu bằng SLSQP
rq = minimize(lambda v: 0.5*v@Q@v + cvec@v, np.zeros(3), constraints=[{'type': 'eq', 'fun': lambda v: Aeq3@v - beq3}], method='SLSQP', options={'ftol': 1e-14})
R["m3_null_ex_num"] = [rq.x.round(4).tolist(), round(float(rq.fun), 4)]
# theo công thức Y, Z của slide
Z = np.array([[-1], [1], [1]], float)
Y = np.array([[1/3, 1/3], [2/3, -1/3], [-1/3, 2/3]], float)
R["m3_null_YZ"] = {"AZ": (Aeq3@Z).tolist(), "AY": (Aeq3@Y).round(6).tolist()}
bbar = beq3; gbar = cvec
dY = np.linalg.solve(Aeq3@Y, bbar)
ZQZ = (Z.T@Q@Z)
dZ = np.linalg.solve(ZQZ, -(Z.T@Q@Y@dY + Z.T@gbar))
d = Y@dY + Z@dZ
mu2 = np.linalg.solve((Aeq3@Y).T, -Y.T@gbar - Y.T@Q@d)  # (AY)^T mu = -Y^T g - Y^T Q d
R["m3_null_steps"] = {"dY": dY.tolist(), "ZtQZ": ZQZ.tolist(), "dZ": dZ.tolist(), "d": d.round(4).tolist(),
                      "mu": mu2.round(4).tolist()}
# ghi chú: slide (4.7) viết (AY)^T mu = -Y^T g + G d ; đúng dấu là -Y^T(g + Q d)

# Bài tập 1: min 3x1^2+2x1x2+x1x3+2.5x2^2+2x2x3+2x3^2-8x1-3x2-3x3 ; x1+x3=0 ; x2+x3=0 ; ĐS (2,-1,1)?
x1_, x2_, x3_ = xs3
f_bt = 3*x1_**2 + 2*x1_*x2_ + x1_*x3_ + sp.Rational(5, 2)*x2_**2 + 2*x2_*x3_ + 2*x3_**2 - 8*x1_ - 3*x2_ - 3*x3_
Hb = np.array(sp.hessian(f_bt, xs3).tolist(), float)
cb = np.array([float(sp.diff(f_bt, v).subs({x1_: 0, x2_: 0, x3_: 0})) for v in xs3])
Ab = np.array([[1, 0, 1], [0, 1, 1]], float); bb = np.zeros(2)
xb, mub, _ = null_space_qp(Hb, cb, Ab, bb, np.zeros(3))
R["m3_bt1"] = {"Hessian": Hb.tolist(), "c": cb.tolist(), "x*": xb.round(6).tolist(), "mu": mub.round(6).tolist(),
               "f": float(0.5*xb@Hb@xb + cb@xb), "slide_ans": [2, -1, 1],
               "slide_ans_feasible": bool(np.allclose(Ab@np.array([2, -1, 1]), 0)),
               "eig": np.linalg.eigvalsh(Hb).round(5).tolist()}
xt = np.array([2, -1, 1.0])
R["m3_bt1"]["f_at_slide_ans"] = float(0.5*xt@Hb@xt + cb@xt)

# Active set: ví dụ tr.69-79
def active_set(Q, c, A, b, x0, W0, maxit=50, verbose=True):
    """min 1/2 x'Qx + c'x s.t. A x <= b ; chỉ số 0-based. Trả về log các bước."""
    x = np.array(x0, float); W = list(W0); log = []
    n = len(x)
    for k in range(maxit):
        g = Q@x + c
        # giải bài toán con: min 1/2 d'Qd + g'd  s.t. a_i'd=0 (i in W)
        if W:
            Aw = A[W]
            K = np.block([[Q, Aw.T], [Aw, np.zeros((len(W), len(W)))]])
            rhs = np.concatenate([-g, np.zeros(len(W))])
            sol = np.linalg.solve(K, rhs)
            d = sol[:n]; lam_w = sol[n:]     # Qd + g + Aw' lam = 0
        else:
            d = np.linalg.solve(Q, -g); lam_w = np.array([])
        step = {"k": k, "x": x.round(6).tolist(), "W": [i+1 for i in W], "g": g.round(6).tolist(), "d": d.round(6).tolist()}
        if np.linalg.norm(d) < 1e-9:
            # nhân tử: g + sum mu_i a_i = 0  (slide) -> mu = lam_w
            mu_ = lam_w
            step["mu"] = {str(i+1): round(float(m_), 6) for i, m_ in zip(W, mu_)}
            step["f"] = float(0.5*x@Q@x + c@x)
            if len(W) == 0 or np.all(mu_ >= -1e-9):
                step["action"] = "dừng: mọi nhân tử >= 0"
                log.append(step); break
            j = int(np.argmin(mu_)); rem = W[j]
            step["action"] = f"loại ràng buộc {rem+1} (nhân tử âm nhất {mu_[j]:.4f})"
            W.pop(j)
        else:
            alpha = 1.0; block = None
            for i in range(len(b)):
                if i in W: continue
                ad = A[i]@d
                if ad > 1e-12:
                    t_ = (b[i] - A[i]@x)/ad
                    if t_ < alpha - 1e-12: alpha = t_; block = i
            step["alpha"] = round(float(alpha), 6)
            x = x + alpha*d
            if block is not None:
                W.append(block); step["action"] = f"đi α={alpha:.4f}, gặp ràng buộc cản {block+1} -> thêm vào W"
            else:
                step["action"] = f"đi α=1 (không bị cản)"
            step["x_next"] = x.round(6).tolist()
        log.append(step)
    return x, log

# slide: min (x1-1)^2+(x2-0.5)^2 ; Q=2I, c=(-2,-1) ; ràng buộc 4 dòng
Qa = 2*np.eye(2); ca = np.array([-2, -1.0])
Aa = np.array([[1, 1], [3, 1], [-1, 0], [0, -1]], float); ba = np.array([1, 1.5, 0, 0])
xa, loga = active_set(Qa, ca, Aa, ba, [0, 0], [2, 3])
R["m3_active_ex"] = {"x*": xa.round(6).tolist(), "f": float((xa[0]-1)**2 + (xa[1]-0.5)**2), "log": loga,
                     "slide_c_typo": "slide ghi c=[-2,1]^T ở tr.55; các bước sau dùng c=(-2,-1) => đúng là c=[-2,-1]^T"}
ra = minimize(lambda v: (v[0]-1)**2 + (v[1]-0.5)**2, [0, 0], constraints=[{'type': 'ineq', 'fun': lambda v: ba - Aa@v}], method='SLSQP', options={'ftol': 1e-14})
R["m3_active_ex_num"] = [ra.x.round(5).tolist(), round(float(ra.fun), 6)]

# bài tập: min (x1-4.5)^2+(x2-3)^2 ; 5 ràng buộc ; x0=(0,0)
Ab2 = np.array([[2, -3], [1, 1], [-3, 5], [-1, 0], [0, -1]], float); bb2 = np.array([6, 5, 15, 0, 0], float)
Qb = 2*np.eye(2); cb2 = np.array([-9, -6.0])
xb2, logb = active_set(Qb, cb2, Ab2, bb2, [0, 0], [3, 4])
R["m3_active_bt"] = {"x*": xb2.round(6).tolist(), "f": float((xb2[0]-4.5)**2 + (xb2[1]-3)**2), "iters": len(logb), "log": logb}
rb2 = minimize(lambda v: (v[0]-4.5)**2 + (v[1]-3)**2, [0, 0], constraints=[{'type': 'ineq', 'fun': lambda v: bb2 - Ab2@v}], method='SLSQP', options={'ftol': 1e-14})
R["m3_active_bt_num"] = [rb2.x.round(5).tolist(), round(float(rb2.fun), 6)]
# W0 = I(x0): tại (0,0) ràng buộc 4,5 (x>=0,y>=0) hoạt động -> chỉ số 0-based [3,4]

# Điều kiện tồn tại: ví dụ x1 trên x1 x2>=1 (Frank-Wolfe không áp dụng)
R["m3_frank_wolfe_counter"] = {"inf": 0.0, "note": "x1 -> 0 khi x2 = 1/x1 -> inf; không đạt"}
# Ví dụ nghiệm nội điểm và min -x2^2 + x1 x2 trên orthant (P1)
rP1 = [((0, 0), 0.0), ((5, 0), 0.0), ((1, 1), -1 + 1), ((0, 1), -1), ((0, 5), -25)]
R["m3_P1_samples"] = [{"x": list(p), "f": -p[1]**2 + p[0]*p[1]} for p, _ in rP1]
# Q xác định dương -> nghiệm duy nhất: min x1^2+x2^2, box
R["m3_pd_box"] = {"x*": [0, 0], "f": 0}



# ---------- MODULE 0 bổ sung ----------
# BTDOC: kế hoạch sản xuất 2 sản phẩm
rp = linprog([-4, -5], A_ub=[[2, 1], [1, 2], [0, 1]], b_ub=[8, 7, 3], bounds=(0, None), method='highs')
R["m0_btdoc_plan"] = {"x": rp.x.round(6).tolist(), "f": round(-rp.fun, 6)}
rdp = linprog([8, 7, 3], A_ub=[[-2, -1, 0], [-1, -2, -1]], b_ub=[-4, -5], bounds=(0, None), method='highs')
R["m0_btdoc_plan_dual"] = {"y": rdp.x.round(6).tolist(), "g": round(rdp.fun, 6)}
verts = []
import itertools as _it
cons = [([2, 1], 8), ([1, 2], 7), ([0, 1], 3), ([-1, 0], 0), ([0, -1], 0)]
for (a1, b1), (a2, b2) in _it.combinations(cons, 2):
    M_ = np.array([a1, a2], float)
    if abs(np.linalg.det(M_)) < 1e-12: continue
    pt = np.linalg.solve(M_, [b1, b2])
    if all(np.dot(a, pt) <= b + 1e-9 for a, b in cons): verts.append(pt.round(6).tolist())
R["m0_btdoc_plan_vertices"] = [{"v": v, "f": 4*v[0] + 5*v[1]} for v in verts]
# BTDOC: bài toán 4 mặt hàng
r4 = linprog([-5, -8, -4, -6], A_ub=[[12, 5, 15, 6], [14, 8, 7, 9], [17, 13, 9, 12]], b_ub=[300, 500, 200], bounds=(0, None), method='highs')
R["m0_btdoc_4prod"] = {"x": r4.x.round(6).tolist(), "f": round(-r4.fun, 6)}
# BTDOC: ma trận nghịch đảo 3x3 và Cramer
A3 = np.array([[1, 2, 3], [2, 5, 3], [1, 0, 8]], float)
R["m0_btdoc_inv"] = {"det": round(float(np.linalg.det(A3)), 6), "inv": np.linalg.inv(A3).round(6).tolist(),
                     "check_AinvA": np.round(np.linalg.inv(A3) @ A3, 6).tolist()}
Ac = np.array([[1, 0, 2], [3, 4, 6], [-1, -2, 3]], float); bc = np.array([6, 30, 8], float)
R["m0_btdoc_cramer"] = {"det": round(float(np.linalg.det(Ac)), 6), "x": np.linalg.solve(Ac, bc).round(6).tolist(),
                        "x_frac": [str(sp.nsimplify(v)) for v in np.linalg.solve(Ac, bc)]}
# Cauchy-Schwarz, nhân ma trận, chuyển vị
u = np.array([1, 2, 2.]); v = np.array([2, 3, 6.])
R["m0_cs"] = {"dot": float(u@v), "nu": float(np.linalg.norm(u)), "nv": float(np.linalg.norm(v)), "prod": float(np.linalg.norm(u)*np.linalg.norm(v))}
Ma = np.array([[1, 2], [3, 4]], float); Mb = np.array([[0, 1], [1, 1]], float)
R["m0_ABT"] = {"AB": (Ma@Mb).tolist(), "ABt": (Ma@Mb).T.tolist(), "BtAt": (Mb.T@Ma.T).tolist()}
# điểm dừng và phân loại
fx1 = xs**2 + xs*ys + ys**2 - 3*xs
st = sp.solve([sp.diff(fx1, xs), sp.diff(fx1, ys)], [xs, ys], dict=True)[0]
R["m0_stat1"] = {"f": str(fx1), "pt": {str(k): str(v) for k, v in st.items()}, "H": np.array(sp.hessian(fx1, (xs, ys)).tolist(), float).tolist(),
                 "eig": np.linalg.eigvalsh(np.array(sp.hessian(fx1, (xs, ys)).tolist(), float)).round(6).tolist(), "fval": float(fx1.subs(st))}
fx2 = xs**3 - 3*xs + ys**2
st2 = sp.solve([sp.diff(fx2, xs), sp.diff(fx2, ys)], [xs, ys], dict=True)
R["m0_stat2"] = {"f": str(fx2), "points": [{"pt": {str(k): str(v) for k, v in s_.items()}, "H_eig": np.linalg.eigvalsh(np.array(sp.hessian(fx2, (xs, ys)).subs(s_).tolist(), float)).round(6).tolist(), "f": float(fx2.subs(s_))} for s_ in st2]}
# gradient descent x^2+3y^2, x0=(-1.8,1.4), t=0.1 : vài bước
xg = np.array([-1.8, 1.4]); traj = [xg.copy()]
for _ in range(5):
    xg = xg - 0.1*np.array([2*xg[0], 6*xg[1]]); traj.append(xg.copy())
R["m0_gd"] = [[round(float(a), 6), round(float(b), 6)] for a, b in traj]
R["m0_gd_f"] = [round(float(a**2 + 3*b**2), 6) for a, b in traj]
# công thức nghịch đảo 2x2 khác, giá trị riêng 2x2
R["m0_eig_2x2b"] = {"A": [[4, 1], [1, 3]], "eig": np.linalg.eigvalsh(np.array([[4, 1], [1, 3]], float)).round(6).tolist()}
# knapsack đầy đủ bảng DP câu 13
def knap_table(W, items):
    n = len(items); T = [[0]*(W+1) for _ in range(n+1)]
    for i, (w_, v_) in enumerate(items, 1):
        for c_ in range(W+1):
            T[i][c_] = T[i-1][c_]
            if c_ >= w_: T[i][c_] = max(T[i][c_], T[i-1][c_-w_] + v_)
    return T
R["m0_knap13_table"] = knap_table(5, [(2, 3), (3, 4), (4, 5), (5, 8)])
R["m0_knap14_table"] = knap_table(10, [(5, 10), (4, 40), (6, 30), (3, 50)])
# LP lồi: điểm đỉnh cực biên và Weierstrass ví dụ: min 1/x trên (0,inf): inf=0 không đạt
R["m0_exist_examples"] = {"e^x": "inf=0 khong dat", "1/x tren (0,inf)": "inf=0 khong dat"}

# ---------- ERRATA slide (phát hiện khi kiểm chứng) ----------
def fpoly_null(v):
    return 2*v[0]**2-4*v[0]*v[1]-2*v[0]*v[2]+2*v[1]**2+2*v[1]*v[2]+5*v[2]**2+10*v[0]-26*v[1]-2*v[2]
rp = minimize(fpoly_null, np.zeros(3), constraints=[{'type': 'eq', 'fun': lambda v: Aeq3@v - beq3}], method='SLSQP', options={'ftol': 1e-14})
xs_slide = np.array(R["m3_null_ex"]["x*"])
xq = xk
R["errata_null_space"] = {
  "poly_at_slide_x": round(float(fpoly_null(xq)), 4),
  "half_form_at_slide_x": round(float(0.5*xq@Q@xq + cvec@xq), 4),
  "true_opt_of_polynomial": {"x": rp.x.round(4).tolist(), "f": round(float(rp.fun), 4)},
  "explain": "Đa thức trên slide có Hessian = 2Q_slide. Thuật toán trên slide giải min (1/2)x'Qx+c'x với Q_slide (f=102.4706). 212.7059 = đa thức tính tại x* đó."
}
Ab_v = np.array([[1, 0, 1], [0, 1, 1]], float)
rv = minimize(lambda v: float(0.5*v@Hb@v + cb@v), np.zeros(3), constraints=[{'type': 'eq', 'fun': lambda v: Ab_v@v - np.array([3, 0])}], method='SLSQP', options={'ftol': 1e-14})
xv, muv, _ = null_space_qp(Hb, cb, Ab_v, np.array([3.0, 0.0]), np.zeros(3))
R["errata_bt1"] = {"constraint_b=(3,0)": {"x": xv.round(6).tolist(), "mu": muv.round(6).tolist(), "f": round(float(0.5*xv@Hb@xv + cb@xv), 6)},
                   "note": "ĐS (2,-1,1) khớp khi b=(3,0), tức x1+x3=3 (không phải 0)."}
R["errata_ex2_kkt"] = "Tại (1/3,8/3): (l1,l2)=(10/9,-16/9), l2<0 nên không phải điểm KKT của min(-f); max f không bị chặn trên."
R["errata_active_c"] = "Slide tr.55 ghi c=[-2,1]; các bước dùng g=(-2,-1) => c=[-2,-1]."

# --- Lưu kết quả ---
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
import os
out = os.path.join(os.path.dirname(__file__), "results.json")
json.dump(clean(R), open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(clean(R), ensure_ascii=False, indent=1)[:12000])
