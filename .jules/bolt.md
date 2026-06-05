## 2025-06-05 - Optimize N+1 queries in viewset statistics
**Learning:** N+1 query bottlenecks often occur when looking up related instances inside a loop (like iterating through database query results and making a DB fetch `.get()` inside the loop for serialization).
**Action:** When looping over query results that require related objects, bulk fetch related instances using `.filter(id__in=ids)` before the loop and construct an in-memory dictionary for O(1) lookups to avoid secondary N+1 queries.
