## 2025-02-23 - Dictionary Unpacking in ListSerializer.create

**Learning:** When using DRF's `ListSerializer` to perform bulk insertions with `update_conflicts=True`, instantiating model objects with explicit dictionary keys (e.g., `item['email']`) is dangerous because `validated_data` omits keys for optional fields not provided in the request payload, causing 500 errors via `KeyError`.

**Action:** Always use dictionary unpacking (e.g., `Contacto(**item)`) when instantiating model objects from DRF `validated_data` to ensure resilience against missing optional fields.
