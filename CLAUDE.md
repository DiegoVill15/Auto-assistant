# RAG que se auto-evalúa

Asistente RAG de código abierto y en español. Cuando cambia el código o la base de conocimiento, mide la calidad con preguntas de prueba y bloquea el cambio si baja. Es un proyecto de portafolio.

La promesa principal es **"se evalúa solo"**. "Se adapta solo" es un extra de la Fase 6 y no se presenta como función central.

Estamos construyendo la versión corta, descrita en `PLAN.md`. El plan completo vive en [Claude Docs](https://claude.ai/artifact/Mr1ft9QxgJArPXCqrYw2JM).

## Reglas de trabajo

1. Trabaja solo en la fase que yo indique. No empieces la siguiente sin mi aprobación explícita.
2. Cada fase termina con código, pruebas que pasan, README actualizado y el comando exacto para que yo la pruebe.
3. Al detenerte, entrega un resumen corto: qué hiciste, qué no, decisiones tomadas y dudas abiertas.
4. No agregues dependencias ni funciones fuera del alcance de la fase sin preguntar.
5. Usa el plugin ponytail para no escribir código de más.

## Git

- Crea una rama por feature completa o por fix. Los cambios pequeños que no son fixes no llevan rama propia.
- Haz commits pequeños con [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `<tipo>[(scope)]: <descripción>`.
- Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `build`, `perf`, `style`, `chore`. Un cambio incompatible lleva `!`, como en `feat!:`.
- Ejemplo: `feat(retrieval): agregar búsqueda top-k`.
- Los commits y los PR no llevan a Claude como coautor ni mencionan que se generaron con Claude.

## Organización del código

Organiza el proyecto para que sea escalable y fácil de mantener.

- Separa carpetas y funciones según su finalidad: cada carpeta, archivo y función tiene una sola responsabilidad.
- Crea una carpeta o archivo cuando la responsabilidad ya exista, no por si acaso.

## Documentación

- **`DECISIONS.md`:** cada decisión ocupa de 1 a 3 líneas: qué se decidió y por qué. Fusiona o elimina lo obsoleto para mantenerlo corto.
- **`README.md`:** crece poco a poco, resumido y para usuarios. Orden: nombre y descripción de una línea, instalación con requisitos, uso con un ejemplo y su salida, arquitectura y licencia. Lo extenso va en `docs/`.

## Sub-agentes

- **Investigar:** sub-agente Haiku 5.5.
- **Codificar:** sub-agente Sonnet 5.5. Las tareas complicadas las edita el agente principal, Opus 5.5.
- Mantén abiertas las sesiones de los sub-agentes y retómalas para no perder contexto ni releer archivos.

## Pruebas

En este proyecto sí están autorizadas las pruebas que pida `PLAN.md`, como excepción a mi regla global de no crear tests y al chequeo de ponytail. Las pruebas adicionales se sugieren primero.

## Reglas técnicas

- Lo que el código puede medir (recall, formato, citas) se mide en código con pruebas unitarias. El LLM no decide eso.
- Las regresiones no usan IA, salvo que sea muy necesario.
- No corras LLM locales en mi MacBook: usa solo modelos en la nube (OpenCode Go, Ollama Cloud y un proveedor gratis). Los embeddings sí corren en local.
- Las evaluaciones con LLM se lanzan desde mi Mac, nunca en CI, con pocas llamadas simultáneas.
- Todo modelo se llama por LiteLLM, nunca con SDKs de proveedores directo en la lógica. Única excepción: el script aparte que genera el golden set con `claude -p` y Opus 5.5, usando mi plan Claude Pro.
- Los modelos se definen en `config/models.yaml`.
- Las preguntas de evaluación se generan con un modelo y se juzgan con otro distinto.
- El juez nunca es uno de los modelos que se comparan.
- Claude Pro solo genera el golden set. No se usa como juez ni en CI.
- El golden set se congela y se versiona.
- Ninguna llave API va en el repo: usa variables de entorno y un `.env.example`.

## Corpus

Corpus significa el conjunto de documentos que el asistente consulta. El de la versión corta es la Ley Federal de Protección al Consumidor, tomada del texto oficial de la Cámara de Diputados. El README aclara que el proyecto no da asesoría legal.

## Resultado final

El proyecto termina con una gráfica pequeña que compara modelos, generada con datos de corridas reales, para respaldar su veracidad.