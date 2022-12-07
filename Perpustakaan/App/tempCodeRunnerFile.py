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