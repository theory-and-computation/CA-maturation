import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

base_dir = "./"
selected_indices = [str(i) for i in range(1, 34)]
directories_sorted = sorted([d for d in os.listdir(base_dir) if d in selected_indices], key=int)
labels = [f"State {i}" for i in range(1, 34)]
pb_total_col = 17

output_dir = "tmp"
os.makedirs(output_dir, exist_ok=True)

sum_matrix = None
count_matrix = None
residues_union = set()

for idx, directory in enumerate(directories_sorted):
    label = labels[idx]
    pairwise_file = os.path.join(base_dir, directory, "FINAL_PAIRWISE.dat")
    if not os.path.isfile(pairwise_file):
        continue

    in_pb = False
    in_complex = False
    in_total_energy = False
    interaction_matrix = defaultdict(dict)

    with open(pairwise_file, "r") as f:
        for line in f:
            if "Poisson Boltzmann solvent" in line:
                in_pb = True
                continue
            if in_pb and "Complex:" in line:
                in_complex = True
                continue
            if in_pb and in_complex and "Total Energy Decomposition" in line:
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
                    residues_union.update([res1_num, res2_num])
                except (ValueError, IndexError):
                    continue

    residues = sorted([int(r) for r in interaction_matrix.keys()])
    residues = [str(r) for r in residues]
    matrix = pd.DataFrame(index=residues, columns=residues, dtype=float)

    for i in residues:
        for j in residues:
            matrix.loc[i, j] = interaction_matrix.get(i, {}).get(j, 0.0)

    matrix = matrix.astype(float)

    if sum_matrix is None:
        sum_matrix = matrix.copy()
        count_matrix = (~matrix.isna()).astype(int)
    else:
        sum_matrix = sum_matrix.add(matrix, fill_value=0)
        count_matrix = count_matrix.add((~matrix.isna()).astype(int), fill_value=0)

    fig, ax = plt.subplots(figsize=(16, 16))
    for spine in ax.spines.values():
        spine.set_visible(False)

    sns_heat = sns.heatmap(
        matrix,
        cmap="coolwarm",
        center=0,
        vmin=-0.25,
        vmax=0.25,
        linewidths=0,
        square=True,
        cbar=False,
        ax=ax
    )

    tick_step = 50
    ax.set_xticks(np.arange(tick_step, len(residues), tick_step) + 0.5)
    ax.set_yticks(np.arange(tick_step, len(residues), tick_step) + 0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.invert_yaxis()
    ax.tick_params(axis='both', which='major', length=10, width=3)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = plt.colorbar(sns_heat.collections[0], cax=cax)
    cbar.ax.tick_params(axis='y', length=10, width=3, labelsize=0)
    cbar.set_label("")
    for spine in cbar.ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/pb_pairwise_heatmap_{label.replace(' ', '_')}.png", dpi=300)
    plt.close()

ordered_residues = sorted([int(r) for r in residues_union])
ordered_residues = [str(r) for r in ordered_residues]
avg_matrix = sum_matrix / count_matrix

fig, ax = plt.subplots(figsize=(16, 16))
for spine in ax.spines.values():
    spine.set_visible(False)

sns_heat = sns.heatmap(
    avg_matrix.loc[ordered_residues, ordered_residues],
    cmap="coolwarm",
    center=0,
    vmin=-0.25,
    vmax=0.25,
    linewidths=0,
    square=True,
    cbar=False,
    ax=ax
)

tick_step = 50
ax.set_xticks(np.arange(tick_step, len(ordered_residues), tick_step) + 0.5)
ax.set_yticks(np.arange(tick_step, len(ordered_residues), tick_step) + 0.5)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.invert_yaxis()
ax.tick_params(axis='both', which='major', length=10, width=3)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(sns_heat.collections[0], cax=cax)
cbar.ax.tick_params(axis='y', length=10, width=3, labelsize=0)
cbar.set_label("")
for spine in cbar.ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f"{output_dir}/heatmap.pdf", dpi=300)
plt.savefig(f"{output_dir}/heatmap.svg", dpi=800)

