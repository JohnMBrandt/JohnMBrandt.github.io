import sys
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
import numpy as np
from rasterio.enums import Resampling
from common import pc_item, pc_sign, read_to_grid, chm_mosaic
it = pc_item("naip", "ny_m_4407447_se_18_060_20221005")
crs = "EPSG:26918"
bounds = (565000.0, 4904800.0, 568600.0, 4907000.0)
res = 0.8
rgb, t = read_to_grid(pc_sign("naip", it["assets"]["image"]["href"]), crs, bounds, res, resampling=Resampling.average, bands=[1, 2, 3])
chm, keys = chm_mosaic(crs, bounds, res)
print("rgb", rgb.shape, rgb.dtype, "chm", chm.shape, "tiles", keys, "chm p50/95/99", np.percentile(chm, [50, 95, 99]))
np.savez_compressed(f"{out}/adk_full.npz", rgb=rgb, chm=chm, bounds=np.array(bounds), res=res)
