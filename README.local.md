# VisualResearcher (autoresearch fork)

This repository is a wrapper around the original [karpathy/autoresearch](https://github.com/karpathy/autoresearch) repository.
The core upstream files (`train.py`, `prepare.py`, `program.md`, `pyproject.toml`) have been kept clean and separated at the root so that merging future upstream changes remains straightforward.

## Scaffolded Structure

- `app/backend/`: FastAPI skeleton logic for managing runs, interacting with SQLite, logging telemetry via Phoenix/Arize, and orchestrating the upstream `train.py`.
- `app/frontend/`: Next.js skeleton structure designed to serve as the user interface, visualizing timelines and graphs over the experiment loop.
- `docs/`: Setup notes, architecture overviews, and a detailed Handoff note for Claude Code.
- `scripts/`: Local dev and bootstrapping script skeletons.

## Handoff

**Note to User:** The repo has been fully scaffolded. You can paste the contents of `docs/handoff.md` to Claude Code to initiate the real implementation of your web wrapper features.

*Please see `docs/setup-notes.md` for information on local execution and prerequisites.*
