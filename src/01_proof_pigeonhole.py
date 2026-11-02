"""
Figure for the proof slide: the pigeonhole idea.

We use the simplest area-preserving map we could think of: a shift on the
torus (a square box with wrap-around edges) by an irrational step

    f(q, p) = (q + a, p + b)  mod 1,   a = sqrt(5)-2, b = sqrt(2)-1

A disk U keeps its area under f. So every image f^n(U) has the same area.
The box has area 1. So at most about 1/area(U) disjoint copies fit.
Sooner or later two images must overlap, and (because f can be undone)
that means some f^k(U) overlaps U itself.

The same argument works for ANY volume-preserving map on a finite box,
including the flow of a Hamiltonian system. We just picked the one that
draws nicely.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import style

STEP = np.array([np.sqrt(5) - 2, np.sqrt(2) - 1])
CENTER = np.array([0.22, 0.25])
RADIUS = 0.06


def torus_dist(a, b):
    d = (a - b + 0.5) % 1.0 - 0.5
    return np.hypot(*d)


def first_overlap():
    """Smallest n >= 1 with f^n(U) touching U (two disks overlap iff centres < 2r apart)."""
    for n in range(1, 10_000):
        c = (CENTER + n * STEP) % 1.0
        if torus_dist(c, CENTER) < 2 * RADIUS:
            return n
    return None


def draw_disk(ax, c, **kw):
    # draw the disk plus its wrapped copies so blobs near an edge look right
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            ax.add_patch(Circle(c + np.array([dx, dy]), RADIUS, **kw))


def main():
    style.apply()
    n_hit = first_overlap()
    area_ratio = np.pi * RADIUS**2
    print(f"area(U) = {area_ratio:.4f} of the box, so at most ~{int(1/area_ratio)} disjoint copies fit")
    print(f"first overlap with U at n = {n_hit}")

    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    cmap = plt.get_cmap("viridis")
    for n in range(1, n_hit + 1):
        c = (CENTER + n * STEP) % 1.0
        last = n == n_hit
        col = style.ORANGE if last else cmap(0.15 + 0.7 * n / n_hit)
        draw_disk(ax, c, fc=col, ec="white", lw=1.0, alpha=0.85 if last else 0.6, zorder=3 if last else 2)
        ax.text(*c, str(n), ha="center", va="center", fontsize=12, color="white", weight="bold", zorder=6, clip_on=True)

    draw_disk(ax, CENTER, fc="none", ec=style.BLUE, lw=3, zorder=5)
    ax.text(CENTER[0] - RADIUS - 0.02, CENTER[1] + RADIUS + 0.01, "$U$", ha="right", fontsize=22,
            color=style.BLUE, weight="bold", zorder=6)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(2)
    ax.set_xlabel("position $q$")
    ax.set_ylabel("momentum $p$")
    ax.set_title("Every copy $f^n(U)$ has the same area as $U$")
    ax.text(0.5, -0.1,
            f"Copy {n_hit} lands on $U$. Finite room plus equal-sized guests means sharing.",
            transform=ax.transAxes, ha="center", fontsize=13, color=style.ORANGE)
    style.save(fig, "01_pigeonhole_proof.png")


if __name__ == "__main__":
    main()
