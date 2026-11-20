# Draws the front page for Friday 20 November 2026 with Pillow.
# Authoring tool only: the grader runs main.py, which copies entry.png.
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (212, 160, 32)
INK = (24, 24, 28)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 112], fill=NAVY)
d.text((512, 26), "T H E   W O R L D   I N   O N E   D A Y", font=F(SANSB, 19),
       fill=GOLD, anchor="mm")
d.text((512, 68), "Friday 20 November 2026", font=F(SERIF, 52),
       fill=(255, 255, 255), anchor="mm")
d.rectangle([0, 112, W, 117], fill=GOLD)

# ---- lead panel: Kyiv ------------------------------------------------------
lx0, ly0, lx1, ly1 = 16, 128, 1008, 424
lead = Image.open("assets/media-generation-news-lead-kyiv-0-2288a6bf-31df-430a-91e6-1503df2bba50.webp").convert("RGB")
lw, lh = lead.size
target_ratio = (lx1 - lx0) / (ly1 - ly0 - 86)
crop_h = int(lw / target_ratio)
top = max(0, (lh - crop_h) // 2 - 40)
lead = lead.crop((0, top, lw, top + crop_h)).resize((lx1 - lx0, ly1 - ly0 - 86), Image.LANCZOS)
img.paste(lead, (lx0, ly0))
d = ImageDraw.Draw(img)
# headline band
d.rectangle([lx0, ly1 - 86, lx1, ly1], fill=(8, 10, 18))
d.text((lx0 + 18, ly1 - 62), "RUSSIAN BARRAGE KILLS AT LEAST 3 IN KYIV",
       font=F(SANSB, 31), fill=(255, 255, 255), anchor="lm")
d.text((lx0 + 18, ly1 - 26), "Power outages, water disruption in parts of Kyiv · Kyiv Independent / FT",
       font=F(SANS, 19), fill=(200, 205, 220), anchor="lm")
d.text((lx1 - 14, ly0 + 16), "ILLUSTRATION", font=F(SANSB, 13),
       fill=(170, 180, 205), anchor="rm")
d.rectangle([lx0, ly0, lx1, ly1], outline=INK, width=2)

# ---- story grid -------------------------------------------------------------
def fit(text, path, size, max_w):
    while size > 9 and d.textlength(text, font=F(path, size)) > max_w:
        size -= 1
    return F(path, size)


GRID_IMG = Image.open("assets/media-generation-news-grid-scenes-0-65756077-79c9-409f-89c8-de4a64060295.webp").convert("RGB")


def cell(idx):
    gw, gh = GRID_IMG.size
    cw, ch = gw // 3, gh // 3
    cx, cy = (idx % 3) * cw, (idx // 3) * ch
    m = 14
    return GRID_IMG.crop((cx + m, cy + m, cx + cw - m, cy + ch - m))


def panel(px, py, bg, draw_scene, head, sub):
    pw, ph = 320, 158
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255), outline=INK, width=2)
    scene = cell(panel.counter).resize((pw - 4, 86), Image.LANCZOS)
    img.paste(scene, (px + 2, py + 2))
    panel.counter += 1
    d.text((px + 12, py + 102), head, font=fit(head, SANSB, 21, pw - 24), fill=INK, anchor="lm")
    d.text((px + 12, py + 132), sub, font=fit(sub, SANSB, 16, pw - 24), fill=(60, 60, 75), anchor="lm")


def sc_cyclone(px, py):
    cx, cy = px + 90, py + 50
    for r in (38, 28, 18):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 320, fill=(255, 255, 255), width=6)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    for i, wy in enumerate((py + 78, py + 88)):
        pts = [(px + 170 + j * 14, wy + (6 if j % 2 else -6)) for j in range(10)]
        d.line(pts, fill=(255, 255, 255), width=4)


def sc_chart(px, py):
    pts = [(px + 30, py + 30), (px + 90, py + 45), (px + 150, py + 38),
           (px + 210, py + 62), (px + 270, py + 80)]
    d.line(pts, fill=(255, 90, 80), width=6)
    d.polygon([(px + 270, py + 80), (px + 252, py + 66), (px + 254, py + 86)],
              fill=(255, 90, 80))
    for gx in range(px + 30, px + 300, 45):
        d.line([gx, py + 14, gx, py + 88], fill=(120, 60, 60), width=1)


def sc_court(px, py):
    d.polygon([(px + 60, py + 26), (px + 160, py + 8), (px + 260, py + 26)],
              fill=(240, 235, 220))
    for i in range(5):
        cx = px + 78 + i * 42
        d.rectangle([cx, py + 30, cx + 16, py + 80], fill=(240, 235, 220))
    d.rectangle([px + 58, py + 80, px + 262, py + 88], fill=(240, 235, 220))


def sc_flags(px, py):
    cols = [(60, 90, 200), (220, 50, 50), (240, 240, 240)]
    for i, c in enumerate(cols):
        fx = px + 60 + i * 80
        d.line([fx, py + 14, fx, py + 86], fill=(30, 30, 30), width=4)
        d.rectangle([fx, py + 14, fx + 52, py + 44], fill=c)


def sc_rocket(px, py):
    d.polygon([(px + 90, py + 16), (px + 66, py + 66), (px + 114, py + 66)],
              fill=(255, 255, 255))
    d.polygon([(px + 78, py + 66), (px + 102, py + 66), (px + 90, py + 88)],
              fill=(255, 180, 60))
    pts = [(px + 150, py + 78), (px + 200, py + 60), (px + 250, py + 44), (px + 295, py + 22)]
    d.line(pts, fill=(120, 255, 170), width=6)


def sc_oil(px, py):
    d.rectangle([px + 70, py + 22, px + 150, py + 84], fill=(40, 40, 46))
    d.ellipse([px + 70, py + 14, px + 150, py + 30], fill=(70, 70, 80))
    d.text((px + 110, py + 54), "OIL", font=F(SANSB, 20), fill=(255, 210, 80), anchor="mm")
    d.line([px + 190, py + 80, px + 300, py + 24], fill=(255, 80, 80), width=7)
    d.line([px + 190, py + 24, px + 300, py + 80], fill=(255, 80, 80), width=7)


def sc_tower(px, py):
    d.rectangle([px + 130, py + 10, px + 190, py + 88], fill=(235, 225, 200))
    for wy in range(py + 18, py + 82, 12):
        d.rectangle([px + 140, wy, px + 180, wy + 6], fill=(120, 130, 150))
    d.line([px + 40, py + 18, px + 130, py + 44], fill=(255, 170, 60), width=4)
    d.ellipse([px + 124, py + 38, px + 140, py + 54], fill=(255, 120, 40))


def sc_globe(px, py):
    d.ellipse([px + 110, py + 6, px + 210, py + 84], outline=(255, 255, 255), width=4)
    d.line([px + 110, py + 45, px + 210, py + 45], fill=(255, 255, 255), width=3)
    d.arc([px + 135, py + 6, px + 185, py + 84], 90, 270, fill=(255, 255, 255), width=3)
    d.arc([px + 135, py + 6, px + 185, py + 84], 270, 90, fill=(255, 255, 255), width=3)


def sc_pad(px, py):
    d.rounded_rectangle([px + 70, py + 30, px + 250, py + 76], 22, fill=(240, 240, 245))
    d.ellipse([px + 96, py + 44, px + 116, py + 64], fill=(60, 60, 70))
    d.ellipse([px + 204, py + 40, px + 220, py + 56], fill=(255, 90, 90))
    d.ellipse([px + 222, py + 56, px + 238, py + 72], fill=(90, 200, 120))
    d.rectangle([px + 146, py + 48, px + 174, py + 58], fill=(60, 60, 70))


grid = [
    ((0, 128, 140), sc_cyclone, "Cyclone Akvan hits India", "300,000 evacuated · PTI"),
    ((70, 20, 30), sc_chart, "AI sell-off sinks Asia", "KOSPI drops below 5,000 · AP"),
    ((90, 90, 100), sc_court, "ICJ finds Myanmar genocide", "Nov 19 · against the Rohingya"),
    ((30, 40, 90), sc_flags, "Trump · Xi · Putin summit", "Nov 19 · Shenzhen declaration"),
    ((180, 90, 20), sc_rocket, "Anthropic +17% on Nasdaq", "Nov 19 IPO close · Asia slides"),
    ((150, 110, 30), sc_oil, "Tanker incidents at Hormuz", "Brent ~$92.50 despite attacks"),
    ((170, 150, 110), sc_tower, "Missile hits Riyadh tower", "Nov 19 · PIF tower damaged"),
    ((30, 120, 70), sc_globe, "COP31 talks stall", "No deal in sight, talks go on"),
    ((90, 40, 140), sc_pad, "GTA 6 smashes sales records", "Sensor Tower est. $2.36B incl. pre-orders"),
]
panel.counter = 0
gx, gy = 16, 436
for i, (bg, sc, head, sub) in enumerate(grid):
    panel(gx + (i % 3) * 336, gy + (i // 3) * 170, bg, sc, head, sub)

# ---- ticker + footer ---------------------------------------------------------
ty = 436 + 3 * 170 + 4
d.rectangle([16, ty, 1008, ty + 40], fill=NAVY)
tick = "Malawi fuel queues, 20-litre cap · Nov 19: Bukele seeks 3rd term · Japan core CPI 2.2%"
d.text((512, ty + 20), tick, font=fit(tick, SANSB, 19, 960), fill=(255, 255, 255), anchor="mm")
d.text((512, ty + 58),
       "33 sourced stories · AP · AFP · PTI · Kyiv Independent · FT · Xinhua · Al Jazeera",
       font=F(SANS, 15), fill=(90, 90, 100), anchor="mm")

img.save("entry.png", optimize=True)
import os
size = os.path.getsize("entry.png")
if size > 1048576:  # gate cap: fall back to JPEG bytes (name stays entry.png)
    img.save("entry.png", "JPEG", quality=86)
    size = os.path.getsize("entry.png")
print("saved entry.png", img.size, size, "bytes")
