# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otonom Finans ve Borsa Analiz Ajanı
Piyasa verilerini analiz eder ve LM Studio (Llama 3.1) ile X (Twitter) içerikleri üretir.
"""

import json
import os
import urllib.request
import urllib.error

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "latest_analysis.json")

def generate_market_analysis(market_type="bist"):
    prompt = f"""Sen Ertuğrul YZ Holding'in Baş Finans ve Borsa Analisti Ajanısın.
Türkiye piyasaları ({market_type.upper()}) ve yatırımcı psikolojisi üzerine günün en etkili, profesyonel ve etkileşim alacak 2 cümlelik bir X (Twitter) analizi yaz.
Sonuna 3 adet uygun hashtag (#Borsa, #BIST100, #Finans gibi) ekle.
Sadece tweet metnini ver, başka hiçbir açıklama yazma."""

    # LM Studio yerel sunucusuna bağlanmayı dene
    try:
        url = "http://localhost:1234/v1/chat/completions"
        payload = {
            "messages": [
                {"role": "system", "content": "Sen profesyonel bir borsa ve finans analisti yapay zekâsın."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            tweet = res_data["choices"][0]["message"]["content"].strip()
            return {"source": "Yerel Llama 3.1", "tweet": tweet}
    except Exception as e:
        # Çevrimdışı / Fallback profesyonel finans kütüphanesi
        fallback_templates = {
            "bist": "BIST 100 endeksinde destek ve direnç seviyeleri test edilirken sabırlı kalan yatırımcı kârı cebine koyar. Piyasanın dalgalanması fırsat yaratır; plana sadık kalın. 📈🪙\n\n#BIST100 #Borsa #Yatırım",
            "altin": "Küresel belirsizliklerin arttığı dönemlerde güvenli liman altın her zaman yatırımcısının kalkanı olmuştur. Sepetteki dengeyi korumak panik anlarında hayat kurtarır. 🥇\n\n#Altın #OnsAltın #Ekonomi",
            "kripto": "Kripto piyasasında sabırsızların parası sabırlı olanların cüzdanına akar. Duyguları masanın dışında bırakıp risk yönetimini elden bırakmayanlar kazanır. 🚀💎\n\n#Bitcoin #Kripto #BTC"
        }
        return {"source": "Yerel Analiz Motoru", "tweet": fallback_templates.get(market_type, fallback_templates["bist"])}

if __name__ == "__main__":
    result = generate_market_analysis("bist")
    print(f"[{result['source']}] Üretilen Tweet:\n{result['tweet']}")
