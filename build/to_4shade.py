"""Convert product photos to 512x512 single-channel 4-shade images.

Output convention: 255 = background (no particles), 170 / 85 / 0 = light / mid / dark ink.
Background = pixels close to white (colour-aware, so light pink still counts as product).
Ink thresholds are set per image from the product's own luminance percentiles,
so every product uses all 3 ink shades (a black tee and a pink top both get detail).
"""
import sys, glob, os
import numpy as np
from PIL import Image

SIZE, FILL, WHITE_TOL = 512, 0.80, 28


def fg_mask(rgb):
    a = np.asarray(rgb).astype(np.int16)
    return (255 - a).max(axis=2) > WHITE_TOL  # any channel clearly below white


def convert(path, out):
    img = Image.open(path).convert("RGB")
    m = fg_mask(img)
    ys, xs = np.where(m)
    img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    w, h = img.size
    side = int(max(w, h) / FILL)
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(img, ((side - w) // 2, (side - h) // 2))
    canvas = canvas.resize((SIZE, SIZE), Image.LANCZOS)

    m = fg_mask(canvas)
    lum = np.asarray(canvas.convert("L")).astype(np.float32)
    t1, t2 = np.percentile(lum[m], [33, 66])
    out_img = np.full(lum.shape, 255, np.uint8)
    out_img[m & (lum >= t2)] = 170   # light ink
    out_img[m & (lum >= t1) & (lum < t2)] = 85  # mid ink
    out_img[m & (lum < t1)] = 0      # dark ink
    Image.fromarray(out_img, "L").save(out)
    return m.mean()


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    for f in sorted(glob.glob(os.path.join(src, "*"))):
        name = os.path.splitext(os.path.basename(f))[0]
        cov = convert(f, os.path.join(dst, name + ".png"))
        print(f"{name:10s} coverage {cov:.1%}")
