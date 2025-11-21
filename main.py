from functions.functions import *
filename = 'add_resources/333.pcm'
N = 8192
signal = read_pcm_file(filename, N)
carrier_bin = 1441
signal = frequency_shift(signal, carrier_bin, N)
plot_time_signal(signal)
building_a_spectrum(signal, N)

