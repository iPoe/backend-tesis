## 2024-10-31 - Resolved N+1 query in CampaignViewSet.statistics
**Learning:** Inside `CampaignViewSet.statistics`, there was an N+1 query problem caused by executing `Contacto.objects.get(identidad=contacantiguo)` inside a loop iterating over results. This was fetching contacts one by one.
**Action:** When optimizing DRF serialization loops over related models, always extract the primary keys first and use `.in_bulk(ids, field_name='pk_field')` (or `__in=` combined with `select_related`) to bulk fetch records in O(1) queries instead of O(N) `.get()` calls.
