'''
Configuration script for using DEERs suite in Windows

This script will check and store if all the needed modules are installed. If not, it will install them.
Also, this script will storage some pre-defined funcitons and constants needed for the program to work.

Any bug can be reported to the creator (me xD) by email at raaguado98@gmail.com or via GitHub at github.com/raul-aguado
'''

import os
import sys
import subprocess
import time

if sys.version_info.major < 3:
    print("ERROR: Python version required is 3.X. Please update python before using DEERs suite.")
    print("INFO: Exiting pre-configuration script...")
    time.sleep(5)
elif sys.version_info.minor < 12:
    print("INFO: DEERs have been tested on Python 3.12. If you encounter some bug try first updating Python.")

try:
    open("DEERs_cfg.log", "r", encoding="utf-8")
    print("INFO: Pre-configuration script has been already executed.")
    print("My work here is done!")
    print()
    print("Exiting...")
    time.sleep(4)
except:
    print("INFO: Running pre-configuration script")
    print("      All needed modules are going to be checked...\n")
    time.sleep(2)

    #As cfg file is not detected. Here the program creates it.
    cfg_file = open("DEERs_cfg.log", "w", encoding="utf-8")

    print("INFO: Upgrading pip")
    subprocess.check_call([sys.executable, "-m", "ensurepyp", "--upgrade"])
    print()

    try:
        import pandas as pd
        print("INFO: 'Pandas' module loaded.\n")
        pd_install = True
    except:
        print()
        print("WARNING: 'Pandas' module has not been found in the system.")
        print("         'Pandas' module is recomended for a better output visualization.")
        print()
        print("INFO: Forcing Pandas install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
            print("INFO: 'Pandas' installed succesfully.\n")
            pd_install = True
        except:
            print("WARNING: 'Pandas' can't be installed.\n")
            pd_install = False
        
    try:
        import numpy as np
        print("INFO: 'NUMPY' module loaded.\n")
        np_install = True
    except:
        print()
        print("WARNING: 'Numpy' module has not been found in the system.")
        print("         'Numpy' module is needed for automated peak finding.")
        print()
        print("INFO: Forcing 'Numpy' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
            print("INFO: 'NUMPY' installed succesfully.\n")
            np_install = True
        except:
            print("WARNING: 'NUMPY' can't be installed.\n")
            np_install = False
        
    try:
        import scipy
        print("INFO: 'SciPy' module loaded.\n")
        sp_install = True
    except:
        print()
        print("WARNING: 'SciPy' module has not been found in the system.")
        print("         'SciPy' module is needed for automated peak finding.")
        print()
        print("INFO: Forcing 'SciPy' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy"])
            print("INFO: 'SciPy' installed succesfully.\n")
            sp_install = True
        except:
            print("WARNING: 'SciPy' can't be installed.\n")
            sp_install = False

    try:
        import matplotlib
        print("INFO: 'matplotlib' module loaded.\n")
        mpl_install = True
    except:
        print()
        print("WARNING: 'Matplotlib' module has not been found in the system.")
        print("         'Matplotlib' module is needed for graph plotting.")
        print()
        print("INFO: Forcing 'Matplotlib' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
            print("INFO: 'Matplotlib' installed succesfully.\n")
            mpl_install = True
        except:
            print("WARNING: 'Matplotlib' can't be installed.\n")
            mpl_install = False

    try:
        import astropy
        print("INFO: 'Astropy' module loaded.\n")
        astro_install = True
    except:
        print()
        print("WARNING: 'Astropy' module has not been found in the system.")
        print("         'Astropy' module is needed for real-time search in spectroscopic databases.")
        print()
        print("INFO: Forcing 'Astropy' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "astropy"])
            print("INFO: 'Astropy' installed succesfully.\n")
            astro_install = True
        except:
            print("WARNING: 'Astropy' can't be installed.\n")
            astro_install = False

    try:
        import astroquery
        print("INFO: 'Astroquery' module loaded.\n")
        astroQ_install = True
    except:
        print()
        print("WARNING: 'Astroquery' module has not been found in the system.")
        print("         'Astroquery' module is needed for real-time search in spectroscopic databases.")
        print()
        print("INFO: Forcing 'Astroquery' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "astroquery"])
            print("INFO: 'Astroquery' installed succesfully.\n")
            astroQ_install = True
        except:
            print("WARNING: 'Astropy' can't be installed.\n")
            astroQ_install = False
            
    print("INFO: All modules checked\n")

    #Writting the header for cfg file
    cfg_file.write("#INITIAL CONFIGURATION FILE FOR DEERs\n")
    cfg_file.write("#This file storages the initial configuration needed to run DEERs software\n")
    cfg_file.write(os.linesep)

    if pd_install == True and np_install == True and sp_install == True:
        print("*********************************************")
        print("* Initial configuration loaded succesfully. *")
        print("*********************************************\n")

        #Write the configuration in cfg file
        cfg_file.write("Initial configuration has been succesfully completed.\n")
        cfg_file.write("Now you can use DEERs. Welcome to the Land of the deers!!!\n")
                                    
    else:
        
        #Write the configuration in cfg file
        cfg_file.write("********\n")
        cfg_file.write("WARNING\n")
        cfg_file.write("********\n")
        cfg_file.write("Error loading necesary modules. Program may not work properly.\n")
        cfg_file.write("This is the information we have:\n")
    #Writting modules' status, predefined environment variables and constants.
    cfg_file.write("#MODULES' STATUS:\n")
    if pd_install == True:
        cfg_file.write("pd_install = True")
        cfg_file.write("             Panda module installed.\n")
    else:
        cfg_file.write("pd_install = False")
        cfg_file.write("             Panda module NOT instllaled. This module is necessary for a clean output visualization.\n")
    if np_install == True:
        cfg_file.write("np_install = True")
        cfg_file.write("             Numpy module installed.\n")
    else:
        cfg_file.write("np_install = False")
        cfg_file.write("             Numpy module NOT installed. This module is necessary for automated peak finding. This feature will not work.\n")
    if sp_install == True:
        cfg_file.write("sp_install = True")
        cfg_file.write("             SciPy module installed.\n")
    else:
        cfg_file.write("sp_install = False")
        cfg_file.write("             SciPy module NOT instllaled. This module is necessary for automated peak finding. This feature will not work.\n")
        cfg_file.write("#WARNING: SciPy installation errors could arise from running Python in 32-bits. Make sure you are running on a 64-bits.")
    if mpl_install == True:
        cfg_file.write("mpl_install = True")
        cfg_file.write("             matplotlib module installed.\n")
    else:
        cfg_file.write("mpl_install = False")
        cfg_file.write("             matplotlib module NOT instllaled. This module is necessary for graph plotting. Many features will not work.\n")
    if astro_install == True:
        cfg_file.write("astro_install = True")
        cfg_file.write("             Astropy module installed.\n")
    else:
        cfg_file.write("astro_install = False")
        cfg_file.write("             Astropy module NOT instllaled. This module is necessary real-time search in spectroscopic databases. Some features will not work.\n")
    if astroQ_install == True:
        cfg_file.write("astroQ_install = True")
        cfg_file.write("             Astroquery module installed.\n")
    else:
        cfg_file.write("astro_install = False")
        cfg_file.write("             Astroquery module NOT instllaled. This module is necessary real-time search in spectroscopic databases. Some features will not work.\n")

    cfg_file.write("#*********************************************************************************************************************************************\n")


    cfg_file.close()
time.sleep(5)
