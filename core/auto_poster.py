# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Tam Otonom X Paylaşım Ajanı (Auto-Poster)
Tarayıcıyı açar, tweet metnini yükler ve beklemeden klavye kısayoluyla (Ctrl+Enter) doğrudan yayınlar.
"""

import time
import os
import sys
import urllib.parse
import ctypes

VK_CONTROL = 0x11
VK_RETURN = 0x0D

def send_ctrl_enter_native():
    """Windows API ile Ctrl + Enter tuşuna basıp gönder butonunu tetikler"""
    # CTRL bas
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.1)
    # ENTER bas
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.1)
    # ENTER bırak
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 2, 0)
    time.sleep(0.1)
    # CTRL bırak
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)

def publish_completely_autonomous(tweet_text):
    encoded = urllib.parse.quote(tweet_text)
    intent_url = f"https://x.com/intent/tweet?text={encoded}"
    
    # 1. Chrome ile aç
    print("[1/3] X paylaşım ekranı Chrome'da açılıyor...")
    os.system(f'start chrome "{intent_url}"')
    
    # 2. Sayfanın yüklenmesi ve kutunun odaklanması için bekle
    print("[2/3] Sayfa yükleniyor (4 saniye bekleniyor)...")
    time.sleep(4)
    
    # 3. Windows Native API ile Ctrl + Enter tuşlayarak 'Gönder' butonuna bas
    try:
        print("[3/3] Ctrl + Enter kısayolu gönderiliyor (Gönder butonu tetikleniyor)...")
        send_ctrl_enter_native()
        print("✅ Tweet başarıyla otonom olarak fırlatıldı!")
        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False

if __name__ == "__main__":
    test_text = sys.argv[1] if len(sys.argv) > 1 else "Ertuğrul YZ Otonom Test"
    publish_completely_autonomous(test_text)
