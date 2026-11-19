# Wednesday Live – Creative Generator

One-page tool for the weekly **Har Budhwar Ab Hoga Uttar Waar** live creative.
Upload the host and astrologer photos, type their names, pick the date, and download a PNG or JPG.

## Use
Open `index.html` in Chrome or Edge, or use the GitHub Pages link.

- Drag a photo in the preview to reposition it; scroll or use the slider to zoom.
- The date defaults to next Wednesday; the "th/st/nd" suffix and month are filled in automatically.
- Long names shrink automatically to fit.
- Sizes: 1920×1080, 3840×2160, 1280×720.

## Edit the template
- UI and logic: `src/app.html`
- Artwork: `assets/template.svg` (CorelDRAW SVG export) plus `assets/images/`
- Fonts: `assets/fonts/`

After changing anything, rebuild the single-file page:

```
python build.py
```
