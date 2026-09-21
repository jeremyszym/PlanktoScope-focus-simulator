# PlanktoScope · Focus Depth Comparator

A static site to host on GitHub Pages. Features a series picker, a
depth-of-field slider, stable zoom/pan, and an automatic micrometer scale
bar. The objective (magnification) is detected automatically from the
folder names — the viewer never needs to select it manually.

## 1. Add your images

Create one folder per series inside `series/`, following EXACTLY this
naming format:

```
series/<series-name>__<objective>/
```

- `<series-name>`: whatever you want (dashes or underscores), e.g.
  `copepod-01`, `diatom-frustule`.
- `<objective>`: must be one of `highmag`, `medmag`, `lowmag`
  (corresponding to High Mag. = 0.53 µm/px, Med Mag. = 0.75 µm/px,
  Low Mag. = 1.34 µm/px).

Inside each folder, name every photo with its focus distance in µm at
the start of the filename:

```
series/copepod-01__medmag/000um.jpg
series/copepod-01__medmag/025um.jpg
series/copepod-01__medmag/050um.jpg
series/copepod-01__medmag/075um.jpg
series/copepod-01__medmag/100um.jpg
series/copepod-01__medmag/125um.jpg
series/copepod-01__medmag/150um.jpg
```

You can add as many series as you like, each with its own objective —
every series keeps its own calibration.

## 2. Generate manifest.json

The site is 100% static: it cannot "scan" a folder by itself. After
adding or changing any photos, run this from the project root:

```bash
python3 generate_manifest.py
```

The script prints what it found (or any naming errors) and regenerates
`manifest.json`, which the site loads on startup.

## 3. Test locally (optional but recommended)

Opening `index.html` directly in your browser (double-click) won't
work: loading `manifest.json` is blocked by the browser over `file://`.
Serve the folder with a small local server instead:

```bash
python3 -m http.server 8000
```

then open `http://localhost:8000` in your browser.

## 4. Deploy with GitHub Pages

1. Create a GitHub repository (public, so Pages is free), for example
   `planktoscope-focus`.
2. From this folder, initialize and push:

   ```bash
   git init
   git add .
   git commit -m "Focus comparator site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/planktoscope-focus.git
   git push -u origin main
   ```

3. On GitHub, go to **Settings → Pages** for the repository.
4. Under "Build and deployment", choose **Deploy from a branch**,
   branch `main`, folder `/ (root)`. Click **Save**.
5. After 1–2 minutes, the site is live at:

   ```
   https://<your-username>.github.io/planktoscope-focus/
   ```

   That's the address you can share.

## 5. Add photos later

Every time you have a new series or new photos:

```bash
# 1. copy the new images into series/...__medmag/ (or highmag/lowmag)
python3 generate_manifest.py
git add .
git commit -m "Add series X"
git push
```

The live site updates automatically (GitHub Pages redeploys on every
push) — nothing else to reconfigure.

## Project structure

```
.
├── index.html            ← the app (don't edit unless changing the style)
├── generate_manifest.py  ← rerun after every photo change
├── manifest.json          ← auto-generated, don't edit by hand
├── README.md
└── series/
    ├── copepod-01__medmag/
    │   ├── 000um.jpg
    │   ├── 025um.jpg
    │   └── ...
    └── diatom-03__highmag/
        ├── 000um.jpg
        └── ...
```

## Changing the objective calibration

If an objective changes or you add a new one, edit the `MAG_CODES`
dictionary at the top of `generate_manifest.py`, and the `MAG_LABELS`
object at the top of the `<script>` in `index.html` (for display).
