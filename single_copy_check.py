import os

# Corrected path to BUSCO outputs
parent_dir = "/DATA/proj_omkar/july/taxonomy/genomes/all_gen/busco_outputs"
common_buscos = None
total_folders_processed = 0
skipped_folders = []

for genome_folder in os.listdir(parent_dir):
    genome_path = os.path.join(
        parent_dir, genome_folder,
        "run_metazoa_odb10", "busco_sequences", "single_copy_busco_sequences"  # ✅ fixed here
    )

    if not os.path.isdir(genome_path):
        skipped_folders.append(genome_folder)
        print(f"Skipping {genome_folder} (missing single_copy folder)")
        continue

    gene_files = [f for f in os.listdir(genome_path) if f.endswith(".faa")]
    busco_genes = set(f.split(".")[0] for f in gene_files)

    print(f"Processed {genome_folder}: Found {len(busco_genes)} BUSCO genes")

    if not busco_genes:
        print(f" Warning: No genes found in {genome_folder}")
        continue

    if common_buscos is None:
        common_buscos = busco_genes
    else:
        common_buscos &= busco_genes

    total_folders_processed += 1

# Final report
if common_buscos:
    output_file = "/DATA/proj_omkar/july/taxonomy/genomes/all_gen/common_busco_genes.txt"
    with open(output_file, "w") as out:
        for gene in sorted(common_buscos):
            out.write(gene + "\n")
    print(f"\n Saved {len(common_buscos)} common BUSCO gene names to '{output_file}'")
    print(f" Processed {total_folders_processed} genomes.")
else:
    print("\n No common BUSCO genes found across genomes.")

if skipped_folders:
    print(f"\n Skipped {len(skipped_folders)} genome folders (missing BUSCO output):")
    for name in skipped_folders:
        print(f"  - {name}")
