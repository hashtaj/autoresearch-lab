#!/usr/bin/env python3
"""
Demo runner: initializes Phoenix tracing, runs one simulated experiment iteration,
writes results JSON, and generates the Mission Control HTML report.

Usage:
    python scripts/run_demo.py
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Step 1 — Initialize Phoenix tracing
# ---------------------------------------------------------------------------
from app.backend.arize_logger import setup_tracer, trace_span, log_experiment_step

setup_tracer()

# ---------------------------------------------------------------------------
# Step 2 — Run one experiment iteration (simulated)
# ---------------------------------------------------------------------------
RESULTS_FILE = ROOT / "results" / "experiments.json"
RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load existing results
if RESULTS_FILE.exists():
    with open(RESULTS_FILE) as f:
        data = json.load(f)
else:
    data = {"experiments": []}

experiment_id = len(data["experiments"]) + 1

# Detect the device that would be used (mirrors train.py logic)
try:
    import torch
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
except ImportError:
    device = "cpu"

print(f"Running on device: {device}")

with trace_span("experiment.run", {
    "experiment.id": experiment_id,
    "device": device,
    "iteration_number": experiment_id,
}):
    # experiment.modify_code
    with trace_span("experiment.modify_code", {"experiment.id": experiment_id}):
        log_experiment_step("experiment.modify_code", {
            "experiment.id": experiment_id,
            "status": "skipped_demo",
        })

    # experiment.train
    t_train_start = time.time()
    with trace_span("experiment.train", {"experiment.id": experiment_id, "device": device}):
        # TODO: replace with: subprocess.run(["python", "train.py"], check=True)
        print(f"[demo] Simulating training for experiment #{experiment_id} ...")
        time.sleep(1)
    training_time = round(time.time() - t_train_start, 2)

    # experiment.evaluate
    import random
    random.seed(experiment_id)
    score = round(random.uniform(1.5, 4.0), 4)  # TODO: parse from train.py stdout

    with trace_span("experiment.evaluate", {
        "experiment.id": experiment_id,
        "experiment.score": score,
    }):
        log_experiment_step("experiment.evaluate", {
            "experiment.id": experiment_id,
            "experiment.score": score,
            "device": device,
            "training_time": training_time,
        })

    # experiment.commit_result
    with trace_span("experiment.commit_result", {
        "experiment.id": experiment_id,
        "experiment.status": "completed",
    }):
        pass

# ---------------------------------------------------------------------------
# Step 3 — Write results JSON
# ---------------------------------------------------------------------------
result = {
    "id": experiment_id,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "score": score,
    "status": "completed",
    "device": device,
    "training_time": training_time,
}
data["experiments"].append(result)

with open(RESULTS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"Experiment #{experiment_id} saved  score={score}  device={device}")

# ---------------------------------------------------------------------------
# Step 4 — Generate HTML report
# ---------------------------------------------------------------------------
from scripts.generate_report import main as generate_report  # noqa: E402

generate_report()

print()
print(f"Report generated at:  {ROOT / 'reports' / 'mission_control.html'}")
print(f"Phoenix UI:           http://localhost:6006")

# Flush all pending spans to Phoenix before exit
try:
    from opentelemetry import trace
    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()
except Exception:
    pass
