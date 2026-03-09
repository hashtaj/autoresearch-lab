# autoresearch-lab


![Python](https://img.shields.io/badge/python-3.10+-blue)
![Platform](https://img.shields.io/badge/platform-Apple%20Silicon%20%7C%20CUDA-lightgrey)
![Observability](https://img.shields.io/badge/observability-Arize%20Phoenix-purple)
![License](https://img.shields.io/badge/license-MIT-green)

Exploring autonomous experiment loops for machine learning systems.

This project is a fork of Andrej Karpathy's **autoresearch** with additions that make experiments **observable and runnable locally**.

The goal is simple:

> Let an AI system run experiments on itself — and make the process visible.

---

# Overview

Karpathy’s original project demonstrates a powerful idea:

An AI agent can autonomously improve a model by repeatedly running experiments.

Each iteration follows a loop:

1. Propose a change to the training setup  
2. Train the model for a fixed time budget  
3. Measure validation performance  
4. Keep improvements  
5. Repeat

Over time the system explores the search space and discovers better configurations.

This repository keeps that experiment loop intact while adding **observability, reporting, and local execution support**.

---

# Mission Control

Every experiment run is tracked in a **Mission Control dashboard** showing score progression, the best result discovered, and recent experiment history.

![Mission Control Dashboard](assets/mission-control.png)

The report is generated locally after experiment runs and provides a quick overview of how the system evolves during experimentation.

The report file is written to:

```
reports/mission_control.html
```

---

# What This Fork Adds

This fork focuses on making the experiment loop easier to **run locally and understand visually**.

---

## Apple Silicon Support

The training code now supports:

- CUDA (NVIDIA GPUs)
- MPS (Apple Silicon GPUs)
- CPU fallback

This allows the experiment loop to run locally on Apple Silicon machines such as **Mac Studio or Mac Mini**.

---

## Arize Phoenix Tracing

Experiment execution is traced using **Arize Phoenix**, an LLM and ML observability platform.

Every experiment emits **OpenTelemetry spans** to Phoenix, providing full trace visibility into the experiment lifecycle.

This allows inspection of each stage of the autonomous experiment loop:

```
experiment.run
→ experiment.modify_code
→ experiment.train
→ experiment.evaluate
→ experiment.commit_result
```

Example Phoenix trace view:

![Phoenix Trace Inspector](assets/phoenix-traces.png)

Phoenix UI runs locally at:

```
http://localhost:6006
```

This makes it possible to understand:

- what change an experiment attempted
- how long training ran
- how evaluation behaved
- which experiment produced improvements

---

# Running the Project Locally

The project can run on Apple Silicon or CUDA systems.

---

## 1. Install Dependencies

Using **uv** (recommended):

```bash
uv sync
```

or using pip:

```bash
pip install -e .
```

---

## 2. Start Phoenix

Start the Phoenix observability server:

```bash
phoenix serve
```

Open the UI:

```
http://localhost:6006
```

---

## 3. Prepare the Dataset

```bash
uv run prepare.py
```

This downloads and preprocesses the dataset used by the experiments.

---

## 4. Run Experiments

```bash
uv run train.py
```

The experiment loop will begin running iterations.

Each iteration:

- modifies the training setup
- runs a short training experiment
- evaluates the result

---

## 5. Generate Mission Control Report

After experiments run:

```bash
python scripts/generate_report.py
```

Open the report:

```
reports/mission_control.html
```

---

# Example Workflow

Typical workflow when running experiments locally:

```bash
phoenix serve

uv run prepare.py
uv run train.py

python scripts/generate_report.py
```

Then inspect:

```
reports/mission_control.html
```

and experiment traces in:

```
http://localhost:6006
```

---

# Future Work: Evaluation with Phoenix

This repository currently uses Phoenix primarily for **experiment tracing**.

However, Phoenix also provides powerful **evaluation capabilities** that could be integrated in future iterations.

Possible extensions include:

- automated evaluation of experiment outputs  
- comparing experiment variants across runs  
- reliability metrics for generated results  
- deeper failure analysis using Phoenix evaluation tools  

This would allow the experiment loop to evolve from simple metric tracking into a more comprehensive **experiment evaluation and analysis system**.

---

# Repository Structure

```
autoresearch-lab
│
train.py
prepare.py
program.md
│
app/backend
  runner.py
  arize_logger.py
  experiment_store.py
│
results/
reports/
│
scripts/
generate_report.py
run_demo.py
│
assets/
  mission-control.png
  phoenix-traces.png
```

---

# Project Status

This project is experimental.

The goal is to explore:

- autonomous experiment loops
- ML experiment observability
- experiment visualization

Expect rough edges as the system evolves.

---

# Credit

Original project by **Andrej Karpathy**

https://github.com/karpathy/autoresearch

This repository builds on that work by adding **local execution support and observability tooling**.

---

# License

Same license as the upstream project.

