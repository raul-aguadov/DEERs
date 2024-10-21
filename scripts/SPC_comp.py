'''
Automated script for FT-MW spectra comparison
'''

import sys
import os
import numpy as np

from extras.defs import pause, find_closest, save_spc, save_peaks
from extras.defs import peak_finder_script as pk
from extras.defs import blank_spectrum as blank


sp1_x_rounded = []
sp2_x_rounded = []

prec = 6  #Decimals taken for round the frequencies
err = 0.01  #Error for finding coincident peaks (in MHz)

print("INFO: Precision set to " + str(prec) + " number of decimals.")
print("INFO: Error accepted for coincidences set to " + str(err*1000) + " KHz.")
print("\n")

print("    Spectrum no.1")
print("*******************************\n")
print("INFO: Note that this first spectrum is going to be taken as the reference spectrum for finding coincidences.\n")

#Loop for loading the spectrum. The loop continue until a correct file is loaded.
while True == True:
    sp1_path = str(input("Insert the path to the first spectrum: "))
    try:
        sp1_x, sp1_y = pk(sp1_path)
        for i in sp1_x:
            sp1_x_rounded.append(round(i, prec))
        print("INFO: Spectrum loaded!\n")
        break
    except:
        print("ERROR: Spectrum cannot be loaded.\n")
        continue
    
print("    Spectrum no.2")
print("*******************************\n")

#Loop for loading the spectrum. The loop continue until a correct file is loaded.
while True == True:
    sp2_path = str(input("Insert the path to the second spectrum: "))
    try:
        sp2_x, sp2_y = pk(sp2_path)
        for j in sp2_x:
            sp2_x_rounded.append(round(j, prec))
        print("INFO: Spectrum loaded!\n")
        break
    except:
        print("ERROR: Spectrum cannot be loaded.\n")
        continue

#Asking for a comparing option
while True == True:
    comp_opt = int(input("Select a task | 1. Find coindident peaks  2. Find non-coincident peaks  | "))
    print()

    if comp_opt == 1 or comp_opt == 2:
        break
    else:
        continue

found_peaks = []

if comp_opt == 1:
    # Looking for coincident lines
    for k in sp1_x_rounded:
        if k in sp2_x_rounded:
            found_peaks.append(k)
elif comp_opt == 2:
    # Looking for non-coincident lines
    for k in sp2_x_rounded:
        if k not in sp1_x_rounded:
            found_peaks.append(k)

print()
print("INFO: Task completed!")
print()

#Asking for the desired output
while True == True:
    out_opt1 = int(input("Select the output | 1. Save findings to a .ASC file  2. Clear spectrum | "))
    print()
    
    if out_opt1 == 1 or out_opt1 == 2:
        break
    else:
        continue

if out_opt1 == 1:
    save_peaks(sp2_path, found_peaks)
    
elif out_opt1 == 2:
    
    out_opt2 = int(input("Select spectrum to blank | 1. Spectrum no.1  2. Spectrum no.2  3. Both spectra | "))

    print()
    print("INFO: Blanking spectrum")
    print()
    
    if out_opt2 == 1 or out_opt2 == 3:
        blanked_sp1_x, blanked_sp1_y = blank(sp1_path, found_peaks)
        save_spc(blanked_sp1_x, blanked_sp1_y, sp1_path)
    elif out_opt == 2 or out_opt == 3:
        blanked_sp2_x, blanked_sp2_y = blank(sp2_path, found_peaks)
        save_spc(blanked_sp2_x, blanked_sp2_y, sp2_path)


