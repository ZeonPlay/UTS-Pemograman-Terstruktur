BATAS_PANAS = 32


def baca_data(nama_file):
    data = []
    try:
        with open(nama_file, "r") as file:
            for baris in file:
                baris = baris.strip()
                if not baris:
                    continue
                hari, suhu = baris.split(";")
                data.append({"hari": hari, "suhu": int(suhu)})
    except FileNotFoundError:
        print(f"Kesalahan: file {nama_file} tidak ditemukan.")
        return []
    return data


def hitung_rata_rata(*suhu):
    return sum(suhu) / len(suhu)


def kategori_suhu(suhu, batas=BATAS_PANAS):
    return "Panas" if suhu >= batas else "Normal"


def analisis(data, batas=BATAS_PANAS):
    if not data:
        return None
    rata = hitung_rata_rata(*[d["suhu"] for d in data])
    tertinggi = max(data, key=lambda d: d["suhu"])
    terendah = min(data, key=lambda d: d["suhu"])
    kategori = [{**d, "kategori": kategori_suhu(d["suhu"], batas=batas)} for d in data]
    jumlah_panas = len([d for d in kategori if d["kategori"] == "Panas"])
    return {
        "rata_rata": rata,
        "tertinggi": tertinggi,
        "terendah": terendah,
        "kategori": kategori,
        "jumlah_panas": jumlah_panas,
    }


def buat_laporan(hasil):
    baris = ["LAPORAN SUHU MINGGUAN", "=" * 28]
    for d in hasil["kategori"]:
        baris.append(f"{d['hari']:<8}: {d['suhu']} C ({d['kategori']})")
    baris.append("-" * 28)
    baris.append(f"Rata-rata suhu   : {hasil['rata_rata']:.2f} C")
    baris.append(f"Suhu tertinggi   : {hasil['tertinggi']['suhu']} C ({hasil['tertinggi']['hari']})")
    baris.append(f"Suhu terendah    : {hasil['terendah']['suhu']} C ({hasil['terendah']['hari']})")
    baris.append(f"Jumlah hari Panas: {hasil['jumlah_panas']}")
    return "\n".join(baris) + "\n"


def tulis_laporan(nama_file, teks):
    with open(nama_file, "w") as file:
        file.write(teks)
    with open(nama_file, "r") as file:
        print(file.read())


def main():
    data = baca_data("suhu.txt")
    hasil = analisis(data)
    if hasil is None:
        return
    tulis_laporan("laporan_suhu.txt", buat_laporan(hasil))


if __name__ == "__main__":
    main()
