import os

# Path to the directory containing BUSCO output folders (named after organisms)
parent_dir = "/DATA/proj_omkar/july/taxonomy/genomes/all_gen/busco_outputs"

# Directory to save output .txt files
output_dir = "/DATA/proj_omkar/july/taxonomy/genomes/all_gen/busco_outputsgene_lists"
os.makedirs(output_dir, exist_ok=True)

# Loop through each organism folder
for genome_folder in os.listdir(parent_dir):
    single_copy_dir = os.path.join(
        parent_dir, genome_folder,
        "run_metazoa_odb10", "busco_sequences", "single_copy_busco_sequences"
    )

    if not os.path.isdir(single_copy_dir):
        print(f"Skipping {genome_folder} — single_copy_busco_sequences not found.")
        continue

    gene_files = sorted(f for f in os.listdir(single_copy_dir) if f.endswith(".faa"))

    # Create a text file named after the organism folder
    output_file = os.path.join(output_dir, f"{genome_folder}.txt")
    with open(output_file, "w") as f:
        for gene_file in gene_files:
            f.write(gene_file + "\n")

    print(f" Saved {len(gene_files)} gene names to {output_file}")
