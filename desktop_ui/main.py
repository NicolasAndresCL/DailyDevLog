import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTabWidget
)
from desktop_ui.forms.task_form import TaskForm
from desktop_ui.views.history_view import HistoryView
from desktop_ui.views.stats_view import StatsView
from desktop_ui.views.export_view import ExportView

class DailyDevLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DailyDevLog")
        self.setGeometry(100, 100, 1000, 700)

        # Instancias únicas compartidas
        self.history_view = HistoryView()
        self.task_form = TaskForm(history_view=self.history_view)
        self.stats_view = StatsView()
        self.export_view = ExportView()

        # Layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Encabezado
        header = QLabel("📘 Bienvenido a tu registro diario TI")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(header)

        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.addTab(self.task_form, "📝 Registrar tarea")
        self.tabs.addTab(self.history_view, "📂 Historial")
        self.tabs.addTab(self.stats_view, "📊 Gráfico de horas")
        self.tabs.addTab(self.export_view, "📤 Exportaciones")

        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

def main():
    app = QApplication(sys.argv)
    window = DailyDevLogWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
