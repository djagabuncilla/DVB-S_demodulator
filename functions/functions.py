import math, struct
import matplotlib.pyplot as plt

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

def apply_hamming_window(signal):
    N = len(signal)
    if N <= 1:
        return signal
    return [signal[n] * (0.54 - 0.46 * math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]

def plot_spectrum(spectrum, N):
    freqs = [-N//2 + k for k in range(N)]
    plt.figure(figsize=(12, 3))
    plt.plot(freqs, spectrum)
    plt.title('Амплитудный спектр (в дБ)')
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда, дБ')
    plt.grid(True)
    plt.xlim(-N//2, N//2)
    plt.ylim(-70, 10)
    plt.show()

def conversion_to_a_logarithmic_scale(amplitude):
    max_amp = max(amplitude)
    if max_amp == 0:
        max_amp = 0.48
    eps = 1e-12
    db_ampl = [20 * math.log10(max(a / max_amp, eps)) for a in amplitude]
    return db_ampl

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

def building_a_spectrum(signal, N):
    spectrum = fast_fourier_transform(signal)
    spectrum = fftshift(spectrum)
    spectrum.reverse
    ampl = [z / len(spectrum) for z in spectrum]  # нормализуем по длине сигнала
    amplitude = [math.sqrt(z.real**2 + z.imag**2) for z in ampl]
    plot_spectrum(amplitude, N)