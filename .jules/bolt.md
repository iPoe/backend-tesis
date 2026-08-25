## 2024-05-24 - Bypass redundant ORM queries for known Foreign Keys
**Learning:** When foreign key IDs are already known during serializer create operations, using `Model.objects.get()` performs an unnecessary `SELECT` query.
**Action:** Assign the known integer ID directly to the underlying `_id` attribute (e.g. `estado_id=1` or `campania_id_id=idcam`) to bypass the redundant fetch.
## 2024-05-24 - Do not bypass implicit DRF validation
**Learning:** When attempting to optimize foreign key assignments in DRF serializers by bypassing `Model.objects.get()` and assigning IDs directly (e.g. `estado_id=1`), it removes implicit DRF validation. If the ID is invalid, it causes a hard `IntegrityError` instead of a graceful 404.
**Action:** Do not bypass `.get()` in DRF serializers when the model instance is used for validation. Look for redundant queries elsewhere, such as in business logic where the object is already in memory.
