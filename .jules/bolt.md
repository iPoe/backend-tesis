## 2024-05-18 - DRF Bulk Creation Performance Issue
**Learning:** When using Django Rest Framework (DRF) to initialize serializers with `many=True`, calling `.save()` falls back to iterating over the list and calling the child serializer's `update_or_create` or `create` repeatedly. This leads to severe N+1 query problems.
**Action:** Always define a custom `ListSerializer` for bulk creation/updates, overriding its `create` method to use PostgreSQL's native `bulk_create(update_conflicts=True)` feature, and assign it to the child serializer's `Meta.list_serializer_class`.
