
# Este módulo permite seleccionar una entrada de audio, escucha esa entrada,
# e identifica la frecuencia fundamenal cada hop_size segundos
# Para usar MIDI hay que instalar mido con la opción de backend, ej 'py -m pip install mido[ports-rtmidi]'
# y posiblemente hay que instalar rtmidi también

# Para usar, abrir ventana CMD e ingresar:
# cd C:\Users\Usuario\OneDrive\Documentos\audio-env
# scripts\activate
# py -m fundamentales

# Importar módulos
import numpy as np               # funciones numéricas
import numpy.fft as fourier      # FFT, alternativa: import scipy.fftpack as fourier
import sounddevice as sd         # para seleccionar dispositivo y leer el audio
import mido                      # biblioteca para MIDI
import struct                    # para desempaquetar los bytes de audio

# Parámetros preconfigurados
sample_type = 'int16'
sample_freq = 44100    # Frecuencia de muestreo (Hz)
block_size = 1024      # Cantidad de frames en el bloque de análisis, ej 2048
# Tiempo que dura en muestrear un block_size: block_size/sample_freq milisegundos
# Menor frecuencia que puede detectarse: sample_freq/block_size
debug = False

# Inicializaciones:
# - Nombres de las notas y Frecuencias 
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
for i in range(3): note_names = np.append(note_names, note_names)
note_names = note_names[:88] # nombres de las 88 teclas del piano
note_freq_list = np.geomspace(13.75, 2093, num=88) # freq de las 88 teclas del piano
# - Frecuencias que calcula FFT
fft_freqs = sample_freq/block_size*np.arange(0, block_size//2)
# - Valores por defecto de muestreo por sounddevice
sd.default.samplerate = sample_freq
sd.default.dtype = sample_type, None
sd.default.channels = 1, None
sd.default.blocksize = block_size
sd.default.latency ='low', 'low'
# - Backend para MIDO
# mido.set_backend('mido.backends.portmidi')
# - Valores para registrar última nota detectada y pico
prev_midi = -1
prev_pk = -1

# Función para seleccionar dispositivo de entrada
def seleccionar_entrada():
  # Enumera dispositivos
  dispos = sd.query_devices() # si especificara 'input' solo trae el input por defecto
  for i in range(len(dispos)):
    di = dispos[i]
    dn = di['name']
    if (di['max_input_channels']>0): print(i, "-", dn)
  bad_sel = True
  while bad_sel:
    dev_index = int(input('Ingrese el nro de dispositivo:'))
    if ((dev_index>=0) and (dev_index<len(dispos))):
      input_dev = sd.query_devices(dev_index)
      bad_sel = (input_dev['max_input_channels']==0)
  try:
    sd.check_input_settings(dev_index, channels=1, dtype=sample_type, samplerate=sample_freq)
  except:
    print('Input settings not supported')
    sys.exit(1)
  print("Sample frequency: ", sample_freq)
  print("Sample type     : ", sample_type)
  print("Block size      : ", block_size)
  print("Block duration  : ", int(1000*block_size/sample_freq), "ms")
  print("Min frequency   : ", int(sample_freq/block_size))
  print('\n')
  return dev_index

# Función para seleccionar MIDI port
def seleccionar_salida():
  dispos = mido.get_output_names()
  for i in range(len(dispos)):
    print(i, "-", dispos[i])
  bad_sel = True
  while bad_sel:
    dev_index = int(input('Ingrese el nro de dispositivo:'))
    if ((dev_index>=0) and (dev_index<len(dispos))):
      bad_sel = False
  print('\n')
  return dispos[dev_index]

# Función para calcular la frecuencia fundamental
def calcular_fundamental(audio_chunk, fft_freqs):
  # Transformada de Fourier
  spectrum = abs(fourier.fft(audio_chunk)) #.astype('int16') # los valores son altos, más rápido con enteros?
  # NO HACE FALTA ACA, es param fft_freqs = fourier.fftfreq(len(spectrum), d=1/sample_freq)
  # PODRIA PROBAR SIN TOMAR MITAD SINO TODO, POR LAS DUDAS QUE PIERDA PRECISION Y SE EQUIVOQUE POR ESO
  spectrum = spectrum[0:block_size//2]  # tomar la primera mitad (es simétrica)
  max_index = np.argmax(spectrum[1:]) + 1 # Encontrar el pico más alto (excluyendo la componente DC)
  pk = spectrum[max_index]
  # EXPERIMENTAL (porque a veces el primer armónico da un pico más alto, porque no son exactos):
  max_index2 = max_index - 2
  if max_index2>1:
    max_index2 = np.argmax(spectrum[1:max_index2]) + 1 # Encontrar el pico más alto anterior
    if 2*spectrum[max_index2]>pk:
      max_index = max_index2
  # fin experimental
  fundamental_freq = fft_freqs[max_index]
  peak = spectrum[max_index]/block_size
  if debug and peak>40:
    f = open("spectrum.csv", "a")
    for i in range(block_size//8):
      a = str(int(spectrum[i])) + ';'
      f.write(a)
    f.write('\n')
    f.close()
  return fundamental_freq, peak

# Función para encontrar la nota correspondiente a la frecuencia
def encontrar_nota(f):
  found = len(note_freq_list)
  for i in range(len(note_freq_list)):
    if note_freq_list[i]>=f:  # la nota está entre i e i-1
      if i==0:
        found = i
      else:
        if note_freq_list[i]==f:
          found = i
        else:
          corte = 1.0293 * note_freq_list[i-1] # da la frec. intermedia considerando alinealidad
          if f<corte:
            found = i-1
          else:
            found = i
      break
  if found>87: found = 87  # revisar, no debería ser mayor a menos que haya puesto uno de más en note_freq_list
  nota = note_names[found]
  octava = int((i+9)/12)-1
  return found+9, nota+str(octava) # número MIDI y string descriptivo

# Selecciona entrada audio y salida MIDI
sd.default.device = seleccionar_entrada(), None
MIDIout = mido.open_output(seleccionar_salida())

# Inicia la captura de audio, bloquea cada vez que lee
print("Capturando audio. Presiona Ctrl+C para detener...")
try:
  while True:
    recdata = sd.rec(block_size) # recibe block_size frames de audio
    sd.wait()                    # espera hasta asegurarse que llenó el bloque
    recdataInt = struct.unpack(str(block_size) + 'h', recdata)  # IMPORTANTE convierte al tipo de datos adecuado
    freq, peak = calcular_fundamental(recdataInt, fft_freqs)    # Calcula la frecuencia fundamental
    midi, nota = encontrar_nota(freq)
    if peak>60:
      print(f"F={freq:.2f}Hz, A={peak}, N={nota}, MIDI={midi}")
      if (midi!=prev_midi) or (peak>prev_peak): # ¿y si toca más suave? ¿cómo detectar ataque?
        msg = mido.Message('control_change', control=123) # all notes off
        MIDIout.send(msg)
        msg = mido.Message('note_on', note=midi)
        MIDIout.send(msg)
        prev_midi = midi
    elif prev_midi>0:
      msg = mido.Message('control_change', control=123) # all notes off, es más seguro que note_off
      MIDIout.send(msg)
      prev_midi = -1
    prev_peak = peak
    # conviene poner un sd.sleep(5)?
except KeyboardInterrupt: 
  MIDIout.close()
  sd.stop()
  print("\nCaptura de audio detenida.")
