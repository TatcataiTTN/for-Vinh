"""Hàm tiện ích sinh MCQ số thực/xác suất."""
from qb import f, fg, nd, ni
def pm(B, rng, stem, p, expl, lvl, topic, src, extra=(), d=4, origin='goc', lo=0.0, hi=1.0):
    """MCQ có đáp án là số thực (thường xác suất) làm tròn d chữ số."""
    ex = [e for e in extra if e is not None]
    B.mcq(stem, f(p, d), nd(p, rng, d, extra=ex, lo=lo, hi=hi), expl, lvl, topic, src, origin)
def frac(B, stem, correct, wrong, expl, lvl, topic, src, origin='goc'):
    B.mcq(stem, correct, wrong, expl, lvl, topic, src, origin)
