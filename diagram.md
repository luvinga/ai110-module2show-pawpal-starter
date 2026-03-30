classDiagram
    class Task {
        +String description
        +String time
        +String frequency
        +Date due_date
        +bool completion_status
        +mark_complete() void
    }

    class Pet {
        +String name
        +String species
        +List~String~ preferences
        +List~Task~ tasks
    }

    class Owner {
        +String name
        +int available_minutes
        +List~Pet~ pets
        +get_all_tasks() List~Task~
    }

    class Scheduler {
        +Owner owner
        +time_to_minutes(String) int
        +sort_by_time(List~Task~) List~Task~
        +filter_tasks(List~Task~, bool, String) List~Task~
        +mark_task_complete(Task, Pet) void
        +handle_recurring_task(Task, Pet) void
        +detect_conflicts(List~Task~) List~String~
        +retrieve_tasks() List~Task~
        +organize_tasks(List~Task~) List~Task~
        +build_schedule() List~Task~
        +explain_plan(List~Task~) String
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : contains
    Scheduler "1" --> "1" Owner : manages


