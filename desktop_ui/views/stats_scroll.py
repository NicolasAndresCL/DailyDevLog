from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import QSize
from desktop_ui.views.stats_view import StatsDashboard

class StatsDashboardScroll(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Dashboard de productividad")
        self.setMinimumSize(1200, 800)

        # Crea la instancia del dashboard de gráficos
        self.dashboard = StatsDashboard()
        
        # Establece un tamaño mínimo para el dashboard que acomode todos los gráficos.
        # Esto es crucial para que el QScrollArea sepa cuándo habilitar el scroll.
        # Las dimensiones son aproximadas y deben ajustarse a la necesidad.
        self.dashboard.setMinimumSize(QSize(1100, 900))

        # Crea un área de desplazamiento y le asigna el dashboard como widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.dashboard)

        # Crea el layout principal y añade el QScrollArea
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)