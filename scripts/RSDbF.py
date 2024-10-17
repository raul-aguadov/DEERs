"""
Rotational Spectroscopy Database Finder

This program works (for the moment) with CDMS and MADEX line databases and PICKETT . It will look for the assinged lines (listed in a .LIN file) in the database.


Created on Mon Sep 19 2022. First stable release on Dec 1 2022
by Raúl Aguado Vesperinas

"""

import sys
import os
import time
from datetime import datetime
import subprocess
import pandas as pd

from extras.defs import pause
from extras.defs import peak_finder_script as pk
try:
    from extras.cfg import fragments_path
    fragments_log = True
except:
    fragments_log = False
    pass

#List for unknown peaks
unk_peaks = []
#-----------------------------------------------------------------------
    

# Loading the database if there are not any pre-defined ----------------

def load_db():
    print("Enter the SDB file containing the spectroscopic data.")
    print("You can also drag your file and drop it here. :D")
    sdb_path = str(input("SDB file... "))
    return sdb_path
#-----------------------------------------------------------------------



# Saving results to csv files ------------------------------------------

def save(data, stats):
    save_path = input("Select the path for saving the results... ")
    save_name = input("Select the name for the file... ")
    print()
    out_path = str(save_path + "/" + save_name + ".csv")
    data.to_csv(out_path)
    out2_path = str(out_path + "_STATS.csv")
    stats.to_csv(out2_path)
    print("INFO: Results saved succesfully to:")
    print(out_path + ".csv and " + out2_path)
    print()
#-----------------------------------------------------------------------


# Counting transitions for each molecule -------------------------------

def count_molecules(molecules_data):
    #Declaring the necessary variables
    molecules = list(molecules_data)
    molecules_dict = {"Molecule": [], "Times detected": []}

    for i in molecules:
        if i not in molecules_dict["Molecule"]:
            molecules_dict["Molecule"].append(i)
            n_times = molecules.count(i)
            molecules_dict["Times detected"].append(n_times)
            print(str(n_times) + " peaks have been detected for molecule " + str(i) + "\n")
            

    global df2
    df2 = pd.DataFrame(molecules_dict)
    print()
    print("===========================================================")
    print("Statistical report")
    print("===========================================================")
    print(df2)
    print()
    return(df2)
    #Aqui podría añadirse un gráfico todo guapo del numero de veces que sale cada molécula, para hacerlo mas visual
    

# Creating a dict for output -------------------------------------------

matches = {
    "Match frequency" : [],
    "Experimental frequency": [],
    "Info" : []
    }
#-----------------------------------------------------------------------

# Load DB and experimental lines ---------------------------------------

#Selecting between CDMS or MADEX databases' type and Trying to get a pre-set path from cfg file
print()
sdb_type = int(input("Select the database's type to load | 1.CDMS  2.MADEX | "))
if sdb_type == 1: 
    print("INFO: CDMS database type selected.\n")
    try:
        from extras.cfg import cdms_db_path as sdb_path
    except:
        sdb_path = load_db()
elif sdb_type == 2:
    print("INFO: MADEX database type selected.\n")
    try:
        from extras.cfg import madex_db_path as sdb_path
    except:
        sdb_path = load_db()

#Read all lines in DB and count them
sdb = open(sdb_path, "r")
sdb_lines = sdb.readlines()
sdb_n_lines = len(sdb_lines)
print("INFO: " + sdb_path + " has been readed. " + str(sdb_n_lines) + " entries have been loaded.")

#Print the last modification date for loaded DB
last_mod = os.path.getmtime(sdb_path)
print("INFO: The file loaded was last updated on " + str(datetime.fromtimestamp(last_mod)) + "\n")

#Loading the experimental frequencies
LIN_opt = int(input("Select the source of experimental lines | 1.LIN FILE  2.Extract from spectrum | "))
if LIN_opt == 1:
    print("Enter the LIN file containing measured lines.")
    print("You can also drag your file again!")
    LIN_path = str(input("LIN file..."))
    with open(LIN_path, "r") as LIN:
        LIN_lines = LIN.readlines()
elif LIN_opt == 2:
    print("Enter the spectrum containing measured lines. (It should be a 2-column ascii file).")
    print("You can also drag your file again!")
    LIN_path = str(input("Spectrum file..."))
    LIN_lines, experimental_y = pk(LIN_path) #Experimental_y is not necessary, but pk gives two arguments (x and y from peaks) and i dont want LIN_lines to be a tuple
    
print()
print("INFO: " + str(len(LIN_lines)) + " experimental lines have been loaded.")

#Option to save non-matching peaks into a SDB
mol_name = str(input("Name of the molecule... "))
conds = str(input("Any experimental detail... "))
#-----------------------------------------------------------------------

# Search for lines in DB -----------------------------------------------

for line in LIN_lines:
    LIN_chars = []

    if LIN_opt == 1:
        #Reading .LIN file
        for char in line:
            LIN_chars.append(char)
        LIN_freq = float(''.join([str(elem) for elem in LIN_chars[39:56] if elem!=" "]))

    elif LIN_opt == 2:
        #Lines obtained from peak_finder
        LIN_freq = line

    LIN_freq_round = round(LIN_freq,2) ### Esto es una chapuza, añade algo para comparar con mayor precision solo los matches
    print("Looking for line " + str(LIN_freq_round) + " in database...")
    
    n = 0
    while n < sdb_n_lines:
        sdb_chars = []
        for char in sdb_lines[n]:
            sdb_chars.append(char)
            
        try: #El try este esta ocultando un error
            #SBD freq from CDMS
            if sdb_type == 1:
                sdb_freq = float(''.join([str(elem) for elem in sdb_chars[0:15] if elem!=" "]))
            #SBD freq from MADEX
            elif sdb_type == 2:
                sdb_freq = float(''.join([str(elem) for elem in sdb_chars[27:37] if elem!=" "]))
            sdb_freq_round = round(sdb_freq,2)
            
            if LIN_freq_round == sdb_freq_round:
                #SBD info from CDMS
                if sdb_type == 1:
                    info = (''.join([str(elem) for elem in sdb_chars[89:115] if elem!=" "]))
                #SBD info from MADEX
                if sdb_type == 2:
                    info = (''.join([str(elem) for elem in sdb_chars[0:25] if elem!=" "]))
                print("One match found!:    " + str(sdb_freq) + "    " + str(info))
                
                #FILLING THE DICTIONARY WITH OUTPUT INFORMATION
                matches["Match frequency"].append(LIN_freq_round)
                matches["Experimental frequency"].append(sdb_freq)
                matches["Info"].append(info) #Añadir funcion que cuente cuantas veces esta cada molecula o residuo con _.count()
                #añadir la transicion que corresponde a cada freq
                
            else:
                pass
        except:
            n = n + 1
            pass

        n = n + 1
#-----------------------------------------------------------------------


# Output generation ----------------------------------------------------

df1 = pd.DataFrame(matches)
print()
print("===========================================================")
print("Results report")
print("===========================================================")
print(df1)
print()

count_molecules(matches["Info"])
save(df1, df2)
#-----------------------------------------------------------------------

# Save unknown peaks in local database ---------------------------------

if fragment_log == True:
    print("INFO: Saving unknown lines into local database " + fragments_path + "\n")
    for i in LIN_lines:
        if i not in matches["Experimental frequency"]:
            unk_peaks.append(i)
    with open(fragments_path, "a") as frag:
        for j in unk_peaks:
            frag.write(str(j) + "         " + mol_name + "         " + conds)
else:
    print("ERROR: Local fragment database can not be accesed. Unknown peaks will not be saved.\n")
#-----------------------------------------------------------------------

        
# Create .asc files for blanking ---------------------------------------

print("INFO: Creating ECHO files...")
with open(("ECHO_" + mol_name + "_COINCIDENT.asc"), "w") as coinc:
    for i in matches["Experimental frequency"]:
        coinc.write(i)
        coinc.write(os.linesep)
print("INFO: Creating ECHO file for COINCIDENT peaks created!")
with open(("ECHO_" + mol_name + "_NON-COINCIDENT.asc"), "w") as noncoinc:
    for j in unk_peaks:
        noncoinc.write(j)
        noncoinc.write(os.linesep)
print("INFO: Creating ECHO file for COINCIDENT peaks created!")

print()
print("INFO: Program completed succesfully...")
#-----------------------------------------------------------------------
