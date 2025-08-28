# stats_scroll.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt

class StatsScroll(QWidget):
    def __init__(self, stats_view):
        super().__init__()
        self.setWindowTitle("📋 Estadísticas detalladas")
        self.setObjectName("statsScroll")

        # Layout raíz
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setObjectName("statsScrollArea")
        scroll.setWidgetResizable(True)

        # Contenedor interno
        content = QFrame()
        content.setObjectName("statsScrollContent")
        content.setLayout(QVBoxLayout())
        content.layout().addWidget(stats_view)

        scroll.setWidget(content)
        layout.addWidget(scroll)
