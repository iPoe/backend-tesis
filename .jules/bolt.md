
## 2024-06-21 - DRF ListSerializer N+1 Bottleneck for Bulk Upserts
**Learning:** When using a Django REST Framework ModelSerializer (like `ContactosSerializer`) initialized with `many=True`, calling `.save()` runs a loop that calls the child's `create()` method. If the child's `create()` method relies on `update_or_create()`, it generates up to 6 database queries per object, causing severe N+1 problems during bulk API endpoint requests.
**Action:** Always override `serializers.ListSerializer`'s `create()` method by defining a custom `ListSerializer` subclass, configuring it via `list_serializer_class` in the child's `Meta`, and using PostgreSQL's native `bulk_create(..., update_conflicts=True)` feature to complete the bulk insertion/update in a single query transaction.
