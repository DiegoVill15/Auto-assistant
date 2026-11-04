# Decisiones

- Todo modelo pasa por LiteLLM. Única excepción: `claude -p` (Opus 5.5, plan Pro) para generar el golden set.
- Python 3.12 fijado con uv (`.python-version`): el del sistema es 3.15 y las dependencias aún no lo soportan.
- El golden set lo genera Opus 5.5; el juez corre en OpenCode Go y nunca es un modelo comparado.
- La puerta de CI no usa LLM ni secretos: solo lint y pruebas unitarias.
- Las carpetas se crean cuando su responsabilidad existe; por eso aún no hay `corpora/` ni `evals/`, aunque PLAN.md los mencione.
- OpenCode Go se llama por el endpoint compatible con OpenAI (`OPENCODE_GO_API_KEY`) hasta que LiteLLM publique el proveedor `opencode_go` en una versión estable.
- Solo modelos en la nube, sin correr LLM en la MacBook.
- OpenRouter como proveedor gratis: límite de 50 peticiones al día, y los modelos `:free` rotan, así que los reportes llevan fecha.
