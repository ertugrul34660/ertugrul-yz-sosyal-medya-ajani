import os
import json
from datetime import datetime

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
KNOWLEDGE_FILE = os.path.join(DATA_DIR, 'ogrenilen_bilgiler.json')

class ContinuousLearner:
    """
    Ertuğrul YZ Sürekli Öğrenme Motoru
    Piyasadan, yayınlanan analizlerden, takipçi etkileşimlerinden ve algoritmik kurallardan
    öğrenilen her veriyi dinamik hafızaya işler ve bulut senkronizasyonuna hazırlar.
    """
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.knowledge = self._load()

    def _load(self):
        data = {}
        if os.path.exists(KNOWLEDGE_FILE):
            try:
                with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                pass
        
        # Standart şema garantisi
        data.setdefault("son_guncelleme", datetime.now().isoformat())
        data.setdefault("ogrenilen_piyasa_kaliplari", [])
        data.setdefault("kanitlanmis_hisse_seviyeleri", {})
        data.setdefault("algoritma_ve_etkilesim_kurallari", [])
        data.setdefault("stratejik_kararlar", [])
        return data

    def save(self):
        self.knowledge["son_guncelleme"] = datetime.now().isoformat()
        with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        print(f"[ContinuousLearner] Hafiza basariyla kaydedildi: {KNOWLEDGE_FILE}")

    def add_market_pattern(self, pattern_name, details, confidence=0.95):
        self.knowledge.setdefault("ogrenilen_piyasa_kaliplari", [])
        # Varsa güncelle, yoksa ekle
        for p in self.knowledge["ogrenilen_piyasa_kaliplari"]:
            if p.get("kalip") == pattern_name:
                p["detay"] = details
                p["guven_skoru"] = confidence
                p["guncelleme"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                return p
        entry = {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kalip": pattern_name,
            "detay": details,
            "guven_skoru": confidence
        }
        self.knowledge["ogrenilen_piyasa_kaliplari"].append(entry)
        self.save()
        return entry

    def record_stock_milestone(self, symbol, entry_level, target_level, gain_pct, status="KAZANC_ALINDI"):
        self.knowledge.setdefault("kanitlanmis_hisse_seviyeleri", {})
        self.knowledge["kanitlanmis_hisse_seviyeleri"][symbol] = {
            "giris_dip_seviyesi": entry_level,
            "hedef_seviye": target_level,
            "kazanc_orani": gain_pct,
            "durum": status,
            "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save()

    def add_algorithmic_rule(self, rule_name, rule_desc):
        self.knowledge.setdefault("algoritma_ve_etkilesim_kurallari", [])
        for r in self.knowledge["algoritma_ve_etkilesim_kurallari"]:
            if r.get("kural") == rule_name:
                r["aciklama"] = rule_desc
                r["guncelleme"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                return r
        entry = {
            "kural": rule_name,
            "aciklama": rule_desc,
            "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.knowledge["algoritma_ve_etkilesim_kurallari"].append(entry)
        self.save()
        return entry

    def sync_proven_records(self):
        # Bugüne kadar kanıtlanan somut hisse başarıları
        self.record_stock_milestone("THYAO", 302.0, 329.5, "+%9.03", "KAZANC_ALINDI_TAM_ISABET")
        self.record_stock_milestone("ASELS", 60.15, 65.95, "+%9.64", "KAZANC_ALINDI_TAM_ISABET")
        self.record_stock_milestone("TUPRS", 142.0, 153.0, "+%8.73", "KAZANC_ALINDI_TAM_ISABET")
        self.record_stock_milestone("EREGL", 48.50, 72.0, "+%48.00 (Hedef Projeksiyon)", "ORTA_VADE_TAKIPTE")

        # Algoritmik Altın Kurallar
        self.add_algorithmic_rule("Dolar Isareti Yasagi", "FinTwit paylasimlarinda $ isareti kesinlikle kullanilmaz; # veya yalin hisse kodu tercih edilir.")
        self.add_algorithmic_rule("Karakter Optimizasyonu", "X ucretsiz hesaplarda gercek karakter limiti 280 olmasina ragmen emoji/link agirliklari nedeniyle 210-230 karakter arasinda tutulmalidir.")
        self.add_algorithmic_rule("Kurumsal Ekosistem Takibi", "0 Following izolasyonunu kirmak icin Borsa Istanbul, SPK, TCMB, BloombergHT, Matriks ve Investing takip edilerek hesap FinTwit haritasina eklemlenmistir.")
        self.add_algorithmic_rule("Sniper Yorum Stratejisi", "Populer borsa tweetlerinin altina reklam yapmadan deger katan teknik yorumlar birakmak, sifir takipcili hesaba organik profil tiklamasi kazandirir.")

        # Piyasa Kalıpları
        self.add_market_pattern("11.800 BIST Konsolidasyonu", "Endeks 11.800 destegi etrafinda yatay dalgalanirken panik satisi yapanlar kaybeder; sektor ve hisse bazli dip donuslerini takip edenler kazanir.", 0.98)
        self.add_market_pattern("Demir Celik Dip Dongusu", "Kuresel emtia ve hurda/cevher fiyatlarinda en kotu donem geride kaldi; EREGL 48.50-52 bandi guclu dip olusumudur.", 0.92)

if __name__ == "__main__":
    learner = ContinuousLearner()
    learner.sync_proven_records()
    print("Sürekli öğrenme hafızası başarıyla eşitlendi!")
