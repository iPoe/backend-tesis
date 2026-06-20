
## 2024-05-18 - DRF Bulk Creation Performance with Nested ListSerializer
**Learning:** Overriding DRF's `ListSerializer.create` method to use PostgreSQL's native `bulk_create` (with `update_conflicts=True`) dramatically reduces query counts during batch insertion. Relying on default iterative child serializer calls creates an N+1 query situation.
**Action:** When working with serializers used in bulk (`many=True`), specifically when the underlying database supports efficient bulk creation/upsert, implement a nested `ListSerializer` subclass to utilize the database's `bulk_create` feature over standard iterative save.
