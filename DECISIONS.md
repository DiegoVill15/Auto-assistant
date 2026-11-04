# Decisiones

**Todos los modelos pasan por LiteLLM.** Así cambiar de proveedor es cambiar la configuración. La excepción es el script del golden set, que usa Opus 5.5 con `claude -p`.

**Opus 5.5 escribe las preguntas de prueba y otro modelo las juzga.** Si el mismo modelo hiciera las dos cosas, se estaría calificando a sí mismo. El juez tampoco puede ser uno de los modelos que comparamos.

**Los LLM corren en la nube y los embeddings en local.** No queremos cargar la MacBook con modelos grandes. Los embeddings locales permiten revisar la calidad en GitHub sin llaves.

**La revisión en GitHub no usa LLM.** Las métricas son repetibles y no se gastan límites en cada PR.

**OpenCode Go usa su URL directa por ahora.** LiteLLM ya tiene el proveedor en su código, pero todavía no en una versión estable. Lo cambiamos cuando salga.

**OpenRouter es el proveedor gratis.** Permite 50 peticiones al día y sus modelos gratis cambian seguido, así que cada reporte lleva fecha.

**Python 3.12 fijado con uv.** La Mac trae la 3.15 y preferimos no depender de una versión tan nueva.

**Las carpetas se crean cuando hacen falta.** Por eso todavía no existen `corpora/` ni `evals/`.
