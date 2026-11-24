"""Tropical tree cover card: Sentinel-2 (upper left) vs the 10 m tree cover map (lower right), diagonal split."""
import sys
sys.path.insert(0, sys.argv[1]); data = sys.argv[2]; out = sys.argv[3]
x0_km, y0_km = float(sys.argv[4]), float(sys.argv[5])
import numpy as np
from PIL import Image, ImageDraw
from viz import HEIGHT_CMAP

d = np.load(f"{data}/ghana_full.npz")
res = float(d["res"])
W_OUT, H_OUT = 1200, 800
c0, r0 = int(x0_km * 1000 / res), int(y0_km * 1000 / res)
c1, r1 = c0 + 600, r0 + 400  # 6 x 4 km at 10 m, shown at exactly 2x
vis = d["vis"][:, r0:r1, c0:c1].transpose(1, 2, 0).astype(np.float32)
tc = d["tc"][r0:r1, c0:c1].astype(np.float32)  # percent tree cover (2020), in 10% steps
print("window", vis.shape, "mean tree cover", tc.mean().round(1))

ref = d["vis"].transpose(1, 2, 0).astype(np.float32)
lo, hi = np.percentile(ref, [0.5, 99.7])
rgb = np.clip((vis - lo) / (hi - lo), 0, 1) ** 0.9
lum = rgb.mean(axis=2, keepdims=True)
rgb = np.clip(lum + (rgb - lum) * 1.15, 0, 1)

# Map side: the tree cover style from sentinel-tree-cover/references/style.qml (discrete classes).
# Cover at or below 36% is transparent in that style; here it is drawn as the ramp's lightest colour.
classes = [(36, "#f7fcf5"), (52, "#a1d99b"), (68, "#74c476"), (84, "#31a354"), (1e9, "#006d2c")]
def hex_rgb(h): return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
mp = np.zeros(tc.shape + (3,), dtype=np.float32)
lower = -1
for upper, colour in classes:
    mp[(tc > lower) & (tc <= upper)] = hex_rgb(colour)
    lower = upper

photo = Image.fromarray((rgb * 255).astype(np.uint8)).resize((W_OUT, H_OUT), Image.LANCZOS)
mapim = Image.fromarray((mp * 255).astype(np.uint8)).resize((W_OUT, H_OUT), Image.NEAREST)
mask = Image.new("L", (W_OUT, H_OUT), 0)
ImageDraw.Draw(mask).polygon([(W_OUT, 0), (W_OUT, H_OUT), (0, H_OUT)], fill=255)
card = Image.composite(mapim, photo, mask)
line = Image.new("RGBA", (W_OUT, H_OUT), (0, 0, 0, 0))
ImageDraw.Draw(line).line([(W_OUT, 0), (0, H_OUT)], fill=(255, 255, 255, 170), width=3)
card = Image.alpha_composite(card.convert("RGBA"), line).convert("RGB")
card.save(f"{out}/card_tree_cover.jpg", quality=84, optimize=True, progressive=True)

gap = 12
fig = Image.new("RGB", (W_OUT * 2 + gap, H_OUT), "white")
fig.paste(photo, (0, 0)); fig.paste(mapim, (W_OUT + gap, 0))
fig.resize((1600, int(1600 * H_OUT / (W_OUT * 2 + gap))), Image.LANCZOS).save(f"{out}/fig_tree_cover_pair.jpg", quality=84, optimize=True, progressive=True)
print("saved")
