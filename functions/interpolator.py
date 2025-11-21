from IFFT import first_computation, plot_time_signal
filtered_signal = first_computation()

def polynomial_interp(x_vals, y_vals, x):
    """
    Обобщённая интерполяция полиномом Лагранжа
    x_vals, y_vals: список координат
    x: точка, в которой вычисляем
    """
    n = len(x_vals)
    assert n == len(y_vals)
    result = 0.0
    for i in range(n):
        xi, yi = x_vals[i], y_vals[i]
        Li = 1.0
        for j in range(n):
            if i != j:
                xj = x_vals[j]
                Li *= (x - xj) / (xi - xj)
        result += yi * Li
    return result

def interpolate_signal(signal, numerator, denominator):
    interpolated_signal = []

    for counter in range(0, len(signal), denominator):
        selection = signal[counter:counter + denominator]
        if len(selection) < denominator:
            # Можно пропустить или дополнить последний блок
            continue

        real_part = [z.real for z in selection]
        imag_part = [z.imag for z in selection]

        x_vals = list(range(len(selection)))


        for j in range(numerator):
            # x от 0 до denominator-1
            x = j * (len(selection) - 1) / (numerator - 1) if numerator > 1 else 0
            real_interp = polynomial_interp(x_vals, real_part, x)
            imag_interp = polynomial_interp(x_vals, imag_part, x)
            interpolated_signal.append(complex(real_interp, imag_interp))

    return interpolated_signal

interpolated_signal = interpolate_signal(filtered_signal, 16, 8)  # 10 точек на 3
print(len(filtered_signal))
print(len(interpolated_signal))
plot_time_signal(filtered_signal)
plot_time_signal(interpolated_signal)
