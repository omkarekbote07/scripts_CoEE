from Bio import SeqIO
import os
from collections import defaultdict

# File paths
fasta_file = "/DATA/proj_omkar/domain_output/satb2_individual_domains/satb2_cladwise_combined.fasta"
hmmer_file = "/DATA/proj_omkar/domain_output/satb2_individual_domains/satb2_cladewise_domains.txt"
output_dir = "/DATA/proj_omkar/domain_output"  # Specify the output directory

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Check if the FASTA file exists
if not os.path.isfile(fasta_file):
    raise FileNotFoundError(f"FASTA file not found: {fasta_file}")

# Check if the HMMER file exists
if not os.path.isfile(hmmer_file):
    raise FileNotFoundError(f"HMMER file not found: {hmmer_file}")

# Parse HMMER output and extract domain coordinates
domain_coordinates = []
with open(hmmer_file, "r") as hmmer:
    for line in hmmer:
        if not line.startswith("#") and line.strip():
            fields = line.split()
            query_name = fields[3]
            domain_name = fields[0]
            domain_start = int(fields[19])
            domain_end = int(fields[20])
            domain_coordinates.append((query_name, domain_name, domain_start, domain_end))

# Parse FASTA file and extract domain sequences
fasta_sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

# Group and concatenate domain sequences for each query
concatenated_sequences = defaultdict(str)

for query_name, domain_name, start, end in domain_coordinates:
    if query_name in fasta_sequences:
        sequence = fasta_sequences[query_name].seq[start - 1:end]  # Adjust for 1-based indexing
        concatenated_sequences[query_name] += str(sequence)  # Concatenate domain sequences

# Write concatenated sequences into a single FASTA file
output_file = os.path.join(output_dir, "concatenated_domains.fasta")
with open(output_file, "w") as out_f:
    for query_name, concatenated_sequence in concatenated_sequences.items():
        out_f.write(f">{query_name}\n{concatenated_sequence}\n")

print(f"Saved concatenated sequences to {output_file}")
