import os
from pathlib import Path

# Paths and files
root_dir = Path('/DATA/proj_omkar/july/taxonomy/genomes/all_gen/busco_outputs')  # Folder containing all 94 organism folders
gene_list_file = '/DATA/proj_omkar/july/taxonomy/scg_list.txt'  # List of 48 genes (with .faa extension)
output_dir = Path('/DATA/proj_omkar/july/taxonomy/scg_with_hydra')
output_dir.mkdir(exist_ok=True)

# Load the list of required genes
with open(gene_list_file) as f:
    required_genes = {line.strip() for line in f}

# Initialize output gene files
gene_to_sequences = {gene: [] for gene in required_genes}

# Iterate through each organism folder
for organism_folder in root_dir.iterdir():
    if not organism_folder.is_dir():
        continue

    organism = organism_folder.name
    seq_dir = organism_folder / 'run_metazoa_odb10' / 'busco_sequences' / 'single_copy_busco_sequences'
    
    if not seq_dir.exists():
        print(f"Skipping {organism}, path doesn't exist")
        continue

    # For each required gene, check if it exists
    for gene in required_genes:
        gene_path = seq_dir / gene
        if gene_path.exists():
            with open(gene_path) as f:
                lines = f.readlines()
            
            # Replace header with organism name
            new_lines = []
            for line in lines:
                if line.startswith('>'):
                    new_lines.append(f'>{organism}\n')
                else:
                    new_lines.append(line)
            gene_to_sequences[gene].extend(new_lines)
        else:
            print(f"{gene} missing in {organism}")

# Write output files
for gene, sequences in gene_to_sequences.items():
    with open(output_dir / gene, 'w') as out_f:
        out_f.writelines(sequences)
