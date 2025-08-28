# stats_view.py
import os
import httpx
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QObject, QRunnable, QThreadPool, Slot, Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import seaborn as sns

API_URL = "http://localhost:8000/api/dailylog/"

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
                r = client.get(self.url, params={"ordering":"fecha_creacion"})
                r.raise_for_status()
                logs = r.json().get("results", [])
            if not logs:
                self.signals.data.emit({"empty": True})
                return

            df = pd.DataFrame(logs)
            df["fecha"] = pd.to_datetime(df["fecha_creacion"], errors="coerce")
            df["hora"]   = df["fecha"].dt.hour
            df["dia"]    = df["fecha"].dt.date
            df["horas"]  = pd.to_numeric(df["horas"], errors="coerce")
            df = df.dropna(subset=["horas"])
            if df.empty:
                self.signals.data.emit({"empty": True})
                return

            # barras por franja
            df_barras = (
                df.groupby(["dia","hora"])
                  .agg({"horas":"sum"})
                  .reset_index()
            )
            df_barras["parte"] = pd.cut(
                df_barras["hora"],
                bins=[0,12,18,24],
                labels=["mañana","tarde","noche"],
                include_lowest=True
            )

            # top tecnologías
            df_tec = df.explode("tecnologias_utilizadas")
            df_tec["tecnologias_utilizadas"] = (
                df_tec["tecnologias_utilizadas"].str.strip()
            )
            df_tec = (
                df_tec.groupby("tecnologias_utilizadas")
                      .agg({"horas":"sum"})
                      .reset_index()
                      .sort_values("horas", ascending=False)
                      .head(10)
            )

            self.signals.data.emit({
                "barras": df_barras,
                "tecnologias": df_tec
            })

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
        self._dibujar_barras(data["barras"])
        self._dibujar_top_tecnologias(data["tecnologias"])

    @Slot(str)
    def _on_error(self, msg):
        self.frame_barras.layout().addWidget(QLabel(f"Error: {msg}"))
        self.frame_tecnologias.layout().addWidget(QLabel(f"Error: {msg}"))

    def _dibujar_barras(self, df):
        fig, ax = plt.subplots(
            figsize=(6,4), facecolor="#121212"
        )
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

    def _dibujar_top_tecnologias(self, df):
        fig, ax = plt.subplots(
            figsize=(6,4), facecolor="#121212"
        )
        ax.set_facecolor("#1A1A1A")
        sns.barplot(
            x="horas", y="tecnologias_utilizadas",
            data=df, ax=ax, color="#00D4FF", edgecolor="#333333"
        )
        ax.set_xlabel("Cantidad de horas", color="#E0E0E0")
        ax.set_title("Top Tecnologías", color="#E0E0E0")
        canvas = Canvas(fig)
        canvas.setStyleSheet("background-color: #121212; border: none;")
        self.frame_tecnologias.layout().addWidget(canvas)
