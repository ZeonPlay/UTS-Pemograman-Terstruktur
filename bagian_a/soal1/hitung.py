BATAS_LULUS = 70


def hitung_rata_rata(*nilai):
    if len(nilai) == 0:
        raise ValueError("Daftar nilai tidak boleh kosong")
    total = 0
    for n in nilai:
        total += int(n)
    return total / len(nilai)


def tentukan_status(rata, batas=BATAS_LULUS):
    return "Lulus" if rata >= batas else "Tidak Lulus"


def tampilkan_hasil(nama, daftar_nilai, batas=BATAS_LULUS):
    rata = hitung_rata_rata(*daftar_nilai)
    print("Nama      :", nama)
    print("Rata-rata :", round(rata, 2))
    print("Status    :", tentukan_status(rata, batas=batas))


if __name__ == "__main__":
    print("--- Pengujian lokal hitung.py ---")
    assert hitung_rata_rata(80, 75, 90) == 81.66666666666667
    assert tentukan_status(70) == "Lulus"
    assert tentukan_status(69.9) == "Tidak Lulus"
    assert tentukan_status(65, batas=60) == "Lulus"
    tampilkan_hasil("Budi", ["80", "75", "90"])
    print("Semua pengujian lokal lulus")
