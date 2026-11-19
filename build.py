"""Builds the creative generators as self-contained pages (template, images, fonts inlined).

    python build.py

  index.html          <- Wednesday Live   (src/wednesday.html + assets/wednesday/)
  sunday/index.html   <- Sunday Live      (src/sunday.html    + assets/sunday/)

Shared styles live in src/common.css. Templates are CorelDRAW SVG exports.
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
A = ROOT / "assets"
F = A / "fonts"
SRC = ROOT / "src"


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def must_sub(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, lambda m: repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"Template changed? pattern not found: {pattern[:80]}")
    return new


def font_face(family, weight, file):
    fmt, mime = ("opentype", "font/otf") if file.endswith(".otf") else ("truetype", "font/ttf")
    return f'@font-face{{font-family:"{family}";font-weight:{weight};src:url({data_uri(F / file, mime)}) format("{fmt}")}}'


def prepare_svg(path, fonts_css):
    """Strip Corel wrapper + subset SVG fonts, embed real fonts, give the root an id."""
    svg = path.read_text(encoding="utf-8")
    svg = svg[svg.index("<svg"):]
    svg = re.sub(r"<font .*?</font>\s*", "", svg, flags=re.S)
    svg = re.sub(r"\s*@font-face \{[^}]*\}", "", svg)
    svg = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', 'id="art"', svg, count=1)
    return svg.replace("<![CDATA[", "<![CDATA[\n" + fonts_css + "\n", 1)


NAV = [("wednesday", "Wednesday Live"), ("sunday", "Sunday Live")]


def page(src_name, svg, active, root_prefix):
    nav = "".join(
        f'<a href="{root_prefix}{"" if key == "wednesday" else key + "/"}"{" class=active" if key == active else ""}>{label}</a>'
        for key, label in NAV)
    html = (SRC / src_name).read_text(encoding="utf-8")
    html = html.replace("/*COMMON_CSS*/", (SRC / "common.css").read_text(encoding="utf-8"))
    html = html.replace("<!--NAV-->", f"<nav>{nav}</nav>")
    return html.replace("<!--ARTWORK-->", svg)


# ---------------------------------------------------------------- Wednesday
def build_wednesday():
    W = A / "wednesday"
    css = "\n".join([
        font_face("Cera Pro", 500, "Cera Pro Medium.otf"),
        font_face("Cera Pro", 900, "Cera Pro Black.otf"),
        font_face("Sora", 400, "Sora-Regular.ttf"),
        font_face("Sora", 700, "Sora-Bold.ttf"),
        ".fntSup {font-weight:900;font-size:174.79px;font-family:'Cera Pro'}",
        ".ph-fill {fill:#E9ECEA} .ph-text {font-family:'Sora';font-weight:400;font-size:120px;fill:#7A847E}",
    ])
    svg = prepare_svg(W / "template.svg", css)
    for img_id, name in [("1", "background"), ("4", "headline"), ("5", "live-badge")]:
        svg = svg.replace(rf'xlink:href="45_Images\45_ImgID{img_id}.png"',
                          f'xlink:href="{data_uri(W / "images" / (name + ".png"), "image/png")}"')

    def slot(key, label):
        return (f'<g id="{key}Slot"><circle class="ph-fill ui-only" id="{key}Ph" cx="0" cy="0" r="0"/>'
                f'<text class="ph-text ui-only" id="{key}PhText" text-anchor="middle">{label}</text>'
                f'<image id="{key}Img" preserveAspectRatio="none" x="0" y="0" width="0" height="0"/></g>')

    svg = must_sub(r'<g id="_1947619060176">\s*<image [^>]*45_ImgID2\.png"/>\s*</g>', slot("host", "Add host photo"), svg)
    svg = must_sub(r'<g id="_1947619061040">\s*<image [^>]*45_ImgID3\.png"/>\s*</g>', slot("astro", "Add astrologer photo"), svg)

    svg = must_sub(r'<text x="5143.25" y="3511.62"  class="fil10 fnt0">Anju Sharma</text>',
                   '<text id="astroName" x="5143.25" y="3511.62" class="fil10 fnt0" data-orig="Anju Sharma">Anju Sharma</text>', svg)
    svg = must_sub(r'<text x="5435.74" y="3662.01"  class="fil11 fnt1">Astrologer </text>',
                   '<text id="astroRole" x="5435.74" y="3662.01" class="fil11 fnt1" data-orig="Astrologer">Astrologer</text>', svg)
    svg = must_sub(r'<text x="3202.23" y="3508.69"  class="fil10 fnt0">Heeru Verma</text>',
                   '<text id="hostName" x="3202.23" y="3508.69" class="fil10 fnt0" data-orig="Heeru Verma">Heeru Verma</text>', svg)
    svg = must_sub(r'<text x="3679.76" y="3672.92"  class="fil11 fnt1">Host</text>',
                   '<text id="hostRole" x="3679.76" y="3672.92" class="fil11 fnt1" data-orig="Host">Host</text>', svg)

    date_block = '''<g id="dateGroup">
   <text id="dateText" x="559.79" y="3221.9"><tspan id="dDay" class="fil12 fnt2">11</tspan><tspan id="dSuf" class="fil12 fntSup" dy="-174.78">th</tspan><tspan id="dRest" class="fil13 fnt4" dy="174.78"> Nov. 2026</tspan></text>
   <text id="timeText" x="600.04" y="3555.81" class="fil12 fnt5">7:30 PM</text>
   <rect id="istBox" class="fil14" x="1777.61" y="3344.76" width="391.67" height="224.45"/>
   <text id="istText" x="1827.37" y="3522.17" class="fil12 fnt6">IST</text>
  </g>
  '''
    svg = must_sub(r'<g id="_1947619064016">.*?(?=<g style="clip-path:url\(#id3\)">)', date_block, svg, flags=re.S)
    hits = ('<circle id="hostHit" class="hit ui-only" cx="3823.43" cy="2513.39" r="767.89"/>'
            '<circle id="astroHit" class="hit ui-only" cx="5749.05" cy="2513.39" r="767.89"/>')
    svg = must_sub(r"</svg>\s*$", hits + "\n</svg>\n", svg)
    return page("wednesday.html", svg, "wednesday", "")


# ---------------------------------------------------------------- Sunday
# Card geometry measured from the background image (mirrored by the template's transform).
SUNDAY_CARDS = {
    "left":  {"x": 702.8,  "w": 5756.3},   # blue card
    "right": {"x": 6773.1, "w": 5771.3},   # orange card
}
CARD_TOP, CARD_BOTTOM, CARD_R = 1898.8, 12469.6, 463
FADE_FROM, FADE_TO = 9250, 10420          # photo fades out into the name band


def build_sunday():
    S = A / "sunday"
    css = "\n".join([
        font_face("Montserrat", 500, "Montserrat-Medium.otf"),
        font_face("Montserrat", 700, "Montserrat-Bold.otf"),
        font_face("Montserrat", 900, "Montserrat-Black.otf"),
        font_face("Anek Devanagari", 600, "AnekDevanagari-SemiBold.ttf"),
        font_face("Anek Devanagari", 700, "AnekDevanagari-Bold.ttf"),
        font_face("Bebas Neue", 700, "BebasNeue Bold.otf"),
        ".ph-text {font-family:'Montserrat';font-weight:500;font-size:420px;fill:#fff;opacity:.85}",
        # Hindi topic styles, taken from the Hindi version of the design (webinar.svg)
        ".hiT1 {font-family:'Anek Devanagari';font-weight:700;font-size:1944.43px}",
        ".hiT2 {font-family:'Anek Devanagari';font-weight:600;font-size:835.99px}",
        ".pillText {font-family:'Bebas Neue';font-weight:700;font-size:740.8px}",
    ])
    svg = prepare_svg(S / "template.svg", css)
    # Corel used separate family names per weight; map them onto one embedded family,
    # with Anek Devanagari as fallback so Hindi typed into any field still renders.
    svg = svg.replace("font-family:'Montserrat Medium'", "font-family:'Montserrat'")
    svg = svg.replace("font-family:'Montserrat Black'", "font-family:'Montserrat'")
    svg = svg.replace("font-family:'Montserrat'}", "font-family:'Montserrat','Anek Devanagari'}")
    # "LIVE WEBINAR" was exported as letter outlines; replace with live text "LIVE SESSION"
    # (position from the Hindi design, shifted by the small pill offset between the two files).
    svg = must_sub(r'<g>\s*<polygon class="fil17".*?</g>',
                   '<text id="pillText" x="16849.43" y="8909.66" class="fil18 pillText">LIVE SESSION</text>', svg, flags=re.S)
    svg = svg.replace(r'xlink:href="Sunday-Live_Images\Sunday-Live_ImgID1.png"',
                      f'xlink:href="{data_uri(S / "images" / "background.png", "image/png")}"')
    # Ganesh ji line-art watermark removed on request
    svg = must_sub(r'\s*<image x="13164.14" y="1451.55"[^>]*ImgID2\.png"/>', "", svg)

    defs = [f'<linearGradient id="fadeGrad" gradientUnits="userSpaceOnUse" x1="0" y1="{FADE_FROM}" x2="0" y2="{FADE_TO}">'
            '<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>']
    for key, c in SUNDAY_CARDS.items():
        defs.append(f'<clipPath id="{key}Clip"><rect x="{c["x"]}" y="{CARD_TOP}" width="{c["w"]}" '
                    f'height="{CARD_BOTTOM - CARD_TOP:.1f}" rx="{CARD_R}"/></clipPath>')
        defs.append(f'<mask id="{key}Mask" maskUnits="userSpaceOnUse" x="0" y="0" width="24999" height="14070">'
                    f'<rect x="0" y="0" width="24999" height="14070" fill="url(#fadeGrad)"/></mask>')
    svg = svg.replace("</defs>", "".join(defs) + "\n </defs>", 1)

    def slot(key, label):
        c = SUNDAY_CARDS[key]
        cx = c["x"] + c["w"] / 2
        return (f'<g id="{key}Slot" clip-path="url(#{key}Clip)">'
                f'<text class="ph-text ui-only" id="{key}PhText" x="{cx:.1f}" y="6000" text-anchor="middle">{label}</text>'
                f'<image id="{key}Img" mask="url(#{key}Mask)" preserveAspectRatio="none" x="0" y="0" width="0" height="0"/></g>')

    svg = must_sub(r'<image x="737.04" y="1969.02"[^>]*ImgID3\.png"/>', slot("left", "+ Add photo"), svg)
    svg = must_sub(r'<image x="6518.33" y="2080.41"[^>]*ImgID4\.png"/>', slot("right", "+ Add photo"), svg)

    # topic
    svg = must_sub(r'<text x="14548.71" y="4893.78"  class="fil9 fnt0">ANANT </text>',
                   '<text id="topic1" x="14548.71" y="4893.78" class="fil9 fnt0">ANANT </text>', svg)
    svg = must_sub(r'<text x="14051.87" y="6096.51"  class="fil10 fnt1">CHATURDASHI</text>',
                   '<text id="topic2" x="14051.87" y="6096.51" class="fil10 fnt1">CHATURDASHI</text>', svg)
    svg = must_sub(r'<text x="14560.77" y="7149.74"  class="fil10 fnt2">Significance &amp; Remedies</text>',
                   '<text id="topic3" x="14560.77" y="7149.74" class="fil10 fnt2">Significance &amp; Remedies</text>', svg)
    # date + time: one flowing line so it can be re-centred
    svg = must_sub(r'<text x="15382.11" y="10640.67"  class="fil11 fnt3">20 SEP. </text>\s*'
                   r'<text x="18806.78" y="10640.67"  class="fil10 fnt4">SUNDAY, </text>',
                   '<text id="dateLine" x="15382.11" y="10640.67"><tspan id="sDate" class="fil11 fnt3">20 SEP. </tspan>'
                   '<tspan id="sDay" class="fil10 fnt4">SUNDAY,</tspan></text>', svg)
    svg = must_sub(r'<text x="16561.45" y="11790"  class="fil10 fnt4">3:00 PM IST</text>',
                   '<text id="timeLine" x="16561.45" y="11790" class="fil10 fnt4">3:00 PM IST</text>', svg)
    # names + titles
    svg = must_sub(r'<text x="7358.75" y="10970.6"  class="fil18 fnt5">Shweta Gupta</text>\s*'
                   r'<text x="7827.36" y="11570.22"  class="fil18 fnt6">Mentor &amp; Panel </text>\s*'
                   r'<text x="8406.81" y="12078.98"  class="fil18 fnt6">Astrologer</text>',
                   '<text id="rightName" x="7358.75" y="10970.6" class="fil18 fnt5">Shweta Gupta</text>'
                   '<text id="rightT1" x="7827.36" y="11570.22" class="fil18 fnt6">Mentor &amp; Panel </text>'
                   '<text id="rightT2" x="8406.81" y="12078.98" class="fil18 fnt6">Astrologer</text>', svg)
    svg = must_sub(r'<text x="1030.01" y="10976.72"  class="fil18 fnt7">Revathi Shridhar</text>\s*'
                   r'<text x="1790.56" y="11570.22"  class="fil18 fnt8">Mentor &amp; Panel </text>\s*'
                   r'<text x="2370.01" y="12078.98"  class="fil18 fnt8">Astrologer</text>',
                   '<text id="leftName" x="1030.01" y="10976.72" class="fil18 fnt7">Revathi Shridhar</text>'
                   '<text id="leftT1" x="1790.56" y="11570.22" class="fil18 fnt8">Mentor &amp; Panel </text>'
                   '<text id="leftT2" x="2370.01" y="12078.98" class="fil18 fnt8">Astrologer</text>', svg)

    hits = "".join(
        f'<rect id="{k}Hit" class="hit ui-only" x="{c["x"]}" y="{CARD_TOP}" width="{c["w"]}" height="{FADE_TO - CARD_TOP:.1f}"/>'
        for k, c in SUNDAY_CARDS.items())
    svg = must_sub(r"</svg>\s*$", hits + "\n</svg>\n", svg)
    return page("sunday.html", svg, "sunday", "../")


def write(rel, html):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {rel}  ({out.stat().st_size / 1e6:.1f} MB)")


write("index.html", build_wednesday())
write("sunday/index.html", build_sunday())
