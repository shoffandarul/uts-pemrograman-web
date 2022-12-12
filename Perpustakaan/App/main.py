from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector
import urllib.request, json
import requests

application = Flask(__name__)
application.secret_key = "abc"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='uts_shoffandarulmufti')

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

def flashResponse(response):
    if response.status_code == 200:
        flash('Berhasil mendapatkan data!')
    else:
        flash('Gagal mendapatkan data!')

@application.route('/')
@application.route('/index')
def index():
    kalimat='Ini kalimat dari python'
    return render_template('index.html',kalimat_tampil=kalimat)

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ============================================================================== #
#                         Route for Register & Login                             #
# ============================================================================== #

@application.route('/register', methods=['GET', 'POST'])   
def register():							
    if request.method =='POST':
        user = request.form['user']			
        passwd = request.form['passwd']	
        passwd_confirm = request.form['passwd_confirm']

    	# cek password confirmation
        if passwd == passwd_confirm:
            postMethod("INSERT INTO `userlist` (`username`, `password`) VALUES ('"+user+"', '"+passwd+"');", 'User behasil dibuat')
        else:
            flash('Password tidak sama', 'error')
        return redirect(url_for('login'))	
    
    return render_template('register.html')	


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        user = request.form['user']			
        passwd = request.form['passwd']		
        
        db = getMysqlConnection()
        try: 
            cur = db.cursor()
            cur.execute("SELECT * FROM `userlist` WHERE `username` = '"+user+"';")
            userlist = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
            flash('invalid username/password')
            return redirect(url_for('login'))
        finally:
            db.close() 
        
        if str(passwd) == userlist[0][2]:
            return redirect(url_for('dashboard'))
        else:
            flash('invalid username/password')
            return render_template('login.html')
        
    return render_template('login.html')	

# ============================================================================== #
#                                Route for Anggota                               #
# ============================================================================== #
@application.route('/anggota')  
def anggota():
    response = requests.get("http://localhost:8000/api/anggota/all")
    # print("\nJSON:\n", response.json(), "\nResponse: ", response.status_code)
    flashResponse(response)
    return render_template('anggota.html', data=response.json()['results'])

@application.route('/anggotaAdd', methods=['GET', 'POST']) 
def anggotaAdd():		
    if request.method =='POST':
        id = request.form['id']			
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("INSERT INTO `anggota` (`id_anggota`, `kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`) VALUES ('"+id+"', '"+kode+"', '"+nama+"', '"+jk+"','"+jurusan+"', '"+hp+"', '"+alamat+"');", 'Data anggota Berhasil Ditambah')
        return redirect(url_for('anggota'))	

    return render_template('anggotaAdd.html')	

@application.route('/anggotaUpdate/<int:id>', methods=['GET', 'POST'])
def anggotaUpdate(id):
    if request.method == 'POST':
        id_anggota = request.form['id_anggota']	
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("UPDATE `anggota` SET `id_anggota` = '"+id_anggota+"', `kode_anggota` = '"+kode+"', `nama_anggota` = '"+nama+"', `jk_anggota` = '"+jk+"', `jurusan_anggota` = '"+jurusan+"', `no_telp_anggota` = '"+hp+"', `alamat_anggota` = '"+alamat+"' WHERE `anggota`.`id_anggota` = "+str(id)+";", 'Data anggota Berhasil Diubah')
        return redirect(url_for('anggota'))

    response = requests.get("http://localhost:8000/api/anggota/"+str(id))
    flashResponse(response)
    return render_template('anggotaUpdate.html', data=response.json()['results'])

@application.route('/anggotaDelete/<int:id>')
def anggotaDelete(id):
    postMethod("DELETE FROM `anggota` WHERE `anggota`.`id_anggota` = '"+str(id)+"';", 'Data anggota Berhasil Dihapus')
    return redirect(url_for('anggota'))

# ============================================================================== #
#                                Route for Petugas                               #
# ============================================================================== #
@application.route('/petugas')  
def petugas():
    response = requests.get("http://localhost:8000/api/petugas/all")
    flashResponse(response)
    return render_template('petugas.html', data=response.json()['results'])

@application.route('/petugasAdd', methods=['GET', 'POST']) 
def petugasAdd():							
    if request.method =='POST':
        id = request.form['id']					
        nama = request.form['nama']				
        jabatan = request.form['jabatan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("INSERT INTO `petugas` (`id_petugas`, `nama_petugas`, `jabatan_petugas`, `no_telp_petugas`, `alamat_petugas`) VALUES ('"+id+"', '"+nama+"', '"+jabatan+"', '"+hp+"', '"+alamat+"');", 'Data petugas Berhasil Ditambah')
        return redirect(url_for('petugas'))	

    return render_template('petugasAdd.html')	

@application.route('/petugasUpdate/<int:id>', methods=['GET', 'POST'])
def petugasUpdate(id):
    if request.method == 'POST':
        id_petugas = request.form['id_petugas']					
        nama = request.form['nama']				
        jabatan = request.form['jabatan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        postMethod("UPDATE `petugas` SET `id_petugas` = '"+id_petugas+"', `nama_petugas` = '"+nama+"', `jabatan_petugas` = '"+jabatan+"', `no_telp_petugas` = '"+hp+"', `alamat_petugas` = '"+alamat+"' WHERE `petugas`.`id_petugas` = "+str(id)+";", 'Data petugas Berhasil Diubah')
        return redirect(url_for('petugas'))
    
    response = requests.get("http://localhost:8000/api/petugas/"+str(id))
    flashResponse(response)
    return render_template('petugasUpdate.html', data=response.json()['results'])

@application.route('/petugasDelete/<int:id>')
def petugasDelete(id):
    postMethod("DELETE FROM `petugas` WHERE `petugas`.`id_petugas` = '"+str(id)+"';", 'Data petugas Berhasil Dihapus')
    return redirect(url_for('petugas'))

# ============================================================================== #
#                                Route for Buku                                  #
# ============================================================================== #
@application.route('/buku')  
def buku():
    response = requests.get("http://localhost:8000/api/buku/all")
    flashResponse(response)
    return render_template('buku.html', data=response.json()['results'])

@application.route('/buku/<int:id>')
def buku_by_id(id):
    response = requests.get("http://localhost:8000/api/buku/"+str(id))
    flashResponse(response)
    return render_template('buku.html', data=response.json()['results'])

@application.route('/bukuAdd', methods=['GET', 'POST']) 
def bukuAdd():							
    if request.method =='POST':		
        kode = request.form['kode']				
        judul = request.form['judul']			
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        postMethod("INSERT INTO `buku` (`id_kode`, `judul_buku`, `penulis_buku`, `penerbit_buku`, `tahun_penerbit`, `stok`) VALUES ('"+kode+"', '"+judul+"','"+penulis+"', '"+penerbit+"', '"+tahun_terbit+"', '"+stok+"');", 'Data buku Berhasil Ditambah')
        return redirect(url_for('buku'))	

    response = requests.get("http://localhost:8000/api/kode-buku/all")
    return render_template('bukuAdd.html', data=response.json()['results'])

@application.route('/bukuUpdate/<int:id>', methods=['GET', 'POST'])
def bukuUpdate(id):
    if request.method == 'POST':		
        kode = request.form['kode']				
        judul = request.form['judul']			
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        tahun_terbit = request.form['tahun_terbit']
        stok = request.form['stok']
        postMethod("UPDATE `buku` SET `id_kode` = '"+kode+"', `judul_buku` = '"+judul+"', `penulis_buku` = '"+penulis+"', `penerbit_buku` = '"+penerbit+"', `tahun_penerbit` = '"+tahun_terbit+"', `stok` = '"+stok+"' WHERE `buku`.`id_buku` = "+str(id)+";", 'Data buku Berhasil Diubah')
        return redirect(url_for('buku'))
    
    data_lama = requests.get("SELECT * from buku WHERE id_buku='"+str(id)+"';")
    kode_buku = requests.get("SELECT id_kode, nama_kode, deskripsi from kode_buku")
    return render_template('bukuAdd.html', data_lama=data_lama.json()['results'], kode_buku=kode_buku.json()['results'])

@application.route('/bukuDelete/<int:id>')
def bukuDelete(id):
    postMethod("DELETE FROM `buku` WHERE `buku`.`id_buku` = '"+str(id)+"';", 'Data buku Berhasil Dihapus')
    return redirect(url_for('buku'))

# ============================================================================== #
#                                Route for Rak                                   #
# ============================================================================== #
@application.route('/rak')  
def rak():
    response_rak = requests.get("http://localhost:8000/api/rak/all")
    print("\nJSON:\n", response_rak.json(), "\nResponse: ", response_rak.status_code)
    if response_rak.status_code == 200: flash('Berhasil mendapatkan data rak! | ')
    else: flash('Gagal mendapatkan data rak! | ')
    
    response_rel = requests.get("http://localhost:8000/api/relasi-rak-buku/all")
    print("\nJSON:\n", response_rel.json(), "\nResponse: ", response_rel.status_code)
    if response_rel.status_code == 200: flash('Berhasil mendapatkan data buku!')
    else: flash('Gagal mendapatkan data buku!')

    return render_template('rak.html', data_rak=response_rak.json()['results'], data_rel=response_rel.json()['results'])

@application.route('/rakAdd', methods=['GET', 'POST']) 
def rakAdd():							
    if request.method =='POST':
        id_rak = request.form['id_rak']			
        nama = request.form['nama']				
        lokasi = request.form['lokasi']			
        buku = request.form.getlist("buku")
        postMethod("INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`) VALUES ('"+id_rak+"', '"+nama+"', '"+lokasi+"');", 'Data rak Berhasil Ditambah')
        for i in buku:
            postMethod("INSERT INTO `relasi_rak_buku` (`id_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+i+"');", 'success')
            print(i)
        return redirect(url_for('rak'))	
    
    id_buku = requests.get("http://localhost:8000/api/buku/all")
    return render_template('rakAdd.html', id_buku=id_buku.json()['results'])

@application.route('/rakUpdate/<int:id>', methods=['GET', 'POST'])
def rakUpdate(id):
    if request.method == 'POST':
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
    
    data_buku = requests.get("http://localhost:8000/api/buku/all")
    data_rak = requests.get("http://localhost:8000/api/rak/"+str(id))
    data_rel = requests.get("http://localhost:8000/api/relasi-rak-buku/"+str(id))
    return render_template('rakUpdate.html', data_buku=data_buku.json()['results'], data_rak=data_rak.json()['results'], data_rel=data_rel.json()['results'])

@application.route('/rakDelete/<int:id>')
def rakDelete(id):
    postMethod("DELETE FROM `relasi_rak_buku` WHERE `relasi_rak_buku`.`id_relasi` = '"+str(id)+"';", 'Data rak Berhasil Dihapus')
    return redirect(url_for('rak'))


# ============================================================================== #
#                           Route for Peminjaman                                 #
# ============================================================================== #
@application.route('/peminjaman')  
def peminjaman():
    response = requests.get("http://localhost:8000/api/peminjaman/all")
    print("\nJSON:\n", response.json(), "\nResponse: ", response.status_code)
    flashResponse(response)
    return render_template('peminjaman.html', data=response.json()['results'])

@application.route('/peminjamanAdd', methods=['GET', 'POST'])   
def peminjamanAdd():							
    if request.method =='POST':		
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `peminjaman` (`tanggal_peminjaman`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+tanggal_pinjam+"', '"+tanggal_kembali+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data Peminjaman Berhasil Ditambah')
        return redirect(url_for('peminjaman'))	

    id_buku = requests.get("http://localhost:8000/api/buku/all")
    id_anggota = requests.get("http://localhost:8000/api/anggota/all")
    id_petugas = requests.get("http://localhost:8000/api/petugas/all")
    return render_template('peminjamanAdd.html', id_buku = id_buku.json()['results'], id_anggota = id_anggota.json()['results'], id_petugas = id_petugas.json()['results'])


@application.route('/peminjamanUpdate/<int:id>', methods=['GET', 'POST'])
def peminjamanUpdate(id):       
    if request.method == 'POST':		
        tanggal_pinjam = request.form['tanggal_pinjam']			
        tanggal_kembali = request.form['tanggal_kembali']				
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `peminjaman` SET `tanggal_peminjaman` = '"+tanggal_pinjam+"', `tanggal_kembali` = '"+tanggal_kembali+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `peminjaman`.`id_peminjaman` = "+str(id)+"; ", 'Data Peminjaman Berhasil Diubah')
        return redirect(url_for('peminjaman'))
    
    data_lama = requests.get("http://localhost:8000/api/peminjaman/"+str(id))
    id_buku = requests.get("http://localhost:8000/api/buku/all")
    id_anggota = requests.get("http://localhost:8000/api/anggota/all")
    id_petugas = requests.get("http://localhost:8000/api/petugas/all")
    return render_template('peminjamanUpdate.html', data_lama = data_lama.json()['results'], id_buku = id_buku.json()['results'], id_anggota = id_anggota.json()['results'], id_petugas = id_petugas.json()['results'])


@application.route('/peminjamanDelete/<int:id>')
def peminjamanDelete(id):
    postMethod("DELETE FROM `peminjaman` WHERE `peminjaman`.`id_peminjaman` = '"+str(id)+"';", 'Data Peminjaman Berhasil Dihapus')
    return redirect(url_for('peminjaman'))

# ============================================================================== #
#                             Route for Pengembalian                             #
# ============================================================================== #
@application.route('/pengembalian')  
def pengembalian():
    response = requests.get("http://localhost:8000/api/pengembalian/all")
    print("\nJSON:\n", response.json(), "\nResponse: ", response.status_code)
    flashResponse(response)
    return render_template('pengembalian.html', data=response.json()['results'])

@application.route('/pengembalianAdd', methods=['GET', 'POST']) 
def pengembalianAdd():							
    if request.method =='POST':	
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("INSERT INTO `pengembalian` (`tanggal_pengembalian`, `denda`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+tanggal_kembali+"', '"+denda+"','"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');", 'Data pengembalian Berhasil Ditambah')
        return redirect(url_for('pengembalian'))	

    id_buku = requests.get("http://localhost:8000/api/buku/all")
    id_anggota = requests.get("http://localhost:8000/api/anggota/all")
    id_petugas = requests.get("http://localhost:8000/api/petugas/all")
    return render_template('pengembalianAdd.html', id_buku = id_buku.json()['results'], id_anggota = id_anggota.json()['results'], id_petugas = id_petugas.json()['results'])


@application.route('/pengembalianUpdate/<int:id>', methods=['GET', 'POST'])
def pengembalianUpdate(id):
    if request.method == 'POST':		
        tanggal_kembali = request.form['tanggal_kembali']				
        denda = request.form['denda']			
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        postMethod("UPDATE `pengembalian` SET `tanggal_pengembalian` = '"+tanggal_kembali+"', `denda` = '"+denda+"', `id_buku` = '"+id_buku+"', `id_anggota` = '"+id_anggota+"', `id_petugas` = '"+id_petugas+"' WHERE `pengembalian`.`id_pengembalian` = "+str(id)+";", 'Data pengembalian Berhasil Diubah')
        return redirect(url_for('pengembalian'))

    data_lama = requests.get("http://localhost:8000/api/pengembalian/"+str(id))
    id_buku = requests.get("http://localhost:8000/api/buku/all")
    id_anggota = requests.get("http://localhost:8000/api/anggota/all")
    id_petugas = requests.get("http://localhost:8000/api/petugas/all")
    return render_template('pengembalianUpdate.html', data_lama = data_lama.json()['results'], id_buku = id_buku.json()['results'], id_anggota = id_anggota.json()['results'], id_petugas = id_petugas.json()['results'])


@application.route('/pengembalianDelete/<int:id>', methods=['GET'])
def pengembalianDelete(id):
    postMethod("DELETE FROM `pengembalian` WHERE `pengembalian`.`id_pengembalian` = '"+str(id)+"';", 'Data pengembalian Berhasil Dihapus')
    return redirect(url_for('pengembalian'))


if __name__ == '__main__':
    application.run(debug=True)