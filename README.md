# Monday 23 November 2026 — The World in One Page

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/keep0626/makefun-news-image-20261123/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/keep0626/makefun-news-image-20261123/reward.svg)](https://make.fun/c/news-image-20261123)

One image summing up the world news of **Monday 23 November 2026** — 32 stories
across 6 regions, drawn as a newspaper front page: the date as masthead, a
region bar, a numbers strip, three lead stories with hand-drawn pictures, six
picture cards, a world map with numbered pins, one-line briefs, and a DATE
CHECK box naming what was deliberately left out as other days' news.

## Files

- `entry.png` — the submitted image (1024×1024, PNG)
- `render.py` — draws `entry.png` from `stories.json` (Pillow)
- `stories.json` — all 32 stories: headlines, decks, briefs, sources
- `SOURCES.md` — per-story source and date verification
- `main.py` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`

## Reproduce

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library, so both grader runs write
byte-identical output.
