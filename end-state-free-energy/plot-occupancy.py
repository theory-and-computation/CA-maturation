import re
import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'

images_dir = "../images"
plots_dir = "../plots"
os.makedirs(images_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

pdb_files = [f for f in os.listdir() if re.match(r"frame-(\d+)\.pdb", f)]
if not pdb_files:
    raise FileNotFoundError("No PDB files with pattern 'frame-(number).pdb' found in the directory.")

mmpbsa_file = "FINAL_DECOMP_MMPBSA.dat"

residue_names = []
residue_numbers = []
binding_energies = []
electrostatic_energies = []
solvation_energies = []
vdw_energies = []

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
        if total_energy_section and "Sidechain Energy Decomposition" in line:
            break
        if total_energy_section:
            try:
                columns = line.strip().split(",")
                if len(columns) < 20:
                    continue
                residue_info = columns[0].strip()
                residue_number = int(residue_info.split()[-1])
                electro = float(columns[-12].strip())
                solvation = float(columns[-9].strip())
                vdw = float(columns[-15].strip())
                total_energy = float(columns[-3].strip())

                residue_names.append(residue_info)
                residue_numbers.append(residue_number)
                electrostatic_energies.append(electro)
                solvation_energies.append(solvation)
                vdw_energies.append(vdw)
                binding_energies.append(total_energy)
            except (ValueError, IndexError):
                continue

energy_dict = {res_num: energy for res_num, energy in zip(residue_numbers, binding_energies)}

for pdb_input in pdb_files:
    frame_number = re.search(r"frame-(\d+)\.pdb", pdb_input).group(1)
    pdb_output = f"frame-ba.pdb"
    energy_output = f"residue-energy.txt"
    tcl_output = f"visualize-residues.tcl"
    render_output = f"render-{frame_number}.tga"
    plot_filename = os.path.join(plots_dir, f"decomp-{frame_number}.png")

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(residue_numbers, vdw_energies, label='van der Waals', color='forestgreen', linewidth=1.5, alpha=0.8)
    ax.plot(residue_numbers, electrostatic_energies, label='Electrostatic', color='darkorange', linewidth=1.5, alpha=0.35)
    ax.plot(residue_numbers, solvation_energies, label='Polar Solvation', color='slateblue', linewidth=1.5, alpha=0.35)
    ax.plot(residue_numbers, binding_energies, label='Total', color='black', linewidth=2.5)

    ax.legend(loc="lower left", frameon=True, framealpha=1, edgecolor="black", fontsize=12)

    ax.axhline(0, color='black', linestyle='--', linewidth=1.5)
    ax.set_xlim(-0.2, 222)
    ax.set_ylim(-25, 25)
    ax.set_yticks([15, 0, -15])
    ax.set_yticklabels(["15", "0", "-15"], fontsize=20)
    ax.set_xlabel("Residue", fontsize=25)
    ax.set_ylabel(r"$\Delta G_{\mathrm{binding}}$ (kcal/mol)", fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=20, width=2, length=8)
    xticks = np.arange(min(residue_numbers), max(residue_numbers) + 1, 50)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize=20)
    ax.grid(True, linestyle='--', alpha=0.5)

    state_label = f"State {33 - int(frame_number)}"
    ax.text(0.03, 0.95, state_label, transform=ax.transAxes, fontsize=20, verticalalignment='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
    plt.tight_layout()
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Energy plot saved as: {plot_filename}")

    with open(energy_output, "w") as outfile:
        outfile.write("Residue Name,Residue Number,Binding Free Energy (kcal/mol),VDW Energy (kcal/mol)\n")
        for res_name, res_num, energy, vdw in zip(residue_names, residue_numbers, binding_energies, vdw_energies):
            outfile.write(f"{res_name},{res_num},{energy:.4f},{vdw:.4f}\n")

    with open(pdb_input, "r") as infile, open(pdb_output, "w") as outfile:
        for line in infile:
            if line.startswith(("ATOM", "HETATM")):
                try:
                    res_num = int(line[22:26].strip())
                    if res_num in energy_dict:
                        energy_value = energy_dict[res_num]
                        new_line = f"{line[:54]}{(energy_value):6.2f}{line[60:]}"
                        outfile.write(new_line)
                        continue
                except ValueError:
                    pass
            outfile.write(line)
    print(f"Processed {pdb_input} -> {pdb_output}")

    residues = []
    with open(energy_output, "r") as infile:
        infile.readline()
        for line in infile:
            parts = line.strip().split(",")
            if len(parts) == 4:
                res_name = parts[0]
                res_num = parts[1]
                energy_value = float(parts[2])
                vdw_value = float(parts[3])
                residues.append((res_name, res_num, energy_value, vdw_value))

    residues_sorted = sorted(residues, key=lambda x: x[2])
    most_stabilizing = residues_sorted[:5]
    most_destabilizing = residues_sorted[-3:]
    vdw_residues = [(res_name, res_num, vdw) for res_name, res_num, _, vdw in residues if vdw <= -15]

    with open(tcl_output, "w") as tcl_file:
        tcl_file.write(f'mol new {pdb_output} type pdb waitfor all\n')
        tcl_file.write('mol delrep 0 top\n')

        tcl_file.write('mol selection "segname 0A0 and resid 1 to 145"\n')
        tcl_file.write('mol representation NewCartoon 0.5 40 3.5 0\n')
        tcl_file.write('mol color ColorID 12\n')
        tcl_file.write('mol material AOChalky\n')
        tcl_file.write('mol addrep top\n')

        tcl_file.write('mol selection "segname 0A0 and resid 146 to 231"\n')
        tcl_file.write('mol representation NewCartoon 0.5 40 3.5 0\n')
        tcl_file.write('mol color ColorID 14\n')
        tcl_file.write('mol material AOChalky\n')
        tcl_file.write('mol addrep top\n')

        tcl_file.write('color scale method BWR\n')
        




 #       for category, residues_list in zip(['most_stabilizing', 'most_destabilizing'], [most_stabilizing, most_destabilizing]):
        for category, residues_list in zip(['most_stabilizing'], [most_stabilizing]):

            for res_name, res_num, energy, _ in residues_list:
            
                tcl_file.write('mol representation Licorice\n')
                tcl_file.write(f'mol selection "resid {res_num} and not hydrogen"\n')
                tcl_file.write('mol color Name\n')
                tcl_file.write('mol material AOChalky\n')
                tcl_file.write('mol resolution 50\n')
                tcl_file.write('mol addrep top\n')
                
                
 #               tcl_file.write('mol representation VDW 0.6 12\n')
 #               tcl_file.write(f'mol selection "resid {res_num} and not hydrogen and not oxygen and not nitrogen"\n')
 #               tcl_file.write('mol color ColorID 10\n')
 #               tcl_file.write('mol material AOChalky\n')
 #               tcl_file.write('mol resolution 50\n')
 #               tcl_file.write('mol addrep top\n')

 #               tcl_file.write('mol representation VDW 0.7 12\n')
 #               tcl_file.write(f'mol selection "resid {res_num} and oxygen"\n')
 #               tcl_file.write('mol color Name\n')
 #               tcl_file.write('mol material AOChalky\n')
 #               tcl_file.write('mol resolution 50\n')
 #               tcl_file.write('mol addrep top\n')


 #               tcl_file.write('mol representation VDW 0.7 12\n')
 #               tcl_file.write(f'mol selection "resid {res_num} and nitrogen"\n')
 #               tcl_file.write('mol color Name\n')
 #               tcl_file.write('mol material AOChalky\n')
 #               tcl_file.write('mol resolution 50\n')
 #               tcl_file.write('mol addrep top\n')



        for res_name, res_num, vdw in vdw_residues:
            tcl_file.write('mol representation VDW\n')
            tcl_file.write(f'mol selection "resid {res_num}"\n')
            tcl_file.write('mol color Name\n')
            tcl_file.write('mol material AOShiny\n')
            tcl_file.write('mol resolution 50\n')
            tcl_file.write('mol addrep top\n')

        tcl_file.write('display resize 1000 1000\n')
        tcl_file.write('display shadows off\n')
        tcl_file.write('display depthcue on\n')
        tcl_file.write('display cuemode linear\n')
        tcl_file.write('display ambientocclusion on\n')
        tcl_file.write('color Display Background white\n')
        tcl_file.write('axes location off\n')
        tcl_file.write('scale by 1.75\n')
        tcl_file.write('rotate x by 60\n')
        tcl_file.write('rotate z by 10\n')
        tcl_file.write('rotate y by 40\n')
        tcl_file.write('material change ambient AOChalky 0.25\n')
        tcl_file.write(f'set filename "{images_dir}/{render_output}"\n')
        tcl_file.write('render TachyonInternal $filename\n')
        tcl_file.write('puts "Rendering completed. Output saved as $filename."\n')
 #       tcl_file.write('quit\n')

    print(f"Generated VMD Tcl script: {tcl_output}")

