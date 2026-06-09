## 2024-06-09 - N+1 Query Resolution in Serialized Django ViewSets
**Learning:** Querying `Contacto.objects.get()` inside a loop that iterates over `resultados` (in `CampaignViewSet.statistics`) creates a significant N+1 query bottleneck.
**Action:** Bulk-fetch related instances upfront via `.filter(identidad__in=contact_ids)` into an in-memory dictionary for O(1) lookups to optimize database performance before processing serialization loops.
