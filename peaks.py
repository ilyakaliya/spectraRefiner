import matplotlib as plt
import pandas as pd
import re
import os

class Spectrum:

  def __init__(self, filename, 
              #  wavelengths, intensities, sample_name, 
               type, 
              #  substrate, exc_power, exc_wavelength,acquisition_number, acquisition_time, temperature
               ):

    self.sample_name = filename.split("_")[0]
    self.type = type
    # self.substrate = substrate
    # self.exc_power = exc_power
    self.exc_wavelength = int(re.search(r'(\d+)nm', filename).group(1))
    # self.acquisition_number = acquisition_number
    # self.acquisition_time = acquisition_time
    # self.temperature = temperature
    # self.wavelengths = wavelengths
    # self.intensities = intensities

  def load_spectrum(self, path, type):
    if type == 'Raman':
      self = pd.read_csv(path, sep = '\t', header = None, names = ['Raman shift, cm-1', 'Intensity, a.u.'])
    elif type == 'PL':
      self = pd.read_csv(path, sep = '\t', header = None, names = ['Raman shift, cm-1', 'Intensity, a.u.'])

  def plot_spectrum(self):
    plt.figure(figsize=(8,5))
    plt.plot(self.wavelengths, self.intensities)

  def normalize(self, raman = True, ss = True):
    if self.type.lower() != "pl":
      raise ValueError("Only PL spectra can be normalized!")

spectrum1 = Spectrum(type='PL', filename = 'D2_633nm_PL_93K.txt')
x = spectrum1.sample_name
print(x)