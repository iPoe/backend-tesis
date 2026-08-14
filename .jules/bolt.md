## 2025-02-23 - Django N+1 query in loop
**Learning:** Calling `Model.objects.get()` inside a loop to fetch related objects based on IDs gathered from another query introduces a severe N+1 problem.
**Action:** Always pre-fetch related records using `.in_bulk()` with a collected list of IDs before iterating, reducing O(N) database calls to O(1).
