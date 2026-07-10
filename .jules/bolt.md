
## 2024-07-10 - Dynamic Q objects for safe mass updating
**Learning:** When performing updates on heterogeneous pairings (e.g. tracking specific (campaign_id, medio_id) tuples), using a `.filter()` on an empty list constructing `Q` objects can mistakenly apply `.update()` across the whole table. Also, `Q` object composition using `|=` efficiently combines multi-column foreign key matching avoiding N+1 loops, taking queries from O(N) down to a constant O(1).
**Action:** Always check `if q_objects:` or similar logic to verify the generated search condition before calling `.update()`, and use iterative `Q` objects for batch updates across multiple criteria.
