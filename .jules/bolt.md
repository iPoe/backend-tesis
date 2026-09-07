## 2024-05-14 - Direct Dictionary Access in DRF Serializers
**Learning:** Overriding DRF's `.create()` with `**item` kwargs is necessary to safely unpack a `validated_data` dictionary. Accessing optional dictionary fields via standard indexing (`item['key']`) is unsafe and will result in `KeyError` crashes when requests omit optional fields.
**Action:** When handling DRF dictionaries in optimizations like `bulk_create()`, always use safe `.get('key')` semantics or pass unpacked kwargs via `**item` for models.
