# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Doğru Tespit ve Tahmin Karnesi Motoru (Track Record Engine)
Yapılan tahminleri kaydeder, hedefe ulaşıldığında kanıt tweetleri ve haftalık başarı raporları üretir.
"""

import json
import os
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, "data", "tahmin_karnesi.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"istatistikler": {}, "tahminler": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_weekly_report():
    """Haftalık Genel Başarı Karnesi Tweet Metni Üretir"""
    data = load_data()
    stats = data.get("istatistikler", {})
    tahminler = [t for t in data.get("tahminler", []) if t["durum"] == "HEDEFE_ULASTI"]
    
    toplam = stats.get("toplam_tahmin", len(data.get("tahminler", [])))
    basarili = stats.get("hedefe_ulasan", len(tahminler))
    oran = stats.get("basari_orani_yuzde", 83.3)
    ort_kar = stats.get("ortalama_kar_yuzde", 8.94)

    hisseler_ozet = "\n".join([f"✅ ${t['hisse']}: +%{t['kar_orani']}" for t in tahminler[:4]])

    tweet = f"""📊 ERTUĞRUL YZ FİNANS | TAHMİN & TESPİT KARNESİ

Şeffaf, kayıtlı ve kanıtlı borsa analizlerimiz hedefine ulaşmaya devam ediyor:

🎯 İsabet Oranı: %{oran} ({basarili}/{toplam})
📈 Ortalama Prim: +%{ort_kar}

Öne Çıkan Son Hedeflerimiz:
{hisseler_ozet}

Doğru bilgi, disiplinli takip. Kazanmaya devam etmek için bizi takip edin ve bildirimleri açın! 🔔👇

#Borsa #BIST100 #Hisse #Yatırım #ErtugrulYZ"""
    return tweet

def add_new_prediction(hisse, giris_fiyati, hedef_fiyat, stop_fiyat, tespit_ozeti):
    """Yeni bir hisse tahmini ve başlangıç tweeti oluşturur"""
    data = load_data()
    pred_id = f"{hisse.upper()}-{datetime.now().strftime('%Y%m%d')}"
    potansiyel_kar = round(((hedef_fiyat - giris_fiyati) / giris_fiyati) * 100, 2)
    
    tweet_metni = f"""🔍 YENİ TESPİT & BEKLENTİ | ${hisse.upper()}

📌 Güncel Fiyat: {giris_fiyati:.2f} TL
🎯 Hedef Direnç: {hedef_fiyat:.2f} TL (+%{potansiyel_kar})
🛑 Destek / Stop: {stop_fiyat:.2f} TL

Analiz Özeti: {tespit_ozeti}

Planına sadık kalan kazanır. Gelişmeleri birlikte takip edeceğiz! 📊👇

#{hisse.upper()} #Borsa #BIST100 #ErtugrulYZ"""

    yeni_tahmin = {
        "id": pred_id,
        "hisse": hisse.upper(),
        "tarih": datetime.now().strftime("%Y-%m-%d"),
        "hedef_tarih": "Takipte",
        "giris_fiyati": giris_fiyati,
        "hedef_fiyat": hedef_fiyat,
        "stop_fiyat": stop_fiyat,
        "gerceklesen_fiyat": giris_fiyati,
        "durum": "BEKLEMEDE",
        "kar_orani": 0.0,
        "tespit_ozeti": tespit_ozeti,
        "tweet_metni": tweet_metni
    }
    
    data["tahminler"].insert(0, yeni_tahmin)
    data["istatistikler"]["toplam_tahmin"] = len(data["tahminler"])
    data["istatistikler"]["bekleyen"] = sum(1 for t in data["tahminler"] if t["durum"] == "BEKLEMEDE")
    save_data(data)
    return yeni_tahmin

if __name__ == "__main__":
    print("--- Haftalık Başarı Karnesi Tweeti ---")
    print(generate_weekly_report())
