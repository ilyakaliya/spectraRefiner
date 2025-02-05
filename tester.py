from peaks import Spectrum
import os
from matplotlib import pyplot as plt

plt.subplots(3,1)

for file in os.listdir('/Users/ilyakaliya/Documents/spectra_refiner/data/raw/tester'):
  if file.endswith('.txt'):
    spectrum = Spectrum('/Users/ilyakaliya/Documents/spectra_refiner/data/raw/tester' + "/" + file)
    spectrum.normalize()
    spectrum.plot_spectrum()