'''

Extra definitions for DEERs scripts

'''
# Import zone -------------------------------------------------

import numpy as np
import scipy
from scipy.signal import find_peaks
import pandas as pd
import matplotlib.pyplot as plt
import random
#---------------------------------------------------------------

# Pre-defined environment variables ----------------------------

#cdms_db_path = ""
#madex_db_path = ""
#fragment_path = ""
#---------------------------------------------------------------

# Pre-defined environment variables ----------------------------

program_version = "v1.0 \n Welcome to the DEERs land!"
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
    print("            ██████╗ ███████╗███████╗██████╗ ███████╗")
    print("            ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝")
    print("            ██║  ██║█████╗  █████╗  ██████╔╝███████╗")
    print("            ██║  ██║██╔══╝  ██╔══╝  ██╔══██╗╚════██║")
    print("            ██████╔╝███████╗███████╗██║  ██║███████║")
    print("            ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝")
    print("      Data Editing and Examination for Rotational Spectroscopy")
    print("            Raul Aguado-Vesperinas             2024")
    print()
    print()
    print("===   ===   ===   ===   ===   ===   ===")
    print("Program version: " + program_version)
    print("===   ===   ===   ===   ===   ===   ===")

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
        sf = float(1.1) #[HAY QUE REVISARLO]
        sf_opt = str()  #Defining an option used for allowing user to modify SF

        x = spc_array[:,0] #Array containing frequencies (X axis)
        y = spc_array[:,1] #Array containing intensities (Y axis)

        int_mean = np.mean(y)  #Mean of y-values. This is aproxinately y = 0
        int_std = np.std(y)   #Standard deviation of intensities. This is aprox. the noise level.

        while True == True:
                baseline = float((int_mean + int_std)* sf) #Obtaining baseline level by adding corrected noise level (corrected_std) to the mean of intensities (int_mean)

                print('Intesity mean: ' + str(int_mean))
                print('Calculated baseline level: y = ' + str(baseline))
        
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


# Min-max normalization algorithm --------

def mm_normalization(lista):
    normalized_list = []
    for i in lista:
        x = (i-min(lista))/(max(lista)-min(lista))
        normalized_list.append(x)
    return(normalized_list)
#---------------------------------------------------------------


# Min-max normalization of a spectrum --------

def spectrum_normalization(spectrum):
    spc_x = np.loadtxt(spectrum, usecols = 0)
    spc_y = np.loadtxt(spectrum, usecols = 1)
    normalized_y = []
    minn = min(spc_y)
    maxx = max(spc_y)
    rest = maxx - minn
    for i in spc_y:
        y = (i-minn)/(rest)
        normalized_y.append(y)
    return(spc_x, normalized_y)
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
    #Printing a random and very interesting fact :")
    print()
    print("---------------------------------------------------------------")
    print("Did you know:")
    print(random.choice(deer_dyk))
    print("---------------------------------------------------------------")
    print()
    
#---------------------------------------------------------------
