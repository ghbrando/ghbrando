"""Render the profile's SVG artwork in light and dark variants.

Same system as the resume site: Swiss / International Typographic. Paper, ink,
one red accent, 1px rules, Helvetica and a monospace. No gradients, no rounded
corners, no glow. GitHub serves SVGs as images, so only system fonts render and
animation has to be pure CSS inside the file.

    python scripts/build.py      # writes assets/*.svg
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": {"paper": "#f2f0ea", "ink": "#0b0b0b", "dim": "#0b0b0b8c", "rule": "#0b0b0b38"},
    "dark": {"paper": "#0d1117", "ink": "#f2f0ea", "dim": "#f2f0ea94", "rule": "#f2f0ea3d"},
}
ACCENT = "#e2231a"
GROTESK = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# The terminal replays the NREIP agent recovering a downed range switch.
TERMINAL = [
    ("cmd", "$ agent diagnose range-switch-07"),
    ("out", "› device record ............ ok"),
    ("out", "› scan 10.0.4.0/24 ......... 42 hosts"),
    ("out", "› ssh diagnostics .......... port 12 down"),
    ("out", "› ePDU cycle outlet 12 ..... ok"),
    ("ok", "✓ recovered in 38s"),
    ("dim", "  0 cloud calls · llama.cpp · local"),
]
CYCLE = 14.0  # seconds per replay
STEP = 1.1    # seconds between lines

FACTS = [
    ("Study", "CS & AI/ML · CBU · B.S. ’27 / M.S. ’28"),
    ("Program", "SMART Scholar · NSWC Dahlgren"),
    ("Clearance", "DoD Secret · Active"),
]

PROJECTS = [
    {
        "slug": "agent", "title": "Offline Ops Agent", "meta": "NSWC Corona · NREIP ’26",
        "desc": "Air-gapped LLM agent that diagnoses and recovers downed range equipment on its own.",
        "tags": "llama.cpp · Rust · NixOS · Docker · Whisper",
    },
    {
        "slug": "dina", "title": "DINA", "meta": "CBU AI/ML Lab · Team lead",
        "desc": "GraphRAG for Navy and Air Force analysts. 25% more accurate than baseline RAG.",
        "tags": "Neo4j · GraphRAG · GCP · Python",
    },
    {
        "slug": "nl2logic", "title": "nl2logic", "meta": "Research · 5-paper series",
        "desc": "Military doctrine into formal logic, with proofs instead of guesses.",
        "tags": "T5 · constrained decoding · KIF · Vampire", "link": True,
    },
    {
        "slug": "unicore", "title": "UniCore", "meta": "Team project",
        "desc": "Rent out spare CPU, or boot a Linux VM on someone else's laptop from the browser.",
        "tags": ".NET 10 · Blazor · GCP · Docker", "link": True,
    },
    {
        "slug": "fod", "title": "F.O.D. Hunter", "meta": "Team project",
        "desc": "Drone-based debris detection for flight decks, driven by voice.",
        "tags": "YOLOv8 · ONNX · Whisper · React", "link": True,
    },
    {
        "slug": "robot", "title": "Autonomous Robot", "meta": "1st place · Lead engineer",
        "desc": "Competition-record 3,000 points, 2,000 ahead of second place.",
        "tags": "PID control · microcontrollers · Python",
    },
]


def style(t):
    return f"""<style>
  .g {{ font-family: {GROTESK}; }}
  .m {{ font-family: {MONO}; }}
  .ink {{ fill: {t['ink']}; }}
  .dim {{ fill: {t['dim']}; }}
  .red {{ fill: {ACCENT}; }}
  .cap {{ font-size: 11px; letter-spacing: .16em; text-transform: uppercase; }}
</style>"""


def hero(name, t):
    W, H = 1000, 440
    tx, ty, tw, th = 548, 92, 404, 236  # terminal panel
    term_ink = {"cmd": "#f2f0ea", "out": "#f2f0eab3", "ok": ACCENT, "dim": "#f2f0ea73"}

    keyframes, lines = [], []
    for i, (kind, text) in enumerate(TERMINAL):
        on = (0.6 + i * STEP) / CYCLE * 100
        keyframes.append(
            f"@keyframes l{i} {{ 0%, {on - 0.01:.2f}% {{ opacity: 0 }} "
            f"{on:.2f}%, 94% {{ opacity: 1 }} 97%, 100% {{ opacity: 0 }} }}"
        )
        weight = ' font-weight="700"' if kind in ("cmd", "ok") else ""
        lines.append(
            f'<text x="{tx + 18}" y="{ty + 58 + i * 23}" class="m" font-size="13"{weight} '
            f'fill="{term_ink[kind]}" style="animation: l{i} {CYCLE}s linear infinite">'
            f"{escape(text)}</text>"
        )
    cursor_y = ty + 58 + len(TERMINAL) * 23

    facts = []
    for i, (label, value) in enumerate(FACTS):
        x = 48 + i * 318
        facts.append(
            f'<text x="{x}" y="{H - 52}" class="m cap red">{escape(label)}</text>'
            f'<text x="{x}" y="{H - 28}" class="g ink" font-size="15">{escape(value)}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Brandon Magana. Offline AI agents, knowledge graphs, and systems that run where the network does not reach.">
{style(t)}
<style>
  {chr(10).join(keyframes)}
  @keyframes blink {{ 0%, 49% {{ opacity: 1 }} 50%, 100% {{ opacity: 0 }} }}
  @keyframes live {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px) }} to {{ opacity: 1; transform: none }} }}
  .n1 {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
  .n2 {{ animation: rise .7s .12s cubic-bezier(.2,.7,.2,1) both; }}
  .ld {{ animation: rise .7s .3s cubic-bezier(.2,.7,.2,1) both; }}
</style>
<rect width="{W}" height="{H}" fill="{t['paper']}"/>

<text x="48" y="38" class="m cap ink">Magana, Brandon</text>
<text x="{W - 48}" y="38" class="m cap dim" text-anchor="end">Index / 2026</text>
<rect x="48" y="52" width="{W - 96}" height="1" fill="{t['ink']}"/>

<text x="44" y="176" class="g ink n1" font-size="104" font-weight="700" letter-spacing="-4">Brandon</text>
<text x="44" y="268" class="g ink n2" font-size="104" font-weight="700" letter-spacing="-4">Magana<tspan class="red" font-size="104">.</tspan></text>

<g class="ld">
  <text x="48" y="312" class="g ink" font-size="17">Offline AI agents, knowledge graphs, and systems</text>
  <text x="48" y="336" class="g dim" font-size="17">that run where the network does not reach.</text>
</g>

<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="#0b0b0b"/>
<rect x="{tx + .5}" y="{ty + .5}" width="{tw - 1}" height="{th - 1}" fill="none" stroke="{t['rule']}"/>
<rect x="{tx}" y="{ty}" width="{tw}" height="30" fill="#161616"/>
<rect x="{tx + 16}" y="{ty + 11}" width="8" height="8" fill="{ACCENT}" style="animation: live 2.4s ease-in-out infinite"/>
<text x="{tx + 32}" y="{ty + 19.5}" class="m" font-size="11" letter-spacing=".08em" fill="#f2f0ea99">agent@range-console · offline</text>
<text x="{tx + tw - 16}" y="{ty + 19.5}" class="m" font-size="11" fill="#f2f0ea59" text-anchor="end">no network</text>
{chr(10).join(lines)}
<rect x="{tx + 18}" y="{cursor_y - 11}" width="8" height="14" fill="{ACCENT}" style="animation: blink 1s steps(1) infinite"/>

<rect x="48" y="{H - 82}" width="{W - 96}" height="1" fill="{t['rule']}"/>
{chr(10).join(facts)}
</svg>
"""
    (OUT / f"hero-{name}.svg").write_text(svg, encoding="utf-8")


def row(p, i, name, t):
    W, H = 1000, 120
    arrow = (
        f'<text x="{W - 4}" y="54" class="g red" font-size="30" text-anchor="end">→</text>'
        if p.get("link") else ""
    )
    meta_x = W - 56 if p.get("link") else W - 4
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p['title'])}: {escape(p['desc'])}">
{style(t)}
<rect x="0" y="0" width="{W}" height="1" fill="{t['ink']}"/>
<text x="0" y="50" class="m red" font-size="14" font-weight="700">{i:02d}</text>
<text x="64" y="54" class="g ink" font-size="32" font-weight="700" letter-spacing="-1">{escape(p['title'])}</text>
<text x="{meta_x}" y="50" class="m cap dim" text-anchor="end">{escape(p['meta'])}</text>
{arrow}
<text x="64" y="84" class="g ink" font-size="17">{escape(p['desc'])}</text>
<text x="64" y="108" class="m dim" font-size="12.5" letter-spacing=".04em">{escape(p['tags'])}</text>
</svg>
"""
    (OUT / f"row-{p['slug']}-{name}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        hero(name, t)
        for i, p in enumerate(PROJECTS, 1):
            row(p, i, name, t)
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)
