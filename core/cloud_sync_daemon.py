import os
import sys
import json
import time
import hashlib
import subprocess
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
POST_CARDS_DIR = os.path.join(ASSETS_DIR, 'post_cards')
MANIFEST_FILE = os.path.join(DATA_DIR, 'cloud_sync_manifest.json')

# Google Drive Cloud Klasör Kimliği
CLOUD_FOLDER_ID = "1C_-DTzNWPb5qdm_E6LqYjcFq7ishbXr1"

def calculate_hash(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

class CloudSyncDaemon:
    """
    Ertuğrul YZ Google Drive Bulut Senkronizasyon Motoru
    Hafıza dosyalarını, operasyon planlarını ve grafik analiz kartlarını
    Google Drive ile her dakika senkronize eder.
    """
    def __init__(self, folder_id=CLOUD_FOLDER_ID):
        self.folder_id = folder_id
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(MANIFEST_FILE):
            try:
                with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "son_esitleme": None,
            "bulut_klasor_id": self.folder_id,
            "dosyalar": {}
        }

    def _save_manifest(self):
        self.manifest["son_esitleme"] = datetime.now().isoformat()
        with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, ensure_ascii=False, indent=2)

    def get_trackable_files(self):
        files = []
        # 1. Veri dosyaları
        for fname in ["ogrenilen_bilgiler.json", "gunluk_operasyon_plani.json", "personel_karne_ledger.json", "sniper_campaign_queue.json"]:
            fpath = os.path.join(DATA_DIR, fname)
            if os.path.exists(fpath):
                files.append(fpath)
        
        # 2. X Banner
        banner_path = os.path.join(ASSETS_DIR, "x_banner_ertugrul_yz.png")
        if os.path.exists(banner_path):
            files.append(banner_path)

        # 3. Post kartları
        if os.path.exists(POST_CARDS_DIR):
            for fname in os.listdir(POST_CARDS_DIR):
                if fname.endswith(".png"):
                    files.append(os.path.join(POST_CARDS_DIR, fname))

        return files

    def sync_file(self, filepath):
        rel_name = os.path.basename(filepath)
        curr_hash = calculate_hash(filepath)
        if not curr_hash:
            return

        file_meta = self.manifest["dosyalar"].get(rel_name, {})
        drive_file_id = file_meta.get("drive_id")
        last_hash = file_meta.get("hash")

        # Dosya değişmemişse atla
        if drive_file_id and last_hash == curr_hash:
            return {"status": "DEGISMEDI", "file": rel_name, "drive_id": drive_file_id}

        if drive_file_id:
            # Güncelle (Update)
            print(f"[CloudSync] Guncelleniyor (Update): {rel_name} -> {drive_file_id}")
            cmd = ["gdrive", "mutate", "update", drive_file_id, filepath, "--json"]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
                self.manifest["dosyalar"][rel_name] = {
                    "drive_id": drive_file_id,
                    "hash": curr_hash,
                    "son_guncelleme": datetime.now().isoformat()
                }
                self._save_manifest()
                return {"status": "GUNCELLENDI", "file": rel_name, "drive_id": drive_file_id}
            except Exception as e:
                print(f"[CloudSync Error] Guncelleme hatasi {rel_name}: {e}")
                return {"status": "HATA", "file": rel_name, "error": str(e)}
        else:
            # Yeni Yükle (Upload)
            print(f"[CloudSync] Yeni Yukleniyor (Upload): {rel_name} -> Klasor {self.folder_id}")
            cmd = ["gdrive", "mutate", "upload", filepath, "--parent", self.folder_id, "--json"]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
                # Parse drive file ID from output
                out = res.stdout.strip()
                drive_id = None
                try:
                    data = json.loads(out)
                    drive_id = data.get("id") or data.get("Id") or data.get("fileId")
                except Exception:
                    # Fallback string parsing
                    for line in out.splitlines():
                        if "ID:" in line or "Uploaded file:" in line:
                            parts = line.split("ID:")
                            if len(parts) > 1:
                                drive_id = parts[1].strip().rstrip(")")
                
                if drive_id:
                    self.manifest["dosyalar"][rel_name] = {
                        "drive_id": drive_id,
                        "hash": curr_hash,
                        "son_guncelleme": datetime.now().isoformat()
                    }
                    self._save_manifest()
                    return {"status": "YUKLENDI", "file": rel_name, "drive_id": drive_id}
                else:
                    return {"status": "BELIRSIZ", "file": rel_name, "output": out}
            except Exception as e:
                print(f"[CloudSync Error] Yukleme hatasi {rel_name}: {e}")
                return {"status": "HATA", "file": rel_name, "error": str(e)}

    def run_sync_cycle(self):
        files = self.get_trackable_files()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CloudSync cevrimi basladi. Takip edilen: {len(files)} dosya.")
        results = []
        for f in files:
            res = self.sync_file(f)
            if res:
                results.append(res)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CloudSync cevrimi tamamlandi. Islem adedi: {len(results)}")
        return results

if __name__ == "__main__":
    daemon = CloudSyncDaemon()
    results = daemon.run_sync_cycle()
    print(json.dumps(results, indent=2, ensure_ascii=False))
