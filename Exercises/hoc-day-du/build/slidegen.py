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


def build_deck(slides, out_path, head_path, foot_path, page_title):
    head = open(head_path, encoding="utf-8").read()
    head = head.replace("<title>Presentation Template</title>", f"<title>{esc(page_title)}</title>")
    foot = open(foot_path, encoding="utf-8").read()
    body = "\n  <div class=\"deck\">\n" + "\n".join(slides) + "\n\n  </div>\n"
    doc = head + "\n</head>\n<body>\n" + body + foot
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print("WROTE", out_path, f"({len(slides)} slides)")
