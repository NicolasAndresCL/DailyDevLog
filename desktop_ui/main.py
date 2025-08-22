import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTabWidget, QPushButton, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PySide6.QtGui import QFont, QIcon, QColor
from PySide6.QtCore import Qt

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
        # 🎨 Estilos globales
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f9fc;
            }
            QLabel {
                color: #2c3e50;
            }
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 12px;
            }
        """)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header con título y botón
        header = self._build_header()
        main_layout.addWidget(header)

        # Tabs con sombra
        self.tabs = self._build_tabs()
        shadow = QGraphicsDropShadowEffect(self.tabs)
        shadow.setBlurRadius(18)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.tabs.setGraphicsEffect(shadow)

        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

    def _build_header(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Título principal
        title = QLabel("DailyDevLog")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #1a252f;")

        # Subtítulo
        subtitle = QLabel("Tu registro de progreso en TI 🚀")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #7f8c8d;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        # Botón estilizado
        btn_recargar = QPushButton("↻ Recargar")
        btn_recargar.setToolTip("Recargar todas las vistas")
        btn_recargar.setCursor(Qt.PointingHandCursor)
        btn_recargar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6391;
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

        # 🎨 Estilo de pestañas moderno
        tabs.setStyleSheet("""
            QTabBar::tab {
                background: #e8ecf1;
                color: #5d6d7e;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 13px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 6px;
                transition: all 0.3s ease;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background: #d6dee6;
                color: #2c3e50;
            }
        """)

        tabs.addTab(self.task_form, "📝 Registro")
        tabs.addTab(self.history_view, "📜 Historial")
        tabs.addTab(self.stats_scroll, "📊 Estadísticas")
        tabs.addTab(self.export_view, "⬇ Exportar")

        return tabs

    def _recargar_vistas(self):
        # Aquí puedes implementar la lógica de recarga
        print("🔄 Recargando vistas...")

        
        # Historial
        if hasattr(self.history_view, "recargar"):
            self.history_view.recargar()

        # Formulario de tareas (ej: limpiar o recargar proyectos)
        if hasattr(self.task_form, "recargar"):
            self.task_form.recargar()

        # Estadísticas
        if hasattr(self.stats_scroll, "recargar"):
            self.stats_scroll.recargar()

        # Exportar
        if hasattr(self.export_view, "recargar"):
            self.export_view.recargar()


def main():
    app = QApplication(sys.argv)
    window = DailyDevLogWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
