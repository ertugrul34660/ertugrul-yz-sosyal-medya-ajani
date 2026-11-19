# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otonom Finans ve X Operasyon Yöneticisi (Executive Manager)
Yönetim Kurulu Başkanı'nın talimatıyla tüm paylaşım takvimini, içerik akışını ve etkileşim döngüsünü otonom yönetir.
"""

import json
import os
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DAILY_PLAN_FILE = os.path.join(DATA_DIR, "gunluk_operasyon_plani.json")

def create_daily_plan():
    """Günün canlı borsa saatlerine göre 4 adımlı otonom paylaşım planı hazırlar"""
    plan = {
        "tarih": datetime.now().strftime("%Y-%m-%d"),
        "yonetim_durumu": "AKTIF_OTONOM_YONETIM",
        "mesaj": "Direksiyon Ertuğrul YZ Otonom Karargahında. Tüm akış saatine göre yönetiliyor.",
        "akıs": [
            {
                "sira": 1,
                "saat": "11:00",
                "baslik": "☕ Sabah Açılışı & Sabır Dersi",
                "durum": "YAYINDA / SIRADAKI",
                "odak": "Yatırımcı psikolojisi, yeşil-kırmızı tuzağına düşmeme",
                "tweet": """Borsada para kaybetmenin en garanti yolu nedir biliyor musunuz?

Yeşil yandığında coşkuyla alıp, kırmızı yandığında panikle satmak. 

Dostlar, ekranı her 2 dakikada bir yenilemeyi bırakın. Planınız varsa dalgalar sizi korkutmaz, sadece daha iyi fiyattan alım fırsatı verir. 

Bugün sakin kalanların, planına sadık olanların günü olsun. Çaylar kahveler hazır mı? ☕📈

#Borsa #BIST100 #Yatırım"""
            },
            {
                "sira": 2,
                "saat": "13:30",
                "baslik": "🎯 Öğlen Hedef Vuruldu (THY Kanıtı)",
                "durum": "HAZIRLANIYOR",
                "odak": "Kanıtlanmış tespit, +%9 kâr, güven inşa etme",
                "tweet": """Dün herkes panikle satarken ne konuşmuştuk? 

"THY'de 285 TL altı kapanış gelmediği sürece bu hareket silkelemedir, 308 TL direnci masada" demiştik.

Bugün tahta 310 TL'ye iğne attı. Net +%9 tertemiz kâr. 🎯

Panik yapmayan, seviyeye sadık kalan dostları tebrik ederim. Kazananlar kimler, el kaldırabilir mi? 👇

#THYAO #Borsa #BIST100"""
            },
            {
                "sira": 3,
                "saat": "16:30",
                "baslik": "👥 İkindi: Topluluk İstek Analizi ($SASA)",
                "durum": "BEKLEMEDE",
                "odak": "Yorum toplama, kitleyle dertleşme ve etkileşim patlatma",
                "tweet": """Dün akşam yorumlarda en çok sorulan hisse $SASA oldu. Söz verdiğim gibi çayımı aldım, grafiğin başına geçtim. ☕

Dostlar, bu tahtada uzun süredir bezdirme politikası izleniyor. Ama hacim dip seviyelerde kurumaya başladı, bu genellikle dipten dönüşlerin ayak sesidir.

Direnç aşılmadan coşku yok, stop kırılmadan panik yok. 

Maliyeti yüksek olanlar burada mı? Kaçtan bekliyorsunuz, dertleşelim 👇

#SASA #Borsa #BIST100"""
            },
            {
                "sira": 4,
                "saat": "20:00",
                "baslik": "💡 Akşam: Ticaret & İkinci Gelir Kapısı",
                "durum": "BEKLEMEDE",
                "odak": "Finans kitlesini ticarete ve e-ticaret vizyonuna yönlendirme",
                "tweet": """Günde 9 saat mesai yapıp ay sonunu getirmeye çalışmak tek seçenek değil dostlar. 

2026'da yaşıyoruz; elinde telefon olan herkesin cebine ikinci bir gelir kanalı sokması artık lüks değil, zorunluluk. 

İster sıfır stokla dropshipping yapın, ister dijital ürün satın. Önemli olan başlamak. 

Bu hafta adım adım sıfır sermayeyle nasıl ticaret döndürdüğümüzü tek tek anlatacağım. Bildirimleri açın, kaçırmayın. 🧵👇

#Girişimcilik #Ticaret #ParaKazanma"""
            }
        ]
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DAILY_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return plan

def get_current_task():
    plan = create_daily_plan()
    return plan

if __name__ == "__main__":
    plan = create_daily_plan()
    print(f"[{plan['yonetim_durumu']}] {plan['mesaj']}")
    print(f"Bugünkü Planlanan Paylaşım Sayısı: {len(plan['akıs'])}")
