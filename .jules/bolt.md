## 2024-05-10 - [Bulk Insert Optimization]
**Learning:** Using `update_or_create` inside a `create` loop of a DRF Serializer with `many=True` causes the N+1 problem. Overriding `ListSerializer.create` and using `bulk_create` natively with `update_conflicts=True` speeds up insertion by bypassing `update_or_create` loop in PostgreSQL!
**Action:** Identify any ModelSerializer handling bulk inserts and override its `ListSerializer` to use `bulk_create(update_conflicts=True)` instead of iterative `.save()`.
