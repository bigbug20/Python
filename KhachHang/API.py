import flask
import pyodbc
conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-BEI8NT7;"
    "Database=KhachHang;"
    "Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)
app = flask.Flask(__name__)


@app.route('/kh/getall', methods=['GET'])
def getAllkh():
    try:
        cursor = conn.cursor()
        cursor.execute("select *from tblKhachHang")
        results = []  # list dict
        keys = []
        # lấy key
        for i in cursor.description:
            keys.append(i[0])  # chứa key
        # lấy values
        for i in cursor.fetchall():
            results.append(dict(zip(keys, i)))
        # chuyển thành json
        resp = flask.jsonify(results)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/kh/add', methods=['POST'])
def addKH():
    try:
        # Lấy dữ liệu từ yêu cầu POST
        data = flask.request.json

        diaChi = data.get("diaChi")
        tenKhach = data.get("tenKhach")
        sdt = data.get("sdt")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO tblKhachHang (DiaChi, TenKH, SDT) VALUES (?, ?, ?)",
                       (diaChi, tenKhach, sdt))
        conn.commit()

        resp = flask.jsonify({"message": "Thêm khách hàng thành công"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

# sua


@app.route('/kh/update/<maKhach>', methods=['PUT'])
def updateKH(maKhach):
    try:
        # Lấy dữ liệu từ yêu cầu PUT
        data = flask.request.json

        tenKhach = data.get("TenKH")
        diaChi = data.get("Diachi")
        sdt = data.get("SDT")

        # Thực hiện câu truy vấn UPDATE vào bảng tblKhachHang
        cursor = conn.cursor()
        cursor.execute("UPDATE tblKhachHang SET Diachi = ?, TenKH = ?, SDT = ? WHERE MaKH = ?",
                       (diaChi, tenKhach, sdt, maKhach))
        conn.commit()

        resp = flask.jsonify({"message": "Cập nhật khách hàng thành công"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


# xoa


@app.route('/kh/delete/<maKhach>', methods=['DELETE'])
def deleteKH(maKhach):
    try:
        # Thực hiện câu truy vấn DELETE vào bảng tblKhachHang
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tblKhachHang WHERE MaKH = ?", (maKhach))
        conn.commit()

        resp = flask.jsonify({"message": "Xóa khách hàng thành công"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        resp = flask.jsonify({"message": "Có lỗi xảy ra khi xóa khách hàng"})
        resp.status_code = 500
        return resp


if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.21')
