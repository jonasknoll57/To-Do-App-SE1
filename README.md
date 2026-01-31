# 📝 Task Manager - MVC TODO-App mit Streamlit & Design Patterns

Eine funktionale TODO-Anwendung mit Python, Streamlit und MVC-Architektur.

Anforderung:
Warum ist die MVC-Architektur für eine TODO-App sinnvoll?
Wie wurde MVC in diesem Projekt konkret umgesetzt?
Dateiorga
Kommentare
1. Bereitstellung der Designs für Desktop und Mobile (falls abweichend)
Format: .fig oder SVG
3. UI: Dokumentation:
Welche UI-Elemente unterstützen welche UI-Prinzipien?
Für jedes der 10 UI-Prinzipien je ein konkretes Beispiel (in der
README)
MVC-Architektur: Kurze Beschreibung in README
Warum ist MVC für TODO-App sinnvoll?
Wie wurde MVC in diesem Projekt umgesetzt?


Windows venv
Macos venv
requirements
playwright install
---

## Inhaltsverzeichnis

1. [MVC-Architektur](#mvc-architektur)
2. [Funktionale Anforderungen](#funktionale-anforderungen)
3. [Nicht-Funktionale Anforderungen](#nicht-funktionale-anforderungen)
4. [10 UI-Prinzipien (Nielsen-Heuristiken)](#10-ui-prinzipien-nielsen-heuristiken)
5. [Design Patterns](#design-patterns)
6. [Projektstruktur](#projektstruktur)
7. [Installation & Start](#installation--start)
8. [Tests](#tests)
9. [Figma Design](#figma-design)

---

## MVC-Architektur

### Warum MVC für eine TODO-App?

MVC (Model-View-Controller) trennt die Anwendung in drei Schichten mit klaren Verantwortlichkeiten. Diese Architektur ist für eine TODO-App besonders sinnvoll, weil:

1. **Testbarkeit**: Model, Repository und Controller können unabhängig von der Streamlit-UI getestet werden. Unit-Tests prüfen die Geschäftslogik isoliert.

2. **Wartbarkeit**: Änderungen am UI (View) erfordern keine Änderungen an der Logik (Controller) oder den Daten (Model). Neue Features können gezielt in der richtigen Schicht ergänzt werden.

3. **Wiederverwendbarkeit**: Der Controller kann mit verschiedenen Views verwendet werden (z.B. CLI, REST-API, andere UI-Frameworks).

4. **Übersichtlichkeit**: Klare Trennung der Verantwortlichkeiten macht den Code verständlicher. Jede Datei hat einen definierten Zweck.

5. **Skalierbarkeit**: Neue Funktionen (z.B. Benutzer, Projekte) können in separaten Modulen ergänzt werden, ohne bestehenden Code zu verändern.

### MVC-Umsetzung in diesem Projekt

| Schicht | Datei | Klassen/Funktionen | Verantwortlichkeit |
|---------|-------|-------------------|-------------------|
| **Model** | `model.py` | `Task` | Datenstruktur, Serialisierung, Validierung |
| **Repository** | `repository.py` | `JSONTaskRepository`, `InMemoryTaskRepository` | Persistenz-Schicht, Datenzugriff |
| **Controller** | `controller.py` | `TaskController` | Geschäftslogik, CRUD-Operationen |
| **Patterns** | `patterns.py` | `TaskFactory`, `TaskAdapter`, `TaskMediator` | Design Patterns für Erweiterbarkeit |
| **View** | `view.py` | `TodoView` | UI-Komponenten, Layout, Darstellung |
| **App** | `app.py` | `main()`, `init_app()` | Einstiegspunkt, Initialisierung |

### Datenfluss

```
User → View (Streamlit) → Mediator → Controller → Repository → JSON-Datei
                                         ↓
                                       Model (Task)
```

---

## Funktionale Anforderungen

### Basisliste (MUSS)

| ID | Beschreibung | Status | Umsetzung |
|----|--------------|--------|-----------|
| FR-01 | Aufgaben persistent speichern | ✅ | `JSONTaskRepository` speichert in `tasks.json` |
| FR-02 | Aufgabe hinzufügen | ✅ | `st.text_input` + "Erstellen" Button |
| FR-03 | Aufgabe löschen | ✅ | 🗑️ Button pro Task |
| FR-04 | Aufgabe bearbeiten | ✅ | ✏️ Button → Edit-Modus mit Speichern/Abbrechen |
| FR-05 | Als erledigt markieren | ✅ | Checkbox pro Task mit `toggle()` |
| FR-06 | Aufgaben in Liste anzeigen | ✅ | Dynamische Liste mit `st.columns` Layout |

### Zusätzliche Anforderungen (>5 über Basisliste)

| ID | Beschreibung | Priorität | Umsetzung |
|----|--------------|-----------|-----------|
| FR-07 | Nach Status filtern (offen/erledigt) | SOLL | `st.radio` horizontal |
| FR-08 | Kategorien zuordnen + verwalten | SOLL | Dropdown + Expander zum Erstellen/Löschen |
| FR-09 | Fälligkeitsdatum mit Datepicker | KANN | `st.date_input` mit min_value=heute |
| FR-10 | Überfällig-Warnung | ZUSATZ | Rote ⚠️ Markierung bei überfälligen Tasks |
| FR-11 | Fortschrittsanzeige | ZUSATZ | `st.progress()` mit Prozentwert |
| FR-12 | Statistiken (Gesamt/Offen/Erledigt) | ZUSATZ | `st.metric()` Dashboard |
| FR-13 | Filter nach Kategorie | ZUSATZ | Dropdown-Filter kombiniert mit Status |
| FR-14 | Smart-Sortierung | ZUSATZ | Automatische Priorisierung nach Dringlichkeit (🎯 Toggle) |

---

## Nicht-Funktionale Anforderungen

| ID | Typ | Beschreibung | Priorität | Umsetzung |
|----|-----|--------------|-----------|-----------|
| NFR-01 | Usability | Aufgabe mit max. 3 Klicks anlegen | MUSS | Titel → Erstellen (2 Klicks) |
| NFR-02 | Performance | App startet in < 2 Sekunden | MUSS | Leichtgewichtiges Streamlit |
| NFR-03 | Reliability | Gleiche Eingabe → gleiches Ergebnis | MUSS | Deterministische Logik |
| NFR-04 | Portability | Läuft auf Windows, Mac, Linux | MUSS | Python + Streamlit cross-platform |
| NFR-05 | Maintainability | MVC-Architektur mit klarer Trennung | MUSS | Separate Dateien pro Schicht |
| NFR-06 | Testability | >80% Code-Coverage möglich | SOLL | Unit, Integration, System, E2E Tests |
| NFR-07 | Usability | Responsive Design (Desktop + Mobile) | SOLL | `st.columns` mit flexiblem Layout |
| NFR-08 | Accessibility | Tooltips für alle Buttons | SOLL | `help=""` Parameter bei Buttons |
| NFR-09 | Reliability | Fehlerhafte Eingaben werden abgefangen | SOLL | ValueError bei leerem Titel |
| NFR-10 | Usability | Smart-Sort für Dringlichkeits-Priorisierung | KANN | Toggle sortiert nach: Überfällig → Heute → Datum |

---

## 10 UI-Prinzipien (Nielsen-Heuristiken)

| # | Prinzip | UI-Element | Konkretes Beispiel in der App |
|---|---------|------------|-------------------------------|
| 1 | **Sichtbarkeit des Systemstatus** | Fortschrittsbalken, Statistiken | `st.progress()` zeigt Erledigungsgrad (25%), `st.metric()` zeigt Gesamt/Offen/Erledigt |
| 2 | **Übereinstimmung System & Wirklichkeit** | Icons, natürliche Sprache | ✅ für erledigt, 🗑️ für Löschen, 📅 für Datum – intuitive Metaphern |
| 3 | **Benutzerkontrolle & Freiheit** | Abbrechen-Button, Undo | "❌ Abbrechen" im Edit-Modus, Kategorien können erstellt UND gelöscht werden |
| 4 | **Konsistenz & Standards** | Einheitliches Layout | Alle Tasks haben identisches Layout (Checkbox, Titel, Buttons in gleicher Reihenfolge) |
| 5 | **Fehlervermeidung** | Validierung, Constraints | Leere Titel werden mit `st.error()` abgelehnt, Datepicker verhindert vergangene Daten |
| 6 | **Wiedererkennung statt Erinnerung** | Sichtbare Optionen | Kategorien als Dropdown sichtbar, Filter als Radio-Buttons permanent angezeigt |
| 7 | **Flexibilität & Effizienz** | Schnellaktionen, Anpassung | Ein-Klick Checkbox, Smart-Sort 🎯 für automatische Priorisierung, Kategorien selbst definierbar |
| 8 | **Ästhetik & minimalistisches Design** | Klares Layout | Nur notwendige Elemente, `st.divider()` für visuelle Struktur, keine überflüssigen Farben |
| 9 | **Fehlererkennung & -behebung** | Klare Fehlermeldungen | `st.error("⚠️ Bitte Titel eingeben")` erklärt das Problem und die Lösung |
| 10 | **Hilfe & Dokumentation** | Tooltips, Hinweise | `st.caption()` mit Tipps, `help="Bearbeiten"` bei Buttons, Footer mit Bedienungshinweis |

---

## Design Patterns

### Übersicht: Implementierte Patterns

| Pattern | Datei | Hauptklasse(n) | Funktioniert? |
|---------|-------|----------------|---------------|
| Factory | `patterns.py` | `TaskFactory` | ✅ Ja |
| Abstract Factory | `patterns.py` | `AbstractTaskFactory`, `SimpleTaskFactory`, `PriorityTaskFactory`, `DetailedTaskFactory` | ✅ Ja |
| Adapter | `patterns.py` | `TaskAdapter`, `ExternalTaskFormat` | ✅ Ja |
| Mediator | `patterns.py` | `TaskMediator` | ✅ Ja (aktiv genutzt) |
| Repository | `repository.py` | `TaskRepositoryInterface`, `JSONTaskRepository`, `InMemoryTaskRepository` | ✅ Ja (aktiv genutzt) |

### 1. Factory Pattern (`patterns.py`)

**Zweck**: Flexible Task-Erstellung ohne direkte Klassenkenntnis. Verschiedene Task-Typen werden mit Präfixen erstellt.

**Klassen**: `TaskFactory`

**Verwendung**:
```python
task = TaskFactory.create("work", "Meeting vorbereiten")
# Ergebnis: Task mit Titel "🔨 Meeting vorbereiten"

task = TaskFactory.create("shopping", "Milch kaufen")
# Ergebnis: Task mit Titel "🛒 Milch kaufen"
```

### 2. Abstract Factory Pattern (`patterns.py`)

**Zweck**: Familien von Task-Varianten erstellen (einfach vs. detailliert).

**Klassen**: `AbstractTaskFactory` (abstrakt), `SimpleTaskFactory`, `PriorityTaskFactory`, `DetailedTaskFactory`

**Verwendung**:
```python
factory = PriorityTaskFactory()
task = factory.create_task("Wichtige Aufgabe")
# Ergebnis: Task mit Titel "⚡ Wichtige Aufgabe"

factory = DetailedTaskFactory(default_category="Arbeit")
task = factory.create_task("Report schreiben")
# Ergebnis: Task mit Titel "📋 Report schreiben", Kategorie "Arbeit", Datum heute
```

### 3. Adapter Pattern (`patterns.py`)

**Zweck**: Externe Datenformate in internes Task-Format konvertieren. Ermöglicht Integration von APIs ohne Codeänderung.

**Klassen**: `ExternalTaskFormat`, `TaskAdapter`

**Verwendung**:
```python
# Externes Format (z.B. von API)
external = ExternalTaskFormat(name="API Task", completed=1, tag="Work")

# Konvertierung zu internem Format
internal = TaskAdapter.adapt(external)
# 'name' → 'title', 'completed' (0/1) → 'done' (bool), 'tag' → 'category'
```

### 4. Mediator Pattern (`patterns.py`)

**Zweck**: Zentrale Kommunikation zwischen View und Controller. Reduziert direkte Abhängigkeiten.

**Klassen**: `TaskMediator`

**Verwendung**:
```python
mediator = TaskMediator(controller)

# Alle Operationen laufen über den Mediator
mediator.add_task("Neue Aufgabe", category="Arbeit")
mediator.toggle_task(task_id)
mediator.delete_task(task_id)

# Listener für UI-Updates
mediator.add_listener(lambda event: print(f"Event: {event}"))
```

### 5. Repository Pattern (`repository.py`)

**Zweck**: Abstraktion der Persistenz-Schicht. Ermöglicht einfaches Austauschen der Speichermethode.

**Klassen**: `TaskRepositoryInterface` (abstrakt), `JSONTaskRepository`, `InMemoryTaskRepository`

**Verwendung**:
```python
# Produktion: JSON-Datei
repo = JSONTaskRepository("tasks.json")

# Tests: In-Memory (kein Dateisystem)
repo = InMemoryTaskRepository()

# Controller nutzt Repository über Interface
controller = TaskController(repository=repo)
```

---

## Smart-Sort Feature (1.0 Feature)

### Was ist Smart-Sort?

Smart-Sort ist eine intelligente Sortierung, die Tasks automatisch nach ihrer **Dringlichkeit** priorisiert. Das Feature ist über einen 🎯 Toggle aktivierbar und hilft dem Nutzer, den Überblick zu behalten.

### Sortier-Reihenfolge

1. **⚠️ Überfällige Tasks** – Rot markiert, immer ganz oben
2. **📅 Heute fällige Tasks** – Orange markiert
3. **📅 Zukünftige Tasks** – Nach Datum sortiert
4. **Tasks ohne Datum** – Am Ende der Liste
5. **✅ Erledigte Tasks** – Ganz unten

### Usability-Vorteile

| Nielsen-Heuristik | Umsetzung |
|-------------------|-----------|
| #1 Sichtbarkeit des Systemstatus | Info-Box zeigt aktiven Sortier-Modus |
| #6 Wiedererkennung statt Erinnerung | Dringende Tasks sind automatisch sichtbar |
| #7 Flexibilität & Effizienz | Toggle erlaubt An/Aus nach Nutzerpräferenz |
| #8 Minimalistisches Design | Subtil integriert, nicht aufdringlich |

### Code-Implementierung (`view.py`)

```python
def _smart_sort_tasks(self, tasks: List[Task]) -> List[Task]:
    def sort_key(task: Task):
        if task.done:
            return (4, date.max)  # Erledigte ganz unten
        if task.is_overdue():
            return (0, task.due_date)  # Überfällige zuerst
        if task.is_due_today():
            return (1, task.due_date)  # Heute fällige als zweites
        if task.due_date:
            return (2, task.due_date)  # Mit Datum nach Fälligkeit
        return (3, date.max)  # Ohne Datum am Ende
    
    return sorted(tasks, key=sort_key)
```

---

## Projektstruktur

```
todo_app/
├── app.py                    # Einstiegspunkt (initialisiert MVC)
├── model.py                  # Model: Task-Datenklasse
├── repository.py             # Repository: Persistenz-Schicht
├── controller.py             # Controller: Geschäftslogik
├── patterns.py               # Design Patterns (Factory, Adapter, Mediator)
├── view.py                   # View: Streamlit UI-Komponenten
├── tasks.json                # Persistente Datenspeicherung
├── README.md                 # Dokumentation
├── design/
│   ├── todo_desktop.svg      # Desktop-Design (1200×800)
│   └── todo_mobile.svg       # Mobile-Design (360×800)
└── tests/
    ├── test_unit.py          # Unit Tests (AAA-Muster)
    ├── test_integration.py   # Integrationstests
    ├── system_test.py        # Systemtests
    └── test_e2e.py           # End-to-End Tests (Playwright)
```

---

## Installation & Start

### Voraussetzungen

- Python 3.8+
- pip

### Installation

```bash
# Repository klonen oder Dateien kopieren
cd todo_app

# Abhängigkeiten installieren
pip install streamlit pytest

# Für E2E-Tests (optional)
pip install pytest-playwright
playwright install chromium
```

### App starten

```bash
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

---

## Tests

### Testübersicht

| Datei | Typ | Anzahl | Fokus |
|-------|-----|--------|-------|
| `test_unit.py` | Unit | ~30 | Einzelne Klassen isoliert |
| `test_integration.py` | Integration | ~10 | Zusammenspiel von Komponenten |
| `system_test.py` | System | ~10 | Gesamtsystem kontrolliert |
| `test_e2e.py` | E2E | ~8 | Echte Benutzerflows mit Browser |

### Tests ausführen

```bash
cd tests

# Alle Tests (ohne E2E)
pytest test_unit.py test_integration.py system_test.py -v

# Nur Unit-Tests
pytest test_unit.py -v

# Mit Coverage
pip install pytest-cov
pytest --cov=.. --cov-report=html -v

# E2E-Tests (erfordert laufende App)
# Terminal 1: streamlit run ../app.py
# Terminal 2: pytest test_e2e.py -v --headed
```

### Teststruktur (AAA-Muster)

Alle Tests folgen dem Arrange-Act-Assert Muster:

```python
def test_add_task_returns_task(self, controller):
    # Arrange - Vorbereitung
    # (controller wird über Fixture bereitgestellt)
    
    # Act - Ausführung
    task = controller.add("Neue Aufgabe")
    
    # Assert - Prüfung
    assert task.title == "Neue Aufgabe"
    assert len(controller.tasks) == 1
```

---

## Figma Design

Die SVG-Designs im `design/` Ordner dienen als Vorlage für Figma:

| Datei | Ansicht | Größe | Beschreibung |
|-------|---------|-------|--------------|
| `todo_desktop.svg` | Desktop | 1200×800px | Vollständiges Layout mit allen Komponenten |
| `todo_mobile.svg` | Mobile | 360×800px | Responsive Anpassung, gestapelte Elemente |

### Import in Figma

1. Figma öffnen → New design file
2. **Datei → Import** oder `Ctrl+Shift+K`
3. SVG-Dateien auswählen
4. Als Referenz platzieren

### Streamlit Design System nutzen

Für echte Streamlit-Komponenten in Figma:

1. [Streamlit Design System](https://www.figma.com/community/file/1166786573904778097) öffnen
2. "Duplicate" klicken
3. Assets mit "st." Präfix verwenden (z.B. `st.button`, `st.text_input`)
4. SVG-Design als Vorlage für Positionierung nutzen

### Komponenten-Mapping

| SVG-Element | Streamlit-Komponente | Figma-Asset |
|-------------|---------------------|-------------|
| Titel-Eingabe | `st.text_input` | st.text_input |
| Kategorie-Dropdown | `st.selectbox` | st.selectbox |
| Datum-Picker | `st.date_input` | st.date_input |
| Erstellen-Button | `st.button(type="primary")` | st.button / primary |
| Filter-Radio | `st.radio(horizontal=True)` | st.radio |
| Checkbox | `st.checkbox` | st.checkbox |
| Statistik | `st.metric` | st.metric |
| Fortschritt | `st.progress` | st.progress |

---

## Lizenz

Dieses Projekt wurde für die DHBW Stuttgart - Software Engineering Vorlesung erstellt.
#   T o - D o - A p p - S E 1 
 
 