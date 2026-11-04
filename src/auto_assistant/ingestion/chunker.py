"""Fragmentación de texto con posiciones exactas en el original."""

import re
from dataclasses import dataclass

ENCABEZADO = re.compile(r"^(#{2,4}) (.+)$", re.MULTILINE)
ARTICULO = "#### Artículo "


@dataclass(frozen=True)
class Chunk:
    document: str
    start: int  # posición inicial en caracteres: text[start:end] es el fragmento
    end: int
    article: str | None
    text: str


def _sections(text: str) -> list[tuple[int, int, str | None]]:
    """Divide el texto en (inicio, fin, artículo): cada encabezado ##, ### o #### abre una sección."""  # noqa: E501
    marcas = [
        (
            m.start(),
            m.group(0)[len(ARTICULO) :].strip() if m.group(0).startswith(ARTICULO) else None,
        )
        for m in ENCABEZADO.finditer(text)
    ]
    inicios = [(0, None)] + marcas if not marcas or marcas[0][0] > 0 else marcas
    fines = [p for p, _ in inicios[1:]] + [len(text)]
    return [(i, f, a) for (i, a), f in zip(inicios, fines, strict=True)]


def _tiene_texto(text: str, ini: int, fin: int) -> bool:
    """Una sección de capítulo o sección solo cuenta si trae texto además de su encabezado."""
    cuerpo = text[ini:fin]
    return bool(ENCABEZADO.sub("", cuerpo, count=1).strip()) if cuerpo.startswith("#") else True


def chunk_text(document: str, text: str, size: int, overlap: int) -> list[Chunk]:
    """Parte el texto en ventanas de ~size caracteres con solapamiento dentro de cada artículo."""
    chunks = []
    for ini, fin, article in _sections(text):
        if article is None and not _tiene_texto(text, ini, fin):
            continue
        start = ini
        while start < fin:
            end = min(start + size, fin)
            if end < fin:  # corta en el último espacio para no partir palabras
                corte = text.rfind(" ", start + size // 2, end)
                end = corte + 1 if corte > start else end
            if text[start:end].strip():
                chunks.append(Chunk(document, start, end, article, text[start:end]))
            if end >= fin:
                break
            start = max(end - overlap, start + 1)
    return chunks
