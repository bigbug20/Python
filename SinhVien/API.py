import flask
import pyodbc
conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-BEI8NT7;"
    "Database=BKCAD_SinhVien;"
    "Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)
app = flask.Flask(__name__)


@app.route('/hv/getall', methods=['GET'])
def getAllkh():
    try:
        cursor = conn.cursor()
        cursor.execute("select *from HocVien")
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


@app.route('/hv/add', methods=['POST'])
def addKH():
    try:
        data = flask.request.json

        TenHV = data.get("ten")
        Tuoi = data.get("tuoi")
        DiaChi = data.get("diachi")
        GioiTinh = data.get("gioitinh")
        Info = data.get("info")
        English = data.get("english")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO HocVien (Ten,Tuoi,DiaChi,GioiTinh,Info,English) VALUES (?, ?, ?, ?, ?, ?)",
                       (TenHV, Tuoi, DiaChi, GioiTinh, Info, English))
        conn.commit()

        resp = flask.jsonify({"message": "Thêm học viên thành công"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/hv/update/<maHV>', methods=['PUT'])
def updateKH(maHV):
    try:
        data = flask.request.json

        TenHV = data.get("ten")
        Tuoi = data.get("tuoi")
        DiaChi = data.get("diachi")
        GioiTinh = data.get("gioitinh")
        Info = data.get("info")
        English = data.get("english")

        cursor = conn.cursor()
        cursor.execute("UPDATE HocVien Set Ten=?,Tuoi=?,DiaChi=?,GioiTinh=?,Info=?,English=? WHERE MaHV =?",
                       (TenHV, Tuoi, DiaChi, GioiTinh, Info, English, maHV))
        conn.commit()

        resp = flask.jsonify({"message": "Cập nhật học viên thành công"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/hv/delete/<maHV>', methods=['DELETE'])
def deleteKH(maHV):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM HocVien WHERE MaHV = ?", (maHV))
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
    app.run(debug=True, host='192.168.100.6')
