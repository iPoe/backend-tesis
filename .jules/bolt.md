## 2024-05-08 - Optimize Bulk Insertions with PostgreSQL bulk_create
**Learning:** DRF `ListSerializer` default iteration over child elements triggers an N+1 queries issue where `update_or_create` is executed per item when saving many objects. PostgreSQL supports `bulk_create` with `update_conflicts=True`, which can drastically speed up batch operations.
**Action:** Override `ListSerializer.create` when doing bulk operations to use `bulk_create(update_conflicts=True)` instead of the default iterative save process.
