
## 2024-05-24 - DRF Bulk Insertions N+1 Bottleneck
**Learning:** By default, initializing a Django REST Framework serializer with `many=True` causes the `.save()` operation to iterate over the validated data list and execute an individual `INSERT` query (or `update_or_create`) for *every single item*. In the `ContactosSerializer`, this caused a severe N+1 database write problem.
**Action:** Always inspect bulk insertion paths in DRF. Override `ListSerializer.create` and map it in the child serializer's `Meta` class using `list_serializer_class` to leverage Django's native `bulk_create(update_conflicts=True)` instead. This reduces 100 queries to 1 query and acts natively as an upsert, significantly improving backend performance.
