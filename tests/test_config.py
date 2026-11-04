import pytest
import yaml

from auto_assistant.models.config import load_models_config


def _escribir(tmp_path, datos):
    ruta = tmp_path / "models.yaml"
    ruta.write_text(yaml.safe_dump(datos), encoding="utf-8")
    return ruta


BASE = {
    "golden_set_generator": "g",
    "judge_candidates": ["j"],
    "compared_models": ["m"],
    "answer_model": "a",
    "embedding_model": "e",
}


def test_carga_config_real():
    config = load_models_config()
    assert config["compared_models"]


def test_carga_valida(tmp_path):
    assert load_models_config(_escribir(tmp_path, BASE)) == BASE


def test_falta_clave(tmp_path):
    with pytest.raises(ValueError, match="compared_models"):
        load_models_config(_escribir(tmp_path, {**BASE, "compared_models": []}))


def test_juez_en_comparados(tmp_path):
    with pytest.raises(ValueError, match="juez"):
        load_models_config(_escribir(tmp_path, {**BASE, "judge_candidates": ["m"]}))
