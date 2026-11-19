# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otomatik X Paylaşım Fırlatıcısı (Auto Publisher)
İstenen sıradaki tweeti tarayıcı üzerinden anında yayına gönderir.
"""

import sys
import os
import json
import urllib.parse
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN_FILE = os.path.join(ROOT_DIR, "data", "gunluk_operasyon_plani.json")

def publish_slot(slot_number=1):
    if not os.path.exists(PLAN_FILE):
        print("Operasyon planı bulunamadı.")
        return False
    
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)

    target_slot = None
    for item in plan.get("akıs", []):
        if item["sira"] == slot_number:
            target_slot = item
            break

    if not target_slot:
        print(f"{slot_number}. sıra bulunamadı.")
        return False

    tweet_text = target_slot["tweet"]
    encoded = urllib.parse.quote(tweet_text)
    intent_url = f"https://twitter.com/intent/tweet?text={encoded}"

    # Windows varsayılan tarayıcısında X'i açar
    os.system(f'start "" "{intent_url}"')
    
    # Durumu güncelle
    target_slot["durum"] = "YAYINLANDI"
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"[{target_slot['saat']}] {target_slot['baslik']} yayına verildi.")
    return True

if __name__ == "__main__":
    slot = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    publish_slot(slot)
