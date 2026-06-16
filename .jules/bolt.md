## 2024-06-16 - Prevent N+1 issues in bulk inserts via ListSerializer

**Learning:** When dealing with Django REST Framework bulk insertions (such as `ContactosSerializer` initialized with `many=True`), relying on the default child serializer's `update_or_create` behavior triggers a severe N+1 query performance bottleneck. It initiates iterative database requests for each element.

**Action:** Override `ListSerializer.create` and construct Django model instances directly (e.g., `[Contacto(**item) for item in validated_data]`). Follow this up by calling PostgreSQL's native `bulk_create(update_conflicts=True, unique_fields=[...], update_fields=[...])` to securely bulk upsert and handle database conflicts efficiently without 500 errors. Note that when applying this, ensure DRF uniqueness validators are appropriately disabled (`validators: []`) for the primary key on the model level so the validations pass and flow directly into the conflict management of PostgreSQL.
