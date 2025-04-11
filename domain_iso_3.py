from Bio import SeqIO
import os
from collections import defaultdict

# File paths
fasta_file = "/DATA/proj_omkar/domain_output/satb1_individual_domains/satb1_combined_cladewise.fasta"
hmmer_file = "//DATA/proj_omkar/domain_output/satb1_individual_domains/satb1_cladewise_domains.txt"
output_dir = "/DATA/proj_omkar/domain_output/satb1_individual_domains"  # Specify the output directory

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

# Group sequences by domain and track counts for each domain per query
domain_sequences = defaultdict(list)
domain_counts = defaultdict(lambda: defaultdict(int))  # Track counts of domains per query

for query_name, domain_name, start, end in domain_coordinates:
    if query_name in fasta_sequences:
        sequence = fasta_sequences[query_name].seq[start - 1:end]  # Adjust for 1-based indexing
        # Increment domain count for this query
        domain_counts[query_name][domain_name] += 1
        domain_suffix = domain_counts[query_name][domain_name]
        # Add suffix to domain name (e.g., CUT1, CUT2)
        domain_name_with_suffix = f"{domain_name}{domain_suffix}"
        header = f"{query_name}|{domain_name_with_suffix}|{start}-{end}"
        domain_sequences[domain_name_with_suffix].append((header, sequence))

# Write all sequences for each domain into a single FASTA file
for domain_name, sequences in domain_sequences.items():
    output_file = os.path.join(output_dir, f"{domain_name}.fasta")
    with open(output_file, "w") as out_f:
        for header, sequence in sequences:
            out_f.write(f">{header}\n{sequence}\n")
    print(f"Saved {len(sequences)} sequences to {output_file}")