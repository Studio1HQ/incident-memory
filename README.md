<div align="center">

<img src="https://raw.githubusercontent.com/Studio1HQ/Studio1HQ/main/assets/banners/incident-memory.webp" alt="Incident Memory with ByteRover and Claude Code: Capture a payment bug fix as queryable context with ByteRover" width="100%" />

<br />
<br />

# Incident Memory with ByteRover and Claude Code

### Capture a payment bug fix as queryable context with ByteRover

A small FastAPI payment service with a deliberate double-credit bug, used to show how ByteRover and Claude Code analyze, fix and document an incident so the knowledge is available at coding time.

<br />

[![Built by Studio1](https://img.shields.io/badge/Built_by_Studio1-f97316?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNjAgMTYwIiBmaWxsPSJub25lIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTAgMzVDMCAxNi42ODA3IDE0LjA3NDQgMS42NDg0NCAzMiAwLjEyNjk1M1YxNDFINTEuMDUyM0M1Mi40MzA4IDEzNy4zNDQgNTQuNzQ0NiAxMzMuNjg5IDU3Ljk5MzggMTMwLjAzM0M2MS4xNDQ2IDEyNi41MDggNjQuNjg5MiAxMjMuNDQgNjguNjI3NyAxMjAuODI5QzcyLjU2NjIgMTE4LjM0OSA3Ni4zNTY5IDExNi43ODIgODAgMTE2LjEyOVY4Ni43NTQ0Qzc1LjQ3MDggODcuOTI5MiA3MS4zODQ2IDg5LjY5MTkgNjcuNzQxNSA5Mi4wNDE1QzY0IDk0LjUyMjUgNjAuNzUwOCA5Ny40NiA1Ny45OTM4IDEwMC44NTRDNTYuNTM0NSAxMDIuNzIgNTUuMjU0NSAxMDQuNjU5IDU0LjE1MzkgMTA2LjY3MVYwSDEyNUMxNDQuMzMgMCAxNjAgMTUuNjY5OSAxNjAgMzVWMTI1QzE2MCAxNDQuMzMgMTQ0LjMzIDE2MCAxMjUgMTYwSDEyNFYxOEgxMDQuOTQ4QzEwMy41NjkgMjEuNjgxNiAxMDEuMjU1IDI1LjM2MjggOTguMDA2MiAyOS4wNDQ0Qzk0Ljg1NTQgMzIuNTk0MiA5MS4zMTA4IDM1LjY4NDEgODcuMzcyMyAzOC4zMTRDODMuNDMzOCA0MC44MTIgNzkuNjQzMSA0Mi4zODk2IDc2IDQzLjA0NzRWNzIuNjMwNEM4MC41MjkyIDcxLjQ0NzMgODQuNjE1NCA2OS42NzI0IDg4LjI1ODUgNjcuMzA1N0M5MiA2NC44MDc2IDk1LjI0OTIgNjEuODQ5MSA5OC4wMDYyIDU4LjQzMDdDOTkuNDY1NSA1Ni41NTEzIDEwMC43NDUgNTQuNTk4NiAxMDEuODQ2IDUyLjU3MjNWMTYwSDM1QzE1LjY3IDE2MCAwIDE0NC4zMyAwIDEyNVYzNVoiIGZpbGw9IiNmZmZmZmYiLz48L3N2Zz4K)](https://studio1hq.com)
[![Built with ByteRover](https://img.shields.io/badge/Built_with_ByteRover-141414?style=for-the-badge)](https://byterover.dev)

[ByteRover docs](https://docs.byterover.dev) &nbsp;·&nbsp; [ByteRover](https://byterover.dev) &nbsp;·&nbsp; [More examples](https://github.com/Studio1HQ) &nbsp;·&nbsp; [studio1hq.com](https://studio1hq.com)

</div>

<br />

## Overview

This repo shows how to capture incident knowledge inside a codebase with [ByteRover](https://byterover.dev) and Claude Code. It uses a deliberately flawed FastAPI payment service: a rollback operation credits user balances but is not idempotent, so retries cause duplicate credits.

The workflow is to analyze the code, document it, reproduce and fix the bug, store the incident as structured context, and then query that context before changing related code. The point is that a postmortem is present when code is written, not only afterwards.

## Features

- **Codebase curation**: `brv curate` has Claude generate structured documentation from the code alone: overview, entry points, execution paths, shared state, bug analysis and a demo workflow.
- **Reproducible bug**: `demo.py` drives the API through a charge that fails, is rolled back and is retried, which triggers the double credit.
- **Idempotent fix**: an idempotency guard, enforced state transitions and no duplicate balance updates, with rollout and reconciliation steps documented.
- **Queryable memory**: `brv query` returns the original bug, why it happened, the approved pattern, code references and rollout constraints.
- **Context next to code**: the generated context tree lives in `.brv/context-tree/` in the repo.

## Tech stack

| Layer | Tool |
| --- | --- |
| Context and memory | [ByteRover](https://byterover.dev) CLI |
| Coding agent | [Claude Code](https://www.anthropic.com/claude-code) |
| Service | [FastAPI](https://fastapi.tiangolo.com) and Uvicorn |
| Language | Python 3.10 or later |

## Getting started

### Prerequisites

- Python 3.10 or later
- ByteRover CLI, installed and authenticated
- Claude Code with the ByteRover integration
- Basic familiarity with FastAPI

### Installation

```bash
git clone https://github.com/Studio1HQ/incident-memory.git
cd incident-memory
pip install -r requirements.txt
```

### Run

Start the service, then run the demo script that reproduces the bug:

```bash
uvicorn app.main:app --port 8000
python demo.py
```

`demo.py` calls `http://127.0.0.1:8000` and uses the `/charge`, `/charge/{id}/confirm` and `/charge/{id}/rollback` endpoints. The service also exposes `/charge/{id}/refund`.

## How it works

```text
app/
  main.py             FastAPI app
  api/routes.py       charge, confirm, rollback, refund routes
  payment/service.py  bug and fix location
  payment/store.py    in-memory state
  payment/models.py   data models
demo.py               reproduces the failure
CLAUDE.md             ByteRover workflow rules for the agent
.brv/context-tree/    generated context: structure, api_design, business_logic, bug_fixes, testing
```

The workflow, step by step:

1. **Initialize**: `brv init` creates ByteRover rules and enables context capture.
2. **Curate**: `brv curate` has Claude analyze the repository and write structured documentation based only on code behavior.
3. **Sync**: `brv push` publishes the context so future engineers and agents can query it.
4. **Fix**: the prompt used was: "Using the existing ByteRover context and current codebase, design and implement a correct, idempotent fix for the double-credit bug, explain why previous behavior failed, update the code accordingly, and document the approved fix and rollout considerations as markdown."
5. **Commit**: the fix is committed so code and context evolve together.
6. **Prevent**: before writing code, a future engineer asks:

```bash
brv query "What patterns should I follow when modifying user balances in payment operations?"
```

The exact layout of the generated documentation is decided by ByteRover and may change.

This is aimed at backend engineers on critical systems, platform teams supporting AI coding agents, and anyone evaluating ByteRover for institutional memory.

## Resources

- [ByteRover](https://byterover.dev): the context and memory product used here.
- [ByteRover docs](https://docs.byterover.dev): CLI commands such as `brv init`, `brv curate`, `brv push` and `brv query`.

<br />

---

<div align="center">

<a href="https://studio1hq.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Studio1HQ/website/main/brand/studio1-logo-on-dark.svg" />
    <img src="https://raw.githubusercontent.com/Studio1HQ/website/main/brand/studio1-logo-on-light.svg" alt="Studio1" width="160" />
  </picture>
</a>

Built by **[Studio1](https://studio1hq.com)**, the technical content and DevRel partner for devtool teams. Made with [ByteRover](https://byterover.dev).<br />
Browse more open-source examples at [github.com/Studio1HQ](https://github.com/Studio1HQ).

[![Website](https://img.shields.io/badge/studio1hq.com-0b0807?style=for-the-badge&logo=googlechrome&logoColor=white)](https://studio1hq.com)
[![Book a call](https://img.shields.io/badge/Book_a_strategy_call-f97316?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://cal.com/studio1/collab)
[![X](https://img.shields.io/badge/%40Studio1HQ-141414?style=for-the-badge&logo=x&logoColor=white)](https://x.com/Studio1HQ)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/studio1hq/)

<sub><a href="https://studio1hq.com">studio1hq.com</a> · Technical content, docs, video and DevRel for devtools</sub>

</div>
