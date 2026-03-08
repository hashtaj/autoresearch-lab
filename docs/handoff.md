# Claude Code Handoff

Welcome to the **VisualResearcher** project. This repository is a wrapper around the upstream `karpathy/autoresearch` repository, which has been preserved in the root. The goal is to build an observability and control wrapper around it.

## What has been scaffolded
- The original `autoresearch` files (`train.py`, `prepare.py`, `program.md`, `pyproject.toml`) have not been touched.
- **Backend Scaffold:** Located in `app/backend/`. Contains placeholders for `main.py`, `runner.py`, `experiment_store.py`, and `arize_logger.py`.
- **Frontend Scaffold:** Located in `app/frontend/`. Contains a minimal piece of Next.js architecture (Layout, Page, Package.json).
- **Scripts:** `scripts/bootstrap.sh` and `scripts/dev.sh`.
- **Docker & Config:** `docker-compose.yml` and `.env.example` exist.

## What Claude Code needs to do next
1. **Flesh out the Backend:** Use FastAPI. 
   - Build endpoints in `main.py`.
   - Complete `runner.py` to correctly fork/call `train.py` or interface with its main logic without rewriting the core loop.
   - Build out `experiment_store.py` with actual SQLite logic for saving run metadata, tracking state, and storing diff outputs.
   - Integrate Phoenix / Arize telemetry in `arize_logger.py` to trace the upstream LLM outputs.
   
2. **Build the Frontend Wrapper:**
   - Expand `app/frontend`. Next.js with React components.
   - Build a timeline UI, configuration editors for `program.md`, and visualizations (charts, outputs).
   - Integrate the frontend with the FastAPI backend.

Remember: Do NOT refactor the core `train.py` unless strictly necessary for hooking into the loops. Prefer to observe strings output or augment minimal wrappers.
