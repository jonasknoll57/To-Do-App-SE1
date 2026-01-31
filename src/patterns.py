from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from model import Task

if TYPE_CHECKING:
    from controller import TaskController


# FACTORY PATTERN
# Zweck: Flexible Task-Erstellung ohne direkte Klassenkenntnis

class TaskFactory:
    #Factory Pattern: Erstellt verschiedene Task-Typen mit Präfixen.
    
    #Verwendung:
        #task = TaskFactory.create("work", "Meeting vorbereiten")
        # Ergebnis: Task mit Titel "🔨 Meeting vorbereiten"
    
    PREFIXES = {
        "work": "🔨 ",
        "personal": "👤 ",
        "shopping": "🛒 ",
        "urgent": "🔴 ",
        "health": "💪 ",
    }
    
    @staticmethod
    def create(task_type: str, title: str, **kwargs) -> Task:
        #Erstellt einen Task basierend auf dem Typ mit entsprechendem Präfix
        prefix = TaskFactory.PREFIXES.get(task_type, "")
        return Task(title=prefix + title, **kwargs)
    
    @staticmethod
    def get_available_types() -> List[str]:
        #Gibt alle verfügbaren Task-Typen zurück
        return list(TaskFactory.PREFIXES.keys())


# ABSTRACT FACTORY PATTERN
# Zweck: Familien von Task-Typen erstellen (einfach vs. detailliert)

class AbstractTaskFactory(ABC):
    """
    Abstract Factory Pattern: Definiert Schnittstelle für Task-Familien.
    Ermöglicht das Erstellen von Task-Varianten ohne konkrete Klassen zu kennen.
    """
    
    @abstractmethod
    def create_task(self, title: str, **kwargs) -> Task:
        """Erstellt einen Task gemäß der Factory-Implementierung."""
        pass


class SimpleTaskFactory(AbstractTaskFactory):
    """Erstellt einfache Tasks ohne Extras."""
    
    def create_task(self, title: str, **kwargs) -> Task:
        return Task(title=title)


class PriorityTaskFactory(AbstractTaskFactory):
    """Erstellt Tasks mit Prioritäts-Markierung (⚡)."""
    
    def create_task(self, title: str, **kwargs) -> Task:
        return Task(title="⚡ " + title, **kwargs)


class DetailedTaskFactory(AbstractTaskFactory):
    """Erstellt Tasks mit allen Details (Kategorie, Datum)."""
    
    def __init__(self, default_category: str = "Allgemein"):
        self.default_category = default_category
    
    def create_task(self, title: str, **kwargs) -> Task:
        if "category" not in kwargs:
            kwargs["category"] = self.default_category
        if "due_date" not in kwargs:
            kwargs["due_date"] = date.today()
        return Task(title="📋 " + title, **kwargs)


# ADAPTER PATTERN
# Zweck: Externe Datenformate in internes Task-Format konvertieren

class ExternalTaskFormat:
    """
    Simuliert externes Task-Format (z.B. von einer API).
    Hat andere Feldnamen als unser internes Task-Format.
    """
    
    def __init__(self, name: str, completed: int, tag: str = ""):
        self.name = name           # statt 'title'
        self.completed = completed  # 0/1 statt bool
        self.tag = tag             # statt 'category'


class TaskAdapter:
    """
    Adapter Pattern: Konvertiert externes Format zu internem Task-Format.
    Ermöglicht Integration externer Datenquellen ohne Codeänderung.
    
    Verwendung:
        external = ExternalTaskFormat(name="API Task", completed=1, tag="Work")
        internal = TaskAdapter.adapt(external)
    """
    
    @staticmethod
    def adapt(external: ExternalTaskFormat) -> Task:
        """Konvertiert ein externes Task-Objekt zu internem Task."""
        task = Task(
            title=external.name,
            category=external.tag
        )
        task.done = bool(external.completed)
        return task
    
    @staticmethod
    def adapt_many(externals: List[ExternalTaskFormat]) -> List[Task]:
        """Konvertiert eine Liste von externen Tasks."""
        return [TaskAdapter.adapt(e) for e in externals]
    
    @staticmethod
    def to_external(task: Task) -> ExternalTaskFormat:
        """Konvertiert internen Task zu externem Format (Reverse-Adapter)."""
        return ExternalTaskFormat(
            name=task.title,
            completed=1 if task.done else 0,
            tag=task.category
        )


# MEDIATOR PATTERN
# Zweck: Zentrale Kommunikation zwischen Komponenten (View <-> Controller)

class TaskMediator:
    """
    Mediator Pattern: Koordiniert Kommunikation zwischen View und Controller.
    
    Reduziert direkte Abhängigkeiten zwischen Komponenten.
    Alle Task-Operationen laufen über den Mediator.
    
    Verwendung:
        mediator = TaskMediator(controller, repository)
        mediator.add_task("Neue Aufgabe", category="Arbeit")
        mediator.toggle_task(task_id)
    """
    
    def __init__(self, controller: "TaskController"):
        self.controller = controller
        self._listeners: List[callable] = []
    
    def add_listener(self, callback: callable) -> None:
        """Registriert einen Listener für Änderungen."""
        self._listeners.append(callback)
    
    def _notify(self, event: str) -> None:
        """Benachrichtigt alle Listener über Änderungen."""
        for listener in self._listeners:
            listener(event)
    
    # Task-Operationen (delegiert an Controller)
    
    def add_task(self, title: str, category: str = "", 
                 due_date: Optional[date] = None) -> Optional[Task]:
        """Fügt einen Task hinzu und benachrichtigt Listener."""
        try:
            task = self.controller.add(title, category, due_date)
            self.controller.save()
            self._notify("task_added")
            return task
        except ValueError:
            return None
    
    def delete_task(self, task_id: str) -> bool:
        """Löscht einen Task und benachrichtigt Listener."""
        result = self.controller.delete(task_id)
        if result:
            self.controller.save()
            self._notify("task_deleted")
        return result
    
    def toggle_task(self, task_id: str) -> bool:
        """Wechselt Task-Status und benachrichtigt Listener."""
        result = self.controller.toggle(task_id)
        if result:
            self.controller.save()
            self._notify("task_toggled")
        return result
    
    def update_task(self, task_id: str, title: str = None, 
                    category: str = None, due_date: Optional[date] = None) -> bool:
        """Aktualisiert einen Task und benachrichtigt Listener."""
        try:
            result = self.controller.update(task_id, title, category, due_date)
            if result:
                self.controller.save()
                self._notify("task_updated")
            return result
        except ValueError:
            return False
    
    # Abfragen (delegiert an Controller)
    
    def get_all_tasks(self) -> List[Task]:
        """Gibt alle Tasks zurück."""
        return self.controller.get_all()
    
    def get_open_tasks(self) -> List[Task]:
        """Gibt offene Tasks zurück."""
        return self.controller.get_open()
    
    def get_done_tasks(self) -> List[Task]:
        """Gibt erledigte Tasks zurück."""
        return self.controller.get_done()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Gibt Task anhand ID zurück."""
        return self.controller.get_by_id(task_id)
    
    def get_categories(self) -> List[str]:
        """Gibt alle verwendeten Kategorien zurück."""
        return self.controller.get_categories()
    
    def get_by_category(self, category: str) -> List[Task]:
        """Filtert Tasks nach Kategorie."""
        return self.controller.get_by_category(category)
    
    # Factory-Integration
    
    def add_typed_task(self, task_type: str, title: str, **kwargs) -> Task:
        """Erstellt einen Task über die Factory und fügt ihn hinzu."""
        task = TaskFactory.create(task_type, title, **kwargs)
        self.controller.tasks.append(task)
        self.controller.save()
        self._notify("task_added")
        return task
    
    def import_external_tasks(self, externals: List[ExternalTaskFormat]) -> int:
        """Importiert externe Tasks über den Adapter."""
        tasks = TaskAdapter.adapt_many(externals)
        for task in tasks:
            self.controller.tasks.append(task)
        self.controller.save()
        self._notify("tasks_imported")
        return len(tasks)
