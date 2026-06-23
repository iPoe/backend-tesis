## 2024-06-23 - Avoid N+1 in statistics ViewSet
**Learning:** In `statistics` method of `CampaignViewSet`, iterating over `resultados` to fetch related `Contacto` entities individually using `Contacto.objects.get()` creates an N+1 query problem, heavily degrading performance when a campaign has many results.
**Action:** Use `.in_bulk()` or a dictionary pre-fetching approach to retrieve all distinct `Contacto` instances in one query, then access them via an in-memory dictionary during iteration.

## 2024-06-23 - Optimize Bulk Insert in Serializers
**Learning:** `ContactosSerializer` initialized with `many=True` relies on standard iteration that loops through `validated_data` and executes `Contacto.objects.update_or_create(...)` individually.
**Action:** Override `ListSerializer.create` in a list serializer class to use PostgreSQL native `bulk_create(update_conflicts=True)` instead of iterative `update_or_create` to prevent database bottlenecks.
