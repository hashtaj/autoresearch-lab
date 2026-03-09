# Autoresearch Learnings Log — autoresearch/mar8

Branch: `autoresearch/mar8`
Session started: 2026-03-08
Device: Apple Silicon (MPS)
Time budget per experiment: 5 minutes
Session target: ≥12 experiments, ≥60 minutes wall-clock

---

<!-- Append one entry per experiment below using the format from program.md -->

### Exp 1 — MPS baseline DEPTH=8 TOTAL=2^14 B=8 [keep]
- **What I tried**: Run with TOTAL_BATCH_SIZE=2^14 (reduced from 2^19), B=8, DEPTH=8 to get workable MPS training (93 steps in 300s). Used fallback val shard (shard_00007 instead of official shard_06542).
- **Result**: val_bpb 1.884818 (baseline, no delta reference; significantly worse than H100 baseline 0.9979)
- **Why I think this happened**: Only 1.5M training tokens total vs ~500M on H100. 94 steps × 16384 tokens = 1.5M tokens is grossly insufficient. The 3.6s/step rate means only 83 steps in 5min budget. MPS is ~40× slower throughput than H100.
- **What this tells me**: Need to dramatically reduce per-step cost — smaller model, larger batch, or both. Each step needs to process more useful training signal. DEPTH=8 with B=8 is extremely slow on MPS.
- **Next idea informed by this**: Try DEPTH=4 or DEPTH=6 to cut per-step latency and get more steps. Also try increasing DEVICE_BATCH_SIZE to 16 or 32 if memory allows to process more tokens per step.
