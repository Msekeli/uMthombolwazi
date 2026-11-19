# Agent Instructions

## Project Context

This repository contains **uMthombolwazi Intelligence**, an isiXhosa linguistic knowledge and intelligence platform. The platform's priority is accurate, traceable and context-aware linguistic knowledge.

Read `AI_DEVELOPMENT_GUIDELINES.md` before making changes. These instructions apply to all AI agents and coding assistants working in this repository.

## Working Rules

- Follow the approved product scope, architecture and current delivery checkpoint.
- Work only on the task requested. Do not expand scope without approval.
- Inspect the relevant code, tests and documentation before editing.
- Prefer small, focused changes that leave the project in a working state.
- Do not invent linguistic content, source details, provenance or test results.
- Preserve existing conventions unless they conflict with an explicit project decision.
- Ask before making a decision that materially changes architecture, data semantics, security or licensing.

## Architecture

- The backend is a Python/FastAPI modular monolith.
- PostgreSQL is the authoritative knowledge store.
- The data-engineering pipeline is a separate Python workspace.
- Use the agreed pragmatic code structure: routers, services, SQLAlchemy models and Pydantic schemas.
- Initial backend modules are `lexicon`, `sources` and `search`.
- Do not introduce microservices or unnecessary abstraction layers.
- Apply SOLID principles where they improve maintainability and testability; do not force patterns where they add complexity.

## Data Integrity

- Preserve original source text, identifiers and provenance.
- Keep source, source version and import batch distinguishable.
- Keep assertion origin separate from assertion review status.
- Review status applies to individual assertions, not automatically to an entire lexical entry.
- Do not promote staging data without validation and controlled promotion.
- Do not silently merge uncertain duplicates.
- Do not present unvalidated lemma mappings or generated linguistic content as verified facts.
- Structural validation does not establish linguistic correctness.

## Repository Organisation

- Keep each file at 100 lines or fewer.
- Split larger files by cohesive responsibility, not arbitrarily.
- Use meaningful file and folder names, normally no more than three words.
- Prefer plural names for collections, such as `unit tests` and `regression tests`.
- Preserve standard filenames and framework-required conventions.
- See `AI_DEVELOPMENT_GUIDELINES.md` for the complete naming and design rules.

## Implementation Workflow

1. Identify the active checkpoint and ticket, if one applies.
2. Read the ticket's tasks and acceptance criteria.
3. Inspect the smallest relevant part of the codebase.
4. Implement the minimum complete change.
5. Add or update tests for the changed behaviour.
6. Run relevant tests and quality checks.
7. Review the diff for unrelated changes and line-limit violations.
8. Summarise files changed, checks run, results and unresolved issues.

Do not claim that a command or test passed unless you ran it and observed the result. If a check cannot be run, state why.

## Documentation

- Project documentation is Markdown (`.md`) only unless the user explicitly requests another format.
- Update relevant documentation when implementation changes affect setup, behaviour, architecture or operational procedures.
- Keep documentation concise, accurate and within the 100-line limit.
- Do not create duplicate or conflicting sources of truth.

## Instruction Priority

When instructions conflict, follow this order:

1. Explicit user instructions for the current task.
2. Approved project decisions and architecture documents.
3. `AI_DEVELOPMENT_GUIDELINES.md`.
4. Existing repository conventions that do not conflict with the above.
5. General AI coding preferences.

Do not silently override a higher-priority instruction. Explain material conflicts and request clarification when needed.
