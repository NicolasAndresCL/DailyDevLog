import httpx
from datetime import datetime
import pytz
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox, QInputDialog,
    QHeaderView
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QUrl, QSize, Qt

from desktop_ui.export.markdown_exporter import exportar_a_markdown

# Constantes
API_URL = "http://localhost:8000/api/dailylog/"
MEDIA_URL_BASE = "http://localhost:8000"
EXPORT_FOLDER = Path("exportaciones_markdown")


class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📂 Historial de tareas")
        self.setMinimumSize(1200, 650)
        self.page = 1
        self.search_term = ""

        self._init_ui()
        self.cargar_datos()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🔍 Filtro de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por tecnología o descripción...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ccd1d9;
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        self.search_btn = QPushButton("Buscar")
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.setStyleSheet(self._button_style("#3498db", "#2980b9"))
        self.search_btn.clicked.connect(self.buscar)

        search_layout.addWidget(QLabel("Filtro:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        # 📊 Tabla
        self.table = self._build_table()
        layout.addWidget(self.table)

        # 📄 Paginación
        pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton("⟵ Anterior")
        self.next_btn = QPushButton("Siguiente ⟶")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.setStyleSheet(self._button_style("#95a5a6", "#7f8c8d"))
        self.next_btn.setStyleSheet(self._button_style("#95a5a6", "#7f8c8d"))
        self.prev_btn.clicked.connect(self.pagina_anterior)
        self.next_btn.clicked.connect(self.pagina_siguiente)

        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.next_btn)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)

    def _build_table(self):
        table = QTableWidget()
        table.setColumnCount(12)
        table.setHorizontalHeaderLabels([
            "Fecha", "Tarea", "Horas", "Tecnologías", "Descripción",
            "Imagen 1", "Imagen 2", "Imagen 3",
            "Estado", "Exportar", "Publicar", "IA Principal"
        ])

        # 🎨 Estilos de la tabla
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ecf0f1;
                border: 1px solid #dfe6e9;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f0f2f5;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #2c3e50;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
        """)

        # Ajuste dinámico de columnas
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for i in range(5, 8):
            header.setSectionResizeMode(i, QHeaderView.Fixed)
            table.setColumnWidth(i, 110)
        table.verticalHeader().setDefaultSectionSize(110)

        return table

    def _button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 6px 14px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def convertir_a_chile(self, utc_str):
        try:
            utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
            chile_tz = pytz.timezone("America/Santiago")
            return utc_dt.astimezone(chile_tz).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "Fecha inválida"

    def cargar_datos(self):
        try:
            response = httpx.get(API_URL, params={
                "page": self.page,
                "search": self.search_term,
                "ordering": "fecha_creacion"
            })
            if response.status_code == 200:
                self.mostrar_resultados(response.json().get("results", []))
            else:
                self.table.setRowCount(0)
        except Exception as e:
            print("⚠ Error al cargar historial:", e)

    def mostrar_resultados(self, registros):
        self.table.setRowCount(len(registros))
        self.table.setSortingEnabled(False)
        for i, log in enumerate(registros):
            self.table.setItem(i, 0, QTableWidgetItem(self.convertir_a_chile(log.get("fecha_creacion", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(log.get("nombre_tarea", "")))
            self.table.setItem(i, 2, QTableWidgetItem(str(log.get("horas", 0))))
            self.table.setItem(i, 3, QTableWidgetItem(log.get("tecnologias_utilizadas", "")))
            self.table.setItem(i, 4, QTableWidgetItem(log.get("descripcion", "")))

            # 📸 Imágenes
            for j, key in enumerate(["imagen_1_url", "imagen_2_url", "imagen_3_url"], start=5):
                self.table.setCellWidget(i, j, self._build_image_label(f"{MEDIA_URL_BASE}{log.get(key)}" if log.get(key) else ""))

            # ✅ Estado
            estado_item = QTableWidgetItem("🟢 Publicado" if log.get("link_publicacion_linkedin") else "🟡 Pendiente")
            estado_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 8, estado_item)

            # 🎛 Botones de acción
            self._build_action_buttons(i, log)

        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents()

    def _build_image_label(self, url):
        label = QLabel()
        label.setFixedSize(QSize(100, 100))
        label.setAlignment(Qt.AlignCenter)
        if url:
            try:
                pixmap = QPixmap()
                r = httpx.get(url, follow_redirects=True)
                if r.status_code == 200 and pixmap.loadFromData(r.content):
                    label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    label.setText("⚠ Error")
            except Exception:
                label.setText("❌")
        else:
            label.setText("—")
        return label

    def _build_action_buttons(self, row, log):
        # Exportar
        btn_exportar = QPushButton("⬇ Exportar")
        btn_exportar.setStyleSheet(self._button_style("#3498db", "#2980b9"))
        btn_exportar.clicked.connect(lambda _, l=log: self.exportar_log(l))
        self.table.setCellWidget(row, 9, btn_exportar)

        # Publicar
        btn_publicar = QPushButton("📢 Publicar")
        btn_publicar.setStyleSheet(self._button_style("#2ecc71", "#27ae60"))
        btn_publicar.clicked.connect(lambda _, l=log: self.agregar_linkedin(l))
        self.table.setCellWidget(row, 10, btn_publicar)

        # IA
        btn_ia = QPushButton("🤖 Ver IA")
        btn_ia.setStyleSheet(self._button_style("#9b59b6", "#8e44ad"))
        btn_ia.clicked.connect(lambda _, url=log.get("link_ia_principal"): self.abrir_url(url))
        self.table.setCellWidget(row, 11, btn_ia)

    def agregar_linkedin(self, log):
        nuevo_link, ok = QInputDialog.getText(self, "Añadir publicación", "Pega el link de LinkedIn:")
        if ok and nuevo_link:
            try:
                r = httpx.patch(f"{API_URL}{log['id']}/", data={"link_publicacion_linkedin": nuevo_link})
                if r.status_code == 200:
                    QMessageBox.information(self, "✅ Actualizado", "Link añadido correctamente.")
                    self.cargar_datos()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo actualizar:\n{r.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error de conexión", str(e))

    def abrir_url(self, url):
        if url:
            QDesktopServices.openUrl(QUrl(url))
        else:
            QMessageBox.warning(self, "Link vacío", "Este registro no contiene un link válido.")

    def exportar_log(self, log):
        EXPORT_FOLDER.mkdir(exist_ok=True)
        try:
            path = exportar_a_markdown(log, EXPORT_FOLDER)
            QMessageBox.information(self, "✅ Exportado", f"Archivo guardado en:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def buscar(self):
        self.search_term = self.search_input.text()
        self.page = 1
        self.cargar_datos()

    def pagina_anterior(self):
        if self.page > 1:
            self.page -= 1
            self.cargar_datos()

    def pagina_siguiente(self):
        self.page += 1
        self.cargar_datos()
