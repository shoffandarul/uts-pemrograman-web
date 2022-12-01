from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, Blueprint
import mysql.connector
import urllib.request, json

api = Blueprint('api', __name__)

api.secret_key = "abc"

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

@api.route('/api/')
def my_api():
    return render_template('api.html')

@api.route('/api/v1/anggota')
def api_anggota():
    output_db = getMethod("SELECT * FROM `anggota`")
    anggota = {}
    anggota['anggota'] = []
    for column in output_db:
        content = {'id_nama':column[0], 'nama':column[1], 'kode':column[2], 'jk':column[3], 'jurusan':column[4], 'no_telp':column[5], 'alamat':column[6]}
        anggota['anggota'].append(content)
        content = {}
    return jsonify(anggota)

@api.route('/api/v1/kode-buku')
def api_kode_buku():
    output_db = getMethod("SELECT * FROM `kode_buku`")
    kode_buku = {}
    kode_buku['kode_buku'] = []
    for column in output_db:
        content = {'id_kode':column[0], 'nama':column[1], 'deskripsi':column[2]}
        kode_buku['kode_buku'].append(content)
        content = {}
    return jsonify(kode_buku)

@api.route('/api/v1/peminjaman')
def api_peminjaman():
    output_db = getMethod("SELECT * FROM `peminjaman`")
    peminjaman = {}
    peminjaman['peminjaman'] = []
    for column in output_db:
        content = {'id_peminjaman':column[0], 'tanggal_peminjaman':column[1], 'tanggal_kembali':column[2], 'id_buku':column[3], 'id_anggota':column[4], 'id_petugas':column[5]}
        peminjaman['peminjaman'].append(content)
        content = {}
    return jsonify(peminjaman)

@api.route('/api/v1/pengembalian')
def api_pengembalian():
    output_db = getMethod("SELECT * FROM `pengembalian`")
    pengembalian = {}
    pengembalian['pengembalian'] = []
    for column in output_db:
        content = {'id_pengembalian':column[0], 'tanggal_pengembalian':column[1], 'denda':column[2], 'id_buku':column[3], 'id_anggota':column[4], 'id_petugas':column[5]}
        pengembalian['pengembalian'].append(content)
        content = {}
    return jsonify(pengembalian)

@api.route('/api/v1/petugas')
def api_petugas():
    output_db = getMethod("SELECT * FROM `petugas`")
    petugas = {}
    petugas['petugas'] = []
    for column in output_db:
        content = {'id_petugas':column[0], 'nama':column[1], 'jabatan':column[2], 'no_telp':column[3], 'alamat':column[4]}
        petugas['petugas'].append(content)
        content = {}
    return jsonify(petugas)

@api.route('/api/v1/rak')
def api_rak():
    output_db = getMethod("SELECT * FROM `rak`")
    rak = {}
    rak['rak'] = []
    for column in output_db:
        content = {'id_rak':column[0], 'nama':column[1], 'lokasi':column[2]}
        rak['rak'].append(content)
        content = {}
    return jsonify(rak)

@api.route('/api/v1/relasi-rak-buku')
def api_relasi_rak_buku():
    output_db = getMethod("SELECT * FROM `relasi_rak_buku`")
    relasi_rak_buku = {}
    relasi_rak_buku['relasi_rak_buku'] = []
    for column in output_db:
        content = {'id_relasi':column[0], 'id_rak':column[1], 'id_buku':column[2]}
        relasi_rak_buku['relasi_rak_buku'].append(content)
        content = {}
    return jsonify(relasi_rak_buku)

@api.route('/api/v1/userlist')
def api_userlist():
    output_db = getMethod("SELECT * FROM `userlist`")
    userlist = {}
    userlist['userlist'] = []
    for column in output_db:
        content = {'id_user':column[0], 'username':column[1], 'password':column[2]}
        userlist['userlist'].append(content)
        content = {}
    return jsonify(userlist)

@api.route('/api/v1/buku')
def api_buku():
    output_db = getMethod("SELECT b.id_buku, b.judul_buku, kb.nama_kode, b.penulis_buku, b.penerbit_buku, b.tahun_penerbit, b.stok from buku b inner join kode_buku kb on kb.id_kode = b.id_kode")
    buku = {}
    buku['buku'] = []
    for column in output_db:
        content = {'id_buku':column[0], 'judul':column[1], 'kode':column[2], 'penulis':column[3], 'penerbit':column[4], 'tahun':column[5], 'stok':column[6]}
        buku['buku'].append(content)
        content = {}
    return jsonify(buku)
