# Open Banking Solutions (OBS) — Company Context

You are working inside Open Banking Solutions (OBS), a fintech startup. This context is **always true** and should inform every decision, code review, naming convention, and architectural choice.

## Company Overview

OBS is a small fintech startup bringing a Core Banking System (CBS) to the US market from Latin America. OBS operates as a **datacenter** hosting multiple Banks and Credit Unions (collectively "Financial Institutions" or "FIs"). Systems fall into two categories:

1. **Per-FI systems** — wrapped around the CBS for each individual financial institution
2. **Shared datacenter systems** — supporting all FI clients centrally

## Core Banking System (CBS)

### Backend — Oracle on OCI
- **Database**: Oracle, hosted on **Oracle Cloud Infrastructure (OCI)**
- **Primary schema**: `DUSBRID_TRANS` — translated from the original Spanish `DUSBRID` schema to English
- **Translation status**: ~97% converted to English; residual Spanish naming exists in places
- **Oracle Thick Client** is required for OCI database connectivity
- **Spanish Wrappers**: The original Spanish-named stored procedures, functions, packages, tables, and views were preserved as wrappers pointing to the new English equivalents. This was necessary because the CBS was part of a multi-product suite. The wrappers use original `DUSBRID` names and parameter signatures but call the English code underneath. Spanish views wrap the English tables/views with original `DUSBRID` names.

### Frontend — Oracle APEX
- **Current UI**: Oracle APEX (~40% of original screens migrated)
- **Previous UI**: Oracle Forms and Reports (legacy; XML exports are used for reference)
- **APEX labelling**: Mostly English, but **APEX application code is still in Spanish**
- **APEX calls**: Primarily invoke the Spanish Wrappers, which then execute the English code

### Origination System (Account & Person Opening)
- Intended as a separate module, but Oracle components reside **directly in `DUSBRID_TRANS`** and cannot easily be separated
- Object naming is cryptic: tables like `A0001`, `C0123` with columns that embed the origin table name followed by Spanish abbreviations of very few characters
- Extremely difficult to understand without deep institutional knowledge

### Customer-Facing Mobile & Web — CFG
- **Schema**: `CFGUSER` (Oracle)
- **Mobile apps**: Built with **Ionic** (platform-agnostic)
- **Backend server**: **Spring Boot / Java 8**
- **Language**: Spanish (original Latin American CBS)

### Business Intelligence — SMART
- Written in Spanish
- Uses **Microsoft SQL Server** flavor
- **Not yet in use**, no translation attempts made

### Collections System
- May use **GeneXus** platform
- **Not yet in use**, no translation attempts made

## The Midgard Ecosystem (OBS-Built Infrastructure)

Midgard is a suite of middleware and infrastructure applications built by OBS to connect community banks and FIs to external payment networks, card processors, and internal operations. The core platform provides:

- **Shared authentication** (JWT / RBAC)
- **Quantum-safe encrypted Oracle connectivity** ("Bifrost Bridge")
- **Centralized FI management**
- **Tech stack**: Python / FastAPI, PostgreSQL, React
- **Deployment**: Docker, Oracle Kubernetes Engine (OKE)
- **Shared security**: All "-gard" projects use Midgard's auth via the `midgard-client` package
- **Integrated services**: Gitea, OCIR (Oracle Container Image Registry)

### Project Portfolio

| Project | Description | Status |
|---------|-------------|--------|
| **midgard** | Core platform — auth, RBAC, Bifrost Bridge (Oracle connections), FI registry, admin UI. FastAPI + React. | ~75% complete |
| **atmgard** | ATM/debit card transaction middleware — ISO 8583, Shazam/Lithic adapters, PCI-scoped. FastAPI + Oracle. | ~90% complete |
| **achgard** | ACH payment processing — NACHA file generation, FedACH, Cloud Core posting. Next.js + FastAPI. | Active development |
| **nightgard** | Batch job orchestration — replaces legacy nightly schedulers. FastAPI + Celery + Redis. | Early build |
| **oragard** | Oracle DBA toolkit — RMAN backup/restore, database discovery, clone operations. Flask + OCI SDK. | Prototype with functional UI |
| **apigard** | CBS API middleware — FastAPI layer over Oracle Core Banking for GenAspire/MuleSoft integration. | Scaffolding complete |
| **asgard** | CBS UI modernization factory — migrates Oracle APEX/Forms screens to React + FastAPI with AI-assisted translation. | Phase 0 done |
| **coregard** | Oracle schema translation — modernizes legacy DUSBRID_TRANS schemas to English-named OBS/ORIG equivalents. | In progress |
| **aigard** | MCP server consolidation — unifies AI tooling (RAG, Oracle, MediaWiki, research) into a single Docker service. | In progress |
| **chatgard** | Sibling workspace to aigard for MCP consolidation work. Same scope. | In progress |
| **obs-oci-infra** | OCI infrastructure-as-code — Terraform for OKE clusters, container registry, networking. | Operational |

## Key Technical Facts

- Oracle databases in OCI require the **Oracle Thick Client**
- The `database-standards` skill defines OBS naming conventions for Oracle PL/SQL, MySQL, and PostgreSQL
- Python projects use **UV** for virtual environment management
- All "-gard" projects share Midgard's JWT/RBAC auth infrastructure
- Legacy Spanish code is progressively being translated/modernized — expect to encounter Spanish identifiers, comments, and variable names in Oracle code
