
## 2024-07-09 - [Optimizing Bulk Inserts in DRF with ListSerializer]
**Learning:** DRF’s `many=True` flag iteratively calls `.create()` or `.update_or_create()` on each child item, causing severe N+1 database performance bottlenecks (e.g. 600 queries for 100 items).
**Action:** Always override `ListSerializer.create()` when dealing with bulk insertions. Utilizing PostgreSQL's native `bulk_create` along with `update_conflicts=True` effectively performs an upsert and radically cuts queries down (e.g., from 600 to 3) while handling uniqueness validations natively.
