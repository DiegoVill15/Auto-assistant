import pytest

from auto_assistant.agent.graph import NO_SE, SIN_SUSTENTO, build_graph
from auto_assistant.agent.verify import verify_citations
from auto_assistant.ingestion.chunker import Chunk
from auto_assistant.retrieval.index import Hit, build_index, has_index, search


def _hit(score):
    return Hit(Chunk("d.md", 0, 5, "7", "texto"), score)


def _grafo(score, respuesta):
    llamadas = []

    def llm(prompt):
        llamadas.append(prompt)
        return respuesta

    return build_graph(lambda q: [_hit(score), _hit(score)], llm, 0.5), llamadas


def test_verifica_citas():
    assert verify_citations("Sí [1] y [2].", 2)
    assert not verify_citations("Sin citas.", 2)
    assert not verify_citations("Cita fantasma [3].", 2)


def test_bajo_umbral_no_llama_al_llm():
    grafo, llamadas = _grafo(0.2, "x [1]")
    r = grafo.invoke({"question": "¿algo?"})
    assert r["answer"] == NO_SE and llamadas == []


def test_respuesta_con_citas_validas():
    grafo, llamadas = _grafo(0.9, "Dice esto [1].")
    r = grafo.invoke({"question": "¿algo?"})
    assert r["answer"] == "Dice esto [1]." and r["cited"] and len(llamadas) == 1


def test_respuesta_sin_sustento():
    grafo, _ = _grafo(0.9, "Dice esto sin cita.")
    assert grafo.invoke({"question": "¿algo?"})["answer"] == SIN_SUSTENTO


def test_indice_y_busqueda_con_embeddings_falsos(tmp_path):
    # Embedding falso: un vector por texto según si contiene "garantía".
    def falso(textos):
        return [[1.0, 0.0] if "garantía" in t else [0.0, 1.0] for t in textos]

    chunks = [Chunk("d.md", 0, 8, "1", "garantía"), Chunk("d.md", 8, 12, "2", "otro")]
    build_index(chunks, falso, tmp_path)
    hits = search("garantía del producto", 2, falso, tmp_path)
    assert hits[0].chunk == chunks[0] and hits[0].score > hits[1].score


def test_sin_indice_ask_pide_ingest(tmp_path, monkeypatch):
    from auto_assistant.cli import main

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(main.sys, "argv", ["ask", "¿algo?"])
    assert not has_index(tmp_path / ".chroma")
    with pytest.raises(SystemExit, match="uv run ingest"):
        main.ask()


def test_build_index_borra_carpetas_viejas(tmp_path):
    def falso(textos):
        return [[1.0, 0.0] for _ in textos]

    (tmp_path / "vieja").mkdir()
    chunk = Chunk("d.md", 0, 4, "1", "algo")
    build_index([chunk], falso, tmp_path)
    build_index([chunk], falso, tmp_path)
    assert not (tmp_path / "vieja").exists()
    assert len([d for d in tmp_path.iterdir() if d.is_dir()]) == 1
