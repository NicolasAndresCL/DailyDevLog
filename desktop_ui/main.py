import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTabWidget, QPushButton, QHBoxLayout
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
        self.setWindowIcon(QIcon("media/icon.png"))

        self._init_views()
        self._init_ui()

    def _init_views(self):
        self.history_view = HistoryView()
        self.task_form = TaskForm(history_view=self.history_view)
        self.stats_view = StatsView()
        self.export_view = ExportView()

    def _init_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        header = self._build_header()
        self.tabs = self._build_tabs()

        self.main_layout.addWidget(header)
        self.main_layout.addWidget(self.tabs)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setStyleSheet("background-color: #f4f6f9;")
        self.setCentralWidget(self.main_widget)

    def _build_header(self):
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("📘 Bienvenido a tu registro diario TI")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #34495e;")
        title.setAlignment(Qt.AlignLeft)

        btn_recargar = QPushButton("🔄 Recargar")
        btn_recargar.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        btn_recargar.clicked.connect(self._recargar_vistas)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(btn_recargar)
        container.setLayout(layout)
        return container

    def _build_tabs(self):
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setDocumentMode(True)
        tabs.setStyleSheet("""
            QTabBar::tab {
                background: #bdc3c7;
                color: #2c3e50;
                padding: 10px 20px;
                font-weight: bold;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: #2ecc71;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                top: -1px;
            }
        """)

        tabs.addTab(self.task_form, "📝 Registrar tarea")
        tabs.addTab(self.history_view, "📂 Historial")
        tabs.addTab(self.stats_view, "📊 Gráfico de horas")
        tabs.addTab(self.export_view, "📤 Exportaciones")

        return tabs

    def _recargar_vistas(self):
        self._init_views()
        self.main_layout.removeWidget(self.tabs)
        self.tabs.deleteLater()
        self.tabs = self._build_tabs()
        self.main_layout.addWidget(self.tabs)

def main():
    app = QApplication(sys.argv)
    window = DailyDevLogWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
