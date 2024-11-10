import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class StudentDatabaseApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Quản lý Tuyển Sinh")

		self.db_name = tk.StringVar(value='students.db')
		self.table_name = tk.StringVar(value='students')

		self.create_widgets()

	def create_widgets(self):
		# Kết nối cơ sở dữ liệu
		connection_frame = tk.Frame(self.root)
		connection_frame.pack(pady=10)

		tk.Label(connection_frame, text="Tên DB:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
		tk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=1, columnspan=2, pady=10)

		# Khung tải dữ liệu
		query_frame = tk.Frame(self.root)
		query_frame.pack(pady=10)

		tk.Label(query_frame, text="Tên bảng:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)
		tk.Button(query_frame, text="Tải Dữ Liệu", command=self.load_data).grid(row=1, columnspan=2, pady=10)

		# Hiển thị dữ liệu với STT
		self.tree = ttk.Treeview(self.root, columns=("STT", "HoTen", "NgaySinh", "Diem", "DieuKien"), show='headings')
		self.tree.heading("STT", text="STT")
		self.tree.heading("HoTen", text="Họ tên")
		self.tree.heading("NgaySinh", text="Ngày sinh")
		self.tree.heading("Diem", text="Điểm")
		self.tree.heading("DieuKien", text="Điều kiện")
		self.tree.pack(pady=10)

		# Khung nhập dữ liệu
		insert_frame = tk.Frame(self.root)
		insert_frame.pack(pady=10)

		self.column1 = tk.StringVar()
		self.column2 = tk.StringVar()
		self.column3 = tk.DoubleVar()

		tk.Label(insert_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)
		tk.Label(insert_frame, text="Ngày sinh:").grid(row=1, column=0, padx=5, pady=5)
		tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)
		tk.Label(insert_frame, text="Điểm:").grid(row=2, column=0, padx=5, pady=5)
		tk.Entry(insert_frame, textvariable=self.column3).grid(row=2, column=1, padx=5, pady=5)

		tk.Button(insert_frame, text="Thêm Sinh Viên", command=self.insert_data).grid(row=3, columnspan=2, pady=10)

		# Nút xóa và cập nhật
		action_frame = tk.Frame(self.root)
		action_frame.pack(pady=10)

		tk.Button(action_frame, text="Xóa Sinh Viên", command=self.delete_data).grid(row=0, column=0, padx=5)
		tk.Button(action_frame, text="Cập nhật Sinh Viên", command=self.update_data).grid(row=0, column=1, padx=5)

	def connect_db(self):
		try:
			self.conn = sqlite3.connect(self.db_name.get())
			self.cur = self.conn.cursor()
			messagebox.showinfo("Thành công", "Kết nối đến cơ sở dữ liệu thành công!")
		except Exception as e:
			messagebox.showerror("Lỗi", f"Lỗi khi kết nối đến cơ sở dữ liệu: {e}")

	def load_data(self):
		try:
			for item in self.tree.get_children():
				self.tree.delete(item)

			self.cur.execute(f"SELECT rowid, HoTen, NgaySinh, Diem, DieuKien FROM {self.table_name.get()}")
			rows = self.cur.fetchall()

			for i, row in enumerate(rows, start=1):
				self.tree.insert("", tk.END, values=(i, row[1], row[2], row[3], row[4]), iid=row[0])  # lưu rowid trong iid
		except Exception as e:
			messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")

	def insert_data(self):
		try:
			hoten = self.column1.get()
			ngaysinh = self.column2.get()
			diem = self.column3.get()
			dieu_kien = "Hợp lệ" if diem >= 18 else "Cần xem xét"

			if hoten and ngaysinh:
				insert_query = f"INSERT INTO {self.table_name.get()} (HoTen, NgaySinh, Diem, DieuKien) VALUES (?, ?, ?, ?)"
				self.cur.execute(insert_query, (hoten, ngaysinh, diem, dieu_kien))
				self.conn.commit()
				messagebox.showinfo("Thành công", "Đã thêm sinh viên thành công!")
				self.load_data()
			else:
				messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
		except Exception as e:
			messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {e}")

	def delete_data(self):
		selected_item = self.tree.selection()
		if not selected_item:
			messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
			return
		try:
			rowid = self.tree.selection()[0]  # Lấy rowid từ mục được chọn
			self.cur.execute(f"DELETE FROM {self.table_name.get()} WHERE rowid=?", (rowid,))
			self.conn.commit()
			messagebox.showinfo("Thành công", "Đã xóa sinh viên thành công!")
			self.load_data()
		except Exception as e:
			messagebox.showerror("Lỗi", f"Lỗi khi xóa dữ liệu: {e}")

	def update_data(self):
		selected_item = self.tree.selection()
		if not selected_item:
			messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để cập nhật!")
			return
		try:
			rowid = self.tree.selection()[0]
			hoten = self.column1.get()
			ngaysinh = self.column2.get()
			diem = self.column3.get()
			dieu_kien = "Hợp lệ" if diem >= 18 else "Cần xem xét"

			if hoten and ngaysinh:
				update_query = f"UPDATE {self.table_name.get()} SET HoTen=?, NgaySinh=?, Diem=?, DieuKien=? WHERE rowid=?"
				self.cur.execute(update_query, (hoten, ngaysinh, diem, dieu_kien, rowid))
				self.conn.commit()
				messagebox.showinfo("Thành công", "Đã cập nhật sinh viên thành công!")
				self.load_data()
			else:
				messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
		except Exception as e:
			messagebox.showerror("Lỗi", f"Lỗi khi cập nhật dữ liệu: {e}")

if __name__ == "__main__":
	root = tk.Tk()
	app = StudentDatabaseApp(root)
	root.mainloop()
