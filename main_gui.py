import sys
import numpy as np
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QFileDialog, QPushButton  # ← для диалога выбора файла
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from functions.functions import *
from functions.signal_plotter import SignalPlotter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file_path = None
        self.signal = None
        loader = QUiLoader()
        ui_file = QFile("qt_gui/main_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.plotter = SignalPlotter(self.ui.findChild(QWidget, "plot_time_Widget"))
        #self._plot_signal()

        choose_button = self.ui.findChild(QWidget, "pushButton_choose_file")
        choose_button.clicked.connect(self.on_choose_file_clicked)

    def save_signal(self, filename, N):
        signal = read_pcm_file(filename, N)
        return signal
    
    # def _plot_signal(self):
    #     t = np.linspace(0, 10, 200)
    #     signal = np.exp(1j * 2 * np.pi * 0.5 * t)  # комплексный сигнал
    #     self.plotter.plot_signal(signal)

    def on_choose_file_clicked(self):
        """Обработчик нажатия кнопки выбора файла."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл сигнала",
            "",  # начальная директория — можно указать, например, "C:/Data"
            "Все файлы (*);;Текстовые файлы (*.txt);;Бинарные файлы (*.bin);;CSV (*.csv)"
        )
        if file_path:
            self.selected_file_path = file_path
            print(f"Выбран файл: {self.selected_file_path}")
            self.signal = self.save_signal(self.selected_file_path, 8192)
            self.plotter.plot_signal(self.signal)

        else:
            print("Файл не выбран")
        

    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()