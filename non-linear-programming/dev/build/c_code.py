"""Trang 'Thực hành code' (code/index.html): chạy code ở đâu, bài mẫu docx, ví dụ slide bằng code, bài tập Pyodide, bài tập cvxpy."""
import html, json, os
from helpers import *

CODE = os.path.join(SITE, 'code')
COLAB = 'https://colab.research.google.com/github/TatcataiTTN/for-Vinh/blob/main/non-linear-programming/code/notebooks/'
RAW = 'https://github.com/TatcataiTTN/for-Vinh/blob/main/non-linear-programming/code/'

def rd(rel):
    return open(os.path.join(CODE, rel), encoding='utf-8').read()

def pre(rel, cls='src'):
    return f'<pre class="{cls}"><code>{html.escape(rd(rel))}</code></pre>'

def dl(rel, label=None):
    return f'<a href="{rel}" download>{label or rel}</a>'

def body():
    ex = json.load(open(os.path.join(CODE, 'exercises.json'), encoding='utf-8'))
    b = '<p class="tag">THỰC HÀNH CODE</p><h1>Giải bài tối ưu bằng code: Python, cvxpy, scipy</h1>'
    b += ('<p class="lead">Thay cho việc làm tay cả bảng dài, ta dùng code để <b>kiểm tra</b> và <b>tự động hóa</b> các bước: tính gradient/Hessian, liệt kê điểm KKT, giải QP, chạy active set. '
          'Trang này có: bài mẫu từ file của bạn, ví dụ slide giải bằng code (có kết quả thật), 7 bài tập chấm tự động ngay trong trình duyệt, và 4 bài tập cvxpy chấm bằng pytest/Colab.</p>')
    b += '<div class="toc">' + ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('chay-o-dau', 'Chạy code ở đâu?'), ('bai-mau', 'Bài mẫu (file docx)'), ('vi-du-slide', 'Ví dụ slide bằng code'), ('bai-tap-web', 'Bài tập chấm trên web'), ('bai-tap-cvxpy', 'Bài tập cvxpy'), ('tai-ve', 'Tải file')]) + '</div>'

    b += '<h2 id="chay-o-dau">Chạy code ở đâu? (GitHub có “biên dịch” được không?)</h2>'
    b += ('<p>GitHub Pages chỉ phục vụ <b>file tĩnh</b>: không có máy chủ để biên dịch hay chạy Python. Vì vậy mỗi loại bài dùng công cụ phù hợp:</p>'
          + table(['Loại', 'Công cụ chạy', 'Thư viện', 'Chấm tự động', 'Giới hạn thật'],
                  [['Bài tập hàm trên trang (7 bài)', '<b>Pyodide</b> (Python/WebAssembly) trong Web Worker', 'numpy, sympy', 'có: ĐÚNG / SAI KẾT QUẢ / LỖI CHẠY / QUÁ GIỜ', 'tải ~10–25 MB lần đầu từ CDN; <b>không có cvxpy</b>'],
                   ['Bài tập cvxpy (4 bài)', '<b>Google Colab</b> (mở notebook trong repo) hoặc máy bạn', 'cvxpy, scipy, numpy', 'có: ô “Chấm bài” hoặc <code>pytest</code>', 'cần tài khoản Google hoặc cài Python'],
                   ['Ví dụ slide (3 script)', 'máy bạn: <code>python3 file.py</code>', 'cvxpy, sympy, scipy', 'in kết quả để đối chiếu', 'cần cài thư viện'],
                   ['Kiểm tra mỗi lần push', '<b>GitHub Actions</b> (<code>.github/workflows/nlp-verify.yml</code>)', 'cvxpy, pytest…', 'có: pytest trên lời giải mẫu', 'chỉ kiểm tra, không chạy trên trang']])
          + callout('info', 'Vì sao không chạy cvxpy trong trình duyệt?', '<p>cvxpy cần các thư viện C/C++ đã biên dịch (không có bản “thuần Python” cho Pyodide). Với <code>numpy</code>/<code>sympy</code> (và <code>scipy</code>) thì chạy được. Muốn dùng cvxpy mà không cài gì, bấm nút Colab bên dưới.</p>'))

    b += '<h2 id="bai-mau">Bài mẫu trong file <code>tam thoi la vay.docx</code></h2>'
    b += ('<p>File của bạn gồm một đoạn code cvxpy và ảnh slide “Ví dụ 1” (KKT), kèm ghi chú: <i>“T7 học về cái này mà k hiểu. Làm các ví dụ trong slide (thấy làm tận cả 4 mặt bảng quá dài nên chắc chắn ko hiểu)”</i>. '
          'Nội dung đã được chuyển sang Markdown và ảnh: <a href="tam-thoi/tam_thoi_la_vay.md">tam_thoi_la_vay.md</a>.</p>')
    b += '<div class="wrow"><div class="wcol"><h3>Code gốc trong file</h3>' + f'<pre class="src"><code>{html.escape(rd("tam-thoi/tam_thoi_la_vay.md").split("```python")[1].split("```")[0].strip())}</code></pre></div>'
    b += '<div class="wcol"><h3>Ảnh trong file (slide tr.21)</h3><figure class="diagram"><img src="tam-thoi/slide-vi-du-1.png" alt="Slide Ví dụ 1" loading="lazy"><figcaption>Ví dụ 1 của slide 2: bài toán lồi, nhân tử (λ, μ) = (0, 1)</figcaption></figure></div></div>'
    b += '<h3>Đọc hiểu đoạn code (từng dòng) và các chỗ nên sửa</h3>' + steps([
        '<code>x = cp.Variable()</code>, <code>y = cp.Variable()</code>: khai báo hai biến quyết định (số thực).',
        '<code>cp.Minimize((x-3)**2 + (y-4)**2 - 2)</code>: hàm mục tiêu — tổng hai bình phương nên <b>lồi</b> (Hessian \\(2I\\succ0\\), Module 1).',
        '<code>x**2 + y**2 &lt;= 36</code>, <code>x &gt;= 0</code>, <code>y &gt;= 0</code>: miền chấp nhận được = hình tròn bán kính 6 ∩ góc phần tư thứ nhất — <b>lồi</b>.',
        '<code>problem.solve()</code>: cvxpy kiểm tra quy tắc DCP rồi gọi bộ giải; kết quả nằm ở <code>problem.value</code>, <code>x.value</code>, <code>y.value</code>.',
        '<b>Sửa 1:</b> <code>import cvxpy as cp</code> bị lặp hai lần — xóa một dòng. <b>Sửa 2:</b> <code>solve(qcp=True)</code> dành cho bài toán <i>tựa lồi</i> (DQCP); bài này là lồi thường nên chỉ cần <code>solve()</code>. <b>Sửa 3:</b> in thêm <code>problem.is_dcp()</code> và nhân tử <code>constraint.dual_value</code> để liên hệ với KKT.'])
    b += ('<h3>Kết quả chạy thật và kiểm tra bằng tay chỉ 3 dòng</h3><pre class="out-pre">' + html.escape(rd('outputs/01_cvxpy_bai_mau.txt')) + '</pre>'
          + callout('good', 'Thay “4 mặt bảng” bằng 3 dòng suy luận', '<p>(1) Cực tiểu <i>không ràng buộc</i> của \\((x-3)^2+(y-4)^2-2\\) là \\((3,4)\\), giá trị \\(-2\\). (2) \\((3,4)\\) có \\(x^2+y^2=25\\le36\\) và \\(x,y>0\\): thỏa mọi ràng buộc, <b>không ràng buộc nào chặt</b>. (3) Ràng buộc lỏng ⇒ mọi nhân tử bằng 0 (điều kiện bù) ⇒ đó là nghiệm bài toán có ràng buộc. Đây là lối tắt chung: <b>thử nghiệm không ràng buộc trước</b>; nếu khả thi thì xong.</p>')
          + '<h3>Ảnh render hai trang của file Word</h3><div class="wrow"><div class="wcol"><img src="tam-thoi/trang-1.png" alt="Trang 1" style="max-width:100%;border:1px solid var(--border)"></div><div class="wcol"><img src="tam-thoi/trang-2.png" alt="Trang 2" style="max-width:100%;border:1px solid var(--border)"></div></div>')

    b += '<h2 id="vi-du-slide">Ví dụ của slide giải bằng code</h2>'
    b += ('<p>Ba script dưới đây giải lại các ví dụ ở Module 2 và 3. Kết quả (đã chạy thật) khớp phần kiểm chứng của site, kể cả những chỗ slide chưa khớp.</p>')
    for rel, title, note in [('scripts/02_kkt_vi_du_slide2.py', 'KKT: Ví dụ 1–4 của slide 2 (cvxpy + sympy)', 'cvxpy giải bài lồi và trả nhân tử (<code>dual_value</code>); hàm <code>kkt_enumerate</code> liệt kê mọi điểm KKT của bài không lồi bằng cách chia trường hợp ràng buộc chặt/lỏng.'),
                             ('scripts/03_qp_vi_du_slide3.py', 'QP: null space và active set của slide 3 (numpy)', 'viết lại hai thuật toán của slide: hệ KKT đối xứng và vòng lặp tập hoạt động, in từng vòng.')]:
        out = rel.replace('scripts/', 'outputs/').replace('.py', '.txt')
        b += f'<details class="solution"><summary>{title}</summary><div class="body"><p>{note}</p><h4>Mã nguồn ({dl(rel, "tải " + os.path.basename(rel))})</h4>{pre(rel)}<h4>Kết quả chạy thật</h4><pre class="out-pre">{html.escape(rd(out))}</pre></div></details>'
    b += f'<p><a class="chk" href="{COLAB}nlp_cvxpy_vi_du.ipynb" target="_blank" rel="noopener" style="display:inline-block;background:var(--accent);color:#fff;padding:8px 14px;border-radius:8px;text-decoration:none;font-weight:700">▶ Mở notebook ví dụ trên Google Colab</a> (có sẵn cvxpy, đã kèm kết quả chạy)</p>'

    b += '<h2 id="bai-tap-web">Bài tập lập trình chấm tự động ngay trên trang (7 bài)</h2>'
    b += ('<p>Mỗi bài có <b>đặc tả đầu vào/đầu ra</b>, mã khởi đầu, test hiển thị và test ẩn. Python chạy trong trình duyệt của bạn (Pyodide); lần chạy đầu tải ~10–25 MB. '
          'Phán quyết: <span class="badge ok">✅ ĐÚNG</span> <span class="badge no">❌ SAI KẾT QUẢ</span> <span class="badge no">💥 LỖI CHẠY</span> <span class="badge no">⏱ QUÁ GIỜ</span>. Mã của bạn được lưu trong trình duyệt. '
          'Đáp án kỳ vọng do <b>lời giải mẫu</b> sinh ra rồi đối chiếu bằng scipy/sympy/vét cạn (pytest), không gõ tay.</p>')
    b += table(['Bài', 'Hàm', 'Đầu vào', 'Đầu ra', 'Mức'], [[f'<a href="#bai-{e["id"]}">{e["title"]}</a>', f'<code>{e["fn"]}</code>', e['inp'], e['out'], e['level']] for e in ex])
    b += '<div id="code-root" data-worker="../shared/pyworker.js"></div>'
    b += callout('warn', 'Giới hạn cần biết', '<ul><li>Cần mạng lần đầu để tải Pyodide từ <code>cdn.jsdelivr.net</code>.</li><li>Chậm hơn máy thật 2–3 lần; mỗi lần chấm giới hạn 10 giây.</li><li>Test ẩn nằm trong dữ liệu trang (ai mở mã nguồn trang đều thấy) — dùng để tự học, không dùng để thi.</li><li>Chỉ có numpy và sympy; bài cvxpy làm ở mục kế tiếp.</li></ul>')

    b += '<h2 id="bai-tap-cvxpy">Bài tập cvxpy (chấm bằng pytest hoặc Colab)</h2>'
    b += ('<p>Bốn bài dùng <b>cvxpy</b>. Có hai cách làm: (a) mở notebook trên Colab, điền <code>TODO</code> rồi chạy ô “Chấm bài”; (b) tải <code>bai_tap_cvxpy.py</code> + <code>test_bai_tap_cvxpy.py</code> về máy và chạy <code>pytest -q</code>.</p>'
          + table(['Bài', 'Hàm', 'Đầu vào', 'Đầu ra', 'Đối chiếu bằng'],
                  [['1. Nhân tử KKT Ví dụ 1 (slide 2)', '<code>kkt_multipliers_example1()</code>', 'không có', 'dict <code>{x, y, f, lambda, mu}</code> (float)', 'giá trị đã biết (1/2, 3/2, −1/4, 0, 1)'],
                   ['2. Danh mục phương sai nhỏ nhất', '<code>min_variance_portfolio(Sigma)</code>', 'Sigma: list[list[float]] n×n', 'dict <code>{w: list[float], variance: float}</code>', 'scipy SLSQP'],
                   ['3. Điểm gần nhất trong đa diện (slide 3)', '<code>project_onto_polyhedron(point, A, b)</code>', 'point (n), A (m×n), b (m)', 'dict <code>{x: list[float], distance_sq: float}</code>', 'ví dụ slide: (0.4, 0.3), 0.4'],
                   ['4. Bình phương tối thiểu không âm', '<code>nonneg_least_squares(A, b)</code>', 'A (m×n), b (m)', 'dict <code>{x: list[float] ≥ 0, residual_sq: float}</code>', 'scipy.optimize.nnls']])
          + f'<p><a class="chk" href="{COLAB}nlp_cvxpy_bai_tap.ipynb" target="_blank" rel="noopener" style="display:inline-block;background:var(--accent);color:#fff;padding:8px 14px;border-radius:8px;text-decoration:none;font-weight:700">▶ Mở notebook bài tập trên Google Colab</a></p>')
    b += f'<details class="solution"><summary>Mã khởi đầu <code>bai_tap_cvxpy.py</code> (điền TODO)</summary><div class="body">{pre("cvxpy_bai_tap/bai_tap_cvxpy.py")}</div></details>'
    b += f'<details class="solution"><summary>Bộ chấm <code>test_bai_tap_cvxpy.py</code></summary><div class="body">{pre("cvxpy_bai_tap/test_bai_tap_cvxpy.py")}</div></details>'
    b += f'<details class="solution"><summary>Lời giải mẫu <code>solutions.py</code> (xem sau khi thử)</summary><div class="body">{pre("cvxpy_bai_tap/solutions.py")}</div></details>'

    b += '<h2 id="tai-ve">Tải file</h2><ul>'
    for rel in ['scripts/01_cvxpy_bai_mau.py', 'scripts/02_kkt_vi_du_slide2.py', 'scripts/03_qp_vi_du_slide3.py', 'cvxpy_bai_tap/bai_tap_cvxpy.py', 'cvxpy_bai_tap/test_bai_tap_cvxpy.py', 'cvxpy_bai_tap/solutions.py', 'notebooks/nlp_cvxpy_vi_du.ipynb', 'notebooks/nlp_cvxpy_bai_tap.ipynb', 'tam-thoi/tam_thoi_la_vay.md', 'exercises.json']:
        b += f'<li>{dl(rel)}</li>'
    b += '</ul><p>Cài đặt trên máy: <code>pip install cvxpy numpy scipy sympy pytest</code>. Tài liệu phát triển và kiểm thử: <a href="../phat-trien/index.html">Phát triển</a>.</p>'
    return b, ex

def data_script(ex):
    return '<script type="application/json" id="code-data">' + json.dumps(ex, ensure_ascii=False).replace('</', '<\\/') + '</script>'
