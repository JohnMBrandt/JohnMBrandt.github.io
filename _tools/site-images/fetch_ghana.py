import sys
sys.path.insert(0, sys.argv[1]); data = sys.argv[2]
import numpy as np
from common import pc_item, pc_sign, read_to_grid, ttc_on_grid
from rasterio.enums import Resampling
item = pc_item("sentinel-2-l2a", "S2B_MSIL2A_20200127T102209_R065_T30NXP_20201002T125606")
crs = "EPSG:32630"
b = (614300.0, 848000.0, 629300.0, 858000.0)  # 15 x 10 km, room to choose the final window
res = 10.0
vis, _ = read_to_grid(pc_sign("sentinel-2-l2a", item["assets"]["visual"]["href"]), crs, b, res, resampling=Resampling.nearest)
ttc = ttc_on_grid(crs, b, res, 14, f"{data}/ttc")
print("vis", vis.shape, "ttc", ttc.shape, ttc.mean().round(3), "acq", item["properties"]["datetime"])
np.savez_compressed(f"{data}/ghana_full.npz", vis=vis, ttc=ttc, bounds=np.array(b), res=res)
