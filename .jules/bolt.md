## 2024-05-18 - Optimize N+1 Query in CampaignViewSet Statistics
**Learning:** Iterating over query results and doing single lookups (e.g. `Contacto.objects.get`) inside the loop leads to an N+1 query problem, increasing execution time and DB load as the number of distinct contacts grows.
**Action:** Bulk fetch the required related objects before the loop using `in_bulk()` or a dictionary comprehension (`{c.identidad: c for c in Model.objects.filter(...) }`) to achieve O(1) lookups in memory.
