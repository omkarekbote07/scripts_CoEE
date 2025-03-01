
def create_traits_file(input_file, output_file):
    
    domain_data = {}
    with open(input_file, "r") as pfam_file:
        for line in pfam_file:
            if line.startswith("#"):
                continue  
            fields = line.strip().split()
            species = fields[3]  # Query ID
            domain = fields[0]    # Domain name
            if species not in domain_data:
                domain_data[species] = set()
            domain_data[species].add(domain)

    # Step 2: List all unique domains
    all_domains = sorted({domain for domains in domain_data.values() for domain in domains})
    
    with open(output_file, "w") as traits_file:
        
        traits_file.write("Species\t" + "\t".join(all_domains) + "\n")
    
        for species, domains in domain_data.items():
            traits = [species] + ["1" if domain in domains else "0" for domain in all_domains]
            traits_file.write("\t".join(traits) + "\n")

    print(f"Traits file saved to {output_file}")

# Main program
if __name__ == "__main__":
    input_file = 'HMM/seq_satb1_curated_hits_2.txt'
    output_file = 'HMM/seq_satb1_curated_traits_2.txt'
    create_traits_file(input_file, output_file)