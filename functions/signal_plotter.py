from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QVBoxLayout, QWidget
from .plot_functions import plot_magnitude_signal_to_axes  # переиспользуем вашу функцию


class SignalPlotter:
    def __init__(self, parent_widget: QWidget):
        """
        Инициализирует график внутри указанного QWidget из .ui файла.
        :param parent_widget: QWidget с objectName например "plot_time_Widget"
        """
        if parent_widget is None:
            raise ValueError("parent_widget не может быть None")

        # Создаём фигуру и холст
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Добавляем холст в layout родительского виджета
        if parent_widget.layout() is None:
            layout = QVBoxLayout()
            parent_widget.setLayout(layout)
        parent_widget.layout().addWidget(self.canvas)

        # Одна ось
        self.ax = self.figure.add_subplot(111)

    def plot_signal(self, signal):
        """Обновляет график с новым сигналом."""
        plot_magnitude_signal_to_axes(signal, self.ax)
        self.canvas.draw()