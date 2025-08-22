import httpx
from datetime import datetime
import pytz
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox, QInputDialog,
    QHeaderView, QSizePolicy
)
from PySide6.QtGui import QPixmap, QDesktopServices, QColor
from PySide6.QtCore import QUrl, QSize, Qt

from desktop_ui.export.markdown_exporter import exportar_a_markdown

# Constantes para la conexión a la API
API_URL = "http://localhost:8000/api/dailylog/"
MEDIA_URL_BASE = "http://localhost:8000"

# Carpeta para las exportaciones
EXPORT_FOLDER = Path("exportaciones_markdown")

class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📂 Historial de tareas")
        self.setMinimumSize(1300, 700)
        self.page = 1
        self.search_term = ""

        self._init_ui()
        self.cargar_datos()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Filtro de búsqueda y botones de acción
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por tecnología o descripción...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        self.search_btn = QPushButton("Buscar")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.search_btn.clicked.connect(self.buscar)
        search_layout.addWidget(QLabel("Filtro:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        # Tabla
        self.table = self._build_table()
        layout.addWidget(self.table)

        # Paginación
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(10)
        self.prev_btn = QPushButton("Anterior")
        self.next_btn = QPushButton("Siguiente")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.next_btn.setStyleSheet(self.prev_btn.styleSheet())
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

        # Estilos de la tabla
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #dfe6e9;
                border: 1px solid #dfe6e9;
            }
            QHeaderView::section {
                background-color: #ecf0f1;
                padding: 8px;
                border: 1px solid #dfe6e9;
                font-weight: bold;
            }
        """)

        # Ajuste de columnas
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        for i in range(5, 8):
            header.setSectionResizeMode(i, QHeaderView.Fixed)
            table.setColumnWidth(i, 110)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(11, QHeaderView.ResizeToContents)
        
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setDefaultSectionSize(110)

        return table

    def convertir_a_chile(self, utc_str):
        try:
            utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
            chile_tz = pytz.timezone("America/Santiago")
            local_dt = utc_dt.astimezone(chile_tz)
            return local_dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "Fecha inválida"

    def cargar_datos(self):
        params = {
            "page": self.page,
            "search": self.search_term,
            "ordering": "fecha_creacion"
        }
        try:
            response = httpx.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                self.mostrar_resultados(data.get("results", []))
            else:
                self.table.setRowCount(0)
        except Exception as e:
            print("Error al cargar historial:", e)

    def mostrar_resultados(self, registros):
        self.table.setRowCount(len(registros))
        self.table.setSortingEnabled(False)
        for i, log in enumerate(registros):
            fecha_local = self.convertir_a_chile(log.get("fecha_creacion", ""))
            self.table.setItem(i, 0, QTableWidgetItem(fecha_local))
            self.table.setItem(i, 1, QTableWidgetItem(log.get("nombre_tarea", "")))
            self.table.setItem(i, 2, QTableWidgetItem(str(log.get("horas", 0))))
            self.table.setItem(i, 3, QTableWidgetItem(log.get("tecnologias_utilizadas", "")))
            self.table.setItem(i, 4, QTableWidgetItem(log.get("descripcion", "")))

            # Imágenes
            for j, key in enumerate(["imagen_1_url", "imagen_2_url", "imagen_3_url"], start=5):
                image_path = log.get(key)
                full_image_url = f"{MEDIA_URL_BASE}{image_path}" if image_path else ""
                label = self._build_image_label(full_image_url)
                self.table.setCellWidget(i, j, label)

            # Estado visual
            estado_item = QTableWidgetItem("🟢 Publicado" if log.get("link_publicacion_linkedin") else "🟡 Pendiente")
            estado_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 8, estado_item)

            # Botones de acción
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
                response = httpx.get(url, follow_redirects=True)
                if response.status_code == 200:
                    if pixmap.loadFromData(response.content):
                        label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    else:
                        label.setText("Error al cargar imagen")
                else:
                    label.setText(f"Error {response.status_code}")
            except Exception as e:
                label.setText("Error de conexión")
        else:
            label.setText("Sin imagen")
        return label

    def _build_action_buttons(self, row, log):
        # Contenedor para los botones para un layout más limpio
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Estilo de botones de acción
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

        btn_exportar = QPushButton("Exportar")
        btn_exportar.setStyleSheet(button_style)
        btn_exportar.clicked.connect(lambda _, l=log: self.exportar_log(l))
        layout.addWidget(btn_exportar)

        btn_publicar = QPushButton("Añadir publicación")
        btn_publicar.setStyleSheet(button_style.replace("#3498db", "#2ecc71").replace("#2980b9", "#27ae60"))
        btn_publicar.clicked.connect(lambda _, l=log: self.agregar_linkedin(l))
        layout.addWidget(btn_publicar)
        
        btn_ia = QPushButton("Ver IA")
        btn_ia.setStyleSheet(button_style.replace("#3498db", "#9b59b6").replace("#2980b9", "#8e44ad"))
        btn_ia.clicked.connect(lambda _, url=log.get("link_ia_principal"): self.abrir_url(url))
        layout.addWidget(btn_ia)

        # Se usa setCellWidget para añadir el contenedor de botones a la celda
        self.table.setCellWidget(row, 9, container)
        self.table.setCellWidget(row, 10, container)
        self.table.setCellWidget(row, 11, container)

    def agregar_linkedin(self, log):
        nuevo_link, ok = QInputDialog.getText(self, "Añadir publicación", "Pega el link de LinkedIn:")
        if ok and nuevo_link:
            try:
                response = httpx.patch(
                    f"{API_URL}{log['id']}/",
                    data={"link_publicacion_linkedin": nuevo_link}
                )
                if response.status_code == 200:
                    QMessageBox.information(self, "Actualizado", "Link de publicación añadido correctamente.")
                    self.cargar_datos()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo actualizar:\n{response.text}")
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
            QMessageBox.information(self, "Exportación exitosa", f"Archivo guardado en:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error al exportar", str(e))

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