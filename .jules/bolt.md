
## 2024-05-23 - Safer DRF bulk fetching
**Learning:** Returning early on empty `campania_ids` bypasses potential post-loop logic. Using a strict `mxc.campania_id_id` can cause `AttributeError` if the foreign key field naming isn't explicitly known.
**Action:** Use an `if campania_ids:` block to contain the query instead of an early return. Extract grouping attributes safely using `getattr(mxc, 'campania_id_id', getattr(mxc, 'campania_id', None))` to support both explicit `_id` naming and conventional django naming.
