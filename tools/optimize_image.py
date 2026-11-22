"""Prepare an image for the site: resize, drop metadata (incl. GPS), keep the ICC profile.

Usage: python3 tools/optimize_image.py <input> <output.jpg|output.png> [--max-width 1440] [--min-psnr 38]

- Output format follows the output extension: JPEG for photos and illustrations, PNG for graphics with
  flat colours or transparency (CLAUDE.md, "Blog posts").
- Images wider than --max-width are resized (LANCZOS); EXIF orientation is applied first.
- JPEG: tries qualities 82-94 with 4:2:0 and 4:4:4 chroma and keeps the smallest file whose PSNR against
  the (resized) original reaches --min-psnr (38 dB is not visible at normal viewing distance).
- Prints sizes and PSNR. The output never contains EXIF or XMP metadata.
"""
import argparse
import io
import math
import os

from PIL import Image, ImageChops, ImageOps

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("output")
ap.add_argument("--max-width", type=int, default=1440)
ap.add_argument("--min-psnr", type=float, default=38.0)
args = ap.parse_args()


def flat(im):
    im = im.convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.getchannel("A"))
    return bg


def psnr(a, b):
    h = ImageChops.difference(a.convert("RGB"), b.convert("RGB")).histogram()
    mse = sum(v * ((i % 256) ** 2) for i, v in enumerate(h)) / float(a.size[0] * a.size[1] * 3)
    return float("inf") if mse == 0 else 10 * math.log10(255 ** 2 / mse)


src = Image.open(args.input)
icc = src.info.get("icc_profile")
im = ImageOps.exif_transpose(src)
if im.size[0] > args.max_width:
    im = im.resize((args.max_width, round(im.size[1] * args.max_width / im.size[0])), Image.LANCZOS)
ref = flat(im)

if args.output.lower().endswith((".jpg", ".jpeg")):
    best = None
    for q in (82, 85, 88, 90, 92, 94):
        for ss in (2, 0):  # 2 = 4:2:0, 0 = 4:4:4
            buf = io.BytesIO()
            ref.save(buf, "JPEG", quality=q, subsampling=ss, optimize=True, progressive=True, icc_profile=icc)
            score = psnr(ref, Image.open(io.BytesIO(buf.getvalue())))
            key = (score >= args.min_psnr, -len(buf.getvalue()) if score >= args.min_psnr else score)
            if best is None or key > best[0]:
                best = (key, q, ss, score, buf.getvalue())
    _, q, ss, score, data = best
    note = f"JPEG q{q} {'4:4:4' if ss == 0 else '4:2:0'}, PSNR {score:.1f} dB" + ("" if score >= args.min_psnr else " (below target)")
else:
    out = im if (im.mode == "RGBA" and im.getchannel("A").getextrema() != (255, 255)) else im.convert("RGB")
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True, icc_profile=icc)
    data, note = buf.getvalue(), "PNG (lossless)"

open(args.output, "wb").write(data)
print(f"{args.input}: {os.path.getsize(args.input)/1e3:.0f} KB {src.size[0]}x{src.size[1]} -> "
      f"{args.output}: {len(data)/1e3:.0f} KB {im.size[0]}x{im.size[1]}, {note}")
