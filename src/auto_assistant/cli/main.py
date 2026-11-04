"""Comandos `ingest` y `ask`."""

import sys
from functools import partial
from pathlib import Path

from auto_assistant.agent.graph import build_graph
from auto_assistant.agent.verify import CITA
from auto_assistant.ingestion.chunker import chunk_text
from auto_assistant.ingestion.reader import read_document
from auto_assistant.models.client import complete
from auto_assistant.models.config import load_models_config
from auto_assistant.rag_config import load_rag_config
from auto_assistant.retrieval.embeddings import embed
from auto_assistant.retrieval.index import build_index, has_index, search


def ingest() -> None:
    """Lee el corpus, lo fragmenta y construye el índice."""
    rag, modelos = load_rag_config(), load_models_config()
    ruta = Path(rag["corpus"])
    chunks = chunk_text(ruta.name, read_document(ruta), rag["chunk_size"], rag["chunk_overlap"])
    build_index(chunks, partial(embed, model=modelos["embedding_model"]))
    print(f"Índice listo: {len(chunks)} fragmentos de {ruta}")


def ask() -> None:
    """Responde una pregunta e imprime sus citas."""
    if len(sys.argv) != 2:
        sys.exit('Uso: ask "pregunta"')
    if not has_index():
        sys.exit("No hay índice: corre primero: uv run ingest")
    rag, modelos = load_rag_config(), load_models_config()
    embedder = partial(embed, model=modelos["embedding_model"])
    grafo = build_graph(
        lambda q: search(q, rag["k"], embedder),
        partial(complete, modelos["answer_model"]),
        rag["threshold"],
    )
    r = grafo.invoke({"question": sys.argv[1]})
    print(r["answer"])
    if r["cited"]:
        print("\nCitas:")
        for n in sorted({int(n) for n in CITA.findall(r["answer"])}):
            c = r["hits"][n - 1].chunk
            print(
                f"[{n}] Artículo {c.article or 's/n'}, posición {c.start}-{c.end} de {c.document}"
            )
