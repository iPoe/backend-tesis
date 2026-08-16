## 2025-05-23 - Prevent N+1 queries in loop list comprehensions
**Learning:** In `campaigns/tasks.py`, list comprehensions extracting attributes from foreign keys (e.g., `[obj.contacto.celular for obj in cons]`) trigger N+1 queries if the relation was not fetched with `.select_related()`.
**Action:** Always eagerly load related foreign keys accessed within loops or list comprehensions using `.select_related()` (or `.prefetch_related()` for many-to-many) when querying the base objects.
