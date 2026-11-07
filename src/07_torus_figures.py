"""
Two more torus pictures for the gas in a box (N = 2 and N = 3 use the same looks as 06_gas_torus.py).

  figures/06_torus_filling.png   after 20, 100 and 400 looks the dots cover the square evenly,
                                 so about 1 look in 4 lands in the "both on the left" quarter
  figures/06_torus_steps.png     circle -> square -> cube: each new particle adds a direction
                                 and halves the target (1/2, 1/4, 1/8)
"""
import importlib
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style

m = importlib.import_module("06_gas_torus")

# a third velocity and start point, used only for the N = 3 panel
V = np.array([0.6180339887, 0.4142135624, 0.7320508076])
X0 = np.array([0.15, 0.35, 0.25])
L = 120


def phi(n, d):
    k = np.arange(n)[:, None]
    return (X0[:d] + V[:d] * k + 0.5) % 2.0


def fig_filling():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.4))
    for ax, n in zip(axes, (20, 100, 400)):
        ph = m.phi(np.arange(n)); ins = m.both_left(ph)
        ax.add_patch(Rectangle((0, 0), 2, 2, fc="white", ec=style.INK, lw=2))
        ax.add_patch(Rectangle((0, 0), 1, 1, fc=style.BLUE, alpha=0.15, ec=style.BLUE, lw=1.5))
        for x in (1,): ax.axvline(x, color=style.MUTED, lw=0.8, ls=":"); ax.axhline(x, color=style.MUTED, lw=0.8, ls=":")
        ax.plot(ph[~ins, 0], ph[~ins, 1], "o", ms=5, color=style.INK, alpha=0.7)
        ax.plot(ph[ins, 0], ph[ins, 1], "o", ms=6, color=style.ORANGE)
        k = int(ins.sum())
        ax.set_title(f"{n} looks: {k} land in the blue quarter\n{n} / {k} = {n/k:.1f} looks per visit", fontsize=14)
        ax.set_xlim(-0.05, 2.05); ax.set_ylim(-0.05, 2.05); ax.set_aspect("equal")
        ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2])
        print(f'{n} looks: {k} in the target, {n / k:.2f} looks per visit')
    fig.suptitle("The dot spreads evenly over the torus, so it lands in a quarter of the area a quarter of the time",
                 fontsize=15, weight="bold", y=1.02)
    fig.tight_layout()
    style.save(fig, "06_torus_filling.png")


def fig_steps():
    fig = plt.figure(figsize=(17, 6.2))
    gs = fig.add_gridspec(1, 5, width_ratios=[1, 0.18, 1, 0.18, 1.15])

    # ---- 1D: a line segment [0,2) with its ends glued = circle
    ax = fig.add_subplot(gs[0])
    p = phi(L, 1)[:, 0]
    ins = p < 1
    ax.plot([0, 2], [0, 0], color=style.INK, lw=2.5)
    ax.plot([0, 1], [0, 0], color=style.BLUE, lw=9, alpha=0.35, solid_capstyle="butt")
    jit = np.linspace(-0.25, 0.25, L)        # spread dots vertically only so they don't overlap
    ax.scatter(p[~ins], 0.0 * p[~ins] + jit[~ins] * 0 + 0.12 + 0.0, s=0)  # placeholder
    ax.plot(p[~ins], np.zeros(ins.size)[~ins] + 0.18, "|", ms=14, color=style.INK, alpha=0.6)
    ax.plot(p[ins], np.zeros(ins.size)[ins] + 0.18, "|", ms=14, color=style.ORANGE)
    for x in (0, 2):
        ax.plot(x, 0, "o", ms=10, color=style.PURPLE, zorder=5)
    ax.annotate("", xy=(2, -0.5), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle="<->", color=style.PURPLE, lw=1.5, connectionstyle="arc3,rad=0.35"))
    ax.text(1, -0.82, "glue the two ends: a circle", ha="center", color=style.PURPLE, fontsize=12)
    ax.text(0.5, 0.45, "left half", ha="center", color=style.BLUE, fontsize=13, weight="bold")
    ax.set_xlim(-0.15, 2.15); ax.set_ylim(-1.0, 0.8)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    for x in (0, 1, 2): ax.text(x, -0.14, str(x), ha="center", va="top", fontsize=13)
    ax.text(1, -0.3, "$\\varphi_1$", ha="center", va="top", fontsize=14)
    k1 = int(ins.sum())
    ax.set_title(f"1 particle: a circle\ntarget = 1/2,  {k1} of {L} looks inside", fontsize=14)

    def arrow(ax, text):
        ax.axis("off")
        ax.add_patch(FancyArrowPatch((0.05, 0.5), (0.95, 0.5), transform=ax.transAxes, arrowstyle="-|>",
                                     mutation_scale=28, color=style.INK, lw=2.5))
        ax.text(0.5, 0.62, text, ha="center", va="bottom", transform=ax.transAxes, fontsize=12)

    arrow(fig.add_subplot(gs[1]), "add a\nparticle\n= add a\ncircle")

    # ---- 2D
    ax = fig.add_subplot(gs[2])
    p = phi(L, 2); ins = np.all(p < 1, axis=1)
    ax.add_patch(Rectangle((0, 0), 2, 2, fc="white", ec=style.INK, lw=2))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=style.BLUE, alpha=0.18, ec=style.BLUE, lw=1.5))
    ax.plot(p[~ins, 0], p[~ins, 1], "o", ms=4, color=style.INK, alpha=0.6)
    ax.plot(p[ins, 0], p[ins, 1], "o", ms=5.5, color=style.ORANGE)
    ax.plot([0, 2], [-0.12, -0.12], color=style.INK, lw=0)
    ax.set_xlim(-0.05, 2.05); ax.set_ylim(-0.05, 2.05); ax.set_aspect("equal")
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2])
    ax.set_xlabel("$\\varphi_1$"); ax.set_ylabel("$\\varphi_2$")
    ax.text(0.5, 0.5, "1/2 × 1/2", ha="center", va="center", color=style.BLUE, fontsize=13, weight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=2), zorder=6)
    k2 = int(ins.sum())
    ax.set_title(f"2 particles: a square (doughnut)\ntarget = 1/4,  {k2} of {L} looks inside", fontsize=14)

    arrow(fig.add_subplot(gs[3]), "add a\nparticle\n= add a\ncircle")

    # ---- 3D
    ax = fig.add_subplot(gs[4], projection="3d")
    p = phi(L, 3); ins = np.all(p < 1, axis=1)
    def box(o, s, color, alpha, lw):
        o = np.array(o, float)
        r = [0, s]
        for a in range(3):
            for b in range(3):
                if b <= a: continue
                c = 3 - a - b
                for u in r:
                    for w in r:
                        P = np.zeros((2, 3)); P[:, a] = u; P[:, b] = w; P[:, c] = r
                        ax.plot(*(P + o).T, color=color, alpha=alpha, lw=lw)
    box((0, 0, 0), 2, style.INK, 0.6, 1.5)
    # shaded target cube faces
    g = np.linspace(0, 1, 2); A, B = np.meshgrid(g, g)
    for a in range(3):
        for side in (0, 1):
            P = [None] * 3; idx = [i for i in range(3) if i != a]
            P[a] = np.full_like(A, side * 1.0); P[idx[0]] = A; P[idx[1]] = B
            ax.plot_surface(*P, color=style.BLUE, alpha=0.18, linewidth=0, shade=False)
    ax.scatter(*p[~ins].T, s=10, color=style.INK, alpha=0.5, depthshade=False)
    ax.scatter(*p[ins].T, s=30, color=style.ORANGE, depthshade=False)
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2]); ax.set_zticks([0, 1, 2])
    ax.set_xlabel("$\\varphi_1$"); ax.set_ylabel("$\\varphi_2$"); ax.set_zlabel("$\\varphi_3$")
    ax.view_init(elev=20, azim=-60); ax.set_box_aspect((1, 1, 1), zoom=0.92)
    k3 = int(ins.sum())
    ax.set_title(f"3 particles: a cube\ntarget = 1/8,  {k3} of {L} looks inside", fontsize=14, pad=0)

    fig.suptitle("Each new particle adds one more circle, so one more direction. The target is the left half "
                 "along every direction, so it halves each time.", fontsize=14.5, weight="bold", y=1.02)
    style.save(fig, "06_torus_steps.png")
    print(f'looks inside the target out of {L}: circle {k1}, square {k2}, cube {k3}')


def main():
    style.apply()
    fig_filling()
    fig_steps()


if __name__ == "__main__":
    main()
