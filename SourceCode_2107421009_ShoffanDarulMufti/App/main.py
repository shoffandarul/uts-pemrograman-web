from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector

application = Flask(__name__)
application.secret_key = "abc"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='uts_shoffandarulmufti')

def getMethod(sqlstr):
    db = getMysqlConnection()
    try: 
        cur = db.cursor()
        print(sqlstr)
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close() 
    return output_json

def postMethod(sqlstr, message):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        print(sqlstr)
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        flash(message,'success')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()

@application.route('/')

@application.route('/index')
def index():
    kalimat='Ini kalimat dari python'
    return render_template('index.html',kalimat_tampil=kalimat)

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@application.route('/peminjaman')
def peminjaman():
    output_json = getMethod("SELECT * from peminjaman")
    return render_template('peminjaman.html',kalimat=output_json)

@application.route('/peminjamanAdd', methods=['GET', 'POST'])   
def peminjamanAdd():							
    if request.method == 'GET':
        # contoh form yang ada relasinya, dia ngambil data dulu dari tabel yang ada primary key
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
        id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
        # terus di lempar ke html peminjamanAdd, line 179 - 203, udah gitu aja :)
        return render_template('peminjamanAdd.html', id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
    elif request.method =='POST':
        id = request.form['id']			
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `peminjaman` (`id_peminjaman`, `tanggal_peminjaman`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id+"', '"+tanggal_pinjam+"', '"+tanggal_kembali+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data Peminjaman Berhasil Ditambah')
        return redirect(url_for('peminjaman'))	

@application.route('/peminjamanUpdate/<int:id>', methods=['GET', 'POST'])
def peminjamanUpdate(id):
    if request.method == 'GET':
        data_lama = getMethod("SELECT * from peminjaman WHERE id_peminjaman='"+str(id)+"';")
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
        id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
        return render_template('peminjamanUpdate.html', data_lama = data_lama, id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
    elif request.method == 'POST':
        id_peminjaman = request.form['id_peminjaman']			
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `peminjaman` SET `id_peminjaman` = '"+id_peminjaman+"', `tanggal_peminjaman` = '"+tanggal_pinjam+"', `tanggal_kembali` = '"+tanggal_kembali+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `peminjaman`.`id_peminjaman` = "+str(id)+"; ", 'Data Peminjaman Berhasil Diubah')
        return redirect(url_for('peminjaman'))

@application.route('/peminjamanDelete/<int:id>', methods=['GET'])
def peminjamanDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `peminjaman` WHERE `peminjaman`.`id_peminjaman` = '"+str(id)+"';", 'Data Peminjaman Berhasil Dihapus')
        return redirect(url_for('peminjaman'))

@application.route('/pengembalian')
def pengembalian():
    output_json = getMethod("SELECT * from pengembalian")
    return render_template('pengembalian.html',kalimat=output_json)

@application.route('/pengembalianAdd', methods=['GET', 'POST']) 
def pengembalianAdd():							
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
        id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
        return render_template('pengembalianAdd.html', id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
    elif request.method =='POST':
        id = request.form['id']			
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `pengembalian` (`id_pengembalian`, `tanggal_pengembalian`, `denda`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id+"', '"+tanggal_kembali+"', '"+denda+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data pengembalian Berhasil Ditambah')
        return redirect(url_for('pengembalian'))	

@application.route('/pengembalianUpdate/<int:id>', methods=['GET', 'POST'])
def pengembalianUpdate(id):
    if request.method == 'GET':
        data_lama = getMethod("SELECT * from pengembalian WHERE id_pengembalian='"+str(id)+"';")
        print(data_lama)
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
        id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
        return render_template('pengembalianUpdate.html', data_lama = data_lama, id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
    elif request.method == 'POST':
        id = request.form['id']			
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `pengembalian` SET `id_pengembalian` = '"+id+"', `tanggal_pengembalian` = '"+tanggal_kembali+"', `denda` = '"+denda+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `pengembalian`.`id_pengembalian` = "+str(id)+";", 'Data pengembalian Berhasil Diubah')
        return redirect(url_for('pengembalian'))

@application.route('/pengembalianDelete/<int:id>', methods=['GET'])
def pengembalianDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `pengembalian` WHERE `pengembalian`.`id_pengembalian` = '"+str(id)+"';", 'Data pengembalian Berhasil Dihapus')
        return redirect(url_for('pengembalian'))

@application.route('/buku')
def buku():
    output_json = getMethod("SELECT * from buku")
    return render_template('buku.html',kalimat=output_json)

@application.route('/bukuAdd', methods=['GET', 'POST']) 
def bukuAdd():							
    if request.method == 'GET':
        return render_template('bukuAdd.html')	
    elif request.method =='POST':
        id = request.form['id']			
        kode = request.form['kode']				
        judul = request.form['judul']			
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        postMethod("INSERT INTO `buku` (`id_buku`, `kode_buku`, `judul_buku`, `penulis_buku`, `penerbit_buku`, `tahun_penerbit`, `stok`) VALUES ('"+id+"', '"+kode+"', '"+judul+"','"+penulis+"', '"+penerbit+"', '"+tahun_terbit+"', '"+stok+"');", 'Data buku Berhasil Ditambah')
        return redirect(url_for('buku'))	

@application.route('/bukuUpdate/<int:id>', methods=['GET', 'POST'])
def bukuUpdate(id):
    if request.method == 'GET':
        data_lama = getMethod("SELECT * from buku WHERE id_buku='"+str(id)+"';")
        return render_template('bukuUpdate.html', data_lama = data_lama)	
    elif request.method == 'POST':
        id = request.form['id']			
        kode = request.form['kode']				
        judul = request.form['judul']			
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        postMethod("UPDATE `buku` SET `id_buku` = '"+id+"', `kode_buku` = '"+kode+"', `judul_buku` = '"+judul+"', `penulis_buku` = '"+penulis+"', `penerbit_buku` = '"+penerbit+"', `tahun_penerbit` = '"+tahun_terbit+"', `stok` = '"+stok+"' WHERE `buku`.`id_buku` = "+str(id)+";", 'Data buku Berhasil Diubah')
        return redirect(url_for('buku'))

@application.route('/bukuDelete/<int:id>', methods=['GET'])
def bukuDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `buku` WHERE `buku`.`id_buku` = '"+str(id)+"';", 'Data buku Berhasil Dihapus')
        return redirect(url_for('buku'))
    return render_template('buku.html')

@application.route('/rak')
def rak():
    output_json = getMethod("SELECT * from rak")
    return render_template('rak.html',kalimat=output_json)

@application.route('/rakAdd', methods=['GET', 'POST']) 
def rakAdd():							
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        return render_template('rakAdd.html', id_buku = id_buku_json)
    elif request.method =='POST':
        id = request.form['id']			
        nama = request.form['nama']				
        lokasi = request.form['lokasi']			
        id_buku = request.form['id_buku']
        postMethod("INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`, `id_buku`) VALUES ('"+id+"', '"+nama+"', '"+lokasi+"','"+id_buku+"');", 'Data rak Berhasil Ditambah')
        return redirect(url_for('rak'))	

@application.route('/rakUpdate/<int:id>', methods=['GET', 'POST'])
def rakUpdate(id):
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        data_lama = getMethod("SELECT * from rak WHERE id_rak='"+str(id)+"';")
        return render_template('rakUpdate.html', id_buku = id_buku_json, data_lama = data_lama)	
    elif request.method == 'POST':
        id = request.form['id']			
        nama = request.form['nama']				
        lokasi = request.form['lokasi']			
        id_buku = request.form['id_buku']
        postMethod("UPDATE `rak` SET `id_rak` = '"+id+"', `nama_rak` = '"+nama+"', `lokasi_rak` = '"+lokasi+"', `id_buku` = '"+id_buku+"' WHERE `rak`.`id_rak` = "+str(id)+";", 'Data rak Berhasil Diubah')
        return redirect(url_for('rak'))

@application.route('/rakDelete/<int:id>', methods=['GET'])
def rakDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `rak` WHERE `rak`.`id_rak` = '"+str(id)+"';", 'Data rak Berhasil Dihapus')
        return redirect(url_for('rak'))
    return render_template('rak.html')

@application.route('/anggota')  
def anggota():                  
    output_json = getMethod("SELECT * from anggota")
    print(output_json)
    return render_template('anggota.html',kalimat=output_json) 

@application.route('/anggotaAdd', methods=['GET', 'POST']) 
def anggotaAdd():							
    if request.method == 'GET':
        return render_template('anggotaAdd.html')		
    elif request.method =='POST':
        id = request.form['id']			
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        genre = request.form.getlist("genre")
        genre_arr = ', '.join(genre)
        postMethod("INSERT INTO `anggota` (`id_anggota`, `kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`, `genre_buku`) VALUES ('"+id+"', '"+kode+"', '"+nama+"', '"+jk+"','"+jurusan+"', '"+hp+"', '"+alamat+"', '"+genre_arr+"');", 'Data anggota Berhasil Ditambah')
        return redirect(url_for('anggota'))	

@application.route('/anggotaUpdate/<int:id>', methods=['GET', 'POST'])
def anggotaUpdate(id):
    if request.method == 'GET':
        output_json = getMethod("SELECT * from anggota WHERE id_anggota='"+str(id)+"';")
        return render_template('anggotaUpdate.html',kalimat=output_json)
        
    elif request.method == 'POST':
        id_anggota = request.form['id_anggota']	
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        genre = request.form.getlist("genre")
        genre_arr = ', '.join(genre)
        postMethod("UPDATE `anggota` SET `id_anggota` = '"+id_anggota+"', `kode_anggota` = '"+kode+"', `nama_anggota` = '"+nama+"', `jk_anggota` = '"+jk+"', `jurusan_anggota` = '"+jurusan+"', `no_telp_anggota` = '"+hp+"', `alamat_anggota` = '"+alamat+"', `genre_buku` = '"+genre_arr+"' WHERE `anggota`.`id_anggota` = "+str(id)+";", 'Data anggota Berhasil Diubah')
        return redirect(url_for('anggota'))

@application.route('/anggotaDelete/<int:id>', methods=['GET'])
def anggotaDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `anggota` WHERE `anggota`.`id_anggota` = '"+str(id)+"';", 'Data anggota Berhasil Dihapus')
        return redirect(url_for('anggota'))

@application.route('/petugas')  
def petugas():                  
    output_json = getMethod("SELECT * from petugas")
    return render_template('petugas.html',kalimat=output_json) 

@application.route('/petugasAdd', methods=['GET', 'POST']) 
def petugasAdd():							
    if request.method == 'GET':
        return render_template('petugasAdd.html')		
    elif request.method =='POST':
        id = request.form['id']					
        nama = request.form['nama']				
        jabatan = request.form['jabatan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("INSERT INTO `petugas` (`id_petugas`, `nama_petugas`, `jabatan_petugas`, `no_telp_petugas`, `alamat_petugas`) VALUES ('"+id+"', '"+nama+"', '"+jabatan+"', '"+hp+"', '"+alamat+"');", 'Data petugas Berhasil Ditambah')
        return redirect(url_for('petugas'))	

@application.route('/petugasUpdate/<int:id>', methods=['GET', 'POST'])
def petugasUpdate(id):
    if request.method == 'GET':
        output_json = getMethod("SELECT * from petugas WHERE id_petugas='"+str(id)+"';")
        return render_template('petugasUpdate.html',kalimat=output_json)
    elif request.method == 'POST':
        id_petugas = request.form['id_petugas']					
        nama = request.form['nama']				
        jabatan = request.form['jabatan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("UPDATE `petugas` SET `id_petugas` = '"+id_petugas+"', `nama_petugas` = '"+nama+"', `jabatan_petugas` = '"+jabatan+"', `no_telp_petugas` = '"+hp+"', `alamat_petugas` = '"+alamat+"' WHERE `petugas`.`id_petugas` = "+str(id)+";", 'Data petugas Berhasil Diubah')
        return redirect(url_for('petugas'))

@application.route('/petugasDelete/<int:id>', methods=['GET'])
def petugasDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `petugas` WHERE `petugas`.`id_petugas` = '"+str(id)+"';", 'Data petugas Berhasil Dihapus')
        return redirect(url_for('petugas'))

if __name__ == '__main__':
    application.run(debug=True)