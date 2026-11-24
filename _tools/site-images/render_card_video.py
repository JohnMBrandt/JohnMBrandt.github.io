"""Restoration card from two aligned frames of the tree detection viewer recording:
imagery only (upper left) vs the same view with detections (lower right), cropped clear of the viewer UI."""
import sys
from PIL import Image, ImageDraw
img_path, det_path, out_card, out_fig = sys.argv[1:5]
x0, y0, w = (int(v) for v in sys.argv[5:8])
h = w * 2 // 3
box = (x0, y0, x0 + w, y0 + h)
W_OUT, H_OUT = 1200, 800
photo = Image.open(img_path).convert("RGB").crop(box).resize((W_OUT, H_OUT), Image.LANCZOS)
dets = Image.open(det_path).convert("RGB").crop(box).resize((W_OUT, H_OUT), Image.LANCZOS)
mask = Image.new("L", (W_OUT, H_OUT), 0)
ImageDraw.Draw(mask).polygon([(W_OUT, 0), (W_OUT, H_OUT), (0, H_OUT)], fill=255)
card = Image.composite(dets, photo, mask)
line = Image.new("RGBA", (W_OUT, H_OUT), (0, 0, 0, 0))
ImageDraw.Draw(line).line([(W_OUT, 0), (0, H_OUT)], fill=(255, 255, 255, 170), width=3)
Image.alpha_composite(card.convert("RGBA"), line).convert("RGB").save(out_card, quality=84, optimize=True, progressive=True)
gap = 12
fig = Image.new("RGB", (W_OUT * 2 + gap, H_OUT), "white")
fig.paste(photo, (0, 0)); fig.paste(dets, (W_OUT + gap, 0))
fig.resize((1600, int(1600 * H_OUT / (W_OUT * 2 + gap))), Image.LANCZOS).save(out_fig, quality=84, optimize=True, progressive=True)
print("crop", box)
