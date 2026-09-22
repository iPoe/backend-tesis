## 2025-02-18 - Avoid N+1 Queries in Background Tasks
**Learning:** Missed `select_related` in Celery tasks (like `enviar_correos` and `envMensajeUsuarias`) processing loops over related `ForeignKey` fields leads to severe N+1 query bottlenecks that can silently delay background job execution. Duplicate querysets can also be inadvertently evaluated.
**Action:** Always verify loops within Celery tasks over Django querysets are utilizing `.select_related()` or `.prefetch_related()` for accessed fields and deduplicate queryset variables to avoid redundant queries.
