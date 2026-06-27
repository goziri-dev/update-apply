# UpdateApply — Top-Down Design

## Product Overview

UpdateApply is a platform that automates the resume tailoring process for job seekers. It connects to users' work-related repositories and documents to extract context — such as skills, experiences, contributions, and achievements — and uses that context to match users to relevant jobs and generate tailored resumes for each application.

## User Flow

1. **Connect** — The user links their work repositories (e.g., Google Drive, Notion, GitHub) where they store work-related files and documents.
2. **Extract** — The system reads and processes data from these files to build a rich profile of the user's skills, experiences, contributions, and achievements.
3. **Match & Generate** — The system intelligently matches the user to suitable job openings and generates a tailored resume for each position.

## Core Features

### 1. Provider Connection & Syncing
Connect to user repository providers — including Google Drive, Notion, and GitHub — to access files and documents stored across platforms.

### 2. Repository Traversal, Filtering & File Extraction
Traverse user repositories, filter relevant files, and extract structured data that serves as context for matching and resume generation.

### 3. Smart Job Recommendation & Matching
Intelligently match users to job openings by analyzing both the job requirements and the user's extracted skills and experience.

### 4. Resume Tailoring System
Understand job requirements and dynamically tailor the user's resume to align with each specific role.

## Data Model

### User Job Profile
- First and last name
- Location (current and preferred work location)
- Email and phone number
- Education and work experience
- Work-related files and documents
- Honors and awards
- Social and personal website links

### Job Postings & Listings
- Company name, URL, and location
- Job title, description, and salary

## High-Level Architecture

### Tech Stack
- **Frontend:** Next.js
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (relational data) + pgvector (vector embeddings for RAG)

### Service Architecture

The backend is a single **FastAPI service** with an **async task queue** (e.g., Celery, Redis Queue, or FastAPI `BackgroundTasks`). This keeps the fast path responsive while offloading slow work to background workers.

```
┌─────────────────────────────────────────────┐
│              FastAPI Backend                │
│                                             │
│  ┌──────────────┐  ┌─────────────────────┐  │
│  │  REST API    │  │  Task Workers       │  │
│  │  (sync)      │  │  (async)            │  │
│  │  • CRUD      │  │  • Document parsing │  │
│  │  • Matching  │  │  • Resume gen       │  │
│  └──────┬───────┘  └──────────┬──────────┘  │
│         │                     │             │
│         └─────────┬───────────┘             │
│                   │                         │
│          ┌────────▼────────┐                │
│          │  PostgreSQL     │                │
│          │  + pgvector     │                │
│          └─────────────────┘                │
└─────────────────────────────────────────────┘
```

If later traffic or resource demands prove that certain workloads need independent scaling, workers can be extracted into standalone services.

### Communication
- **Frontend → Backend:** REST
- **Sync requests** (CRUD, matching) return immediately.
- **Async tasks** (document parsing, resume generation) are queued to workers. The client polls or receives a callback when the task completes.

### Authentication
- **User Identity:** Clerk handles basic user authentication on the frontend.
- **Provider OAuth:** GitHub, Google Drive, and Notion are authenticated via their respective OAuth flows, also initiated from the frontend.
- **Token Storage:** JWT/OAuth tokens are stored in the database. Services read the stored tokens when pulling data from provider APIs on behalf of the user.

### AI / Matching Strategy
- **Job Matching:** Synchronous. Uses fuzzy keyword matching between the user's extracted skills and the skills listed in job descriptions. No LLM required.
- **Resume Tailoring:** Async. Uses RAG to retrieve relevant context from the user's profile and job description, feeds both to an LLM, which generates a tailored resume as structured HTML. The backend then converts the HTML to a downloadable PDF.

## Data Flow

### Phase 1 — Provider Connection & Token Storage

```
User clicks "Connect GitHub/Google Drive/Notion"
        │
        ▼
Frontend initiates provider OAuth flow
        │
        ▼
User authorizes the application
        │
        ▼
Frontend receives provider JWT/tokens
        │
        ▼
Backend encrypts tokens and stores them in PostgreSQL
```

### Phase 2 — File Retrieval & Processing

```
Backend reads stored tokens for the user
        │
        ▼
Worker hits provider API with the user's token
        │
        ▼
Pulls user's files and documents
        │
        ▼
Filters for meaningful file types only:
  ✅ .md, .docx, .py, .txt, .pdf, .json, .yaml, .csv
  ❌ .png, .jpg, .mp4, .exe (binary/unstructured files)
        │
        ▼
Extracts raw text from each accepted file
        │
        ▼
Calls LLM/AI to derive structured context
(skills, experiences, projects, achievements)
        │
        ▼
Generates vector embeddings from the extracted context
        │
        ▼
Stores embeddings in pgvector + structured data in PostgreSQL
```

### Phase 3 — Job Listing Ingestion

```
Scheduled job (or on-demand) fetches recent job postings
        │
        ▼
Job listings API returns job data
        │
        ▼
For each job listing:
  ├── Store structured data in PostgreSQL
  │     (title, company, description, salary, etc.)
  └── Vectorize job description
        │
        ▼
Store job description embeddings in pgvector
```

### Phase 4 — Job Matching

```
Trigger: user requests matches or background schedule
        │
        ▼
Load user's skills & experience from PostgreSQL
        │
        ▼
Load all active job listings
        │
        ▼
Fuzzy keyword match: user skills ↔ job listed skills
        │
        ▼
Score and rank matches
        │
        ▼
Store results as job_recommendations → display to user
```

### Phase 5 — Resume Generation

```
User selects a job match → clicks "Generate Resume"
        │
        ▼
POST /api/resume/generate → enqueues async task
        │
        ▼
RAG retrieval:
  ├── Relevant user context from pgvector
  └── Job description + requirements from pgvector
        │
        ▼
LLM generates a tailored resume in structured HTML
        │
        ▼
Backend converts HTML → PDF
        │
        ▼
PDF stored in PostgreSQL / file storage
        │
        ▼
User is notified → downloads or edits the resume
```

### End-to-End Flow Diagram

```
┌──────────┐   ┌────────────────────────────────────────────────────────┐
│  User    │   │                 FastAPI Backend                        │
│ (Next.js)│   │                                                        │
│          │   │  ┌──────────────────┐   ┌──────────────────────────┐   │
│  OAuth   │───┼─►│  REST API        │   │  Task Workers (async)    │   │
│  Flow    │   │  │  (sync)          │   │                          │   │
│          │   │  │  • CRUD          │   │  • Pull files from       │   │
│  Poll    │◄──┼──│  • Get matches   │   │    providers             │   │
│  status  │   │  │  • Trigger gen   │   │  • Parse & extract text  │   │
│          │   │  └────────┬─────────┘   │  • AI context extraction │   │
│  Download│   │           │             │  • Embedding generation  │   │
│  PDF     │◄──┼───────────┼─────────────│  • Resume generation     │   │
│          │   │           │             │  • HTML → PDF conversion │   │
│          │   │           │             └──────────┬───────────────┘   │
│          │   │           │                        │                   │
│          │   │           └────────────┬───────────┘                   │
│          │   │                        │                               │
│          │   │               ┌────────▼────────────────┐              │
│          │   │               │  PostgreSQL + pgvector  │              │
│          │   │               │                         │              │
│          │   │               │  • Encrypted OAuth JWTs │              │
│          │   │               │  • User profile (struct)│              │
│          │   │               │  • Extracted context    │              │
│          │   │               │  • Job listings + desc  │              │
│          │   │               │  • Vector embeddings    │              │
│          │   │               │  • Generated resumes    │              │
│          │   │               └─────────────────────────┘              │
│          │   └────────────────────────────────────────────────────────┘
│          │
│  ┌───────▼──────────┐
│  │  External         │
│  │  Providers        │
│  │                   │
│  │  • GitHub API     │
│  │  • Google Drive   │
│  │  • Notion API     │
│  │  • Job Listings   │
│  └───────────────────┘
```

## External APIs

1. **Job Listings API** — Fetches recent and legitimate job postings. E.g. Adzuna, TechMap, TheirStack
2. **Repository Provider APIs** — Integrates with GitHub, Google Drive, Notion, and similar services for file access.