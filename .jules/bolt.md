## 2025-02-23 - DRF list N+1 Optimization
**Learning:** In Django Rest Framework, when augmenting serialized list data using relations, executing a separate `.filter()` query inside a `for x in data:` loop introduces an N+1 query bottleneck.
**Action:** When serializing collections, always extract the primary keys first (`[x['id'] for x in data]`), perform a single bulk fetch using `__in=ids`, and group the related objects in Python memory using `collections.defaultdict` mapped to the ID before appending the related data to each item.
