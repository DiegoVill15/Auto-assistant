"""Índice persistente en ChromaDB y búsqueda top-k."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.config import Settings

from auto_assistant.ingestion.chunker import Chunk

RUTA_POR_DEFECTO = Path(".chroma")
COLECCION = "corpus"
Embedder = Callable[[list[str]], list[list[float]]]


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float  # similitud coseno: más alto es más parecido


def _client(path: Path):
    return chromadb.PersistentClient(path=str(path), settings=Settings(anonymized_telemetry=False))


def _collection(path: Path):
    return _client(path).get_or_create_collection(COLECCION, metadata={"hnsw:space": "cosine"})


def has_index(path: Path = RUTA_POR_DEFECTO) -> bool:
    """Dice si existe un índice con fragmentos, sin crearlo."""
    client = _client(path)
    return COLECCION in [c.name for c in client.list_collections()] and (
        client.get_collection(COLECCION).count() > 0
    )


def build_index(chunks: list[Chunk], embedder: Embedder, path: Path = RUTA_POR_DEFECTO) -> None:
    """Reemplaza el índice con los fragmentos dados."""
    client = _client(path)
    if COLECCION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLECCION)
    coleccion = client.create_collection(COLECCION, metadata={"hnsw:space": "cosine"})
    for i in range(0, len(chunks), 32):  # por lotes para no saturar al modelo de embeddings
        lote = chunks[i : i + 32]
        coleccion.add(
            ids=[f"{c.document}:{c.start}-{c.end}" for c in lote],
            embeddings=embedder([c.text for c in lote]),
            documents=[c.text for c in lote],
            metadatas=[
                {"document": c.document, "start": c.start, "end": c.end, "article": c.article or ""}
                for c in lote
            ],
        )


def search(query: str, k: int, embedder: Embedder, path: Path = RUTA_POR_DEFECTO) -> list[Hit]:
    """Devuelve los k fragmentos más parecidos a la consulta, del mejor al peor."""
    r = _collection(path).query(query_embeddings=embedder([query]), n_results=k)
    return [
        Hit(Chunk(m["document"], m["start"], m["end"], m["article"] or None, t), 1 - d)
        for t, m, d in zip(r["documents"][0], r["metadatas"][0], r["distances"][0], strict=True)
    ]
