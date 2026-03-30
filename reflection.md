# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

- What classes did you include, and what responsibilities did you assign to each?
I initially planned to create a class called petName, but realized a pet's name is an attribute of a Pet class, not a class itself. I redesigned it so Pet holds name, species, and preferences, and Scheduler takes a Pet and list of CareTask objects to build a plan.

**b. Design changes**

- Did your design change during implementation?
Yes, several changes were made during implementation to better fit the requirements and improve functionality.
- If yes, describe at least one change and why you made it.
One major change was renaming CareTask to Task and updating its attributes: changed duration_minutes (int) to time (str in HH:MM format) for better time parsing, added due_date (Date) for recurring tasks, and added frequency (str) for recurrence. This was done to support advanced features like sorting by time and automatic recurrence, making the system more robust for pet scheduling.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers available time (owner's available_minutes), task completion status, and pet associations. It prioritizes incomplete tasks and sorts them by time.
- How did you decide which constraints mattered most?
Time availability was prioritized as the primary constraint to ensure schedules are feasible. Completion status ensures only pending tasks are scheduled, and pet associations prevent overloading individual pets.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler assumes tasks are performed sequentially and only checks for pet overload (multiple tasks per pet) rather than time-based overlaps, as tasks lack explicit start times. This tradeoff prioritizes simplicity and avoids complex time slot management, making the system easier to implement and understand, while still providing useful warnings for potential scheduling issues in a pet care context.

**c. Edge cases**

- What edge cases did you consider in your scheduling algorithm?
Edge cases considered include: no tasks available (returns empty schedule), owner's available time is zero (no tasks scheduled), tasks with invalid time formats (handled by sort_by_time method), recurring tasks that exceed available time (only scheduled once per day), and multiple pets with conflicting tasks (detected by detect_conflicts).
- How did you handle them?
For no tasks or zero time, the scheduler returns an empty list. Invalid times are parsed safely in sort_by_time, raising ValueError if unparseable. Recurrence is handled by creating new tasks only if due_date matches current date and time allows. Conflicts are warned via st.warning in the UI.

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
AI was used extensively for design brainstorming (generating UML diagrams and class skeletons), code generation (implementing dataclasses and methods), debugging (fixing time parsing issues), refactoring (simplifying recurrence logic), and documentation (writing README and reflection).
- What kinds of prompts or questions were most helpful?
Prompts asking for "generate class skeletons from UML", "add methods for sorting and filtering", "write unit tests", and "update documentation" were most helpful, as they provided structured, incremental development steps.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When AI suggested a complex recurrence system with multiple frequency options (daily, weekly, monthly), I simplified it to basic daily recurrence to avoid overcomplicating the scheduler for this pet care app.
- How did you evaluate or verify what the AI suggested?
I evaluated by considering the project scope (simple pet scheduling), testing the suggestion in code, and verifying if it aligned with user requirements; I ran tests to ensure the simplified version worked correctly without unnecessary complexity.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested sorting tasks by time, filtering incomplete tasks, marking tasks complete with recurrence, detecting pet overload conflicts, and generating schedules within available time.
- Why were these tests important?
These tests ensure the core scheduling logic works correctly, preventing bugs in task management and recurrence, which are critical for a reliable pet care app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
Very confident, as all unit tests pass and the app runs without errors in the UI.
- What edge cases would you test next if you had more time?
I would test overlapping tasks with explicit start/end times, multiple owners sharing pets, and long-term recurrence over weeks to ensure scalability.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with the integration of smart scheduling features like recurrence and conflict detection, which make the app practical for real pet care.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would add explicit start and end times for tasks to enable more precise scheduling and conflict detection, and redesign the UI for better mobile responsiveness.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that iterative design with AI can accelerate development, but human judgment is essential for simplifying complex suggestions to fit project scope and maintain usability.
