## 2024-05-24 - Bulk Creating DRF Serializers
**Learning:** Overriding `ListSerializer.create` using `bulk_create` significantly improves performance by reducing N+1 queries during data insertion, particularly when `many=True` is used.
**Action:** Always optimize bulk data creation by creating models directly with `bulk_create` (and setting `update_conflicts=True` to replicate `update_or_create` logic when necessary), bypassing default iterative updates.
