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
    fig, ax = plt.subplots()

    x = np.arange(30)

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
        if i < 3:
            ax.plot(
                x,
                neumann_dDim(x, i),
                label=f"${i}D$ von Neumann",
                c="k",
                linestyle=(0, (5, 10 - 3 * i)),
            )
    # ax.plot(x, moore_1d(x), label="Moore $1D$", c="darkslateblue", linestyle="--")
    # ax.plot(x, moore_2d(x), label="Moore $2D$", c="darkslateblue", linestyle="-:")
    # ax.plot(x, moore_dDim(x, 3), label="Moore $3D$", c="darkslateblue")
    # ax.plot(
    #     x, moore_dDim_kStep(x, 2, 2), label="Moore $2D$ $2$-step", c="darkslateblue"
    # )
    # ax.plot(
    #     x, moore_dDim_kStep(x, 3, 2), label="Moore $3D$ $2$-step", c="darkslateblue"
    # )

    # ax.plot(x, neumann_2d(x), label="Moore $3D$ $2$-step")

    ax.plot(x, exponential(x), label="Exponential $2^n$", c="darkslateblue")
    ax.plot(x, logistic(x), label="Exponential $2^n$", c="darkslateblue")

    ax.set_yscale("log")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Living Cells")
    ax.legend()

    plt.show()
