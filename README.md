<div align="center">

# Strategic Engine

### The AI Decision Operating System for High-Performance Organizations

*Companies don't fail because of bad strategies. They fail because decisions made in meetings never become execution.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini 1.5 Pro](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-6366f1?style=flat-square)](LICENSE)

</div>

---

## The Problem Worth Solving

Every organization runs on decisions. Decisions made in meetings, over calls, in rooms where someone said *"we're doing X"* and everyone nodded — and then nothing happened, or the wrong thing happened, or three weeks later the same decision was made again because nobody wrote it down clearly the first time.

**The cost of this is not trivial.**

- The average knowledge worker attends 18+ hours of meetings per week.
- Studies estimate that 67% of decisions made in meetings are either forgotten, reassigned, or quietly abandoned within 72 hours.
- Organizations with 200+ employees lose an estimated $2.5M annually to misaligned direction and execution failure that originates in meetings.

Existing tools don't fix this. Note-takers capture text. Project managers chase tasks. AI summarizers produce readable prose. None of them tell you which decision is about to fail, who is most likely to drop something critical, or that the commitment made today directly contradicts one made last month.

**Strategic Engine does.**

---

## What Strategic Engine Is

Strategic Engine is an **AI Decision Operating System** — a structured intelligence layer that sits between what your team *discusses* and what your organization *executes*.

It processes meeting transcripts and returns not just a summary, but a full organizational intelligence report: every decision extracted and confidence-scored, every task weighted by failure probability, every risk triaged with a prevention strategy, and every pattern in your organization's decision-making history made visible.

It is purpose-built to answer the questions that matter to leadership:

> *What was formally decided — and how clear was it?*
> *Which commitments are likely to fail, and why?*
> *Where are the ownership gaps nobody is talking about?*
> *Is today's direction consistent with last month's strategy?*

This is not a productivity tool. It is an execution intelligence system.

---

## How It Works

```
INPUT        →  Transcript text or structured file (.txt / .csv)
VALIDATION   →  Token volume, quality, and format verification
ANALYSIS     →  Gemini 1.5 Pro processes full context using chain-of-thought extraction
EXTRACTION   →  Decisions, tasks, risks, and next steps scored against a structured schema
PERSISTENCE  →  Intelligence stored as a relational decision graph — not flat text
DASHBOARD    →  Executive Command Center surfaces insights across all historical sessions
```

Each pipeline stage is **isolated, logged, and fault-tolerant**. Failures surface as structured errors with full diagnostic context. The system never crashes silently.

---

## Core Capabilities

### Decision Intelligence Engine

Most conversations produce vague direction. Strategic Engine surfaces what was *actually committed to*.

- Extracts every formal decision from unstructured conversation
- Assigns a **Confidence Score (0–100)** per decision based on linguistic clarity and explicitness
- Detects **Ambiguous Mandates** — commitments lacking ownership, timeline, or method — and flags them as execution risks before they become missed deliverables
- Classifies **Impact Level**: `Critical` / `High` / `Medium` / `Low`
- Tracks decision lifecycle: `Active` → `Executed` → `Stale` → `Conflict`

The result is a decision matrix you can act on, not a narrative you have to parse.

---

### Predictive Execution Risk

The system doesn't just record what needs to happen. It tells you what is likely to *not* happen.

- Extracts every action item with owner attribution and deadline inference
- Assigns a **Failure Probability (0–100%)** per task, derived from assignment clarity, deadline specificity, and contextual complexity
- Identifies **Structural Bottlenecks** — tasks dependent on overloaded owners or unresolved upstream decisions
- Surfaces the highest-risk items first, so attention goes where it's needed most

This is early-warning infrastructure for execution, not a to-do list.

---

### Strategic Risk Detection

Risks stated in meetings are only part of the problem. The other part is what the conversation implies but never names.

- Detects implicit risks embedded in discussion — dependency exposure, ownership voids, timeline compression
- Classifies severity: `Critical` / `Moderate` / `Low`
- Generates a **Prevention Strategy** for each identified risk — concrete, contextual, and actionable
- Paired with task failure predictions to surface compounding risk vectors

---

### Organizational Memory

Every meeting is a data point. Treated in isolation, it has limited value. Treated as part of a continuous organizational record, it becomes strategic intelligence.

- All extracted intelligence persists as structured, queryable data — not archived text
- Decision history is tracked across all sessions, enabling longitudinal pattern detection
- Foundation for cross-meeting reasoning: the system can detect when today's decision contradicts one made weeks earlier
- The longer it runs, the more valuable it becomes

---

### Executive Command Center

The dashboard is designed around the information needs of people who make decisions, not people who track tasks.

- **Strategic Impact Score (0–100)**: quantified measure of the meeting's organizational significance
- **Sentiment Navigator**: `Positive` / `Neutral` / `Contention` / `Negative` — the emotional temperature of the room
- **Decision Matrix**: filterable, cross-session view of all decisions with confidence and impact metadata
- **Predictive Workload Risk**: visual distribution of failure risk by assignee — surface who is overloaded before they miss a deadline

---

### Self-Healing Infrastructure

Production systems fail on schema drift. Strategic Engine is built to absorb it.

- On every startup, the database engine performs a **deep schema inspection** — comparing live SQLite/PostgreSQL schema against SQLAlchemy model definitions
- Missing columns are automatically injected via `ALTER TABLE` — zero downtime, no data loss, no manual migration scripts
- A global error handler intercepts any `OperationalError` that escapes the boot sequence and surfaces a clean recovery interface instead of a crash
- The system validates schema integrity before any user-facing query executes

Add a new field to any model. Restart the app. It works.

---

## Business Impact

| Organizational Cost | How Strategic Engine Eliminates It |
|---|---|
| Decisions made but never recorded formally | Every decision extracted, scored, and persisted automatically |
| Commitments dropped between meeting and execution | Failure Probability flagged per task before it misses its deadline |
| Duplicate direction — same decision made twice | Cross-session memory detects contradictions across meetings |
| Ownership gaps that nobody claims | Ambiguity detection flags every commitment without a clear owner |
| Hours spent writing meeting recaps | Full structured report generated in seconds, requiring zero manual effort |
| Risk identified only after it materializes | Prevention strategies surfaced at the moment of extraction |

---

## Who This Is Built For

### Leadership & Executive Teams
Organizations where misaligned direction is expensive. Strategic Engine gives leadership a continuous, structured audit trail of every commitment made — not a filtered summary written by the person who called the meeting.

### Product & Engineering Organizations
Teams running agile cycles where technical decisions compound rapidly. Track architectural commitments, unresolved dependencies, and sprint-level execution risk across every planning session.

### High-Growth Startups
Speed creates gaps. Strategic Engine closes the gap between `discussed in a meeting` and `reflected in the sprint board` without adding process overhead.

### Consulting & Professional Services
Client decisions generate liability. Every engagement produces a time-stamped, machine-readable record of what was agreed, who owns it, and where the risk sits.

### Boards & Investor Relations
Board-level decisions carry governance weight. Strategic Engine creates a structured, auditable decision record that holds every commitment to the same standard.

---

## Technology Architecture

| Layer | Technology | Rationale |
|---|---|---|
| **AI Engine** | Gemini 1.5 Pro | 2M token context window; native structured JSON extraction via chain-of-thought prompting |
| **Backend** | FastAPI (Python) | Async-first, type-safe, production-ready; built for API-first evolution |
| **ORM** | SQLAlchemy 2.0 | Declarative models with full relationship mapping and runtime introspection |
| **Database** | SQLite → PostgreSQL | Local-first development with a production migration path requiring zero schema changes |
| **Schema Management** | Custom self-healing engine | Runtime `ALTER TABLE` injection; no Alembic dependency in development |
| **Frontend** | Streamlit + Custom CSS | Linear-inspired design system; premium component library with predictive risk indicators |
| **Architecture** | Service-oriented monolith | `models → crud → ai_service → api → ui`; clean separation ready for microservice extraction |

---

## Roadmap — From Intelligence to Autonomy

Strategic Engine v1 converts meetings into decision intelligence. The roadmap converts decision intelligence into autonomous organizational action.

### Phase 2 — Organizational Intelligence Graph
Replace the flat relational model with a **Neo4j property graph**. Every employee, task, and decision becomes a node. Every relationship — `OWNS`, `BLOCKS`, `CONTRADICTS`, `DEPENDS_ON` — becomes a queryable edge. The system surfaces hidden bottlenecks, identifies who *actually* drives organizational decisions (versus who appears on the org chart), and detects single points of failure before they trigger.

### Phase 3 — Cross-Meeting Reasoning (RAG)
Integrate **vector embeddings** (Pinecone / Qdrant) to give the AI a persistent, semantic memory across all sessions. When a new meeting is analyzed, the system retrieves relevant historical context and injects it into the analysis pass. If today's direction contradicts a decision made six weeks ago, the system flags it — automatically.

### Phase 4 — Hidden Pattern Intelligence
Move beyond what was said to what the conversation reveals. Detect unclaimed ownership, passive disagreement patterns, repeated unresolved topics, and structural team misalignment — none of which appear explicitly in the transcript but all of which are recoverable from the signal. Output as named, categorized alerts: *"No clear ownership detected in 3 consecutive sessions on this workstream."*

### Phase 5 — Voice & Emotion Layer
Process audio natively via Gemini's multimodal pipeline. Overlay tone, confidence level, and stress signals onto the meeting timeline. Distinguish between a decision that was agreed on enthusiastically and one that was agreed on reluctantly — because those produce very different execution outcomes.

### Phase 6 — Autonomous Execution Layer
The AI drafts Jira tickets, Slack messages, and Notion pages directly from extracted mandates. Human-in-the-loop confirmation required before any external write. The system handles the operational translation between *what was decided* and *what needs to be created* — which is currently done manually at significant cost.

### Phase 7 — Multi-Tenant SaaS Platform
Full workspace isolation with row-level PostgreSQL security, role-based access control (`Admin / Manager / Member`), Stripe billing integration, and WebSocket-based real-time collaboration. The architecture is designed for this transition from day one.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Gemini API Key — [Generate here](https://makersuite.google.com/app/apikey)

### Install

```bash
git clone https://github.com/your-org/strategic-engine.git
cd strategic-engine

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### Configure

```env
# .env
GEMINI_API_KEY=your_key_here
DATABASE_URL=sqlite:///strategic_engine.db
DEV_MODE=True
```

### Run

```bash
cd app
streamlit run main.py
```

On first launch, the system initializes the database, runs a full schema integrity check, applies any outstanding structural migrations, and opens the Executive Command Center. No manual setup required.

---

## Project Structure

```
strategic-engine/
├── app/
│   ├── main.py             # Application entry point, view router, global error handler
│   ├── ai_service.py       # AI orchestration, prompt engineering, structured extraction
│   ├── models.py           # SQLAlchemy ORM — Decision Intelligence schema
│   ├── crud.py             # Data access layer — decisions, tasks, risks, memory
│   ├── db.py               # Self-healing database engine — runtime schema repair
│   ├── ui_components.py    # Decision cards, risk indicators, executive dashboard components
│   ├── config.py           # Environment resolution and configuration validation
│   └── styles.css          # Linear-inspired design system, CSS custom properties
├── migrate.py              # Idempotent standalone migration CLI
├── requirements.txt
└── .env
```

---

## Competitive Position

| Capability | Meeting Summarizers | Task Managers | Strategic Engine |
|---|---|---|---|
| Extracts decisions with confidence scoring | ✗ | ✗ | ✓ |
| Predicts task failure before it happens | ✗ | ✗ | ✓ |
| Detects ambiguous ownership | ✗ | ✗ | ✓ |
| Generates risk prevention strategies | ✗ | ✗ | ✓ |
| Cross-session organizational memory | ✗ | Partial | ✓ |
| Self-healing schema management | N/A | N/A | ✓ |
| Forward-looking execution intelligence | ✗ | ✗ | ✓ |

Tools like Otter, Fathom, and Fireflies tell you what was said.  
Tools like Jira and Linear tell you what was planned.  
**Strategic Engine tells you what was truly decided, what is at risk of failing, and where your organization's execution is structurally weak.**

These are different problems. This is a different product.

---

<div align="center">

**Strategic Engine is the intelligence layer between what organizations discuss and what they actually execute.**

*Built to replace the gap. Designed to scale to a category.*

</div>
