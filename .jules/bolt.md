
## 2024-05-24 - N+1 Query in Django Serialization Loops
**Learning:** In Django DRF viewsets, performing an `objects.get()` lookup inside a loop over serialized data (like in `campaigns/viewsets.py`'s `statistics` method) leads to severe N+1 query problems. For 50 contacts, it executed 58 queries.
**Action:** Always extract the unique IDs from the list, perform a single `.filter(id__in=ids)` query beforehand, and build a dictionary mapping for O(1) in-memory lookups. This drops queries to O(1) relative to the number of items.
