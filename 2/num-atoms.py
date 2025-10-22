import parmed as pmd

# Load topology files
complex_prmtop = pmd.load_file("frame-1.prmtop")
receptor_prmtop = pmd.load_file("frame-1-ntd.prmtop")
ligand_prmtop = pmd.load_file("frame-1-ctd.prmtop")

# Count total atoms in each file
complex_atoms = complex_prmtop.atoms
receptor_atoms = receptor_prmtop.atoms
ligand_atoms = ligand_prmtop.atoms

# Print atom counts
print(f"Complex atoms: {len(complex_atoms)}")
print(f"Receptor atoms: {len(receptor_atoms)}")
print(f"Ligand atoms: {len(ligand_atoms)}")
print(f"Total (Receptor + Ligand): {len(receptor_atoms) + len(ligand_atoms)}\n")

# Create dictionaries of atoms by (name, residue name, residue number)
complex_dict = {(atom.name, atom.residue.name, atom.residue.number): atom for atom in complex_atoms}
receptor_dict = {(atom.name, atom.residue.name, atom.residue.number): atom for atom in receptor_atoms}
ligand_dict = {(atom.name, atom.residue.name, atom.residue.number): atom for atom in ligand_atoms}

# Combine receptor and ligand atoms into one dictionary
rec_lig_dict = {**receptor_dict, **ligand_dict}

# Compare atoms between complex and receptor+ligand
extra_in_rec_lig = rec_lig_dict.keys() - complex_dict.keys()
extra_in_complex = complex_dict.keys() - rec_lig_dict.keys()
"""
# Display differences
if extra_in_rec_lig:
    print("🔴 Atoms in Receptor+Ligand but NOT in Complex:")
    for key in sorted(extra_in_rec_lig):
        print(f" - Atom: {key[0]}, Residue: {key[1]}, Residue Number: {key[2]}")

if extra_in_complex:
    print("\n🟢 Atoms in Complex but NOT in Receptor+Ligand:")
    for key in sorted(extra_in_complex):
        print(f" - Atom: {key[0]}, Residue: {key[1]}, Residue Number: {key[2]}")

if not extra_in_rec_lig and not extra_in_complex:
    print("\n✅ No Differences: All atoms match between Complex and Receptor+Ligand.")
"""
