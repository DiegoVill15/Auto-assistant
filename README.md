# Auto-assistant

Un asistente RAG en español que se revisa solo. Mide su calidad con preguntas de prueba y frena los cambios que la empeoran.

Responde sobre la Ley Federal de Protección al Consumidor. Es solo material de consulta, así que no lo tomes como asesoría legal.

## Instalación

Necesitas [uv](https://docs.astral.sh/uv/) y [Ollama](https://ollama.com) con tu sesión iniciada, porque usamos sus modelos en la nube. Para la prueba completa también necesitas la CLI de `claude` con el plan Pro.

```bash
uv sync
cp .env.example .env
```

Después pon tus llaves de OpenCode Go y OpenRouter en `.env`. Los embeddings corren en tu máquina con bge-m3, así que descárgalo una vez:

```bash
ollama pull bge-m3
```

## Uso

Primero indexa la ley. Esto fragmenta el texto y guarda los embeddings en `.chroma/`:

```bash
uv run ingest
```

Después pregunta lo que quieras. Con tus llaves cargadas:

```bash
set -a
source .env
set +a
uv run ask "¿Qué es la publicidad engañosa según la ley?"
```

La respuesta trae citas con el artículo y la posición del fragmento en el texto de la ley:

```
Según la Ley Federal de Protección al Consumidor, la publicidad engañosa o abusiva es aquella
que refiere características o información relacionadas con algún bien, producto o servicio que,
pudiendo o no ser verdaderas, inducen a error o confusión al consumidor [1].

Citas:
[1] Artículo 32, posición 40350-41547 de lfpc.md
```

Si la ley no habla del tema, responde que no sabe sin llamar al modelo. Si la respuesta no trae citas válidas, dice que no pudo sustentarla.

También puedes comprobar que todos los proveedores responden. El script hace una llamada muy corta a cada uno:

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

La configuración vive en `config/`: `models.yaml` con los modelos y `rag.yaml` con el tamaño de los fragmentos, cuántos se recuperan y el umbral para decir que no sabe. La ley en Markdown está en `corpora/lfpc/` y viene del texto oficial de la Cámara de Diputados.

En `src/auto_assistant/` cada carpeta hace una cosa. `ingestion/` lee el texto y lo parte en fragmentos que recuerdan su artículo y su posición exacta. `retrieval/` calcula los embeddings y busca en ChromaDB. `agent/` es el flujo de LangGraph que busca, responde y verifica las citas en código. `models/` carga la configuración y llama a los modelos con LiteLLM. `cli/` tiene los comandos `ingest` y `ask`.

## Licencia

Va a ser MIT. El archivo se agrega al final del proyecto.
