## 2024-05-26 - Django DRF Bulk Insertion Performance Bottleneck
**Learning:** When dealing with DRF bulk insertions (like `ContactosSerializer` initialized with `many=True`), relying on the child serializer's iterative `update_or_create` calls results in severe N+1 database performance bottlenecks.
**Action:** Always override `ListSerializer.create` to use PostgreSQL's native `bulk_create(update_conflicts=True)` instead of relying on the child serializer's iterative `update_or_create` calls to avoid N+1 queries.
