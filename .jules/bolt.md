## 2024-05-24 - Resolve N+1 query in CampaignViewSet.statistics
**Learning:** When retrieving campaign statistics, looping through results and querying `Contacto.objects.get()` inside the loop for each unique contact ID creates an N+1 query bottleneck.
**Action:** Bulk fetch the `Contacto` objects before the loop using `Contacto.objects.in_bulk(contacto_ids)` to create a dictionary for O(1) lookups, drastically reducing database queries and optimizing performance.
