@echo off
chcp 65001 >nul
title Ertugrul YZ - Google Drive Bulut Senkronizasyon & Surekli Ogrenme Motoru
color 0B

echo ======================================================================
echo    ERTUGRUL YZ - GOOGLE DRIVE BULUT SENKRONIZASYON & OGRENME
echo ======================================================================
echo.
echo [1/2] Surekli Ogrenme Motoru Calistiriliyor...
python "%~dp0..\core\continuous_learner.py"
echo.
echo [2/2] Google Drive Bulut Senkronizasyonu Baslatiliyor...
python "%~dp0..\core\cloud_sync_daemon.py"
echo.
echo ======================================================================
echo    BULUT ESITLEMESI BASARIYLA TAMAMLANDI!
echo    Google Drive Klasoru: Ertugrul_YZ_Finans_Cloud
echo ======================================================================
timeout /t 5 >nul
exit
