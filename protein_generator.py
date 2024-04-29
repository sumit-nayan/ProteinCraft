import random
import subprocess
import os
import zipfile
def generate_protein_data(num_lines, exclude_aa, num_models):
    zip_series = 1
    while True:
        zip_filename = f"Result/protein{zip_series}.zip"
        if not os.path.exists(zip_filename):
            break
        zip_series += 1

    os.makedirs("Result", exist_ok=True)  # Create Result folder if it doesn't exist

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for i in range(num_models):
            filename = f"random_protein_data_{i}.rib"
            with open(filename, "w") as outfile:
                outfile.write("TITLE RIBOSOME 1\n")
                model_data = generate_model(num_lines, exclude_aa)
                for line in model_data:
                    outfile.write("{}\n".format(line))

            try:
                subprocess.run(["./ribosome", filename, f"output_{i}.pdb", "res.zmat"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error generating .pdb file for model {i}: {e}")
                continue

            if os.path.exists(f"output_{i}.pdb"):
                zipf.write(f"output_{i}.pdb")
                os.remove(f"output_{i}.pdb")
            else:
                print(f"Warning: .pdb file for model {i} not found.")

            os.remove(filename)

    # Write summary information
    with open("Result/summary.txt", "w") as summary_file:
        summary_file.write(f"File Name: {zip_filename}\n")
        summary_file.write(f"Number of Protein Excluded: {len(exclude_aa)}\n")
        summary_file.write(f"Number of Files: {num_models}\n")
        summary_file.write(f"Number of Models: {num_models}\n")

    return zip_filename
    

def pick_random_phi_psi():
    PHI_RANGE1 = (-180,-40)
    PHI_RANGE2 = (40,100)

    if random.random() < 0.5:
        phi = random.uniform(PHI_RANGE1[0], PHI_RANGE1[1])
    else:
        phi = random.uniform(PHI_RANGE2[0], PHI_RANGE2[1])

    if random.random() < 0.5:
        psi = random.uniform(PSI_RANGE[0], PSI_RANGE[1])
    else:
        psi = random.uniform(PSI_RANGE_2[0], PSI_RANGE_2[1])

    return round(phi,2), round(psi,2)

def generate_line(aa_list):
    res_aa = random.choice(aa_list)
    phi, psi = pick_random_phi_psi()
    return "res {} phi {} psi {}".format(res_aa, phi, psi)

def generate_model(num_lines, exclude_aa):
    aa_list = [AA_CODES[aa] for aa in AA_CODES if aa not in exclude_aa]
    model_data = []
    for _ in range(num_lines):
        model_data.append(generate_line(aa_list))
    return model_data


    
PHI_RANGE = (-135, 135)
PSI_RANGE = (-45, 45)
PSI_RANGE_2 = (-90, -150)

AA_CODES = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS", 
    "Q": "GLN", "E": "GLU", "G": "GLY", "H": "HIS", "I": "ILE", 
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO", 
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL",
}

