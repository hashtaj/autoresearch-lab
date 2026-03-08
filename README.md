# AutoResearch Lab

Work in progress.  
This is a fork of the original [karpathy/autoresearch](https://github.com/karpathy/autoresearch) repository.



## Upstream Concept

The original `autoresearch` idea: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats.

The core upstream files (`train.py`, `prepare.py`, `program.md`, `pyproject.toml`) have been kept clean and separated at the root so that merging future upstream changes remains straightforward.

See `docs/setup-notes.md` for information on local execution and prerequisites.
