"""Shared plot style so every figure in the deck looks like it came from one team."""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

FIG_DIR = Path(__file__).resolve().parent.parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

# A small, high-contrast palette that survives a washed-out projector.
INK = "#1b1f2a"
MUTED = "#6b7280"
BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
PURPLE = "#7c3aed"
RED = "#dc2626"
PALETTE = [BLUE, ORANGE, GREEN, PURPLE, RED]


def apply():
    mpl.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.family": "DejaVu Sans",
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.labelsize": 13,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "legend.frameon": False,
        "mathtext.fontset": "cm",
    })


def save(fig, name):
    path = FIG_DIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"saved {path.relative_to(FIG_DIR.parent)}")
    return path
