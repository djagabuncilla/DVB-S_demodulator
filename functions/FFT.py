import math, struct


def read_pcm_file(filename, N, max_ampl_mV=0.488281):
    with open(filename, 'rb') as f:
        f.seek(256)
        raw_bytes = f.read(N * 8)  # N комплексных отсчетов = N * 2 * 4 байта

    raw_data = []
    for i in range(0, len(raw_bytes), 8):  # читаем по 8 байт (I и Q)
        if i + 7 < len(raw_bytes):
            i_val, q_val = struct.unpack('<ii', raw_bytes[i:i+8])  # unpack I и Q сразу
            raw_data.append(complex(i_val, q_val))

    max_dig = 2**31 - 1
    scale = max_ampl_mV / max_dig
    complex_signal = [z * scale for z in raw_data]  # масштабируем сразу комплексные значения
    return complex_signal[:N]  # возвращаем ровно N отсчетов

def fast_fourier_transform(compl_sig):
    N = len(compl_sig)
    if N <= 1:
        return compl_sig
    ch = fast_fourier_transform(compl_sig[0::2])
    nch = fast_fourier_transform(compl_sig[1::2])
    result = [0.0 + 0.0j] * N
    for k in range(N//2):
        angle = -2*math.pi * k/N
        w = math.cos(angle) + 1j * math.sin(angle)
        t = w * nch[k]
        result[k] = ch[k] + t
        result[k + N//2] = ch[k] - t
    return result

def slow_fourier_transform(compl_sig):
    N = len(compl_sig)
    spectr = [0.0 + 0.0j] * N
    for k in range (N):
        for n in range (N):
            W = complex(math.cos(2*math.pi*k*n/N), -math.sin(2*math.pi*k*n/N))
            spectr[k] += compl_sig[n] * W
    return spectr

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def fftshift(ampl):
    N = len(ampl)
    return ampl[N//2:] + ampl[:N//2]

def plot_spectrum(ampl):
    plt.figure(figsize=(12, 3))
    plt.plot(ampl)
    plt.title('Амплитудный спектр')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()

def apply_hamming_window(signal):
    N = len(signal)
    return [signal[n] * (0.54 - 0.46 * math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]


filename = '333.pcm'
N = 8192
signal = read_pcm_file(filename, N)
signal = apply_hamming_window(signal)
ampl = fast_fourier_transform(signal)
ampl = [z / len(signal) for z in ampl]  # нормализуем по длине сигнала

amplitude = [math.sqrt(z.real**2 + z.imag**2) for z in ampl]
shifted_amplitude = fftshift(amplitude)


plot_spectrum(shifted_amplitude)
