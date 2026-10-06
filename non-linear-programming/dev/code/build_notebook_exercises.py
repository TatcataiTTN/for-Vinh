"""Sinh notebook bài tập cvxpy có tự chấm: notebooks/nlp_cvxpy_bai_tap.ipynb (chưa chạy: để người học tự điền rồi chạy trên Colab)."""
import os, re, nbformat as nbf
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cvxpy_bai_tap", "bai_tap_cvxpy.py"), encoding="utf-8").read()
test = open(os.path.join(HERE, "cvxpy_bai_tap", "test_bai_tap_cvxpy.py"), encoding="utf-8").read()
# tách từng hàm starter
funcs = re.findall(r"(def \w+\(.*?\n(?:    .*\n|\n)+)", src)
nb = nbf.v4.new_notebook(); C = nbf.v4.new_code_cell; M = nbf.v4.new_markdown_cell
cells = [M("# Bài tập cvxpy có tự chấm\n\nĐiền vào các chỗ `TODO` (xoá `raise NotImplementedError`), chạy ô của hàm, rồi chạy ô **Chấm bài** ở cuối. Mỗi hàm có đặc tả đầu vào/đầu ra trong docstring. "
           "Test so sánh với đáp án đã được đối chiếu bằng `scipy` (cách giải khác)."),
         C("try:\n    import cvxpy as cp\nexcept ImportError:\n    %pip install -q cvxpy\n    import cvxpy as cp\nimport numpy as np\nfrom scipy.optimize import minimize, nnls\nprint('cvxpy', cp.__version__)")]
for i, f in enumerate(funcs, 1):
    name = re.match(r"def (\w+)", f).group(1)
    cells.append(M(f"## Bài {i}: `{name}`"))
    cells.append(C(f.rstrip() + "\n"))
body = test.split("mod = importlib.import_module", 1)[1].split("\n", 1)[1]           # bỏ dòng nạp module
body = body.replace("import pytest", "")
grade = ("import types, sys, math\n"
         "class _P:\n    @staticmethod\n    def approx(v, rel=1e-6, abs=1e-12):\n        return _Approx(v, rel, abs)\n"
         "class _Approx:\n    def __init__(s, v, rel, abs): s.v, s.rel, s.abs = v, rel, abs\n"
         "    def __eq__(s, o):\n        a, b = np.array(o, float), np.array(s.v, float)\n        return bool(np.all(np.abs(a - b) <= np.maximum(s.abs, s.rel * np.abs(b))))\n"
         "pytest = _P\nmod = types.SimpleNamespace(**{k: v for k, v in globals().items() if callable(v) and not k.startswith('_')})\n"
         + body + "\n\ndef chấm():\n    ok = 0\n    tests = [(k, v) for k, v in globals().items() if k.startswith('test_') and callable(v)]\n"
         "    for k, v in tests:\n        try:\n            v(); print('✔', k); ok += 1\n        except NotImplementedError:\n            print('… chưa làm:', k)\n"
         "        except AssertionError as e:\n            print('✘', k, '— sai kết quả')\n        except Exception as e:\n            print('✘', k, '— lỗi:', type(e).__name__, e)\n"
         "    print(f'\\nĐạt {ok}/{len(tests)} test')\nchấm()\n")
cells += [M("## Chấm bài"), C(grade)]
nb["cells"] = cells
nb["metadata"] = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}, "colab": {"provenance": []}}
out = os.path.join(HERE, "notebooks", "nlp_cvxpy_bai_tap.ipynb"); nbf.write(nb, out); print("ghi", out)
