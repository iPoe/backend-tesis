## 2024-09-30 - N+1 Query in DRF List View
**Learning:** Using a loop over `serializer.data` and making a separate query for each element in DRF views causes significant N+1 problems (O(N) queries).
**Action:** Always bulk-fetch related models mapping them in memory by ID using `defaultdict` and `.select_related()` to achieve O(1) database queries when serializing lists.
