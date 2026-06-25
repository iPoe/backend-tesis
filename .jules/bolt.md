## 2026-06-25 - [Bulk Create Override Fixes N+1 Query Problem in Serializers]
**Learning:** DRF's default implementation for saving nested or multiple elements iteratively calls `update_or_create` and `save`, leading to massive N+1 issues when ingesting bulk data.
**Action:** Overrode `ListSerializer.create` for `ContactosSerializer` to use `Contacto.objects.bulk_create(..., update_conflicts=True)` which bypasses individual ORM round trips.
