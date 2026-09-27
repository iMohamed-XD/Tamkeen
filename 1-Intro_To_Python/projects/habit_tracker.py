import datetime

habits:list[list] = []
def choice():
    return int(input("""
    ===== Habit Tracker =====
    1. Add habit
    2. View habits
    3. Mark habit as completed
    4. Remove habit
    5. Show statistics
    6. Show completions for a habit in this week
    7. Exit
    """))

def add_habit(name:str) -> bool:
    habit:list = [name, 0, []]
    habits.append(habit)
    return True

def mark_habit_completed(name:str) -> bool:
    for habit in habits:
        if habit[0] == name:
            habit[1] += 1
            habit[2].append(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            return True
    return False


def view_habits() -> None:
    if len(habits) == 0:
        print("No habits found")
    else:
        for habit in habits:
            print(f"{habit[0]} - Completed {habit[1]} times")
            if habit[2]:
                print("  Completions:")
                for completion in habit[2]:
                    print(f"    {completion}")


def remove_habit(name:str) -> bool:
    for habit in habits:
        if habit[0] == name:
            habits.remove(habit)
            return True
    return False

def show_statistics() -> None:
    total_habits = len(habits)
    total_completions = sum(habit[1] for habit in habits)
    most_completed_habit = max(habits, key=lambda x: x[1], default=None)
    print("===== Habit Statistics =====")
    print(f"""
    Total habits: {total_habits}
    Total completions: {total_completions}
    Most completed habit:
    {most_completed_habit[0] if most_completed_habit is not None else 'No habits found'} - {most_completed_habit[1] if most_completed_habit is not None else ''}{' completions' if most_completed_habit is not None else ''}
    """)

def show_completions_for_habit_this_week(name:str) -> None:
    for habit in habits:
        if habit[0] == name:
            completions_this_week = [completion for completion in habit[2] if datetime.datetime.strptime(completion, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).isocalendar()[1] == datetime.datetime.now(datetime.timezone.utc).isocalendar()[1]]
            print(f"Completions for {name} this week: {len(completions_this_week)}")
            return
    print("Habit not found")

while True:
    user_choice = choice()
    match user_choice:
        case 1:
            habit_name = input("Enter habit name: \n")
            if add_habit(habit_name):
                print("Habit added successfully")
            else:
                print("Failed to add habit")
        case 2:
            view_habits()
        case 3:
            if len(habits) == 0:
                print("No habits found")
            else:
                habit_name = input("Enter habit name to mark as completed: \n")
                if mark_habit_completed(habit_name):
                    print("Habit marked as completed")
                else:
                    print("Habit not found")
        case 4:
            if len(habits) == 0:
                print("No habits found")
            else:
                habit_name = input("Enter habit name to remove: \n")
                if remove_habit(habit_name):
                    print("Habit removed successfully")
                else:
                    print("Habit not found")
        case 5:
            show_statistics()
        case 6:
            if len(habits) == 0:
                print("No habits found")
            else:
                habit_name = input("Enter habit name to show completions for this week: \n")
                show_completions_for_habit_this_week(habit_name)
        case 7:
            print("Exiting...")
            break