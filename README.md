# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation summary

The logic layer lives in `pawpal_system.py` (class design in `diagrams/uml.mmd`). `main.py` is a terminal demo and `tests/test_pawpal.py` holds the pytest tests.

- **`Task`** (dataclass): one activity with a title, type, due time, duration, priority, frequency and completion status. It can mark itself complete, reschedule, and report whether it is overdue.
- **`Pet`** (dataclass): a pet's details plus its own list of tasks and health records. `add_task` stamps the task with the pet's id so a task always knows who it belongs to.
- **`Owner`** (dataclass): holds multiple pets. `get_all_tasks()` returns every pet's tasks in one list, and `get_upcoming_tasks()` filters that to what is due soon.
- **`Scheduler`**: the "brain". It reads tasks through `Owner.get_all_tasks()` (never from a single pet), so plans cover all pets. It builds the daily plan (sorted by priority, then time), detects overlapping tasks, and creates the next occurrence of daily/weekly/monthly tasks when one is completed.
- **Enums** (`TaskType`, `Frequency`, `Priority`) keep task attributes consistent.

How they fit together: an `Owner` has `Pet`s, each `Pet` has `Task`s, and the `Scheduler` takes an `Owner` and works across all of its pets' tasks.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
$ python main.py
Today's Schedule for Jordan (Saturday, October 17, 2026)
========================================================================
Time    Pet       Task                    Priority  Duration
------------------------------------------------------------------------
07:30   Biscuit   Morning walk            High      30 min
08:00   Biscuit   Heartworm pill          High      5 min
07:45   Whiskers  Breakfast               Medium    10 min
18:00   Whiskers  Brush fur               Low       15 min
------------------------------------------------------------------------
4 task(s) today

Warning: overlapping tasks:
  - 07:30 Biscuit: Morning walk
  - 07:45 Whiskers: Breakfast

```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
