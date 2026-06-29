## 2024-05-24 - [Fix N+1 query on DRF Bulk Inserts]
**Learning:** Overriding `ListSerializer.create` and utilizing PostgreSQL's native `bulk_create(update_conflicts=True)` drastically reduces the massive overhead (N+1 queries) when repeatedly calling `update_or_create` on child serializers inside large lists.
**Action:** Always check if a Django REST framework serializer initialized with `many=True` handles bulk insertions efficiently. Replace default iteration with native DB operations where possible for a huge performance win.
