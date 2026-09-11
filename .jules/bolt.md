## 2024-05-18 - Optimized N+1 Query in DRF ViewSet loop
**Learning:** Inside `CampaignViewSet.list`, serializing related objects one-by-one inside a `for x in data:` loop creates an N+1 query problem, taking O(N) database calls.
**Action:** Bulk fetch the related items using `.filter(campania_id__in=campania_ids).select_related(...)` and group them via `defaultdict(list)` before the loop, achieving O(1) in-memory lookup. Add explicit `if not campania_ids: return Response(data)` to prevent empty `__in=[]` filter queries.
