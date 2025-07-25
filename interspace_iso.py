from Bio import SeqIO
from collections import defaultdict
import os

# STEP 1: Parse HMMER domain table output
def parse_domtblout(filepath):
    coords = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            seq_id = fields[3]  # Query name
            aln_start = int(fields[17])  # Alignment start
            aln_end = int(fields[18])    # Alignment end
            coords[seq_id].append((aln_start, aln_end))
    return coords

# STEP 2: Extract interspaces and flanking regions
def extract_interspaces_grouped(fasta_file, domain_coords, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    seqs = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    interspace_groups = defaultdict(list)  # Group interspaces by their position (IS1, IS2, etc.)

    for seq_id, coords in domain_coords.items():
        if seq_id not in seqs:
            continue

        seq = seqs[seq_id].seq
        coords.sort()

        # Extract region before the first domain
        if coords[0][0] > 1:
            interspace_start = 1
            interspace_end = coords[0][0] - 1
            interspace_seq = seq[interspace_start - 1:interspace_end]
            interspace_len = len(interspace_seq)
            interspace_id = "BeforeFirstDomain"
            interspace_groups[interspace_id].append((seq_id, interspace_seq, interspace_len, interspace_start, interspace_end))

        # Extract interspaces between domains
        for i in range(len(coords) - 1):
            end_prev = coords[i][1]  # End of the current domain
            start_next = coords[i + 1][0]  # Start of the next domain

            if start_next > end_prev + 1:
                interspace_start = end_prev + 1
                interspace_end = start_next - 1
                interspace_seq = seq[interspace_start - 1:interspace_end]
                interspace_len = len(interspace_seq)
                interspace_id = f"IS{i + 1}"
                interspace_groups[interspace_id].append((seq_id, interspace_seq, interspace_len, interspace_start, interspace_end))

        # Extract region after the last domain
        if coords[-1][1] < len(seq):
            interspace_start = coords[-1][1] + 1
            interspace_end = len(seq)
            interspace_seq = seq[interspace_start - 1:interspace_end]
            interspace_len = len(interspace_seq)
            interspace_id = "AfterLastDomain"
            interspace_groups[interspace_id].append((seq_id, interspace_seq, interspace_len, interspace_start, interspace_end))

    # Write grouped interspaces to separate files
    for interspace_id, interspaces in interspace_groups.items():
        out_filename = os.path.join(output_dir, f"{interspace_id}.fasta")
        with open(out_filename, "w") as out_f:
            for seq_id, interspace_seq, interspace_len, interspace_start, interspace_end in interspaces:
                out_f.write(f">{seq_id}_{interspace_id} len={interspace_len} start={interspace_start} end={interspace_end}\n{interspace_seq}\n")
        print(f"Wrote {out_filename} with {len(interspaces)} interspaces.")

# MAIN
domain_file = "/DATA/proj_omkar/july/analysis/satb2_ext_out.txt"
fasta_file = "/DATA/proj_omkar/july/analysis/ext_satb2.fasta"
output_dir = "/DATA/proj_omkar/july/analysis/satb2_interspaces"  # Specify your output directory here

domain_coords = parse_domtblout(domain_file)
extract_interspaces_grouped(fasta_file, domain_coords, output_dir)