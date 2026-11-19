# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otonom Yorum ve Etkileşim Gözlemcisi (Comment Watcher)
@sessizceyazacaz hesabına gelen yorumları denetler, soruları tespit eder ve
samimi insan diliyle anında yanıt üretir.
"""

import os
import json
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
COMMENTS_LOG_FILE = os.path.join(DATA_DIR, "yorum_takip_gunlugu.json")

def initialize_comment_log():
    if not os.path.exists(COMMENTS_LOG_FILE):
        initial_data = {
            "hesap": "@sessizceyazacaz",
            "son_kontrol": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "durum": "NOBETCI_AKTIF",
            "tespit_edilen_yorumlar": [
                {
                    "id": "c-001",
                    "kullanici": "ornek_takipci",
                    "yorum_metni": "Hocam SASA ne zaman toparlar?",
                    "kategori": "HISSE_SORUSU",
                    "hazir_insan_dili_yanit": "Gözüm üzerinde dostum, grafiğini çizdim. Akşam çayında özel olarak değineceğim, bildirimleri aç beklemede kal! ☕📊",
                    "yanit_durumu": "BEKLEMEDE"
                }
            ]
        }
        with open(COMMENTS_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)

def check_and_categorize_comment(user_comment):
    """Gelen bir yorumu analiz eder ve en uygun insan dili cevabı döner"""
    txt = user_comment.lower()
    if any(w in txt for w in ["teşekkür", "eline sağlık", "harika", "kazandık", "sayende", "bereket"]):
        return {
            "kategori": "TESEKKUR",
            "yanit": "Bereketli olsun dostum, kârı cebe koymayı sakın ihmal etme ☕ Afiyetle harca! Birlikte kazanmaya devam."
        }
    elif any(w in txt for w in ["zarar", "battık", "korkuyorum", "panik", "düştü", "stop"]):
        return {
            "kategori": "PANIK_ZARAR",
            "yanit": "Sakin ol dostum, ekranı kapatıp bir kahve iç. Panikle satılan malı her zaman sabırlı olan toplar. Stopuna sadık kal, piyasada fırsat bitmez."
        }
    else:
        return {
            "kategori": "GENEL_SORU",
            "yanit": "Listeme aldım dostum, grafiği masada. Akşam bülteninde detaylıca bakacağız, takipte kal! ☕📊"
        }

if __name__ == "__main__":
    initialize_comment_log()
    print("Yorum Takip Nöbetçisi Hazır.")
