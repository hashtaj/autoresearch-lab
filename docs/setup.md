# Setup Guide

## Prerequisites

```bash
# uv — Python package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Arize Phoenix — local observability server
pip install arize-phoenix
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

## Steps

**1. Start Phoenix**
```bash
phoenix serve
```
UI available at http://localhost:6006

**2. Prepare dataset** *(one-time — downloads ~1 GB of training shards)*
```bash
uv run prepare.py
```

**3. Run one training experiment**
```bash
uv run train.py
```
Runs for 5 minutes, prints `val_bpb` at the end.

**4. Generate the Mission Control report**
```bash
python scripts/generate_report.py
open reports/mission_control.html
```

**5. Run the full autonomous 1-hour loop**

Follow the instructions in `program.md` — the agent modifies `train.py`, runs experiments, tracks results in `results.tsv` and `learnings.md`, and writes a final research summary after 60 minutes.

**6. Inspect traces**

Open http://localhost:6006 to view experiment spans in Arize Phoenix.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PHOENIX_COLLECTOR_ENDPOINT` | `http://localhost:6006` | Phoenix OTLP endpoint |
| `PHOENIX_PROJECT_NAME` | `autoresearch-lab` | Project name in Phoenix UI |

---

## What you can and cannot modify

| File | Status |
|------|--------|
| `train.py` | ✅ Modify freely — this is what the agent experiments with |
| `prepare.py` | 🔒 Read-only — fixed evaluation, dataloader, tokenizer |
| `program.md` | ✅ Modify — agent instructions and experiment directions |
| `results.tsv` | ✅ Auto-updated by agent |
| `learnings.md` | ✅ Auto-updated by agent |
