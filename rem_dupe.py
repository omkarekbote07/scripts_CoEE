from Bio import SeqIO

def remove_duplicates(input_fasta, output_fasta):
    sequences = {}
    for record in SeqIO.parse(input_fasta, "fasta"):
        seq = str(record.seq)
        if seq not in sequences:
            sequences[seq] = record

    with open(output_fasta, "w") as output_handle:
        SeqIO.write(sequences.values(), output_handle, "fasta")

if __name__ == "__main__":
    input_fasta = "/home/snu/Desktop/proj_omkar/test_for_rem_dupe.fasta"  # replace with your input file path
    output_fasta = "/home/snu/Desktop/proj_omkar/test_for_rem_dupe_out.fasta"  # replace with your desired output file path
    remove_duplicates(input_fasta, output_fasta)