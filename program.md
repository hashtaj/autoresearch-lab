# autoresearch

This is an experiment to have the LLM do its own research.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `mar5`). The branch `autoresearch/<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current master.
3. **Read the in-scope files**: The repo is small. Read these files for full context:
   - `README.md` — repository context.
   - `prepare.py` — fixed constants, data prep, tokenizer, dataloader, evaluation. Do not modify.
   - `train.py` — the file you modify. Model architecture, optimizer, training loop.
4. **Verify data exists**: Check that `~/.cache/autoresearch/` contains data shards and a tokenizer. If not, tell the human to run `uv run prepare.py`.
5. **Initialize results.tsv**: Create `results.tsv` with header row and baseline entry. The baseline results are already known from the output format section below (val_bpb: 0.997900, peak_vram_mb: 45060.2). Do NOT re-run the baseline — just record it.
6. **Confirm and go**: Confirm setup looks good.

Once you get confirmation, kick off the experimentation.

## Experimentation

Each experiment runs on a single GPU. The training script runs for a **fixed time budget of 5 minutes** (wall clock training time, excluding startup/compilation). You launch it simply as: `uv run train.py`.

**What you CAN do:**
- Modify `train.py` — this is the only file you edit. Everything is fair game: model architecture, optimizer, hyperparameters, training loop, batch size, model size, etc.

**What you CANNOT do:**
- Modify `prepare.py`. It is read-only. It contains the fixed evaluation, data loading, tokenizer, and training constants (time budget, sequence length, etc).
- Install new packages or add dependencies. You can only use what's already in `pyproject.toml`.
- Modify the evaluation harness. The `evaluate_bpb` function in `prepare.py` is the ground truth metric.

**The goal is simple: get the lowest val_bpb.** Since the time budget is fixed, you don't need to worry about training time — it's always 5 minutes. Everything is fair game: change the architecture, the optimizer, the hyperparameters, the batch size, the model size. The only constraint is that the code runs without crashing and finishes within the time budget.

**VRAM** is a soft constraint. Some increase is acceptable for meaningful val_bpb gains, but it should not blow up dramatically.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win. When evaluating whether to keep a change, weigh the complexity cost against the improvement magnitude. A 0.001 val_bpb improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 val_bpb improvement from deleting code? Definitely keep. An improvement of ~0 but much simpler code? Keep.

**The first run**: Your very first run should always be to establish the baseline, so you will run the training script as is.

## Output format

Once the script finishes it prints a summary like this:

```
---
val_bpb:          0.997900
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     45060.2
mfu_percent:      39.80
total_tokens_M:   499.6
num_steps:        953
num_params_M:     50.3
depth:            8
```

Note that the script is configured to always stop after 5 minutes, so depending on the computing platform of this computer the numbers might look different. You can extract the key metric from the log file:

```
grep "^val_bpb:" run.log
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated, NOT comma-separated — commas break in descriptions).

The TSV has a header row and 5 columns:

```
commit	val_bpb	memory_gb	status	description
```

1. git commit hash (short, 7 chars)
2. val_bpb achieved (e.g. 1.234567) — use 0.000000 for crashes
3. peak memory in GB, round to .1f (e.g. 12.3 — divide peak_vram_mb by 1024) — use 0.0 for crashes
4. status: `keep`, `discard`, or `crash`
5. short text description of what this experiment tried

Example:

```
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

## The experiment loop

The experiment runs on a dedicated branch (e.g. `autoresearch/mar5` or `autoresearch/mar5-gpu0`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune `train.py` with an experimental idea by directly hacking the code.
3. git commit
4. Run the experiment: `uv run train.py > run.log 2>&1` (redirect everything — do NOT use tee or let output flood your context)
5. Read out the results: `grep "^val_bpb:\|^peak_vram_mb:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the Python stack trace and attempt a fix. If you can't get things to work after more than a few attempts, give up.
7. Record the results in the tsv
8. **Update `learnings.md`** — append a brief entry for this experiment (see Learnings Tracking section below)
9. If val_bpb improved (lower), you "advance" the branch, keeping the git commit
10. If val_bpb is equal or worse, you git reset back to where you started

The idea is that you are a completely autonomous researcher trying things out. If they work, keep. If they don't, discard. And you're advancing the branch so that you can iterate. If you feel like you're getting stuck in some way, you can rewind but you should probably do this very very sparingly (if ever).

**Timeout**: Each experiment should take ~5 minutes total (+ a few seconds for startup and eval overhead). If a run exceeds 10 minutes, kill it and treat it as a failure (discard and revert).

**Crashes**: If a run crashes (OOM, or a bug, or etc.), use your judgment: If it's something dumb and easy to fix (e.g. a typo, a missing import), fix it and re-run. If the idea itself is fundamentally broken, just skip it, log "crash" as the status in the tsv, and move on.

**NEVER STOP**: Once the experiment loop has begun (after the initial setup), do NOT pause to ask the human if you should continue. Do NOT ask "should I keep going?" or "is this a good stopping point?". The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical architectural changes. The loop runs until the human interrupts you, period.

As an example use case, a user might leave you running while they sleep. If each experiment takes you ~5 minutes then you can run approx 12/hour, for a total of about 100 over the duration of the average human sleep. The user then wakes up to experimental results, all completed by you while they slept!

## Learnings Tracking

After **every experiment** (keep, discard, or crash), append a new entry to `learnings.md` using this format:

```
### Exp N — <short title> [keep/discard/crash]
- **What I tried**: <one sentence>
- **Result**: val_bpb <value> (delta vs best: <+/-> <value>)
- **Why I think this happened**: <your mechanistic hypothesis>
- **What this tells me**: <what you now believe is true or false about this model/setup>
- **Next idea informed by this**: <what you'll try next because of this result>
```

Keep each entry concise (5 bullet points max). Do not re-summarize old entries, just append.

After completing **≥12 experiments AND ≥60 minutes wall-clock** (both conditions must be met), write a final section at the bottom of `learnings.md` titled `## END-OF-SESSION RESEARCH SUMMARY`. Do NOT write this section early — only once the full 1-hour window is complete. This section must include:

1. **What worked** — ranked list of changes that improved val_bpb, with delta for each
2. **What didn't work** — changes that hurt or had no effect, and your hypothesis why
3. **Key insights** — 3–5 patterns you observed across the full experiment set (e.g. "LR is more important than depth for this time budget", "MLP ratio changes are cheaper to tune than architecture depth")
4. **Active hypotheses** — things you believe are likely true but haven't yet fully tested, with suggested next experiments to test them
5. **Advice for next researcher** — concrete, actionable recommendations if someone were to continue this run
6. **Time-to-target estimate** — based on your observed rate of improvement (val_bpb/experiment), estimate how many more experiments (and roughly how many more hours at 5 min/experiment) would be needed to reach val_bpb targets of **0.97**, **0.95**, and **0.90**. Be honest if the trajectory looks like it won't reach those targets within a reasonable time frame.

This summary is the primary deliverable of the session. Write it clearly — it will be read by a human who did not watch the experiments run.

## Suggested experiment directions (MPS-aware)

On Apple Silicon, MPS is ~3–5× slower per step than an H100. This means in the fixed 5-min budget you get far fewer gradient steps. The best strategies exploit this constraint:

1. **Smaller model, more steps** — reduce DEPTH (try 6, 5, 4) or ASPECT_RATIO (try 48). Fewer params = faster steps = more gradient updates = potentially better val_bpb despite smaller model.
2. **Batch size** — try DEVICE_BATCH_SIZE=64 or 32 to get more optimizer steps per minute (at cost of gradient estimate quality). Or try 256 for fewer but higher-quality steps.
3. **LR tuning** — MATRIX_LR=0.04, EMBEDDING_LR=0.6 are tuned for H100 step counts. With fewer steps on MPS, try higher LR (0.06, 0.08) to compensate.
4. **Warmdown schedule** — WARMDOWN_RATIO=0.5 is aggressive for a low-step run. Try 0.3 or 0.4 to spend more time at peak LR.
5. **Warmup** — try WARMUP_RATIO=0.05 to stabilize early steps on MPS.
6. **Window pattern** — try `"SSL"` or `"SL"` (shorter patterns = cheaper attention on MPS).
7. **GQA** — reduce n_kv_head (set `n_kv_head=num_heads//2` in build_model_config) to cut KV compute.
8. **MLP ratio** — change `4 * config.n_embd` to `3 * config.n_embd` in MLP for a cheaper forward pass.
9. **Adam betas** — try beta1=0.9 (more momentum, better for low-step regimes).
10. **Combined** — once you identify what works individually, try combining the top 2–3 improvements.

Always establish the MPS baseline first (run unmodified), then explore systematically.

## Apple Silicon (MPS) notes

- The training script runs on MPS when CUDA is unavailable.
- Flash attention 3 (FA3) is CUDA-only. On MPS, the script automatically falls back to `F.scaled_dot_product_attention` (PyTorch native). This is slower per step but fully functional.
- `torch.compile` is disabled on MPS (enabled on CUDA only).
- Training will be slower on MPS than on a GPU. Expect ~3–5× more wall-clock time per step compared to an H100. The 5-minute time budget still applies.
- **Target for this run: at least 1 hour** — run the experiment loop continuously for ≥60 minutes (≥12 experiments). Record all results in `results.tsv`.
