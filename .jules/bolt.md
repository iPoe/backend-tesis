## 2026-08-28 - Avoid N+1 queries inside bulk creation loops
**Learning:** In Django, when preparing instances for `bulk_create` using list comprehensions, querying the database inside the comprehension (e.g., `Campania.objects.get(pk=campania.id)`) causes an N+1 query bottleneck, executing O(N) redundant queries when the instance is already in memory.
**Action:** Always reuse the already-fetched or newly-created model instance (e.g., `campania = campania`) directly when instantiating related objects within loops or comprehensions.
