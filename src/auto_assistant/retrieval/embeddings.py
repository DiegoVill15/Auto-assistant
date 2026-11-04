"""Embeddings por LiteLLM."""

import math

import litellm


def embed(texts: list[str], model: str) -> list[list[float]]:
    """Devuelve un vector por texto. Falla si el modelo devuelve NaN."""
    respuesta = litellm.embedding(model=model, input=texts)
    vectores = [d["embedding"] for d in respuesta.data]
    if any(math.isnan(x) for v in vectores for x in v):
        raise ValueError(f"El modelo {model} devolvió NaN en los embeddings")
    return vectores
