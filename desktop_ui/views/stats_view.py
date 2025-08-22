import httpx
import pandas as pd
from datetime import datetime
from collections import defaultdict, Counter

from PySide6.QtWidgets import QWidget, QGridLayout, QMessageBox, QLabel, QSizePolicy, QFrame, QVBoxLayout
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


class StatsDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setSpacing(25)  # Más aire entre gráficos
        self.setLayout(self.layout)

        self.cargar_datos()

    def cargar_datos(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        try:
            response = httpx.get("http://localhost:8000/api/dailylog/?ordering=fecha_creacion")
            if response.status_code == 200:
                logs = response.json().get("results", [])
                if logs:
                    df = pd.DataFrame(logs)
                    df["fecha"] = pd.to_datetime(df["fecha_creacion"], errors="coerce")
                    df["dia"] = df["fecha"].dt.date
                    df["hora"] = df["fecha"].dt.hour
                    df["horas"] = pd.to_numeric(df["horas"], errors="coerce")
                    df = df.dropna(subset=["horas"])
                    self.generar_dashboard(df)
                else:
                    self.mostrar_mensaje("No hay tareas registradas para graficar.")
            else:
                self.mostrar_mensaje(f"Error al obtener datos: {response.status_code}")
        except Exception as e:
            self.mostrar_mensaje(f"Error de conexión: {str(e)}")

    def generar_dashboard(self, df):
        try:
            # 4 gráficos organizados en grilla
            self.layout.addWidget(self._card("Horas por franja horaria", self._grafico_barras_qt(df)), 0, 0)
            self.layout.addWidget(self._card("Evolución diaria de horas", self._grafico_linea_matplotlib(df)), 0, 1)
            self.layout.addWidget(self._card("Heatmap de productividad por hora", self._heatmap_seaborn(df)), 1, 0)
            self.layout.addWidget(self._card("Distribución por tecnologías", self._grafico_circular_plotly(df)), 1, 1)

            # Ajusta tamaño mínimo del dashboard
            self.setMinimumSize(QSize(1100, 900))
        except Exception as e:
            self.mostrar_mensaje(f"Error al generar gráficos: {str(e)}")

    # ---------- Helpers visuales ----------
    def _card(self, titulo, widget):
        """ Crea un card con encabezado y un gráfico """
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #dfe6e9;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header = QLabel(titulo)
        header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        header.setAlignment(Qt.AlignCenter)

        layout.addWidget(header)
        layout.addWidget(widget)
        return frame

    # ---------- Gráficos ----------
    def _grafico_barras_qt(self, df):
        agrupado = defaultdict(lambda: {"mañana": 0, "tarde": 0, "noche": 0})
        for _, row in df.iterrows():
            hora = row["hora"]
            franja = "mañana" if 6 <= hora < 12 else "tarde" if 12 <= hora < 18 else "noche"
            agrupado[str(row["dia"])][franja] += float(row["horas"])

        fechas = sorted(agrupado.keys())
        series = QBarSeries()
        colores = {"mañana": "#3498db", "tarde": "#2ecc71", "noche": "#e67e22"}

        for franja in ["mañana", "tarde", "noche"]:
            bar_set = QBarSet(franja.capitalize())
            bar_set.setColor(QColor(colores[franja]))
            for fecha in fechas:
                bar_set.append(agrupado[fecha][franja])
            series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append(fechas)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%.1f")
        axis_y.setTitleText("Horas")
        axis_y.setRange(0, max(sum(agrupado[f].values()) for f in fechas) + 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return chart_view

    def _grafico_linea_matplotlib(self, df):
        plt.style.use("seaborn-v0_8")
        fig, ax = plt.subplots(figsize=(8, 5))
        df.groupby("dia")["horas"].sum().plot(kind="line", marker="o", ax=ax, color="#2ecc71")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Horas")
        ax.set_title("")
        ax.grid(True)
        fig.tight_layout()
        return Canvas(fig)

    def _heatmap_seaborn(self, df):
        pivot = df.pivot_table(index="hora", columns="dia", values="horas", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(pivot, cmap="YlGnBu", ax=ax, annot=True, fmt=".1f", linewidths=0.5, linecolor="gray")
        ax.set_title("")
        fig.tight_layout()
        return Canvas(fig)

    def _grafico_circular_plotly(self, df):
        tech_list = df["tecnologias_utilizadas"].dropna().str.split(", ")
        flat_list = [tech for sublist in tech_list for tech in sublist]
        tech_counter = Counter(flat_list)
        tech_df = pd.DataFrame.from_dict(tech_counter, orient="index", columns=["horas"]).reset_index()
        tech_df.columns = ["tecnologia", "horas"]

        fig = px.pie(tech_df, names="tecnologia", values="horas")
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          marker=dict(line=dict(color="#000000", width=1)))
        temp_image_path = "media/temp_pie.png"
        fig.write_image(temp_image_path, scale=2.0)

        label = QLabel()
        pixmap = QPixmap(temp_image_path)
        label.setPixmap(pixmap.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        return label

    def mostrar_mensaje(self, texto):
        QMessageBox.information(self, "Dashboard", texto)
