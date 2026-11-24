"""Shared helpers for reading windows from open geospatial data."""
import json
import os
import urllib.request

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from rasterio.transform import from_origin

os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")
os.environ.setdefault("GDAL_HTTP_MERGE_CONSECUTIVE_RANGES", "YES")
os.environ.setdefault("VSI_CACHE", "TRUE")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.TIF,.tiff,.jp2")

PC = "https://planetarycomputer.microsoft.com/api"
CHM_BASE = "https://dataforgood-fb-data.s3.amazonaws.com/forests/v2/global/dinov3_global_chm_v2_ml3/chm/"
_tokens = {}


def get_json(url, data=None):
    headers = {"Content-Type": "application/json"} if data is not None else {}
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def pc_item(collection, item_id):
    return get_json(f"{PC}/stac/v1/collections/{collection}/items/{item_id}")


def pc_search(body):
    return get_json(f"{PC}/stac/v1/search", body)["features"]


def pc_sign(collection, href):
    if collection not in _tokens:
        _tokens[collection] = get_json(f"{PC}/sas/v1/token/{collection}")["token"]
    return f"{href}?{_tokens[collection]}"


def read_to_grid(src_url, crs, bounds, res, resampling=Resampling.bilinear, bands=None, nodata=None):
    """Read a remote raster resampled onto a north-up grid in `crs` covering `bounds` at `res` m."""
    left, bottom, right, top = bounds
    width = int(round((right - left) / res))
    height = int(round((top - bottom) / res))
    transform = from_origin(left, top, res, res)
    with rasterio.open("/vsicurl/" + src_url) as src:
        vrt_kwargs = dict(crs=crs, transform=transform, width=width, height=height, resampling=resampling)
        if nodata is not None:
            vrt_kwargs["src_nodata"] = nodata
            vrt_kwargs["nodata"] = nodata
        with WarpedVRT(src, **vrt_kwargs) as vrt:
            idx = bands or list(range(1, vrt.count + 1))
            arr = vrt.read(idx)
    return arr, transform


def quadkey(lat, lon, z=10):
    import math
    x = (lon + 180) / 360
    s = math.sin(math.radians(lat))
    y = 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    tx, ty = int(x * 2 ** z), int(y * 2 ** z)
    return "".join(str((1 if tx >> (i - 1) & 1 else 0) + (2 if ty >> (i - 1) & 1 else 0)) for i in range(z, 0, -1))


def stretch(rgb, lo=2, hi=98, gamma=1.0):
    """Percentile stretch a (3, H, W) array to uint8."""
    out = np.zeros(rgb.shape, dtype=np.float32)
    for i in range(rgb.shape[0]):
        b = rgb[i].astype(np.float32)
        valid = b[b > 0]
        if valid.size == 0:
            continue
        a, z = np.percentile(valid, [lo, hi])
        out[i] = np.clip((b - a) / max(z - a, 1e-6), 0, 1) ** gamma
    return (out * 255).astype(np.uint8)


def chm_mosaic(crs, bounds, res, z=10, vrt_path=None):
    """Read CHMv2 onto a grid. All level-10 quadkey tiles covering `bounds` are joined in a VRT first,
    so resampling is seamless across tile edges."""
    import subprocess, tempfile
    from rasterio.warp import transform_bounds
    w, s, e, n = transform_bounds(crs, "EPSG:4326", *bounds)
    keys = sorted({quadkey(lat, lon, z) for lat in np.linspace(s, n, 8) for lon in np.linspace(w, e, 8)})
    vrt = vrt_path or tempfile.mktemp(suffix=".vrt")
    srcs = ["/vsicurl/" + CHM_BASE + k + ".tif" for k in keys]
    subprocess.run(["gdalbuildvrt", "-q", vrt] + srcs, check=True, env={**os.environ})
    left, bottom, right, top = bounds
    width, height = int(round((right - left) / res)), int(round((top - bottom) / res))
    with rasterio.open(vrt) as src:
        with WarpedVRT(src, crs=crs, transform=from_origin(left, top, res, res), width=width, height=height,
                       resampling=Resampling.bilinear) as v:
            a = v.read(1).astype(np.float32)
    return a, keys


def tile_edge_lines(keys):
    """Longitudes and latitudes of internal edges between level-z quadkey tiles."""
    import math
    xs, ys = set(), set()
    for k in keys:
        z = len(k); tx = ty = 0
        for ch in k:
            d = int(ch); tx = tx * 2 + (d & 1); ty = ty * 2 + (d >> 1)
        n = 2 ** z
        xs.update([tx / n * 360 - 180, (tx + 1) / n * 360 - 180])
        for t in (ty, ty + 1):
            ys.add(math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * t / n)))))
    return sorted(xs), sorted(ys)


def blur_lines(z, cols=(), rows=(), half=5, sigma=2.0):
    """Blur a narrow band across given pixel columns/rows (hides tile-edge hairlines in renders)."""
    from scipy.ndimage import gaussian_filter1d
    z = z.astype(np.float32).copy()
    for c in cols:
        if 0 < c < z.shape[1] - 1:
            lo, hi = max(c - half, 0), min(c + half, z.shape[1])
            seg = gaussian_filter1d(z[:, max(lo - 10, 0):min(hi + 10, z.shape[1])], sigma, axis=1)
            z[:, lo:hi] = seg[:, lo - max(lo - 10, 0):hi - max(lo - 10, 0)]
    for r in rows:
        if 0 < r < z.shape[0] - 1:
            lo, hi = max(r - half, 0), min(r + half, z.shape[0])
            seg = gaussian_filter1d(z[max(lo - 10, 0):min(hi + 10, z.shape[0]), :], sigma, axis=0)
            z[lo:hi, :] = seg[lo - max(lo - 10, 0):hi - max(lo - 10, 0), :]
    return z


def edge_pixels(keys, crs, bounds, res, shape):
    """Pixel columns/rows of quadkey tile edges inside a north-up grid."""
    from pyproj import Transformer
    lons, lats = tile_edge_lines(keys)
    tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    left, bottom, right, top = bounds
    midlat = tr.transform(0, 0) and None
    from rasterio.warp import transform_bounds
    w, s, e, n = transform_bounds(crs, "EPSG:4326", *bounds)
    cols = [int(round((tr.transform(lon, (s + n) / 2)[0] - left) / res)) for lon in lons if w < lon < e]
    rows = [int(round((top - tr.transform((w + e) / 2, lat)[1]) / res)) for lat in lats if s < lat < n]
    return [c for c in cols if 0 < c < shape[1]], [r for r in rows if 0 < r < shape[0]]


def detect_lines(chm, axis=1, k=2.3, min_h=3.0):
    """Find straight vertical (axis=1) or horizontal (axis=0) hairlines in a CHM, e.g. where two
    satellite scenes meet. Returns the centre index of each cluster of anomalous columns/rows."""
    from scipy.ndimage import gaussian_filter
    z = chm.astype(np.float32)
    if axis == 1:
        zs = gaussian_filter(z, (3, 0)); lap = np.abs(zs[:, 2:] - 2 * zs[:, 1:-1] + zs[:, :-2]); land = chm[:, 1:-1] > min_h
        prof = (lap * land).sum(0) / np.maximum(land.sum(0), 1)
    else:
        zs = gaussian_filter(z, (0, 3)); lap = np.abs(zs[2:, :] - 2 * zs[1:-1, :] + zs[:-2, :]); land = chm[1:-1, :] > min_h
        prof = (lap * land).sum(1) / np.maximum(land.sum(1), 1)
    hits = np.where(prof > k * np.median(prof))[0] + 1
    out, cur = [], []
    for h in hits:
        if cur and h - cur[-1] > 3:
            out.append(int(np.mean(cur))); cur = []
        cur.append(h)
    if cur:
        out.append(int(np.mean(cur)))
    return out


TTC_URL = "https://tiles.globalforestwatch.org/wri_tropical_tree_cover_extent/v20220922/dynamic/{z}/{x}/{y}.png?implementation=tcd_40"


def ttc_on_grid(crs, bounds, res, z, cache_dir):
    """Tropical Tree Cover extent (>=40% cover) from GFW's public map tiles, reprojected (nearest)
    onto a north-up grid. Returns a 0/1 uint8 array."""
    import math
    from PIL import Image
    from rasterio.warp import reproject, transform_bounds
    w, s, e, n = transform_bounds(crs, "EPSG:4326", *bounds)
    def txy(lat, lon):
        x = (lon + 180) / 360 * 2 ** z
        sl = math.sin(math.radians(lat)); y = (0.5 - math.log((1 + sl) / (1 - sl)) / (4 * math.pi)) * 2 ** z
        return int(x), int(y)
    x0, y0 = txy(n, w); x1, y1 = txy(s, e)
    mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), dtype=np.uint8)
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            f = os.path.join(cache_dir, f"{z}_{tx}_{ty}.png")
            if not os.path.exists(f):
                urllib.request.urlretrieve(TTC_URL.format(z=z, x=tx, y=ty), f)
            a = np.array(Image.open(f).convert("RGBA"))
            mos[(ty - y0) * 256:(ty - y0 + 1) * 256, (tx - x0) * 256:(tx - x0 + 1) * 256] = (a[..., 3] > 0)
    R = 6378137.0; tile_m = 2 * math.pi * R / 2 ** z
    src_t = from_origin(-math.pi * R + x0 * tile_m, math.pi * R - y0 * tile_m, tile_m / 256, tile_m / 256)
    left, bottom, right, top = bounds
    W, H = int(round((right - left) / res)), int(round((top - bottom) / res))
    dst = np.zeros((H, W), dtype=np.uint8)
    reproject(mos, dst, src_transform=src_t, src_crs="EPSG:3857", dst_transform=from_origin(left, top, res, res),
              dst_crs=crs, resampling=Resampling.nearest)
    return dst
