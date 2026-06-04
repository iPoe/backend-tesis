## 2024-06-03 - N+1 Insertions in Django REST Framework
**Learning:** Initializing DRF's built-in serializers with `many=True` for bulk creation issues individual `update_or_create` calls, causing a massive N+1 query problem during bulk saves.
**Action:** Always override `ListSerializer.create` and use PostgreSQL's native `bulk_create(update_conflicts=True)` or `bulk_create()` whenever processing bulk data lists using DRF.
