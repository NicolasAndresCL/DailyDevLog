# main.py
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QIcon

from forms.task_form import TaskForm
from views.history_view import HistoryView
from views.stats_scroll import StatsScroll
from views.export_view import ExportView
from views.stats_view import StatsView


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("💻 Dashboard TI diarias")
        self.showMaximized()
        self._pool = QThreadPool.globalInstance()
        self._init_ui()

        # 🎨 Estilo global inspirado en Visual Studio Code (Dark+)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #D4D4D4;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QLineEdit, QTextEdit, QDoubleSpinBox {
                background-color: #252526;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 6px;
                color: #D4D4D4;
            }

            QLabel {
                color: #9CDCFE;
                font-weight: bold;
            }

            QPushButton {
                background-color: #701a75;
                color: #9a3412;
                border-radius: 4px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #2899F5;
            }

            QTabWidget::pane {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 4px;
            }

            QTabBar::tab {
                background-color: #252526;
                color: #fde68a;
                padding: 8px 16px;
                border: 1px solid #3C3C3C;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #1E1E1E;
                border-bottom: 2px solid #007ACC;
            }

            QScrollArea {
                border: none;
            }
        """)

    def _init_ui(self):
        """Inicia la interfaz de usuario."""
        tabs = QTabWidget()
        tabs.setTabsClosable(False)
        tabs.setMovable(False)

        icono_tarea = QIcon("desktop_ui/iconos/notebook.png")
        icono_historial = QIcon("desktop_ui/iconos/database.png")
        icono_estadisticas = QIcon("desktop_ui/iconos/balance.png")
        icono_exportar = QIcon("desktop_ui/iconos/document-copy.png")

        # ---------------- TAB 1: Task Form ----------------
        task_form_widget = TaskForm()
        tabs.addTab(task_form_widget, icono_tarea, "Formulario Tareas")

        # ---------------- TAB 2: Historial ----------------
        history_widget = HistoryView()
        tabs.addTab(history_widget, icono_historial, "Historial")

        # ---------------- TAB 3: Estadísticas ----------------
        stats_view = StatsScroll(StatsView())
        tabs.addTab(stats_view, icono_estadisticas, "Estadísticas")

        # ----------------- TAB 4: Exportar --------------------
        export_view = ExportView()
        tabs.addTab(export_view, icono_exportar, "Exportar")

        # ---------------- Layout principal ----------------
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(tabs)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
