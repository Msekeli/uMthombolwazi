# AI Development Guidelines

**Project:** uMthombolwazi Intelligence  
**Purpose:** Rules for AI coding assistants working in this repository.

## 1. General Rules

- Follow the approved product scope, architecture and active checkpoint.
- Make the smallest complete change that satisfies the task.
- Inspect relevant code and documentation before editing.
- Do not add features, dependencies, abstractions or infrastructure without a clear need.
- Preserve existing conventions unless there is a documented reason to change them.
- Do not invent linguistic facts, provenance, test results or validation outcomes.
- State assumptions and unresolved issues. Do not silently guess.
- Keep changes focused; avoid unrelated rewrites.

## 2. File and Folder Organisation

- Every source, configuration and documentation file must contain **100 lines or fewer**.
- Split larger files into cohesive files with distinct responsibilities; do not split artificially.
- Use meaningful file and folder names, normally no more than three words, following the repository's `snake_case` convention.
- Name files by their responsibility or content, e.g. `import_records.py`, `source_validation.py`, `search_service.py`.
- Name every folder after the responsibility or clearly defined category of the items it contains. A folder name must make its intended contents understandable without opening it.
- Keep each folder focused on one cohesive responsibility; do not use a folder as an unexplained dumping ground or create it before its purpose and contents are known.
- Use names that distinguish the folder from neighbouring folders; avoid vague names such as `stuff`, `helpers`, `common` or `data` when a precise name is possible.
- Prefer plural names for folders that hold collections, e.g. `unit_tests/` and `regression_tests/`; use singular names when the folder represents one domain or responsibility, e.g. `lexicon/`.
- Apply the same naming rules to nested folders. Their names should communicate their role within the parent context.
- Preserve framework-required names and standard conventions, even when they differ from the project's preferred naming style.
- Avoid one-word names unless a standard convention or genuine technical need requires one.
- Preserve standard names such as `.env`, `.gitignore`, `README.md` and `pyproject.toml`.
- Follow the repository's established casing and separator convention consistently.
- Test files should identify the component or behaviour being tested.
- Do not create empty folders merely to anticipate possible future work; retain only approved structural placeholders that are part of the agreed architecture.

## 3. SOLID Principles

Aim to apply SOLID when it improves maintainability, testability and separation of responsibilities.

- **Single Responsibility:** Give each module, class and function one clear responsibility.
- **Open/Closed:** Allow stable behaviour to be extended where genuine variation is expected.
- **Liskov Substitution:** Keep implementations interchangeable when substitutable contracts or inheritance are used.
- **Interface Segregation:** Keep interfaces focused on the needs of their consumers.
- **Dependency Inversion:** Keep important application logic independent of concrete infrastructure where useful.

SOLID is a design guide, not a compliance checklist. Do not create interfaces for every class, add abstraction layers without a use case, introduce inheritance where composition or a function is clearer, or add factories/repositories/wrappers by default. Do not make simple code harder merely to demonstrate a principle. Prefer the simplest testable design. If a principle would add disproportionate complexity, choose the simpler design and explain material trade-offs.

## 4. Backend Architecture Boundaries

- Keep the backend a modular monolith; do not introduce microservices without approval.
- Use the agreed pragmatic structure: routers, services, SQLAlchemy models and Pydantic schemas.
- Keep HTTP handling in routers, application behaviour in services and persistence in the data-access layer.
- Do not duplicate domain/entity layers unless real complexity justifies them.
- Keep the Python data-engineering pipeline separate from the FastAPI application.
- Start with `lexicon`, `sources` and `search`; add modules only for genuine responsibilities.
- PostgreSQL is the authoritative knowledge store.

## 5. Data and Linguistic Integrity

- Preserve original source text and identifiers.
- Store canonical text in Unicode NFC; keep search-normalised text separate.
- Preserve isiXhosa click letters and meaningful orthographic distinctions.
- Never invent missing glosses, examples, grammatical labels, dialects or meanings.
- Keep assertion origin separate from review status; review each assertion independently.
- Preserve source, source version, import batch and transformation provenance.
- Do not silently merge uncertain duplicates or present unvalidated lemma guesses as facts.
- Structural validation is not linguistic verification.
- A successful import does not make imported data verified.

## 6. Implementation and Testing

- Work against the active checkpoint and its acceptance criteria; complete one meaningful ticket at a time.
- Add or update tests with the implementation.
- Use unit tests for isolated logic, PostgreSQL integration tests for persistence, API tests for contracts and permissions, and fixtures for pipeline tests.
- Add regression tests when fixing defects.
- Never claim tests passed unless they were actually run.
- Do not weaken or remove tests merely to make a change pass.
- Update relevant Markdown documentation when behaviour, setup or architecture changes.

## 7. Change Discipline

Before editing, identify relevant files, conventions, checkpoint requirements and effects on migrations, API contracts, provenance, security or existing data. After editing, review the full diff, check names and line limits, run relevant formatting/lint/type/test commands, and report changes, tests run and unresolved issues.

## 8. Conflict Resolution

Apply instructions in this order: (1) explicit task requirements and user decisions; (2) approved architecture and documented data/licensing constraints; (3) these guidelines; (4) compatible local conventions; (5) AI defaults. Do not silently change agreed scope or architecture. Ask for direction when a conflict materially affects the product, data integrity, security or future compatibility.
