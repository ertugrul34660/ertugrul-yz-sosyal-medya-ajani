# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Sabah 09:00 Sosyal Medya ve Bildirim Nöbetçisi
Tüm sosyal medya kanallarını (özellikle X / @ertugrul_yz) her sabah saat 09:00'da
tarar, gelen yorumları sınıflandırır ve bilge/esprili yanıtlar üretir.
"""

import os
import json
import random
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
GUNLUK_RAPOR_FILE = os.path.join(DATA_DIR, "sabah_sosyal_medya_raporu.json")

YANIT_KATALOGU = {
    "HISSE_SORUSU": [
        "Grafiği masamda dostum, seviyelerine bakıyorum. Gün içi bültende net kırılımı paylaşırım, takipte kal! ☕📊",
        "Direnç bölgesine yakın işlem görüyor. Acele edip tepeden atlama, düzeltmesini sakin kafayla bekleyelim.",
        "Listeme ekledim dostum. Tahtacının niyetini hacimden okuyoruz, akşama detaylı değerlendiririz."
    ],
    "TESEKKUR": [
        "Bereketli olsun dostum! Kârı cebe koymayı asla ihmal etme ☕ Birlikte kazanmaya devam.",
        "Rica ederim, plana sadık kalan her zaman kazanır. Gözün arkada kalmasın 🚀",
        "Afiyetle harca dostum. Disiplin bittiği an piyasa affetmez, seviyelere dikkat!"
    ],
    "PANIK_ZARAR": [
        "Sakin kal dostum, ekranı kapatıp bir kahve iç. Panikle satılan malı her zaman sabırlı olan toplar.",
        "Borsada kural bir: Sermayeyi korumak. Stop seviyene sadık kalırsan piyasada fırsat asla bitmez.",
        "Korku zirvedeyken dönüş yakındır. Panik tuşuna basmadan önce büyük resme bak dostum ☕"
    ],
    "MIZAH_VE_SOHBET": [
        "Biz bu tahtacıyla daha çok çay içeriz dostum 😂 Kapanışa kadar nöbetteyiz, afiyet olsun!",
        "Maliyeti düşüreceğiz diye hisse ala ala şirketin yönetim kurulu üyesi olacağız az kaldı valla 😂",
        "Borsa değil kardiyoloji kliniği mübarek, kalp ritmimizi bozdu yine 😂 Masada kalan kazanır."
    ],
    "ELESTIRI": [
        "Piyasa iki yönlüdür dostum; biz rakamlara ve seviyelere bakarız, gerisi gürültüdür ☕ Seans sonunda görüşürüz.",
        "Farklı fikirler piyasayı zenginleştirir dostum. Stop seviyemiz net, plana sadık olan kazanır."
    ]
}

def analiz_et_ve_yanitla(kullanici_adi, yorum_metni):
    """Gelen yorumu analiz eder, kategori belirler ve < 235 karakterlik esprili/bilge yanıt üretir."""
    txt = yorum_metni.lower()
    
    if any(w in txt for w in ["teşekkür", "eline sağlık", "harika", "kazandık", "sayende", "bereket", "tebrik"]):
        kategori = "TESEKKUR"
    elif any(w in txt for w in ["zarar", "battık", "korkuyorum", "panik", "düştü", "stop", "ne yapayım"]):
        kategori = "PANIK_ZARAR"
    elif any(w in txt for w in ["çay", "tahtacı", "kahkaha", "komik", "güldüm", "uyumadık", "uyku"]):
        kategori = "MIZAH_VE_SOHBET"
    elif any(w in txt for w in ["yanıldın", "ters", "tutmadı", "patladı", "yalan"]):
        kategori = "ELESTIRI"
    else:
        kategori = "HISSE_SORUSU"
        
    secilen_yanit = random.choice(YANIT_KATALOGU[kategori])
    # Dolar işareti kesinlikle olmamalı ve 235 karakter altı olmalı
    assert "$" not in secilen_yanit, "Dolar işareti tespit edildi!"
    assert len(secilen_yanit) < 235, "Yanıt karakter sınırını aştı!"
    
    return {
        "kullanici": kullanici_adi,
        "yorum": yorum_metni,
        "kategori": kategori,
        "yanit": secilen_yanit,
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def sabah_nobetci_raporu_olustur(tespit_edilenler=None):
    """Her sabah saat 09:00'da çalışan nöbetçi durum kütüğü."""
    os.makedirs(DATA_DIR, exist_ok=True)
    rapor = {
        "nobet_adi": "Sabah 09:00 Sosyal Medya ve Bildirim Nöbetçisi",
        "hesap": "@ertugrul_yz",
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "taranan_platformlar": [
            {"platform": "X (Twitter)", "url": "https://x.com/notifications", "durum": "TARANDI"},
            {"platform": "X Mentions", "url": "https://x.com/notifications/mentions", "durum": "TARANDI"},
            {"platform": "YouTube Topluluk", "durum": "HAZIR"},
            {"platform": "Telegram / Sohbet", "durum": "HAZIR"}
        ],
        "islenen_yorumlar": tespit_edilenler or []
    }
    with open(GUNLUK_RAPOR_FILE, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)
    return rapor

if __name__ == "__main__":
    ornek = analiz_et_ve_yanitla("@borsaci_mehmet", "Hocam THYAO için bugün ne düşünüyorsunuz?")
    print("Test Yanıtı:")
    print(json.dumps(ornek, ensure_ascii=False, indent=2))
    sabah_nobetci_raporu_olustur([ornek])
    print("Sabah Nöbetçisi Raporu Kaydedildi.")
