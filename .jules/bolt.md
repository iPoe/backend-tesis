## 2025-02-28 - Optimize envMensajeUsuarias and enviar_correos with select_related
**Learning:** The `envMensajeUsuarias` and `enviar_correos` functions in `campaigns/tasks.py` have N+1 query problems because they iterate over `contactosxcampa` and access the related `contacto` field to get phone numbers and emails without using `select_related('contacto')`. In addition, `enviar_correos` queries `contactosxcampa` twice, which is redundant.
**Action:** Optimize by adding `.select_related('contacto')` to the `contactosxcampa.objects.filter(...)` queries and reuse the first query's result in `enviar_correos` instead of running it again.

## 2025-02-28 - Optimize reply_whatsapp with select_related
**Learning:** The `reply_whatsapp` function in `campaigns/views.py` has an N+1 query problem during the list comprehension of `campañas_usuaria` that accesses the related `campania` and its `estado`. For each item, it triggers additional queries.
**Action:** Optimize by adding `.select_related('campania', 'campania__estado')` to the `contactosxcampa.objects.filter(contacto=usuaria)` query to fetch the related objects in a single query.
