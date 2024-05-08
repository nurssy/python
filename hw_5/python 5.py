import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import difflib

# Levenshtein mesafesi hesaplama fonksiyonu
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

# Kelime frekanslarını hesapla fonksiyonu
def kelime_frekanslarını_hesapla(metin):
    kelime_frekansları = {}
    kelimeler = metin.split()
    for kelime in kelimeler:
        kelime = kelime.lower() 
        if kelime in kelime_frekansları:
            kelime_frekansları[kelime] += 1
        else:
            kelime_frekansları[kelime] = 1
    return kelime_frekansları

# Metin x benzerlik oranını hesapla fonksiyonu
def metin_x_benzerlik_oranını_hesapla(metin1, metin2):
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

# Metin y benzerlik oranını hesapla fonksiyonu
def metin_y_benzerlik_oranını_hesapla(metin1, metin2):
    levenshtein_mesafesi = levenshtein_distance(metin1, metin2)
    max_len = max(len(metin1), len(metin2))
    benzerlik_orani = (max_len - levenshtein_mesafesi) / max_len
    return benzerlik_orani

# SQLite veritabanı bağlantısı
conn = sqlite3.connect('kullanici_veritabani.db')
c = conn.cursor()

# Kullanıcı tablosu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
             kullanici_adi TEXT PRIMARY KEY,
             sifre TEXT)''')

# Kullanıcı girişi kontrolü
def giris_kontrol():
    kullanici_adi = kullanici_entry.get()
    sifre = sifre_entry.get()
    c.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
    kullanici = c.fetchone()
    if kullanici:
        messagebox.showinfo("Başarılı Giriş", "Hoş geldiniz, {}".format(kullanici_adi))
        menu_ekrani()
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış")

# Kullanıcı kayıt olma
def kayit_ol():
    kullanici_adi = kullanici_entry.get()
    sifre = sifre_entry.get()
    try:
        c.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
        conn.commit()
        messagebox.showinfo("Başarılı Kayıt", "Kayıt başarıyla tamamlandı")
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut")

# İşlemler Menüsü ve Şifre Alt Menüsü
def islemler_menu():
    # İşlemler menüsü
    islemler_menu = tk.Toplevel(root)
    islemler_menu.title("İşlemler Menüsü")
    islemler_menu.geometry("300x200")

    # Şifre alt menüsü
    def sifre_menu():
        sifre_menu = tk.Toplevel(islemler_menu)
        sifre_menu.title("Şifre Menüsü")

        # Şifre değiştirme ekranı
        def sifre_degistir():
            sifre_degistir_ekrani = tk.Toplevel(sifre_menu)
            sifre_degistir_ekrani.title("Şifre Değiştirme Ekranı")

            yeni_sifre_label = tk.Label(sifre_degistir_ekrani, text="Yeni Şifre:")
            yeni_sifre_label.grid(row=0, column=0)
            yeni_sifre_entry = tk.Entry(sifre_degistir_ekrani, show="*")
            yeni_sifre_entry.grid(row=0, column=1)

            def sifre_guncelle():
                yeni_sifre = yeni_sifre_entry.get()
                c.execute("UPDATE kullanicilar SET sifre=? WHERE kullanici_adi=?", (yeni_sifre, kullanici_entry.get()))
                conn.commit()
                messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi")
                sifre_degistir_ekrani.destroy()

            guncelle_button = tk.Button(sifre_degistir_ekrani, text="Güncelle", command=sifre_guncelle)
            guncelle_button.grid(row=1, column=0, columnspan=2)

        sifre_degistir_button = tk.Button(sifre_menu, text="Şifre Değiştir", command=sifre_degistir)
        sifre_degistir_button.pack()

    sifre_menu_button = tk.Button(islemler_menu, text="Şifre Menüsü", command=sifre_menu)
    sifre_menu_button.pack()

# Menü ekranı
def menu_ekrani():
    menu_ekrani = tk.Toplevel(root)
    menu_ekrani.title("Menü")

    # Karşılaştırma menüsü
    def karsilastirma_menu():
        karsilastirma_menu = tk.Toplevel(menu_ekrani)
        karsilastirma_menu.title("Karşılaştırma Menüsü")

        # Metin karşılaştırma ekranı
        def metin_karsilastir(algoritma):
            def karşılaştır():
                metin1 = dosya1_entry.get()
                metin2 = dosya2_entry.get()
                if algoritma == "x":
                    benzerlik_orani, ortak_kelimeler = metin_x_benzerlik_oranını_hesapla(metin1, metin2)
                elif algoritma == "y":
                    benzerlik_orani = metin_y_benzerlik_oranını_hesapla(metin1, metin2)
                sonuc_label.config(text="Benzerlik Oranı: {:.2f}".format(benzerlik_orani))

            metin_karsilastir_ekrani = tk.Toplevel(karsilastirma_menu)
            metin_karsilastir_ekrani.title("Metin Karşılaştırma Ekranı")

            dosya1_label = tk.Label(metin_karsilastir_ekrani, text="Dosya 1:")
            dosya1_label.grid(row=0, column=0)
            dosya1_entry = tk.Entry(metin_karsilastir_ekrani)
            dosya1_entry.grid(row=0, column=1)
            dosya1_button = tk.Button(metin_karsilastir_ekrani, text="Dosya Seç", command=lambda: dosya_sec(dosya1_entry))
            dosya1_button.grid(row=0, column=2)

            dosya2_label = tk.Label(metin_karsilastir_ekrani, text="Dosya 2:")
            dosya2_label.grid(row=1, column=0)
            dosya2_entry = tk.Entry(metin_karsilastir_ekrani)
            dosya2_entry.grid(row=1, column=1)
            dosya2_button = tk.Button(metin_karsilastir_ekrani, text="Dosya Seç", command=lambda: dosya_sec(dosya2_entry))
            dosya2_button.grid(row=1, column=2)

            # Karşılaştırma butonu
            karsilastir_button = tk.Button(metin_karsilastir_ekrani, text="Karşılaştır", command=karşılaştır)
            karsilastir_button.grid(row=2, column=0, columnspan=3)

            # Sonuç etiketi
            sonuc_label = tk.Label(metin_karsilastir_ekrani, text="Benzerlik Oranı: ")
            sonuc_label.grid(row=3, column=0, columnspan=3)

        # Örnek algoritmaları buraya ekleyin
        metin_x_button = tk.Button(karsilastirma_menu, text="Metin x Algoritması", command=lambda: metin_karsilastir("x"))
        metin_x_button.pack()

        metin_y_button = tk.Button(karsilastirma_menu, text="Metin y Algoritması", command=lambda: metin_karsilastir("y"))
        metin_y_button.pack()

    karsilastirma_button = tk.Button(menu_ekrani, text="Karşılaştır", command=karsilastirma_menu)
    karsilastirma_button.pack()

    islemler_button = tk.Button(menu_ekrani, text="İşlemler", command=islemler_menu)
    islemler_button.pack()

    cikis_button = tk.Button(menu_ekrani, text="Çıkış", command=root.destroy)
    cikis_button.pack()

# Dosya seçme fonksiyonu
def dosya_sec(entry):
    dosya_yolu = filedialog.askopenfilename(initialdir="/", title="Dosya Seç", filetypes=(("Text Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")))
    entry.delete(0, tk.END)
    entry.insert(tk.END, dosya_yolu)

# Ana pencere
root = tk.Tk()
root.title("Kullanıcı Girişi")

# Kullanıcı adı ve şifre girişi alanları
kullanici_label = tk.Label(root, text="Kullanıcı Adı:")
kullanici_label.grid(row=0, column=0)
kullanici_entry = tk.Entry(root)
kullanici_entry.grid(row=0, column=1)

sifre_label = tk.Label(root, text="Şifre:")
sifre_label.grid(row=1, column=0)
sifre_entry = tk.Entry(root, show="*")
sifre_entry.grid(row=1, column=1)

# Giriş ve kayıt ol buonları
giris_button = tk.Button(root, text="Giriş Yap", command=giris_kontrol)
giris_button.grid(row=2, column=0)

kayit_button = tk.Button(root, text="Kayıt Ol", command=kayit_ol)
kayit_button.grid(row=2, column=1)

root.mainloop()
