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
  data, fs = read_wave_file("alo-do-lula.wav")
  data = data[:,0]

  # Valores entre -1 e 1
  max_value = np.max(np.abs(data))
  data = data / max_value
  t = np.arange(0, len(data)/fs, 1/fs)

  # play_sound(data, fs) # Sem spoiler para o professor

  # Plotar o gráfico do sinal
  plt.plot(t, data)
  plt.title("Gráfico sinal de áudio normalizado")
  plt.show()

  # Remove acima de 2.2Khz
  W = fftfreq(data.size, d=1/fs)
  f_signal = rfft(data)

  cut_f_signal = f_signal.copy()
  for i in range(len(W)):
    if np.abs(W[i] > 4400):
      cut_index = i
      break
  cut_f_signal[cut_index:] = 0

  new_signal = irfft(cut_f_signal)

  plt.plot(t, new_signal)
  plt.title("Gráfico sinal de áudio filtrado")
  plt.show()

  signal = signalMeu()
  signal.plotFFT(new_signal, fs, "Gráfico 3: Domínio da frequência do sinal filtrado")
  # play_sound(new_signal, fs)

  # Modulação do sinal
  # Portadora
  a_carrier = 1
  f_carrier = 14000
  w_carrier = 2*pi*f_carrier

  carrier_wave = []
  for i in t:
    carrier_wave.append(a_carrier*sin(w_carrier*i))
  carrier_wave = np.array(carrier_wave)

  modulated_wave = []
  for i in range(len(carrier_wave)):
    modulated_wave.append(carrier_wave[i]*new_signal[i])
  modulated_wave = np.array(modulated_wave)

  # Normalizar
  max_value = np.max(np.abs(modulated_wave))
  modulated_wave = modulated_wave / max_value

  plt.plot(t, modulated_wave)
  plt.title("Gráfico sinal de áudio modulado no tempo")
  plt.show()
  play_sound(modulated_wave, fs)

  signal.plotFFT(modulated_wave, fs, "Gráfico 4: Domínio da frequência do sinal modulado (Fourier)")

  export_wave_file("modulated.wav", modulated_wave, fs)

if __name__ == "__main__":
  main()

