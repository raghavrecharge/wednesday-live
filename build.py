"""Builds index.html: one self-contained file (template, images, fonts inlined).

Run:  python build.py
Edit the UI in src/app.html; the creative itself comes from assets/template.svg (CorelDRAW export).
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
A = ROOT / "assets"
OUT = ROOT / "index.html"


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def must_sub(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Template changed? pattern not found: {pattern[:70]}")
    return new


svg = (A / "template.svg").read_text(encoding="utf-8")

# --- strip Corel wrapper + the subset SVG fonts (they only contain the letters used in the old names)
svg = svg[svg.index("<svg"):]
svg = re.sub(r"<font .*?</font>\s*", "", svg, flags=re.S)
svg = re.sub(r"\s*@font-face \{[^}]*\}", "", svg)
svg = must_sub(r'width="108.373mm" height="60.96mm"', 'id="art"', svg)

# --- real fonts, embedded
F = A / "fonts"
font_css = "\n".join([
    f'@font-face{{font-family:"Cera Pro";font-weight:500;src:url({data_uri(F / "Cera Pro Medium.otf", "font/otf")}) format("opentype")}}',
    f'@font-face{{font-family:"Cera Pro";font-weight:900;src:url({data_uri(F / "Cera Pro Black.otf", "font/otf")}) format("opentype")}}',
    f'@font-face{{font-family:"Sora";font-weight:400;src:url({data_uri(F / "Sora-Regular.ttf", "font/ttf")}) format("truetype")}}',
    f'@font-face{{font-family:"Sora";font-weight:700;src:url({data_uri(F / "Sora-Bold.ttf", "font/ttf")}) format("truetype")}}',
    ".fntSup {font-weight:900;font-size:174.79px;font-family:'Cera Pro'}",
    ".ph-fill {fill:#E9ECEA} .ph-text {font-family:'Sora';font-weight:400;font-size:120px;fill:#7A847E}",
])
svg = svg.replace("<![CDATA[", "<![CDATA[\n" + font_css + "\n", 1)

# --- static images
IMG = A / "images"
svg = svg.replace(r'xlink:href="45_Images\45_ImgID1.png"', f'xlink:href="{data_uri(IMG / "background.png", "image/png")}"')
svg = svg.replace(r'xlink:href="45_Images\45_ImgID4.png"', f'xlink:href="{data_uri(IMG / "headline.png", "image/png")}"')
svg = svg.replace(r'xlink:href="45_Images\45_ImgID5.png"', f'xlink:href="{data_uri(IMG / "live-badge.png", "image/png")}"')


# --- photo slots: placeholder + replaceable image inside the existing circle clips
def slot(key, label):
    return (f'<g id="{key}Slot"><circle class="ph-fill ui-only" id="{key}Ph" cx="0" cy="0" r="0"/>'
            f'<text class="ph-text ui-only" id="{key}PhText" text-anchor="middle">{label}</text>'
            f'<image id="{key}Img" preserveAspectRatio="none" x="0" y="0" width="0" height="0"/></g>')


svg = must_sub(r'<g id="_1947619060176">\s*<image [^>]*45_ImgID2\.png"/>\s*</g>', slot("host", "Add host photo"), svg)
svg = must_sub(r'<g id="_1947619061040">\s*<image [^>]*45_ImgID3\.png"/>\s*</g>', slot("astro", "Add astrologer photo"), svg)

# --- names / roles (keep Corel's x so the app can measure the original centre)
svg = must_sub(r'<text x="5143.25" y="3511.62"  class="fil10 fnt0">Anju Sharma</text>',
               '<text id="astroName" x="5143.25" y="3511.62" class="fil10 fnt0" data-orig="Anju Sharma">Anju Sharma</text>', svg)
svg = must_sub(r'<text x="5435.74" y="3662.01"  class="fil11 fnt1">Astrologer </text>',
               '<text id="astroRole" x="5435.74" y="3662.01" class="fil11 fnt1" data-orig="Astrologer">Astrologer</text>', svg)
svg = must_sub(r'<text x="3202.23" y="3508.69"  class="fil10 fnt0">Heeru Verma</text>',
               '<text id="hostName" x="3202.23" y="3508.69" class="fil10 fnt0" data-orig="Heeru Verma">Heeru Verma</text>', svg)
svg = must_sub(r'<text x="3679.76" y="3672.92"  class="fil11 fnt1">Host</text>',
               '<text id="hostRole" x="3679.76" y="3672.92" class="fil11 fnt1" data-orig="Host">Host</text>', svg)

# --- date + time block (Corel split it into ~10 pieces; rebuild as flowing text)
date_block = '''<g id="dateGroup">
   <text id="dateText" x="559.79" y="3221.9"><tspan id="dDay" class="fil12 fnt2">11</tspan><tspan id="dSuf" class="fil12 fntSup" dy="-174.78">th</tspan><tspan id="dRest" class="fil13 fnt4" dy="174.78"> Nov. 2026</tspan></text>
   <text id="timeText" x="600.04" y="3555.81" class="fil12 fnt5">7:30 PM</text>
   <rect id="istBox" class="fil14" x="1777.61" y="3344.76" width="391.67" height="224.45"/>
   <text id="istText" x="1827.37" y="3522.17" class="fil12 fnt6">IST</text>
  </g>
  '''
svg = must_sub(r'<g id="_1947619064016">.*?(?=<g style="clip-path:url\(#id3\)">)', date_block, svg, flags=re.S)

# --- drag/zoom hit areas on top (preview only)
hits = ('<circle id="hostHit" class="hit ui-only" cx="3823.43" cy="2513.39" r="767.89"/>'
        '<circle id="astroHit" class="hit ui-only" cx="5749.05" cy="2513.39" r="767.89"/>')
svg = must_sub(r"</svg>\s*$", hits + "\n</svg>\n", svg)

app = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
OUT.write_text(app.replace("<!--ARTWORK-->", svg), encoding="utf-8")
print(f"Wrote {OUT.name}  ({OUT.stat().st_size / 1e6:.1f} MB)")
