import pytest

from auto_assistant.ingestion.chunker import chunk_text
from auto_assistant.ingestion.reader import read_document

TEXTO = (
    "Preámbulo de la ley.\n\n"
    "#### Artículo 1\n\n" + "uno dos tres cuatro cinco seis siete. " * 20 + "\n\n"
    "## Capítulo II. De algo\n\n"
    "### Sección primera. Otra\n\n"
    "#### Artículo 2 Bis\n\nTexto corto del segundo.\n"
)


def test_lee_md_y_txt(tmp_path):
    for nombre in ("a.md", "a.txt"):
        (tmp_path / nombre).write_text("hola\r\n ñ", encoding="utf-8")
        assert read_document(tmp_path / nombre) == "hola\r\n ñ"


def test_rechaza_otros_formatos(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"x")
    with pytest.raises(ValueError):
        read_document(tmp_path / "a.pdf")


def test_posiciones_exactas():
    chunks = chunk_text("doc.md", TEXTO, size=100, overlap=20)
    assert len(chunks) > 3
    for c in chunks:
        assert TEXTO[c.start : c.end] == c.text


def test_solapamiento_y_cobertura():
    chunks = [c for c in chunk_text("doc.md", TEXTO, 100, 20) if c.article == "1"]
    for a, b in zip(chunks, chunks[1:], strict=False):
        assert b.start < a.end  # hay solapamiento
        assert b.start > a.start  # y se avanza
    assert chunks[-1].end == TEXTO.index("## Capítulo II")


def test_articulo_asignado_y_sin_cruces():
    chunks = chunk_text("doc.md", TEXTO, 100, 20)
    assert chunks[0].article is None
    assert {c.article for c in chunks} == {None, "1", "2 Bis"}
    for c in chunks:
        if c.article == "1":
            assert "#### Artículo 2" not in c.text


def test_encabezados_de_capitulo_no_se_pegan_a_fragmentos():
    chunks = chunk_text("doc.md", TEXTO, 100, 20)
    for c in chunks:
        assert "## Capítulo" not in c.text and "### Sección" not in c.text
