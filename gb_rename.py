from pathlib import Path
from Bio import SeqIO

# Set the directory containing Gblocks output files
input_dir = Path("/DATA/proj_omkar/july/taxonomy/44_aln/44_gb_out")  # replace with your actual path

# Process each Gblocks-trimmed file
for file in input_dir.glob("gene_*.fasta-gb"):
    # Read all sequences (there might be multiple)
    sequences = list(SeqIO.parse(file, "fasta"))
    
    if not sequences:
        print(f"No sequences found in {file.name}")
        continue

    # Assuming all sequences are the same length after alignment
    # If not, take average or max/min as needed
    seq_length = len(sequences[0].seq)

    # Rename file with new length-based name
    new_filename = file.with_name(f"{file.stem.split('.')[0]}_len{seq_length}.fasta")
    file.rename(new_filename)

    print(f"Renamed {file.name} → {new_filename.name}")
