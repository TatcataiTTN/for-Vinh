from drawio_util import D
import os
ROOT = os.path.join(os.path.dirname(__file__), '..')
d = D(1000, 520)
d.text(20, 8, 960, 34, 'Bản đồ ôn tập: câu hỏi đề thi ↔ module', 22, True)
rows = [('Giữa kỳ (HK2 22–23)', 'blue', ['C1 Bayes → M4', 'C2 bảng phân phối → M5', 'C3 chuẩn + nhị thức → M6', 'C4 khoảng tin cậy t → M8']),
        ('Giữa kỳ mẫu', 'green', ['Đếm → M2', 'P(Ā), nhị thức → M3', 'Bayes, k → M4, M5', 'chuẩn, t_α, CI → M6, M8']),
        ('Cuối kỳ 3TC (HK2, 2024)', 'orange', ['C1 chuẩn → M6', 'C2 CI → M8', 'C3 kiểm định → M10', 'C4 tương quan/hồi quy → M13', 'C5 mật độ/MLE → M5, M7']),
        ('Cuối kỳ 2TC (HK1)', 'yellow', ['C1 bảng PP → M5', 'C2 CI t → M8', 'C3 kiểm định → M10', 'C4 hồi quy → M13'])]
y = 70
for name, col, items in rows:
    d.box(20, y, 210, 80, name, 'dark', 15, True)
    x = 250
    for it in items:
        d.box(x, y + 6, 150, 68, it, col, 13, True); x += 158
    y += 100
d.save(os.path.join(ROOT, 'drawio', 'm09.drawio'), os.path.join(ROOT, 'img', 'm09.png'))
