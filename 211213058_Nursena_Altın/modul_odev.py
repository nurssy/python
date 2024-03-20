# modul_odev.py

def harf_kontrol(char):
   
    if char.isalpha():
        return True
    else:
        return False

def kücük_harf(char):
   
    return char.lower()

def harf_kullanim_sikligi(text):
   
    letter_count = {}
    total_letters = 0

    for char in text:
        if char.isalpha():
            char = char.lower()
            letter_count[char] = letter_count.get(char, 0) + 1
            total_letters += 1
    
    frequency_percentage = {char: (count / total_letters) * 100 for char, count in letter_count.items()}
    return frequency_percentage

def kelime_sayisi(text):
    print("Cümledeki kelime sayısı:")
    words = text.split()
    return len(words)

def uzun_kelime(text):
    print("Cümledeki en uzun kelime:")
    words = text.split()
    longest_word = max(words, key=len)
    return longest_word
    

def bilgi():
 
    print("Ad Soyad: [Nursena Altın]")
    print("Öğrenci Numarası: [211213058]")
    print("Not: [Ağlama ben ağlarım]")
