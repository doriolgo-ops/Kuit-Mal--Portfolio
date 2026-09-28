# Perroco Lab — pipeline de investigación (piloto)

Pipeline que investiga materiales del master `Perroco_Lab_Research_Master_v2.xlsx` **sin modificarlo**.
Cada dato pasa por: `RAW SOURCE → EXTRACTED CLAIM → NORMALISED CLAIM → VALIDATION → PROPOSED CHANGE`.

## Qué mirar (para el revisor)

| Archivo | Qué es |
|---|---|
| `output/pilot_report.md` | Informe del piloto: resumen global + detalle de los 20 materiales |
| `output/materials/<ID>.md` | Informe de un material |
| `output/proposed_changes.jsonl` | Propuesta de cambios al master (una línea por cambio, con evidencia y estado de revisión) |
| `output/pilot_summary.csv` | Tabla resumen (se abre en Excel) |
| `data/audit/audit_verdicts.json` | Auditoría manual de una muestra de claims (estimación de precisión) |

Estados de revisión: `AUTO_ELIGIBLE` (fabricante oficial + identidad exacta + sin conflicto),
`NEEDS_REVIEW`, `BLOCKED_CONFLICT`. En el piloto **nada** se aplica al master.

## Estructura

```
config/            selección del piloto, ajustes, registro de dominios/licencias, protocolo de búsqueda
perroco/           código (fetch con robots.txt, extracción HTML/PDF/SDS, identidad, validación, propuestas, informe)
data/search_ingest queries de búsqueda y resultados en bruto (capa de búsqueda)
data/staging.sqlite  staging completo: estados, leads, documentos, claims, conflictos, propuestas
data/manifests/    procedencia: hash sha256 + URLs de cada documento, log de descargas, historial de estados
data/cache/        documentos descargados (solo local; no se publican por copyright)
logs/              logs de ejecución
input/             copia local del master (no se publica)
```

## Ejecutar / reanudar

```
pip install -r requirements.txt
python run_pilot.py            # ejecuta o reanuda todas las fases
python run_pilot.py --status   # estado de cada material
python run_pilot.py --redo extract   # recalcula desde una fase sin volver a descargar
```

Estados por material: NOT_STARTED, SEARCHING, SOURCES_FOUND, EXTRACTED, NEEDS_REVIEW, VALIDATED,
NO_PUBLIC_DATA_FOUND, PUBLIC_RESEARCH_EXHAUSTED, ERROR. Las fases completadas se registran por material
y los documentos se guardan por hash, así que una interrupción no obliga a repetir nada.

## Reglas que el código aplica

- robots.txt se respeta para nuestro agente **y** para los agentes de Anthropic/Claude; 401/403/429 o páginas
  anti-bot → `MANUAL_RETRIEVAL_REQUIRED` y el dominio no se vuelve a pedir en esa ejecución.
- Un documento = un hash; espejos y copias casi idénticas no cuentan como evidencia independiente.
- Datos de distribuidor nunca se convierten en datos de fabricante.
- Valores contradictorios → `CONFLICT`, se guardan todos, no se sobrescribe nada.
- GC-MS publicado → `REFERENCE_COMPOSITION` (muestra de investigación, nunca la botella ISIPCA).
- Hazards de sustancia pura (PubChem) no se trasladan a CLP HAZARDS de un producto comercial.
- Solo se guardan hechos y fragmentos de contexto ≤200 caracteres.

## Capa de búsqueda

Los buscadores web no son accesibles por script desde este entorno (robots.txt de Google/Bing, DuckDuckGo
cortado por el proxy, sin clave de API). Las búsquedas las ejecuta el agente operador con su herramienta de
búsqueda y quedan registradas tal cual en `data/search_ingest/` (ver `config/SEARCH_PROTOCOL.md`). Si en el
futuro se dispone de una API de búsqueda (p. ej. Brave/SerpAPI), basta con escribir el mismo formato de archivo.
PubChem y NCBI PMC se consultan directamente por sus APIs públicas.
