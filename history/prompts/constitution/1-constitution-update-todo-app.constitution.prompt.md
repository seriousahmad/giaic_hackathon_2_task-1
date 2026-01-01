---
id: 1
title: constitution-update-todo-app
stage: constitution
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: todo-app
branch: master
user: claude-code
command: sp.constitution
labels: ["constitution", "todo-app", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
# Project: In-Memory Console Todo App

## Project Overview

**Objective**
Design and implement a fully functional, console-based Todo application that operates entirely in memory. The project emphasizes clean architecture, clear specifications, and deterministic behavior suitable for AI-assisted development workflows using Spec-Kit Plus and Claude Code.

**Phase Details**
- **Phase 1 (MVP):** Core task management (CRUD, completion status, viewing).
- **Phase 2 (Enhanced Productivity):** Priorities, tags, search, filtering, sorting.
- **Phase 3 (Advanced Scheduling):** Recurring tasks, due dates, and reminders.

**MVP Focus**
- No external databases or file persistence.
- All data exists only during runtime (in-memory collections).
- Interaction is strictly via a terminal/console interface.
- Designed to be easily spec-generated and code-generated.

The application is intended as a reference-quality console app that demonstrates disciplined software design, extensibility, and AI-native development practices.

---

## Core Requirements

### 1. Add Task
- Users can create new todo items via console prompts or commands.
- Each task must support:
  - Title (required)
  - Optional description
  - Optional due date and time
  - Optional priority (default: medium)
  - Optional tags/categories
- Tasks are assigned a unique in-memory identifier.

### 2. Delete Task
- Users can remove a task by its identifier.
- Deletion must confirm the target task before removal.
- Attempting to delete a non-existent task must produce a clear error message.

### 3. Update Task
- Users can modify existing task fields:
  - Title
  - Description
  - Due date/time
  - Priority
  - Tags
- Partial updates are allowed (unchanged fields remain intact).
- Updates must validate inputs before applying changes.

### 4. View Task List
- Display all tasks in a readable, tabular or structured console format.
- Each task display must include:
  - ID
  - Title
  - Completion status
  - Priority
  - Due date (if any)
  - Tags (if any)
- Completed tasks should be visually distinguishable (e.g., `[✓]` vs `[ ]`).

### 5. Mark as Complete
- Users can toggle a task's completion status.
- Completed tasks remain visible unless filtered out.
- Toggling must be idempotent and reversible.

### 6. Priorities & Tags / Categories
- Supported priorities: `High`, `Medium`, `Low`.
- Tags are free-form labels (e.g., `work`, `home`, `urgent`).
- Tasks may have zero, one, or multiple tags.
- Priority and tags must be searchable and filterable.

### 7. Search & Filter
- Keyword search across task titles and descriptions.
- Filters supported:
  - Completion status (complete / incomplete)
  - Priority level
  - Due date or date range
  - Tag/category
- Search and filters can be combined.

### 8. Sort Tasks
- Tasks can be reordered by:
  - Due date (ascending / descending)
  - Priority (High → Low)
  - Alphabetical order (A–Z)
- Sorting must not mutate underlying data unless explicitly requested.

### 9. Recurring Tasks
- Tasks may be marked as recurring with a defined interval:
  - Daily
  - Weekly
  - Monthly
- When a recurring task is marked complete:
  - A new task instance is automatically scheduled with an updated due date.
- Recurrence logic must be deterministic and testable.

### 10. Due Dates & Time Reminders
- Tasks can have optional due dates with time precision.
- Console-based date/time input must follow a consistent format.
- Reminder behavior:
  - Console notifications when a task is due or overdue.
  - No reliance on external schedulers or OS-level services.
- Reminder checks occur during user interactions (polling model).

---

## Non-Functional Requirements

### Code Quality
- Follow **PEP 8** standards strictly.
- Use modular architecture:
  - Models (Task, enums)
  - Services (task manager, scheduler)
  - UI layer (console input/output)
- Mandatory use of Python type hints.
- Functions and classes must have docstrings.

### Error Handling
- Graceful handling of invalid input.
- No unhandled exceptions during normal user interaction.
- Clear, human-readable error messages.

### Console UX
- Prompts must be concise and consistent.
- Commands and menus should be discoverable.
- Output formatting must prioritize readability.
- No raw stack traces shown to users.

---

## Technology Stack and Tools

### Runtime & Language
- **Python 3.12+**

### Package & Environment Management
- **UV** for dependency and virtual environment management.

### AI-Native Tooling
- **Spec-Kit Plus**
  - Used for generating structured specifications from this constitution.
  - Maintains spec history and evolution.
- **Claude Code**
  - Used for AI-assisted code generation directly from specs.
  - Must adhere strictly to constraints and principles defined here.

---

## Core Principles

- **Simplicity:** In-memory, no persistence, no external services.
- **Determinism:** Same input must always produce the same output.
- **Extensibility:** Clear separation of concerns for future enhancements.
- **AI-First Design:** Specifications must be unambiguous and machine-readable.
- **User Respect:** Console interactions should feel intentional, not noisy.

---

## Constraints

- No file system storage (no JSON, SQLite, or flat files).
- No external databases or APIs.
- No GUI or web interface.
- Single-process, single-user execution.
- Must run in a standard terminal environment.

---

## Success Criteria

- All core features implemented and functional in-memory.
- Clean, readable, and modular Python code.
- Zero critical runtime errors during normal use.
- Fully spec-generatable and code-generatable using Spec-Kit Plus and Claude Code.
- Clear foundation for future persistence or UI layers without refactoring core logic.
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with specific principles and guidelines for the In-Memory Console Todo App project based on the provided requirements. The new constitution includes:

- Core Principles: Simplicity and In-Memory Operation, Deterministic and Testable Behavior, AI-First Design and Spec-Driven Development, Clean Architecture and Modularity, User-Respectful Console UX, Extensible Foundation
- Technology Stack and Constraints section
- Development Workflow and Quality Standards section
- Governance section
- Sync Impact Report documenting the changes

The constitution is now properly configured for the Todo App project with version 1.0.0.

## Outcome

- ✅ Impact: New constitution created for Todo App project with clear principles
- 🧪 Tests: No tests required for this constitution update
- 📁 Files: Updated .specify/memory/constitution.md with new constitution
- 🔁 Next prompts: Ready to proceed with spec generation using /sp.specify
- 🧠 Reflection: Constitution properly reflects the project requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate feature specification using /sp.specify