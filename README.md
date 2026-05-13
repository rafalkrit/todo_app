<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Todo App — CLI Task Manager</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0c10;
    --surface: #111318;
    --surface2: #1a1d24;
    --border: rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.13);
    --text: #e8eaf0;
    --muted: #6b7280;
    --accent: #7c6cf8;
    --accent2: #4ade80;
    --accent3: #f59e0b;
    --accent4: #38bdf8;
    --danger: #f87171;
    --mono: 'JetBrains Mono', monospace;
    --sans: 'Syne', sans-serif;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--mono);
    font-size: 14px;
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* ── NOISE OVERLAY ── */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 80px 40px 60px;
    overflow: hidden;
  }

  .hero-grid {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(124,108,248,0.08) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124,108,248,0.08) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 30%, transparent 100%);
  }

  .hero-glow {
    position: absolute;
    width: 600px;
    height: 300px;
    background: radial-gradient(ellipse, rgba(124,108,248,0.15) 0%, transparent 70%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124,108,248,0.12);
    border: 1px solid rgba(124,108,248,0.3);
    color: #a78bfa;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 24px;
    position: relative;
  }

  .badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent2);
    box-shadow: 0 0 8px var(--accent2);
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .hero h1 {
    font-family: var(--sans);
    font-size: clamp(48px, 8vw, 96px);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 0.95;
    position: relative;
    margin-bottom: 16px;
  }

  .hero h1 .word-todo { color: var(--accent); }
  .hero h1 .word-app { color: var(--text); opacity: 0.9; }

  .hero-subtitle {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--muted);
    font-weight: 300;
    max-width: 440px;
    margin-bottom: 36px;
    position: relative;
  }

  .hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    position: relative;
  }

  .pill {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 100px;
    border: 1px solid;
  }

  .pill-purple { background: rgba(124,108,248,0.1); border-color: rgba(124,108,248,0.3); color: #a78bfa; }
  .pill-green  { background: rgba(74,222,128,0.08); border-color: rgba(74,222,128,0.25); color: #4ade80; }
  .pill-amber  { background: rgba(245,158,11,0.08); border-color: rgba(245,158,11,0.25); color: #fbbf24; }
  .pill-blue   { background: rgba(56,189,248,0.08); border-color: rgba(56,189,248,0.25); color: #38bdf8; }
  .pill-red    { background: rgba(248,113,113,0.08); border-color: rgba(248,113,113,0.25); color: #f87171; }

  /* ── LAYOUT ── */
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 32px 100px;
    position: relative;
    z-index: 1;
  }

  /* ── SECTION ── */
  .section {
    margin-bottom: 64px;
  }

  .section-label {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(124,108,248,0.3), transparent);
  }

  .section-title {
    font-family: var(--sans);
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 20px;
  }

  /* ── TERMINAL ── */
  .terminal {
    background: #0d0f14;
    border: 1px solid var(--border2);
    border-radius: 12px;
    overflow: hidden;
    font-family: var(--mono);
    font-size: 13px;
  }

  .terminal-bar {
    background: #161920;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid var(--border);
  }

  .terminal-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }

  .dot-red    { background: #ff5f57; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green  { background: #28ca41; }

  .terminal-title {
    flex: 1;
    text-align: center;
    font-size: 11px;
    color: var(--muted);
    font-weight: 400;
  }

  .terminal-body {
    padding: 20px 24px;
    line-height: 1.8;
  }

  .t-prompt   { color: var(--accent2); }
  .t-cmd      { color: var(--text); }
  .t-comment  { color: var(--muted); }
  .t-output   { color: #94a3b8; }
  .t-highlight{ color: var(--accent); }
  .t-selected { color: var(--accent2); }
  .t-muted    { color: var(--muted); }
  .t-warn     { color: var(--accent3); }
  .t-success  { color: #4ade80; }
  .t-value    { color: var(--accent4); }
  .t-error    { color: var(--danger); }

  /* ── CARDS GRID ── */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
  }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    transition: border-color 0.2s, transform 0.2s;
  }

  .card:hover {
    border-color: var(--border2);
    transform: translateY(-2px);
  }

  .card-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 12px;
  }

  .icon-purple { background: rgba(124,108,248,0.12); }
  .icon-green  { background: rgba(74,222,128,0.1); }
  .icon-amber  { background: rgba(245,158,11,0.1); }
  .icon-blue   { background: rgba(56,189,248,0.1); }

  .card-title {
    font-family: var(--sans);
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
  }

  .card-desc {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.6;
  }

  /* ── TABLE ── */
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
  }

  .data-table thead th {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: left;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
  }

  .data-table tbody td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }

  .data-table tbody tr:last-child td {
    border-bottom: none;
  }

  .data-table tbody tr:hover td {
    background: rgba(255,255,255,0.02);
  }

  .field-name {
    font-family: var(--mono);
    color: var(--accent4);
    font-weight: 500;
    white-space: nowrap;
  }

  .field-type {
    color: var(--accent);
    font-style: italic;
  }

  .field-desc {
    color: #94a3b8;
  }

  /* ── TECH STACK ── */
  .stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
  }

  .stack-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.2s;
  }

  .stack-item:hover { border-color: var(--border2); }

  .stack-area {
    font-size: 11px;
    color: var(--muted);
  }

  .stack-tech {
    font-size: 12px;
    font-weight: 500;
    color: var(--text);
  }

  /* ── ARCH DIAGRAM ── */
  .arch {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 32px;
    font-family: var(--mono);
    font-size: 12px;
    line-height: 2.2;
    overflow-x: auto;
  }

  .arch-layer {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
  }

  .arch-box {
    padding: 4px 14px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
  }

  .arch-main  { background: rgba(124,108,248,0.12); border: 1px solid rgba(124,108,248,0.3); color: #a78bfa; }
  .arch-cli   { background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.25); color: #38bdf8; }
  .arch-domain{ background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.25); color: #4ade80; }
  .arch-store { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); color: #fbbf24; }
  .arch-ui    { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.25); color: #f87171; }

  .arch-arrow {
    color: var(--muted);
    font-size: 14px;
  }

  /* ── QUICKSTART STEPS ── */
  .steps {
    counter-reset: step;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .step {
    display: grid;
    grid-template-columns: 40px 1fr;
    gap: 16px;
    align-items: start;
  }

  .step-num {
    counter-increment: step;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(124,108,248,0.1);
    border: 1px solid rgba(124,108,248,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
    flex-shrink: 0;
  }

  .step-content {}

  .step-title {
    font-family: var(--sans);
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 10px;
  }

  /* ── INLINE CODE ── */
  code {
    font-family: var(--mono);
    font-size: 12px;
    background: rgba(124,108,248,0.1);
    border: 1px solid rgba(124,108,248,0.2);
    color: #c4b5fd;
    padding: 2px 7px;
    border-radius: 5px;
  }

  /* ── STATUS BADGE ── */
  .status-todo       { color: var(--muted); }
  .status-inprogress { color: var(--accent4); }
  .status-completed  { color: var(--accent2); }
  .status-blocked    { color: var(--danger); }

  /* ── DIVIDER ── */
  hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 48px 0;
  }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    font-size: 11px;
    color: var(--muted);
    padding: 40px 0;
    border-top: 1px solid var(--border);
    font-family: var(--mono);
  }

  /* ── COVERAGE BAR ── */
  .coverage-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .bar-track {
    flex: 1;
    height: 6px;
    background: var(--surface2);
    border-radius: 100px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #4ade80, #22d3ee);
    border-radius: 100px;
    animation: fillBar 1.5s ease-out forwards;
    width: 0%;
  }

  @keyframes fillBar {
    to { width: 100%; }
  }

  .bar-label {
    font-size: 13px;
    font-weight: 700;
    color: var(--accent2);
    white-space: nowrap;
  }

  .bar-desc {
    font-size: 11px;
    color: var(--muted);
    flex: 1;
  }

  /* ── ROADMAP ── */
  .roadmap-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .roadmap-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: #94a3b8;
    padding: 8px 14px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
  }

  .roadmap-list li::before {
    content: '○';
    color: var(--muted);
    font-size: 10px;
    flex-shrink: 0;
  }

  /* ── BLINKING CURSOR ── */
  .cursor {
    display: inline-block;
    width: 9px;
    height: 16px;
    background: var(--accent2);
    vertical-align: text-bottom;
    animation: blink 1.1s step-end infinite;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }

  /* ── ENV VAR ── */
  .env-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
  }

  .env-key {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--accent3);
    font-weight: 500;
  }

  .env-val {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--muted);
  }

  .scroll-to-top {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 40px;
    height: 40px;
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    color: var(--muted);
    transition: color 0.2s, border-color 0.2s;
    text-decoration: none;
    z-index: 10;
  }
  .scroll-to-top:hover { color: var(--text); border-color: var(--accent); }

  @media (max-width: 600px) {
    .hero { padding: 60px 20px 40px; }
    .container { padding: 0 16px 60px; }
    .env-row { grid-template-columns: 1fr; }
    .arch { padding: 20px 16px; }
  }
</style>
</head>
<body>

<!-- HERO -->
<div class="hero" id="top">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="badge">● Active · Python 3.13</div>
  <h1>
    <span class="word-todo">Todo</span><br>
    <span class="word-app">App</span>
  </h1>
  <p class="hero-subtitle">Professional command-line task manager — typed domain model, JSON persistence, interactive terminal workflow.</p>
  <div class="hero-badges">
    <span class="pill pill-purple">Python ≥3.13</span>
    <span class="pill pill-blue">Typer · Rich</span>
    <span class="pill pill-green">100% Coverage</span>
    <span class="pill pill-amber">pytest · uv</span>
    <span class="pill pill-red">pre-commit</span>
  </div>
</div>

<div class="container">

  <!-- DEMO TERMINAL -->
  <div class="section">
    <div class="section-label">Interactive workflow</div>
    <div class="terminal">
      <div class="terminal-bar">
        <div class="terminal-dot dot-red"></div>
        <div class="terminal-dot dot-yellow"></div>
        <div class="terminal-dot dot-green"></div>
        <div class="terminal-title">todo_app — python main.py</div>
      </div>
      <div class="terminal-body">
        <div><span class="t-prompt">$</span> <span class="t-cmd">uv run python main.py</span></div>
        <div style="margin-top:10px"></div>
        <div><span class="t-output">┌─────────────────────────────────────────────────────┐</span></div>
        <div><span class="t-output">│</span>  <span class="t-highlight">#   Description                  Status       Pri  Deadline</span>    <span class="t-output">│</span></div>
        <div><span class="t-output">├─────────────────────────────────────────────────────┤</span></div>
        <div><span class="t-output">│</span>  <span class="t-muted">1   Prepare release checklist</span>  <span class="t-value">in progress</span>  <span class="t-warn">HIGH</span>  <span class="t-muted">2026-05-20</span>  <span class="t-output">│</span></div>
        <div><span class="t-output">│</span>  <span class="t-muted">2   Review PR from @kacper</span>      <span class="t-muted">todo</span>         <span class="t-value">MED</span>   <span class="t-muted">—</span>           <span class="t-output">│</span></div>
        <div><span class="t-output">│</span>  <span class="t-muted">3   Write unit tests for ui/</span>    <span class="t-success">completed</span>    <span class="t-muted">LOW</span>   <span class="t-muted">—</span>           <span class="t-output">│</span></div>
        <div><span class="t-output">│</span>  <span class="t-muted">4   Fix deadline validation bug</span> <span class="t-error">blocked</span>      <span class="t-warn">HIGH</span>  <span class="t-muted">2026-05-15</span>  <span class="t-output">│</span></div>
        <div><span class="t-output">└─────────────────────────────────────────────────────┘</span></div>
        <div style="margin-top:10px"></div>
        <div><span class="t-output">Menu</span></div>
        <div><span class="t-selected">❯ Show tasks</span></div>
        <div><span class="t-muted">  Add task</span></div>
        <div><span class="t-muted">  Update task</span></div>
        <div><span class="t-muted">  Remove task</span></div>
        <div><span class="t-muted">  Exit</span></div>
        <div style="margin-top:4px"><span class="cursor"></span></div>
      </div>
    </div>
  </div>

  <!-- CAPABILITIES -->
  <div class="section">
    <div class="section-label">What it does</div>
    <div class="cards-grid">
      <div class="card">
        <div class="card-icon icon-purple">📋</div>
        <div class="card-title">Display &amp; Filter</div>
        <div class="card-desc">Formatted Rich table. Filter by status, priority, tag, deadline range, or custom predicate.</div>
      </div>
      <div class="card">
        <div class="card-icon icon-green">➕</div>
        <div class="card-title">Add Tasks</div>
        <div class="card-desc">Interactive prompts: description, status, priority, deadline, and tags with full validation.</div>
      </div>
      <div class="card">
        <div class="card-icon icon-amber">✏️</div>
        <div class="card-title">Update Tasks</div>
        <div class="card-desc">Field-level update flow. Auto-manages <code>completed_at</code> on status transitions.</div>
      </div>
      <div class="card">
        <div class="card-icon icon-blue">💾</div>
        <div class="card-title">Persist</div>
        <div class="card-desc">Full JSON persistence. Typed domain serialization. Controlled via <code>STORAGE_PATH_ENV</code>.</div>
      </div>
    </div>
  </div>

  <!-- QUICKSTART -->
  <div class="section">
    <div class="section-label">Quick start</div>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-content">
          <div class="step-title">Install dependencies</div>
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
              <div class="terminal-title">PowerShell</div>
            </div>
            <div class="terminal-body">
              <div><span class="t-prompt">$</span> <span class="t-cmd">uv sync</span></div>
            </div>
          </div>
        </div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-content">
          <div class="step-title">Create storage file</div>
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
              <div class="terminal-title">PowerShell</div>
            </div>
            <div class="terminal-body">
              <div><span class="t-prompt">$</span> <span class="t-cmd">New-Item -ItemType Directory -Force .\temp</span></div>
              <div><span class="t-prompt">$</span> <span class="t-cmd">'{"tasks": []}' | Set-Content -Encoding utf8 .\temp\todo_list.json</span></div>
            </div>
          </div>
        </div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-content">
          <div class="step-title">Set storage path</div>
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
              <div class="terminal-title">PowerShell</div>
            </div>
            <div class="terminal-body">
              <div><span class="t-prompt">$</span> <span class="t-cmd">$env:STORAGE_PATH_ENV = "$PWD\temp\todo_list.json"</span></div>
            </div>
          </div>
        </div>
      </div>
      <div class="step">
        <div class="step-num">4</div>
        <div class="step-content">
          <div class="step-title">Run the application</div>
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
              <div class="terminal-title">PowerShell</div>
            </div>
            <div class="terminal-body">
              <div><span class="t-prompt">$</span> <span class="t-cmd">uv run python main.py</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- CONFIGURATION -->
  <div class="section">
    <div class="section-label">Configuration</div>
    <div class="env-row">
      <div>
        <div class="env-key">STORAGE_PATH_ENV</div>
        <div style="font-size:11px; color: var(--danger); margin-top:4px;">required</div>
      </div>
      <div>
        <div class="env-val">Path to the JSON file used as task storage. Must exist and contain valid task-list JSON.</div>
        <div style="margin-top:6px; font-size:11px; font-family:var(--mono); color:#94a3b8;">e.g. C:\Users\rafal\pythonprojects\todo_app\temp\todo_list.json</div>
      </div>
    </div>
  </div>

  <!-- DATA MODEL -->
  <div class="section">
    <div class="section-label">Data model — Task</div>
    <div class="terminal" style="background: var(--surface); border-color: var(--border);">
      <div class="terminal-bar">
        <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
        <div class="terminal-title">storage.json — example task</div>
      </div>
      <div class="terminal-body">
<pre style="font-family:var(--mono); font-size:12.5px; line-height:1.8; color:#94a3b8;">{
  <span class="t-highlight">"description"</span>: <span class="t-success">"Prepare release checklist"</span>,
  <span class="t-highlight">"status"</span>:      <span class="t-success">"in progress"</span>,
  <span class="t-highlight">"priority"</span>:    <span class="t-value">3</span>,             <span class="t-comment">// HIGH</span>
  <span class="t-highlight">"created_at"</span>:  <span class="t-success">"2026-05-13T08:00:00+00:00"</span>,
  <span class="t-highlight">"deadline"</span>:    <span class="t-success">"2026-05-20"</span>,
  <span class="t-highlight">"completed_at"</span>:<span class="t-muted">null</span>,
  <span class="t-highlight">"tags"</span>:        [<span class="t-success">"release"</span>, <span class="t-success">"ops"</span>],
  <span class="t-highlight">"idx"</span>:         <span class="t-success">"63614577-08fa-4049-8e23-267d6867517c"</span>
}</pre>
      </div>
    </div>
    <div style="margin-top:16px;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Field</th>
            <th>Type</th>
            <th>Rules</th>
          </tr>
        </thead>
        <tbody>
          <tr><td class="field-name">idx</td><td class="field-type">UUIDv4</td><td class="field-desc">Auto-generated when omitted. Must be valid UUIDv4.</td></tr>
          <tr><td class="field-name">description</td><td class="field-type">string</td><td class="field-desc">Required. 3–120 characters.</td></tr>
          <tr><td class="field-name">status</td><td class="field-type">enum</td><td class="field-desc"><span class="status-todo">todo</span> · <span class="status-inprogress">in progress</span> · <span class="status-completed">completed</span> · <span class="status-blocked">blocked</span></td></tr>
          <tr><td class="field-name">priority</td><td class="field-type">enum/int</td><td class="field-desc">LOW = 1 · MEDIUM = 2 · HIGH = 3</td></tr>
          <tr><td class="field-name">created_at</td><td class="field-type">datetime</td><td class="field-desc">UTC timestamp, assigned at creation.</td></tr>
          <tr><td class="field-name">deadline</td><td class="field-type">date/null</td><td class="field-desc">Optional. Must not predate <code>created_at</code>.</td></tr>
          <tr><td class="field-name">completed_at</td><td class="field-type">datetime/null</td><td class="field-desc">Auto-set when status → completed; cleared otherwise.</td></tr>
          <tr><td class="field-name">tags</td><td class="field-type">list[str]</td><td class="field-desc">Lowercase, trimmed, de-duplicated, order-preserved.</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- ARCHITECTURE -->
  <div class="section">
    <div class="section-label">Architecture</div>
    <div class="arch">
      <div class="arch-layer">
        <div class="arch-box arch-main">main.py</div>
        <span class="arch-arrow">→</span>
        <div class="arch-box arch-cli">cli/registry.py</div>
        <span class="arch-arrow">→</span>
        <div class="arch-box arch-cli">cli/commands/</div>
      </div>
      <div class="arch-layer" style="padding-left:120px;">
        <span class="arch-arrow">↙</span>
        <span style="color:var(--muted); font-size:11px; margin-left:4px; margin-right:16px">split</span>
      </div>
      <div class="arch-layer" style="padding-left:20px; gap:24px; flex-wrap:wrap;">
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="arch-box arch-cli">cli/state.py</div>
          <div class="arch-box arch-store">JSON storage</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="arch-box arch-domain">src/task/</div>
          <div class="arch-box arch-domain">src/task_list/</div>
          <div class="arch-box arch-domain">src/schemas/</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div class="arch-box arch-ui">src/ui/</div>
          <div class="arch-box arch-ui">Rich · Questionary</div>
        </div>
      </div>
      <div style="margin-top:20px; display:flex; gap:16px; flex-wrap:wrap;">
        <span style="font-size:11px; color:var(--muted);">Legend:</span>
        <span class="arch-box arch-main" style="font-size:10px;">entry / registry</span>
        <span class="arch-box arch-cli" style="font-size:10px;">CLI layer</span>
        <span class="arch-box arch-domain" style="font-size:10px;">domain</span>
        <span class="arch-box arch-store" style="font-size:10px;">persistence</span>
        <span class="arch-box arch-ui" style="font-size:10px;">UI</span>
      </div>
    </div>
  </div>

  <!-- TECH STACK -->
  <div class="section">
    <div class="section-label">Technology stack</div>
    <div class="stack-grid">
      <div class="stack-item"><span class="stack-area">Language</span><span class="stack-tech">Python ≥3.13</span></div>
      <div class="stack-item"><span class="stack-area">CLI framework</span><span class="stack-tech">Typer</span></div>
      <div class="stack-item"><span class="stack-area">Prompts</span><span class="stack-tech">Questionary</span></div>
      <div class="stack-item"><span class="stack-area">Rendering</span><span class="stack-tech">Rich</span></div>
      <div class="stack-item"><span class="stack-area">Package manager</span><span class="stack-tech">uv</span></div>
      <div class="stack-item"><span class="stack-area">Test runner</span><span class="stack-tech">pytest</span></div>
      <div class="stack-item"><span class="stack-area">Coverage</span><span class="stack-tech">pytest-cov</span></div>
      <div class="stack-item"><span class="stack-area">Lint &amp; format</span><span class="stack-tech">Ruff</span></div>
      <div class="stack-item"><span class="stack-area">Type check</span><span class="stack-tech">ty</span></div>
      <div class="stack-item"><span class="stack-area">Git hooks</span><span class="stack-tech">pre-commit</span></div>
    </div>
  </div>

  <!-- QUALITY GATES -->
  <div class="section">
    <div class="section-label">Quality gates</div>
    <div style="display:flex; flex-direction:column; gap:12px;">
      <div class="coverage-bar">
        <div class="bar-track"><div class="bar-fill"></div></div>
        <div class="bar-label">100%</div>
        <div class="bar-desc">branch coverage requirement</div>
      </div>
      <div class="terminal">
        <div class="terminal-bar">
          <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
          <div class="terminal-title">quality checks</div>
        </div>
        <div class="terminal-body">
          <div><span class="t-prompt">$</span> <span class="t-cmd">uv run ruff format</span>       <span class="t-success">✓ formatting</span></div>
          <div><span class="t-prompt">$</span> <span class="t-cmd">uv run ruff check</span>        <span class="t-success">✓ linting</span></div>
          <div><span class="t-prompt">$</span> <span class="t-cmd">uv run ty check</span>          <span class="t-success">✓ types</span></div>
          <div><span class="t-prompt">$</span> <span class="t-cmd">uv run pytest</span>            <span class="t-success">✓ tests + 100% coverage</span></div>
          <div><span class="t-muted">  DeprecationWarning → error</span></div>
          <div><span class="t-muted">  FutureWarning      → error</span></div>
        </div>
      </div>
    </div>
  </div>

  <!-- PROJECT STRUCTURE -->
  <div class="section">
    <div class="section-label">Project structure</div>
    <div class="terminal">
      <div class="terminal-bar">
        <div class="terminal-dot dot-red"></div><div class="terminal-dot dot-yellow"></div><div class="terminal-dot dot-green"></div>
        <div class="terminal-title">todo_app/</div>
      </div>
      <div class="terminal-body">
<pre style="font-family:var(--mono); font-size:12.5px; line-height:1.9; color:#94a3b8;"><span class="t-highlight">todo_app/</span>
├── <span class="t-value">main.py</span>
├── <span class="t-muted">pyproject.toml</span>
├── <span class="t-muted">pytest.toml</span>
├── <span class="t-muted">ruff.toml</span>
├── <span class="t-highlight">src/</span>
│   ├── <span class="t-value">cli/</span>
│   │   ├── <span class="t-muted">commands/</span>        <span class="t-comment"># add · list · update · remove · exit</span>
│   │   ├── <span class="t-muted">registry.py</span>
│   │   └── <span class="t-muted">state.py</span>         <span class="t-comment"># singleton TaskList + JSON I/O</span>
│   ├── <span class="t-value">enums/</span>               <span class="t-comment"># StatusEnum · PriorityEnum</span>
│   ├── <span class="t-value">schemas/</span>             <span class="t-comment"># TypedDict contracts + guards</span>
│   ├── <span class="t-value">task/</span>                <span class="t-comment"># Task domain model</span>
│   ├── <span class="t-value">task_list/</span>           <span class="t-comment"># TaskList collection</span>
│   └── <span class="t-value">ui/</span>                  <span class="t-comment"># Rich table · Questionary prompts</span>
└── <span class="t-highlight">tests/</span>
    ├── <span class="t-muted">cli/</span>
    ├── <span class="t-muted">schemas/</span>
    ├── <span class="t-muted">task/</span>
    ├── <span class="t-muted">task_list/</span>
    └── <span class="t-muted">ui/</span></pre>
      </div>
    </div>
  </div>

  <!-- ROADMAP -->
  <div class="section">
    <div class="section-label">Roadmap</div>
    <ul class="roadmap-list">
      <li>Packaged console command <code>todo-app</code></li>
      <li>Non-interactive subcommands: <code>add</code> · <code>list</code> · <code>done</code> · <code>remove</code> · <code>update</code></li>
      <li>Storage initialization command <code>init</code></li>
      <li>Structured logging</li>
      <li>JSON schema versioning and migrations</li>
      <li>File locking / SQLite for concurrent usage</li>
      <li>CI: Ruff · ty · pytest · coverage</li>
      <li>Release automation and changelog generation</li>
    </ul>
  </div>

  <hr>

  <div class="footer">
    todo_app · Python 3.13 · local-first · MIT · maintained by Rafał
  </div>

</div>

<a href="#top" class="scroll-to-top" title="Back to top">↑</a>

</body>
</html>