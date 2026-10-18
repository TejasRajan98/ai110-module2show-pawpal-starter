"""Temporary testing ground: build some data and print today's schedule."""

from datetime import date, datetime, time

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task, TaskType


def at(hour: int, minute: int = 0) -> datetime:
    """Return today's date at the given time."""
    return datetime.combine(date.today(), time(hour, minute))


def print_schedule(owner: Owner, plan: list[Task], scheduler: Scheduler) -> None:
    pet_names = {pet.id: pet.name for pet in owner.get_pets()}
    print(f"Today's Schedule for {owner.name} ({date.today():%A, %B %d, %Y})")
    print("=" * 72)
    print(f"{'Time':<8}{'Pet':<10}{'Task':<24}{'Priority':<10}{'Duration':<9}")
    print("-" * 72)
    for task in plan:
        print(
            f"{task.due_at:%H:%M}   "
            f"{pet_names.get(task.pet_id, '?'):<10}"
            f"{task.title:<24}"
            f"{task.priority.name.title():<10}"
            f"{task.duration_minutes} min"
        )
    print("-" * 72)
    print(f"{len(plan)} task(s) today")

    conflicts = scheduler.detect_conflicts(plan)
    if conflicts:
        print("\nWarning: overlapping tasks:")
        for task in conflicts:
            print(f"  - {task.due_at:%H:%M} {pet_names.get(task.pet_id, '?')}: {task.title}")


def main() -> None:
    owner = Owner(id=1, name="Jordan", email="jordan@example.com")
    biscuit = Pet(id=1, name="Biscuit", species="dog", breed="Beagle")
    whiskers = Pet(id=2, name="Whiskers", species="cat", breed="Tabby")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    biscuit.add_task(Task(1, "Morning walk", TaskType.WALK, at(7, 30),
                          Frequency.DAILY, Priority.HIGH, duration_minutes=30))
    biscuit.add_task(Task(2, "Heartworm pill", TaskType.MEDICATION, at(8, 0),
                          Frequency.MONTHLY, Priority.HIGH, duration_minutes=5))
    whiskers.add_task(Task(3, "Breakfast", TaskType.FEEDING, at(7, 45),
                           Frequency.DAILY, Priority.MEDIUM, duration_minutes=10))
    whiskers.add_task(Task(4, "Brush fur", TaskType.GROOMING, at(18, 0),
                           Frequency.WEEKLY, Priority.LOW, duration_minutes=15))

    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner, date.today())
    print_schedule(owner, plan, scheduler)


if __name__ == "__main__":
    main()
