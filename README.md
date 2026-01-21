# ToDo Manager für Home Assistant

Eine umfassende ToDo-Liste-Erweiterung für Home Assistant mit erweiterten Funktionen für persönliche und familiäre Aufgabenverwaltung.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Home Assistant](https://img.shields.io/badge/home%20assistant-2023.1%2B-green)

## 🎯 Features

### ToDo-Typen

1. **Einfache ToDos** - Einfache Erinnerungen, die als "erledigt" markiert werden können
2. **Komplexe ToDos** - Mit zusätzlichem Ergebnis-Feld für detaillierte Notizen
3. **Einkaufslisten ToDos** - Produkte mit Mengen, die beim Einkaufen abgehakt werden können
4. **Packlisten ToDo** - Gegenstände für Reisen/Urlaube mit Checkboxen

### Weitere Features

- 📅 **Fälligkeitsdaten** - Jedes ToDo hat ein Datum und eine Uhrzeit
- 👥 **Personenzuweisung** - ToDos können einer oder mehreren Personen zugewiesen werden (min. 1, max. alle)
- 🔄 **Wiederkehrende ToDos** - Automatische Erstellung wiederkehrender Aufgaben (täglich, wöchentlich, monatlich)
- 📊 **Dringlichkeits-Sortierung** - Übersichtsseite sortiert nach Dringlichkeit
- 🎨 **Personenfarben** - Visuelle Unterscheidung durch individuell wählbare Farben
- ✅ **Statusverfolgung** - Nachverfolgung von erledigten Aufgaben mit Zeitstempel

## 📦 Installation

### Über HACS (empfohlen)

1. Öffne HACS in Home Assistant
2. Gehe zu "Integrations"
3. Klicke auf "Custom repositories"
4. Füge dieses Repository hinzu
5. Klicke auf "Download" und starte Home Assistant neu

### Manuelle Installation

1. Kopiere den `custom_components/todo_manager` Ordner in deinen `custom_components` Ordner
2. Kopiere den `www/community/todo_manager` Ordner in deinen `www/community` Ordner
3. Starte Home Assistant neu
4. Gehe zu **Einstellungen** > **Geräte & Dienste** > **Integrationen**
5. Klicke auf **+ Integration hinzufügen**
6. Suche nach "ToDo Manager" und füge es hinzu

## 🚀 Verwendung

### Lovelace Card

Füge die ToDo Manager Card zu deiner Lovelace-Ansicht hinzu:

```yaml
type: custom:todo-manager-card
title: Meine ToDos
show_completed: true
```

Oder über die UI:
1. Gehe zu einer Lovelace-Ansicht
2. Klicke auf **⋮** > **Karte bearbeiten**
3. Klicke auf **+ Karte hinzufügen**
4. Scrolle nach unten zu **Manuelle Karte**
5. Wähle **Todo Manager Card**

### Services

Die Integration stellt folgende Services bereit:

#### ToDos verwalten

**`todo_manager.create_todo`** - Neues ToDo erstellen
```yaml
service: todo_manager.create_todo
data:
  title: "Mülltonnen rausbringen"
  description: "Blaue und gelbe Tonne"
  due_date: "2024-01-15"
  due_time: "08:00"
  todo_type: simple
  recurring: true
  recurring_rule:
    interval: 1
    unit: weeks
  persons:
    - person_id_1
    - person_id_2
```

**`todo_manager.update_todo`** - ToDo aktualisieren
```yaml
service: todo_manager.update_todo
data:
  todo_id: "todo-id-here"
  title: "Neuer Titel"
  completed: true
```

**`todo_manager.delete_todo`** - ToDo löschen
```yaml
service: todo_manager.delete_todo
data:
  todo_id: "todo-id-here"
```

**`todo_manager.complete_todo`** - ToDo als erledigt markieren
```yaml
service: todo_manager.complete_todo
data:
  todo_id: "todo-id-here"
  result: "Optionales Ergebnis"
```

#### Personen verwalten

**`todo_manager.create_person`** - Person erstellen
```yaml
service: todo_manager.create_person
data:
  person_name: "Max Mustermann"
  person_color: "#1976d2"
```

**`todo_manager.update_person`** - Person aktualisieren
```yaml
service: todo_manager.update_person
data:
  person_id: "person-id-here"
  person_name: "Neuer Name"
  person_color: "#ff5722"
```

**`todo_manager.delete_person`** - Person löschen
```yaml
service: todo_manager.delete_person
data:
  person_id: "person-id-here"
```

### Beispiel-Konfigurationen

#### Einkaufsliste erstellen
```yaml
service: todo_manager.create_todo
data:
  title: "Einkaufen"
  description: "Wocheneinkauf"
  due_date: "2024-01-20"
  due_time: "14:00"
  todo_type: shopping
  items:
    - name: "Milch"
      quantity: "1 Liter"
    - name: "Brot"
      quantity: "1 Laib"
    - name: "Eier"
      quantity: "10 Stück"
  persons:
    - person_id_1
```

#### Packliste für Urlaub erstellen
```yaml
service: todo_manager.create_todo
data:
  title: "Packerliste Skiurlaub"
  due_date: "2024-02-01"
  todo_type: packing
  items:
    - name: "Skijacke"
    - name: "Skihose"
    - name: "Skischuhe"
    - name: "Handschuhe"
    - name: "Mütze"
  persons:
    - person_id_1
    - person_id_2
```

#### Wiederkehrendes ToDo
```yaml
service: todo_manager.create_todo
data:
  title: "Essen bestellen"
  description: "Wöchentliche Bestellung"
  todo_type: simple
  recurring: true
  recurring_rule:
    interval: 1
    unit: weeks
  persons:
    - person_id_1
```

## 📊 Sensoren

Die Integration erstellt automatisch folgende Sensoren:

- **`sensor.todo_manager_all`** - Gesamtanzahl aller ToDos (inkl. erledigte)
- **`sensor.todo_manager_active`** - Anzahl aktiver ToDos (mit Attributen der Top 10)
- **`sensor.todo_manager_overdue`** - Anzahl überfälliger ToDos

Die Sensoren aktualisieren sich automatisch jede Minute.

## 🎨 UI-Features

Die Lovelace Card bietet:

- **Übersichtsseite** mit allen ToDos, sortiert nach Dringlichkeit
- **Visuelle Indikatoren:**
  - 🔴 Rote Markierung für überfällige ToDos
  - 🟠 Orange Markierung für dringende ToDos (< 24h)
- **Modal-Dialoge** zum Erstellen und Bearbeiten
- **Personen-Badges** mit individuellen Farben
- **Item-Verwaltung** für Einkaufs- und Packlisten
- **Ergebnis-Anzeige** für komplexe ToDos

## 🔧 Konfiguration

### Card-Konfiguration

| Option | Typ | Standard | Beschreibung |
|--------|-----|----------|--------------|
| `title` | string | "ToDo Manager" | Titel der Card |
| `show_completed` | boolean | `true` | Erledigte ToDos anzeigen |

## 💾 Datenspeicherung

Alle Daten werden lokal in Home Assistant gespeichert (im `.storage` Verzeichnis). Es werden keine externen Dienste verwendet.

## 🐛 Fehlerbehebung

### Card wird nicht angezeigt

1. Überprüfe, ob die Frontend-Dateien im `www/community/todo_manager` Ordner vorhanden sind
2. Lösche den Browser-Cache und lade die Seite neu
3. Überprüfe die Browser-Konsole auf Fehler

### Services funktionieren nicht

1. Überprüfe, ob die Integration korrekt installiert ist
2. Überprüfe die Logs auf Fehler
3. Stelle sicher, dass alle erforderlichen Felder (z.B. `todo_id`) korrekt angegeben sind

### Wiederkehrende ToDos werden nicht erstellt

- Wiederkehrende ToDos werden nur erstellt, wenn das ursprüngliche ToDo als erledigt markiert wurde
- Die Überprüfung erfolgt jede Minute

## 📝 Entwickler-Informationen

### Projekt-Struktur

```
custom_components/todo_manager/
├── __init__.py          # Haupt-Initialisierung
├── manifest.json        # Metadaten
├── config_flow.py       # Konfigurations-Flow
├── const.py             # Konstanten
├── coordinator.py       # Daten-Koordinator
├── sensor.py            # Sensor-Entities
└── services.py          # Service-Definitionen

www/community/todo_manager/
└── todo-manager-card.js # Frontend Lovelace Card
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte erstelle einen Pull Request oder ein Issue.

## 🙏 Danksagungen

- Home Assistant Community
- HACS für die einfache Installation
