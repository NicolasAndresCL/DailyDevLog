# history_view.py
from pathlib import Path
from datetime import datetime
import pytz
import httpx

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, QObject, QRunnable, QThreadPool, Signal, Slot

from export.markdown_exporter import exportar_a_markdown

API_URL = "http://localhost:8000/api/dailylog/"
MEDIA_URL_BASE = "http://localhost:8000"
EXPORT_FOLDER = Path("exportaciones_markdown")


class _HistorySignals(QObject):
    data = Signal(list)
    error = Signal(str)


class _HistoryWorker(QRunnable):
    def __init__(self, page: int, search: str):
        super().__init__()
        self.page = page
        self.search = search
        self.signals = _HistorySignals()

    def run(self):
        try:
            with httpx.Client(timeout=20.0) as client:
                r = client.get(
                    API_URL,
                    params={
                        "page": self.page,
                        "search": self.search,
                        "ordering": "-fecha_creacion"
                    }
                )
            if r.status_code == 200:
                self.signals.data.emit(r.json().get("results", []))
            else:
                self.signals.error.emit(f"HTTP {r.status_code}")
        except Exception as e:
            self.signals.error.emit(str(e))


class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📂 Historial de tareas")
        self.setMinimumSize(1200, 650)
        self.setObjectName("historyView")
        self.setStyleSheet("""
            QWidget#historyView {
                background-color: #1E1E1E;
                color: #D4D4D4;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QLineEdit {
                background-color: #252526;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 6px;
                color: #D4D4D4;
            }

            QLabel#filterLabel {
                color: #9CDCFE;
                font-weight: bold;
            }

            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 4px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #2899F5;
            }

            QTableWidget {
                background-color: #1E1E1E;
                gridline-color: #3C3C3C;
                border: 1px solid #3C3C3C;
            }

            QHeaderView::section {
                background-color: #252526;
                color: #D4D4D4;
                padding: 4px;
                border: 1px solid #3C3C3C;
            }
        """)
        self.page = 1
        self.search_term = ""
        self._pool = QThreadPool.globalInstance()
        self._workers = []

        self._init_ui()
        self.cargar_datos_async()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🔍 Filtro
        hl = QHBoxLayout()
        lbl_filter = QLabel("Filtro:")
        lbl_filter.setObjectName("filterLabel")

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(
            "Buscar por tecnología o descripción..."
        )

        btn_search = QPushButton("Buscar")
        btn_search.setObjectName("searchButton")
        btn_search.clicked.connect(self.buscar)

        hl.addWidget(lbl_filter)
        hl.addWidget(self.search_input)
        hl.addWidget(btn_search)
        layout.addLayout(hl)

        # 📊 Tabla de historial
        self.table = QTableWidget()
        self.table.setObjectName("historyTable")
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Tarea", "Horas", "Tecnologías", "Descripción",
            "Estado", "Exportar", "Publicar", "IA Principal"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Horas
        header.setSectionResizeMode(4, QHeaderView.Interactive)       # Descripción

        # Ajustar mínimo de alto para filas
        self.table.verticalHeader().setMinimumSectionSize(40)

        layout.addWidget(self.table)

        # 📄 Paginación
        hl2 = QHBoxLayout()
        hl2.addStretch()

        self.prev_btn = QPushButton("⟵ Anterior")
        self.prev_btn.setObjectName("prevButton")
        self.prev_btn.clicked.connect(self.pagina_anterior)

        self.next_btn = QPushButton("Siguiente ⟶")
        self.next_btn.setObjectName("nextButton")
        self.next_btn.clicked.connect(self.pagina_siguiente)

        hl2.addWidget(self.prev_btn)
        hl2.addWidget(self.next_btn)
        layout.addLayout(hl2)

    def convertir_a_chile(self, utc_str):
        try:
            dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
            tz = pytz.timezone("America/Santiago")
            return dt.astimezone(tz).strftime("%Y-%m-%d %H:%M")
        except:
            return "Fecha inválida"

    def cargar_datos_async(self):
        worker = _HistoryWorker(self.page, self.search_term)
        worker.signals.data.connect(self._on_data_ready)
        worker.signals.error.connect(self._on_error)
        self._workers.append(worker)
        self._pool.start(worker)

    @Slot(list)
    def _on_data_ready(self, registros):
        self.table.setRowCount(len(registros))
        self.table.setSortingEnabled(False)

        # Ajuste de columnas
        self.table.setColumnWidth(0, 110)  # Fecha
        self.table.setColumnWidth(1, 180)  # Tarea
        self.table.setColumnWidth(2, 60)   # Horas
        self.table.setColumnWidth(3, 140)  # Tecnologías
        self.table.setColumnWidth(4, 300)  # Descripción
        self.table.setColumnWidth(5, 90)   # Estado
        self.table.setColumnWidth(6, 90)   # Exportar
        self.table.setColumnWidth(7, 90)   # Publicar
        self.table.setColumnWidth(8, 90)   # IA Principal

        # Ajustar filas al contenido, respetando mínimo
        self.table.resizeRowsToContents()

        for i, log in enumerate(registros):
            self.table.setItem(
                i, 0,
                QTableWidgetItem(self.convertir_a_chile(
                    log.get("fecha_creacion", "")
                ))
            )
            self.table.setItem(i, 1, QTableWidgetItem(log.get("nombre_tarea", "")))
            self.table.setItem(i, 2, QTableWidgetItem(str(log.get("horas", 0))))
            self.table.setItem(i, 3, QTableWidgetItem(log.get("tecnologias_utilizadas", "")))
            self.table.setItem(i, 4, QTableWidgetItem(log.get("descripcion", "")))

            estado = QTableWidgetItem(
                "🟢 Publicado" if log.get("link_publicacion_linkedin") else "🟡 Pendiente"
            )
            estado.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 5, estado)

            btn_exp = QPushButton("⬇ Exportar")
            btn_exp.setObjectName("exportButton")
            btn_exp.clicked.connect(lambda _, l=log: self._export_log(l))
            self.table.setCellWidget(i, 6, btn_exp)

            btn_pub = QPushButton("🔗 Publicar")
            btn_pub.setObjectName("publishButton")
            btn_pub.clicked.connect(lambda _, l=log: self._publicar_en_linkedin(l))
            self.table.setCellWidget(i, 7, btn_pub)

            btn_ia = QPushButton("🤖 IA")
            btn_ia.setObjectName("iaButton")
            btn_ia.clicked.connect(lambda _, l=log: self._mostrar_info_ia(l))
            self.table.setCellWidget(i, 8, btn_ia)

        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents()

    def _publicar_en_linkedin(self, log):
        link = log.get("link_publicacion_linkedin")
        if link:
            QMessageBox.information(self, "Publicación", f"Ya fue publicado:\n{link}")
        else:
            QMessageBox.information(
                self, "Publicación",
                "Simulación: se publicaría en LinkedIn con los datos de esta tarea."
            )

    def _mostrar_info_ia(self, log):
        ia_link = log.get("link_ia_principal")
        if ia_link:
            QMessageBox.information(self, "IA Principal", f"Link IA principal:\n{ia_link}")
        else:
            QMessageBox.information(
                self, "IA Principal",
                "No se ha registrado un link de IA principal."
            )

    @Slot(str)
    def _on_error(self, msg):
        QMessageBox.warning(self, "Error", f"No se pudo cargar el historial:\n{msg}")
        self.table.setRowCount(0)

    def _export_log(self, log):
        try:
            EXPORT_FOLDER.mkdir(exist_ok=True)
            p = EXPORT_FOLDER / f"{log.get('nombre_tarea','log')}.md"
            exportar_a_markdown(log, p)
            QMessageBox.information(self, "Exportar", f"Exportado a {p}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo exportar:\n{e}")

    def buscar(self):
        self.search_term = self.search_input.text()
        self.page = 1
        self.cargar_datos_async()

    def pagina_anterior(self):
        if self.page > 1:
            self.page -= 1
            self.cargar_datos_async()

    def pagina_siguiente(self):
        self.page += 1
        self.cargar_datos_async()
