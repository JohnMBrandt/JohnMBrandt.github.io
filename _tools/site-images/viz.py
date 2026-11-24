"""Rendering helpers shared by the banner and card scripts."""
import numpy as np
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

# Height ramp used across the site: deep blue-green (ground) -> green -> pale yellow (tallest).
CMAPS = {
    "green": LinearSegmentedColormap.from_list("green", ["#0b1d2a", "#123d4a", "#1b6b5a", "#3f9a4f", "#9cc74a", "#f2e79a"], N=256),
    "tealgold": LinearSegmentedColormap.from_list("tealgold", ["#0d1b2a", "#1b3a5c", "#22668a", "#2a9d8f", "#8ac926", "#ffd166", "#fff3c4"], N=256),
    "viridis": matplotlib.colormaps["viridis"],
    # viridis-like, but starting at navy so water and bare ground match dark lakes in the photos
    "canopy": LinearSegmentedColormap.from_list("canopy", [(0, "#0d1b2a"), (0.2, "#1d3b63"), (0.4, "#26688d"), (0.6, "#1f9e89"), (0.8, "#6cce59"), (1.0, "#fde725")], N=256),
}
HEIGHT_CMAP = CMAPS["canopy"]


def soften_seams(chm, axis=1, thresh=4.0, half=4):
    """CHMv2 tiles are predicted independently, so a tile edge can leave a one-pixel discontinuity.
    Find columns (axis=1) or rows (axis=0) whose mean jump stands far above the rest and blur across them."""
    from scipy.ndimage import gaussian_filter1d
    z = chm.astype(np.float32).copy()
    jump = np.abs(np.diff(z, axis=axis)).mean(axis=1 - axis)
    med = np.median(jump)
    for k in np.where(jump > thresh * med)[0]:
        lo, hi = max(k - half, 0), min(k + half + 2, z.shape[axis])
        sl = [slice(None), slice(None)]; sl[axis] = slice(max(lo - 8, 0), min(hi + 8, z.shape[axis]))
        blurred = gaussian_filter1d(z[tuple(sl)], 2.0, axis=axis)
        inner = [slice(None), slice(None)]; inner[axis] = slice(lo - sl[axis].start, hi - sl[axis].start)
        tgt = [slice(None), slice(None)]; tgt[axis] = slice(lo, hi)
        z[tuple(tgt)] = blurred[tuple(inner)]
    return z, [int(k) for k in np.where(jump > thresh * med)[0]]


def hillshade(z, res, azimuth=315.0, altitude=40.0, zf=1.0):
    gy, gx = np.gradient(z * zf, res)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    az, alt = np.radians(360 - azimuth + 90), np.radians(altitude)
    hs = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
    return np.clip(hs, 0, 1)


def multi_hillshade(z, res, zf=1.5):
    """Softer, direction-balanced shading (weighted blend of four light directions)."""
    dirs = [(315, 0.45), (270, 0.2), (0, 0.2), (225, 0.15)]
    return sum(w * hillshade(z, res, a, 40, zf) for a, w in dirs)


def height_rgb(chm, res, vmax, cmap=HEIGHT_CMAP, shade_strength=0.6, zf=1.5, sigma=1.2):
    """Colour canopy height with the site ramp and modulate by hillshade so crowns read in 3D.
    CHMv2 is stored in whole metres, so it is smoothed slightly before shading to avoid terracing."""
    from scipy.ndimage import gaussian_filter
    z = gaussian_filter(chm.astype(np.float32), sigma) if sigma else chm
    col = cmap(np.clip(z / vmax, 0, 1))[..., :3]
    hs = multi_hillshade(z, res, zf)
    hs = (hs - hs.min()) / max(hs.max() - hs.min(), 1e-6)
    shade = (1 - shade_strength) + shade_strength * (0.35 + 0.9 * hs)
    return np.clip(col * shade[..., None], 0, 1)


def stretch_params(rgb, lo=0.5, hi=99.7):
    """Per-band percentile limits from a reference (3, H, W) array, so several crops share one look."""
    return [tuple(np.percentile(rgb[i][rgb[i] > 0][::7], [lo, hi])) for i in range(3)]


def photo_rgb(rgb, params=None, gamma=0.95, sat=1.08):
    """Per-band linear stretch with a small saturation lift; input (3, H, W) uint8."""
    params = params or stretch_params(rgb)
    out = np.zeros(rgb.shape[1:] + (3,), dtype=np.float32)
    for i, (a, z) in enumerate(params):
        out[..., i] = np.clip((rgb[i].astype(np.float32) - a) / (z - a), 0, 1) ** gamma
    grey = out.mean(axis=2, keepdims=True)
    return np.clip(grey + (out - grey) * sat, 0, 1)


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def to_image(arr, size=None):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    if size:
        im = im.resize(size, Image.LANCZOS)
    return im
