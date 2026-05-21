## 2025-03-09 - DRF Bulk Inserts and PostgreSQL update_conflicts
**Learning:** In DRF, standard serializers initialized with `many=True` lead to catastrophic N+1 database operations because they iteratively call `update_or_create` for each child item. This is extremely slow for bulk data ingests.
**Action:** Always implement a custom `ListSerializer` using PostgreSQL's native `bulk_create(update_conflicts=True)` instead. When doing this, explicitly disable standard uniqueness validators in the child serializer and let the database act as the conflict resolver via `unique_fields`.
