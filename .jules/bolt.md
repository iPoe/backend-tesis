## 2023-10-21 - Fix N+1 query in DRF list actions
**Learning:** DRF list endpoints that query related objects sequentially inside a Python loop can cause severe N+1 bottlenecks.
**Action:** Extract instance IDs from serialized data and perform a single `__in` query using `.select_related()`, then map them via `collections.defaultdict` in memory.
