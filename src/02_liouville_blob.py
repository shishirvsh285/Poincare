"""
Why Hamiltonian systems obey the theorem: Liouville's theorem, seen directly.

We fill a small disk of initial conditions in the (q, p) plane of a pendulum

    H = p^2 / 2 - cos q,     dq/dt = p,   dp/dt = -sin q

and let every point move. The blob stretches into a thin swirl, but its
AREA never changes. Then we add friction (dp/dt = -sin q - gamma p).
Now the area shrinks like exp(-gamma t), every blob falls to the bottom,
and nothing ever comes back. No area conservation, no recurrence.

Outputs
  figures/02_liouville_blobs.png     snapshots, frictionless vs damped
  figures/02_area_vs_time.png        measured area against theory
  figures/02_liouville.gif           animation (for the live/HTML deck)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

import style

CENTER = np.array([0.0, 1.55])   # (q, p), sits just inside the separatrix p = 2 at q = 0
RADIUS = 0.45
GAMMA = 0.25                     # friction for the damped case
N_EDGE = 20000                   # points on the blob's boundary (for the area)
N_FILL = 6000                    # points inside (for the picture)
T_SNAP = [0.0, 3.0, 6.0, 12.0]
T_END = 12.0


def rhs(gamma):
    def f(t, y):
        n = y.size // 2
        q, p = y[:n], y[n:]
        return np.concatenate([p, -np.sin(q) - gamma * p])
    return f


def blob_points(rng):
    th = np.linspace(0, 2 * np.pi, N_EDGE, endpoint=False)
    edge = CENTER + RADIUS * np.column_stack([np.cos(th), np.sin(th)])
    ang = rng.uniform(0, 2 * np.pi, N_FILL)
    rad = RADIUS * np.sqrt(rng.uniform(0, 1, N_FILL))
    fill = CENTER + np.column_stack([rad * np.cos(ang), rad * np.sin(ang)])
    return edge, fill


def evolve(points, gamma, t_eval):
    y0 = np.concatenate([points[:, 0], points[:, 1]])
    sol = solve_ivp(rhs(gamma), (0, t_eval[-1]), y0, t_eval=t_eval,
                    method="DOP853", rtol=1e-10, atol=1e-12)
    n = points.shape[0]
    return sol.y[:n].T, sol.y[n:].T          # shape (len(t), n)


def shoelace(q, p):
    return 0.5 * abs(np.dot(q, np.roll(p, -1)) - np.dot(p, np.roll(q, -1)))


def wrap(q):
    return (q + np.pi) % (2 * np.pi) - np.pi


def phase_portrait(ax):
    qg, pg = np.meshgrid(np.linspace(-np.pi, np.pi, 400), np.linspace(-3, 3, 400))
    H = 0.5 * pg**2 - np.cos(qg)
    ax.contour(qg, pg, H, levels=np.linspace(-0.9, 3, 12), colors="#d1d5db", linewidths=0.7,
               negative_linestyles="solid")
    ax.contour(qg, pg, H, levels=[1.0], colors=style.MUTED, linewidths=1.2, linestyles="--")


def main():
    style.apply()
    rng = np.random.default_rng(0)
    edge, fill = blob_points(rng)
    A0 = np.pi * RADIUS**2

    t_area = np.linspace(0, T_END, 61)
    results = {}
    for gamma in (0.0, GAMMA):
        eq, ep = evolve(edge, gamma, t_area)
        fq, fp = evolve(fill, gamma, np.array(T_SNAP) if T_SNAP[0] > 0 else np.array(T_SNAP))
        areas = np.array([shoelace(eq[i], ep[i]) for i in range(len(t_area))])
        results[gamma] = dict(fq=fq, fp=fp, areas=areas)
        print(f"gamma={gamma}: area at t=0 {areas[0]:.5f}, at t={T_END} {areas[-1]:.5f}, "
              f"theory {A0*np.exp(-gamma*T_END):.5f}")

    # ---- snapshots ----
    fig, axes = plt.subplots(2, len(T_SNAP), figsize=(15, 7.4), sharex=True, sharey=True)
    for row, gamma in enumerate((0.0, GAMMA)):
        r = results[gamma]
        colour = style.BLUE if gamma == 0 else style.RED
        for col, t in enumerate(T_SNAP):
            ax = axes[row, col]
            phase_portrait(ax)
            i = int(np.argmin(np.abs(np.array(T_SNAP) - t)))
            ax.scatter(wrap(r["fq"][i]), r["fp"][i], s=0.8, color=colour, linewidths=0)
            ia = int(np.argmin(np.abs(t_area - t)))
            ax.set_title(f"$t = {t:g}$    area $= {r['areas'][ia]:.3f}$", fontsize=12.5)
            ax.set_xlim(-np.pi, np.pi)
            ax.set_ylim(-3, 3)
            ax.set_xticks([-np.pi, 0, np.pi], ["$-\\pi$", "0", "$\\pi$"])
            if col == 0:
                ax.set_ylabel("$p$")
            if row == 1:
                ax.set_xlabel("$q$")
    fig.text(0.005, 0.73, "No friction\n(Hamiltonian)", rotation=90, va="center", ha="left",
             fontsize=14, weight="bold", color=style.BLUE)
    fig.text(0.005, 0.29, f"With friction\n($\\gamma = {GAMMA}$)", rotation=90, va="center", ha="left",
             fontsize=14, weight="bold", color=style.RED)
    fig.suptitle("A blob of pendulums: it may stretch, but without friction its area stays fixed",
                 fontsize=16, weight="bold")
    fig.tight_layout(rect=(0.03, 0, 1, 0.96))
    style.save(fig, "02_liouville_blobs.png")

    # ---- compact 2 x 3 version for the slide ----
    t_slide = [0.0, 6.0, 12.0]
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 6.6), sharex=True, sharey=True)
    for row, gamma in enumerate((0.0, GAMMA)):
        r = results[gamma]
        colour = style.BLUE if gamma == 0 else style.RED
        for col, t in enumerate(t_slide):
            ax = axes[row, col]
            phase_portrait(ax)
            i = T_SNAP.index(t)
            ax.scatter(wrap(r["fq"][i]), r["fp"][i], s=1.0, color=colour, linewidths=0)
            ia = int(np.argmin(np.abs(t_area - t)))
            ax.set_title(f"$t={t:g}$, area $={r['areas'][ia]:.3f}$", fontsize=13, color=colour)
            ax.set_xlim(-np.pi, np.pi)
            ax.set_ylim(-3, 3)
            ax.set_xticks([])
            ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_visible(True)
                sp.set_color("#9ca3af")
    axes[0, 0].set_ylabel("no friction", fontsize=15, color=style.BLUE, weight="bold")
    axes[1, 0].set_ylabel("with friction", fontsize=15, color=style.RED, weight="bold")
    fig.tight_layout(h_pad=1.2, w_pad=0.6)
    style.save(fig, "02_liouville_slide.png")

    # ---- area vs time ----
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(t_area, results[0.0]["areas"] / A0, "o", ms=4, color=style.BLUE, label="no friction (measured)")
    ax.axhline(1.0, color=style.BLUE, lw=1, alpha=0.5)
    ax.plot(t_area, results[GAMMA]["areas"] / A0, "o", ms=4, color=style.RED, label="friction (measured)")
    ax.plot(t_area, np.exp(-GAMMA * t_area), color=style.RED, lw=1.5, alpha=0.7,
            label=f"theory $e^{{-\\gamma t}}$")
    ax.set_xlabel("time $t$")
    ax.set_ylabel("area / starting area")
    ax.set_ylim(0, 1.15)
    ax.legend(loc="center right")
    ax.set_title("Liouville's theorem, checked numerically")
    style.save(fig, "02_area_vs_time.png")

    # ---- gif (frictionless only) ----
    t_gif = np.linspace(0, T_END, 90)
    gq, gp = evolve(fill, 0.0, t_gif)
    fig, ax = plt.subplots(figsize=(5.5, 5.2))
    phase_portrait(ax)
    sc = ax.scatter(wrap(gq[0]), gp[0], s=1.2, color=style.BLUE, linewidths=0)
    ttl = ax.set_title("")
    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("$q$")
    ax.set_ylabel("$p$")

    def update(k):
        sc.set_offsets(np.column_stack([wrap(gq[k]), gp[k]]))
        ttl.set_text(f"pendulum phase space, t = {t_gif[k]:.1f}")
        return sc, ttl

    anim = FuncAnimation(fig, update, frames=len(t_gif), blit=False)
    anim.save(style.FIG_DIR / "02_liouville.gif", writer=PillowWriter(fps=15), dpi=80)
    plt.close(fig)
    print("saved figures/02_liouville.gif")


if __name__ == "__main__":
    main()
