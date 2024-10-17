"""
Data Editing and Erasing tool for Rotational Spectroscopy

Created on Mon Sep 19 2022. First alpha release on Dec 1 2022 as RSDBF.

Raúl Aguado Vesperinas
"""

#Importing, definition and configuration zone

import sys
import os
import time
from datetime import datetime
import subprocess
import pandas as pd

from extras.defs import banner, pause, program_version, dyk, save_spc, save_peaks
from extras.defs import peak_finder_script as pk
from extras.defs import blank_spectrum as blk

# Forcing windows cmd to initiate with 
os.system('mode con: cols=105 lines=40')

#Defining the menu (this part of the code is here for clearness)
def main_menu():
    print(" ******************")
    print("     MAIN MENU")
    print(" ******************")
    print()
    print(" Avaiable tasks:")
    print("   1. Extract peaks from a spectrum")
    print("   2. Analyze SN ratio during a experiment")
    print("   3. Search for peaks in a database")
    print("   4. Remove lines from spectrum")
    print("   5. QUIRALITY mode")
    print("   6. Compare spectra")
    print("   7. Exit")
    print()
    print("   h. Help menu")
    print()
    global main_opt
    main_opt = input(" Select a task... ")

## Estaria bien indicar las opciones que se estan cargando por defecto

print()
banner()

##########################################################################
#MENU LOOP
##########################################################################
while True == True:
    print()
    main_menu()
    print()

    try:
        main_opt = int(main_opt)
    except:
        if main_opt == 'h':
            from extras.main_help import texto
            texto()
            pass
        else:
            print("ERROR: Enter a valid option...\n")
            pass
        
    if main_opt == 1:
        print()
        print("INFO: Launching peak finding utility\n")
        try:
            file = input("Spectrum file... (.txt/.dat): ")
            final_x, final_y = pk(file)  #Running peak finder script
            save_peaks(file, final_x)

        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass
    
    elif main_opt == 2:
        print()
        print("INFO: Launching SN-comparer script\n")
        try:
            import scripts.SN
            
        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass
    
    elif main_opt == 3:
        print()
        print("INFO: Launching DB-finder script\n")
        try:
            import scripts.RSDbF_v2
        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass
    
    elif main_opt == 4:
        print()
        print("INFO: Launching Blanking utility\n")
        try:
            spc_file = input("Spectrum file... (.txt/.dat): ")
        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass
        
        print()
        peaks_file = input("Peaks file... (.txt/.asc): ")
        blanked_spc_x, blanked_spc_y = blk(spc_file, peaks_file)

        save_opt = str(input("Save blanked spectrum? (y/n)..."))
        if save_opt == "y" or save_opt == "Y":
            save_spc(blanked_spc_x, blanked_spc_y, spc_file)
        else:
            pass

    elif main_opt == 5:
        print()
        print("INFO: Launching QUIRALITY script\n")
        try:
            import scripts.QUIRALITY
        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass
        

    elif main_opt == 6:
        print()
        print("INFO: Launching SPC-comparer script\n")
        try:
            import scripts.SPC_comp
        except OSError:
            print()
            print("ERROR: Path not found or path not declared\n")
            pass

    elif main_opt == 7:
        print()
        print("INFO: Exiting DEERs\n")
        print(":(")
        print()
        pause()

        raise SystemExit

    else:
        pass

    dyk()
    pause()
