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
    
    # Task Satus toggeln über Mediator
    def test_toggle_task(self, mediator):
        task = mediator.add_task("Toggle")
        result = mediator.toggle_task(task.id)
        
        assert result == True
        assert task.done == True
    
    def test_toggle_task_not_found(self, mediator):
        result = mediator.toggle_task("nicht-vorhanden")
        assert result == False
    
    def test_update_task(self, mediator):
        task = mediator.add_task("Original")
        result = mediator.update_task(task.id, title="Geändert", category="Neu")
        
        assert result == True
        assert task.title == "Geändert"
        assert task.category == "Neu"
    
    def test_update_task_with_date(self, mediator):
        task = mediator.add_task("Test")
        new_date = date.today() + timedelta(days=10)
        mediator.update_task(task.id, due_date=new_date)
        
        assert task.due_date == new_date
    
    def test_update_task_empty_title_returns_false(self, mediator):
        task = mediator.add_task("Original")
        result = mediator.update_task(task.id, title="")
        
        assert result == False
    
    def test_update_task_not_found(self, mediator):
        """Update nicht existierenden Tasks gibt False."""
        result = mediator.update_task("nicht-vorhanden", title="Test")
        assert result == False
    
    def test_get_all_tasks(self, mediator):
        """Alle Tasks werden zurückgegeben."""
        mediator.add_task("Task 1")
        mediator.add_task("Task 2")
        
        all_tasks = mediator.get_all_tasks()
        assert len(all_tasks) == 2
    
    def test_get_open_tasks(self, mediator):
        mediator.add_task("Offen")
        task2 = mediator.add_task("Erledigt")
        mediator.toggle_task(task2.id)
        
        open_tasks = mediator.get_open_tasks()
        assert len(open_tasks) == 1
    
    def test_get_done_tasks(self, mediator):
        task = mediator.add_task("Erledigt")
        mediator.toggle_task(task.id)
        
        done_tasks = mediator.get_done_tasks()
        assert len(done_tasks) == 1
    
    def test_get_task_by_id(self, mediator):
        task = mediator.add_task("Find Me")
        found = mediator.get_task_by_id(task.id)
        assert found == task

    
    def test_add_listener_and_notify(self, mediator):
        events = []
        mediator.add_listener(lambda e: events.append(e))
        
        task = mediator.add_task("Test")
        mediator.toggle_task(task.id)
        mediator.update_task(task.id, title="Updated")
        mediator.delete_task(task.id)
        
        assert "task_added" in events
        assert "task_toggled" in events
        assert "task_updated" in events
        assert "task_deleted" in events
    
    def test_add_typed_task(self, mediator):
        task = mediator.add_typed_task("work", "Meeting")
        
        assert len(mediator.get_all_tasks()) == 1
        assert "Meeting" in task.title
    
    def test_import_external_tasks(self, mediator):
        externals = [
            ExternalTaskFormat(name="Import 1", completed=0, tag="API"),
            ExternalTaskFormat(name="Import 2", completed=1)
        ]
        
        count = mediator.import_external_tasks(externals)
        
        assert count == 2
        assert len(mediator.get_all_tasks()) == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=term-missing"])
