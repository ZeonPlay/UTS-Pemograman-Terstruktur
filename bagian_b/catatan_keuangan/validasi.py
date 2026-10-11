"""validasi.py - pengecekan input dan data."""


class DataTidakValidError(Exception):
    """Exception buatan sendiri: dipakai untuk field kosong atau nilai negatif."""


def validasi_teks(nilai, nama_field):
    """Memastikan field teks tidak kosong. Mengembalikan teks yang sudah dirapikan."""
    nilai = str(nilai).strip()
    if nilai == "":
        raise DataTidakValidError(f"Field '{nama_field}' tidak boleh kosong")  # raise
    return nilai


def validasi_nominal(teks):
    """Mengubah teks menjadi int positif.

    ValueError muncul otomatis jika bukan angka (mis. 'abc');
    DataTidakValidError muncul jika angkanya negatif atau nol.
    """
    nominal = int(str(teks).strip())  # bisa memunculkan ValueError
    if nominal <= 0:
        raise DataTidakValidError(f"Nominal harus lebih dari 0, diterima: {nominal}")  # raise
    return nominal


def validasi_baris(baris):
    """Memecah satu baris 'tanggal;kategori;nominal;keterangan' menjadi tuple bersih.

    Memunculkan ValueError / DataTidakValidError jika baris rusak.
    """
    bagian = baris.strip().split(";")
    if len(bagian) != 4:
        raise ValueError(f"Jumlah kolom harus 4, ditemukan {len(bagian)}")
    tanggal, kategori, nominal, keterangan = bagian
    return (
        validasi_teks(tanggal, "tanggal"),
        validasi_teks(kategori, "kategori").lower(),
        validasi_nominal(nominal),
        validasi_teks(keterangan, "keterangan"),
    )


# Pengujian lokal: hanya jalan jika file ini dieksekusi langsung
if __name__ == "__main__":
    print("--- Pengujian lokal validasi.py ---")
    print(validasi_baris("2026-10-01;Makan;15000;Nasi goreng"))
    for contoh in ("2026-10-01;makan;abc;rusak", "2026-10-01;makan;-5;negatif", "2026-10-01;;100;kosong"):
        try:
            validasi_baris(contoh)
        except (ValueError, DataTidakValidError) as err:
            print(f"Ditolak -> {contoh!r}: {err}")
