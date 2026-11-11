"""Sinh vectors đối chiếu hàm toán JS (Φ, t, χ²) với SciPy."""
import json
from scipy import stats as st
V = dict(phi=[[z, float(st.norm.cdf(z))] for z in [-3.2, -1.96, -0.57, 0, 0.5, 1.23, 2.33, 3.5]],
         z=[[p, float(st.norm.ppf(p))] for p in [0.01, 0.07, 0.3, 0.5, 0.93, 0.975, 0.995]],
         t=[[df, F, float(st.t.ppf(F, df))] for df in [1, 2, 5, 9, 18, 31, 47, 120] for F in [0.6, 0.9, 0.93, 0.95, 0.975, 0.999]],
         chi=[[m, F, float(st.chi2.ppf(F, m))] for m in [1, 3, 9, 20, 47, 150] for F in [0.005, 0.05, 0.95, 0.99]])
json.dump(V, open('tests/vectors.json', 'w')); print(sum(len(v) for v in V.values()), 'vector')
