# Plan: versión corta

Objetivo: un RAG en español que mide su recuperación y formato contra preguntas revisadas, y bloquea el cambio si la calidad baja. La fidelidad se reporta aparte.

Estimación: 4 a 6 días, a 3 o 4 horas diarias. Cada fase termina en una parada para revisión.

**Stack:** Python, LangGraph, LiteLLM, bge-m3, ChromaDB, Pydantic, pytest, ruff y GitHub Actions.

**Fuera por ahora:** guardrails y fallbacks (Fase 4), auto-optimización (Fase 6), corpus ficticios, Langfuse, API, ingesta de PDF y HTML, y demo en vivo.

## Fase 0: Cimientos

- Estructura `tests/`, `corpora/`, `evals/` y `src/`, con una carpeta por responsabilidad: `models/` en esta fase; después `ingestion/`, `retrieval/`, `agent/`, `evaluation/` y `cli/`. Además, `pyproject.toml`, ruff y pytest.
- Capa de modelos con LiteLLM y configuración en YAML.
- Modelos definidos en `config/models.yaml`.
- Script de humo con Ollama y OpenCode Go, con user agent propio. Una llamada aparte confirma que `claude -p` funciona con Opus 5.5 en el plan Pro.
- GitHub Actions con lint y pruebas; README y `DECISIONS.md` iniciales.

**Aceptación:** pruebas en verde en local y en CI; el script responde con ambos proveedores y `claude -p` responde con Opus 5.5.

**Parada:** corres el script con tus llaves.

## Fase 1: RAG base

- Ley Federal de Protección al Consumidor, convertida una vez a Markdown desde el texto oficial.
- Ingesta de md y txt con chunking configurable y metadatos de fuente.
- Embeddings bge-m3, con sentence-transformers como alternativa si Ollama falla; índice local y recuperación top-k.
- Flujo LangGraph: recuperar, responder con citas y verificar soporte.
- Responde que no sabe cuando la recuperación es débil (umbral configurable).
- CLI `ask`.

**Aceptación:** pruebas de ingesta y chunking; respuestas con citas sobre la ley.

**Parada:** haces 10 preguntas propias.

## Fase 2: Golden set

- Preguntas por tipo (directas, multi-contexto, razonamiento y sin respuesta), con respuesta esperada y pasaje fuente.
- Cada pasaje se guarda por documento y posición, no por ID de chunk, para poder comparar configuraciones de chunking.
- Filtros deterministas: formato Pydantic, deduplicación y respuesta verificable contra el pasaje.
- Generador: Opus 5.5 con `claude -p`, en un script aparte que corre una vez y en lotes pequeños.
- Dataset en JSONL, versionado y congelado.
- CLI de revisión humana que registra aprobada o rechazada.

**Aceptación:** al menos 60 preguntas, mínimo 15% sin respuesta en los documentos y las 60 revisadas por ti. Tasa de aprobación propuesta: 80%.

**Parada:** revisas el golden set.

## Fase 3: Evaluación y comparación

- Métricas de recuperación en código: recall@k, MRR y hit rate.
- Juez solo en local, con pocas llamadas simultáneas: fidelidad y rechazo correcto. Elegir una herramienta (Ragas, DeepEval o propia) tras una prueba corta en español.
- Elegir al juez entre `kimi-k3` y `deepseek-v4-pro`: gana el que más coincida con 20 respuestas etiquetadas a mano.
- Reporte en Markdown con calidad, latencia y tokens.
- Gráfica pequeña que compara `glm-5.3-flash`, `mimo-v2.6-flash` y un modelo local de Ollama.
- La clave de caché incluye modelo, prompt, contexto y número de corrida.

**Aceptación:** corrida completa con al menos 2 modelos. Empieza con 1 corrida por modelo y llega a 3 solo si los límites de OpenCode Go lo permiten.

**Parada:** comparas el reporte contra tu criterio en 10 casos.

## Fase 5: Puerta de calidad

- GitHub Actions corre solo métricas deterministas, sin LLM ni llaves.
- Umbrales configurables, con un margen para no bloquear por ruido: con 60 preguntas, cada una vale 1.67 puntos.
- Una prueba local con el juez cubre el caso de un documento que contradice a otro.

**Aceptación:** un PR que empeora el chunking queda bloqueado.

**Parada:** abres un PR de prueba que rompa algo.

## Fase 7: Presentación

- README con arquitectura, gráfica de modelos y pasos para reproducir.

**Aceptación:** alguien que no conoce el proyecto clona el repo y reproduce un reporte siguiendo solo el README.

## Decisiones abiertas

- [ ] Nombre del proyecto y licencia (MIT o Apache-2.0)
- [ ] Modelo local de Ollama para la comparación
