"""Única puerta de entrada a los modelos: todo pasa por LiteLLM."""

import os
import uuid

import litellm

USER_AGENT = "auto-assistant/0.1"

# ponytail: LiteLLM 1.108 aún no publica opencode_go (ya está en su main). Al salir la versión estable, usar el proveedor y borrar esto.  # noqa: E501
OPENCODE_GO_PREFIJO = "opencode_go/"
OPENCODE_GO_API_BASE = "https://opencode.ai/inference/go/openai/v1"
OPENCODE_GO_ENV = "OPENCODE_GO_API_KEY"


def complete(
    model: str, prompt: str, temperature: float = 0.0, session_id: str | None = None
) -> str:
    """Envía un prompt al modelo y devuelve el texto de la respuesta."""
    extra = {}
    headers = {"User-Agent": USER_AGENT}
    if model.startswith(OPENCODE_GO_PREFIJO):
        model = "openai/" + model.removeprefix(OPENCODE_GO_PREFIJO)
        extra = {"api_base": OPENCODE_GO_API_BASE, "api_key": os.environ.get(OPENCODE_GO_ENV)}
        # Sin ID de sesión, cada llamada es su propia conversación.
        headers["x-opencode-session"] = session_id or str(uuid.uuid4())
    respuesta = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        extra_headers=headers,
        **extra,
    )
    return respuesta.choices[0].message.content
