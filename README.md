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
- You will need a software to produce the actual sounds and send them to the audio output. In Windows, you can use the built-in *Microsoft GS Wavetable Synth*; you can instead use standalone VST (virtual instrument) or a VST plus a DAW (digital audio controller, e.g. Reaper, Ableton Live, Cubase, etc.). In any case, you have to set your VST input or DAW MIDI track input to use the loopMIDI output.

In summary, the route of the sound will be:

*raw audio->[DAC]->[USB]*->[this application]-> *[loopMIDI]->[VST or VST+DAW]->sound output*

## Creating the environment and installing packages (Windows)
After installing Python, you must run the following commands in the command window to create an environment, import the required libraries and run the application. The "root_path" is the root folder where you will create an environment (e.g. C:\, C:\Users\<user>\Documents, etc.):

C:\Users\\*<current_user>*> **cd <root_path>**

*<root_path>*> **python -m venv audio2midi**

This will create a **audio2midi** folder in the root path, which includes some folders, packages and scripts used for development.

*<root_path>*> **cd audio2midi**

*<root_path>\\audio2midi*> **scripts\\activate**

(audio2midi) *<root_path>\\audio2midi*> 

As shown in the prompt, we have activated the *audio2midi* environment. Now we need to install the necessary packages.

(audio2midi) *<root_path>\\audio2midi*> **python -m pip install numpy**

*(if requested, run **python -m pip install --upgrade pip**)*

(audio2midi) *<root_path>\\audio2midi*> **python -m pip install sounddevice**

(audio2midi) *<root_path>\\audio2midi*> **python -m pip install mido**

Finally, copy the **audio2midi.py** file to the environment folder (<root_path>\\audio2midi).

## Running the application
First, make sure you have running the other applications (loopMIDI and VST or DAW) and set the input for the VST (or the input for the MIDI track in the DAW) to come from loopMIDI. If using a DAW, check that the corresponding MIDI track is in recording mode and not muted.

Then go back to the command window and run the application with:

(audio2midi) *<root_path>\\audio2midi*> **python -m audio2midi**

# Current issues and improvement ideas
