from scipy.io import wavfile
from scipy import signal, interpolate
import matplotlib.pyplot as plt
import numpy as np


def integral_image(img: np.array) -> np.array:
   integral_img = np.zeros(shape=img.shape)
   integral_img[0, 0] = img[0, 0]

   for x in range(1, img.shape[0]):
      integral_img[x, 0] = img[x, 0] + integral_img[x - 1, 0]

   for y in range(1, img.shape[1]):
      integral_img[0, y] = img[0, y] + integral_img[0, y - 1]

   for x in range(1, img.shape[0]):
      for y in range(1, img.shape[1]):
         integral_img[x, y] = img[x, y] \
                              - integral_img[x - 1, y - 1] \
                              + integral_img[x - 1, y] \
                              + integral_img[x, y - 1]

   return integral_img


def sum_in_frame(integral_img: np.array, x: int, y: int, frame_size: int):
   len = integral_img.shape[1] - 1
   hight = integral_img.shape[0] - 1

   half_frame = frame_size // 2
   above = y - half_frame - 1
   low = y + half_frame
   left = x - half_frame - 1
   right = x + half_frame

   A = integral_img[max(above, 0), max(left, 0)]
   B = integral_img[max(0, above), min(len, right)]
   C = integral_img[min(hight, low), max(left, 0)]
   D = integral_img[min(hight, low), min(right, len)]

   if max(left + 1, 0) == 0 and max(above + 1, 0) == 0:
      return D
   elif max(left + 1, 0) == 0:
      return D - B
   elif max(above + 1, 0) == 0:
      return D - C

   return D - C - B + A


def culculate_mean(integral_image: np.array, x: int, y: int, frame_size):
   square = frame_size ** 2
   s = sum_in_frame(integral_image, x, y, frame_size)
   return s // square


def change_sample_rate(path, new_sample_rate=22050):
   audioPath = "source/" + path
   old_samplerate, old_audio = wavfile.read(audioPath)

   if old_samplerate != new_sample_rate:
      duration = old_audio.shape[0] / old_samplerate

      time_old = np.linspace(0, duration, old_audio.shape[0])
      time_new = np.linspace(0, duration, int(old_audio.shape[0] * new_sample_rate / old_samplerate))

      interpolator = interpolate.interp1d(time_old, old_audio.T)
      new_audio = interpolator(time_new).T

      wavfile.write("result/" + path, new_sample_rate, np.round(new_audio).astype(old_audio.dtype))


def find_formants(freqs, integral_spec, x, frame_size):
   res = [0] * integral_spec.shape[0]

   for i in range(1, integral_spec.shape[0], frame_size):
      res[i] = culculate_mean(integral_spec, x, i, frame_size)

   origin = res.copy()
   res.sort()

   res = res[-3:]

   return list(map(lambda power: (int(freqs[origin.index(power)]), int(power)), res))


def find_all_formants(freqs, integral_spec, frame_size):
   res = set()
   for i in range(integral_spec.shape[1]):
      formant = find_formants(freqs, integral_spec, i, frame_size)
      form = list(map(lambda bind: bind[0], formant))
      for j in range(3):
         res.add(form[j])

   res.discard(0)
   return res


def power(freqs, integral_spec, frame_size, formant_s):
   power = dict()
   for i in formant_s:
      power[i] = 0

   for i in range(integral_spec.shape[1]):
      for j in find_formants(freqs, integral_spec, i, frame_size):
         if (j[0] != 0):
            power[j[0]] += j[1]

   return power


def spectrogram_plot(samples, sample_rate,t = 11000):
    frequencies, times, my_spectrogram = signal.spectrogram(samples, sample_rate, scaling = 'spectrum', window = ('hann'))
    spec = np.log10(my_spectrogram)
    plt.pcolormesh(times, frequencies, spec, shading='gouraud', vmin=spec.min(), vmax=spec.max())

    
    plt.ylim(top=t)
    plt.yticks(np.arange(min(frequencies), max(frequencies), 500))
    plt.ylabel('Частота [Гц]')
    plt.xlabel('Время [с]')
    return my_spectrogram, frequencies

if __name__ == '__main__':
   change_sample_rate("AA.wav")
   sample_rate_a , samples_a = wavfile.read("./source/AA.wav")

   dpi = 500
   spectogram_a, frequencies_a = spectrogram_plot(samples_a, sample_rate_a, 11000)
   plt.axhline(y = 344,  color = 'r', linestyle = '-', lw= 0.5, label = "Форманты")
   plt.axhline(y = 602,  color = 'r', linestyle = '-', lw= 0.5)
   plt.axhline(y = 861,  color = 'r', linestyle = '-', lw= 0.5)
   plt.axhline(y = 1119,  color = 'r', linestyle = '-', lw= 0.5)
   plt.legend()
   plt.savefig('result/spectrogram_a.png', dpi = dpi)
   plt.clf()

   change_sample_rate("I.wav")
   sample_rate_i , samples_i = wavfile.read("source/I.wav")
   spectogram_i, frequencies_i = spectrogram_plot(samples_i, sample_rate_i, 11000)
   plt.axhline(y = 344,  color = 'r', linestyle = '-', lw= 0.5, label = "Форманты")
   plt.axhline(y = 602,  color = 'r', linestyle = '-', lw= 0.5)
   plt.axhline(y = 86,  color = 'r', linestyle = '-', lw= 0.5)
   plt.axhline(y = 2928,  color = 'r', linestyle = '-', lw= 0.5)
   plt.legend()
   plt.savefig('result/spectrogram_i.png', dpi = dpi)
   plt.clf()

   change_sample_rate("bruh.wav")
   sample_rate_gav , samples_gav = wavfile.read("source/bruh.wav")
   spectogram_gav, frequencies_gav = spectrogram_plot(samples_gav, sample_rate_gav, 11000)
   plt.savefig('result/spectrogram_bruh.png', dpi = dpi)
   plt.clf()

   spec_a = integral_image(spectogram_a)
   
   formants_a = list(find_all_formants(frequencies_a, spec_a, 3))
   formants_a.sort()

   print("Минимальная частота для звука А: " + str(formants_a[0]))
   print("Максимальная частота для звука А: " + str(formants_a[-1]))

   print("Тембрально окрашенный тон для звука А: " + str(formants_a[0]))

   power_a = power(frequencies_a, spec_a, 3, formants_a)
   print(sorted(power_a.items(), key = lambda item: item[1], reverse=True))
   print("Четыре самые сильные форманты: " + str(sorted(power_a, key=lambda i: power_a[i])[-4:]))

   spec_i = integral_image(spectogram_i)
   
   formants_i = list(find_all_formants(frequencies_i, spec_i, 3))
   formants_i.sort()

   print("\n\nМинимальная частота для звука И: " + str(formants_i[0]))
   print("Максимальная частота для звука И: " + str(formants_i[-1]))

   print("Тембрально окрашенный тон для звука И: " + str(formants_i[0]))

   power_i = power(frequencies_i, spec_i, 3, formants_i)
   print(sorted(power_i.items(), key = lambda item: item[1], reverse=True))
   print("Четыре самые сильные форманты: " + str(sorted(power_i, key=lambda i: power_i[i])[-4:]))

   spec_gav = integral_image(spectogram_gav)
   
   formants_gav = list(find_all_formants(frequencies_gav, spec_gav, 5))
   formants_gav.sort()

   print("\n\nМинимальная частота для звука ГАВ: " + str(formants_gav[0]))
   print("Максимальная частота для звука ГАВ: " + str(formants_gav[-2]))

#    print("Тембрально окрашенный тон для звука ГАВ: " + str(formants_gav[0]))

#    power_gav = power(frequencies_gav, spec_gav, 5, formants_gav)
#    power_gav.pop(8268)
#    print(sorted(power_gav.items(), key = lambda item: item[1], reverse=True))
#    print("Четыре самые сильные форманты: " + str(sorted(power_gav, key=lambda i: power_gav[i])[-4:]))
