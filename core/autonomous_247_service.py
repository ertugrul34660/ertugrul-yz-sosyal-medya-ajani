import os
import sys
import time
import json
import traceback
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'service_247.log')
HEARTBEAT_FILE = os.path.join(DATA_DIR, 'service_heartbeat.json')

sys.path.append(os.path.join(BASE_DIR, 'core'))

try:
    from continuous_learner import ContinuousLearner
    from cloud_sync_daemon import CloudSyncDaemon
    from autonomous_growth_radar import AutonomousGrowthRadar
except ImportError:
    pass

def log_event(message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line)
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    except Exception:
        pass

def update_heartbeat(status="ONLINE", last_action="Idle"):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        data = {
            "servis_adi": "Ertugrul_YZ_Finans_247_Service",
            "durum": status,
            "son_kalp_atisi": datetime.now().isoformat(),
            "son_islem": last_action,
            "pid": os.getpid()
        }
        with open(HEARTBEAT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def run_247_loop():
    log_event("=====================================================")
    log_event("ERTUGRUL YZ • 7/24 OTONOM BULUT & SERVIS MOTORU BASLADI")
    log_event(f"PID: {os.getpid()} | Proje: {BASE_DIR}")
    log_event("=====================================================")

    learner = None
    cloud_daemon = None
    radar = None

    try:
        learner = ContinuousLearner()
        cloud_daemon = CloudSyncDaemon()
        radar = AutonomousGrowthRadar()
    except Exception as e:
        log_event(f"[Baslatma Hatasi]: {e}")

    tick_count = 0

    while True:
        try:
            tick_count += 1
            now = datetime.now()
            time_str = now.strftime("%H:%M")

            # 1. Her dakika Google Drive Bulut Senkronizasyonu
            if cloud_daemon:
                try:
                    res = cloud_daemon.run_sync_cycle()
                    log_event(f"[Bulut Senkron] 1C_-DTzNWPb5... klasorune {len(res)} dosya denetlendi.")
                except Exception as ce:
                    log_event(f"[Bulut Senkron Hatasi]: {ce}")

            # 2. Kalp Atışı Güncellemesi
            update_heartbeat(status="ONLINE", last_action=f"Dakikalik Bulut ve Gundem Taramasi (Tick #{tick_count})")

            # 3. Her 5 dakikada bir hafıza kontrolü
            if tick_count % 5 == 0 and learner:
                try:
                    learner.sync_proven_records()
                    log_event("[Hafiza] Surekli ogrenme kütüğü tazelendi.")
                except Exception as le:
                    log_event(f"[Hafiza Hatasi]: {le}")

            # 4. Her 45 dakikada bir (Tick % 45 == 0) Organik Sniper & Büyüme Değerlendirmesi
            if tick_count % 45 == 0 and radar:
                try:
                    pol = radar.get_timing_policy()
                    log_event(f"[Organik Sniper Politikasi] Mod: {pol['durum']}, İki Yorum Arası: {pol['yorumlar_arasi_bekleme_sn_min']}-{pol['yorumlar_arasi_bekleme_sn_max']}s, Periyot: {pol['yorum_dalga_periyodu_dakika']}dk")
                except Exception as re:
                    log_event(f"[Radar Hatasi]: {re}")

            # 60 saniye bekle
            time.sleep(60)

        except KeyboardInterrupt:
            log_event("[Kullanici Tarafindan Durduruldu]")
            update_heartbeat(status="STOPPED", last_action="Kullanici durdurdu")
            break
        except Exception as err:
            log_event(f"[Kritik Servis Hatasi]: {err}\n{traceback.format_exc()}")
            time.sleep(10) # Hata sonrasi kisa bekleme ve otonom devam

if __name__ == "__main__":
    run_247_loop()
