def edit_fasta(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                part = line.split('>')
                line = part[1]
                parts = line.split('[')
                accession = parts[0].strip()
                scientific_name = parts[1].split(']')[0]
                outfile.write(f">{scientific_name} {accession}\n")
            else:
                outfile.write(line)

# Usage
input_file = '/home/snu/Desktop/proj_omkar/aligned.fasta'
output_file = '/home/snu/Desktop/proj_omkar/aligned_edited.fasta'
edit_fasta(input_file, output_file)