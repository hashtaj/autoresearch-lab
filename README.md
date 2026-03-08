# AutoResearch Lab

Work in progress.  
This is a fork of the original [karpathy/autoresearch](https://github.com/karpathy/autoresearch) repository.



## Upstream Concept

The original `autoresearch` idea: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats.

The core upstream files (`train.py`, `prepare.py`, `program.md`, `pyproject.toml`) have been kept clean and separated at the root so that merging future upstream changes remains straightforward.

See `docs/setup-notes.md` for information on local execution and prerequisites.

---

## Running locally on Apple Silicon

This branch adds minimal Apple Silicon (MPS) support, Arize Phoenix tracing, and a static Mission Control HTML report around the upstream autoresearch core. No backend server required.

### Prerequisites

```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

### Steps

**1. Start Phoenix**
```bash
phoenix serve
```
UI available at http://localhost:6006

**2. Prepare dataset** *(one-time)*
```bash
uv run prepare.py
```

**3. Run the demo** *(traces one simulated experiment and generates the report)*
```bash
python scripts/run_demo.py
```

**4. Open the report**
```bash
open reports/mission_control.html
```

**5. Inspect traces**

Open http://localhost:6006 in your browser.

---

> This is a minimal observability + report layer around the upstream autoresearch engine.
> It does not include a full UI platform or backend API.
