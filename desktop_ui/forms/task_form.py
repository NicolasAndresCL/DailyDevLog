# task_form.py
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QTextEdit, QDoubleSpinBox, QPushButton, QMessageBox,
    QFileDialog, QScrollArea, QFrame, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QObject, QRunnable, QThreadPool
import weakref

API_URL = "http://localhost:8000/api/dailylog/"

class _SendTaskSignals(QObject):
    success = Signal(str)
    error = Signal(str)

class _SendTaskWorker(QRunnable):
    def __init__(self, data, files):
        super().__init__()
        self.data = data
        self.files = files
        self.signals = _SendTaskSignals()

    def run(self):
        import httpx
        try:
            with httpx.Client(timeout=30.0) as client:
                r = client.post(API_URL, data=self.data, files=self.files)
            if r.status_code == 201:
                self.signals.success.emit("Tarea registrada correctamente.")
            else:
                self.signals.error.emit(f"Error al registrar: {r.text}")
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            for f in self.files.values():
                try: f.close()
                except: pass

class TaskForm(QWidget):
    task_added = Signal()

    def __init__(self, history_view=None):
        super().__init__()
        self.setWindowTitle("Registrar Tarea Diaria")
        self._pool = QThreadPool.globalInstance()
        self._workers = []
        self.history_view_ref = weakref.ref(history_view) if history_view else None
        self._init_ui()

        # 🎨 Estilo global inspirado en vsc
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #86198f;
                font-family: 'Segoe UI';
                font-size: 13px;
            }

            QLineEdit, QTextEdit, QDoubleSpinBox {
                background-color: #252526;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 6px;
                color: #0d9488;
            }

            QLabel {
                color: #9CDCFE;
                font-weight: bold;
            }

            QPushButton {
                background-color: #701a75;
                color: #007ACC;
                border-radius: 4px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #2899F5;
            }

            QScrollArea {
                border: none;
            }

            QFrame {
                border: 1px solid #3C3C3C;
                border-radius: 6px;
                padding: 8px;
                background-color: #1E1E1E;
            }
        """)


    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        title_label = QLabel("Registrar Tarea Diaria")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        content_layout.addWidget(self._create_section("Datos de la tarea", self._build_task_form_layout()))
        content_layout.addWidget(self._create_section("Links y Repositorio", self._build_link_form_layout()))
        content_layout.addWidget(self._create_section("Capturas de pantalla", self._build_image_form_layout()))

        scroll_area.setWidget(content_widget)
        self.submit_btn = QPushButton("Guardar Tarea")
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
        section_title.setAlignment(Qt.AlignCenter)
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        section_title.setStyleSheet("""
            QLabel {
                color: #007ACC;
                background-color: #1E1E1E;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 8px;
            }
        """)

        section_layout.addWidget(section_title)
        section_layout.addLayout(layout)
        return section_frame


    def _crear_fila_estilizada(self, texto_label, widget):
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(QLabel(texto_label))
        layout.addWidget(widget)
        return contenedor

    def _build_task_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.nombre_tarea = QLineEdit()
        self.horas = QDoubleSpinBox()
        self.horas.setRange(0.0, 24.0)
        self.horas.setSingleStep(0.25)
        self.descripcion = QTextEdit()
        self.descripcion.setPlaceholderText("Describe la tarea...")
        self.tecnologias = QLineEdit()

        form.addRow(self._crear_fila_estilizada("Nombre de tarea:", self.nombre_tarea))
        form.addRow(self._crear_fila_estilizada("Horas trabajadas:", self.horas))
        form.addRow(self._crear_fila_estilizada("Descripción:", self.descripcion))
        form.addRow(self._crear_fila_estilizada("Tecnologías utilizadas:", self.tecnologias))
        return form

    def _build_link_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.link_ia1 = QLineEdit()
        self.link_ia2 = QLineEdit()
        self.link_ia3 = QLineEdit()
        self.link_repo = QLineEdit()
        self.commit = QLineEdit()

        form.addRow(self._crear_fila_estilizada("Link IA principal:", self.link_ia1))
        form.addRow(self._crear_fila_estilizada("Link IA secundaria:", self.link_ia2))
        form.addRow(self._crear_fila_estilizada("Link IA terciaria:", self.link_ia3))
        form.addRow(self._crear_fila_estilizada("Link repositorio:", self.link_repo))
        form.addRow(self._crear_fila_estilizada("Commit principal:", self.commit))
        return form

    def _build_image_form_layout(self):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.imagen_1 = QLineEdit()
        self.imagen_2 = QLineEdit()
        self.imagen_3 = QLineEdit()

        form.addRow(self._crear_fila_estilizada("Imagen 1:", self._create_image_selector(self.imagen_1)))
        form.addRow(self._crear_fila_estilizada("Imagen 2:", self._create_image_selector(self.imagen_2)))
        form.addRow(self._crear_fila_estilizada("Imagen 3:", self._create_image_selector(self.imagen_3)))
        return form

    def _create_image_selector(self, campo_line_edit):
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        btn = QPushButton("Seleccionar")
        btn.clicked.connect(lambda _, c=campo_line_edit: self.seleccionar_imagen(c))
        layout.addWidget(campo_line_edit)
        layout.addWidget(btn)
        return contenedor

    def seleccionar_imagen(self, campo):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            campo.setText(file_path)

    def enviar_tarea(self):
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
        QMessageBox.information(self, "Enviando", "La tarea se está enviando en segundo plano...")

        worker = _SendTaskWorker(data, files)
        worker.signals.success.connect(lambda msg, self_ref=weakref.ref(self): self_ref() and self_ref()._on_send_success(msg))
        worker.signals.error.connect(lambda msg, self_ref=weakref.ref(self): self_ref() and self_ref()._on_send_error(msg))
        self._workers.append(worker)
        self._pool.start(worker)

    def _on_send_success(self, msg):
        QMessageBox.information(self, "Éxito", msg)
        self.clear_fields()
        if self.history_view_ref and self.history_view_ref():
            self.history_view_ref().cargar_datos()
        self.task_added.emit()

    def _on_send_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

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

    