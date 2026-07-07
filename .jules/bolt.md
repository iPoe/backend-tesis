
## 2024-07-07 - Fix DRF ListSerializer N+1 Instantiation
**Learning:** DRF's default implementation of `many=True` runs standard `create` (which may trigger `update_or_create`) iteratively for every single item, causing severe N+1 SQL queries. The exact impact measured was 6 queries per item (600 queries per 100 insertions).
**Action:** Always override `ListSerializer.create` when handling large batch inserts through DRF, utilizing PostgreSQL's native `bulk_create(update_conflicts=True)` functionality to reduce the complexity back to O(1).
