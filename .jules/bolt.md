## 2025-02-23 - Avoid re-fetching model instances in setup scripts
**Learning:** Found an N+1 query issue in `campaigns/setup.py` where a `Campania` object was being re-fetched from the database inside a list comprehension for bulk creation, even though the instance was already available in memory.
**Action:** Use already instantiated model objects and IDs in loops and bulk operations instead of performing redundant `.objects.get()` calls.
