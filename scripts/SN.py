'''

Script for the comparison of SN in a batch of FT-MW spectra

'''
# Import zone -------------------------------------------------

import os
from os import getcwd, scandir
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from extras.defs import peak_finder_script as pk
from extras.defs import pause, find_closest, program_version
#---------------------------------------------------------------


# Dict for storagin values of signal, noise and SN ratio -------

data = {"Signal":[], "Noise":[], "SN":[]}
#---------------------------------------------------------------


# Locate freqs of signal and noise in the spectrum -------------

def S_N_locate(file,signal,noise):  #Defining a function to locate in every spectrum the freq of the signal and the noise and append their Y value
    spectrum = np.loadtxt(file, usecols=(0, 1))
    spectrum_x = np.array(spectrum[:,0])
    spectrum_y = np.array(spectrum[:,1])
    
    n = 0
    m = len(spectrum_x)-1

    Csignal = find_closest(spectrum_x, signal)
    
    Cnoise = find_closest(spectrum_x, noise)
    
    while n < m:
        if spectrum_x[n] == Csignal:
            signal_h = float(spectrum_y[n])
            data["Signal"].append(signal_h)
            n = n + 1
        elif spectrum_x[n] == Cnoise:
            noise_h = float(spectrum_y[n])
            data["Noise"].append(noise_h)
            n = n + 1
        else:
            n = n + 1
#---------------------------------------------------------------


# Calculate signal noise ratio ---------------------------------
            
def SN_calc():
    print("INFO: Calculating SN ratio...\n")
    n = 0
    m = (len(data["Signal"]))
    while n < m:
        SN = (data["Signal"][n])/(data["Noise"][n])
        data["SN"].append(SN)
        n = n + 1
#---------------------------------------------------------------


# Create a Signal/Noise ratio vs. spectrum plot-----------------

def create_plot(n, sn):
    print("INFO: Creating graph..\n")
    x_axis = []
    for i in range(0,n):
        x_axis.append(i+1)
    plt.plot(x_axis, sn)
    plt.show()
#---------------------------------------------------------------


# Save results -------------------------------------------------

def save_results(save_path):
    out = open(save_path, "w")
    out.write("==============================================================================\n")
    out.write("DEERS " + program_version + "                   Raul Aguado-Vesperinas 2023\n")
    out.write("==============================================================================\n")
    out.write("       Spectrum No.            Signal            Noise              SN ratio\n")
    
    n = 0
    m = (len(data["Signal"])-1)
    while n < m:
        out.write("       " + str(n) + "       " + str(round((data["Signal"][n]),3)) + "       " + str(round((data["Noise"][n]),3)) + "       " + str(round((data["SN"][n]),3)) + "\n")
        n = n + 1
    out.close()
#---------------------------------------------------------------


# Main flow of the script --------------------------------------

# Taking the folder of the spectra and signal and noise freqs
print("Select the folder of your FTMW spectra (only 2-column ascii)")
path = input("Path of your spectra: ")
print()
print("Select the target signal frequency and the noise frequency. Give AT LEAST 2 decimals!")
signal_freq = round(float(input("Frequency of your signal (in MHz): ")),2)
noise_freq = round(float(input("Frequency of noise (in MHz): ")),2)
print()
print("INFO: Signal freq set to " + str(signal_freq) + " MHz and noise freq set to " + str(noise_freq) + " MHz\n")

# Selecting the .txt files which contains "freq" (inherited of GEM CP-FTMW)
path_files = [arch.name for arch in scandir(path) if arch.is_file()]
spectra_files = []
for file in path_files:
    extension = os.path.splitext(file)[-1].lower()
    if extension == ".txt" and "freq" in file:
        spectra_files.append(file)
files_number = len(spectra_files)  #Storaging here the number of spectra. This data will be used in create_plot() func for X values of the plot
print("INFO: " + str(files_number) + " data files have been loaded.\n")

# Using previous definitions to obtain the signal, noise and SN ratio
print("INFO: Extracting values from spectrum\n")
for file in spectra_files:
    spectra_complete_path = (path + "\\" + file)
    S_N_locate(spectra_complete_path, signal_freq, noise_freq)

SN_calc()

# Creating plot to visualize the evolution of the SN ratio
create_plot(files_number, data["SN"])

# Option for saving the results
save_opt = input("Dou you want to save this data?(y/n)... ")
if save_opt == "y" or save_opt == "Y":
    save_path = path + "\SN_comparer_OUTPUT.out"
    save_results(save_path)
    print("INFO: Data saved to " + save_path)


print("INFO: Script finished.")
#---------------------------------------------------------------
