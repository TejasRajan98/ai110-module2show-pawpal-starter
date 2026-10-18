"""PawPal logic layer: backend classes for the pet care app (skeleton, based on diagrams/uml.mmd)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import List, Optional


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
        """Send the reminder and mark it as sent."""
        pass


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
    reminders: List[Reminder] = field(default_factory=list)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def reschedule(self, new_due: datetime) -> None:
        """Move the task to a new due date/time."""
        pass

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not completed."""
        pass


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

    def get_age(self) -> int:
        """Return the pet's age in years."""
        pass

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        pass

    def add_health_record(self, record: HealthRecord) -> None:
        """Add a health record to this pet."""
        pass


@dataclass
class Owner:
    id: int
    name: str
    email: str = ""
    phone: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet_id: int) -> None:
        """Remove the pet with the given id."""
        pass

    def get_pets(self) -> List[Pet]:
        """Return all of this owner's pets."""
        pass

    def get_upcoming_tasks(self, days: int) -> List[Task]:
        """Return incomplete tasks across all pets due within the next `days` days."""
        pass


class Scheduler:
    """Builds and organizes care plans from an owner's pets and tasks."""

    def generate_daily_plan(self, owner: Owner, plan_date: date) -> List[Task]:
        """Return the ordered list of tasks for the given day."""
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority (then due time)."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Return tasks whose scheduled times conflict."""
        pass

    def next_occurrence(self, task: Task) -> Optional[Task]:
        """Return the next instance of a recurring task, or None if it is one-off."""
        pass
