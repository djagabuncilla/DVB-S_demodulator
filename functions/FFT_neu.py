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

def fftshift(ampl):
    N = len(ampl)
    return ampl[N//2:] + ampl[:N//2]

def apply_hamming_window(signal):
    N = len(signal)
    if N <= 1:
        return signal
    return [signal[n] * (0.54 - 0.46 * math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]


filename = 'add_resources/333.pcm'
N = 8192
carrier_bin = 1441
signal = read_pcm_file(filename, N)
signal = frequency_shift(signal, carrier_bin, N)
#signal = apply_hamming_window(signal)

# FFT
ampl = fast_fourier_transform(signal)
ampl = [z / len(signal) for z in ampl]


amplitude = [abs(z) for z in ampl]
shifted_amplitude = fftshift(amplitude)
shifted_amplitude.reverse()

# В дБ
max_amp = max(shifted_amplitude)
if max_amp == 0:
    max_amp = 0.48
eps = 1e-12
db_spectrum = [20 * math.log10(max(a / max_amp, eps)) for a in shifted_amplitude]

freqs = [-N//2 + k for k in range(N)]

# График
plt.figure(figsize=(12, 3))
plt.plot(freqs, db_spectrum)
plt.title('Амплитудный спектр (в дБ)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда, дБ')
plt.grid(True)
plt.xlim(-N//2, N//2)
plt.ylim(-70, 10)
plt.show()