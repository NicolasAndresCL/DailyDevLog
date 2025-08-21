import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton,
    QTextEdit, QHBoxLayout, QMessageBox, QApplication
)
from PySide6.QtGui import QDesktopServices, QClipboard
from PySide6.QtCore import QUrl, Qt

EXPORT_FOLDER = "exports"

class ExportView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📤 Exportaciones Markdown")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.mostrar_preview)
        layout.addWidget(self.file_list)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        btn_layout = QHBoxLayout()
        self.btn_abrir = QPushButton("Abrir archivo")
        self.btn_abrir.clicked.connect(self.abrir_archivo)

        self.btn_copiar = QPushButton("Copiar contenido")
        self.btn_copiar.clicked.connect(self.copiar_contenido)

        btn_layout.addWidget(self.btn_abrir)
        btn_layout.addWidget(self.btn_copiar)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.cargar_archivos()

    def cargar_archivos(self):
        if not os.path.exists(EXPORT_FOLDER):
            os.makedirs(EXPORT_FOLDER)
        archivos = [f for f in os.listdir(EXPORT_FOLDER) if f.endswith(".md")]
        self.file_list.clear()
        self.file_list.addItems(archivos)

    def mostrar_preview(self, item):
        path = os.path.join(EXPORT_FOLDER, item.text())
        try:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.preview.setPlainText(contenido)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer el archivo:\n{str(e)}")

    def abrir_archivo(self):
        item = self.file_list.currentItem()
        if item:
            path = os.path.join(EXPORT_FOLDER, item.text())
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def copiar_contenido(self):
        contenido = self.preview.toPlainText()
        if contenido:
            clipboard = QApplication.clipboard()
            clipboard.setText(contenido, QClipboard.Clipboard)
            QMessageBox.information(self, "Copiado", "Contenido copiado al portapapeles.")
