#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.font_manager import FontProperties

base_dir = "./"
selected_indices = ["1", "4", "10", "15", "19", "21", "28", "32"]
directories = [
    d for d in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, d)) and d in selected_indices
]
directories_sorted = sorted(directories, key=lambda x: int(x))

labels = ["Mature", "I", "II", "III", "IV", "V", "VI", "Immature"]

label_display_map = {
    "Mature": "Mat.",
    "Immature": "Imm."
}

color_map = {
    "Immature": "#FF6600",
    "I": "#FF8C00",
    "II": "#FFB347",
    "III": "#FFE5B4",
    "IV": "#B3CDE0",
    "V": "#6497B1",
    "VI": "#005B96",
    "Mature": "#03396C",
}

alpha_map = {
    "Immature": 1.0, "I": 0.8, "II": 0.81, "III": 0.82, "IV": 0.85,
    "V": 0.88, "VI": 0.9, "Mature": 1.0
}

# Option 1:
# - Use PB section for Electrostatic/vdW/Polar/Total
# - Use GB section for Nonpolar
energy_terms = OrderedDict([
    ("Electrostatic",      (8,  "Poisson Boltzmann")),
    ("van der Waals",      (5,  "Poisson Boltzmann")),
    ("Polar Solvation",    (11, "Poisson Boltzmann")),
    ("Nonpolar Solvation", (14, "Generalized Born")),
    ("Total",              (17, "Poisson Boltzmann")),
])

y_axis_config = {
    "Electrostatic": (-50, 50),
    "van der Waals": (-10, 10),
    "Polar Solvation": (-50, 50),
    "Nonpolar Solvation": (-0.5, 0.5),
    "Total": (-10, 10),
}

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

fig, axs = plt.subplots(3, 2, figsize=(24, 20))
axs = axs.flatten()

for i, (energy_label, (col_index, section_keyword)) in enumerate(energy_terms.items()):
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
        in_section = False
        in_total_decomp = False

        with open(mmpbsa_file, "r") as infile:
            for line in infile:
                # Enter either PB or GB section depending on energy term
                if section_keyword in line:
                    in_section = True
                    in_total_decomp = False
                    continue

                # Once inside the requested section, enter the "Total Energy Decomposition" table
                if in_section and "Total Energy Decomposition" in line:
                    in_total_decomp = True
                    continue

                if not in_total_decomp:
                    continue

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

        if not residue_numbers:
            continue

        sorted_data = sorted(zip(residue_numbers, energy_values))
        residue_numbers, energy_values = zip(*sorted_data)

        z = 10 if label == "Mature" else 1
        ax.plot(
            residue_numbers,
            energy_values,
            label=label_display_map.get(label, label),
            color=color_map[label],
            linewidth=2,
            alpha=alpha_map[label],
            zorder=z
        )

    ax.axhline(0, color="gray", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_title(f"{energy_label} Energy", fontsize=24, family="DejaVu Sans")

    ax.set_xlim(0, 221)
    ax.set_xticks([50, 100, 150, 200])

    if energy_label in y_axis_config:
        ax.set_ylim(*y_axis_config[energy_label])

    ax.tick_params(axis="both", which="major", labelsize=22)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontname("DejaVu Sans")

    if i in (0, 2, 4):
        ax.set_ylabel("Energy (kcal/mol)", fontsize=18, family="DejaVu Sans")
    if i in (4, 5):
        ax.set_xlabel("Residue", fontsize=24, family="DejaVu Sans")

axs[5].axis("off")

handles, labels_legend = axs[0].get_legend_handles_labels()
desired_order = ["Immature", "I", "II", "III", "IV", "V", "VI", "Mature"]
legend_dict = OrderedDict()

for lab in desired_order:
    target = label_display_map.get(lab, lab)
    for handle, lbl in zip(handles, labels_legend):
        if lbl == target:
            legend_dict[lab] = handle
            break

legend_title_font = FontProperties(family="DejaVu Sans", size=25)
legend_label_font = FontProperties(family="DejaVu Sans", size=20)

fig.legend(
    list(legend_dict.values()),
    [label_display_map.get(k, k) for k in desired_order],
    title="States",
    title_fontproperties=legend_title_font,
    prop=legend_label_font,
    loc="lower center",
    ncol=1,
    bbox_to_anchor=(0.9, 0.5)
).set_frame_on(False)

plt.subplots_adjust(
    left=0.07,
    right=0.80,
    top=0.92,
    bottom=0.08,
    hspace=0.35,
    wspace=0.22
)

outpath = os.path.join(output_dir, "combined_energy_terms.svg")
fig.savefig(outpath, dpi=600, bbox_inches="tight")
plt.show()

