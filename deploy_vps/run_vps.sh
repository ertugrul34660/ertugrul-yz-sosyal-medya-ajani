#!/bin/bash
# Ertugrul YZ - 7/24 Linux VPS Hizli Baslatici
echo "=========================================================="
echo "   ERTUGRUL YZ - 7/24 OTONOM BULUT VPS KURULUMU"
echo "=========================================================="

# 1. Dizin ve Izinler
mkdir -p /opt/ertugrul-yz-finans
cp -r . /opt/ertugrul-yz-finans/

# 2. Systemd Servis Kurulumu
cp deploy_vps/ertugrul-yz-finans.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable ertugrul-yz-finans.service
systemctl restart ertugrul-yz-finans.service

echo ""
echo "[OK] 7/24 Otonom Borsa Motoru Systemd servisi olarak baslatildi!"
systemctl status ertugrul-yz-finans.service --no-pager
