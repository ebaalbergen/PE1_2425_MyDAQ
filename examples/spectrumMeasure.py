"""
Simple example measurement of a LTI, and how to use
the Bode() class to extract information for the bode plots
"""
import numpy as np
from span.bode import Bode, plotBode
from span.daq import MyDAQ

# Create daq object
daq = MyDAQ()
daq.samplerate = 200_000
daq.name = "myDAQ1"
print(daq)

# Keep track of power and phase
powers = []
phases = []

# Do measurement in the domain [1Hz, 100kHz)
freqs = np.logspace(0, 5, 50)

# Measure over range of frequencies
for freq in freqs:
    print(freq)

    # Create sinusoidal waveform
    timeArray, signalIn = daq.generateWaveform("sine", daq.samplerate, frequency=freq)

    # Write to channel AO0 and read on channel AI0
    signalOut = daq.readwrite(signalIn, "AI0", "AO0")

    # Create Bode() instance
    bode = Bode(daq.samplerate, signalOut, signalIn)
    
    # Get power and phase of freq, with a bandwidth delta=1
    power = bode.getPower(freq, 1)
    phase = bode.getPhase(freq, 1)
    
    # Add to list
    powers.append(power)
    phases.append(phase)

# Plot the bode plots
plotBode(2*np.pi*freqs, np.sqrt(powers), phases)
