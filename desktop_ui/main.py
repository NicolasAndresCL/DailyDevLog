import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTabWidget, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

from desktop_ui.forms.task_form import TaskForm
from desktop_ui.views.history_view import HistoryView
from desktop_ui.views.stats_view import StatsView
from desktop_ui.views.export_view import ExportView

class DailyDevLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛠️ DailyDevLog")
        self.setGeometry(100, 100, 1100, 720)
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon("media/icon.png"))  # Opcional: ícono personalizado

        self._init_views()
        self._init_ui()

    def _init_views(self):
        """Inicializa las vistas compartidas entre pestañas."""
        self.history_view = HistoryView()
        self.task_form = TaskForm(history_view=self.history_view)
        self.stats_view = StatsView()
        self.export_view = ExportView()

    def _init_ui(self):
        """Construye la interfaz principal con encabezado y pestañas."""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header = self._build_header()
        tabs = self._build_tabs()

        main_layout.addWidget(header)
        main_layout.addWidget(tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _build_header(self):
        """Crea el encabezado visual con estilo profesional."""
        header = QLabel("📘 Bienvenido a tu registro diario TI")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        return header

    def _build_tabs(self):
        """Crea el sistema de pestañas con vistas integradas."""
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setDocumentMode(True)
        tabs.setStyleSheet("QTabBar::tab { padding: 10px 20px; font-weight: bold; }")

        tabs.addTab(self.task_form, "📝 Registrar tarea")
        tabs.addTab(self.history_view, "📂 Historial")
        tabs.addTab(self.stats_view, "📊 Gráfico de horas")
        tabs.addTab(self.export_view, "📤 Exportaciones")

        return tabs

def main():
    app = QApplication(sys.argv)
    window = DailyDevLogWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
