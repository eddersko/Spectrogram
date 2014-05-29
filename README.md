Spectrogram
===========
This script outputs a spectrogram returns a 2-D array arranged in terms of the chromatic scale on the y-axis.

This was part of the programming assignment for CS591 Computational Audio with Professor Wayne Snyder.

Write a program spectrogram.py which contains a method getSpectrogram(x) which takes an array representing a musical signal, and returns a 2D array whose columns are a spectrum of the signal over a series of overlapping windows (each column represents one window). Use the FFT with a window size of 4096, and overlap by 2048. I would like you to organize the y-axis of this spectrum according to the chromatic scale, from the lowest note on the piano (A 22.5) to just under the Nyquist Limit (E 20495.5968); this will end up being a log scale, and can easily be transformed into a chroma of pitches. You should also scale the amplitudes logarithmically, by converting the 16-bit integer amplitude A into a double log(A) to the base 2. 
