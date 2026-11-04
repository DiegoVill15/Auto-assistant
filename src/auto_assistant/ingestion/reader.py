"""Lectura de documentos md y txt."""

from pathlib import Path

EXTENSIONES = {".md", ".txt"}


def read_document(path: Path) -> str:
    """Lee un documento tal cual, sin normalizar: las posiciones dependen de eso."""
    path = Path(path)
    if path.suffix not in EXTENSIONES:
        raise ValueError(f"Formato no soportado: {path.suffix}")
    with open(path, encoding="utf-8", newline="") as f:  # newline="": no traduce saltos de línea
        return f.read()
