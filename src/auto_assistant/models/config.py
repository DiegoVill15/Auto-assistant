"""Carga y validación de config/models.yaml."""

from pathlib import Path

import yaml

RUTA_POR_DEFECTO = Path(__file__).resolve().parents[3] / "config" / "models.yaml"
CLAVES = (
    "golden_set_generator",
    "judge_candidates",
    "compared_models",
    "answer_model",
    "embedding_model",
)


def load_models_config(path: Path = RUTA_POR_DEFECTO) -> dict:
    """Devuelve la configuración de modelos o lanza ValueError si es inválida."""
    config = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    faltan = [k for k in CLAVES if not config.get(k)]
    if faltan:
        raise ValueError(f"Faltan claves en models.yaml: {', '.join(faltan)}")
    repetidos = set(config["judge_candidates"]) & set(config["compared_models"])
    if repetidos:
        raise ValueError(
            f"El juez candidato no puede estar en compared_models: {', '.join(sorted(repetidos))}"
        )
    return config
