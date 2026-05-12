## 2024-05-12 - N+1 query in DRF bulk creates using update_or_create
**Learning:** DRF's default bulk creation fallback loops over objects and repeatedly queries/inserts (`update_or_create`). This causes a huge performance bottleneck (N+1 database calls) for large dataset ingestion like bulk contact uploads.
**Action:** Always create a custom `ListSerializer` and override the `create()` method. Use Postgres's native `bulk_create(update_conflicts=True)` feature to condense the N queries into a single database operation.
