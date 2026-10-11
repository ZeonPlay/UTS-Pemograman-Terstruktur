import os
import tempfile
import unittest

from .fileio import baca_transaksi, buat_file_data, tambah_transaksi, tulis_laporan
from .models import Transaksi, buat_transaksi
from .processing import PengelolaKeuangan
from .validasi import DataTidakValidError, validasi_baris, validasi_nominal


class TestValidasi(unittest.TestCase):
    def test_nominal_valid(self):
        self.assertEqual(validasi_nominal(" 15000 "), 15000)

    def test_nominal_bukan_angka(self):
        with self.assertRaises(ValueError):
            validasi_nominal("abc")

    def test_nominal_negatif(self):
        with self.assertRaises(DataTidakValidError):
            validasi_nominal("-100")

    def test_field_kosong(self):
        with self.assertRaises(DataTidakValidError):
            validasi_baris("2026-10-01;;1000;kosong")

    def test_jumlah_kolom_salah(self):
        with self.assertRaises(ValueError):
            validasi_baris("2026-10-01;makan;1000")


class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.pk = PengelolaKeuangan(
            [
                Transaksi("2026-10-01", "makan", 10000, "Roti"),
                Transaksi("2026-10-02", "makan", 20000, "Nasi"),
                Transaksi("2026-10-03", "transport", 5000, "Angkot"),
            ]
        )

    def test_total(self):
        self.assertEqual(self.pk.total(), 35000)

    def test_per_kategori(self):
        self.assertEqual(self.pk.total_per_kategori(), {"makan": 30000, "transport": 5000})

    def test_terbesar(self):
        self.assertEqual(self.pk.terbesar(jumlah=1)[0].nominal, 20000)

    def test_filter_minimal(self):
        self.assertEqual(len(self.pk.filter_minimal(batas=10000)), 2)

    def test_kwargs_atribut_tambahan(self):
        t = buat_transaksi(tanggal="2026-10-04", kategori="Hiburan", nominal=30000, keterangan="Bioskop", metode="QRIS")
        self.assertEqual(t.tambahan, {"metode": "QRIS"})


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(tempfile.mkdtemp(), "data.txt")

    def test_mode_x_tidak_menimpa(self):
        self.assertTrue(buat_file_data(self.path, "2026-10-01;makan;1000;A\n"))
        self.assertFalse(buat_file_data(self.path, "ISI BARU\n"))
        self.assertEqual(len(baca_transaksi(self.path)[0]), 1)

    def test_baris_rusak_dilewati(self):
        buat_file_data(self.path, "2026-10-01;makan;1000;A\n2026-10-02;makan;abc;B\n2026-10-03;makan;-1;C\n")
        data, rusak = baca_transaksi(self.path)
        self.assertEqual(len(data), 1)
        self.assertEqual(len(rusak), 2)

    def test_file_tidak_ada(self):
        self.assertEqual(baca_transaksi(self.path), ([], []))

    def test_tambah_dan_laporan(self):
        buat_file_data(self.path)
        tambah_transaksi(self.path, Transaksi("2026-10-01", "makan", 1000, "A"))
        self.assertEqual(len(baca_transaksi(self.path)[0]), 1)
        laporan = os.path.join(os.path.dirname(self.path), "laporan.txt")
        tulis_laporan(laporan, "isi")
        with open(laporan) as f:
            self.assertEqual(f.read(), "isi")


def jalankan_semua_tes():
    """Menjalankan seluruh pengujian; dipanggil dari main.py."""
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__, fromlist=["x"]))
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    unittest.main()
