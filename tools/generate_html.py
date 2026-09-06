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
    '<a href="https://jw3b.dev" class="font-mono flex items-center gap-2 select-none mr-2" title="jw3b.dev">'
    '<span class="text-emerald-400 font-bold tracking-tight">~❯ '
    '<span class="text-slate-100">JW</span><span class="text-cyan-400">3</span>'
    '<span class="text-slate-100">B</span><span class="text-cyan-400">.</span>'
    '<span class="animate-pulse text-cyan-400">_</span></span></a>'
)

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSI Crosshair 15 Cooling Mod Guide</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config = { darkMode: 'media' }</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        html { scroll-behavior: smooth; scroll-padding-top: 4.5rem; }
        body { font-family: 'Inter', sans-serif; }
        .hero-bg { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); }
        .content p { margin-bottom: 1rem; line-height: 1.6; }
        .content li { margin-bottom: 0.5rem; }
        .content code { background-color: #f3f4f6; color: #dc2626; padding: 0.15rem 0.4rem; border-radius: 0.25rem; font-size: 0.875em; }
        .content pre { background: #0f172a; color: #e2e8f0; padding: 1rem 1.25rem; border-radius: 0.5rem; overflow-x: auto; margin: 0 0 1rem; font-size: 0.85rem; line-height: 1.5; }
        .content pre code { background: none; color: inherit; padding: 0; font-size: inherit; }
        .content table { width: 100%; border-collapse: collapse; margin: 0 0 1.25rem; font-size: 0.9rem; }
        .content th, .content td { border: 1px solid #e5e7eb; padding: 0.5rem 0.75rem; text-align: left; vertical-align: top; }
        .content th { background: #f9fafb; font-weight: 600; }
        .content blockquote { border-left: 4px solid #ef4444; background: #fef2f2; padding: 0.75rem 1rem; margin: 0 0 1rem; border-radius: 0 0.375rem 0.375rem 0; }
        .content blockquote p { margin: 0; }
        .content a { color: #dc2626; text-decoration: underline; }
        .table-wrap { overflow-x: auto; }
        @media (prefers-color-scheme: dark) {
            .content code { background-color: #1f2937; color: #f87171; }
            .content th, .content td { border-color: #374151; }
            .content th { background: #1f2937; }
            .content blockquote { background: #3f1d1d; }
            .content a { color: #f87171; }
        }
        @media print {
            nav, .hero-img, footer { display: none !important; }
            body { background: #fff !important; color: #000 !important; }
            section { break-inside: avoid; box-shadow: none !important; border: 1px solid #ccc !important; }
            .content pre { background: #f3f4f6 !important; color: #000 !important; border: 1px solid #ccc; }
            a { color: #000 !important; text-decoration: none; }
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-700 dark:bg-gray-950 dark:text-gray-300">

    <header class="hero-bg text-white py-16 shadow-lg mb-8">
        <div class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center gap-8">
            <div class="flex-1">
                <span class="font-mono text-sm text-cyan-400"><span class="text-emerald-400">~❯</span> jw3b.dev / crosshair15-cooling <span class="text-slate-500">// extreme desktop replacement</span></span>
                <h1 class="text-4xl md:text-5xl font-bold mt-2 mb-4 leading-tight">MSI Crosshair 15<br/>Cooling Mod Guide</h1>
                <p class="text-gray-300 text-lg">Deep-dive build guides, complete parts lists, and risk mitigation strategies for pushing the i9-12900H and RTX 3070 Ti beyond factory limits &mdash; now with a Linux-native tuning and validation path.</p>
            </div>
            <div class="flex-1 flex justify-center hero-img">
                <img src="https://asset.msi.com/resize/image/global/product/product_1641372545f95843dcceec4f23b2ed2ebf53106be8.png62405b38c58fe0f07fcef2367d8a9ba1/1024.png" alt="MSI Crosshair 15" class="w-full max-w-lg drop-shadow-2xl hover:scale-105 transition-transform duration-300 object-contain">
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
          if (net) net.textContent = navigator.onLine ? '🟢 connected' : '🔴 offline';
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
    t = re.sub(r"\*\*(.+?)\*\*", r'<strong class="text-gray-900 dark:text-gray-100">\1</strong>', t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r'<em class="text-gray-600 dark:text-gray-400">\1</em>', t)
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
                self.out.append(f'<h2 id="{sid}" class="text-3xl font-bold text-gray-900 dark:text-gray-100 border-b-2 border-red-500 pb-2 mb-6 mt-4 inline-block">{title}</h2>\n')
            elif line.startswith("### "):
                self.close_list()
                self.out.append(f'<h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mt-8 mb-4">{inline(line[4:])}</h3>\n')
            elif line.startswith("#### "):
                self.close_list()
                self.out.append(f'<h4 class="text-base font-semibold text-gray-800 dark:text-gray-200 mt-6 mb-2 uppercase tracking-wide">{inline(line[5:])}</h4>\n')
            elif line.startswith(("* ", "- ")):
                if self.list_type != "ul":
                    self.close_list()
                    self.out.append('<ul class="list-disc pl-6 mb-4 space-y-2 text-gray-600 dark:text-gray-400">\n')
                    self.list_type = "ul"
                self.out.append(f"<li>{inline(line[2:])}</li>\n")
            elif re.match(r"^\d+\.\s", line):
                if self.list_type != "ol":
                    self.close_list()
                    start = int(line.split(".", 1)[0])
                    attr = f' start="{start}"' if start != 1 else ""
                    self.out.append(f'<ol{attr} class="list-decimal pl-6 mb-4 space-y-2 text-gray-600 dark:text-gray-400">\n')
                    self.list_type = "ol"
                self.out.append(f'<li class="pl-2">{inline(re.sub(r"^\d+\.\s*", "", line))}</li>\n')
            else:
                self.close_list()
                self.out.append(f'<p class="text-gray-600 dark:text-gray-400">{inline(line)}</p>\n')
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
        caption = (f'<p class="text-[10px] text-gray-400 dark:text-gray-500 mt-2 text-center">Photo: <a href="{credit[1]}" class="underline" target="_blank" rel="noopener">{credit[0]}</a></p>'
                   if credit else "")
        body = r.section(sec)
        if img:
            rendered.append(
                '<section class="bg-white dark:bg-gray-900 rounded-xl shadow-md border border-gray-200 dark:border-gray-800 overflow-hidden flex flex-col lg:flex-row">\n'
                f'<div class="p-8 content lg:w-2/3">{body}</div>\n'
                '<div class="bg-gray-50 dark:bg-gray-800 lg:w-1/3 flex flex-col items-center justify-center p-8 border-l border-gray-100 dark:border-gray-800 hero-img">'
                f'<img src="{img}" alt="Mod Illustration" loading="lazy" onerror="this.parentElement.remove()" class="max-w-full h-auto rounded-lg shadow-sm mix-blend-multiply dark:mix-blend-normal object-contain max-h-80 hover:scale-105 transition-transform duration-300">{caption}</div>\n'
                "</section>"
            )
        else:
            rendered.append(
                '<section class="bg-white dark:bg-gray-900 rounded-xl shadow-md border border-gray-200 dark:border-gray-800 overflow-hidden p-8 content">'
                f"{body}</section>"
            )

    nav = (
        '<nav class="sticky top-0 z-20 bg-slate-950/95 backdrop-blur border-b border-slate-800 mb-8">'
        '<div class="max-w-6xl mx-auto px-6 py-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">'
        + BRAND_HEADER +
        '<span class="text-slate-700 hidden sm:inline">|</span>'
        + "".join(
            f'<a href="#{sid}" class="font-mono text-slate-400 hover:text-cyan-400 whitespace-nowrap">{inline(t.split(":")[0])}</a>'
            for sid, t in r.toc
        )
        + "</div></nav>\n"
    )

    out = HEAD + nav + '<main class="max-w-6xl mx-auto px-6 py-6 space-y-16">\n' + "\n".join(rendered) + "\n</main>" + FOOT
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out)
    print(f"wrote {DST} ({len(out):,} bytes, {len(r.toc)} sections)")


if __name__ == "__main__":
    convert_to_html()
