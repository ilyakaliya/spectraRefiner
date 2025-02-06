from matplotlib import pyplot as plt
import pandas as pd
import scipy.signal as signal
import re

class Spectrum:

  def __init__(self, path
               ):
    self.filename = path.split("/")[-1]
    self.sample_name = self.filename.split("_")[1]
    self.substrate = self.filename.split("_")[2]
    self.exc_power = self.filename.split("_")[5]
    self.exc_wavelength = int(re.search(r'(\d+)nm', self.filename).group(1))
    self.acquisition_number = self.filename.split("_")[-4]
    self.acquisition_time = self.filename.split("_")[-3]
    self.temperature = self.filename.split("_")[-2].replace('K','')
    if self.filename.rsplit("_", 1)[-1].replace('.txt','') == 'ram':
      self.type = 'Raman'
    elif self.filename.rsplit("_", 1)[-1].replace('.txt','') == 'lum':
      self.type = 'PL'
    else:
      self.type = 'unknwn'

    self.wavelengths = pd.read_csv(path, sep = '\t', header = None, names = ['wavelength','intensity'])['wavelength']
    self.intensities = pd.read_csv(path, sep = '\t', header = None, names = ['wavelength','intensity'])['intensity']

  def plot_spectrum(self):
    """Plots the spectrum with title, including spectrum type, sample name and temperature"""
    plt.plot(self.wavelengths, self.intensities)
    plt.title(f'{self.type} spectrum of sample {self.sample_name} at {self.temperature} K')
    plt.legend([f'{self.sample_name}'])
    plt.show()

  def find_peaks_in_region(self, wavelengths, intensities, start_wl, end_wl, prominence=100, distance=5):
    """Find peaks in a defined spectral region."""
    
    # Crop the spectrum to the selected region
    mask = (wavelengths >= start_wl) & (wavelengths <= end_wl)
    cropped_wl = wavelengths[mask]
    cropped_int = intensities[mask]

    # Find peaks in the cropped region
    peaks, properties = signal.find_peaks(cropped_int, prominence=prominence, distance=distance)

    # Return peak positions in the original wavelength scale
    return cropped_wl[peaks[0]+cropped_wl.index[0]], cropped_int[peaks[0]+cropped_int.index[0]]

  def normalize(self, raman = True, ss = True):
    if raman == True:
        if self.type.lower() != "pl":
          raise ValueError("Only PL spectra can be normalized!")
        else:
          raman_wavelength_initial = 1/(1/(float(self.exc_wavelength))-(1332./10**7))
          raman_wavelength, raman_intensity = self.find_peaks_in_region(self.wavelengths, 
                                                                        self.intensities, 
                                                                        raman_wavelength_initial - 5,
                                                                        raman_wavelength_initial + 5,
                                                                        prominence = 500)
          self.intensities = self.intensities.div(raman_intensity)

# spectrum1 = Spectrum(filename = '/Users/ilyakaliya/Documents/spectra_refiner/data/raw/17_D2_633nm_x50LF_P5_1a_10s_77K_lum.txt')
# spectrum1.normalize()
# spectrum1.plot_spectrum()