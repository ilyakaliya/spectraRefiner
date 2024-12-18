import pandas as pd
from scipy.signal import find_peaks

def find_peaks(input_file, output_dir):
    """Find peaks and save results for each spectrum."""
    data = pd.read_csv(input_file)
    unique_metadata = data['Metadata'].drop_duplicates()
    
    for metadata in unique_metadata:
        spectrum = data[data['Metadata'] == metadata]
        peaks, properties = find_peaks(spectrum['Corrected_Intensity'], height=10, distance=5)
        peaks_data = spectrum.iloc[peaks]
        
        # Save peaks for this spectrum
        sample_name = metadata['sample']
        output_file = f"{output_dir}/{sample_name}_{metadata['excitation']}_{metadata['spectrumType']}_{metadata['temperature']}K.txt"
        peaks_data.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    find_peaks(input_file, output_dir)