from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from model import Task

if TYPE_CHECKING:
    from controller import TaskController


# Factory Pattern: Flexible Task-Erstellung ohne direkte Klassenkenntnis
class TaskFactory:
    #Erstellt verschiedene Task-Typen mit Präfixen.
    
    PREFIXES = {
        "work": "🔨 ",
        "personal": "👤 ",
        "shopping": "🛒 ",
        "urgent": "🔴 ",
        "health": "💪 ",
    }
    
    @staticmethod
    def create(task_type: str, title: str, **kwargs) -> Task:
        prefix = TaskFactory.PREFIXES.get(task_type, "")
        return Task(title=prefix + title, **kwargs)
    
    @staticmethod
    def get_available_types() -> List[str]:
        return list(TaskFactory.PREFIXES.keys())


# Abstract Factory Pattern: Definiert Schnittstelle für Task-Familien
class AbstractTaskFactory(ABC):
    
    @abstractmethod
    def create_task(self, title: str, **kwargs) -> Task:
        pass


class SimpleTaskFactory(AbstractTaskFactory):
    
    def create_task(self, title: str, **kwargs) -> Task:
        return Task(title=title)


class PriorityTaskFactory(AbstractTaskFactory):
    
    def create_task(self, title: str, **kwargs) -> Task:
        return Task(title="⚡ " + title, **kwargs)


class DetailedTaskFactory(AbstractTaskFactory):
    
    def __init__(self, default_category: str = "Allgemein"):
        self.default_category = default_category
    
    def create_task(self, title: str, **kwargs) -> Task:
        if "category" not in kwargs:
            kwargs["category"] = self.default_category
        if "due_date" not in kwargs:
            kwargs["due_date"] = date.today()
        return Task(title="📋 " + title, **kwargs)


# Adapter Pattern: Integration externer Task-Formate ohne Codeänderung

class ExternalTaskFormat:
    
    def __init__(self, name: str, completed: int, tag: str = ""):
        self.name = name          
        self.completed = completed  
        self.tag = tag            


# Adapter für externe Task-Formate

class TaskAdapter:
    
    @staticmethod
    def adapt(external: ExternalTaskFormat) -> Task:
        task = Task(
            title=external.name,
            category=external.tag
        )
        task.done = bool(external.completed)
        return task
    
    @staticmethod
    def adapt_many(externals: List[ExternalTaskFormat]) -> List[Task]:
        return [TaskAdapter.adapt(e) for e in externals]
    
    @staticmethod
    def to_external(task: Task) -> ExternalTaskFormat:
        return ExternalTaskFormat(
            name=task.title,
            completed=1 if task.done else 0,
            tag=task.category
        )


# Zusätzlich Implementiert
# Mediator Pattern: Koordiniert Kommunikation zwischen View und Controller
class TaskMediator:
    def __init__(self, controller: "TaskController"):
        self.controller = controller
        self._listeners: List[callable] = []
    
    def add_listener(self, callback: callable) -> None:
        self._listeners.append(callback)
    
    def _notify(self, event: str) -> None:
        for listener in self._listeners:
            listener(event)
    
    # Task-Operationen (delegiert an Controller)
    
    def add_task(self, title: str, category: str = "", 
                 due_date: Optional[date] = None) -> Optional[Task]:
        try:
            task = self.controller.add(title, category, due_date)
            self.controller.save()
            self._notify("task_added")
            return task
        except ValueError:
            return None
    
    def delete_task(self, task_id: str) -> bool:
        result = self.controller.delete(task_id)
        if result:
            self.controller.save()
            self._notify("task_deleted")
        return result
    
    def toggle_task(self, task_id: str) -> bool:
        result = self.controller.toggle(task_id)
        if result:
            self.controller.save()
            self._notify("task_toggled")
        return result
    
    def update_task(self, task_id: str, title: str = None, 
                    category: str = None, due_date: Optional[date] = None) -> bool:
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
        return self.controller.get_all()
    
    def get_open_tasks(self) -> List[Task]:
        return self.controller.get_open()
    
    def get_done_tasks(self) -> List[Task]:
        return self.controller.get_done()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.controller.get_by_id(task_id)
    
    def get_categories(self) -> List[str]:
        return self.controller.get_categories()
    
    def get_by_category(self, category: str) -> List[Task]:
        return self.controller.get_by_category(category)
    
    # Factory-Integration
    
    def add_typed_task(self, task_type: str, title: str, **kwargs) -> Task:
        task = TaskFactory.create(task_type, title, **kwargs)
        self.controller.tasks.append(task)
        self.controller.save()
        self._notify("task_added")
        return task
    
    def import_external_tasks(self, externals: List[ExternalTaskFormat]) -> int:
        tasks = TaskAdapter.adapt_many(externals)
        for task in tasks:
            self.controller.tasks.append(task)
        self.controller.save()
        self._notify("tasks_imported")
        return len(tasks)
