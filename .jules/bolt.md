## 2024-08-19 - N+1 Query in Django List Comprehension and Bulk Update

**Learning:** When generating a list of related instances from an evaluated QuerySet inside a loop or comprehension (e.g., `[c.campania for c in campañas_usuaria]`), it creates an N+1 query problem unless `.select_related()` or `.prefetch_related()` is explicitly used on the initial QuerySet. Also, when iteratively updating multiple rows in a loop (`_cambiar_estado_bulk`), generating individual update statements causes an N query overhead.

**Action:** Fix the list comprehension N+1 by chaining `.select_related()` (e.g., `.select_related('campania', 'campania__estado')`). Replace the loop of `.update()` calls with a single `.filter(Q(...)).update(...)` statement by combining the filtering criteria using Django's `Q` objects. Make sure to check `if not result:` before executing an empty `Q` object to prevent unintentionally updating the entire table.
