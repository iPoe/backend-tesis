
## 2025-02-23 - Bulk fetch statistics N+1
**Learning:** Found an N+1 query loop when getting Contacto instances in `campaigns/viewsets.py` inside the `CampaignViewSet.statistics` action. For each row in `resultados`, it queries the DB for `Contacto.objects.get(identidad=contacantiguo)`.
**Action:** Use `.in_bulk(ids, field_name='identidad')` before the loop, extracting unique contact IDs, mapping them by the integer primary key, and accessing via the mapped dictionary in memory.
