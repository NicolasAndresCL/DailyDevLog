"""Configuración global de pytest.

Fuerza SQLite en memoria para la suite de tests, independiente de `DATABASE_URL`
del entorno (producción usa Postgres). Ver skill.md §5.
"""
import os

# Debe ejecutarse antes de que Django cargue `config.settings`.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ.setdefault("DEBUG", "True")
