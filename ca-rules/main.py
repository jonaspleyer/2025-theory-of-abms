import numpy as np
from typing import Generator
from pathlib import Path
from tqdm import tqdm
from PIL import Image


def ca_rule_generator() -> Generator[np.ndarray]:
    rule_base = np.zeros((2, 2, 2), dtype=int)

    for a8 in range(2):
        for b in range(2):
            for a6 in range(2):
                for c in range(2):
                    for a3 in range(2):
                        new_rule = np.array(rule_base)
                        new_rule[1, 1, 1] = a8
                        new_rule[1, 1, 0] = b
                        new_rule[1, 0, 1] = a6
                        new_rule[1, 0, 0] = c
                        new_rule[0, 1, 1] = b
                        new_rule[0, 1, 0] = a3
                        new_rule[0, 0, 1] = c
                        new_rule[0, 0, 0] = 0
                        yield new_rule


def update_ca(x: np.ndarray, rule: np.ndarray) -> np.ndarray:
    # Check the length of the array
    y = np.zeros(x.shape, dtype=int)
    for i in range(0, x.shape[0] - 2):
        q = rule[x[i], x[i + 1], x[i + 2]]
        y[i + 1] = q
        if q == 1 and (i == 0 or i == x.shape[0] - 3):
            raise ValueError("Exceeded bounds")
    if np.all(y == x):
        raise ValueError("Encountered Duplicate")
    return y


def generate_rule_name(rule):
    binary = np.array(
        [
            rule[1, 1, 1],
            rule[1, 1, 0],
            rule[1, 0, 1],
            rule[1, 0, 0],
            rule[0, 1, 1],
            rule[0, 1, 0],
            rule[0, 0, 1],
            rule[0, 0, 0],
        ]
    )
    decimal = np.sum(2 ** (np.arange(8)[::-1]) * np.array(binary))
    return "".join([str(b) for b in binary]), f"{decimal:03}"


def compute_rule(rule, start: np.ndarray, folder: Path):
    (n_grid_x,) = start.shape
    n_grid_y = n_grid_x
    total = np.zeros((n_grid_y, n_grid_x), dtype=int)
    total[0] = start

    x = start
    n = 0
    for n in range(1, n_grid_y):
        try:
            x = update_ca(x, rule)
            total[n] = x
        except ValueError:
            break
    x_low = np.min(np.where(np.any(total > 0, axis=0)))
    x_high = np.max(np.where(np.any(total > 0, axis=0)))
    total = total[0:n, x_low - 2 : x_high + 2]
    return total


def save_rule(total, rules, folder: Path):
    names = [generate_rule_name(r)[1] for r in rules]
    name = "-".join(names)
    if np.sum(total[1:]) > 0 and np.any(total[1] != total[0]):
        folder.mkdir(parents=True, exist_ok=True)
        img = Image.fromarray(255 * total.astype(np.uint8))
        img.save(folder / f"rule-{name}.pdf", dpi=(300, 300))
        img.save(folder / f"rule-{name}.png", dpi=(300, 300))


def plot_rules(
    rules,
    start,
    folder,
    n_rules: int | None,
):
    imgs_rules = []
    for rule in tqdm(rules, total=n_rules):
        img = compute_rule(rule, start, folder)
        for i, saved_rules in imgs_rules:
            if i.shape == img.shape and np.all(i == img):
                saved_rules.append(rule)
                break
        else:
            imgs_rules.append((img, [rule]))

    for img, saved_rules in imgs_rules:
        save_rule(img, saved_rules, folder)


if __name__ == "__main__":
    # Plot Single1 Histories
    n_grid_x = 450
    start = np.zeros(n_grid_x, dtype=int)
    start[5 * 45] = 1

    plot_rules(ca_rule_generator(), start, Path("single1"), 32)

    # Plot Double1 Histories
    n_grid_x = 450
    start = np.zeros(n_grid_x, dtype=int)
    start[5 * 30] = 1
    start[5 * 60] = 1

    plot_rules(ca_rule_generator(), start, Path("double1-spaced"), 32)

    # Plot Double1 Histories
    n_grid_x = 450
    start = np.zeros(n_grid_x, dtype=int)
    start[5 * 45 - 1] = 1
    start[5 * 45 + 1] = 1

    plot_rules(ca_rule_generator(), start, Path("double1-close"), 32)

    # Plot alternating
    n_gridx = 450
    start = np.zeros(n_grid_x, dtype=int)
    start[5 * 30 : 5 * 60][::2] = 1

    plot_rules(ca_rule_generator(), start, Path("alternating"), 32)
