from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

# Create Owner
owner = Owner(name="Jordan", available_minutes=60)

# Create Pets
mochi = Pet(name="Mochi", species="dog", preferences=["walks", "play"])
whiskers = Pet(name="Whiskers", species="cat", preferences=["grooming", "food"])

# Create Tasks with different times in HH:MM format, added out of order
play_task = Task(description="Play with Mochi", time="00:20", frequency="daily", due_date=date.today())
walk_task = Task(description="Walk Mochi", time="00:30", frequency="daily", due_date=date.today())
feed_task = Task(description="Feed Whiskers", time="00:10", frequency="daily", due_date=date.today())
groom_task = Task(description="Groom Whiskers", time="00:15", frequency="weekly", due_date=date.today())

# Add tasks to pets (out of order)
mochi.tasks.append(walk_task)
mochi.tasks.append(play_task)
whiskers.tasks.append(feed_task)
whiskers.tasks.append(groom_task)

# Add pets to owner
owner.pets = [mochi, whiskers]

# Create Scheduler
scheduler = Scheduler(owner)

# Retrieve all tasks
all_tasks = scheduler.retrieve_tasks()
print("All tasks (unsorted):")
for t in all_tasks:
    print(f"- {t.description}: {t.time}, Due: {t.due_date}, Status: {'Complete' if t.completion_status else 'Incomplete'}")

# Sort by time
sorted_tasks = scheduler.sort_by_time(all_tasks)
print("\nTasks sorted by time:")
for t in sorted_tasks:
    print(f"- {t.description}: {t.time}")

# Filter incomplete tasks
incomplete_tasks = scheduler.filter_tasks(all_tasks, completed=False)
print("\nIncomplete tasks:")
for t in incomplete_tasks:
    print(f"- {t.description}: {t.time}")

# Filter tasks for Mochi
mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
print("\nTasks for Mochi:")
for t in mochi_tasks:
    print(f"- {t.description}: {t.time}")

# Demonstrate recurring tasks: Mark feed_task complete
print("\nMarking 'Feed Whiskers' complete...")
scheduler.mark_task_complete(feed_task, whiskers)
print("Tasks for Whiskers after marking complete:")
for t in whiskers.tasks:
    print(f"- {t.description}: {t.time}, Due: {t.due_date}, Status: {'Complete' if t.completion_status else 'Incomplete'}")

# Build and print schedule
schedule = scheduler.build_schedule()
print("\nToday's Schedule")
print(scheduler.explain_plan(schedule))
def detect_conflicts(self, schedule: list[Task], owner: Owner) -> list[str]:
    conflicts = []
    total_time = sum(t.time for t in schedule)
    if total_time > owner.available_minutes:
        conflicts.append(f"Time overflow: {total_time} min > {owner.available_minutes} min")
    pet_task_counts = {}
    for task in schedule:
        for pet in owner.pets:
            if task in pet.tasks:
                pet_task_counts[pet.name] = pet_task_counts.get(pet.name, 0) + 1
    for pet, count in pet_task_counts.items():
        if count > 3:  # Arbitrary limit
            conflicts.append(f"{pet} overloaded with {count} tasks")
    return conflicts