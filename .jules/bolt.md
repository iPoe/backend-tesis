## 2024-05-13 - Test run
**Learning:** Checking things out
**Action:** Let's look for performance bottlenecks.
## 2024-05-13 - N+1 optimization and bypass redundant `.get()` queries
**Learning:** Found redundant DB calls that were using `.get(pk=ID)` where ID was already known. Replaced `.get(pk=ID)` inside the `resultados` creation with directly mapping the foreign keys `_id` like `campania_id_id=ID`. Also added `.select_related()` correctly, and learned that replacing `.get()` with `.filter().first()` ruins proper error handling. Always use `.get()` to properly throw `DoesNotExist` exception.
**Action:** Use `campania_id_id=ID` to directly assign known IDs in `bulk_create` objects without traversing to trigger `.get()` and N+1. Keep `.get()` intact for object lookups when you expect an explicit error handling logic.
