# ToDo Manager für Home Assistant

Eine vollständige ToDo-Liste-Erweiterung für Home Assistant mit erweiterten Funktionen.

## Features

- ✅ **4 ToDo-Typen:**
  - Einfache ToDos: Einfache Erinnerungen
  - Komplexe ToDos: Mit Ergebnis-Erfassung
  - Einkaufslisten: Produkte mit Mengen
  - Packlisten: Für Reisen und Urlaube

- 📅 **Fälligkeitsdaten:** Jedes ToDo hat ein Datum und eine Uhrzeit
- 👥 **Personenzuweisung:** ToDos können einer oder mehreren Personen zugewiesen werden
- 🔄 **Wiederkehrende ToDos:** Automatische Erstellung wiederkehrender Aufgaben
- 📊 **Übersicht:** Sortiert nach Dringlichkeit mit visuellen Indikatoren
- 🎨 **Personenfarben:** Visuelle Unterscheidung durch Farben

## Installation

1. Installiere über HACS: Suche nach "ToDo Manager"
2. Oder kopiere den `custom_components/todo_manager` Ordner in deinen `custom_components` Ordner
3. Starte Home Assistant neu
4. Gehe zu Einstellungen > Integrationen > + Integration hinzufügen
5. Suche nach "ToDo Manager" und füge es hinzu

## Verwendung

### Lovelace Card

Füge folgende Konfiguration zu deiner Lovelace-Konfiguration hinzu:

```yaml
type: custom:todo-manager-card
title: Meine ToDos
show_completed: true
```

### Services

Die Integration stellt folgende Services bereit:

- `todo_manager.create_todo` - Neues ToDo erstellen
- `todo_manager.update_todo` - ToDo aktualisieren
- `todo_manager.delete_todo` - ToDo löschen
- `todo_manager.complete_todo` - ToDo als erledigt markieren
- `todo_manager.create_person` - Person erstellen
- `todo_manager.update_person` - Person aktualisieren
- `todo_manager.delete_person` - Person löschen

### Beispiel-Services

```yaml
# ToDo erstellen
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

# Person erstellen
service: todo_manager.create_person
data:
  person_name: "Max Mustermann"
  person_color: "#1976d2"

# Einkaufsliste erstellen
service: todo_manager.create_todo
data:
  title: "Einkaufen"
  todo_type: shopping
  items:
    - name: "Milch"
      quantity: "1 Liter"
    - name: "Brot"
      quantity: "1 Laib"
```

## Sensoren

Die Integration erstellt automatisch folgende Sensoren:

- `sensor.todo_manager_all` - Gesamtanzahl aller ToDos
- `sensor.todo_manager_active` - Anzahl aktiver ToDos (mit Attributen)
- `sensor.todo_manager_overdue` - Anzahl überfälliger ToDos

## Frontend

Das Frontend wird automatisch installiert. Die Lovelace Card bietet:

- Übersicht aller ToDos sortiert nach Dringlichkeit
- Visuelle Kennzeichnung überfälliger und dringender ToDos
- Modal-Dialoge zum Erstellen und Bearbeiten
- Verwaltung von Personen
- Item-Verwaltung für Einkaufs- und Packlisten

## Support

Bei Fragen oder Problemen erstelle bitte ein Issue auf GitHub.
