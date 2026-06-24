## 2024-05-19 - Bulk Create with `update_conflicts=True`
**Learning:** Using `.update_or_create()` iteratively inside DRF's default create/update behavior for serializers instantiated with `many=True` causes huge N+1 queries during bulk operations (N selects, N inserts/updates).
**Action:** Always write a custom `ListSerializer.create` when handling mass payload insertions, using PostgreSQL's native `.bulk_create(update_conflicts=True)` with `unique_fields` and `update_fields` to turn N+1 queries into a single database hit.
