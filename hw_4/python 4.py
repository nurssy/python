import sqlite3

def kelime_frekanslarını_hesapla(metin):
    kelime_frekansları = {}
    kelimeler = metin.split()
    for kelime in kelimeler:
        kelime = kelime.lower()  # Kelimeleri küçük harfe dönüştürüyoruz
        if kelime in kelime_frekansları:
            kelime_frekansları[kelime] += 1
        else:
            kelime_frekansları[kelime] = 1
    return kelime_frekansları

def benzerlik_oranını_hesapla(metin1, metin2):
    frekanslar1 = kelime_frekanslarını_hesapla(metin1)
    frekanslar2 = kelime_frekanslarını_hesapla(metin2)

    toplam_fark = 0
    ortak_kelimeler = []

    for kelime, frekans in frekanslar1.items():
        if kelime in frekanslar2:
            toplam_fark += abs(frekans - frekanslar2[kelime])
            ortak_kelimeler.append(kelime)

    for kelime, frekans in frekanslar2.items():
        if kelime not in frekanslar1:
            toplam_fark += frekans

    benzerlik_orani = 1 - (toplam_fark / (len(metin1.split()) + len(metin2.split())))
    return benzerlik_orani, ortak_kelimeler

# Kullanıcıdan metinleri alalım
metin1 = input("Birinci metni giriniz: ")
print("\n")
metin2 = input("İkinci metni giriniz: ")
print("\n")

# SQLite veritabanına metinleri kaydedelim
baglanti = sqlite3.connect('metinler.db')
imlec = baglanti.cursor()
imlec.execute('''CREATE TABLE IF NOT EXISTS metinler (
                    id INTEGER PRIMARY KEY,
                    metin TEXT
                )''')
imlec.execute("INSERT INTO metinler (metin) VALUES (?)", (metin1,))
imlec.execute("INSERT INTO metinler (metin) VALUES (?)", (metin2,))
baglanti.commit()

# Benzerlik oranını hesaplayalım
benzerlik_orani, ortak_kelimeler = benzerlik_oranını_hesapla(metin1, metin2)

# Sonucu ekrana yazdıralım
print("Metinler arasındaki benzerlik oranı:", benzerlik_orani)
print("Ortak kelimeler:", ortak_kelimeler)

# Benzerlik durumunu dosyaya yazdıralım
with open("benzerlik_durumu.txt", "w") as dosya:
    dosya.write("Metinler arasındaki benzerlik oranı: {}\n".format(benzerlik_orani))
    dosya.write("Ortak kelimeler:\n")
    for kelime in ortak_kelimeler:
        dosya.write(kelime + "\n")

# Bağlantıyı kapat
baglanti.close()
