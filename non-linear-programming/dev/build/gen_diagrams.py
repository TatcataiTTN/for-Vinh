#!/usr/bin/env python3
"""Sinh sơ đồ .drawio bằng script (toạ độ theo dải, không gõ tay), xuất SVG bằng drawio CLI, strip light-dark().
Chạy: python3 NLP-work/build/gen_diagrams.py"""
import os, re, subprocess, html, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'NLP-work', 'diagrams')
OUT = os.path.join(ROOT, 'for-Vinh', 'non-linear-programming', 'assets', 'diagrams')
os.makedirs(SRC, exist_ok=True); os.makedirs(OUT, exist_ok=True)

PAL = {  # fill, stroke
    'blue': ('#dae8fc', '#6c8ebf'), 'yellow': ('#fff2cc', '#d6b656'), 'green': ('#d5e8d4', '#82b366'),
    'red': ('#f8cecc', '#b85450'), 'purple': ('#e1d5e7', '#9673a6'), 'orange': ('#ffe6cc', '#d79b00'),
    'gray': ('#f5f5f5', '#999999'), 'white': ('#ffffff', '#666666'),
}

class Diagram:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.cells = []; self.n = 1

    def _id(self):
        self.n += 1; return f'c{self.n}'

    @staticmethod
    def esc(t):
        return html.escape(t, quote=True).replace('\n', '&#10;')

    def box(self, x, y, w, h, text, color='blue', fs=15, bold=False, shape='rounded=1;arcSize=12', align='center', valign='middle', extra=''):
        i = self._id(); f, s = PAL[color]
        style = f'{shape};whiteSpace=wrap;html=0;fillColor={f};strokeColor={s};strokeWidth=1.6;fontSize={fs};fontColor=#1c2330;align={align};verticalAlign={valign};spacing=6;'
        if bold: style += 'fontStyle=1;'
        style += extra
        self.cells.append(f'<mxCell id="{i}" value="{self.esc(text)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def diamond(self, x, y, w, h, text, color='yellow', fs=14):
        return self.box(x, y, w, h, text, color, fs, shape='rhombus', extra='')

    def header(self, x, y, w, h, text, fill='#1d4ed8', fs=16):
        i = self._id()
        style = f'rounded=1;arcSize=20;whiteSpace=wrap;fillColor={fill};strokeColor={fill};fontColor=#ffffff;fontSize={fs};fontStyle=1;align=center;verticalAlign=middle;'
        self.cells.append(f'<mxCell id="{i}" value="{self.esc(text)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def label(self, x, y, w, h, text, fs=14, color='#1c2330', align='left', bold=False):
        i = self._id()
        style = f'text;whiteSpace=wrap;html=0;align={align};verticalAlign=top;fontSize={fs};fontColor={color};' + ('fontStyle=1;' if bold else '')
        self.cells.append(f'<mxCell id="{i}" value="{self.esc(text)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def edge(self, a, b, text='', color='#444444', dashed=False, extra=''):
        i = self._id()
        style = f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=0;endArrow=block;endFill=1;strokeColor={color};strokeWidth=2;fontSize=13;labelBackgroundColor=#ffffff;' + ('dashed=1;' if dashed else '') + extra
        self.cells.append(f'<mxCell id="{i}" value="{self.esc(text)}" style="{style}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
        return i

    def xml(self):
        body = '\n'.join(self.cells)
        return (f'<mxfile><diagram name="{self.esc(self.name)}"><mxGraphModel dx="{self.w}" dy="{self.h}" grid="0" page="1" pageWidth="{self.w}" pageHeight="{self.h}" background="#ffffff">'
                f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n{body}\n</root></mxGraphModel></diagram></mxfile>')

    def save(self, fname):
        p = os.path.join(SRC, fname + '.drawio')
        open(p, 'w', encoding='utf-8').write(self.xml())
        import xml.etree.ElementTree as ET
        ET.parse(p)  # XML hợp lệ
        svg = os.path.join(OUT, fname + '.svg')
        r = subprocess.run(['drawio', '--export', '--format', 'svg', '--output', svg, p], capture_output=True, text=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(svg):
            print('drawio lỗi', fname, r.stderr[:300]); sys.exit(1)
        s = open(svg, encoding='utf-8').read()
        s = re.sub(r'color-scheme:\s*light dark\s*;?', 'color-scheme: light;', s)
        s = re.sub(r'light-dark\(([^,]+),\s*[^)]+\)', r'\1', s)
        open(svg, 'w', encoding='utf-8').write(s)
        assert 'light-dark' not in s, 'còn light-dark'
        # bản PNG để tự kiểm tra bằng mắt (giữ trong dự án, không đưa lên site)
        subprocess.run(['drawio', '--export', '--format', 'png', '--scale', '1.4', '--output', os.path.join(SRC, fname + '.png'), p], capture_output=True, timeout=180)
        print('OK', fname)


# ------------------------------------------------------------------ D1: phân loại bài toán tối ưu
def d1():
    d = Diagram('Phân loại bài toán tối ưu', 1040, 600)
    d.header(20, 14, 1000, 40, 'Bản đồ các lớp bài toán tối ưu — từ tuyến tính tới phi tuyến tổng quát', fs=17)
    d.box(20, 70, 610, 500, '', 'gray', extra='dashed=1;')
    d.label(34, 76, 560, 26, 'Tối ưu phi tuyến (NLP): f hoặc g, h phi tuyến', 15, bold=True)
    d.box(48, 112, 556, 436, '', 'blue')
    d.label(62, 118, 520, 26, 'Tối ưu LỒI: f lồi, g_i lồi, h_j affine (cực tiểu địa phương = toàn cục)', 14, bold=True)
    d.box(76, 168, 500, 350, '', 'green')
    d.label(90, 174, 470, 26, 'QP lồi: ½xᵀQx + cᵀx, Q ⪰ 0, ràng buộc tuyến tính', 14, bold=True)
    d.box(104, 226, 444, 270, '', 'yellow')
    d.label(118, 232, 400, 26, 'Quy hoạch tuyến tính (LP): Q = 0', 14, bold=True)
    d.box(132, 286, 388, 84, 'Miền chấp nhận = đa diện lồi\nnghiệm tại đỉnh → đơn hình', 'white', 14)
    d.box(132, 384, 388, 84, 'Bài toán vận tải, phân công,\nphối trộn, khẩu phần…', 'white', 14)
    # cột phải: ví dụ & phương pháp
    d.header(660, 70, 360, 34, 'Mỗi lớp: ví dụ và công cụ giải', '#136f3a', 15)
    d.box(660, 116, 360, 92, 'NLP không lồi\nví dụ: min xy trên đĩa x²+y²≤2\nKKT chỉ là điều kiện cần → so sánh các ứng viên', 'red', 13, align='left')
    d.box(660, 220, 360, 92, 'Tối ưu lồi\nví dụ: bình phương tối thiểu, danh mục Markowitz\nKKT + Slater ⇒ điều kiện cần và đủ', 'blue', 13, align='left')
    d.box(660, 324, 360, 92, 'QP lồi\nví dụ: chiếu điểm lên đa diện\nnull-space (đẳng thức), tập hoạt động (bất đẳng thức)', 'green', 13, align='left')
    d.box(660, 428, 360, 92, 'LP\nví dụ: kế hoạch sản xuất\nđơn hình, điểm trong, đối ngẫu', 'yellow', 13, align='left')
    d.box(660, 532, 360, 50, 'Ngoài sơ đồ: quy hoạch nguyên (miền rời rạc) — NP-khó', 'orange', 13)
    d.save('d1-phan-loai-toi-uu')


# ------------------------------------------------------------------ D2: kiểm tra hàm lồi
def d2():
    d = Diagram('Quy trình kiểm tra hàm lồi', 1000, 760)
    d.header(20, 14, 960, 38, 'Quy trình kiểm tra f có lồi hay không', fs=17)
    a = d.box(360, 70, 280, 52, 'Cho hàm f: dom f ⊆ Rⁿ → R', 'blue', 15, True)
    b = d.diamond(340, 146, 320, 96, 'dom f có lồi không?', 'yellow', 15)
    n1 = d.box(30, 166, 230, 56, 'Không lồi\n(miền xác định không lồi)', 'red', 14)
    c = d.diamond(340, 268, 320, 96, 'f khả vi hai lần?', 'yellow', 15)
    d1_ = d.box(690, 288, 290, 56, 'Dùng định nghĩa Jensen\nhoặc phép bảo toàn tính lồi', 'purple', 14)
    e = d.box(340, 392, 320, 66, 'Tính Hessian ∇²f(x)\n(ma trận đối xứng)', 'blue', 15)
    f = d.box(340, 482, 320, 66, 'Kiểm tra dấu: giá trị riêng\nhoặc minor chính (Sylvester)', 'blue', 15)
    g = d.diamond(340, 572, 320, 100, '∇²f(x) ⪰ 0 với mọi x ∈ dom f?', 'yellow', 14)
    y = d.box(30, 596, 250, 62, 'f LỒI\n(∇²f ≻ 0 ⇒ lồi chặt)', 'green', 15, True)
    n2 = d.box(720, 596, 250, 62, 'f KHÔNG lồi\ntìm x có λ_min(∇²f(x)) < 0', 'red', 14)
    d.edge(a, b); d.edge(b, n1, 'không'); d.edge(b, c, 'có'); d.edge(c, d1_, 'không'); d.edge(c, e, 'có')
    d.edge(e, f); d.edge(f, g); d.edge(g, y, 'có'); d.edge(g, n2, 'không')
    d.label(700, 350, 280, 60, 'Lưu ý: dấu của các định thức con chính chỉ đủ để kết luận XÁC ĐỊNH DƯƠNG; muốn kết luận NỬA xác định dương phải dùng giá trị riêng hoặc MỌI minor chính.', 12, '#555555')
    d.save('d2-kiem-tra-ham-loi')


# ------------------------------------------------------------------ D3: quy trình KKT
def d3():
    d = Diagram('Quy trình giải bằng KKT', 1000, 860)
    d.header(20, 14, 960, 38, 'Quy trình giải bài toán có ràng buộc bằng điều kiện KKT', fs=17)
    ys = 70
    s1 = d.box(300, ys, 400, 60, '1. Chuẩn hóa: min f(x)\ng_i(x) ≤ 0,  h_j(x) = 0', 'blue', 15, True)
    s2 = d.box(300, ys + 84, 400, 60, '2. Kiểm tra lồi: f lồi? g_i lồi?\nh_j affine?', 'blue', 15)
    s3 = d.box(300, ys + 168, 400, 60, '3. Điều kiện chính quy:\nSlater (bài lồi) hoặc LICQ', 'blue', 15)
    s4 = d.box(300, ys + 252, 400, 60, '4. Lập L = f + Σλ_i g_i + Σμ_j h_j\nviết hệ KKT', 'blue', 15)
    s5 = d.box(300, ys + 336, 400, 74, '5. Chia trường hợp theo tập ràng buộc chặt\n(λ_i = 0 nếu g_i không chặt): ≤ 2ᵐ trường hợp', 'yellow', 14)
    s6 = d.box(300, ys + 434, 400, 60, '6. Giải hệ; lọc điểm KHẢ THI\nvà có λ_i ≥ 0', 'yellow', 15)
    q = d.diamond(310, ys + 520, 380, 110, 'Bài toán LỒI và\nSlater thỏa mãn?', 'yellow', 15)
    yes = d.box(30, ys + 556, 230, 74, 'KKT là điều kiện CẦN VÀ ĐỦ\n⇒ điểm KKT là nghiệm\ntoàn cục', 'green', 14, True)
    no = d.box(740, ys + 540, 240, 110, 'KKT chỉ là điều kiện cần (cần CQ)\n⇒ so sánh f tại các ứng viên,\nxét bậc 2, kiểm điều kiện tồn tại nghiệm', 'red', 13)
    fin = d.box(300, ys + 672, 400, 56, '7. Kiểm tra lại: thay nghiệm vào từng ràng buộc,\ntính f(x*), đối chiếu bằng phần mềm', 'purple', 14)
    for a, b in [(s1, s2), (s2, s3), (s3, s4), (s4, s5), (s5, s6), (s6, q)]:
        d.edge(a, b)
    d.edge(q, yes, 'có'); d.edge(q, no, 'không'); d.edge(yes, fin); d.edge(no, fin)
    d.label(730, ys + 90, 250, 100, 'Ví dụ thực hành: min xy trên x²+y²≤2\n→ 3 điểm KKT hợp lệ, chỉ 2 điểm là cực tiểu', 12, '#555555')
    d.save('d3-quy-trinh-kkt')


# ------------------------------------------------------------------ D4: active set
def d4():
    d = Diagram('Lưu đồ thuật toán tập hoạt động', 1000, 820)
    d.header(20, 14, 960, 38, 'Thuật toán tập hoạt động (Active Set) cho QP có ràng buộc bất đẳng thức', fs=17)
    a = d.box(330, 68, 340, 64, 'Khởi tạo: x⁰ khả thi,\nW₀ = I(x⁰) (ràng buộc chặt)', 'blue', 15, True)
    b = d.box(330, 156, 340, 76, 'Giải bài toán con (không gian hạt nhân):\nmin ½dᵀQd + gᵀd  với aᵢᵀd = 0, i ∈ Wk\n(g = Qxᵏ + c)', 'blue', 14)
    c = d.diamond(350, 258, 300, 96, 'dᵏ = 0 ?', 'yellow', 16)
    e1 = d.box(30, 290, 250, 100, 'αk = min{1, min_{i∉W, aᵢᵀd>0} (bᵢ − aᵢᵀxᵏ)/(aᵢᵀdᵏ)}\nxᵏ⁺¹ = xᵏ + αk dᵏ', 'purple', 13)
    e2 = d.box(30, 424, 250, 76, 'Nếu α < 1 (bị cản):\nthêm ràng buộc cản vào W', 'purple', 14)
    f = d.box(720, 290, 260, 76, 'Tính nhân tử μ̂ᵢ (i ∈ Wk) từ\nQxᵏ + c + Σ μ̂ᵢ aᵢ = 0', 'blue', 14)
    g = d.diamond(720, 396, 260, 110, 'μ̂ᵢ ≥ 0\nvới mọi i ∈ Wk ?', 'yellow', 15)
    ok = d.box(730, 546, 240, 86, 'DỪNG: xᵏ là nghiệm tối ưu\n(Q ⪰ 0 ⇒ nghiệm toàn cục)', 'green', 14, True)
    rm = d.box(400, 546, 260, 86, 'Loại chỉ số j = argmin μ̂ᵢ\nkhỏi W: W ← W \\ {j}', 'red', 14)
    lp = d.label(330, 660, 340, 60, 'Mỗi vòng luôn giữ xᵏ khả thi và f không tăng; hữu hạn vòng khi không suy biến.', 12, '#555555')
    d.edge(a, b); d.edge(b, c)
    d.edge(c, e1, 'không'); d.edge(e1, e2); d.edge(c, f, 'có'); d.edge(f, g)
    d.edge(g, ok, 'có'); d.edge(g, rm, 'không')
    d.edge(e2, b, 'lặp k+1', dashed=True, extra='exitX=0.5;exitY=1;entryX=0;entryY=0.5;')
    d.edge(rm, b, 'lặp k+1', dashed=True, extra='exitX=0.5;exitY=0;entryX=1;entryY=0.5;')
    d.save('d4-active-set')


# ------------------------------------------------------------------ D5: lộ trình
def d5():
    d = Diagram('Lộ trình học', 1060, 420)
    d.header(20, 12, 1020, 38, 'Lộ trình bốn module (bám 3 slide chính khóa và giáo trình Boyd & Vandenberghe)', fs=17)
    xs = [20, 285, 550, 815]
    cols = ['gray', 'blue', 'green', 'purple']
    ttl = ['Module 0\nKiến thức tiên quyết', 'Module 1\nTập lồi & hàm lồi', 'Module 2\nBài toán có ràng buộc & KKT', 'Module 3\nQuy hoạch toàn phương']
    sub = ['Đại số tuyến tính, giải tích nhiều biến,\ntối ưu cơ bản, ôn QHTT\n(Boyd Ch.1, phụ lục A)',
           'Slide 1 (54 trang)\ntập lồi, bao lồi, siêu phẳng,\nHessian, phép bảo toàn\n(Boyd Ch.2–3)',
           'Slide 2 (68 trang)\nLagrange, KKT, Slater,\nđiều kiện cần và đủ\n(Boyd Ch.4–5)',
           'Slide 3 (81 trang)\ntồn tại nghiệm, tính chất tập nghiệm,\nnull space, active set\n(Boyd 4.4, 10.1)']
    ids = []
    for i in range(4):
        h = d.header(xs[i], 70, 245, 64, ttl[i], '#1d4ed8' if i else '#5d6879', 15)
        b = d.box(xs[i], 146, 245, 130, sub[i], cols[i], 13, align='center')
        ids.append(h)
    for i in range(3):
        d.edge(ids[i], ids[i+1])
    d.box(20, 300, 1020, 96, 'Cách học: (1) xem deck từng phần → (2) đọc ví dụ chi tiết và lời giải → (3) thử công cụ tương tác → (4) làm bài tính chấm số → (5) làm quiz. Đầu ra mong muốn: nhận diện bài toán lồi, viết và giải hệ KKT, giải QP bằng null space và active set.', 'white', 14, align='left')
    d.save('d5-lo-trinh')


# ------------------------------------------------------------------ D6: phân loại QP theo Q
def d6():
    d = Diagram('Tính chất nghiệm QP theo Q', 1000, 520)
    d.header(20, 12, 960, 38, 'Dạng của Q quyết định tính chất tập nghiệm của QP', fs=17)
    r = d.box(380, 68, 240, 60, 'Q trong min ½xᵀQx + cᵀx\ntrên đa diện Δ ≠ ∅', 'blue', 15, True)
    b1 = d.box(20, 190, 220, 120, 'Q ≻ 0\nxác định dương', 'green', 15, True)
    b2 = d.box(270, 190, 220, 120, 'Q ⪰ 0\nnửa xác định dương', 'green', 15, True)
    b3 = d.box(510, 190, 220, 120, 'Q ≺ 0\nxác định âm', 'red', 15, True)
    b4 = d.box(760, 190, 220, 120, 'Q không xác định\n(có cả λ>0 và λ<0)', 'orange', 15, True)
    t1 = d.box(20, 350, 220, 130, 'Có nghiệm DUY NHẤT\nSol(P) = loc(P)\nbài toán lồi chặt', 'white', 13)
    t2 = d.box(270, 350, 220, 130, 'Sol(P) là tập lồi đóng\n(có thể vô số nghiệm)\ntồn tại ⇔ điều kiện Eaves', 'white', 13)
    t3 = d.box(510, 350, 220, 130, 'Mọi cực tiểu địa phương\nlà ĐIỂM CỰC BIÊN của Δ\nSol(P) ⊂ loc(P) ⊂ extr Δ', 'white', 13)
    t4 = d.box(760, 350, 220, 130, 'KHÔNG lồi: nhiều cực tiểu\nđịa phương; loc(P) có thể\nkhông đóng, Sol(P) không lồi', 'white', 13)
    for b in (b1, b2, b3, b4): d.edge(r, b)
    for b, t in ((b1, t1), (b2, t2), (b3, t3), (b4, t4)): d.edge(b, t)
    d.save('d6-qp-theo-Q')


if __name__ == '__main__':
    for fn in (d1, d2, d3, d4, d5, d6):
        fn()
