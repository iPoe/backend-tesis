## 2024-05-18 - Bulk Create Update Conflicts in Django Rest Framework
**Learning:** Overriding `ListSerializer.create` when multiple records are created dynamically to bypass DRF's default iterative `update_or_create` loop avoids massive database query bottleneck issues.
**Action:** Always provide a custom `ListSerializer` for nested serializers with `many=True` and utilize PostgreSQL's native `bulk_create` feature, especially when relying on uniqueness constraints that trigger updates using `update_conflicts=True`.
