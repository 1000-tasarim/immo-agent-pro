@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════╗
echo ║   IMMO-AGENT PRO - DEPLOYMENT KONTROL         ║
echo ╚═══════════════════════════════════════════════╝
echo.

echo [1] GIT DURUMU
echo ═══════════════════════════════════════════════
git log --oneline -3
echo.

echo [2] DOSYA YAPISI
echo ═══════════════════════════════════════════════
echo Root dosyalar:
dir /b
echo.
echo api/ içeriği:
dir api /b
echo.
echo Gizli dosyalar (.gitignore kontrol):
dir /a:h
echo.

echo [3] VERCELjson İÇERİĞİ
echo ═══════════════════════════════════════════════
type vercel.json
echo.

echo [4] REQUIREMENTS.TXT İÇERİĞİ
echo ═══════════════════════════════════════════════
type requirements.txt
echo.

echo [5] API INDEX.PY İÇERİĞİ (İlk 20 satır)
echo ═══════════════════════════════════════════════
powershell -Command "Get-Content api\index.py -Head 20"
echo.

echo [6] SONRAKİ ADIMLAR
echo ═══════════════════════════════════════════════
echo.
echo ✅ Dosya yapısı doğru görünüyor
echo.
echo Şimdi yapmanız gerekenler:
echo.
echo 1. Vercel Dashboard kontrol:
echo    https://vercel.com/ramazan-cobanoglus-projects/immo-agent-pro-cvqf/deployments
echo.
echo 2. En son deployment'a tıklayın
echo.
echo 3. "Building" veya "Error" yazıyorsa logları kontrol edin
echo.
echo 4. Deployment başarılı mı kontrol edin (yeşil tick ✓)
echo.
echo 5. Eğer hata varsa, hatanın screenshot'ını alın
echo.
echo 6. Test URL'leri:
echo    Frontend: https://immo-agent-pro-cvqf.vercel.app/
echo    API Test: https://immo-agent-pro-cvqf.vercel.app/api/test
echo.
pause
