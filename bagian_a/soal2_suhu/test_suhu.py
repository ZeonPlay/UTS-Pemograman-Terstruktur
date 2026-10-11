import unittest

from suhu import analisis, hitung_rata_rata, kategori_suhu

DATA = [
    {"hari": "Senin", "suhu": 31}, {"hari": "Selasa", "suhu": 33},
    {"hari": "Rabu", "suhu": 29}, {"hari": "Kamis", "suhu": 35},
    {"hari": "Jumat", "suhu": 32}, {"hari": "Sabtu", "suhu": 30},
    {"hari": "Minggu", "suhu": 28},
]


class TestAnalisisSuhu(unittest.TestCase):
    def test_rata_rata(self):
        self.assertAlmostEqual(hitung_rata_rata(*[d["suhu"] for d in DATA]), 218 / 7)

    def test_tertinggi_dan_terendah(self):
        hasil = analisis(DATA)
        self.assertEqual(hasil["tertinggi"], {"hari": "Kamis", "suhu": 35})
        self.assertEqual(hasil["terendah"], {"hari": "Minggu", "suhu": 28})

    def test_kategori_batas_32(self):
        self.assertEqual(kategori_suhu(32), "Panas")
        self.assertEqual(kategori_suhu(31), "Normal")

    def test_jumlah_panas(self):
        self.assertEqual(analisis(DATA)["jumlah_panas"], 3)

    def test_data_kosong(self):
        self.assertIsNone(analisis([]))


if __name__ == "__main__":
    unittest.main()
