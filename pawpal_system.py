"""PawPal logic layer: backend classes for the pet care app (see diagrams/uml.mmd)."""

from __future__ import annotations

import calendar
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from enum import Enum
from itertools import count
from typing import List, Optional

# Ids for auto-generated recurring tasks; starts high to avoid clashing with caller-chosen ids.
_generated_ids = count(1_000_000)


class TaskType(Enum):
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    GROOMING = "grooming"
    VET_VISIT = "vet_visit"
    PLAY = "play"


class Frequency(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Reminder:
    id: int
    remind_at: datetime
    sent: bool = False

    def send(self) -> None:
        """Mark the reminder as sent (delivery itself is left to the UI layer)."""
        self.sent = True


@dataclass
class Task:
    id: int
    title: str
    type: TaskType
    due_at: datetime
    frequency: Frequency = Frequency.ONCE
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    notes: str = ""
    duration_minutes: int = 30
    pet_id: Optional[int] = None  # set by Pet.add_task
    end_date: Optional[date] = None  # last day a recurring task may occur
    reminders: List[Reminder] = field(default_factory=list)

    @property
    def end_at(self) -> datetime:
        """Return when the task finishes (due time plus duration)."""
        return self.due_at + timedelta(minutes=self.duration_minutes)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, new_due: datetime) -> None:
        """Move the task to a new due date/time and reopen it."""
        self.due_at = new_due
        self.completed = False

    def is_overdue(self, now: Optional[datetime] = None) -> bool:
        """Return True if the task is past due and not completed."""
        now = now or datetime.now()
        return not self.completed and self.due_at < now


@dataclass
class HealthRecord:
    id: int
    record_date: date
    description: str
    vet_name: str = ""
    weight_kg: Optional[float] = None


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str = ""
    birth_date: Optional[date] = None
    weight_kg: Optional[float] = None
    tasks: List[Task] = field(default_factory=list)
    health_records: List[HealthRecord] = field(default_factory=list)

    def get_age(self, today: Optional[date] = None) -> Optional[int]:
        """Return the pet's age in whole years, or None if the birth date is unknown."""
        if self.birth_date is None:
            return None
        today = today or date.today()
        had_birthday = (today.month, today.day) >= (self.birth_date.month, self.birth_date.day)
        return today.year - self.birth_date.year - (0 if had_birthday else 1)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        task.pet_id = self.id
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def add_health_record(self, record: HealthRecord) -> None:
        """Add a health record; a recorded weight updates the pet's current weight."""
        self.health_records.append(record)
        if record.weight_kg is not None:
            self.weight_kg = record.weight_kg


@dataclass
class Owner:
    id: int
    name: str
    email: str = ""
    phone: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet; raises ValueError if a pet with the same id already exists."""
        if any(p.id == pet.id for p in self.pets):
            raise ValueError(f"Pet id {pet.id} already exists")
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove the pet with the given id; raises KeyError if not found."""
        for i, pet in enumerate(self.pets):
            if pet.id == pet_id:
                del self.pets[i]
                return
        raise KeyError(f"No pet with id {pet_id}")

    def get_pets(self) -> List[Pet]:
        """Return a copy of this owner's pet list."""
        return list(self.pets)

    def get_pet(self, pet_id: int) -> Optional[Pet]:
        """Return the pet with the given id, or None."""
        return next((p for p in self.pets if p.id == pet_id), None)

    def get_all_tasks(self) -> List[Task]:
        """Return every pet's tasks together in one list."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def get_upcoming_tasks(self, days: int, now: Optional[datetime] = None) -> List[Task]:
        """Return incomplete tasks, across all pets, due within the next `days` days."""
        now = now or datetime.now()
        limit = now + timedelta(days=days)
        upcoming = [t for t in self.get_all_tasks() if not t.completed and now <= t.due_at <= limit]
        return sorted(upcoming, key=lambda t: t.due_at)


class Scheduler:
    """Builds and organizes care plans from all of an owner's pets via Owner.get_all_tasks()."""

    def generate_daily_plan(self, owner: Owner, plan_date: date) -> List[Task]:
        """Return the day's incomplete tasks for all pets, ordered by priority then time."""
        todays = [
            t for t in owner.get_all_tasks()
            if not t.completed and t.due_at.date() == plan_date
        ]
        return self.sort_by_priority(todays)

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted highest priority first, earliest due time breaking ties."""
        return sorted(tasks, key=lambda t: (-t.priority.value, t.due_at))

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Return tasks whose time windows overlap another task's (O(n log n))."""
        ordered = sorted(tasks, key=lambda t: t.due_at)
        conflicts: List[Task] = []
        latest: Optional[Task] = None  # task with the latest end time seen so far
        for task in ordered:
            if latest is not None and task.due_at < latest.end_at:
                if latest not in conflicts:
                    conflicts.append(latest)
                conflicts.append(task)
            if latest is None or task.end_at > latest.end_at:
                latest = task
        return conflicts

    def next_occurrence(self, task: Task) -> Optional[Task]:
        """Return the next instance of a recurring task, or None if one-off or past its end date."""
        if task.frequency == Frequency.ONCE:
            return None
        if task.frequency == Frequency.DAILY:
            next_due = task.due_at + timedelta(days=1)
        elif task.frequency == Frequency.WEEKLY:
            next_due = task.due_at + timedelta(weeks=1)
        else:  # MONTHLY: clamp the day, e.g. Jan 31 -> Feb 28
            year = task.due_at.year + task.due_at.month // 12
            month = task.due_at.month % 12 + 1
            day = min(task.due_at.day, calendar.monthrange(year, month)[1])
            next_due = task.due_at.replace(year=year, month=month, day=day)
        if task.end_date is not None and next_due.date() > task.end_date:
            return None
        return replace(task, id=next(_generated_ids), due_at=next_due, completed=False, reminders=[])

    def complete_task(self, owner: Owner, task: Task) -> Optional[Task]:
        """Complete a task and, if it recurs, add the next occurrence to the same pet."""
        task.mark_complete()
        following = self.next_occurrence(task)
        pet = owner.get_pet(task.pet_id) if task.pet_id is not None else None
        if following is not None and pet is not None:
            pet.add_task(following)
        return following
