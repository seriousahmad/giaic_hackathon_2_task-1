---
description: "Task list for In-Memory Console Todo App implementation"
---

# Tasks: In-Memory Console Todo App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Create src directory structure (models, services, cli, lib)
- [X] T003 [P] Create tests directory structure (unit, integration, contract)
- [X] T004 Initialize requirements.txt with pytest for testing

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 Create Task model in src/models/task.py with all required attributes (id, title, description, completed, priority, tags, due_date, recurrence, created_at, updated_at)
- [X] T006 [P] Create Priority and Recurrence enums in src/models/__init__.py
- [X] T007 Create TaskManager service in src/services/task_manager.py with in-memory storage (dict[int, Task])
- [X] T008 Create utils module in src/lib/utils.py with date/time handling functions
- [X] T009 [P] Implement error handling classes in src/lib/errors.py (TaskNotFound, ValidationError)
- [X] T010 [P] Set up basic CLI structure in src/cli/console_ui.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, and delete tasks in a console-based application - the core functionality that enables all other features.

**Independent Test**: Can be fully tested by adding a task, viewing it, updating its properties, and deleting it from the console interface, delivering the fundamental todo management capability.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [X] T012 [P] [US1] Unit test for TaskManager CRUD operations in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [X] T013 [P] [US1] Implement Task model with validation rules from data-model.md in src/models/task.py
- [X] T014 [US1] Implement TaskManager CRUD methods (add_task, get_task, update_task, delete_task) in src/services/task_manager.py
- [X] T015 [US1] Implement console UI for task creation in src/cli/console_ui.py
- [X] T016 [US1] Implement console UI for task viewing in src/cli/console_ui.py
- [X] T017 [US1] Implement console UI for task updating in src/cli/console_ui.py
- [X] T018 [US1] Implement console UI for task deletion with confirmation in src/cli/console_ui.py
- [X] T019 [US1] Add error handling for non-existent tasks in src/lib/errors.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Task Completion and Prioritization (Priority: P2)

**Goal**: Enable users to mark tasks as complete and manage priorities and tags to organize their work effectively.

**Independent Test**: Can be fully tested by toggling task completion status and assigning different priority levels and tags, delivering task organization and progress tracking capabilities.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T020 [P] [US2] Unit test for toggle_completion functionality in tests/unit/test_task_manager.py
- [X] T021 [P] [US2] Unit test for priority and tag assignment in tests/unit/test_task.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Implement toggle_completion method in src/services/task_manager.py
- [X] T023 [US2] Implement priority validation and assignment in src/models/task.py
- [X] T024 [US2] Implement tag management functionality in src/models/task.py
- [X] T025 [US2] Add console UI for toggling task completion status in src/cli/console_ui.py
- [X] T026 [US2] Add console UI for modifying priorities and tags in src/cli/console_ui.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Search, Filter, and Sort Tasks (Priority: P3)

**Goal**: Enable users to find specific tasks and organize them by various criteria to efficiently manage their workload.

**Independent Test**: Can be fully tested by searching for tasks by keyword, applying various filters (status, priority, tags, due date), and sorting tasks by different criteria, delivering efficient task discovery and organization capabilities.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T027 [P] [US3] Unit test for search functionality in tests/unit/test_task_manager.py
- [X] T028 [P] [US3] Unit test for filter functionality in tests/unit/test_task_manager.py
- [X] T029 [P] [US3] Unit test for sort functionality in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [X] T030 [P] [US3] Implement search_tasks method in src/services/task_manager.py
- [X] T031 [US3] Implement filter_tasks method in src/services/task_manager.py
- [X] T032 [US3] Implement sort_tasks method in src/services/task_manager.py
- [X] T033 [US3] Implement recurring task service in src/services/recurring_service.py
- [X] T034 [US3] Add console UI for search functionality in src/cli/console_ui.py
- [X] T035 [US3] Add console UI for filter and sort functionality in src/cli/console_ui.py
- [X] T036 [US3] Integrate recurring task handling with task completion in src/services/task_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T037 [P] Add console-based reminder checks for due and overdue tasks in src/services/task_manager.py
- [X] T038 [P] Add input validation and graceful error handling throughout the application
- [X] T039 [P] Improve console UI formatting and readability
- [X] T040 [P] Add type hints to all functions and methods across all modules
- [X] T041 [P] Add docstrings to all public classes and functions
- [X] T042 [P] Add menu-driven or command-driven interaction in src/cli/console_ui.py
- [X] T043 Run quickstart.md validation to ensure all functionality works as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Unit test for TaskManager CRUD operations in tests/unit/test_task_manager.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation rules from data-model.md in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence