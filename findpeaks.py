import numpy as np
import scipy.signal as signal
from matplotlib import pyplot as plt

def find_peaks_in_region(wavelengths, intensities, start_wl, end_wl, prominence=0.1, distance=5):
    """Find peaks in a defined spectral region."""
    
    # Crop the spectrum to the selected region
    mask = (wavelengths >= start_wl) & (wavelengths <= end_wl)
    cropped_wl = wavelengths[mask]
    cropped_int = intensities[mask]

    # Find peaks in the cropped region
    peaks, properties = signal.find_peaks(cropped_int, prominence=prominence, distance=distance)

    # Return peak positions in the original wavelength scale
    return cropped_wl[peaks], cropped_int[peaks]

# Simulated spectrum
wavelengths = np.linspace(400, 800, 500)  # Wavelength range
intensities = np.exp(-((wavelengths - 600) / 30) ** 2) + 0.1 * np.random.rand(500)  # Gaussian peak with noise

# Define the spectral region (e.g., 500-700 nm)
start_wl, end_wl = 500, 700

# Find peaks in this region
peaks_wl, peaks_int = find_peaks_in_region(wavelengths, intensities, start_wl, end_wl)

# Print detected peaks
print("Peaks found at:", peaks_wl)

# Plot
plt.plot(x, y, label="Spectrum")
plt.plot(x[peaks_wl], y[peaks_int], "ro", label="Detected Peaks")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.legend()
plt.show()