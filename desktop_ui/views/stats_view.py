import httpx
import pandas as pd
from datetime import datetime
from collections import defaultdict, Counter

from PySide6.QtWidgets import QWidget, QGridLayout, QMessageBox, QLabel, QSizePolicy
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt, QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class StatsDashboard(QWidget):
    def __init__(self):
        super().__init__()
        # Se elimina el setMinimumSize aquí, ya que será gestionado por el layout.
        # self.setMinimumSize(1200, 800)

        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.cargar_datos()

    def cargar_datos(self):
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
            self.layout.addWidget(self._encabezado("Horas por franja horaria"), 0, 0)
            self.layout.addWidget(self._grafico_barras_qt(df), 1, 0)

            self.layout.addWidget(self._encabezado("Evolución diaria de horas"), 0, 1)
            self.layout.addWidget(self._grafico_linea_matplotlib(df), 1, 1)

            self.layout.addWidget(self._encabezado("Heatmap de productividad por hora"), 2, 0)
            self.layout.addWidget(self._heatmap_seaborn(df), 3, 0)

            self.layout.addWidget(self._encabezado("Distribución por tecnologías"), 2, 1)
            self.layout.addWidget(self._grafico_circular_plotly(df), 3, 1)

            # --- Corrección Principal ---
            # Establece un tamaño mínimo para el layout para garantizar que se muestren todos los gráficos
            min_width = 1100  # Ancho mínimo adecuado
            min_height = 900  # Altura mínima adecuada para los 4 gráficos
            self.setMinimumSize(QSize(min_width, min_height))
            # ---------------------------
        except Exception as e:
            self.mostrar_mensaje(f"Error al generar gráficos: {str(e)}")
            
    # Los métodos de gráficos permanecen igual
    def _encabezado(self, texto):
        label = QLabel(texto)
        label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        label.setAlignment(Qt.AlignCenter)
        return label

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
            bar_set.setColor(colores[franja])
            for fecha in fechas:
                bar_set.append(agrupado[fecha][franja])
            series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Horas por franja horaria")

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
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 8)) # Aumenta el tamaño de la figura para mejorar la proporción
        df.groupby("dia")["horas"].sum().plot(kind="line", marker="o", ax=ax, color="#2ecc71")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Horas")
        ax.set_title("Evolución diaria de horas")
        ax.grid(True)
        
        # Ajusta el layout para que no se superpongan los elementos
        fig.tight_layout(pad=3.0) 
        
        canvas = Canvas(fig)
        return canvas

    def _heatmap_seaborn(self, df):
        pivot = df.pivot_table(index="hora", columns="dia", values="horas", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 8)) # Aumenta el tamaño de la figura
        sns.heatmap(pivot, cmap="YlGnBu", ax=ax, annot=True, fmt=".1f", linewidths=0.5, linecolor="gray")
        ax.set_title("Heatmap de productividad por hora")
        ax.set_xlabel("Día")
        ax.set_ylabel("Hora")
        
        # Ajusta el layout para que el título no se solape con el heatmap
        fig.tight_layout(pad=3.0) 
        
        canvas = Canvas(fig)
        return canvas

    def _grafico_circular_plotly(self, df):
        tech_list = df["tecnologias_utilizadas"].dropna().str.split(", ")
        flat_list = [tech for sublist in tech_list for tech in sublist]
        tech_counter = Counter(flat_list)
        tech_df = pd.DataFrame.from_dict(tech_counter, orient="index", columns=["horas"]).reset_index()
        tech_df.columns = ["tecnologia", "horas"]

        fig = px.pie(tech_df, names="tecnologia", values="horas", title="Distribución por tecnologías")
        fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))

        temp_image_path = "media/temp_pie.png"
        fig.write_image(temp_image_path, scale=2.0)
        
        label = QLabel()
        pixmap = QPixmap(temp_image_path)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return label

    def mostrar_mensaje(self, texto):
        QMessageBox.information(self, "Dashboard", texto)