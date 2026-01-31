# TODO-App mit MVC-Architektur

Eine funktionale TODO-Anwendung mit Python, Streamlit und MVC-Architektur, inklusive Design Patterns, umfangreicher Teststrategie und responsivem UI-Design.

---

## Inhaltsverzeichnis

1. [MVC-Architektur](#mvc-architektur)
2. [Funktionale Anforderungen](#funktionale-anforderungen)
3. [Nicht-Funktionale Anforderungen](#nicht-funktionale-anforderungen)
4. [UI-Dokumentation (Nielsen-Heuristiken)](#ui-dokumentation-nielsen-heuristiken)
5. [Installation & Start](#installation--start)
6. [Tests](#tests)
7. [Projektstruktur](#projektstruktur)
8. [Figma-Designs](#figma-designs)

---

## MVC-Architektur

### Warum ist MVC für eine TODO-App sinnvoll?

MVC (Model-View-Controller) trennt die Anwendung in drei Schichten mit klaren Verantwortlichkeiten. Diese Architektur ist für eine TODO-App besonders sinnvoll, weil:

- **Testbarkeit:** Model, Repository und Controller lassen sich unabhängig von der Streamlit-UI (View) testen. Unit-Tests prüfen die Geschäftslogik isoliert, ohne dass ein Browser oder eine laufende Anwendung nötig ist.
- **Wartbarkeit:** Änderungen am UI (View) erfordern keine Änderungen an der Logik (Controller) oder den Daten (Model). Neue Features können gezielt in der richtigen Schicht ergänzt werden, ohne bestehenden Code zu brechen.
- **Wiederverwendbarkeit:** Der Controller kann mit verschiedenen Views verwendet werden (z.B. CLI, REST-API, anderes UI-Framework), da er keine Abhängigkeit zur Darstellungsschicht hat.
- **Übersichtlichkeit:** Klare Trennung der Verantwortlichkeiten macht den Code verständlicher. Jede Datei hat einen definierten Zweck und eine begrenzte Zuständigkeit.
- **Skalierbarkeit:** Neue Funktionen (z.B. Benutzer, Projekte, Tags) können in separaten Modulen ergänzt werden, ohne bestehenden Code zu verändern.

### Wie wurde MVC in diesem Projekt konkret umgesetzt?

| Schicht | Datei | Klasse(n) | Verantwortlichkeit |
|---------|-------|-----------|--------------------|
| **Model** | `src/model.py` | `Task` | Datenstruktur (dataclass) mit Feldern: title, done, category, due_date, id, created_at. Methoden für Serialisierung (`to_dict`, `from_dict`), Status (`toggle`, `is_overdue`, `is_due_today`). |
| **Repository** | `src/repository.py` | `TaskRepositoryInterface`, `JSONTaskRepository`, `InMemoryTaskRepository` | Abstrakte Persistenz-Schicht. JSON-Implementierung für Produktion, In-Memory für Tests. |
| **Controller** | `src/controller.py` | `TaskController` | Geschäftslogik und CRUD-Operationen: add, delete, update, toggle, get_all, get_open, get_done, get_by_category, get_overdue, get_due_today, get_statistics. |
| **View** | `src/view.py` | `TodoView` | Streamlit-UI mit Methoden: render_header, render_add_task_form, render_task_section, render_statistics, render. |
| **App** | `app.py` | `main()`, `init_app()` | Einstiegspunkt. Initialisiert Repository, Controller und Mediator, erstellt die View und startet die Anwendung. |


---

## Funktionale Anforderungen

| ID | Beschreibung |
|----|--------------|
| FR-01 | Aufgaben werden persistent in einer JSON-Datei gespeichert und bleiben nach Neustart erhalten |
| FR-02 | Neue Aufgaben können über ein Formular mit Titel,  (optionaler) Kategorie und (optionalem) Fälligkeitsdatum hinzugefügt werden |
| FR-03 | Aufgaben können einzeln gelöscht werden |
| FR-04 | Bestehende Aufgaben können bearbeitet werden (Titel, Kategorie, Datum) |
| FR-05 | Aufgaben können per Checkbox als erledigt oder offen markiert werden |
| FR-06 | Alle Aufgaben werden in einer dynamischen Liste angezeigt |
| FR-07 | Aufgaben können nach Status gefiltert werden (Alle, Offen, Erledigt) |
| FR-08 | Aufgaben können Kategorien zugeordnet werden; Kategorien sind vom Benutzer erstellbar und löschbar |
| FR-09 | Ein Fälligkeitsdatum kann per Datepicker gesetzt werden (nur zukünftige Daten) |
| FR-10 | Überfällige Aufgaben werden visuell mit einer Warnung hervorgehoben |
| FR-11 | Ein Fortschrittsbalken zeigt den Erledigungsgrad aller Aufgaben an |
| FR-12 | Ein Statistik-Dashboard zeigt Gesamt-, Offen- und Erledigt-Anzahl als Metriken an |
| FR-13 | Aufgaben können nach Kategorie gefiltert werden |
| FR-14 | Eine Smart-Sortierung priorisiert Aufgaben automatisch nach Dringlichkeit (Überfällig -> Heute -> Zukunft -> Ohne Datum -> Erledigt) |

---

## Nicht-Funktionale Anforderungen

| ID  | Beschreibung |
|----|--------------|
| NFR-01 | Eine Aufgabe kann mit maximal 3 Klicks angelegt werden |
| NFR-02 | Die App startet in unter 2 Sekunden |
| NFR-03 | Gleiche Eingaben führen immer zum gleichen Ergebnis (deterministische Logik) |
| NFR-04 | Die App läuft auf Windows, macOS und Linux |
| NFR-05 | MVC-Architektur mit klarer Trennung der Verantwortlichkeiten |
| NFR-06 | Code-Coverage von über 80% ist erreichbar |
| NFR-07 | Responsive Design für Desktop und Mobile |
| NFR-08 | Alle interaktiven Elemente haben Tooltips |
| NFR-09 | Fehlerhafte Eingaben (z.B. leere Titel) werden abgefangen und dem Benutzer gemeldet |
| NFR-10 | Smart-Sort ordnet Aufgaben automatisch nach Dringlichkeit |

---

## UI-Dokumentation (Nielsen-Heuristiken)

für jedes der 10 UI-Prinzipien nach Nielsen wurde mindestens ein konkretes Beispiel in der App umgesetzt:

| Nr. | Prinzip | UI-Element | Konkretes Beispiel |
|---|---------|------------|--------------------|
| 1 | **Sichtbarkeit des Systemstatus** | Fortschrittsbalken, Statistiken | `st.progress()` zeigt den Erledigungsgrad in Prozent an. `st.metric()` zeigt Gesamt-, Offen- und Erledigt-Anzahl als Zahlenwerte im Dashboard. Der Benutzer sieht jederzeit, wie weit er ist. |
| 2 | **Übereinstimmung zwischen System und realer Welt** | Icons, natürliche Sprache | Vertraute Symbole werden verwendet: Checkbox für erledigt, ein Papierkorb-Icon für Löschen, ein Kalender-Icon für Datum, ein Warn-Icon für überfällige Aufgaben. Die Begriffe entsprechen der Alltagssprache (z.B. "Erstellen", "Erledigt", "Offen"). |
| 3 | **Benutzerkontrolle und Freiheit** | Abbrechen-Button, Rückgängig | Im Bearbeitungsmodus gibt es einen "Abbrechen"-Button, um Änderungen zu verwerfen. Kategorien können sowohl erstellt als auch wieder gelöscht werden. Erledigte Aufgaben können wieder als offen markiert werden. |
| 4 | **Konsistenz und Standards** | Einheitliches Layout | Alle Aufgaben folgen demselben Layout: Checkbox links, Titel in der Mitte, Aktions-Buttons rechts. Farben, Abstande und Schriftgroessen sind durchgehend konsistent. |
| 5 | **Fehlervermeidung** | Validierung, Constraints | Leere Titel werden abgelehnt und eine Fehlermeldung angezeigt. Der Datepicker erlaubt nur Daten ab heute und verhindert so die Eingabe vergangener Fälligkeitsdaten. |
| 6 | **Wiedererkennung statt Erinnerung** | Sichtbare Optionen | Kategorien werden als Dropdown dauerhaft angezeigt, Filter sind als Segmented Control permanent sichtbar. Der Benutzer muss sich nichts merken, alle Optionen sind direkt erkennbar. |
| 7 | **Flexibilität und Effizienz** | Schnellaktionen, Anpassung | Ein-Klick-Checkbox für schnelles Abhaken. Smart-Sort-Toggle für automatische Priorisierung. Kategorien können individuell erstellt und verwaltet werden. |
| 8 | **Ästhetik und minimalistisches Design** | Klares Layout | Nur notwendige Elemente werden angezeigt. Visuelle Trennlinien (`st.divider()`) schaffen Struktur. Dezente Farben und ausreichend Whitespace sorgen für Übersichtlichkeit. |
| 9 | **Fehlererkennung und -behebung** | Klare Fehlermeldungen | Bei leerem Titel erscheint eine verständliche Fehlermeldung, die das Problem benennt und die Loesung vorgibt. Fehlermeldungen sind kontextnah platziert. |
| 10 | **Hilfe und Dokumentation** | Tooltips, Hinweise | Ein Hilfe-Fenster erklärt die Bedienung der App. Alle Buttons haben `help`-Tooltips. Hinweistexte (`st.caption`) geben Orientierung im Formular. |

---

## Installation & Start

### Voraussetzungen

- Python 3.8 oder höher
- pip

### 1. Virtual Environment erstellen

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**macOS & Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Abhängigkeiten installieren

```
pip install -r requirements.txt

playwright install
```

### 3. App starten

```
streamlit run app.py
```
---

## Tests

Es wurden bewusst mehr Tests (z.B. Unit-Tests) implementiert als notwendig, um die geforderte Coverage zu erreichen.

### Testuebersicht

| Datei | Typ | Beschreibung |
|-------|-----|--------------|
| `tests/test_unit.py` | Unit-Tests | Isolierte Tests einzelner Klassen und Methoden (Model, Controller, Patterns) |
| `tests/test_integration.py` | Integrationstests | Tests des Zusammenspiels von Controller und Repository |
| `tests/system_test.py` | Systemtests | Tests des Gesamtsystems mit persistenter Speicherung |
| `tests/test_e2e.py` | End-to-End-Tests | Browser-basierte Tests mit Playwright |

### Tests ausführen

```
# Alle Tests (ohne E2E)
pytest tests/test_unit.py tests/test_integration.py tests/system_test.py -v

# E2E-Tests (App muss in separatem Terminal laufen)
# Terminal 1: streamlit run app.py
# Terminal 2: pytest tests/test_e2e.py -v
```

---

## Projektstruktur

```
To-Do-App-SE1/
├── app.py                    # Einstiegspunkt (initialisiert MVC)
├── requirements.txt          # Python-Abhängigkeiten
├── pytest.ini                # Pytest-Konfiguration
├── conftest.py               # Pytest-Fixtures
├── .coveragerc               # Coverage-Konfiguration
├── .streamlit/
│   └── config.toml           # Streamlit-Theme
├── data/
│   └── tasks.json            # Persistente Datenspeicherung
├── designs/
│   ├── ToDo_Desktop.svg      # Desktop-Design (SVG)
│   ├── ToDo_Desktop.png      # Desktop-Design (PNG-Vorschau)
│   ├── ToDo_Mobile.svg       # Mobile-Design (SVG)
│   └── ToDo_Mobile.png       # Mobile-Design (PNG-Vorschau)
├── src/
│   ├── model.py              # Model: Task-Datenklasse
│   ├── repository.py         # Repository: Persistenz-Schicht
│   ├── controller.py         # Controller: Geschäftslogik
│   ├── patterns.py           # Design Patterns (Factory, Adapter, Mediator)
│   └── view.py               # View: Streamlit-UI
└── tests/
    ├── test_unit.py           # Unit-Tests
    ├── test_integration.py    # Integrationstests
    ├── system_test.py         # Systemtests
    └── test_e2e.py            # End-to-End-Tests
```

---

## Figma-Designs

Im Ordner `designs/` befinden sich die Designs für Desktop und Mobile als SVG- und PNG-Dateien. Die SVG-Dateien können in Figma importiert werden, zeigen jedoch nicht die spezifischen Icons an. Die PNG-Dateien zeigen das tatsächliche Design.
