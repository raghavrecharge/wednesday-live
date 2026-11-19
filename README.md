# Asttrolok Live – Creative Generators

One-page tools for the weekly live creatives. Upload photos, type names (and the topic), pick the date, download PNG/JPG.

| Page | Live link | What changes each week |
|---|---|---|
| **Wednesday Live** (Har Budhwar Ab Hoga Uttar Waar) | `/` | host + astrologer photo & name, date, time |
| **Sunday Live** (Live Session) | `/sunday/` | topic in English (3 lines) or Hindi (2 lines), two astrologers' photos, names & titles, date, time |

## Use
Open the GitHub Pages link in Chrome or Edge (or open `index.html` / `sunday/index.html` locally).

- Drag a photo in the preview to reposition it; scroll or use the slider to zoom.
- Dates default to the next Wednesday / Sunday; suffixes, month and weekday are filled in automatically.
- Long names and topics shrink automatically to fit.
- Sunday: cut-out PNG photos look best; plain photos are clipped to the card and faded into the name band.
- Sunday topic: switch English / हिंदी. Hindi uses Anek Devanagari, as in the Hindi design.
- Sizes: 1920×1080, 3840×2160, 1280×720.

## Edit the templates
- UI and logic: `src/wednesday.html`, `src/sunday.html`, shared styles in `src/common.css`
- Artwork: `assets/<creative>/template.svg` (CorelDRAW SVG export) plus `assets/<creative>/images/`
- Fonts: `assets/fonts/`

After changing anything, rebuild the pages:

```
python build.py
```
