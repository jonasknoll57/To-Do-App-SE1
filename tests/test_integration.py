"""
Integrationstests für die TODO-App.
Testet das Zusammenspiel von Controller und Repository.

Ausführung:
    pytest test_integration.py -v
"""
import pytest
from controller import TaskController
from repository import InMemoryTaskRepository


class TestIntegration:
    
    # 1. Mehrere Aufgaben erstellen → Repository konsistent
    def test_multiple_tasks_repository_consistent(self):
        # Arrange
        repo = InMemoryTaskRepository()
        ctrl = TaskController(repository=repo)
        
        # Act
        ctrl.add("Aufgabe 1", category="Arbeit")
        ctrl.add("Aufgabe 2", category="Privat")
        ctrl.add("Aufgabe 3")
        ctrl.save()
        
        # Assert
        loaded = repo.load()
        assert len(loaded) == 3
    
    # 2. Status ändern → Repository aktualisiert
    def test_status_change_updates_repository(self):
        # Arrange
        repo = InMemoryTaskRepository()
        ctrl = TaskController(repository=repo)
        task = ctrl.add("Status Test")
        
        # Act
        ctrl.toggle(task.id)
        ctrl.save()
        
        # Assert
        loaded = repo.load()
        assert loaded[0].done == True
    
    # 3. Löschen → aus Repository verschwunden
    def test_delete_removes_from_repository(self):
        # Arrange
        repo = InMemoryTaskRepository()
        ctrl = TaskController(repository=repo)
        task = ctrl.add("Zu loeschen")
        ctrl.save()
        
        # Act
        ctrl.delete(task.id)
        ctrl.save()
        
        # Assert
        loaded = repo.load()
        assert len(loaded) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
