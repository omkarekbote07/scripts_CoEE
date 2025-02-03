import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def extract_hit_sequences(blast_file, nuc_fasta, output_fasta):
    # Load the nucleotide sequences into a dictionary keyed by sequence ID
    nuc_records = SeqIO.to_dict(SeqIO.parse(nuc_fasta, "fasta"))
    extracted_records = []

    with open(blast_file) as f:
        for line in f:
            # Skip comment lines (if any) or empty lines
            if line.startswith("#") or not line.strip():
                continue
            
            # Split the line by whitespace; we expect the following columns:
            # 1. query id
            # 2. subject id (e.g. CR936560.6)
            # 3. % identity
            # 4. alignment length
            # 5. mismatches
            # 6. gap opens
            # 7. query start
            # 8. query end
            # 9. subject start (sstart)
            # 10. subject end (send)
            # 11. evalue
            # 12. bitscore
            fields = line.strip().split()
            if len(fields) < 10:
                continue  # skip if not enough columns

            query_id = fields[0]
            subject_id = fields[1]
            try:
                sstart = int(fields[8])
                send = int(fields[9])
            except ValueError:
                print(f"Error parsing coordinates in line:\n{line}")
                continue

            # Check if subject_id is present in the nucleotide FASTA file
            if subject_id not in nuc_records:
                print(f"Subject {subject_id} not found in {nuc_fasta}. Skipping hit.")
                continue

            # Get the full nucleotide sequence for this subject
            subject_record = nuc_records[subject_id]
            seq = subject_record.seq

            # Determine the region to extract 
            start = min(sstart, send)
            end = max(sstart, send)
            extracted_seq = seq[start - 1:end]

          
            if sstart > send:
                extracted_seq = extracted_seq.reverse_complement()

          
            record_id = f"{subject_id}_{sstart}_{send}"
            description = f"Hit from {query_id} extracted from {subject_id} positions {sstart} to {send}"
            extracted_record = SeqRecord(extracted_seq, id=record_id, description=description)
            extracted_records.append(extracted_record)
    
    # Write all extracted sequences to the output FASTA file
    with open(output_fasta, "w") as out_handle:
        SeqIO.write(extracted_records, out_handle, "fasta")
    
    print(f"Extracted {len(extracted_records)} sequences to {output_fasta}")

if __name__ == "__main__":
    # Modify these filenames as needed:
    blast_file = "/home/snu/Desktop/proj_omkar/phylo_analysis/nucleotide_zone/tblastn_danrer.txt"         # Your BLAST output file (with the format similar to your posted lines)
    nucleotide_fasta = "/home/snu/Desktop/proj_omkar/phylo_analysis/nucleotide_zone/danrer_nuc_check.fasta"  # Your long nucleotide FASTA file containing CR936560.6
    output_fasta = "extracted_hits_danrer.fasta"  # The output file where extracted sequences will be saved

    extract_hit_sequences(blast_file, nucleotide_fasta, output_fasta)
