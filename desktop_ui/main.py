# main.py
import sys
from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QIcon

from desktop_ui.forms.task_form import TaskForm
from desktop_ui.views.history_view import HistoryView
from desktop_ui.views.stats_scroll import StatsScroll
from desktop_ui.views.export_view import ExportView
from desktop_ui.views.stats_view import StatsView


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("💻 Dashboard TI diarias")
        self.showMaximized()
        self._pool = QThreadPool.globalInstance()
        self._init_ui()

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


def _cargar_tema(app: QApplication) -> None:
    """Aplica el tema oscuro unificado (theme_dark.qss) a toda la app."""
    qss = Path(__file__).parent / "theme_dark.qss"
    if qss.exists():
        app.setStyleSheet(qss.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    _cargar_tema(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
