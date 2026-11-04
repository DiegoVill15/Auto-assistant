"""Carga config/rag.yaml."""

from pathlib import Path

import yaml

RUTA_POR_DEFECTO = Path(__file__).resolve().parents[2] / "config" / "rag.yaml"
CLAVES = ("corpus", "chunk_size", "chunk_overlap", "k", "threshold")


def load_rag_config(path: Path = RUTA_POR_DEFECTO) -> dict:
    """Devuelve la configuración del RAG o lanza ValueError si es inválida."""
    config = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    faltan = [k for k in CLAVES if k not in config]
    if faltan:
        raise ValueError(f"Faltan claves en rag.yaml: {', '.join(faltan)}")
    if not 0 <= config["chunk_overlap"] < config["chunk_size"]:
        raise ValueError("chunk_overlap debe ser menor que chunk_size")
    return config
