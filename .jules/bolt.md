## 2024-06-26 - Fix N+1 Query in List Endpoints
**Learning:** Returning nested related data within a Django viewset's `list` method often causes an N+1 query bottleneck if we perform iterative `.filter()` lookups inside the loop over the serializer data.
**Action:** Always batch-fetch related objects using `.filter(foreign_key__in=ids)` (with `select_related`/`prefetch_related` as needed), and group them in memory using `collections.defaultdict(list)` before iterating through the main serialized list to dramatically reduce DB queries.
