"""Flujo LangGraph: buscar, responder con citas y verificar."""

from collections.abc import Callable
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from auto_assistant.agent.verify import verify_citations
from auto_assistant.retrieval.index import Hit

NO_SE = "No sé: no encontré información suficiente en la ley para responder esa pregunta."
SIN_SUSTENTO = "No pude sustentar la respuesta con citas de la ley."

PROMPT = """Responde en español usando SOLO los fragmentos de la Ley Federal de Protección al \
Consumidor. Cita cada afirmación con el número del fragmento entre corchetes, como [1]. \
Si los fragmentos no bastan, di que no lo sabes.

{fragmentos}

Pregunta: {pregunta}"""


class Estado(TypedDict, total=False):
    question: str
    hits: list[Hit]
    answer: str
    cited: bool


def build_graph(search: Callable[[str], list[Hit]], llm: Callable[[str], str], threshold: float):
    """Arma el grafo. `search` y `llm` se inyectan para poder simularlos en pruebas."""

    def buscar(s: Estado) -> Estado:
        return {"hits": search(s["question"])}

    def responder(s: Estado) -> Estado:
        hits = s["hits"]
        if not hits or hits[0].score < threshold:
            return {"answer": NO_SE}  # evidencia débil: no se llama al LLM
        fragmentos = "\n\n".join(
            f"[{i}] (Artículo {h.chunk.article or 's/n'})\n{h.chunk.text}"
            for i, h in enumerate(hits, 1)
        )
        return {"answer": llm(PROMPT.format(fragmentos=fragmentos, pregunta=s["question"]))}

    def verificar(s: Estado) -> Estado:
        if s["answer"] == NO_SE:
            return {"cited": False}
        if verify_citations(s["answer"], len(s["hits"])):
            return {"cited": True}
        return {"answer": SIN_SUSTENTO, "cited": False}

    g = StateGraph(Estado)
    g.add_node("buscar", buscar)
    g.add_node("responder", responder)
    g.add_node("verificar", verificar)
    g.add_edge(START, "buscar")
    g.add_edge("buscar", "responder")
    g.add_edge("responder", "verificar")
    g.add_edge("verificar", END)
    return g.compile()
