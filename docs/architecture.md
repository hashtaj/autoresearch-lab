# VisualResearcher Architecture Note

## High Level Concept
This repository is a wrapper around the upstream `karpathy/autoresearch` repository, which operates as a minimal self-contained AI research loop relying on simple scripts (`prepare.py`, `train.py`, etc.).
The goal of this wrapper is to retain the original experiment loop unchanged while building a robust control plane (backend) and observability layer (frontend) around it.

## Scaffolded Components

### 1. Core Experiment Engine (Upstream)
- `train.py`, `prepare.py`, `program.md`, `pyproject.toml`
- Remains untouched so updates from upstream can be smoothly merged.

### 2. Backend (`app/backend/`)
- A minimal FastAPI server placeholder.
- **Claude Code TODO:** Implement `runner.py` to orchestrate `train.py`.
- **Claude Code TODO:** Build `experiment_store.py` (SQLite) to log outputs and code diffs.
- **Claude Code TODO:** Configure `arize_logger.py` for LLM tracing via Phoenix / Arize.

### 3. Frontend (`app/frontend/`)
- A minimal Next.js scaffold.
- **Claude Code TODO:** Develop the actual UI wrapper. Needs visual timelines, config editors, and charting of experiment metrics.
