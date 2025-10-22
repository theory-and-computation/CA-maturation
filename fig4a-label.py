import os
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.font_manager import FontProperties

base_dir = "./"
#selected_indices = ["1", "4", "10", "15", "19", "21", "28", "32"]
selected_indices = ["1", "6", "8", "12", "21", "24", "30", "32"]
directories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d in selected_indices]
directories_sorted = sorted(directories, key=lambda x: int(x))

labels = ["Mature", "I", "II", "III", "IV", "V", "VI", "Immature"]

label_display_map = {
    "Mature": "Mat.",
    "Immature": "Imm."
}

color_map = {
    "Immature": "#FF6600", "I": "#FF9F45", "II": "#CCE5FF", "III": "#A6C6FF",
    "IV": "#7D9DE9", "V": "#5C7CC9", "VI": "#3B5BA9", "Mature": "#1E3A8A"
}

alpha_map = {
    "Immature": 1.0, "I": 0.8, "II": 0.81, "III": 0.82, "IV": 0.85,
    "V": 0.88, "VI": 0.9, "Mature": 1.0
}

energy_terms = {
    "Electrostatic": 8, "van der Waals": 5,
    "Solvation": 11, "Total": 17
}

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

fig, axs = plt.subplots(2, 2, figsize=(32, 24))
axs = axs.flatten()

for i, (energy_label, col_index) in enumerate(energy_terms.items()):
    ax = axs[i]
    for spine in ax.spines.values():
        spine.set_linewidth(3)
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
        ax.plot(residue_numbers, energy_values,
                label=label_display_map.get(label, label),
                color=color_map[label],
                linewidth=2,
                alpha=alpha_map[label],
                zorder=z)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.6)
    ax.set_title(f"{energy_label} Energy", fontsize=24, fontweight='bold', family='DejaVu Sans')
    ax.set_xlim(0, 221)
    ax.set_ylim(-60, 60)
    ax.set_yticks([-40, 0, 40])
    ax.set_xticks([50, 100, 150, 200])
    ax.tick_params(axis='both', which='major', labelsize=22)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontweight('bold')
        tick.set_fontname('DejaVu Sans')
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    if i % 2 == 0:
        ax.set_ylabel("Energy (kcal/mol)", fontsize=18, fontweight='bold', family='DejaVu Sans')
    if i >= 2:
        ax.set_xlabel("Residue", fontsize=24, fontweight='bold', family='DejaVu Sans')

handles, labels_legend = axs[0].get_legend_handles_labels()
desired_order = ["Immature", "I", "II", "III", "IV", "V", "VI", "Mature"]
legend_dict = OrderedDict()
for label in desired_order:
    for handle, lbl in zip(handles, labels_legend):
        if lbl == label_display_map.get(label, label):
            legend_dict[label] = handle
            break

legend_title_font = FontProperties(family='DejaVu Sans', weight='bold', size=25)
legend_label_font = FontProperties(family='DejaVu Sans', weight='bold', size=20)

fig.legend(
    list(legend_dict.values()),
    [label_display_map.get(k, k) for k in desired_order],
    title="States",
    title_fontproperties=legend_title_font,
    prop=legend_label_font,
    loc='lower center',
    ncol=1,
    bbox_to_anchor=(0.9, 0.5)
).set_frame_on(False)

fig.suptitle("Interdomain Energy Decomposition Across Transition States",
             fontsize=30, fontweight='bold', family='DejaVu Sans')

plt.subplots_adjust(left=0.06, right=0.80, top=0.90, bottom=0.25, hspace=0.3, wspace=0.2)

fig.savefig(os.path.join(output_dir, "combined_energy_terms.png"), dpi=1000, bbox_inches='tight')
fig.savefig(os.path.join(output_dir, "combined_energy_terms.pdf"), dpi=1000, bbox_inches='tight')
plt.show()

