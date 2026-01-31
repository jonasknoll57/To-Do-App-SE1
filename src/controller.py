#Controller: Geschäftslogik für die TODO-App.
#Verwaltet CRUD-Operationen und delegiert Persistenz an das Repository.
from typing import List, Optional
from datetime import date
from model import Task
from repository import TaskRepositoryInterface, JSONTaskRepository


class TaskController:
    """
   für CRUD-Operationen
    """
    
    def __init__(self, repository: TaskRepositoryInterface = None):
        """
        Initialisiert Controller mit Repository
        
        """
        self.repository = repository or JSONTaskRepository()
        self.tasks: List[Task] = []
    
    #CRUD Operationen
    
    def add(self, title: str, category: str = "", 
            due_date: Optional[date] = None) -> Task:
      
            #ValueError: Wenn der Titel leer ist
        if not title or not title.strip():
            raise ValueError("Titel darf nicht leer sein")
        
        task = Task(
            title=title.strip(),
            category=category,
            due_date=due_date
        )
        self.tasks.append(task)
        return task
    
    def delete(self, task_id: str) -> bool:
        #Löscht einen Task anhand der ID
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def toggle(self, task_id: str) -> bool:
        """Wechselt den Erledigt-Status eines Tasks."""
        task = self.get_by_id(task_id)
        if task:
            task.toggle()
            return True
        return False
    
    def update(self, task_id: str, title: str = None, category: str = None,
               due_date: Optional[date] = None) -> bool:
        """
        Aktualisiert einen Task.
        
        Raises:
            ValueError: Wenn der neue Titel leer ist
        """
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        if title is not None:
            if not title.strip():
                raise ValueError("Titel darf nicht leer sein")
            task.title = title.strip()
        
        if category is not None:
            task.category = category
        
        if due_date is not None:
            task.due_date = due_date
        
        return True
    
    # Abfragen
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Gibt Task anhand ID zurück."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all(self) -> List[Task]:
        """Gibt alle Tasks zurück."""
        return self.tasks
    
    def get_open(self) -> List[Task]:
        """Gibt offene Tasks zurück."""
        return [t for t in self.tasks if not t.done]
    
    def get_done(self) -> List[Task]:
        """Gibt erledigte Tasks zurück."""
        return [t for t in self.tasks if t.done]
    
    def get_categories(self) -> List[str]:
        """Gibt alle verwendeten Kategorien zurück (sortiert)."""
        categories = set(t.category for t in self.tasks if t.category)
        return sorted(list(categories))
    
    def get_by_category(self, category: str) -> List[Task]:
        """Filtert Tasks nach Kategorie."""
        return [t for t in self.tasks if t.category == category]
    
    def get_overdue(self) -> List[Task]:
        """Gibt überfällige Tasks zurück."""
        return [t for t in self.tasks if t.is_overdue()]
    
    def get_due_today(self) -> List[Task]:
        """Gibt heute fällige Tasks zurück."""
        return [t for t in self.tasks if t.is_due_today()]
    
    # Persistenz (delegiert an Repository)
    
    def save(self) -> None:
        """Speichert alle Tasks über das Repository."""
        self.repository.save(self.tasks)
    
    def load(self) -> None:
        """Lädt alle Tasks aus dem Repository."""
        self.tasks = self.repository.load()
    
    # Statistiken
    
    def get_statistics(self) -> dict:
        """Gibt Statistiken über die Tasks zurück."""
        total = len(self.tasks)
        done = len(self.get_done())
        open_count = len(self.get_open())
        
        return {
            "total": total,
            "done": done,
            "open": open_count,
            "progress": done / total if total > 0 else 0,
            "overdue": len(self.get_overdue()),
            "due_today": len(self.get_due_today())
        }
