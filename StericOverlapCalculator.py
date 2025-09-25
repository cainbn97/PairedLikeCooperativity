## PYMOL will automatically remove clashing areas if in the same object
## Create objects with each chain separately so we can calculate the true surface area
## Then calculate the combined with the full object

import pymol
from pymol import cmd
import numpy as np
import os

def calculate_overlap(residue1, residue2, structure_file):
    # Calculate surface area of individual residues
    #cmd.select("res1_atoms", f'object {chain_identifiers[0]} and chain {chain_identifiers[0]} and resi {residue1}')
    cmd.create("res1_atoms", f'object {objects[0]} and chain {chain_identifiers[0]} and resi {residue1}')
    area1 = cmd.get_area("res1_atoms")
    
    #cmd.select("res2_atoms", f'object {chain_identifiers[1]} and {chain_identifiers[1]} and resi {residue2}')
    cmd.create("res2_atoms", f'object {objects[0]} and chain {chain_identifiers[1]} and resi {residue2}')
    area2 = cmd.get_area("res2_atoms")

    
    # Calculate surface area of combined residues
    cmd.select("residue1_full", f'{objects[0]} and chain {chain_identifiers[0]} and resi {residue1}')
    cmd.select("residue2_full", f'{objects[0]} and chain {chain_identifiers[1]} and resi {residue2}')

    cmd.create("combined", "residue1_full or residue2_full")

    combined_area = cmd.get_area("combined")

    # Estimate overlapping area
    overlap_area = (area1 + area2) - combined_area
    
    #print(f"Surface area of residue {residue1}: {area1} Å²")
    #print(f"Surface area of residue {residue2}: {area2} Å²")
    #print(f"Combined surface area: {combined_area} Å²")
    #print(f"Estimated overlapping area: {overlap_area} Å²")
    
    cmd.delete("res1_atoms")
    cmd.delete("res2_atoms")
    cmd.delete("combined")

    return(overlap_area)



# Collect residue identifiers
def get_residue_identifiers(chain):
    residue_ids = set()
    cmd.iterate(f'chain {chain}', 'residue_ids.add((resi))', space={'residue_ids': residue_ids})
    return residue_ids


## Grab structure name
objects = cmd.get_object_list()
print(objects)

## Grab file path information
structure_directory = os.path.dirname(objects[0])
structure_file = os.path.basename(objects[0])

print(structure_directory); print(structure_file)

## Grab all protein chain identifiers
# Select all protein atoms
cmd.select("protein_atoms", "polymer.protein")

# Get the list of atoms in the selection
atoms = cmd.get_model("protein_atoms").atom

## Grab unique chain identifiers
chain_identifiers = set()
for atom in atoms:
    chain_identifiers.add(atom.chain)


# Print the unique chain identifiers
print(f"Unique chain identifiers: {chain_identifiers}")

chain_identifiers = list(chain_identifiers)
if len(chain_identifiers) != 2:
    exit("You must have two chains for this to function.")

## Remove DNA from the object so this is only a protein-protein interface analysis
cmd.remove('polymer.nucleic')

## Make protein chains into individual objects for accurate surface area calculations
cmd.create(f'{chain_identifiers[0]}', f'chain {chain_identifiers[0]}')
cmd.create(f'{chain_identifiers[1]}', f'chain {chain_identifiers[1]}')

resi1_set = get_residue_identifiers(chain_identifiers[0])
resi2_set = get_residue_identifiers(chain_identifiers[1])                          


matrix = np.zeros((len(resi1_set), len(resi2_set)))

## Python making things 100x harder than they need to be
resi1_set = list(resi1_set)
resi1_set2 = [int(num) for num in resi1_set]
resi1_set3 = np.sort(resi1_set2)
print(resi1_set3)

resi2_set = list(resi2_set)
resi2_set2 = [int(num) for num in resi2_set]
resi2_set3 = np.sort(resi2_set2)
print(resi2_set3)

cj = 0; ci = 0;
for resi1 in resi1_set3:
    for resi2 in resi2_set3: 

        matrix[ci,cj] = calculate_overlap(resi1, resi2, structure_file)
        print(f"{resi1}, {resi2}, {matrix[ci,cj]}")

        cj += 1
    ci += 1
    cj = 0

matrix.tofile("ResidueOverlap.txt", sep = "\t")
print('DONE')

