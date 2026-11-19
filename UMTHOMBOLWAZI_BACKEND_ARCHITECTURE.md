# uMthombolwazi Intelligence --- Backend Architecture

**Version:** 1.2\
**Status:** Implementation baseline\
**Last updated:** 19 November 2026

## 1. Purpose

This document defines the initial backend architecture and
implementation decisions. It is intentionally pragmatic: support a
linguistically complex knowledge base without imposing abstractions or
infrastructure that are not justified by real data and use cases.

## 2. Architecture Decisions

The backend adopts:

1.  **Modular Monolith:** One deployable FastAPI application with clear
    functional module boundaries.
2.  **Independent Data Engineering Pipeline:** Acquisition, inspection,
    transformation, reconciliation and bulk loading happen outside
    normal API request handling.
3.  **PostgreSQL:** The authoritative application and linguistic
    knowledge database.

Use a simple internal structure: routers, services, SQLAlchemy models
and Pydantic schemas. Do not implement a full four-layer Clean
Architecture in every module. Do not duplicate ORM models with separate
domain entities unless complex business rules justify that separation.

## 3. High-Level System

``` text
React Native / Expo / Expo Web
              |
              v
        FastAPI REST API
              |
       Routers and Services
              |
     SQLAlchemy / PostgreSQL
              |
     Application Knowledge Base

External datasets
       |
       v
Data engineering pipeline
       |
       v
Immutable raw files
       |
       v
Inspection and profiling
       |
       v
Transformation and reconciliation
       |
       v
Validation
       |
       v
PostgreSQL staging schema
       |
       v
Versioned, tested promotion SQL
       |
       v
Application knowledge tables
```

The pipeline is independent. It may share database configuration and
reusable validation code, but bulk raw loads must not pass through
public API endpoints.

## 4. Initial Backend Modules

Start with three modules only.

### 4.1 `lexicon`

Owns core lexical records: lexical entries and headwords, senses and
meanings, English glosses, word forms, form-to-lemma relationships, and
usage examples where the initial model requires them.

### 4.2 `sources`

Owns provenance and resource metadata: sources, source versions, import
batches, contributors, claim-to-source relationships, review events and
audit history.

The application module may be named `sources`; its database schema can
be named `provenance`.

### 4.3 `search`

Provides read operations over lexical data. It does not own canonical
linguistic records.

Initial capabilities: - Exact search. - Prefix and partial search. -
Approximate search. - English gloss search. - Search across attested
forms. - Search by canonical lexical form.

Do not describe English gloss search as semantic search. Semantic search
is deferred.

### Later modules

Add `expressions`, `context` and `linguistics` when real records and
workflows demonstrate the need for separate boundaries.

## 5. Directory Structure

``` text
umthombolwazi/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── modules/
│   │   │   ├── lexicon/
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   ├── models.py
│   │   │   │   └── schemas.py
│   │   │   ├── sources/
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   ├── models.py
│   │   │   │   └── schemas.py
│   │   │   └── search/
│   │   │       ├── router.py
│   │   │       ├── service.py
│   │   │       └── schemas.py
│   │   └── shared/
│   ├── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── data-engineering/
│   ├── registry/
│   ├── acquisition/
│   ├── inspection/
│   ├── staging/
│   ├── transformation/
│   ├── reconciliation/
│   ├── validation/
│   ├── ingestion/
│   └── reporting/
├── datasets/
│   ├── raw/
│   ├── staging/
│   └── processed/
├── database/
│   ├── documentation/
│   └── promotion/
├── docker-compose.yml
├── .gitignore
└── README.md
```

Create directories as implementation begins; an empty directory tree is
not a deliverable.

## 6. Assertion and Verification Model

### 6.1 Assertion-specific tables

Do not use a generic polymorphic claim table for the initial known
assertion types. Use assertion-specific tables with real foreign keys
and their own review state.

Initial provisional assertion types:

  Table                     Assertion
  ------------------------- --------------------------------------------
  `lexicon.lexical_sense`   A lexical entry has a particular sense
  `lexicon.sense_gloss`     A sense has a particular English gloss
  `lexicon.form_lemma`      A form belongs to a particular lemma
  `lexicon.usage_example`   An example demonstrates a particular usage

Dataset profiling may show that some need a different representation or
that more assertion types are needed.

Each assertion should carry: - `id` - `origin_method` -
`review_status` - `created_at` - `updated_at`

### 6.2 Origin method

Origin describes how the assertion entered the system:

-   `imported`
-   `derived`
-   `manual`
-   `user_submitted`

### 6.3 Review status

Review describes the current assessment of that assertion:

-   `unreviewed`
-   `verified`
-   `disputed`
-   `rejected`

Origin and review status are independent. An imported assertion can be
verified; a manually submitted assertion can be disputed.

Review applies to the individual assertion, not automatically to the
whole lexical entry.

## 7. Sources and Provenance

Keep source identity, source version and import run distinct.

### `source`

Represents the resource or organisation from which information
originates. Suggested metadata includes name, description,
publisher/creator, resource URL or catalogue identifier, source
authority/quality category, access conditions and general licence
information.

### `source_version`

Represents a specific release of a source. Suggested metadata includes
source ID, version label, release date, download URL or repository item
identifier, file metadata and checksum, applicable licence, citation and
attribution instructions.

### `import_batch`

Represents one acquisition or processing run. Suggested metadata
includes source version ID, start/completion timestamps, status, records
read/staged/promoted/rejected, pipeline version or Git commit, input
checksums, run configuration and report location.

Possible statuses: `running`, `completed`, `failed`, `rolled_back`.

### `contributor`

Provides minimal identity for reviewers and contributors. Do not build a
full public identity system at this stage. Review events must identify
the responsible contributor or service account.

### Source quality

Source authority/quality is separate from review outcome. Descriptive
categories may include institutional, academic, lexicographer-edited,
community-contributed, machine-generated and individual-contributed.
These are not automatic quality scores. Retain source notes and
limitations.

## 8. Claim-to-Source Links

A claim may have multiple supporting or contradicting sources.

Use a shared `provenance.claim_source` table with typed nullable foreign
keys for supported assertion tables. Enforce that exactly one assertion
foreign key is populated and add a real foreign-key constraint for each.

Suggested fields: - `id` - `lexical_sense_id` (nullable FK) -
`sense_gloss_id` (nullable FK) - `form_lemma_id` (nullable FK) -
`usage_example_id` (nullable FK) - `source_version_id` (FK) -
`import_batch_id` (nullable FK) - `relationship_type` - `created_at`

Initial relationship types: - `direct_source` - `supporting_evidence` -
`derived_from` - `contradicting_evidence`

Use a database check constraint equivalent to `num_nonnulls(...) = 1`.

The source link is not replaced by `origin_method`: one describes
acquisition method; the other records evidence and provenance.

## 9. Review Events and Append-Only History

Use a shared `provenance.review_event` table with typed nullable foreign
keys to the assertion tables.

Suggested fields: - `id` - Typed assertion foreign keys. -
`contributor_id` (FK). - `previous_status`. - `new_status`. -
`reason`. - `created_at`.

Enforce exactly one assertion foreign key per event and enforce real
foreign keys.

Review events are append-only. The current `review_status` on the
assertion is a convenient current-state projection; the event table is
the audit history.

Important changes to assertion content must also be auditable. Before
enabling user corrections, decide whether to add assertion revision
tables or an append-only change-event mechanism. A review-status event
alone does not preserve the history of changed text.

## 10. Database Layout and Migrations

PostgreSQL is the system of record.

Initial application schemas: - `lexicon` - `provenance`

A separate `staging` schema is used for raw and transformed import
tables.

Alembic manages application-owned tables and schema changes. Pipeline
staging tables and transient raw-load structures are managed separately
so they do not conflict with ORM metadata or Alembic autogeneration.

Promotion SQL must be version-controlled, reviewed and tested against
representative staging fixtures. A schema change must not silently break
an import.

Use PostgreSQL 18 `uuidv7()` where available. For older versions,
generate UUIDv7 in the application.

Use foreign keys, check constraints, unique constraints and indexes
where they represent actual invariants.

## 11. Text Normalisation and Search

Preserve original text. Store a canonical NFC-normalised representation
and, where needed, separate search representations.

Search preparation must be based on isiXhosa examples and linguistic
review:

-   Normalise apostrophe and quotation-mark variants where safe.
-   Apply carefully tested case handling.
-   Preserve click letters `c`, `q` and `x`.
-   Preserve meaningful digraphs, including `kh`, `ph`, `th` and `gc`.
-   Do not use generic English accent-folding rules as the linguistic
    specification.
-   Never replace or discard original spelling.

Evaluate PostgreSQL `pg_trgm` for approximate matching. Use PostgreSQL
full-text search where appropriate. A normalised or relaxed search
column may be added alongside canonical text.

Build an isiXhosa test set before locking search normalisation
behaviour.

## 12. Lemma Resolution

Lemma resolution belongs primarily in the data-engineering pipeline.

Evaluate NCHLT lemma resources and relevant ctextcore capabilities. Do
not assume their conventions, availability or quality before inspection.

Initial process: 1. Inspect the resource and documentation. 2. Record
tokenisation and annotation conventions. 3. Build a small manually
checked evaluation set. 4. Separate development examples from held-out
evaluation examples. 5. Tune only on the development set. 6. Report
held-out accuracy and coverage. 7. Build a precomputed form-to-lemma
index where results justify it. 8. Preserve the origin and source of
each mapping.

An optional runtime lookup may be added later. Machine-generated
mappings remain unreviewed unless independently validated.

### 50-token evaluation gate

Before evaluation, document: - What counts as a token. - What counts as
the correct lemma. - Treatment of ambiguous forms and multiple valid
analyses. - Scoring method. - Required minimum accuracy and coverage. -
Held-out evaluation procedure.

Do not choose or change the threshold after seeing the held-out result.
If the tool falls below the agreed threshold, use it only to generate
candidates or assist the pipeline; do not present its output as
authoritative.

The numerical threshold must be agreed and recorded before the test
begins.

## 13. Data Pipeline and Promotion

``` text
Resource registry
      |
Acquisition
      |
Immutable raw files + checksums
      |
Inspection and profiling
      |
Transformation
      |
Reconciliation
      |
Validation
      |
PostgreSQL staging
      |
Versioned promotion SQL
      |
Application tables + provenance
```

Raw files are immutable. Transformations write to new staging or
processed outputs.

Bulk loads go directly into staging tables. Promotion is performed in
controlled transactions and must create the necessary provenance and
review records.

Every import is associated with a source version and import batch.

Promotion scripts are versioned and tested against fixtures. Import
reports include counts, rejected records, warnings and checksums.

Rollback must not erase the audit trail. It should reverse or deactivate
promoted records through a controlled, recorded operation.

## 14. Correction Submissions and Administrative Protection

A future correction endpoint accepts a proposed change and creates a
reviewable submission. It must not directly overwrite accepted
linguistic knowledge.

Minimum workflow: 1. Identify the target assertion. 2. Record the
proposed value or correction. 3. Record contributor identity and
submission time. 4. Add the submission to a review queue. 5. Allow an
authorised reviewer to accept or reject it. 6. Record the decision and
preserve prior content and status.

Any write endpoint must have basic administrative protection from the
beginning, including local development. Public read access can be
considered separately.

A minimal admin key or equivalent local mechanism is sufficient
initially; do not build a full authentication platform prematurely.

## 15. Offline SQLite Export

A separate export job generates versioned SQLite knowledge packs.

### Initial publication policy

For usable early coverage, the pack may include imported but unreviewed
records if clearly labelled as unreviewed. Verified records must be
distinguishable. Rejected records are excluded. Disputed records are
excluded by default.

This is a publication decision, not an assertion that imported data is
correct.

### Pack contents

-   Eligible lexical entries and senses.
-   English glosses.
-   Eligible word forms and form-to-lemma mappings.
-   Examples and required relationships.
-   Review labels.
-   Source and attribution metadata.
-   Licence/content-separation metadata.
-   Pack version and generation metadata.

Evaluate SQLite FTS5 for offline search. Include the form-to-lemma index
where supported by evaluation. Validate foreign-key integrity, FTS
indexes, counts, version metadata and licensing metadata before
publishing a pack.

Keep content with different licence obligations identifiable and
separable.

## 16. API Design

Versioned REST API prefix: `/api/v1`

Initial endpoint groups: - `/lexicon` - `/sources` - `/search`

Examples:

``` http
GET /api/v1/lexicon/{entry_id}
GET /api/v1/search?q=ukuhamba
GET /api/v1/sources
```

Later endpoints may include correction submissions, review operations,
expressions and contextual examples.

Routers handle HTTP concerns and call services. Services coordinate
application operations. SQLAlchemy models define persistence. Pydantic
schemas define API inputs and outputs.

Do not put substantial business logic or ad hoc database operations in
route handlers.

## 17. Testing

Minimum testing approach: - Unit tests for pure linguistic functions and
service logic. - Integration tests against PostgreSQL. - API tests for
request validation, status codes and response shapes. - Importer tests
using representative source fixtures. - Promotion SQL tests against
staging fixtures. - Provenance and review-integrity tests. - Lemma
evaluation tests with held-out examples. - Search tests using
isiXhosa-specific words and near-matches. - SQLite export tests,
including FTS5 and licence metadata.

## 18. Implementation Order

### Phase 1 --- Acquisition and Profiling

Do this before building the full API.

1.  Profile the current isiXhosa.click dataset or backup.
2.  Inspect fields, encoding, counts, duplicates, examples,
    relationships and licence metadata.
3.  Run the 50-token lemma evaluation after recording scoring rules and
    acceptance threshold.
4.  Inspect NCHLT lemma/POS resources and ctextcore capabilities.
5.  Inspect selected SADiLaR and Autshumato resources.
6.  Produce dataset inventories and an integration mapping report.

**Deliverables:** - Dataset inventory. - isiXhosa.click profiling
report. - Lemma evaluation report. - Source/licence register. - Initial
source-to-canonical-field mapping. - List of unresolved linguistic and
modelling questions.

### Phase 2 --- Canonical Knowledge Model

1.  Define lexical entries, senses, glosses and forms.
2.  Define assertion-specific review fields.
3.  Define source, source-version and import-batch relationships.
4.  Define claim-source and review-event relationships.
5.  Validate the model against real records from Phase 1.
6.  Document licence-aware export requirements.

### Phase 3 --- Backend Foundation

1.  Create the FastAPI project.
2.  Configure Docker and PostgreSQL.
3.  Configure SQLAlchemy and Alembic.
4.  Implement `lexicon`, `sources` and `search`.
5.  Add health checks, configuration and logging.
6.  Add tests and protected write-operation foundations.

### Phase 4 --- Data Integration

1.  Implement source-specific acquisition and import adapters.
2.  Load raw data into staging.
3.  Transform and reconcile records.
4.  Validate candidate assertions.
5.  Promote through versioned, tested SQL.
6.  Generate import and quality reports.

### Phase 5 --- First Product API

1.  Implement lexical retrieval.
2.  Implement bilingual exact, partial and approximate search.
3.  Expose provenance and review labels appropriately.
4.  Implement correction submissions and administrative review.

### Phase 6 --- Offline and Expansion

1.  Implement versioned SQLite export.
2.  Evaluate FTS5 and form-to-lemma pack support.
3.  Add expressions, context and linguistic processing as requirements
    mature.
4.  Measure search and linguistic quality before introducing advanced
    intelligence.

## 19. Decisions Requiring Evidence Before Finalisation

Do not hard-code assumptions for: - Exact canonical lexical schema. -
Whether examples initially attach to senses or need a separate reusable
context model. - Exact assertion types after source profiling. - Lemma
tool acceptance threshold. - Exact text-folding and normalisation
rules. - Source-specific redistribution rights. - Detailed SQLite pack
publication rules for each licence. - Runtime lemma lookup requirements.

Resolve these through dataset inspection, linguistic evidence, licence
review and measured product needs.

## 20. Final Position

Build a pragmatic Modular Monolith with three initial modules:
`lexicon`, `sources` and `search`.

Keep data engineering independent. Use PostgreSQL as the source of
truth. Represent provenance and review at assertion level with real
foreign keys. Preserve source and import history. Build from profiled
data rather than designing a large abstract model in advance.

The immediate next task is Phase 1: acquire, inspect and profile the
first datasets.
