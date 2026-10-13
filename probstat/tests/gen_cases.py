import json, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'build'))
from scipy import stats as st
from pskit import quartiles, mean, var_s
r = random.Random(5); C = dict(norm=[], t=[], chi2=[], binom=[], pois=[], desc=[])
for _ in range(200):
    z = r.uniform(-3.5, 3.5); C['norm'].append([z, float(st.norm.cdf(z))])
    v = r.randint(1, 60); t = r.uniform(-4, 4); a = r.choice([.005, .01, .025, .05, .1]); C['t'].append([t, v, float(st.t.cdf(t, v)), a, float(st.t.ppf(1 - a, v))])
    k = r.randint(1, 40); x = r.uniform(.5, 70); C['chi2'].append([x, k, float(st.chi2.cdf(x, k)), a, float(st.chi2.ppf(1 - a, k))])
    n = r.randint(1, 60); p = r.uniform(.01, .99); kk = r.randint(0, n); C['binom'].append([kk, n, p, float(st.binom.pmf(kk, n, p)), float(st.binom.cdf(kk, n, p))])
    mu = r.uniform(.2, 20); kk = r.randint(0, 40); C['pois'].append([kk, mu, float(st.poisson.pmf(kk, mu)), float(st.poisson.cdf(kk, mu))])
    n = r.randint(3, 25); xs = [round(r.uniform(-50, 120), 2) for _ in range(n)]; a_, b_, c_ = quartiles(xs)
    C['desc'].append(dict(x=xs, mean=mean(xs), var=var_s(xs), qL=a_, qM=b_, qU=c_))
json.dump(C, open(os.path.join(os.path.dirname(__file__), 'cases.json'), 'w'))
