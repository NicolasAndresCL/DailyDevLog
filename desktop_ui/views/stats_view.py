from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
import httpx
from collections import defaultdict
from datetime import datetime

class StatsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horas trabajadas por día")
        self.setMinimumSize(900, 600)

        layout = QVBoxLayout()
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            response = httpx.get("http://localhost:8000/api/dailylog/?ordering=fecha_creacion")
            if response.status_code == 200:
                logs = response.json().get("results", [])
                if logs:
                    self.generar_grafico(logs)
                else:
                    self.mostrar_mensaje("No hay tareas registradas para graficar.")
                    self.chart_view.setChart(QChart())  # gráfico vacío
            else:
                self.mostrar_mensaje(f"Error al obtener datos: {response.status_code}")
        except Exception as e:
            self.mostrar_mensaje(f"Error de conexión: {str(e)}")

    def generar_grafico(self, logs):
        # Agrupar horas por fecha (día)
        horas_por_dia = defaultdict(float)
        for log in logs:
            fecha_raw = log["fecha_creacion"]
            fecha_obj = datetime.fromisoformat(fecha_raw)
            fecha_str = fecha_obj.strftime("%Y-%m-%d")
            horas_por_dia[fecha_str] += float(log["horas"])

        fechas = list(horas_por_dia.keys())
        horas = list(horas_por_dia.values())

        bar_set = QBarSet("Horas trabajadas")
        bar_set.append(horas)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Horas trabajadas por día")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append(fechas)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%.1f")
        axis_y.setTitleText("Horas")
        axis_y.setRange(0, max(horas) + 1 if horas else 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)

    def mostrar_mensaje(self, texto):
        QMessageBox.information(self, "Gráfico de horas", texto)
