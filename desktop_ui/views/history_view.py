# history_view.py
import weakref
from pathlib import Path
from datetime import datetime
import pytz
import httpx

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, QSize, QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtGui import QPixmap

from export.markdown_exporter import exportar_a_markdown

API_URL = "http://localhost:8000/api/dailylog/"
MEDIA_URL_BASE = "http://localhost:8000"
EXPORT_FOLDER = Path("exportaciones_markdown")


class _HistorySignals(QObject):
    data  = Signal(list)
    error = Signal(str)


class _HistoryWorker(QRunnable):
    def __init__(self, page: int, search: str):
        super().__init__()
        self.page    = page
        self.search  = search
        self.signals = _HistorySignals()

    def run(self):
        try:
            with httpx.Client(timeout=20.0) as client:
                r = client.get(
                    API_URL,
                    params={
                        "page": self.page,
                        "search": self.search,
                        "ordering": "fecha_creacion"
                    }
                )
            if r.status_code == 200:
                self.signals.data.emit(r.json().get("results", []))
            else:
                self.signals.error.emit(f"HTTP {r.status_code}")
        except Exception as e:
            self.signals.error.emit(str(e))


class _ImageSignals(QObject):
    loaded = Signal(int, int, QPixmap)


class _ImageWorker(QRunnable):
    def __init__(self, row: int, col: int, url: str):
        super().__init__()
        self.row     = row
        self.col     = col
        self.url     = url
        self.signals = _ImageSignals()

    def run(self):
        try:
            with httpx.Client(timeout=10.0) as client:
                r = client.get(self.url, follow_redirects=True)
            if r.status_code == 200:
                pix = QPixmap()
                if pix.loadFromData(r.content):
                    self.signals.loaded.emit(self.row, self.col, pix)
        except Exception:
            pass


class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📂 Historial de tareas")
        self.setMinimumSize(1200, 650)
        self.setObjectName("historyView")

        self.page         = 1
        self.search_term  = ""
        self._pool        = QThreadPool.globalInstance()
        self._workers     = []
        self._image_labels = {}

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
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Tarea", "Horas", "Tecnologías", "Descripción",
            "Imagen 1", "Imagen 2", "Imagen 3",
            "Estado", "Exportar", "Publicar", "IA Principal"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for col in range(5, 8):
            header.setSectionResizeMode(col, QHeaderView.Fixed)
            self.table.setColumnWidth(col, 110)

        self.table.verticalHeader().setDefaultSectionSize(110)
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

        for i, log in enumerate(registros):
            self.table.setItem(
                i, 0,
                QTableWidgetItem(self.convertir_a_chile(
                    log.get("fecha_creacion", "")
                ))
            )
            self.table.setItem(
                i, 1,
                QTableWidgetItem(log.get("nombre_tarea", ""))
            )
            self.table.setItem(
                i, 2,
                QTableWidgetItem(str(log.get("horas", 0)))
            )
            self.table.setItem(
                i, 3,
                QTableWidgetItem(log.get("tecnologias_utilizadas", ""))
            )
            self.table.setItem(
                i, 4,
                QTableWidgetItem(log.get("descripcion", ""))
            )

            # Carga de imágenes asíncronas
            for j, key in enumerate(
                ["imagen_1_url", "imagen_2_url", "imagen_3_url"],
                start=5
            ):
                lbl = QLabel("⏳")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(QSize(100, 100))
                self.table.setCellWidget(i, j, lbl)
                self._image_labels[(i, j)] = lbl

                url = log.get(key)
                if url:
                    iw = _ImageWorker(i, j, f"{MEDIA_URL_BASE}{url}")
                    iw.signals.loaded.connect(
                        lambda r, c, p, lref=weakref.ref(lbl):
                        self._safe_set_pixmap(r, c, p, lref)
                    )
                    self._workers.append(iw)
                    self._pool.start(iw)
                else:
                    lbl.setText("—")

            estado = QTableWidgetItem(
                "🟢 Publicado"
                if log.get("link_publicacion_linkedin")
                else "🟡 Pendiente"
            )
            estado.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 8, estado)

            # Botón exportar
            btn_exp = QPushButton("⬇ Exportar")
            btn_exp.setObjectName("exportButton")
            btn_exp.clicked.connect(lambda _, l=log: self._export_log(l))
            self.table.setCellWidget(i, 9, btn_exp)

        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents()

    def _safe_set_pixmap(self, row, col, pixmap, lbl_ref):
        lbl = lbl_ref()
        if lbl:
            lbl.setPixmap(
                pixmap.scaled(
                    100, 100,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

    @Slot(str)
    def _on_error(self, msg):
        QMessageBox.warning(
            self, "Error",
            f"No se pudo cargar el historial:\n{msg}"
        )
        self.table.setRowCount(0)

    def _export_log(self, log):
        try:
            EXPORT_FOLDER.mkdir(exist_ok=True)
            p = EXPORT_FOLDER / f"{log.get('nombre_tarea','log')}.md"
            exportar_a_markdown(log, p)
            QMessageBox.information(
                self, "Exportar",
                f"Exportado a {p}"
            )
        except Exception as e:
            QMessageBox.warning(
                self, "Error",
                f"No se pudo exportar:\n{e}"
            )

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
