import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from extras.defs import pause, calculate_step
from extras.defs import peak_finder_script as pk

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


file="F:/LacticAcid_HeRun/37k-2x-CP3000-7000-LacticAcid-1bar-0Att-Max-80C-freq-freq.txt"

Frequency = np.loadtxt(file, delimiter="\t", usecols=0)
Spec = np.loadtxt(file, delimiter="\t", usecols=1)


#Frequency = np.array([ 5.0, 6.3, 8.0, 10.0, 12.5, 16.0, 20.0, 25.0, 31.5, 40.0, 50.0, 63.0, 80.0, 100.0, 125.0, 160.0, 200.0, 250.0, 315.0]) #third octave band spectrum, 19 Values
#Spec = np.array([ 40, 45, 51, 42, 44, 56, 42, 55, 57, 58, 45, 40, 38, 36, 32, 30, 28, 30, 29]) #noise level, 19 Values

blank_peaks = []
final_peaks = []
step = calculate_step(Frequency)

w = float(0.25)



#peaks, _ = find_peaks(Spec, prominence=1)
peaks, pInts = pk(file)
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

'''        
m = np.zeros(Frequency.shape, dtype=bool)
print(m)
print(final_peaks)
m[final_peaks] = True
'''

blanked_spectrum_x = []
blanked_spectrum_y = []

print(final_peaks)

pause()

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
