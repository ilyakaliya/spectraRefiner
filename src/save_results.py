def save_peaks_to_csv(peaks_data, output_path):
    """Saves all peaks data into a CSV file."""
    peaks_data.to_csv(output_path, index=False)
