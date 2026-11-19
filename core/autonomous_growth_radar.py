import os
import json
import random
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
QUEUE_FILE = os.path.join(DATA_DIR, 'radar_targets_queue.json')
WALL_QUEUE_FILE = os.path.join(DATA_DIR, 'wall_forecast_queue.json')

# 0. Aşama: Zamanlama ve Aralık Politikası (Turbo Hızlı Büyüme Modu)
TIMING_POLICY = {
    "yorumlar_arasi_bekleme_sn_min": 30,   # 30 saniye (Hızlı organik insan hızı)
    "yorumlar_arasi_bekleme_sn_max": 60,   # 60 saniye
    "yorum_dalga_periyodu_dakika": 10,     # Her 10-15 dakikada bir aktif tarama ve sniper döngüsü
    "gunluk_maksimum_yorum": 50,           # Hızlı takipçi kazanımı için yüksek frekanslı etkileşim
    "durum": "TURBO_HIZLI_BUYUME_MODU"
}

# 1. Aşama: Taranacak Arama ve Gündem Konuları
RADAR_SEARCH_QUERIES = [
    "halka arz tavan",
    "halka arz hisse",
    "BIST100 endeks",
    "borsa hedef",
    "#HalkaArz",
    "#BIST100"
]

# 2. Aşama: Bağlama Göre Seçilecek Sniper Yorum Şablonları (Kesinlikle $ işareti yok)
SNIPER_COMMENT_LIBRARY = {
    "halka_arz": [
        "Halka arzlarda tavan serisinde kaçıncı günde olduğundan çok, tavandaki bekleyen lot miktarının erime hızını izlemek gerekir. Emir silmeler başladığında kâr realizasyonu planı hazır olmalı. Disiplin kazandırır.",
        "Halka arz hissesinde tavan kilit bozulduğunda panikle tabana emir yazmak yerine, hacimli dip desteğinin oluşmasını beklemek sermayeyi korur. Seviyesini bilen kazanır.",
        "Tavan serisi bozulduktan sonra hissenin kaderini küçük yatırımcı satışı değil, kurumsal fonların takas toplaması belirler. Temeli sağlamsa kademede sabredilir."
    ],
    "endeks_ve_seviye": [
        "11.800 desteğindeki yatay hareketler düzeltme sürecinin parçasıdır. Sağlıklı bir yükseliş için bu dinlenmeler şart. Günlük dalgalara değil, büyük resme odaklanan kazanır.",
        "Endekste 11.850 üzerindeki kalıcılık 12.000 direncini masada tutuyor. Ancak bu dönemde endeksten ziyade doğru hissede sabreden kazanır. Disiplin kazandırır.",
        "Piyasa sabırsızlardan sabırlılara para aktarma mekanizmasıdır. Doğru seviyeden maliyetlenen için her geri çekilme fırsattır."
    ],
    "sektor_ve_hisse": [
        "Faiz indirim döngüsünde bilanço gücü ve nakit akışı yüksek sanayi devleri öncülüğünde yeni bir ralli dönemi göreceğiz. Sabır masada tutar.",
        "Kısa vadeli gürültüye takılmadan, büyük resme ve bilanço gücüne odaklanan yatırımcı her zaman hedefine ulaşır. Disiplin = Özgürlük.",
        "Borsada para kaybettiren hisseler değil; plansızlık ve FOMO'dur. Dip teyidini alan hissede bekleyen masadan kârlı kalkar."
    ]
}

# 3. Aşama: Kendi Duvarımızda Paylaşılacak Borsa Öngörüleri (Kesinlikle $ işareti yok)
WALL_FORECAST_TEMPLATES = [
    {
        "baslik": "Kapanış Öncesi Nabız (17:15 Kuşağı)",
        "metin": "BIST 100 seans kapanışına doğru 11.800 üzerinde dengeleniyor. 📊\n\nSon saatlerde para girişi olan hisselerde yarın için pozitif ayrışma görebiliriz.\n\nPanikle değil, seviyeyle işlem yap. Akşam kapanış bülteninde detayları konuşacağız. ☕\n\n#BIST100 #Borsa"
    },
    {
        "baslik": "Seans Kapanış Karnesi (18:15 Kuşağı)",
        "metin": "Günü tamamladık. THYAO, ASELSAN ve TÜPRAŞ'ta dip seviyelerden yakaladığımız kâr realizasyonları saat gibi işledi. 🎯\n\n11.800 desteği korundukça trend yukarı.\n\nDisiplinle kazanan tüm dostları tebrik ederim. Akşam KCHOL analizimiz yayında olacak. ☕🚀\n\n#Borsa #BIST100"
    },
    {
        "baslik": "Koç Holding (KCHOL) Orta Vade Projeksiyonu (19:30 Kuşağı)",
        "metin": "Koç Holding (KCHOL) için orta vade projeksiyonumuz: 🎯\n\nNet Aktif Değerine (NAD) göre %35'in üzerinde iskontoyla işlem gören hissede dip konsolidasyonu tamamlanıyor.\n\nGeleceğe yönelik hedef bandımız 245 - 265 TL.\n\nBüyük resme bakan kazanır. ☕📈\n\n#KCHOL #Borsa #BIST100"
    },
    {
        "baslik": "Gece Strateji Bülteni (21:00 Kuşağı)",
        "metin": "Yarın seans açılışında takip edeceğimiz 2 kritik altın kural: 🧠\n\n1. 11.800 altı kapanış gelmedikçe panik satışı yok.\n2. Tavan kovalayan değil, dip dönüşü teyitli hisselerde kademeli pozisyon.\n\nPlana sadık kal, yarın kazanmaya devam edelim. İyi geceler. ☕\n\n#BIST100 #Borsa"
    }
]

class AutonomousGrowthRadar:
    """
    3 Ayaklı Otonom Büyüme & Paylaşım Motoru:
    1. X Platformunu ve arama akışlarını tarar.
    2. Bulunan paylaşımlara bağlama uygun sniper yorumlar üretir.
    3. Kendi duvarımızda düzenli borsa öngörüleri yayınlar.
    """
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    def get_next_wall_forecast(self, current_hour_minute):
        # Saat dilimine göre en uygun öngörüyü seçer
        if "16:" in current_hour_minute or "17:" in current_hour_minute:
            return WALL_FORECAST_TEMPLATES[0] # Kapanış Öncesi Nabız
        elif "18:" in current_hour_minute:
            return WALL_FORECAST_TEMPLATES[1] # Kapanış Karnesi
        elif "19:" in current_hour_minute or "20:" in current_hour_minute:
            return WALL_FORECAST_TEMPLATES[2] # KCHOL Analizi
        else:
            return WALL_FORECAST_TEMPLATES[3] # Gece Bülteni

    def get_sniper_comment(self, category="halka_arz"):
        comments = SNIPER_COMMENT_LIBRARY.get(category, SNIPER_COMMENT_LIBRARY["endeks_ve_seviye"])
        return random.choice(comments)

    def get_timing_policy(self):
        return TIMING_POLICY

    def get_comment_delay_seconds(self):
        """İki yorum arasında beklenmesi gereken organik saniye (3-5 dk)"""
        return random.randint(TIMING_POLICY["yorumlar_arasi_bekleme_sn_min"], TIMING_POLICY["yorumlar_arasi_bekleme_sn_max"])

if __name__ == "__main__":
    radar = AutonomousGrowthRadar()
    now_hm = datetime.now().strftime("%H:%M")
    forecast = radar.get_next_wall_forecast(now_hm)
    comment = radar.get_sniper_comment("halka_arz")
    print(f"[{now_hm}] Otonom Radar Hazır:")
    print("Sıradaki Duvar Öngörüsü:", forecast["baslik"])
    print("Sıradaki Halka Arz Yorumu:", comment)
