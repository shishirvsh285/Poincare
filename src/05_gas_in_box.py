"""
MAIN NUMERICAL CASE: a gas in a box, and how long it takes to "un-mix".

Setup
  N non-interacting particles in a square box of side 1, bouncing off the
  walls (elastic). All start in the LEFT half. We watch them spread out
  and ask: when are they all back in the left half?

Why this is a Poincare system
  Each particle's x-motion is a bounce between walls. Unfold the bounce and
  it becomes a point running round a circle of length 2:
      theta(t) = theta0 + v t  (mod 2),     x = theta if theta < 1 else 2 - theta
  So the full x-state is a point on an N-dimensional torus, moving in a
  straight line. That flow preserves volume and the torus is finite, so
  Poincare says the gas MUST come back to the left half, again and again.

What we measure (the prediction we test)
  Look at the box once per time step. Let A = "all N particles in the left
  half". A takes up a fraction mu(A) = (1/2)^N of the torus. Kac's lemma
  (the quantitative version of Poincare) says the AVERAGE number of steps
  between visits to A is exactly

      <T> = 1 / mu(A) = 2^N.

  We simulate long runs, measure <T> for N = 1..14, and compare.

Outputs
  figures/05_gas_snapshots.png   the box at a few moments, ending at a return
  figures/05_left_fraction.png   fraction of particles on the left vs time, N=10 vs N=40
  figures/05_kac_scaling.png     measured mean return time vs 2^N
  figures/05_gas.gif             animation of the spread and the return
  figures/05_results.csv         the numbers behind the Kac plot
"""
import csv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

import style

DT = 1.0                 # we look at the box once per unit of time
RNG_SEED = 7


# ---------------------------------------------------------------- physics
def bounce(theta):
    """Unfolded coordinate on a circle of length 2 -> position in the box [0, 1]."""
    th = theta % 2.0
    return np.where(th < 1.0, th, 2.0 - th)


def make_gas(n, rng):
    """Random start with everyone in the left half, Maxwell-like random velocities."""
    x0 = rng.uniform(0, 0.5, n)
    y0 = rng.uniform(0, 1.0, n)
    vx = rng.normal(0, 1, n)
    vy = rng.normal(0, 1, n)
    return x0, y0, vx, vy


def positions(x0, y0, vx, vy, t):
    t = np.atleast_1d(t)[:, None]
    return bounce(x0 + vx * t), bounce(y0 + vy * t)


def visits_to_left_half(x0, vx, n_steps, chunk=1_000_000):
    """Step indices k (k >= 1) at which ALL particles have x < 1/2."""
    hits = []
    for start in range(1, n_steps + 1, chunk):
        k = np.arange(start, min(start + chunk, n_steps + 1))
        x = bounce(x0[None, :] + vx[None, :] * (k[:, None] * DT))
        hits.append(k[np.all(x < 0.5, axis=1)])
    return np.concatenate(hits)


# ---------------------------------------------------------------- figures
def draw_box(ax, x, y, t, highlight=False):
    ax.add_patch(Rectangle((0, 0), 0.5, 1, fc=style.BLUE, alpha=0.08, lw=0))
    ax.axvline(0.5, color=style.MUTED, lw=1, ls=":")
    left = x < 0.5
    ax.scatter(x[left], y[left], s=60, color=style.BLUE, edgecolor="white", lw=0.8, zorder=3)
    ax.scatter(x[~left], y[~left], s=60, color=style.ORANGE, edgecolor="white", lw=0.8, zorder=3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(3 if highlight else 1.5)
        sp.set_color(style.GREEN if highlight else style.INK)
    ax.set_title(f"t = {t:g}" + ("   all back!" if highlight else ""),
                 color=style.GREEN if highlight else style.INK, fontsize=13)


def fig_snapshots(rng):
    n = 10
    x0, y0, vx, vy = make_gas(n, rng)
    k_ret = int(visits_to_left_half(x0, vx, 200_000)[0])
    print(f"[snapshots] N={n}: first return to the left half at step {k_ret} (Kac average 2^{n} = {2**n})")
    times = [0, 0.5, 2, 30, k_ret]
    fig, axes = plt.subplots(1, len(times), figsize=(3.0 * len(times), 3.3))
    for ax, t in zip(axes, times):
        x, y = positions(x0, y0, vx, vy, t)
        draw_box(ax, x[0], y[0], t, highlight=(t == k_ret))
    fig.suptitle(f"{n} particles start in the left half. They spread out. "
                 f"After {k_ret} looks, they are all back on the left.",
                 fontsize=14, weight="bold", y=1.03)
    style.save(fig, "05_gas_snapshots.png")
    return (x0, y0, vx, vy), k_ret


def fig_left_fraction(rng):
    t = np.arange(0, 6001) * DT
    fig, axes = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True)
    for ax, n, col in zip(axes, (10, 40), (style.BLUE, style.PURPLE)):
        x0, _, vx, _ = make_gas(n, rng)
        x = bounce(x0[None, :] + vx[None, :] * t[:, None])
        frac = np.mean(x < 0.5, axis=1)
        ax.plot(t, frac, lw=0.5, color=col)
        back = np.nonzero(frac[1:] == 1.0)[0] + 1
        ax.plot(t[back], frac[back], "v", color=style.GREEN, ms=8)
        ax.axhline(0.5, color=style.MUTED, lw=1, ls=":")
        ax.set_ylim(0, 1.12)
        ax.set_ylabel("fraction on left")
        msg = (f"N = {n}: {len(back)} returns (green) in {len(t)-1} looks"
               if len(back) else f"N = {n}: no return in {len(t)-1} looks "
                                 f"(expected wait about $2^{{{n}}} \\approx 10^{{{int(round(n*np.log10(2)))}}}$)")
        ax.set_title(msg, loc="left", fontsize=13)
    axes[-1].set_xlabel("time (number of looks)")
    fig.tight_layout()
    style.save(fig, "05_left_fraction.png")


def fig_kac(rng):
    Ns = np.arange(1, 15)
    rows = []
    for n in Ns:
        x0, _, vx, _ = make_gas(n, rng)
        n_steps = int(min(4000 * 2.0**n, 6e7))
        hits = visits_to_left_half(x0, vx, n_steps)
        gaps = np.diff(hits)
        mean = gaps.mean()
        err = gaps.std(ddof=1) / np.sqrt(len(gaps))
        rows.append((int(n), len(gaps), mean, err, 2.0**n))
        print(f"N={n:2d}  returns={len(gaps):7d}  mean gap={mean:10.1f} +/- {err:7.1f}   Kac 2^N={2**n}")

    with open(style.FIG_DIR / "05_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["N", "returns_counted", "mean_return_steps", "std_error", "kac_prediction"])
        w.writerows(rows)

    r = np.array(rows)
    fig, ax = plt.subplots(figsize=(7.6, 5))
    nn = np.linspace(1, 14, 100)
    ax.semilogy(nn, 2.0**nn, color=style.ORANGE, lw=2.5, label="Kac's prediction $2^N$", zorder=1)
    ax.errorbar(r[:, 0], r[:, 2], yerr=r[:, 3], fmt="o", ms=8, color=style.BLUE,
                capsize=3, label="our simulation", zorder=2)
    ax.set_xlabel("number of particles $N$")
    ax.set_ylabel("mean wait between returns (looks)")
    ax.set_title("Waiting time doubles with every particle")
    ax.legend(loc="upper left")
    ax.set_xticks(Ns)
    style.save(fig, "05_kac_scaling.png")

    # The punchline numbers
    ms_per_look = 1e-3
    year = 3.156e7
    for n in (100, 1000):
        yrs = 2.0**n * ms_per_look / year
        print(f"N={n}: 2^N looks at one per millisecond = {yrs:.2e} years "
              f"= {yrs/1.38e10:.1e} x age of universe")
    return rows


def gif_gas(gas, k_ret):
    x0, y0, vx, vy = gas
    early = np.linspace(0, 6, 60)
    late = np.linspace(k_ret - 6, k_ret, 60)
    times = list(early) + [None] * 6 + list(late) + [k_ret] * 12
    fig, ax = plt.subplots(figsize=(4.2, 4.5))

    def update(i):
        ax.clear()
        t = times[i]
        if t is None:
            ax.text(0.5, 0.5, f"... fast forward\nto t = {k_ret - 6:g} ...", ha="center",
                    va="center", fontsize=15, transform=ax.transAxes)
            ax.set_xticks([]), ax.set_yticks([])
            return
        x, y = positions(x0, y0, vx, vy, t)
        draw_box(ax, x[0], y[0], round(t, 1), highlight=bool(np.all(x[0] < 0.5) and t > 1))

    anim = FuncAnimation(fig, update, frames=len(times))
    anim.save(style.FIG_DIR / "05_gas.gif", writer=PillowWriter(fps=12), dpi=80)
    plt.close(fig)
    print("saved figures/05_gas.gif")


def main():
    style.apply()
    rng = np.random.default_rng(RNG_SEED)
    gas, k_ret = fig_snapshots(rng)
    fig_left_fraction(rng)
    fig_kac(rng)
    gif_gas(gas, k_ret)


if __name__ == "__main__":
    main()
