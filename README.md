# Auto-assistant

Asistente RAG de código abierto y en español que se auto-evalúa: mide su calidad con preguntas de prueba y bloquea los cambios que la bajan.

> Este proyecto no da asesoría legal. El corpus es la Ley Federal de Protección al Consumidor, solo como material de consulta.

## Instalación

Requisitos: [uv](https://docs.astral.sh/uv/), [Ollama](https://ollama.com) con `qwen3.5:9b` y, para el script de humo, la CLI `claude` con sesión del plan Pro.

```bash
uv sync
cp .env.example .env   # y completa OPENCODE_GO_API_KEY
```

## Uso

Prueba de humo (una llamada mínima por proveedor; no corre en CI):

```bash
set -a; source .env; set +a
uv run python scripts/smoke.py
```

Ejemplo de salida:

```
OK    ollama
OK    opencode_go
OK    claude -p
```

Pruebas y lint: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`.

## Arquitectura (estado actual)

- `config/models.yaml`: modelos comparados, jueces candidatos y generador del golden set.
- `src/auto_assistant/models/`: carga de la configuración y `complete()`, único acceso a modelos vía LiteLLM.
- `scripts/smoke.py`: verifica Ollama, OpenCode Go y `claude -p`.

## Licencia

Por definir.
