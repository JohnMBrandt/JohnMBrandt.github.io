import sys
sys.path.insert(0, sys.argv[1]); data = sys.argv[2]; src_path = sys.argv[3]
import numpy as np, rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rasterio.transform import from_origin
d = dict(np.load(f"{data}/ghana_full.npz"))
left, bottom, right, top = d["bounds"]; res = float(d["res"])
W, H = int((right - left) / res), int((top - bottom) / res)
with rasterio.open(src_path) as src:
    print("src", src.crs, src.res, src.nodata, src.dtypes)
    with WarpedVRT(src, crs="EPSG:32630", transform=from_origin(left, top, res, res), width=W, height=H,
                   resampling=Resampling.nearest, nodata=255) as v:
        tc = v.read(1)
vals, cnt = np.unique(tc, return_counts=True)
print("window", tc.shape, "unique", len(vals), "min/max", vals.min(), vals.max(), "nodata frac", (tc == 255).mean().round(4))
print("top values", sorted(zip(cnt.tolist(), vals.tolist()), reverse=True)[:12])
print("pctiles of valid", np.percentile(tc[tc != 255], [10, 25, 50, 75, 90]))
print("agree with GFW >=40 tiles:", ((tc >= 40) == (d["ttc"] > 0))[tc != 255].mean().round(3))
d["tc"] = tc
np.savez_compressed(f"{data}/ghana_full.npz", **d)
