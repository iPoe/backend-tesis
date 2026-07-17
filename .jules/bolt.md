## 2024-07-17 - Optimize CampaignViewSet.statistics N+1 queries
**Learning:** `CampaignViewSet.statistics` had an N+1 query issue inside a loop retrieving contact information (`Contacto.objects.get`).
**Action:** Replaced the loop query with a single `in_bulk()` lookup pre-fetched before the loop (`Contacto.objects.in_bulk(..., field_name="identidad")`), then mapped the objects iteratively. Using `field_name` with `in_bulk` is crucial when the mapping key is not the primary key.
