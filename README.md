# DEERs
Data Editing and Examination for Rotational Spectroscopy

![Deers](https://github.com/user-attachments/assets/a68f70ea-15d8-4eb2-b3f5-8ebc33b47b38)

## Some info
    Name of the Program: DEERs
    First Beta-Version Release: Feb 19, 2024 
    Actual Program Version : 1.0
    Actual Program Version Date: Oct 21, 2024
    Author: Raúl Aguado Vesperinas

DEERs suite is an compilation of scripts that I have made during my PhD, working with FTMW spectroscopy techniques. It has been designed to facilitate the work with frequency-domain rotational spectra. The full list of functions available are summarized below. Futher information, bug reports or any other consideration about the program can be made by email at raaguado98@gmail.es.

I have to aknowledge **Sergio Mato's help** on the conceptual design and for the alpha- and beta-testing. GRACIAS SERGIO!

## Description of files

 Contents of the folders distributed in this version:
  - **extras/**       : some extra files (the help menu [coming soon will be a user manual], extra defs, the pre-configuration script and a database for molecular lookup)
  - **scripts/**      : Folder containing the scrips included in this version of DEERS
  - **DEERS.py**      : The interface connecting all scripts :O

## Pre-configuration
This suite is coded under Python 3.

Adittionally, I could add here a boring list of python libraries needed by DEERS to work properly but I really hate that, so I coded a simple script that will automatically check if you have the necessary modules and force the intallation of those missing.

Yeah, you are welcome.


Just connect to internet and run precfg.py file. This script will generate a configuration report (cfg.log) to sum up all about the installation of needed modules. Now you can use DEERS!

## Setting up external parameters
In **/extras/defs.py** there is a section named _Pre-defined environment variables_ which contains different variables that can be configured:
  - **cdms_db_path**    : location of your CDMS last backup
  - **madex_db_path**    : location of your MADEX last backup
  - **fragment_path**    : location of your own fragment database

CDMS and MADEX database backups can be downloaded from their project pages. The configuation of these paths here makes DEERs to check the directories every time you search for peaks in a database. The fragment database is a file used to storage every peak of the analyzed spectra that is not found in the CDMS or MADEX databases (this are unknown peaks).

## DEERs features
As I mentioned before, this is a compilation of different scripts that I coded during my PhD in order to automate or ease some processes in the investigation of rotational spectra. Here, a brief explanation of each module:
  - **Extract peaks from a spectrum:** this is a peak finding utility based on the SciPy _peak_finder_ module, this script takes a 2-column ASCII spectra and allows you to detect all the peaks in a spectrum and list them in a txt file. A automated detection is carried out based on the mean and RMS of the signal. However, the script will prompt the spectrum, highlighting detected peaks in red. If peaks have not been correctly detected, you also can change the security factor (SF), that controls the sensitivity when selecting peaks (more SF, more intensity needed to detect a peak and _viceversa_).
  - **Analyze SN ratio during a experiment:** during our broadband FTMW experiments, data captured by the oscilloscope is saved with regularity (_i.e._ every 5k-10k adquisition). The SN ratio of the experiment should increase as the number of adquisitions does, but certain experimental conditions could lead to a worse SN ratio in some cases. This script will take a folder that contains the same experiment data but with different acqusition and will compare the SN for a given signal and noise. This helps to locate the spectrum with the better SN ratio."
  - **Search for peaks in a database:** this script compares peaks with different spectroscopic databases such as MADEX or CDMS. The input peaks can be given from a .lin file (output of the ASCP program coded by Kisiel) or directly from a experimental spectrum. In the former case the frequencies will readed directly from de .lin file. Meanwhile, in the latter case, the _peak finding_ script will be used to locate peaks in a spectrum given as input. Then the frequencies obtained in of these manners will be compared with those present in the selected spectroscopic database. This database (for the moment) should be given as an adittional input. In _extras/_ folder, CDMS database is included (may not be the latest version, which can be downloaded from https://cdms.astro.uni-koeln.de/cgi-bin/cdmssearch) (I'm already working with Splatalogue to obtain always the latest version of the Databases).
  - **Remove lines from spectrum:** this script takes a spectrum and a list of frequencies, and allows to clean the first spectrum by zeroing the frequencies in the list with the desired width. 
  - **CHIRALITY mode:** this script has been coded for working with chiral tagging experiments. In those experiments a chiral tag is introduced with the sample to generate diasteroisomeric complexes that can be diferenciated by rotational spectroscopy (shotout here to Yungie Xu, Brooks Pate and other spectroscopist working on this technique). This script will take the spectrum of the chiral tag, the sample and the final (mixed) spectrum to clear any peak from sample and tag (by zeroing the frequencies in a given range), easing the analysis of the spectrum, as long as the final spectrum will only contain those signals of the complexes.
  - **Compare spectra:** this script will take two different spectra (2-column ASCII files) and compare the signals in them. It can generate a list of 1) coincident or 2) non-coincident peaks. Adittionally, it can blank 3) coincident or 4) non-coincident peaks. 
 

