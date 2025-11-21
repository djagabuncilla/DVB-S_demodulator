import math, struct
import matplotlib.pyplot as plt
from .FFT import plot_spectrum


def plot_time_signal(signal):
    if not signal:
        raise ValueError("filtered_signal пустой!")

    t = list(range(len(signal)))

    real_part = [z.real for z in signal]
    imag_part = [z.imag for z in signal]
    magnitude = [abs(z) for z in signal]

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t, real_part, label='Real (I)', color='blue')
    plt.title('Real Part (I)')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(t, imag_part, label='Imag (Q)', color='orange')
    plt.title('Imaginary Part (Q)')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(t, magnitude, label='Magnitude', color='green')
    plt.title('Magnitude |z|')
    plt.xlabel('Sample Index')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
    
def read_pcm_file(filename, N, max_ampl_mV=0.488281):
    with open(filename, 'rb') as f:
        f.seek(0)
        raw_bytes = f.read(N * 4)
    signal = []
    for i in range(0, len(raw_bytes), 4):
        if i + 3 < len(raw_bytes):
            i_val, q_val = struct.unpack('<hh', raw_bytes[i:i+4])
            signal.append(complex(i_val, q_val))
    max_dig = 2**15 - 1
    scale = max_ampl_mV / max_dig
    return [z * scale for z in signal[:N]]

def frequency_shift(signal, freq_bin, N):

    shifted_signal = []
    for n in range(len(signal)):
        angle = -2 * math.pi * freq_bin * n / N
        rotator = math.cos(angle) - 1j * math.sin(angle)
        shifted_signal.append(signal[n] * rotator)
    return shifted_signal

def fast_fourier_transform(compl_sig):
    N = len(compl_sig)
    if N <= 1:
        return compl_sig
    ch = fast_fourier_transform(compl_sig[0::2])
    nch = fast_fourier_transform(compl_sig[1::2])
    result = [0j] * N
    for k in range(N // 2):
        angle = -2 * math.pi * k / N
        w = math.cos(angle) + 1j * math.sin(angle)
        t = w * nch[k]
        result[k] = ch[k] + t
        result[k + N//2] = ch[k] - t
    return result

def inverse_fast_fourier_transform(compl_sig):
    N = len(compl_sig)
    if N <= 1:
        return compl_sig

    ch = inverse_fast_fourier_transform(compl_sig[0::2])
    nch = inverse_fast_fourier_transform(compl_sig[1::2])

    result = [0j] * N
    for k in range(N // 2):
        angle = 2 * math.pi * k / N
        w = math.cos(angle) + 1j * math.sin(angle)
        t = w * nch[k]
        result[k] = ch[k] + t
        result[k + N//2] = ch[k] - t


    return [x / 2 for x in result]

def freq_cut(spectr, f1, f2, N):
    result = [0j] * N
    for i in range(N//2 + f1, N//2 + f2+1):
        result[i] = spectr[i]
    return result
def fftshift(ampl):
    N = len(ampl)
    return ampl[N//2:] + ampl[:N//2]

def first_computation():
    filename = 'add_resources/333.pcm'
    N = 8192
    carrier_bin = 1441
    signal = read_pcm_file(filename, N)
    signal = frequency_shift(signal, carrier_bin, N)

    # FFT
    ampl = fast_fourier_transform(signal)
    ampl = fftshift(ampl)
    ampl.reverse()
    ampl = freq_cut(ampl, -380, 380, N)
    #вернём форму спектра обратно
    ampl = fftshift(ampl)
    ampl.reverse()

    filtered_signal = inverse_fast_fourier_transform(ampl)

    #plot_time_signal(filtered_signal)
    return filtered_signal

def building_a_spectrum(signal, N):
    spectrum = fast_fourier_transform(signal)
    spectrum = fftshift(spectrum)
    spectrum.reverse
    ampl = [z / len(signal) for z in ampl]  # нормализуем по длине сигнала
    amplitude = [math.sqrt(z.real**2 + z.imag**2) for z in ampl]
    plot_spectrum(amplitude)




