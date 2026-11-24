"""Canopy height card: one place split diagonally, aerial photo (upper left) and CHMv2 height (lower right).
Also writes a wider side-by-side figure for the project page."""
import sys
sys.path.insert(0, sys.argv[1]); data = sys.argv[2]; out = sys.argv[3]
x0_m, y0_m, w_m = float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
import numpy as np
from PIL import Image, ImageDraw
from viz import height_rgb, photo_rgb, stretch_params, to_image
from common import edge_pixels, blur_lines, detect_lines

d = np.load(f"{data}/adk_full.npz")
res = float(d["res"])
W_OUT, H_OUT = 1200, 800
h_m = w_m * H_OUT / W_OUT
r0, c0 = int(y0_m / res), int(x0_m / res)
r1, c1 = r0 + int(round(h_m / res)), c0 + int(round(w_m / res))
rgb = d["rgb"][:, r0:r1, c0:c1]
chm = d["chm"][r0:r1, c0:c1]
cols, rows = edge_pixels(["0302321122", "0302321123"], "EPSG:26918", tuple(d["bounds"]), res, d["chm"].shape)
cols = [c - c0 for c in cols if c0 < c < c1] + detect_lines(chm, 1)
rows = [r - r0 for r in rows if r0 < r < r1] + detect_lines(chm, 0)
chm = blur_lines(chm, sorted(set(cols)), sorted(set(rows)), half=6)
print("crop", chm.shape, "lines", cols, rows, "chm p50/p99", np.percentile(chm[chm > 2], [50, 99]))

photo = to_image(photo_rgb(rgb, stretch_params(d['rgb'])), (W_OUT, H_OUT))
height = to_image(height_rgb(chm, res, vmax=26), (W_OUT, H_OUT))

# Diagonal split from the top-right corner to the bottom-left corner.
mask = Image.new("L", (W_OUT, H_OUT), 0)
ImageDraw.Draw(mask).polygon([(W_OUT, 0), (W_OUT, H_OUT), (0, H_OUT)], fill=255)
card = Image.composite(height, photo, mask)
line = Image.new("RGBA", (W_OUT, H_OUT), (0, 0, 0, 0))
ImageDraw.Draw(line).line([(W_OUT, 0), (0, H_OUT)], fill=(255, 255, 255, 170), width=3)
card = Image.alpha_composite(card.convert("RGBA"), line).convert("RGB")
card.save(f"{out}/card_canopy_height.jpg", quality=84, optimize=True, progressive=True)

# Project page figure: photo | height, side by side with a small gap.
gap = 12
fig = Image.new("RGB", (W_OUT * 2 + gap, H_OUT), "white")
fig.paste(photo, (0, 0)); fig.paste(height, (W_OUT + gap, 0))
fig = fig.resize((1600, int(1600 * H_OUT / (W_OUT * 2 + gap))), Image.LANCZOS)
fig.save(f"{out}/fig_canopy_height_pair.jpg", quality=84, optimize=True, progressive=True)
print("saved card and figure")
