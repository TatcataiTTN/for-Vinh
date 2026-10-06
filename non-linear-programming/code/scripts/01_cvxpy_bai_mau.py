"""01 — Bài mẫu trong file 'tam thoi la vay.docx' (đã dọn code và giải thích từng dòng).

Bài toán:  min (x-3)^2 + (y-4)^2 - 2   với   x^2 + y^2 <= 36,  x >= 0,  y >= 0.
Chạy:      python3 01_cvxpy_bai_mau.py
Cần:       pip install cvxpy numpy
"""
import cvxpy as cp

# 1) Biến quyết định (hai số thực)
x = cp.Variable()
y = cp.Variable()

# 2) Hàm mục tiêu: tổng hai bình phương trừ 2 -> hàm LỒI (Hessian = 2I, xác định dương)
objective = cp.Minimize((x - 3) ** 2 + (y - 4) ** 2 - 2)

# 3) Ràng buộc: x^2 + y^2 <= 36 là hình tròn bán kính 6 (tập lồi); x, y >= 0 là hai nửa mặt phẳng
constraints = [x ** 2 + y ** 2 <= 36, x >= 0, y >= 0]

problem = cp.Problem(objective, constraints)

# 4) Kiểm tra bài toán thuộc lớp "lồi theo quy tắc DCP" -> cvxpy mới đảm bảo nghiệm toàn cục
print("is_dcp (bài toán lồi theo quy tắc DCP):", problem.is_dcp())

# 5) Giải. KHÔNG cần qcp=True: qcp dành cho bài toán tựa lồi (quasiconvex), còn đây đã là bài toán lồi thường.
problem.solve()

print("Giá trị nhỏ nhất của f(x, y):", round(problem.value, 6))
print("x =", round(float(x.value), 6), " y =", round(float(y.value), 6))

# 6) Nhân tử Lagrange (cvxpy gọi là dual_value), cùng quy ước với L = f + sum(lambda_i * g_i), lambda_i >= 0
for name, c in zip(["x^2+y^2<=36", "x>=0", "y>=0"], constraints):
    print(f"nhân tử của {name:12s}: {abs(float(c.dual_value)):.6f}")

# 7) Kiểm tra bằng tay (3 dòng, thay cho bảng dài):
#    - Cực tiểu KHÔNG ràng buộc của (x-3)^2 + (y-4)^2 - 2 là (3, 4), giá trị -2.
#    - Điểm (3, 4) có x^2 + y^2 = 25 <= 36 và x, y > 0 => thỏa mọi ràng buộc, không ràng buộc nào chặt.
#    - Ràng buộc lỏng => mọi nhân tử bằng 0 (điều kiện bù) => nghiệm bài toán có ràng buộc = (3, 4), f* = -2.
