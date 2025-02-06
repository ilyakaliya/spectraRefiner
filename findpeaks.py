import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from peaks import Spectrum

def find_peaks_in_region(wavelengths, intensities, start_wl, end_wl, prominence=1000, distance=5):
    """Find peaks in a defined spectral region."""
    
    # Crop the spectrum to the selected region
    mask = (wavelengths >= start_wl) & (wavelengths <= end_wl)
    cropped_wl = wavelengths[mask]
    cropped_int = intensities[mask]

    # Find peaks in the cropped region
    peaks, properties = signal.find_peaks(cropped_int, prominence=prominence, distance=distance)

    # Return peak positions in the original wavelength scale
    return cropped_wl[peaks[0]+cropped_wl.index[0]], cropped_int[peaks[0]+cropped_int.index[0]]

# # Simulated discrete spectrum
# x = np.linspace(400, 800, 500)  # Wavelengths
# y = np.exp(-((x - 600) / 30) ** 2) + 0.1 * np.random.rand(len(x))  # Gaussian peak with noise

spectrum = Spectrum('/Users/ilyakaliya/Documents/spectra_refiner/data/raw/17_D2_633nm_x50LF_P5_1a_10s_77K_lum.txt')

# Find peaks with prominence filtering
peaks, properties = find_peaks_in_region(spectrum.wavelengths, spectrum.intensities, 680,700)
print(properties)
print(type(properties))

# Plot
plt.plot(spectrum.wavelengths, spectrum.intensities, label="Spectrum")
plt.plot(peaks, properties, "ro", label="Detected Peaks")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.legend()
plt.show()