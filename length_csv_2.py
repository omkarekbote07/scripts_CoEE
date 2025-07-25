import os
import csv

def get_species_list(file_path):
    """
    Reads a list of species from a text file, with one species name per line.
    Returns a list of species names.
    """
    if not os.path.exists(file_path):
        print(f" Error: Species file not found at '{file_path}'. Cannot continue.")
        return None
        
    try:
        with open(file_path, 'r') as f:
            # Read each line, strip whitespace, and ignore any empty lines
            species = [line.strip() for line in f if line.strip()]
        print(f"  Found {len(species)} species to process from '{os.path.basename(file_path)}'.")
        return species
    except Exception as e:
        print(f" Error reading species file: {e}")
        return None

def parse_fasta(file_path):
    """
    Parses a FASTA file and returns a dictionary of {header: sequence}.
    Handles file not found errors gracefully.
    """
    sequences = {}
    try:
        with open(file_path, 'r') as f:
            current_header = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    current_header = line
                    sequences[current_header] = ''
                elif current_header:
                    sequences[current_header] += line
    except FileNotFoundError:
        # This warning is expected if a domain file is intentionally missing
        print(f"  - ℹ  Info: File not found: {file_path}. This column will have 0s.")
        return {}
    print(f"  -   Loaded {file_path}")
    return sequences

def create_sequence_length_csv():
    """
    Generates a CSV file with sequence lengths. It reads the species list from a 
    user-specified text file and automatically finds corresponding FASTA files
    in the same directory as the script.
    """
    print("--- Sequence Length CSV Generator ---")
    
    # --- Get path to the species list file ---
    species_file_path = input("Enter the path to your species list text file:/DATA/proj_omkar/july/analysis/species_list.txt")
    species_to_process = get_species_list(species_file_path)
    
    # If the species file wasn't found or was empty, stop the script.
    if not species_to_process:
        return

    # These are the columns for the output CSV file.
    # The script automatically derives the required FASTA filenames from this list.
    csv_columns = [
        "Species", "SATB1", "SATB2", "ULD1_satb1", "ULD1_satb2", "CUT1_satb1",
        "CUT1_satb2", "CUT2_satb1", "CUT2_satb2", "CUTL1_satb1", "CUTL2_satb2",
        "Homeodomain1_satb1", "Homeodomain1_satb2", "IS0_satb1", "IS0_satb2",
        "IS1_satb1", "IS1_satb2", "IS3_satb1", "IS3_satb2", "IS4_satb1",
        "IS4_satb2", "IS5_satb1", "IS5_satb2"
    ]

    output_csv_filename = 'sequence_domain_lengths.csv'

    # --- SCRIPT LOGIC ---
    
    # Pre-load all FASTA data into memory from the local directory
    print("\n--- Loading all FASTA files from the script's directory ---")
    all_fasta_data = {
        col: parse_fasta(f"{col}.fasta") for col in csv_columns[1:]
    }
    print("-" * 30)

    # Create and write to the CSV file
    with open(output_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)  # Write the header row

        print(f"Processing {len(species_to_process)} species...")
        # Iterate over each species to create a row in the CSV
        for species in species_to_process:
            row_data = [species]
            # Iterate through each column type (domain/interspace)
            for col_name in csv_columns[1:]:
                length = 0  # Default to 0 if not found
                # Search for the species in the pre-loaded data for this column
                for header, sequence in all_fasta_data.get(col_name, {}).items():
                    if species in header:
                        length = len(sequence)
                        break  # Found the sequence, move to the next column
                row_data.append(length)

            writer.writerow(row_data) # Write the completed row for the species

    print("-" * 30)
    print(f" Success! Your file '{output_csv_filename}' has been created.")


if __name__ == '__main__':
    create_sequence_length_csv()
