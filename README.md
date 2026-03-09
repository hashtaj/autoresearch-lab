# AutoResearch Lab

A fork of [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) — an autonomous ML research loop where a Claude agent modifies model code, trains for 5 minutes, checks if results improved, keeps or discards, and repeats indefinitely.

This fork adds three capabilities on top of the upstream core:

1. **Apple Silicon (MPS) support** — runs locally on M1/M2/M3 Macs without modification
2. **Arize Phoenix tracing** — every experiment emits OpenTelemetry spans for observability
3. **Mission Control report** — a static HTML dashboard summarizing experiment results

---

## Repo structure

```
train.py                      The model training script — this is what the agent modifies
prepare.py                    Fixed: data prep, tokenizer, dataloader, evaluation (do not modify)
program.md                    Instructions for the autonomous research agent
results.tsv                   Tab-separated log of all experiment results
learnings.md                  Living research log: per-experiment insights + end-of-session summary
analysis.ipynb                Notebook for visualizing results.tsv (charts, best experiments)
app/backend/arize_logger.py   OpenTelemetry tracer → Arize Phoenix
scripts/run_demo.py           Runs one simulated experiment and generates the report
scripts/generate_report.py    Reads results/experiments.json → reports/mission_control.html
reports/mission_control.html  Static Mission Control dashboard (auto-generated)
results/experiments.json      Experiment results in JSON (auto-generated)
```

---

## Running locally on Apple Silicon

### Prerequisites

```bash
# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Arize Phoenix (observability)
pip install arize-phoenix
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

### Steps

**1. Start Phoenix**
```bash
phoenix serve
```
UI available at http://localhost:6006

**2. Prepare dataset** *(one-time — downloads ~1 GB of training shards)*
```bash
uv run prepare.py
```

**3. Run the autonomous experiment loop**
```bash
uv run train.py
```
This runs one 5-minute experiment. For the full autonomous loop (agent modifies, trains, evaluates, repeats for 1+ hours), see `program.md`.

**4. Generate the Mission Control report**
```bash
python scripts/generate_report.py
open reports/mission_control.html
```

**5. Inspect traces**

Open http://localhost:6006 in your browser to see experiment spans in Arize Phoenix.

---

## What was added over upstream

### Apple Silicon (MPS) support

The upstream `train.py` assumes CUDA. This fork adds device detection in priority order: CUDA → MPS → CPU. CUDA-only calls (FA3 flash attention, `torch.compile`) are guarded and replaced with MPS-compatible equivalents (`F.scaled_dot_product_attention`). The 5-minute time budget and all experiment logic are unchanged.

### Arize Phoenix tracing

`app/backend/arize_logger.py` provides a lightweight OpenTelemetry tracer that emits spans to a locally-running Phoenix instance. Each experiment creates spans for:

- `experiment.run`
- `experiment.modify_code`
- `experiment.train`
- `experiment.evaluate`
- `experiment.commit_result`

Tracing fails silently if Phoenix is unavailable — the experiment loop continues regardless.

### Mission Control report

`scripts/generate_report.py` reads `results/experiments.json` and renders a static HTML dashboard with an experiment timeline chart (Chart.js), a best-result card, run statistics, and a link to the Phoenix trace inspector.

### Research learnings log

`learnings.md` is a living document the agent updates after every experiment: what it tried, the result, its mechanistic hypothesis, and what it plans to try next. After the full 1-hour session (≥12 experiments), the agent appends an `END-OF-SESSION RESEARCH SUMMARY` with ranked findings, key insights, active hypotheses, advice for the next researcher, and a time-to-target estimate for further improvement.

---

## Upstream

Original concept and core engine by **Andrej Karpathy**: https://github.com/karpathy/autoresearch

> The upstream files (`train.py`, `prepare.py`, `program.md`, `pyproject.toml`) are kept clean at the repo root so future upstream merges remain straightforward.
