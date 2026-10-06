"""Trang chủ."""
import os
from helpers import *

def body(MODULES, reps, roadmap_fig):
    ready = {m['key'] for m in MODULES if os.path.exists(os.path.join(os.path.dirname(__file__), 'c_' + m['key'] + '.py'))}
    b = '<p class="tag">HỌC PHẦN CSE703057 · ĐẠI HỌC PHENIKAA</p><h1>Tối ưu hóa phi tuyến và tối ưu lồi</h1>'
    b += ('<p class="lead">Bộ bài giảng tự học 4 module, bám sát 3 slide chính khóa của ORLab (tập lồi và hàm lồi; bài toán có ràng buộc và KKT; quy hoạch toàn phương) '
          'và giáo trình Boyd &amp; Vandenberghe. Mỗi module có deck slide, ví dụ có lời giải, công cụ tương tác, và ngân hàng câu hỏi có giải thích.</p>')
    b += '<div class="grid">'
    for m in MODULES:
        rep = reps.get(m['key'])
        cnt = f'<p><span class="badge ok">{rep["n_total"]} câu hỏi</span></p>' if rep else ''
        if m['key'] in ready:
            b += f'<a class="mod-card" href="modules/{m["slug"]}/index.html"><span class="tag">MODULE {m["num"]}</span><h3>{m["title"]}</h3><p>{m["short"]}</p>{cnt}<p><b>Mở bài giảng →</b></p></a>'
        else:
            b += f'<div class="mod-card" style="opacity:.55;cursor:default;border:1px dashed var(--border);border-radius:14px;padding:16px"><span class="tag">MODULE {m["num"]}</span><h3>{m["title"]}</h3><p>{m["short"]}</p><p><i>Sắp có</i></p></div>'
    b += '</div>'
    b += '<h2>Lộ trình</h2>' + roadmap_fig
    b += callout('info', 'Cách học gợi ý', '<ol><li>Xem deck từng phần (phím ← →), mở “📖 Giải thích cho người mới” khi chưa rõ.</li><li>Đọc “Ví dụ chi tiết” và tự làm lại trước khi xem lời giải.</li><li>Thử các công cụ tương tác (Hessian, KKT, active set…).</li><li>Làm ngân hàng câu hỏi: trắc nghiệm có giải thích ngay, điền số, tự luận có đáp án mẫu; có nút làm lại từng câu và làm lại toàn bộ.</li></ol>')
    b += callout('warn', 'Về độ tin cậy', '<p>Nội dung chính bám <b>3 slide trong thư mục Slides</b> và đề cương chính thức. Các tài liệu Studocu (đề/bài tập giữa kỳ, giáo trình BTDOC) rất cũ và thuộc ngành khác, chỉ dùng để <b>tham khảo</b>, được gắn nhãn riêng; không suy ra cấu trúc đề thi thật. '
                                    'Khi kiểm chứng bằng code, một số chỗ trong slide chưa khớp — xem trang <a href="kiem-chung/index.html">Kiểm chứng</a>.</p>')
    b += '<div class="foot">Tiến độ làm bài lưu trong trình duyệt của bạn (localStorage); xóa dữ liệu duyệt web sẽ mất tiến độ. Không có máy chủ.</div>'
    return b
