from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import datetime
import uvicorn

app = FastAPI()

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_pelanggaran_siswa'
}

# Model Pydantic untuk data siswa
class Siswa(BaseModel):
    nis: str
    nama: str
    kelas: str
    hportu: str

    class Config:
        arbitrary_types_allowed = True

class Pelanggaran(BaseModel):
    tgljam: datetime
    idsiswa: int
    pelanggaran: str

    class Config:
        arbitrary_types_allowed = True

def get_all_siswa():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Siswa")
        siswa_list = cursor.fetchall()
        return siswa_list
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fungsi untuk menambahkan siswa baru ke database
def tambah_siswa(siswa: Siswa):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Siswa (nis, nama, kelas, hportu) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (siswa.nis, siswa.nama, siswa.kelas, siswa.hportu))
        connection.commit()
        return True
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fungsi untuk mendapatkan daftar semua pelanggaran dari database
def get_all_pelanggaran():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pelanggaran")
        pelanggaran_list = cursor.fetchall()
        return pelanggaran_list
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fungsi untuk menambahkan pelanggaran baru ke database
def tambah_pelanggaran(pelanggaran: Pelanggaran):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Pelanggaran (tgljam, idsiswa, pelanggaran) VALUES (%s, %s, %s)"
        cursor.execute(query, (pelanggaran.tgljam, pelanggaran.idsiswa, pelanggaran.pelanggaran))
        connection.commit()
        return True
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fungsi untuk menghitung total siswa dari database
def count_total_siswa():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_siswa FROM Siswa")
        total_siswa = cursor.fetchone()["total_siswa"]
        return total_siswa
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fungsi untuk menghitung total pelanggaran dari database
def count_total_pelanggaran():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_pelanggaran FROM Pelanggaran")
        total_pelanggaran = cursor.fetchone()["total_pelanggaran"]
        return total_pelanggaran
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint API untuk mendapatkan seluruh data siswa
@app.get('/siswa', response_model=list[Siswa])
def read_all_siswa():
    return get_all_siswa()

# Endpoint API untuk menambahkan siswa baru
@app.post('/siswa')
def create_siswa(siswa: Siswa):
    if tambah_siswa(siswa):
        return {"message": "Siswa berhasil ditambahkan"}
    else:
        raise HTTPException(status_code=500, detail="Gagal menambahkan siswa")

# Endpoint API untuk mendapatkan seluruh data pelanggaran
@app.get('/pelanggaran', response_model=list[Pelanggaran])
def read_all_pelanggaran():
    return get_all_pelanggaran()

# Endpoint API untuk menambahkan pelanggaran baru
@app.post('/pelanggaran')
def create_pelanggaran(pelanggaran: Pelanggaran):
    if tambah_pelanggaran(pelanggaran):
        return {"message": "Pelanggaran berhasil ditambahkan"}
    else:
        raise HTTPException(status_code=500, detail="Gagal menambahkan pelanggaran")

# Endpoint API untuk mendapatkan total siswa
@app.get('/total-siswa')
def get_total_siswa():
    total_siswa = count_total_siswa()
    return {"total_siswa": total_siswa}

# Endpoint API untuk mendapatkan total pelanggaran
@app.get('/total-pelanggaran')
def get_total_pelanggaran():
    total_pelanggaran = count_total_pelanggaran()
    return {"total_pelanggaran": total_pelanggaran}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
