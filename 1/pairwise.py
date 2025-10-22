import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

base_dir = "./"
selected_indices = [str(i) for i in range(1, 34)]
directories_sorted = sorted([d for d in os.listdir(base_dir) if d in selected_indices], key=int)
labels = [f"State {i}" for i in range(1, 34)]
pb_total_col = 18

for idx, directory in enumerate(directories_sorted):
    label = labels[idx]
    pairwise_file = os.path.join(base_dir, directory, "FINAL_PAIRWISE.dat")

    in_complex = False
    in_total_energy = False
    interaction_matrix = defaultdict(dict)

    with open(pairwise_file, "r") as f:
        for line in f:
            if "Complex:" in line:
                in_complex = True
                continue
            if in_complex and "Total Energy Decomposition" in line:
                in_total_energy = True
                continue
            if in_total_energy and line.strip().startswith("Resid 1"):
                continue
            if in_total_energy and line.strip() == "":
                break
            if in_total_energy:
                try:
                    cols = line.strip().split(",")
                    res1 = cols[0].strip()
                    res2 = cols[1].strip()
                    energy = float(cols[pb_total_col].strip())
                    res1_num = f"{res1.split()[-1]}"
                    res2_num = f"{res2.split()[-1]}"
                    interaction_matrix[res1_num][res2_num] = energy
                    interaction_matrix[res2_num][res1_num] = energy
                except (ValueError, IndexError):
                    continue

    residues = sorted([int(r) for r in interaction_matrix.keys()])
    residues = [str(r) for r in residues]
    matrix = pd.DataFrame(index=residues, columns=residues, dtype=float)

    for i in residues:
        for j in residues:
            matrix.loc[i, j] = interaction_matrix.get(i, {}).get(j, 0.0)

    plt.figure(figsize=(14, 12), dpi=200)
    ax = sns.heatmap(
        matrix.astype(float),
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        linecolor="gray",
        square=True,
        cbar_kws={"label": "Interaction Energy (kcal/mol)"}
    )

    ax.set_xticks(np.arange(0, len(residues), 20))
    ax.set_yticks(np.arange(0, len(residues), 20))
    ax.set_xticklabels(residues[::20], rotation=90, fontsize=10)
    ax.set_yticklabels(residues[::20], fontsize=10)

    ax.set_title(f"PB Pairwise Energy Heatmap - {label}", fontsize=18, fontweight='_

