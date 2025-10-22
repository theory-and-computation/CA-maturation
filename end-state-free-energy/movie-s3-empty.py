import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as patches
import subprocess
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import matplotlib.cm as cm

plt.rcParams['font.family'] = 'sans-serif'

def build_centered_gradient_cmap(vmax: float):
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
    base = cm.get_cmap("RdBu_r")
    colors = [
        (0.0,  base(0.00)),
        (0.20, base(0.20)),
        (0.40, base(0.40)),
        (0.50, "white"),
        (0.60, base(0.60)),
        (0.80, base(0.80)),
        (1.0,  base(1.00)),
    ]
    cmap = LinearSegmentedColormap.from_list("rdblu_center_grad", colors)
    return cmap, norm

VMAX = 0.25

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
selected_indices = [str(i) for i in range(1, 33)]
directories_sorted = sorted(
    [d for d in os.listdir(base_dir) if d in selected_indices and os.path.isdir(os.path.join(base_dir, d))],
    key=int
)

pb_total_col = 17
output_dir = "tmp"
os.makedirs(output_dir, exist_ok=True)

sum_matrix = None
count_matrix = None
residues_union = set()
residue_stability = defaultdict(lambda: {"count": 0, "sum_dG": 0.0})

highlight_rects = [
    (24, 162, 22, 13),
    (162, 24, 13, 22),
    (165, 140, 13, 13),
    (140, 165, 13, 13)
]
highlight_color = 'black'
highlight_linewidth = 3

cmap_band, norm_band = build_centered_gradient_cmap(vmax=VMAX)

with open("top5-stabilizing.txt", "w") as out_file:
    total = len(directories_sorted)
    for pos, directory in enumerate(directories_sorted, start=1):
        rev_num = total - pos + 1
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
        for a in residues:
            for b in residues:
                matrix.loc[a, b] = interaction_matrix.get(a, {}).get(b, 0.0)
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
            cmap=cmap_band,
            norm=norm_band,
            linewidths=0,
            square=True,
            cbar_kws={"label": "Interaction Energy (kcal/mol)", "shrink": 0.75}
        )
        ax.text(
            0.02, 0.98, f"State {rev_num}",
            transform=ax.transAxes,
            fontsize=20,
            color='black',
            verticalalignment='top',
            horizontalalignment='left',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
        )
        for res1, res2, w, h in highlight_rects:
            if str(res1) in residues and str(res2) in residues:
                ii = residues.index(str(res1))
                jj = residues.index(str(res2))
                ax.add_patch(patches.Rectangle((jj, ii), w, h, fill=False,
                                               edgecolor=highlight_color,
                                               linewidth=highlight_linewidth))
        set_residue_ticks(ax, residues, tick_step=50, start=50, fontsize=20)
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', length=10, width=3)
        ax.set_xlabel("Residue", fontsize=25)
        ax.set_ylabel("Residue", fontsize=25)
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=18)
        cbar.set_label("Interaction Energy (kcal/mol)", fontsize=20)
        cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        height = matrix.shape[0]
        width = matrix.shape[1]
        ax.add_patch(patches.Rectangle((0, 0), width, height, linewidth=8,
                                       edgecolor='black', facecolor='none'))
        plt.savefig(f"{output_dir}/{directory}.png", dpi=300, bbox_inches='tight')
        plt.close()
        flattened = matrix.stack().reset_index()
        flattened.columns = ['Residue1', 'Residue2', 'Energy']
        flattened['res1'] = flattened['Residue1'].astype(int)
        flattened['res2'] = flattened['Residue2'].astype(int)
        flattened = flattened[flattened['res1'] != flattened['res2']]
        flattened = flattened[abs(flattened['res1'] - flattened['res2']) > 1]
        flattened['Pair'] = flattened.apply(
            lambda row: tuple(sorted([row['Residue1'], row['Residue2']])),
            axis=1
        )
        flattened = flattened.drop_duplicates(subset='Pair')
        stabilizing = flattened.nsmallest(5, 'Energy')
        destabilizing = flattened.nlargest(5, 'Energy')
        for _, row in pd.concat([stabilizing, destabilizing]).iterrows():
            out_file.write(f"{rev_num} {row['Residue1']} {row['Residue2']} {row['Energy']:.3f}\n")
            for res in [row['Residue1'], row['Residue2']]:
                residue_stability[res]["count"] += 1
                residue_stability[res]["sum_dG"] += row['Energy']

    out_file.write("\n=== Residue Stability Summary Across States ===\n")
    sorted_residues = sorted(residue_stability.items(), key=lambda x: x[1]["sum_dG"])
    for res, stats in sorted_residues:
        count = stats["count"]
        sum_dG = stats["sum_dG"]
        out_file.write(f"Residue {res}: {count} appearances, cumulative ΔG = {sum_dG:.4f} kcal/mol\n")

ordered_residues = sorted([int(r) for r in residues_union])
ordered_residues = [str(r) for r in ordered_residues]
avg_matrix = sum_matrix.divide(count_matrix.replace(0, np.nan))

plt.figure(figsize=(16, 16))
cmap_avg, norm_avg = build_centered_gradient_cmap(vmax=VMAX)
ax = sns.heatmap(
    avg_matrix.loc[ordered_residues, ordered_residues],
    cmap=cmap_avg,
    norm=norm_avg,
    linewidths=0,
    square=True,
    cbar_kws={"label": "Avg Interaction Energy (kcal/mol)", "shrink": 0.75}
)
set_residue_ticks(ax, ordered_residues, tick_step=50, start=50, fontsize=20)
ax.invert_yaxis()
ax.tick_params(axis='both', which='major', length=10, width=3)
ax.set_title("Average Pairwise Interactions Across Transition States", fontsize=24)
ax.set_xlabel("Residue", fontsize=25)
ax.set_ylabel("Residue", fontsize=25)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=18)
cbar.set_label("Avg Interaction Energy (kcal/mol)", fontsize=20)
cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
height = avg_matrix.shape[0]
width = avg_matrix.shape[1]
ax.add_patch(patches.Rectangle((0, 0), width, height, linewidth=8, edgecolor='black', facecolor='none'))
plt.savefig(f"{output_dir}/heatmap.pdf", dpi=600)
plt.savefig(f"{output_dir}/heatmap.svg", dpi=600)

subprocess.run("cd tmp && yes | ./gif-heat.sh", shell=True)

