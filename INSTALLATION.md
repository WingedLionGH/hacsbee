# Installationsanleitung - ToDo Manager

## Problem: Integration oder Card wird nicht gefunden

Wenn die Integration nicht in der Integrationsliste erscheint oder die Card nicht verfügbar ist, befolgen Sie diese Schritte:

## Schritt 1: Überprüfen Sie die Installation

1. **Stellen Sie sicher, dass die Dateien korrekt installiert sind:**
   - `custom_components/todo_manager/` muss im Home Assistant `custom_components/` Ordner sein
   - `www/community/todo_manager/todo-manager-card.js` muss im Home Assistant `www/community/todo_manager/` Ordner sein

2. **Überprüfen Sie die Dateistruktur:**
   ```
   config/
   ├── custom_components/
   │   └── todo_manager/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── coordinator.py
   │       ├── sensor.py
   │       ├── services.py
   │       └── translations/
   │           ├── en.json
   │           └── de.json
   └── www/
       └── community/
           └── todo_manager/
               └── todo-manager-card.js
   ```

## Schritt 2: Integration hinzufügen

1. **Starten Sie Home Assistant neu** (wichtig!)
2. Gehen Sie zu **Einstellungen** > **Geräte & Dienste**
3. Klicken Sie auf **+ Integration hinzufügen**
4. Suchen Sie nach **"ToDo Manager"** oder **"todo_manager"**
5. Wenn die Integration nicht erscheint:
   - Überprüfen Sie die Logs auf Fehler
   - Stellen Sie sicher, dass `manifest.json` korrekt ist
   - Überprüfen Sie, ob alle Python-Dateien vorhanden sind

## Schritt 3: Card als Ressource hinzufügen

Die Card muss manuell als Lovelace-Ressource hinzugefügt werden:

1. Gehen Sie zu **Einstellungen** > **Dashboard** > **Lovelace-Dashboards**
2. Klicken Sie auf **Ressourcen** (oben rechts)
3. Klicken Sie auf **+ Ressource hinzufügen**
4. Geben Sie folgende URL ein:
   ```
   /local/community/todo_manager/todo-manager-card.js
   ```
   Oder wenn das nicht funktioniert:
   ```
   /hacsfiles/todo_manager/todo-manager-card.js
   ```
5. Wählen Sie als Typ: **JavaScript-Modul**
6. Klicken Sie auf **Erstellen**

## Schritt 4: Card verwenden

Nachdem die Ressource hinzugefügt wurde:

1. Gehen Sie zu einer Lovelace-Ansicht
2. Klicken Sie auf **⋮** (drei Punkte) > **Karte bearbeiten**
3. Klicken Sie auf **+ Karte hinzufügen**
4. Scrolle nach unten zu **Manuelle Karte**
5. Wählen Sie **Todo Manager Card**

Oder fügen Sie die Card direkt in YAML hinzu:

```yaml
type: custom:todo-manager-card
title: Meine ToDos
show_completed: true
```

## Fehlerbehebung

### Integration erscheint nicht

1. **Überprüfen Sie die Logs:**
   - Gehen Sie zu **Einstellungen** > **System** > **Logs**
   - Suchen Sie nach Fehlern mit "todo_manager"

2. **Überprüfen Sie die Dateien:**
   ```bash
   # Überprüfen Sie, ob alle Dateien vorhanden sind
   ls -la config/custom_components/todo_manager/
   ```

3. **Löschen Sie den Cache:**
   - Löschen Sie den Browser-Cache
   - Starten Sie Home Assistant neu

### Card erscheint nicht

1. **Überprüfen Sie die Ressource:**
   - Gehen Sie zu **Einstellungen** > **Dashboard** > **Ressourcen**
   - Stellen Sie sicher, dass die Ressource hinzugefügt wurde
   - Überprüfen Sie, ob die URL korrekt ist

2. **Überprüfen Sie die Browser-Konsole:**
   - Öffnen Sie die Entwicklertools (F12)
   - Gehen Sie zum Tab "Console"
   - Suchen Sie nach Fehlern

3. **Testen Sie die URL:**
   - Öffnen Sie im Browser: `http://YOUR_HA_IP:8123/local/community/todo_manager/todo-manager-card.js`
   - Die Datei sollte geladen werden können

## Manuelle Installation (falls HACS nicht funktioniert)

1. **Kopieren Sie die Dateien manuell:**
   ```bash
   # Integration
   cp -r custom_components/todo_manager /config/custom_components/
   
   # Card
   cp -r www/community/todo_manager /config/www/community/
   ```

2. **Starten Sie Home Assistant neu**

3. **Fügen Sie die Integration hinzu** (siehe Schritt 2)

4. **Fügen Sie die Card als Ressource hinzu** (siehe Schritt 3)

## Unterstützung

Wenn die Probleme weiterhin bestehen:
1. Überprüfen Sie die Home Assistant Version (mindestens 2023.1.0 erforderlich)
2. Überprüfen Sie die Logs auf detaillierte Fehlermeldungen
3. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
