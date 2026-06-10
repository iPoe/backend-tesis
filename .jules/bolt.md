
## 2024-05-24 - N+1 Query in Django Rest Framework Viewset Loop
**Learning:** Overriding DRF's `list` method to manually append related records (like `mediosxcampania` to `Campania`) within a `for x in data:` loop creates a severe N+1 query bottleneck. Secondary queries are generated when the nested serializer references a foreign key (`source='medio_id.tipo_medio'`).
**Action:** When appending related items to serialized data iteratively, prefetch all related objects outside the loop using `.filter(parent_id__in=parent_ids).select_related(...)` and map them in-memory using a `defaultdict` to ensure an O(1) constant number of queries regardless of record count.
