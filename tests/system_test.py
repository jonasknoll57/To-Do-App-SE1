# -*- coding: utf-8 -*-
"""
Systemtests für die TODO-App.
Testet das gesamte System technisch, kontrolliert.

Ausführung mit Coverage:
    pytest system_test.py -v --cov=. --cov-report=term-missing
"""
import pytest
from datetime import date, timedelta
from model import Task
from controller import TaskController
from repository import JSONTaskRepository, InMemoryTaskRepository
from patterns import TaskMediator, TaskFactory, ExternalTaskFormat


class TestTodoSystem:
    """Systemtests: Gesamtsystem prüfen."""
    
    @pytest.fixture
    def system(self):
        repo = InMemoryTaskRepository()
        ctrl = TaskController(repository=repo)
        mediator = TaskMediator(ctrl)
        return mediator
    
    def test_full_lifecycle(self, system):
        """Vollständiger Lebenszyklus: Create -> Update -> Toggle -> Delete."""
        # CREATE
        task = system.add_task("Lifecycle", category="Test", due_date=date.today())
        assert len(system.get_all_tasks()) == 1
        
        # UPDATE
        system.update_task(task.id, title="Geändert", category="Neu")
        assert task.title == "Geändert"
        
        # TOGGLE
        system.toggle_task(task.id)
        assert task.done == True
        
        # DELETE
        system.delete_task(task.id)
        assert len(system.get_all_tasks()) == 0
    
    def test_persistence_across_sessions(self, tmp_path):
        """Tasks bleiben nach Neustart erhalten."""
        filepath = str(tmp_path / "tasks.json")
        
        # Session 1
        repo1 = JSONTaskRepository(filepath)
        ctrl1 = TaskController(repository=repo1)
        mediator1 = TaskMediator(ctrl1)
        mediator1.add_task("Persistent", category="Test")
        
        # Session 2
        repo2 = JSONTaskRepository(filepath)
        ctrl2 = TaskController(repository=repo2)
        ctrl2.load()
        
        assert len(ctrl2.get_all()) == 1
    
    def test_system_import_external(self, system):
        """System importiert externe Tasks."""
        # Arrange
        externals = [
            ExternalTaskFormat(name="Import 1", completed=0, tag="API"),
            ExternalTaskFormat(name="Import 2", completed=1, tag="External")
        ]
        
        # Act
        count = system.import_external_tasks(externals)
        
        # Assert
        assert count == 2
        assert len(system.get_all_tasks()) == 2
    
    def test_system_statistics(self, system):
        """System Statistiken korrekt."""
        # Arrange
        system.add_task("Task 1")
        system.add_task("Task 2")
        task3 = system.add_task("Task 3")
        system.toggle_task(task3.id)
        
        # Act
        stats = system.controller.get_statistics()
        
        # Assert
        assert stats["total"] == 3
        assert stats["done"] == 1
        assert stats["open"] == 2
    


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=term-missing"])