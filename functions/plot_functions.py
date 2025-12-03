def plot_magnitude_signal_to_axes(signal, ax):
    if len(signal) == 0:  # ← так можно и для list, и для np.ndarray
        raise ValueError("Сигнал пустой!")

    t = list(range(len(signal)))
    magnitude = [abs(z) for z in signal]

    ax.clear()
    ax.plot(t, magnitude, label='Magnitude', color='green')
    ax.set_title('Magnitude |z|')
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()