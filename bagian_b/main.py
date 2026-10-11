from catatan_keuangan.fileio import baca_transaksi, buat_file_data, tambah_transaksi, tulis_laporan
from catatan_keuangan.models import Transaksi
from catatan_keuangan.processing import PengelolaKeuangan
from catatan_keuangan.testing import jalankan_semua_tes
from catatan_keuangan.validasi import DataTidakValidError

FILE_DATA = "pengeluaran.txt"
FILE_LAPORAN = "laporan_pengeluaran.txt"

# Data awal contoh. Dua baris terakhir sengaja rusak untuk memperlihatkan
# bahwa baris rusak dilewati (tidak menghentikan program).
DATA_AWAL = (
    "2026-10-01;makan;15000;Nasi goreng\n"
    "2026-10-01;transport;8000;Ojek ke kampus\n"
    "2026-10-02;makan;12000;Mie ayam\n"
    "2026-10-03;hiburan;50000;Nonton bioskop\n"
    "2026-10-04;kuliah;35000;Fotokopi modul\n"
    "2026-10-05;makan;abc;Salah ketik nominal\n"
    "2026-10-06;transport;-5000;Nominal negatif\n"
)


def tampilkan_data():
    """Menu 1: tampilkan semua data valid dan laporkan baris yang rusak."""
    data, rusak = baca_transaksi(FILE_DATA)
    for t in data:
        print(t)
    for nomor, isi, alasan in rusak:
        print(f"[DILEWATI] baris {nomor}: {isi!r} -> {alasan}")


def input_transaksi():
    """Menu 2: minta input pengguna lalu tambahkan ke file (mode a)."""
    try:
        transaksi = Transaksi(
            input("Tanggal (YYYY-MM-DD): "),
            input("Kategori            : "),
            input("Nominal (Rp)        : "),
            input("Keterangan          : "),
        )
    except (ValueError, DataTidakValidError) as err:
        print("Input ditolak:", err)
        return
    tambah_transaksi(FILE_DATA, transaksi)
    print("Data berhasil ditambahkan.")


def buat_laporan():
    """Menu 3: hitung analisis, tulis ke file laporan (mode w), lalu tampilkan."""
    data, _ = baca_transaksi(FILE_DATA)
    if not data:
        print("Belum ada data untuk dilaporkan.")
        return
    teks = PengelolaKeuangan(data).buat_laporan(jumlah_teratas=3)
    tulis_laporan(FILE_LAPORAN, teks)
    print(teks)


def main():
    buat_file_data(FILE_DATA, isi_awal=DATA_AWAL)  # mode x
    menu = {"1": tampilkan_data, "2": input_transaksi, "3": buat_laporan, "4": jalankan_semua_tes}
    while True:
        print("\n=== PENCATAT PENGELUARAN HARIAN ===")
        print("1. Lihat data\n2. Tambah pengeluaran\n3. Buat laporan\n4. Jalankan pengujian\n5. Keluar")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "5":
            print("Sampai jumpa.")
            break
        menu.get(pilihan, lambda: print("Menu tidak dikenal"))()


if __name__ == "__main__":
    main()
