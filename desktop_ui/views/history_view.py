from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox, QInputDialog
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QUrl, QSize
import httpx
from desktop_ui.export.markdown_exporter import exportar_a_markdown

MEDIA_URL = "http://localhost:8000/media/"

class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de tareas")
        self.setMinimumSize(1300, 700)

        self.page = 1
        self.search_term = ""

        layout = QVBoxLayout()

        # Filtro de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por tecnología o descripción...")
        self.search_btn = QPushButton("Buscar")
        self.search_btn.clicked.connect(self.buscar)

        search_layout.addWidget(QLabel("Filtro:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        # Tabla con columnas extendidas
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Fecha", "Tarea", "Horas", "Tecnologías", "Descripción",
            "Imagen 1", "Imagen 2", "Imagen 3",
            "Estado", "Exportar", "Publicar", "IA Principal"
        ])
        layout.addWidget(self.table)

        # Paginación
        pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Anterior")
        self.next_btn = QPushButton("Siguiente")
        self.prev_btn.clicked.connect(self.pagina_anterior)
        self.next_btn.clicked.connect(self.pagina_siguiente)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.next_btn)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        params = {
            "page": self.page,
            "search": self.search_term,
            "ordering": "-fecha_creacion"
        }
        try:
            response = httpx.get("http://localhost:8000/api/dailylog/", params=params)
            if response.status_code == 200:
                data = response.json()
                self.mostrar_resultados(data.get("results", []))
            else:
                self.table.setRowCount(0)
        except Exception as e:
            print("Error al cargar historial:", e)

    def mostrar_resultados(self, registros):
        self.table.setRowCount(len(registros))
        for i, log in enumerate(registros):
            self.table.setItem(i, 0, QTableWidgetItem(log["fecha_creacion"]))
            self.table.setItem(i, 1, QTableWidgetItem(log["nombre_tarea"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(log["horas"])))
            self.table.setItem(i, 3, QTableWidgetItem(log["tecnologias_utilizadas"]))
            self.table.setItem(i, 4, QTableWidgetItem(log["descripcion"]))

            # Previews de imágenes
            for j, key in enumerate(["imagen_1", "imagen_2", "imagen_3"], start=5):
                label = QLabel()
                label.setFixedSize(QSize(100, 100))
                url = log.get(key)
                if url:
                    try:
                        pixmap = QPixmap()
                        pixmap.loadFromData(httpx.get(url).content)
                        label.setPixmap(pixmap.scaled(100, 100))
                    except Exception as e:
                        label.setText("Error")
                self.table.setCellWidget(i, j, label)

            # Estado visual
            estado = "🟢 Publicado" if log["link_publicacion_linkedin"] else "🟡 Pendiente"
            self.table.setItem(i, 8, QTableWidgetItem(estado))

            # Botón exportar
            btn_exportar = QPushButton("Exportar")
            btn_exportar.clicked.connect(lambda _, l=log: self.exportar_log(l))
            self.table.setCellWidget(i, 9, btn_exportar)

            # Botón añadir publicación
            btn_publicar = QPushButton("Añadir publicación")
            btn_publicar.clicked.connect(lambda _, l=log: self.agregar_linkedin(l))
            self.table.setCellWidget(i, 10, btn_publicar)

            # Botón IA principal
            btn_ia = QPushButton("Ver IA")
            btn_ia.clicked.connect(lambda _, url=log["link_ia_principal"]: self.abrir_url(url))
            self.table.setCellWidget(i, 11, btn_ia)

    def agregar_linkedin(self, log):
        nuevo_link, ok = QInputDialog.getText(self, "Añadir publicación", "Pega el link de LinkedIn:")
        if ok and nuevo_link:
            try:
                response = httpx.put(
                    f"http://localhost:8000/api/dailylog/{log['id']}/",
                    json={"link_publicacion_linkedin": nuevo_link}
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
        path = exportar_a_markdown(log)
        QMessageBox.information(self, "Exportación exitosa", f"Archivo guardado en:\n{path}")

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
