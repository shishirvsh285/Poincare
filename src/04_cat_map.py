"""
Example 2: Arnold's cat map, the most dramatic recurrence there is.

On an N x N grid of pixels, move the pixel at (x, y) to

    (x, y)  ->  (2x + y,  x + y)   mod N

The matrix [[2, 1], [1, 1]] has determinant 1, so the map is a one-to-one
shuffle of pixels: it preserves "area" (pixel count) exactly. It is also
chaotic: nearby pixels fly apart fast. The picture turns to static.
But a shuffle of a FINITE set of pixels must repeat. For N = 101 the
picture comes back perfectly after exactly 25 steps.

Outputs
  figures/04_cat_map_strip.png   selected frames in a row
  figures/04_cat_map.gif         the full loop
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

import style

N = 101


def make_picture(n=N):
    """A home-made test picture: a smiling face with a pendulum next to it."""
    y, x = np.mgrid[0:n, 0:n] / n
    img = np.ones((n, n, 3)) * np.array([0.93, 0.95, 0.99])          # pale background
    face = (x - 0.38) ** 2 + (y - 0.45) ** 2 < 0.27**2
    img[face] = [0.99, 0.80, 0.20]
    for ex in (0.29, 0.47):                                           # eyes
        img[(x - ex) ** 2 + (y - 0.37) ** 2 < 0.045**2] = [0.11, 0.12, 0.16]
    r = np.hypot(x - 0.38, y - 0.47)                                  # smile
    img[(np.abs(r - 0.15) < 0.025) & (y > 0.52) & face] = [0.11, 0.12, 0.16]
    # pendulum on the right: a string and a blue bob
    img[(np.abs(x - 0.82) < 0.012) & (y > 0.08) & (y < 0.66)] = [0.42, 0.45, 0.50]
    img[(x - 0.82) ** 2 + (y - 0.74) ** 2 < 0.09**2] = [0.15, 0.39, 0.92]
    img[(y < 0.08) & (x > 0.68) & (x < 0.96)] = [0.11, 0.12, 0.16]    # ceiling
    return img


def cat(img):
    n = img.shape[0]
    ys, xs = np.mgrid[0:n, 0:n]
    out = np.empty_like(img)
    out[(xs + ys) % n, (2 * xs + ys) % n] = img[ys, xs]               # row index = y
    return out


def main():
    style.apply()
    frames = [make_picture()]
    for _ in range(60):
        frames.append(cat(frames[-1]))
        if np.array_equal(frames[-1], frames[0]):
            break
    period = len(frames) - 1
    print(f"cat map on a {N}x{N} grid returns exactly after {period} steps")

    show = [0, 1, 2, 4, 12, 20, 24, period]
    fig, axes = plt.subplots(1, len(show), figsize=(2.1 * len(show), 2.75))
    for ax, k in zip(axes, show):
        ax.imshow(frames[k], interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        last = k == period
        col = style.ORANGE if last else style.INK
        ax.set_title(f"step {k}", color=col, fontsize=13)
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_color(style.ORANGE if last else style.MUTED)
            sp.set_linewidth(3 if last else 0.8)
    fig.suptitle(f"Arnold's cat map on {N}$\\times${N} pixels: scrambled to noise, "
                 f"then back exactly at step {period}", fontsize=14, weight="bold", y=1.04)
    style.save(fig, "04_cat_map_strip.png")

    fig, ax = plt.subplots(figsize=(4, 4.3))
    im = ax.imshow(frames[0], interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ttl = ax.set_title("step 0")

    def update(k):
        im.set_data(frames[k])
        ttl.set_text(f"step {k}" + ("  (back!)" if k == period else ""))
        return im, ttl

    order = list(range(period + 1)) + [period] * 8          # pause on the return
    anim = FuncAnimation(fig, lambda i: update(order[i]), frames=len(order))
    anim.save(style.FIG_DIR / "04_cat_map.gif", writer=PillowWriter(fps=4), dpi=90)
    plt.close(fig)
    print("saved figures/04_cat_map.gif")


if __name__ == "__main__":
    main()
