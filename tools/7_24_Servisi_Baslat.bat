@echo off
chcp 65001 >nul
title Ertugrul YZ - 7/24 Kesintisiz Otonom Servis Yoneticisi
color 0A

echo ======================================================================
echo       ERTUGRUL YZ - 7/24 KESINTISIZ OTONOM SERVIS YONETICISI
echo ======================================================================
echo.
echo [1] 7/24 Arka Plan Servisini Baslat (Gorunmez Mod)
echo [2] Canli Log Akisini Izle (service_247.log)
echo [3] Windows Acilisina Ekle (Oto-Baslatma Zirhi)
echo [4] Servisi Durdur
echo [0] Cikis
echo.
set /p secim="Seciminiz (0-4): "

if "%secim%"=="1" goto BASLAT
if "%secim%"=="2" goto LOG_IZLE
if "%secim%"=="3" goto OTO_EKLE
if "%secim%"=="4" goto DURDUR
goto CIKIS

:BASLAT
wscript.exe "%~dp0Start_247_Background.vbs"
echo.
echo [OK] 7/24 Otonom Servis arka planda sessizce baslatildi!
timeout /t 3 >nul
exit

:LOG_IZLE
cls
echo [Canli Log Akisi - Cikmak icin Ctrl+C]
powershell -Command "Get-Content -Path '%~dp0..\data\service_247.log' -Wait -Tail 30"
pause
goto CIKIS

:OTO_EKLE
schtasks /create /tn "Ertugrul_YZ_724_Service" /tr "wscript.exe \"%~dp0Start_247_Background.vbs\"" /sc onlogon /f
echo.
echo [OK] Windows acilisina basariyla eklendi! Bilgisayar her acildiginda otomatik calisacak.
pause
goto CIKIS

:DURDUR
taskkill /f /im python.exe /fi "WINDOWTITLE eq *autonomous_247_service*" 2>nul
echo [OK] Servis durduruldu.
pause
goto CIKIS

:CIKIS
exit
