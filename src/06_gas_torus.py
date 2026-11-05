"""
The gas in a box, drawn as a point moving on a torus.

Step 1: one particle bouncing between the walls x = 0 and x = 1 is the same as
        a point running round a circle of length 2. Going once round the circle
        is: left wall -> right wall -> back to the left wall.
        We use the angle  phi = (theta + 1/2) mod 2,  where  theta = x0 + v t
        is the unfolded position. Then
            phi in [0, 1)  <=>  particle is in the LEFT half of the box
            phi in [1, 2)  <=>  particle is in the RIGHT half
Step 2: two particles = two angles (phi1, phi2) = a point on a torus.
        Cut open, the torus is the square [0, 2) x [0, 2) with opposite edges glued.
        The gas just moves in a straight line with slope v2 / v1, wrapping round.
Step 3: "both particles on the left" is the square [0, 1) x [0, 1):
        a quarter of the torus. Kac's lemma: mean wait = 1 / (1/4) = 4 looks.
        N particles: N-torus, target is 2^-N of it, mean wait 2^N looks.

Outputs
  figures/06_torus_idea.png         circle -> square torus -> doughnut, for N = 2
  figures/06_torus_dimensions.png   square (1/4) -> cube (1/8) -> 2^-N
  figures/06_torus_gas.gif          the box and the torus moving together
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle, FancyArrowPatch, Wedge

import style

V = np.array([0.6180339887, 0.4142135624])     # velocities (units: box widths per look)
X0 = np.array([0.15, 0.35])                    # both start in the left half
N_LOOKS_DEMO = 14


# ------------------------------------------------------------------ physics
def phi(t):
    """Torus angles in [0, 2) at time(s) t, shape (len(t), 2)."""
    t = np.atleast_1d(t)[:, None]
    return (X0 + V * t + 0.5) % 2.0


def x_of_phi(ph):
    th = (ph - 0.5) % 2.0
    return np.where(th < 1.0, th, 2.0 - th)


def both_left(ph):
    return np.all(ph < 1.0, axis=-1)


def mean_wait(n_looks=200_000):
    ph = phi(np.arange(1, n_looks + 1))
    hits = np.nonzero(both_left(ph))[0]
    gaps = np.diff(hits)
    return gaps.mean(), len(gaps)


# ------------------------------------------------------------------ drawing helpers
def path_segments(t0, t1, n=4000):
    """Straight-line path on the square, split where it wraps round an edge."""
    ph = phi(np.linspace(t0, t1, n))
    jump = np.any(np.abs(np.diff(ph, axis=0)) > 1.0, axis=1)
    ph = ph.astype(float)
    out = ph.copy()
    out[1:][jump] = np.nan
    return out


def draw_square(ax, n_looks, show_numbers=True, fs=12):
    ax.add_patch(Rectangle((0, 0), 2, 2, fc="white", ec=style.INK, lw=2))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=style.BLUE, alpha=0.16, ec="none"))
    ax.text(0.5, 0.5, "both on\nthe left", ha="center", va="center", color=style.BLUE,
            fontsize=fs + 1, weight="bold")
    seg = path_segments(0, n_looks)
    ax.plot(seg[:, 0], seg[:, 1], color=style.MUTED, lw=1.0, alpha=0.8)
    ph = phi(np.arange(n_looks + 1))
    inside = both_left(ph)
    for k, (a, b) in enumerate(ph):
        col = style.ORANGE if (inside[k] and k > 0) else (style.GREEN if k == 0 else style.INK)
        ax.plot(a, b, "o", ms=9 if k == 0 or inside[k] else 6, color=col, zorder=5, mec="white")
        if show_numbers:
            ax.text(a + 0.05, b + 0.05, str(k), fontsize=fs - 2, color=col, zorder=6)
    # glued-edge arrows: single arrows on left/right, double on top/bottom
    for y in (0.0, 2.0):
        ax.annotate("", xy=(1.15, y), xytext=(0.85, y),
                    arrowprops=dict(arrowstyle="-|>", color=style.PURPLE, lw=2.2))
    for x in (0.0, 2.0):
        ax.annotate("", xy=(x, 1.15), xytext=(x, 0.85),
                    arrowprops=dict(arrowstyle="-|>", color=style.RED, lw=2.2))
    ax.set_xlim(-0.08, 2.08)
    ax.set_ylim(-0.08, 2.08)
    ax.set_aspect("equal")
    ax.set_xticks([0, 1, 2], ["0", "1", "2"])
    ax.set_yticks([0, 1, 2], ["0", "1", "2"])
    ax.set_xlabel("particle 1 angle $\\varphi_1$")
    ax.set_ylabel("particle 2 angle $\\varphi_2$")
    return inside


def draw_circle(ax):
    R = 1.0
    ax.add_patch(Wedge((0, 0), R, 90, 270, width=0.16, fc=style.BLUE, ec="none"))   # phi in [0,1): left
    ax.add_patch(Wedge((0, 0), R, -90, 90, width=0.16, fc=style.ORANGE, ec="none"))  # phi in [1,2): right
    # angle on the circle: phi = 0 at the top, increasing anticlockwise; half a turn = 1
    def pt(p, r=R):
        a = np.pi / 2 + np.pi * p
        return r * np.cos(a), r * np.sin(a)
    for p, lab, off in [(0.5, "left wall\n$x = 0$", 1.32), (1.5, "right wall\n$x = 1$", 1.32),
                        (0.0, "middle", 1.2), (1.0, "middle", 1.2)]:
        x, y = pt(p, R - 0.08)
        ax.plot(x, y, "o", color=style.INK, ms=6, zorder=5)
        lx, ly = pt(p, off)
        ax.text(lx, ly, lab, ha="center", va="center", fontsize=11)
    ax.add_patch(FancyArrowPatch(pt(0.12, 0.72), pt(0.38, 0.72), connectionstyle="arc3,rad=0.25",
                                 arrowstyle="-|>", mutation_scale=16, color=style.INK, lw=1.5))
    ax.text(-0.45, 0, "left\nhalf", color=style.BLUE, ha="center", va="center", fontsize=13, weight="bold")
    ax.text(0.45, 0, "right\nhalf", color=style.ORANGE, ha="center", va="center", fontsize=13, weight="bold")
    ax.text(0, -1.55, "middle = the line $x = 1/2$", ha="center", fontsize=10.5, color=style.MUTED)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.7, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_doughnut(ax, n_looks):
    R, r = 3.0, 1.15
    elev, azim = 40, -60
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 120), np.linspace(0, 2 * np.pi, 60))
    X = (R + r * np.cos(v)) * np.cos(u)
    Y = (R + r * np.cos(v)) * np.sin(u)
    Z = r * np.sin(v)
    target = (u < np.pi) & (v < np.pi)                 # phi1 in [0,1), phi2 in [0,1)
    cols = np.where(target[..., None], np.array([0.55, 0.68, 0.96, 1.0]), np.array([0.90, 0.91, 0.93, 1.0]))
    ax.plot_surface(X, Y, Z, facecolors=cols, linewidth=0, shade=True, antialiased=True)

    e, az = np.radians(elev), np.radians(azim)
    view = np.array([np.cos(e) * np.cos(az), np.cos(e) * np.sin(az), np.sin(e)])

    def place(ph, lift):
        uu, vv = np.pi * ph[:, 0], np.pi * ph[:, 1]
        rr = r + lift
        P = np.stack([(R + rr * np.cos(vv)) * np.cos(uu), (R + rr * np.cos(vv)) * np.sin(uu), rr * np.sin(vv)])
        normal = np.stack([np.cos(vv) * np.cos(uu), np.cos(vv) * np.sin(uu), np.sin(vv)])
        return P, view @ normal > 0

    P, front = place(phi(np.linspace(0, n_looks, 4000)), 0.03)
    ax.plot(*np.where(front, P, np.nan), color=style.INK, lw=1.2)      # only the side facing us
    pk = phi(np.arange(n_looks + 1))
    ins = both_left(pk)
    Pk, fk = place(pk, 0.08)
    for k in range(len(pk)):
        if not fk[k]:
            continue
        col = style.GREEN if k == 0 else (style.ORANGE if ins[k] else style.INK)
        ax.scatter(*Pk[:, k], color=col, s=90 if (k == 0 or ins[k]) else 25, depthshade=False,
                   edgecolors="white", linewidths=0.8)
    ax.set_box_aspect((1, 1, 0.4), zoom=1.35)
    ax.view_init(elev=elev, azim=azim)
    ax.computed_zorder = False
    ax.axis("off")


# ------------------------------------------------------------------ figures
def fig_idea():
    fig = plt.figure(figsize=(16.5, 5.6))
    ax1 = fig.add_subplot(1, 3, 1)
    draw_circle(ax1)
    ax1.set_title("1. One particle: a bounce is a circle", pad=12)
    ax2 = fig.add_subplot(1, 3, 2)
    inside = draw_square(ax2, N_LOOKS_DEMO)
    ax2.set_title("2. Two particles: a point on a torus\n(square with opposite edges glued)", pad=10)
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    draw_doughnut(ax3, N_LOOKS_DEMO)
    ax3.set_title("3. Glue the edges: a doughnut\n(blue = both on the left; front side shown)", pad=0)
    first = int(np.nonzero(inside[1:])[0][0]) + 1
    fig.text(0.5, -0.06,
             f"Green dot = start (look 0). Orange = both particles back on the left (first at look {first}). "
             "Blue patch = a quarter of the torus.", ha="center", fontsize=13, color=style.INK)
    fig.tight_layout()
    style.save(fig, "06_torus_idea.png")
    return first


def fig_dimensions():
    fig = plt.figure(figsize=(13, 4.8))
    ax = fig.add_subplot(1, 3, 1)
    ax.add_patch(Rectangle((0, 0), 2, 2, fc="white", ec=style.INK, lw=2))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=style.BLUE, alpha=0.35, ec=style.BLUE, lw=1.5))
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-0.1, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("$N = 2$: square torus\ntarget = $1/4$, wait = 4 looks")

    ax = fig.add_subplot(1, 3, 2, projection="3d")
    def cube(ax, o, s, face, edge, alpha):
        o = np.array(o, float)
        for a in range(3):
            for side in (0, 1):
                idx = [i for i in range(3) if i != a]
                g = np.linspace(0, s, 2)
                A, B = np.meshgrid(g, g)
                P = [None] * 3
                P[a] = np.full_like(A, o[a] + side * s)
                P[idx[0]] = o[idx[0]] + A
                P[idx[1]] = o[idx[1]] + B
                ax.plot_surface(*P, color=face, alpha=alpha, edgecolor=edge, linewidth=1.2, shade=False)
    cube(ax, (0, 0, 0), 2, "white", style.INK, 0.05)
    cube(ax, (0, 0, 0), 1, style.BLUE, style.BLUE, 0.45)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-58)
    ax.axis("off")
    ax.set_title("$N = 3$: cube torus\ntarget = $1/8$, wait = 8 looks", pad=0)

    ax = fig.add_subplot(1, 3, 3)
    ax.axis("off")
    ax.text(0.5, 0.62, "$N$ particles", ha="center", fontsize=20, weight="bold")
    ax.text(0.5, 0.44, "$N$-torus,  target $= 2^{-N}$", ha="center", fontsize=19)
    ax.text(0.5, 0.26, "mean wait $= 2^{N}$ looks", ha="center", fontsize=19, color=style.ORANGE)
    fig.tight_layout()
    style.save(fig, "06_torus_dimensions.png")


def gif_gas():
    fpl = 6                                   # frames per look
    n_looks = 30
    times = np.arange(n_looks * fpl + 1) / fpl
    ph_all = phi(times)
    xs = x_of_phi(ph_all)
    looks = phi(np.arange(n_looks + 1))
    ins = both_left(looks)

    fig, (axb, axt) = plt.subplots(1, 2, figsize=(9.6, 4.9), gridspec_kw={"width_ratios": [1, 1.05]})
    seg = path_segments(0, n_looks, 6000)

    def update(i):
        t = times[i]
        k = int(np.floor(t + 1e-9))
        for ax in (axb, axt):
            ax.clear()
        # the box
        axb.add_patch(Rectangle((0, 0), 0.5, 1, fc=style.BLUE, alpha=0.12, ec="none"))
        axb.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=style.INK, lw=2))
        axb.axvline(0.5, color=style.MUTED, ls=":", lw=1)
        axb.plot(xs[i, 0], 0.65, "o", ms=16, color=style.PURPLE, mec="white", zorder=5)
        axb.plot(xs[i, 1], 0.35, "o", ms=16, color=style.GREEN, mec="white", zorder=5)
        axb.text(0.02, 0.92, "particle 1", color=style.PURPLE, fontsize=11, transform=axb.transAxes)
        axb.text(0.02, 0.05, "particle 2", color=style.GREEN, fontsize=11, transform=axb.transAxes)
        axb.set_xlim(-0.02, 1.02)
        axb.set_ylim(-0.02, 1.02)
        axb.set_aspect("equal")
        axb.set_xticks([])
        axb.set_yticks([])
        for sp in axb.spines.values():
            sp.set_visible(False)
        n_ret = int(ins[1:k + 1].sum())
        axb.set_title(f"the box   (look {k}, returns so far: {n_ret})", fontsize=12)
        # the torus
        axt.add_patch(Rectangle((0, 0), 2, 2, fc="white", ec=style.INK, lw=2))
        axt.add_patch(Rectangle((0, 0), 1, 1, fc=style.BLUE, alpha=0.16, ec="none"))
        upto = int(t / n_looks * (len(seg) - 1))
        axt.plot(seg[:upto + 1, 0], seg[:upto + 1, 1], color=style.MUTED, lw=1.0)
        for j in range(k + 1):
            col = style.GREEN if j == 0 else (style.ORANGE if ins[j] else style.INK)
            axt.plot(*looks[j], "o", ms=7 if (j == 0 or ins[j]) else 4, color=col, zorder=5)
        axt.plot(*ph_all[i], "o", ms=12, color=style.RED, mec="white", zorder=6)
        axt.set_xlim(-0.05, 2.05)
        axt.set_ylim(-0.05, 2.05)
        axt.set_aspect("equal")
        axt.set_xticks([0, 1, 2])
        axt.set_yticks([0, 1, 2])
        axt.set_xlabel("$\\varphi_1$")
        axt.set_ylabel("$\\varphi_2$")
        axt.set_title("the same gas: one point on a torus", fontsize=12)

    frames = list(range(len(times))) + [len(times) - 1] * 12
    FuncAnimation(fig, lambda f: update(frames[f]), frames=len(frames)).save(
        style.FIG_DIR / "06_torus_gas.gif", writer=PillowWriter(fps=12), dpi=70)
    plt.close(fig)
    print("saved figures/06_torus_gas.gif")


def main():
    style.apply()
    m, n = mean_wait()
    print(f"N = 2: mean wait between returns = {m:.3f} looks over {n} returns (Kac: 4)")
    first = fig_idea()
    print(f"first return to 'both on the left' at look {first}")
    fig_dimensions()
    gif_gas()


if __name__ == "__main__":
    main()
