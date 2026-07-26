## 2024-05-30 - N+1 Insert Optimization
**Learning:** In Django tasks processing bulk messages (like `enviarWhatsapp`), iterating over users and calling `.save()` on newly instantiated log models creates an N+1 insertion problem.
**Action:** Always refactor such loops to prepare a list of objects in memory and execute a single `.bulk_create()` operation, which returns the inserted objects with their populated PKs (when using PostgreSQL) allowing us to pair them with original inputs using `zip()` if needed.
## 2024-05-30 - N+1 Query in Django ViewSet loops
**Learning:** Using `.get()` inside a `for` loop (like `Contacto.objects.get(identidad=contacantiguo)` while iterating over statistics results) causes severe N+1 query performance degradation.
**Action:** Extract unique identifiers from the results beforehand, bulk fetch related instances using `.in_bulk(id_list)` mapped by their unique field, and use the resulting dictionary for fast O(1) in-memory lookups during the loop iteration.
