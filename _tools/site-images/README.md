# Site images

Scripts that make the home page banner and the three "Current work" cards and figures from open data.
Jekyll ignores this folder (its name starts with `_`), so none of it is published.

| Image | Place | Data |
|---|---|---|
| `home-banner.jpg`, `card-canopy-height.jpg`, `fig-canopy-height.jpg` | Adirondacks, New York | USDA NAIP aerial photo, Oct 2022 (public domain), via Microsoft Planetary Computer; CHMv2 (CC BY 4.0), AWS Open Data |
| `card-tree-cover.jpg`, `fig-tree-cover.jpg` | Near Techiman, Ghana | Copernicus Sentinel-2 L2A, Jan 2020, via Planetary Computer; 2020 tree cover from the local Ghana mosaic |
| `card-restoration.jpg`, `fig-restoration.jpg` | Restoration planting ("14. Massive planting") | Two frames of `treecountv1/tree_detections.mp4`: imagery only (30.5 s) and with detections (32.5 s) |

Only small windows are read from the remote Cloud-Optimized GeoTIFFs, so each site downloads tens of MB at most. The restoration card instead comes from a local screen recording; its imagery may be commercial, so check its licence before reusing it elsewhere.

## Setup

Python 3.10+ with `rasterio`, `numpy`, `scipy`, `pillow`, `matplotlib` and `pyproj`, plus the GDAL command-line tools (`gdalbuildvrt` is used to join CHMv2 tiles).

```bash
S=_tools/site-images   # scripts
D=/tmp/site-images/data; O=/tmp/site-images/out; mkdir -p $D/ttc $O
```

## Steps

```bash
# Adirondacks: banner and canopy height card (x, y, width in metres from the top-left of the fetched area)
python $S/fetch_adk.py $S $D
python $S/render_banner.py $S $D $O 400 900 2700 b_canopy canopy
python $S/render_card_chm.py $S $D $O 170 0 1080

# Ghana: tree cover card (window offset in km). fetch_ghana.py also caches GFW map tiles, used only for comparison.
python $S/fetch_ghana.py $S $D
python $S/read_ghana_mosaic.py $S $D "/Volumes/John/mosaics-2020/Ghana.tif"
python $S/render_card_ttc.py $S $D $O 0.3 4.0

# Restoration card: two aligned frames from the tree detection viewer recording ("blink trees" toggles detections),
# cropped clear of the control panel (x, y, width in video pixels; height is 2/3 of width)
V=/Users/work/Desktop/treecountv1/tree_detections.mp4
ffmpeg -ss 30.5 -i $V -frames:v 1 $D/frame_imagery.png
ffmpeg -ss 32.5 -i $V -frames:v 1 $D/frame_detections.png
python $S/render_card_video.py $D/frame_imagery.png $D/frame_detections.png $O/card_restoration.jpg $O/fig_restoration_pair.jpg 790 40 2820

# Write web-sized JPEGs into the site
python $S/encode.py $O assets/images
```

## Notes

- Colours: `viz.py` defines the canopy height ramp (`canopy`): navy for ground and water, through blue and green to yellow for the tallest canopy. The tree cover card uses the discrete classes from `sentinel-tree-cover/references/style.qml` (36 / 52 / 68 / 84%).
- CHMv2 is stored in whole metres, so heights are smoothed slightly before hillshading to avoid terracing.
- CHMv2 tiles are predicted independently and some contain seams between satellite scenes; `common.detect_lines` and `blur_lines` hide those hairlines in the renders only.
- CHMv2 reads lower than the 3DEP lidar max-height layer in every US site checked (by 5 to 17 m), partly because that layer keeps the highest return per 2 m cell. The figures therefore show aerial photo vs CHMv2, not CHMv2 vs lidar.
