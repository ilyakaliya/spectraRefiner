import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
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

# Simulated discrete spectrum
x = np.linspace(400, 800, 500)  # Wavelengths
y = np.exp(-((x - 600) / 30) ** 2) + 0.1 * np.random.rand(len(x))  # Gaussian peak with noise

# Find peaks with prominence filtering
peaks, properties = find_peaks_in_region(x, y,500,700)

# Plot
plt.plot(x, y, label="Spectrum")
plt.plot(peaks[0], properties[0], "ro", label="Detected Peaks")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.legend()
plt.show()

print(peaks)
print(properties)