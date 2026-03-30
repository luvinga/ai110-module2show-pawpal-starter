from pawpal_system import Task, Pet, Owner, Scheduler

# Create Owner
owner = Owner(name="Jordan", available_minutes=60)

# Create Pets
mochi = Pet(name="Mochi", species="dog", preferences=["walks", "play"])
whiskers = Pet(name="Whiskers", species="cat", preferences=["grooming", "food"])

# Create Tasks with different times
walk_task = Task(description="Walk Mochi", time=30, frequency="daily")
feed_task = Task(description="Feed Whiskers", time=10, frequency="daily")
play_task = Task(description="Play with Mochi", time=20, frequency="daily")

# Add tasks to pets
mochi.tasks.append(walk_task)
mochi.tasks.append(play_task)
whiskers.tasks.append(feed_task)

# Add pets to owner
owner.pets = [mochi, whiskers]

# Create Scheduler and build schedule
scheduler = Scheduler(owner)
schedule = scheduler.build_schedule()

# Print Today's Schedule
print("Today's Schedule")
print(scheduler.explain_plan(schedule))
