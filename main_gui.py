import sys
import numpy as np
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("qt_gui/main_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setup_plot()

    def setup_plot(self):
            # 1. Берём ссылку на QWidget из .ui
            plot_widget = self.ui.findChild(QWidget, "plotWidget")
            if plot_widget is None:
                raise RuntimeError("Не найден QWidget с objectName='plotWidget'")

            # 2. Создаём Figure и Canvas
            self.figure = Figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvas(self.figure)  # ← Это QWidget!

            # 3. Добавляем canvas в layout plot_widget
            #    (предполагается, что у plotWidget есть layout — иначе создадим)
            if plot_widget.layout() is None:
                from PySide6.QtWidgets import QVBoxLayout
                layout = QVBoxLayout()
                plot_widget.setLayout(layout)
            plot_widget.layout().addWidget(self.canvas)

            # 4. Рисуем график
            self.plot_data()

    def plot_data(self):
        # Очистка
        self.figure.clear()

        # Пример данных
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Создаём оси и строим
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, label="sin(x)", color="tab:blue")
        ax.set_title("График из matplotlib в Qt")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.legend()

        # Обновляем холст
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()