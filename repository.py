#Repository: Persistenz-Schicht für die TODO-App
# Abstrahiert den Datenzugriff vom Rest der Anwendung.

import json
import os
from typing import List, Optional
from abc import ABC, abstractmethod
from model import Task


class TaskRepositoryInterface(ABC):
    
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        pass
    
    @abstractmethod
    def load(self) -> List[Task]:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass

# Konkrete Implementierung: JSON-Datei als Speicher
class JSONTaskRepository(TaskRepositoryInterface):
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath
    
    def save(self, tasks: List[Task]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
    
    def load(self) -> List[Task]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def clear(self) -> None:
        self.save([])


class InMemoryTaskRepository(TaskRepositoryInterface):
 
    def __init__(self):
        self._tasks: List[Task] = []
    
    def save(self, tasks: List[Task]) -> None:
        self._tasks = tasks.copy()
    
    def load(self) -> List[Task]:
        return self._tasks.copy()
    
    def clear(self) -> None:
        self._tasks = []
