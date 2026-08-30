## 2024-05-18 - Optimized CampaignViewSet.statistics N+1 Query
**Learning:** Serializing campaign statistics loops through grouped database records and previously fetched the `Contacto` model via `.get()` for every distinct contact identity, causing severe O(N) query inflation.
**Action:** Pre-calculate the unique contact identities needed, bulk-fetch the models using `Contacto.objects.in_bulk(ids, field_name='identidad')`, and perform O(1) dictionary lookups during the aggregation loop.
