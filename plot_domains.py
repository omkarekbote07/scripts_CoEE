import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict


hmmscan_file = "/home/snu/Desktop/proj_omkar/HMM/satb2_seq_domains.txt"  # Change this if your filename is different

# Dictionary to store domain data {sequence_id: [(domain_name, start, end, color)]}
sequences = defaultdict(list)
protein_lengths = {}

# Assign colors to domains
domain_colors = {
    "CUTL": "red",
    "CUT": "blue",
    "ULD": "green",
    "Homeodomain": "purple"
}

# Read the hmmscan output file
with open(hmmscan_file, "r") as f:
    for line in f:
        if line.startswith("#") or not line.strip():  # Skip comments and empty lines
            continue
        fields = line.strip().split()
        
        if len(fields) < 19:  # Ensure we have enough columns
            continue
        
        domain_name = fields[0]  
        query_name = fields[3]   
        start = int(fields[15])  
        end = int(fields[16])   
        
        protein_lengths[query_name] = max(protein_lengths.get(query_name, 0), end)

        color = domain_colors.get(domain_name, "gray")  
        
        sequences[query_name].append((domain_name, start, end, color))

for query_name, domains in sequences.items():
    protein_length = protein_lengths[query_name]

    fig, ax = plt.subplots(figsize=(12, 2))
    ax.set_xlim(0, protein_length)
    ax.set_ylim(0, 1)

    # Draw the protein backbone
    ax.hlines(0.5, 0, protein_length, color="black", linewidth=3)

    # Draw the domains as colored blocks
    for domain, start, end, color in domains:
        ax.add_patch(mpatches.Rectangle((start, 0.35), end - start, 0.3, color=color))
        ax.text((start + end) / 2, 0.7, domain, ha='center', va='bottom', fontsize=10)


    label_position = (start + end) / 2
    label_offset = 0.1  # Increase if labels overlap more
    ax.text(label_position, 0.7 + label_offset, domain, ha='center', va='bottom', fontsize=8, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.axis("off")
    plt.title(f"{query_name} Protein Domain Structure")
    
    output_file = f"{query_name}_domains.png"  
    plt.savefig(output_file, dpi=300)  
    plt.close()
