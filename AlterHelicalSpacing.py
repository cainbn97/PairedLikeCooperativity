# Import the PyMOL module
import pymol
import numpy as np
import os


## Input PDB IDs for processing
Prd = "9D9R"
ANTP = "1HDD"

## Ensure that only the asymmetric unit or one bound unit is in the PSE
## Ensure that Prd DNA are labeled as chains C and D

## Remove DNA of ANTP factor
cmd.remove(f"{ANTP} and polymer.nucleic")


## Align ANTP to both chains of Paired-like factor and created PDB
## in which ANTP factor is docked on P3 site
cmd.set_name(ANTP, "ANTP_chainA")
cmd.alter("ANTP_chainA", "chain='A'")

cmd.create("ANTP_chainB", "ANTP_chainA")
cmd.alter("ANTP_chainB", "chain='B'")

## The gui version of alignment uses only the alpha carbons which is preferred in this case
## The function below uses all atoms which was resulting in less than ideal behavior
## Below I select the alpha carbons to align

cmd.align("ANTP_chainA////CA", f"/{Prd}/A///CA")
cmd.align("ANTP_chainB////CA", f"/{Prd}/B///CA")

cmd.create("Prd_DNA", f"{Prd} and polymer.nucleic")
cmd.alter("Prd_DNA", "chain='C'")

cmd.create(f"{ANTP}_docked_on_P3", f"ANTP_chainA or ANTP_chainB or Prd_DNA")

## Create CIF file
cmd.save(f"{ANTP}_docked_on_P3.cif", f"{ANTP}_docked_on_P3", format = "cif")


## Break up Prd monomers and align these to ANTP helices

# Function to collect residue identifiers
def get_residue_identifiers(chain):
    residue_ids = set()
    cmd.iterate(f'chain {chain}', 'residue_ids.add((resi))', space={'residue_ids': residue_ids})
    return residue_ids



for Chain in ['A', 'B']:
	
	resiID = get_residue_identifiers(Chain)
	resi1_set = list(resiID)
	resi1_set2 = [int(num) for num in resi1_set]
	minResi = np.min(resi1_set2)
	maxResi = np.max(resi1_set2)

	## Keep N-terminal ARM consistent with Prd structures; this is not expected to move
	cmd.create(f"{Prd}_Nterm_{Chain}", f"{Prd} and chain {Chain} and resi {str(minResi)}-8")

	## Align Helix 1
	cmd.create(f"{Prd}_Helix1_{Chain}", f"{Prd} and chain {Chain} and resi 9-25")
	cmd.align(f"{Prd}_Helix1_{Chain}////CA", f"ANTP_chain{Chain} and chain {Chain} and resi 9-25 and name CA")


	## Align Helix 2
	cmd.create(f"{Prd}_Helix2_{Chain}", f"{Prd} and chain {Chain} and resi 26-39")
	cmd.align(f"{Prd}_Helix2_{Chain}////CA", f"ANTP_chain{Chain} and chain {Chain} and resi 26-39 and name CA")

	## Align Helix 3 and C-terminal tail
	cmd.create(f"{Prd}_Helix3_{Chain}", f"{Prd} and chain {Chain} and resi 40-{str(maxResi)}")
	cmd.align(f"{Prd}_Helix3_{Chain}////CA", f"ANTP_chain{Chain} and chain {Chain} and resi 40-60 and name CA")

	cmd.create(f"{Prd}w{ANTP}_helicalSpacing_{Chain}", 
		f"{Prd}_Nterm_{Chain} or {Prd}_Helix1_{Chain} or {Prd}_Helix2_{Chain} or {Prd}_Helix3_{Chain}")
	
	## Bond regions back together
	cmd.bond(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 8 and name C", f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 9 and name N")

	cmd.bond(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 25 and name C", f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 26 and name N")

	cmd.bond(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 39 and name C", f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 40 and name N")
    
	## Clean these bonded regions
	cmd.clean(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 7-10")
	cmd.clean(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 24-27")
	cmd.clean(f"{Prd}w{ANTP}_helicalSpacing_{Chain} and chain {Chain} and resi 38-41")
	

cmd.create(f"{Prd}w{ANTP}_helicalSpacing",
	f"{Prd}w{ANTP}_helicalSpacing_A or {Prd}w{ANTP}_helicalSpacing_B or Prd_DNA")

cmd.save(f"{Prd}w{ANTP}_helicalSpacing.cif", f"{Prd}w{ANTP}_helicalSpacing", format = "cif")