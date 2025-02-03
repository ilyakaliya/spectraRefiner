from matplotlib import pyplot as plt
import pandas as pd
import scipy.signal as signal
import re

class Spectrum:

  def __init__(self, filename
               ):

    self.sample_name = filename.split("_")[1]
    self.substrate = filename.split("_")[2]
    self.exc_power = filename.split("_")[5]
    self.exc_wavelength = int(re.search(r'(\d+)nm', filename).group(1))
    self.acquisition_number = filename.split("_")[-4]
    self.acquisition_time = filename.split("_")[-3]
    self.temperature = filename.split("_")[-2].replace('K','')
    if filename.rsplit("_", 1)[-1].replace('.txt','') == 'ram':
      self.type = 'Raman'
    elif filename.rsplit("_", 1)[-1].replace('.txt','') == 'lum':
      self.type = 'PL'
    else:
      self.type = 'unknwn'

    self.wavelengths = pd.read_csv(filename, sep = '\t', header = None, names = ['wavelength','intensity'])['wavelength']
    self.intensities = pd.read_csv(filename, sep = '\t', header = None, names = ['wavelength','intensity'])['intensity']

  def plot_spectrum(self):
    plt.plot(self.wavelengths, self.intensities)
    plt.title(f'{self.type} spectrum of sample {self.sample_name} at {self.temperature} K')
    plt.legend([f'{self.sample_name}'])
    plt.show()

  def normalize(self, raman = True, ss = True):
    if raman == True:
        if self.type.lower() != "pl":
          raise ValueError("Only PL spectra can be normalized!")
        else:
          # combined = pd.concat([self.wavelengths, self.intensities], axis = 1)
          # print(combined.head())
          around = 1/(1/(float(self.exc_wavelength))-(1332./10**7))
          mask = (self.wavelengths > around - 5) & (self.wavelengths < around + 5)
          cropped_wl = self.wavelengths[mask]
          cropped_int = self.intensities[mask]
          peak = signal.find_peaks(cropped_int)
          print(peak)

          # self.intensities = self.intensities.div(self.intensities.iloc(self.wavelengths.index(1/(1/(float(self.exc_wavelength))-(1332./10**7)))))

spectrum1 = Spectrum(filename = 'G:\\Ilia\\spectraRefiner\\data\\raw\\2_G218G214_Ge_488nm_x50_P10_1a_10s_300K_lum.txt')
spectrum1.normalize()
# spectrum1.plot_spectrum()