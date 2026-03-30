import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Manage application memory with st.session_state
# st.session_state acts like a dictionary that persists across page refreshes
# Check if 'owner' key exists; if not, create a default Owner instance
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("PawPal+ Pet Care Scheduler")

# Display current state
st.write(f"**Owner:** {st.session_state.owner.name} (Available time: {st.session_state.owner.available_minutes} min)")
st.write(f"**Pets:** {', '.join([p.name + f' ({p.species})' for p in st.session_state.owner.pets]) or 'None'}")
if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name}: {len(pet.tasks)} tasks")

st.divider()

# Update Owner
st.subheader("Update Owner Info")
new_owner_name = st.text_input("Owner Name", value=st.session_state.owner.name)
new_available_time = st.number_input("Available Time (min)", value=st.session_state.owner.available_minutes, min_value=1)
if st.button("Update Owner"):
    st.session_state.owner.name = new_owner_name
    st.session_state.owner.available_minutes = new_available_time
    st.success("Owner updated!")

st.divider()

# Add Pet
st.subheader("Add a Pet")
pet_name = st.text_input("Pet Name", value="Mochi")
pet_species = st.selectbox("Species", ["dog", "cat", "other"])
pet_preferences = st.text_input("Preferences (comma-separated)", value="walks, play")
if st.button("Add Pet"):
    preferences_list = [p.strip() for p in pet_preferences.split(",") if p.strip()]
    new_pet = Pet(name=pet_name, species=pet_species, preferences=preferences_list)
    st.session_state.owner.pets.append(new_pet)
    st.success(f"Pet '{pet_name}' added!")
    st.rerun()  # Refresh to show updated list

st.divider()

# Add Task to a Pet
st.subheader("Add a Task to a Pet")
if st.session_state.owner.pets:
    selected_pet = st.selectbox("Select Pet", [p.name for p in st.session_state.owner.pets])
    task_desc = st.text_input("Task Description", value="Walk the pet")
    task_time = st.number_input("Time (min)", value=30, min_value=1)
    task_freq = st.selectbox("Frequency", ["daily", "weekly"])
    if st.button("Add Task"):
        pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        new_task = Task(description=task_desc, time=task_time, frequency=task_freq)
        pet.tasks.append(new_task)
        st.success(f"Task '{task_desc}' added to {selected_pet}!")
        st.rerun()
else:
    st.info("Add a pet first to add tasks.")

st.divider()

# Build and Display Schedule
st.subheader("Build Schedule")
if st.button("Generate Schedule"):
    if st.session_state.owner.pets and any(pet.tasks for pet in st.session_state.owner.pets):
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.build_schedule()
        explanation = scheduler.explain_plan(schedule)
        st.text_area("Today's Schedule", explanation, height=300)
    else:
        st.error("Add pets and tasks first!")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
