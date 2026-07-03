## 2024-07-03 - Bulk Insert Optimization in Django Rest Framework
**Learning:** DRF's default behavior for multiple object creation invokes the child serializer's `create` method iteratively, leading to severe N+1 database performance bottlenecks (e.g., executing `update_or_create` on every single item in a large array).
**Action:** Always override `ListSerializer.create` when dealing with large payloads containing `many=True` to use PostgreSQL's native `bulk_create(update_conflicts=True)`, minimizing database round trips.
