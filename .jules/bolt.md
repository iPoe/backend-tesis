## 2024-08-08 - Optimized ContactosSerializer Bulk Insert
**Learning:** Overriding `ListSerializer.create` and utilizing `bulk_create(update_conflicts=True)` drastically reduces query count when inserting or updating multiple entries, resolving an N+1 query problem where `update_or_create` was being called inside a loop.
**Action:** Always prefer `bulk_create(update_conflicts=True)` instead of `update_or_create` in loops for efficient database operations in Django when the database supports it (e.g. PostgreSQL, SQLite 3.24+).
