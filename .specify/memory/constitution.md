<!-- SYNC IMPACT REPORT:
Version change: N/A → 1.0.0 (initial version)
List of modified principles:
- Simplicity and In-Memory Operation (new)
- Deterministic and Testable Behavior (new)
- AI-First Design and Spec-Driven Development (new)
- Clean Architecture and Modularity (new)
- User-Respectful Console UX (new)
- Extensible Foundation (new)
Added sections: Technology Stack and Constraints, Development Workflow and Quality Standards, Governance
Removed sections: None (completely new constitution)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated (Constitution Check section will now reference new principles)
- .specify/templates/spec-template.md ✅ updated (requirements should align with new principles)
- .specify/templates/tasks-template.md ✅ updated (task categorization reflects new principles)
Follow-up TODOs: RATIFICATION_DATE needs to be set when constitution is officially adopted
-->

# In-Memory Console Todo App Constitution

## Core Principles

### Simplicity and In-Memory Operation
All data exists only during runtime in memory collections; no external databases or file persistence; single-process, single-user execution.

### Deterministic and Testable Behavior
Same input must always produce the same output; clear, unambiguous specifications that are machine-readable; strict adherence to PEP 8 standards and type hints.

### AI-First Design and Spec-Driven Development
Specifications must be unambiguous and machine-readable; designed for AI-assisted development workflows using Spec-Kit Plus and Claude Code; clear separation of concerns for extensibility.

### Clean Architecture and Modularity
Follow modular architecture with clear separation: Models (Task, enums), Services (task manager, scheduler), UI layer (console input/output); mandatory use of Python type hints and docstrings.

### User-Respectful Console UX
Console interactions should feel intentional, not noisy; prompts must be concise and consistent; output formatting must prioritize readability; no raw stack traces shown to users.

### Extensible Foundation
Clear foundation for future persistence or UI layers without refactoring core logic; designed to support all phases (MVP, Enhanced Productivity, Advanced Scheduling).

## Technology Stack and Constraints

Runtime & Language: Python 3.12+; Package & Environment Management: UV; No file system storage, external databases, GUI or web interface. The application operates entirely in memory with console-based interaction, single-process and single-user execution, running in standard terminal environments.

## Development Workflow and Quality Standards

Follow PEP 8 standards strictly; mandatory use of Python type hints and docstrings; graceful error handling with clear, human-readable messages; all core features implemented and functional in-memory. The codebase must support AI-assisted development workflows using Spec-Kit Plus and Claude Code, with clear specifications that are unambiguous and machine-readable.

## Governance

Constitution supersedes all other practices; amendments require documentation and approval; all implementations must adhere to constraints and principles defined here; must run in standard terminal environment. The constitution provides the foundational rules that guide all development decisions for the In-Memory Console Todo App project.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-28