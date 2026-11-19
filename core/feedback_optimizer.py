# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Akıllı Etkileşim ve Geri Bildirim Optimize Edici
X (Twitter) üzerindeki beğeni, yorum ve takipçi reaksiyonlarına göre içerik stratejisini otomatik ayarlar.
"""

import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, "data", "etkilesim_ayarlari.json")

def get_default_config():
    return {
        "en_cok_tutan_format": "HEDEF_VURULDU_KANIT",
        "yorum_oranina_gore_strateji": "SORU_VE_ANKET_AGIRLIKLI",
        "topluluktan_gelen_populer_hisseler": ["THYAO", "SASA", "ASELS", "EREGL", "TUPRS"],
        "hazir_cevaplar": {
            "tesekkur": [
                "Bereketli olsun dostum, kârı cebe koymayı sakın ihmal etme ☕ Afiyetle harca!",
                "Rica ederim, disiplinli kalan her zaman kazanır. Birlikte büyümeye devam 🚀",
                "Ne demek dostum, gözün arkada kalmasın. Seviyelere sadık kaldığımız sürece sorun yok."
            ],
            "panik_zarar": [
                "Sakin kal dostum, ekranı kapatıp bir hava al. Panikle verilen karar her zaman zarar ettirir.",
                "Borsada kural 1: Sermayeyi korumak. Stop seviyene sadık kal, piyasada fırsat asla bitmez.",
                "Korkma, panik satanların malını sabırlılar toplar. Planına sadık kalırsan toparlar."
            ],
            "hisse_soran": [
                "Gözüm üzerinde dostum, grafiğini çiziyorum. Akşam kahvesinde detaylı bakarız ☕",
                "Şu an tam direnç bölgesinde, acele edip tepeden atlama. Düzeltmesini bekleyelim.",
                "Listeme aldım, yarın sabah bülteninde ilk ona değineceğim. Bildirimleri aç beklemede kal!"
            ]
        }
    }

def load_config():
    if not os.path.exists(DATA_FILE):
        cfg = get_default_config()
        save_config(cfg)
        return cfg
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def generate_community_post(hisse="SASA"):
    """Yorumlarda en çok sorulan hisse için samimi insan dili analiz tweeti üretir"""
    return f"""Dün akşam yorumlarda en çok sorulan hisse ${hisse.upper()} oldu. Söz verdiğim gibi çayımı aldım, grafiğin başına geçtim. ☕

Dostlar, bu tahtada uzun süredir bezdirme politikası izleniyor. Ama hacim dip seviyelerde kurumaya başladı, bu genellikle dönüşlerin ayak sesidir.

Direnç aşılmadan coşku yok, stop kırılmadan panik yok. 

Maliyeti yüksek olanlar burada mı? Kaçtan bekliyorsunuz, dertleşelim 👇

#{hisse.upper()} #Borsa #BIST100"""

if __name__ == "__main__":
    cfg = load_config()
    print("--- Topluluk İsteği Örnek Tweeti ---")
    print(generate_community_post("SASA"))
