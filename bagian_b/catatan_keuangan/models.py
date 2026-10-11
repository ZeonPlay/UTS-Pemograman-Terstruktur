"""models.py - class Transaksi (satu record pengeluaran)."""
from .validasi import validasi_nominal, validasi_teks


class Transaksi:
    """Satu catatan pengeluaran. Atribut tambahan boleh ditambah lewat **kwargs."""

    def __init__(self, tanggal, kategori, nominal, keterangan, **tambahan):
        self.tanggal = validasi_teks(tanggal, "tanggal")
        self.kategori = validasi_teks(kategori, "kategori").lower()
        self.nominal = validasi_nominal(nominal)
        self.keterangan = validasi_teks(keterangan, "keterangan")
        assert isinstance(self.nominal, int), "nominal harus bertipe int"  # assert
        # **kwargs: atribut opsional yang bervariasi (mis. metode="QRIS", lokasi="Kantin")
        self.tambahan = dict(tambahan)

    def ke_baris(self):
        """Mengubah record menjadi satu baris teks untuk disimpan ke file."""
        return f"{self.tanggal};{self.kategori};{self.nominal};{self.keterangan}"

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Transaksi dari satu baris file (format tanggal;kategori;nominal;keterangan)."""
        tanggal, kategori, nominal, keterangan = baris.strip().split(";")
        return cls(tanggal, kategori, nominal, keterangan)

    def __str__(self):
        return f"{self.tanggal} | {self.kategori:<10} | Rp{self.nominal:>9,} | {self.keterangan}"


def buat_transaksi(**data):
    """Membuat record dari keyword argument; field wajib diambil, sisanya jadi atribut tambahan."""
    return Transaksi(
        data.pop("tanggal", ""),
        data.pop("kategori", ""),
        data.pop("nominal", ""),
        data.pop("keterangan", ""),
        **data,
    )
