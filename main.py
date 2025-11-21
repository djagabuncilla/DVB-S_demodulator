from functions.functions import *
filename = 'add_resources/333.pcm'
N = 8192
signal = read_pcm_file(filename, N) #чтение файла
carrier_bin = 1441 #частота переноса в бинах 
signal = frequency_shift(signal, carrier_bin, N) #теперь несущая в центре графика
# plot_time_signal(signal)
# building_a_spectrum(signal, N)

#попыточка фильтрации через FIR-фильтр
# fc_bins = 380
# num_taps = 2048
# taps = generate_fir(fc_bins, num_taps, N)
# signal = fir_filter_apply(signal, taps)
# plot_time_signal(signal)

#теперь мы будем фильтровать сигнал с помощью IFFT
spectrum = fast_fourier_transform(signal)
spectrum = fftshift(spectrum)
spectrum = spectrum.reverse()
spectrum = freq_cut(spectrum, -380, 380, N)
spectrum = fftshift(spectrum)
spectrum.reverse()
filtered_signal = inverse_fast_fourier_transform(spectrum)
#проверим сигнал и спектр
plot_time_signal(filtered_signal)
plot_spectrum(filtered_signal)



