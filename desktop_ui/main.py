import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTabWidget, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvgWidgets import QSvgWidget # Para íconos SVG

from desktop_ui.forms.task_form import TaskForm
from desktop_ui.views.history_view import HistoryView
from desktop_ui.views.stats_scroll import StatsDashboardScroll
from desktop_ui.views.export_view import ExportView

class DailyDevLogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DailyDevLog")
        self.setGeometry(100, 100, 1100, 720)
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon("media/icon.png"))

        self._init_views()
        self._init_ui()

    def _init_views(self):
        self.history_view = HistoryView()
        self.task_form = TaskForm(history_view=self.history_view)
        self.stats_scroll = StatsDashboardScroll()
        self.export_view = ExportView()

    def _init_ui(self):
        # Estilos globales para la ventana principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5; /* Fondo gris claro */
            }
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Encabezado (header)
        header = self._build_header()
        main_layout.addWidget(header)

        # Pestañas (tabs)
        self.tabs = self._build_tabs()
        main_layout.addWidget(self.tabs)

        self.setCentralWidget(central_widget)

    def _build_header(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        title = QLabel("DailyDevLog")
        title.setFont(QFont("Segoe UI", 26, QFont.ExtraBold))
        title.setStyleSheet("color: #2c3e50;")
        
        subtitle = QLabel("Tu registro de progreso TI")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #7f8c8d;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        btn_recargar = QPushButton("Recargar")
        btn_recargar.setToolTip("Recargar todas las vistas")
        btn_recargar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_recargar.clicked.connect(self._recargar_vistas)

        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(btn_recargar)
        return container

    def _build_tabs(self):
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        
        # Estilo CSS para las pestañas
        tabs.setStyleSheet("""
            QTabBar::tab {
                background: #e0e4e8;
                color: #5d6d7e;
                padding: 12px 25px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
            }
        """)

        tabs.addTab(self.task_form, "Registro")
        tabs.addTab(self.history_view, "Historial")
        tabs.addTab(self.stats_scroll, "Estadísticas")
        tabs.addTab(self.export_view, "Exportar")

        return tabs

    def _recargar_vistas(self):
        # Recarga de forma más eficiente para evitar parpadeos
        self.task_form.recargar_datos()
        self.history_view.cargar_datos()
        self.stats_scroll.cargar_datos()
        
        QMessageBox.information(self, "Recarga Completa", "Las vistas se han actualizado correctamente.")


def main():
    app = QApplication(sys.argv)
    window = DailyDevLogWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()