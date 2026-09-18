## 2025-02-20 - N+1 query problem during DRF list serialization
**Learning:** Serializing list views without prefetching related models in Django Rest Framework can easily cause an N+1 database query problem.
**Action:** Optimize DRF list serialization by bulk fetching related objects into an in-memory map based on `serializer.data` IDs (e.g., `campania_ids = [x['id'] for x in data]`). Explicitly handle the case where the serialized dataset is empty (e.g., `if not campania_ids: return Response(data)`) to prevent executing unnecessary database queries with an empty `__in=[]` filter.
