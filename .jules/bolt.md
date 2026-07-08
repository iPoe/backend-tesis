
## 2024-07-08 - Fixed N+1 Query in CampaignViewSet
**Learning:** Found N+1 query bottlenecks within `CampaignViewSet.statistics` looping over `resultados` (iteratively fetching `Contacto.objects.get()`) and inside `_get_base_stats()` fetching related `Medio` objects during the `mxc` loop without `select_related`.
**Action:** Used `Contacto.objects.in_bulk(contacto_ids)` before looping through results to fetch all contacts into an in-memory dictionary. Added `.select_related('medio_id__tipo_medio', 'medio_id__smsmedio', 'medio_id__whatsappmedio')` to the `mediosxcampania` query to perform a single query to the database for relations.
