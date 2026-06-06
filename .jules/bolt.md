## 2024-06-06 - Optimized Bulk Insertion of Contactos
**Learning:** DRF’s standard ModelSerializer does not support efficient bulk insertion natively; when `many=True` is provided to `ContactosSerializer`, DRF iterates over the array calling `update_or_create` individually, leading to an N+1 queries performance bottleneck.
**Action:** Always override `serializers.ListSerializer.create` utilizing `Django`'s `bulk_create` (especially with `update_conflicts=True` to support upserts matching `update_or_create`) and define it within the target serializer’s `Meta.list_serializer_class`.
