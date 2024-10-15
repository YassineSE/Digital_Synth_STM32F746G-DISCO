#!/usr/bin/python
#jupyter-qtconsole
import numpy as np
from scipy.signal import dlti
from control import *
from scipy import signal
from scipy.signal import freqz, get_window
import matplotlib.pyplot as plt
import sys
#=================================================
#  		CAHIER DES CHARGES
#=================================================
sample_rate=44100.0
Filter_Order = 63 # low pass filter -> ODD | high pass filter -> EVEN
Filter_Type='low' # low / high / bandpass / bandstop
cutoff_1_hz = 0   # 0.0 if low or high pass filter
cutoff_2_hz = 4500.0
numtaps = Filter_Order + 1  # Length of the filter (number of coefficients, i.e. the filter order + 1)
#=================================================
#       CALCUL DES COEFFICIENTS
#=================================================
nyq_rate = sample_rate / 2.
norm_freq1=cutoff_1_hz/nyq_rate
norm_freq2=cutoff_2_hz/nyq_rate
if Filter_Type=='low':
   fir_coeff = signal.firwin(numtaps, norm_freq2, window='hamming')
elif Filter_Type=='high':
   fir_coeff = signal.firwin(numtaps, norm_freq2,pass_zero=False, window='hamming')
elif Filter_Type=='bandpass':
   fir_coeff = signal.firwin(numtaps, [norm_freq1, norm_freq2],pass_zero=False,window='hamming')
elif Filter_Type=='bandstop':   
   fir_coeff = signal.firwin(numtaps, [norm_freq1, norm_freq2],window='hamming')
print(fir_coeff)
#=================================================
#       TRACES
#=================================================
plt.subplot(211)
f, h = signal.freqz(fir_coeff, fs=sample_rate)
h_dB = 20*np.log10(abs(h))
plt.plot(f,h_dB)
plt.subplot(212)
h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
plt.subplot(212)
plt.plot(f,h_Phase)
# MISE EN FORME
plt.subplot(211)
plt.ylabel("Module $H(e^{j\omega})\ en\ dB$")
plt.xlabel("Frequence [Hz]")
plt.xlim([0, sample_rate/2])
plt.grid()
plt.subplot(212)
plt.ylabel("Phase $H(e^{j\omega})\ en\ rad$")
plt.xlabel("Frequence [Hz]")
plt.xlim([0, sample_rate/2])
plt.grid()
plt.show()
#=================================================
#      MISE EN FORME DANS UN FICHIER
#=================================================
fd = open("FIR.txt", "a")
fd.truncate(0)
print("float h_%s_%d_%d__f32[%d]=\n{" % (Filter_Type,cutoff_1_hz,cutoff_2_hz,numtaps),file=fd)
for i in range(numtaps):
    print("%f" % fir_coeff[i],end =",",file=fd)
print("\n};\n", file=fd)
print("int16_t h_%s_%d_%d__q15[%d]=\n{" % (Filter_Type,cutoff_1_hz,cutoff_2_hz,numtaps),file=fd)
for i in range(numtaps):
    print("%d" % int(fir_coeff[i]*32768),end =",", file=fd)
print("\n};\n", file=fd)
fd.close()
#============================================================