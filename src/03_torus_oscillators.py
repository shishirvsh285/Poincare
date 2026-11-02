"""
Example 1: two uncoupled oscillators with an irrational frequency ratio.

    H = (p1^2 + w1^2 x1^2)/2 + (p2^2 + w2^2 x2^2)/2,   w2 / w1 = golden ratio

Each oscillator keeps its own energy, so the state lives on a 2-torus
labelled by two phase angles (theta1, theta2) = (w1 t, w2 t). Because the
ratio is irrational the motion never exactly repeats. Yet it keeps coming
back as close as we like to where it started. That is Poincare recurrence
in its friendliest form.

Outputs
  figures/03_torus.png              trajectory winding on a doughnut
  figures/03_distance.png           distance from the start vs time, with returns
  figures/03_return_scaling.png     how the return time grows as we ask for a closer return
"""
import numpy as np
import matplotlib.pyplot as plt

import style

PHI = (1 + 5**0.5) / 2
W = np.array([1.0, PHI])


def torus_distance(theta, theta0):
    d = (theta - theta0 + np.pi) % (2 * np.pi) - np.pi
    return np.sqrt(np.sum(d**2, axis=-1))


def mean_return_time(omegas, eps, t_total, chunk=2_000_000):
    """Average time between visits to the eps-ball around the start.

    We run for a long time and count how many times the phase point ENTERS
    the ball. Mean return time = total time / number of entries.
    """
    dt = eps / 6
    entries, inside_prev, t0 = 0, True, 0.0
    while t0 < t_total:
        t = t0 + dt * np.arange(chunk)
        inside = torus_distance(np.outer(t, omegas), 0.0) < eps
        prev = np.concatenate([[inside_prev], inside[:-1]])
        entries += np.count_nonzero(inside & ~prev)
        inside_prev = inside[-1]
        t0 = t[-1] + dt
    return t0 / entries if entries else np.nan


def theory_return_time(omegas, eps):
    """Flux argument: torus volume / (speed x cross-section of the eps-ball)."""
    n = len(omegas)
    speed = np.linalg.norm(omegas)
    cross = 2 * eps if n == 2 else np.pi * eps**2      # 1D 'diameter' or 2D disk
    return (2 * np.pi) ** n / (speed * cross)


def draw_torus(ax, t_end=60):
    R, r = 3.0, 1.1
    elev, azim = 38, -60
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 80), np.linspace(0, 2 * np.pi, 40))
    X = (R + r * np.cos(v)) * np.cos(u)
    Y = (R + r * np.cos(v)) * np.sin(u)
    Z = r * np.sin(v)
    ax.plot_surface(X, Y, Z, color="#dbe3f0", alpha=0.55, linewidth=0, shade=True, zorder=1)

    t = np.linspace(0, t_end, 8000)
    th1, th2 = W[0] * t, W[1] * t
    x = (R + r * np.cos(th2)) * np.cos(th1)
    y = (R + r * np.cos(th2)) * np.sin(th1)
    z = r * np.sin(th2)
    # crude depth cue: is the surface normal pointing at the camera?
    e, a = np.radians(elev), np.radians(azim)
    view = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    normal = np.stack([np.cos(th2) * np.cos(th1), np.cos(th2) * np.sin(th1), np.sin(th2)])
    front = view @ normal > 0
    xb, yb, zb = (np.where(front, np.nan, c) for c in (x, y, z))
    xf, yf, zf = (np.where(front, c, np.nan) for c in (x, y, z))
    ax.plot(xb, yb, zb, color=style.BLUE, lw=0.8, alpha=0.25, zorder=2)
    ax.plot(xf, yf, zf, color=style.BLUE, lw=1.3, alpha=0.95, zorder=3)
    ax.scatter([R + r], [0], [0], s=90, color=style.ORANGE, zorder=10, depthshade=False)
    ax.set_box_aspect((1, 1, 0.38), zoom=1.35)
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)
    ax.computed_zorder = False


def draw_unfolded(ax, t_end=60):
    t = np.linspace(0, t_end, 20000)
    th = (np.outer(t, W)) % (2 * np.pi)
    jump = np.any(np.abs(np.diff(th, axis=0)) > np.pi, axis=1)
    th = th.copy()
    th[1:][jump] = np.nan
    ax.plot(th[:, 0], th[:, 1], color=style.BLUE, lw=1.0)
    ax.plot([0], [0], "o", ms=11, color=style.ORANGE, clip_on=False, zorder=5)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 2 * np.pi)
    ax.set_aspect("equal")
    ticks = [0, np.pi, 2 * np.pi]
    labels = ["0", "$\\pi$", "$2\\pi$"]
    ax.set_xticks(ticks, labels)
    ax.set_yticks(ticks, labels)
    ax.set_xlabel("phase of oscillator 1, $\\theta_1$")
    ax.set_ylabel("phase of oscillator 2, $\\theta_2$")
    for sp in ax.spines.values():
        sp.set_visible(True)


def main():
    style.apply()

    # ---- torus picture: doughnut + the same thing cut open ----
    fig = plt.figure(figsize=(12, 5.0))
    ax3 = fig.add_subplot(1, 2, 1, projection="3d")
    draw_torus(ax3)
    ax3.set_title("on the doughnut")
    ax2 = fig.add_subplot(1, 2, 2)
    draw_unfolded(ax2)
    ax2.set_title("cut open into a square")
    style.save(fig, "03_torus.png")

    # ---- distance from start ----
    t = np.linspace(0, 400, 400_000)
    d = torus_distance(np.outer(t, W), 0.0)
    eps = 0.15
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(t, d, lw=0.6, color=style.BLUE)
    ax.axhline(eps, color=style.ORANGE, lw=1.5, ls="--")
    ax.text(402, eps, f"  $\\varepsilon = {eps}$", color=style.ORANGE, va="center")
    close = d < eps
    starts = np.nonzero(close & ~np.roll(close, 1))[0]
    ax.plot(t[starts[1:]], d[starts[1:]], "v", color=style.ORANGE, ms=9)
    ax.set_xlim(0, 400)
    ax.set_xlabel("time $t$  (units of $1/\\omega_1$)")
    ax.set_ylabel("distance from start")
    ax.set_title("It keeps coming back: every orange marker is a return within $\\varepsilon$")
    style.save(fig, "03_distance.png")
    print(f"returns within eps={eps} up to t=400: {len(starts) - 1}")

    # ---- return-time scaling with eps (2 and 3 oscillators) ----
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    configs = [
        (np.array([1.0, PHI]), np.geomspace(0.4, 0.01, 7), style.BLUE, "2 oscillators", 1, 1.5e5),
        (np.array([1.0, PHI, 2**0.5]), np.geomspace(0.5, 0.08, 6), style.GREEN, "3 oscillators", 2, 1.5e6),
    ]
    for om, epss, col, lab, slope, t_total in configs:
        T = np.array([mean_return_time(om, e, t_total) for e in epss])
        Th = theory_return_time(om, epss)
        print(lab, "measured", np.round(T, 1), "theory", np.round(Th, 1))
        ax.loglog(epss, T, "o", color=col, label=f"{lab} (simulated)", ms=7)
        ax.loglog(epss, Th, "-", color=col, alpha=0.6, label=f"theory $\\propto \\varepsilon^{{-{slope}}}$")
    ax.invert_xaxis()
    ax.set_xlabel("how close we demand: $\\varepsilon$")
    ax.set_ylabel("mean return time $T$")
    ax.set_title("Each extra oscillator costs a factor $1/\\varepsilon$")
    ax.legend(fontsize=11)
    style.save(fig, "03_return_scaling.png")


if __name__ == "__main__":
    main()
