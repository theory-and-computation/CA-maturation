import os
import matplotlib.pyplot as plt
from collections import OrderedDict

base_dir = "./"
#selected_indices = ["1", "4", "10", "15", "19", "21", "28", "32"]
selected_indices = ["1", "6", "8", "12", "21", "24", "30", "32"]
directories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d in selected_indices]
directories_sorted = sorted(directories, key=lambda x: int(x))

labels = ["Mature", "I", "II", "III", "IV", "V", "VI", "Immature"]

# 4 oranges (light → dark) and 4 blues (light → dark)
color_map = {
    "Immature": "#E65100",  # light orange
    "I": "#FF8C00",         # medium orange
    "II": "#FFB347",        # dark orange
    "III": "#FFE5B4",       # very dark orange
    "IV": "#B3CDE0",        # light blue
    "V": "#6497B1",         # medium blue
    "VI": "#005B96",        # dark blue
    "Mature": "#03396C",    # very dark blue
}

alpha_map = {
    "Immature": 1.0, "I": 0.8, "II": 0.81, "III": 0.82, "IV": 0.85,
    "V": 0.88, "VI": 0.9, "Mature": 1.0
}

energy_terms = OrderedDict([
    ("Electrostatic", 8),
    ("van der Waals", 5),
    ("Solvation", 11),
    ("Nonpolar", 14),
    ("Total", 17),
])

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

rows, cols = 3, 2
fig, axs = plt.subplots(rows, cols, figsize=(32, 36))
axs = axs.flatten()

for i, (energy_label, col_index) in enumerate(energy_terms.items()):
    ax = axs[i]
    for spine in ax.spines.values():
        spine.set_linewidth(0)
    for idx, directory in enumerate(directories_sorted):
        label = labels[idx]
        mmpbsa_file = os.path.join(base_dir, directory, "FINAL_DECOMP_MMPBSA.dat")
        if not os.path.isfile(mmpbsa_file):
            continue
        residue_numbers = []
        energy_values = []
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
                        residue_numbers.append(residue_number)
                        energy_values.append(energy_value)
                    except (ValueError, IndexError):
                        continue
        if residue_numbers and energy_values:
            sorted_data = sorted(zip(residue_numbers, energy_values))
            residue_numbers, energy_values = zip(*sorted_data)
        z = 10 if label == "Mature" else 1
        ax.plot(residue_numbers, energy_values, label=label, color=color_map[label], linewidth=2, alpha=alpha_map[label], zorder=z)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    ax.set_title(energy_label, fontsize=26, fontweight='bold')
    ax.set_xlim(-0, 221.)
    if energy_label == "Total":
        ax.set_ylim(-10, 10)
        ax.set_yticks([-5, 0, 5])
    else:
        ax.set_ylim(-60, 60)
        ax.set_yticks([-40, 0, 40])
    ax.set_xticks([50, 100, 150, 200])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.tick_params(axis='both', which='major', length=10, width=3)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontweight('bold')
        tick.set_fontname('DejaVu Sans')

for j in range(len(energy_terms), len(axs)):
    fig.delaxes(axs[j])

handles, labels_found = axs[0].get_legend_handles_labels()
label_order = ["Immature", "I", "II", "III", "IV", "V", "VI", "Mature"]
legend_dict = OrderedDict()
for lbl in label_order:
    for h, l in zip(handles, labels_found):
        if l == lbl:
            legend_dict[lbl] = h
            break

fig.legend(
    list(legend_dict.values()),
    list(legend_dict.keys()),
    title="States",
    loc='lower center',
    ncol=8,
    frameon=False,
    bbox_to_anchor=(0.5, 0.02),
    fontsize=20,
    title_fontsize=24
)

fig.suptitle("", fontsize=28, fontweight='bold')
plt.subplots_adjust(left=0.06, right=0.80, top=0.93, bottom=0.10, hspace=0.35, wspace=0.25)

fig.savefig(os.path.join(output_dir, "combined_energy_terms.svg"), dpi=1000, bbox_inches='tight')
fig.savefig(os.path.join(output_dir, "combined_energy_terms.pdf"), dpi=1000, bbox_inches='tight')
plt.show()

