#Repository: Persistenz-Schicht für die TODO-App.
#Abstrahiert den Datenzugriff vom Rest der Anwendung.

import json
import os
from typing import List, Optional
from abc import ABC, abstractmethod
from model import Task


class TaskRepositoryInterface(ABC):
    """Abstrakte Schnittstelle für Task-Repositories."""
    
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        """Speichert alle Tasks."""
        pass
    
    @abstractmethod
    def load(self) -> List[Task]:
        """Lädt alle Tasks."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Löscht alle Tasks."""
        pass


class JSONTaskRepository(TaskRepositoryInterface):
    """
    Repository-Implementierung mit JSON-Datei als Persistenz.
    Kapselt alle Datei-Operationen.
    Zum testen
    """
    
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath
    
    def save(self, tasks: List[Task]) -> None:
        """Speichert Tasks persistent in JSON-Datei."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
    
    def load(self) -> List[Task]:
        """Lädt Tasks aus JSON-Datei."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def clear(self) -> None:
        """Löscht alle Tasks (leert die Datei)."""
        self.save([])


class InMemoryTaskRepository(TaskRepositoryInterface):
    """
    In-Memory Repository für Tests.
    Speichert Tasks nur im Arbeitsspeicher.
    """
    
    def __init__(self):
        self._tasks: List[Task] = []
    
    def save(self, tasks: List[Task]) -> None:
        """Speichert Tasks im Speicher."""
        self._tasks = tasks.copy()
    
    def load(self) -> List[Task]:
        """Lädt Tasks aus dem Speicher."""
        return self._tasks.copy()
    
    def clear(self) -> None:
        """Löscht alle Tasks."""
        self._tasks = []
