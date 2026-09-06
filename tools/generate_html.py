#!/usr/bin/env python3
"""Render Cooling_Mod_Report.md -> Cooling_Mod_Report.html (Tailwind, TOC, dark mode, print CSS).

Supported markdown: #..#### headings, *, -, 1. lists, **bold**, *em*, `code`, [text](url),
fenced ``` code blocks, | pipe | tables |, > blockquotes. Sections are split on '---' lines.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "Cooling_Mod_Report.md"
DST = HERE.parent / "site" / "index.html"

# Section heading prefix -> side illustration (sections without one render full width)
IMAGES = {
    "Mod 1": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=800&q=80",
    "Mod 2": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=800&q=80",
    "Mod 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Water_Cooled_PC.jpg/960px-Water_Cooled_PC.jpg",
    "Mod 4": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=800&q=80",
    "Part 5": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=800&q=80",
    "Part 6": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
}
# Attribution for images whose licence requires it (rendered as a caption under the image)
CREDITS = {
    "Mod 3": ('"Water Cooled PC" via Wikimedia Commons, CC BY-SA 2.0',
              "https://commons.wikimedia.org/wiki/File:Water_Cooled_PC.jpg"),
}
SECTION_KEY = re.compile(r"^## ((?:Mod|Part) \d+[a-z]?)\b", re.M)

# jw3b.dev brand header (BrandHeader.jsx, mode="full") translated to static Tailwind
BRAND_HEADER = (
    '<a href="https://jw3b.dev" class="jw3b-brand font-mono flex items-center gap-2 select-none mr-2" title="jw3b.dev">'
    '<span class="text-emerald-400 font-bold tracking-tight">~❯ '
    '<span class="jw3b-t text-slate-100" style="--i:0">J</span>'
    '<span class="jw3b-t text-slate-100" style="--i:1">W</span>'
    '<span class="jw3b-t text-cyan-400" style="--i:2">3</span>'
    '<span class="jw3b-t text-slate-100" style="--i:3">B</span>'
    '<span class="jw3b-t text-cyan-400" style="--i:4">.</span>'
    '<span class="jw3b-cursor text-cyan-400" aria-hidden="true">_</span></span></a>'
)

HEAD = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSI Crosshair 15 Cooling Mod Guide</title>
    <meta name="description" content="Cooling mods, researched alternatives and Linux thermal tooling for the MSI Crosshair 15 B12UGSZ. By jw3b.dev.">
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#020617">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config = { darkMode: 'class', theme: { extend: { fontFamily: { mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'], sans: ['Inter', 'system-ui', 'sans-serif'] } } } }</script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        html { scroll-behavior: smooth; scroll-padding-top: 4.5rem; }
        body {
            font-family: 'Inter', system-ui, sans-serif; background-color: #020617; color: #cbd5e1;
            background-image: linear-gradient(rgba(34,211,238,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(34,211,238,.045) 1px, transparent 1px);
            background-size: 32px 32px;
        }
        .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; }
        .glow { text-shadow: 0 0 18px rgba(34,211,238,.35); }
        .panel { background: rgba(15,23,42,.72); border: 1px solid #1e293b; box-shadow: 0 0 0 1px rgba(34,211,238,.04), 0 20px 60px -30px rgba(34,211,238,.25); backdrop-filter: blur(6px); }
        .panel-bar { border-bottom: 1px solid #1e293b; background: rgba(2,6,23,.6); }
        .content p { margin-bottom: 1rem; line-height: 1.7; }
        .content li { margin-bottom: 0.5rem; line-height: 1.6; }
        .content ul > li::marker { color: #22d3ee; }
        .content ol > li::marker { color: #34d399; font-family: 'JetBrains Mono', monospace; }
        .content code { font-family: 'JetBrains Mono', monospace; background: rgba(34,211,238,.08); color: #67e8f9; border: 1px solid rgba(34,211,238,.15); padding: 0.1rem 0.4rem; border-radius: 0.25rem; font-size: 0.85em; }
        .content pre { font-family: 'JetBrains Mono', monospace; background: #020617; color: #a7f3d0; border: 1px solid #1e293b; border-left: 3px solid #34d399; padding: 1rem 1.25rem; border-radius: 0.375rem; overflow-x: auto; margin: 0 0 1rem; font-size: 0.82rem; line-height: 1.55; }
        .content pre code { background: none; border: 0; color: inherit; padding: 0; font-size: inherit; }
        .content table { width: 100%; border-collapse: collapse; margin: 0 0 1.25rem; font-size: 0.88rem; }
        .content th, .content td { border: 1px solid #1e293b; padding: 0.55rem 0.75rem; text-align: left; vertical-align: top; }
        .content th { font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 0.75rem; letter-spacing: .06em; text-transform: uppercase; color: #22d3ee; background: rgba(2,6,23,.7); }
        .content tr:nth-child(even) td { background: rgba(2,6,23,.35); }
        .content blockquote { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; border: 1px solid rgba(251,191,36,.35); border-left: 3px solid #fbbf24; background: rgba(251,191,36,.06); color: #fde68a; padding: 0.75rem 1rem; margin: 0 0 1rem; border-radius: 0 0.375rem 0.375rem 0; }
        .content blockquote p { margin: 0; }
        .content blockquote p::before { content: "// WARN  "; color: #fbbf24; font-weight: 700; }
        .content a { color: #22d3ee; text-decoration: underline; text-decoration-color: rgba(34,211,238,.4); text-underline-offset: 3px; }
        .content a:hover { color: #67e8f9; text-decoration-color: #67e8f9; }
        .content h2 .hash { color: #22d3ee; margin-right: .5rem; }
        .table-wrap { overflow-x: auto; }
        .fig { border: 1px solid #1e293b; border-radius: .375rem; overflow: hidden; background: #020617; }
        .fig img { filter: saturate(.85) contrast(1.05); opacity: .9; transition: all .3s; }
        .fig:hover img { filter: none; opacity: 1; }
        /* jw3b.dev brand: the mark types itself in after the prompt, then a terminal cursor blinks */
        .jw3b-t { opacity: 0; animation: jw3b-in 0.01s steps(1) forwards; animation-delay: calc(0.5s + var(--i) * 0.14s); }
        .jw3b-cursor { animation: jw3b-blink 1s steps(1, end) infinite; }
        .jw3b-brand:hover .jw3b-t { animation: jw3b-in 0.01s steps(1) forwards; animation-delay: calc(var(--i) * 0.12s); opacity: 0; }
        .hero-line { opacity: 0; animation: jw3b-in 0.01s steps(1) forwards; }
        @keyframes jw3b-in { to { opacity: 1; } }
        @keyframes jw3b-blink { 0%, 50% { opacity: 1; } 50.01%, 100% { opacity: 0; } }
        @keyframes scan { from { transform: translateY(-100%); } to { transform: translateY(100vh); } }
        .scan { pointer-events: none; position: fixed; left: 0; right: 0; top: 0; height: 2px; background: linear-gradient(90deg, transparent, rgba(34,211,238,.25), transparent); animation: scan 9s linear infinite; z-index: 5; }
        @media (prefers-reduced-motion: reduce) {
            .jw3b-t, .jw3b-brand:hover .jw3b-t, .hero-line { animation: none; opacity: 1; }
            .jw3b-cursor, .scan { animation: none; }
            .scan { display: none; }
        }
        @media print {
            nav, .hero-img, footer, .scan { display: none !important; }
            body { background: #fff !important; color: #000 !important; background-image: none !important; }
            .panel { background: #fff !important; border: 1px solid #ccc !important; box-shadow: none !important; break-inside: avoid; }
            .content pre { background: #f3f4f6 !important; color: #000 !important; border: 1px solid #ccc; }
            a { color: #000 !important; text-decoration: none; }
        }
    </style>
</head>
<body class="antialiased">
    <div class="scan"></div>

    <!-- Hero: a terminal window. The brand mark types itself in; the readouts are the Part 0 baseline of this machine. -->
    <header class="max-w-6xl mx-auto px-6 pt-10 pb-4">
        <div class="panel rounded-lg overflow-hidden">
            <div class="panel-bar px-4 py-2 flex items-center gap-3 mono text-xs text-slate-500">
                <span class="flex gap-1.5"><span class="h-3 w-3 rounded-full bg-rose-500/80"></span><span class="h-3 w-3 rounded-full bg-amber-400/80"></span><span class="h-3 w-3 rounded-full bg-emerald-400/80"></span></span>
                <span>jw3b@crosshair15: ~/cooling</span>
                <span class="ml-auto hidden sm:inline">[8453:BASE] <span id="jw3b-net-top">🟢 connected</span></span>
            </div>
            <div class="grid lg:grid-cols-5 gap-8 px-6 sm:px-10 py-10">
                <div class="lg:col-span-3 mono">
                    <div class="text-5xl sm:text-7xl font-bold tracking-tight glow mb-6 jw3b-brand">
                        <span class="text-emerald-400">~❯ </span><span class="jw3b-t text-slate-100" style="--i:0">J</span><span class="jw3b-t text-slate-100" style="--i:1">W</span><span class="jw3b-t text-cyan-400" style="--i:2">3</span><span class="jw3b-t text-slate-100" style="--i:3">B</span><span class="jw3b-t text-cyan-400" style="--i:4">.</span><span class="jw3b-cursor text-cyan-400" aria-hidden="true">_</span>
                    </div>
                    <p class="hero-line text-slate-500 text-sm mb-1" style="animation-delay:1.4s"><span class="text-emerald-400">~❯</span> cat Cooling_Mod_Report.md</p>
                    <h1 class="hero-line text-2xl sm:text-3xl font-bold text-slate-100 leading-tight mb-3" style="animation-delay:1.6s">MSI Crosshair 15 <span class="text-cyan-400">//</span> Cooling Mod Guide</h1>
                    <p class="hero-line font-sans text-slate-400 text-base leading-relaxed max-w-xl" style="animation-delay:1.8s">Four hardware mods with researched alternatives, a zero-hardware software path, a decision matrix, and Linux-native tuning and validation for the i9-12900H and RTX 3070 Ti. Every number below was read from this machine.</p>
                    <p class="hero-line mt-5 flex flex-wrap gap-2 text-xs" style="animation-delay:2.0s">
                        <a href="#mod-0-the-zero-hardware-software-path" class="border border-cyan-400/40 text-cyan-300 px-3 py-1 rounded hover:bg-cyan-400/10">./start --free</a>
                        <a href="#tiers-and-decision-matrix" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-cyan-400/40 hover:text-cyan-300">./decide</a>
                        <a href="#part-6b-linux-validation-suite" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-cyan-400/40 hover:text-cyan-300">./validate</a>
                        <a href="https://github.com/jw3b-dev/crosshair15-cooling" class="border border-slate-700 text-slate-300 px-3 py-1 rounded hover:border-emerald-400/40 hover:text-emerald-300">git clone</a>
                    </p>
                </div>
                <div class="lg:col-span-2 mono text-xs hero-line" style="animation-delay:1.2s">
                    <div class="border border-slate-800 rounded bg-slate-950/80 p-4 space-y-1.5">
                        <div class="text-slate-500 mb-2">// baseline 2026-09-06 · tools/thermal_baseline.sh</div>
                        <div class="flex justify-between"><span class="text-slate-400">pkg_temp</span><span class="text-rose-400 font-bold">96 °C <span class="text-rose-500/70">CRIT</span></span></div>
                        <div class="flex justify-between"><span class="text-slate-400">core_spread</span><span class="text-rose-400 font-bold">29 °C</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">fans</span><span class="text-amber-300">6857 / 6233 rpm <span class="text-slate-500">boost=on</span></span></div>
                        <div class="flex justify-between"><span class="text-slate-400">PL1 / PL2</span><span class="text-amber-300">30 W / 45 W <span class="text-slate-500">spec 45/115</span></span></div>
                        <div class="flex justify-between"><span class="text-slate-400">throttle_count</span><span class="text-rose-400">3,231,620 <span class="text-slate-500">+6/s</span></span></div>
                        <div class="flex justify-between"><span class="text-slate-400">gpu</span><span class="text-emerald-400">45 °C · 25 W · idle</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">msi-ec</span><span class="text-slate-300">shift=<span class="text-amber-300">unknown(192)</span> fan=auto</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">kernel</span><span class="text-slate-300">7.0.0-31 · ubuntu 24.04.4 · x11</span></div>
                        <div class="pt-2 mt-2 border-t border-slate-800 text-slate-500">verdict: <span class="text-cyan-300">TIM failed or mount uneven → Mod 4 first</span></div>
                    </div>
                </div>
            </div>
        </div>
    </header>
"""

FOOT = """
    <!-- IdeFooter.jsx translated to static Tailwind; status values are live, not hardcoded -->
    <footer class="mt-12 bg-slate-950 border-t border-slate-800 font-mono text-slate-500">
        <div class="max-w-6xl mx-auto px-6 py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm">
            <div class="flex items-center gap-3">
                <a href="https://jw3b.dev" class="font-bold tracking-tight text-slate-100 hover:text-cyan-400">JW<span class="text-cyan-400">3</span>B<span class="text-cyan-400">.</span></a>
                <span class="text-slate-700">|</span>
                <a href="https://github.com/jw3b-dev" class="hover:text-cyan-400">github.com/jw3b-dev</a>
                <span class="text-slate-700">|</span>
                <a href="https://github.com/jw3b-dev/crosshair15-cooling" class="hover:text-cyan-400">source &amp; tooling</a>
            </div>
            <div class="text-slate-600 text-xs">MSI Crosshair 15 B12UGSZ &middot; cooling mods &amp; Linux thermal tooling &middot; MIT</div>
        </div>
        <div class="h-6 w-full bg-slate-950 border-t border-slate-800 px-3 flex items-center justify-between text-xs">
            <div class="flex items-center gap-3">
                <span class="flex items-center gap-1 text-emerald-400">
                    <span class="relative flex h-2 w-2"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span></span>
                    KTHULHU_ORCHESTRATOR_ONLINE
                </span>
                <span>|</span>
                <span>ENV: PRODUCTION</span>
                <span class="hidden sm:inline">|</span>
                <span class="hidden sm:inline">[8453:BASE] <span id="jw3b-net">🟢 connected</span> | latency: <span id="jw3b-lat">…</span></span>
            </div>
            <div class="flex items-center gap-2 text-slate-400 hover:text-cyan-400 transition-colors">
                <span>// STAY WEIRD</span>
                <span class="text-sm">👽</span>
            </div>
        </div>
    </footer>
    <script>
      (function () {
        var lat = document.getElementById('jw3b-lat'), net = document.getElementById('jw3b-net');
        function tick() {
          var nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
          var ms = nav ? Math.max(1, Math.round(nav.responseStart - nav.requestStart)) : null;
          if (lat) lat.textContent = ms ? ms + 'ms' : 'n/a';
          var txt = navigator.onLine ? '🟢 connected' : '🔴 offline';
          if (net) net.textContent = txt;
          var top = document.getElementById('jw3b-net-top'); if (top) top.textContent = txt;
        }
        tick(); window.addEventListener('online', tick); window.addEventListener('offline', tick);
      })();
    </script>
</body>
</html>
"""


def slug(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def inline(text: str) -> str:
    """Escape HTML, then apply inline markdown."""
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    # bare URLs (not already inside an href or a markdown link)
    t = re.sub(r'(?<!["\'>(])(https?://[^\s<>"]+?)(?=[.,;:)]*(?:\s|$))',
               r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r'<strong class="text-slate-100 font-semibold">\1</strong>', t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r'<em class="text-slate-400">\1</em>', t)
    return t


def render_table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    if len(cells) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in cells[1] if c):
        head, body = cells[0], cells[2:]
    else:
        head, body = None, cells
    out = ['<div class="table-wrap"><table>']
    if head:
        out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
    out.append("<tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out) + "\n"


class Renderer:
    def __init__(self):
        self.out: list[str] = []
        self.list_type: str | None = None
        self.table: list[str] = []
        self.quote: list[str] = []
        self.toc: list[tuple[str, str]] = []

    def close_list(self):
        if self.list_type:
            self.out.append(f"</{self.list_type}>\n")
            self.list_type = None

    def flush_table(self):
        if self.table:
            self.out.append(render_table(self.table))
            self.table = []

    def flush_quote(self):
        if self.quote:
            self.out.append("<blockquote>" + "".join(f"<p>{inline(q)}</p>" for q in self.quote) + "</blockquote>\n")
            self.quote = []

    def flush_all(self):
        self.close_list()
        self.flush_table()
        self.flush_quote()

    def section(self, text: str) -> str:
        self.out = []
        lines = text.strip("\n").split("\n")
        i = 0
        while i < len(lines):
            raw = lines[i]
            line = raw.strip()

            if line.startswith("```"):
                self.flush_all()
                lang = line[3:].strip()
                buf = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                cls = f' class="language-{lang}"' if lang else ""
                self.out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre>\n")
                i += 1
                continue

            if line.startswith("|"):
                self.close_list(); self.flush_quote()
                self.table.append(line)
                i += 1
                continue
            self.flush_table()

            if line.startswith(">"):
                self.close_list()
                self.quote.append(line[1:].strip())
                i += 1
                continue
            self.flush_quote()

            if not line:
                i += 1
                continue

            if line.startswith("# "):
                pass  # document title lives in the hero
            elif line.startswith("## "):
                self.close_list()
                title = inline(line[3:])
                sid = slug(line[3:])
                self.toc.append((sid, line[3:]))
                self.out.append(f'<h2 id="{sid}" class="mono text-2xl sm:text-3xl font-bold text-slate-100 tracking-tight mb-6 mt-2"><span class="hash">#</span>{title}</h2>\n')
            elif line.startswith("### "):
                self.close_list()
                self.out.append(f'<h3 class="mono text-lg font-semibold text-cyan-300 mt-8 mb-4"><span class="text-slate-600 mr-2">##</span>{inline(line[4:])}</h3>\n')
            elif line.startswith("#### "):
                self.close_list()
                self.out.append(f'<h4 class="mono text-xs font-semibold text-emerald-400 mt-6 mb-2 uppercase tracking-widest">{inline(line[5:])}</h4>\n')
            elif line.startswith(("* ", "- ")):
                if self.list_type != "ul":
                    self.close_list()
                    self.out.append('<ul class="list-disc pl-6 mb-4 space-y-2 text-slate-300">\n')
                    self.list_type = "ul"
                self.out.append(f"<li>{inline(line[2:])}</li>\n")
            elif re.match(r"^\d+\.\s", line):
                if self.list_type != "ol":
                    self.close_list()
                    start = int(line.split(".", 1)[0])
                    attr = f' start="{start}"' if start != 1 else ""
                    self.out.append(f'<ol{attr} class="list-decimal pl-6 mb-4 space-y-2 text-slate-300">\n')
                    self.list_type = "ol"
                self.out.append(f'<li class="pl-2">{inline(re.sub(r"^\d+\.\s*", "", line))}</li>\n')
            else:
                self.close_list()
                self.out.append(f'<p class="text-slate-300">{inline(line)}</p>\n')
            i += 1

        self.flush_all()
        return "".join(self.out)


def convert_to_html():
    md = SRC.read_text()
    sections = [s for s in re.split(r"\n---+\n", md) if s.strip()]
    r = Renderer()

    rendered = []
    for sec in sections:
        m = SECTION_KEY.search(sec)
        img = IMAGES.get(m.group(1)) if m else None
        credit = CREDITS.get(m.group(1)) if m else None
        caption = (f'<p class="mono text-[10px] text-slate-500 mt-2 text-center">// photo: <a href="{credit[1]}" class="underline" target="_blank" rel="noopener">{credit[0]}</a></p>'
                   if credit else "")
        body = r.section(sec)
        label = m.group(1).lower().replace(" ", "-") if m else "readme"
        bar = f'<div class="panel-bar px-5 py-1.5 mono text-[11px] text-slate-500 flex items-center gap-2"><span class="text-emerald-400">~❯</span> less {label}.md <span class="ml-auto text-slate-700">jw3b.dev</span></div>'
        if img:
            rendered.append(
                f'<section class="panel rounded-lg overflow-hidden">{bar}<div class="flex flex-col lg:flex-row">\n'
                f'<div class="p-6 sm:p-8 content lg:w-2/3">{body}</div>\n'
                '<div class="lg:w-1/3 flex flex-col items-center justify-center p-6 sm:p-8 border-t lg:border-t-0 lg:border-l border-slate-800 hero-img">'
                f'<div class="fig"><img src="{img}" alt="Mod Illustration" loading="lazy" onerror="this.closest(\'.hero-img\').remove()" class="max-w-full h-auto object-contain max-h-80"></div>{caption}</div>\n'
                "</div></section>"
            )
        else:
            rendered.append(
                f'<section class="panel rounded-lg overflow-hidden">{bar}<div class="p-6 sm:p-8 content">'
                f"{body}</div></section>"
            )

    nav = (
        '<nav class="sticky top-0 z-20 bg-slate-950/90 backdrop-blur border-y border-slate-800 mb-10">'
        '<div class="max-w-6xl mx-auto px-6 py-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs mono">'
        + BRAND_HEADER +
        '<span class="text-slate-700 hidden sm:inline">|</span>'
        + "".join(
            f'<a href="#{sid}" class="text-slate-400 hover:text-cyan-300 whitespace-nowrap">{inline(t.split(":")[0])}</a>'
            for sid, t in r.toc
        )
        + "</div></nav>\n"
    )

    out = HEAD + nav + '<main class="max-w-6xl mx-auto px-6 pb-6 space-y-10">\n' + "\n".join(rendered) + "\n</main>" + FOOT
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out)
    print(f"wrote {DST} ({len(out):,} bytes, {len(r.toc)} sections)")


if __name__ == "__main__":
    convert_to_html()
