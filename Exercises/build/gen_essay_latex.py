# -*- coding: utf-8 -*-
# Sinh file LaTeX cho 12 cau tu luan tu chinh data/essays.json (nguon duy nhat, khong go tay lai).
import json, os

BASE = "/Users/tuannghiat/Downloads/for-Vinh-Exercises"
OUT = "/Users/tuannghiat/Downloads/Phenikaa - Cơ sở dữ liệu/TU_LUAN_CSDL_ERD_TRIGGER_CHUAN_HOA.tex"

essays = json.load(open(os.path.join(BASE, "data", "essays.json"), encoding="utf-8"))

def esc(s):
    if s is None:
        return ""
    return (s.replace("\\", "\\textbackslash{}")
             .replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")
             .replace("_", "\\_").replace("{", "\\{").replace("}", "\\}"))

def multiline(s):
    # Giữ xuống dòng trong prompt/model answer bằng \\ của LaTeX
    return esc(s).replace("\n", "\\\\\n")

PREAMBLE = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{vietnam}
\usepackage[margin=2.2cm]{geometry}
\usepackage{xcolor}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{listings}
\usepackage[most]{tcolorbox}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{titlesec}

\definecolor{navy}{HTML}{16324f}
\definecolor{teal}{HTML}{0f766e}
\definecolor{tealbg}{HTML}{f0fdfa}
\definecolor{navybg}{HTML}{eef2f7}
\definecolor{ink}{HTML}{1a1a1a}
\definecolor{graytext}{HTML}{555555}
\definecolor{linegray}{HTML}{c7ccd1}
\definecolor{warnbg}{HTML}{fff4ec}
\definecolor{warnborder}{HTML}{c2410c}
\definecolor{resultbg}{HTML}{fbfbfb}

\color{ink}
\hypersetup{colorlinks=true, linkcolor=teal, urlcolor=teal,
  pdftitle={Tu Luan CSDL - ERD, Trigger, Chuan hoa - Phenikaa},
  pdfauthor={Phenikaa CSDL}}

\titleformat{\section}{\Large\bfseries\color{navy}}{\thesection}{0.6em}{}[{\color{teal}\titlerule[1.1pt]}]

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\small\color{graytext}Tự luận CSDL -- ERD, Trigger, Chuẩn hóa}
\fancyhead[R]{\small\color{graytext}\thepage}

\newtcolorbox{problembox}[1]{enhanced, colback=navybg, colframe=navy,
  fonttitle=\bfseries\color{white}, coltitle=white, title=#1, arc=2pt, boxrule=1pt,
  top=7pt, bottom=7pt, left=9pt, right=9pt}
\newtcolorbox{ideabox}[1]{enhanced, colback=tealbg, colframe=teal,
  fonttitle=\bfseries\color{white}, coltitle=white, title=#1, arc=2pt, boxrule=1pt,
  top=7pt, bottom=7pt, left=9pt, right=9pt}
\newtcolorbox{resultbox}[1]{enhanced, colback=resultbg, colframe=graytext,
  fonttitle=\bfseries\itshape\color{white}, coltitle=white, title=#1, arc=2pt, boxrule=0.8pt,
  top=6pt, bottom=6pt, left=9pt, right=9pt}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{0.5cm}
    {\small\color{graytext} ĐẠI HỌC PHENIKAA}\\[2pt]
    {\small\color{graytext} KHOA CÔNG NGHỆ THÔNG TIN}\\[0.8cm]
    {\color{teal}\rule{0.5\linewidth}{1.4pt}}\\[1.6cm]
    {\Huge \bfseries \color{navy} BÀI TẬP TỰ LUẬN}\\[0.35cm]
    {\Huge \bfseries \color{navy} CƠ SỞ DỮ LIỆU}\\[0.7cm]
    {\large \color{teal} \bfseries ERD -- MÔ HÌNH QUAN HỆ -- TRIGGER/VIEW -- CHUẨN HÓA -- KHÓA}\\[2cm]

    \begin{tcolorbox}[enhanced,colback=navybg,colframe=navy,arc=3pt,boxrule=1pt,width=0.86\linewidth,top=10pt,bottom=10pt]
        \centering
        \textbf{Bám sát cấu trúc:} Phần Tự luận của đề thi thật (BM.ĐBCL.17.1c) -- thiết kế ERD,
        chuyển mô hình quan hệ, dự đoán hành vi TRIGGER/VIEW.\\[4pt]
        \textbf{Cách dùng:} Tự làm trước ra giấy nháp theo đúng thang điểm, rồi mới xem đáp án mẫu.\\[4pt]
        \textbf{Bản tương tác:} 12 câu này cũng có trên website luyện tập, mục "Tự Luận".
    \end{tcolorbox}
    \vfill
    {\large \textbf{\color{graytext}Hà Nội -- 2026}}
\end{titlepage}

\tableofcontents
\newpage
"""

FOOTER = r"""
\end{document}
"""

parts = [PREAMBLE]

for i, q in enumerate(essays, start=1):
    stars = "★" * q["difficulty"] + "☆" * (3 - q["difficulty"])
    rubric_items = "\n".join(
        f"    \\item {esc(r['criterion'])} \\textbf{{({r['points']} điểm)}}" for r in q["rubric"]
    )
    parts.append(f"""
% ======================================================================
\\section{{Câu {i} -- {esc(q['title'])}}}

\\begin{{problembox}}{{Đề bài ({stars} · {esc(q['topic'])} · thang điểm {q['totalPoints']})}}
{multiline(q['prompt'])}
\\end{{problembox}}

\\begin{{ideabox}}{{Gợi ý cách trình bày}}
{multiline(q['guidance'])}
\\end{{ideabox}}

\\textbf{{Đáp án mẫu:}}

{multiline(q['modelAnswer'])}

\\begin{{resultbox}}{{Thang điểm chi tiết (tổng {q['totalPoints']} điểm)}}
\\begin{{itemize}}[leftmargin=*]
{rubric_items}
\\end{{itemize}}
\\end{{resultbox}}

\\newpage
""")

parts.append(FOOTER)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))

print("WROTE:", OUT)
print("So cau:", len(essays))
