import pandas as pd
import numpy as np
from pathlib import Path
import os

def subtract_baseline(data, method="polynomial", **kwargs):
    """Subtract baseline from spectral data using specified method."""
    if method == "polynomial":
        degree = kwargs.get("degree", 3)
        baseline_values = pd.Series(data["intensity"]).rolling(degree).mean()
        data["intensity"] -= baseline_values.fillna(0)
    elif method == "asymmetric_least_squares":
        # Placeholder for ALSS method implementation
        pass
    else:
        raise ValueError(f"Unsupported baseline method: {method}")
    return data

def crop_spectral_region(data, start, end):
    """Crop the spectral profile to the selected spectral region."""
    return data[(data["wavelength"] >= start) & (data["wavelength"] <= end)]

def process_spectra(input_dir, output_dir, crop_region=None, baseline_method=None, **baseline_kwargs):
    """Load spectra from .txt files, process them, and save as .csv files."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    cropped_dir = output_dir / "cropped"
    cropped_dir.mkdir(parents=True, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            file_path = input_dir / file_name 

            # Load the spectral data
            try:
                data = pd.read_csv(file_path)
                print(type(eval(data["metadata"][0])['sample'])) # need to turn str to dict!!! to later add cropped files!!! do tmrw
            except Exception as e:
                print(f"Failed to load file {file_name}: {e}")
                continue

            # Subtract baseline if requested
            if baseline_method:
                data = subtract_baseline(data, method=baseline_method, **baseline_kwargs)

            # Crop spectral region if requested
            if crop_region:
                start, end = crop_region
                data = crop_spectral_region(data, start, end)

            # Create output folder for the sample
            sample_folder = cropped_dir / eval(data["metadata"][0])['sample']
            sample_folder.mkdir(parents=True, exist_ok=True)

            # Save processed data as .csv
            spectrum_type = eval(data["metadata"][0])['spectrumType']
            temperature = eval(data["metadata"][0])['temperature']
            output_file = sample_folder / f"{spectrum_type}_{temperature}_cropped.csv"
            data.to_csv(output_file, index=False)
            print(f"Processed {file_name} -> {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python process.py <input_dir> <output_dir> [start] [end] [baseline_method]")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    crop_start = float(sys.argv[3]) if len(sys.argv) > 3 else None
    crop_end = float(sys.argv[4]) if len(sys.argv) > 4 else None
    baseline_method = sys.argv[5] if len(sys.argv) > 5 else None

    crop_region = (crop_start, crop_end) if crop_start and crop_end else None

    process_spectra(input_directory, output_directory, crop_region=crop_region, baseline_method=baseline_method)