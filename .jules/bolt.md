## 2024-05-18 - Bulk Create with Update Conflicts in Django Serializers
**Learning:** Serializing large lists using default `ModelSerializer.create` combined with `update_or_create` causes severe N+1 query bottlenecks during imports.
**Action:** Implement a custom `ListSerializer` using Django's `bulk_create(update_conflicts=True)` and explicitly deduplicate Python data before insertion to handle unique constraints efficiently without throwing `IntegrityError`s.
