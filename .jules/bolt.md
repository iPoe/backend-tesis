## 2024-05-24 - DRF N+1 Bulk Update/Insert Bottleneck
**Learning:** Initializing DRF ModelSerializers with `many=True` causes severe N+1 database performance bottlenecks when dealing with bulk updates/inserts because it iterates and calls `save` or `update_or_create` on each individual object.
**Action:** Always override `ListSerializer.create` when working with `many=True` to use Django's native `bulk_create` combined with PostgreSQL's `update_conflicts=True` to significantly speed up bulk updates and insertions in DRF.
