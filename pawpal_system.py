from dataclasses import dataclass, field

@dataclass
class Task:
    """Represents a single activity for a pet."""
    description: str
    time: int  # duration in minutes
    frequency: str  # e.g., "daily", "weekly"
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

    def retrieve_tasks(self) -> list[Task]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_tasks(self, tasks: list[Task]) -> list[Task]:
        """Organize tasks by sorting them (e.g., by time ascending, then by frequency)."""
        # Sort by completion status (incomplete first), then by time
        return sorted(tasks, key=lambda t: (t.completion_status, t.time))

    def build_schedule(self) -> list[Task]:
        """Build a schedule by retrieving and organizing tasks, considering owner's available time."""
        tasks = self.retrieve_tasks()
        organized = self.organize_tasks(tasks)
        # Filter to fit within available minutes, prioritizing incomplete tasks
        scheduled = []
        total_time = 0
        for task in organized:
            if not task.completion_status and total_time + task.time <= self.owner.available_minutes:
                scheduled.append(task)
                total_time += task.time
        return scheduled

    def explain_plan(self, schedule: list[Task]) -> str:
        """Explain the built schedule."""
        if not schedule:
            return f"No tasks scheduled for {self.owner.name}. Check available time or task completion status."
        explanation = f"Care plan for {self.owner.name} (available time: {self.owner.available_minutes} min):\n"
        total_time = sum(task.time for task in schedule)
        explanation += f"Total scheduled time: {total_time} min\n\nScheduled tasks:\n"
        for task in schedule:
            status = "Incomplete" if not task.completion_status else "Complete"
            explanation += f"- {task.description} ({task.time} min, {task.frequency}, Status: {status})\n"
        return explanation
