## 2024-05-24 - N+1 Query in envMensajeUsuarias
**Learning:** Similar to other celery tasks like `enviar_correos`, `envMensajeUsuarias` iterated over `contactosxcampa` to get contact phone numbers, which triggered an N+1 query issue for the `contacto` relation because `.select_related('contacto')` was omitted.
**Action:** Always verify if a `.filter()` query that will be iterated over accesses related objects. If so, apply `.select_related()` to preemptively load those objects in a single query.
