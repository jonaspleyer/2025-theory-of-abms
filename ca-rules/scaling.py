import matplotlib.pyplot as plt
import numpy as np


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
        return None


def neumann_dDim_kStep(n, d, k):
    return None


def exponential(n):
    return 2**n


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8, 8))

    x = np.arange(20)

    ax.plot(x, moore_1d(x), label="$1D$", c="k")
    # ax.plot(x, moore_dDim_kStep(x, 1, 2), label="$1D$ $2$-step", c="darkmagenta")
    for i in range(2, 4):
        ax.plot(
            x,
            moore_dDim(x, i),
            label=f"${i}D$ Moore",
            c="k",
            linestyle=(0, (1, 10 - 3 * i)),
        )
    for i in range(2, 3):
        ax.plot(
            x,
            neumann_dDim(x, i),
            label=f"${i}D$ Neumann",
            c="k",
            linestyle=(0, (5, 10 - 3 * i)),
        )

    ax.plot(x, exponential(x), label="Exponential $2^n$", c="coral")

    ax.set_yscale("log")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Living Cells")
    ax.legend()

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.10),
        ncol=5,
        frameon=False,
    )
    ax.grid(True, which="major", linestyle="-", linewidth=0.75, alpha=0.25)
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle="-", linewidth=0.25, alpha=0.15)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig("ca-rules/ca-scaling.pdf")
