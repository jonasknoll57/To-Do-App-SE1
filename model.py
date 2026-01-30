from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import uuid4
from typing import Optional


@dataclass
class Task:
    #Repräsentiert eine Aufgabe
    title: str
    done: bool = False
    category: str = ""
    due_date: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def toggle(self) -> None:
        """Wechselt den Erledigt-Status."""
        self.done = not self.done
    
    def is_overdue(self) -> bool:
        """Prüft ob Task überfällig ist."""
        if self.due_date and not self.done:
            return self.due_date < date.today()
        return False
    
    def is_due_today(self) -> bool:
        """Prüft ob Task heute fällig ist."""
        return self.due_date == date.today() if self.due_date else False
    
    def to_dict(self) -> dict:
        """Konvertiert Task zu Dictionary für JSON-Serialisierung."""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "category": self.category,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Erstellt Task aus Dictionary."""
        return Task(
            id=data["id"],
            title=data["title"],
            done=data["done"],
            category=data.get("category", ""),
            due_date=date.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            created_at=data.get("created_at", datetime.now().isoformat())
        )
