'''
Configuration script for using DEERs suite in Windows

This script will check and store if all the needed modules are installed. If not, it will install them.
Also, this script will storage some pre-defined funcitons and constants needed for the program to work.

Any bug can be reported to the creator (me xD) by email at raul.aguado@uva.es or via GitHub at github.com/raul-aguado
'''

import os
import sys
import subprocess

try:
    import cfg
    if cfg.INIT_CFG == True:
        print("INFO: Initial configuration loaded succesfully from cfg file.\n")
    elif cfg.INIT_CFG == False:
        print("WARNING: Misconfiguration. Program may not work properly.")
        print("         For detailed information check cfg file.")
        raise SystemError
except:
    print("WARNING: Initial configuration not detected. Running pre-configuration script")
    print("INFO: All needed modules are going to be checked...\n")

    #As cfg file is not detected. Here the program creates it.
    cfg_file = open("DEERs_cfg.log", "w", encoding="utf-8")
            
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
            sp_install = True
        except:
            print("WARNING: 'Matplotlib' can't be installed.\n")
            sp_install = False

    try:
        import astropy
        print("INFO: 'Astropy' module loaded.\n")
        mpl_install = True
    except:
        print()
        print("WARNING: 'Astropy' module has not been found in the system.")
        print("         'Astropy' module is needed for real-time search in spectroscopic databases.")
        print()
        print("INFO: Forcing 'Astropy' install...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "astropy"])
            print("INFO: 'matplotlib' installed succesfully.\n")
            astro_install = True
        except:
            print("WARNING: 'Astropy' can't be installed.\n")
            astro_install = False
            
    print("INFO: All modules checked\n")

    #Writting the header for cfg file
    cfg_file.write("#INITIAL CONFIGURATION REPORT FOR DEERs suite\n")
    cfg_file.write("#This file storages information about initial configuration needed to run DEERs software\n")

    if pd_install == True and np_install == True and sp_install == True:
        print("*********************************************")
        print("* Initial configuration loaded succesfully. *")
        print("*********************************************\n")

        #Write the configuration in cfg file
        cfg_file.write("INIT_CFG = True\n")
                                    
    else:
        print("WARNING: Error loading necesary modules. Program may not work properly.")

        #Write the configuration in cfg file
        cfg_file.write("INIT_CFG = False\n")

    #Writting modules' status, predefined environment variables and constants.
    cfg_file.write("#*********************************************************************************************************************************************\n")
    cfg_file.write("#MODULES' STATUS:\n")
    if pd_install == True:
        cfg_file.write("pd_install = True")
        cfg_file.write(" #Panda module installed.\n")
    else:
        cfg_file.write("pd_install = False")
        cfg_file.write(" #Panda module NOT instllaled. This module is necessary for a clean output visualization.\n")
    if np_install == True:
        cfg_file.write("np_install = True")
        cfg_file.write(" #Numpy module installed.\n")
    else:
        cfg_file.write("np_install = False")
        cfg_file.write(" #Numpy module NOT installed. This module is necessary for automated peak finding. This feature will not work.\n")
    if sp_install == True:
        cfg_file.write("sp_install = True")
        cfg_file.write(" #SciPy module installed.\n")
    else:
        cfg_file.write("sp_install = False")
        cfg_file.write(" #SciPy module NOT instllaled. This module is necessary for automated peak finding. This feature will not work.\n")
        cfg_file.write("#WARNING: SciPy installation errors could arise from running Python in 32-bits. Make sure you are running on a 64-bits.")
    if mpl_install == True:
        cfg_file.write("mpl_install = True")
        cfg_file.write(" #matplotlib module installed.\n")
    else:
        cfg_file.write("mpl_install = False")
        cfg_file.write(" #matplotlib module NOT instllaled. This module is necessary for graph plotting. Many features will not work.\n")
    if astro_install == True:
        cfg_file.write("astro_install = True")
        cfg_file.write(" #Astropy module installed.\n")
    else:
        cfg_file.write("astro_install = False")
        cfg_file.write(" #Astropy module NOT instllaled. This module is necessary real-time search in spectroscopic databases. Some features will not work.\n")

    cfg_file.write("#*********************************************************************************************************************************************\n")
   
    
    cfg_file.close()
