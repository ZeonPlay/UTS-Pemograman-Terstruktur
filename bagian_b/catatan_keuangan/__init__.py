"""Package catatan_keuangan - pencatat pengeluaran harian berbasis file teks.

Pembagian modul:
    models.py      : class Transaksi (satu record data)
    validasi.py    : pengecekan input/data + exception buatan sendiri
    fileio.py      : baca / tulis / tambah file (mode x, a, r, w)
    processing.py  : class PengelolaKeuangan (perhitungan dan analisis)
    testing.py     : pengujian global dengan library unittest
"""
