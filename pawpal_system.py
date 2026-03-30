from dataclasses import dataclass, field
from datetime import date, timedelta
from collections import Counter

@dataclass
class Task:
    """Represents a single activity for a pet."""
    description: str
    time: str  # duration in "HH:MM" format, e.g., "00:30"
    frequency: str  # e.g., "daily", "weekly"
    due_date: date  # when this task is due
    completion_status: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completion_status = True

@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    preferences: list[str]
    tasks: list[Task] = field(default_factory=list)

@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM string to minutes."""
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by time in ascending order using HH:MM format."""
        return sorted(tasks, key=lambda t: self.time_to_minutes(t.time))

    def filter_tasks(self, tasks: list[Task], completed: bool = None, pet_name: str = None) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered = tasks
        if completed is not None:
            filtered = [t for t in filtered if t.completion_status == completed]
        if pet_name:
            pet = next((p for p in self.owner.pets if p.name == pet_name), None)
            if pet:
                filtered = [t for t in filtered if t in pet.tasks]
        return filtered

    def mark_task_complete(self, task: Task, pet: Pet):
        """Mark a task complete and handle recurring tasks by creating next occurrence."""
        task.mark_complete()
        self.handle_recurring_task(task, pet)

    def handle_recurring_task(self, task: Task, pet: Pet):
        """Create a new instance for the next occurrence if task is recurring."""
        if task.frequency == "daily":
            next_due = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_due = task.due_date + timedelta(weeks=1)
        else:
            return  # Non-recurring
        
        new_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            due_date=next_due,
            completion_status=False
        )
        pet.tasks.append(new_task)

    def detect_conflicts(self, schedule: list[Task]) -> list[str]:
        """Detect lightweight conflicts in the schedule and return warning messages."""
        warnings = []
        pet_task_counts = Counter()
        for task in schedule:
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet_task_counts[pet.name] += 1
        
        for pet_name, count in pet_task_counts.items():
            if count > 1:
                warnings.append(f"Warning: {pet_name} has {count} tasks scheduled. Ensure they can be done sequentially without overlap.")
        
        total_min = sum(self.time_to_minutes(t.time) for t in schedule)
        if total_min > self.owner.available_minutes:
            warnings.append(f"Warning: Total scheduled time ({total_min} min) exceeds available time ({self.owner.available_minutes} min).")
        
        return warnings

    def retrieve_tasks(self) -> list[Task]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_tasks(self, tasks: list[Task]) -> list[Task]:
        """Organize tasks by sorting them (e.g., by time ascending, then by frequency)."""
        # Sort by completion status (incomplete first), then by time
        return sorted(tasks, key=lambda t: (t.completion_status, self.time_to_minutes(t.time)))

    def build_schedule(self) -> list[Task]:
        """Build a schedule by retrieving and organizing tasks, considering owner's available time."""
        tasks = self.retrieve_tasks()
        organized = self.organize_tasks(tasks)
        # Filter to fit within available minutes, prioritizing incomplete tasks
        scheduled = []
        total_time = 0
        for task in organized:
            task_min = self.time_to_minutes(task.time)
            if not task.completion_status and total_time + task_min <= self.owner.available_minutes:
                scheduled.append(task)
                total_time += task_min
        return scheduled

    def explain_plan(self, schedule: list[Task]) -> str:
        """Explain the built schedule."""
        if not schedule:
            return f"No tasks scheduled for {self.owner.name}. Check available time or task completion status."
        explanation = f"Care plan for {self.owner.name} (available time: {self.owner.available_minutes} min):\n"
        total_time = sum(self.time_to_minutes(t.time) for t in schedule)
        explanation += f"Total scheduled time: {total_time} min\n\nScheduled tasks:\n"
        for task in schedule:
            status = "Incomplete" if not task.completion_status else "Complete"
            explanation += f"- {task.description} ({task.time}, {task.frequency}, Status: {status})\n"
        
        # Add conflict warnings
        warnings = self.detect_conflicts(schedule)
        if warnings:
            explanation += "\nWarnings:\n"
            for warning in warnings:
                explanation += f"- {warning}\n"
        
        return explanation
