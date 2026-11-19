# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/yylt00-dev/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/yylt00-dev/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page that sums up the world news of Thursday 19 November 2026 in one image: Anthropic pricing the biggest IPO ever at $81.3 billion, GTA VI rolling out worldwide after a 13-year wait, Hakeem Jeffries nominated for US House Speaker in a historic first, Israel's first Gaza ground operation since the ceasefire, and the US and Iran trading fire again as the Gulf crisis widens — plus a strip of the day's other stories (Cyclone Akvan, Voyager 1's one-light-day milestone, the EU's €45bn Ukraine loan, and Pew's faith projection). Every panel is drawn from scratch with Pillow by `draw_news.py` (flat vector-style art, no photos, no third-party artwork); `main.py` copies the finished page to `/output/entry.png`.

## Run it

```sh
python3 draw_news.py   # regenerate entry.png (needs Pillow, local use only)
python3 main.py        # writes entry.png to /output (MAKEFUN_OUTPUT_DIR to relocate)
```

`main.py` is standard library only, deterministic, and uses no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=e7064d5m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
