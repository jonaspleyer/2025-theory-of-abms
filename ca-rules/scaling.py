import matplotlib.pyplot as plt
import numpy as np

COLOR1 = "#e8702a"
COLOR2 = "#ffbe4f"
COLOR3 = "#6bd2db"
COLOR4 = "#0ea7b5"
COLOR5 = "#0c457d"


def moore_1d(n):
    return 2 * n + 1


def moore_2d(n):
    return (2 * n + 1) ** 2


def moore_dDim(n, d):
    return (2 * n + 1) ** d


def moore_dDim_kStep(n, d, k):
    return (2 * n * k + 1) ** d


def neumann_2d(n):
    return 2 * n * (n + 1) + 1


def neumann_dDim(n, d):
    if d == 1:
        return moore_1d(n)
    if d == 2:
        return neumann_2d(n)
    else:
        return 1 + 2 * np.sum([neumann_dDim(k, d - 1) for k in np.arange(1, n + 1)])


def neumann_dDim_kStep(n, d, k):
    return None


def exponential(n):
    return 2**n


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Courier New",  # monospace font
            "font.size": 14,
            "axes.titlesize": 14,
            "axes.labelsize": 14,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
            "figure.titlesize": 14,
        }
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    x = np.arange(20)

    linestyles = ["-", "-", "--", ":", "-."]
    ax.plot(x, moore_dDim(x, 3), label="3D Moore", c=COLOR1, linestyle="-")
    ax.plot(
        x,
        [neumann_dDim(xi, 3) for xi in x],
        label="3D von Neumann",
        c=COLOR5,
        linestyle="-",
    )
    ax.plot(x, moore_2d(x), label="2D Moore", c=COLOR1, linestyle="--")
    ax.plot(x, neumann_2d(x), label="2D von Neumann", c=COLOR5, linestyle="--")
    ax.plot(x, moore_1d(x), label="1D", c=COLOR1, linestyle=":")
    ax.plot(x, exponential(x), label="Exponential $2^n$", c=COLOR4)

    ax.set_yscale("log")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Living Cells")
    ax.legend()

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=3,
        frameon=False,
    )
    ax.grid(True, which="major", linestyle="-", linewidth=0.75, alpha=0.25)
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle="-", linewidth=0.25, alpha=0.15)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig("ca-rules/ca-scaling.pdf")
