from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector

application = Flask(__name__)
application.secret_key = "abc"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='perpustakaan_shoffan') # x ganti pake nama databasenya

@application.route('/')

@application.route('/index')
def index():
    kalimat='Ini kalimat dari python'
    return render_template('index.html',kalimat_tampil=kalimat)

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@application.route('/anggota')  
def anggota():                  
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from anggota" 
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('anggota.html',kalimat=output_json) 

@application.route('/anggotaAdd', methods=['GET', 'POST']) 
def anggotaAdd():							
    if request.method == 'GET':
        return render_template('anggotaAdd.html')		
    elif request.method =='POST':
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']

        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = "INSERT INTO `anggota` (`kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`) VALUES ('"+kode+"', '"+nama+"', '"+jk+"','"+jurusan+"', '"+hp+"', '"+alamat+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data added successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('anggota'))	

@application.route('/anggotaUpdate/<int:id>', methods=['GET', 'POST'])
def anggotaUpdate(id):
    if request.method == 'GET':

        db = getMysqlConnection()
        try:
            sqlstr = "SELECT * from anggota WHERE id_anggota='"+str(id)+"';"
            print(sqlstr)
            cur = db.cursor()
            cur.execute(sqlstr)
            output_json = cur.fetchall()
            print(output_json)
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('anggotaUpdate.html',kalimat=output_json)
        
    elif request.method == 'POST':
        kode = request.form['kode']			
        nama = request.form['nama']				
        jk = request.form['jk']
        jurusan = request.form['jurusan']
        hp = request.form['hp']
        alamat = request.form['alamat']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = "UPDATE `anggota` SET `kode_anggota` = '"+kode+"', `nama_anggota` = '"+nama+"', `jk_anggota` = '"+jk+"', `jurusan_anggota` = '"+jurusan+"', `no_telp_anggota` = '"+hp+"', `alamat_anggota` = '"+alamat+"' WHERE `anggota`.`id_anggota` = "+str(id)+";"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data updated successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('anggota'))

    return render_template('anggota.html')

@application.route('/anggotaDelete/<int:id>', methods=['GET'])
def anggotaDelete(id):
    if request.method == 'GET':
        db = getMysqlConnection()
        try:
            sqlstr = "DELETE FROM `anggota` WHERE `anggota`.`id_anggota` = "+str(id)
            print(sqlstr)
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data deleted successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('anggota'))

    return render_template('anggota.html')


@application.route('/tables')  
def tables():                 
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from list_materi" # x ganti pake nama tabelnya
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('tables.html',kalimat=output_json) # nama file html sesuain aja

@application.route('/insert', methods=['GET', 'POST'])  # nama route sesuain aja, taro dimana aja asal dibawahnya route utama
def insert():								# nama fungsi sesuain juga
    if request.method == 'GET':
        return render_template('insert.html')		# nama file html sesuain juga
    elif request.method =='POST':
        materi = request.form['materi']			# art_name sebelah kiri = variabel buat di python, art_name sebelah kanan = samain kaya di html
        tanggal = request.form['tanggal']				# nama variabel dan jumlahnya sesuain aja
        content = request.form['content']

        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = "INSERT INTO `list_materi` (`materi`, `tanggal`, `konten`) VALUES ('"+materi+"', '"+tanggal+"', '"+content+"');"
		# nama tabel, field, variabel sesuain, jumlahnya juga. Kalau di database ada timestamp pake current_timestamp(), kalo gada hapus aja.
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data added successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('tables'))	
        # return render_template('insert.html')		# nama file html sesuain

@application.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':

        db = getMysqlConnection()
        try:
            sqlstr = "SELECT * from list_materi WHERE id='"+str(id)+"';"
            print(sqlstr)
            cur = db.cursor()
            cur.execute(sqlstr)
            output_json = cur.fetchall()
            print(output_json)
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('update.html',kalimat=output_json)
        
    elif request.method == 'POST':
        materi = request.form['materi']			
        tanggal = request.form['tanggal']			
        content = request.form['content']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = "UPDATE `list_materi` SET `materi` = '"+materi+"', `tanggal` = '"+tanggal+"', `konten` = '"+content+"' WHERE `list_materi`.`id` = "+str(id)+";"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data updated successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('tables'))

    return render_template('tables.html')

@application.route('/delete/<int:id>', methods=['GET'])
def articleDelete(id):
    if request.method == 'GET':
        db = getMysqlConnection()
        try:
            sqlstr = "DELETE FROM `list_materi` WHERE `list_materi`.`id` = "+str(id)
            print(sqlstr)
            cur = db.cursor()
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            flash('Data deleted successfully','success')
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('tables'))

    return render_template('tables.html')

if __name__ == '__main__':
    application.run(debug=True)