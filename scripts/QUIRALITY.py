'''
Automated script for quiral search
'''
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from extras.defs import pause, calculate_step
from extras.defs import peak_finder_script as pk


# Some definitions   ---------------------------------------------------
blank_peaks = []
final_peaks = []
#-----------------------------------------------------------------------


# Some baner to know what in the hell is running -----------------------
print()
print("-----------------------------------------------------------------")
print("                         CHIRALITY MODE")
print("                       Script version V2.1")
print("-----------------------------------------------------------------")
print()
#-----------------------------------------------------------------------


# Setting up the blanking width   --------------------------------------
w = float(0.25)
print("Blanking width is set to " + str(w*2*1000) + " KHz\n")
w_opt = False
while w_opt !="y" or w_opt != "Y" or w_opt != "n" or w_opt != "N":
    w_opt = str(input("Change blanking width? (y/n)... "))
    if w_opt == "y" or w_opt == "Y":
        w = float(input("Set new blanking width in KHz... "))/2000
        print("Blanking width set to " + str(w*2*1000) + " KHz\n")
        break
    if w_opt == "n" or w_opt == "N":
        break
#-----------------------------------------------------------------------


# Importing spectra   --------------------------------------------------

print()
print("-----------------------------------------------------------------")
print("                      SAMPLE SPECTRUM\n")
print()
sample_path = str(input("Insert the path to the chiral sample spectrum: "))
try:
    sample_x, sample_y = pk(sample_path)
    print("Info: Sample spectrum loaded!\n")
except:
    print("ERROR: Spectrum cannot be loaded. Exiting...\n")
    pause()
    raise SystemExit
    
print("-----------------------------------------------------------------")
print("                    QUIRAL TAG SPECTRUM\n")
print()
tag_path = str(input("Insert the path to the quiral tag spectrum: "))
try:
    tag_x, tag_y = pk(tag_path)
    print("Info: quiral tag spectrum loaded!\n")
except:
    print("ERROR: Spectrum cannot be loaded. Exiting...\n")
    pause()
    raise SystemExit

print("-----------------------------------------------------------------")
print("                      FINAL SPECTRUM\n")
print()
final_path = str(input("Insert the path to the final spectrum: "))
try:
    final_array = np.loadtxt(final_path, usecols=(0, 1))
    final_x = final_array[:,0]
    final_y = final_array[:,1]
    print("Info: quiral tag spectrum loaded!\n")
except:
    print("ERROR: Spectrum cannot be loaded. Exiting...\n")
    pause()
    raise SystemExit
print("-----------------------------------------------------------------\n")
#-----------------------------------------------------------------------


# Calculating step for final spectrum ----------------------------------
step = calculate_step(final_x)
#-----------------------------------------------------------------------


# Using blanking width to create the blanking range (r) in final_peaks -
print("INFO: Creating blanking ranges...\n")
peaks = []
for i in sample_x:
    peaks.append(i)
for j in tag_x:
    peaks.append(j)

for peak in peaks:
    r = np.arange(peak-w, peak+w, step)
    blank_peaks.append(r)

blank_peaks_np = np.array(blank_peaks)
blank_peaks_np.flatten()
for i in blank_peaks_np:
    for j in list(i):
        final_peaks.append(round(j,1))
#-----------------------------------------------------------------------



# Setting up the final spectrum lists ----------------------------------
blanked_spectrum_x = []
blanked_spectrum_y = []
#-----------------------------------------------------------------------


# Iterating through final spectrum to blank it -------------------------
print("INFO: Blanking the spectrum...\n")

L = len(final_x)
n = 0

while n < L:
    if round(final_x[n],1) in final_peaks:
        blanked_spectrum_x.append(final_x[n])
        blanked_spectrum_y.append(0.0000)
        n = n + 1
    else:
        blanked_spectrum_x.append(final_x[n])
        blanked_spectrum_y.append(final_y[n])
        n = n + 1
#-----------------------------------------------------------------------

# Plotting both spectra ------------------------------------------------
print("INFO: Plotting results...\n")

plt.plot(final_x, final_y, label="Original Spectrum")
plt.plot(blanked_spectrum_x, blanked_spectrum_y, label="Blanked Spectrum")
plt.scatter(sample_x, sample_y, label="Sample peaks")
plt.scatter(tag_x, tag_y, label="Chiral tag peaks")
plt.legend() 

plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------


# Saving blanked spectrum ----------------------------------------------
print("INFO: Saving results...\n")
try:
    blanked_spc = open((final_path.replace(".txt", "_BLANKED.txt")), "w")
except:
    try:
        blanked_spc = open((final_path.replace(".dat", "BLANKED.txt")), "w")
    except:
        blanked_spc = open((final_path + "BLANKED.txt"), "w")

blanked_spc.write("Spectrum blanked using DEERs Suite                     Raúl Aguado-Vesperinas  2024")
for i in final_x:
    for j in final_y:
        blanked_spc.write(str(i) + "    " + str(j))
        blanked_spc.write(os.linesep)

blanked_spc.close()

print("INFO: Spectrum blanked and results saved\n")
#-----------------------------------------------------------------------


pause()

