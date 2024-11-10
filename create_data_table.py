import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('students.db')

# Tạo đối tượng con trỏ để thực hiện các thao tác SQL
c = conn.cursor()

# Tạo bảng "students" với các cột: id, HoTen, NgaySinh, Diem, DieuKien
c.execute('''
	CREATE TABLE IF NOT EXISTS students (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		HoTen TEXT NOT NULL,
		NgaySinh TEXT NOT NULL,
		Diem REAL NOT NULL,
		DieuKien TEXT NOT NULL
	)
''')

# Lưu thay đổi
conn.commit()

# Đóng kết nối
conn.close()

print("Database và bảng 'students' đã được tạo thành công với các cột bổ sung.")
