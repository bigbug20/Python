from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
import pyodbc
import requests

conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-BEI8NT7;"
    "Database=BKCAD_SinhVien;"
    "Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)

root = Tk()
root.title("Quản lý học viên")
root.resizable(height=True, width=False)
root.minsize(1000, 600)
# Label
lb1 = Label(root, text='CHƯƠNG TRÌNH QUẢN LÝ HỌC VIÊN', bg='white')
lb1.grid(row=0, column=1)
# ID
lb7 = Label(root, text='ID', bg='white')
lb7.grid(row=1, column=2)
maHV = IntVar()
etr7 = Entry(root, width=30, textvariable=maHV)
etr7.grid(row=2, column=2)

# tên
lb2 = Label(root, text='Name', bg='white')
lb2.grid(row=1, column=0)
name = StringVar()
etr1 = Entry(root, width=30, textvariable=name)
etr1.grid(row=1, column=1)

# tuổi
lb3 = Label(root, text='Age', bg='white')
lb3.grid(row=2, column=0)
age = IntVar()
etr2 = Entry(root, width=30, textvariable=age)
etr2.grid(row=2, column=1)

# tp
lb4 = Label(root, text='Country', bg='white')
lb4.grid(row=3, column=0)
city = StringVar()
etr3 = Entry(root, width=30, textvariable=city)
etr3.grid(row=3, column=1)

# sex
lb4 = Label(root, text='Sex', bg='white')
lb4.grid(row=4, column=0)
sex = StringVar()
sex.set('Nam')
cbB1 = Combobox(root, textvariable=sex)
cbB1['value'] = ('Nam', 'Nữ', 'Không')
cbB1.grid(row=4, column=1)

# in4
lb5 = Label(root, text='Infomation', bg='white')
lb5.grid(row=5, column=0)
info = StringVar()
etr4 = Entry(root, width=30, textvariable=info)
etr4.grid(row=5, column=1)

# English
lb6 = Label(root, text='English', bg='white')
lb6.grid(row=6, column=0)
eng = StringVar()
etr5 = Entry(root, width=30, textvariable=eng)
etr5.grid(row=6, column=1)
# scoll
etr6 = Entry(root, width=30)
etr6.grid(row=9, column=1)
scb1 = ScrolledText(root, width=60, height=10)
scb1.grid(row=10, column=1)


def them():
    try:
        url = "http://192.168.100.6:5000/hv/add"

        data = {
            "ten": name.get(),
            "tuoi": age.get(),
            "diachi": city.get(),
            "gioitinh": sex.get(),
            "info": info.get(),
            "english": eng.get()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Thêm khách hàng thành công!")
            etr6.delete(0, END)
            etr6.insert(INSERT, "Đã Thêm")

        else:
            print("Yêu cầu thêm khách hàng không thành công. Mã trạng thái:",
                  response.status_code)

    except requests.exceptions.RequestException as e:
        print("Đã xảy ra lỗi:", e)


def hienthi():
    scb1.delete(1.0, END)

    # Gửi yêu cầu GET đến API để lấy danh sách khách hàng
    url = "http://192.168.100.6:5000/hv/getall"
    response = requests.get(url)

    # Kiểm tra mã trạng thái của phản hồi
    if response.status_code == 200:
        data = response.json()
        for item in data:
            scb1.insert(INSERT, str(item)+"\n")
    else:
        print("Có lỗi xảy ra khi lấy danh sách học viên")


def sua():
    try:
        maHVN = maHV.get()
        data = {
            "ten": name.get(),
            "tuoi": age.get(),
            "diachi": city.get(),
            "gioitinh": sex.get(),
            "info": info.get(),
            "english": eng.get()
        }

        url = f"http://192.168.100.6:5000/hv/update/{maHVN}"

        response = requests.put(url, json=data)

        if response.status_code == 200:
            print("Sửa thông tin học viên thành công")
            etr6.delete(0, END)
            etr6.insert(INSERT, "Đã Sửa")
        else:
            print("Có lỗi xảy ra khi sửa thông tin học viên")
    except Exception as e:
        print("Có lỗi xảy ra:", e)


def xoa():
    try:
        mk = maHV.get()

        url = f"http://192.168.100.6:5000/hv/delete/{mk}"
        response = requests.delete(url)

        if response.status_code == 200:
            print("Xóa học viên thành công")
            etr6.delete(0, END)
            etr6.insert(INSERT, "Đã Xóa")
        else:
            print("Có lỗi xảy ra khi xóa học viên")
    except Exception as e:
        print("Có lỗi xảy ra:", e)


def test():
    scb1.delete(1.0, END)
    scb1.insert(INSERT, "Connect Successfull")


# button
btn1 = Button(root, text='Thêm Học Viên', width=20, command=them)
btn1.grid(row=7, column=0)
btn2 = Button(root, text='Sửa Học Viên', width=20, command=sua)
btn2.grid(row=7, column=1)
btn3 = Button(root, text='Xóa Học Viên', width=20, command=xoa)
btn3.grid(row=8, column=0)
btn4 = Button(root, text='Hiển thị Học Viên', width=20, command=hienthi)
btn4.grid(row=8, column=1)
btn5 = Button(root, text='Kiểm tra kết nối', width=20, command=test)
btn5.grid(row=11, column=1)
root.mainloop()
