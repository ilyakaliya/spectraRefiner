import os
import pandas as pd
import re
from pathlib import Path

def parse_filename(file_name):
    """Extract metadata from the file name."""
    pattern = r"(?P<sample>.+?)_(?P<excitation>\d+nm)_(?P<spectrumType>PL|Raman)_(?P<temperature>\d+K).txt"
    match = re.match(pattern, file_name)
    if match:
        return match.groupdict()
    else:
        raise ValueError(f"Filename '{file_name}' does not match the expected pattern.")

def process_spectra(input_dir, output_dir):
    """Load spectra from .txt files, process them, and save as .csv files."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            file_path = input_dir / file_name

            # Parse metadata from the file name
            try:
                metadata = parse_filename(file_name)
            except ValueError as e:
                print(e)
                continue

            # Load the spectral data
            try:
                data = pd.read_csv(file_path, sep='\t', header=None, names=['wavelength', 'intensity'])
            except Exception as e:
                print(f"Failed to load file {file_name}: {e}")
                continue

            # Add metadata as a column
            data['metadata'] = str(metadata)

            # Create output folder for the sample
            sample_folder = output_dir / metadata['sample']
            sample_folder.mkdir(parents=True, exist_ok=True)

            # Save processed data as .csv
            spectrum_type = metadata['spectrumType']
            output_file = sample_folder / f"{spectrum_type}_{metadata['temperature']}.csv"
            data.to_csv(output_file, index=False)
            print(f"Processed {file_name} -> {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python process_spectra.py <input_dir> <output_dir>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    process_spectra(input_directory, output_directory)