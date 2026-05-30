## 2024-05-30 - N+1 Query in Django Rest Framework ListSerializer

**Learning:** When a ViewSet's `list` method iterates over serialized data (e.g., `for x in data:`) and makes database queries per item (like `mediosxcampania.objects.filter(campania_id=x['id'])`), it creates an N+1 query performance bottleneck. Additionally, if the child serializer accesses nested fields via its source attribute (like `source='medio_id.tipo_medio'`), that will trigger further N+1 queries.

**Action:** Solve N+1 problems in List views by extracting all IDs from the parent dataset, performing a single `.filter(id__in=ids)` query, and grouping the results in memory using `collections.defaultdict`. Always chain `.select_related()` (or `.prefetch_related()`) to batch-fetch any nested fields accessed by child serializers.
