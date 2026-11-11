## 2024-05-19 - In-memory mapped grouping for DRF serialization
**Learning:** Optimizing DRF list serialization loops requires fetching related objects in bulk, then grouping them in-memory using `collections.defaultdict` mapped by the underlying integer ForeignKey attribute (e.g., `campania_id_id`) to avoid an N+1 query for each serialized item. Also, passing a list directly to `__in=` in Django handles instances correctly.
**Action:** Always pre-fetch IDs from serialized data, bulk fetch with `__in=`, and map by relation ID rather than looping querysets inside DRF loops.
