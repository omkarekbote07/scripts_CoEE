# Re-import required modules after code execution environment was reset
from collections import Counter
import pandas as pd

# Load the uploaded file again
fasta_path = "/DATA/proj_omkar/ens_orthos_NEW/clade-wise/satb1/satb1_combined_cladewise_aligned.fasta"

# Parse FASTA file
sequences = {}
with open(fasta_path) as f:
    lines = f.read().splitlines()

current_id = ""
for line in lines:
    if line.startswith(">"):
        current_id = line[1:].strip()
        sequences[current_id] = ""
    else:
        sequences[current_id] += line.strip()

# Extract clade info and sequences
parsed_data = []
for header, seq in sequences.items():
    clade = header.split("_")[0]  # Assumes format like "Mammal_Human" or "Fish_Zebrafish"
    parsed_data.append({
        "header": header,
        "clade": clade,
        "sequence": seq
    })

# Convert to DataFrame
seq_df = pd.DataFrame(parsed_data)
seq_df.head()
# Clean and simplify clade names (e.g., "amphibian|Ambystoma" → "amphibian")
seq_df["clean_clade"] = seq_df["clade"].apply(lambda x: x.split("|")[0].lower())

# Get number of sequences and alignment length
alignment_len = len(seq_df.iloc[0]["sequence"])
num_sequences = len(seq_df)

# Group sequences by clade
clade_groups = seq_df.groupby("clean_clade")["sequence"].apply(list).to_dict()

# Analyze per-position amino acid differences by clade
position_differences = []
for i in range(alignment_len):
    position_info = {"Position": i + 1}
    aa_by_clade = {}
    
    for clade, seqs in clade_groups.items():
        aas = [seq[i] for seq in seqs]
        aa_counts = Counter(aas)
        most_common_aa = aa_counts.most_common(1)[0][0] if aa_counts else "-"
        aa_by_clade[clade] = most_common_aa
    
    unique_aas = set(aa_by_clade.values()) - set("-")
    
    # Only keep positions with different AAs across clades
    if len(unique_aas) > 1:
        position_info.update(aa_by_clade)
        position_info["Num_Diff_Clades"] = len(unique_aas)
        position_differences.append(position_info)

# Convert to DataFrame and preview
clade_diff_df = pd.DataFrame(position_differences)
clade_diff_df.head(10)

# Convert to DataFrame and preview
clade_diff_df = pd.DataFrame(position_differences)

# Save the output to a CSV file
output_path = "//DATA/proj_omkar/ens_orthos_NEW/clade-wise/satb1/satb1_cladewise_align_diff.csv"
clade_diff_df.to_csv(output_path, index=False)

# Optionally print a message to confirm the file was saved
print(f"Output saved to {output_path}")

