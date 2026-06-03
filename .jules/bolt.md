## 2024-06-03 - DRF Bulk Insertion N+1 Bottleneck
**Learning:** DRF's default ListSerializer iteration causes severe N+1 database performance bottlenecks when `many=True` is used for creating nested items. Specifically, `ContactosSerializer` relies on an iterative `update_or_create` leading to N queries.
**Action:** Override `ListSerializer.create` to use PostgreSQL's native `bulk_create(update_conflicts=True)` whenever performing bulk insertions to reduce database calls to a single query.
