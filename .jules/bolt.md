## 2024-05-25 - Fix N+1 Query in CampaignViewSet List

**Learning:** When using DRF ViewSets with nested data constructed manually (like appending related instances to a dictionary after the main query), it can trigger catastrophic N+1 database queries. A seemingly innocent query inside a loop like `mediosxcampania.objects.filter(campania_id=x['id'])` runs one database query per item returned by the parent queryset. Additionally, accessing nested foreign keys during serialization (`source='medio_id.tipo_medio'`) triggers secondary N+1 queries if those relations aren't pre-fetched.

**Action:** To resolve Django N+1 query problems within loops over serialized data, bulk fetch related instances using `.filter(id__in=ids)` before the loop and construct an in-memory dictionary (using `defaultdict(list)`) for O(1) lookups. Always chain `.select_related()` or `.prefetch_related()` for any nested fields accessed by the serializer to avoid secondary N+1 queries during serialization.
