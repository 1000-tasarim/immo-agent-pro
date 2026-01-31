# 🚀 Immo-Agent Pro - Deployment Anleitung

## ⚠️ WICHTIG: Alte Dateien LÖSCHEN!

Bevor Sie die neuen Dateien deployen, **MÜSSEN** Sie diese löschen:

```bash
# IM REPOSITORY ROOT:
git rm main.py                    # Falls vorhanden
git rm -rf api/                   # Falls alte api/ vorhanden
git rm vercel.json               # Alte Config löschen
git commit -m "cleanup: remove old files"
git push
```

## 📁 Korrekte Dateistruktur

```
immo-agent-pro/
├── api/
│   └── index.py          ← Serverless Function (FastAPI + Mangum)
├── index.html            ← Frontend (Root)
├── requirements.txt      ← Python Dependencies
├── vercel.json          ← Vercel Config
├── .gitignore           ← Git Ignore
└── DEPLOYMENT.md        ← Diese Datei
```

## 🔧 Schritt-für-Schritt Deployment

### Schritt 1: Dateien Vorbereiten

```bash
# Navigieren Sie zu Ihrem Projekt
cd Y:\Lkhst.DE\SIGNBOXX\Ram\Ajan\immo-agent-pro

# Alte Dateien löschen (WICHTIG!)
git rm main.py 2>/dev/null || true
git rm -rf api/ 2>/dev/null || true
git rm vercel.json 2>/dev/null || true

# Neue Dateien kopieren
# (Kopieren Sie alle Dateien aus dem clean-project/ Ordner hierher)

# Dateistruktur prüfen
ls -la
# Sie sollten sehen:
# - api/index.py
# - index.html
# - requirements.txt
# - vercel.json
# - .gitignore
```

### Schritt 2: Git Commit & Push

```bash
git add .
git commit -m "refactor: complete restructure for vercel serverless"
git push origin main
```

### Schritt 3: Vercel Environment Variables

1. **Gehen Sie zu:** https://vercel.com/dashboard
2. **Ihr Projekt auswählen** → Settings → Environment Variables
3. **Fügen Sie hinzu:**
   ```
   Key:   GOOGLE_API_KEY
   Value: AIza... (Ihr Google API Key)
   ```
4. **Wählen Sie:** Production, Preview, Development (alle 3!)
5. **Klicken:** Save

### Schritt 4: Google API Key Erstellen (falls nicht vorhanden)

1. Gehen Sie zu: https://makersuite.google.com/app/apikey
2. Klicken Sie auf "Create API Key"
3. Wählen Sie ein Projekt oder erstellen Sie ein neues
4. Kopieren Sie den API-Schlüssel
5. Fügen Sie ihn in Vercel Environment Variables ein

### Schritt 5: Redeploy

**WICHTIG:** Nach dem Hinzufügen von Environment Variables **MÜSSEN** Sie neu deployen!

**Option A - Automatisch (empfohlen):**
```bash
git commit --allow-empty -m "trigger: redeploy with env vars"
git push
```

**Option B - Manuell:**
1. Vercel Dashboard → Deployments
2. Neuestes Deployment → "..." (3 Punkte) → Redeploy

## ✅ Testing

### 1. Root URL Test
```
https://immo-agent-pro-cyqf.vercel.app/
```
**Erwartung:** Frontend mit Formular wird angezeigt

### 2. API Health Check
```
https://immo-agent-pro-cyqf.vercel.app/api/test
```
**Erwartung:**
```json
{
  "status": "ok",
  "message": "API funktioniert!",
  "environment": {
    "has_api_key": true,
    "api_key_length": 39,
    "langchain_available": true,
    "llm_initialized": true
  }
}
```

### 3. Frontend Test
1. Öffnen Sie die Root URL
2. Oben rechts sollte "System Bereit" (grün) stehen
3. Füllen Sie das Formular aus:
   - Typ: "Zur Miete" oder "Zum Kauf"
   - Beschreibung: z.B. "3 Zimmer Wohnung in Berlin, 80m2, Balkon"
4. Klicken Sie "KI-Anzeige Erstellen"
5. Nach 5-10 Sekunden sollte deutscher Anzeigentext erscheinen

## 🐛 Troubleshooting

### Problem: `{"status":"running"}` wird angezeigt

**Ursache:** Sie rufen die falsche URL auf (`/` statt `/api/test`)

**Lösung:**
- ✅ Richtig: `https://your-app.vercel.app/` (Frontend)
- ✅ Richtig: `https://your-app.vercel.app/api/test` (API Test)
- ❌ Falsch: Direkt `/` als API endpoint aufrufen

### Problem: "GOOGLE_API_KEY nicht konfiguriert"

**Lösung:**
1. Vercel Dashboard → Settings → Environment Variables
2. Prüfen Sie, ob `GOOGLE_API_KEY` vorhanden ist
3. Prüfen Sie, ob "Production" ausgewählt ist
4. Nach Änderungen: Redeploy!

### Problem: "langchain-google-genai nicht installiert"

**Lösung:**
1. Prüfen Sie `requirements.txt` auf Tippfehler
2. Vercel Logs prüfen: Dashboard → Deployments → Neuestes → Function Logs
3. Falls Fehler: `git commit --allow-empty -m "trigger rebuild" && git push`

### Problem: API antwortet nicht

**Debug-Schritte:**
1. Öffnen Sie Browser DevTools (F12)
2. Gehen Sie zum Network Tab
3. Versuchen Sie, eine Anzeige zu generieren
4. Sehen Sie sich die `/api/generate` Anfrage an
5. Prüfen Sie Response Headers und Body

### Problem: Cold Start / Langsame Antwort

**Das ist normal!** Serverless Functions haben einen "Cold Start":
- Erste Anfrage: 5-15 Sekunden
- Folgende Anfragen: 1-3 Sekunden
- Nach 5 Minuten Inaktivität: Wieder Cold Start

## 📊 Vercel Logs Prüfen

```bash
# Vercel CLI installieren
npm i -g vercel

# Login
vercel login

# Logs anzeigen (live)
vercel logs --follow

# Nur Fehler
vercel logs --since 1h | grep ERROR
```

## 🔄 Bekannte Änderungen für erfolgreiche Deployments:

1. ✅ `api/index.py` mit Mangum handler
2. ✅ Kein `main.py` im Root
3. ✅ `vercel.json` nur mit rewrites
4. ✅ Environment Variable `GOOGLE_API_KEY` gesetzt
5. ✅ Nach env var Änderung: Redeploy
6. ✅ Frontend ruft `/api/*` endpoints auf

## 📞 Support

Falls Probleme weiterhin bestehen:
1. Vercel Deployment Logs prüfen
2. Browser Console prüfen (F12)
3. `/api/test` Endpoint testen
4. Alle Schritte dieser Anleitung nochmal durchgehen

---

**Viel Erfolg! 🚀**
