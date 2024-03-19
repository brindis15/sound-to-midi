# sound-to-midi
This project is about creating an application that reads audio in realtime from an audio input, finds the fundamental frequency and sends the corresponding MIDI note to a MIDI device.

## Block diagram

*[raw audio]->[DAC]* ->[audio sampling]->[FFT]->[note identification]->[MIDI output]-> *[MIDI device]->[DAW or VST]*

The center blocks are implemented by a Python application that uses the following libraries:
- sounddevice is used to read audio input
- struct      is used to unpack the audio input in a format accepted by the
- numpy FFT   is used to convert the audio signal to a frequency spectrum
- mido        is used to send MIDI messages to the MIDI device

To implement the frequency identification I studied the [ProcesamientoDatos](https://github.com/DavidReveloLuna/ProcesamientoDatos) project by David Revelo Luna.
