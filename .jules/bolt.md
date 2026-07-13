
## 2024-05-23 - Fixed N+1 query in CampaignViewSet.statistics
**Learning:** Found a severe N+1 query problem when processing campaign statistics where `Contacto.objects.get()` was called in a loop for each unique contact in a results list.
**Action:** Use `Contacto.objects.in_bulk(list(contacto_ids))` before the loop to fetch all related contacts in a single query (O(1) instead of O(N)), drastically reducing the number of database queries and improving endpoint response times.
