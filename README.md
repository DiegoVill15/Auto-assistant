# Auto-assistant

Un asistente RAG en español que se revisa solo. Mide su calidad con preguntas de prueba y frena los cambios que la empeoran.

Responde sobre la Ley Federal de Protección al Consumidor. Es solo material de consulta, así que no lo tomes como asesoría legal.

## Instalación

Necesitas [uv](https://docs.astral.sh/uv/) y [Ollama](https://ollama.com) con tu sesión iniciada, porque usamos sus modelos en la nube. Para la prueba completa también necesitas la CLI de `claude` con el plan Pro.

```bash
uv sync
cp .env.example .env
```

Después pon tus llaves de OpenCode Go y OpenRouter en `.env`.

## Uso

Por ahora puedes comprobar que todos los proveedores responden. El script hace una llamada muy corta a cada uno:

```bash
set -a
source .env
set +a
uv run python scripts/smoke.py
```

Si todo va bien, verás esto:

```
OK    ollama
OK    openrouter
OK    opencode_go
OK    claude -p
```

Para correr las pruebas y revisar el estilo del código:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Arquitectura

El proyecto apenas empieza, así que por ahora son tres piezas. En `config/models.yaml` están los modelos que usamos. En `src/auto_assistant/models/` está el código que los carga y los llama. Y `scripts/smoke.py` es el script de arriba.

## Licencia

Va a ser MIT. El archivo se agrega al final del proyecto.
