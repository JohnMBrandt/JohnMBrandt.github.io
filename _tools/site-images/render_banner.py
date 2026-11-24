"""Home page banner: NAIP aerial photo on the left blending into shaded CHMv2 canopy height on the right."""
import sys
sys.path.insert(0, sys.argv[1]); data = sys.argv[2]; out = sys.argv[3]
x0_m, y0_m, w_m = float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
tag = sys.argv[7] if len(sys.argv) > 7 else "a"
cmap_name = sys.argv[8] if len(sys.argv) > 8 else "canopy"
import numpy as np
from viz import height_rgb, photo_rgb, stretch_params, smoothstep, to_image, CMAPS
from common import edge_pixels, blur_lines, detect_lines

d = np.load(f"{data}/adk_full.npz")
res = float(d["res"])
W_OUT, H_OUT = 2400, 880
h_m = w_m * H_OUT / W_OUT
r0, c0 = int(y0_m / res), int(x0_m / res)
r1, c1 = r0 + int(h_m / res), c0 + int(w_m / res)
rgb = d["rgb"][:, r0:r1, c0:c1]
chm = d["chm"][r0:r1, c0:c1]
full = d["chm"]
cols, rows = edge_pixels(["0302321122", "0302321123"], "EPSG:26918", tuple(d["bounds"]), res, full.shape)
cols = [c - c0 for c in cols if c0 < c < c1]; rows = [r - r0 for r in rows if r0 < r < r1]
cols = sorted(set(cols + detect_lines(chm, 1))); rows = sorted(set(rows + detect_lines(chm, 0)))
chm = blur_lines(chm, cols, rows, half=6)
print("tile edges blurred at cols", cols, "rows", rows)
print("crop", rgb.shape, "chm p50/p99", np.percentile(chm, [50, 99]))

photo = photo_rgb(rgb, stretch_params(d['rgb']))
height = height_rgb(chm, res, vmax=26, cmap=CMAPS[cmap_name])
H, W = chm.shape
yy, xx = np.mgrid[0:H, 0:W]
# Transition band runs from ~42% to ~72% of the width, tilted so it leans right toward the top.
pos = (xx / W) - 0.10 * (1 - yy / H)
mask = smoothstep((pos - 0.36) / 0.30)[..., None]
blend = photo * (1 - mask) + height * mask
to_image(blend, (W_OUT, H_OUT)).save(f"{out}/banner_{tag}.jpg", quality=86, optimize=True, progressive=True)
to_image(height, (W_OUT // 2, H_OUT // 2)).save(f"{out}/banner_{tag}_heightonly.jpg", quality=85)
print("saved", f"{out}/banner_{tag}.jpg")
