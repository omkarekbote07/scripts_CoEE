from Bio import SeqIO
import re

# File paths
accession_file = "/home/snu/Desktop/proj_omkar/satb1_curated_tree/accessions.txt"  # File containing the accession IDs
fasta_file = "/home/snu/Desktop/proj_omkar/satb1_curated_tree/combined_remdupe_satb1.fasta"  # Original FASTA file
output_file = "/home/snu/Desktop/proj_omkar/satb1_curated_tree/seq_satb1_curated.fasta"  # Output file for extracted sequences

# Read the accession IDs into a set
with open(accession_file, 'r') as f:
    accession_ids = set(line.strip() for line in f)


# 1. XP_015910068.1 (starts with letters, followed by numbers and optional version)
# 2. GFT99095.1 (starts with letters, followed by numbers and optional version)
# 3. CAL1288737.1 (starts with letters, followed by numbers and optional version)
# 4. ur|UPI001C4B90BE| (starts with "ur|", followed by letters and numbers)
# 5. ur|A0A803STW1| (starts with "ur|", followed by letters and numbers)
# 6. sp|Q01826| (starts with "sp|", followed by letters and numbers)
accession_pattern = re.compile(r'^>?(?:sp\|([A-Za-z0-9]+)\||ur\|([A-Za-z0-9]+)\||([A-Za-z0-9]+\.[0-9]+))')

# Open the output file for writing
with open(output_file, 'w') as out_f:
    # Parse the original FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Extract the accession ID from the header using the regex pattern
        match = accession_pattern.search(record.description)
        if match:
            # The regex has 3 capturing groups, so we need to find the non-None group
            header_id = next((group for group in match.groups() if group), None)
            
            # Check if the extracted ID is in the set of accession IDs
            if header_id in accession_ids:
                # Write the record to the output file
                SeqIO.write(record, out_f, "fasta")

print(f"Extracted sequences have been saved to {output_file}")
