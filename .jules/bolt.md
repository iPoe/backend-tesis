## 2024-06-12 - [Optimize Django Rest Framework Bulk Insertions]
**Learning:** Overriding DRF's default iterative `update_or_create` calls in `ListSerializer.create` using PostgreSQL's native `bulk_create(update_conflicts=True)` dramatically resolves N+1 query problems. In bulk operations, this drops database trips per item to a single query.
**Action:** When implementing DRF bulk insertion endpoints, always override the parent `ListSerializer.create` to execute an upsert with `bulk_create` rather than looping over individual creations.
