# Decisiones

**Todos los modelos pasan por LiteLLM.** Así cambiar de proveedor es cambiar la configuración. La excepción es el script del golden set, que usa Opus 5.5 con `claude -p`.

**Opus 5.5 escribe las preguntas de prueba y otro modelo las juzga.** Si el mismo modelo hiciera las dos cosas, se estaría calificando a sí mismo. El juez tampoco puede ser uno de los modelos que comparamos.

**Los LLM corren en la nube y los embeddings en local.** No queremos cargar la MacBook con modelos grandes. Los embeddings locales permiten revisar la calidad en GitHub sin llaves.

**La revisión en GitHub no usa LLM.** Las métricas son repetibles y no se gastan límites en cada PR.

**OpenCode Go usa su URL directa por ahora.** LiteLLM ya tiene el proveedor en su código, pero todavía no en una versión estable. Lo cambiamos cuando salga.

**OpenRouter es el proveedor gratis.** Permite 50 peticiones al día y sus modelos gratis cambian seguido, así que cada reporte lleva fecha.

**Python 3.12 fijado con uv.** La Mac trae la 3.15 y preferimos no depender de una versión tan nueva.

**Las carpetas se crean cuando hacen falta.** Por eso todavía no existe `evals/`.

**La ley se convirtió una vez a Markdown desde el .doc oficial.** No se tocó el texto, solo se agregaron encabezados por capítulo y artículo. Los transitorios de los decretos de reforma quedaron fuera porque no responden preguntas sobre la ley vigente.

**Los fragmentos nunca cruzan artículos.** Así cada cita apunta a un solo artículo, y la posición en caracteres coincide exacta con el archivo.

**Chroma guarda el índice en `.chroma/` y se reconstruye en cada `ingest`.** Es más simple que actualizarlo y el corpus es chico.

**El umbral es 0.55 de similitud coseno.** Con 10 consultas de prueba, las preguntas sobre la ley sacaron de 0.59 a 0.69 y las de fuera de la ley de 0.33 a 0.50. Hay que revisarlo si cambian el corpus o el modelo de embeddings.

**Las citas se verifican en código.** Cada cita [n] debe apuntar a un fragmento recuperado y debe haber al menos una. Si no, la respuesta se descarta.
