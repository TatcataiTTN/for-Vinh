# -*- coding: utf-8 -*-
"""Thư viện dựng slide HTML theo đúng hệ thống thiết kế của template blue-professional
(beautiful-html-templates). Chỉ dùng các class CSS đã có sẵn trong shell_head.html,
cộng thêm layout-code / exam-badge tự thiết kế theo §5 AGENTS.md (cùng font, cùng
màu, cùng bo góc, cùng ngữ pháp component với phần còn lại của template)."""
import html


def esc(s):
    return html.escape(s, quote=False)


def cover_slide(kicker, title_lines, subtitle, meta_left, meta_right, active=True):
    active_cls = " active" if active else ""
    title_html = "<br>".join(esc(t) for t in title_lines)
    return f"""
    <div class="slide layout-cover{active_cls}">
      <div class="cover-decoration"></div>
      <div class="cover-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
      <div class="accent-line"></div>
      <h1>{title_html}</h1>
      <p class="subtitle">{esc(subtitle)}</p>
      <p class="meta">{esc(meta_left)} &nbsp;&middot;&nbsp; {esc(meta_right)}</p>
    </div>"""


def agenda_slide(tag, items):
    # items: list of (title, desc)
    rows = []
    for i, (t, d) in enumerate(items, start=1):
        rows.append(f"""
          <div class="agenda-item">
            <span class="agenda-num">{i:02d}</span>
            <div>
              <h3>{esc(t)}</h3>
              <p>{esc(d)}</p>
            </div>
          </div>""")
    return f"""
    <div class="slide layout-agenda">
      <div class="slide-header">
        <h4>Nội Dung Bài Học</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <div class="accent-line"></div>
        <div class="agenda-grid">{''.join(rows)}
        </div>
      </div>
    </div>"""


def _code_panel(caption, code):
    return f"""
          <div class="code-panel">
            <div class="code-caption">{esc(caption)}</div>
            <pre>{esc(code)}</pre>
          </div>"""


def code_slide(tag, title, h2, panels, explain=None, exam_badge=False):
    # panels: list of (caption, code)
    panels_html = "".join(_code_panel(c, code) for c, code in panels)
    badge = '<span class="exam-badge">Giống đề thi thật</span> ' if exam_badge else ""
    explain_html = f'<p class="code-explain">{badge}{explain}</p>' if explain else (
        f'<p class="code-explain">{badge}</p>' if exam_badge else "")
    return f"""
    <div class="slide layout-code">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        {panels_html}
        {explain_html}
      </div>
    </div>"""


def code_two_col_slide(tag, title, h2, left, right, explain=None):
    # left/right: (caption, code)
    return f"""
    <div class="slide layout-code">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        <div class="two-col-code">
          {_code_panel(*left)}
          {_code_panel(*right)}
        </div>
        {f'<p class="code-explain">{explain}</p>' if explain else ""}
      </div>
    </div>"""


def detail_slide(tag, title, h2, col1, col2):
    # col1/col2: list of (h3, [li,...])
    def block(h3, items):
        lis = "".join(f"<li>{esc(x)}</li>" for x in items)
        return f'<div class="detail-block"><h3>{esc(h3)}</h3><ul>{lis}</ul></div>'
    c1 = "".join(block(*b) for b in col1)
    c2 = "".join(block(*b) for b in col2)
    return f"""
    <div class="slide layout-detail">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        <div class="detail-body">
          <div class="detail-col">{c1}</div>
          <div class="detail-col">{c2}</div>
        </div>
      </div>
    </div>"""


def timeline_slide(tag, title, h2, steps):
    # steps: list of (title, desc)
    items = "".join(f"""
          <div class="timeline-step">
            <div class="step-circle">{i}</div>
            <div class="step-title">{esc(t)}</div>
            <div class="step-desc">{esc(d)}</div>
          </div>""" for i, (t, d) in enumerate(steps, start=1))
    return f"""
    <div class="slide layout-timeline">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        <div class="timeline-track">{items}
        </div>
      </div>
    </div>"""


def split_slide(tag, title, h2, insights, highlight_text, highlight_cite, ministats):
    # insights: list[str]; ministats: list[(val,label)]
    lis = "".join(f"<li>{esc(x)}</li>" for x in insights)
    stats = "".join(f'<div class="mini-stat"><div class="mini-val">{esc(v)}</div><div class="mini-label">{esc(l)}</div></div>' for v, l in ministats)
    return f"""
    <div class="slide layout-split">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        <div class="split-body">
          <div class="split-left"><ul class="insight-list">{lis}</ul></div>
          <div class="split-right">
            <div class="split-highlight">{esc(highlight_text)}<cite>{esc(highlight_cite)}</cite></div>
            <div class="mini-stat-row">{stats}</div>
          </div>
        </div>
      </div>
    </div>"""


def _entity_box(cx, cy, w, h, name, attrs):
    """Hộp thực thể ERD: tên in đậm trên, danh sách thuộc tính bên dưới, viền --primary."""
    x, y = cx - w / 2, cy - h / 2
    lines = "".join(
        f'<text x="{cx}" y="{cy - h/2 + 34 + i*20}" text-anchor="middle" '
        f'font-family="Inter, sans-serif" font-size="12.5" fill="#444">{esc(a)}</text>'
        for i, a in enumerate(attrs)
    )
    return f'''
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="#1e2bfa" stroke-width="2.2"/>
      <text x="{cx}" y="{cy - h/2 + 20}" text-anchor="middle" font-family="'Space Grotesk',sans-serif"
            font-size="15" font-weight="700" fill="#111111">{esc(name)}</text>
      <line x1="{x+10}" y1="{cy - h/2 + 26}" x2="{x+w-10}" y2="{cy - h/2 + 26}" stroke="#e2e5f5" stroke-width="1.5"/>
      {lines}'''


def _diamond(cx, cy, w, h, name):
    pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    return f'''
      <polygon points="{pts}" fill="#eef2ff" stroke="#1e2bfa" stroke-width="2"/>
      <text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="'Space Grotesk',sans-serif"
            font-size="12.5" font-weight="700" fill="#1e2bfa">{esc(name)}</text>'''


def erd_diagram_svg(center, side_nn, side_1n, rel_nn, rel_1n):
    """Sơ đồ ERD 3 thực thể: side_nn --(N-N, rel_nn)-- center --(1-N, rel_1n)-- side_1n.
    Mỗi tham số entity là (tên, [thuộc_tính,...]); side_1n là phía '1'."""
    W, H = 900, 460
    cx_center, cy_center = 620, 130
    cx_nn, cy_nn = 260, 130
    cx_1n, cy_1n = 400, 380
    box_w, box_h = 230, 26 + 20 * max(len(center[1]), len(side_nn[1]), len(side_1n[1])) + 10

    svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-height:44vh;">']

    # Duong noi + nhan ban so (ve TRUOC de nam duoi hop/thoi)
    dia1_x, dia1_y = (cx_nn + cx_center) / 2, cy_center
    svg.append(f'<line x1="{cx_nn+box_w/2}" y1="{cy_nn}" x2="{dia1_x-55}" y2="{dia1_y}" stroke="#8892b0" stroke-width="1.6"/>')
    svg.append(f'<line x1="{dia1_x+55}" y1="{dia1_y}" x2="{cx_center-box_w/2}" y2="{cy_center}" stroke="#8892b0" stroke-width="1.6"/>')
    svg.append(f'<text x="{cx_nn+box_w/2+18}" y="{cy_nn-8}" font-family="\'Space Grotesk\',sans-serif" font-size="13" font-weight="700" fill="#1e2bfa">N</text>')
    svg.append(f'<text x="{cx_center-box_w/2-22}" y="{cy_center-8}" font-family="\'Space Grotesk\',sans-serif" font-size="13" font-weight="700" fill="#1e2bfa">N</text>')

    dia2_x, dia2_y = cx_center - 90, (cy_center + cy_1n) / 2 + 30
    dia2_half_h = 30  # phải khớp đúng chiều cao hình thoi (60) truyền vào _diamond bên dưới, không tự bịa số
    svg.append(f'<line x1="{cx_center-30}" y1="{cy_center+box_h/2}" x2="{dia2_x}" y2="{dia2_y-dia2_half_h}" stroke="#8892b0" stroke-width="1.6"/>')
    svg.append(f'<line x1="{dia2_x}" y1="{dia2_y+dia2_half_h}" x2="{cx_1n+40}" y2="{cy_1n-box_h/2}" stroke="#8892b0" stroke-width="1.6"/>')
    svg.append(f'<text x="{cx_center-70}" y="{cy_center+box_h/2+22}" font-family="\'Space Grotesk\',sans-serif" font-size="13" font-weight="700" fill="#1e2bfa">N</text>')
    svg.append(f'<text x="{cx_1n+55}" y="{cy_1n-box_h/2-10}" font-family="\'Space Grotesk\',sans-serif" font-size="13" font-weight="700" fill="#1e2bfa">1</text>')

    svg.append(_entity_box(cx_nn, cy_nn, box_w, box_h, *side_nn))
    svg.append(_entity_box(cx_center, cy_center, box_w, box_h, *center))
    svg.append(_entity_box(cx_1n, cy_1n, box_w, box_h, *side_1n))
    svg.append(_diamond(dia1_x, dia1_y, 110, 60, rel_nn))
    svg.append(_diamond(dia2_x, dia2_y, 110, 60, rel_1n))

    svg.append("</svg>")
    return "".join(svg)


def erd_slide(tag, title, h2, center, side_nn, side_1n, rel_nn, rel_1n, note=None):
    diagram = erd_diagram_svg(center, side_nn, side_1n, rel_nn, rel_1n)
    note_html = f'<p class="code-explain" style="margin-top:.6rem;">{note}</p>' if note else ""
    return f"""
    <div class="slide layout-code">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        <div style="display:flex;justify-content:center;align-items:center;flex:1;">{diagram}</div>
        {note_html}
      </div>
    </div>"""


def mcq_sample_slide(tag, title, h2, samples):
    """samples: list of (question, options[4], correctIndex) — minh hoạ vài câu mẫu, đáp án tô sẵn."""
    blocks = []
    for q, opts, ci in samples:
        opts_html = "".join(
            f'<div style="display:flex;gap:8px;align-items:baseline;{"font-weight:700;color:#1e2bfa;" if i==ci else "color:#444;"}">'
            f'<span>{LETTERS_ERD[i]}.</span><span>{esc(o)}</span>{" <span style=\"font-size:.75rem;\">✔ Đáp án đúng</span>" if i==ci else ""}</div>'
            for i, o in enumerate(opts)
        )
        blocks.append(f'''
          <div class="code-panel" style="background:#fff;border-left:4px solid var(--primary);color:#111;">
            <div style="text-transform:none;letter-spacing:normal;font-family:'Space Grotesk',sans-serif;font-size:.92rem;font-weight:600;color:#111;margin-bottom:8px;">{esc(q)}</div>
            <div style="display:flex;flex-direction:column;gap:5px;font-size:.85rem;font-family:Inter,sans-serif;">{opts_html}</div>
          </div>''')
    return f"""
    <div class="slide layout-code">
      <div class="slide-header">
        <h4>{esc(title)}</h4>
        <span class="tag">{esc(tag)}</span>
      </div>
      <div class="slide-content">
        <h2>{esc(h2)}</h2>
        {''.join(blocks)}
      </div>
    </div>"""

LETTERS_ERD = "ABCD"


def quote_slide(text, source):
    return f"""
    <div class="slide layout-quote">
      <div class="quote-decoration"></div>
      <div class="quote-decoration-2"></div>
      <div class="quote-mark">&ldquo;</div>
      <blockquote>{esc(text)}</blockquote>
      <p class="quote-source"><strong>{esc(source)}</strong></p>
    </div>"""


def closing_slide(title, sub, cta_text, cta_href, contact):
    return f"""
    <div class="slide layout-closing">
      <div class="closing-decoration"></div>
      <div class="closing-decoration-2"></div>
      <div class="accent-line" style="margin: 0 auto 1.5rem;"></div>
      <h1>{esc(title)}</h1>
      <p class="closing-sub">{esc(sub)}</p>
      <a href="{cta_href}" class="cta-btn">{esc(cta_text)}</a>
      <p class="closing-contact">{contact}</p>
    </div>"""


def build_deck(slides, out_path, head_path, foot_path, page_title,
                practice_href=None, practice_label="🧪 Luyện tập chủ đề này"):
    head = open(head_path, encoding="utf-8").read()
    head = head.replace("<title>Presentation Template</title>", f"<title>{esc(page_title)}</title>")
    foot = open(foot_path, encoding="utf-8").read()
    if practice_href:
        pin = f'<a class="practice-pin" href="{practice_href}">{practice_label}</a>'
    else:
        pin = ""
    foot = foot.replace("{{PRACTICE_LINK}}", pin)
    body = "\n  <div class=\"deck\">\n" + "\n".join(slides) + "\n\n  </div>\n"
    doc = head + "\n</head>\n<body>\n" + body + foot
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print("WROTE", out_path, f"({len(slides)} slides)")
