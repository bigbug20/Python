from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pyodbc
import requests
import json

conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-BEI8NT7;"
    "Database=KhachHang;"
    "Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)

root = Tk()
root.title("Cập nhật danh mục khách hàng")
root.resizable(height=True, width=False)
root.minsize(900, 400)

# Các label
lb1 = Label(root, text='Danh sách các khách hàng', bg='white', fg='red')
lb1.grid(row=0, column=2)
lb2 = Label(root, text='Mã khách', bg='white')
lb2.grid(row=1, column=0)
lb2 = Label(root, text='Địa chỉ ', bg='white')
lb2.grid(row=1, column=2)
lb2 = Label(root, text='Tên khách', bg='white')
lb2.grid(row=2, column=0)
lb2 = Label(root, text='Điện thoại', bg='white')
lb2.grid(row=2, column=2)

# entry
# Mã khách
ma = IntVar()
etr1 = Entry(root, width=30, textvariable=ma)
etr1.grid(row=1, column=1)
# Địa chỉ
dc = StringVar()
etr2 = Entry(root, width=30, textvariable=dc)
etr2.grid(row=1, column=3)
# Tên khách
ten = StringVar()
etr3 = Entry(root, width=30, textvariable=ten)
etr3.grid(row=2, column=1)
# Điện thoại
sdt = StringVar()
etr4 = Entry(root, width=30, textvariable=sdt)
etr4.grid(row=2, column=3)

# Scrolled Bar
scb1 = ScrolledText(root, width=60, height=10)
scb1.grid(row=3, column=1)


def them():
    try:
        # Thay thế bằng URL của API thêm khách hàng
        url = "http://192.168.1.21:5000/kh/add"

        # Dữ liệu để gửi đến API
        data = {
            "diaChi": dc.get(),
            "tenKhach": ten.get(),
            "sdt": sdt.get()
        }
        # Gửi yêu cầu GET với dữ liệu truyền qua tham số URL
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # Yêu cầu thành công
            print("Thêm khách hàng thành công!")
            hienthi()  # Cập nhật hiển thị danh sách khách hàng sau khi thêm

        else:
            # Xử lý lỗi nếu có
            print("Yêu cầu thêm khách hàng không thành công. Mã trạng thái:",
                  response.status_code)

    except requests.exceptions.RequestException as e:
        # Xử lý lỗi kết nối hoặc yêu cầu
        print("Đã xảy ra lỗi:", e)


def hienthi():
    scb1.delete(1.0, END)

    # Gửi yêu cầu GET đến API để lấy danh sách khách hàng
    url = "http://192.168.1.21:5000/kh/getall"
    response = requests.get(url)

    # Kiểm tra mã trạng thái của phản hồi
    if response.status_code == 200:
        data = response.json()
        for item in data:
            scb1.insert(INSERT, str(item)+"\n")
    else:
        print("Có lỗi xảy ra khi lấy danh sách khách hàng")


def sua():
    try:
        # Lấy thông tin khách hàng từ nguồn dữ liệu
        maKhachN = ma.get()
        tenKhachN = ten.get()
        diaChiN = dc.get()
        dienThoaiN = sdt.get()

        # Tạo dữ liệu
        data = {
            "MaKH": maKhachN,
            "TenKH": tenKhachN,
            "Diachi": diaChiN,
            "SDT": dienThoaiN
        }

        # Gửi yêu cầu PUT đến API để sửa khách hàng
        url = f"http://192.168.1.21:5000/kh/update/{maKhachN}"
        response = requests.put(url, json=data)  # Changed from data=data to json=data

        # Kiểm tra mã trạng thái của phản hồi
        if response.status_code == 200:
            print("Sửa thông tin khách hàng thành công")
            hienthi()  # Gọi hàm hienThi() để hiển thị thông tin sau khi sửa
        else:
            print("Có lỗi xảy ra khi sửa thông tin khách hàng")
    except Exception as e:
        print("Có lỗi xảy ra:", e)


def xoa():
    try:
        mk = ma.get()

        # Gửi yêu cầu DELETE đến API để xóa khách hàng
        url = f"http://192.168.1.21:5000/kh/delete/{mk}"
        response = requests.delete(url)

        # Kiểm tra mã trạng thái của phản hồi
        if response.status_code == 200:
            print("Xóa khách hàng thành công")
            hienthi()
        else:
            print("Có lỗi xảy ra khi xóa khách hàng")
    except Exception as e:
        print("Có lỗi xảy ra:", e)


# button
btn1 = Button(root, text='Thêm', width=10, command=them)
btn1.grid(row=4, column=0)
btn2 = Button(root, text='Sửa', width=10, command=sua)
btn2.grid(row=4, column=1)
btn3 = Button(root, text='Xóa', width=10, command=xoa)
btn3.grid(row=4, column=2)
btn4 = Button(root, text='Hiển thị', width=10, command=hienthi)
btn4.grid(row=4, column=3)

root.mainloop()
