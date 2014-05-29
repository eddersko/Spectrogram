'''
File: spectrogram.py
Author: Edwin Ko
Purpose: A simple script that computers a spectrogram given an array of musical signal.
'''
import cmath
import array
import contextlib
import wave
from math import sin, cos, pi, log

scale = [26.71712838,
28.30581151,
29.98896265,
31.77219916,
33.66147244,
35.66308775,
37.78372531,
40.03046253,
42.4107977,
44.93267496,
47.60451086,
50.43522238,
53.43425676,
56.61162302,
59.9779253,
63.54439833,
67.32294488,
71.32617551,
75.56745061,
80.06092506,
84.8215954,
89.86534993,
95.20902171,
100.8704448,
106.8685135,
113.223246,
119.9558506,
127.0887967,
134.6458898,
142.652351,
151.1349012,
160.1218501,
169.6431908,
179.7306999,
190.4180434,
201.7408895,
213.7370271,
226.4464921,
239.9117012,
254.1775933,
269.2917795,
285.304702,
302.2698024,
320.2437002,
339.2863816,
359.4613997,
380.8360868,
403.481779,
427.4740541,
452.8929841,
479.8234024,
508.3551866,
538.5835591,
570.609404,
604.5396049,
640.4874005,
678.5727632,
718.9227994,
761.6721737,
806.963558,
854.9481082,
905.7859682,
959.6468047,
1016.710373,
1077.167118,
1141.218808,
1209.07921,
1280.974801,
1357.145526,
1437.845599,
1523.344347,
1613.927116,
1709.896216,
1811.571936,
1919.293609,
2033.420746,
2154.334236,
2282.437616,
2418.15842,
2561.949602,
2714.291053,
2875.691198,
3046.688695,
3227.854232,
3419.792433,
3623.143873,
3838.587219,
4066.841493,
4308.668472,
4564.875232,
4836.316839,
5123.899204,
5428.582105,
5751.382395,
6093.377389,
6455.708464,
6839.584866,
7246.287746,
7677.174438,
8133.682986,
8617.336945,
9129.750465,
9672.633678,
10247.79841,
10857.16421,
11502.76479,
12186.75478,
12911.41693,
13679.16973,
14492.57549,
15354.34888,
16267.36597,
17234.67389,
18259.50093,
19345.26736,
20495.59681]

chroma = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'] # mod 12

# complex variable i
i = complex(0.0, 1.0)

# Read a wave file and return the entire file as an array, and the parameters
# Parameters are:  (numChannels, sampleWidth, sampleRate, numFrames, not-used, not-used)
def readwav(fname):
    with contextlib.closing(wave.open(fname)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params

# akin to DFT - only takes window sizes of power of 2
def FFT(x):
    x = zeroPadding(x)
    N = len(x)
    mI2pidN = -i * 2.0 * pi / N
    
    if N == 1:
        return [complex(x[0])]
    else:
        E = []
        O = []
        for j in range(0, N, 2):
            E.append(x[j])
            O.append(x[j+1])
        E = FFT(E)
        O = FFT(O)
        X = [0]*N
        for k in range(N//2):
            t = cmath.exp(mI2pidN * k) * O[k]
            X[k] = E[k] + t
            X[k + (N//2)] = E[k] - t
        for k in range(len(X)):
            X[k] = X[k]/2
        return X

# pads the window with 0's if window size not a power of 2
def zeroPadding(x):
    N = len(x)
    if log(N, 2) == int(log(N, 2)):
        return x
    else:
        n = round(log(N, 2) + .5)
        k = (2 ** n) - N
        x = x + ([0] * k)
        return x

def getSpectrogram(x, params):
    
    sampleRate = params[2]
    
    current = 0
    window_size = 4096
    next = window_size
    slide = 2048

    amplitude = []      # list of lists
    
    while(next < len(x)):
        amp = [] 
        spectra = FFT(x[current:current+window_size])
        for i in range(len(spectra)):
            a = spectra[i].real
            if abs(a) < 1:
                a = 1
            amp.append((log(abs(a))/log(2)))
        amplitude.append(amp)
        # update condition
        current += slide
        next += slide
        
    bins = len(amplitude[0])/2 # nyquist limit
    frequency = []

    for i in range(bins):
        frequency.append(i * (sampleRate/float(window_size)))

    for i in range(len(amplitude)):
        amplitude[i] = amplitude[i][:bins]

    spectro = [0]*len(amplitude)
    spectrogram = []
    for i in range(116):
        spectrogram.append(spectro[:])

    for i in range(len(amplitude)):
        for j in range(len(frequency)):
            for k in range(len(scale)):
                if k == len(scale)-1:
                    break
                if frequency[j] >= scale[k] and frequency[j] < scale[k+1]:
                    if amplitude[i][j] > spectrogram [k][i]:
                        spectrogram[k][i] = int(amplitude[i][j])
                        break
    return spectrogram

def printSpectrogram(x):
    for i in range(len(x)-1, -1, -1):
        chrome = chroma[i%12]
        print chrome, x[i]
    
def main():
    print "This is a simple script that computes a spectrogram."
    infileName = raw_input("Enter the name of the input .wav file: ")
    data, params = readwav(infileName)
    spectrogram = getSpectrogram(data, params)
    printSpectrogram(spectrogram)
    
main()
    
