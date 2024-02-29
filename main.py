from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pertemuan4'

# konfigurasi agar main.py dapat mengakses database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'database_baru'

# deklarasi mysql 
mysql = MySQL(app)

# route untuk ke halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('mahasiswa'))
    return render_template('login.html')

# route untuk halaman mahasiswa
@app.route('/mahasiswa')
def mahasiswa(): #fungsi ini mengambil semua data dari database bernama 'mahasiswa'
    cursor = mysql.connection.cursor() #melakukan koneksi ke databse
    cursor.execute(''' SELECT * FROM mahasiswa ''') #memilih semua data dari database
    mahasiswa = cursor.fetchall() #setelah data di ambil semua, dimasukkan kedalam variabel mahasisiwa
    cursor.close() #close database
    
    return render_template('mahasiswa.html', mahasiswa=mahasiswa) #mereturn ke laman mahasiswa setelah membaca data dalam database

# route untuk halaman daftar matkul
@app.route('/mahasiswa/mata_kuliah')
def matakuliah(): #fungsi ini menambil semua data matkul dalam database
    cursor = mysql.connection.cursor() #melakukan koneksi ke database
    cursor.execute(''' SELECT * FROM mata_kuliah ''') #men select semua data matkul dalam database
    mata_kuliah = cursor.fetchall() #semua data matkul di masukkan kedalam cariable mata_kuliah
    cursor.close() #database closed
    
    return render_template('mata_kuliah.html', mata_kuliah=mata_kuliah) #render html untuk mata_kuliah

# route untuk tempat input matkul baru
@app.route('/mahasiswa/mata_kuliah/tambah', methods=['GET', 'POST'])
def tambahMataKuliah(): #fungsi untuk menambah daftar matkul
    if request.method == 'POST': #request method POST karena membutuhkan input user
        kode_matakuliah = request.form['kodematkul'] #input kode matkul disimpan dalam variabel kode_matakuliah
        nama_matakuliah = request.form['matkul'] #input nama matkul disimpan dalam variabel nama_matakuliah
        fakultas = request.form['fakultas'] #input fakultas disimpan dalam variabel fakultas
        sks = request.form['sks'] #input sks disimpan dalam variabel sks

        cursor = mysql.connection.cursor() #melakukan koneksi ke database
        cursor.execute('''INSERT INTO mata_kuliah (kode_matkul, nama_mk, fakultas, sks) VALUES (%s, %s, %s, %s)
        ''', (kode_matakuliah, nama_matakuliah, fakultas, sks)) #input dari semua variabel ke dalam database
        mysql.connection.commit() #melakukan submission ke dalam database
        cursor.close() #database closed
        
        return redirect('/mahasiswa/mata_kuliah')
    else:   
        return render_template('tambah_mata_kuliah.html')

# route untuk halaman mengubah/mengedit matakuliah
@app.route('/mahasiswa/mata_kuliah/edit/<int:kode_matkul>', methods=['GET', 'POST']) #menggunakan <int:kode_matkul>. Karena kode matkul merupakan primary key
def editMataKuliah(kode_matkul):
    if request.method == 'POST': #fungsi untuk mengedit matkul
        kode_matakuliah = request.form['kodematkul'] #input kodematkul dimasukkan ke cariabel kode_matakuliah
        nama_matakuliah = request.form['matkul'] #input matkul dimasukkan ke variabel nama_matakuliah
        fakultas = request.form['fakultas'] #input fakultas dimasukkan ke variabel fakultas 
        sks = request.form['sks'] #input sks dimasukkan ke variabel sks

        cursor = mysql.connection.cursor() #melakukan koneksi ke database
        cursor.execute('''UPDATE mata_kuliah SET kode_matkul = %s, nama_mk = %s, fakultas = %s, sks = %s WHERE kode_matkul = %s'''
        , (kode_matakuliah, nama_matakuliah, fakultas, sks, kode_matkul)) #updating data ke database
        mysql.connection.commit() #submission ke database
        cursor.close() # database closed
        
        return redirect('/mahasiswa/mata_kuliah')
    else:   
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul,))
        mata_kuliah = cursor.fetchone()
        cursor.close()

        if mata_kuliah:
            return render_template('edit_mata_kuliah.html', mata_kuliah=mata_kuliah)
        else:
            return "Mata kuliah not found."

# route untuk halaman (double confirm) hapus matakuliah
@app.route('/matakuliah/delete/<int:kode_matkul>', methods=['GET', 'POST'])
def deleteMataKuliah(kode_matkul): #menggunakan <int:kode_matkul>. Karena kode matkul merupakan primary key
    if request.method == 'POST':
        cursor = mysql.connection.cursor() #melakukan koneksi ke database
        cursor.execute("DELETE FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul,)) #eksekusi penghapusan data pada database
        mysql.connection.commit() #melakukan submission data baru ke database
        cursor.close() #database closed
        
        flash('Mata kuliah berhasil dihapus', 'success') #dialog box database dihapus
        
        return redirect(url_for('matakuliah')) #redirect ke laman matakuliah
    else:
        return render_template('hapus_matkul.html', kode_matkul=kode_matkul) #direct ke laman untuk double check dalam penghapusan

if __name__ == '__main__':
    app.run(debug=True, port = '3000')
