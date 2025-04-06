CÀI ĐẶT -----------------------------------------------------------------------
Trước khi chạy chương trình, thực hiện cài đặt pip sử dụng lệnh sau:
> pip install python-sat

CHẠY CHƯƠNG TRÌNH -------------------------------------------------------------
Có 2 cách chạy chương trình:

[CÁCH 1: SỬ DỤNG MENU]
- Nhập lệnh sau vào Terminal:
	py main.py
- Lần lượt nhập [số thứ tự] của testcase và thuật toán cần sử dụng để giải testcase theo hướng dẫn của chương trình

[CÁCH 2: SỬ DỤNG ARGUMENTS]
- Nhập lệnh theo cú pháp sau vào Terminal: 
	py main.py [testcase] [thuật toán]
- Trong đó:
	+ [testcase]: nhận giá trị 1, 2 hoặc 3 (số thứ tự của Testcase)
	+ [algorithm]: nhận giá trị:
		> pysat hoặc py: thuật toán của PySAT Solver
		> backtracking hoặc bt: thuật toán Backtracking
		> bruteforce hoặc bf: thuật toán Brute Force