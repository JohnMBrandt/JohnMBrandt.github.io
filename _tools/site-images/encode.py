"""Re-encode rendered images into the site's assets/images folder at web-friendly sizes."""
import os
import sys
from PIL import Image

out, assets = sys.argv[1], sys.argv[2]
jobs = {
    "banner_b_canopy.jpg": ("home-banner.jpg", 68),
    "card_canopy_height.jpg": ("card-canopy-height.jpg", 82),
    "card_tree_cover.jpg": ("card-tree-cover.jpg", 76),
    "card_restoration.jpg": ("card-restoration.jpg", 82),
    "fig_canopy_height_pair.jpg": ("fig-canopy-height.jpg", 82),
    "fig_tree_cover_pair.jpg": ("fig-tree-cover.jpg", 76),
    "fig_restoration_pair.jpg": ("fig-restoration.jpg", 82),
}
for src, (dst, q) in jobs.items():
    p = os.path.join(assets, dst)
    Image.open(os.path.join(out, src)).convert("RGB").save(p, "JPEG", quality=q, optimize=True, progressive=True)
    print(f"{dst:26s} {os.path.getsize(p) // 1024} KB")
