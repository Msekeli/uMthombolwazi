# uMthombolwazi Intelligence --- Version 1 Product Architecture and Delivery Plan

**Version:** 1.0\
**Status:** Proposed implementation baseline\
**Last updated:** 19 November 2026

> This document defines the architecture and delivery plan for the
> complete first version of uMthombolwazi Intelligence. It covers the
> client applications, backend, database, linguistic data pipeline,
> offline capability, and the work required to deliver V1. It supersedes
> the earlier backend-only architecture specification.

------------------------------------------------------------------------

## 1. Purpose

This document describes how we will build and deliver the first usable
version of uMthombolwazi Intelligence.

V1 is a complete product slice, not just a backend. It includes:

-   A mobile application built with React Native and Expo.
-   A browser-accessible application using Expo Web initially.
-   A Python FastAPI backend.
-   A PostgreSQL linguistic knowledge database.
-   A separate Python data-engineering pipeline.
-   A small protected administrative workflow for managing and reviewing
    linguistic records.
-   A defined path to publishable offline SQLite knowledge packs, with
    the first pack included in V1 only if the data and licensing gates
    are met.

The purpose of V1 is to deliver a dependable bilingual isiXhosa
knowledge and discovery application backed by traceable linguistic data.
It is not intended to deliver the entire long-term AI ecosystem.

## 2. V1 Product Outcome

At the end of V1, a user should be able to open the application on a
phone or in a browser, search for an isiXhosa word or an English gloss,
inspect the available lexical information, understand how reliable the
information is, and explore related forms and examples where the data
supports them.

The product must be useful even when the underlying data is incomplete.
It must communicate missing information rather than invent it.

### 2.1 Primary users

-   IsiXhosa learners who need explanations and English glosses.
-   Existing isiXhosa speakers who want to explore words, meanings and
    usage.
-   Early reviewers or administrators who help maintain the quality of
    the knowledge base.

### 2.2 V1 user capabilities

A user should be able to:

1.  Search in isiXhosa.
2.  Search using an English gloss.
3.  Find a word through an attested form where a validated form-to-lemma
    mapping exists.
4.  Open a lexical entry.
5.  View its available senses and explanations.
6.  View English glosses associated with individual senses.
7.  View grammatical information when available.
8.  View attested forms and lemma relationships when available.
9.  Read examples and their source/review labels when available.
10. See whether information is imported, derived or manually
    contributed, and whether it has been reviewed.
11. Save entries to a personal vocabulary list, if local persistence is
    included in the V1 implementation.
12. Submit a correction suggestion, if the protected review workflow is
    completed within V1.

The application must not imply that every word has every type of
information. Empty or unavailable fields should be handled clearly.

## 3. What V1 Does Not Include

The following are part of the longer-term product vision but are not V1
delivery requirements:

-   AI chatbot or conversational tutor.
-   Generative AI writing assistant.
-   AI story generation.
-   AI content studio.
-   Social-media content generation.
-   Video or image generation.
-   Speech recognition or text-to-speech.
-   Production-grade machine translation.
-   Model training or fine-tuning.
-   Full lexicographer research suite.
-   Multi-organisation collaboration.
-   Public developer API plans, billing or API keys.
-   Microservices or distributed deployment.
-   Full user account, social and synchronisation system unless a
    demonstrated V1 requirement emerges.

These capabilities may later consume uMthombolwazi's knowledge and
language services through separate products. They must not expand the V1
scope.

## 4. V1 Architecture Decisions

  -----------------------------------------------------------------------
  Area                                V1 decision
  ----------------------------------- -----------------------------------
  Overall architecture                Modular Monolith

  Mobile client                       React Native + Expo + TypeScript

  Web client                          Expo Web initially

  Client navigation                   Expo Router

  Client data fetching                A small typed API client; use a
                                      query/cache library only where it
                                      adds clear value

  Backend                             Python + FastAPI

  Backend structure                   Functional modules with routers,
                                      services, SQLAlchemy models and
                                      Pydantic schemas

  Database                            PostgreSQL

  ORM                                 SQLAlchemy

  Migrations                          Alembic for application-owned
                                      schema

  Data engineering                    Separate Python pipeline

  Raw data                            Immutable files with checksums and
                                      resource metadata

  Bulk loading                        PostgreSQL staging schema and
                                      controlled promotion

  Offline data                        SQLite knowledge pack, subject to
                                      V1 publication gates

  Offline search                      SQLite FTS5, subject to evaluation

  Local development                   Docker Compose

  Testing                             Pytest for Python; client component
                                      and end-to-end tests as appropriate

  Source control                      Private Git repository
  -----------------------------------------------------------------------

Do not introduce microservices. Do not implement a full Clean
Architecture layer hierarchy in every module. Keep the design
understandable and testable for a solo developer.

## 5. System Context

``` text
                  V1 CLIENT APPLICATIONS
          +-------------------+-------------------+
          |                   |                   |
     iOS / Android         Web Browser       Local SQLite Pack
    React Native + Expo    Expo Web          Offline read access
          |                   |                   ^
          +-------------------+                   |
                      |                           |
                      v                           |
                 HTTPS REST API                   |
                      |                           |
                FASTAPI BACKEND                   |
          +-----------+------------+              |
          |           |            |              |
       Lexicon      Sources       Search          |
       services     services      read layer      |
          |           |            |              |
          +-----------+------------+              |
                      |                           |
                      v                           |
                  POSTGRESQL                      |
          +---------------------------+           |
          | Lexicon                   |           |
          | Provenance                |           |
          | Review / contributor data |           |
          +---------------------------+           |
                      ^                           |
                      |                           |
             Controlled promotion                 |
                      ^                           |
                      |                           |
              DATA ENGINEERING                    |
          +---------------------------+           |
          | Resource registry         |           |
          | Acquisition                |           |
          | Inspection and profiling  |           |
          | Transformation            |           |
          | Reconciliation            |           |
          | Validation                |           |
          | Staging and promotion     |           |
          +---------------------------+           |
                      ^                           |
                      |                           |
          Licensed datasets and research sources  |
```

The client communicates with the backend through the REST API for online
operations. Offline access, if delivered, reads a generated and
versioned SQLite pack. The data pipeline is not part of normal API
request handling.

## 6. Client Application Architecture

### 6.1 Technology

Use:

-   React Native.
-   Expo.
-   TypeScript.
-   Expo Router.
-   Expo Web for initial browser support.

The client should be mobile-first and responsive. Shared product logic
and UI components should be reused where practical, while
platform-specific behaviour should be isolated where necessary.

Expo Web is the initial web strategy, not an irrevocable commitment. If
the product later needs web-specific capabilities that Expo Web cannot
support cleanly, a separate web client can be evaluated.

### 6.2 Suggested client structure

``` text
frontend/
├── app/
│   ├── _layout.tsx
│   ├── index.tsx
│   ├── search.tsx
│   ├── entry/
│   │   └── [entryId].tsx
│   ├── saved.tsx
│   └── settings.tsx
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── search/
│   │   └── lexicon/
│   ├── features/
│   │   ├── search/
│   │   ├── lexicon/
│   │   ├── saved/
│   │   └── corrections/
│   ├── lib/
│   │   ├── api/
│   │   ├── storage/
│   │   └── validation/
│   ├── hooks/
│   ├── types/
│   └── constants/
├── assets/
├── tests/
├── app.json
├── package.json
└── tsconfig.json
```

This is a starting point. Do not create empty feature directories before
those features are implemented.

### 6.3 V1 screens

**Home / Search** - Search input. - Clear language direction or search
mode where useful. - Recent searches, if implemented. - Entry points to
saved vocabulary.

**Search Results** - Matching lexical entries. - English gloss
matches. - Attested form matches where available. - Clear distinction
between exact and approximate matches. - Review/source indicators where
useful.

**Lexical Entry Detail** - Headword. - Pronunciation only if reliable
data becomes available; do not invent it. - Part of speech where
known. - Separate senses. - English glosses for each sense. - Attested
forms and lemma links. - Grammatical information where available. -
Contextual examples. - Source and review labels.

**Saved Vocabulary** - Locally saved entries. - Basic organisation or
filtering if justified.

**Settings / About** - App and knowledge-pack version. - Data/source
information. - Offline pack status where applicable. - Clear explanation
of review labels.

**Correction Submission** - Proposed correction linked to a specific
entry or assertion. - Optional explanation. - Submission
acknowledgement. - No direct modification of trusted knowledge.

### 6.4 Client state and persistence

Keep server-owned linguistic data authoritative.

Use in-memory state and an API cache for online browsing. Use device
persistence for user preferences and saved entries.

If offline packs are delivered in V1: - Store the pack in app-accessible
local storage. - Record pack version and generation date. - Validate the
pack before activating it. - Make offline search read-only. - Do not
implement bidirectional synchronisation in V1. - Do not let local edits
silently overwrite server records.

The first offline scope is read-only knowledge access, not a full
offline-first collaborative system.

## 7. Backend Architecture

### 7.1 Structure

The backend is a single FastAPI application organised as a Modular
Monolith.

Start with three modules:

1.  `lexicon`
2.  `sources`
3.  `search`

Add separate `expressions`, `context` or `linguistics` modules only when
real data and workflows justify them.

### 7.2 Suggested backend structure

``` text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── modules/
│   │   ├── lexicon/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── sources/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   └── search/
│   │       ├── router.py
│   │       ├── service.py
│   │       └── schemas.py
│   └── shared/
├── migrations/
├── tests/
├── pyproject.toml
└── .env.example
```

### 7.3 Responsibilities

-   Routers handle HTTP requests, response codes and API-level
    validation.
-   Services implement application workflows and business operations.
-   SQLAlchemy models represent persistence.
-   Pydantic schemas define request and response contracts.
-   Core contains configuration, database setup, security and logging.

Do not put substantial business logic in route handlers. Do not
duplicate every SQLAlchemy model with a separate domain entity without a
demonstrated need.

### 7.4 Initial API surface

Prefix: `/api/v1`

Initial read endpoints:

``` http
GET /api/v1/search?q=ukuhamba
GET /api/v1/lexicon/{entry_id}
GET /api/v1/lexicon/{entry_id}/related
GET /api/v1/sources
GET /api/v1/health
```

Exact endpoint details will be finalised after the canonical model is
validated.

Protected write endpoints, if included in V1:

``` http
POST /api/v1/corrections
POST /api/v1/admin/reviews/{assertion_id}
```

All write operations must require administrative or contributor
authorisation. Public read access can remain separate.

## 8. Database and Knowledge Model

PostgreSQL is the authoritative store.

Initial application schemas:

-   `lexicon`
-   `provenance`

A separate `staging` schema is used for pipeline imports. Alembic
manages application-owned tables; staging structures are managed
separately to avoid conflicts with ORM metadata and migration
autogeneration.

### 8.1 Core lexical concepts

The model must distinguish:

-   Lexical entry.
-   Sense.
-   English gloss.
-   Word form.
-   Form-to-lemma relationship.
-   Usage example, where the source and modelling evidence justify it.

A lexical entry may have multiple senses. A sense may have multiple
glosses. A word form is not automatically a separate lexical entry.

The exact schema is finalised after Phase 1 data profiling.

### 8.2 Assertion-level review

Initial provisional assertion tables:

  Table                     Assertion
  ------------------------- --------------------------------------
  `lexicon.lexical_sense`   Entry has a particular sense
  `lexicon.sense_gloss`     Sense has a particular English gloss
  `lexicon.form_lemma`      Form belongs to a lemma
  `lexicon.usage_example`   Example demonstrates a usage

Each assertion carries an independent `origin_method` and
`review_status`.

Origin methods: - `imported` - `derived` - `manual` - `user_submitted`

Review statuses: - `unreviewed` - `verified` - `disputed` - `rejected`

Do not assign a verified status to an entire entry merely because one of
its assertions has been reviewed.

### 8.3 Provenance

Keep these entities distinct:

-   `source`: the resource or organisation.
-   `source_version`: a particular release.
-   `import_batch`: one acquisition/processing run.
-   `contributor`: a reviewer or contributor.

Use a `claim_source` relationship table with typed nullable foreign keys
for the known assertion tables. Enforce exactly one assertion reference
per row and use real foreign-key constraints.

Use an append-only `review_event` table with typed assertion references
and a contributor foreign key.

Important content changes must also be auditable. Review-status events
alone do not preserve previous assertion text.

### 8.4 Source quality

Source authority is separate from assertion review. Record descriptive
source classifications and limitations, such as institutional, academic,
lexicographer-edited, community-contributed or machine-generated. These
are not automatic quality scores.

### 8.5 Database implementation

-   SQLAlchemy for persistence.
-   Alembic for application schema migrations.
-   PostgreSQL constraints and foreign keys for integrity.
-   PostgreSQL 18 `uuidv7()` where available; otherwise generate UUIDv7
    in the application.
-   Preserve original source text.
-   Use Unicode NFC for canonical normalisation.
-   Keep search-normalised representations separate from original text.

## 9. Search Design

Search is a read layer over the lexicon. It does not own the linguistic
records.

V1 search includes:

-   Exact lexical lookup.
-   Partial and prefix matching.
-   English gloss search.
-   Search across attested forms.
-   Approximate matching where measured quality supports it.

Evaluate PostgreSQL `pg_trgm` and full-text search where appropriate.

Normalisation rules must be tested against isiXhosa. Normalise
apostrophe and quotation variants where safe, and apply carefully tested
case handling. Preserve click letters `c`, `q`, `x` and meaningful
digraphs such as `kh`, `ph`, `th` and `gc`.

Do not apply generic English accent-folding as the language
specification. Original text must never be replaced by a folded search
value.

Semantic search is not a V1 requirement.

## 10. Data Engineering Pipeline

The pipeline is a separate Python workspace and execution workflow.

Suggested structure:

``` text
data-engineering/
├── registry/
├── acquisition/
├── inspection/
├── staging/
├── transformation/
├── reconciliation/
├── validation/
├── ingestion/
└── reporting/

datasets/
├── raw/
├── staging/
└── processed/
```

### 10.1 Pipeline flow

1.  Register source metadata and licence.
2.  Acquire the permitted dataset version.
3.  Preserve raw files unchanged.
4.  Calculate checksums.
5.  Inspect file structure, encoding, fields and counts.
6.  Profile duplicates, nulls and anomalies.
7.  Document linguistic conventions and limitations.
8.  Transform into staging representations.
9.  Reconcile potential duplicates without destructive merging.
10. Validate records.
11. Load to PostgreSQL staging.
12. Promote through version-controlled, tested SQL.
13. Generate import and quality reports.

Bulk imports must not pass through public API endpoints.

Every import must identify the source version, import batch, input
checksum and pipeline version. Promotion and rollback must be controlled
and auditable.

### 10.2 Initial resources

Evaluate, rather than blindly ingest:

-   isiXhosa.click.
-   NCHLT isiXhosa text and POS/lemma resources.
-   Selected SADiLaR datasets.
-   Autshumato monolingual and parallel corpora.
-   Other resources only after their relevance, licence and quality are
    established.

## 11. Lemma Resolution

Lemma processing is initially a data-engineering concern.

Evaluate NCHLT lemma data and relevant ctextcore capabilities. Inspect
conventions and quality rather than assuming compatibility.

Before the 50-token evaluation, define: - Token selection. - Correct
lemma criteria. - Ambiguity handling. - Development and held-out
examples. - Scoring method. - Minimum acceptable accuracy and coverage.

Do not tune against the held-out set. Record the numerical acceptance
threshold before evaluation. If the result is inadequate, retain the
tool as a candidate generator, not as an authoritative runtime feature.

A precomputed form-to-lemma index can be included in the knowledge base
when supported by the evaluation. Runtime lookup is optional and not
required for the first release.

## 12. Offline Knowledge Packs

Offline capability is desirable but must not delay the core online
product.

If the data and licensing gates are met, generate a versioned SQLite
pack containing eligible entries, senses, glosses, forms, lemma
mappings, examples, review labels and source/licence metadata.

Initial publication policy: - Verified records may be included. -
Imported unreviewed records may be included if clearly labelled. -
Rejected records are excluded. - Disputed records are excluded by
default.

Evaluate SQLite FTS5 for offline search. Validate pack integrity,
relationships, search indexes, version metadata and licence separation
before release.

V1 offline behaviour is read-only. No bidirectional sync is required.

If a legally reusable and sufficiently useful pack is not ready, V1 can
launch online first and deliver offline packs in a subsequent release.

## 13. Corrections and Administration

A small protected administrative capability is needed to manage review
and quality.

At minimum: - Contributor identity. - Protected write operations. -
Correction submissions linked to specific assertions. - Review queue. -
Accept/reject decisions. - Append-only review events. - Audit trail for
content changes.

User corrections must never overwrite accepted knowledge automatically.

A minimal admin key or equivalent local mechanism is sufficient for
early development. Before public deployment, use an appropriately
managed authentication and authorisation mechanism; do not expose a
shared development secret as production security.

## 14. V1 Deployment and Environments

### Local development

Use Docker Compose for PostgreSQL and any required local services. Run
the FastAPI server and Expo development server locally.

The application must be testable on: - iOS through Expo Go or an
appropriate development build. - Android through an emulator or device
when available. - Desktop browser through Expo Web.

The developer's primary development environment is macOS. Android
emulator performance may be constrained by older Intel hardware; browser
testing and physical-device testing should be used pragmatically.

### Production deployment

Choose hosting only after the local application and data pipeline work
reliably.

V1 deployment requires: - HTTPS. - Managed secrets and environment
configuration. - Database backups. - Migration procedure. - Basic
monitoring and error logging. - A repeatable deployment process. - A way
to publish and version client releases.

Do not commit to a specific cloud provider in this architecture. Select
one when deployment requirements, cost and regional availability are
known.

## 15. Security and Privacy

-   Keep credentials and API keys out of source control.
-   Validate all API input.
-   Protect every write endpoint.
-   Use least-privilege database credentials.
-   Keep public read operations separate from administrative operations.
-   Avoid logging secrets or unnecessary personal data.
-   Back up the database.
-   Record contributor identity for review actions.
-   Treat user correction submissions as untrusted until reviewed.

A full consumer account system is not a prerequisite for the first
public search experience. If saved vocabulary must synchronise across
devices, account and identity requirements must be revisited.

## 16. Testing and Quality Gates

### Client

-   Search and result rendering tests.
-   Entry detail rendering tests.
-   Loading, empty and error states.
-   Responsive web layout checks.
-   iOS and Android smoke tests.
-   Offline pack tests if offline is included.

### Backend

-   Unit tests for service and linguistic logic.
-   PostgreSQL integration tests.
-   API contract and validation tests.
-   Authorisation tests for write operations.

### Data pipeline

-   Importer tests using source fixtures.
-   Raw-file checksum and immutability checks.
-   Transformation and reconciliation tests.
-   Staging-to-application promotion tests.
-   Provenance and licence checks.

### Linguistic quality

-   Reviewed reference examples.
-   Held-out lemma evaluation.
-   Search tests with isiXhosa words and near-matches.
-   Manual review of representative senses, glosses and examples.

A successful technical import is not proof of linguistic correctness.

## 17. Repository Layout

The complete V1 repository is expected to contain:

``` text
umthombolwazi/
├── frontend/
├── backend/
├── data-engineering/
├── datasets/
│   ├── raw/
│   ├── staging/
│   └── processed/
├── database/
│   ├── documentation/
│   └── promotion/
├── docs/
│   ├── SOURCE_OF_TRUTH.md
│   ├── PRODUCT_VISION.md
│   └── V1_ARCHITECTURE.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

Do not commit downloaded raw datasets unless their licence and
repository policy explicitly permit it. Prefer keeping large or licensed
source files outside Git and recording acquisition instructions,
metadata and checksums in the repository.

## 18. V1 Delivery Plan

The order is deliberately data-first. We will not design the final
database around assumptions about datasets we have not inspected.

### Phase 0 --- Project Setup

Deliverables: - Private Git repository. - Source of Truth and Product
Vision documents in `docs/`. - This V1 architecture document in
`docs/`. - Initial README and `.gitignore`. - Agreed local development
environment.

### Phase 1 --- Dataset Acquisition and Profiling

Tasks: 1. Verify the current isiXhosa.click resource and permitted
download route. 2. Acquire a local copy and preserve it unchanged. 3.
Record its source version, licence, checksum and download date. 4.
Profile file formats, columns, encodings, counts, nulls, duplicates and
relationships. 5. Inspect example records manually. 6. Inspect NCHLT
lemma/POS resources and ctextcore. 7. Define and run the 50-token lemma
evaluation with development and held-out examples. 8. Inspect selected
SADiLaR and Autshumato resources.

Deliverables: - Source and licence register. - Dataset inventory. -
isiXhosa.click profile report. - Lemma evaluation report. - Initial
source-to-canonical mapping. - Unresolved data and linguistic questions.

**Exit gate:** We understand the structure and limitations of the first
datasets well enough to design the initial lexical model. The lemma tool
is either accepted for a clearly defined role or explicitly limited to
candidate generation.

### Phase 2 --- Canonical Knowledge Model

Tasks: 1. Define lexical entry, sense, gloss and form concepts. 2.
Decide how examples are represented based on actual source structures.
3. Define assertion-level origin and review status. 4. Define source,
source version and import batch. 5. Define typed claim-source and
review-event relationships. 6. Define contributor identity. 7. Define
licensing and publication metadata. 8. Validate the model against real
source records.

Deliverables: - Entity relationship diagram. - Data dictionary. -
Initial PostgreSQL schema design. - Import mapping specification. -
Review and provenance rules.

**Exit gate:** Representative source records can be mapped without
losing source meaning, identity or licensing information.

### Phase 3 --- Technical Foundation

Tasks: 1. Create the Expo React Native TypeScript application. 2.
Confirm Expo Web support for the intended V1 screens. 3. Create the
FastAPI application. 4. Configure PostgreSQL with Docker Compose. 5.
Configure SQLAlchemy and Alembic. 6. Add application configuration,
logging and health checks. 7. Add initial tests and CI checks. 8.
Establish protected write-operation foundations.

Deliverables: - App starts on iOS and web. - Android build/emulator
smoke test where practical. - API starts locally. - PostgreSQL runs
locally. - Database migrations run reproducibly. - Basic health check
works. - Client can call the API.

**Exit gate:** A working end-to-end skeleton exists: Expo client →
FastAPI → PostgreSQL.

### Phase 4 --- Data Ingestion

Tasks: 1. Implement source-specific acquisition/import adapters. 2.
Preserve raw data and checksums. 3. Create staging tables and loading
scripts. 4. Transform source records into the canonical model. 5.
Reconcile possible duplicates. 6. Validate records and licensing
metadata. 7. Promote through versioned, tested SQL. 8. Record import
batches, source links and review status. 9. Produce quality and import
reports.

Deliverables: - Repeatable import process. - Populated initial lexical
knowledge base. - Provenance traceability. - Reconciliation and
rejection reports.

**Exit gate:** A repeatable import can be run without corrupting raw
files or losing provenance.

### Phase 5 --- Core Backend API

Tasks: 1. Implement lexical entry retrieval. 2. Implement sense and
gloss retrieval. 3. Implement form and lemma lookup. 4. Implement
source/review metadata retrieval. 5. Implement exact and partial search.
6. Add English gloss search. 7. Evaluate approximate matching with
isiXhosa test data. 8. Add protected correction/review endpoints if the
review workflow is included in V1.

Deliverables: - Documented `/api/v1` endpoints. - API tests. - Search
quality report. - Consistent error and response structures.

**Exit gate:** The API supports all data required by the V1 client
experience.

### Phase 6 --- Client Application

Tasks: 1. Build the home/search experience. 2. Build search results. 3.
Build lexical entry detail. 4. Display senses and English glosses
correctly. 5. Display available forms, grammar, examples and provenance.
6. Build saved vocabulary if included. 7. Build settings/about and
data-status information. 8. Add correction submission UI if supported by
the backend. 9. Implement loading, empty, error and unavailable-data
states. 10. Test on iOS, Android where practical, and browser.

Deliverables: - Usable Expo mobile application. - Usable Expo Web
application. - Consistent API integration. - Responsive layouts and
basic accessibility checks.

**Exit gate:** A user can complete the core search-to-entry-detail
journey on a phone and in a browser.

### Phase 7 --- Offline Pack and Release Readiness

Tasks: 1. Confirm data licensing and publication eligibility. 2.
Implement versioned SQLite export. 3. Add FTS5 if search tests justify
it. 4. Include eligible form-to-lemma mappings. 5. Validate pack
integrity and licence metadata. 6. Integrate read-only offline pack
access into the client. 7. Test installation, update and failure
behaviour. 8. Complete security, backup, deployment and smoke-test
checklists.

Deliverables: - Offline knowledge pack if the gate is met. - Release
candidate. - Deployment and recovery notes. - V1 known-limitations list.

**Exit gate:** V1 is ready for controlled release. If offline licensing
or implementation is not ready, ship the online product first and
schedule offline packs as the next release.

## 19. Definition of Done for V1

V1 is complete when all of the following are true:

### Product

-   A user can access the app on a supported mobile platform.
-   A user can access the app in a desktop browser.
-   A user can search in isiXhosa and by English gloss.
-   Search results lead to useful lexical detail.
-   Multiple senses are displayed distinctly.
-   Available forms, examples and grammar are shown without inventing
    missing data.
-   Source and review labels are understandable.

### Data

-   Initial imported records are traceable to source versions and import
    batches.
-   Raw datasets are preserved.
-   Licence metadata is retained.
-   Review status applies at assertion level.
-   Imports can be repeated and tested.
-   Known data limitations are documented.

### Engineering

-   Client, API and database run in the documented development
    environment.
-   Migrations are reproducible.
-   Automated tests cover critical paths.
-   Write operations are protected.
-   Errors are handled consistently.
-   A backup and deployment procedure exists.

### Offline

-   If included in V1, the SQLite pack is versioned, licence-aware,
    validated and read-only.
-   If not ready, the online product is still releasable and offline
    delivery is explicitly scheduled after V1.

## 20. Key Risks and Controls

  -----------------------------------------------------------------------
  Risk                                Control
  ----------------------------------- -----------------------------------
  Imported data contains errors       Preserve source, label origin,
                                      validate and review assertions

  Conflicting definitions             Keep separate claims and evidence;
                                      do not destructively merge

  Poor lemma accuracy                 Held-out evaluation; use as
                                      candidate generator if below
                                      threshold

  Search normalisation damages        Test with isiXhosa examples;
  distinctions                        preserve original text

  Licence restrictions prevent        Track licence per
  redistribution                      source/version/content and gate
                                      exports

  V1 scope expands into AI content    Keep content products out of V1;
  generation                          consume core services later

  Expo Web limitations                Validate required web flows early;
                                      reassess only against concrete gaps

  Offline work delays release         Treat offline pack as gated; launch
                                      online first if necessary

  Solo-developer complexity           Modular monolith, three initial
                                      modules, defer abstractions
  -----------------------------------------------------------------------

## 21. Final V1 Architecture Statement

V1 is a complete client-and-server product built around a trusted
isiXhosa knowledge base.

It consists of a React Native and Expo application for mobile, Expo Web
for initial browser access, a FastAPI Modular Monolith, PostgreSQL, and
an independent Python data-engineering pipeline. The first backend
modules are `lexicon`, `sources` and `search`.

The development sequence begins with dataset acquisition and profiling,
then defines the canonical knowledge model, establishes the technical
foundation, imports and validates data, builds the API, completes the
client application, and prepares a controlled release.

The first version succeeds when people can reliably discover and
understand available isiXhosa lexical knowledge on a phone or in a
browser, with clear source information and honest representation of
uncertainty. The larger AI writing, content-creation, storytelling,
speech and multimedia ecosystem remains a future layer built on top of
this foundation.
