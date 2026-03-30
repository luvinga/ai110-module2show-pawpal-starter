import sys
import os
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Test that calling mark_complete() changes the task's status to True."""
    task = Task(description="Test Task", time="00:10", frequency="daily", due_date=date.today(), completion_status=False)
    assert not task.completion_status  # Initially False
    task.mark_complete()
    assert task.completion_status  # Should be True after marking complete

def test_task_addition():
    """Test that adding a task to a Pet increases the pet's task count."""
    pet = Pet(name="Test Pet", species="dog", preferences=["play"])
    initial_count = len(pet.tasks)
    task = Task(description="New Task", time="00:15", frequency="daily", due_date=date.today())
    pet.tasks.append(task)
    assert len(pet.tasks) == initial_count + 1

def test_sorting_correctness():
    """Verify tasks are returned in chronological order by time."""
    tasks = [
        Task("Task C", "00:30", "daily", date.today()),
        Task("Task A", "00:10", "daily", date.today()),
        Task("Task B", "00:20", "daily", date.today())
    ]
    owner = Owner("Test Owner", 60, [])
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(tasks)
    # Should be sorted by time: 00:10, 00:20, 00:30
    assert sorted_tasks[0].description == "Task A"
    assert sorted_tasks[1].description == "Task B"
    assert sorted_tasks[2].description == "Task C"

def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    pet = Pet("Test Pet", "dog", [])
    task = Task("Daily Walk", "00:30", "daily", date.today())
    pet.tasks.append(task)
    owner = Owner("Test Owner", 60, [pet])
    scheduler = Scheduler(owner)
    
    # Mark complete
    scheduler.mark_task_complete(task, pet)
    
    # Should have two tasks now: original (complete) and new one
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completion_status == True  # Original
    assert pet.tasks[1].completion_status == False  # New
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)  # Next day

def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times (pet overload)."""
    pet = Pet("Test Pet", "dog", [])
    task1 = Task("Task 1", "00:10", "daily", date.today())
    task2 = Task("Task 2", "00:20", "daily", date.today())
    pet.tasks.extend([task1, task2])
    owner = Owner("Test Owner", 60, [pet])
    scheduler = Scheduler(owner)
    schedule = [task1, task2]  # Simulate schedule with both tasks
    
    warnings = scheduler.detect_conflicts(schedule)
    # Should warn about pet having multiple tasks
    assert any("Test Pet has 2 tasks scheduled" in w for w in warnings)