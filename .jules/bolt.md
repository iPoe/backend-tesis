## 2024-05-18 - Optimize CampaignViewSet.list N+1 issue
**Learning:** In Django DRF viewsets, iterating over serialized list items and performing ORM `.filter()` lookups creates severe N+1 database queries.
**Action:** When a method loops over `serializer.data` and executes queries based on item keys, extract the IDs first and use a single `.filter(id__in=ids)` to fetch all related items, map them using `collections.defaultdict(list)`, and append to the serialized items in O(1) time. Ensure you add `select_related()` for any deep relationships accessed in the sub-serializer.
