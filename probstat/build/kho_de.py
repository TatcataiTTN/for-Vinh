"""Trang 'Kho đề': mọi bộ đề, phạm vi, hình thức, số lượng, đáp án và lộ trình ôn, xếp ở một chỗ."""
import html
from hx import callout, ul, table
from sitelib import page, write, load_bank
from modules import MODS

def build():
    tot_q = tot_e = 0
    for m in MODS:
        try: b = load_bank(m['id'])
        except FileNotFoundError: continue
        tot_q += len(b['items']); tot_e += len(b['essays'])
    L = lambda href, t: f'<a href="{href}">{t}</a>'
    rows = [
        ['<b>1. Đề giữa kỳ thật HK2.2 2025–2026</b> (10 mã đề) + 30 mã mới cùng mẫu', 'M1–M8', '8 câu điền đáp số (0,5đ) + 1 tự luận (6đ), 60 phút', '40 mã đề', 'Chấm tự động, lời giải câu 9 · ' + L('../de-thi-that-hk22/index.html', 'Làm đề')],
        ['2. Đề giữa kỳ mẫu + đáp án giữa kỳ HK2 2022–2023', 'M1–M8', 'Đề mẫu 9 câu; đáp án 4 câu tham số hóa', '1 đề mẫu + 1 bộ đáp án', L('../cau-truc-de/index.html', 'Đối chiếu đáp án chính thức') + ' · ' + L('../m09-on-tap-giua-ky/index.html', 'Module 9')],
        ['3. Đề cuối kỳ gốc (2021–22 HK1 3TC; 2022–23 HK1 2TC và HK2 3TC; đề mẫu 03/2024)', 'M5–M13', '4–5 câu tự luận', '4 bộ đề', L('../cau-truc-de/index.html', 'Cấu trúc đề') + ' (đáp án chính thức đã tính lại)'],
        ['4. Đề giữa kỳ tự soạn lần 1', 'M1–M3 (mục 1.1–1.5)', '8 câu ngắn + 1 tự luận', '3 đề', L('../de-giua-ky/index.html', 'Mở đề') + ' · đáp án khóa mật khẩu'],
        ['5. Đề giữa kỳ tự soạn lần 2 (trọng tâm Bayes và biến ngẫu nhiên)', 'M1–M5 (mục 1.1–1.9)', '8 câu ngắn + 2 bài tự luận', '3 đề', L('../de-giua-ky-2/index.html', 'Mở đề') + ' · đáp án khóa mật khẩu'],
        ['6. Bài mẫu tự luận có lời giải từng bước', 'M1, M4, M5', 'Deck 24 slide: chép đề, tự làm, tập chữa', '3 bài + 3 bài tương tự', L('../bai-mau-tu-luan/index.html', 'Mở deck')],
        ['7. Luyện đề trắc nghiệm', 'M1–M13', '15 câu, 30 phút, có điểm và giải thích', '12 đề', L('../luyen-de/index.html', 'Làm đề') + ' (đề 9–12 theo khung giữa kỳ)'],
        ['8. Ngân hàng câu hỏi theo module', 'M1–M13', 'Trắc nghiệm có giải thích + tự luận', f'{tot_q} câu trắc nghiệm, {tot_e} bài tự luận', L('../index.html#lo-trinh', 'Chọn module')]]
    tb = '<div style="overflow:auto">' + table(['Bộ đề', 'Phạm vi', 'Hình thức', 'Số lượng', 'Đáp án / liên kết'], rows, 'left') + '</div>'
    plan = ul([
        '<b>Bước 1 · Học kiến thức:</b> slide và quiz của <a href="../index.html#lo-trinh">Module 1–8</a>, xem <a href="../bang-tra/index.html">bảng tra</a> cho Φ, U_α, t_α.',
        '<b>Bước 2 · Học cách làm tự luận:</b> <a href="../bai-mau-tu-luan/index.html">3 bài mẫu</a> (chép đề, tự làm, đối chiếu từng bước, làm bài tương tự).',
        '<b>Bước 3 · Làm đề thật:</b> 10 mã đề HK2.2 <a href="../de-thi-that-hk22/index.html">bấm giờ 60 phút</a>; sai dạng nào thì quay về bảng “chín dạng câu” trên trang đó.',
        '<b>Bước 4 · Mở rộng:</b> 30 mã đề mới cùng mẫu, đề tự soạn <a href="../de-giua-ky-2/index.html">lần 2</a>, và <a href="../luyen-de/index.html">luyện đề trắc nghiệm</a> 9–12.',
        '<b>Bước 5 · Sửa lỗi:</b> ghi lại lỗi mỗi lần làm (số học, quên n − 1, đọc nhầm U<sub>α</sub> và U<sub>α/2</sub>); làm lại các câu sai sau 1 ngày.'], True)
    body = f'''<div class="crumbs"><a href="../index.html">Trang chủ</a> › Kho đề</div>
<h1>Kho đề thi và luyện đề</h1>
<p class="lead">Mọi bộ đề ở một chỗ, xếp từ sát đề thật nhất đến luyện mở rộng. Mỗi bộ ghi rõ phạm vi (module), hình thức, số lượng và nơi xem đáp án.</p>
{callout('good', 'Đề thi giữa kỳ học kỳ này', '<p>10 mã đề HK2.2 2025–2026 cùng một khung 9 câu, chỉ đổi số. Học một mã đề là học cả mười: xem <a href="../de-thi-that-hk22/index.html">bảng chín dạng câu và làm đề tại đây</a>.</p>')}
<h2>Các bộ đề</h2>{tb}
<h2>Lộ trình ôn giữa kỳ gợi ý</h2>{plan}
<p style="font-size:.85rem;color:var(--muted)">Ghi chú: các đề tự soạn và mã đề mới là đề do người biên soạn tạo theo khung đề thật; đề thật và đề mẫu lấy từ tài liệu của học phần. Đáp án số do chương trình tính và đối chiếu độc lập.</p>'''
    write('vi/kho-de/index.html', page('Kho đề thi', body, 2, 'Tất cả bộ đề: đề thật HK2.2, đề mẫu, đề tự soạn, bài mẫu và luyện đề', math=False))
    print('kho-de ok', tot_q, 'câu', tot_e, 'tự luận')
