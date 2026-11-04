"""Verificación de citas, hecha en código y sin LLM."""

import re

CITA = re.compile(r"\[(\d+)\]")


def verify_citations(answer: str, n_fragments: int) -> bool:
    """Debe haber al menos una cita [n] y cada n debe ser un fragmento recuperado (1..n)."""
    citas = {int(n) for n in CITA.findall(answer)}
    return bool(citas) and all(1 <= n <= n_fragments for n in citas)
