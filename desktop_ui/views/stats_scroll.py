# desktop_ui/views/stats_scroll.py
from PySide6.QtWidgets import QScrollArea
from .stats_view import StatsDashboard

class StatsDashboardScroll(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.dashboard = StatsDashboard()
        self.setWidget(self.dashboard)

    def recargar(self):
        self.dashboard.cargar_datos()
