from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from myAPI import *
import mysql.connector
import urllib.request, json

application = Flask(__name__)
application.secret_key = "abc"

application.register_blueprint(api)

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
        
def getData(url):
    response = urllib.request.urlopen(url)
    content = response.read()
    output = json.loads(content) 
    # print(output)
    return output

@application.route('/')

@application.route('/index')
def index():
    kalimat='Ini kalimat dari python'
    return render_template('index.html',kalimat_tampil=kalimat)

@application.route('/register', methods=['GET', 'POST'])   
def register():							
    if request.method == 'GET':
        return render_template('register.html')	
    elif request.method =='POST':
        user = request.form['user']			
        passwd = request.form['passwd']	
        passwd_confirm = request.form['passwd_confirm']

    	# cek password confirmation
        if passwd == passwd_confirm:
            postMethod("INSERT INTO `userlist` (`username`, `password`) VALUES ('"+user+"', '"+passwd+"');", 'User behasil dibuat')
        else:
            flash('Password tidak sama', 'error')
        return render_template('register.html')		


@application.route('/login', methods=['GET', 'POST'])
def login():
    userlist = getMethod("SELECT * FROM `userlist`")
    if request.method == 'GET':
        return render_template('login.html')	
    elif request.method =='POST':
        user = request.form['user']			
        passwd = request.form['passwd']		
        	
        for kolom in userlist:
            for i in range(len(kolom)):
                if str(user) == kolom[i]:
                    if str(passwd) == kolom[i+1]:
                        return redirect(url_for('dashboard'))
                    else:
                        break
        flash('invalid username/password', 'error')
        return render_template('login.html')

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@application.route('/peminjaman')
def peminjaman():
    output = getData(f"http://127.0.0.1:5000/api/v1/peminjaman")
    flash('Data peminjaman berhasil didapatkan!', 'success')
    return render_template('peminjaman.html', data=output['peminjaman'])

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
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `peminjaman` (`tanggal_peminjaman`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+tanggal_pinjam+"', '"+tanggal_kembali+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data Peminjaman Berhasil Ditambah')
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
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `peminjaman` SET `tanggal_peminjaman` = '"+tanggal_pinjam+"', `tanggal_kembali` = '"+tanggal_kembali+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `peminjaman`.`id_peminjaman` = "+str(id)+"; ", 'Data Peminjaman Berhasil Diubah')
        return redirect(url_for('peminjaman'))

@application.route('/peminjamanDelete/<int:id>', methods=['GET'])
def peminjamanDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `peminjaman` WHERE `peminjaman`.`id_peminjaman` = '"+str(id)+"';", 'Data Peminjaman Berhasil Dihapus')
        return redirect(url_for('peminjaman'))

@application.route('/pengembalian')
def pengembalian():
    output = getData(f"http://127.0.0.1:5000/api/v1/pengembalian")
    flash('Data pengembalian berhasil didapatkan!', 'success')
    return render_template('pengembalian.html', data=output['pengembalian'])

@application.route('/pengembalianAdd', methods=['GET', 'POST']) 
def pengembalianAdd():							
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
        id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
        return render_template('pengembalianAdd.html', id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
    elif request.method =='POST':	
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `pengembalian` (`tanggal_pengembalian`, `denda`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+tanggal_kembali+"', '"+denda+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data pengembalian Berhasil Ditambah')
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
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `pengembalian` SET `tanggal_pengembalian` = '"+tanggal_kembali+"', `denda` = '"+denda+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `pengembalian`.`id_pengembalian` = "+str(id)+";", 'Data pengembalian Berhasil Diubah')
        return redirect(url_for('pengembalian'))

@application.route('/pengembalianDelete/<int:id>', methods=['GET'])
def pengembalianDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `pengembalian` WHERE `pengembalian`.`id_pengembalian` = '"+str(id)+"';", 'Data pengembalian Berhasil Dihapus')
        return redirect(url_for('pengembalian'))

@application.route('/buku')
def buku():
    output = getData(f"http://127.0.0.1:5000/api/v1/buku")
    flash('Data buku berhasil didapatkan!', 'success')
    return render_template('buku.html', data=output['buku'])

@application.route('/buku/id/<int:id>', methods=['GET'])
def buku_by_id(id):
    output = getData(f"http://127.0.0.1:5000/api/v1/buku/id/"+str(id))
    flash('Data buku '+str(id)+'  berhasil didapatkan!', 'success')
    return render_template('buku.html', data=output['buku'])

@application.route('/buku/insert', methods=['GET', 'POST']) 
def buku_insert():							
    if request.method == 'GET':
        output = getData(f"http://127.0.0.1:5000/api/v1/kode-buku")
        return render_template('bukuAdd.html', data=output['kode_buku'])	
    elif request.method =='POST':
        api_buku_insert()
        return redirect(url_for('buku'))

# @application.route('/bukuAdd', methods=['GET', 'POST']) 
# def bukuAdd():							
#     if request.method == 'GET':
#         kode_buku = getMethod("SELECT id_kode, nama_kode, deskripsi from kode_buku")
#         return render_template('bukuAdd.html', kode_buku=kode_buku)	
#     elif request.method =='POST':		
#         kode = request.form['kode']				
#         judul = request.form['judul']			
#         penulis = request.form['penulis']
#         penerbit = request.form['penerbit']
#         tahun_terbit = request.form['tahun_terbit']
#         stok = request.form['stok']
#         postMethod("INSERT INTO `buku` (`id_kode`, `judul_buku`, `penulis_buku`, `penerbit_buku`, `tahun_penerbit`, `stok`) VALUES ('"+kode+"', '"+judul+"','"+penulis+"', '"+penerbit+"', '"+tahun_terbit+"', '"+stok+"');", 'Data buku Berhasil Ditambah')
#         return redirect(url_for('buku'))	

@application.route('/bukuUpdate/<int:id>', methods=['GET', 'POST'])
def bukuUpdate(id):
    if request.method == 'GET':
        data_lama = getMethod("SELECT * from buku WHERE id_buku='"+str(id)+"';")
        kode_buku = getMethod("SELECT id_kode, nama_kode, deskripsi from kode_buku")
        return render_template('bukuUpdate.html', data_lama = data_lama, kode_buku=kode_buku)	
    elif request.method == 'POST':		
        kode = request.form['kode']				
        judul = request.form['judul']			
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        postMethod("UPDATE `buku` SET `id_kode` = '"+kode+"', `judul_buku` = '"+judul+"', `penulis_buku` = '"+penulis+"', `penerbit_buku` = '"+penerbit+"', `tahun_penerbit` = '"+tahun_terbit+"', `stok` = '"+stok+"' WHERE `buku`.`id_buku` = "+str(id)+";", 'Data buku Berhasil Diubah')
        return redirect(url_for('buku'))

@application.route('/bukuDelete/<int:id>', methods=['GET'])
def bukuDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `buku` WHERE `buku`.`id_buku` = '"+str(id)+"';", 'Data buku Berhasil Dihapus')
        return redirect(url_for('buku'))
    return render_template('buku.html')

@application.route('/rak')
def rak():
    output = getData(f"http://127.0.0.1:5000/api/v1/rak")
    flash('Data rak berhasil didapatkan!', 'success')
    return render_template('rak.html', data=output['rak'])

@application.route('/rakAdd', methods=['GET', 'POST']) 
def rakAdd():							
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        return render_template('rakAdd.html', id_buku = id_buku_json)
    elif request.method =='POST':
        id_rak = request.form['id_rak']			
        nama = request.form['nama']				
        lokasi = request.form['lokasi']			
        buku = request.form.getlist("buku")
        postMethod("INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`) VALUES ('"+id_rak+"', '"+nama+"', '"+lokasi+"');", 'Data rak Berhasil Ditambah')
        for i in buku:
            postMethod("INSERT INTO `relasi_rak_buku` (`id_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+i+"');", 'success')
            print(i)
        return redirect(url_for('rak'))	

@application.route('/rakUpdate/<int:id>', methods=['GET', 'POST'])
def rakUpdate(id):
    if request.method == 'GET':
        id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
        data_rak = getMethod("SELECT * from rak WHERE id_rak='"+str(id)+"';")
        return render_template('rakUpdate.html', data_buku = id_buku_json, data_rak = data_rak)	
    elif request.method == 'POST':
        id_rak = request.form['id_rak']			
        nama = request.form['nama']				
        lokasi = request.form['lokasi']			
        buku = request.form.getlist("buku")
        postMethod("UPDATE `rak` SET `id_rak` = '"+str(id_rak)+"', `nama_rak` = '"+nama+"', `lokasi_rak` = '"+lokasi+"' WHERE `rak`.`id_rak` = "+str(id_rak)+";", 'Data rak Berhasil Diubah')
        postMethod("DELETE FROM `relasi_rak_buku` WHERE `relasi_rak_buku`.`id_rak` = '"+str(id)+"';", 'Data rak Berhasil Diubah')
        for i in buku:
            postMethod("INSERT INTO `relasi_rak_buku` (`id_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+i+"');", 'success')
            print(i)
        return redirect(url_for('rak'))	

@application.route('/rakDelete/<int:id>', methods=['GET'])
def rakDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `relasi_rak_buku` WHERE `relasi_rak_buku`.`id_relasi` = '"+str(id)+"';", 'Data rak Berhasil Dihapus')
        return redirect(url_for('rak'))
    return render_template('rak.html')

@application.route('/anggota')  
def anggota():
    output = getData(f"http://127.0.0.1:5000/api/v1/anggota") 
    flash('Data anggota berhasil didapatkan!', 'success')
    return render_template('anggota.html', data=output['anggota'])

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
        postMethod("INSERT INTO `anggota` (`id_anggota`, `kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`) VALUES ('"+id+"', '"+kode+"', '"+nama+"', '"+jk+"','"+jurusan+"', '"+hp+"', '"+alamat+"');", 'Data anggota Berhasil Ditambah')
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
        postMethod("UPDATE `anggota` SET `id_anggota` = '"+id_anggota+"', `kode_anggota` = '"+kode+"', `nama_anggota` = '"+nama+"', `jk_anggota` = '"+jk+"', `jurusan_anggota` = '"+jurusan+"', `no_telp_anggota` = '"+hp+"', `alamat_anggota` = '"+alamat+"' WHERE `anggota`.`id_anggota` = "+str(id)+";", 'Data anggota Berhasil Diubah')
        return redirect(url_for('anggota'))

@application.route('/anggotaDelete/<int:id>', methods=['GET'])
def anggotaDelete(id):
    if request.method == 'GET':
        postMethod("DELETE FROM `anggota` WHERE `anggota`.`id_anggota` = '"+str(id)+"';", 'Data anggota Berhasil Dihapus')
        return redirect(url_for('anggota'))

@application.route('/petugas')  
def petugas():
    output = getData(f"http://127.0.0.1:5000/api/v1/petugas")
    flash('Data petugas berhasil didapatkan!', 'success')
    return render_template('petugas.html', data=output['petugas'])

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