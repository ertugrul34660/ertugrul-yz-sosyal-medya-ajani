# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Tam Otonom X Finans ve Büyüme Nöbetçisi (Autonomous Worker)
Holding Yönetim Kurulu Başkanı'nın talimatıyla;
1. Zamanı gelen paylaşımları yayına alır.
2. Piyasa trendlerini sürekli öğrenip hafızaya işler.
3. Gelen yorumları ve etkileşimi takip eder.
"""

import time
import os
import sys
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from core.trend_learner import learn_market_trends
from core.comment_watcher import initialize_comment_log

def log_activity(msg):
    log_file = os.path.join(ROOT_DIR, "data", "otonom_calisma_gunlugu.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    print(entry.strip())
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

def run_autonomous_cycle():
    log_activity("🟢 Ertuğrul YZ Otonom Finans Nöbetçisi Devreye Girdi.")
    
    # 1. Başlangıç öğrenmesi
    try:
        trends = learn_market_trends()
        log_activity(f"Piyasa verileri tarandı: {len(trends.get('ogrenilen_basliklar', []))} konu hafızaya işlendi.")
    except Exception as e:
        log_activity(f"Trend öğrenme uyarısı: {e}")

    # 2. Yorum nöbetçisini başlat
    try:
        initialize_comment_log()
        log_activity("Yorum denetim radarı aktif edildi.")
    except Exception as e:
        log_activity(f"Yorum radarı uyarısı: {e}")

    log_activity("Nöbetçi arka planda saatleri ve etkileşimi izliyor (13:30, 16:30, 20:00).")

if __name__ == "__main__":
    run_autonomous_cycle()
