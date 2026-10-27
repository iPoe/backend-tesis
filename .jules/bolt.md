
## 2023-10-27 - N+1 bottleneck in WhatsApp Replies
**Learning:** Using list comprehensions to check related models mapped through multiple `.estado` associations inside `contactosxcampa` creates profound N+1 queries. Further, performing query `.filter().update()` iteratively inside loops exacerbates DB bottlenecks.
**Action:** Eager load related fields beforehand using `.select_related()`, and use single bulk queries with combined `Q()` objects to eliminate iterative operations inside loops.
