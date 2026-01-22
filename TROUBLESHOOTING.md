# Fehlerbehebung - ToDo Manager

## Problem: Integration erscheint nicht in der Liste

### Lösung 1: Überprüfen Sie die Installation

1. **Stellen Sie sicher, dass die Dateien korrekt installiert sind:**
   - Die Integration muss im `custom_components/todo_manager/` Ordner sein
   - Überprüfen Sie, ob alle Dateien vorhanden sind:
     - `__init__.py`
     - `manifest.json`
     - `config_flow.py`
     - `const.py`
     - `coordinator.py`
     - `sensor.py`
     - `services.py`
     - `translations/en.json`
     - `translations/de.json`

2. **Überprüfen Sie die Logs:**
   - Gehen Sie zu **Einstellungen** > **System** > **Logs**
   - Suchen Sie nach Fehlern mit "todo_manager" oder "ToDo Manager"
   - Häufige Fehler:
     - "Integration not found" → Dateien fehlen
     - "Import error" → Syntaxfehler in Python-Dateien
     - "Config flow error" → Problem mit config_flow.py

3. **Starten Sie Home Assistant neu:**
   - Wichtig: Nach der Installation muss Home Assistant neu gestartet werden
   - Gehen Sie zu **Einstellungen** > **System** > **Neu starten**

### Lösung 2: Manuelle Integration hinzufügen

Wenn die Integration nicht in der Liste erscheint:

1. Gehen Sie zu **Einstellungen** > **Geräte & Dienste**
2. Klicken Sie auf **+ Integration hinzufügen**
3. Suchen Sie nach **"todo_manager"** (ohne Leerzeichen)
4. Falls nicht gefunden, versuchen Sie:
   - "ToDo Manager" (mit Leerzeichen)
   - "todo" (Teil des Namens)

5. **Falls immer noch nicht gefunden:**
   - Überprüfen Sie, ob die Integration korrekt installiert ist
   - Überprüfen Sie die Home Assistant Version (mindestens 2023.1.0)
   - Überprüfen Sie die Logs auf Fehler

## Problem: Card erscheint nicht

### Lösung 1: Card als Ressource hinzufügen

Die Card muss manuell als Lovelace-Ressource hinzugefügt werden:

1. **Gehen Sie zu den Ressourcen:**
   - Einstellungen > Dashboard > Lovelace-Dashboards
   - Klicken Sie auf **Ressourcen** (oben rechts, neben dem Hamburger-Menü)

2. **Fügen Sie die Ressource hinzu:**
   - Klicken Sie auf **+ Ressource hinzufügen**
   - Geben Sie die URL ein:
     ```
     /local/community/todo_manager/todo-manager-card.js
     ```
   - **Wichtig:** Der Typ muss **JavaScript-Modul** sein
   - Klicken Sie auf **Erstellen**

3. **Alternative URL (wenn HACS installiert ist):**
   ```
   /hacsfiles/todo_manager/todo-manager-card.js
   ```

### Lösung 2: Überprüfen Sie die Datei

1. **Testen Sie die URL im Browser:**
   - Öffnen Sie: `http://YOUR_HA_IP:8123/local/community/todo_manager/todo-manager-card.js`
   - Die Datei sollte geladen werden können
   - Falls nicht: Die Datei ist nicht korrekt installiert

2. **Überprüfen Sie die Browser-Konsole:**
   - Öffnen Sie die Entwicklertools (F12)
   - Gehen Sie zum Tab "Console"
   - Suchen Sie nach Fehlern wie:
     - "Failed to load resource"
     - "404 Not Found"
     - "SyntaxError"

### Lösung 3: Cache leeren

1. **Browser-Cache leeren:**
   - Drücken Sie `Ctrl + Shift + Delete`
   - Wählen Sie "Cached images and files"
   - Klicken Sie auf "Clear data"

2. **Hard Refresh:**
   - Drücken Sie `Ctrl + F5` oder `Ctrl + Shift + R`
   - Lädt die Seite neu ohne Cache

## Häufige Fehler und Lösungen

### Fehler: "Integration not found"

**Ursache:** Die Integration ist nicht korrekt installiert.

**Lösung:**
1. Überprüfen Sie, ob alle Dateien vorhanden sind
2. Überprüfen Sie die Dateistruktur
3. Starten Sie Home Assistant neu
4. Überprüfen Sie die Logs

### Fehler: "Card not found" oder "Custom element doesn't exist"

**Ursache:** Die Card ist nicht als Ressource registriert.

**Lösung:**
1. Fügen Sie die Card als Ressource hinzu (siehe oben)
2. Überprüfen Sie die URL
3. Leeren Sie den Browser-Cache
4. Starten Sie Home Assistant neu

### Fehler: "SyntaxError" in der Browser-Konsole

**Ursache:** Die JavaScript-Datei hat einen Syntaxfehler.

**Lösung:**
1. Überprüfen Sie die Datei `todo-manager-card.js`
2. Stellen Sie sicher, dass die Datei vollständig ist
3. Überprüfen Sie die Browser-Konsole auf detaillierte Fehlermeldungen

### Fehler: "404 Not Found" für die Card-Datei

**Ursache:** Die Datei ist nicht am erwarteten Ort.

**Lösung:**
1. Überprüfen Sie, ob die Datei existiert:
   - `www/community/todo_manager/todo-manager-card.js`
2. Überprüfen Sie die Berechtigungen
3. Stellen Sie sicher, dass die Datei nicht beschädigt ist

## Schritt-für-Schritt Installation

### Für HACS-Installation:

1. **Installieren Sie über HACS:**
   - Gehen Sie zu HACS > Integrations
   - Suchen Sie nach "ToDo Manager"
   - Klicken Sie auf "Download"
   - Warten Sie, bis der Download abgeschlossen ist

2. **Starten Sie Home Assistant neu:**
   - Gehen Sie zu Einstellungen > System > Neu starten
   - Warten Sie, bis Home Assistant vollständig gestartet ist

3. **Fügen Sie die Integration hinzu:**
   - Gehen Sie zu Einstellungen > Geräte & Dienste
   - Klicken Sie auf + Integration hinzufügen
   - Suchen Sie nach "ToDo Manager"

4. **Fügen Sie die Card als Ressource hinzu:**
   - Gehen Sie zu Einstellungen > Dashboard > Ressourcen
   - Fügen Sie `/hacsfiles/todo_manager/todo-manager-card.js` hinzu
   - Typ: JavaScript-Modul

### Für manuelle Installation:

1. **Kopieren Sie die Dateien:**
   ```bash
   # Integration
   cp -r custom_components/todo_manager /config/custom_components/
   
   # Card
   mkdir -p /config/www/community/todo_manager
   cp www/community/todo_manager/todo-manager-card.js /config/www/community/todo_manager/
   ```

2. **Starten Sie Home Assistant neu**

3. **Fügen Sie die Integration hinzu** (siehe oben)

4. **Fügen Sie die Card als Ressource hinzu** (siehe oben)

## Unterstützung

Wenn die Probleme weiterhin bestehen:

1. **Sammeln Sie Informationen:**
   - Home Assistant Version
   - HACS Version (falls installiert)
   - Fehlermeldungen aus den Logs
   - Browser-Konsole-Fehler

2. **Überprüfen Sie die Anforderungen:**
   - Home Assistant: Mindestens 2023.1.0
   - Python: 3.10 oder höher

3. **Erstellen Sie ein Issue:**
   - Beschreiben Sie das Problem detailliert
   - Fügen Sie Logs und Fehlermeldungen bei
   - Beschreiben Sie, was Sie bereits versucht haben
