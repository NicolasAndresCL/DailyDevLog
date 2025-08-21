from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDoubleSpinBox, QPushButton, QFormLayout, QMessageBox, QFileDialog
)
import httpx
import os

class TaskForm(QWidget):
    def __init__(self, history_view=None):
        super().__init__()
        self.setWindowTitle("Registrar Tarea Diaria")
        self.setMinimumSize(600, 600)
        self.history_view = history_view

        layout = QVBoxLayout()
        form = QFormLayout()

        self.nombre_tarea = QLineEdit()
        self.horas = QDoubleSpinBox()
        self.horas.setRange(0.0, 24.0)
        self.horas.setSingleStep(0.25)

        self.descripcion = QTextEdit()
        self.tecnologias = QLineEdit()

        self.link_ia1 = QLineEdit()
        self.link_ia2 = QLineEdit()
        self.link_ia3 = QLineEdit()
        self.link_repo = QLineEdit()
        self.commit = QLineEdit()

        # Campos de imagen
        self.imagen_1 = QLineEdit()
        self.imagen_2 = QLineEdit()
        self.imagen_3 = QLineEdit()

        btn_img1 = QPushButton("Seleccionar imagen 1")
        btn_img1.clicked.connect(lambda: self.seleccionar_imagen(self.imagen_1))
        btn_img2 = QPushButton("Seleccionar imagen 2")
        btn_img2.clicked.connect(lambda: self.seleccionar_imagen(self.imagen_2))
        btn_img3 = QPushButton("Seleccionar imagen 3")
        btn_img3.clicked.connect(lambda: self.seleccionar_imagen(self.imagen_3))

        form.addRow("Nombre de tarea:", self.nombre_tarea)
        form.addRow("Horas trabajadas:", self.horas)
        form.addRow("Descripción:", self.descripcion)
        form.addRow("Tecnologías utilizadas:", self.tecnologias)
        form.addRow("Link IA principal:", self.link_ia1)
        form.addRow("Link IA secundaria:", self.link_ia2)
        form.addRow("Link IA terciaria:", self.link_ia3)
        form.addRow("Link repositorio:", self.link_repo)
        form.addRow("Commit principal:", self.commit)

        form.addRow("Imagen 1:", self.imagen_1)
        form.addRow("", btn_img1)
        form.addRow("Imagen 2:", self.imagen_2)
        form.addRow("", btn_img2)
        form.addRow("Imagen 3:", self.imagen_3)
        form.addRow("", btn_img3)

        self.submit_btn = QPushButton("Guardar tarea")
        self.submit_btn.clicked.connect(self.enviar_tarea)

        layout.addLayout(form)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def seleccionar_imagen(self, campo):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            campo.setText(file_path)

    def enviar_tarea(self):
        # Datos como multipart
        files = {}
        for idx, campo in enumerate([self.imagen_1, self.imagen_2, self.imagen_3], start=1):
            path = campo.text()
            if path and os.path.exists(path):
                files[f"imagen_{idx}"] = open(path, "rb")

        data = {
            "nombre_tarea": self.nombre_tarea.text(),
            "horas": str(self.horas.value()),
            "descripcion": self.descripcion.toPlainText(),
            "tecnologias_utilizadas": self.tecnologias.text(),
            "link_ia_principal": self.link_ia1.text(),
            "link_ia_secundaria": self.link_ia2.text(),
            "link_ia_terciaria": self.link_ia3.text(),
            "link_respositorio": self.link_repo.text(),
            "commit_principal": self.commit.text(),
        }

        try:
            response = httpx.post("http://localhost:8000/api/dailylog/", data=data, files=files)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Tarea registrada correctamente.")
                self.clear_fields()
                if self.history_view:
                    self.history_view.cargar_datos()
            else:
                QMessageBox.warning(self, "Error", f"Error al registrar: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
        finally:
            for f in files.values():
                f.close()

    def clear_fields(self):
        self.nombre_tarea.clear()
        self.horas.setValue(0.0)
        self.descripcion.clear()
        self.tecnologias.clear()
        self.link_ia1.clear()
        self.link_ia2.clear()
        self.link_ia3.clear()
        self.link_repo.clear()
        self.commit.clear()
        self.imagen_1.clear()
        self.imagen_2.clear()
        self.imagen_3.clear()
