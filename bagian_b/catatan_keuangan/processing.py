class PengelolaKeuangan:
    """Menyimpan daftar Transaksi dan menyediakan fungsi analisis."""

    def __init__(self, daftar=None):
        self.daftar = list(daftar) if daftar else []

    def tambah(self, transaksi):
        """Menambah satu Transaksi ke daftar di memori."""
        self.daftar.append(transaksi)

    @staticmethod
    def jumlahkan(*angka):
        """Menjumlahkan angka sebanyak apa pun (*args)."""
        return sum(angka)

    def total(self):
        """Total seluruh pengeluaran."""
        return self.jumlahkan(*[t.nominal for t in self.daftar])

    def rata_rata(self):
        """Rata-rata pengeluaran per transaksi (0 jika belum ada data)."""
        return self.total() / len(self.daftar) if self.daftar else 0

    def total_per_kategori(self):
        """Dictionary {kategori: total}."""
        hasil = {}
        for t in self.daftar:
            hasil[t.kategori] = hasil.get(t.kategori, 0) + t.nominal
        return hasil

    def terbesar(self, jumlah=3):
        """Transaksi dengan nominal terbesar; urutan memakai lambda sebagai key."""
        return sorted(self.daftar, key=lambda t: t.nominal, reverse=True)[:jumlah]

    def filter_minimal(self, batas=0):
        """Transaksi dengan nominal >= batas (filter + lambda)."""
        return list(filter(lambda t: t.nominal >= batas, self.daftar))

    def buat_laporan(self, judul="LAPORAN PENGELUARAN HARIAN", jumlah_teratas=3):
        """Menyusun teks laporan lengkap (jumlah_teratas dipanggil sebagai keyword argument)."""
        baris = [judul, "=" * len(judul)]
        baris.append(f"Jumlah transaksi : {len(self.daftar)}")
        baris.append(f"Total pengeluaran: Rp{self.total():,}")
        baris.append(f"Rata-rata        : Rp{self.rata_rata():,.0f}")
        baris.append("")
        baris.append("Total per kategori:")
        per_kategori = self.total_per_kategori()
        for kategori, jumlah in sorted(per_kategori.items(), key=lambda item: item[1], reverse=True):
            baris.append(f"  {kategori:<10}: Rp{jumlah:,}")
        baris.append("")
        baris.append(f"{jumlah_teratas} pengeluaran terbesar:")
        for no, t in enumerate(self.terbesar(jumlah=jumlah_teratas), start=1):
            baris.append(f"  {no}. {t}")
        return "\n".join(baris) + "\n"


# Pengujian lokal
if __name__ == "__main__":
    from .models import Transaksi

    print("--- Pengujian lokal processing.py ---")
    pk = PengelolaKeuangan(
        [Transaksi("2026-10-01", "makan", 10000, "Roti"), Transaksi("2026-10-02", "transport", 5000, "Angkot")]
    )
    assert pk.total() == 15000
    print(pk.buat_laporan())
