import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'sans-serif'


def set_residue_ticks(ax, residues, tick_step=50, start=50, fontsize=20):
    max_res = int(residues[-1])
    want = list(range(start, max_res + 1, tick_step))
    positions = [i for i, r in enumerate(residues) if int(r) in want]
    labels = [residues[i] for i in positions]
    ax.set_xticks(positions)
    ax.set_yticks(positions)
    ax.set_xticklabels(labels, rotation=0, fontsize=fontsize)
    ax.set_yticklabels(labels, fontsize=fontsize)


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

    plt.figure(figsize=(16, 16))
    ax = sns.heatmap(
        matrix.astype(float),
        cmap="coolwarm",
        center=0,
        vmin=-0.25,
        vmax=0.25,
        linewidths=0,
        square=True,
        cbar_kws={"label": "Interaction Energy (kcal/mol)", "shrink": 0.75},
    )

    set_residue_ticks(ax, residues, tick_step=50, start=50, fontsize=20)
    ax.invert_yaxis()
    ax.tick_params(axis="both", which="major", length=10, width=3)
    ax.set_xlabel("Residue", fontsize=25)
    ax.set_ylabel("Residue", fontsize=25)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=18)
    cbar.set_label("Interaction Energy (kcal/mol)", fontsize=20)
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

    height = matrix.shape[0]
    width = matrix.shape[1]
    rect = patches.Rectangle((0, 0), width, height, linewidth=8, edgecolor="black", facecolor="none")
    ax.add_patch(rect)

    plt.savefig(f"{output_dir}/{idx+1:02d}.png", dpi=300, bbox_inches="tight")
    plt.close()

    flattened = matrix.stack().reset_index()
    flattened.columns = ["Residue1", "Residue2", "Energy"]
    flattened["res1"] = flattened["Residue1"].astype(int)
    flattened["res2"] = flattened["Residue2"].astype(int)

    flattened = flattened[flattened["res1"] != flattened["res2"]]
    flattened = flattened[abs(flattened["res1"] - flattened["res2"]) > 1]

    flattened["Pair"] = flattened.apply(
        lambda row: tuple(sorted([row["Residue1"], row["Residue2"]])), axis=1
    )
    flattened = flattened.drop_duplicates(subset="Pair")

    stabilizing = flattened.nsmallest(20, "Energy")
    destabilizing = flattened.nlargest(1, "Energy")

    # Disabled output:
    # for _, row in pd.concat([stabilizing, destabilizing]).iterrows():
    #     out_file.write(f"{idx+1} {row['Residue1']} {row['Residue2']} {row['Energy']:.3f}\n")


ordered_residues = sorted([int(r) for r in residues_union])
ordered_residues = [str(r) for r in ordered_residues]

avg_matrix = sum_matrix / count_matrix

plt.figure(figsize=(16, 16))
ax = sns.heatmap(
    avg_matrix.loc[ordered_residues, ordered_residues],
    cmap="coolwarm",
    center=0,
    vmin=-0.25,
    vmax=0.25,
    linewidths=0,
    square=True,
    cbar_kws={"label": "Avg Interaction Energy (kcal/mol)", "shrink": 0.75},
)

set_residue_ticks(ax, ordered_residues, tick_step=50, start=50, fontsize=20)
ax.invert_yaxis()
ax.tick_params(axis="both", which="major", length=10, width=3)

ax.set_title("Average Pairwise Interactions Across Transition States", fontsize=24)
ax.set_xlabel("Residue", fontsize=25)
ax.set_ylabel("Residue", fontsize=25)

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=18)
cbar.set_label("Avg Interaction Energy (kcal/mol)", fontsize=20)
cbar.ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

height = avg_matrix.shape[0]
width = avg_matrix.shape[1]
rect = patches.Rectangle((0, 0), width, height, linewidth=8, edgecolor="black", facecolor="none")
ax.add_patch(rect)

#plt.savefig(f"{output_dir}/heatmap.pdf", dpi=600)
plt.savefig(f"output/heatmap.svg", dpi=600)
plt.show()

