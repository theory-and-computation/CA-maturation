import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable


base_dir = "./"
selected_indices = [str(i) for i in range(1, 34)]
directories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d in selected_indices]
directories_sorted = sorted(directories, key=lambda x: int(x))
labels = [f"State {i}" for i in range(1, 34)]

energy_terms = {
    "van der Waals": 5,
    "Electrostatic": 8,
    "Polar Solvation": 11,
    "Total": 17
}

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for energy_label, col_index in energy_terms.items():
    out_stem = energy_label.lower().replace(" ", "_")
    residue_energy_by_state = {label: {} for label in labels}

    for idx, directory in enumerate(directories_sorted):
        label = labels[idx]
        mmpbsa_file = os.path.join(base_dir, directory, "FINAL_DECOMP_MMPBSA.dat")
        pb_section = False
        total_energy_section = False

        with open(mmpbsa_file, "r") as infile:
            for line in infile:
                if "Poisson Boltzmann" in line:
                    pb_section = True
                    continue
                if pb_section and "Total Energy Decomposition" in line:
                    total_energy_section = True
                    continue
                if total_energy_section:
                    try:
                        columns = line.strip().split(",")
                        if len(columns) <= col_index:
                            continue
                        residue_info = columns[0].strip()
                        residue_number = int(residue_info.split()[-1])
                        energy_value = float(columns[col_index].strip())
                        residue_energy_by_state[label][residue_number] = energy_value
                    except (ValueError, IndexError):
                        continue

    all_residues = sorted(set().union(*[set(d.keys()) for d in residue_energy_by_state.values()]))
    residue_idx_map = {resid: i for i, resid in enumerate(all_residues)}
    n_residues = len(all_residues)
    n_states = len(labels)

    heatmap = np.full((n_states, n_residues), np.nan)
    for state_idx, label in enumerate(labels):
        for resid, energy in residue_energy_by_state[label].items():
            col_idx = residue_idx_map[resid]
            heatmap[state_idx, col_idx] = energy

    if np.all(np.isnan(heatmap)):
        print(f"Skipping {energy_label}: heatmap contains only NaNs.")
        continue

    cell_size = 0.3
    fig_width = min(cell_size * n_residues, 25)
    fig_height = min(cell_size * n_states, 15)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    for spine in ax.spines.values():
        spine.set_linewidth(3)

    norm = TwoSlopeNorm(vmin=-9, vcenter=0, vmax=9)
    im = ax.imshow(heatmap, aspect='auto', cmap='RdBu_r', norm=norm, interpolation='nearest')

    xticks = np.arange(0, len(all_residues), 20)
    ax.set_xticks(xticks - 0.1)
    ax.set_xticklabels([str(all_residues[i]) if i < len(all_residues) else "" for i in xticks],
                       fontsize=20, fontname='DejaVu Sans', fontweight='bold', rotation=0, ha='right')
    ax.set_xlim(-0.5, len(all_residues) - 0.5)
    ax.set_ylim(-0.5, len(labels) - 0.5)

    yticks = np.arange(0, len(labels), 5)
    ax.set_yticks(yticks)
    ytick_labels = [str(i + 1) for i in yticks]
    ytick_labels[0] = "Mature"
    ytick_labels[-1] = "Immature"
    ax.set_yticklabels(ytick_labels, fontsize=20, fontname='DejaVu Sans', fontweight='bold')

    ax.set_xlabel("Residue", fontsize=20, fontname='DejaVu Sans', fontweight='bold')
    ax.set_ylabel("Transition State", fontsize=20, fontname='DejaVu Sans', fontweight='bold')
    ax.set_title(f"{energy_label} Energy", fontsize=20, fontname='DejaVu Sans', fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Energy (kcal/mol)", fontsize=20, fontname='DejaVu Sans', fontweight='bold')
    cbar.ax.tick_params(labelsize=16)

    plt.tight_layout(pad=1.0)
    plt.savefig(os.path.join(output_dir, f"{out_stem}_heatmap.svg"), dpi=700)
    plt.close()

    if energy_label == "Total":
        regions = {
            "residues_21_41": (21, 41),
            "residues_141_161": (136, 156),
            "residues_161_181": (163, 183)
        }

        for region_label, (start, end) in regions.items():
            cols = [i for i, r in enumerate(all_residues) if start <= r <= end]
            if not cols:
                print(f"Warning: No residues found in range {start}-{end}")
                continue

            heatmap_slice = heatmap[:, cols]
            residue_labels = [all_residues[i] for i in cols]

            fig, ax = plt.subplots(figsize=(len(cols) * 0.3, len(labels) * 0.3))
            for spine in ax.spines.values():
                spine.set_linewidth(3)

            im = ax.imshow(np.flipud(heatmap_slice), aspect='auto', cmap='RdBu_r', norm=norm, interpolation='nearest')

            xticks = np.arange(0, len(residue_labels), 8)
            ax.set_xticks(xticks)
            ax.set_xticklabels([str(residue_labels[i]) for i in xticks],
                               fontsize=22, fontname='DejaVu Sans', fontweight='bold')
            ax.tick_params(axis='both', which='major', length=10, width=3, direction='out')



            ytick_positions = [0, 25, 16, 8, 32]  
            ytick_labels = ["Imm.", "8", "17", "25", "Mat."]
            ax.set_yticks(ytick_positions)
            ax.set_yticklabels(ytick_labels, fontsize=24, fontname='DejaVu Sans', fontweight='bold')

            ax.set_xlabel("Residue", fontsize=24, fontname='DejaVu Sans', fontweight='bold')
            ax.set_ylabel("Transition State", fontsize=28, fontname='DejaVu Sans', fontweight='bold')
            ax.set_title(f"{energy_label} Energy", fontsize=25, fontname='DejaVu Sans', fontweight='bold')

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="8%", pad=0.15)
            cbar = plt.colorbar(im, cax=cax)
            cbar.set_label("Energy (kcal/mol)", fontsize=23, fontname='DejaVu Sans', fontweight='bold', labelpad=10)
            cbar.ax.tick_params(labelsize=20,length=10, width=2)



            plt.tight_layout(pad=1.0)
            plt.savefig(os.path.join(output_dir, f"{out_stem}_{region_label}_zoom.pdf"), dpi=600)
            plt.close()


