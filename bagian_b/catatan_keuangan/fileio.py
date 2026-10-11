from .models import Transaksi
from .validasi import DataTidakValidError


def buat_file_data(nama_file, isi_awal=""):
    """Mode 'x': membuat file data pertama kali; tidak menimpa file yang sudah ada.

    Mengembalikan True jika file dibuat, False jika sudah ada.
    """
    try:
        with open(nama_file, "x", encoding="utf-8") as file:
            file.write(isi_awal)
        return True
    except FileExistsError:
        print(f"Info: {nama_file} sudah ada, tidak dibuat ulang (data lama aman).")
        return False


def tambah_transaksi(nama_file, transaksi):
    """Mode 'a': menambah satu record di akhir file tanpa menghapus data lama."""
    with open(nama_file, "a", encoding="utf-8") as file:
        file.write(transaksi.ke_baris() + "\n")


def baca_transaksi(nama_file):
    """Mode 'r': membaca baris demi baris (iteratif).

    Baris rusak dilewati (tidak menghentikan program).
    Mengembalikan (daftar_transaksi, daftar_baris_rusak).
    """
    data, rusak = [], []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            for nomor, baris in enumerate(file, start=1):
                if not baris.strip():
                    continue
                try:
                    data.append(Transaksi.dari_baris(baris))
                except (ValueError, DataTidakValidError) as err:
                    rusak.append((nomor, baris.strip(), str(err)))
    except FileNotFoundError:
        print(f"Kesalahan: file '{nama_file}' belum ada. Jalankan pembuatan file data terlebih dahulu.")
        return [], []
    return data, rusak


def tulis_laporan(nama_file, teks):
    """Mode 'w': menulis laporan; isi lama ditimpa karena laporan selalu dibuat ulang."""
    with open(nama_file, "w", encoding="utf-8") as file:
        file.write(teks)


# Pengujian lokal
if __name__ == "__main__":
    import os
    import tempfile

    print("--- Pengujian lokal fileio.py ---")
    path = os.path.join(tempfile.mkdtemp(), "uji.txt")
    print("Dibuat:", buat_file_data(path, "2026-10-01;makan;10000;Roti\n"))
    print("Dibuat lagi:", buat_file_data(path))
    tambah_transaksi(path, Transaksi("2026-10-02", "transport", 5000, "Angkot"))
    print(baca_transaksi(path)[0][1])
    print(baca_transaksi("tidak_ada.txt"))
