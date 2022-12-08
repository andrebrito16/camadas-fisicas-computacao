import soundfile as sf
import sounddevice as sd
from suaBibSignal import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import *
from math import *

def read_wave_file(file):
    data, fs = sf.read(file)
    return data, fs

def play_sound(signal, fs):
    sd.play(signal, fs)
    sd.wait()

def export_wave_file(file, signal, fs):
    sf.write(file, signal, fs)

def main():
  data, fs = read_wave_file("modulated.wav")
  signal = signalMeu()

  play_sound(data, fs)

  t = np.arange(0, len(data)/fs, 1/fs)

  a_carrier = 1
  f_carrier = 14000
  w_carrier = 2 * pi * f_carrier
  carrier_wave = []

  for i in t:
    carrier_wave.append(a_carrier * sin(w_carrier * i))
  carrier_wave = np.array(carrier_wave)

  demodulated_wave = []
  for i in range(len(carrier_wave)):
    demodulated_wave.append(data[i] * carrier_wave[i])
  demodulated_wave = np.array(demodulated_wave)

  plt.plot(t, demodulated_wave)
  plt.title("Gráfico sinal demodulado")
  plt.show()

  signal.plotFFT(demodulated_wave, fs, "Gráfico 3: Domínio da frequência do sinal demodulado")

  W = fftfreq(demodulated_wave.size, d=1/fs)
  f_signal = rfft(demodulated_wave)

  cut_f_signal = f_signal.copy()
  for i in range(len(W)):
    if np.abs(W[i]) > 4400:
      cut_index = i
      break
  
  cut_f_signal[cut_index:] = 0

  new_signal = irfft(cut_f_signal)
  signal.plotFFT(new_signal, fs, "Gráfico 3: Domínio da frequência do sinal filtrado")
  export_wave_file("demodulated.wav", new_signal, fs)
  play_sound(new_signal, fs)

if __name__ == "__main__":
  main()