import os
from pathlib import Path

# Set the directory containing the 48 .faa files
input_dir = Path("/DATA/proj_omkar/july/taxonomy/scg_with_hydra")  

# Get all .faa files and sort them (to ensure consistent order)
faa_files = sorted(input_dir.glob("*.faa"))

# Sanity check
if len(faa_files) != 44:
    print(f"Expected 48 files, found {len(faa_files)}. Aborting.")
else:
    for i, file_path in enumerate(faa_files, start=1):
        new_name = input_dir / f"gene_{i}.fasta"
        file_path.rename(new_name)
        print(f"Renamed: {file_path.name} → gene_{i}.fasta")
