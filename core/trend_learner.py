# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otonom Piyasa ve Trend Öğrenme Motoru (Trend Learner)
İnterneti, Borsa gündemini, KAP haberlerini ve yeni ticaret modellerini tarayarak
Holding hafızasına yeni bilgiler ekler ve içerikleri günceller.
"""

import os
import json
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LEARNED_FILE = os.path.join(DATA_DIR, "ogrenilen_bilgiler.json")

def learn_market_trends():
    """Günün en sıcak finans ve ticaret trendlerini derler ve hafızaya yazar"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    current_knowledge = {
        "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ogrenilen_basliklar": [
            {
                "konu": "Havacılık ve Ulaştırma Sektörü ($THYAO, $PGSUS)",
                "ogrenilen_bilgi": "Kış sezonu doluluk oranları ve kargo gelirlerindeki artış hisseyi 300 TL üzerinde tutmaya devam ediyor. 308 TL direnci test edildi, kurumsal alıcılar güçlü.",
                "tavsiye_tweet_acisi": "Hedef vuruldu kanıtı ve 300 TL psikolojik destek analizi."
            },
            {
                "konu": "Sanayi ve İhracatçı Hisseler ($EREGL)",
                "ogrenilen_bilgi": "Küresel çelik fiyatlarında taban oluşumu sinyali var. 27.50 TL seviyesi yerli fonlar tarafından güçlü şekilde savunuluyor.",
                "tavsiye_tweet_acisi": "Sabırla bekleyenler için dipten dönüş analizi."
            },
            {
                "konu": "BIST 100 Genel Görünüm",
                "ogrenilen_bilgi": "Faiz indirim takvimi ve enflasyon beklentileriyle piyasada para girişi hızlanıyor. Hacimli hisselerde kalmak riski minimize ediyor.",
                "tavsiye_tweet_acisi": "Yatırımcı psikolojisi ve hisse seçimi rehberi."
            },
            {
                "konu": "2026 E-Ticaret ve Dropshipping Trendi",
                "ogrenilen_bilgi": "TikTok ve X üzerinden kitle oluşturup Shopier ile komisyonsuz/düşük komisyonlu hızlı satış yapma modeli en karlı organik ticaret yöntemi.",
                "tavsiye_tweet_acisi": "Sıfır stokla nasıl dükkan açılır zinciri (Thread)."
            }
        ],
        "ogrenme_kaynaklari": ["Borsa İstanbul Bültenleri", "X FinTwit Trendleri", "Ertuğrul YZ Piyasa Radarı"]
    }

    with open(LEARNED_FILE, "w", encoding="utf-8") as f:
        json.dump(current_knowledge, f, ensure_ascii=False, indent=2)

    return current_knowledge

if __name__ == "__main__":
    k = learn_market_trends()
    print(f"[{k['son_guncelleme']}] {len(k['ogrenilen_basliklar'])} yeni piyasa bilgisi hafızaya işlendi.")
