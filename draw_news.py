#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (entry.png).

Pure Pillow drawing: flat vector-style panels plus DejaVu text, all drawn
from scratch in this file. No photos, no network, no third-party artwork.
Deterministic: same input, same bytes.
Run:  python3 draw_news.py   (writes entry.png next to this file)
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24  # outer margin
PAPER = (247, 242, 232)
INK = (24, 24, 24)
NAVY = (20, 32, 60)
GOLD = (212, 160, 60)
RED = (178, 34, 34)
TEAL = (13, 92, 92)
RULE = (120, 110, 95)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines top-left anchored; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def panel_frame(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=(90, 82, 70), width=1)


def kicker_headline(draw, x, y, w, kick, head, fnt_head, deck=None,
                    fnt_deck=None, deck_leading=None):
    """Kicker + headline (+ optional deck) inside a panel; returns next y."""
    draw.text((x, y), kick, font=F(SANS_B, 20), fill=RED)
    y += 30
    lines = wrap(draw, head, fnt_head, w)
    y = block(draw, x, y, lines, fnt_head, INK)
    if deck:
        y += 4
        dlines = wrap(draw, deck, fnt_deck, w)
        y = block(draw, x, y, dlines, fnt_deck, (60, 58, 52),
                  leading=deck_leading)
    return y


# ---------------------------------------------------------------- panels
def ipo_panel(draw, x, y, w, h):
    """Rising market chart: navy board, gold line, green bars, $ tag."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for gy in range(y + 24, y + h - 20, 26):
        draw.line([x + 10, gy, x + w - 10, gy], fill=(52, 66, 100), width=1)
    # bars
    bars = [18, 26, 22, 34, 30, 44, 40, 56, 52, 68, 64, 84]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 20 + i * bw
        draw.rectangle([bx, y + h - 18 - bh, bx + bw - 6, y + h - 18],
                       fill=(28, 120, 90))
    # rising line with arrowhead (ends below the price tag)
    pts = []
    n = 9
    for i in range(n):
        px = x + 24 + i * (w - 134) / (n - 1)
        py = y + h - 46 - (i / (n - 1)) ** 1.6 * (h - 132) \
            - 8 * math.sin(i * 1.7)
        pts.append((px, py))
    draw.line(pts, fill=GOLD, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex + 2, ey - 16), (ex + 18, ey + 2), (ex - 12, ey + 6)],
                 fill=GOLD)
    # price tag
    tag = "$81.3bn"
    tf = F(SANS_B, 44)
    tw = draw.textlength(tag, font=tf)
    draw.rectangle([x + w - tw - 34, y + 14, x + w - 14, y + 66],
                   fill=(255, 255, 255))
    draw.text((x + w - tw - 24, y + 18), tag, font=tf, fill=(16, 28, 52))
    draw.text((x + 20, y + 16), "ANT  ·  NASDAQ", font=F(SANS_B, 20),
              fill=(150, 190, 220))


def gta_panel(draw, x, y, w, h):
    """Vice City at dusk: orange-purple sky, sun, skyline, palms, big VI."""
    for i in range(h):
        t = i / h
        r = int(255 - 60 * t)
        g = int(120 - 20 * t)
        b = int(150 + 60 * t)
        draw.line([x, y + i, x + w, y + i], fill=(r, g, b))
    draw.ellipse([x + 16, y + 10, x + 68, y + 62],
                 fill=(255, 214, 120))
    # skyline, back row then front row
    import random
    rnd = random.Random(19)
    for row, col, base in ((0.42, (58, 32, 74), 0.62),
                           (0.30, (34, 20, 52), 0.52)):
        bx = x + 4
        while bx < x + w - 26:
            bw2 = rnd.randint(26, 46)
            bh2 = int(h * row * rnd.uniform(0.55, 1.0))
            top = y + h - bh2
            draw.rectangle([bx, top, bx + bw2, y + h], fill=col)
            for wy in range(top + 8, y + h - 6, 14):
                for wx in range(bx + 5, bx + bw2 - 4, 11):
                    if rnd.random() < 0.5:
                        draw.rectangle([wx, wy, wx + 4, wy + 6],
                                       fill=(255, 214, 120))
            bx += bw2 + 3
    # palm silhouettes
    for px, py, s in ((x + 52, y + h - 6, 26), (x + w - 66, y + h - 6, 30)):
        draw.line([px, py, px, py - s], fill=(20, 12, 30), width=4)
        for a in (-70, -35, 0, 35, 70):
            ang = math.radians(a - 90)
            ex = px + s * 0.9 * math.cos(ang)
            ey = py - s + s * 0.55 * math.sin(ang)
            draw.line([px, py - s, ex, ey], fill=(20, 12, 30), width=3)
    # neon signs on the skyline
    for sx, sy, sw in ((x + 120, y + h - 58, 34), (x + 260, y + h - 66, 28),
                       (x + w - 150, y + h - 52, 40)):
        draw.rectangle([sx, sy, sx + sw, sy + 12], fill=(255, 92, 168))


def capitol_panel(draw, x, y, w, h):
    """US Capitol dome on a pale sky, with a small flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(198, 220, 238))
    # dome
    cx = x + w // 2
    draw.rectangle([cx - 118, y + h - 52, cx + 118, y + h], fill=(245, 245, 240))
    draw.rectangle([cx - 118, y + h - 62, cx + 118, y + h - 52],
                   fill=(225, 225, 215))
    draw.polygon([(cx - 84, y + h - 62), (cx + 84, y + h - 62),
                  (cx + 46, y + 46), (cx - 46, y + 46)], fill=(250, 250, 245))
    draw.ellipse([cx - 46, y + 30, cx + 46, y + 78], fill=(250, 250, 245))
    draw.rectangle([cx - 3, y + 14, cx + 3, y + 32], fill=(120, 120, 115))
    draw.ellipse([cx - 9, y + 8, cx + 9, y + 22], fill=(200, 170, 60))
    for i in range(9):
        colx = cx - 100 + i * 25
        draw.rectangle([colx, y + h - 52, colx + 12, y + h - 8],
                       fill=(210, 210, 200))
    # flag
    fx, fy = x + 30, y + 18
    draw.rectangle([fx, fy, fx + 3, fy + 52], fill=(80, 80, 80))
    draw.rectangle([fx + 3, fy, fx + 63, fy + 34], fill=(178, 34, 52))
    for sy in range(fy + 4, fy + 32, 8):
        draw.rectangle([fx + 3, sy, fx + 63, sy + 4], fill=(255, 255, 255))
    draw.rectangle([fx + 3, fy, fx + 27, fy + 18], fill=(30, 50, 110))


def gaza_panel(draw, x, y, w, h):
    """Central Gaza: sand land, blue sea at left, yellow line, red arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    draw.rectangle([x, y, x + 74, y + h], fill=(70, 130, 180))
    for wy in (y + h - 40, y + h - 18):
        for wx in range(x + 6, x + 66, 26):
            draw.arc([wx, wy, wx + 22, wy + 12], 180, 360,
                     fill=(255, 255, 255), width=2)
    # built-up blocks (Nuseirat / Bureij), top band only
    for bx, by, bw2, bh2 in ((150, 24, 62, 20), (232, 34, 54, 18),
                             (268, 18, 48, 16), (300, 40, 58, 18)):
        draw.rectangle([x + bx, y + by, x + bx + bw2, y + by + bh2],
                       fill=(188, 164, 120), outline=(150, 128, 92), width=1)
    # the Yellow Line (ceasefire line)
    ly = y + h * 0.62
    for lx in range(x + 84, x + w - 8, 18):
        draw.line([lx, ly, lx + 10, ly], fill=(220, 170, 0), width=4)
    # tanks crossing west, arrow + vehicles
    draw.line([x + w - 40, y + 14, x + 150, ly - 8], fill=RED, width=4)
    draw.polygon([(x + 150, ly - 8), (x + 174, ly - 18), (x + 172, ly + 2)],
                 fill=RED)
    for tx, ty in ((x + w - 116, y + 12), (x + w - 168, y + 28)):
        draw.rectangle([tx, ty, tx + 34, ty + 12], fill=(70, 74, 60))
        draw.rectangle([tx + 8, ty - 7, tx + 22, ty], fill=(70, 74, 60))
        draw.line([tx + 22, ty - 3, tx + 36, ty - 3], fill=(70, 74, 60),
                  width=3)
        draw.rectangle([tx + 2, ty + 12, tx + 32, ty + 15],
                       fill=(50, 52, 44))
    draw.text((x + 92, y + h - 22), "NUSEIRAT", font=F(SANS_B, 16),
              fill=(90, 78, 60))
    draw.text((x + 300, y + h - 22), "YELLOW LINE", font=F(SANS_B, 16),
              fill=(150, 110, 0))


def gulf_panel(draw, x, y, w, h):
    """The Gulf at night: dark sea, two coasts, missile arcs, bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 34, 58))
    for i in range(14):
        sx = x + 20 + i * 32
        sy = y + 14 + (i * 37) % 30
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # Iran coast (top) and Arab coast (bottom)
    draw.polygon([(x, y + 34), (x + w * 0.55, y + 22), (x + w, y + 44),
                  (x + w, y + 74), (x + w * 0.6, y + 62), (x, y + 66)],
                 fill=(120, 100, 70))
    draw.polygon([(x, y + h), (x + w * 0.4, y + h - 26), (x + w, y + h - 44),
                  (x + w, y + h), (x, y + h)], fill=(96, 84, 62))
    draw.text((x + 16, y + 44), "IRAN", font=F(SANS_B, 16),
              fill=(210, 195, 160))
    draw.text((x + w - 116, y + h - 26), "GULF STATES", font=F(SANS_B, 16),
              fill=(200, 188, 155))
    # missile arcs, both ways
    for (x0, y0, x1, y1, col) in ((x + 120, y + 52, x + 330, y + h - 58, (255, 120, 40)),
                                  (x + 360, y + h - 44, x + 150, y + 58, (255, 190, 60))):
        mx, my = (x0 + x1) / 2, min(y0, y1) - 34
        pts = []
        for t in [i / 20 for i in range(21)]:
            px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * x1
            py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * y1
            pts.append((px, py))
        draw.line(pts, fill=col, width=3)
        burst(draw, x1, y1, 22, 10, 10, col)
        burst(draw, x1, y1, 11, 5, 8, (255, 240, 200))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((W // 2, 6), "THE WORLD", font=F(SERIF_B, 66), fill=(255, 255, 255),
           anchor="ma")
    d.text((W // 2, 82), "THURSDAY  ·  19 NOVEMBER 2026",
           font=F(SANS_B, 24), fill=GOLD, anchor="ma")
    # tagline + gold rule
    d.text((W // 2, 116), "The day's world news, in one image",
           font=F(SERIF, 26), fill=(90, 80, 66), anchor="ma")
    d.line([M, 152, W - M, 152], fill=GOLD, width=3)

    # ---- lead story: Anthropic IPO
    ly, lh = 164, 296
    ipo_panel(d, M, ly, 436, lh)
    panel_frame(d, M, ly, 436, lh)
    tx = M + 436 + 24
    tw = W - M - tx
    y = ly + 10
    d.text((tx, y), "BUSINESS  ·  MARKETS", font=F(SANS_B, 21), fill=RED)
    y += 32
    y = block(d, tx, y, wrap(d, "Anthropic prices the biggest IPO ever at $81.3 billion",
                             F(SERIF_B, 40), tw), F(SERIF_B, 40), INK,
              leading=48)
    y += 8
    d.line([tx, y, tx + tw, y], fill=RULE, width=1)
    y += 12
    block(d, tx, y, wrap(
        d, "At $83 a share, the AI lab is worth about $1.5 trillion. "
           "Shares start trading today on Nasdaq as ANT.",
        F(SANS, 22), tw), F(SANS, 22), (60, 58, 52), leading=28)

    # ---- row 2: GTA VI | Jeffries
    ry, rh = 476, 216
    for px, fn, kick, head in (
            (M, gta_panel, "CULTURE  ·  GAMING",
             "GTA VI rolls out worldwide after a 13-year wait"),
            (M + 492, capitol_panel, "US POLITICS",
             "Jeffries nominated for Speaker in historic first")):
        fn(d, px, ry, 484, 108)
        panel_frame(d, px, ry, 484, rh)
        d.rectangle([px, ry + 108, px + 484, ry + rh], fill=PAPER)
        kicker_headline(d, px + 14, ry + 116, 484 - 28, kick, head,
                        F(SERIF_B, 28))

    # ---- row 3: Gaza | Gulf
    ry, rh = 708, 240
    for px, fn, kick, head, deck in (
            (M, gaza_panel, "MIDDLE EAST",
             "Israel launches first Gaza ground raid since truce",
             "Tanks cross the Yellow Line into central Gaza; Hamas calls "
             "it a breach of the ceasefire."),
            (M + 492, gulf_panel, "GULF CRISIS",
             "US and Iran trade fire again as Gulf war widens",
             "Tehran hits a US base in Kuwait and strikes Bahrain again "
             "after US jets hit Qeshm Island.")):
        fn(d, px, ry, 484, 88)
        panel_frame(d, px, ry, 484, rh)
        d.rectangle([px, ry + 88, px + 484, ry + rh], fill=PAPER)
        kicker_headline(d, px + 14, ry + 96, 484 - 28, kick, head,
                        F(SERIF_B, 28), deck=deck, fnt_deck=F(SANS, 18),
                        deck_leading=22)

    # ---- also today
    ay = 952
    d.line([M, ay, W - M, ay], fill=INK, width=2)
    d.text((W // 2, ay + 8), "ALSO TODAY", font=F(SANS_B, 20), fill=RED,
           anchor="ma")
    block(d, M, ay + 36, wrap(
        d, "Akvan nears India  ·  Voyager 1: one light-day out  ·  "
           "EU €45bn for Ukraine  ·  Pew: Islam largest by 2035",
        F(SANS, 18), W - 2 * M), F(SANS, 18), INK, leading=22)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
