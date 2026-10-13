"""Sai sót phát hiện trong tài liệu gốc (hiện trên trang Tài liệu)."""
ERRATA = [
 'Lecture Notes Ví dụ 1.1 (§1.1.1): dữ liệu đã sắp xếp có 14 giá trị; giáo trình in “qU = x₁₁ = 98” nhưng x₁₁ = 89 (các phép tính sau đó dùng đúng 89).',
 'Lecture Notes Ví dụ 1.11 (§1.3.3): “7!/(2!3!2!) = 201” sai; đúng là 5040/24 = 210 số.',
 'Lecture Notes Ví dụ 1.7: “B ∪ C = {2,4,5,6}” sai; với B = {1,…,5}, C = {2,4,6} thì B ∪ C = S = {1,…,6} (đúng như Kreyszig Example 8).',
 'Lecture Notes Ví dụ 1.8: “B ∩ C = {4, 6}” sai; đúng là B ∩ C = {2, 4} ({4, 6} là C ∩ A).',
]
ERRATA += [
 'Lecture Notes Ví dụ 1.31(a): “(c − 5)/0.2 = 1.654” là lỗi in; giá trị tra bảng A8 là z = 1.645 (đã dùng để tính c = 5.329).',
 'Đáp án đề số 1 và 2 (2021–2022, 3TC), Câu 1(b): với a = 9, b = 2 đáp án chính thức là k = −1.702 (và k = −2.758 với a = 4, b = 3): vì b lớn hơn (k + b)/σ·σ nên k âm — tham số của đề chưa hợp lý, nhưng phép tính theo đáp án chính thức vẫn đúng.',
]
ERRATA += [
 'Lecture Notes Ví dụ 1.33: β = (360 − 320 + 0.5)/8 = 5.0625 (giáo trình in “7.5625”); kết quả cuối P ≈ 0.9948 không đổi vì Φ(β) ≈ 1.',
]
ERRATA += [
 'Lecture Notes Ví dụ 3.2(ii): ngưỡng in “x̄ > 25.56” nhưng phần chấp nhận in “x̄ ≤ 25.58”; đúng cả hai là 24 + 1.645·3/√10 = 25.56.',
]
