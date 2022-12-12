import uvicorn
from fastapi import FastAPI, Response
from database import *
# from schema import *

api = FastAPI()
api.secret_key = "teuayanunyahoisina"

@api.get('/')
def index():
    return ({'title': 'API for Perpustakaan TMJ', 'developer': 'sh.fanda'})

# ============================================================================== #
#                                API for Anggota                                 #
# ============================================================================== #

@api.get('/api/anggota/all')
async def anggota_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `anggota` ORDER BY `id_anggota` ASC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_anggota': i[0], 'nama': i[1], 'kode': i[2], 'jk': i[3], 'jurusan': i[4], 'no_telp': i[5], 'alamat': i[6]})

    print("Result:\n",result)
    return result

@api.get('/api/anggota/{id}')
async def anggota_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `anggota` WHERE `id_anggota` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_anggota': i[0], 'nama': i[1], 'kode': i[2], 'jk': i[3], 'jurusan': i[4], 'no_telp': i[5], 'alamat': i[6]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                                API for Petugas                                 #
# ============================================================================== #

@api.get('/api/petugas/all')
async def petugas_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `petugas` ORDER BY `id_petugas` ASC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_petugas': i[0], 'nama': i[1], 'jabatan': i[2], 'no_telp': i[3], 'alamat': i[4]})

    print("Result:\n",result)
    return result

@api.get('/api/petugas/{id}')
async def petugas_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `petugas` WHERE `id_petugas` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_petugas': i[0], 'nama': i[1], 'jabatan': i[2], 'no_telp': i[3], 'alamat': i[4]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                                API for Buku                                    #
# ============================================================================== #

@api.get('/api/buku/all')
async def buku_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT b.id_buku, b.judul_buku, kb.nama_kode, b.penulis_buku, b.penerbit_buku, b.tahun_penerbit, b.stok from buku b inner join kode_buku kb on kb.id_kode = b.id_kode ORDER BY b.judul_buku ASC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_buku': i[0], 'judul': i[1], 'kode': i[2], 'penulis': i[3], 'penerbit': i[4], 'tahun': i[5], 'stok': i[6]})

    print("Result:\n",result)
    return result

@api.get('/api/buku/{id}')
async def buku_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT b.id_buku, b.judul_buku, kb.nama_kode, b.penulis_buku, b.penerbit_buku, b.tahun_penerbit, b.stok from buku b inner join kode_buku kb on kb.id_kode = b.id_kode WHERE `id_buku` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_buku': i[0], 'judul': i[1], 'kode': i[2], 'penulis': i[3], 'penerbit': i[4], 'tahun': i[5], 'stok': i[6]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                                API for Rak                                     #
# ============================================================================== #

@api.get('/api/rak/all')
async def rak_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `rak` ORDER BY `id_rak` ASC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_rak': i[0], 'nama': i[1], 'lokasi': i[2]})

    print("Result:\n",result)
    return result

@api.get('/api/rak/{id}')
async def rak_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `rak` WHERE `id_rak` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_rak': i[0], 'nama': i[1], 'lokasi': i[2]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                             API for Peminjaman                                 #
# ============================================================================== #

@api.get('/api/peminjaman/all')
async def peminjaman_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT p.id_peminjaman, p.tanggal_peminjaman, p.tanggal_kembali, b.judul_buku, a.nama_anggota, t.nama_petugas from peminjaman p inner join buku b on b.id_buku = p.id_buku inner join anggota a on a.id_anggota = p.id_anggota inner join petugas t on t.id_petugas = p.id_petugas ORDER BY `p`.`tanggal_peminjaman` DESC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_peminjaman': i[0], 'tgl_pinjam': i[1], 'tgl_kembali': i[2], 'judul_buku': i[3], 'nama_anggota': i[4], 'nama_petugas': i[5]})

    print("Result:\n",result)
    return result

@api.get('/api/peminjaman/{id}')
async def peminjaman_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT p.id_peminjaman, p.tanggal_peminjaman, p.tanggal_kembali, b.judul_buku, a.nama_anggota, t.nama_petugas from peminjaman p inner join buku b on b.id_buku = p.id_buku inner join anggota a on a.id_anggota = p.id_anggota inner join petugas t on t.id_petugas = p.id_petugas WHERE `p`.`id_peminjaman` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_peminjaman': i[0], 'tgl_pinjam': i[1], 'tgl_kembali': i[2], 'judul_buku': i[3], 'nama_anggota': i[4], 'nama_petugas': i[5]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                             API for Pengembalian                               #
# ============================================================================== #

@api.get('/api/pengembalian/all')
async def pengembalian_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT p.id_pengembalian, p.tanggal_pengembalian, p.denda, b.judul_buku, a.nama_anggota, t.nama_petugas from pengembalian p inner join buku b on b.id_buku = p.id_buku inner join anggota a on a.id_anggota = p.id_anggota inner join petugas t on t.id_petugas = p.id_petugas ORDER BY `p`.`tanggal_pengembalian` DESC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_pengembalian': i[0], 'tgl_kembali': i[1], 'denda': i[2], 'judul_buku': i[3], 'nama_anggota': i[4], 'nama_petugas': i[5]})

    print("Result:\n",result)
    return result

@api.get('/api/pengembalian/{id}')
async def pengembalian_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT p.id_pengembalian, p.tanggal_pengembalian, p.denda, b.judul_buku, a.nama_anggota, t.nama_petugas from pengembalian p inner join buku b on b.id_buku = p.id_buku inner join anggota a on a.id_anggota = p.id_anggota inner join petugas t on t.id_petugas = p.id_petugas WHERE `p`.`id_pengembalian` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_pengembalian': i[0], 'tgl_kembali': i[1], 'denda': i[2], 'judul_buku': i[3], 'nama_anggota': i[4], 'nama_petugas': i[5]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                                API for Kode Buku                               #
# ============================================================================== #

@api.get('/api/kode-buku/all')
async def kode_buku_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `kode_buku`"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_kode': i[0], 'nama': i[1], 'deskripsi': i[2]})

    print("Result:\n",result)
    return result

@api.get('/api/kode-buku/{id}')
async def kode_buku_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `kode_buku` WHERE `id_kode` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_kode': i[0], 'nama': i[1], 'deskripsi': i[2]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                          API for Relasi Rak Buku                               #
# ============================================================================== #

@api.get('/api/relasi-rak-buku/all')
async def relasi_rak_buku_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT rb.id_relasi, rb.id_rak, rb.id_buku, b.judul_buku FROM relasi_rak_buku rb INNER JOIN buku b ON b.id_buku = rb.id_buku ORDER BY `rb`.`id_rak` ASC"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_relasi': i[0], 'id_rak': i[1], 'id_buku': i[2], 'judul_buku': i[3]})

    print("Result:\n",result)
    return result

@api.get('/api/relasi-rak-buku/{id}')
async def relasi_rak_buku_readbyidrak(id:int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM relasi_rak_buku WHERE id_rak = {id}"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_relasi': i[0], 'id_rak': i[1], 'id_buku': i[2]})

    print("Result:\n",result)
    return result

# ============================================================================== #
#                                API for Userlist                                #
# ============================================================================== #

# @api.get('/api/userlist/all')
# async def userlist_read():
#     result = {}
#     result['results'] = []
#     sqlstr = f"SELECT * FROM `userlist`"
#     output_json = getMethod(sqlstr)

#     for i in output_json:
#         result['results'].append({'id_user': i[0], 'username': i[1], 'password': i[2]})

#     print("Result:\n",result)
#     return result

# @api.get('/api/userlist/{id}')
# async def userlist_readbyid(id: int):
#     result = {}
#     result['results'] = []
#     sqlstr = f"SELECT * FROM `userlist` WHERE `id_user` = {id};"
#     output_json = getMethod(sqlstr)

#     for i in output_json: 
#         result['results'].append({'id_user': i[0], 'username': i[1], 'password': i[2]})

#     print("Result:\n",result)
#     return result


if __name__ == '__main__':
    uvicorn.run(api)