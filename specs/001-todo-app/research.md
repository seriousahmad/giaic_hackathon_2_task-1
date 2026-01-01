# Research: In-Memory Console Todo App

## Decision: Python Console Application Architecture
**Rationale**: Based on the feature specification and constitutional principles, we'll implement a console-based todo application using Python 3.12+ with a clean architecture pattern. This approach aligns with the requirements for in-memory operation, single-user execution, and console interface.

**Alternatives considered**:
- Web-based application: Would violate the "no GUI or web components" constraint from the constitution
- GUI application: Would violate the "console interface only" requirement
- Multi-process architecture: Would violate "single-process, single-user execution" principle

## Decision: In-Memory Data Storage
**Rationale**: The constitution explicitly requires "All data exists only during runtime in memory collections; no external databases or file persistence." We'll implement a simple in-memory task collection using Python data structures (likely a dictionary with task IDs as keys).

**Alternatives considered**:
- File-based storage: Would violate the "no persistence" constraint
- Database storage: Would violate the "no external databases" constraint
- Redis/other in-memory stores: Would introduce unnecessary external dependencies

## Decision: Console UI Implementation
**Rationale**: The specification requires a "Menu-driven or command-driven interaction" with "Human-readable task listings". We'll use Python's built-in `input()` function for user interaction and `print()` for output, following the constitutional principle of "Console interactions should feel intentional, not noisy".

**Alternatives considered**:
- Third-party console libraries (like click, rich): Would introduce unnecessary dependencies when standard library suffices
- Advanced TUI frameworks: Would violate the "no GUI or web components" constraint

## Decision: Date/Time Handling
**Rationale**: For handling due dates and time, we'll use Python's built-in `datetime` module, which provides robust date/time functionality without external dependencies.

**Alternatives considered**:
- Third-party date libraries (like dateutil): Would add unnecessary dependencies
- String-based date handling: Would be less robust and harder to validate

## Decision: Task ID Generation
**Rationale**: For unique in-memory task identification, we'll use a simple incrementing integer counter that resets when the application restarts (appropriate for in-memory only application).

**Alternatives considered**:
- UUID generation: Would be overkill for an in-memory application
- Hash-based IDs: Would add unnecessary complexity

## Decision: Recurring Task Implementation
**Rationale**: Recurring tasks will be implemented using a service that creates new task instances when recurring tasks are marked complete, with updated due dates according to the recurrence pattern.

**Alternatives considered**:
- Complex scheduling libraries: Would violate the "no background schedulers" constraint
- State-based recurrence: Would be more complex to implement than creating new instances

## Decision: Testing Framework
**Rationale**: Using pytest as it's the standard Python testing framework that integrates well with type hints and provides comprehensive testing capabilities.

**Alternatives considered**:
- Built-in unittest module: pytest offers better functionality and is more widely used
- Other frameworks: Would add unnecessary complexity