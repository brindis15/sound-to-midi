# sound-to-midi
This project is about creating an application that reads audio in realtime from an audio input, finds the fundamental frequency and sends the corresponding MIDI note to a MIDI device.

## Block diagram

*raw audio->[DAC]* ->[audio sampling]->[FFT]->[note identification]->[MIDI output]-> *[MIDI device]->[DAW or VST]->sound output*

The center blocks are implemented by a Python application that uses the following libraries:
- sounddevice is used to read audio input
- struct      is used to unpack the audio input in a format accepted by the
- numpy FFT   is used to convert the audio signal to a frequency spectrum
- mido        is used to send MIDI messages to the MIDI device

To implement the frequency identification I studied the [ProcesamientoDatos](https://github.com/DavidReveloLuna/ProcesamientoDatos) project by David Revelo Luna, in particular the real-time FFT example.

# Creating and using the application (Python 3.10.6)
## Other hardware and software required
- You will need a hardware to capture and digitalize the audio (DAC). I am currently using the Behringer UCA222, a *zero latency* device that receives audio input (RCA plugs) and sends the digitalized audio to the PC via USB.
- To produce the notes, you need a software MIDI device capable of receiving the MIDI messages. I am using [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) by Tobias Erichsen. Just install it and use the "+" button to create a virtual MIDI port.
- You will need a software to produce the actual sounds and send them to the audio output. In Windows, you can use the built-in *Microsoft GS Wavetable Synth*; you can instead use standalone VST (virtual instrument) or a VST plus a DAW (digital audio controller, e.g. Reaper, Ableton Live, Cubase, etc.). In any case, you have to set your VST input or DAW MIDI channel input to use the loopMIDI output.

In summary, the route of the sound will be:
*raw audio->[DAC]->[USB]*->[this application]-> *->[loopMIDI]->[VST or VST+DAW]->sound output*

## Installing and running the application
After installing Python, you must run the following commands in the command window to create an environment, import the required libraries and run the application:

## Current issues and improvement ideas
