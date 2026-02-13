import pytest
import sys
import os
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controller import TaskController
from repository import InMemoryTaskRepository
from patterns import (
    ExternalTaskFormat, 
    TaskMediator
)

class TestTodoApp:
    
    @pytest.fixture
    def controller(self):
        return TaskController(repository=InMemoryTaskRepository())
    
    # Hinzufügen eines neue Task
    def test_add_todo_item(self, controller):

        # Arrange
        title = "Neue Aufgabe"
        
        # Act
        task = controller.add(title, category="Arbeit")
        
        # Assert
        assert task.title == title
        assert len(controller.tasks) == 1
    
    #Entfernen eines Items
    def test_remove_todo_item(self, controller):

        task = controller.add("Zu loeschen")
        
        result = controller.delete(task.id)
        
        assert result == True
        assert len(controller.tasks) == 0
    
    # Markieren als erledigt
    def test_mark_as_done(self, controller):

        task = controller.add("Erledigen")
        
        controller.toggle(task.id)
        
        assert task.done == True
    
    # Markieren als nicht erledigt
    def test_mark_as_not_done(self, controller):

        task = controller.add("Wieder oeffnen")
        controller.toggle(task.id)
        
        controller.toggle(task.id)
        
        assert task.done == False
    
    #Bearbeiten eines Items
    def test_edit_todo_item(self, controller):

        task = controller.add("Alter Titel")
        
        controller.update(task.id, title="Neuer Titel", category="Neu")
        
        assert task.title == "Neuer Titel"
        assert task.category == "Neu"

# Mediator-Tests
class TestTaskMediator:
    
    @pytest.fixture
    # Mediator mit InMemory-Repository für Tests
    def mediator(self):
        repo = InMemoryTaskRepository()
        ctrl = TaskController(repository=repo)
        return TaskMediator(ctrl)
    
    # Task hinzufügen über Mediator
    def test_add_task(self, mediator):
        task = mediator.add_task("Mediator Task", category="Test")
        assert task is not None
        assert len(mediator.get_all_tasks()) == 1
    
    # Task mit Fälligkeitsdatum hinzufügen
    def test_add_task_with_due_date(self, mediator):
        due = date.today() + timedelta(days=3)
        task = mediator.add_task("Mit Datum", due_date=due)
        assert task.due_date == due
    
    # Task mit leerem Titel hinzufügen (gibt None zurück)
    def test_add_task_empty_returns_none(self, mediator):
        result = mediator.add_task("")
        assert result is None
    
    # Löschen eines Tasks über Mediator
    def test_delete_task(self, mediator):
        task = mediator.add_task("Zu löschen")
        result = mediator.delete_task(task.id)
        
        assert result == True
        assert len(mediator.get_all_tasks()) == 0
    
    # Löschen nicht existierenden Tasks gibt False
    def test_delete_task_not_found(self, mediator):
        result = mediator.delete_task("nicht-vorhanden")
        assert result == False
        

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=term-missing"])
