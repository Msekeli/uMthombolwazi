# uMthombolwazi Intelligence
## Backend V1 — Checkpoint and Ticket Delivery Plan

**Version:** 1.0  
**Status:** Proposed execution baseline  
**Date:** 19 November 2026  
**Scope:** Backend and data-engineering work only

---

## 1. Purpose

This document turns the agreed V1 backend architecture into an executable sequence of checkpoints and tickets. Each checkpoint must leave behind a working, testable capability. We should not move to the next checkpoint merely because files have been created; the stated exit criteria must pass.

This is a delivery plan, not a list of technologies to install. Tickets are deliberately small enough to implement, review and test independently, while each checkpoint produces a meaningful outcome.

## 2. Backend V1 outcome

At completion, the backend will provide:

1. A deployable FastAPI modular monolith.
2. A PostgreSQL knowledge store with lexical records, senses, glosses, forms and usage examples where supported by evidence.
3. Traceable source, source-version and import-batch provenance.
4. Assertion-level review states and an append-only review history.
5. A repeatable Python data pipeline that acquires permitted datasets, preserves raw inputs, profiles and transforms them, loads staging data and promotes validated records.
6. An online read API for lexical search, entry details, related forms and source metadata.
7. A protected correction and review workflow if the V1 admin scope is completed.
8. Automated tests, operational logging, configuration, deployment and backup procedures.
9. Optionally, a versioned SQLite export job if data licensing and quality gates pass.

The backend must not invent missing linguistic information. Missing fields remain missing and are represented honestly by the API.

## 3. Scope boundaries

### Included

- Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL and pytest.
- A modular monolith, not microservices.
- Initial backend modules: `lexicon`, `sources`, `search`.
- A separate Python data-engineering workspace.
- `lexicon` and `provenance` application schemas, plus a separately managed `staging` schema.
- Read endpoints and a minimal protected write/review workflow.
- Data validation, provenance, licensing metadata and controlled promotion.
- Backend security, testing, deployment and operational readiness.

### Excluded from this backend V1

- React Native, Expo, web UI and client-side state.
- AI chatbot, tutor, writing assistant or content studio.
- Story, social-media, image or video generation.
- Speech recognition and text-to-speech.
- Production machine translation, model training or fine-tuning.
- Semantic/vector search.
- Public API monetisation, subscriptions or developer portal.
- Microservices, event streaming or premature distributed infrastructure.
- Full user identity, social profiles or cross-device synchronisation unless a real V1 requirement is approved.

## 4. Delivery rules

1. **Checkpoint-based:** Each checkpoint has a demonstrable outcome and exit criteria.
2. **Ticket-based:** A ticket is complete only when its acceptance criteria and tests pass.
3. **Evidence before schema:** Dataset profiling and linguistic conventions must inform the canonical schema. Do not finalise the full data model before inspecting real candidate sources.
4. **No silent data promotion:** Imported data enters staging first. Only validated data is promoted.
5. **Provenance by design:** Every imported or derived assertion must be traceable to its source version and import batch.
6. **Review is assertion-level:** A reviewed gloss does not automatically verify every other fact in the lexical entry.
7. **Preserve raw inputs:** Raw source files are immutable. Transformations create new outputs.
8. **No false confidence:** Imported, derived, manual and user-submitted origins are distinct from verified, unreviewed, disputed and rejected review states.
9. **Keep the monolith simple:** Routers, services, SQLAlchemy models and Pydantic schemas are sufficient. Do not add layers without a concrete reason.
10. **Tests are part of the ticket:** Do not defer all testing to a final phase.

## 5. Checkpoint map

| Checkpoint | Outcome | Exit condition |
|---|---|---|
| CP0 — Backend workspace | Reproducible local backend and pipeline workspace | A clean clone can install, configure and run the health endpoint and test suite |
| CP1 — Dataset intelligence | Evidence-based source and dataset assessment | Candidate sources, licences, formats, quality and linguistic conventions are documented |
| CP2 — Canonical knowledge model | Approved, evidence-informed schema | Model decisions and relationships are validated against representative source records |
| CP3 — Database foundation | Versioned PostgreSQL schema | Migrations create the database cleanly and integrity tests pass |
| CP4 — Data pipeline foundation | Repeatable raw-to-staging pipeline | One approved dataset can be acquired, checksummed, profiled and loaded into staging |
| CP5 — First controlled ingestion | Trusted, traceable records in production tables | A complete import batch can be promoted, audited and safely re-run or rolled back |
| CP6 — Lexicon read API | Reliable lexical entry retrieval | API returns entries, senses, glosses, forms and provenance with contract tests |
| CP7 — Search API | Useful isiXhosa and English lookup | Exact, prefix/partial, gloss and supported form lookup pass the search evaluation set |
| CP8 — Review and correction workflow | Protected knowledge maintenance | Corrections can be submitted, reviewed and audited without overwriting accepted facts |
| CP9 — Production readiness | Deployable, observable and recoverable backend | Security, deployment, backup/restore and operational checks pass |
| CP10 — Optional offline export | Versioned read-only SQLite knowledge pack | Pack passes licence, content, integrity and search validation gates |

CP10 is optional and must not block the online backend release.

---

# 6. Detailed checkpoint tickets

## CP0 — Backend workspace and developer foundation

**Checkpoint outcome:** A clean, reproducible backend workspace exists. The application starts locally, connects to a development database and exposes a health endpoint. The data pipeline has its own isolated workspace.

### BE-001 — Create backend project skeleton
**Tasks**
- Create the `backend/` Python project.
- Add `pyproject.toml` and pin compatible dependency ranges.
- Add the FastAPI application entry point.
- Create `core/`, `modules/`, `shared/` and `tests/` directories.
- Create only the initial module folders: `lexicon`, `sources`, `search`.

**Acceptance criteria**
- The application starts through a documented command.
- Importing the application has no database side effects.
- No frontend code is placed in the backend project.
- The module structure matches the agreed modular-monolith approach.

### BE-002 — Configure local development environment
**Tasks**
- Add Docker Compose for PostgreSQL.
- Add `.env.example` with non-secret placeholders.
- Implement typed settings/configuration.
- Separate development and test configuration.
- Ensure secrets and local environment files are ignored by Git.

**Acceptance criteria**
- A developer can start PostgreSQL with one documented command.
- The backend reads configuration from environment variables.
- Missing required configuration fails clearly.
- No credentials are committed.

### BE-003 — Add health and readiness endpoints
**Tasks**
- Add `/api/v1/health`.
- Add a database readiness check separately from process liveness.
- Return stable response schemas and appropriate status codes.

**Acceptance criteria**
- Liveness works without a database connection.
- Readiness reports database availability accurately.
- Failure responses do not expose secrets or connection strings.

### BE-004 — Establish quality automation
**Tasks**
- Configure pytest.
- Add formatting, linting and type-checking tools appropriate to the project.
- Add a basic CI workflow to install dependencies and run checks.
- Document local commands.

**Acceptance criteria**
- Tests and static checks run from a clean environment.
- CI fails when a check fails.
- A clean clone can reproduce the checks using the documentation.

### BE-005 — Create the data-engineering workspace
**Tasks**
- Create a separate `data-engineering/` Python workspace.
- Add the planned pipeline packages: `registry`, `acquisition`, `inspection`, `transformation`, `reconciliation`, `validation`, `ingestion`, `reporting`.
- Create `datasets/raw`, `datasets/staging` and `datasets/processed` conventions.
- Add ignore rules so large/private raw datasets are not accidentally committed.

**Acceptance criteria**
- Pipeline dependencies are isolated from API dependencies where practical.
- Raw, staging and processed data have distinct locations.
- The pipeline can run a basic command and produce a report.

**CP0 exit gate**
- Backend starts locally.
- PostgreSQL starts locally.
- Health/readiness endpoints work.
- CI runs tests and checks.
- Pipeline workspace runs independently.
- Setup instructions work from a clean clone.

---

## CP1 — Dataset intelligence and acquisition decisions

**Checkpoint outcome:** The team knows what data is actually available, what it contains, what it permits and what it can safely contribute. No bulk ingestion begins before this checkpoint passes.

### DATA-001 — Build the resource registry
**Tasks**
- Define a machine-readable registry format.
- Capture resource name, publisher, URL or access route, version/release, acquisition date, file format, language, intended use, licence, attribution requirements, restrictions and known limitations.
- Record whether the resource is downloadable, request-only, API-based or reference-only.

**Acceptance criteria**
- Every candidate dataset has a registry record.
- Unknown licence or access terms are explicitly marked unresolved.
- No resource is marked approved merely because it is publicly accessible.

### DATA-002 — Verify licensing and permitted use
**Tasks**
- Inspect the licence attached to the exact resource version.
- Distinguish dataset licence from software licence and website terms.
- Record attribution, share-alike, non-commercial, redistribution and derivative-work obligations.
- Identify third-party content embedded in a resource.

**Acceptance criteria**
- Each resource has a documented use decision: approved, conditional, reference-only or rejected.
- Unresolved rights block ingestion and redistribution.
- Offline-pack eligibility is recorded separately from internal research eligibility.

### DATA-003 — Acquire and preserve candidate source files
**Tasks**
- Acquire only resources with a permitted access route.
- Preserve original files unchanged.
- Record source URL/access route, date, version and file metadata.
- Calculate SHA-256 checksums.
- Store acquisition logs.

**Acceptance criteria**
- Raw files are never overwritten by transformed output.
- Every acquired file is linked to a resource and version.
- Re-acquiring a changed file produces a new version/checksum record.

### DATA-004 — Inspect formats, encodings and structure
**Tasks**
- Identify file types and compression.
- Inspect encodings and Unicode handling.
- Identify fields, identifiers, row/record counts and nested structures.
- Detect malformed rows, truncation and parsing issues.
- Preserve source identifiers.

**Acceptance criteria**
- Each source has a reproducible inspection report.
- Parsing does not silently discard malformed records.
- Encoding issues and assumptions are documented.

### DATA-005 — Profile data quality
**Tasks**
- Measure nulls, duplicates, field distributions and record counts.
- Inspect language labels and mixed-language content.
- Profile headwords, senses, glosses, parts of speech, examples and morphology fields where present.
- Identify likely duplicates without merging them.
- Record corpus quality limitations and annotation status.

**Acceptance criteria**
- A profile report exists for each candidate dataset.
- Quality observations are based on actual sample and count evidence.
- Suspected duplicates are candidates for reconciliation, not automatically deleted.

### DATA-006 — Document linguistic conventions and compatibility
**Tasks**
- Determine how each resource represents headwords, roots, stems, lemmas, word forms, senses and parts of speech.
- Record tokenisation, orthography, dialect/register labels and annotation conventions.
- Determine whether identifiers and fields can be mapped across resources.
- Identify where two resources use similar labels with different meanings.

**Acceptance criteria**
- A source-convention document exists.
- Incompatible concepts are not force-mapped.
- Uncertain mappings are explicitly listed for later review.

### DATA-007 — Evaluate lemma resource on held-out examples
**Tasks**
- Select a 50-token evaluation set with a development/held-out split.
- Define what counts as a correct lemma, how ambiguity is scored and how coverage is measured.
- Set the numerical acceptance threshold before examining held-out results.
- Evaluate the candidate lemma resource/tool without tuning against the held-out set.
- Record errors and limitations.

**Acceptance criteria**
- The threshold and scoring protocol are timestamped before evaluation.
- Held-out examples are not used for tuning.
- The report records accuracy, coverage and error categories.
- If performance is insufficient, output is treated only as candidate suggestions, not authoritative lemma mappings.

### DATA-008 — Approve the V1 source set
**Tasks**
- Compare candidate resources by relevance, rights, quality, compatibility and acquisition burden.
- Select a small first ingestion set.
- Identify resources that remain reference-only or deferred.
- Record why each source was selected or excluded.

**Acceptance criteria**
- V1 source set is explicitly approved.
- Every approved source has a licence/use decision and profile report.
- No schema or import ticket depends on an unapproved resource.

**CP1 exit gate**
- Source registry complete for candidates.
- Licence decisions documented.
- Raw files and checksums preserved.
- Data profiles and linguistic conventions documented.
- Lemma evaluation completed or formally deferred with a reason.
- Initial V1 source set approved.

---

## CP2 — Canonical linguistic knowledge model

**Checkpoint outcome:** The backend has a defensible data model based on the source evidence. This checkpoint produces the schema specification before implementation.

### MODEL-001 — Define canonical lexical concepts
**Tasks**
- Define lexical entry/lemma identity.
- Define lexical sense as a distinct meaning assertion.
- Define sense-level English glosses.
- Define word forms and form-to-lemma relationships.
- Define usage examples and contextual metadata where source evidence supports them.
- Define part-of-speech and grammatical metadata strategy.

**Acceptance criteria**
- A glossary of model concepts exists.
- Entry, sense, gloss and form are not collapsed into one flat dictionary record.
- Multiple senses and multiple glosses are representable.
- A form is not automatically treated as a separate lexical entry.

### MODEL-002 — Define linguistic context fields
**Tasks**
- Decide how dialect/variety, register, domain, era and geographic/contextual labels are represented.
- Define whether labels attach to senses, forms, examples or source assertions.
- Define how unknown or unspecified values are represented.
- Model ideophones and other special lexical categories without forcing them into unsuitable assumptions.
- Define how code-switching examples are represented if required by selected sources.

**Acceptance criteria**
- Context labels have documented semantics.
- The model does not imply a universal dialect/register when none is known.
- Unsupported context is omitted rather than guessed.

### MODEL-003 — Define equivalence and relationship semantics
**Tasks**
- Distinguish direct translation equivalent, approximate equivalent, contextual equivalent, synonym, related form, cognate, false friend, borrowing and avoidance/ukuhlonipha substitution where applicable.
- Decide which relationships are required for V1 and which are deferred.
- Ensure English glosses do not imply one-to-one equivalence.

**Acceptance criteria**
- Relationship types have precise definitions.
- V1 only implements relationship types supported by actual source evidence.
- Contextual and approximate equivalents cannot be mistaken for exact synonyms.

### MODEL-004 — Define assertion origin and review state
**Tasks**
- Define `origin_method`: `imported`, `derived`, `manual`, `user_submitted`.
- Define `review_status`: `unreviewed`, `verified`, `disputed`, `rejected`.
- Apply review independently to each assertion.
- Define permitted state transitions and who can perform them.

**Acceptance criteria**
- Origin and review are separate fields/concepts.
- An entry does not receive a blanket verified status.
- State transitions are documented and testable.

### MODEL-005 — Define provenance and contributor model
**Tasks**
- Define `source`, `source_version`, `import_batch` and minimal `contributor`.
- Define source relationships for each assertion.
- Use typed nullable foreign keys for known assertion tables in the shared source-evidence relationship, with a database check that exactly one target is populated.
- Define relationship types: `direct_source`, `supporting_evidence`, `derived_from`, `contradicting_evidence`.
- Define append-only review events with typed assertion references.
- Define content revision history so old assertion content can be reconstructed.

**Acceptance criteria**
- Every imported assertion can be traced to source version and import batch.
- Multiple sources can support or contradict one assertion.
- Review history records actor, prior state, new state, reason and timestamp.
- Content changes preserve the previous content, not just the status transition.

### MODEL-006 — Define identity, deduplication and normalisation
**Tasks**
- Define stable identifiers for entries, senses, forms and assertions.
- Use UUIDv7 where supported, with application generation fallback.
- Define Unicode NFC canonical storage.
- Preserve original source strings and separate search-normalised values.
- Define candidate duplicate matching stages: normalised form, morphology/POS compatibility, sense/context comparison and human review.
- Define how uncertain duplicates remain separate.

**Acceptance criteria**
- No destructive prefix stripping or automatic merge is used as the identity strategy.
- Original text is preserved.
- Normalisation and deduplication rules have test examples.

### MODEL-007 — Produce and review schema specification
**Tasks**
- Draw entity relationships.
- Specify columns, types, nullability, constraints and indexes.
- Identify which fields are source facts versus platform-generated metadata.
- Map representative records from each approved source into the proposed model.
- Record unresolved modelling decisions.

**Acceptance criteria**
- Schema specification is reviewed before Alembic implementation.
- Representative source records can be expressed without losing important distinctions.
- Unresolved decisions are explicit and do not silently become assumptions.

**CP2 exit gate**
- Approved entity relationship model.
- Data dictionary and controlled vocabularies.
- Provenance and review semantics defined.
- Representative source-to-model mappings reviewed.
- No unresolved critical modelling question blocks implementation.

---

## CP3 — PostgreSQL schema and persistence foundation

**Checkpoint outcome:** The canonical model exists as a migrated PostgreSQL database with enforceable integrity.

### DB-001 — Configure SQLAlchemy and database sessions
**Tasks**
- Configure SQLAlchemy engine and session lifecycle.
- Provide dependency injection for request-scoped sessions.
- Configure test database sessions and transaction rollback strategy.
- Keep connection settings in central configuration.

**Acceptance criteria**
- API requests receive correctly scoped sessions.
- Tests do not leak state between cases.
- Database connection failures are handled safely.

### DB-002 — Configure Alembic migrations
**Tasks**
- Initialise Alembic.
- Connect metadata and environment configuration.
- Separate application schema migrations from staging schema management.
- Document migration generation, review and application.

**Acceptance criteria**
- A new database can be created from migrations.
- Migrations are committed and reproducible.
- Autogenerated migrations are reviewed, not accepted blindly.

### DB-003 — Implement lexicon tables
**Tasks**
- Implement the approved entry, sense, gloss, form, form-lemma and example structures.
- Add required foreign keys and uniqueness constraints.
- Add controlled vocabulary constraints or reference tables as chosen in CP2.
- Preserve source identifiers where required.

**Acceptance criteria**
- Database constraints prevent invalid relationships.
- Multiple senses/glosses are supported.
- Form-to-lemma mappings can represent ambiguity if evidence requires it.
- Optional data can be absent without fabricating placeholders.

### DB-004 — Implement provenance tables
**Tasks**
- Implement source, source_version, import_batch and contributor.
- Implement assertion-to-source links with typed foreign keys and exactly-one-target checks.
- Implement append-only review events.
- Implement content revision history.

**Acceptance criteria**
- Provenance references are enforced by actual foreign keys.
- A source version cannot be confused with the abstract source.
- Review and content history are queryable.
- Application roles cannot silently rewrite historical event records.

### DB-005 — Implement constraints and indexes
**Tasks**
- Add required check constraints, unique constraints and indexes.
- Add indexes for foreign keys and common retrieval paths.
- Add text and normalised search columns needed by the approved search design.
- Evaluate PostgreSQL extensions such as `pg_trgm` only when justified by search tests.

**Acceptance criteria**
- Constraints reject invalid data in integration tests.
- Indexes support known API access patterns.
- Extensions are documented and enabled reproducibly.

### DB-006 — Establish database roles and permissions
**Tasks**
- Define least-privilege roles for application reads, controlled writes, pipeline staging and migrations.
- Separate migration privileges from runtime API credentials.
- Prevent public request paths from using broad database permissions.

**Acceptance criteria**
- Runtime API credentials cannot perform schema changes.
- Pipeline permissions are limited to required staging/promotion operations.
- Permission tests verify intended boundaries.

### DB-007 — Add database integrity test suite
**Tasks**
- Test foreign keys, check constraints, unique rules and review-state constraints.
- Test provenance linkage.
- Test append-only audit behaviour.
- Test migration upgrade from an empty database.

**Acceptance criteria**
- All critical integrity rules have automated tests.
- Migration tests pass against a clean PostgreSQL instance.
- CP3 schema is reproducible.

**CP3 exit gate**
- PostgreSQL schema created by migrations.
- ORM persistence works.
- Integrity constraints and permissions tested.
- Database can be rebuilt from scratch.

---

## CP4 — Data pipeline foundation: raw to staging

**Checkpoint outcome:** A permitted dataset can be processed repeatably into staging without changing or losing the original source.

### PIPE-001 — Define pipeline run and batch metadata
**Tasks**
- Define a run manifest with source version, checksum, pipeline version/commit, start/end times and status.
- Generate a unique import batch.
- Record input and output counts and error counts.

**Acceptance criteria**
- Every run has a reproducible manifest.
- Failed runs remain visible and are not represented as successful imports.
- Batch identifiers flow through all pipeline stages.

### PIPE-002 — Implement source acquisition adapters
**Tasks**
- Implement only the acquisition mechanisms required by approved V1 sources.
- Support local file input as the reliable baseline.
- Add remote download/API support only where terms and source behaviour permit.
- Validate file checksums and expected file metadata.

**Acceptance criteria**
- Acquisition never overwrites an existing raw file.
- A changed source file creates a new immutable version.
- Access failures and checksum mismatches fail clearly.

### PIPE-003 — Implement inspection and profiling reports
**Tasks**
- Produce format, encoding, structure and data-quality reports.
- Record parsing errors and malformed records.
- Add source-specific profile adapters where needed.

**Acceptance criteria**
- Reports can be regenerated from the same raw file.
- Counts reconcile between input and parsed output.
- Data loss is not silently hidden.

### PIPE-004 — Implement source-specific transformations
**Tasks**
- Map source records into intermediate canonical staging structures.
- Preserve source record IDs and original strings.
- Preserve source-specific fields that do not yet map cleanly.
- Record every transformation rule and version.

**Acceptance criteria**
- Transformations are deterministic for a fixed input and pipeline version.
- Unmapped fields are reported, not discarded.
- Original values remain recoverable.

### PIPE-005 — Implement validation rules
**Tasks**
- Validate required identifiers and fields.
- Validate language labels and expected content types.
- Validate relationships and references within the source.
- Check Unicode normalisation without replacing original text.
- Detect duplicates and anomalies for review.
- Separate structural validation from linguistic validation.

**Acceptance criteria**
- Invalid rows are quarantined with reason codes.
- Warnings and errors are distinguished.
- Structural validity is not described as linguistic correctness.

### PIPE-006 — Load into PostgreSQL staging
**Tasks**
- Create staging tables managed separately from application Alembic metadata.
- Bulk load transformed records.
- Record batch ID and source version on staging rows.
- Make staging loads idempotent per batch.

**Acceptance criteria**
- A staging load can be repeated without duplicate rows for the same batch.
- Staging data is isolated from public API reads.
- Batch-level row counts reconcile.

### PIPE-007 — Generate pipeline reports
**Tasks**
- Report acquired, parsed, accepted, rejected and quarantined counts.
- Report duplicates, missing values, unmapped fields and validation failures.
- Include source, version, checksum, batch and pipeline commit.

**Acceptance criteria**
- Every run produces a human-readable report and machine-readable summary.
- A reviewer can decide whether to proceed to promotion from the report alone.

**CP4 exit gate**
- At least one approved source completes raw-to-staging.
- Raw source is unchanged.
- Pipeline is repeatable and idempotent.
- Validation and reconciliation reports are produced.

---

## CP5 — Controlled ingestion and knowledge promotion

**Checkpoint outcome:** Validated staging data can be promoted into authoritative lexicon/provenance tables with a traceable and recoverable import.

### ING-001 — Define promotion rules per source
**Tasks**
- Map staging records to canonical entries, senses, glosses, forms and examples.
- Define create/update/skip/conflict behaviour.
- Define matching rules and duplicate candidate handling.
- Define which assertions are imported versus derived.
- Assign initial review status according to source policy; do not mark imported data verified by default.

**Acceptance criteria**
- Promotion rules are documented and version controlled.
- Ambiguous matches are held for review.
- No destructive merge occurs automatically.

### ING-002 — Implement transactional promotion
**Tasks**
- Implement controlled promotion scripts/services.
- Link created assertions to source version and import batch.
- Use database transactions or bounded, resumable batches with clear recovery semantics.
- Record promotion outcome and counts.

**Acceptance criteria**
- A failed promotion does not leave an undocumented partial state.
- Every promoted assertion has provenance.
- Re-running a completed batch does not duplicate its records.

### ING-003 — Implement conflict and reconciliation queue
**Tasks**
- Record possible duplicates and conflicting source assertions.
- Preserve competing source values and their evidence.
- Provide a report for manual resolution.
- Do not select a winner solely by source authority label.

**Acceptance criteria**
- Conflicts remain visible and traceable.
- The system can represent multiple claims/evidence for a concept.
- Human resolution is recorded as a new auditable action.

### ING-004 — Implement import rollback/reversal procedure
**Tasks**
- Define how a batch is withdrawn or reversed.
- Preserve audit history and original source data.
- Prevent rollback from deleting records that have since been independently edited or referenced without explicit reconciliation.
- Document recovery steps.

**Acceptance criteria**
- A test batch can be safely reversed.
- Rollback does not erase provenance or review history.
- Reversal is logged and attributable.

### ING-005 — Validate promoted knowledge
**Tasks**
- Compare staging counts with promoted counts.
- Check all foreign keys and provenance links.
- Sample records against original source records.
- Run linguistic sanity checks and reviewer sampling.
- Produce a promotion report.

**Acceptance criteria**
- Count differences are explained.
- Sampled records can be traced back to raw source records.
- No source is considered linguistically verified solely because it passed structural validation.

**CP5 exit gate**
- One approved dataset is promoted end-to-end.
- Import is traceable, repeatable and reversible.
- Conflicts and uncertain mappings are preserved.
- Promoted data passes integrity and sample review.

---

## CP6 — Lexicon read API

**Checkpoint outcome:** Clients can retrieve lexical records through stable, documented API contracts.

### API-001 — Define API response contracts
**Tasks**
- Define response schemas for lexical entry, sense, gloss, form, example and provenance summary.
- Define pagination conventions where collections may grow.
- Define not-found and validation error formats.
- Define how unavailable fields and review states are represented.

**Acceptance criteria**
- Contracts distinguish entry-level data from sense-level data.
- API never fabricates absent glosses, examples or grammatical labels.
- Response schemas are documented and tested.

### API-002 — Implement lexical entry retrieval
**Tasks**
- Implement `GET /api/v1/lexicon/{entry_id}`.
- Retrieve entry and related senses, glosses and available grammatical metadata.
- Include review/origin labels at assertion level.

**Acceptance criteria**
- A known entry returns its available information.
- Missing or invalid identifiers return appropriate status codes.
- Assertion-level status is not collapsed into one entry-level confidence flag.

### API-003 — Implement related forms and lemma relationships
**Tasks**
- Implement `GET /api/v1/lexicon/{entry_id}/related`.
- Return only supported, stored form-to-lemma relationships.
- Preserve ambiguous mappings where the data model permits them.

**Acceptance criteria**
- The endpoint does not infer forms by blindly stripping prefixes.
- Unsupported relationships are omitted.
- Each returned relationship carries its available origin/review metadata.

### API-004 — Implement source metadata read endpoint
**Tasks**
- Implement `GET /api/v1/sources`.
- Return approved public source metadata and attribution/licence details.
- Avoid exposing internal credentials, private acquisition paths or restricted metadata.

**Acceptance criteria**
- Public source attribution is accurate.
- Restricted source details are not leaked.
- Source versions can be distinguished.

### API-005 — Add API pagination, filtering and error handling
**Tasks**
- Apply consistent pagination to potentially large result sets.
- Validate query/path parameters.
- Add request IDs and structured error responses.
- Avoid returning raw database errors.

**Acceptance criteria**
- API behaviour is consistent across endpoints.
- Error responses are safe and predictable.
- Pagination does not create duplicate or skipped results under stable ordering.

### API-006 — Add API integration and contract tests
**Tasks**
- Test representative entries with multiple senses and glosses.
- Test missing data and disputed/rejected assertions.
- Test source metadata visibility.
- Test authorization boundaries for write routes.

**Acceptance criteria**
- Tests run against PostgreSQL.
- OpenAPI output matches intended contracts.
- API contracts are stable enough for frontend integration.

**CP6 exit gate**
- Entry detail, related forms and source metadata endpoints work.
- API contracts are documented.
- Integration tests pass against realistic fixtures.

---

## CP7 — Search API

**Checkpoint outcome:** The backend supports practical isiXhosa and English lexical discovery using tested database search behaviour.

### SEARCH-001 — Build isiXhosa search test corpus
**Tasks**
- Select representative words and forms from approved data.
- Include click letters `c`, `q`, `x`, meaningful digraphs such as `kh`, `ph`, `th`, `gc`, apostrophe variants where relevant, case variants, and words with multiple senses.
- Include known negative cases and ambiguous forms.
- Have examples reviewed by a competent isiXhosa speaker where possible.

**Acceptance criteria**
- Search evaluation set is version controlled.
- Expected results and ranking expectations are documented.
- Test set is not built solely from easy English-like examples.

### SEARCH-002 — Define safe text normalisation
**Tasks**
- Implement Unicode NFC canonical handling.
- Preserve original strings.
- Create separate search-normalised representations.
- Normalise quote/apostrophe variants only where safe.
- Evaluate case handling using isiXhosa test cases.
- Preserve meaningful letters and digraphs.

**Acceptance criteria**
- Original stored text remains unchanged.
- Normalisation does not collapse meaningful distinctions.
- Tests cover the agreed character cases.

### SEARCH-003 — Implement exact and prefix/partial lookup
**Tasks**
- Implement exact lexical lookup.
- Implement prefix and partial matching.
- Define deterministic ranking and tie-breaking.
- Add appropriate indexes.

**Acceptance criteria**
- Exact match ranks above weaker matches.
- Results are stable and paginated.
- Search performance is measured on realistic data volume.

### SEARCH-004 — Implement English gloss search
**Tasks**
- Search English glosses linked to individual senses.
- Return the corresponding isiXhosa entry and matching sense.
- Preserve the relationship between the English gloss and its sense.

**Acceptance criteria**
- English search does not treat a gloss as an independent isiXhosa entry.
- Results expose the matched sense and its review status.
- Ambiguous English glosses can return multiple valid entries.

### SEARCH-005 — Implement attested form lookup
**Tasks**
- Search stored forms and validated form-to-lemma relationships.
- Include lemma mapping only when supported by approved data/evaluation.
- Preserve ambiguity and provenance.

**Acceptance criteria**
- Only attested or validated forms are used.
- No runtime morphological guess is presented as fact.
- If lemma evaluation fails its threshold, the endpoint does not claim authoritative lemma resolution.

### SEARCH-006 — Evaluate approximate search
**Tasks**
- Evaluate PostgreSQL `pg_trgm` or another justified approximate method.
- Compare results against the evaluation set.
- Set thresholds to avoid noisy matches.
- Disable the feature if it harms precision.

**Acceptance criteria**
- Approximate search is enabled only if measured quality supports it.
- Exact and prefix matches retain priority.
- False positives are recorded and reviewed.

### SEARCH-007 — Implement search endpoint
**Tasks**
- Implement `GET /api/v1/search?q=...`.
- Support documented search modes/filters only where needed.
- Return entry summary, matched field/type and relevant sense information.
- Add pagination and result limits.

**Acceptance criteria**
- Empty, too-short, malformed and oversized queries are handled safely.
- Search result ordering is deterministic.
- API response distinguishes whether the match came from a headword, form or English gloss.

### SEARCH-008 — Search performance and regression tests
**Tasks**
- Test search behaviour on the approved evaluation corpus.
- Record precision/recall or suitable task-specific measures for each mode.
- Add query-plan/index checks for representative data volume.
- Add regression tests for previously fixed language-specific errors.

**Acceptance criteria**
- Search quality is measured, not judged only by visual inspection.
- Performance is acceptable for the measured dataset and documented target.
- Regressions fail CI where practical.

**CP7 exit gate**
- Exact, prefix/partial and English gloss search work.
- Attested-form search works only where validated.
- Search normalisation passes language-specific tests.
- Approximate search is included only if justified by evidence.

---

## CP8 — Corrections, review and protected administration

**Checkpoint outcome:** Knowledge can be improved without allowing public users or automated imports to overwrite accepted records.

### ADMIN-001 — Define authentication and authorisation boundary
**Tasks**
- Choose a production-appropriate authentication approach for the small reviewer/admin group.
- Define roles/permissions such as reviewer and administrator only if needed.
- Protect all write endpoints from the first implementation.
- Keep public read endpoints separate from privileged operations.

**Acceptance criteria**
- No write endpoint is publicly callable without authorisation.
- Development credentials are not accepted as production credentials.
- Permission checks are tested.

### ADMIN-002 — Implement correction submission
**Tasks**
- Implement `POST /api/v1/corrections`.
- Require a target assertion or clearly scoped target.
- Capture proposed correction, submitter identity or permitted anonymous metadata, reason and timestamp.
- Validate and rate-limit submissions.

**Acceptance criteria**
- Submission creates a pending item; it does not mutate accepted knowledge.
- Submission is linked to the assertion it concerns.
- Invalid or abusive payloads are rejected safely.

### ADMIN-003 — Implement review queue
**Tasks**
- Provide protected listing/filtering of pending corrections and unreviewed assertions.
- Include relevant source evidence and history.
- Support pagination and reviewer assignment only if needed.

**Acceptance criteria**
- Reviewer can inspect target assertion, current value, proposal and provenance.
- Restricted source content is not exposed to unauthorised users.
- Queue state is queryable and auditable.

### ADMIN-004 — Implement review decisions and state transitions
**Tasks**
- Implement protected accept, reject and dispute actions.
- Validate allowed state transitions.
- Require a reason for material decisions.
- Record actor, timestamp, prior status and new status.

**Acceptance criteria**
- Every review action appends a review event.
- Current status is updated consistently.
- Invalid transitions are rejected.
- A review action cannot erase prior history.

### ADMIN-005 — Implement content revision history
**Tasks**
- Preserve previous assertion content when a reviewer edits or accepts a correction.
- Link revisions to review events and contributor.
- Record change reason and timestamp.

**Acceptance criteria**
- Previous and current values can be reconstructed.
- Status history and content history are both preserved.
- No privileged edit silently destroys the old value.

### ADMIN-006 — Add abuse protection and audit tests
**Tasks**
- Add request size limits and rate limiting appropriate to correction submission.
- Add security logging for privileged actions.
- Test unauthorised access, invalid transitions and audit immutability.

**Acceptance criteria**
- Public users cannot perform reviewer actions.
- Sensitive information is not written to logs.
- Security tests pass.

**CP8 exit gate**
- Corrections are submitted as proposals.
- Reviewers can decide with reasons.
- Assertions retain complete provenance and history.
- All write paths are protected and tested.

---

## CP9 — Production readiness and operations

**Checkpoint outcome:** The backend can be deployed and operated with reasonable security, visibility and recovery procedures.

### OPS-001 — Finalise production configuration and secrets
**Tasks**
- Separate local, test and production configuration.
- Use the deployment platform's secret manager/environment settings.
- Validate required production settings at startup.
- Disable debug behaviour in production.

**Acceptance criteria**
- No production secret is stored in the repository.
- Misconfiguration fails safely.
- Production settings are documented.

### OPS-002 — Configure structured logging and request tracing
**Tasks**
- Add structured application logs.
- Add request/correlation IDs.
- Log import batch identifiers for pipeline activity.
- Redact credentials and sensitive user-submitted content.

**Acceptance criteria**
- API errors can be traced to a request ID.
- Pipeline runs can be traced to a batch ID.
- Logs do not expose secrets.

### OPS-003 — Add operational monitoring
**Tasks**
- Monitor health/readiness, error rates and response latency.
- Monitor database connectivity and connection pool behaviour.
- Record pipeline run outcomes and failed batches.
- Define basic alert thresholds appropriate to the chosen host.

**Acceptance criteria**
- Operational failures are detectable.
- Monitoring does not expose private data.
- A documented operator can identify common failure modes.

### OPS-004 — Define backup and restore procedure
**Tasks**
- Configure database backups appropriate to the hosting service.
- Define retention and restore testing.
- Document migration recovery and data import recovery.
- Test restoring into a separate environment.

**Acceptance criteria**
- A database backup can be restored successfully.
- Restore procedure is documented and repeatable.
- Backup existence is not treated as proof of recoverability.

### OPS-005 — Deploy backend to a production-like environment
**Tasks**
- Select hosting only after local implementation and data requirements are understood.
- Configure HTTPS, environment variables, database networking and runtime command.
- Apply migrations through a controlled deployment step.
- Verify health, readiness and core endpoints.

**Acceptance criteria**
- Deployment can be repeated from documented steps.
- Database is not publicly exposed.
- Only intended API routes are exposed.
- Deployment smoke tests pass.

### OPS-006 — Security and release review
**Tasks**
- Review input validation, authentication, authorisation and database privileges.
- Review dependency vulnerabilities and secret handling.
- Review CORS and allowed origins for the intended client.
- Review API documentation exposure and administrative routes.
- Confirm licence/attribution obligations are met.

**Acceptance criteria**
- No known critical security issue remains unresolved.
- Production write operations are protected.
- Data licensing obligations are reflected in API and deployment behaviour.

**CP9 exit gate**
- Production-like deployment works.
- HTTPS and secrets are configured.
- Logs and monitoring are usable.
- Backup restore has been tested.
- Security and licensing review passes.

---

## CP10 — Optional offline SQLite export

**Checkpoint outcome:** A separate, versioned read-only SQLite knowledge pack can be generated for clients, without making SQLite the authoritative database.

### OFFLINE-001 — Define publication eligibility
**Tasks**
- Define which sources and assertions may be redistributed.
- Include verified assertions.
- Decide whether imported unreviewed assertions can be included with clear labels.
- Exclude rejected assertions and, by default, disputed assertions.
- Preserve source/licence attribution.

**Acceptance criteria**
- Publication rules are explicit and testable.
- Licence-restricted content is excluded or handled according to its terms.
- The pack never hides review state.

### OFFLINE-002 — Build SQLite pack exporter
**Tasks**
- Export eligible lexical entries, senses, glosses, forms, examples and provenance metadata.
- Add pack version, schema version, generated timestamp and source manifest.
- Keep export deterministic where practical.

**Acceptance criteria**
- Export is separate from normal API request handling.
- Pack is read-only from the client perspective.
- Export manifest identifies included source versions.

### OFFLINE-003 — Add SQLite search and integrity validation
**Tasks**
- Evaluate SQLite FTS5.
- Validate foreign-key relationships and required indexes.
- Test pack opening and read queries.
- Verify content counts and licence separation.

**Acceptance criteria**
- Pack passes integrity checks.
- Search results meet the agreed offline test cases.
- Pack version and schema version are readable.

### OFFLINE-004 — Publish and retain pack versions
**Tasks**
- Define storage and distribution location.
- Retain previous pack versions for rollback.
- Generate checksums.
- Document release and withdrawal procedure.

**Acceptance criteria**
- A client can identify pack version and checksum.
- A defective pack can be withdrawn or superseded.
- Offline export does not block online release if not ready.

**CP10 exit gate**
- Export passes licensing, content, integrity and search checks.
- A versioned pack is reproducible.
- Online PostgreSQL remains authoritative.

---

# 7. Cross-cutting engineering requirements

These apply to every checkpoint and are not deferred to the end.

## 7.1 API conventions
- Prefix all public API routes with `/api/v1`.
- Use consistent response and error schemas.
- Validate all external input with Pydantic.
- Apply sensible request and result size limits.
- Do not expose raw SQLAlchemy/database exceptions.
- Keep OpenAPI documentation aligned with implemented behaviour.

## 7.2 Data integrity
- Use real foreign keys for relationships.
- Use database constraints for invariants that must never be violated.
- Use transactions for multi-table writes.
- Keep source records and platform assertions distinguishable.
- Do not use a generic polymorphic claim table as the initial model.
- Do not silently merge uncertain duplicate records.

## 7.3 Linguistic integrity
- Preserve source text and source-specific identifiers.
- Store canonical text in Unicode NFC.
- Keep search-normalised values separate.
- Preserve isiXhosa click letters and meaningful digraphs.
- Do not infer linguistic correctness from a successful import.
- Do not make a derived lemma authoritative without passing its evaluation gate.
- Represent uncertainty and conflicting evidence explicitly.

## 7.4 Testing policy
- Unit tests for pure service and transformation functions.
- Integration tests against PostgreSQL for persistence, constraints and transactions.
- API tests for response contracts, validation and permissions.
- Pipeline tests using small, version-controlled fixtures.
- Regression tests for linguistic normalisation and search.
- Promotion tests for idempotency, provenance and reversal.
- Security tests for all write operations.

## 7.5 Definition of done for an individual ticket
A ticket is done only when:
- The implementation meets its acceptance criteria.
- Relevant automated tests pass.
- Failure cases are handled.
- Configuration and migration changes are committed.
- Documentation is updated where behaviour or operation changes.
- No unrelated scope has been added.
- The work is demonstrable locally.

---

# 8. Recommended implementation order

The intended sequence is:

1. CP0 — Backend workspace.
2. CP1 — Dataset intelligence.
3. CP2 — Canonical model.
4. CP3 — Database foundation.
5. CP4 — Pipeline to staging.
6. CP5 — Controlled ingestion.
7. CP6 — Lexicon read API.
8. CP7 — Search API.
9. CP8 — Review workflow.
10. CP9 — Production readiness.
11. CP10 — Offline export, if the publication gates pass.

Some tickets within a checkpoint can be parallelised, but checkpoint exit criteria should remain sequential. In particular:

- Do not finalise database tables before CP1 and CP2.
- Do not ingest directly into authoritative tables.
- Do not build search ranking before the language-specific evaluation set exists.
- Do not expose write endpoints before authentication and authorisation are in place.
- Do not choose hosting based only on preference; choose it after the local system and operational needs are clear.
- Do not let optional offline export delay a working online API.

# 9. Release acceptance checklist

The backend V1 is ready for client integration and release when all required items below pass:

- [ ] Backend can be installed and run from a clean clone.
- [ ] PostgreSQL schema is reproducible from migrations.
- [ ] Approved source resources have documented licence and provenance.
- [ ] At least one source has completed the controlled ingestion process.
- [ ] Imported assertions are traceable to source version and import batch.
- [ ] Lexical entries and senses are represented without flattening meanings.
- [ ] English glosses are linked to individual senses.
- [ ] Attested forms and lemma relationships are only exposed where supported.
- [ ] Review status and origin method are separate and assertion-level.
- [ ] Search supports exact, partial/prefix and English gloss lookup.
- [ ] Search normalisation passes isiXhosa-specific regression tests.
- [ ] API contracts and error handling are documented.
- [ ] All write operations are protected.
- [ ] Corrections do not overwrite accepted knowledge automatically.
- [ ] Tests cover database integrity, API behaviour, pipeline and security.
- [ ] Production deployment, logging and backup/restore procedures are tested.
- [ ] Data licensing and attribution obligations are satisfied.
- [ ] Optional offline pack passes its own gates, or is explicitly deferred.

## 10. Important implementation discipline

This plan is intentionally comprehensive, but it is not a reason to build every possible abstraction immediately. Implement the smallest solution that satisfies each ticket. When a source does not provide a field, do not invent it. When a proposed model cannot represent a real source record cleanly, revisit the model rather than forcing the record into the wrong shape.

The first concrete implementation target is **CP0**. Complete its tickets and exit gate, then move to CP1. Do not start by building every API endpoint or every database table before the source data has been inspected.
