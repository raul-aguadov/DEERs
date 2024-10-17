'''

Extra definitions for DEERs scripts

'''
# Import zone -------------------------------------------------

import sys
import os
import numpy as np
import scipy
from scipy.signal import find_peaks
import pandas as pd
import matplotlib.pyplot as plt
import random
#---------------------------------------------------------------

# Pre-defined environment variables ----------------------------
cdms_db_path = "E:/DEERs_v1/extras/CDMS_0-16GHz.sdb"
madex_db_path = "E:/DEERs_v1/extras/MADEX.sdb"
fragments_path = "E:/DEERs_v1/cacas.txt"
#---------------------------------------------------------------

# Pre-defined environment variables ----------------------------

program_version = "v1.0"
#---------------------------------------------------------------


# Universal constants ------------------------------------------

H_const = 6.62606896E-34            # Planck constant    [J*s]
C0_const = 2.99792458E8             # speed of light     [m/s]
NA_const = 6.022140857E+023         # Avogradro's number [mol^-1]
KB_const = 1.3806504E-23            # Boltzmann const    [J/K]
QE_const = 1.6021766208E-019        # charge of electron [C]
ME_const = 9.10938356E-031          # mass of electron   [kg]
MC12_const = 1.66053904E-027        # mass of C12        [kg]
CAL_const = 4.184                   # 1 cal = 4.184 J
#---------------------------------------------------------------


# Program banner -----------------------------------------------

def banner():
    print("                        ██████╗ ███████╗███████╗██████╗ ███████╗")
    print("                        ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝")
    print("                        ██║  ██║█████╗  █████╗  ██████╔╝███████╗")
    print("                        ██║  ██║██╔══╝  ██╔══╝  ██╔══██╗╚════██║")
    print("                        ██████╔╝███████╗███████╗██║  ██║███████║")
    print("                        ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝")
    print("               Data Editing and Examination for Rotational Spectroscopy")
    print("                        Raul Aguado-Vesperinas             2024")
    print()
    print()
    print("Program version: " + program_version)
    print()

#---------------------------------------------------------------


# Pause function -----------------------------------------------

def pause():
    input('Press enter to continue:')
#---------------------------------------------------------------


# Find the closest value for a given one from a list -----------

def find_closest(lst, K):
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]
#---------------------------------------------------------------


# Calculate the step between the points in the spectrum --------

def calculate_step(x):
    step = (x[1]-x[0])
    m = 0
    while m < len(x):
        if m > 1:
            step = (step + (x[m]-x[m-1]))/2
            m = m + 1
        else:
            m = m + 1
    return(step)
#---------------------------------------------------------------


# Peak finding script with console -----------------------------

def peak_finder_script(file):
        spc_array = np.loadtxt(file, usecols=(0, 1))
        sf = float(1.25) #[HAY QUE REVISARLO]
        sf_opt = str()  #Defining an option used for allowing user to modify SF

        x = spc_array[:,0] #Array containing frequencies (X axis)
        y = spc_array[:,1] #Array containing intensities (Y axis)

        int_mean = np.mean(y)  #Mean of y-values. This is aproxinately y = 0
        int_std = np.std(y)   

        while True == True:
                baseline = float(sf*int_mean) #Obtaining baseline level by adding corrected noise level (corrected_std) to the mean of intensities (int_mean)

                print()
                print('INFO: Intesity mean: ' + str(int_mean))
                print('INFO: Intensity standard deviation: ' + str(int_std))
                print('INFO: Calculated baseline level: y = ' + str(baseline) + '\n')
        
                peaks_filtered  = find_peaks(y, height = baseline)  #Using SciPy to locate peaks higher than baseline

                final_x = np.array(x[peaks_filtered[0]])  #Creating an array with the frequencies of the peaks
                final_y = peaks_filtered[1]['peak_heights']  #Creating an array with the intensities of the peaks

                plt.plot(x,y)
                plt.bar(final_x, final_y, width=0.5, color = 'red')
                plt.show()

                sf_opt = str(input('Have peaks correctly detected? (y/n)... '))  #If the program has detected correctly the peaks the loop breaks, if not, retries with othe

                if sf_opt == 'y' or sf_opt == 'Y':
                    break
                else:
                    sf = float(input('Set a new SecurityFactor. Last used: ' + str(sf) + "..."))
        return final_x, final_y
#---------------------------------------------------------------


# Save a list of detected peaks into a txt file ----------------

def save_peaks(path, peaks_list):
    try:
        out_path = path.replace(".txt", "_PEAKS.asc")
    except:
        try:
            out_path = path.replace(".dat", "_PEAKS.asc")
        except:
            spc_out = (spc_path + "-PEAKS.asc")
            
    with open(out_path, "w") as out:
        for peak in peaks_list:
            out.write(str(peak) + "\n")
    print()
    print("INFO: Peaks saved to: " + out_path)
#---------------------------------------------------------------

    
# Blank a given spectrum ---------------------------------------

def blank_spectrum(SPC_file, peaks_file):
    Frequency = np.loadtxt(SPC_file, delimiter="\t", usecols=0)
    Spec = np.loadtxt(SPC_file, delimiter="\t", usecols=1)


    blank_peaks = []
    final_peaks = []

    # Calculating the step
    step = calculate_step(Frequency)

    # Setting up the blanking width
    w = float(0.25)
    print()
    print("INFO: Blanking width is set to " + str(w*2*1000) + " KHz\n")
    w_opt = False
    while w_opt !="y" or w_opt != "Y" or w_opt != "n" or w_opt != "N":
        w_opt = str(input("Change blanking width? (y/n)... "))
        if w_opt == "y" or w_opt == "Y":
            w = float(input("Set new blanking width in KHz... "))/2000
            print()
            print("INFO: Blanking width set to " + str(w*2*1000) + " KHz\n")
            break
        if w_opt == "n" or w_opt == "N":
            break
        
    # Read peaks file and create the range
    peaks = []
    try:
        with open(peaks_file, 'r') as l:
            lines = l.readlines()
        for i in lines:
            peaks.append(float(i.replace("\n","0")))
        
    except TypeError:  #In this case, the main routine is passing a list, not a peak file
        lines = peaks_file
        for i in lines:
            peaks.append(i)    
    
    for peak in peaks:
        r = np.arange(peak-w, peak+w, step)
        blank_peaks.append(r)
        
    ############################# ESTO ES HORRIBLE #############################
    blank_peaks_np = np.array(blank_peaks)
    blank_peaks_np.flatten()
    for i in blank_peaks_np:
        for j in list(i):
            final_peaks.append(round(j,1))
    ############################# ESTO ES HORRIBLE #############################

    blanked_spectrum_x = []
    blanked_spectrum_y = []

    L = len(Frequency)
    n = 0

    while n < L:
        if round(Frequency[n],1) in final_peaks:
            blanked_spectrum_x.append(Frequency[n])
            blanked_spectrum_y.append(0.0000)
            n = n + 1
        else:
            blanked_spectrum_x.append(Frequency[n])
            blanked_spectrum_y.append(Spec[n])
            n = n + 1
     
    plt.plot(Frequency, Spec, label="Original Spectrum")
    plt.plot(blanked_spectrum_x, blanked_spectrum_y, label="Blanked Spectrum")
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    return(blanked_spectrum_x,blanked_spectrum_y)
#---------------------------------------------------------------

# Save a spectrum ----------------------------------------------

def save_spc(spc_x, spc_y, spc_path):
    print()
    print("INFO: Saving results...\n")
    try:
        spc_out = spc_path.replace(".txt", "_BLANKED.txt")
    except:
        try:
            spc_out = spc_path.replace(".dat", "BLANKED.txt")
        except:
            spc_out = (spc_path + "-BLANKED.txt")

    spc = open(spc_out, "w")

    n = 0 # Tool for iterating through lists

    while n < len(spc_x):
        spc.write(str(spc_x[n]) + "    " + str(spc_y[n]))
        spc.write(os.linesep)
        n = n + 1

    spc.close()

    print()
    print("INFO: Spectrum blanked and results saved to")
    print(spc_out)
#---------------------------------------------------------------

























































































































































































































#You have scrolled so far that you have encountered the secret definition!
#---------------------------------------------------------------
def dyk():
    #Setting up the deers-facts library 
    deer_dyk = [
        "White-tailed deer are the most popular large game animal in the USA.",
        "A deer can't drive a Subaru WRZ.",
        "White-tail deer are good swimmers and will use large streams and lakes to escape predators.",
        "White-tailed deer have good eyesight and hearing. ",
        "All species of deer have antlers, with the exception of the Chinese water deer. Instead of antlers, they have long canine teeth which can be as long as 8cm!",
        "All species of deer have a four chamber stomach which allows them to chew the cud. This is a processes of partially chewing food, regurgitating it, and chewing it again to make it easier to digest.",
        "The largest deer species was the Irish Giant Deer which went extinct 11,000 years ago. Reaching 7ft tall at the shoulder, the Irish Deer’s antlers could span 12ft, four times the width of a single bed!",
        "Deer can have a homeland range which can span 30 miles. They move about depending on food availability",
        "Deer have special ways of communication. They communicate through visual, vocal, and chemical means. They have a scent produced in various parts of the body that gives important information such as physique, sex, social status, and whether there is danger looming in an area.",
        "Despite Deer have special ways of communication, they can't use cell phones.",
        "Deer are an important part of the ecosystem. Deer are considered prey to many wild animals, even humans hunt them down which makes them an important link in the food chains.",
        "Deer were part of the cave paintings. Paleontologists found deer as part of the artwork in the caves and they have been a great part of that history.",
        "Earth is not spherical, it's deer-shaped!!",
        "Some species of the deer have been recorded on film eating infant birds, this is uncanny as deer are primarily herbivores.",
        "A female deer digests its fetus naturally when subjected to harsh conditions that leave it malnourished.",
        "Deer are color blind to neon orange, which is why hunters where jackets of that color in order to increase their chances of gunning down a deer.",
        "In Yakushima, a Japanese island, deer are groomed and provided with food by macaque monkeys. They, in turn, let the monkeys ride on their backs to move from one place to another.",
        "In North America, deer are considered the biggest threat to humans among all mammals.",
        "A deer can't drive a bus"
        ]
    #Printing a random (and very interesting) fact about deers :")
    print()
    print("---------------------------------------------------------------")
    print("Did you know:")
    print(random.choice(deer_dyk))
    print("---------------------------------------------------------------")
    print()
    
#---------------------------------------------------------------
