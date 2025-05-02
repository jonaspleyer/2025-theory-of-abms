import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))

data = np.loadtxt("data.csv", dtype=int, delimiter=",")

ax.plot(data[:, 0], label="Prey")
ax.plot(data[:, 1], label="Predator")

ax.legend()

fig.savefig("pred-prey.pdf")
