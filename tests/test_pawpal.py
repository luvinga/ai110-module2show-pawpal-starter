import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from pawpal_system import Task, Pet

def test_task_completion():
    """Test that calling mark_complete() changes the task's status to True."""
    task = Task(description="Test Task", time=10, frequency="daily", completion_status=False)
    assert not task.completion_status  # Initially False
    task.mark_complete()
    assert task.completion_status  # Should be True after marking complete

def test_task_addition():
    """Test that adding a task to a Pet increases the pet's task count."""
    pet = Pet(name="Test Pet", species="dog", preferences=["play"])
    initial_count = len(pet.tasks)
    task = Task(description="New Task", time=15, frequency="daily")
    pet.tasks.append(task)
    assert len(pet.tasks) == initial_count + 1