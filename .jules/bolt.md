## 2024-05-24 - N+1 query and redundant querying in Django tasks
**Learning:** Background tasks dispatching external messages were querying the `contactosxcampa` model and then iterating over it without `select_related('contacto')`, leading to N+1 queries. Additionally, `enviar_correos` was performing the exact same `.filter(campania=ID)` query twice instead of reusing the queryset.
**Action:** Use `select_related('contacto')` when iterating over a queryset that accesses a foreign key, and always reuse querysets rather than executing identical `.filter()` calls.
