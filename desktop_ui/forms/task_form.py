from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QTextEdit, QDoubleSpinBox, QPushButton, QMessageBox,
    QFileDialog, QScrollArea, QFrame, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, Signal
import httpx
import os

API_URL = "http://localhost:8000/api/dailylog/"

class TaskForm(QWidget):
    # Señal para notificar a otras vistas que se ha añadido una tarea
    task_added = Signal()

    def __init__(self, history_view=None):
        super().__init__()
        self.setWindowTitle("📝 Registrar Tarea Diaria")
        self.history_view = history_view
        self._init_ui()
        self.setStyleSheet(self._get_stylesheet())

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Contenedor principal con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Título principal
        title_label = QLabel("Registrar Tarea Diaria")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        # Secciones del formulario
        content_layout.addWidget(self._create_section("Datos de la tarea", self._build_task_form_layout()))
        content_layout.addWidget(self._create_section("Links y Repositorio", self._build_link_form_layout()))
        content_layout.addWidget(self._create_section("Capturas de pantalla", self._build_image_form_layout()))

        scroll_area.setWidget(content_widget)

        # Botón de guardar
        self.submit_btn = QPushButton("✅ Guardar Tarea")
        self.submit_btn.setFixedHeight(45)
        self.submit_btn.clicked.connect(self.enviar_tarea)

        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.submit_btn)

    def _create_section(self, title, layout):
        section_frame = QFrame()
        section_layout = QVBoxLayout(section_frame)
        section_layout.setContentsMargins(15, 15, 15, 15)
        section_layout.setSpacing(10)
        
        section_title = QLabel(title)
        section_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        section_title.setStyleSheet("color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px;")

        section_layout.addWidget(section_title)
        section_layout.addLayout(layout)
        return section_frame

    def _build_task_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.nombre_tarea = QLineEdit()
        self.horas = QDoubleSpinBox()
        self.horas.setRange(0.0, 24.0)
        self.horas.setSingleStep(0.25)
        self.descripcion = QTextEdit()
        self.descripcion.setPlaceholderText("Describe la tarea, su objetivo y lo aprendido...")
        self.tecnologias = QLineEdit()

        form.addRow("Nombre de tarea:", self.nombre_tarea)
        form.addRow("Horas trabajadas:", self.horas)
        form.addRow("Descripción:", self.descripcion)
        form.addRow("Tecnologías utilizadas:", self.tecnologias)
        return form

    def _build_link_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.link_ia1 = QLineEdit()
        self.link_ia2 = QLineEdit()
        self.link_ia3 = QLineEdit()
        self.link_repo = QLineEdit()
        self.commit = QLineEdit()

        form.addRow("Link IA principal:", self.link_ia1)
        form.addRow("Link IA secundaria:", self.link_ia2)
        form.addRow("Link IA terciaria:", self.link_ia3)
        form.addRow("Link repositorio:", self.link_repo)
        form.addRow("Commit principal:", self.commit)
        return form

    def _build_image_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        self.imagen_1 = QLineEdit()
        self.imagen_2 = QLineEdit()
        self.imagen_3 = QLineEdit()

        form.addRow(self._create_image_selector("Imagen 1:", self.imagen_1))
        form.addRow(self._create_image_selector("Imagen 2:", self.imagen_2))
        form.addRow(self._create_image_selector("Imagen 3:", self.imagen_3))
        return form

    def _create_image_selector(self, label_text, campo_line_edit):
        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        label = QLabel(label_text)
        btn = QPushButton("Seleccionar")
        btn.clicked.connect(lambda: self.seleccionar_imagen(campo_line_edit))
        h_layout.addWidget(label)
        h_layout.addWidget(campo_line_edit)
        h_layout.addWidget(btn)
        return h_layout

    def seleccionar_imagen(self, campo):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            campo.setText(file_path)

    def enviar_tarea(self):
        # Validaciones básicas
        if not self.nombre_tarea.text() or self.horas.value() == 0.0 or not self.descripcion.toPlainText():
            QMessageBox.warning(self, "Campos incompletos", "Los campos 'Nombre de tarea', 'Horas' y 'Descripción' son obligatorios.")
            return

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
            response = httpx.post(API_URL, data=data, files=files)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Tarea registrada correctamente.")
                self.clear_fields()
                if self.history_view:
                    self.history_view.cargar_datos()
                self.task_added.emit()
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

    def _get_stylesheet(self):
        return """
            QWidget {
                background-color: #f8f9fa;
                font-family: "Segoe UI", sans-serif;
            }
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton#selectImageBtn {
                background-color: #6c757d;
            }
            QPushButton#selectImageBtn:hover {
                background-color: #5a6268;
            }
        """
