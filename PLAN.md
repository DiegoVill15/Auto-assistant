# Plan de la versión corta

Queremos un RAG en español que mida qué tan bien encuentra la información y frene cualquier cambio que lo empeore. La fidelidad de las respuestas se reporta aparte.

Calculamos de 4 a 6 días, a 3 o 4 horas diarias. Al terminar cada fase paramos para revisarla.

Usamos Python, LangGraph, LiteLLM, bge-m3, ChromaDB, Pydantic, pytest, ruff y GitHub Actions.

Dejamos para después los guardrails, los fallbacks, la auto-optimización, los corpus ficticios, Langfuse, la API, la lectura de PDF y HTML, y la demo en vivo.

## Fase 0: Cimientos

Dejamos listo el proyecto con uv, ruff y pytest, con una carpeta por cada responsabilidad. Hoy solo existe `models/`. Después vendrán `ingestion/`, `retrieval/`, `agent/`, `evaluation/` y `cli/`.

Los modelos se definen en `config/models.yaml` y se llaman por LiteLLM. Un script hace una llamada corta a Ollama Cloud, OpenCode Go, OpenRouter y `claude -p` con Opus 5.5. GitHub Actions corre el lint y las pruebas.

**Está lista cuando** las pruebas pasan en local y en GitHub, y responden los cuatro proveedores.

**Para revisarla,** corres el script con tus llaves.

## Fase 1: RAG base

Convertimos una vez la Ley Federal de Protección al Consumidor a Markdown, desde el texto oficial. Luego la partimos en fragmentos, guardamos de dónde sale cada uno y creamos sus embeddings con bge-m3 en local. Si Ollama da problemas, usamos sentence-transformers.

El flujo en LangGraph busca, responde con citas y comprueba que la respuesta tenga sustento. Si lo que encuentra es débil, dice que no sabe. Todo se usa con el comando `ask`.

**Está lista cuando** pasan las pruebas de lectura y fragmentación, y las respuestas sobre la ley traen citas.

**Para revisarla,** haces 10 preguntas tuyas.

## Fase 2: Golden set

El golden set es el conjunto de preguntas revisadas con el que medimos todo lo demás. Lo genera Opus 5.5 una sola vez y en lotes pequeños, con un script aparte.

Incluye preguntas directas, que combinan varios artículos, que piden razonar y que la ley no responde. Cada una trae su respuesta esperada y el pasaje de donde sale. El pasaje se guarda por documento y posición, porque así seguimos pudiendo medir aunque cambie la forma de fragmentar.

El código descarta las preguntas repetidas, las mal formadas y las que no se pueden comprobar contra su pasaje. Un comando te deja aprobar o rechazar cada pregunta. Al final, el set se guarda en JSONL y ya no se toca.

**Está lista cuando** hay al menos 60 preguntas, 15% o más no tienen respuesta en la ley y revisaste todas. Proponemos aprobar al menos 80%.

**Para revisarla,** lees el golden set.

## Fase 3: Evaluación y comparación

El código mide la búsqueda con recall@k, MRR y hit rate. Un modelo juez califica la fidelidad y si el asistente se niega a responder cuando debe. Lo corremos solo desde tu Mac, nunca en GitHub, y con pocas llamadas a la vez.

Para elegir al juez entre `kimi-k3` y `deepseek-v4-pro`, etiquetas 20 respuestas a mano y gana el que más coincida contigo. También probamos en español Ragas, DeepEval o algo propio, y nos quedamos con uno.

El resultado es un reporte con calidad, tiempos y tokens, más una gráfica pequeña que compara `glm-5.3-flash`, `mimo-v2.6-flash`, `gemma4:31b-cloud` y `nemotron-3-ultra-550b-a55b:free`. La caché separa cada corrida para poder medir cuánto varían los resultados.

**Está lista cuando** tenemos una corrida completa con al menos 2 modelos. Empezamos con una corrida por modelo y llegamos a tres solo si los límites lo permiten.

**Para revisarla,** comparas el reporte con tu criterio en 10 casos.

## Fase 5: Puerta de calidad

GitHub Actions corre solo las métricas del código, sin LLM ni llaves. Los umbrales llevan un margen para no bloquear por ruido, porque con 60 preguntas cada una vale 1.67 puntos.

El caso de un documento que contradice a otro lo probamos en tu Mac con el juez.

**Está lista cuando** un PR que empeora la fragmentación queda bloqueado.

**Para revisarla,** abres un PR que rompa algo a propósito.

## Fase 7: Presentación

Terminamos el README con la arquitectura, la gráfica de modelos y los pasos para reproducir todo. También agregamos la licencia MIT.

**Está lista cuando** alguien que no conoce el proyecto puede clonarlo y sacar un reporte siguiendo solo el README.
