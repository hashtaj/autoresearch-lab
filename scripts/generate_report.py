#!/usr/bin/env python3
"""
Generate a static Mission Control HTML report from results/experiments.json.
Styled after the mockup in /mockup/code.html.

Usage:
    python scripts/generate_report.py
Output:
    reports/mission_control.html
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = ROOT / "results" / "experiments.json"
REPORT_FILE = ROOT / "reports" / "mission_control.html"
PHOENIX_URL = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")


def load_experiments():
    if not RESULTS_FILE.exists():
        return []
    with open(RESULTS_FILE) as f:
        data = json.load(f)
    return data.get("experiments", [])


def generate_html(experiments: list) -> str:
    total = len(experiments)
    best = min(experiments, key=lambda e: e.get("score", float("inf")), default=None)
    latest = experiments[-1] if experiments else None

    best_score = f"{best['score']:.4f}" if best else "—"
    best_id = best["id"] if best else "—"
    best_device = best.get("device", "—") if best else "—"
    latest_score = f"{latest['score']:.4f}" if latest else "—"

    # Chart data
    labels = json.dumps([str(e["id"]) for e in experiments])
    scores = json.dumps([round(e.get("score", 0), 6) for e in experiments])

    # Experiment rows
    rows_html = ""
    for e in reversed(experiments[-10:]):
        status = e.get("status", "completed")
        status_color = "text-lime-neon" if status == "completed" else "text-alert-orange"
        rows_html += f"""
        <tr class="border-t border-holo-border hover:bg-white/5 transition-colors">
            <td class="px-4 py-3 font-mono text-electric-turquoise">#{e['id']}</td>
            <td class="px-4 py-3 font-mono text-slate-300">{e.get('score', '—'):.4f}</td>
            <td class="px-4 py-3 font-mono text-slate-400">{e.get('device', '—')}</td>
            <td class="px-4 py-3 text-xs {status_color} uppercase tracking-widest">{status}</td>
            <td class="px-4 py-3 text-xs text-slate-500 font-mono">{e.get('timestamp', '—')[:19]}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html class="dark" lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AUTORESEARCH LAB — Mission Control</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@300;500;700&family=Michroma&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<script id="tailwind-config">
tailwind.config = {{
    darkMode: "class",
    theme: {{
        extend: {{
            colors: {{
                "cosmic-dark": "#020817",
                "cosmic-deep": "#0B1120",
                "electric-turquoise": "#00F5FF",
                "lime-neon": "#39FF14",
                "alert-orange": "#FF6B00",
                "holo-border": "rgba(0, 245, 255, 0.2)",
                "holo-glass": "rgba(11, 17, 32, 0.7)"
            }},
            fontFamily: {{
                "display": ["Michroma", "sans-serif"],
                "mono": ["'JetBrains Mono'", "monospace"],
                "body": ["Outfit", "sans-serif"]
            }}
        }}
    }}
}}
</script>
<style type="text/tailwindcss">
@layer base {{
    body {{
        @apply bg-cosmic-dark text-slate-100 font-body;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(0, 245, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(57, 255, 20, 0.05) 0%, transparent 50%);
    }}
}}
.holo-panel {{
    @apply bg-holo-glass backdrop-blur-xl border border-holo-border rounded-xl;
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.05), inset 0 0 10px rgba(0, 245, 255, 0.05);
}}
.glow-turquoise {{ text-shadow: 0 0 10px rgba(0, 245, 255, 0.5); }}
.glow-lime {{ text-shadow: 0 0 10px rgba(57, 255, 20, 0.5); }}
.scanline {{
    background: linear-gradient(to bottom, transparent 50%, rgba(0, 245, 255, 0.02) 50%);
    background-size: 100% 4px;
}}
</style>
</head>
<body class="min-h-screen flex flex-col relative">
<div class="fixed inset-0 pointer-events-none scanline z-50 opacity-20"></div>

<!-- Header -->
<header class="border-b border-holo-border bg-cosmic-deep/80 backdrop-blur-2xl px-8 py-5 flex items-center justify-between z-40">
  <div class="flex items-center gap-4">
    <div class="w-10 h-10 rounded-lg bg-electric-turquoise/10 border border-electric-turquoise/30 flex items-center justify-center">
      <span class="material-symbols-outlined text-electric-turquoise glow-turquoise text-xl">hub</span>
    </div>
    <div>
      <h1 class="font-display text-sm tracking-tighter text-electric-turquoise glow-turquoise">AUTORESEARCH LAB</h1>
      <p class="text-[10px] uppercase tracking-[0.3em] text-lime-neon font-bold">Mission Control</p>
    </div>
  </div>
  <p class="text-xs text-slate-400 max-w-md text-right hidden sm:block">
    Autonomous experiments modifying model code and measuring performance.
  </p>
  <div class="flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-lime-neon animate-pulse"></span>
    <span class="text-xs font-mono text-lime-neon">LIVE</span>
  </div>
</header>

<!-- Main -->
<main class="flex-1 p-6 md:p-8 space-y-6">

  <!-- Stat cards -->
  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
    <div class="holo-panel p-5">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500 mb-2">Total Experiments</p>
      <p class="text-3xl font-display text-electric-turquoise glow-turquoise">{total}</p>
    </div>
    <div class="holo-panel p-5">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500 mb-2">Latest Score (BPB)</p>
      <p class="text-3xl font-display text-slate-100">{latest_score}</p>
    </div>
    <div class="holo-panel p-5 col-span-2 md:col-span-1">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500 mb-2">Best Score (BPB)</p>
      <p class="text-3xl font-display text-lime-neon glow-lime">{best_score}</p>
    </div>
  </div>

  <!-- Chart + Best card -->
  <div class="grid md:grid-cols-3 gap-4">
    <!-- Timeline chart -->
    <div class="holo-panel p-6 md:col-span-2">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500 mb-4">Experiment Score Timeline</p>
      <div class="relative h-48">
        <canvas id="scoreChart"></canvas>
      </div>
    </div>

    <!-- Best experiment card -->
    <div class="holo-panel p-6 flex flex-col justify-between">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500 mb-4">Best Experiment</p>
      <div class="space-y-4">
        <div>
          <p class="text-[9px] text-slate-500 uppercase tracking-widest">Score</p>
          <p class="text-2xl font-display text-lime-neon glow-lime">{best_score}</p>
        </div>
        <div>
          <p class="text-[9px] text-slate-500 uppercase tracking-widest">Experiment ID</p>
          <p class="text-xl font-mono text-electric-turquoise">#{best_id}</p>
        </div>
        <div>
          <p class="text-[9px] text-slate-500 uppercase tracking-widest">Device</p>
          <p class="text-sm font-mono text-slate-300">{best_device}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Experiment table -->
  <div class="holo-panel overflow-hidden">
    <div class="px-6 py-4 border-b border-holo-border">
      <p class="text-[10px] uppercase tracking-[0.25em] text-slate-500">Recent Experiments</p>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-[9px] uppercase tracking-widest text-slate-500">
            <th class="px-4 py-3 text-left">ID</th>
            <th class="px-4 py-3 text-left">Score</th>
            <th class="px-4 py-3 text-left">Device</th>
            <th class="px-4 py-3 text-left">Status</th>
            <th class="px-4 py-3 text-left">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {rows_html if rows_html else '<tr><td colspan="5" class="px-4 py-8 text-center text-slate-500 font-mono text-xs">No experiments yet — run scripts/run_demo.py</td></tr>'}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Trace inspection -->
  <div class="holo-panel p-6 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="w-10 h-10 rounded-lg bg-electric-turquoise/10 border border-electric-turquoise/30 flex items-center justify-center">
        <span class="material-symbols-outlined text-electric-turquoise text-xl">timeline</span>
      </div>
      <div>
        <p class="text-xs font-display text-electric-turquoise">Arize Phoenix</p>
        <p class="text-xs text-slate-400 mt-0.5">Inspect experiment traces in Arize Phoenix.</p>
      </div>
    </div>
    <a href="{PHOENIX_URL}" target="_blank"
       class="px-4 py-2 rounded-lg border border-electric-turquoise/40 text-electric-turquoise text-xs font-mono hover:bg-electric-turquoise/10 transition-colors">
      Open Phoenix UI →
    </a>
  </div>

</main>

<script>
const ctx = document.getElementById('scoreChart');
if (ctx) {{
  new Chart(ctx, {{
    type: 'line',
    data: {{
      labels: {labels},
      datasets: [{{
        label: 'Score (BPB)',
        data: {scores},
        borderColor: '#00F5FF',
        backgroundColor: 'rgba(0, 245, 255, 0.08)',
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: '#00F5FF',
        tension: 0.3,
        fill: true,
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(11,17,32,0.95)',
          borderColor: 'rgba(0,245,255,0.3)',
          borderWidth: 1,
          titleColor: '#00F5FF',
          bodyColor: '#94a3b8',
        }}
      }},
      scales: {{
        x: {{
          grid: {{ color: 'rgba(0,245,255,0.05)' }},
          ticks: {{ color: '#475569', font: {{ family: 'JetBrains Mono', size: 10 }} }},
          title: {{ display: true, text: 'Experiment', color: '#475569', font: {{ size: 10 }} }}
        }},
        y: {{
          grid: {{ color: 'rgba(0,245,255,0.05)' }},
          ticks: {{ color: '#475569', font: {{ family: 'JetBrains Mono', size: 10 }} }},
          title: {{ display: true, text: 'Score (BPB)', color: '#475569', font: {{ size: 10 }} }}
        }}
      }}
    }}
  }});
}}
</script>
</body>
</html>"""


def main():
    experiments = load_experiments()
    html = generate_html(experiments)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(html, encoding="utf-8")
    print(f"Report generated at: {REPORT_FILE}")


if __name__ == "__main__":
    main()
