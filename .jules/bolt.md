## 2025-02-28 - Optimize Redundant ORM Get Queries
**Learning:** Instantiating models directly in list comprehensions without considering that the object is already loaded into memory results in severe N+1 problems. In `setup.py` the `Campania` instance is re-fetched for every `contactosxcampa` creation despite already being stored in `campania`.
**Action:** Always reuse the in-memory object instance across related object initializations to bypass redundant `.get()` queries.
