# stats_view.py
import httpx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from core.stats import compute_stats
from desktop_client.config import API_URL


class _StatsSignals(QObject):
    data     = Signal(dict)
    error    = Signal(str)
    finished = Signal()

class _StatsWorker(QRunnable):
    def __init__(self, url: str):
        super().__init__()
        self.url     = url
        self.signals = _StatsSignals()

    def run(self):
        try:
            with httpx.Client(timeout=15.0) as client:
                r = client.get(self.url, params={"ordering": "fecha_creacion"})
                r.raise_for_status()
                logs = r.json().get("results", [])
            # Agregación pura y testeable (core), sin lógica de negocio en el worker.
            self.signals.data.emit(compute_stats(logs))
        except Exception as e:
            try:
                self.signals.error.emit(str(e))
            except RuntimeError:
                pass

class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Estadísticas de productividad")
        self.setObjectName("statsView")

        # Asignar objectName a frames para QSS
        self.frame_barras       = QFrame(objectName="sectionFrame")
        self.frame_tecnologias  = QFrame(objectName="sectionFrame")

        # Configurar Seaborn/Matplotlib para alto contraste
        sns.set_theme(
            style    = "darkgrid",
            palette  = "pastel",
            rc       = {
                "axes.facecolor":    "#1A1A1A",
                "figure.facecolor":  "#121212",
                "savefig.facecolor": "#121212",
                "grid.color":        "#333333",
                "text.color":        "#E0E0E0",
                "xtick.color":       "#E0E0E0",
                "ytick.color":       "#E0E0E0",
                "axes.edgecolor":    "#444444",
                "axes.labelcolor":   "#E0E0E0",
                "legend.facecolor":  "#1A1A1A",
                "legend.edgecolor":  "#333333"
            }
        )

        self._pool    = QThreadPool.globalInstance()
        self._workers = []

        self._init_ui()
        self.cargar_stats_async()

    def _init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(15)

        # Panel de barras
        self.frame_barras.setLayout(QVBoxLayout())
        layout.addWidget(self.frame_barras, 0, 0)

        # Panel de top tecnologías
        self.frame_tecnologias.setLayout(QVBoxLayout())
        layout.addWidget(self.frame_tecnologias, 0, 1)

    def cargar_stats_async(self):
        worker = _StatsWorker(API_URL)
        worker.signals.data.connect(self._on_data)
        worker.signals.error.connect(self._on_error)
        self._workers.append(worker)
        self._pool.start(worker)

    @Slot(dict)
    def _on_data(self, data):
        if data.get("empty"):
            self.frame_barras.layout().addWidget(QLabel("No hay datos."))
            self.frame_tecnologias.layout().addWidget(QLabel("No hay datos."))
            return
        self._dibujar_barras(data["por_franja"])
        self._dibujar_top_tecnologias(data["top_tecnologias"])

    @Slot(str)
    def _on_error(self, msg):
        self.frame_barras.layout().addWidget(QLabel(f"Error: {msg}"))
        self.frame_tecnologias.layout().addWidget(QLabel(f"Error: {msg}"))

    def _dibujar_barras(self, por_franja):
        df = pd.DataFrame(por_franja)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="#121212")
        ax.set_facecolor("#1A1A1A")
        sns.barplot(
            x="parte", y="horas",
            hue="dia", data=df,
            ax=ax, edgecolor="#333333"
        )
        ax.set_ylabel("Horas trabajadas")
        ax.set_xlabel("Franja del día")
        ax.set_title("Horas por franja del día", color="#E0E0E0")
        ax.legend(title="Día", facecolor="#1A1A1A", edgecolor="#333333")
        canvas = Canvas(fig)
        canvas.setStyleSheet("background-color: #121212; border: none;")
        self.frame_barras.layout().addWidget(canvas)

    def _dibujar_top_tecnologias(self, top_tecnologias):
        df = pd.DataFrame(top_tecnologias)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor="#121212")
        ax.set_facecolor("#1A1A1A")
        sns.barplot(
            x="horas", y="tecnologia",
            data=df, ax=ax, color="#00D4FF", edgecolor="#333333"
        )
        ax.set_xlabel("Cantidad de horas", color="#E0E0E0")
        ax.set_title("Top Tecnologías", color="#E0E0E0")
        canvas = Canvas(fig)
        canvas.setStyleSheet("background-color: #121212; border: none;")
        self.frame_tecnologias.layout().addWidget(canvas)
