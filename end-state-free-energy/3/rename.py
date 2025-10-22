import glob

def fix_pdb(input_pdb, output_pdb):
    with open(input_pdb, "r") as f:
        lines = f.readlines()

    fixed_lines = []
    
    for line in lines:
        if line.startswith(("ATOM", "HETATM")):
            residue_name = line[17:20]  # Extract residue name
            atom_name = line[12:16]     # Extract atom name
            
            # Fix ILE CD -> CD1
            if residue_name == "ILE" and atom_name.strip() == "CD":
                line = line[:12] + " CD1" + line[16:]

            # Fix C-terminal VAL (CVAL -> VAL)
            if residue_name == "CVAL":
                line = line[:17] + "VAL" + line[20:]

            # Fix OT1 and OT2 -> O
            if residue_name == "VAL" and atom_name.strip() in ["OT1", "OT2"]:
                line = line[:12] + " O  " + line[16:]

            # Fix HSD -> HID (histidine correction)
            if residue_name == "HSD":
                line = line[:17] + "HID" + line[20:]

        fixed_lines.append(line)

    with open(output_pdb, "w") as f:
        f.writelines(fixed_lines)

# Process the specific file 'fixed.pdb'
input_file = "fixed.pdb"
output_file = "done.pdb"

fix_pdb(input_file, output_file)
print(f"Processed {input_file} -> {output_file}")

